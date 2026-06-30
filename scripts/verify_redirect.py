#!/usr/bin/env python3
"""Verify ThePawLight tracking redirect page points to the Etsy listing."""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

EXPECTED_TARGET = "https://thepawlightofficial.etsy.com/listing/1375236596"
BRAND_CANONICAL = "https://thepawlight.com/"
LISTING_ID = "1375236596"


def read_url(url: str) -> tuple[int, str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "thepawlight-redirect-check/1.1"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.geturl(), response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.geturl(), exc.read().decode("utf-8", errors="replace")


def read_file(path: str) -> tuple[int, str, str]:
    return 200, str(Path(path).resolve()), Path(path).read_text(encoding="utf-8")


def _has(pattern: str, html: str) -> bool:
    return re.search(pattern, html, re.I | re.S) is not None


def validate(status: int, source: str, html: str) -> int:
    print(f"source={source}")
    print(f"status={status}")
    if status != 200:
        print(f"FAIL: expected status 200, got {status}", file=sys.stderr)
        return 1
    if LISTING_ID not in html:
        print(f"FAIL: missing Etsy listing id {LISTING_ID}", file=sys.stderr)
        return 1

    checks = {
        "brand_canonical": _has(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']' + re.escape(BRAND_CANONICAL), html),
        "meta_refresh_fallback": _has(r'<meta[^>]+http-equiv=["\']refresh["\'][^>]+content=["\'][^"\']*' + re.escape(EXPECTED_TARGET), html),
        "javascript_redirect": _has(r'window\.location\.replace\([^)]*etsyUrl\.toString\(\)', html),
        "fallback_link": _has(r'<a[^>]+href=["\']' + re.escape(EXPECTED_TARGET), html),
        "utm_preservation": "utm_source" in html and "URLSearchParams" in html,
        "cloudflare_web_analytics_ready": "static.cloudflareinsights.com/beacon.min.js" in html,
    }
    missing = [name for name, matched in checks.items() if not matched]
    if missing:
        print(f"FAIL: missing redirect/tracking mechanisms: {', '.join(missing)}", file=sys.stderr)
        return 1

    print(f"PASS: tracks source and redirects to {EXPECTED_TARGET}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file")
    group.add_argument("--url")
    args = parser.parse_args()

    status, source, html = read_file(args.file) if args.file else read_url(args.url)
    return validate(status, source, html)


if __name__ == "__main__":
    raise SystemExit(main())
