#!/usr/bin/env python3
"""Deterministic SVG compositor for approved Character Sheet panels.

Usage:
    python scripts/compose_sheet.py sheet-manifest.json output.svg

The manifest must contain only PASS or PASS_WITH_LIMITS panels.
BLOCK panels are rejected.
"""

from __future__ import annotations
import base64
import json
import mimetypes
import sys
from html import escape
from pathlib import Path


def data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    if mime not in {"image/png", "image/jpeg", "image/webp", "image/svg+xml"}:
        raise ValueError(f"Unsupported panel image type: {path}")
    raw = path.read_bytes()
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: compose_sheet.py <sheet-manifest.json> <output.svg>", file=sys.stderr)
        return 2

    manifest_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

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

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        ".title{font:700 34px Arial,sans-serif;fill:#ffffff}",
        ".sub{font:400 16px Arial,sans-serif;fill:#d8dde3}",
        ".label{font:600 15px Arial,sans-serif;fill:#222}",
        ".meta{font:400 12px Arial,sans-serif;fill:#555}",
        ".panel{fill:#fff;stroke:#c9c4bc;stroke-width:2}",
        ".badge{fill:#f4f1eb;stroke:#b9b2a8;stroke-width:1}",
        "</style>",
        f'<rect width="{width}" height="{height}" fill="{escape(background)}"/>',
        f'<rect x="0" y="0" width="{width}" height="92" fill="#24292f"/>',
        f'<text x="28" y="43" class="title">{escape(str(manifest["title"]))}</text>',
        f'<text x="28" y="70" class="sub">{escape(str(manifest["character_id"]))} · {escape(str(manifest["version"]))} · {escape(str(manifest["level"]))}</text>',
    ]

    base_dir = manifest_path.parent
    for panel in panels:
        x, y = int(panel["x"]), int(panel["y"])
        w, h = int(panel["width"]), int(panel["height"])
        label_h = 54
        image_path = (base_dir / panel["image"]).resolve()
        uri = data_uri(image_path)
        label = escape(str(panel["label"]))
        ev = escape(str(panel["evidence_status"]))
        gate = escape(str(panel["gate_result"]))
        notes = escape(str(panel.get("notes", "")))

        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="panel"/>')
        svg.append(f'<image href="{uri}" x="{x+8}" y="{y+8}" width="{w-16}" height="{h-label_h-12}" preserveAspectRatio="xMidYMid meet"/>')
        svg.append(f'<text x="{x+12}" y="{y+h-31}" class="label">{label}</text>')
        svg.append(f'<text x="{x+12}" y="{y+h-12}" class="meta">{ev} · {gate}{(" · " + notes) if notes else ""}</text>')

    svg.append("</svg>")
    output_path.write_text("\n".join(svg), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
