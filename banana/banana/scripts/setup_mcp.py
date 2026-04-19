#!/usr/bin/env python3
"""Configure the nanobanana MCP server for Claude Code."""

import json
import os
import sys
from pathlib import Path

SETTINGS_FILE = Path.home() / ".claude" / "settings.json"
MCP_NAME = "nanobanana-mcp"
MCP_PACKAGE = "@ycse/nanobanana-mcp"
DEFAULT_MODEL = "gemini-3.1-flash-image-preview"


def load_settings():
    if not SETTINGS_FILE.exists():
        return {}
    try:
        return json.loads(SETTINGS_FILE.read_text())
    except json.JSONDecodeError:
        return {}


def save_settings(settings):
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(settings, indent=2))


def check_setup():
    settings = load_settings()
    mcp_servers = settings.get("mcpServers", {})
    if MCP_NAME in mcp_servers:
        cfg = mcp_servers[MCP_NAME]
        env = cfg.get("env", {})
        key = env.get("GOOGLE_AI_API_KEY", "")
        masked = key[:8] + "..." + key[-4:] if len(key) > 12 else "***"
        print(f"MCP server '{MCP_NAME}' is configured.")
        print(f"  Package: {MCP_PACKAGE}")
        print(f"  API key: {masked}")
        print(f"  Model: {env.get('NANOBANANA_MODEL', DEFAULT_MODEL)}")
    else:
        print(f"MCP server '{MCP_NAME}' is NOT configured.")
        print("Run: python3 setup_mcp.py --key YOUR_API_KEY")


def remove_mcp():
    settings = load_settings()
    mcp_servers = settings.get("mcpServers", {})
    if MCP_NAME in mcp_servers:
        del mcp_servers[MCP_NAME]
        settings["mcpServers"] = mcp_servers
        save_settings(settings)
        print(f"Removed MCP server '{MCP_NAME}'.")
    else:
        print(f"MCP server '{MCP_NAME}' was not configured.")


def setup_mcp(api_key):
    settings = load_settings()
    if "mcpServers" not in settings:
        settings["mcpServers"] = {}

    settings["mcpServers"][MCP_NAME] = {
        "command": "npx",
        "args": ["-y", MCP_PACKAGE],
        "env": {
            "GOOGLE_AI_API_KEY": api_key,
            "NANOBANANA_MODEL": DEFAULT_MODEL,
        },
    }

    save_settings(settings)
    output_dir = Path.home() / "Documents" / "nanobanana_generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"MCP server '{MCP_NAME}' configured successfully.")
    print(f"Output directory: {output_dir}")
    print("Restart Claude Code to apply changes.")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("Usage: setup_mcp.py [--key API_KEY] [--check] [--remove]")
        print("  --key KEY   Set Google AI API key")
        print("  --check     Show current configuration")
        print("  --remove    Remove MCP configuration")
        return

    if "--check" in args:
        check_setup()
        return

    if "--remove" in args:
        remove_mcp()
        return

    api_key = None
    if "--key" in args:
        idx = args.index("--key")
        if idx + 1 < len(args):
            api_key = args[idx + 1]

    if not api_key:
        api_key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        api_key = input("Enter your Google AI API key: ").strip()

    if not api_key:
        print("Error: API key is required.", file=sys.stderr)
        sys.exit(1)

    setup_mcp(api_key)


if __name__ == "__main__":
    main()
