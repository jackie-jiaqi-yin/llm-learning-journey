#!/usr/bin/env python3
"""Deterministic helpers for recurring arXiv digest automations.

This script handles the non-LLM parts of the weekly digest workflow:
- repo preflight and idempotency checks
- copying the rendered HTML report into the website repo
- maintaining the topic date index
- local verification
- cleanup of temporary artifacts
- commit/push and remote/public verification
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
from datetime import datetime


LA_TZ = ZoneInfo("America/Los_Angeles")
PLACEHOLDER_PREFIX = "<!-- Future automation:"
FORBIDDEN_PAGE_TERMS = [
    "Automation Contract",
    "Topic Scope",
    "Papers summarized",
    "Key Themes",
    "Practical Takeaways",
]


class AutomationError(RuntimeError):
    def __init__(self, step: str, message: str):
        self.step = step
        super().__init__(message)


@dataclass
class TopicConfig:
    repo_root: Path
    topic_page: Path
    report_slug: str
    run_date: str

    @property
    def report_path(self) -> Path:
        return self.topic_page.parent / "reports" / self.report_slug / f"{self.run_date}.html"

    @property
    def expected_link(self) -> str:
        return f"- [{self.run_date}](reports/{self.report_slug}/{self.run_date}.html)"


def _json_print(payload: dict) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _run(
    cmd: list[str],
    *,
    cwd: Path,
    retries: int = 1,
    backoff_sec: int = 1,
    step: str,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    last: subprocess.CompletedProcess[str] | None = None
    for attempt in range(1, retries + 1):
        last = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            capture_output=capture,
        )
        if last.returncode == 0:
            return last
        if attempt < retries:
            time.sleep(backoff_sec * attempt)
    assert last is not None
    stderr = (last.stderr or "").strip()
    stdout = (last.stdout or "").strip()
    details = stderr or stdout or f"Command failed with exit code {last.returncode}"
    raise AutomationError(step, f"{' '.join(cmd)} :: {details}")


def _today_la() -> str:
    return datetime.now(LA_TZ).strftime("%Y-%m-%d")


def _load_topic_config(args: argparse.Namespace) -> TopicConfig:
    repo_root = Path(args.repo_root).resolve()
    topic_page = Path(args.topic_page)
    if not topic_page.is_absolute():
        topic_page = repo_root / topic_page
    return TopicConfig(
        repo_root=repo_root,
        topic_page=topic_page.resolve(),
        report_slug=args.report_slug,
        run_date=args.run_date or _today_la(),
    )


def _check_dns_and_https(host: str, url: str, timeout_sec: int) -> dict:
    try:
        ip = socket.gethostbyname(host)
    except OSError as exc:
        raise AutomationError("preflight:reachability", f"DNS failed for {host}: {exc}") from exc

    req = Request(url, method="HEAD", headers={"User-Agent": "codex-arxiv-digest-automation/1.0"})
    try:
        with urlopen(req, timeout=timeout_sec) as resp:
            status = getattr(resp, "status", None) or resp.getcode()
    except HTTPError as exc:
        status = exc.code
    except URLError as exc:
        raise AutomationError("preflight:reachability", f"HTTPS failed for {url}: {exc}") from exc

    return {"host": host, "ip": ip, "url": url, "status": status}


def _extract_existing_links(page_text: str, report_slug: str) -> list[str]:
    lines = []
    for line in page_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [") and f"](reports/{report_slug}/" in stripped and stripped.endswith(".html)"):
            lines.append(stripped)
    return lines


def _update_topic_page(config: TopicConfig) -> tuple[str, bool]:
    content = config.topic_page.read_text(encoding="utf-8")
    start_marker = "<!-- arxiv-runs:start -->"
    end_marker = "<!-- arxiv-runs:end -->"
    if start_marker not in content or end_marker not in content:
        raise AutomationError("update-topic-page", f"Missing run markers in {config.topic_page}")

    before, remainder = content.split(start_marker, 1)
    middle, after = remainder.split(end_marker, 1)

    existing = []
    for line in middle.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(PLACEHOLDER_PREFIX):
            continue
        if stripped == "_No automated arXiv summary runs have been added yet._":
            continue
        if stripped.startswith("- [") and f"](reports/{config.report_slug}/" in stripped:
            existing.append(stripped)

    deduped = [config.expected_link]
    for line in existing:
        if line != config.expected_link and line not in deduped:
            deduped.append(line)

    rebuilt_middle = "\n" + "\n".join(deduped) + "\n"
    updated = before + start_marker + rebuilt_middle + end_marker + after
    changed = updated != content
    if changed:
        config.topic_page.write_text(updated, encoding="utf-8")
    return updated, changed


def cmd_preflight(args: argparse.Namespace) -> int:
    config = _load_topic_config(args)
    repo_root = config.repo_root

    status = _run(["git", "status", "--short"], cwd=repo_root, step="preflight:status")
    if status.stdout.strip():
        raise AutomationError("preflight:status", status.stdout.strip())

    branch = _run(["git", "branch", "--show-current"], cwd=repo_root, step="preflight:branch").stdout.strip()
    if branch != "main":
        _run(["git", "checkout", "main"], cwd=repo_root, step="preflight:checkout-main")
        branch = "main"

    _run(["git", "fetch", "origin"], cwd=repo_root, retries=3, backoff_sec=1, step="preflight:fetch")
    _run(["git", "merge", "--ff-only", "origin/main"], cwd=repo_root, step="preflight:pull")

    reachability = [
        _check_dns_and_https("github.com", "https://github.com", args.timeout_sec),
        _check_dns_and_https("export.arxiv.org", "https://export.arxiv.org", args.timeout_sec),
    ]

    topic_text = config.topic_page.read_text(encoding="utf-8")
    report_exists = config.report_path.exists()
    link_exists = config.expected_link in topic_text

    payload = {
        "branch": branch,
        "repo_root": str(repo_root),
        "run_date": config.run_date,
        "topic_page": str(config.topic_page),
        "report_path": str(config.report_path),
        "link_exists": link_exists,
        "report_exists": report_exists,
        "verification_only": link_exists and report_exists,
        "reachability": reachability,
    }
    return _json_print(payload)


def cmd_publish_local(args: argparse.Namespace) -> int:
    config = _load_topic_config(args)
    source_report = Path(args.source_report_html).resolve()
    if not source_report.exists():
        raise AutomationError("publish-local", f"Missing source report HTML: {source_report}")

    config.report_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_report, config.report_path)
    _, page_changed = _update_topic_page(config)

    return _json_print(
        {
            "run_date": config.run_date,
            "topic_page": str(config.topic_page),
            "report_path": str(config.report_path),
            "page_changed": page_changed,
            "report_copied": True,
        }
    )


def _assert(condition: bool, step: str, message: str) -> None:
    if not condition:
        raise AutomationError(step, message)


def cmd_verify_local(args: argparse.Namespace) -> int:
    config = _load_topic_config(args)
    repo_root = config.repo_root

    tests = _run(
        [sys.executable, "-m", "unittest", "reading.tests.test_arxiv_learning_docs"],
        cwd=repo_root,
        step="verify-local:unittest",
    )
    mkdocs = _run([sys.executable, "-m", "mkdocs", "build"], cwd=repo_root / "reading", step="verify-local:mkdocs")

    page_text = config.topic_page.read_text(encoding="utf-8")
    _assert(config.expected_link in page_text, "verify-local:topic-link", f"Missing topic link {config.expected_link}")
    _assert(config.report_path.exists(), "verify-local:report-exists", f"Missing report {config.report_path}")
    for term in FORBIDDEN_PAGE_TERMS:
        _assert(term not in page_text, "verify-local:forbidden-text", f"Found forbidden text {term!r} in {config.topic_page}")

    return _json_print(
        {
            "run_date": config.run_date,
            "unittest_ok": True,
            "mkdocs_ok": True,
            "topic_page": str(config.topic_page),
            "report_path": str(config.report_path),
            "topic_link_verified": True,
            "report_verified": True,
            "forbidden_text_verified": True,
            "unittest_stdout": tests.stdout.strip(),
            "mkdocs_stdout": mkdocs.stdout.strip(),
        }
    )


def _remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def cmd_cleanup(args: argparse.Namespace) -> int:
    removed: list[str] = []
    for raw in args.paths:
        path = Path(raw).resolve()
        if path.exists():
            _remove_path(path)
            removed.append(str(path))
    return _json_print({"removed": removed})


def cmd_commit_push(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()

    before = _run(["git", "status", "--short"], cwd=repo_root, step="commit-push:status-before").stdout.strip()
    for path in args.paths:
        _run(["git", "add", path], cwd=repo_root, step="commit-push:git-add")

    staged = _run(["git", "diff", "--cached", "--name-only"], cwd=repo_root, step="commit-push:staged").stdout.splitlines()
    if not staged:
        head = _run(["git", "rev-parse", "HEAD"], cwd=repo_root, step="commit-push:head").stdout.strip()
        return _json_print(
            {
                "changed": False,
                "commit": "none",
                "push": "skipped",
                "status_before": before,
                "head": head,
            }
        )

    _run(["git", "commit", "-m", args.message], cwd=repo_root, step="commit-push:commit")
    head = _run(["git", "rev-parse", "HEAD"], cwd=repo_root, step="commit-push:head-after").stdout.strip()
    _run(["git", "push", "origin", "main"], cwd=repo_root, retries=3, backoff_sec=1, step="commit-push:push", capture=True)

    return _json_print({"changed": True, "commit": head, "push": "ok", "staged": staged})


def _gh_run_list(repo_root: Path) -> list[dict]:
    out = _run(
        [
            "gh",
            "run",
            "list",
            "--branch",
            "main",
            "--limit",
            "30",
            "--json",
            "databaseId,workflowName,headSha,status,conclusion,url",
        ],
        cwd=repo_root,
        step="wait-workflows:gh-run-list",
    ).stdout
    return json.loads(out)


def cmd_wait_workflows(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    wanted = set(args.workflow_name)
    deadline = time.time() + args.timeout_sec
    matched: dict[str, dict] = {}

    while time.time() < deadline:
        runs = _gh_run_list(repo_root)
        matched = {}
        for workflow in wanted:
            for run in runs:
                if run["workflowName"] == workflow and run["headSha"] == args.commit:
                    matched[workflow] = run
                    break

        if matched.keys() == wanted:
            unfinished = [run for run in matched.values() if run["status"] != "completed"]
            failed = [run for run in matched.values() if run["status"] == "completed" and run["conclusion"] != "success"]
            if failed:
                raise AutomationError("wait-workflows", json.dumps(failed, indent=2))
            if not unfinished:
                return _json_print({"commit": args.commit, "workflows": matched, "result": "success"})
        time.sleep(args.poll_sec)

    raise AutomationError("wait-workflows", f"Timed out waiting for workflows for commit {args.commit}")


def _fetch_status(url: str, timeout_sec: int) -> int:
    req = Request(url, method="HEAD", headers={"User-Agent": "codex-arxiv-digest-automation/1.0"})
    try:
        with urlopen(req, timeout=timeout_sec) as resp:
            return getattr(resp, "status", None) or resp.getcode()
    except HTTPError as exc:
        return exc.code
    except URLError as exc:
        raise AutomationError("verify-public", f"{url}: {exc}") from exc


def cmd_verify_public(args: argparse.Namespace) -> int:
    deadline = time.time() + args.timeout_sec
    latest: dict[str, int] = {}

    while time.time() < deadline:
        latest = {}
        all_ok = True
        for url in args.url:
            status = _fetch_status(url, args.request_timeout_sec)
            latest[url] = status
            if status != 200:
                all_ok = False
        if all_ok:
            return _json_print({"result": "success", "statuses": latest})
        time.sleep(args.poll_sec)

    raise AutomationError("verify-public", json.dumps(latest, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Helpers for arXiv digest automations")
    sub = parser.add_subparsers(dest="command", required=True)

    common_parent = argparse.ArgumentParser(add_help=False)
    common_parent.add_argument("--repo-root", required=True)
    common_parent.add_argument("--topic-page", required=True)
    common_parent.add_argument("--report-slug", required=True)
    common_parent.add_argument("--run-date", help="YYYY-MM-DD; defaults to America/Los_Angeles today")

    preflight = sub.add_parser("preflight", parents=[common_parent])
    preflight.add_argument("--timeout-sec", type=int, default=20)
    preflight.set_defaults(func=cmd_preflight)

    publish_local = sub.add_parser("publish-local", parents=[common_parent])
    publish_local.add_argument("--source-report-html", required=True)
    publish_local.set_defaults(func=cmd_publish_local)

    verify_local = sub.add_parser("verify-local", parents=[common_parent])
    verify_local.set_defaults(func=cmd_verify_local)

    cleanup = sub.add_parser("cleanup")
    cleanup.add_argument("paths", nargs="+")
    cleanup.set_defaults(func=cmd_cleanup)

    commit_push = sub.add_parser("commit-push")
    commit_push.add_argument("--repo-root", required=True)
    commit_push.add_argument("--message", required=True)
    commit_push.add_argument("paths", nargs="+")
    commit_push.set_defaults(func=cmd_commit_push)

    wait_workflows = sub.add_parser("wait-workflows")
    wait_workflows.add_argument("--repo-root", required=True)
    wait_workflows.add_argument("--commit", required=True)
    wait_workflows.add_argument("--timeout-sec", type=int, default=900)
    wait_workflows.add_argument("--poll-sec", type=int, default=15)
    wait_workflows.add_argument("--workflow-name", action="append", required=True)
    wait_workflows.set_defaults(func=cmd_wait_workflows)

    verify_public = sub.add_parser("verify-public")
    verify_public.add_argument("--timeout-sec", type=int, default=600)
    verify_public.add_argument("--poll-sec", type=int, default=20)
    verify_public.add_argument("--request-timeout-sec", type=int, default=20)
    verify_public.add_argument("--url", action="append", required=True)
    verify_public.set_defaults(func=cmd_verify_public)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except AutomationError as exc:
        print(json.dumps({"result": "blocked", "step": exc.step, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
