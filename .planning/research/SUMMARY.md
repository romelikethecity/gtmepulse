# Project Research Summary

**Project:** GTME Pulse (gtmepulse.com)
**Domain:** Programmatic SEO static site (niche salary data + tool reviews + career content)
**Researched:** 2026-03-10
**Confidence:** HIGH

## Executive Summary

GTME Pulse is a niche career intelligence site for the GTM Engineer role, built as a zero-dependency Python static site generator producing 200+ pages of salary data, tool reviews, career guides, and a glossary. The proven approach is a 3-file Python build system (build.py, templates.py, nav_config.py) that generates HTML from structured data and f-string templates, deployed to GitHub Pages via GitHub Actions. This exact pattern runs five production sites in the portfolio (SultanOfSaaS, b2bsalestools, Cannabisers, Provyx, RevOps Report), all generating 145-713 pages with zero external Python dependencies. The stack is locked: no frameworks, no templating engines, no CSS preprocessors, no JavaScript build tools.

The anchor differentiator is salary data for a role that has no BLS category, no Radford benchmark, and no established competitor covering it. Salary-by-company-stage pages (Seed through Enterprise) are pure whitespace that no competitor offers. The site monetizes through tool review affiliate links, newsletter sponsorships, and job board paid listings, not display ads. The newsletter infrastructure clones the production RevOps Report pattern (Cloudflare Worker + Resend API). The competitive landscape is wide open: neither gtmengineerclub.com (5 stale posts) nor gtmehq.com (Clay template shop) has salary data, tool comparisons, job boards, or glossary content.

The single biggest risk is Google's site-wide quality penalty from thin template pages. Programmatic SEO in 2026 requires 1,200+ words per page with 30-40% unique content differentiation between pages in the same template family. Launching 45 salary pages simultaneously with boilerplate content will poison the entire domain. The mitigation is clear: stagger launches (5-10 strong pages first), enforce content depth minimums, and build a deduplication validator into the build system that fails on identical meta tags. Secondary risk is salary data credibility; the methodology page must ship before any salary content pages.

## Key Findings

### Recommended Stack

Zero-dependency Python static site generator, cloned from production implementations. The entire build runs with `python3 scripts/build.py` using only stdlib modules (os, json, shutil, datetime). CSS uses custom properties (no Sass, no Tailwind). Newsletter signup handled by a Cloudflare Worker calling Resend Audiences API. Deployed to GitHub Pages with a standard Actions workflow.

**Core technologies:**
- **Python 3.12+ (stdlib only):** Static site generator. No pip dependencies for the build. Proven across 5+ production sites.
- **f-string HTML templates:** Page generation via Python functions returning HTML strings. No Jinja2, no Mako. Templates are code, not files.
- **3-layer CSS (tokens/components/styles):** Design tokens as CSS custom properties, component classes, page-scoped styles. tokens.css already built from brand kit.
- **Cloudflare Worker + Resend API:** Newsletter signup endpoint. Clone of production RevOps Report worker (~90 lines).
- **GitHub Pages + GitHub Actions:** Free static hosting with CI/CD. Proven deploy workflow exists.
- **Google Fonts (Sora, Plus Jakarta Sans, Source Code Pro):** Single combined request with display=swap and preconnect hints.

**What NOT to install:** Node.js (for site build), any CSS preprocessor, any frontend framework, any database, Docker, any Python package manager beyond pip.

### Expected Features

**Must have (table stakes):**
- Salary index page with aggregate stats (median, average, range, sample size)
- Salary breakdowns by seniority (4), location (15), company stage (5)
- 10 salary comparison pages (GTM Engineer vs X)
- FAQ sections with FAQPage schema on content pages
- Newsletter signup in 4 placements with contextual copy
- Breadcrumb navigation + BreadcrumbList schema
- Mobile-responsive design (375/768/1024 breakpoints)
- Auto-generated sitemap.xml + robots.txt
- About page with real author (E-E-A-T)
- Methodology/data sources page
- Clean directory-based URL structure
- Privacy policy + Terms (required for email collection)

**Should have (differentiators):**
- Salary by company stage (no competitor has this)
- Email-gated salary calculator (free preview + gated percentile breakdown)
- Contextual newsletter CTAs (2-3x conversion vs generic)
- Definition blocks on every page (therevopsreport.com pattern)
- Deep content (1,200-2,000 words per page, 30-40% unique)
- Job posting growth stats (205% YoY anchor stat)

**Defer (Wave 2+):**
- Tool reviews and comparisons (Wave 2, 80 pages, high writing effort)
- Career guides (Wave 3, 25 pages)
- 50-term glossary (Wave 3)
- Job board with live scraper data (Wave 4, needs scraper maturity)
- Week-over-week salary trend data (needs consistent scraper runs)
- Weekly email automation (Wave 4, needs subscriber base first)
- Tool stack correlation with salary (Wave 4+, needs enriched data volume)

**Anti-features (do NOT build):**
- User-submitted salary data, content paywalls, display ads, comment system, user accounts, client-side search, cookie consent banner, dark mode toggle UI, social share buttons, animated transitions, estimated salary schema (deprecated Sep 2025)

### Architecture Approach

The 3-file split pattern with content module auto-discovery. nav_config.py holds pure configuration (~100 lines). templates.py provides the HTML shell, schema helpers, and write_page() with automatic ALL_PAGES tracking for sitemap generation (~400 lines). build.py contains all structured data, page generator functions, and the build pipeline (~3,000-5,000 lines at scale). Content modules in content/ provide extended prose and are auto-discovered at build time; pages render with defaults when modules are missing, enabling incremental content depth.

**Major components:**
1. **nav_config.py** -- Site constants, navigation structure, footer columns. Pure data, zero logic.
2. **templates.py** -- HTML head/nav/footer/wrapper, write_page() + ALL_PAGES tracking, schema JSON-LD helpers (breadcrumb, FAQ, organization), newsletter CTA component.
3. **build.py** -- All salary/tool/career data as Python dicts, page generator functions (one per page type), build pipeline orchestrator (clean, copy assets, generate pages, sitemap, robots, CNAME).
4. **content/*.py** -- Auto-discovered prose modules keyed by slug. Graceful degradation: pages render without them.
5. **data/*.json** -- Volatile data from external sources (scraper exports, market stats). Loaded at build time.
6. **assets/css/** -- 3-layer cascade: tokens.css (variables only) -> components.css (reusable classes) -> styles.css (page-scoped via body class).
7. **worker/subscribe.js** -- Cloudflare Worker for newsletter signup (Resend Audiences API).

### Critical Pitfalls

1. **Site-wide quality poisoning from thin template pages** -- The #1 risk. Google's Helpful Content system penalizes the entire domain if template pages lack genuine differentiation. Enforce 1,200+ words with 30-40% unique content per page. Stagger launch: 5-10 strong pages first, expand after indexing proves quality signals.

2. **Duplicate meta tags across template pages** -- Near-identical titles/descriptions cause keyword cannibalization. Each title must include a unique data point ("$145K Median, 12% Above National Average"). Build a dedup validator into build.py that fails on duplicate titles or descriptions.

3. **Salary data credibility collapse** -- GTM Engineer has no BLS category. Publishing precise numbers without clear methodology will get torn apart by the community. Ship methodology page before salary content. Show sample sizes. Distinguish posted ranges from actual compensation. Add visible disclaimers.

4. **Malformed schema markup (silent failure)** -- JSON-LD breaks silently from unescaped quotes or missing commas. Use json.dumps() for all schema generation, never string concatenation. Add build-time JSON validation. Test with Google Rich Results Test before launch.

5. **Orphaned pages with weak internal linking** -- Template pages need 3+ contextual internal links beyond nav/footer. Build an explicit link graph mapping page relationships. Add "Related Salary Data" sections with 4-6 contextual links per page.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Build System Skeleton
**Rationale:** Every page depends on the template shell, CSS foundation, and write pipeline. Nothing can render without this.
**Delivers:** nav_config.py, templates.py skeleton (head/nav/footer/wrapper/write_page/schema helpers), components.css + styles.css foundation, build.py main() pipeline with asset copying.
**Addresses:** Mobile-responsive design, breadcrumb navigation, clean URL structure, sitemap/robots generation.
**Avoids:** CSS cascade conflicts (Pitfall 8) by establishing body-class scoping and zero-!important convention from day one.

### Phase 2: Core Static Pages
**Rationale:** Homepage, About, Newsletter, Privacy, Terms, and 404 prove the full pipeline end-to-end with simple pages. Newsletter infrastructure must work before the salary calculator can gate.
**Delivers:** 6 core pages + Cloudflare Worker for newsletter signup + Resend integration.
**Addresses:** About page (E-E-A-T), newsletter signup placements, privacy/terms (legal prerequisite for email collection).
**Avoids:** Sub-1% newsletter conversion (Pitfall 6) by building contextual CTAs from the start.

### Phase 3: Salary Data Engine
**Rationale:** Salary is the anchor differentiator and the content vertical with the most programmatic leverage (45 pages from data structures). The methodology page must ship first to establish credibility.
**Delivers:** Methodology page, salary index, 4 seniority pages, 15 location pages, 5 company-stage pages, 10 comparison pages, salary calculator with email gate. ~45 pages total.
**Addresses:** All table-stakes salary features, company-stage differentiator, email-gated calculator, definition blocks, deep content, FAQ sections.
**Avoids:** Quality poisoning (Pitfall 1) via staggered launch and content depth enforcement. Data credibility (Pitfall 3) via methodology-first approach. Duplicate meta (Pitfall 2) via build-time dedup validator. Mobile table breakage (Pitfall 7) via card-stack responsive pattern.

### Phase 4: Tool Reviews and Comparisons
**Rationale:** Separate content vertical with significant per-page writing effort. Depends on build system and CSS components being stable. Monetization via affiliate links starts here.
**Delivers:** 30 tool reviews, 8 category pages, 20 comparisons, 10 alternatives, 10 roundups. ~80 pages.
**Addresses:** Vendor-neutral tool reviews differentiator, affiliate revenue channel.
**Avoids:** AI-generated feel by requiring honest criticism and specific pricing in every review.

### Phase 5: Career Guides + Glossary
**Rationale:** Top-of-funnel capture and topical authority building. Lower priority than salary (the anchor) and tools (the monetization engine).
**Delivers:** 15 career guide pages, 50 glossary term pages. ~65 pages.
**Addresses:** "What is a GTM Engineer" definitional content, career path guides, skills breakdowns.
**Avoids:** Thin glossary pages tanking domain quality by enforcing 400+ words with examples per term.

### Phase 6: Job Board + Newsletter Automation + Insights
**Rationale:** Depends on scraper pipeline maturity and subscriber base. Currently only 7 tagged job postings; needs volume before a job board adds value.
**Delivers:** Job board page wired to scraper exports, weekly email automation, insight articles, WoW trend data on salary pages.
**Addresses:** Live job data differentiator, newsletter automation, recurring content.
**Avoids:** Stale job data by displaying "last scraped" date and handling zero-results gracefully.

### Phase Ordering Rationale

- Build system before content because every page depends on the template shell, CSS, and write pipeline.
- Core pages before salary because the newsletter signup flow must work before the calculator can gate results, and About/Privacy are prerequisites for email collection.
- Salary before tools because salary data is the primary differentiator (no competitor has it) while tool reviews are a crowded space. Salary pages also have higher programmatic leverage (45 pages from data dicts vs 30 individually-written reviews).
- Tools before career/glossary because tools generate affiliate revenue immediately, while career/glossary are authority-building plays with slower payoff.
- Job board last because it depends on scraper pipeline maturity (7 tagged postings today is insufficient) and benefits from an existing subscriber base for distribution.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3 (Salary Data):** Needs validation of salary numbers against current job posting data. Sample sizes per segment must be documented. Compensation definitions (base vs OTE vs TC) need a firm decision before data entry.
- **Phase 4 (Tool Reviews):** Affiliate program terms and signup processes need verification for each of the 30 tools. Review scoring methodology needs definition.
- **Phase 6 (Job Board + Automation):** Scraper pipeline integration points need mapping. Email send cadence and content format need testing with early subscribers.

Phases with standard patterns (skip research-phase):
- **Phase 1 (Build System):** Direct clone of SultanOfSaaS/b2bsalestools. Every pattern documented and proven.
- **Phase 2 (Core Pages):** Standard static pages + Cloudflare Worker clone from RevOps Report.
- **Phase 5 (Career + Glossary):** Standard programmatic SEO content pages using existing build system.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Exact pattern runs 5+ production sites. Zero unknowns. Every technology already in use. |
| Features | HIGH | Based on direct analysis of levels.fyi, Glassdoor, Built In, therevopsreport.com. Feature gaps and anti-features clearly identified. |
| Architecture | HIGH | Based on direct inspection of 2 production codebases (SultanOfSaaS 3,847 lines/145 pages, b2bsalestools 2,988 lines/196 pages). |
| Pitfalls | MEDIUM-HIGH | Programmatic SEO risks well-documented but Google's quality thresholds are a moving target. Salary data credibility is a real concern given no established benchmarks for this role. |

**Overall confidence:** HIGH

### Gaps to Address

- **Salary data validation:** The hardcoded salary numbers in build.py need cross-referencing against current job posting data from the scraper. Sample sizes per segment (especially smaller cities and company stages) may be too small for precise medians.
- **Scraper pipeline readiness:** Only 7 GTM Engineer jobs currently tagged. The job board and WoW trend features depend on significantly more data volume. Timeline for scraper maturity is unclear.
- **Email deliverability setup:** Domain verification in Resend for gtmepulse.com (SPF, DKIM, DMARC) not yet done. Must complete before any email sends.
- **Content differentiation at scale:** The 30-40% unique content requirement across 15 location pages and 10 comparison pages is a significant writing effort. Content modules help structurally, but each page still needs genuinely unique analysis paragraphs.
- **Analytics:** No analytics solution specified. Cloudflare Web Analytics (free, cookieless) is the obvious choice but needs explicit decision.
- **Canonical URL convention:** Need to pick trailing-slash convention and enforce it everywhere. Recommendation: with trailing slash (matches GitHub Pages default behavior with index.html files).
- **OG image generation:** Not needed for Wave 1 but Playwright-based approach is a separate pipeline to plan for later.

## Sources

### Primary (HIGH confidence)
- SultanOfSaaS production codebase: `/Users/rome/Documents/projects/sultanofsaas/scripts/` (3-file pattern, 145 pages, direct inspection)
- b2bsalestools production codebase: `/Users/rome/Documents/projects/b2bsalestools/` (196 pages, direct inspection)
- RevOps Report newsletter infrastructure: `/Users/rome/Documents/revops_report/worker/subscribe.js` (production Cloudflare Worker + Resend)
- GTME Pulse CLAUDE.md and PROJECT.md (architecture spec and requirements)
- Salary.com Data Subscription Agreement (legal reference for salary data publishing)
- Resend Python SDK: PyPI resend 2.23.0 (Feb 2026)
- GitHub Pages Actions: actions/deploy-pages@v4

### Secondary (MEDIUM confidence)
- levels.fyi, Glassdoor, Built In, therevopsreport.com (page structure, feature analysis, CTA patterns)
- Google Estimated Salary schema deprecation (September 2025, confirmed)
- Programmatic SEO guides (Backlinko, SEOmatic, Victorious) for content thresholds and internal linking patterns
- Google Helpful Content Update December 2025 analysis
- Newsletter signup conversion benchmarks (Omnisend, bdow.com)
- Common schema markup errors (Robert Celt, Zeo.org)
- CSS responsive table patterns (dev.to)

### Tertiary (LOW confidence)
- Glassdoor/Levels.fyi community discussions on salary data accuracy (anecdotal)

---
*Research completed: 2026-03-10*
*Ready for roadmap: yes*
