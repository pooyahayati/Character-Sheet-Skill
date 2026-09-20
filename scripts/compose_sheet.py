#!/usr/bin/env python3
"""Deterministic Character Sheet compositor.

Supported outputs:
    .svg  .png  .jpg/.jpeg  .pdf

Examples:
    python scripts/compose_sheet.py sheet-manifest.json output.svg
    python scripts/compose_sheet.py sheet-manifest.json output.svg --image-mode linked
    python scripts/compose_sheet.py sheet-manifest.json output.png
    python scripts/compose_sheet.py sheet-manifest.json preview.jpg --direction rtl --locale fa

Only PASS / PASS_WITH_LIMITS panels may be composed.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import mimetypes
import os
from html import escape
from pathlib import Path

from PIL import Image

SUPPORTED_MIME = {"image/png", "image/jpeg", "image/webp", "image/svg+xml"}


def resolve_panel_path(base_dir: Path, rel: str, panel_id: str) -> Path:
    path = (base_dir / rel).resolve()
    if base_dir not in path.parents and path != base_dir:
        raise ValueError(f"Panel image escapes manifest directory: {panel_id}")
    if not path.exists():
        raise FileNotFoundError(f"Missing panel image for {panel_id}: {path}")
    return path


def raster_bytes(path: Path, max_dim: int, jpeg_quality: int) -> tuple[str, bytes]:
    mime, _ = mimetypes.guess_type(str(path))
    if mime not in {"image/png", "image/jpeg", "image/webp"}:
        raise ValueError(f"Not a raster image: {path}")

    with Image.open(path) as im:
        im.load()
        if max(im.size) > max_dim:
            scale = max_dim / float(max(im.size))
            im = im.resize(
                (max(1, round(im.width * scale)), max(1, round(im.height * scale))),
                Image.Resampling.LANCZOS,
            )

        out = io.BytesIO()
        if "A" in im.getbands():
            im.save(out, "PNG", optimize=True)
            return "image/png", out.getvalue()

        im = im.convert("RGB")
        im.save(out, "JPEG", quality=jpeg_quality, optimize=True, progressive=True)
        return "image/jpeg", out.getvalue()


def data_uri(path: Path, max_dim: int, jpeg_quality: int) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    if mime not in SUPPORTED_MIME:
        raise ValueError(f"Unsupported panel image type: {path}")

    if mime == "image/svg+xml":
        raw = path.read_bytes()
    else:
        mime, raw = raster_bytes(path, max_dim, jpeg_quality)

    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def href_for(path: Path, output_path: Path, image_mode: str, max_dim: int, jpeg_quality: int) -> str:
    if image_mode == "embed":
        return data_uri(path, max_dim, jpeg_quality)
    rel = os.path.relpath(path, output_path.parent).replace("\\", "/")
    return rel


def direction_for(locale: str, requested: str) -> str:
    if requested in {"ltr", "rtl"}:
        return requested
    lang = locale.lower().split("-")[0]
    return "rtl" if lang in {"fa", "ar", "he", "ur"} else "ltr"


def svg_text_attrs(direction: str, x_ltr: int, x_rtl: int) -> tuple[int, str]:
    if direction == "rtl":
        return x_rtl, 'text-anchor="end" direction="rtl" unicode-bidi="plaintext"'
    return x_ltr, 'text-anchor="start" direction="ltr"'


def build_svg(
    manifest: dict,
    manifest_path: Path,
    output_path: Path,
    image_mode: str,
    locale: str,
    direction: str,
    font_family: str,
    max_embed_dim: int,
    jpeg_quality: int,
) -> str:
    canvas = manifest.get("canvas", {})
    width = int(canvas.get("width", 1800))
    height = int(canvas.get("height", 1200))
    background = str(canvas.get("background", "#ece9e4"))

    panels = manifest.get("panels", [])
    if not panels:
        raise ValueError("Manifest has no panels")
    for panel in panels:
        if panel.get("gate_result") not in {"PASS", "PASS_WITH_LIMITS"}:
            raise ValueError(f"Panel {panel.get('id')} is not approved for composition")

    dir_value = direction_for(locale, direction)
    header_x, header_attrs = svg_text_attrs(dir_value, 28, width - 28)
    safe_font = escape(font_family, quote=True)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" lang="{escape(locale)}" direction="{dir_value}">',
        "<style>",
        f'.title{{font:700 34px {safe_font};fill:#ffffff}}',
        f'.sub{{font:400 16px {safe_font};fill:#d8dde3}}',
        f'.label{{font:600 15px {safe_font};fill:#222}}',
        f'.meta{{font:400 12px {safe_font};fill:#555}}',
        ".panel{fill:#fff;stroke:#c9c4bc;stroke-width:2}",
        "</style>",
        f'<rect width="{width}" height="{height}" fill="{escape(background)}"/>',
        f'<rect x="0" y="0" width="{width}" height="92" fill="#24292f"/>',
        f'<text x="{header_x}" y="43" class="title" {header_attrs}>{escape(str(manifest["title"]))}</text>',
        f'<text x="{header_x}" y="70" class="sub" {header_attrs}>{escape(str(manifest["character_id"]))} · {escape(str(manifest["version"]))} · {escape(str(manifest["level"]))}</text>',
    ]

    base_dir = manifest_path.parent
    for panel in panels:
        x, y = int(panel["x"]), int(panel["y"])
        w, h = int(panel["width"]), int(panel["height"])
        label_h = 54
        image_path = resolve_panel_path(base_dir, panel["image"], str(panel.get("id")))
        href = href_for(image_path, output_path, image_mode, max_embed_dim, jpeg_quality)
        label = escape(str(panel["label"]))
        ev = escape(str(panel["evidence_status"]))
        gate = escape(str(panel["gate_result"]))
        notes = escape(str(panel.get("notes", "")))
        text_x, text_attrs = svg_text_attrs(dir_value, x + 12, x + w - 12)

        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="panel"/>')
        svg.append(
            f'<image href="{escape(href, quote=True)}" x="{x+8}" y="{y+8}" '
            f'width="{w-16}" height="{h-label_h-12}" preserveAspectRatio="xMidYMid meet"/>'
        )
        svg.append(f'<text x="{text_x}" y="{y+h-31}" class="label" {text_attrs}>{label}</text>')
        meta = f"{ev} · {gate}" + (f" · {notes}" if notes else "")
        svg.append(f'<text x="{text_x}" y="{y+h-12}" class="meta" {text_attrs}>{meta}</text>')

    svg.append("</svg>")
    return "\n".join(svg)


def render(svg: str, output_path: Path, width: int, height: int, jpeg_quality: int) -> None:
    suffix = output_path.suffix.lower()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if suffix == ".svg":
        output_path.write_text(svg, encoding="utf-8")
        return

    try:
        import cairosvg
    except ImportError as exc:
        raise RuntimeError(
            "Raster/PDF output requires CairoSVG. Install requirements-runtime.txt."
        ) from exc

    raw = svg.encode("utf-8")
    if suffix == ".png":
        cairosvg.svg2png(bytestring=raw, write_to=str(output_path), output_width=width, output_height=height)
        return
    if suffix == ".pdf":
        cairosvg.svg2pdf(bytestring=raw, write_to=str(output_path))
        return
    if suffix in {".jpg", ".jpeg"}:
        png = cairosvg.svg2png(bytestring=raw, output_width=width, output_height=height)
        with Image.open(io.BytesIO(png)) as im:
            rgb = Image.new("RGB", im.size, "white")
            if "A" in im.getbands():
                rgb.paste(im.convert("RGB"), mask=im.getchannel("A"))
            else:
                rgb.paste(im.convert("RGB"))
            rgb.save(output_path, "JPEG", quality=jpeg_quality, optimize=True, progressive=True)
        return
    raise ValueError(f"Unsupported output extension: {suffix}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--image-mode", choices=["embed", "linked"], default=None)
    parser.add_argument("--locale", default=None)
    parser.add_argument("--direction", choices=["auto", "ltr", "rtl"], default=None)
    parser.add_argument("--font-family", default=None)
    parser.add_argument("--max-embed-dim", type=int, default=None)
    parser.add_argument("--jpeg-quality", type=int, default=None)
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    output_path = args.output.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    render_cfg = manifest.get("render", {})

    locale = args.locale or render_cfg.get("locale", "en")
    direction = args.direction or render_cfg.get("direction", "auto")
    font_family = args.font_family or render_cfg.get("font_family", 'Arial, "Noto Sans", sans-serif')
    max_embed_dim = args.max_embed_dim or int(render_cfg.get("max_embed_dim", 2400))
    jpeg_quality = args.jpeg_quality or int(render_cfg.get("jpeg_quality", 88))
    image_mode = args.image_mode or render_cfg.get("image_mode", "embed")

    if output_path.suffix.lower() != ".svg":
        image_mode = "embed"

    canvas = manifest.get("canvas", {})
    width = int(canvas.get("width", 1800))
    height = int(canvas.get("height", 1200))

    svg = build_svg(
        manifest, manifest_path, output_path, image_mode, locale, direction,
        font_family, max_embed_dim, jpeg_quality
    )
    render(svg, output_path, width, height, jpeg_quality)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
