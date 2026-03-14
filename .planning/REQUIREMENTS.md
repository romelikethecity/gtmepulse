# Requirements: GTME Pulse v3.0 — Tool Reviews, Glossary, and Infrastructure

**Defined:** 2026-03-14
**Core Value:** GTM Engineers can find accurate, vendor-neutral salary benchmarks and career intelligence in one place, with data no competitor provides.

## v3.0 Requirements

### Tool Reviews

- [x] **TREV-01**: Clay review (data enrichment, 84% adoption, honest criticism)
- [x] **TREV-02**: Apollo review (enrichment + sequencing, 15-20% affiliate)
- [x] **TREV-03**: ZoomInfo review (enterprise enrichment, pricing criticism)
- [x] **TREV-04**: Clearbit review (enrichment, Salesforce acquisition context)
- [x] **TREV-05**: FullEnrich review (waterfall enrichment)
- [x] **TREV-06**: Lusha review (contact data)
- [x] **TREV-07**: Cognism review (EMEA-focused enrichment)
- [x] **TREV-08**: LeadIQ review (prospecting)
- [x] **TREV-09**: Persana review (AI enrichment)
- [x] **TREV-10**: Instantly review (outbound sequencing, 20-40% affiliate)
- [x] **TREV-11**: Smartlead review (outbound sequencing)
- [x] **TREV-12**: Outreach review (enterprise sequencing)
- [x] **TREV-13**: Salesloft review (enterprise sequencing)
- [x] **TREV-14**: Lemlist review (outbound + personalization)
- [x] **TREV-15**: HeyReach review (LinkedIn automation)
- [x] **TREV-16**: Woodpecker review (cold email)
- [x] **TREV-17**: HubSpot review (CRM for GTM Engineers)
- [x] **TREV-18**: Salesforce review (CRM for GTM Engineers)
- [x] **TREV-19**: Pipedrive review (SMB CRM)
- [x] **TREV-20**: Close review (sales-focused CRM)
- [x] **TREV-21**: Attio review (modern CRM)
- [x] **TREV-22**: Make review (workflow automation)
- [x] **TREV-23**: n8n review (self-hosted automation)
- [x] **TREV-24**: Zapier review (no-code automation)
- [x] **TREV-25**: 6sense review (intent data)
- [x] **TREV-26**: Bombora review (intent data)
- [x] **TREV-27**: LinkedIn Sales Navigator review
- [x] **TREV-28**: PhantomBuster review (LinkedIn automation)
- [x] **TREV-29**: Segment review (CDP/analytics)
- [x] **TREV-30**: PostHog review (product analytics)

### Tool Category Indexes

- [x] **TCAT-01**: Data Enrichment & Orchestration category index
- [x] **TCAT-02**: Outbound Sequencing category index
- [x] **TCAT-03**: CRM category index
- [x] **TCAT-04**: Workflow Automation category index
- [x] **TCAT-05**: AI & LLM Tools category index
- [x] **TCAT-06**: Intent & Signal Data category index
- [x] **TCAT-07**: Analytics & Product Signals category index
- [x] **TCAT-08**: LinkedIn & Social category index

### Tool Comparisons

- [x] **TCMP-01**: Clay vs Apollo
- [x] **TCMP-02**: Clay vs ZoomInfo
- [x] **TCMP-03**: Instantly vs Smartlead
- [x] **TCMP-04**: Outreach vs Salesloft
- [x] **TCMP-05**: HubSpot vs Salesforce (deep comparison)
- [x] **TCMP-06**: Make vs n8n
- [x] **TCMP-07**: Make vs Zapier
- [x] **TCMP-08**: Apollo vs ZoomInfo
- [x] **TCMP-09**: Lemlist vs Instantly
- [x] **TCMP-10**: Clay vs Clearbit
- [x] **TCMP-11**: 6sense vs Bombora
- [x] **TCMP-12**: Mixpanel vs Amplitude
- [x] **TCMP-13**: Close vs Pipedrive
- [x] **TCMP-14**: HeyReach vs Expandi
- [x] **TCMP-15**: Segment vs PostHog
- [x] **TCMP-16**: Hightouch vs Census
- [x] **TCMP-17**: LinkedIn Sales Nav vs Apollo
- [x] **TCMP-18**: Cognism vs ZoomInfo
- [x] **TCMP-19**: LeadIQ vs Lusha
- [x] **TCMP-20**: Smartlead vs Lemlist

### Alternatives Pages

- [x] **TALT-01**: Clay alternatives
- [x] **TALT-02**: Apollo alternatives
- [x] **TALT-03**: ZoomInfo alternatives
- [x] **TALT-04**: Instantly alternatives
- [x] **TALT-05**: Outreach alternatives
- [x] **TALT-06**: HubSpot alternatives
- [x] **TALT-07**: Salesforce alternatives
- [x] **TALT-08**: Zapier alternatives
- [x] **TALT-09**: 6sense alternatives
- [x] **TALT-10**: LinkedIn Sales Navigator alternatives

### Best-For Roundups

- [x] **TBST-01**: Best GTM tools for startups
- [x] **TBST-02**: Best GTM tools for enterprise
- [x] **TBST-03**: Best free GTM tools
- [x] **TBST-04**: Best data enrichment tools
- [x] **TBST-05**: Best outbound sequencing tools
- [x] **TBST-06**: Best CRM for GTM Engineers
- [x] **TBST-07**: Best workflow automation tools
- [x] **TBST-08**: Best AI tools for GTM
- [x] **TBST-09**: Best LinkedIn prospecting tools
- [x] **TBST-10**: Best intent data platforms

### Glossary

- [x] **GLOS-01**: Glossary index page with alphabetical listing and category grouping
- [x] **GLOS-02**: 50 individual glossary term pages (300-600 words each, definition, examples, related links)

### Job Board

- [x] **JOBS-01**: Job board page with cards, filters (seniority, location, remote), aggregate stats banner
- [x] **JOBS-02**: Build pipeline to read scraper JSON exports from data/ directory

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
| TREV-01 | Phase 8 | Complete |
| TREV-02 | Phase 8 | Complete |
| TREV-03 | Phase 8 | Complete |
| TREV-04 | Phase 8 | Complete |
| TREV-05 | Phase 8 | Complete |
| TREV-06 | Phase 8 | Complete |
| TREV-07 | Phase 8 | Complete |
| TREV-08 | Phase 8 | Complete |
| TREV-09 | Phase 8 | Complete |
| TREV-10 | Phase 8 | Complete |
| TREV-11 | Phase 8 | Complete |
| TREV-12 | Phase 8 | Complete |
| TREV-13 | Phase 8 | Complete |
| TREV-14 | Phase 8 | Complete |
| TREV-15 | Phase 8 | Complete |
| TREV-16 | Phase 8 | Complete |
| TREV-17 | Phase 8 | Complete |
| TREV-18 | Phase 8 | Complete |
| TREV-19 | Phase 8 | Complete |
| TREV-20 | Phase 8 | Complete |
| TREV-21 | Phase 8 | Complete |
| TREV-22 | Phase 8 | Complete |
| TREV-23 | Phase 8 | Complete |
| TREV-24 | Phase 8 | Complete |
| TREV-25 | Phase 8 | Complete |
| TREV-26 | Phase 8 | Complete |
| TREV-27 | Phase 8 | Complete |
| TREV-28 | Phase 8 | Complete |
| TREV-29 | Phase 8 | Complete |
| TREV-30 | Phase 8 | Complete |
| TCAT-01 | Phase 9 | Complete |
| TCAT-02 | Phase 9 | Complete |
| TCAT-03 | Phase 9 | Complete |
| TCAT-04 | Phase 9 | Complete |
| TCAT-05 | Phase 9 | Complete |
| TCAT-06 | Phase 9 | Complete |
| TCAT-07 | Phase 9 | Complete |
| TCAT-08 | Phase 9 | Complete |
| TCMP-01 | Phase 9 | Complete |
| TCMP-02 | Phase 9 | Complete |
| TCMP-03 | Phase 9 | Complete |
| TCMP-04 | Phase 9 | Complete |
| TCMP-05 | Phase 9 | Complete |
| TCMP-06 | Phase 9 | Complete |
| TCMP-07 | Phase 9 | Complete |
| TCMP-08 | Phase 9 | Complete |
| TCMP-09 | Phase 9 | Complete |
| TCMP-10 | Phase 9 | Complete |
| TCMP-11 | Phase 9 | Complete |
| TCMP-12 | Phase 9 | Complete |
| TCMP-13 | Phase 9 | Complete |
| TCMP-14 | Phase 9 | Complete |
| TCMP-15 | Phase 9 | Complete |
| TCMP-16 | Phase 9 | Complete |
| TCMP-17 | Phase 9 | Complete |
| TCMP-18 | Phase 9 | Complete |
| TCMP-19 | Phase 9 | Complete |
| TCMP-20 | Phase 9 | Complete |
| TALT-01 | Phase 10 | Complete |
| TALT-02 | Phase 10 | Complete |
| TALT-03 | Phase 10 | Complete |
| TALT-04 | Phase 10 | Complete |
| TALT-05 | Phase 10 | Complete |
| TALT-06 | Phase 10 | Complete |
| TALT-07 | Phase 10 | Complete |
| TALT-08 | Phase 10 | Complete |
| TALT-09 | Phase 10 | Complete |
| TALT-10 | Phase 10 | Complete |
| TBST-01 | Phase 10 | Complete |
| TBST-02 | Phase 10 | Complete |
| TBST-03 | Phase 10 | Complete |
| TBST-04 | Phase 10 | Complete |
| TBST-05 | Phase 10 | Complete |
| TBST-06 | Phase 10 | Complete |
| TBST-07 | Phase 10 | Complete |
| TBST-08 | Phase 10 | Complete |
| TBST-09 | Phase 10 | Complete |
| TBST-10 | Phase 10 | Complete |
| GLOS-01 | Phase 11 | Complete |
| GLOS-02 | Phase 11 | Complete |
| JOBS-01 | Phase 11 | Complete |
| JOBS-02 | Phase 11 | Complete |
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
