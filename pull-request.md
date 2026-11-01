## Problem and scope

Fixes #296. The Markdown encoding check accepts two common corruption sequences: a UTF-8 em dash and right apostrophe decoded as Windows-1252. Both reported examples reproduce at `f4900e8f17ed1c52d005605680d1a75ea4a2a19e`.

This change is limited to repository-quality validation and its documentation.

## What changed

- Add the two exact missing markers while preserving the existing checks.
- Include the affected filename and detected markers in assertion failures.
- Add 11 file-based regression cases: five corrupt fixtures and six valid Unicode fixtures.
- Document the check and its finite-marker limitation.

The valid fixtures cover correctly encoded punctuation, accents and multilingual text, a standalone lowercase a with circumflex, and the euro sign. The check does not reject every occurrence of the lowercase character shared by the two corrupt sequences.

## Verification

- The two issue-specific regression cases fail against the original implementation and pass with this patch.
- [x] `python -m black --config .github/quality/pyproject.toml --check .github/quality/tests`
- [x] `python -m flake8 --config .github/quality/.flake8 -j 1 .github/quality/tests`
- [x] `python -m pytest -c .github/quality/pyproject.toml .github/quality/tests`: **931 passed** on Python 3.12.14 / Windows.
- [x] Documentation updated for the changed validation behavior.
- [x] No credentials, proprietary source, customer data or generated customer reports included.

An analyzer review was not run: this changes only the repository-maintenance test check, not analyzer/CLI behavior, engineering guidance or code-specific workflow claims. The fixtures are temporary local Markdown files; no hosted service is needed.

## Remaining limitations

This remains a small, marker-based heuristic. Existing broad markers are retained, and other encoding problems or false positives may remain outside this patch's scope.

Prepared with AI assistance. No workflow packs or runtime package code are changed.
