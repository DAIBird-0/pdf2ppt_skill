#!/usr/bin/env python
"""Crop one region from a rendered PDF page image.

This helper is intentionally small: render PDF pages first, inspect the page
image, then crop the exact figure/table/equation bbox from that rendered page.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def parse_bbox(value: str) -> tuple[int, int, int, int]:
    parts = [p.strip() for p in value.replace(";", ",").split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bbox must be left,top,right,bottom")
    try:
        left, top, right, bottom = [int(float(p)) for p in parts]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("bbox values must be numbers") from exc
    if right <= left or bottom <= top:
        raise argparse.ArgumentTypeError("bbox must satisfy right > left and bottom > top")
    return left, top, right, bottom


def clamp_bbox(bbox: tuple[int, int, int, int], width: int, height: int, pad: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = bbox
    return (
        max(0, left - pad),
        max(0, top - pad),
        min(width, right + pad),
        min(height, bottom + pad),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Crop a precise region from a rendered PDF page image.")
    parser.add_argument("--image", required=True, help="Rendered page image path, e.g. page_007.png")
    parser.add_argument("--bbox", required=True, type=parse_bbox, help="Pixel bbox: left,top,right,bottom")
    parser.add_argument("--out", required=True, help="Output cropped PNG path")
    parser.add_argument("--pad", type=int, default=0, help="Optional pixel padding around bbox")
    parser.add_argument("--qa", help="Optional QA image showing the bbox over the source page")
    args = parser.parse_args()

    src = Path(args.image)
    out = Path(args.out)
    if not src.exists():
        raise FileNotFoundError(src)

    with Image.open(src) as im:
        im = im.convert("RGB")
        bbox = clamp_bbox(args.bbox, im.width, im.height, max(0, args.pad))
        if bbox[2] - bbox[0] < 10 or bbox[3] - bbox[1] < 10:
            raise ValueError(f"Crop too small after clamping: {bbox}")
        crop = im.crop(bbox)
        out.parent.mkdir(parents=True, exist_ok=True)
        crop.save(out)

        if args.qa:
            qa = Path(args.qa)
            marked = im.copy()
            draw = ImageDraw.Draw(marked)
            draw.rectangle(bbox, outline=(220, 38, 38), width=max(3, im.width // 600))
            qa.parent.mkdir(parents=True, exist_ok=True)
            marked.save(qa)

    print(f"cropped {src} bbox={bbox} -> {out}")


if __name__ == "__main__":
    main()
