#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps


def parse_box(value: str) -> tuple[int, int, int, int]:
    try:
        parts = tuple(int(part.strip()) for part in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("box must be four comma-separated integers") from exc
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("box must be x1,y1,x2,y2")
    x1, y1, x2, y2 = parts
    if x2 <= x1 or y2 <= y1:
        raise argparse.ArgumentTypeError("box must have positive width and height")
    return parts


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def compose(
    source: Path,
    output: Path,
    canvas: tuple[int, int],
    box: tuple[int, int, int, int],
    blur: int,
    dim: int,
    radius: int,
) -> None:
    canvas_w, canvas_h = canvas
    src = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    src_w, src_h = src.size

    bg_scale = max(canvas_w / src_w, canvas_h / src_h)
    bg_size = (math.ceil(src_w * bg_scale), math.ceil(src_h * bg_scale))
    background = src.resize(bg_size, Image.Resampling.LANCZOS)
    bg_left = (background.width - canvas_w) // 2
    bg_top = (background.height - canvas_h) // 2
    background = background.crop((bg_left, bg_top, bg_left + canvas_w, bg_top + canvas_h))
    background = background.filter(ImageFilter.GaussianBlur(blur)).convert("RGBA")
    background.alpha_composite(Image.new("RGBA", canvas, (3, 5, 6, dim)))

    x1, y1, x2, y2 = box
    if x1 < 0 or y1 < 0 or x2 > canvas_w or y2 > canvas_h:
        raise ValueError("box must fit inside the canvas")
    max_w, max_h = x2 - x1, y2 - y1
    fg_scale = min(max_w / src_w, max_h / src_h)
    fg_size = (max(1, round(src_w * fg_scale)), max(1, round(src_h * fg_scale)))
    foreground = src.resize(fg_size, Image.Resampling.LANCZOS).convert("RGBA")
    foreground.putalpha(rounded_mask(fg_size, radius))
    px = x1 + (max_w - fg_size[0]) // 2
    py = y1 + (max_h - fg_size[1]) // 2

    shadow = Image.new("RGBA", canvas, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (px - 10, py - 10, px + fg_size[0] + 10, py + fg_size[1] + 10),
        radius=radius + 8,
        fill=(0, 0, 0, 210),
    )
    background.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(26)))
    background.alpha_composite(foreground, (px, py))
    ImageDraw.Draw(background, "RGBA").rounded_rectangle(
        (px - 2, py - 2, px + fg_size[0] + 2, py + fg_size[1] + 2),
        radius=radius + 2,
        outline=(255, 255, 255, 100),
        width=4,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() in {".jpg", ".jpeg"}:
        background.convert("RGB").save(output, quality=95, optimize=True)
    else:
        background.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Preserve a still inside a vertical blurred-background canvas.")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--box", type=parse_box, default="60,100,1020,1380")
    parser.add_argument("--blur", type=int, default=48)
    parser.add_argument("--dim", type=int, default=145, choices=range(0, 256), metavar="0-255")
    parser.add_argument("--radius", type=int, default=18)
    args = parser.parse_args()

    if args.width <= 0 or args.height <= 0 or args.blur < 0 or args.radius < 0:
        parser.error("width/height must be positive; blur/radius must be non-negative")
    if not args.source.is_file():
        parser.error(f"source not found: {args.source}")

    compose(
        args.source,
        args.output,
        (args.width, args.height),
        args.box,
        args.blur,
        args.dim,
        args.radius,
    )
    print(args.output.resolve())


if __name__ == "__main__":
    main()
