#!/usr/bin/env python3
"""Build a small static HTML wiki from a V3 requirement asset package."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_FILES = ["feature-map.md", "human-view.md", "prd.md"]
ID_RE = re.compile(r"\b(FEATURE|STORY|RULE|GWT|QUESTION|RISK)-\d+\b")


@dataclass
class Story:
    story_id: str
    title: str
    status: str
    overall_decision: str
    reason: str
    source_path: Path
    rules: list[str]
    gwts: list[str]


@dataclass
class Feature:
    feature_id: str
    title: str
    source_path: Path | None
    stories: list[Story]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def slug(text: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_-]+", "-", text.strip()).strip("-")
    return value or "section"


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + 4 :].lstrip("\r\n")
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data, body


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def find_ids(text: str, prefix: str | None = None) -> list[str]:
    ids = sorted(set(match.group(0) for match in ID_RE.finditer(text)))
    if prefix:
        ids = [item for item in ids if item.startswith(prefix + "-")]
    return ids


def parse_inline_refs(value: str) -> list[str]:
    return find_ids(value)


def md_to_html(markdown: str) -> str:
    """Small markdown renderer covering headings, lists, tables, code and paragraphs."""
    lines = markdown.splitlines()
    out: list[str] = []
    in_code = False
    in_list = False
    in_table = False
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(item.strip() for item in paragraph)
            out.append(f"<p>{html.escape(text)}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def close_table() -> None:
        nonlocal in_table
        if in_table:
            out.append("</tbody></table>")
            in_table = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            close_list()
            close_table()
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append("<pre><code>")
                in_code = True
            i += 1
            continue

        if in_code:
            out.append(html.escape(line))
            i += 1
            continue

        if not stripped:
            flush_paragraph()
            close_list()
            close_table()
            i += 1
            continue

        if stripped.startswith("#"):
            flush_paragraph()
            close_list()
            close_table()
            level = min(len(stripped) - len(stripped.lstrip("#")), 4)
            title = stripped[level:].strip()
            out.append(f'<h{level} id="{slug(title)}">{html.escape(title)}</h{level}>')
            i += 1
            continue

        if "|" in stripped and stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            close_list()
            cells = [html.escape(cell.strip()) for cell in stripped.strip("|").split("|")]
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            is_separator = bool(re.fullmatch(r"\|?[\s:|\-]+\|?", next_line))
            if not in_table:
                out.append("<table>")
                if is_separator:
                    out.append("<thead><tr>" + "".join(f"<th>{cell}</th>" for cell in cells) + "</tr></thead><tbody>")
                    in_table = True
                    i += 2
                    continue
                out.append("<tbody>")
                in_table = True
            if not is_separator:
                out.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")
            i += 1
            continue

        close_table()

        if stripped.startswith("- "):
            flush_paragraph()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{html.escape(stripped[2:].strip())}</li>")
            i += 1
            continue

        close_list()
        paragraph.append(stripped)
        i += 1

    flush_paragraph()
    close_list()
    close_table()
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def localize_markdown(markdown: str) -> str:
    replacements = {
        "# Quality Review": "# 质量评审",
        "## Decision": "## 结论",
        "## Why": "## 原因",
        "## Checklist Result": "## Checklist 结果",
        "## Findings": "## 问题清单",
        "## Ready Scope": "## 可推进范围",
        "## Need Revision Scope": "## 需修订范围",
        "| ID | Severity | Related | Finding | Required Change |": "| ID | 严重级别 | 关联对象 | 问题 | 需要补充 |",
        "In scope:": "范围内：",
        "Out of scope:": "范围外：",
        "## Missing Context": "## 缺失上下文",
        "# Human View:": "# 人类阅读视图:",
        "reason:": "原因：",
        "related_ids:": "关联 ID：",
        "The system shall": "系统应",
        "When ": "当 ",
        " If ": "；如果 ",
    }
    for source, target in replacements.items():
        markdown = markdown.replace(source, target)
    return markdown


def link_asset_paths(fragment: str, root_prefix: str) -> str:
    def feature_link(match: re.Match[str]) -> str:
        path = match.group(0).strip("`")
        feature_id = match.group(1)
        return f'<a href="{root_prefix}features/{feature_id}.html">{html.escape(path)}</a>'

    def story_link(match: re.Match[str]) -> str:
        path = match.group(0).strip("`")
        story_id = match.group(2)
        return f'<a href="{root_prefix}review-cockpit.html#story-{story_id}">{html.escape(path)}</a>'

    fragment = re.sub(r"`features/(FEATURE-\d+)/(?:feature-spec|story-map|ai-coding-input|ai-testing-input)\.md`", feature_link, fragment)
    fragment = re.sub(r"`features/(FEATURE-\d+)/stories/(STORY-\d+)\.md`", story_link, fragment)
    fragment = fragment.replace("`prd.md`", f'<a href="{root_prefix}prd.html">prd.md</a>')
    fragment = fragment.replace("`quality-review.md`", f'<a href="{root_prefix}quality-review.html">quality-review.md</a>')
    return fragment


def link_known_ids(fragment: str, root_prefix: str) -> str:
    def repl(match: re.Match[str]) -> str:
        item = match.group(0)
        if item.startswith("FEATURE-"):
            href = f"{root_prefix}features/{item}.html"
        elif item.startswith("STORY-"):
            href = f"{root_prefix}review-cockpit.html#story-{item}"
        elif item.startswith("QUESTION-"):
            href = f"{root_prefix}review-cockpit.html#question-{item}"
        else:
            return item
        return f'<a class="xref" href="{href}">{item}</a>'

    def link_text_only(part: str) -> str:
        pieces = re.split(r"(<[^>]+>)", part)
        return "".join(piece if piece.startswith("<") else ID_RE.sub(repl, piece) for piece in pieces)

    parts = re.split(r"(<a\b[^>]*>.*?</a>)", fragment, flags=re.IGNORECASE | re.DOTALL)
    return "".join(part if part.lower().startswith("<a") else link_text_only(part) for part in parts)


def render_markdown(markdown: str, root_prefix: str = "") -> str:
    """Render markdown body while hiding YAML front matter from the human view."""
    _, body = parse_front_matter(markdown)
    rendered = md_to_html(localize_markdown(body))
    rendered = link_known_ids(link_asset_paths(rendered, root_prefix), root_prefix)
    return re.sub(r"`(<a\b[^>]*>.*?</a>)`", r"\1", rendered, flags=re.IGNORECASE | re.DOTALL)


def page(title: str, body: str, root_prefix: str = "") -> str:
    css = f"{root_prefix}assets/styles.css"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <header class="topbar">
    <a href="{root_prefix}index.html">首页</a>
    <a href="{root_prefix}review-cockpit.html">评审驾驶舱</a>
    <a href="{root_prefix}prd.html">PRD</a>
    <a href="{root_prefix}quality-review.html">质量评审</a>
  </header>
  <main class="page">
    {body}
  </main>
</body>
</html>
"""


def css() -> str:
    return """
:root { --bg:#f7f8fa; --fg:#1f2937; --muted:#667085; --line:#d8dee8; --card:#ffffff; --ready:#0f7b45; --warn:#a15c00; --blocked:#b42318; }
* { box-sizing: border-box; }
body { margin:0; font:15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; background:var(--bg); color:var(--fg); }
.topbar { display:flex; gap:18px; padding:14px 24px; border-bottom:1px solid var(--line); background:#fff; position:sticky; top:0; z-index:2; }
.topbar a { color:#1f2937; text-decoration:none; font-weight:600; }
.page { max-width:1120px; margin:0 auto; padding:28px 24px 56px; }
.hero, .card { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:20px; margin:0 0 18px; }
.grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:14px; }
.badge { display:inline-block; border-radius:999px; padding:2px 9px; font-size:12px; border:1px solid var(--line); background:#fff; }
.ready { color:var(--ready); border-color:#9dd9b5; }
.need_revision, .warning { color:var(--warn); border-color:#ffd699; }
.blocked, .error { color:var(--blocked); border-color:#f4b8b2; }
.muted { color:var(--muted); }
table { width:100%; border-collapse:collapse; margin:12px 0 18px; background:#fff; }
th, td { border:1px solid var(--line); padding:8px 10px; text-align:left; vertical-align:top; }
th { background:#eef2f7; }
pre { background:#111827; color:#e5e7eb; padding:14px; overflow:auto; border-radius:6px; }
code { font-family:Consolas, "SFMono-Regular", monospace; }
h1, h2, h3 { line-height:1.25; }
a { color:#175cd3; }
.xref { font-weight:600; text-decoration:none; border-bottom:1px dotted #175cd3; }
.reason { background:#fff7ed; border-left:3px solid var(--warn); padding:8px 10px; }
"""


def extract_reason(text: str) -> str:
    match = re.search(r"(?im)^reason:\s*(.+)$", text)
    return match.group(1).strip() if match else ""


def story_from_file(path: Path) -> Story:
    text = read_text(path)
    fm, body = parse_front_matter(text)
    story_id = fm.get("story_id") or path.stem
    title = fm.get("title") or first_heading(body, story_id)
    status = fm.get("status") or "unknown"
    overall = fm.get("overall_decision") or status
    reason = fm.get("reason") or extract_reason(text)
    rules = parse_inline_refs(fm.get("related_rule_refs", "")) or find_ids(text, "RULE")
    gwts = parse_inline_refs(fm.get("related_gwt_refs", "")) or find_ids(text, "GWT")
    return Story(story_id, title, status, overall, reason, path, rules, gwts)


def discover_features(input_dir: Path, warnings: list[str]) -> list[Feature]:
    features_dir = input_dir / "features"
    if not features_dir.exists():
        warnings.append("缺少 features/ 目录，无法生成 Feature 页面。")
        return []

    features: list[Feature] = []
    for feature_dir in sorted(path for path in features_dir.iterdir() if path.is_dir()):
        feature_id = feature_dir.name
        feature_spec = feature_dir / "feature-spec.md"
        title = feature_id
        if feature_spec.exists():
            text = read_text(feature_spec)
            title = first_heading(parse_front_matter(text)[1], feature_id)
        else:
            warnings.append(f"{feature_id} 缺少 feature-spec.md。")

        story_dir = feature_dir / "stories"
        stories: list[Story] = []
        if story_dir.exists():
            for story_path in sorted(story_dir.glob("STORY-*.md")):
                stories.append(story_from_file(story_path))
        else:
            warnings.append(f"{feature_id} 缺少 stories/ 目录。")

        story_map = feature_dir / "story-map.md"
        if story_map.exists():
            for story_id in find_ids(read_text(story_map), "STORY"):
                if not any(story.story_id == story_id for story in stories):
                    warnings.append(f"{feature_id} 的 story-map.md 引用了缺失 Story 文件：{story_id}.md。")

        features.append(Feature(feature_id, title, feature_spec if feature_spec.exists() else None, stories))
    return features


def collect_questions(paths: Iterable[Path]) -> list[str]:
    questions: set[str] = set()
    for path in paths:
        if path.exists():
            questions.update(find_ids(read_text(path), "QUESTION"))
    return sorted(questions)


def collect_question_details(paths: Iterable[Path]) -> dict[str, str]:
    details: dict[str, str] = {}
    for path in paths:
        if not path.exists():
            continue
        for line in read_text(path).splitlines():
            for question_id in find_ids(line, "QUESTION"):
                cleaned = line.strip().lstrip("-").strip()
                cleaned = re.sub(r"`?(QUESTION-\d+)`?\s*[:|]?\s*", "", cleaned).strip()
                if cleaned and question_id not in details:
                    details[question_id] = cleaned
    return details


def validate_input(input_dir: Path) -> list[str]:
    missing = [name for name in REQUIRED_FILES if not (input_dir / name).exists()]
    if missing:
        raise SystemExit("ERROR: 缺少必需输入文件: " + ", ".join(missing))
    return []


def build(args: argparse.Namespace) -> int:
    input_dir = Path(args.input).resolve()
    output_dir = Path(args.output).resolve()
    if not input_dir.exists():
        print(f"ERROR: 输入目录不存在: {input_dir}", file=sys.stderr)
        return 2

    try:
        warnings = validate_input(input_dir)
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    quality_path = input_dir / "quality-review.md"
    if not quality_path.exists():
        warnings.append("缺少 quality-review.md，review cockpit 状态为 incomplete。")

    features = discover_features(input_dir, warnings)
    question_ids = collect_questions(
        [input_dir / "human-view.md", input_dir / "quality-review.md"]
        + [story.source_path for feature in features for story in feature.stories]
    )
    question_details = collect_question_details(
        [input_dir / "prd.md", input_dir / "feature-map.md", input_dir / "human-view.md", input_dir / "quality-review.md"]
        + [story.source_path for feature in features for story in feature.stories]
    )

    write_text(output_dir / "assets" / "styles.css", css())

    human_html = render_markdown(read_text(input_dir / "human-view.md"))
    feature_links = "\n".join(
        f'<li><a href="features/{feature.feature_id}.html">{html.escape(feature.title)}</a></li>' for feature in features
    )
    index_body = f"""
<section class="hero">
  <h1>{html.escape(args.title)}</h1>
  <p class="muted">从 V3 requirement asset package 生成的静态 human-view。Markdown 是 source of truth，HTML 是消费视图。</p>
</section>
<section class="card">
  <h2>导航</h2>
  <ul>
    <li><a href="review-cockpit.html">评审驾驶舱</a></li>
    <li><a href="prd.html">PRD</a></li>
    <li><a href="quality-review.html">质量评审</a></li>
    {feature_links}
  </ul>
</section>
<section class="card">
  <h2>人类阅读视图</h2>
  {human_html}
</section>
"""
    write_text(output_dir / "index.html", page(args.title, index_body))

    prd_body = f'<section class="card">{render_markdown(read_text(input_dir / "prd.md"))}</section>'
    write_text(output_dir / "prd.html", page(f"{args.title} - PRD", prd_body))

    if quality_path.exists():
        quality_body = f'<section class="card">{render_markdown(read_text(quality_path))}</section>'
    else:
        quality_body = '<section class="card"><h1>质量评审</h1><p class="badge warning">incomplete</p><p>缺少 quality-review.md。</p></section>'
    write_text(output_dir / "quality-review.html", page(f"{args.title} - 质量评审", quality_body))

    story_cards: list[str] = []
    for feature in features:
        for story in feature.stories:
            rules = ", ".join(story.rules[:8]) if story.rules else "未发现 Rule 引用"
            gwts = ", ".join(story.gwts[:8]) if story.gwts else "未发现 GWT 引用"
            reason_label = "需要修订原因" if "need_revision" in f"{story.status} {story.overall_decision}" else "Gate 原因"
            reason = f'<p class="reason"><strong>{reason_label}:</strong> {html.escape(story.reason)}</p>' if story.reason else ""
            story_cards.append(
                f"""<div class="card" id="story-{html.escape(story.story_id)}">
<h3>{html.escape(story.story_id)}: {html.escape(story.title)}</h3>
<p><span class="badge {html.escape(story.status)}">{html.escape(story.status)}</span>
<span class="badge">{html.escape(story.overall_decision)}</span></p>
{reason}
<p><strong>规则:</strong> {html.escape(rules)}</p>
<p><strong>验收场景:</strong> {html.escape(gwts)}</p>
</div>"""
            )

    warning_items = "\n".join(f'<li><span class="badge warning">warning</span> {html.escape(item)}</li>' for item in warnings)
    question_items = "\n".join(
        f'<li id="question-{html.escape(item)}"><a class="xref" href="prd.html">{html.escape(item)}</a>'
        + (f" - {html.escape(question_details.get(item, ''))}" if question_details.get(item) else "")
        + "</li>"
        for item in question_ids
    ) or "<li>未发现集中开放问题 ID。</li>"
    cockpit_body = f"""
<section class="hero">
  <h1>评审驾驶舱</h1>
  <p class="muted">用于快速判断 Feature / Story 就绪状态、开放问题和生成风险。</p>
</section>
<section class="grid">
  <div class="card"><h2>Feature 数</h2><p>{len(features)}</p></div>
  <div class="card"><h2>Story 数</h2><p>{sum(len(feature.stories) for feature in features)}</p></div>
  <div class="card"><h2>开放问题</h2><p>{len(question_ids)}</p></div>
  <div class="card"><h2>警告</h2><p>{len(warnings)}</p></div>
</section>
<section class="card">
  <h2>警告 / 不完整项</h2>
  <ul>{warning_items or "<li>无构建 warning。</li>"}</ul>
</section>
<section class="card">
  <h2>开放问题</h2>
  <ul>{question_items}</ul>
</section>
<section>
  <h2>Story 就绪状态</h2>
  {''.join(story_cards)}
</section>
"""
    write_text(output_dir / "review-cockpit.html", page(f"{args.title} - 评审驾驶舱", cockpit_body))

    for feature in features:
        feature_body_parts = [f'<section class="hero"><h1>{html.escape(feature.title)}</h1><p class="badge">{html.escape(feature.feature_id)}</p></section>']
        if feature.source_path:
            feature_body_parts.append(f'<section class="card">{render_markdown(read_text(feature.source_path), "../")}</section>')
        if feature.stories:
            rows = "\n".join(
                "<tr>"
                f"<td>{html.escape(story.story_id)}</td>"
                f"<td>{html.escape(story.title)}</td>"
                f"<td>{html.escape(story.status)}</td>"
                f"<td>{html.escape(story.overall_decision)}</td>"
                f"<td>{html.escape(story.reason)}</td>"
                f"<td>{html.escape(', '.join(story.rules[:5]))}</td>"
                "</tr>"
                for story in feature.stories
            )
            feature_body_parts.append(
                f"""<section class="card"><h2>Story 摘要</h2>
<table><thead><tr><th>Story</th><th>标题</th><th>状态</th><th>执行口径</th><th>Gate 原因 / 修订原因</th><th>规则</th></tr></thead><tbody>{rows}</tbody></table></section>"""
            )
        write_text(output_dir / "features" / f"{feature.feature_id}.html", page(feature.title, "\n".join(feature_body_parts), "../"))

    search_index = [
        {"title": args.title, "url": "index.html", "type": "index"},
        {"title": "评审驾驶舱", "url": "review-cockpit.html", "type": "review"},
        {"title": "PRD", "url": "prd.html", "type": "prd"},
        {"title": "质量评审", "url": "quality-review.html", "type": "quality"},
    ]
    for feature in features:
        search_index.append({"title": feature.title, "url": f"features/{feature.feature_id}.html", "type": "feature", "id": feature.feature_id})
        for story in feature.stories:
            search_index.append({"title": story.title, "url": f"features/{feature.feature_id}.html", "type": "story", "id": story.story_id})
    write_text(output_dir / "search-index.json", json.dumps(search_index, ensure_ascii=False, indent=2))
    write_text(output_dir / "build-report.json", json.dumps({"warnings": warnings, "features": len(features), "stories": sum(len(f.stories) for f in features)}, ensure_ascii=False, indent=2))

    for warning in warnings:
        print("WARNING:", warning)
    print(f"Generated wiki: {output_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a static HTML wiki from a V3 requirement asset package.")
    parser.add_argument("--input", required=True, help="Path to requirement-asset directory.")
    parser.add_argument("--output", required=True, help="Output directory for generated HTML.")
    parser.add_argument("--title", required=True, help="Wiki title.")
    return build(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
