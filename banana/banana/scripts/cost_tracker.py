#!/usr/bin/env python3
"""Cost tracking for Banana Claude image generation."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

LEDGER_PATH = Path.home() / ".banana" / "costs.json"

PRICING = {
    "gemini-3.1-flash-image-preview": {"512": 0.020, "1K": 0.039, "2K": 0.078, "4K": 0.156},
    "gemini-2.5-flash-image": {"512": 0.020, "1K": 0.039, "2K": 0.078, "4K": 0.156},
}
DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_RESOLUTION = "1K"


def _load_ledger():
    if not LEDGER_PATH.exists():
        return {"total_cost": 0.0, "total_images": 0, "entries": [], "daily": {}}
    try:
        return json.loads(LEDGER_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {"total_cost": 0.0, "total_images": 0, "entries": [], "daily": {}}


def _save_ledger(ledger):
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2))


def _lookup_cost(model, resolution, batch=False):
    model_key = model
    if model_key not in PRICING:
        model_key = DEFAULT_MODEL
    res_key = resolution if resolution in PRICING[model_key] else DEFAULT_RESOLUTION
    cost = PRICING[model_key][res_key]
    return cost * 0.5 if batch else cost


def cmd_log(args):
    ledger = _load_ledger()
    cost = _lookup_cost(args.model, args.resolution)
    today = datetime.now().strftime("%Y-%m-%d")
    entry = {
        "timestamp": datetime.now().isoformat(),
        "model": args.model,
        "resolution": args.resolution,
        "cost": cost,
        "prompt": args.prompt[:80] if args.prompt else "",
    }
    ledger["entries"].append(entry)
    ledger["total_cost"] = ledger.get("total_cost", 0.0) + cost
    ledger["total_images"] = ledger.get("total_images", 0) + 1
    daily = ledger.setdefault("daily", {})
    if today not in daily:
        daily[today] = {"cost": 0.0, "images": 0}
    daily[today]["cost"] += cost
    daily[today]["images"] += 1
    _save_ledger(ledger)
    print(f"Logged: ${cost:.3f} ({args.model} @ {args.resolution})")


def cmd_summary(args):
    ledger = _load_ledger()
    print(f"Total: ${ledger.get('total_cost', 0):.3f} across {ledger.get('total_images', 0)} images")
    print("\nLast 7 days:")
    daily = ledger.get("daily", {})
    for day in sorted(daily.keys())[-7:]:
        d = daily[day]
        print(f"  {day}: ${d['cost']:.3f} ({d['images']} images)")


def cmd_today(args):
    ledger = _load_ledger()
    today = datetime.now().strftime("%Y-%m-%d")
    d = ledger.get("daily", {}).get(today, {"cost": 0.0, "images": 0})
    print(f"Today ({today}): ${d['cost']:.3f} across {d['images']} images")


def cmd_estimate(args):
    cost_per = _lookup_cost(args.model, args.resolution)
    total = cost_per * args.count
    batch_total = cost_per * 0.5 * args.count
    print(f"Estimate for {args.count} images ({args.model} @ {args.resolution}):")
    print(f"  Standard: ${total:.3f}")
    print(f"  Batch API (50% off): ${batch_total:.3f}")


def cmd_reset(args):
    if not args.confirm:
        print("Use --confirm to reset the ledger.")
        return
    _save_ledger({"total_cost": 0.0, "total_images": 0, "entries": [], "daily": {}})
    print("Ledger reset.")


def main():
    parser = argparse.ArgumentParser(description="Cost tracker for Banana Claude")
    sub = parser.add_subparsers(dest="command")

    log_p = sub.add_parser("log", help="Log a generation")
    log_p.add_argument("--model", default=DEFAULT_MODEL)
    log_p.add_argument("--resolution", default=DEFAULT_RESOLUTION)
    log_p.add_argument("--prompt", default="")

    sub.add_parser("summary", help="Show total and last 7 days")
    sub.add_parser("today", help="Show today's usage")

    est_p = sub.add_parser("estimate", help="Estimate batch cost")
    est_p.add_argument("--model", default=DEFAULT_MODEL)
    est_p.add_argument("--resolution", default=DEFAULT_RESOLUTION)
    est_p.add_argument("--count", type=int, required=True)

    reset_p = sub.add_parser("reset", help="Clear ledger")
    reset_p.add_argument("--confirm", action="store_true")

    args = parser.parse_args()
    if args.command == "log":
        cmd_log(args)
    elif args.command == "summary":
        cmd_summary(args)
    elif args.command == "today":
        cmd_today(args)
    elif args.command == "estimate":
        cmd_estimate(args)
    elif args.command == "reset":
        cmd_reset(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
