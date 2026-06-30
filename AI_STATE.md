# ThePawLight Site — AI State

Last updated: 2026-06-30

## Live goal

- `https://thepawlight.com/` redirects visitors to Etsy listing `1375236596`.
- Redirect method: static HTML meta refresh + JavaScript `window.location.replace` + fallback link.

## DNS

- DNS source of truth for `thepawlight.com`: GoDaddy.
- DNS cutover is managed from `/home/ubuntu/pawlight-fulfilment/infra/dns`.
- Desired GitHub Pages DNS:
  - Apex A: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  - `www` CNAME: `eizoefoer.github.io`

## Release gates

1. CI green on PR/main.
2. GitHub Pages build green.
3. `python3 scripts/verify_redirect.py --url https://thepawlight.com/` passes.
4. Browser navigation reaches Etsy listing URL or Etsy anti-bot page on listing `1375236596`.
