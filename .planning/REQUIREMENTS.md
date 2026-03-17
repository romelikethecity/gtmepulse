# Requirements: GTME Pulse v4.0 — Content Expansion and Go-Live Infrastructure

**Defined:** 2026-03-16
**Core Value:** GTM Engineers can find accurate, vendor-neutral salary benchmarks and career intelligence in one place, with data no competitor provides.

## v4.0 Requirements

### Insight Articles

- [ ] **ART-01**: Job market analysis article (total GTME roles, growth trends, top hiring companies, remote %)
- [ ] **ART-02**: Salary trends deep dive (median shifts, seniority premiums, location arbitrage, equity breakdown)
- [ ] **ART-03**: Tool adoption report (which tools appear in job postings, market share shifts, emerging tools)
- [ ] **ART-04**: "State of GTM Engineering 2026" summary article (key findings from n=228 survey)
- [ ] **ART-05**: Clay ecosystem breakdown (integrations, use cases, why 69% adoption, limitations)
- [ ] **ART-06**: Outbound automation stack guide (sequencing + enrichment + CRM wiring)
- [ ] **ART-07**: Building your first Clay table playbook (step-by-step for new GTM Engineers)
- [ ] **ART-08**: LinkedIn outreach automation playbook (Sales Nav + PhantomBuster/HeyReach)
- [ ] **ART-09**: Email deliverability guide for GTM Engineers (warmup, domains, reputation)
- [ ] **ART-10**: API integration patterns for GTM Engineers (webhooks, Zapier/Make, Python scripts)
- [ ] **ART-11**: Data enrichment waterfall strategy (multi-vendor, cost optimization, accuracy benchmarks)
- [ ] **ART-12**: GTM Engineer hiring guide for managers (what to look for, interview process, comp benchmarks)
- [ ] **ART-13**: Freelance GTM Engineering rate guide (hourly vs retainer, pricing by deliverable)
- [ ] **ART-14**: GTM Engineer vs SDR team ROI analysis (cost comparison, pipeline output, scalability)
- [ ] **ART-15**: Intent data buying guide (6sense vs Bombora vs G2, signal types, integration)
- [ ] **ART-16**: CRM hygiene automation playbook (dedup, routing, lifecycle stages via code)
- [ ] **ART-17**: Monthly pulse report template page (auto-populated from scraper data)
- [ ] **ART-18**: GTM Engineer tech stack audit checklist (evaluate your current stack)
- [ ] **ART-19**: Revenue attribution for GTM Engineers (proving pipeline impact with data)
- [ ] **ART-20**: Remote GTM Engineering market report (geo distribution, salary by location, timezone patterns)

### Analytics

- [x] **ANLYT-01**: GA4 tracking snippet added to all pages via templates.py
- [x] **ANLYT-02**: Google Search Console verification (HTML file or meta tag method)
- [x] **ANLYT-03**: Event tracking for newsletter signups (GA4 custom event on form submit)

### Newsletter Go-Live

- [ ] **NLIVE-01**: Deploy Cloudflare Worker (npx wrangler deploy)
- [ ] **NLIVE-02**: Create Resend Audience for GTME Pulse
- [ ] **NLIVE-03**: Verify gtmepulse.com domain in Resend (DNS records in Cloudflare)
- [ ] **NLIVE-04**: Set worker secrets (RESEND_API_KEY, RESEND_AUDIENCE_ID)
- [ ] **NLIVE-05**: Set up server cron for Monday email sends
- [ ] **NLIVE-06**: Send test email and verify end-to-end flow

### OG Images

- [ ] **OG-01**: Playwright-based OG image generator script (reads HTML templates, screenshots to PNG)
- [ ] **OG-02**: OG image HTML templates for each page type (salary, tool review, comparison, article, glossary)
- [ ] **OG-03**: Build integration (generate OG images as part of build.py pipeline)
- [ ] **OG-04**: All 280+ pages reference their generated OG image in meta tags

### Quality

- [ ] **QUAL4-01**: All new article pages pass existing validation (title length, word count, internal links, schema)
- [ ] **QUAL4-02**: Zero-warning build across all ~283+ pages after v4.0 additions

## Future Requirements

### Content Expansion
- **BLOG-01**: Weekly pulse report auto-generation from scraper data
- **BLOG-02**: Tool pricing tracker (automated price change detection)

### Monetization
- **MON-01**: Paid job board listings with payment integration
- **MON-02**: Newsletter sponsorship slots in email template

## Out of Scope

| Feature | Reason |
|---------|--------|
| Dark mode toggle UI | tokens.css has variables but no user toggle needed |
| Smart newsletter personalization | Standard broadcast sufficient for launch |
| Real-time job board updates | Static build from JSON is sufficient |
| Video content / YouTube embeds | Text-first, revisit after traffic baseline |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ANLYT-01 | Phase 13 | Complete |
| ANLYT-02 | Phase 13 | Complete |
| ANLYT-03 | Phase 13 | Complete |
| NLIVE-01 | Phase 13 | Pending |
| NLIVE-02 | Phase 13 | Pending |
| NLIVE-03 | Phase 13 | Pending |
| NLIVE-04 | Phase 13 | Pending |
| NLIVE-05 | Phase 13 | Pending |
| NLIVE-06 | Phase 13 | Pending |
| ART-01 | Phase 14 | Pending |
| ART-02 | Phase 14 | Pending |
| ART-03 | Phase 14 | Pending |
| ART-04 | Phase 14 | Pending |
| ART-05 | Phase 14 | Pending |
| ART-06 | Phase 14 | Pending |
| ART-07 | Phase 14 | Pending |
| ART-08 | Phase 14 | Pending |
| ART-09 | Phase 14 | Pending |
| ART-10 | Phase 14 | Pending |
| ART-11 | Phase 15 | Pending |
| ART-12 | Phase 15 | Pending |
| ART-13 | Phase 15 | Pending |
| ART-14 | Phase 15 | Pending |
| ART-15 | Phase 15 | Pending |
| ART-16 | Phase 15 | Pending |
| ART-17 | Phase 15 | Pending |
| ART-18 | Phase 15 | Pending |
| ART-19 | Phase 15 | Pending |
| ART-20 | Phase 15 | Pending |
| OG-01 | Phase 16 | Pending |
| OG-02 | Phase 16 | Pending |
| OG-03 | Phase 16 | Pending |
| OG-04 | Phase 16 | Pending |
| QUAL4-01 | Phase 17 | Pending |
| QUAL4-02 | Phase 17 | Pending |

**Coverage:**
- v4.0 requirements: 35 total
- Mapped to phases: 35
- Unmapped: 0

---
*Requirements defined: 2026-03-16*
*Last updated: 2026-03-16 after roadmap phase assignment*
