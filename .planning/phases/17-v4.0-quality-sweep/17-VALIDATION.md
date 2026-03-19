---
phase: 17
slug: v4.0-quality-sweep
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 17 — Validation Strategy

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
- **After every plan wave:** Full build — must show zero warnings
- **Before `/gsd:verify-work`:** Full suite must be green, zero warnings
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 17-01-01 | 01 | 1 | QUAL4-01 | build validation | `python3 scripts/build.py` | Existing | ⬜ pending |
| 17-01-02 | 01 | 1 | QUAL4-02 | build validation | `python3 scripts/build.py` | Existing | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. No new test framework or helpers needed.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Content quality of added words | QUAL4-02 | Subjective quality | Spot-check 2-3 articles that received word count fixes for natural prose |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
