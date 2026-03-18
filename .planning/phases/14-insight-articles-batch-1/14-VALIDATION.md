---
phase: 14
slug: insight-articles-batch-1
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 14 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Build-time validator in `build.py:validate_pages()` |
| **Config file** | None (inline in build.py) |
| **Quick run command** | `cd /Users/rome/Documents/projects/gtmepulse && python3 scripts/build.py 2>&1 \| tail -30` |
| **Full suite command** | `cd /Users/rome/Documents/projects/gtmepulse && python3 scripts/build.py` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python3 scripts/build.py 2>&1 | tail -30`
- **After every plan wave:** Full build + manual spot-check of 2-3 articles in browser
- **Before `/gsd:verify-work`:** Full suite must be green, zero warnings
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 14-01-01 | 01 | 1 | ART-01 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 14-01-02 | 01 | 1 | ART-02 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 14-01-03 | 01 | 1 | ART-03 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 14-01-04 | 01 | 1 | ART-04 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 14-01-05 | 01 | 1 | ART-05 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 14-01-06 | 01 | 1 | ART-06 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 14-01-07 | 01 | 1 | ART-07 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 14-01-08 | 01 | 1 | ART-08 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 14-01-09 | 01 | 1 | ART-09 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 14-01-10 | 01 | 1 | ART-10 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `get_article_schema()` helper in templates.py — Article JSON-LD with Person author markup
- [ ] Add `"insights/"` to `DATA_DIRS` in validator
- [ ] Add word count check for insights pages (1300+ floor)

*These must be created before article content tasks can pass validation.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Article readability and writing quality | ART-01 through ART-10 | Subjective quality assessment | Read each article, verify voice matches CLAUDE.md standards, no banned words |
| Internal link relevance | ART-01 through ART-10 | Contextual judgment | Verify 3+ internal links per article point to relevant pages |
| Outbound citation quality | ART-01 through ART-10 | Source authority judgment | Verify 2+ outbound links per article cite authoritative sources |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
