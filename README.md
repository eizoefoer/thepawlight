# The PawLight Redirect Site

Static GitHub Pages brand landing + tracked redirect for `thepawlight.com`.

Live target:

- Brand URL: `https://thepawlight.com/`
- Etsy listing: `https://thepawlightofficial.etsy.com/listing/1375236596`

Marketing links:

- QR print: `https://thepawlight.com/?utm_source=qr&utm_medium=print&utm_campaign=pawlight_launch&utm_content=general`
- Reddit thread: `https://thepawlight.com/?utm_source=reddit&utm_medium=social&utm_campaign=pawlight_launch&utm_content=thread`
- Instagram bio: `https://thepawlight.com/?utm_source=instagram&utm_medium=social&utm_campaign=pawlight_launch&utm_content=bio`

Analytics adoption path:

1. **Now: Cloudflare Web Analytics** — keep as the default lightweight, privacy-first top-of-funnel tracker for visits, referrers, geography, device/browser/OS, Core Web Vitals, and UTM splits before redirecting to Etsy.
2. **Landing page phase: Microsoft Clarity** — add only after ThePawLight has a real landing page with copy/images/FAQs/CTAs and we need heatmaps, click/scroll maps, rage/dead-click signals, or session recordings. Configure masking/consent carefully before enabling.
3. **Paid ads phase: Google Analytics 4** — add only when running paid ads or needing deeper campaign/funnel attribution, custom conversion events, Google Ads integration, or remarketing-style analysis.

Etsy remains the sales/conversion source of truth; site analytics measure top-of-funnel traffic and outbound intent.

Commands:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/generate_qr_assets.py
python3 -m unittest discover -v
python3 scripts/verify_redirect.py --file index.html
python3 scripts/verify_redirect.py --url http://thepawlight.com/
```

Docs:

- `docs/analytics-and-qr.md`
- `campaigns.json`
- `assets/qr/manifest.json`

Release rule:

- Done only when CI is green, the PR is merged/deployed, and the live custom domain redirects to Etsy listing `1375236596` while preserving source UTM tags.
