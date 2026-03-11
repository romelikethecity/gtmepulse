# GTME Pulse

## What This Is

An independent resource hub for GTM Engineers at gtmepulse.com. Vendor-neutral salary data, tool reviews and comparisons, career guides, glossary, job board, and weekly newsletter. Python static site generator following the therevopsreport.com model. All content attributed to Rome Thorndike.

## Core Value

GTM Engineers can find accurate, vendor-neutral salary benchmarks and career intelligence in one place, with data no competitor provides.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Build system skeleton (3-file Python split: build.py, templates.py, nav_config.py)
- [ ] CSS architecture (tokens.css + components.css + styles.css)
- [ ] Homepage with hero, stats grid, section previews, newsletter CTA
- [ ] About page (Rome Thorndike bio, site mission)
- [ ] Newsletter page with fully wired Resend signup via Cloudflare Worker
- [ ] Privacy policy and Terms of service pages
- [ ] 404 error page
- [ ] Salary index page with aggregate stats and links to all breakdowns
- [ ] 4 salary-by-seniority pages (Junior, Mid, Senior, Lead/Staff)
- [ ] 15 salary-by-location pages (SF, NYC, Austin, Seattle, Boston, Denver, Chicago, LA, Miami, Atlanta, Portland, DC, Dallas, San Diego, Remote)
- [ ] 5 salary-by-company-stage pages (Seed, Series A, Series B, Growth, Enterprise)
- [ ] 10 salary-vs-comparison pages (GTM Engineer vs RevOps, Sales Ops, Growth Engineer, SDR, Solutions Engineer, Marketing Ops, Sales Engineer, Data Engineer, Product Manager, AE)
- [ ] Salary calculator page (email-gated full results)
- [ ] Salary methodology page
- [ ] Newsletter infrastructure (Cloudflare Worker + Resend Audiences integration)
- [ ] Auto-generated sitemap.xml, robots.txt, CNAME
- [ ] BreadcrumbList schema on all inner pages
- [ ] FAQPage schema on salary comparison and breakdown pages
- [ ] Organization + WebSite schema on homepage
- [ ] 3+ internal links per page beyond nav/footer
- [ ] Mobile-responsive design (375px, 768px, 1024px breakpoints)

### Out of Scope

- Tool review pages (30 tools) — Wave 2
- Tool comparison pages (20 matchups) — Wave 2
- Career guide pages (~15 pages) — Wave 3
- Glossary pages (50 terms) — Wave 3
- Job board page — Wave 4
- Insight articles — Wave 4
- Email generation + weekly send automation — Wave 4
- OG image auto-generation via Playwright — future enhancement
- Dark mode toggle UI — tokens.css has dark mode variables but no toggle needed for v1

## Context

**GTM Engineer** is a technical, hybrid B2B SaaS role that builds automated outbound/revenue systems using Clay, Apollo, AI APIs, and workflow automation. 205% YoY job posting growth (2024-2025). 3,000+ open roles. $132K-$250K salary range.

**Competitive landscape:** gtmengineerclub.com (5 stale posts), gtmehq.com (Clay template shop, mostly vaporware). Neither has salary data, tool comparisons, job board, or glossary. Wide open.

**Reference implementations:**
- therevopsreport.com (CRO Report) — salary page structure, newsletter worker pattern
- SultanOfSaaS — template architecture, 3-file build system, content module pattern

**Brand:** "Volt" direction. Light-mode dominant, #FF4F1F orange-red accent, Sora/Plus Jakarta Sans/Source Code Pro fonts. All brand assets (logos, favicons, tokens.css, OG template) already in project.

**Data source:** Salary benchmarks hardcoded in build.py for Wave 1. Job board data will come from unified scraper (gtme audience, id=8, 21 search terms) in Wave 4.

**Newsletter:** "The GTME Pulse" via Resend + Cloudflare Worker. Signup form on site, automated Monday sends from scraper data (Wave 4).

**Monetization:** Tool affiliate links (Apollo 15-20%, Instantly 20-40%, Clay $50), newsletter sponsorships, job board paid listings, email-gated salary calculator.

## Constraints

- **Tech stack**: Python static site generator only. No frameworks, no JS build tools, no databases.
- **Hosting**: GitHub Pages + Cloudflare DNS. Output to `output/` directory.
- **Content depth**: No thin pages. Every salary page must have 1,200-2,000 words with stats, market context, comp drivers, FAQ, and related links.
- **Writing rules**: No em-dashes, no false reframes, no banned AI words (see CLAUDE.md), no spaces in stat numbers.
- **SEO**: Every page needs title (50-60 chars), description (150-158 chars), canonical URL, schema markup, and internal links.
- **Brand**: Must use tokens.css variables. Sora for headings, Plus Jakarta Sans for body, Source Code Pro for data/stats.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Hardcode salary data in build.py | No external data source yet; move to JSON when scraper data available | — Pending |
| 3-file Python split (build/templates/nav_config) | Proven pattern from SultanOfSaaS; easy to maintain at scale | — Pending |
| Resend + Cloudflare Worker for newsletter | Same stack as therevopsreport.com; Rome already has Resend account and Workers setup | — Pending |
| Wave ordering (salary first) | Salary data is the anchor differentiator; no competitor has it | — Pending |
| Email-gate salary calculator only | Keep most content free for SEO; gate the high-value interactive tool | — Pending |

---
*Last updated: 2026-03-10 after initialization*
