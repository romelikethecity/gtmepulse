# Requirements: GTME Pulse v3.0 — Tool Reviews, Glossary, and Infrastructure

**Defined:** 2026-03-14
**Core Value:** GTM Engineers can find accurate, vendor-neutral salary benchmarks and career intelligence in one place, with data no competitor provides.

## v3.0 Requirements

### Tool Reviews

- [ ] **TREV-01**: Clay review (data enrichment, 84% adoption, honest criticism)
- [ ] **TREV-02**: Apollo review (enrichment + sequencing, 15-20% affiliate)
- [ ] **TREV-03**: ZoomInfo review (enterprise enrichment, pricing criticism)
- [ ] **TREV-04**: Clearbit review (enrichment, Salesforce acquisition context)
- [ ] **TREV-05**: FullEnrich review (waterfall enrichment)
- [ ] **TREV-06**: Lusha review (contact data)
- [ ] **TREV-07**: Cognism review (EMEA-focused enrichment)
- [ ] **TREV-08**: LeadIQ review (prospecting)
- [ ] **TREV-09**: Persana review (AI enrichment)
- [ ] **TREV-10**: Instantly review (outbound sequencing, 20-40% affiliate)
- [ ] **TREV-11**: Smartlead review (outbound sequencing)
- [ ] **TREV-12**: Outreach review (enterprise sequencing)
- [ ] **TREV-13**: Salesloft review (enterprise sequencing)
- [ ] **TREV-14**: Lemlist review (outbound + personalization)
- [ ] **TREV-15**: HeyReach review (LinkedIn automation)
- [ ] **TREV-16**: Woodpecker review (cold email)
- [ ] **TREV-17**: HubSpot review (CRM for GTM Engineers)
- [ ] **TREV-18**: Salesforce review (CRM for GTM Engineers)
- [ ] **TREV-19**: Pipedrive review (SMB CRM)
- [ ] **TREV-20**: Close review (sales-focused CRM)
- [ ] **TREV-21**: Attio review (modern CRM)
- [ ] **TREV-22**: Make review (workflow automation)
- [ ] **TREV-23**: n8n review (self-hosted automation)
- [ ] **TREV-24**: Zapier review (no-code automation)
- [ ] **TREV-25**: 6sense review (intent data)
- [ ] **TREV-26**: Bombora review (intent data)
- [ ] **TREV-27**: LinkedIn Sales Navigator review
- [ ] **TREV-28**: PhantomBuster review (LinkedIn automation)
- [ ] **TREV-29**: Segment review (CDP/analytics)
- [ ] **TREV-30**: PostHog review (product analytics)

### Tool Category Indexes

- [ ] **TCAT-01**: Data Enrichment & Orchestration category index
- [ ] **TCAT-02**: Outbound Sequencing category index
- [ ] **TCAT-03**: CRM category index
- [ ] **TCAT-04**: Workflow Automation category index
- [ ] **TCAT-05**: AI & LLM Tools category index
- [ ] **TCAT-06**: Intent & Signal Data category index
- [ ] **TCAT-07**: Analytics & Product Signals category index
- [ ] **TCAT-08**: LinkedIn & Social category index

### Tool Comparisons

- [ ] **TCMP-01**: Clay vs Apollo
- [ ] **TCMP-02**: Clay vs ZoomInfo
- [ ] **TCMP-03**: Instantly vs Smartlead
- [ ] **TCMP-04**: Outreach vs Salesloft
- [ ] **TCMP-05**: HubSpot vs Salesforce (deep comparison)
- [ ] **TCMP-06**: Make vs n8n
- [ ] **TCMP-07**: Make vs Zapier
- [ ] **TCMP-08**: Apollo vs ZoomInfo
- [ ] **TCMP-09**: Lemlist vs Instantly
- [ ] **TCMP-10**: Clay vs Clearbit
- [ ] **TCMP-11**: 6sense vs Bombora
- [ ] **TCMP-12**: Mixpanel vs Amplitude
- [ ] **TCMP-13**: Close vs Pipedrive
- [ ] **TCMP-14**: HeyReach vs Expandi
- [ ] **TCMP-15**: Segment vs PostHog
- [ ] **TCMP-16**: Hightouch vs Census
- [ ] **TCMP-17**: LinkedIn Sales Nav vs Apollo
- [ ] **TCMP-18**: Cognism vs ZoomInfo
- [ ] **TCMP-19**: LeadIQ vs Lusha
- [ ] **TCMP-20**: Smartlead vs Lemlist

### Alternatives Pages

- [ ] **TALT-01**: Clay alternatives
- [ ] **TALT-02**: Apollo alternatives
- [ ] **TALT-03**: ZoomInfo alternatives
- [ ] **TALT-04**: Instantly alternatives
- [ ] **TALT-05**: Outreach alternatives
- [ ] **TALT-06**: HubSpot alternatives
- [ ] **TALT-07**: Salesforce alternatives
- [ ] **TALT-08**: Zapier alternatives
- [ ] **TALT-09**: 6sense alternatives
- [ ] **TALT-10**: LinkedIn Sales Navigator alternatives

### Best-For Roundups

- [ ] **TBST-01**: Best GTM tools for startups
- [ ] **TBST-02**: Best GTM tools for enterprise
- [ ] **TBST-03**: Best free GTM tools
- [ ] **TBST-04**: Best data enrichment tools
- [ ] **TBST-05**: Best outbound sequencing tools
- [ ] **TBST-06**: Best CRM for GTM Engineers
- [ ] **TBST-07**: Best workflow automation tools
- [ ] **TBST-08**: Best AI tools for GTM
- [ ] **TBST-09**: Best LinkedIn prospecting tools
- [ ] **TBST-10**: Best intent data platforms

### Glossary

- [ ] **GLOS-01**: Glossary index page with alphabetical listing and category grouping
- [ ] **GLOS-02**: 50 individual glossary term pages (300-600 words each, definition, examples, related links)

### Job Board

- [ ] **JOBS-01**: Job board page with cards, filters (seniority, location, remote), aggregate stats banner
- [ ] **JOBS-02**: Build pipeline to read scraper JSON exports from data/ directory

### Newsletter Infrastructure

- [ ] **NEWS-01**: Cloudflare Worker for signup (worker/subscribe.js, clone RevOps pattern)
- [ ] **NEWS-02**: Worker deployment config (worker/wrangler.toml)
- [ ] **NEWS-03**: Weekly email generator script (scripts/generate_weekly_email.py)
- [ ] **NEWS-04**: Cron script for automated Monday sends (scripts/send_weekly_email.sh)

### Content Quality

- [ ] **QUAL3-01**: Every tool review has SoftwareApplication JSON-LD schema
- [ ] **QUAL3-02**: Every tool comparison has FAQPage schema with 3+ Q&A
- [ ] **QUAL3-03**: Site-wide validation passes with zero warnings after all pages added

## Future Requirements

### v3.1+ (Deferred)

- **FUTURE-01**: Tray.io review (workflow automation, enterprise tier)
- **FUTURE-02**: G2, TrustRadius reviews (intent data, review platform)
- **FUTURE-03**: Hightouch, Census reviews (reverse ETL)
- **FUTURE-04**: Mixpanel, Amplitude reviews (product analytics)
- **FUTURE-05**: Dripify, Expandi reviews (LinkedIn automation)
- **FUTURE-06**: OG image auto-generation via Playwright
- **FUTURE-07**: Dark mode toggle UI

## Out of Scope

| Feature | Reason |
|---------|--------|
| Interactive data visualizations (charts) | Static site, no JS frameworks |
| User-generated reviews/comments | No backend |
| Tool pricing database with historical tracking | Would require scraping/API, maintenance burden |
| Automated affiliate link management | Manual for now, low volume |
| Email drip sequences beyond weekly | v3.0 ships weekly send only |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| TREV-01 | Phase 8 | Pending |
| TREV-02 | Phase 8 | Pending |
| TREV-03 | Phase 8 | Pending |
| TREV-04 | Phase 8 | Pending |
| TREV-05 | Phase 8 | Pending |
| TREV-06 | Phase 8 | Pending |
| TREV-07 | Phase 8 | Pending |
| TREV-08 | Phase 8 | Pending |
| TREV-09 | Phase 8 | Pending |
| TREV-10 | Phase 8 | Pending |
| TREV-11 | Phase 8 | Pending |
| TREV-12 | Phase 8 | Pending |
| TREV-13 | Phase 8 | Pending |
| TREV-14 | Phase 8 | Pending |
| TREV-15 | Phase 8 | Pending |
| TREV-16 | Phase 8 | Pending |
| TREV-17 | Phase 8 | Pending |
| TREV-18 | Phase 8 | Pending |
| TREV-19 | Phase 8 | Pending |
| TREV-20 | Phase 8 | Pending |
| TREV-21 | Phase 8 | Pending |
| TREV-22 | Phase 8 | Pending |
| TREV-23 | Phase 8 | Pending |
| TREV-24 | Phase 8 | Pending |
| TREV-25 | Phase 8 | Pending |
| TREV-26 | Phase 8 | Pending |
| TREV-27 | Phase 8 | Pending |
| TREV-28 | Phase 8 | Pending |
| TREV-29 | Phase 8 | Pending |
| TREV-30 | Phase 8 | Pending |
| TCAT-01 | Phase 9 | Pending |
| TCAT-02 | Phase 9 | Pending |
| TCAT-03 | Phase 9 | Pending |
| TCAT-04 | Phase 9 | Pending |
| TCAT-05 | Phase 9 | Pending |
| TCAT-06 | Phase 9 | Pending |
| TCAT-07 | Phase 9 | Pending |
| TCAT-08 | Phase 9 | Pending |
| TCMP-01 | Phase 9 | Pending |
| TCMP-02 | Phase 9 | Pending |
| TCMP-03 | Phase 9 | Pending |
| TCMP-04 | Phase 9 | Pending |
| TCMP-05 | Phase 9 | Pending |
| TCMP-06 | Phase 9 | Pending |
| TCMP-07 | Phase 9 | Pending |
| TCMP-08 | Phase 9 | Pending |
| TCMP-09 | Phase 9 | Pending |
| TCMP-10 | Phase 9 | Pending |
| TCMP-11 | Phase 9 | Pending |
| TCMP-12 | Phase 9 | Pending |
| TCMP-13 | Phase 9 | Pending |
| TCMP-14 | Phase 9 | Pending |
| TCMP-15 | Phase 9 | Pending |
| TCMP-16 | Phase 9 | Pending |
| TCMP-17 | Phase 9 | Pending |
| TCMP-18 | Phase 9 | Pending |
| TCMP-19 | Phase 9 | Pending |
| TCMP-20 | Phase 9 | Pending |
| TALT-01 | Phase 10 | Pending |
| TALT-02 | Phase 10 | Pending |
| TALT-03 | Phase 10 | Pending |
| TALT-04 | Phase 10 | Pending |
| TALT-05 | Phase 10 | Pending |
| TALT-06 | Phase 10 | Pending |
| TALT-07 | Phase 10 | Pending |
| TALT-08 | Phase 10 | Pending |
| TALT-09 | Phase 10 | Pending |
| TALT-10 | Phase 10 | Pending |
| TBST-01 | Phase 10 | Pending |
| TBST-02 | Phase 10 | Pending |
| TBST-03 | Phase 10 | Pending |
| TBST-04 | Phase 10 | Pending |
| TBST-05 | Phase 10 | Pending |
| TBST-06 | Phase 10 | Pending |
| TBST-07 | Phase 10 | Pending |
| TBST-08 | Phase 10 | Pending |
| TBST-09 | Phase 10 | Pending |
| TBST-10 | Phase 10 | Pending |
| GLOS-01 | Phase 11 | Pending |
| GLOS-02 | Phase 11 | Pending |
| JOBS-01 | Phase 11 | Pending |
| JOBS-02 | Phase 11 | Pending |
| NEWS-01 | Phase 11 | Pending |
| NEWS-02 | Phase 11 | Pending |
| NEWS-03 | Phase 11 | Pending |
| NEWS-04 | Phase 11 | Pending |
| QUAL3-01 | Phase 12 | Pending |
| QUAL3-02 | Phase 12 | Pending |
| QUAL3-03 | Phase 12 | Pending |

**Coverage:**
- v3.0 requirements: 109 total (TREV:30, TCAT:8, TCMP:20, TALT:10, TBST:10, GLOS:2, JOBS:2, NEWS:4, QUAL3:3)
- Mapped to phases: 109
- Unmapped: 0

---
*Requirements defined: 2026-03-14*
*Last updated: 2026-03-14 after roadmap creation*
