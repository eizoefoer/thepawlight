#!/usr/bin/env python3
"""Create/read Cloudflare Web Analytics token for ThePawLight."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "assets" / "js" / "analytics-config.js"
HOST = "thepawlight.com"


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value.strip().strip('"').strip("'"))


def cf_request(method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    token = os.environ["CLOUDFLARE_API_TOKEN"]
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Cloudflare API HTTP {exc.code}: {details}") from exc


def find_site(host: str) -> dict[str, Any] | None:
    data = cf_request("GET", "/rum/site_info/list?per_page=100")
    if not data.get("success"):
        raise RuntimeError(json.dumps(data, indent=2))
    for site in data.get("result") or []:
        if (site.get("host") or "").lower() == host.lower():
            return site
    return None


def create_site(host: str) -> dict[str, Any]:
    data = cf_request("POST", "/rum/site_info", {"host": host, "auto_install": False})
    if not data.get("success"):
        raise RuntimeError(json.dumps(data, indent=2))
    return data["result"]


def write_config(token: str, path: Path = CONFIG) -> None:
    text = path.read_text(encoding="utf-8")
    replacement = f'cloudflareToken: "{token}"'
    if re.search(r'cloudflareToken:\s*"[^"]*"', text):
        text = re.sub(r'cloudflareToken:\s*"[^"]*"', replacement, text)
    else:
        raise RuntimeError(f"Could not find cloudflareToken in {path}")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", default="~/.hermes/.env")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--create", action="store_true", help="Create the site if missing")
    parser.add_argument("--write-config", action="store_true", help="Write public site token to assets/js/analytics-config.js")
    args = parser.parse_args()

    load_env(Path(args.env_file).expanduser())
    missing = [key for key in ("CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN") if not os.environ.get(key)]
    if missing:
        print(f"FAIL: missing env vars: {', '.join(missing)}", file=sys.stderr)
        return 2

    try:
        site = find_site(args.host)
        if site is None and args.create:
            site = create_site(args.host)
        if site is None:
            print(f"FAIL: no Cloudflare Web Analytics site found for {args.host}; re-run with --create", file=sys.stderr)
            return 1
    except RuntimeError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        print("Hint: API token needs Cloudflare Account Analytics/RUM edit permission to create sites.", file=sys.stderr)
        return 1

    print(json.dumps({
        "host": site.get("host"),
        "site_tag": site.get("site_tag"),
        "site_token": site.get("site_token"),
        "snippet": site.get("snippet"),
    }, indent=2))
    if args.write_config:
        write_config(str(site["site_token"]))
        print(f"wrote {CONFIG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
