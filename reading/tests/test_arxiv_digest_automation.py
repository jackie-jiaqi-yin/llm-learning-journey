from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from reading.scripts.arxiv_digest_automation import TopicConfig, _update_topic_page


class ArxivDigestAutomationTest(unittest.TestCase):
    def test_update_topic_page_inserts_new_date_and_removes_placeholder(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page = root / "agent.md"
            page.write_text(
                """# Agent

<!-- arxiv-topic: agent -->
<!-- arxiv-runs:start -->
<!-- Future automation: insert the newest run below as "- [YYYY-MM-DD](reports/agent/YYYY-MM-DD.html)" and keep runs in reverse chronological order. -->

_No automated arXiv summary runs have been added yet._

<!-- arxiv-runs:end -->
""",
                encoding="utf-8",
            )

            config = TopicConfig(
                repo_root=root,
                topic_page=page,
                report_slug="agent",
                run_date="2026-05-24",
            )

            updated, changed = _update_topic_page(config)

            self.assertTrue(changed)
            self.assertIn("- [2026-05-24](reports/agent/2026-05-24.html)", updated)
            self.assertNotIn("_No automated arXiv summary runs have been added yet._", updated)
            self.assertIn('[YYYY-MM-DD](reports/agent/YYYY-MM-DD.html)', updated)

    def test_update_topic_page_dedupes_same_date_and_keeps_existing_order_after_newest(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page = root / "llm-post-train.md"
            page.write_text(
                """# LLM Post-Train

<!-- arxiv-topic: llm-post-train -->
<!-- arxiv-runs:start -->
- [2026-05-17](reports/llm-post-train/2026-05-17.html)
- [2026-05-10](reports/llm-post-train/2026-05-10.html)
- [2026-05-17](reports/llm-post-train/2026-05-17.html)
<!-- arxiv-runs:end -->
""",
                encoding="utf-8",
            )

            config = TopicConfig(
                repo_root=root,
                topic_page=page,
                report_slug="llm-post-train",
                run_date="2026-05-24",
            )

            updated, changed = _update_topic_page(config)
            lines = [line.strip() for line in updated.splitlines() if line.strip().startswith("- [")]

            self.assertTrue(changed)
            self.assertEqual(
                lines,
                [
                    "- [2026-05-24](reports/llm-post-train/2026-05-24.html)",
                    "- [2026-05-17](reports/llm-post-train/2026-05-17.html)",
                    "- [2026-05-10](reports/llm-post-train/2026-05-10.html)",
                ],
            )


if __name__ == "__main__":
    unittest.main()
