#!/usr/bin/env python3
"""Validate a complete Character Sheet output directory.

Usage:
    python scripts/validate_character_output.py character-output/
    python scripts/validate_character_output.py --self-test
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
LEVEL_RANK = {"None": 0, "Base": 1, "Advanced": 2, "Full": 3}


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def require_file(root: Path, rel: str) -> Path:
    path = (root / rel).resolve()
    if root not in path.parents and path != root:
        raise ValueError(f"Path escapes output root: {rel}")
    if not path.is_file():
        raise FileNotFoundError(f"Required output missing: {rel}")
    return path


def validate(root: Path) -> None:
    root = root.resolve()
    request = load_json(require_file(root, "build-request.json"))
    coverage = load_json(require_file(root, "coverage-audit.json"))
    preflight = load_json(require_file(root, "preflight-plan.json"))
    plan = load_json(require_file(root, "sheet-plan.json"))

    rid = request["request_id"]
    for name, doc in [("coverage-audit", coverage), ("preflight-plan", preflight), ("sheet-plan", plan)]:
        if doc.get("request_id") != rid:
            raise AssertionError(f"{name} request_id does not match build-request")

    if coverage.get("blocking_gaps"):
        raise AssertionError(f"Approved output still has blocking coverage gaps: {coverage['blocking_gaps']}")
    if not coverage.get("generation_allowed"):
        raise AssertionError("Coverage Audit did not allow generation")
    if coverage.get("resolution") == "Blocked-Pending-References":
        raise AssertionError("Coverage is still waiting for required references")

    requested = request["requested_level"]
    supported = coverage["supported_level"]
    if requested != "Auto" and LEVEL_RANK[supported] < LEVEL_RANK[requested]:
        if coverage.get("resolution") != "User-Accepted-Lower-Level":
            raise AssertionError(
                f"Evidence level silently downgraded from {requested} to {supported}"
            )

    if plan.get("selected_level") != supported:
        raise AssertionError("sheet-plan selected_level must match Coverage Audit supported_level")
    if plan.get("layout_scope") != request.get("layout_scope"):
        raise AssertionError("sheet-plan layout_scope must match build-request")
    if coverage.get("layout_scope") != request.get("layout_scope"):
        raise AssertionError("Coverage Audit layout_scope must match build-request")
    if preflight.get("output_mode") != request.get("output_mode"):
        raise AssertionError("preflight output_mode mismatch")

    panel_ids = [p["panel_id"] for p in plan.get("panels", [])]
    if len(panel_ids) != len(set(panel_ids)):
        raise AssertionError("sheet-plan panel IDs must be unique")

    if request.get("layout_scope") == "Complete":
        layout_contract = json.loads((ROOT / "config/layout-scope-contract.json").read_text(encoding="utf-8"))
        required_types = set(layout_contract["scopes"]["Complete"]["required_face_panels"])
        planned_types = {p["panel_type"] for p in plan.get("panels", []) if p.get("required")}
        missing = sorted(required_types - planned_types)
        if missing:
            raise AssertionError(f"Complete layout is missing required face panels: {missing}")

    mode = request["output_mode"]
    if mode == "Quick-Sheet":
        summary = load_json(require_file(root, "build-summary.json"))
        if summary.get("request_id") != rid:
            raise AssertionError("build-summary request_id mismatch")
        if summary.get("evidence_level") != supported:
            raise AssertionError("build-summary evidence_level mismatch")
        if summary.get("layout_scope") != request.get("layout_scope"):
            raise AssertionError("build-summary layout_scope mismatch")
        require_file(root, "final/character-sheet.png")
        require_file(root, "final/character-sheet-preview.jpg")
    elif mode == "Production-Package":
        required = [
            "reference-analysis.json",
            "character-profile.json",
            "identity-anchor-bank.json",
            "cross-panel-identity-matrix.json",
            "extremity-profile.json",
            "skin-identity.json",
            "hair-dynamics.json",
            "clothing-behavior.json",
            "sheet-manifest.json",
            "build-report.json",
        ]
        for rel in required:
            require_file(root, rel)

        manifest = load_json(root / "sheet-manifest.json")
        seen = set()
        for panel in manifest.get("panels", []):
            pid = panel["id"]
            if pid in seen:
                raise AssertionError(f"Duplicate manifest panel id: {pid}")
            seen.add(pid)
            if panel["gate_result"] == "BLOCK":
                raise AssertionError(f"BLOCK panel entered final manifest: {pid}")
            require_file(root, panel["image"])

        report = load_json(root / "build-report.json")
        if report.get("request_id") != rid:
            raise AssertionError("build-report request_id mismatch")
        for result in report.get("panel_results", []):
            if result.get("gate_result") == "BLOCK" and result.get("included_in_final"):
                raise AssertionError(f"BLOCK panel marked included: {result.get('panel_id')}")

        final_dir = root / "final"
        if not any((final_dir / f"character-sheet{ext}").is_file() for ext in (".png", ".jpg", ".jpeg", ".svg", ".pdf")):
            raise AssertionError("Production package has no final character-sheet render")
    else:
        raise AssertionError(f"Unknown output mode: {mode}")

    print("Character output validation passed.")


def self_test() -> None:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        examples = ROOT / "examples"

        mapping = {
            "build-request.json": "sample-build-request.json",
            "coverage-audit.json": "sample-coverage-audit.json",
            "preflight-plan.json": "sample-preflight-plan.json",
            "build-summary.json": "sample-quick-build-summary.json",
        }
        for dest, src in mapping.items():
            (out / dest).write_bytes((examples / src).read_bytes())

        request = load_json(out / "build-request.json")
        plan = {
            "request_id": request["request_id"],
            "character_id": "CS-DEMO-001",
            "selected_level": "Advanced",
            "layout_scope": "Compact",
            "panels": [
                {
                    "panel_id": "canonical-face",
                    "panel_type": "Canonical-Face",
                    "required": True,
                    "evidence_expectation": "Observed-Preferred",
                    "source_reference_ids": ["ref-front"],
                    "reconstruction_allowed": False,
                    "generation_route": "R1-Identity-Reference",
                    "identity_anchor_ids": ["anchor-front"],
                    "camera_lighting_contract_file": None
                }
            ]
        }
        (out / "sheet-plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
        (out / "final").mkdir()
        Image.new("RGB", (64, 64), "white").save(out / "final/character-sheet.png")
        Image.new("RGB", (64, 64), "white").save(out / "final/character-sheet-preview.jpg")
        validate(out)
        print("validate_character_output self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not args.output_dir:
        parser.error("output_dir is required unless --self-test is used")
    validate(args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
