# ThePawLight Site — Agent Guide

## Project

Public GitHub Pages redirect site for `thepawlight.com` -> Etsy listing `1375236596`.

## Commands

```bash
python3 scripts/verify_redirect.py --file index.html
python3 scripts/verify_redirect.py --url http://thepawlight.com/
```

## Rules

- Keep this repo public for free GitHub Pages.
- Use PR branches after initial bootstrap.
- Maintain CI + auto-merge workflow.
- Release is done only after the custom domain is live and verified redirecting to Etsy.
- Keep `CNAME` as `thepawlight.com` unless the DNS plan changes.

## Live target

- Custom domain: `http://thepawlight.com/` (`https://thepawlight.com/` pending GitHub Pages certificate)
- GitHub Pages fallback: `https://eizoefoer.github.io/thepawlight/`
- Etsy target: `https://thepawlightofficial.etsy.com/listing/1375236596`
