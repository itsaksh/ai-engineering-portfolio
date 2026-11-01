# AI Engineering Portfolio

Three AI-assisted Python developer-tool projects prepared in November 2026, with source, reproducible evidence and explicit limitations. The code and contribution artifacts are public; personal resume files are not part of these repositories.

| Project | Source and evidence | What it demonstrates |
| --- | --- | --- |
| 1. Repository Context MCP | [Public repository](https://github.com/itsaksh/repo-context-mcp) | Eight read-only MCP tools, conservative Python AST relationships, source citations, official SDK integration and a pinned Click demo. |
| 2. Retrieval and Context Evaluation Lab | [Public repository](https://github.com/itsaksh/retrieval-eval-lab) | Overlap, BM25, local MiniLM embeddings, rank fusion and exact WordPiece packing budgets on 39 cited excerpts and 24 authored queries. |
| 3. UnvibeCode quality contribution | [Upstream PR #392](https://github.com/FinanceFlash/unvibecode/pull/392) · [Public fork branch](https://github.com/itsaksh/unvibecode/tree/fix/markdown-encoding-regressions) | Reproduce issue #296, implement a narrow encoding-check fix, add 11 Unicode regression cases and pass the 931-test public quality suite locally. |

The contribution is an open pull request, not a merged or accepted change. CI and publication records are in each project's validation documents and this repository's `STATUS.json`.

## Run and explain project 3

Read [the contribution case study](CONTRIBUTION.md), [the submitted PR description](pull-request.md), and the before/after JSON records in `evidence/`. The [patch](issue-296.patch) changes exactly three upstream files and retains the upstream Apache-2.0 contribution license.

From a local UnvibeCode checkout containing the original revision and the fix, install its `.github/quality/requirements.txt` into a virtual environment. Then run this repository's portable reproduction script:

```sh
python reproduce.py --checkout /path/to/unvibecode --revision f4900e8f17ed1c52d005605680d1a75ea4a2a19e --expect before --output evidence/before.json
python reproduce.py --checkout /path/to/unvibecode --expect after --output evidence/after.json
```

The first command confirms the two misses in the original check. The second confirms they are fixed while the valid Unicode cases still pass. Use `--git /path/to/git` if Git is not on PATH. The 11-case upstream regression file adds further valid-fixture coverage.

## Contribution and measurement honesty

These implementations were created with AI assistance. Akshaya should run and understand them, review their design and make a change she can explain before describing her own contribution in an interview. No historic commits, production usage, external users, merged contribution or guaranteed hiring outcome is claimed.

The retrieval scores describe a small authored relevance set, not an independent production benchmark. Embedding truncation, failed queries and evidence lost during packing remain visible in the report. The encoding check remains a finite marker heuristic.

Original code in projects 1 and 2 is MIT licensed; Click excerpts retain BSD-3-Clause notices. The UnvibeCode contribution and this case study use Apache-2.0. Model weights are downloaded separately under their own license.
