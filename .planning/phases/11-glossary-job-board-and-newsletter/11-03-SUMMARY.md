---
plan: 11-03
status: complete
commits:
  - "feat(11-03): add newsletter signup worker and weekly email generator"
  - "feat(11-03): wire signup forms to worker and add cron script"
files_created:
  - worker/subscribe.js
  - worker/wrangler.toml
  - scripts/generate_weekly_email.py
  - scripts/send_weekly_email.sh
files_modified:
  - scripts/templates.py
  - scripts/nav_config.py
verification: "Worker files exist, SIGNUP_WORKER_URL in nav_config, signup JS wired into all pages, email preview generates with GTME Pulse branding, cron script syntax valid. Human checkpoint approved."
---

## Results

- **worker/subscribe.js** — Cloudflare Worker handling POST {email} → Resend Audiences API. CORS for gtmepulse.com + localhost:8090.
- **worker/wrangler.toml** — Worker deployment config (name: gtme-newsletter-signup)
- **SIGNUP_WORKER_URL** added to nav_config.py, imported in templates.py
- **handleSignup() JS** wired into all pages via get_page_wrapper() — targets .hero-signup, .footer-newsletter-form, .newsletter-cta-form
- **generate_weekly_email.py** — Loads market_intelligence.json + comp_analysis.json, computes week-over-week diffs, renders branded HTML email, sends via Resend API. Flags: --preview, --send, --add-subscriber, --list-subscribers
- **send_weekly_email.sh** — Monday cron script (0 18 * * 1 = 10 AM PST). Loads .env, git pulls, runs generator with --send
- Human checkpoint approved: signup forms, email preview, worker code all verified
