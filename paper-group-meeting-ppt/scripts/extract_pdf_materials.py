from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

from pypdf import PdfReader


HEADING_RE = re.compile(r"^(\d+(\.\d+)?\s+[A-Z].*|REFERENCES|APPENDIX.*)$")


def safe_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
    return cleaned or "asset"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def reset_output_dir(outdir: Path) -> None:
    for subdir_name in ("pages", "figures", "page_images"):
        subdir = outdir / subdir_name
        if not subdir.exists():
            continue
        for child in subdir.iterdir():
            if child.is_file():
                child.unlink()

    for filename in ("full_text.txt", "outline.md", "asset_summary.md", "page_manifest.json"):
        target = outdir / filename
        if target.exists():
            target.unlink()


def render_pages(pdf_path: Path, outdir: Path, dpi: int) -> list[dict[str, object]]:
    page_images_dir = outdir / "page_images"
    page_images_dir.mkdir(parents=True, exist_ok=True)

    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        return [
            {
                "status": "skipped",
                "reason": "pdftoppm not found; install Poppler or render pages with another PDF tool",
            }
        ]

    prefix = page_images_dir / "page"
    command = [pdftoppm, "-png", "-r", str(dpi), str(pdf_path), str(prefix)]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return [
            {
                "status": "error",
                "command": command,
                "stderr": completed.stderr.strip(),
            }
        ]

    rendered = []
    for image_path in sorted(page_images_dir.glob("page-*.png")):
        match = re.search(r"page-(\d+)\.png$", image_path.name)
        page_number = int(match.group(1)) if match else None
        stable_name = f"page_{page_number:03d}.png" if page_number else image_path.name
        stable_path = page_images_dir / stable_name
        if stable_path != image_path:
            image_path.replace(stable_path)
        rendered.append(
            {
                "status": "ok",
                "page": page_number,
                "file": str(stable_path.relative_to(outdir)).replace("\\", "/"),
                "bytes": stable_path.stat().st_size,
            }
        )
    return rendered


def extract(pdf_path: Path, outdir: Path, min_image_bytes: int, render: bool, render_dpi: int) -> None:
    reader = PdfReader(str(pdf_path))

    reset_output_dir(outdir)

    pages_dir = outdir / "pages"
    figures_dir = outdir / "figures"
    pages_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    full_text_parts: list[str] = []
    outline_entries: list[dict[str, object]] = []
    manifest: list[dict[str, object]] = []
    total_images = 0
    skipped_small_images = 0
    rendered_pages: list[dict[str, object]] = []

    if render:
        rendered_pages = render_pages(pdf_path, outdir, render_dpi)

    for page_index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        page_text_file = pages_dir / f"page_{page_index:03d}.txt"
        write_text(page_text_file, text)

        full_text_parts.append(f"\n\n=== Page {page_index} ===\n{text}")

        page_headings = []
        for line in text.splitlines():
            stripped = line.strip()
            if stripped and HEADING_RE.match(stripped):
                page_headings.append(stripped)
                outline_entries.append({"page": page_index, "heading": stripped})

        extracted_images = []
        try:
            images = list(page.images)
        except Exception as exc:
            images = []
            extracted_images.append(
                {
                    "status": "error",
                    "reason": f"image enumeration failed: {exc}",
                }
            )

        for image_index, image in enumerate(images, start=1):
            original_name = getattr(image, "name", f"image_{image_index}")
            image_name = safe_name(original_name)
            image_file = figures_dir / f"page_{page_index:03d}_{image_index:02d}_{image_name}"
            image_size = len(image.data)
            if image_size < min_image_bytes:
                extracted_images.append(
                    {
                        "status": "skipped_small",
                        "source_name": original_name,
                        "bytes": image_size,
                    }
                )
                skipped_small_images += 1
                continue
            try:
                image_file.write_bytes(image.data)
                extracted_images.append(
                    {
                        "status": "ok",
                        "file": str(image_file.name),
                        "source_name": original_name,
                        "bytes": image_size,
                    }
                )
                total_images += 1
            except Exception as exc:
                extracted_images.append(
                    {
                        "status": "error",
                        "source_name": original_name,
                        "bytes": image_size,
                        "reason": str(exc),
                    }
                )

        manifest.append(
            {
                "page": page_index,
                "text_file": str(page_text_file.relative_to(outdir)).replace("\\", "/"),
                "headings": page_headings,
                "images": extracted_images,
            }
        )

    outline_lines = ["# Rough Outline", ""]
    for entry in outline_entries:
        outline_lines.append(f"- page {entry['page']}: {entry['heading']}")

    summary_lines = [
        "# Asset Summary",
        "",
        f"- PDF: {pdf_path}",
        f"- Pages: {len(reader.pages)}",
        f"- Extracted images: {total_images}",
        f"- Skipped small images: {skipped_small_images}",
        f"- Min image bytes threshold: {min_image_bytes}",
        f"- Rendered pages requested: {render}",
        f"- Render DPI: {render_dpi if render else 'n/a'}",
        "",
        "## Pages With Headings",
    ]
    if outline_entries:
        for entry in outline_entries:
            summary_lines.append(f"- page {entry['page']}: {entry['heading']}")
    else:
        summary_lines.append("- No headings detected.")

    summary_lines.extend(["", "## Image Count By Page"])
    for entry in manifest:
        ok_count = sum(1 for item in entry["images"] if item.get("status") == "ok")
        summary_lines.append(f"- page {entry['page']}: {ok_count}")

    summary_lines.extend(["", "## Rendered Page Images"])
    if rendered_pages:
        for entry in rendered_pages:
            if entry.get("status") == "ok":
                summary_lines.append(f"- page {entry.get('page')}: {entry.get('file')} ({entry.get('bytes')} bytes)")
            else:
                summary_lines.append(f"- {entry.get('status')}: {entry.get('reason') or entry.get('stderr')}")
    else:
        summary_lines.append("- Not requested.")

    write_text(outdir / "full_text.txt", "".join(full_text_parts).strip())
    write_text(outdir / "outline.md", "\n".join(outline_lines) + "\n")
    write_text(outdir / "asset_summary.md", "\n".join(summary_lines) + "\n")
    write_text(
        outdir / "page_manifest.json",
        json.dumps(
            {
                "pdf": str(pdf_path),
                "pages": len(reader.pages),
                "rendered_pages": rendered_pages,
                "outline": outline_entries,
                "manifest": manifest,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text and embedded images from a paper PDF.")
    parser.add_argument("--pdf", required=True, help="Path to the source PDF.")
    parser.add_argument("--outdir", required=True, help="Directory to write extracted materials into.")
    parser.add_argument(
        "--min-image-bytes",
        type=int,
        default=1024,
        help="Skip embedded images smaller than this size in bytes. Default: 1024.",
    )
    parser.add_argument(
        "--render-pages",
        action="store_true",
        help="Render each PDF page to PNG using pdftoppm. Use these images for whole-figure/table/equation crops.",
    )
    parser.add_argument(
        "--render-dpi",
        type=int,
        default=220,
        help="DPI for rendered page PNGs when --render-pages is used. Default: 220.",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf).expanduser().resolve()
    outdir = Path(args.outdir).expanduser().resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    outdir.mkdir(parents=True, exist_ok=True)
    extract(pdf_path, outdir, args.min_image_bytes, args.render_pages, args.render_dpi)


if __name__ == "__main__":
    main()
