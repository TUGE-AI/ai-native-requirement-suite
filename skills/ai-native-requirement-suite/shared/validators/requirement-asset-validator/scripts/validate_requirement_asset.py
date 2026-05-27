#!/usr/bin/env python3
"""Validate a V3 requirement asset package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


REQUIRED_ROOT = [
    "feature-map.md",
    "prd.md",
    "quality-review.md",
    "human-view.md",
    "ai-coding-input.md",
    "ai-testing-input.md",
]
ID_RE = re.compile(r"\b(FEATURE|STORY|RULE|GWT|QUESTION|RISK|QR)-\d+\b")
PATH_RE = re.compile(r"`([^`]+\.md)`")


@dataclass
class Finding:
    severity: str
    code: str
    location: str
    message: str
    recommendation: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def ids(text: str, prefix: str | None = None) -> set[str]:
    values = {match.group(0) for match in ID_RE.finditer(text)}
    if prefix:
        values = {item for item in values if item.startswith(prefix + "-")}
    return values


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory(root: Path) -> list[dict[str, str | int]]:
    items: list[dict[str, str | int]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        items.append({"path": rel, "size": path.stat().st_size, "sha256": sha256(path)})
    return items


def add(findings: list[Finding], severity: str, code: str, location: str, message: str, recommendation: str) -> None:
    findings.append(Finding(severity, code, location, message, recommendation))


def check_required_files(root: Path, findings: list[Finding]) -> None:
    for name in REQUIRED_ROOT:
        if not (root / name).exists():
            add(findings, "error", "missing_required_file", name, f"缺少必需文件 {name}。", "补齐该文件后再进入下游消费。")


def collect_file_texts(root: Path) -> dict[str, str]:
    texts: dict[str, str] = {}
    for path in sorted(root.rglob("*.md")):
        texts[path.relative_to(root).as_posix()] = read_text(path)
    return texts


def check_feature_story_refs(root: Path, texts: dict[str, str], findings: list[Finding]) -> None:
    features_dir = root / "features"
    if not features_dir.exists():
        add(findings, "error", "missing_features_dir", "features/", "缺少 features/ 目录。", "补齐 Feature 目录。")
        return

    feature_map = texts.get("feature-map.md", "")
    for raw_path in PATH_RE.findall(feature_map):
        if raw_path.startswith("features/") and not (root / raw_path).exists():
            add(findings, "error", "missing_referenced_file", "feature-map.md", f"feature-map.md 引用了不存在的文件 {raw_path}。", "修正引用或补齐文件。")

    for feature_dir in sorted(p for p in features_dir.iterdir() if p.is_dir()):
        feature_id = feature_dir.name
        feature_spec = feature_dir / "feature-spec.md"
        story_map = feature_dir / "story-map.md"
        story_dir = feature_dir / "stories"
        if not feature_spec.exists():
            add(findings, "error", "missing_feature_spec", feature_id, f"{feature_id} 缺少 feature-spec.md。", "补齐 Feature 规格。")
        if not story_map.exists():
            add(findings, "error", "missing_story_map", feature_id, f"{feature_id} 缺少 story-map.md。", "补齐 Story 导航。")
        if not story_dir.exists():
            add(findings, "error", "missing_story_dir", feature_id, f"{feature_id} 缺少 stories/ 目录。", "补齐 Story 目录。")
            continue

        story_files = {path.stem for path in story_dir.glob("STORY-*.md")}
        story_map_text = read_text(story_map) if story_map.exists() else ""
        story_map_ids = ids(story_map_text, "STORY")
        for story_id in sorted(story_map_ids - story_files):
            add(findings, "error", "story_map_missing_file", story_map.relative_to(root).as_posix(), f"story-map.md 引用了缺失 Story 文件 {story_id}.md。", "补齐 Story 文件或修正 story-map。")
        for story_id in sorted(story_files - story_map_ids):
            add(findings, "warning", "story_file_not_in_story_map", f"{feature_id}/stories/{story_id}.md", f"{story_id}.md 未在 story-map.md 中出现。", "将 Story 加入 story-map，便于人类和下游 agent 导航。")

        for story_path in sorted(story_dir.glob("STORY-*.md")):
            fm = parse_front_matter(read_text(story_path))
            if fm.get("feature_id") and fm["feature_id"] != feature_id:
                add(findings, "error", "feature_id_mismatch", story_path.relative_to(root).as_posix(), f"Story front matter feature_id={fm['feature_id']} 与目录 {feature_id} 不一致。", "修正 front matter 或目录。")
            if fm.get("story_id") and fm["story_id"] != story_path.stem:
                add(findings, "error", "story_id_mismatch", story_path.relative_to(root).as_posix(), f"Story front matter story_id={fm['story_id']} 与文件名 {story_path.stem} 不一致。", "修正 front matter 或文件名。")


def check_questions(texts: dict[str, str], findings: list[Finding]) -> None:
    package_question_sources = ["prd.md", "feature-map.md", "human-view.md", "quality-review.md"]
    q_by_file = {name: ids(texts.get(name, ""), "QUESTION") for name in package_question_sources}
    package_questions = set().union(*q_by_file.values())
    quality_questions = q_by_file["quality-review.md"]
    prd_feature_questions = q_by_file["prd.md"] | q_by_file["feature-map.md"]

    if not package_questions:
        add(findings, "warning", "no_questions_found", "package", "未发现 QUESTION-* ID。", "若需求存在未决问题，应使用稳定 QUESTION ID。")

    for name, questions in q_by_file.items():
        if package_questions and not questions:
            add(findings, "warning", "missing_question_list", name, f"{name} 未包含 QUESTION-*，可能导致问题清单断裂。", "在该文件中同步开放问题或明确豁免。")

    missing_quality = sorted(prd_feature_questions - quality_questions)
    if missing_quality:
        add(findings, "warning", "quality_review_missing_questions", "quality-review.md", "quality-review.md 未覆盖问题: " + ", ".join(missing_quality), "在 quality-review.md 中补齐对应 QR 发现或说明豁免。")

    story_questions: set[str] = set()
    for path, text in texts.items():
        if "/stories/STORY-" in path:
            story_questions.update(ids(text, "QUESTION"))
    missing_package = sorted(story_questions - package_questions)
    if missing_package:
        add(findings, "warning", "story_question_missing_package_list", "stories/", "Story 中的问题未进入包级问题清单: " + ", ".join(missing_package), "同步到 PRD、feature-map 或 human-view。")


def has_visible_reason(text: str) -> bool:
    if re.search(r"(?im)^reason\s*:", text):
        return True
    if "原因" in text:
        return True
    if ids(text, "QUESTION"):
        return True
    return False


def check_readiness_reasons(texts: dict[str, str], findings: list[Finding]) -> None:
    for path, text in texts.items():
        if not path.endswith(".md"):
            continue
        is_readiness_asset = (
            path == "human-view.md"
            or path.endswith("feature-spec.md")
            or path.endswith("story-map.md")
            or "/stories/STORY-" in path
        )
        if not is_readiness_asset:
            continue
        lower = text.lower()
        if any(state in lower for state in ["need_revision", "blocked", "ready_for_coding_only"]):
            if not has_visible_reason(text):
                add(findings, "warning", "readiness_missing_reason", path, f"{path} 包含 need_revision / blocked / ready_for_coding_only，但没有可见原因或关联问题。", "补充 reason 或 QUESTION 引用。")
            elif "need_revision" in lower:
                add(findings, "warning", "need_revision_detected", path, f"{path} 标记为 need_revision，且已有原因或关联问题。", "下游只能在接受该缺口的情况下继续。")
            elif "blocked" in lower:
                add(findings, "warning", "blocked_detected", path, f"{path} 标记为 blocked，且已有原因或关联问题。", "关闭阻塞项前不要进入下游消费。")
            if "ready_for_coding_only" in lower:
                add(findings, "info", "partial_ready_detected", path, f"{path} 标记为 ready_for_coding_only，不应解释为完整 ready。", "下游只能进入局部 coding 或技术探查。")


def check_human_view(texts: dict[str, str], findings: list[Finding]) -> None:
    text = texts.get("human-view.md", "")
    required_tokens = {
        "FEATURE-": "Feature 入口",
        "STORY-": "Story 入口",
        "ai-coding-input.md": "AI coding 入口",
        "ai-testing-input.md": "AI testing 入口",
        "quality-review.md": "quality review 入口",
    }
    for token, label in required_tokens.items():
        if token not in text:
            add(findings, "warning", "human_view_missing_entry", "human-view.md", f"human-view.md 缺少 {label}。", "补充面向人类和下游 agent 的导航入口。")


def check_source_mutation(before: list[dict[str, str | int]], after: list[dict[str, str | int]], findings: list[Finding]) -> None:
    if before != after:
        add(findings, "error", "source_mutation_detected", "input", "输入源资产在验证前后发生变化。", "validator 必须只读输入；检查脚本或并发任务。")


def render_markdown(title: str, input_dir: Path, findings: list[Finding], inventory_items: list[dict[str, str | int]]) -> str:
    counts = {severity: sum(1 for item in findings if item.severity == severity) for severity in ["error", "warning", "info"]}
    decision = "blocked" if counts["error"] else ("needs_attention" if counts["warning"] else "pass")
    lines = [
        f"# Validation Report: {title}",
        "",
        f"- Input: `{input_dir}`",
        f"- Decision: `{decision}`",
        f"- Errors: {counts['error']}",
        f"- Warnings: {counts['warning']}",
        f"- Info: {counts['info']}",
        f"- Source files inventoried: {len(inventory_items)}",
        "",
        "## Findings",
        "",
        "| Severity | Code | Location | Message | Recommendation |",
        "|---|---|---|---|---|",
    ]
    if findings:
        for item in findings:
            lines.append(f"| {item.severity} | {item.code} | `{item.location}` | {item.message} | {item.recommendation} |")
    else:
        lines.append("| info | no_findings | package | 未发现问题。 | 可以进入下游消费。 |")
    lines.extend([
        "",
        "## Consumer Guidance",
        "",
        "- `error_count > 0` 时，不应进入下游 wiki/coding/testing 消费。",
        "- `warning_count > 0` 时，只能在明确接受已知缺口的情况下继续。",
        "- 本报告是生成产物，不替代输入 Markdown source of truth。",
    ])
    return "\n".join(lines) + "\n"


def build(args: argparse.Namespace) -> int:
    input_dir = Path(args.input).resolve()
    output_dir = Path(args.output).resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"ERROR: 输入目录不存在或不是目录: {input_dir}", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    findings: list[Finding] = []
    before = inventory(input_dir)

    check_required_files(input_dir, findings)
    texts = collect_file_texts(input_dir)
    check_feature_story_refs(input_dir, texts, findings)
    check_questions(texts, findings)
    check_readiness_reasons(texts, findings)
    check_human_view(texts, findings)

    after = inventory(input_dir)
    check_source_mutation(before, after, findings)

    counts = {severity: sum(1 for item in findings if item.severity == severity) for severity in ["error", "warning", "info"]}
    decision = "blocked" if counts["error"] else ("needs_attention" if counts["warning"] else "pass")
    report = {
        "title": args.title,
        "input": str(input_dir),
        "decision": decision,
        "error_count": counts["error"],
        "warning_count": counts["warning"],
        "info_count": counts["info"],
        "findings": [asdict(item) for item in findings],
    }
    write_text(output_dir / "validation-report.json", json.dumps(report, ensure_ascii=False, indent=2))
    write_text(output_dir / "source-inventory.json", json.dumps(after, ensure_ascii=False, indent=2))
    write_text(output_dir / "validation-report.md", render_markdown(args.title, input_dir, findings, after))

    print(f"Generated validation report: {output_dir}")
    print(f"decision={decision} errors={counts['error']} warnings={counts['warning']} info={counts['info']}")
    return 1 if counts["error"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a V3 requirement asset package.")
    parser.add_argument("--input", required=True, help="Path to requirement asset directory.")
    parser.add_argument("--output", required=True, help="Output directory for validation-report files.")
    parser.add_argument("--title", required=True, help="Human-readable case title.")
    return build(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
