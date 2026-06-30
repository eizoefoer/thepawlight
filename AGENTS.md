# ThePawLight Site — Agent Guide

## Project

Public GitHub Pages brand landing + tracking redirect site for `thepawlight.com` -> Etsy listing `1375236596`.

## Commands

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/generate_qr_assets.py
python3 -m unittest discover -v
python3 scripts/verify_redirect.py --file index.html
python3 scripts/verify_redirect.py --url http://thepawlight.com/
```

## Rules

- Keep this repo public for free GitHub Pages.
- Use PR branches after initial bootstrap.
- Maintain CI + auto-merge workflow.
- Release is done only after the custom domain is live and verified redirecting to Etsy.
- Keep `CNAME` as `thepawlight.com` unless the DNS plan changes.
- Use ThePawLight brand URL as the primary QR/social destination; direct Etsy QR is backup only.
- Track source with standard UTM tags: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`.
- Preserve UTM tags when forwarding to Etsy.

## Live target

- Custom domain: `http://thepawlight.com/` (`https://thepawlight.com/` pending GitHub Pages certificate)
- GitHub Pages fallback: `https://eizoefoer.github.io/thepawlight/`
- Etsy target: `https://thepawlightofficial.etsy.com/listing/1375236596`

## Analytics + QR

- Source of truth: `campaigns.json`.
- QR assets: `assets/qr/`.
- Analytics docs: `docs/analytics-and-qr.md`.
- Preferred analytics: Cloudflare Web Analytics via `assets/js/analytics-config.js`.
- Analytics adoption path: keep Cloudflare Web Analytics now; add Microsoft Clarity only for a fuller landing page that needs heatmaps/session recordings/UX diagnosis; add Google Analytics 4 only when paid ads or deeper funnel/campaign attribution justify the privacy/setup overhead.
- Etsy remains the sales/conversion source of truth; this site measures top-of-funnel source attribution and outbound intent.
- Cloudflare must stay free/free-tier only. Do not enable paid plans, Workers paid features, paid Pages add-ons, domains, R2 billable storage, Zaraz paid features, or any upgrade without explicit user approval.
- Billing guardrail: Hermes cron job `Cloudflare Free Tier Billing Watchdog` (`d27c9e4b6a04`) checks Cloudflare subscriptions, billing history, and PayGo usage every 6 hours and stays silent unless cost/non-free plan appears.
