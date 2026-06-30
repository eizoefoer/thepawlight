# ThePawLight analytics + QR tracking

## Best-practice choice

Use the brand landing URL first:

```text
https://thepawlight.com/?utm_source=qr&utm_medium=print&utm_campaign=pawlight_launch&utm_content=general
```

Why:

- Keeps SEO and brand signals on `thepawlight.com` instead of only Etsy.
- Lets us change the final shop later without reprinting QR codes.
- Lets analytics split QR, Reddit, Instagram, direct, and referral traffic before the visitor goes to Etsy.
- Still sends shoppers to the Etsy listing automatically.

Use direct Etsy QR only as a backup marketplace-only code:

```text
https://thepawlightofficial.etsy.com/listing/1375236596?utm_source=qr&utm_medium=print&utm_campaign=pawlight_launch&utm_content=etsy_direct_backup
```

## Source links

Source of truth: `campaigns.json`.

Primary links:

- QR print: `https://thepawlight.com/?utm_source=qr&utm_medium=print&utm_campaign=pawlight_launch&utm_content=general`
- Reddit thread: `https://thepawlight.com/?utm_source=reddit&utm_medium=social&utm_campaign=pawlight_launch&utm_content=thread`
- Instagram bio/story: `https://thepawlight.com/?utm_source=instagram&utm_medium=social&utm_campaign=pawlight_launch&utm_content=bio`
- Direct/organic: `https://thepawlight.com/` with no UTM tags.

## QR generator

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/generate_qr_assets.py
```

Outputs:

- `assets/qr/thepawlight-qr-print.svg`
- `assets/qr/thepawlight-qr-print.png`
- `assets/qr/thepawlight-reddit-thread.svg`
- `assets/qr/thepawlight-reddit-thread.png`
- `assets/qr/thepawlight-instagram-bio.svg`
- `assets/qr/thepawlight-instagram-bio.png`
- `assets/qr/thepawlight-etsy-direct-backup.svg`
- `assets/qr/thepawlight-etsy-direct-backup.png`
- `assets/qr/manifest.json`

## Analytics provider

Preferred free/privacy-first provider: Cloudflare Web Analytics.

Cloudflare docs confirm it works without moving DNS to Cloudflare proxy. It uses a JavaScript beacon and can report page views, visits, referrers, country, browser, OS, and device type.

The site is wired for Cloudflare Web Analytics in:

- `assets/js/analytics-config.js`
- `index.html`
- `404.html`

Create/read the public site token:

```bash
python3 scripts/configure_cloudflare_web_analytics.py --env-file ~/.hermes/.env --create --write-config
```

If Cloudflare returns `HTTP 403 Authentication error`, the token can list analytics but lacks Web Analytics/RUM edit permission. Fix by creating the Web Analytics site in the Cloudflare dashboard or updating the API token permissions, then rerun:

```bash
python3 scripts/configure_cloudflare_web_analytics.py --env-file ~/.hermes/.env --write-config
```

## Reading the numbers

In Cloudflare Web Analytics, split traffic by:

- Path/page URL query for `utm_source=qr`, `utm_source=reddit`, `utm_source=instagram`.
- Referer host for untagged sources.
- Direct/none for direct traffic.
- Country, device type, browser, OS for audience profile.

Etsy remains the sales/conversion source of truth. ThePawLight analytics is the top-of-funnel source attribution layer.
