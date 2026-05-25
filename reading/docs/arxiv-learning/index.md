# arXiv Research Digest

Up-to-date arXiv paper summaries organized by topic.

This section is for recurring arXiv paper digests generated from my Codex `arxiv-latest-summary` workflow. Each topic page is designed as an append-only research log, so future automation can add a new dated update without changing the rest of the site.

## Topics

- **[Agent](agent.md)** - agent architectures, planning, tool use, workflow orchestration, and multi-agent systems.
- **[LLM Post-Train](llm-post-train.md)** - instruction tuning, alignment, preference optimization, reinforcement learning, evaluation, and data quality after pretraining.

## Update Format

Automation should write each run under the target topic page between the `arxiv-runs` markers. Newest runs should appear first, and each run title should use the run date:

```markdown
## YYYY-MM-DD

Summary content for that run.
```

Suggested fields for each run:

- Run window and query scope
- Key research themes
- Notable papers to read first
- Practical takeaways
- Links to generated reports or source paper URLs

## Website Artifact Policy

Weekly automation should keep only the artifacts that are useful on the website:

- The updated topic Markdown page
- The copied HTML report under `reports/<topic-slug>/YYYY-MM-DD.html`

Generated run directories, PDFs, catalogs, recursive chunk files, and other intermediate artifacts should be deleted after the website update is verified and published.
