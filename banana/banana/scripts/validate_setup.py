#!/usr/bin/env python3
"""Validate Banana Claude MCP server configuration."""

import json
import shutil
import sys
from pathlib import Path

SETTINGS_FILE = Path.home() / ".claude" / "settings.json"
MCP_NAME = "nanobanana-mcp"
MCP_PACKAGE = "@ycse/nanobanana-mcp"
OUTPUT_DIR = Path.home() / "Documents" / "nanobanana_generated"


def check(label, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    line = f"[{status}] {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    return passed


def main():
    all_passed = True

    # 1. settings.json exists
    ok = check("settings.json exists", SETTINGS_FILE.exists(), str(SETTINGS_FILE))
    all_passed = all_passed and ok
    if not ok:
        print("\nRun: python3 setup_mcp.py --key YOUR_API_KEY")
        sys.exit(1)

    # 2. Valid JSON
    try:
        settings = json.loads(SETTINGS_FILE.read_text())
        ok = check("settings.json is valid JSON", True)
    except json.JSONDecodeError as e:
        check("settings.json is valid JSON", False, str(e))
        sys.exit(1)

    # 3. MCP server entry configured
    mcp_servers = settings.get("mcpServers", {})
    ok = check(f"MCP server '{MCP_NAME}' configured", MCP_NAME in mcp_servers)
    all_passed = all_passed and ok
    if not ok:
        print("\nRun: python3 setup_mcp.py --key YOUR_API_KEY")
        sys.exit(1)

    cfg = mcp_servers[MCP_NAME]

    # 4. Command is npx
    ok = check("command is 'npx'", cfg.get("command") == "npx")
    all_passed = all_passed and ok

    # 5. Package is correct
    args = cfg.get("args", [])
    ok = check(f"package is '{MCP_PACKAGE}'", MCP_PACKAGE in args)
    all_passed = all_passed and ok

    # 6. API key configured
    env = cfg.get("env", {})
    api_key = env.get("GOOGLE_AI_API_KEY", "")
    masked = api_key[:8] + "..." if api_key else "(not set)"
    ok = check("GOOGLE_AI_API_KEY is set", bool(api_key), masked)
    all_passed = all_passed and ok

    # 7. Model configured
    model = env.get("NANOBANANA_MODEL", "")
    ok = check("NANOBANANA_MODEL is set", bool(model), model or "(using default)")
    all_passed = all_passed and ok

    # 8. npx available in PATH
    ok = check("npx available in PATH", shutil.which("npx") is not None)
    all_passed = all_passed and ok

    # 9. Output directory
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        ok = check("output directory exists", True, str(OUTPUT_DIR))
    except OSError as e:
        ok = check("output directory accessible", False, str(e))
    all_passed = all_passed and ok

    print()
    if all_passed:
        print("All checks passed. Banana Claude is ready!")
        sys.exit(0)
    else:
        print("Some checks failed. Run: python3 setup_mcp.py --key YOUR_API_KEY")
        sys.exit(1)


if __name__ == "__main__":
    main()
