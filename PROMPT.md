# GTME Pulse — Session Start Prompt

Copy and paste everything below this line into a new Claude Code session to start building.

---

I'm building **GTME Pulse** (gtmepulse.com), an independent resource site for GTM Engineers. Read the CLAUDE.md at `/Users/rome/Documents/projects/gtmepulse/CLAUDE.md` for the full build guide — brand identity, architecture, writing standards, SEO rules, page plan, and phase ordering.

**Quick context:** GTM Engineers are technical B2B SaaS roles that build automated outbound/revenue systems using Clay, Apollo, AI APIs, and workflow automation. This site follows the therevopsreport.com model: salary data, tool reviews/comparisons, career guides, glossary, job board, and weekly insights. Vendor-neutral. Author: Rome Thorndike.

**Architecture:** Python static site generator. 3-file split: `scripts/build.py` (data + page generators), `scripts/templates.py` (HTML components + schema helpers), `scripts/nav_config.py` (nav, footer, site constants). Content modules in `content/` directory. JSON data in `data/`. Output to `output/`. Preview at http://localhost:8090/.

**Brand:** "Volt" direction. Light-mode dominant, `#FF4F1F` orange-red accent, Sora/Plus Jakarta Sans/Source Code Pro fonts. All brand assets (logos, favicons, tokens.css, OG template) already in the project folder.

**Newsletter:** Resend + Cloudflare Worker (same stack as therevopsreport.com). Fully automated weekly digest called "The GTME Pulse." Signup form → Worker → Resend Audiences. Monday cron generates + sends email from scraper data.

**Job board:** Wired to unified scraper at `/Users/rome/Documents/projects/scrapers/master/` — `gtme` audience (id=8) with 21 search terms. Exports CSV + JSON + market_intelligence.json + comp_analysis.json to `data/`.

**Phase ordering (go deep, no thin pages):**
1. Wave 1: Build system skeleton + homepage + salary pages (~45 pages)
2. Wave 2: Tool reviews + comparisons (~80 pages)
3. Wave 3: Career guides + glossary (~65 pages)
4. Wave 4: Job board + insight articles (~20+ pages)

**What to build now:** [SPECIFY YOUR TASK HERE — e.g., "Build Wave 1: the build system skeleton (build.py, templates.py, nav_config.py, CSS) with homepage, about page, newsletter page, and all 45 salary pages"]

**Reference sites for style/structure:**
- therevopsreport.com (primary model — jobs, salaries, tools, insights, glossary)
- SultanOfSaaS at `/Users/rome/Documents/projects/sultanofsaas/` (best template architecture)
- B2B Sales Tools at `/Users/rome/Documents/projects/b2bsalestools/` (best content module pattern)

Before writing any code, read CLAUDE.md fully. Follow the architecture pattern, writing standards, and SEO rules exactly as documented.
