#!/usr/bin/env python3
"""Generate a QR code (SVG or PNG) from a link, ready to use in slides.

Part of the `slide-creator` skill (the `/slide-creator qr` command). Typical use:

    python3 generate_qr.py \
        --url https://example.com \
        --out <SLIDES_DIR>/my-deck/assets/qr/example.svg \
        --dark "#43012A" --round

SVG is vector (scales without pixelating) → recommended format for slides.
PNG is for destinations that don't accept SVG.

--round rounds the corners (card look). The radius stays INSIDE the quiet zone
so it doesn't clip the QR's finder patterns (the corner squares) — clipping them
would break scanning.

Requires `segno` (pip install segno). The `--round --png` combo also needs
`Pillow` (pip install Pillow).
"""
import argparse
import io
import re
import sys
from pathlib import Path

import segno


def _round_svg(svg: str, radius_units: float) -> str:
    """Wrap the SVG content in a rounded-rect clipPath."""
    open_tag = re.search(r"<svg\b[^>]*>", svg)
    if not open_tag:
        return svg
    tag = open_tag.group(0)
    w = re.search(r'width="([\d.]+)"', tag)
    h = re.search(r'height="([\d.]+)"', tag)
    if not (w and h):
        return svg
    defs = (
        f'<defs><clipPath id="qr-round">'
        f'<rect width="{w.group(1)}" height="{h.group(1)}" '
        f'rx="{radius_units}" ry="{radius_units}"/>'
        f'</clipPath></defs><g clip-path="url(#qr-round)">'
    )
    svg = svg.replace(tag, tag + defs, 1)
    return svg.replace("</svg>", "</g></svg>")


def _round_png(png_bytes: bytes, radius_px: int) -> bytes:
    """Apply a rounded-corner alpha mask to the PNG (via Pillow)."""
    from PIL import Image, ImageDraw

    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, img.size[0] - 1, img.size[1] - 1], radius=radius_px, fill=255
    )
    img.putalpha(mask)
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def main() -> None:
    p = argparse.ArgumentParser(description="Generate a QR code from a link.")
    p.add_argument("--url", required=True,
                   help="QR content (link, text, vCard, etc.)")
    p.add_argument("--out", required=True,
                   help="Output path (.svg or .png). Parent folders are created.")
    p.add_argument("--dark", default="#000000",
                   help="Module color (default black). Use a DARK color from the "
                        "deck's palette for high contrast.")
    p.add_argument("--light", default="#FFFFFF",
                   help="Background color (default white). 'transparent' for a "
                        "transparent background (lowers scannability over textured backgrounds).")
    p.add_argument("--scale", type=int, default=8,
                   help="Size per module. PNG: px/module (raise for sharpness). "
                        "SVG: only affects intrinsic size, scales the same via CSS.")
    p.add_argument("--border", type=int, default=2,
                   help="Quiet zone in modules (default 2; recommended minimum 2). "
                        "With --round it's raised to 4 if lower, to make room for rounding.")
    p.add_argument("--error", default="m", choices=["l", "m", "q", "h"],
                   help="Error correction: l=7%% m=15%% q=25%% h=30%%. "
                        "Higher = denser QR but tolerates damage/logo (default m).")
    p.add_argument("--round", action="store_true",
                   help="Rounded corners (card look). The radius stays inside the "
                        "quiet zone so it doesn't break the QR.")
    p.add_argument("--radius", type=int, default=None,
                   help="Rounding radius in modules. Default: the quiet zone width "
                        "(border). Capped to border so it never clips data.")
    args = p.parse_args()

    out = Path(args.out).expanduser()
    ext = out.suffix.lower()
    if ext not in (".svg", ".png"):
        sys.exit(f"Unsupported format: '{out.suffix}'. Use .svg or .png")
    out.parent.mkdir(parents=True, exist_ok=True)

    light = None if args.light.lower() == "transparent" else args.light

    border = args.border
    if args.round:
        border = max(border, 4)  # enough margin to round without touching finder patterns
    # radius in modules, never larger than the quiet zone → never clips data
    radius_modules = min(args.radius if args.radius is not None else border, border)
    radius_units = radius_modules * args.scale

    qr = segno.make(args.url, error=args.error)
    buff = io.BytesIO()
    qr.save(buff, kind=ext.lstrip("."), dark=args.dark, light=light,
            border=border, scale=args.scale)
    data = buff.getvalue()

    if ext == ".svg":
        text = data.decode("utf-8")
        if args.round:
            text = _round_svg(text, radius_units)
        out.write_text(text, encoding="utf-8")
    else:
        if args.round:
            data = _round_png(data, radius_units)
        out.write_bytes(data)

    shape = f"round(r={radius_modules})" if args.round else "square"
    print(f"OK  {out}")
    print(f"    url={args.url!r}  version={qr.version}  error={args.error.upper()}  "
          f"dark={args.dark} light={args.light}  corners={shape}")


if __name__ == "__main__":
    main()
