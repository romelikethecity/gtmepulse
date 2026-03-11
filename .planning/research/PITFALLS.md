# Domain Pitfalls

**Domain:** Programmatic SEO static site (salary data + tool reviews + career content)
**Project:** GTME Pulse
**Researched:** 2026-03-10

---

## Critical Pitfalls

Mistakes that cause site-wide ranking loss, legal exposure, or rewrites.

### Pitfall 1: Site-Wide Quality Poisoning from Template Pages

**What goes wrong:** Google's Helpful Content system evaluates your entire domain, not individual pages. If 30 of your 200 pages are thin template output with swapped city names or role titles, the penalty drags down every page, including the good ones. An e-commerce case study showed a 73% organic traffic drop where the penalty affected all pages, not just the programmatic ones.

**Why it happens:** Programmatic SEO makes it trivially easy to generate 45 salary pages from a template + data dict. The temptation is to ship all pages simultaneously with boilerplate paragraphs that only differ by one variable (city name, seniority level). Google's December 2025 update specifically targets "experience dilution," content that technically covers a topic but lacks genuine first-hand expertise.

**Consequences:** Entire domain deindexed or suppressed. Recovery takes 3-6 months minimum after a core update cycle. All the good content (homepage, methodology, about) gets buried alongside the thin pages.

**Prevention:**
- Enforce the existing 1,200-2,000 word minimum per salary page with real differentiation. Each page needs unique market context, comp drivers specific to that segment, and distinct FAQ pairs.
- Aim for 30-40% content differentiation between any two pages in the same template family. A San Francisco salary page must discuss cost-of-living adjustments, startup equity norms, and Bay Area hiring velocity. An Austin page must discuss Texas tax advantages, emerging tech hub dynamics, and remote-first company concentration. Not just "replace $CITY."
- Run a manual diff check before launch: pick any two pages from the same template type and verify a human could tell them apart without looking at the title.
- Never ship all 45 salary pages at once. Stagger: launch 5-10 strong pages, let them index and prove quality signals, then expand.

**Detection:** Google Search Console showing "Excluded - Crawled, currently not indexed" on template pages. Sudden drops in indexed page count. Pages getting impressions but zero clicks (Google showing but users bouncing).

**Phase:** Wave 1 (Salary pages). This is the single biggest risk to the project.

---

### Pitfall 2: Duplicate or Near-Duplicate Meta Tags Across Template Pages

**What goes wrong:** Every programmatically generated page ends up with identical or near-identical title tags and meta descriptions. Google treats these as duplicate content signals and may only index one representative page from the group.

**Why it happens:** Template functions like `write_page(path, title, description, content)` make it easy to pass generic strings. A salary template might generate "GTM Engineer Salary in {city}" for the title and "Learn about GTM Engineer salaries in {city}" for the description across 15 pages. These are technically unique but functionally identical to Google.

**Consequences:** Pages compete against each other (keyword cannibalization). Google picks one and suppresses the rest. Click-through rates tank because descriptions all say the same thing in SERPs.

**Prevention:**
- Each title must include a unique data point: "GTM Engineer Salary in Austin: $145K Median, 12% Above National Average" vs "GTM Engineer Salary in SF: $178K Median, Highest in US"
- Meta descriptions must reference specific, unique content from that page: salary ranges, comparison points, or unique market factors
- Build a validation step in `build.py` that fails the build if any two pages share identical titles or descriptions. This is cheap insurance.
- Keep titles at 50-60 characters but front-load the differentiator

**Detection:** Screaming Frog or manual grep of output HTML for duplicate `<title>` or `<meta name="description">` content.

**Phase:** Wave 1 (build system). Build the dedup validator into `build.py` from day one.

---

### Pitfall 3: Salary Data Accuracy and Legal Exposure

**What goes wrong:** Publishing specific salary numbers ($132K median, $250K ceiling) without clear sourcing methodology creates two risks: (1) users distrust the data and the site loses credibility permanently, and (2) potential legal liability if compensation claims are used in hiring negotiations or pay equity disputes.

**Why it happens:** GTM Engineer is a new role (coined ~2023). There is no BLS category, no established compensation survey data, and no Radford/Mercer benchmark for it. The salary data in build.py is hardcoded from job posting analysis, not employer-reported compensation. This is a fundamentally different data quality tier than Levels.fyi (self-reported verified) or Salary.com (employer-reported surveys).

**Consequences:** A methodology page that hand-waves sourcing ("based on market data") gets torn apart by the GTM Engineer community. Worse, if a candidate cites your numbers in a negotiation and the employer knows them to be inflated, your site's reputation is dead on arrival. Glassdoor's credibility problems (inflated website numbers vs app numbers, mixing base and TC) are a cautionary tale.

**Prevention:**
- Build the methodology page first, before any salary pages. It must clearly state:
  - Data sources (job postings with disclosed ranges, not self-reported)
  - Sample sizes per segment (if Austin has 8 postings, say so)
  - Date ranges of data collection
  - What "salary" means (base only? base + OTE? base + equity?)
  - Statistical method (median vs mean, outlier handling)
- Add a visible disclaimer on every salary page: "Salary estimates are based on analysis of job postings with disclosed compensation ranges. Individual compensation varies based on experience, company, location, and negotiation. These figures are not guarantees."
- Distinguish between posted salary ranges (what employers advertise) and actual compensation (what people earn). These differ significantly, especially for roles where equity is a major component.
- When sample sizes are small (under 20 data points), display confidence intervals or ranges rather than precise medians. "Austin: $130K-$165K range (based on 12 postings)" is more honest than "$147K median."

**Detection:** Users calling out specific numbers as wrong on social media or HN. Methodology page getting zero traffic (means nobody trusts it enough to check).

**Phase:** Wave 1. Write methodology page before salary content pages.

---

### Pitfall 4: Missing or Malformed Schema Markup

**What goes wrong:** JSON-LD schema blocks have silent failures. A single missing comma, unclosed bracket, or unescaped quote breaks the entire block. Google silently ignores it. You get no rich results, no FAQ snippets, no breadcrumb trails in SERPs, and you never know because there's no visible error.

**Why it happens:** Python string interpolation into JSON is fragile. F-strings with nested quotes, special characters in FAQ answers, or apostrophes in content break JSON syntax. The `faq_schema_and_html()` helper in `templates.py` must handle arbitrary text content safely.

**Consequences:** Competitors who have working FAQ schema get 2-3x the SERP real estate. BreadcrumbList schema drives click-through by showing site hierarchy. Without it, you're leaving ranking signals and click-through rate on the table.

**Prevention:**
- Use Python's `json.dumps()` to serialize schema data, never manual string concatenation. This handles escaping automatically.
- Add a build-time validation step that parses every JSON-LD block with `json.loads()` and fails on invalid JSON.
- Test with Google's Rich Results Test (search.google.com/test/rich-results) on 3-5 pages from each template type before launch.
- For FAQ schema specifically: the FAQ content in the schema must exactly match visible content on the page. Mismatches are considered spammy and can result in manual actions.
- Use the @graph pattern on the homepage (Organization + WebSite in one block) to avoid duplicate Organization blocks.

**Detection:** Zero rich results showing in Search Console after 2-4 weeks of indexing. Rich Results Test showing "No valid items detected."

**Phase:** Wave 1 (build system). The `templates.py` schema helpers must use `json.dumps()` from the start.

---

## Moderate Pitfalls

### Pitfall 5: Orphaned Pages and Weak Internal Linking

**What goes wrong:** Programmatically generated pages only link to each other through nav and footer. Google sees these as orphaned or shallow-linked pages and deprioritizes them. The "3+ internal links per page beyond nav/footer" requirement exists for a reason, but template-generated pages often miss it.

**Why it happens:** Internal linking requires intentional content relationships. A "GTM Engineer Salary in Austin" page should link to "Austin vs Remote salary comparison," "Series A salary ranges" (many Austin startups are Series A), and "GTM Engineer vs RevOps salary." But building these contextual links into templates requires explicit relationship mapping, not just "related pages in the same category."

**Prevention:**
- Build a link graph in `build.py` that defines explicit relationships between pages: location pages link to relevant company-stage pages, comparison pages link back to both salary breakdowns, methodology page is linked from every salary page.
- Add a "Related Salary Data" section at the bottom of every salary page with 4-6 contextual links. Not random. Each link should have a reason to exist from the reader's perspective.
- Add a build-time check: fail if any page has fewer than 3 internal links beyond nav/footer.
- Consider a "salary crosslinks" data structure that maps each page to its most relevant siblings.

**Detection:** Screaming Frog internal link audit. Google Search Console coverage report showing crawled-but-not-indexed pages.

**Phase:** Wave 1. Design the link graph before building page templates.

---

### Pitfall 6: Newsletter Signup That Converts at Sub-1%

**What goes wrong:** "Sign up for our newsletter" with a bare email field converts at 1-2% of visitors. For a new site with no brand recognition, the actual rate will be closer to 0.5%. You need hundreds or thousands of signups to make the newsletter channel viable, and a weak CTA bleeds visitors.

**Why it happens:** Generic signup CTAs ("Subscribe to our newsletter") offer no specific value. Users see 50 of these per week. No urgency, no specificity, no proof of value.

**Consequences:** Newsletter list grows too slowly to monetize through sponsorships. The email-gated salary calculator underperforms because users don't trust giving their email to an unknown site.

**Prevention:**
- Lead with specific deliverables: "Every Monday: new GTME job count, median salary shifts, and which tools are hiring for." Not "weekly insights."
- Place signup CTAs in three locations with different hooks: (1) hero area with the primary value prop, (2) inline after a salary data table with "Get weekly updates on these numbers," (3) dedicated /newsletter page with full preview of what an issue looks like.
- The email-gated salary calculator should show partial results (top-line number) and gate the detailed breakdown. Full gate with zero preview kills conversion.
- Social proof as soon as possible: subscriber count once it passes 100, or "Trusted by GTM Engineers at [company logos]" once you have them.
- Avoid popups on first visit. Delay any popup until 30+ seconds or 50%+ scroll. Immediate popups on a new, unknown site feel desperate.
- Bottom-center sticky bar (12.88% conversion in studies) outperforms modal popups (4.65% average).

**Detection:** Resend Audiences dashboard showing sub-1% signup rate relative to page views (check via Cloudflare Analytics).

**Phase:** Wave 1 (newsletter infrastructure). Get the CTA copy and placement right from launch.

---

### Pitfall 7: Data Tables That Break on Mobile

**What goes wrong:** Salary comparison tables with 4-5 columns (Role, Base, OTE, Equity, Total) overflow on 375px screens. Text wraps awkwardly, columns compress to unreadable widths, or horizontal scrolling creates a broken experience. Stat numbers with spaces ("$132 K") cause mid-number line breaks.

**Why it happens:** Tables are inherently wide. A salary comparison table needs enough columns to be useful but mobile viewports can only fit 2-3 columns comfortably. CSS `overflow-x: auto` "solves" it technically but creates a scroll-within-scroll UX that users hate.

**Consequences:** Mobile is 60%+ of traffic for content sites. Broken tables on mobile means broken pages for the majority of visitors. Google's mobile-first indexing means the mobile version IS your indexed version.

**Prevention:**
- Use the card-stack pattern for mobile: at 768px and below, transform table rows into stacked cards where each row becomes a vertical card showing label-value pairs. This is more work to implement but dramatically better UX.
- For simpler tables (2-3 columns), horizontal scroll with visual scroll indicators (fade/shadow on right edge) is acceptable.
- Enforce the existing rule: no spaces in stat numbers. Use `$132K` not `$132 K`. Use `&#8209;` (non-breaking hyphen) for ranges like `$130K&#8209;$165K`.
- Test every table template at 375px width during build. Add width/max-width constraints to table containers.
- Use `font-variant-numeric: tabular-nums` on salary figures so columns align properly.

**Detection:** Chrome DevTools device toolbar at 375px. Lighthouse mobile audit.

**Phase:** Wave 1 (CSS architecture). Build the responsive table/card component in `components.css` before creating salary page templates.

---

### Pitfall 8: CSS Token Cascade Conflicts

**What goes wrong:** Three CSS files (tokens.css, components.css, styles.css) create specificity conflicts when page-specific styles in `styles.css` need to override component defaults in `components.css`. Developers add `!important` to fix one page, which breaks the cascade for the next page.

**Why it happens:** The 3-file architecture is clean in theory but requires strict discipline. If `components.css` defines `.card { padding: var(--space-lg) }` and a salary page needs tighter cards, the override in `styles.css` must have equal or higher specificity. Without a naming convention, you end up with `.salary-page .card` fighting `.card.card-highlight` and nobody remembers which wins.

**Consequences:** Visual bugs that appear only on specific page types. "I changed the card padding and now the tool review cards are broken." Cascading fixes that touch multiple files.

**Prevention:**
- Strict layer ordering: tokens (variables only, no selectors) -> components (class-based, no nesting deeper than 2 levels) -> styles (page-scoped selectors using page-type class on body).
- Every page type gets a body class: `<body class="page-salary-location">`, `<body class="page-tool-review">`. Page-specific overrides scope to that class.
- Zero `!important` rule. If you need `!important`, you have a specificity architecture problem. Fix the architecture.
- Document the specificity contract: tokens = 0 specificity (just variables), components = single class (0,1,0), styles = body-class + component-class (0,2,0).

**Detection:** Visual regression on pages that weren't touched by a CSS change. Grep for `!important` in CSS files.

**Phase:** Wave 1 (CSS architecture). Establish the convention in tokens.css/components.css/styles.css before writing any page styles.

---

## Minor Pitfalls

### Pitfall 9: Stale Salary Data with No Update Cadence

**What goes wrong:** Salary pages show 2026 Q1 data indefinitely. Six months later, the data is stale and users notice. Google's freshness signals also deprioritize pages with old dates and no updates.

**Prevention:**
- Display "Last updated: [date]" prominently on every salary page.
- Plan quarterly data refreshes. When the job scraper pipeline (Wave 4) is live, automate this.
- Version the data: "Q1 2026 salary data" makes staleness explicit rather than pretending numbers are evergreen.
- Add `dateModified` to schema markup and update it with each data refresh.

**Phase:** Wave 1 (data structure). Build the update-date display into salary templates from the start, even if the first update is manual.

---

### Pitfall 10: Canonical URL Mistakes on Template Pages

**What goes wrong:** Template pages generate canonical URLs with trailing slashes inconsistently, or canonical URLs point to the wrong page due to a bug in the path-building logic. Google receives conflicting signals about which page is the "real" version.

**Prevention:**
- Standardize: all canonical URLs end without trailing slash (e.g., `https://gtmepulse.com/salary/austin` not `https://gtmepulse.com/salary/austin/`).
- Build a validation step that checks every canonical URL in the output matches the actual file path.
- Ensure GitHub Pages serves the same content whether accessed with or without trailing slash (it does by default with `index.html` files).

**Phase:** Wave 1. Canonical logic in `templates.py` from build one.

---

### Pitfall 11: Sitemap Including Non-Indexable Pages

**What goes wrong:** Auto-generated sitemap.xml includes every page, including pages you may not want indexed (404, privacy policy, terms). Or worse, it includes 200+ URLs on day one, and Google crawls them all, finds thin content on half, and flags the whole site.

**Prevention:**
- Exclude utility pages (404, terms, privacy) from sitemap.xml.
- If launching in phases, only include pages that are fully built in the sitemap. Don't sitemap placeholder pages.
- Set a crawl-delay in robots.txt if you want to pace Google's initial crawl.

**Phase:** Wave 1 (build system).

---

### Pitfall 12: Outbound Link Neglect

**What goes wrong:** Salary pages cite statistics ("205% YoY growth") without linking to sources. Google's E-E-A-T evaluation looks for outbound links to authoritative sources as a quality signal. Pages with zero outbound links look like they're making claims without evidence.

**Prevention:**
- Every stat needs an outbound link to its source. Job posting growth -> LinkedIn Economic Graph or similar. Salary ranges -> link to example job postings or BLS data for comparison roles.
- 2+ outbound links per content page minimum (already in CLAUDE.md requirements).
- Link to authoritative sources: BLS, LinkedIn, specific company career pages with disclosed salary ranges.

**Phase:** Wave 1 (content templates). Build source citation into the salary page template structure.

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|---|---|---|
| Wave 1: Build system | Schema markup silently broken (Pitfall 4) | `json.dumps()` + build-time JSON validation |
| Wave 1: CSS architecture | Token cascade conflicts (Pitfall 8) | Body class scoping, zero `!important` rule |
| Wave 1: Salary pages | Thin content penalty (Pitfall 1) | 30%+ differentiation, staggered launch |
| Wave 1: Salary pages | Data credibility collapse (Pitfall 3) | Methodology page first, visible disclaimers |
| Wave 1: Salary pages | Mobile table breakage (Pitfall 7) | Card-stack pattern at 768px breakpoint |
| Wave 1: Salary pages | Duplicate meta tags (Pitfall 2) | Build-time dedup validator |
| Wave 1: Newsletter | Sub-1% signup rate (Pitfall 6) | Specific deliverable CTA, bottom-center sticky |
| Wave 2: Tool pages | Review pages feel AI-generated | Honest criticism required, personal tool experience, specific pricing |
| Wave 2: Comparisons | Template pages all read the same | Each comparison needs a clear winner call, not "it depends" |
| Wave 3: Glossary | 50 thin 300-word pages tank domain quality | Glossary terms must hit 400+ words with examples and context |
| Wave 4: Job board | Stale job data after scraper gaps | Display "last scraped" date, handle zero-results gracefully |

## Sources

- [Programmatic SEO: Scale Without Google Penalties (2025)](https://guptadeepak.com/the-programmatic-seo-paradox-why-your-fear-of-creating-thousands-of-pages-is-both-valid-and-obsolete/) - MEDIUM confidence
- [Google's December 2025 Helpful Content Update](https://dev.to/synergistdigitalmedia/googles-december-2025-helpful-content-update-hit-your-site-heres-what-actually-changed-2bal) - MEDIUM confidence
- [Common Programmatic SEO Mistakes](https://seomatic.ai/blog/programmatic-seo-mistakes) - MEDIUM confidence
- [Programmatic SEO Duplicate Content](https://seomatic.ai/blog/programmatic-seo-duplicate-content) - MEDIUM confidence
- [Common Schema Markup Errors](https://robertcelt95.medium.com/common-schema-markup-errors-that-kill-your-seo-rankings-cc64a83480af) - MEDIUM confidence
- [Most Common JSON-LD Schema Issues](https://zeo.org/resources/blog/most-common-json-ld-schema-issues-and-solutions) - MEDIUM confidence
- [Salary.com Data Subscription Agreement](https://www.salary.com/legal/dsa/) - HIGH confidence (primary source)
- [Best Salary Websites 2026](https://www.salarycube.com/salaries/best-salary-website-for-accurate-pay-data-and-career-insights) - MEDIUM confidence
- [CSS Responsive Tables Guide](https://dev.to/satyam_gupta_0d1ff2152dcc/css-responsive-tables-complete-guide-with-code-examples-for-2025-225p) - MEDIUM confidence
- [Newsletter Signup Examples That Convert](https://www.omnisend.com/blog/newsletter-signup-examples/) - MEDIUM confidence
- [Email Signup Benchmarks](https://bdow.com/stories/email-signup-benchmarks/) - MEDIUM confidence
- Glassdoor/Levels.fyi community discussions on data accuracy - LOW confidence (anecdotal)
