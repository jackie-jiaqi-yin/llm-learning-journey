from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "reading" / "docs"
MKDOCS_CONFIG = ROOT / "reading" / "mkdocs.yml"
POST_TRAIN_PAGE = DOCS / "arxiv-learning" / "llm-post-train.md"
POST_TRAIN_REPORTS = DOCS / "arxiv-learning" / "reports" / "llm-post-train"


EXPECTED_TOPIC_PAGES = {
    "Agent": "arxiv-learning/agent.md",
    "LLM Post-Train": "arxiv-learning/llm-post-train.md",
}

EXPECTED_TOPIC_REPORTS = {
    "Agent": "agent",
    "LLM Post-Train": "llm-post-train",
}


class ArxivLearningDocsTest(unittest.TestCase):
    def test_mkdocs_nav_exposes_arxiv_research_digest_top_level_tab(self):
        config = yaml.load(MKDOCS_CONFIG.read_text(), Loader=yaml.BaseLoader)

        tab_entries = [
            item["arXiv Research Digest"]
            for item in config["nav"]
            if isinstance(item, dict) and "arXiv Research Digest" in item
        ]

        self.assertEqual(len(tab_entries), 1)
        tab_nav = tab_entries[0]
        self.assertIn("arxiv-learning/index.md", tab_nav)

        topic_links = {}
        for item in tab_nav:
            if isinstance(item, dict):
                topic_links.update(item)

        self.assertEqual(topic_links, EXPECTED_TOPIC_PAGES)

    def test_topic_pages_define_stable_automation_markers(self):
        for topic, relative_path in EXPECTED_TOPIC_PAGES.items():
            with self.subTest(topic=topic):
                page_path = DOCS / relative_path
                self.assertTrue(page_path.exists(), f"{relative_path} should exist")
                content = page_path.read_text()

                self.assertIn("<!-- arxiv-topic:", content)
                self.assertIn("<!-- arxiv-runs:start -->", content)
                self.assertIn("<!-- arxiv-runs:end -->", content)
                report_slug = EXPECTED_TOPIC_REPORTS[topic]
                self.assertIn(
                    f"[YYYY-MM-DD](reports/{report_slug}/YYYY-MM-DD.html)",
                    content,
                )

    def test_arxiv_topic_pages_are_date_indexes_with_direct_report_links(self):
        for topic, relative_path in EXPECTED_TOPIC_PAGES.items():
            with self.subTest(topic=topic):
                report_slug = EXPECTED_TOPIC_REPORTS[topic]
                page_path = DOCS / relative_path
                report_dir = DOCS / "arxiv-learning" / "reports" / report_slug
                content = page_path.read_text()

                self.assertTrue(report_dir.exists())
                self.assertTrue((report_dir / ".gitkeep").exists())
                self.assertNotIn("Automation Contract", content)
                self.assertNotIn("Topic Scope", content)
                self.assertNotIn("Papers summarized", content)
                self.assertNotIn("Key Themes", content)
                self.assertNotIn("Practical Takeaways", content)

                run_links = re.findall(
                    rf"- \[(\d{{4}}-\d{{2}}-\d{{2}})\]\(reports/{report_slug}/\1\.html\)",
                    content,
                )
                self.assertEqual(run_links, sorted(run_links, reverse=True))

                for run_date in run_links:
                    self.assertTrue((report_dir / f"{run_date}.html").exists())

        post_train_links = re.findall(
            r"- \[(\d{4}-\d{2}-\d{2})\]\(reports/llm-post-train/\1\.html\)",
            POST_TRAIN_PAGE.read_text(),
        )
        self.assertIn("2026-05-24", post_train_links)


if __name__ == "__main__":
    unittest.main()
