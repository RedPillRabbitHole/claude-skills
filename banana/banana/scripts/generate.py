#!/usr/bin/env python3
"""Fallback image generation via Gemini REST API (no MCP dependency)."""

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
DEFAULT_RESOLUTION = "2K"
DEFAULT_RATIO = "1:1"
OUTPUT_DIR = Path.home() / "Documents" / "nanobanana_generated"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

VALID_RATIOS = ["1:1", "16:9", "9:16", "4:3", "3:4", "2:3", "3:2", "4:5", "5:4", "21:9", "1:4", "4:1", "1:8", "8:1"]
VALID_RESOLUTIONS = ["512", "1K", "2K", "4K"]


def get_api_key(args):
    key = args.api_key or os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print(json.dumps({"error": "No API key found. Set GOOGLE_AI_API_KEY or use --api-key."}))
        sys.exit(1)
    return key


def generate_image(args):
    api_key = get_api_key(args)
    model = args.model or DEFAULT_MODEL
    resolution = args.resolution or DEFAULT_RESOLUTION
    ratio = args.aspect_ratio or DEFAULT_RATIO

    if ratio not in VALID_RATIOS:
        print(json.dumps({"error": f"Invalid ratio '{ratio}'. Valid: {VALID_RATIOS}"}))
        sys.exit(1)
    if resolution not in VALID_RESOLUTIONS:
        print(json.dumps({"error": f"Invalid resolution '{resolution}'. Valid: {VALID_RESOLUTIONS}"}))
        sys.exit(1)

    generation_config = {
        "responseModalities": ["IMAGE"] if args.image_only else ["TEXT", "IMAGE"],
        "imageGenerationConfig": {
            "aspectRatio": ratio,
            "imageSize": resolution,
        },
    }

    if args.thinking:
        generation_config["thinkingConfig"] = {"thinkingLevel": args.thinking}

    body = {
        "contents": [{"parts": [{"text": args.prompt}]}],
        "generationConfig": generation_config,
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
        print(json.dumps({"error": f"Generation blocked: {finish_reason}", "finish_reason": finish_reason}))
        sys.exit(1)

    image_data = None
    text_response = None
    for part in candidate.get("content", {}).get("parts", []):
        if "inlineData" in part:
            image_data = part["inlineData"]["data"]
        elif "text" in part:
            text_response = part["text"]

    if not image_data:
        print(json.dumps({"error": "No image in response.", "raw": result}))
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"generated_{timestamp}.png"
    output_path.write_bytes(base64.b64decode(image_data))

    print(json.dumps({
        "success": True,
        "file_path": str(output_path),
        "model": model,
        "aspect_ratio": ratio,
        "resolution": resolution,
        "text": text_response,
    }))


def main():
    parser = argparse.ArgumentParser(description="Generate image via Gemini API")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--aspect-ratio", default=DEFAULT_RATIO, help="Aspect ratio")
    parser.add_argument("--resolution", default=DEFAULT_RESOLUTION, help="Resolution: 512, 1K, 2K, 4K")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model ID")
    parser.add_argument("--api-key", help="Google AI API key")
    parser.add_argument("--thinking", help="Thinking level: minimal, low, medium, high")
    parser.add_argument("--image-only", action="store_true", help="Return image only, no text")
    args = parser.parse_args()
    generate_image(args)


if __name__ == "__main__":
    main()
