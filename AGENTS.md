# AGENTS.md

## Project Scope

This repository contains Jackie Yin's public LLM learning website and related
course notes, code examples, and automated arXiv research digests.

The published MkDocs site lives under `reading/`:

- MkDocs config: `reading/mkdocs.yml`
- Public pages: `reading/docs/`
- arXiv digest pages: `reading/docs/arxiv-learning/`
- Topic notes: `reading/docs/topics/`
- Tests: `reading/tests/`

## Site SEO Maintenance

When adding or materially changing public learning content, update the site's
search-facing pages so the new material can be discovered by readers and search
engines.

This applies especially to changes under:

- `reading/docs/topics/`
- `reading/docs/arxiv-learning/`
- `reading/docs/talks/`
- `reading/docs/courses/`
- `genai-5day-course-with-google/`
- `huggingface-agent-ai-course/`
- `huggingface-finetune-llm/`

Do not update SEO pages for tiny typo fixes, formatting-only edits, broken-link
fixes, or other changes that do not add new searchable subject matter.

## SEO Update Workflow

For material content additions:

1. Scan the changed notes and nearby related notes for real topics, methods,
   paper names, frameworks, tools, benchmarks, and course or conference coverage.
2. Update the relevant public entry pages with visible, natural text:
   - `reading/docs/index.md`
   - `reading/docs/topics/index.md`
   - `reading/docs/courses/index.md`
   - `reading/docs/talks/index.md`
   - `reading/docs/about.md`
   - `reading/docs/arxiv-learning/index.md`
   - specific arXiv topic pages such as `agent.md` or `llm-post-train.md`
3. Update `site_description` in `reading/mkdocs.yml` when the site's top-level
   topic coverage materially changes.
4. Add or update tests that protect important searchable coverage, usually in
   `reading/tests/test_site_seo_docs.py` or another focused docs test.

Use reader-facing prose. Do not add hidden keyword stuffing, irrelevant terms,
or meta keyword lists. Prefer clear topic descriptions and internal links.

## arXiv Digest Automation Rules

Preserve the automation markers in arXiv topic pages:

- `<!-- arxiv-topic: ... -->`
- `<!-- arxiv-runs:start -->`
- `<!-- arxiv-runs:end -->`

Do not reorder or remove existing report links unless the task is specifically
about fixing the digest index. New report links should remain newest-first and
deduplicated by date.

For recurring digest work, keep the established flow:

`preflight -> prepare -> synthesis -> finalize -> publish-local -> verify-local -> cleanup -> commit-push -> wait-workflows -> verify-public`

Treat `prepare` as a hard gate. If `prepare` fails because of arXiv 429s,
timeouts, missing `run_manifest.json`, or missing `catalog.csv`, stop and report
the exact failure instead of improvising downstream publishing.

## Verification

Before claiming site or SEO work is complete, run the relevant tests:

```bash
python -m pytest reading/tests
```

For site-rendering work, also run:

```bash
python -m mkdocs build --config-file reading/mkdocs.yml --site-dir /tmp/llm-learning-site
```

If strict build is used and fails on pre-existing warnings, report the warnings
and also run the non-strict build that matches the GitHub Pages deployment path.

When publishing to GitHub Pages:

1. Push the intended branch, usually `main`.
2. Wait for the `Deploy MkDocs to GitHub Pages` workflow to finish.
3. Verify public URLs with HTTP 200 checks.
4. For SEO changes, verify the public HTML contains the expected visible text,
   `robots.txt` is reachable, and `sitemap.xml` includes relevant public pages.

Do not claim a published site change is live until the workflow succeeds and
the public page content has been checked.

## Git Hygiene

The worktree may contain unrelated user changes. Do not revert, stage, commit,
or rewrite changes you did not make unless explicitly asked.

When committing SEO or site changes, stage only the files relevant to the task.
If a file contains both user changes and task changes, use partial staging or a
clean temporary worktree to verify the exact patch being committed.

Ignore local accidental `$CODEX_HOME/` paths unless the user explicitly asks to
inspect or clean them up.
