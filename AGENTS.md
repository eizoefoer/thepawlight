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

- Custom domains: `https://thepawlight.com/` and `https://www.thepawlight.com/`
- Hosting path: Caddy on Oracle VM serving `/srv/thepawlight`; DNS/Caddy/live E2E are tracked in private `eizoefoer/site-infra` at `/home/ubuntu/site-infra`.
- Etsy target: `https://thepawlightofficial.etsy.com/listing/1375236596`

## Analytics + QR

- Source of truth: `campaigns.json`.
- QR assets: `assets/qr/`.
- Analytics docs: `docs/analytics-and-qr.md`.
- Preferred analytics: Cloudflare Web Analytics via `assets/js/analytics-config.js`.
- Analytics adoption path: keep Cloudflare Web Analytics now; add Microsoft Clarity only for a fuller landing page that needs heatmaps/session recordings/UX diagnosis; add Google Analytics 4 only when paid ads or deeper funnel/campaign attribution justify the privacy/setup overhead.
- Etsy remains the sales/conversion source of truth; this site measures top-of-funnel source attribution and outbound intent.
- Cloudflare must stay free/free-tier only. Do not enable paid plans, Workers paid features, paid Pages add-ons, domains, R2 billable storage, Zaraz paid features, or any upgrade without explicit user approval.
- UI must keep dark-mode support. The landing page uses `assets/js/theme.js` plus CSS variables and a visible theme toggle.
- Billing guardrail: Hermes cron job `Cloudflare Free Tier Billing Watchdog` (`d27c9e4b6a04`) checks Cloudflare subscriptions, billing history, and PayGo usage every 6 hours and stays silent unless cost/non-free plan appears.

<!-- agent-state-standard:v1 -->
## Agent state standard

`AGENTS.md` is the single source of truth for agentic work in this repo. Before starting or completing work, every agent must:

1. Read this file and any referenced project docs.
2. Check `.agents/project-memory.json` and `.agents/task-log.jsonl` for current state.
3. Update `.agents/task-log.jsonl` with a JSON line for meaningful starts, decisions, blockers, tests, and completions.
4. Keep `README.md` current when behavior, setup, deployment, or public usage changes.
5. Keep `CLAUDE.md` and other agent-specific entrypoints as pointers back to `AGENTS.md`; do not duplicate rules there.
6. Put reusable project-specific skill code/templates under `skills/`.
7. Prefer IaC/config/scripts over clickops. If clickops are unavoidable, document the exact manual step and the IaC replacement TODO.
8. Prefer local/free/self-hosted tools first. Use free-tier fallbacks only when they are better for the task or their limits have reset. Paid providers require explicit approval.

Project state files:

- `.agents/project-memory.json` — compact durable project facts and agent handoff pointers.
- `.agents/task-log.jsonl` — append-only event log for cross-model/machine task resumption.
- `skills/project-memory/SKILL.md` — project-local skill explaining how to resume and update state.

JSONL event shape:

```json
{"ts":"2026-07-04T00:00:00Z","actor":"agent-or-human","event":"start|decision|change|test|blocker|complete","summary":"short factual note","files":["path"],"next":["optional next action"]}
```

## Obsidian synthesis and retrieval

Use `/home/ubuntu/vault/projects/managed/thepawlight-0063b75f.md` for concise cross-project storage and retrieval. Read it before meaningful work, then use this repository's `.agents/` files as authoritative task state. Update repository state first; update the vault only when it improves durable cross-project retrieval. Shared policy: `/home/ubuntu/vault/system/project-obsidian-memory.md`.
