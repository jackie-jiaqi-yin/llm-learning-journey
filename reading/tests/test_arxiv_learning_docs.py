from pathlib import Path
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
                self.assertIn("## YYYY-MM-DD", content)

    def test_post_train_weekly_automation_contract_is_documented(self):
        content = POST_TRAIN_PAGE.read_text()

        self.assertTrue(POST_TRAIN_REPORTS.exists())
        self.assertTrue((POST_TRAIN_REPORTS / ".gitkeep").exists())
        self.assertIn("Weekly cadence: Wednesday 19:00 America/Los_Angeles", content)
        self.assertIn("Window: last 7 days", content)
        self.assertIn("reports/llm-post-train/YYYY-MM-DD.html", content)
        self.assertIn("Only the Markdown entry and copied HTML report are retained", content)


if __name__ == "__main__":
    unittest.main()
