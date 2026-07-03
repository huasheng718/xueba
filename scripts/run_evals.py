#!/usr/bin/env python3
"""Run deterministic checks for the xueba skill package.

This does not call an LLM. It validates the local skill metadata, eval files,
required expert references, and optionally a generated Markdown note.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "references/note-template.md",
    "references/tag-taxonomy.md",
    "references/obsidian-workflow.md",
    "references/authenticated-sources.md",
    "references/learning-expert.md",
    "references/expert-personality.md",
    "references/expert-capabilities.md",
    "references/xueba-agent.md",
    "references/upgrade-mode.md",
    "scripts/resolve_obsidian_vault.py",
    "scripts/install_obsidian.py",
    "scripts/classify_learning_path.py",
    "scripts/write_obsidian_note.py",
    "scripts/run_evals.py",
    "evals/evals.json",
    "evals/trigger-evals.json",
    "evals/assertions.md",
]

REQUIRED_MAIN_HEADINGS = [
    "## 1. 全景",
    "## 2. 概念",
    "## 3. 正文",
    "## 4. 练习",
    "## 5. 来源",
]

REQUIRED_FRONTMATTER_KEYS = ["title", "tags", "source", "created"]
REQUIRED_TAG_PREFIXES = ["status/", "type/", "domain/", "source/", "access/", "confidence/"]
REQUIRED_AI_YAML_KEYS = ["summary:", "concepts:", "relations:", "keywords:", "qa_pairs:"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(read_text(path))


def add_result(results: list[dict[str, Any]], name: str, passed: bool, evidence: str = "") -> None:
    results.append({"name": name, "passed": passed, "evidence": evidence})


def validate_required_files(root: Path, results: list[dict[str, Any]]) -> None:
    for relative in REQUIRED_FILES:
        path = root / relative
        add_result(results, f"required file exists: {relative}", path.is_file(), str(path))


def validate_skill_metadata(root: Path, results: list[dict[str, Any]]) -> None:
    text = read_text(root / "SKILL.md")
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    add_result(results, "SKILL.md has YAML frontmatter", bool(frontmatter_match))
    if not frontmatter_match:
        return

    frontmatter = frontmatter_match.group(1)
    add_result(results, "skill name remains xueba", re.search(r"^name:\s*xueba\s*$", frontmatter, flags=re.M) is not None)
    description_match = re.search(r"^description:\s*(.+)$", frontmatter, flags=re.M)
    description = description_match.group(1).strip() if description_match else ""
    add_result(results, "description starts with Use when", description.startswith("Use when"), description[:120])
    add_result(results, "frontmatter is under 1024 characters", len(frontmatter) <= 1024, f"{len(frontmatter)} characters")

    for phrase in [
        "Learning Expert Mode",
        "Agent Design Mode",
        "references/expert-personality.md",
        "references/expert-capabilities.md",
        "references/learning-expert.md",
    ]:
        add_result(results, f"SKILL.md references {phrase}", phrase in text)


def validate_learning_expert_refs(root: Path, results: list[dict[str, Any]]) -> None:
    text = read_text(root / "references/learning-expert.md")
    for phrase in [
        "references/expert-personality.md",
        "references/expert-capabilities.md",
        "Role Override",
        "Capability Precheck",
        "Expert Workflow",
        "Quality Gate",
    ]:
        add_result(results, f"learning expert includes {phrase}", phrase in text)

    personality = read_text(root / "references/expert-personality.md")
    capabilities = read_text(root / "references/expert-capabilities.md")
    for phrase in ["学习架构师", "概念建模者", "知识库工程师", "训练教练"]:
        add_result(results, f"personality covers {phrase}", phrase in personality)
    for phrase in ["资料解析专家", "概念建模专家", "学习路径专家", "练习设计专家", "Obsidian 整理专家", "质量审查专家"]:
        add_result(results, f"capabilities cover {phrase}", phrase in capabilities)


def validate_evals(root: Path, results: list[dict[str, Any]]) -> None:
    data = load_json(root / "evals/evals.json")
    add_result(results, "evals skill_name is xueba", data.get("skill_name") == "xueba")
    evals = data.get("evals")
    add_result(results, "evals contains a non-empty list", isinstance(evals, list) and len(evals) > 0, f"{len(evals) if isinstance(evals, list) else 'not-list'}")
    if not isinstance(evals, list):
        return

    seen_ids: set[Any] = set()
    for item in evals:
        eval_id = item.get("id")
        add_result(results, f"eval {eval_id} has unique id", eval_id not in seen_ids)
        seen_ids.add(eval_id)
        add_result(results, f"eval {eval_id} has prompt", bool(str(item.get("prompt", "")).strip()))
        add_result(results, f"eval {eval_id} has expected_output", bool(str(item.get("expected_output", "")).strip()))
        expectations = item.get("expectations")
        add_result(
            results,
            f"eval {eval_id} has machine-checkable expectations",
            isinstance(expectations, list) and len(expectations) >= 4 and all(str(value).strip() for value in expectations),
            f"{len(expectations) if isinstance(expectations, list) else 'missing'} expectations",
        )


def validate_trigger_evals(root: Path, results: list[dict[str, Any]]) -> None:
    data = load_json(root / "evals/trigger-evals.json")
    add_result(results, "trigger evals skill_name is xueba", data.get("skill_name") == "xueba")
    should_trigger = data.get("should_trigger")
    should_not_trigger = data.get("should_not_trigger")
    add_result(results, "trigger evals has should_trigger list", isinstance(should_trigger, list) and len(should_trigger) >= 8)
    add_result(results, "trigger evals has should_not_trigger list", isinstance(should_not_trigger, list) and len(should_not_trigger) >= 8)

    for group_name, group in [("should_trigger", should_trigger), ("should_not_trigger", should_not_trigger)]:
        if not isinstance(group, list):
            continue
        for index, item in enumerate(group, start=1):
            add_result(results, f"{group_name} {index} has prompt", bool(str(item.get("prompt", "")).strip()))
            add_result(results, f"{group_name} {index} has reason", bool(str(item.get("reason", "")).strip()))


def frontmatter_block(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    return match.group(1) if match else ""


def validate_note(note_path: Path, results: list[dict[str, Any]]) -> None:
    text = read_text(note_path)
    fm = frontmatter_block(text)
    add_result(results, "note has YAML frontmatter", bool(fm))
    for key in REQUIRED_FRONTMATTER_KEYS:
        add_result(results, f"note frontmatter has {key}", re.search(rf"^{re.escape(key)}\s*:", fm, flags=re.M) is not None)
    for prefix in REQUIRED_TAG_PREFIXES:
        add_result(results, f"note frontmatter has {prefix} tag", prefix in fm)

    for heading in REQUIRED_MAIN_HEADINGS:
        add_result(results, f"note has heading {heading}", re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.M) is not None)

    for phrase in ["一句话系统本质", "学习目标", "前置知识", "Why", "What", "How", "Limits", "Evidence", "Links"]:
        add_result(results, f"note contains {phrase}", phrase in text)

    add_result(results, "note uses stable concept ID C001", "C001" in text)
    add_result(results, "note separates source and inference labels", all(label in text for label in ["原文依据", "推论", "待补充", "待验证"]))
    add_result(results, "note includes AI 读取区", "AI 读取区" in text)
    for key in REQUIRED_AI_YAML_KEYS:
        add_result(results, f"AI 读取区 has {key}", key in text)
    add_result(results, "note includes quality checklist", "质量检查" in text)
    add_result(results, "note does not expose temporary paths", "/private/tmp" not in text and "/tmp" not in text)


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in results if not item["passed"]]
    return {
        "ok": not failed,
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic xueba skill checks.")
    parser.add_argument("--root", default=None, help="Skill root. Defaults to the parent of this script directory.")
    parser.add_argument("--note", default=None, help="Optional generated Markdown note to validate.")
    parser.add_argument("--json", action="store_true", help="Print full JSON result.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve() if args.root else Path(__file__).resolve().parents[1]
    results: list[dict[str, Any]] = []

    try:
        validate_required_files(root, results)
        validate_skill_metadata(root, results)
        validate_learning_expert_refs(root, results)
        validate_evals(root, results)
        validate_trigger_evals(root, results)
        if args.note:
            validate_note(Path(args.note).expanduser().resolve(), results)
    except (OSError, json.JSONDecodeError) as exc:
        add_result(results, "runner completed without parser errors", False, str(exc))

    report = summarize(results)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if report["ok"] else "FAIL"
        print(f"{status}: {report['passed']} passed, {report['failed']} failed")
        for item in results:
            marker = "ok" if item["passed"] else "FAIL"
            evidence = f" - {item['evidence']}" if item.get("evidence") else ""
            print(f"[{marker}] {item['name']}{evidence}")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
