# ThePawLight Site — AI State

Last updated: 2026-06-30

## Live goal

- `http://thepawlight.com/` redirects visitors to Etsy listing `1375236596`.
- `https://thepawlight.com/` is pending GitHub Pages certificate provisioning at cutover time.
- Redirect method: branded static HTML page + Cloudflare Web Analytics-ready beacon loader + UTM-preserving JavaScript redirect + meta refresh fallback + fallback link.

## Analytics and attribution

- Best practice: use `thepawlight.com` as the primary QR/social destination, not direct Etsy, so the brand owns SEO/attribution and can change destinations later without reprinting QR codes.
- Source of truth for campaign links: `campaigns.json`.
- Primary tracked links:
  - QR print: `https://thepawlight.com/?utm_source=qr&utm_medium=print&utm_campaign=pawlight_launch&utm_content=general`
  - Reddit: `https://thepawlight.com/?utm_source=reddit&utm_medium=social&utm_campaign=pawlight_launch&utm_content=thread`
  - Instagram: `https://thepawlight.com/?utm_source=instagram&utm_medium=social&utm_campaign=pawlight_launch&utm_content=bio`
- QR assets are generated into `assets/qr/` by `scripts/generate_qr_assets.py`.
- Cloudflare Web Analytics script is wired but requires a public site token in `assets/js/analytics-config.js`.
- Cloudflare guardrail: use free/free-tier Cloudflare only. Do not enable paid plans, Workers paid features, paid Pages add-ons, paid domains, R2 billable storage, Zaraz paid features, or any upgrade without explicit user approval.
- Billing monitor: Hermes cron job `Cloudflare Free Tier Billing Watchdog` (`d27c9e4b6a04`) runs every 6 hours. It is silent when subscriptions are `free`/price `0`, billing history has no positive charges, and PayGo usage has zero rows/cost; it alerts this chat on any new non-free/cost signal.
- Current billing check: Cloudflare API shows 1 account/user subscription on rate plan `free` with price `0 USD`, no billing history items, and no PayGo usage rows.
- Current Cloudflare API token can list RUM/Web Analytics sites but returned `HTTP 403 Authentication error` when trying to create the `thepawlight.com` site; create via dashboard or grant RUM/Web Analytics edit permission, then run `scripts/configure_cloudflare_web_analytics.py --write-config`.

## DNS

- DNS source of truth for `thepawlight.com`: GoDaddy.
- DNS cutover is managed from `/home/ubuntu/pawlight-fulfilment/infra/dns`.
- Desired GitHub Pages DNS:
  - Apex A: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  - `www` CNAME: `eizoefoer.github.io`

## Release gates

1. CI green on PR/main.
2. GitHub Pages build green.
3. `python3 scripts/verify_redirect.py --url http://thepawlight.com/` passes.
4. Browser navigation reaches Etsy listing URL or Etsy anti-bot page on listing `1375236596`.
5. After GitHub Pages certificate provisioning, enforce HTTPS and switch live checks back to `https://thepawlight.com/`.
6. For attribution changes, verify campaign URLs preserve UTM tags into the Etsy destination.
