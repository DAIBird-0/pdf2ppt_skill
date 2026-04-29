from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


SLIDE_HEADER_RE = re.compile(r"^(?:##+)\s*(?:Slide\s*)?(\d+)[\s:：-]+(.+?)\s*$", re.IGNORECASE)
LIST_ITEM_RE = re.compile(r"^\s*[-*]\s+(.+?)\s*$")


@dataclass
class SlideBlock:
    number: int
    title: str
    body: list[str]


def parse_slide_specs(path: Path) -> list[SlideBlock]:
    slides: list[SlideBlock] = []
    current: SlideBlock | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        header_match = SLIDE_HEADER_RE.match(raw_line.strip())
        if header_match:
            if current:
                slides.append(current)
            current = SlideBlock(number=int(header_match.group(1)), title=header_match.group(2).strip(), body=[])
            continue
        if current:
            item_match = LIST_ITEM_RE.match(raw_line)
            if item_match:
                current.body.append(item_match.group(1).strip())
            elif raw_line.strip():
                current.body.append(raw_line.strip())
    if current:
        slides.append(current)
    return slides


def load_manifest(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_tokens(text: str) -> list[str]:
    lowered = text.lower()
    lowered = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", " ", lowered)
    return [token for token in lowered.split() if token]


def choose_group(tokens: list[str], keyword_groups: dict[str, list[str]]) -> str | None:
    scores: dict[str, int] = {}
    token_set = set(tokens)
    for group, keywords in keyword_groups.items():
        score = sum(1 for keyword in keywords if keyword.lower() in token_set)
        if score:
            scores[group] = score
    if not scores:
        return None
    return max(scores, key=scores.get)


def choose_icon(group: str, paper_manifest: dict[str, list[dict[str, object]]], global_icons: list[dict[str, object]]) -> tuple[str, str | None]:
    if group in paper_manifest and paper_manifest[group]:
        return "current_extracted_figures", paper_manifest[group][0].get("file")
    for icon in global_icons:
        tags = {str(tag).lower() for tag in icon.get("tags", [])}
        if group.lower() in tags:
            return "historical_harvested_icon", icon.get("file")
    return "ppt_native_fallback", None


def render_plan(slides: list[SlideBlock], keyword_groups: dict[str, list[str]], paper_manifest: dict[str, list[dict[str, object]]], global_icons: list[dict[str, object]]) -> tuple[str, list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    lines = ["# Icon Plan", ""]
    for slide in slides:
        tokens = normalize_tokens(" ".join([slide.title, *slide.body]))
        group = choose_group(tokens, keyword_groups)
        if not group:
            continue
        source_class, source_file = choose_icon(group, paper_manifest, global_icons)
        record = {
            "slide": slide.number,
            "title": slide.title,
            "semantic_group": group,
            "source_class": source_class,
            "source_file": source_file,
            "placement_note": "lower-right or lower-middle of the sparse card / short-text area",
            "status": "planned",
        }
        records.append(record)
        lines.extend(
            [
                f"## Slide {slide.number}: {slide.title}",
                f"- semantic group: {group}",
                f"- source class: {source_class}",
                f"- source file: {source_file or 'ppt-native fallback'}",
                "- placement: lower-right or lower-middle of the nearby sparse card / short-text area",
                "- status: planned",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n", records


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a deterministic icon plan from slide specs and local icon manifests.")
    parser.add_argument("--slide-specs", required=True, help="Path to slide_specs.md or a similarly structured markdown file.")
    parser.add_argument("--global-manifest", required=True, help="Path to the reusable icon-library manifest.json.")
    parser.add_argument("--paper-manifest", help="Optional JSON manifest of current paper icon candidates grouped by semantic class.")
    parser.add_argument("--out-md", required=True, help="Destination path for icon_plan.md.")
    parser.add_argument("--out-json", required=True, help="Destination path for icon_plan.json.")
    args = parser.parse_args()

    slide_specs_path = Path(args.slide_specs).expanduser().resolve()
    global_manifest_path = Path(args.global_manifest).expanduser().resolve()
    paper_manifest_path = Path(args.paper_manifest).expanduser().resolve() if args.paper_manifest else None
    out_md = Path(args.out_md).expanduser().resolve()
    out_json = Path(args.out_json).expanduser().resolve()

    slides = parse_slide_specs(slide_specs_path)
    global_manifest = load_manifest(global_manifest_path)
    paper_manifest = load_manifest(paper_manifest_path) if paper_manifest_path and paper_manifest_path.exists() else {}

    keyword_groups = global_manifest.get("keyword_groups", {})
    global_icons = global_manifest.get("icons", [])
    markdown, records = render_plan(slides, keyword_groups, paper_manifest, global_icons)

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(markdown, encoding="utf-8")
    out_json.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
