#!/usr/bin/env python3
"""CSV batch workflow processor for Banana Claude."""

import argparse
import csv
import json
import sys
from pathlib import Path

DEFAULT_RATIO = "1:1"
DEFAULT_RESOLUTION = "1K"
DEFAULT_MODEL = "gemini-3.1-flash-image-preview"

PRICING = {
    "gemini-3.1-flash-image-preview": {"512": 0.020, "1K": 0.039, "2K": 0.078, "4K": 0.156},
    "gemini-2.5-flash-image": {"512": 0.020, "1K": 0.039, "2K": 0.078, "4K": 0.156},
}


def estimate_cost(model, resolution):
    model_pricing = PRICING.get(model, PRICING[DEFAULT_MODEL])
    return model_pricing.get(resolution, model_pricing[DEFAULT_RESOLUTION])


def main():
    parser = argparse.ArgumentParser(description="CSV batch image generation planner")
    parser.add_argument("--csv", required=True, help="Path to CSV file")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(json.dumps({"error": f"CSV file not found: {args.csv}"}))
        sys.exit(1)

    rows = []
    errors = []

    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=2):
                prompt = row.get("prompt", "").strip()
                if not prompt:
                    errors.append(f"Row {i}: missing 'prompt' field")
                    continue
                rows.append({
                    "prompt": prompt,
                    "ratio": row.get("ratio", DEFAULT_RATIO).strip() or DEFAULT_RATIO,
                    "resolution": row.get("resolution", DEFAULT_RESOLUTION).strip() or DEFAULT_RESOLUTION,
                    "model": row.get("model", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
                    "preset": row.get("preset", "").strip(),
                })
    except (csv.Error, UnicodeDecodeError) as e:
        print(json.dumps({"error": f"CSV parse error: {e}"}))
        sys.exit(1)

    if not rows:
        print(json.dumps({"error": "No valid rows found in CSV.", "validation_errors": errors}))
        sys.exit(1)

    total_cost = sum(estimate_cost(r["model"], r["resolution"]) for r in rows)
    batch_cost = total_cost * 0.5

    print(json.dumps({
        "rows": rows,
        "count": len(rows),
        "estimated_cost": round(total_cost, 4),
        "estimated_cost_batch": round(batch_cost, 4),
        "validation_errors": errors,
    }, indent=2))


if __name__ == "__main__":
    main()
