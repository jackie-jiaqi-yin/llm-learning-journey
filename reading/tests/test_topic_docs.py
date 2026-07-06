from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "reading" / "docs"
MKDOCS_CONFIG = ROOT / "reading" / "mkdocs.yml"
TOPIC_LABEL = "General Knowledge of Natural Language"
TOPIC_INDEX = "topics/Natural-Language/index.md"
TOPIC_NOTES = "topics/Natural-Language/notes.md"
TOPIC_DIR = DOCS / "topics" / "Natural-Language"

EXPECTED_FIGURES = {
    "attention-full-steps.png",
    "attention.png",
    "encoder-decoder.png",
    "gpt-left-to-right.png",
    "lstm-memory-cell.png",
    "lstm-memory.png",
    "rnn-elememt.png",
    "seq2seq-encoder-decoder.png",
    "seq2seq.png",
    "teacher-forcing.png",
    "transformer-decoder-cross-attention.png",
    "transformer-multi-head-attention.png",
    "transformer-self-attention-qkv.png",
}

EXPECTED_TOP_LEVEL_NOTE_SECTIONS = [
    "Fundamentals of Language Models",
    "Modern Neural Architectures",
]

EXPECTED_NOTE_SUBSECTIONS = [
    "Encoder and Decoder",
    "Recurrent Neural Networks (RNN)",
    "Long Short-Term Memory (LSTM)",
    "Sequence-to-Sequence Models",
    "Attention",
    "Perplexity",
    "Transformer",
    "BERT",
    "GPT",
    "Why Do Modern Large Language Models Use Decoder-Only Architectures?",
]


class TopicDocsTest(unittest.TestCase):
    def test_natural_language_topic_is_exposed_in_nav_and_overview(self):
        config = yaml.load(MKDOCS_CONFIG.read_text(), Loader=yaml.BaseLoader)

        topics_entries = [
            item["Topics"]
            for item in config["nav"]
            if isinstance(item, dict) and "Topics" in item
        ]

        self.assertEqual(len(topics_entries), 1)
        topics_nav = topics_entries[0]
        topic_links = {}
        for item in topics_nav:
            if isinstance(item, dict):
                topic_links.update(item)

        self.assertIn(TOPIC_LABEL, topic_links)
        self.assertIn(TOPIC_INDEX, topic_links[TOPIC_LABEL])
        self.assertIn({ "Language Model Fundamentals": TOPIC_NOTES }, topic_links[TOPIC_LABEL])

        overview = (DOCS / "topics" / "index.md").read_text()
        self.assertIn("[General Knowledge of Natural Language](Natural-Language/index.md)", overview)

    def test_natural_language_notes_include_all_imported_markdown_and_figures(self):
        index = (TOPIC_DIR / "index.md").read_text()
        notes = (TOPIC_DIR / "notes.md").read_text()

        self.assertIn("language_model.md", index)
        self.assertIn("Georgia Tech CS7650", notes)
        self.assertIn("# General Knowledge of Natural Language - Notes", notes)

        stale_refs = re.findall(r"\]\(images/[^)]+\)", notes)
        self.assertEqual(stale_refs, [])

        figure_refs = set(re.findall(r"\]\(figs/([^)]+\.png)\)", notes))
        self.assertEqual(figure_refs, EXPECTED_FIGURES)

        for figure in EXPECTED_FIGURES:
            with self.subTest(figure=figure):
                self.assertTrue((TOPIC_DIR / "figs" / figure).exists())

    def test_natural_language_notes_heading_hierarchy_drives_sidebar_toc(self):
        notes = (TOPIC_DIR / "notes.md").read_text()
        headings = [
            (len(match.group(1)), match.group(2).strip())
            for match in re.finditer(r"^(#{1,6})\s+(.+)$", notes, flags=re.MULTILINE)
        ]

        self.assertEqual([title for level, title in headings if level == 1], ["General Knowledge of Natural Language - Notes"])
        self.assertNotIn((2, "Contents"), headings)

        top_level_sections = [title for level, title in headings if level == 2]
        for section in EXPECTED_TOP_LEVEL_NOTE_SECTIONS:
            self.assertIn(section, top_level_sections)

        subsections = [title for level, title in headings if level == 3]
        for subsection in EXPECTED_NOTE_SUBSECTIONS:
            self.assertIn(subsection, subsections)

    def test_natural_language_math_uses_mkdocs_safe_syntax(self):
        notes = (TOPIC_DIR / "notes.md").read_text()

        indented_display_math = [
            line
            for line in notes.splitlines()
            if line.startswith("  ") and line.strip().startswith("$$")
        ]

        self.assertEqual(indented_display_math, [])
        self.assertNotIn(r"\color{", notes)

    def test_natural_language_lists_have_markdown_separators(self):
        lines = (TOPIC_DIR / "notes.md").read_text().splitlines()
        missing_separators = []

        for index, line in enumerate(lines[:-1]):
            current = line.lstrip()
            next_line = lines[index + 1].lstrip()
            starts_list = next_line.startswith("- ") or next_line.startswith("1. ")
            current_is_list_item = current.startswith("- ") or re.match(r"\d+\. ", current)

            if line.strip() and starts_list and not current_is_list_item:
                missing_separators.append(f"{index + 1}: {line}")

        self.assertEqual(missing_separators, [])

    def test_natural_language_nested_lists_use_python_markdown_indentation(self):
        lines = (TOPIC_DIR / "notes.md").read_text().splitlines()
        uneven_nested_markers = []

        for index, line in enumerate(lines, start=1):
            match = re.match(r"( +)(?:[-*+]|\d+\.) ", line)
            if match and len(match.group(1)) % 4 != 0:
                uneven_nested_markers.append(f"{index}: {line}")

        self.assertEqual(uneven_nested_markers, [])


if __name__ == "__main__":
    unittest.main()
