---
phase: 15
slug: insight-articles-batch-2
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 15 — Validation Strategy

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
| 15-01-01 | 01 | 1 | ART-11, ART-12, ART-13 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 15-01-02 | 01 | 1 | ART-14 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 15-02-01 | 02 | 2 | ART-15, ART-16, ART-17 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 15-02-02 | 02 | 2 | ART-18 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |
| 15-03-01 | 03 | 3 | ART-19, ART-20 | build validation | `python3 scripts/build.py` | Will be created | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. No new helpers, validators, or nav changes needed.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Article readability and writing quality | ART-11 through ART-20 | Subjective quality assessment | Read each article, verify voice matches CLAUDE.md standards |
| Internal link relevance | ART-11 through ART-20 | Contextual judgment | Verify 3+ internal links per article point to relevant pages |
| Outbound citation quality | ART-11 through ART-20 | Source authority judgment | Verify 2+ outbound links per article cite authoritative sources |
| ART-17 data rendering | ART-17 | Visual check | Verify pulse report template renders data from JSON correctly |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
