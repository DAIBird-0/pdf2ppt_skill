from __future__ import annotations

import argparse
import json
import math
import shutil
from pathlib import Path

try:
    from PIL import Image, ImageOps, ImageStat, ImageDraw
except ImportError as exc:  # pragma: no cover - runtime dependency check
    raise SystemExit("Pillow is required for harvest_icons_from_figures.py") from exc


ALLOWED_SUFFIXES = {".png", ".jpg", ".jpeg", ".jp2", ".webp"}
MIN_BYTES = 1024
MAX_BYTES = 900_000
MIN_DIM = 24
MAX_DIM = 900
MAX_ASPECT_RATIO = 5.5


def discover_figure_dirs(roots: list[Path]) -> list[Path]:
    found: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for figures_dir in root.rglob("figures"):
            if figures_dir.is_dir() and "extracted" in {part.lower() for part in figures_dir.parts}:
                found.append(figures_dir)
    return sorted(set(found))


def image_is_candidate(path: Path) -> tuple[bool, str, dict[str, object]]:
    if path.suffix.lower() not in ALLOWED_SUFFIXES:
        return False, "unsupported_suffix", {}

    size_bytes = path.stat().st_size
    if size_bytes < MIN_BYTES:
        return False, "too_small_bytes", {"bytes": size_bytes}
    if size_bytes > MAX_BYTES:
        return False, "too_large_bytes", {"bytes": size_bytes}

    try:
        with Image.open(path) as image:
            image.load()
            width, height = image.size
            if width < MIN_DIM or height < MIN_DIM:
                return False, "too_small_dimensions", {"width": width, "height": height}
            if width > MAX_DIM or height > MAX_DIM:
                return False, "too_large_dimensions", {"width": width, "height": height}

            aspect_ratio = max(width / height, height / width)
            if aspect_ratio > MAX_ASPECT_RATIO:
                return False, "extreme_aspect_ratio", {"width": width, "height": height}

            grayscale = ImageOps.grayscale(image)
            stat = ImageStat.Stat(grayscale)
            mean = stat.mean[0]
            stddev = stat.stddev[0]
            if mean > 248 and stddev < 2:
                return False, "near_blank", {"mean": mean, "stddev": stddev}

            metadata = {
                "width": width,
                "height": height,
                "bytes": size_bytes,
                "mean_luma": round(mean, 2),
                "stddev_luma": round(stddev, 2),
            }
            return True, "candidate", metadata
    except Exception as exc:
        return False, "open_failed", {"error": str(exc)}


def slugify(parts: list[str]) -> str:
    raw = "_".join(part.strip().replace(" ", "_") for part in parts if part.strip())
    safe = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in raw)
    return safe.strip("_") or "icon"


def build_contact_sheet(images: list[Path], destination: Path, thumb_size: int = 160, columns: int = 4) -> None:
    if not images:
        return

    rows = math.ceil(len(images) / columns)
    header = 28
    sheet = Image.new("RGB", (columns * thumb_size, rows * (thumb_size + header)), "#F5F8FB")
    draw = ImageDraw.Draw(sheet)

    for index, image_path in enumerate(images):
        row = index // columns
        column = index % columns
        x = column * thumb_size
        y = row * (thumb_size + header)

        with Image.open(image_path) as image:
            image = image.convert("RGB")
            thumb = ImageOps.contain(image, (thumb_size - 16, thumb_size - 28))
            pad_x = x + (thumb_size - thumb.width) // 2
            pad_y = y + 8 + (thumb_size - 36 - thumb.height) // 2
            sheet.paste(thumb, (pad_x, pad_y))
        draw.text((x + 6, y + thumb_size - 16), image_path.stem[:22], fill="#1F2937")

    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description="Harvest reusable icon candidates from historical extracted/figures folders.")
    parser.add_argument(
        "--roots",
        nargs="+",
        required=True,
        help="One or more roots to scan for extracted/figures directories.",
    )
    parser.add_argument(
        "--outdir",
        required=True,
        help="Directory to write icon candidates, manifest, and contact sheet into.",
    )
    parser.add_argument(
        "--copy-limit",
        type=int,
        default=60,
        help="Maximum number of candidate files to copy. Default: 60.",
    )
    args = parser.parse_args()

    roots = [Path(item).expanduser().resolve() for item in args.roots]
    outdir = Path(args.outdir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    candidates_dir = outdir / "icon_candidates"
    candidates_dir.mkdir(parents=True, exist_ok=True)

    figure_dirs = discover_figure_dirs(roots)
    records: list[dict[str, object]] = []
    copied_images: list[Path] = []

    for figures_dir in figure_dirs:
        for image_path in sorted(figures_dir.iterdir()):
            if not image_path.is_file():
                continue
            ok, reason, metadata = image_is_candidate(image_path)
            record = {
                "source_dir": str(figures_dir),
                "source_file": str(image_path),
                "filename": image_path.name,
                "status": "candidate" if ok else "rejected",
                "reason": reason,
                **metadata,
            }
            if ok and len(copied_images) < args.copy_limit:
                parent_hint = next((part for part in reversed(image_path.parts) if part not in {"figures", "extracted"}), "paper")
                copied_name = slugify([parent_hint, image_path.stem]) + image_path.suffix.lower()
                destination = candidates_dir / copied_name
                shutil.copy2(image_path, destination)
                record["copied_to"] = str(destination)
                copied_images.append(destination)
            records.append(record)

    manifest_path = outdir / "candidates.json"
    manifest_path.write_text(json.dumps({"roots": [str(root) for root in roots], "records": records}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    build_contact_sheet(copied_images, outdir / "contact_sheet.png")


if __name__ == "__main__":
    main()
