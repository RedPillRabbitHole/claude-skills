#!/usr/bin/env python3
"""Manage brand/style presets for Banana Claude."""

import argparse
import json
import re
import sys
from pathlib import Path

PRESETS_DIR = Path.home() / ".banana" / "presets"


def _ensure_dir():
    PRESETS_DIR.mkdir(parents=True, exist_ok=True)


def _sanitize_name(name):
    return re.sub(r"[^a-zA-Z0-9_-]", "", name)


def _preset_path(name):
    return PRESETS_DIR / f"{_sanitize_name(name)}.json"


def _load_preset(name):
    path = _preset_path(name)
    if not path.exists():
        print(f"Preset '{name}' not found.", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text())


def cmd_list(args):
    _ensure_dir()
    presets = list(PRESETS_DIR.glob("*.json"))
    if not presets:
        print("No presets found. Create one with: presets.py create NAME")
        return
    for p in sorted(presets):
        try:
            data = json.loads(p.read_text())
            desc = data.get("description", "")
            print(f"  {p.stem}: {desc}")
        except (json.JSONDecodeError, OSError):
            print(f"  {p.stem}: (unreadable)")


def cmd_show(args):
    preset = _load_preset(args.name)
    print(json.dumps(preset, indent=2))


def cmd_create(args):
    _ensure_dir()
    name = _sanitize_name(args.name)
    if not name:
        print("Invalid preset name.", file=sys.stderr)
        sys.exit(1)

    preset = {
        "name": name,
        "description": args.description or "",
        "colors": [c.strip() for c in args.colors.split(",")] if args.colors else [],
        "style": args.style or "",
        "typography": args.typography or "",
        "lighting": args.lighting or "",
        "mood": args.mood or "",
        "default_ratio": args.ratio or "16:9",
        "default_resolution": args.resolution or "2K",
    }

    path = _preset_path(name)
    path.write_text(json.dumps(preset, indent=2))
    print(f"Preset '{name}' created at {path}")


def cmd_delete(args):
    if not args.confirm:
        print("Use --confirm to delete a preset.")
        return
    path = _preset_path(args.name)
    if not path.exists():
        print(f"Preset '{args.name}' not found.", file=sys.stderr)
        sys.exit(1)
    path.unlink()
    print(f"Preset '{args.name}' deleted.")


def main():
    parser = argparse.ArgumentParser(description="Manage Banana Claude presets")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List all presets")

    show_p = sub.add_parser("show", help="Show preset details")
    show_p.add_argument("name")

    create_p = sub.add_parser("create", help="Create a new preset")
    create_p.add_argument("name")
    create_p.add_argument("--description", default="")
    create_p.add_argument("--colors", help="Comma-separated hex colors")
    create_p.add_argument("--style", default="")
    create_p.add_argument("--typography", default="")
    create_p.add_argument("--lighting", default="")
    create_p.add_argument("--mood", default="")
    create_p.add_argument("--ratio", default="16:9")
    create_p.add_argument("--resolution", default="2K")

    delete_p = sub.add_parser("delete", help="Delete a preset")
    delete_p.add_argument("name")
    delete_p.add_argument("--confirm", action="store_true")

    args = parser.parse_args()
    if args.command == "list":
        cmd_list(args)
    elif args.command == "show":
        cmd_show(args)
    elif args.command == "create":
        cmd_create(args)
    elif args.command == "delete":
        cmd_delete(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
