#!/usr/bin/env python3
"""Build or validate the installable Character Sheet Skill ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "package-manifest.json"
DIST = ROOT / "dist"
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def package_name(manifest: dict) -> str:
    return f"{manifest['package_name']}-v{manifest['version']}.zip"


def iter_files(manifest: dict):
    files = []
    for rel in manifest["runtime_files"]:
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        files.append(path)

    for rel in manifest["runtime_scripts"]:
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        files.append(path)

    for rel in manifest["runtime_directories"]:
        base = ROOT / rel
        if not base.is_dir():
            raise FileNotFoundError(rel)
        for path in sorted(base.rglob("*")):
            if path.is_file():
                files.append(path)

    unique = sorted(set(files), key=lambda p: p.relative_to(ROOT).as_posix())
    return unique


def build(output: Path | None = None) -> Path:
    manifest = load_manifest()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != manifest["version"]:
        raise ValueError(f"VERSION ({version}) != package manifest ({manifest['version']})")

    output = output or (DIST / package_name(manifest))
    output.parent.mkdir(parents=True, exist_ok=True)

    root_dir = manifest["package_name"]
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as zf:
        for path in iter_files(manifest):
            rel = path.relative_to(ROOT).as_posix()
            arcname = f"{root_dir}/{rel}"
            info = ZipInfo(arcname, FIXED_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    (output.parent / "SHA256SUMS.txt").write_text(
        f"{digest}  {output.name}\n", encoding="utf-8"
    )
    return output


def check(path: Path) -> None:
    manifest = load_manifest()
    root_dir = manifest["package_name"]
    required = {
        f"{root_dir}/SKILL.md",
        f"{root_dir}/VERSION",
        f"{root_dir}/LICENSE",
        f"{root_dir}/package-manifest.json",
    }
    forbidden_prefixes = (
        f"{root_dir}/.github/",
        f"{root_dir}/tests/",
        f"{root_dir}/dist/",
        f"{root_dir}/references/",
        f"{root_dir}/character-output/",
        f"{root_dir}/workspaces/",
    )
    forbidden_exact = {
        f"{root_dir}/scripts/validate_repo.py",
        f"{root_dir}/scripts/package_skill.py",
        f"{root_dir}/requirements-dev.txt",
    }

    with ZipFile(path, "r") as zf:
        names = set(zf.namelist())
        missing = required - names
        if missing:
            raise AssertionError(f"Missing required package files: {sorted(missing)}")
        bad = sorted(
            n for n in names
            if n in forbidden_exact or any(n.startswith(p) for p in forbidden_prefixes)
        )
        if bad:
            raise AssertionError(f"Developer/private files leaked into package: {bad}")
        skill_text = zf.read(f"{root_dir}/SKILL.md").decode("utf-8")
        if not skill_text.startswith("---\n"):
            raise AssertionError("SKILL.md frontmatter is missing")
        if "name: character-sheet-skill" not in skill_text:
            raise AssertionError("Unexpected skill name")
        if "description:" not in skill_text:
            raise AssertionError("Skill description is missing")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    if args.check:
        check(args.check.resolve())
        print(f"Package validation passed: {args.check}")
        return 0

    output = build(args.output.resolve() if args.output else None)
    check(output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
