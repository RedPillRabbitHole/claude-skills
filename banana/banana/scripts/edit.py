#!/usr/bin/env python3
"""Fallback image editing via Gemini REST API (no MCP dependency)."""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
OUTPUT_DIR = Path.home() / "Documents" / "nanobanana_generated"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


def get_api_key(args):
    key = args.api_key or os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print(json.dumps({"error": "No API key found. Set GOOGLE_AI_API_KEY or use --api-key."}))
        sys.exit(1)
    return key


def edit_image(args):
    api_key = get_api_key(args)
    model = args.model or DEFAULT_MODEL

    image_path = Path(args.image)
    if not image_path.exists():
        print(json.dumps({"error": f"Image not found: {args.image}"}))
        sys.exit(1)

    suffix = image_path.suffix.lower()
    mime_type = MIME_TYPES.get(suffix, "image/png")
    image_b64 = base64.b64encode(image_path.read_bytes()).decode()

    body = {
        "contents": [{
            "parts": [
                {"text": args.prompt},
                {"inlineData": {"mimeType": mime_type, "data": image_b64}},
            ]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        },
    }

    url = f"{API_BASE}/{model}:generateContent?key={api_key}"
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
                break
        except urllib.error.HTTPError as e:
            body_text = e.read().decode()
            if e.code == 429:
                wait = 2 ** attempt * 2
                print(f"Rate limited. Waiting {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            if e.code == 400 and "FAILED_PRECONDITION" in body_text:
                print(json.dumps({"error": "Billing not enabled. Visit console.cloud.google.com to enable billing."}))
                sys.exit(1)
            print(json.dumps({"error": f"HTTP {e.code}: {body_text}"}))
            sys.exit(1)
    else:
        print(json.dumps({"error": "Max retries exceeded (rate limited)."}))
        sys.exit(1)

    candidates = result.get("candidates", [])
    if not candidates:
        print(json.dumps({"error": "No candidates returned.", "raw": result}))
        sys.exit(1)

    candidate = candidates[0]
    finish_reason = candidate.get("finishReason", "")
    if finish_reason in ("IMAGE_SAFETY", "PROHIBITED_CONTENT", "SAFETY"):
        print(json.dumps({"error": f"Edit blocked: {finish_reason}", "finish_reason": finish_reason}))
        sys.exit(1)

    image_data = None
    text_response = None
    for part in candidate.get("content", {}).get("parts", []):
        if "inlineData" in part:
            image_data = part["inlineData"]["data"]
        elif "text" in part:
            text_response = part["text"]

    if not image_data:
        print(json.dumps({"error": "No edited image in response.", "raw": result}))
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"edited_{timestamp}.png"
    output_path.write_bytes(base64.b64decode(image_data))

    print(json.dumps({
        "success": True,
        "file_path": str(output_path),
        "original": str(image_path),
        "model": model,
        "text": text_response,
    }))


def main():
    parser = argparse.ArgumentParser(description="Edit image via Gemini API")
    parser.add_argument("--image", required=True, help="Path to source image")
    parser.add_argument("--prompt", required=True, help="Editing instructions")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model ID")
    parser.add_argument("--api-key", help="Google AI API key")
    args = parser.parse_args()
    edit_image(args)


if __name__ == "__main__":
    main()
