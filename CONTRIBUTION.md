# Project 3 — UnvibeCode encoding-validation contribution

AI-assisted contribution prepared in November 2026 for the public UnvibeCode repository. This is a focused upstream bug fix, not an independently authored copy of UnvibeCode.

## Problem and scope

[Issue #296](https://github.com/FinanceFlash/unvibecode/issues/296) reports that the Markdown quality check misses an em dash and a right apostrophe whose UTF-8 bytes were decoded as Windows-1252. Both cases reproduce at upstream commit `f4900e8f17ed1c52d005605680d1a75ea4a2a19e`.

The patch adds those two exact markers, preserves the existing checks and includes the failing filename and markers in the diagnostic. Eleven regression cases exercise the real file-based check, covering five corrupt fixtures and six valid Unicode fixtures. It does not broadly reject the valid lowercase a with circumflex, correctly encoded punctuation, accents, multilingual text or the euro sign.

Changed upstream files:

- `.github/quality/tests/test_repository_quality.py`
- `.github/quality/tests/test_encoding_regressions.py`
- `.github/quality/README.md`

## Verification

The two new issue cases failed against the original implementation. After the patch, all 931 repository-quality tests pass, including the 11 new regression cases. Black and Flake8 also pass with the upstream configuration. The direct before/after reproduction records are in `evidence/before.json` and `evidence/after.json`.

The check remains a finite marker heuristic, not a general encoding detector. Existing broad markers are preserved; this contribution does not solve every possible false positive or mis-decoding.

This change affects repository-maintenance validation only. No UnvibeCode analyzer/CLI code, engineering guidance, business workflow claims or customer-facing report behavior changes, and no hosted analyzer review was run. Validation uses temporary local Markdown fixtures and the full public repository-quality suite.

## Review and demonstrate

Explain the distinction between UTF-8 bytes and decoded Unicode characters. Run the regression file on the original revision, apply `issue-296.patch`, and rerun the same tests. Point to the exact two misses before the fix and explain why valid Unicode must remain accepted. Akshaya should review and run this AI-assisted work before describing a personal contribution.

The patch follows the upstream Apache-2.0 contribution license. Publication and pull-request status are recorded separately in `STATUS.json`; an open pull request must not be described as merged or accepted.
