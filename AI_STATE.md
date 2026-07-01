# ThePawLight Site — AI State

Last updated: 2026-06-30

## Live goal

- `https://thepawlight.com/` and `https://www.thepawlight.com/` serve the branded redirect page from Caddy on the Oracle VM and redirect visitors to Etsy listing `1375236596`.
- Redirect method: branded static HTML page + Cloudflare Web Analytics beacon loader + dark-mode theme support + UTM-preserving JavaScript redirect + meta refresh fallback + fallback link.
- Cross-site hosting/DNS/Caddy/Playwright source of truth: private repo `eizoefoer/site-infra` at `/home/ubuntu/site-infra`.

## Analytics and attribution

- Best practice: use `thepawlight.com` as the primary QR/social destination, not direct Etsy, so the brand owns SEO/attribution and can change destinations later without reprinting QR codes.
- Source of truth for campaign links: `campaigns.json`.
- Primary tracked links:
  - QR print: `https://thepawlight.com/?utm_source=qr&utm_medium=print&utm_campaign=pawlight_launch&utm_content=general`
  - Reddit: `https://thepawlight.com/?utm_source=reddit&utm_medium=social&utm_campaign=pawlight_launch&utm_content=thread`
  - Instagram: `https://thepawlight.com/?utm_source=instagram&utm_medium=social&utm_campaign=pawlight_launch&utm_content=bio`
- QR assets are generated into `assets/qr/` by `scripts/generate_qr_assets.py`.
- Cloudflare Web Analytics public site token is configured in `assets/js/analytics-config.js` after dashboard creation for `thepawlight.com`.
- Analytics adoption path: Cloudflare Web Analytics stays active now; Microsoft Clarity is a later landing-page UX tool for heatmaps/session recordings and must be added only with masking/consent care; Google Analytics 4 is a later paid-ads/deep-attribution tool, not needed for the current redirect page.
- Etsy remains the sales/conversion source of truth; ThePawLight analytics tracks top-of-funnel visits, campaign source, and outbound intent before Etsy.
- Cloudflare guardrail: use free/free-tier Cloudflare only. Do not enable paid plans, Workers paid features, paid Pages add-ons, paid domains, R2 billable storage, Zaraz paid features, or any upgrade without explicit user approval.
- Billing monitor: Hermes cron job `Cloudflare Free Tier Billing Watchdog` (`d27c9e4b6a04`) runs every 6 hours. It is silent when subscriptions are `free`/price `0`, billing history has no positive charges, and PayGo usage has zero rows/cost; it alerts this chat on any new non-free/cost signal.
- Current billing check: Cloudflare API shows 1 account/user subscription on rate plan `free` with price `0 USD`, no billing history items, and no PayGo usage rows.
- The previous Cloudflare API token could list RUM/Web Analytics sites but returned `HTTP 403 Authentication error` when trying to create the `thepawlight.com` site; dashboard-created public snippet was used instead.

## DNS

- DNS source of truth for `thepawlight.com`: GoDaddy, with managed records tracked in `/home/ubuntu/site-infra/inventory/dns.json`.
- Current VM-hosted DNS:
  - Apex A: `192.9.160.136`
  - `www` CNAME: `@`
- Caddy serves valid HTTPS for both apex and `www`.

## Release gates

1. CI green on PR/main.
2. Static redirect tests pass in this repo.
3. Cross-site IaC/live E2E checks pass in `eizoefoer/site-infra`.
4. Browser navigation reaches Etsy listing URL or Etsy anti-bot page on listing `1375236596`.
5. For attribution changes, verify campaign URLs preserve UTM tags into the Etsy destination.
