# Technology Stack

**Project:** GTME Pulse (gtmepulse.com)
**Researched:** 2026-03-10
**Overall Confidence:** HIGH

## Recommended Stack

### Core Build System

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Python 3.12+ | 3.12-3.14 | Static site generator | Already on system (3.14). No dependencies needed. stdlib `os`, `json`, `shutil`, `datetime` handle everything. Use 3.12 in CI for stability. |
| f-strings + triple-quoted HTML | stdlib | Templating | Proven pattern from SultanOfSaaS (145 pages) and b2bsalestools (196 pages). Zero dependencies. Jinja2 adds complexity with no benefit when all templates are Python functions. |
| `json` stdlib | stdlib | Data files | Salary data, job postings, market stats in `data/*.json`. Loaded at build time. No YAML, no TOML, no frontmatter parsing needed. |
| `shutil` stdlib | stdlib | Asset copying | Copy `assets/` to `output/` at build time. |

**Confidence:** HIGH. This exact pattern runs 5+ production sites in this portfolio (SultanOfSaaS, b2bsalestools, Cannabisers, Provyx, RevOps Report). Zero external Python dependencies for the build.

### 3-File Build Architecture

| File | Role | Exports |
|------|------|---------|
| `scripts/build.py` | Data definitions + page generators | Main entry point. Defines all structured data (salary benchmarks, tool specs, categories). Calls generator functions that produce HTML. |
| `scripts/templates.py` | Reusable HTML components + schema helpers | `get_html_head()`, `get_nav_html()`, `get_footer_html()`, `get_page_wrapper()`, `write_page()`, `breadcrumb_html()`, `breadcrumb_schema()`, `faq_schema_and_html()`, `newsletter_cta_html()`. Tracks `ALL_PAGES` for sitemap. |
| `scripts/nav_config.py` | Site constants + navigation structure | `SITE_NAME`, `SITE_URL`, `CSS_VERSION`, `NAV_ITEMS`, `FOOTER_COLUMNS`. Single source of truth for nav across all pages. |

**Content modules** (`content/*.py`) hold expanded prose. Auto-discovered by `build.py`. Pages render with defaults when module is missing, so you can build structure first and fill prose later.

**Confidence:** HIGH. Direct clone of the SultanOfSaaS architecture which generated 145 pages cleanly.

### CSS Architecture

| File | Purpose | Why |
|------|---------|-----|
| `assets/css/tokens.css` | Design tokens (colors, spacing, typography, shadows, radii, z-index) | Already built. 90 lines. Includes dark mode via `prefers-color-scheme` and `data-theme="dark"`. All values as CSS custom properties. |
| `assets/css/components.css` | Reusable component styles (cards, buttons, tags, tables, badges, stat grids, CTAs) | Separates structural components from page layout. Components reference tokens exclusively. Never hardcode colors or spacing. |
| `assets/css/styles.css` | Page-specific styles (hero, salary breakdown layout, tool review layout, job board) | Handles page-level composition. References tokens and extends component classes where needed. |

**Loading order:** tokens.css -> components.css -> styles.css. Cache-busted via `?v={CSS_VERSION}` query param (integer in `nav_config.py`, increment on every CSS change).

**Key design decisions:**
- CSS custom properties only (no Sass, no PostCSS, no build step). Modern browser support is 97%+. Sass adds a build dependency for zero benefit on a token-driven static site.
- Fluid typography via `clamp()` already in tokens.css. No JS-based responsive font sizing needed.
- Mobile breakpoints at 375px, 768px, 1024px (declared in PROJECT.md). Use `@media` in styles.css.
- No CSS reset library. A minimal reset block (box-sizing, margin zero on body) at the top of components.css is sufficient.
- No utility-class framework (Tailwind, etc.). Token-driven component CSS is cleaner for programmatic HTML generation where class names are composed in Python strings.

**Confidence:** HIGH. tokens.css is already built and verified. The 3-file CSS split matches every site in the portfolio.

### Fonts (Google Fonts)

| Font | Weights | Role | Loading Strategy |
|------|---------|------|-----------------|
| Sora | 400, 500, 600, 700 | Headings | `<link rel="preconnect" href="https://fonts.googleapis.com">` + `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` + single `<link>` combining all three families with `display=swap` |
| Plus Jakarta Sans | 400, 500, 600, 700, 800 | Body text | Same combined request |
| Source Code Pro | 400, 500, 600, 700 | Data labels, stats, code | Same combined request |

**Performance note:** One combined Google Fonts request for all three families. `display=swap` prevents FOIT. Preconnect hints eliminate DNS/TLS latency. Do NOT self-host; Google Fonts CDN is faster for cold loads and the cache hit rate across sites is high.

**Confidence:** HIGH. Standard pattern, fonts already specified in tokens.css.

### Newsletter Infrastructure

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Resend API | v2 (Audiences endpoint) | Subscriber management + email sending | Already in use for RevOps Report. Same Resend account. Audiences API adds contacts, Emails API sends. Python SDK for server-side sends, REST API from Worker for signups. |
| `resend` Python SDK | 2.23.0 | Server-side email generation + send | Latest stable. `pip install resend==2.23.0`. Used only in `generate_weekly_email.py` (Wave 4), not in the static build. |
| Cloudflare Worker | ES modules format | Form POST -> Resend Audiences | Proven pattern: `worker/subscribe.js` handles CORS, validates email, POSTs to Resend Audiences API. ~90 lines. Clone from RevOps Report and update `ALLOWED_ORIGINS` and audience ID. |
| Wrangler CLI | 4.x (latest) | Worker deployment | `npx wrangler deploy` from `worker/` dir. Secrets via `wrangler secret put RESEND_API_KEY`. `compatibility_date: "2025-01-01"` in wrangler.toml. |

**Signup flow:**
1. Static HTML form calls `handleSignup()` JS function (inline, ~30 lines)
2. JS POSTs `{email}` to `gtme-newsletter-signup.rome-workers.workers.dev`
3. Worker validates, calls Resend Audiences API, returns JSON
4. JS shows success/error state in-page

**Confidence:** HIGH. Exact clone of production RevOps Report worker (`/Users/rome/Documents/revops_report/worker/subscribe.js`). Verified working.

### Deployment

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| GitHub Pages | v4 Actions | Static hosting | Free, fast, automatic deploys on push to main. 1GB limit is irrelevant for HTML/CSS site. |
| GitHub Actions | actions/deploy-pages@v4 | CI/CD pipeline | Build validation -> upload artifact -> deploy. Proven workflow from RevOps Report. |
| Cloudflare DNS | N/A | DNS management + CDN | Handles CNAME, SSL, and edge caching. Already configured for other domains in portfolio. |

**GitHub Actions Workflow (`.github/workflows/deploy-site.yml`):**
```yaml
name: Deploy Site
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Build site
        run: python3 scripts/build.py
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: "./output"

  deploy:
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

**Key details:**
- Build outputs to `output/`. GitHub Pages serves from that artifact.
- `CNAME` file auto-generated by build.py containing `gtmepulse.com`.
- Python 3.12 in CI (stable, widely available on ubuntu-latest). Local dev can use 3.14.
- No `requirements.txt` needed. Build uses stdlib only.
- `validate_build.py` optional but recommended: check page count, verify no broken internal links, confirm sitemap entries match built pages.

**Confidence:** HIGH. Clone of RevOps Report deploy workflow, verified working.

### SEO / Schema Markup

| Technology | Purpose | Implementation |
|------------|---------|---------------|
| JSON-LD | Structured data | Inline `<script type="application/ld+json">` blocks generated by Python schema helpers in templates.py |
| BreadcrumbList | Navigation hierarchy | Every inner page. Generated from page path. |
| FAQPage | FAQ sections | Salary comparison pages, tool pages. Min 3 Q&A pairs. |
| Organization + WebSite | Homepage identity | `@graph` pattern combining both on homepage only. |
| SoftwareApplication | Tool reviews (Wave 2) | Individual tool review pages. |
| Article + Person | Insight articles (Wave 4) | Author: Rome Thorndike. |

**Auto-generated files:**
- `sitemap.xml` from `ALL_PAGES` list (built during page generation)
- `robots.txt` with `Sitemap: https://gtmepulse.com/sitemap.xml`
- `CNAME` with `gtmepulse.com`

**Confidence:** HIGH. Schema helpers are proven across portfolio sites.

### Supporting Tools (Development Only)

| Tool | Purpose | When |
|------|---------|------|
| `python3 -m http.server 8090` | Local preview | `cd output && python3 -m http.server 8090`. No install needed. |
| `git` | Version control | Standard. Private repo at `romelikethecity/gtmepulse`. |
| `npx wrangler` | Worker deployment | Only needed when deploying/updating newsletter signup worker. Not part of site build. |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Templating | f-strings in Python | Jinja2 | Adds a dependency for no benefit. Templates are Python functions returning strings. Jinja's file-based template model fights against programmatic page generation. Every other site in this portfolio uses f-strings. |
| Templating | f-strings in Python | Mako | Same as Jinja2. Extra dependency, different paradigm, no advantage. |
| CSS | Custom properties (tokens) | Tailwind CSS | Utility classes make programmatic HTML harder to read/maintain. Token-driven CSS with component classes is cleaner when HTML is generated from Python dicts. Tailwind also requires a Node build step. |
| CSS | Custom properties (tokens) | Sass/SCSS | Adds a build dependency (Node or dart-sass). CSS custom properties do everything Sass variables do, natively. No nesting needed when component CSS is well-structured. |
| Static generator | Custom Python (3-file) | Pelican | Pelican's Markdown-based content model doesn't fit programmatic page generation from structured data. Our pages are generated from Python dicts, not Markdown files. |
| Static generator | Custom Python (3-file) | Hugo / Eleventy / Astro | Non-Python. Adds Node dependency. Template systems fight against the data-driven generation model. |
| Newsletter | Resend API | Mailchimp / ConvertKit | Resend is API-first, cheaper at scale, already in use. Mailchimp adds bloat and widget JS. ConvertKit is creator-focused, not developer-focused. |
| Hosting | GitHub Pages | Cloudflare Pages | GitHub Pages is already proven in portfolio. Cloudflare Pages would require repo connection setup and different deploy pattern. No benefit for a static HTML site. |
| Hosting | GitHub Pages | Vercel | Overkill for static HTML. Vercel's value is in serverless functions and framework support, neither of which applies here. |
| Form handling | Cloudflare Worker | Netlify Forms / Formspree | Cloudflare Worker is free tier, already configured, gives full control. Third-party form services add branding, limits, and another vendor dependency. |

## What NOT to Install

| Technology | Why Not |
|------------|---------|
| Node.js / npm (for the site build) | Zero JavaScript build tools needed. The site is Python-generated HTML + vanilla CSS. Node is only needed for `npx wrangler` (worker deployment), which is a separate concern. |
| Any Python package manager beyond pip | No `poetry`, no `pipenv`, no `conda`. The build has zero Python dependencies. The only pip install is `resend` for Wave 4 email sends (server-side script, not build). |
| Any CSS preprocessor | No Sass, Less, PostCSS, or Tailwind. CSS custom properties handle everything. |
| Any frontend framework | No React, Vue, Svelte, Alpine.js. Zero client-side JS beyond the ~30-line newsletter signup handler and optional mobile nav toggle. |
| Any database | Data lives in Python dicts (Wave 1) and JSON files (Wave 2+). SQLite or Postgres would be pointless overhead. |
| Any image optimization pipeline | WebP images added manually. No sharp, no imagemin, no Pillow pipeline. If OG image generation is added later (Playwright), it runs separately. |
| Docker | Static HTML site. No containers needed for build or deploy. |

## Installation

```bash
# Core build — zero dependencies
python3 scripts/build.py

# Local preview
cd output && python3 -m http.server 8090

# Newsletter worker (one-time setup)
cd worker && npx wrangler deploy
npx wrangler secret put RESEND_API_KEY
npx wrangler secret put RESEND_AUDIENCE_ID

# Email sends (Wave 4 only, server-side)
pip install resend==2.23.0
```

## File Structure (Final)

```
gtmepulse/
├── .github/workflows/
│   └── deploy-site.yml          # GitHub Pages deploy
├── scripts/
│   ├── build.py                 # Data + page generators
│   ├── templates.py             # HTML components + schema helpers
│   └── nav_config.py            # Nav, footer, site constants
├── content/                     # Expanded prose modules (auto-discovered)
│   ├── salary_insights.py
│   └── ...
├── data/                        # JSON data files
│   ├── salary_data.json
│   └── ...
├── worker/
│   ├── subscribe.js             # Cloudflare Worker (newsletter signup)
│   └── wrangler.toml            # Worker config
├── assets/
│   ├── css/
│   │   ├── tokens.css           # Design tokens (BUILT)
│   │   ├── components.css       # Component styles
│   │   └── styles.css           # Page-specific styles
│   ├── logos/                   # SVG logo variants
│   ├── favicons/                # Favicon files
│   └── images/                  # Page images (WebP)
├── output/                      # Built site (gitignored)
├── CLAUDE.md                    # Build guide
└── PROMPT.md                    # Session starter
```

## Sources

- SultanOfSaaS reference implementation: `/Users/rome/Documents/projects/sultanofsaas/scripts/` (3-file pattern, 145 pages)
- b2bsalestools reference: `/Users/rome/Documents/projects/b2bsalestools/` (196 pages, same pattern)
- RevOps Report newsletter worker: `/Users/rome/Documents/revops_report/worker/subscribe.js` (production Cloudflare Worker + Resend)
- RevOps Report deploy workflow: `/Users/rome/Documents/revops_report/.github/workflows/deploy-site.yml`
- Resend Python SDK: [PyPI resend 2.23.0](https://pypi.org/project/resend/) (Feb 23, 2026)
- Wrangler CLI: [Cloudflare Workers docs](https://developers.cloudflare.com/workers/wrangler/) (v4.x, actively maintained)
- GitHub Pages Actions: [actions/deploy-pages@v4](https://github.com/actions/deploy-pages)
- Google Fonts: [Sora](https://fonts.google.com/specimen/Sora), [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans), [Source Code Pro](https://fonts.google.com/specimen/Source+Code+Pro)
