# Requirements: GTME Pulse

**Defined:** 2026-03-10
**Core Value:** GTM Engineers can find accurate, vendor-neutral salary benchmarks and career intelligence in one place, with data no competitor provides.

## v1 Requirements

Requirements for Wave 1 release. Each maps to roadmap phases.

### Build System

- [ ] **BUILD-01**: 3-file Python build system (build.py, templates.py, nav_config.py) generates all pages to output/
- [ ] **BUILD-02**: CSS architecture with 3 layers (tokens.css, components.css, styles.css) using design token variables
- [ ] **BUILD-03**: write_page() function writes HTML files and registers them in ALL_PAGES for sitemap
- [ ] **BUILD-04**: Auto-generated sitemap.xml from ALL_PAGES list
- [ ] **BUILD-05**: Auto-generated robots.txt with sitemap reference
- [ ] **BUILD-06**: Auto-generated CNAME file (gtmepulse.com)
- [ ] **BUILD-07**: Build script copies assets/ directory to output/ with cache-busted CSS links (?v=CSS_VERSION)
- [ ] **BUILD-08**: Build prints summary with page count on completion

### HTML Shell

- [ ] **HTML-01**: get_html_head() generates complete head with title, meta description, canonical URL, OG tags, Twitter Card, favicons, fonts, CSS
- [ ] **HTML-02**: get_nav_html() generates responsive nav with logo, menu items, dropdown support, mobile hamburger, newsletter CTA button
- [ ] **HTML-03**: get_footer_html() generates multi-column footer with links, newsletter mini-signup, copyright
- [ ] **HTML-04**: get_page_wrapper() assembles full HTML page (head + nav + main + footer)
- [ ] **HTML-05**: Mobile-responsive layout at 375px, 768px, and 1024px breakpoints

### Schema Markup

- [ ] **SEO-01**: Organization + WebSite JSON-LD schema on homepage (@graph pattern)
- [ ] **SEO-02**: BreadcrumbList JSON-LD schema on all inner pages
- [ ] **SEO-03**: FAQPage JSON-LD schema on salary breakdown and comparison pages (min 3 Q&A, matches visible content)
- [ ] **SEO-04**: All schema uses json.dumps() for safe serialization (never string concatenation)

### Core Pages

- [ ] **CORE-01**: Homepage with hero section, key stats grid (3,000+ roles, $132K-$250K range, 205% growth), section previews linking to salary/tools/career, newsletter CTA
- [ ] **CORE-02**: About page with Rome Thorndike bio, site mission, methodology overview
- [ ] **CORE-03**: Newsletter page with dedicated Resend signup form, value proposition, sample content preview
- [ ] **CORE-04**: Privacy policy page
- [ ] **CORE-05**: Terms of service page
- [ ] **CORE-06**: Custom 404 error page with navigation back to main sections

### Salary Pages

- [ ] **SAL-01**: Salary index page with aggregate stats, visual breakdowns, and links to all salary sub-pages
- [ ] **SAL-02**: 4 salary-by-seniority pages (Junior/Associate, Mid-Level, Senior, Lead/Staff) with stats grid, range bar, market context, comp drivers, FAQ, related links
- [ ] **SAL-03**: 15 salary-by-location pages (SF, NYC, Austin, Seattle, Boston, Denver, Chicago, LA, Miami, Atlanta, Portland, DC, Dallas, San Diego, Remote) with location-specific market context
- [ ] **SAL-04**: 5 salary-by-company-stage pages (Seed, Series A, Series B, Growth, Enterprise) with equity context and stage-specific comp dynamics
- [ ] **SAL-05**: 10 salary-vs-comparison pages (GTM Engineer vs RevOps, Sales Ops, Growth Engineer, SDR, Solutions Engineer, Marketing Ops, Sales Engineer, Data Engineer, Product Manager, AE) with side-by-side data, overlap analysis, career path notes
- [ ] **SAL-06**: Salary calculator page with email-gated full percentile results via Resend signup
- [ ] **SAL-07**: Methodology page explaining data sources, collection methods, limitations, and update frequency (must ship before salary content per research findings)

### Salary Page Quality

- [ ] **QUAL-01**: Every salary page has 1,200-2,000 words of content
- [ ] **QUAL-02**: Every salary page has unique market context paragraphs (30%+ differentiated from other same-type pages)
- [ ] **QUAL-03**: Every salary page has 3+ internal links beyond nav/footer
- [ ] **QUAL-04**: Every salary comparison page has FAQ section with 3-4 unique Q&A pairs
- [ ] **QUAL-05**: Stats display uses Source Code Pro font, no spaces in numbers ($132K not $132 K), non-breaking hyphens (&#8209;)
- [ ] **QUAL-06**: Salary tables convert to card-stack layout on mobile (below 768px)

### Newsletter Infrastructure

- [ ] **NEWS-01**: Cloudflare Worker (subscribe.js) validates email and POSTs to Resend Audiences API
- [ ] **NEWS-02**: Worker config (wrangler.toml) with name gtme-newsletter-signup
- [ ] **NEWS-03**: CORS configured for gtmepulse.com and localhost:8090
- [ ] **NEWS-04**: handleSignup() JS function in templates.py POSTs to Worker endpoint
- [ ] **NEWS-05**: Signup form placements: homepage hero CTA, inline after salary data, /newsletter page, footer mini-form
- [ ] **NEWS-06**: Success/error feedback shown to user after form submission

### Content Standards

- [ ] **CONTENT-01**: Title tags 50-60 chars, keyword-first, hyphens not pipes
- [ ] **CONTENT-02**: Meta descriptions 150-158 chars, action-oriented, unique per page
- [ ] **CONTENT-03**: One H1 per page, 46-60 chars
- [ ] **CONTENT-04**: No banned words (robust, leverage, seamless, etc. per CLAUDE.md)
- [ ] **CONTENT-05**: No em-dashes anywhere
- [ ] **CONTENT-06**: No false reframes ("not X, it's Y" pattern)

## v2 Requirements

Deferred to future waves. Tracked but not in current roadmap.

### Tools (Wave 2)

- **TOOL-01**: 30 individual tool review pages across 8 categories
- **TOOL-02**: Tools index + 8 category pages
- **TOOL-03**: 20 X vs Y comparison pages
- **TOOL-04**: 10 alternatives pages
- **TOOL-05**: 10 "Best for" roundup pages
- **TOOL-06**: SoftwareApplication schema on tool review pages

### Career (Wave 3)

- **CAREER-01**: Career guide index + 15 career guide pages
- **CAREER-02**: Glossary index + 50 individual term pages

### Jobs & Insights (Wave 4)

- **JOBS-01**: Job board page wired to unified scraper exports
- **JOBS-02**: Weekly email generation and automated Monday sends
- **JOBS-03**: Insight articles (job market analysis, tool trends)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Occupation/estimatedSalary schema | Google deprecated salary structured data in Sep 2025 |
| Dark mode toggle UI | tokens.css has dark mode vars but no toggle needed for v1 |
| OG image auto-generation | Playwright rendering is nice-to-have, not required for launch |
| Paywall/subscription model | All content free for SEO; only calculator gated behind email |
| User accounts/login | Static site, no backend |
| Comments/community features | Content-first, no UGC |
| Analytics integration | Defer to post-launch (recommend Cloudflare Web Analytics) |
| A/B testing | Premature for a new site |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| BUILD-01 through BUILD-08 | Phase 1 | Pending |
| HTML-01 through HTML-05 | Phase 1 | Pending |
| SEO-01 through SEO-04 | Phase 1 | Pending |
| CONTENT-01 through CONTENT-06 | Phase 1 | Pending |
| CORE-01 through CORE-06 | Phase 2 | Pending |
| NEWS-01 through NEWS-06 | Phase 2 | Pending |
| SAL-01 through SAL-07 | Phase 3 | Pending |
| QUAL-01 through QUAL-06 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 48 total (BUILD:8, HTML:5, SEO:4, CONTENT:6, CORE:6, NEWS:6, SAL:7, QUAL:6)
- Mapped to phases: 48
- Unmapped: 0

---
*Requirements defined: 2026-03-10*
*Last updated: 2026-03-10 after roadmap creation*
