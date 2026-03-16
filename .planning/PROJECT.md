# GTME Pulse

## What This Is

An independent resource hub for GTM Engineers at gtmepulse.com. Vendor-neutral salary data, tool reviews and comparisons, career guides, glossary, job board, and weekly newsletter. Python static site generator following the therevopsreport.com model. All content attributed to Rome Thorndike.

## Core Value

GTM Engineers can find accurate, vendor-neutral salary benchmarks and career intelligence in one place, with data no competitor provides.

## Current State

**v3.0 shipped 2026-03-16.** 263 pages live. Zero build warnings. Full tool review vertical complete with newsletter infrastructure.

**What shipped in v3.0:**
- 30 tool reviews across 8 categories with SoftwareApplication JSON-LD and honest criticism
- 8 category index pages + 20 head-to-head comparisons with FAQPage schema
- 10 alternatives pages + 10 "best for" roundup pages
- 50 glossary term pages with definitions, category grouping, and cross-linking
- Job board page with filterable cards, stats banner, and scraper data pipeline
- Newsletter infrastructure: Cloudflare Worker signup, weekly email generator, Monday cron
- QUAL3 schema validation (SoftwareApplication on reviews, FAQPage on comparisons/alternatives/roundups)

**Cumulative site stats:**
- 263 pages, zero validation warnings
- ~13,300 LOC Python (build system) + ~5,500 LOC content modules
- 3 milestones shipped (v1.0, v2.0, v3.0) across 12 phases, 33 plans

## Requirements

### Validated

- ✓ Build system skeleton (3-file Python split) — v1.0
- ✓ CSS architecture (tokens.css + components.css + styles.css) — v1.0
- ✓ Homepage, About, Newsletter, Privacy, Terms, 404 pages — v1.0
- ✓ 45 salary pages (seniority, location, stage, vs comparisons, calculator, methodology) — v1.0
- ✓ Newsletter signup via Cloudflare Worker + Resend — v1.0, v3.0
- ✓ Auto-generated sitemap.xml, robots.txt, CNAME — v1.0
- ✓ BreadcrumbList + FAQPage + Organization/WebSite schema — v1.0
- ✓ Salary data overhaul with real State of GTME Report 2026 data (n=228) — v2.0
- ✓ 28 career/agency/job-market pages — v2.0
- ✓ 25 tools and benchmarks pages + 6 comparisons — v2.0
- ✓ 14 blog articles — v2.0
- ✓ Site-wide quality validation (9 QUAL2 categories) — v2.0
- ✓ 30 tool reviews with SoftwareApplication schema — v3.0
- ✓ 8 category indexes + 20 comparisons with FAQPage schema — v3.0
- ✓ 10 alternatives + 10 roundup pages — v3.0
- ✓ 50 glossary terms — v3.0
- ✓ Job board with filterable cards and scraper pipeline — v3.0
- ✓ Weekly email generator + automated Monday cron — v3.0
- ✓ QUAL3 schema validation, zero-warning build — v3.0

### Active

(None — planning next milestone)

### Out of Scope

- OG image auto-generation via Playwright — future enhancement
- Dark mode toggle UI — tokens.css has dark mode variables but no toggle needed
- Smart newsletter personalization — standard broadcast for now
- Paid job board listings — manual JSON for now, payment integration later

## Context

**GTM Engineer** is a technical, hybrid B2B SaaS role that builds automated outbound/revenue systems using Clay, Apollo, AI APIs, and workflow automation. 205% YoY job posting growth (2024-2025). 3,000+ open roles. $132K-$250K salary range.

**Competitive landscape:** gtmengineerclub.com (5 stale posts), gtmehq.com (Clay template shop, mostly vaporware). Neither has salary data, tool comparisons, job board, or glossary. Wide open.

**Tech stack:** Python static site generator, GitHub Pages + Cloudflare DNS, Cloudflare Worker for newsletter, Resend for email.

**Data sources:** State of GTME Report 2026 (n=228), Clay Job Data (3,342 postings), unified scraper (gtme audience, 21 search terms).

**Monetization:** Tool affiliate links (Apollo 15-20%, Instantly 20-40%, Clay $50), newsletter sponsorships, job board paid listings, email-gated salary calculator.

## Constraints

- **Tech stack**: Python static site generator only. No frameworks, no JS build tools, no databases.
- **Hosting**: GitHub Pages + Cloudflare DNS. Output to `output/` directory.
- **Content depth**: No thin pages. Every page must meet minimum word counts per type.
- **Writing rules**: No em-dashes, no false reframes, no banned AI words (see CLAUDE.md).
- **SEO**: Every page needs title (50-60 chars), description (150-158 chars), canonical URL, schema markup.
- **Brand**: Amber dark-mode-first. tokens.css variables. Sora/Plus Jakarta Sans/Source Code Pro fonts.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Hardcode salary data in build.py | No external data source yet; move to JSON when scraper data available | ✓ Good (v1.0), migrated to real data (v2.0) |
| 3-file Python split (build/templates/nav_config) | Proven pattern from SultanOfSaaS; easy to maintain at scale | ✓ Good |
| Resend + Cloudflare Worker for newsletter | Same stack as therevopsreport.com; Rome already has Resend account and Workers setup | ✓ Good |
| Wave ordering (salary first) | Salary data is the anchor differentiator; no competitor has it | ✓ Good |
| Email-gate salary calculator only | Keep most content free for SEO; gate the high-value interactive tool | ✓ Good |
| Use real State of GTME Report data | First-party survey data (n=228) is more credible than hardcoded estimates | ✓ Good |
| Content modules in content/ directory | Keep build.py manageable as page count grows; auto-discovery via importlib | ✓ Good |
| JSON data files in data/ directory | Separate volatile data from build code; scraper writes JSON, build reads it | ✓ Good |
| Category index intros inlined in data dicts | 150-300 words per category, not worth separate content modules | ✓ Good |
| Reuse salary CSS classes for tool/glossary pages | Avoid CSS bloat; salary-header/salary-content work for all data-heavy pages | ✓ Good |

---
*Last updated: 2026-03-16 after v3.0 milestone*
