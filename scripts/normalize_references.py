#!/usr/bin/env python3
"""Normalize reference images before analysis/generation.

Features:
- verifies decoding;
- applies EXIF orientation;
- converts to RGB;
- resizes oversized images;
- writes normalized JPEG files;
- computes source and normalized SHA-256 hashes;
- flags exact/normalized duplicates;
- emits normalization-report.json.

Usage:
    python scripts/normalize_references.py <input-dir> <output-dir>
    python scripts/normalize_references.py --self-test
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
DEFAULT_MAX_DIM = 4096


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_name(index: int, source: Path) -> str:
    stem = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in source.stem)
    return f"{index:03d}-{stem}.jpg"


def normalize_one(source: Path, target: Path, max_dim: int) -> dict:
    raw = source.read_bytes()
    source_hash = sha256_bytes(raw)

    try:
        with Image.open(source) as im:
            im.load()
            original_size = [int(im.width), int(im.height)]
            exif_orientation = None
            try:
                exif_orientation = im.getexif().get(274)
            except Exception:
                exif_orientation = None

            im = ImageOps.exif_transpose(im)
            if im.mode not in {"RGB", "L"}:
                if "A" in im.getbands():
                    bg = Image.new("RGB", im.size, "white")
                    alpha = im.getchannel("A")
                    bg.paste(im.convert("RGB"), mask=alpha)
                    im = bg
                else:
                    im = im.convert("RGB")
            elif im.mode == "L":
                im = im.convert("RGB")

            resized = False
            longest = max(im.size)
            if longest > max_dim:
                scale = max_dim / float(longest)
                new_size = (
                    max(1, round(im.width * scale)),
                    max(1, round(im.height * scale)),
                )
                im = im.resize(new_size, Image.Resampling.LANCZOS)
                resized = True

            target.parent.mkdir(parents=True, exist_ok=True)
            im.save(
                target,
                "JPEG",
                quality=92,
                optimize=True,
                progressive=True,
                exif=b"",
            )

        normalized_raw = target.read_bytes()
        return {
            "status": "OK",
            "source_file": source.name,
            "normalized_file": target.name,
            "source_sha256": source_hash,
            "normalized_sha256": sha256_bytes(normalized_raw),
            "original_size": original_size,
            "normalized_size": list(Image.open(target).size),
            "exif_orientation": exif_orientation,
            "exif_orientation_applied": exif_orientation not in (None, 1),
            "resized": resized,
            "output_mode": "RGB",
            "output_format": "JPEG",
        }
    except Exception as exc:
        if target.exists():
            target.unlink()
        return {
            "status": "CORRUPT_OR_UNSUPPORTED",
            "source_file": source.name,
            "source_sha256": source_hash,
            "error": f"{type(exc).__name__}: {exc}",
        }


def run(input_dir: Path, output_dir: Path, max_dim: int) -> dict:
    files = sorted(
        p for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED
    )
    if not files:
        raise ValueError(f"No supported image files found in {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    source_seen: dict[str, str] = {}
    normalized_seen: dict[str, str] = {}

    for index, source in enumerate(files, 1):
        target = output_dir / normalized_name(index, source)
        rec = normalize_one(source, target, max_dim)

        source_hash = rec.get("source_sha256")
        if source_hash:
            rec["exact_duplicate_of"] = source_seen.get(source_hash)
            source_seen.setdefault(source_hash, source.name)

        normalized_hash = rec.get("normalized_sha256")
        if normalized_hash:
            rec["normalized_duplicate_of"] = normalized_seen.get(normalized_hash)
            normalized_seen.setdefault(normalized_hash, rec["normalized_file"])

        records.append(rec)

    report = {
        "schema_version": "1.0",
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "max_dimension": max_dim,
        "summary": {
            "input_files": len(files),
            "normalized_ok": sum(r["status"] == "OK" for r in records),
            "corrupt_or_unsupported": sum(r["status"] != "OK" for r in records),
            "exact_duplicates": sum(bool(r.get("exact_duplicate_of")) for r in records),
            "normalized_duplicates": sum(bool(r.get("normalized_duplicate_of")) for r in records),
        },
        "files": records,
    }
    (output_dir / "normalization-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return report


def self_test() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        src = root / "src"
        dst = root / "dst"
        src.mkdir()

        im = Image.new("RGB", (5000, 2500), (120, 140, 160))
        im.save(src / "a.png")
        (src / "duplicate.png").write_bytes((src / "a.png").read_bytes())
        (src / "broken.jpg").write_bytes(b"not-an-image")

        report = run(src, dst, 1024)
        assert report["summary"]["normalized_ok"] == 2
        assert report["summary"]["corrupt_or_unsupported"] == 1
        assert report["summary"]["exact_duplicates"] == 1
        ok = [x for x in report["files"] if x["status"] == "OK"]
        assert max(ok[0]["normalized_size"]) <= 1024
        print("normalize_references self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", nargs="?", type=Path)
    parser.add_argument("output_dir", nargs="?", type=Path)
    parser.add_argument("--max-dim", type=int, default=DEFAULT_MAX_DIM)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0

    if not args.input_dir or not args.output_dir:
        parser.error("input_dir and output_dir are required unless --self-test is used")
    if args.max_dim < 512:
        parser.error("--max-dim must be at least 512")

    report = run(args.input_dir.resolve(), args.output_dir.resolve(), args.max_dim)
    print(json.dumps(report["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
