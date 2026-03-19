---
phase: 16
slug: og-image-generation
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 16 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Build-time validator in `build.py:validate_pages()` + OG generator output |
| **Config file** | None (inline in build.py) |
| **Quick run command** | `cd /Users/rome/Documents/projects/gtmepulse && python3 scripts/build.py 2>&1 \| tail -30` |
| **Full suite command** | `cd /Users/rome/Documents/projects/gtmepulse && python3 scripts/build.py` |
| **Estimated runtime** | ~120 seconds (includes OG image generation) |

---

## Sampling Rate

- **After every task commit:** Run `python3 scripts/build.py 2>&1 | tail -30`
- **After every plan wave:** Full build + manual spot-check of 3-5 OG images
- **Before `/gsd:verify-work`:** Full suite must be green, zero warnings, all OG images present
- **Max feedback latency:** 120 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 16-01-01 | 01 | 1 | OG-01, OG-02 | build + smoke | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 16-01-02 | 01 | 1 | OG-03 | build integration | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 16-01-03 | 01 | 1 | OG-04 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `scripts/generate_og_images.py` — OG image generation script with Playwright
- [ ] `og-templates/og-default.html` — fallback template for misc pages
- [ ] `og-templates/og-salary.html` — salary page template with stat highlight
- [ ] `og-templates/og-tool.html` — tool review/comparison template
- [ ] `og-templates/og-glossary.html` — glossary term template
- [ ] Add `og:image` validation check to `validate_pages()`

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| OG image visual quality | OG-02 | Subjective visual assessment | Open 5 generated PNGs, verify fonts load, branding correct, text legible |
| Social preview rendering | OG-04 | External service behavior | Paste 3 URLs into Twitter Card Validator / LinkedIn Post Inspector |
| Title truncation handling | OG-02 | Visual edge case | Find longest title, verify it renders acceptably in OG card |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 120s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
