# GTME Pulse — Build Guide

## Project

**Site:** gtmepulse.com
**What:** Independent resource hub for GTM Engineers — salary data, tool reviews, job market analysis, career guides, weekly insights
**Model:** therevopsreport.com pattern. Vendor-neutral (not affiliated with Clay, Apollo, or any tool vendor)
**Audience:** Technical B2B SaaS professionals, $130K–$250K salary range. Builders, not managers. They value speed, automation, data, cutting through noise.
**Hosting:** GitHub Pages + Cloudflare DNS
**Build:** `python3 scripts/build.py` → all pages to `output/`
**Preview:** `cd output && python3 -m http.server 8090` → http://localhost:8090/

---

## Architecture

### File Structure
```
gtmepulse/
├── scripts/
│   ├── build.py          # Main build (data + page generators)
│   ├── templates.py      # Reusable HTML components + schema helpers
│   └── nav_config.py     # Navigation, footer, site constants
├── content/              # Expanded prose (auto-discovered .py modules)
│   ├── tools_crm.py      # Tool review content by category
│   ├── comparisons.py    # Comparison article content
│   ├── salary_insights.py
│   └── ...
├── data/                 # External/frequently updated data (JSON)
│   ├── salary_data.json  # Salary benchmarks
│   ├── job_postings.json # Job market data
│   └── ...
├── assets/
│   ├── css/
│   │   ├── tokens.css    # Design tokens (from brand kit)
│   │   ├── components.css # Reusable component styles
│   │   └── styles.css    # Page-specific styles
│   ├── logos/            # All logo variants (SVG)
│   ├── favicons/         # All favicon files
│   └── images/           # Page images (WebP preferred)
├── og-templates/         # OG image HTML templates
├── docs/                 # Head snippet, reference docs
├── output/               # Built site (gitignored)
├── CLAUDE.md             # This file
└── PROMPT.md             # Copy-paste prompt for new sessions
```

### Build System Pattern
- **3-file Python split:** `build.py` (data + generators), `templates.py` (HTML components), `nav_config.py` (nav/footer/constants)
- **Content modules:** `content/` directory with auto-discovery via `_load_content()`. Structural data (tool names, scores, categories) in build.py. Prose (overview paragraphs, expanded analysis) in content modules. Pages render with defaults if content module missing.
- **JSON for volatile data:** Salary benchmarks, job posting counts, market stats live in `data/` as JSON. Updated independently of build code.
- **Page tracking:** Every page appends to `ALL_PAGES` list for auto-sitemap generation.
- **Write helper:** `write_page(path, title, description, content)` in templates.py composes full HTML via `get_page_wrapper()`.

### CSS Architecture
- `tokens.css` — Design tokens/variables (from brand kit, includes dark mode)
- `components.css` — Reusable component styles (cards, buttons, tags, tables, badges)
- `styles.css` — Page-specific styles (hero, salary pages, tool pages, etc.)
- Cache bust via `?v=N` query param on CSS links. Increment `CSS_VERSION` in nav_config.py on every CSS change.

### Template Functions (templates.py)
Required exports:
- `get_html_head(title, description, canonical_path, og_image)` — meta tags, favicons, fonts, CSS
- `get_nav_html()` — responsive nav with dropdowns
- `get_footer_html()` — footer with columns, newsletter CTA
- `get_page_wrapper(title, description, canonical_path, body_content, og_image)` — full page assembly
- `write_page(filepath, title, description, body_content, canonical_path, og_image)` — write to disk + track in ALL_PAGES
- `breadcrumb_html(crumbs)` — visual breadcrumb
- `breadcrumb_schema(crumbs)` — BreadcrumbList JSON-LD
- `faq_schema_and_html(qa_pairs)` — FAQPage schema + visible FAQ section
- `newsletter_cta_html(context)` — contextual email capture block
- `definition_block(term, definition)` — glossary-style definition

### Navigation (nav_config.py)
Required exports:
- `SITE_NAME = "GTME Pulse"`
- `SITE_URL = "https://gtmepulse.com"`
- `SITE_TAGLINE` — main tagline
- `CTA_HREF` — primary CTA destination
- `CTA_LABEL` — primary CTA text
- `CSS_VERSION` — cache bust integer
- `NAV_ITEMS` — list of dicts with `href`, `label`, optional `children` for dropdowns
- `FOOTER_COLUMNS` — dict of column name to list of `{href, label}` links

---

## Brand Identity: Volt

Light-mode dominant, Swiss-precision layout, searing orange-red accent. "Stripe's design team built a career intelligence platform."

### Colors
| Token | Hex | Usage |
|---|---|---|
| `--gtme-accent` | `#FF4F1F` | Primary accent — buttons, links, highlights, logo "Pulse" |
| `--gtme-bg-primary` | `#FAFAFA` | Page background |
| `--gtme-bg-surface` | `#FFFFFF` | Cards, elevated surfaces |
| `--gtme-bg-tinted` | `#FFF0EB` | Accent-tinted backgrounds (CTAs, callouts) |
| `--gtme-bg-dark` | `#111111` | Dark sections, footer, OG cards |
| `--gtme-text-primary` | `#111111` | Headings, body text |
| `--gtme-text-secondary` | `#6B6B6B` | Descriptions, meta |

Full token set in `assets/css/tokens.css`. Includes dark mode via `prefers-color-scheme` and `data-theme="dark"`.

### Competitive Distance
- Clay: coral `#FF6B6B` — ours is hotter, more saturated
- Apollo: blue — no overlap
- therevopsreport: green — no overlap

### Typography
| Role | Font | Weights |
|---|---|---|
| Headings | **Sora** | 400, 500, 600, 700 |
| Body | **Plus Jakarta Sans** | 400, 500, 600, 700, 800 |
| Code/Data | **Source Code Pro** | 400, 500, 600, 700 |

Rules: Sora 700 for headings (letter-spacing -0.5px to -1px). Plus Jakarta Sans 400 for body (line-height 1.65–1.75). Source Code Pro for data labels, stat numbers, tool names, inline code.

### Logo
- **Full mark:** Icon (orange rounded square + white pulse waveform) + "GTME" dark + "Pulse" orange
- **Files:** `assets/logos/logo-horizontal-light.svg` (light bg), `logo-horizontal-dark.svg` (dark bg), `icon-mark.svg`, `wordmark-*.svg`
- **Favicon:** `assets/favicons/` — SVG, ICO, PNGs, apple-touch, android-chrome, webmanifest

---

## Page Types & Site Structure

### Phase 1 Target: ~200+ pages

**Core pages (5):**
- Homepage (hero + stats + sections)
- About
- Newsletter
- Privacy, Terms

**Salary pages (~45):**
- Salary index
- By seniority (Junior, Mid, Senior, Lead/Staff) — 4 pages
- By location (top 15 tech hubs) — 15 pages
- By company stage (Seed, Series A, Series B, Growth, Enterprise) — 5 pages
- GTM Engineer vs X salary comparisons (vs RevOps, vs Sales Ops, vs Growth Engineer, vs SDR, etc.) — 10 pages
- Salary calculator page (email-gated full results)
- Methodology page

**Tool pages (~80):**
- Tools index
- Category index + category pages (8 categories: Data Enrichment, Outbound Sequencing, CRM, Workflow Automation, AI/LLM, Intent Data, Analytics, LinkedIn Tools) — 9 pages
- Individual tool reviews (30 tools) — 30 pages
- X vs Y comparisons (20 matchups) — 20 pages
- "Best for" roundups (Best for Startups, Best for Enterprise, Best Free, etc.) — 10 pages
- Alternatives pages (Clay alternatives, Apollo alternatives, etc.) — 10 pages

**Career pages (~25):**
- Career guide index
- "What is a GTM Engineer?" definitive guide
- "How to Become a GTM Engineer" (career path)
- "GTM Engineer Job Description Template"
- "GTM Engineer Interview Questions"
- "GTM Engineer vs RevOps" (role comparison)
- "GTM Engineer vs Sales Engineer"
- "GTM Engineer vs Growth Engineer"
- "SDR to GTM Engineer Career Switch"
- Skills breakdown pages (Clay, Python, API integration, etc.)
- Resume/portfolio guide
- Freelance/consulting guide
- Remote GTM Engineer guide
- Additional career articles — ~12 pages

**Glossary (~50):**
- Glossary index
- Individual term pages — 50 pages

**Insights/Articles (~20):**
- Articles index
- Data-driven articles (job market analysis, tool trends, salary reports)
- Playbooks and how-to guides
- Weekly/monthly pulse reports

---

## Writing Standards

### Voice
Direct, analytical, occasionally wry. "Smart friend who cuts through the noise." Practitioner-first — write like someone who has actually built these systems, not someone reporting on them from the outside.

- Use contractions always (it's, don't, won't)
- Vary sentence length dramatically. Short punches. Then longer context.
- State opinions confidently when backed by evidence
- Give real answers, not "it depends"
- Every tool review includes honest criticism
- Specific numbers always: "$132K median" not "six figures"
- Name competitors and make direct comparisons
- Reference real job posting data when available

### HARD RULES — ZERO TOLERANCE

**1. NEVER use false reframes.**
Banned: "not X, it's Y" / "isn't X. It's Y." / "less about X and more about Y" / "The pattern isn't X. It's Y."
Just say what the thing IS. Directly.

**2. NEVER use em-dashes.**
Use periods, commas, or restructure.

**3. Banned words/phrases:**
- robust, leverage, synergy, holistic, cutting-edge, seamless, game-changer, paradigm shift, revolutionary
- genuinely, truly, really, actually, quite, extremely
- unlock, unleash, enhance, exceed, empower, supercharge, harness, spearhead, delve
- landscape, tapestry, frontier, resonates, positioning
- "continues to", "in today's market", "navigate the landscape"
- "X, full stop.", "at the end of the day", "it's worth noting"
- "Let's dive in", "Let's explore", "In today's fast-paced..."
- "It's important to note that...", "First and foremost"
- "In conclusion", "To summarize"
- leverage (use "use"), utilize (use "use")
- "Basically", "Essentially"

**4. AI writing tells to avoid:**
- Uniform section lengths (vary dramatically)
- "Here's the thing:" / "The bottom line is this:" / "That matters because" (just state it)
- "That's either X or Y. Probably both." (delete)
- Patronizing: "That's not inherently good or bad" / "This is something to keep in mind" (delete)
- Dramatic dichotomies: "exciting if X, terrifying if Y" (just describe it)
- Tautologies: "Time will tell" / "Success depends on execution" (delete)
- Transition words as openers: "So," "Meanwhile," "Additionally" (start with the point)

**5. What reads as human:**
- Punchy metaphors and visceral imagery
- Personal anecdotes (brief setup, tight story, pivot to insight)
- Spicy takes with evidence
- Rhythmic summaries: "Own the data. Own the pipeline. Own the meeting."
- Naming the era: "We're in the year of the one-person GTM team"

### Copywriting Principles

**Three tests for every line:**
1. Can I visualize it?
2. Can I falsify it?
3. Can nobody else say this?

**The SO WHAT chain:** Feature → Functional benefit → Financial benefit → Emotional benefit. Write from the emotional end.

**Title rules:** Under 8 words / 44 characters max. A caveman should grunt back what you offer.

**CTA rules:** Call to VALUE not action. "See My Salary Range" not "Submit." First-person CTAs outperform ("Get My Report" vs "Get Your Report").

**Rhythm:** Short. Then breathe. Land it.

**Above the fold (Harry Dry formula):**
1. Title — explain value (VALUE + OBJECTION hook for most pages)
2. Subtitle — explain HOW
3. Visual — show the product/data in action (no stock photos)
4. Social proof — metrics, logos, stats
5. CTA — call to value, handle objections

### Content Length Targets
- Tool reviews: 1,500–2,500 words
- X vs Y comparisons: 3,000–5,000 words
- Salary pages: 1,200–2,000 words
- Career guides: 2,000–3,500 words
- Glossary terms: 300–600 words
- Insight articles: 1,500–2,500 words

---

## SEO Standards

### Meta Tags (every page)
- `<title>`: 50-60 chars, keyword-first, hyphens not pipes
- `<meta name="description">`: 150-158 chars, action-oriented, unique per page
- `<link rel="canonical">`: absolute URL, `https://gtmepulse.com/[path]`
- H1: one per page, 46-60 chars
- OG + Twitter Card tags with unique title/description/image per page

### Schema Markup (JSON-LD)
- Homepage: Organization + WebSite (@graph pattern)
- Inner pages: BreadcrumbList
- FAQ pages: FAQPage (min 3 Q&A, must match visible content)
- Tool reviews: SoftwareApplication
- Articles: Article with author Person
- Salary pages: structured data where applicable

### Content Quality
- 3+ internal links per page beyond nav/footer
- 2+ outbound links to authoritative sources per content page
- Related links section at bottom of every content page
- FAQ section on every comparison, alternative, and career guide page
- Every stat needs an authoritative source citation
- Heading hierarchy: h1 > h2 > h3, never skip levels

### Pain Stats Formatting
- NO SPACES in stat numbers (causes mobile line wrapping)
- Good: `30%`, `$132K`, `24&#8209;48hr`, `18mo`, `3,000+`
- Bad: `13 hrs`, `84 days`, `24-48 hr`
- Use `&#8209;` for non-breaking hyphens

### Technical
- All images: width/height attributes (prevents CLS)
- Lighthouse targets: Performance 90+, Accessibility 90+, SEO 100
- sitemap.xml + robots.txt auto-generated by build
- CNAME file auto-generated (gtmepulse.com)

---

## Tool Categories & Initial Tool List

### Categories (8)
1. **Data Enrichment & Orchestration** — Clay, Apollo, ZoomInfo, Clearbit, FullEnrich, Lusha, Cognism, LeadIQ, Persana
2. **Outbound Sequencing** — Instantly, Smartlead, Outreach, Salesloft, Lemlist, HeyReach, Woodpecker
3. **CRM** — HubSpot, Salesforce, Pipedrive, Close, Attio
4. **Workflow Automation** — Make, n8n, Zapier, Tray.io
5. **AI & LLM Tools** — Claude, ChatGPT/OpenAI, Perplexity
6. **Intent & Signal Data** — 6sense, Bombora, G2, TrustRadius, Hightouch, Census
7. **Analytics & Product Signals** — Mixpanel, Amplitude, Segment, PostHog
8. **LinkedIn & Social** — LinkedIn Sales Navigator, PhantomBuster, Dripify, Expandi

### Initial Comparisons (20)
Clay vs Apollo, Clay vs ZoomInfo, Instantly vs Smartlead, Outreach vs Salesloft, HubSpot vs Salesforce, Make vs n8n, Make vs Zapier, Apollo vs ZoomInfo, Lemlist vs Instantly, Clay vs Clearbit, 6sense vs Bombora, Mixpanel vs Amplitude, Close vs Pipedrive, HeyReach vs Expandi, Segment vs PostHog, Hightouch vs Census, LinkedIn Sales Nav vs Apollo, Cognism vs ZoomInfo, LeadIQ vs Lusha, Smartlead vs Lemlist

---

## Monetization

### Affiliate Programs
| Tool | Commission | Type |
|---|---|---|
| Apollo.io | 15-20% first year revenue | Recurring |
| Instantly.ai | 20-40% (tiered) | Recurring monthly |
| Clay | $50 per sale | One-time |
| Smartlead | Active program | Recurring |
| Lemlist | Active program | Recurring |

### Revenue Channels
1. Tool affiliate links in reviews/comparisons
2. Newsletter sponsorships (high-value B2B audience)
3. Job board (paid listings from hiring companies)
4. Email-gated salary calculator/reports

---

## Author

**Rome Thorndike** — all content attributed to Rome Thorndike. Use for author bios, article bylines, schema Person markup, and About page.

---

## Newsletter Strategy

**Platform:** Resend (API-based email sending + subscriber storage) + Cloudflare Worker (signup endpoint)
**Name:** The GTME Pulse
**From:** `insights@gtmepulse.com` (verify domain in Resend)
**Signup hook:** "Weekly GTM Engineer job market data, salary shifts, and tool intel."
**Schedule:** Every Monday (stagger 1-2 hours after RevOps Report send to avoid overlap)
**Fully automated — zero manual steps.**

### Architecture (clone of therevopsreport.com pattern)

**Signup flow:**
1. Static HTML form on site calls `handleSignup()` JS function
2. JS POSTs `{email: "..."}` to Cloudflare Worker at `gtme-newsletter-signup.rome-workers.workers.dev`
3. Worker validates email, calls Resend Audiences API to add contact
4. Signup placements: hero CTA, inline after salary data, sticky footer, dedicated /newsletter page

**Data pipeline (already built):**
1. Unified scraper runs Tue/Fri 8 PM PST on server
2. Exports `gtme` audience data: `jobs.json`, `market_intelligence.json`, `comp_analysis.json`
3. Pushes to gtmepulse repo → GitHub Pages deploys

**Email generation + send (Monday cron):**
1. `scripts/generate_weekly_email.py` loads latest `data/market_intelligence.json` + `data/comp_analysis.json`
2. Loads `data/previous_market_snapshot.json` for week-over-week diffs
3. Computes changes: total GTME job count, median salary shifts, top hiring companies, tool mention frequencies, hiring signals
4. Renders branded HTML email with trend arrows, tables, data highlights
5. Fetches subscriber list from Resend Audiences API
6. Sends to each subscriber via `resend.Emails.send()`
7. Saves current data as new snapshot for next week's diff

**Server cron:** `0 18 * * 1` (18:00 UTC = 10:00 AM PST every Monday)

### Key files to build
| File | Purpose |
|---|---|
| `worker/subscribe.js` | Cloudflare Worker — form POST → Resend Audiences |
| `worker/wrangler.toml` | Worker config (name: `gtme-newsletter-signup`) |
| `scripts/generate_weekly_email.py` | Email content generator + sender |
| `scripts/send_weekly_email.sh` | Monday cron script |
| `.env` | `RESEND_API_KEY`, `RESEND_AUDIENCE_ID` |

### Setup steps
1. Create new Resend Audience for GTME Pulse (same Resend account as RevOps Report)
2. Verify `gtmepulse.com` domain in Resend (DNS records)
3. Clone `worker/subscribe.js` from revops_report, update audience ID
4. Deploy worker: `cd worker && npx wrangler deploy`
5. Set worker secrets: `wrangler secret put RESEND_API_KEY` + `RESEND_AUDIENCE_ID`
6. Build `generate_weekly_email.py` (clone revops pattern, GTME branding)
7. Add Monday cron on server

### Reference implementation
RevOps Report newsletter code at `/Users/rome/Documents/revops_report/`:
- `worker/subscribe.js` — signup worker
- `scripts/generate_weekly_email.py` — email generator + sender
- `scripts/send_weekly_email.sh` — cron script
- `scripts/templates.py` line 41 (`SIGNUP_WORKER_URL`) + line 1191 (`handleSignup()`)

---

## Job Board

**Data source:** Unified job scraper at `/Users/rome/Documents/projects/scrapers/master/`
**Audience:** `gtme` (audience id=8, created 2026-03-10)
**Pipeline:** Scraper runs Tue/Fri → tags jobs → exports to `data/` in gtmepulse project
**Search terms (21):** GTM Engineer, Go-to-Market Engineer, Senior/Lead/Staff/Principal GTM Engineer, Head of/Director/VP GTM Engineering, GTM Systems/Automation Engineer, Revenue Engineer, Growth Engineer, Marketing/Sales Automation Engineer, Outbound/Pipeline/Revenue Systems/GTM Operations Engineer

**Classification rules:** `title_must_contain` with GTM/revenue/growth engineer variants. Excludes traditional engineering (civil, mechanical, software, DevOps, etc.) via `title_must_not_contain`.

**Display:** Cards with title, company, location, salary range (when disclosed), remote badge. Aggregate stats banner (total roles, avg salary, % remote, WoW change). Filter by seniority, location, remote.

**Export format:** `StandardExporter` produces CSV + JSON + market_intelligence.json + comp_analysis.json. The comp_analysis.json feeds salary pages directly.

**Current data:** 7 jobs tagged from existing scrapes. Will grow significantly once new search terms are actively scraped (next server cron run).

---

## Build Phases (Go Deep)

No thin pages. Every page built to full content depth before moving to the next wave.

### Wave 1: Foundation + Salary (THE ANCHOR)
Build system skeleton, then salary pages as the first content vertical.

**Build system:**
- `scripts/build.py` — data + page generators
- `scripts/templates.py` — HTML components + schema helpers
- `scripts/nav_config.py` — nav, footer, site constants
- `assets/css/components.css` + `assets/css/styles.css`
- Homepage (hero + stats + section previews)
- Newsletter page (Resend signup form via Cloudflare Worker)
- About page (Rome Thorndike bio)
- Privacy, Terms, 404

**Salary pages (~45):**
- Salary index (aggregate stats, links to all breakdowns)
- By seniority: Junior, Mid, Senior, Lead/Staff — 4 pages
- By location: SF, NYC, Austin, Seattle, Boston, Denver, Chicago, LA, Miami, Atlanta, Portland, DC, Dallas, San Diego, Remote — 15 pages
- By company stage: Seed, Series A, Series B, Growth, Enterprise — 5 pages
- Vs comparisons: GTM Engineer vs RevOps, vs Sales Ops, vs Growth Engineer, vs SDR, vs Solutions Engineer, vs Marketing Ops, vs Sales Engineer, vs Data Engineer, vs Product Manager, vs AE — 10 pages
- Salary calculator page (email-gated full results via Resend signup)
- Methodology page

### Wave 2: Tools
- Tool reviews (30 tools across 8 categories) — deep reviews with honest criticism
- Category index + 8 category pages
- X vs Y comparisons (20 matchups)
- Alternatives pages (10)
- "Best for" roundups (10)

### Wave 3: Career + Glossary
- Career guide pages (~15): What is a GTME, how to become one, interview questions, role comparisons, skills, freelancing, remote guide
- Glossary (50 terms)

### Wave 4: Insights + Job Board
- Job board page (wired to scraper exports)
- Insight articles (job market analysis, tool trends, weekly pulse reports)
- Remaining content pages

---

## Canonical Domain & Deployment

- **Always:** `https://gtmepulse.com` (no www)
- **CNAME:** `gtmepulse.com`
- **Repo:** `romelikethecity/gtmepulse` (private)
- **Deploy:** Push to main → GitHub Pages serves `output/`

---

## What GTM Engineers Are

For context when writing content:

**GTM Engineer** is a technical, hybrid role that builds automated outbound/revenue systems using AI + APIs + data pipelines. They replace manual SDR work with code and automation. Clay coined the term in 2023; it exploded in 2024-2025.

**They are NOT:** General "go to market" strategists, marketing managers, or traditional sales ops. They are builders who write code, configure workflows, and architect data pipelines.

**Core stack:** Clay (center of gravity, appears in 69% of job postings), Apollo, Instantly/Smartlead, Make/n8n, Python, LLM APIs (Claude/OpenAI), HubSpot/Salesforce.

**Key stats:** 205% YoY job posting growth (2024→2025). 3,000+ open roles. $132K–$250K salary range. ~100 new listings/month.

**Key people:** Varun Anand (Clay co-founder, originated role), Eric Nowoslawski (Clay's first visible GTME), Nathan Lippi (Clay Bootcamp), Matteo Tittarelli (GTM Engineer School).

**Competitors:** gtmengineerclub.com (5 stale blog posts), gtmehq.com (Clay template shop, mostly vaporware). Neither has salary data, tool comparisons, job board, or glossary. Wide open.
