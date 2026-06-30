#!/usr/bin/env python3
"""Generate QR assets for ThePawLight campaign links."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from qrcode.image.svg import SvgPathImage

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGNS = ROOT / "campaigns.json"


def load_campaigns(path: Path = CAMPAIGNS) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def make_qr(url: str) -> qrcode.QRCode:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=12,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr


def insert_svg_metadata(svg_path: Path, title: str, description: str) -> None:
    svg = svg_path.read_text(encoding="utf-8")
    marker = ">"
    idx = svg.find(marker)
    if idx == -1:
        return
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_desc = description.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    metadata = f"\n<title>{safe_title}</title>\n<desc>{safe_desc}</desc>"
    svg_path.write_text(svg[: idx + 1] + metadata + svg[idx + 1 :], encoding="utf-8")


def generate_assets(data: dict[str, Any], include_png: bool = True) -> dict[str, Any]:
    assets: dict[str, Any] = {}
    for key, campaign in data["campaigns"].items():
        url = campaign["url"]
        label = campaign.get("label", key)
        qr = make_qr(url)

        svg_rel = campaign["qr_svg"]
        svg_path = ROOT / svg_rel
        svg_path.parent.mkdir(parents=True, exist_ok=True)
        qr.make_image(image_factory=SvgPathImage).save(svg_path)
        insert_svg_metadata(svg_path, f"ThePawLight {key}", f"{label}: {url}")

        asset: dict[str, Any] = {
            "label": label,
            "url": url,
            "svg": svg_rel,
            "primary": campaign.get("primary", True),
        }

        png_rel = campaign.get("qr_png")
        if include_png and png_rel:
            png_path = ROOT / png_rel
            png_path.parent.mkdir(parents=True, exist_ok=True)
            img = qr.make_image(fill_color="#111827", back_color="#ffffff")
            img.save(png_path)
            asset["png"] = png_rel

        assets[key] = asset

    manifest = {
        "generated_at": "deterministic-build",
        "base_url": data["base_url"],
        "etsy_url": data["etsy_url"],
        "campaign": data["campaign"],
        "assets": assets,
    }
    manifest_path = ROOT / "assets" / "qr" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-png", action="store_true", help="Generate SVG only")
    args = parser.parse_args()
    manifest = generate_assets(load_campaigns(), include_png=not args.no_png)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
