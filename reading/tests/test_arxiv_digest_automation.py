from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from reading.scripts.arxiv_digest_automation import (
    TopicConfig,
    _update_topic_page,
    build_parser,
    cmd_preflight,
    cmd_publish_local,
)


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

    def test_preflight_defaults_to_regeneration_even_if_same_date_artifacts_exist(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page = root / "reading" / "docs" / "arxiv-learning" / "agent.md"
            report = root / "reading" / "docs" / "arxiv-learning" / "reports" / "agent" / "2026-05-24.html"
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text("<html></html>", encoding="utf-8")
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(
                """# Agent

<!-- arxiv-runs:start -->
- [2026-05-24](reports/agent/2026-05-24.html)
<!-- arxiv-runs:end -->
""",
                encoding="utf-8",
            )

            parser = build_parser()
            args = parser.parse_args(
                [
                    "preflight",
                    "--repo-root",
                    str(root),
                    "--topic-page",
                    str(page),
                    "--report-slug",
                    "agent",
                    "--run-date",
                    "2026-05-24",
                ]
            )

            with patch("reading.scripts.arxiv_digest_automation._run") as run_mock, patch(
                "reading.scripts.arxiv_digest_automation._check_dns_and_https"
            ) as reachability_mock, patch(
                "reading.scripts.arxiv_digest_automation._json_print"
            ) as json_print_mock:
                run_mock.side_effect = [
                    type("Proc", (), {"stdout": "", "returncode": 0})(),
                    type("Proc", (), {"stdout": "main\n", "returncode": 0})(),
                    type("Proc", (), {"stdout": "", "returncode": 0})(),
                    type("Proc", (), {"stdout": "", "returncode": 0})(),
                ]
                reachability_mock.side_effect = [
                    {"host": "github.com", "status": 200},
                    {"host": "export.arxiv.org", "status": 200},
                ]
                json_print_mock.side_effect = lambda payload: payload

                payload = cmd_preflight(args)

            self.assertFalse(payload["verification_only"])
            self.assertTrue(payload["link_exists"])
            self.assertTrue(payload["report_exists"])

    def test_preflight_can_still_opt_into_verification_only(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page = root / "reading" / "docs" / "arxiv-learning" / "agent.md"
            report = root / "reading" / "docs" / "arxiv-learning" / "reports" / "agent" / "2026-05-24.html"
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text("<html></html>", encoding="utf-8")
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(
                """# Agent

<!-- arxiv-runs:start -->
- [2026-05-24](reports/agent/2026-05-24.html)
<!-- arxiv-runs:end -->
""",
                encoding="utf-8",
            )

            parser = build_parser()
            args = parser.parse_args(
                [
                    "preflight",
                    "--repo-root",
                    str(root),
                    "--topic-page",
                    str(page),
                    "--report-slug",
                    "agent",
                    "--run-date",
                    "2026-05-24",
                    "--verification-only-if-exists",
                ]
            )

            with patch("reading.scripts.arxiv_digest_automation._run") as run_mock, patch(
                "reading.scripts.arxiv_digest_automation._check_dns_and_https"
            ) as reachability_mock, patch(
                "reading.scripts.arxiv_digest_automation._json_print"
            ) as json_print_mock:
                run_mock.side_effect = [
                    type("Proc", (), {"stdout": "", "returncode": 0})(),
                    type("Proc", (), {"stdout": "main\n", "returncode": 0})(),
                    type("Proc", (), {"stdout": "", "returncode": 0})(),
                    type("Proc", (), {"stdout": "", "returncode": 0})(),
                ]
                reachability_mock.side_effect = [
                    {"host": "github.com", "status": 200},
                    {"host": "export.arxiv.org", "status": 200},
                ]
                json_print_mock.side_effect = lambda payload: payload

                payload = cmd_preflight(args)

            self.assertTrue(payload["verification_only"])

    def test_preflight_allows_unrelated_dirty_files(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page = root / "reading" / "docs" / "arxiv-learning" / "agent.md"
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(
                """# Agent

<!-- arxiv-runs:start -->
<!-- arxiv-runs:end -->
""",
                encoding="utf-8",
            )

            parser = build_parser()
            args = parser.parse_args(
                [
                    "preflight",
                    "--repo-root",
                    str(root),
                    "--topic-page",
                    str(page),
                    "--report-slug",
                    "agent",
                    "--run-date",
                    "2026-05-24",
                ]
            )

            with patch("reading.scripts.arxiv_digest_automation._run") as run_mock, patch(
                "reading.scripts.arxiv_digest_automation._check_dns_and_https"
            ) as reachability_mock, patch(
                "reading.scripts.arxiv_digest_automation._json_print"
            ) as json_print_mock:
                run_mock.side_effect = [
                    type("Proc", (), {"stdout": " M notes/todo.md\n", "returncode": 0})(),
                    type("Proc", (), {"stdout": "main\n", "returncode": 0})(),
                    type("Proc", (), {"stdout": "", "returncode": 0})(),
                    type("Proc", (), {"stdout": "", "returncode": 0})(),
                ]
                reachability_mock.side_effect = [
                    {"host": "github.com", "status": 200},
                    {"host": "export.arxiv.org", "status": 200},
                ]
                json_print_mock.side_effect = lambda payload: payload

                payload = cmd_preflight(args)

            self.assertEqual(payload["run_date"], "2026-05-24")

    def test_preflight_blocks_dirty_topic_artifacts(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page = root / "reading" / "docs" / "arxiv-learning" / "agent.md"
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(
                """# Agent

<!-- arxiv-runs:start -->
<!-- arxiv-runs:end -->
""",
                encoding="utf-8",
            )

            parser = build_parser()
            args = parser.parse_args(
                [
                    "preflight",
                    "--repo-root",
                    str(root),
                    "--topic-page",
                    str(page),
                    "--report-slug",
                    "agent",
                    "--run-date",
                    "2026-05-24",
                ]
            )

            with patch("reading.scripts.arxiv_digest_automation._run") as run_mock:
                run_mock.side_effect = [
                    type(
                        "Proc",
                        (),
                        {
                            "stdout": " M reading/docs/arxiv-learning/agent.md\n?? reading/docs/arxiv-learning/reports/agent/2026-05-24.html\n",
                            "returncode": 0,
                        },
                    )(),
                ]

                with self.assertRaisesRegex(RuntimeError, "reading/docs/arxiv-learning/agent.md"):
                    cmd_preflight(args)

    def test_publish_local_adds_return_navigation_to_report_html(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "source.html"
            source.write_text(
                """<!doctype html>
<html lang="en">
<head>
  <style>body { margin: 0; }</style>
</head>
<body>
  <article class="report-shell">Report</article>
</body>
</html>
""",
                encoding="utf-8",
            )
            page = root / "reading" / "docs" / "arxiv-learning" / "llm-post-train.md"
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(
                """# LLM Post-Train

<!-- arxiv-runs:start -->
<!-- arxiv-runs:end -->
""",
                encoding="utf-8",
            )

            parser = build_parser()
            args = parser.parse_args(
                [
                    "publish-local",
                    "--repo-root",
                    str(root),
                    "--topic-page",
                    str(page),
                    "--report-slug",
                    "llm-post-train",
                    "--run-date",
                    "2026-05-24",
                    "--source-report-html",
                    str(source),
                ]
            )

            with patch("reading.scripts.arxiv_digest_automation._json_print") as json_print_mock:
                json_print_mock.side_effect = lambda payload: payload

                payload = cmd_publish_local(args)

            report_html = Path(payload["report_path"]).read_text(encoding="utf-8")
            self.assertIn("arxiv-report-nav:start", report_html)
            self.assertIn('href="../../llm-post-train/"', report_html)
            self.assertIn('href="../../"', report_html)
            self.assertIn("Back to LLM Post-Train", report_html)


if __name__ == "__main__":
    unittest.main()
