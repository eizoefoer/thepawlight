from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
ETSY_LISTING_ID = "1375236596"
BRAND_HOST = "thepawlight.com"


class TrackingSiteTests(unittest.TestCase):
    def test_campaign_urls_use_brand_domain_and_standard_utm_tags(self) -> None:
        campaigns_path = ROOT / "campaigns.json"
        self.assertTrue(campaigns_path.exists(), "campaigns.json should define trackable source URLs")
        data = json.loads(campaigns_path.read_text(encoding="utf-8"))

        self.assertEqual(data["base_url"], "https://thepawlight.com/")
        self.assertIn(ETSY_LISTING_ID, data["etsy_url"])

        campaigns = data["campaigns"]
        for key in ("qr_print", "reddit_thread", "instagram_bio"):
            with self.subTest(campaign=key):
                self.assertIn(key, campaigns)
                url = campaigns[key]["url"]
                parsed = urlparse(url)
                params = parse_qs(parsed.query)
                self.assertEqual(parsed.scheme, "https")
                self.assertEqual(parsed.netloc, BRAND_HOST)
                self.assertEqual(params.get("utm_campaign"), ["pawlight_launch"])
                self.assertIn("utm_source", params)
                self.assertIn("utm_medium", params)
                self.assertTrue(campaigns[key].get("qr_svg", "").startswith("assets/qr/"))

    def test_homepage_is_brand_canonical_and_tracks_before_redirecting(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertRegex(html, r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']https://thepawlight\.com/[^"\']*["\']')
        self.assertNotRegex(html, r'<meta[^>]+name=["\']robots["\'][^>]+noindex')
        self.assertIn("static.cloudflareinsights.com/beacon.min.js", html)
        self.assertIn("assets/js/theme.js", html)
        self.assertIn("data-theme-toggle", html)
        self.assertIn("pawlight-theme", (ROOT / "assets" / "js" / "theme.js").read_text(encoding="utf-8"))
        self.assertIn("data-theme='dark'", html)
        self.assertIn("URLSearchParams", html)
        self.assertIn("utm_source", html)
        self.assertRegex(html, r"setTimeout\([^,]+,\s*1[0-9]{3}\)")
        self.assertRegex(html, re.escape(ETSY_LISTING_ID))

    def test_cloudflare_web_analytics_token_is_configured(self) -> None:
        config = (ROOT / "assets" / "js" / "analytics-config.js").read_text(encoding="utf-8")
        match = re.search(r'cloudflareToken:\s*"([0-9a-f]{32})"', config)
        self.assertIsNotNone(match, "Cloudflare Web Analytics public token should be configured")
        if match is None:
            return
        self.assertNotEqual(match.group(1), "")

    def test_qr_assets_and_manifest_are_generated(self) -> None:
        manifest = ROOT / "assets" / "qr" / "manifest.json"
        self.assertTrue(manifest.exists(), "QR manifest should be generated for print/social assets")
        data = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertIn("generated_at", data)
        self.assertIn("assets", data)
        for key in ("qr_print", "reddit_thread", "instagram_bio"):
            with self.subTest(campaign=key):
                asset = data["assets"][key]
                svg_path = ROOT / asset["svg"]
                self.assertTrue(svg_path.exists(), f"missing {svg_path}")
                svg = svg_path.read_text(encoding="utf-8")
                self.assertIn("<svg", svg)
                self.assertIn(BRAND_HOST, svg, "SVG should include human-readable target metadata")
                self.assertEqual(asset["url"], json.loads((ROOT / "campaigns.json").read_text(encoding="utf-8"))["campaigns"][key]["url"])


if __name__ == "__main__":
    unittest.main()
