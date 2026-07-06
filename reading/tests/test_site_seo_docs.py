from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "reading" / "docs"
MKDOCS_CONFIG = ROOT / "reading" / "mkdocs.yml"


class SiteSeoDocsTest(unittest.TestCase):
    def test_homepage_exposes_broad_scanned_topic_coverage(self):
        content = (DOCS / "index.md").read_text()

        expected_terms = [
            "encoder-decoder architectures",
            "multi-head attention",
            "AutoGen",
            "TaskWeaver",
            "Graph RAG",
            "multimodal embeddings",
            "preference optimization",
            "SFTTrainer",
            "LLM-as-Judges",
            "Qwen3-Coder",
        ]

        for term in expected_terms:
            with self.subTest(term=term):
                self.assertIn(term, content)

    def test_course_and_talk_indexes_include_scanned_note_keywords(self):
        courses = (DOCS / "courses" / "index.md").read_text()
        talks = (DOCS / "talks" / "index.md").read_text()
        about = (DOCS / "about.md").read_text()

        for term in ["vector stores", "smolagents", "LoRA", "chat templates"]:
            with self.subTest(term=term):
                self.assertIn(term, courses)

        for term in ["machine unlearning", "text-3D scene retrieval", "Qwen3-Coder"]:
            with self.subTest(term=term):
                self.assertIn(term, talks)

        for term in ["Graph RAG", "reward modeling", "knowledge distillation"]:
            with self.subTest(term=term):
                self.assertIn(term, about)

    def test_site_description_reflects_expanded_topic_map(self):
        config = yaml.load(MKDOCS_CONFIG.read_text(), Loader=yaml.BaseLoader)
        description = config["site_description"].lower()

        for term in ["ai agents", "rag", "rlhf", "embeddings", "transformers", "multimodal ai"]:
            with self.subTest(term=term):
                self.assertIn(term, description)


if __name__ == "__main__":
    unittest.main()
