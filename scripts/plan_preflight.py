#!/usr/bin/env python3
"""Build a pre-generation execution estimate from request, coverage and sheet plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DETAIL_TYPES = {"Eye-Detail","Mouth-Lip-Detail","Hair","Distinctive-Features","Metadata","Color-Palette"}
FACE_TYPES = {"Canonical-Face","Face-Front","Face-Three-Quarter-Left","Face-Three-Quarter-Right","Face-Profile-Left","Face-Profile-Right"}
EXPRESSION_TYPES = {"Smile"}
BODY_TYPES = {"Body-Front","Body-Side","Body-Back","Modeling-Pose","Pose-Diagnostic","Hands-Nails"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def group_panels(panels: list[dict]) -> list[list[str]]:
    groups = []
    for types in (FACE_TYPES, DETAIL_TYPES, EXPRESSION_TYPES, BODY_TYPES):
        ids = [p["panel_id"] for p in panels if p["panel_type"] in types]
        if ids:
            groups.append(ids)
    return groups


def estimate(request: dict, coverage: dict, plan: dict, seconds_per_call: float | None, cost_per_call: float | None) -> dict:
    if not coverage.get("generation_allowed"):
        raise ValueError("Coverage Audit blocks generation; do not create an execution plan yet.")

    panels = plan.get("panels", [])
    budget = request.get("budget_mode", "Balanced")
    repair_budget = {"Economy": 1, "Balanced": 2, "Maximum-Fidelity": 3}[budget]

    min_calls = 0
    max_base_calls = 0
    generative_panels = 0
    for panel in panels:
        ptype = panel["panel_type"]
        if ptype in {"Metadata","Color-Palette"}:
            continue
        # Detail panels can often be direct crops/edits and may not need a new generation.
        if ptype in DETAIL_TYPES and panel.get("source_reference_ids"):
            max_base_calls += 1
            continue
        min_calls += 1
        max_base_calls += 1
        generative_panels += 1

    # Repairs are a budget ceiling, not an assumption that every panel will fail.
    max_calls = max_base_calls + min(repair_budget, max(0, generative_panels))
    mode = request["output_mode"]
    if mode == "Quick-Sheet":
        min_files = 4
        max_files = 6 + len(panels)
    else:
        min_files = 14
        max_files = 24 + len(panels)

    if max_calls <= 4:
        relative = "Low"
    elif max_calls <= 8:
        relative = "Medium"
    elif max_calls <= 14:
        relative = "High"
    else:
        relative = "Very-High"

    if seconds_per_call is not None:
        wall = {
            "status": "Estimated-From-History",
            "value": f"serial upper-bound approx. {min_calls * seconds_per_call:.0f}-{max_calls * seconds_per_call:.0f} seconds before parallelism"
        }
    else:
        wall = {"status": "Unavailable", "value": None}

    if cost_per_call is not None:
        cost = {
            "status": "Estimated-From-Backend-Pricing",
            "value": f"approx. {min_calls * cost_per_call:.2f}-{max_calls * cost_per_call:.2f} in backend billing units"
        }
    else:
        cost = {"status": "Relative-Only", "value": f"{relative} relative generation cost; backend pricing unavailable."}

    return {
        "schema_version": "1.0",
        "request_id": request["request_id"],
        "output_mode": mode,
        "budget_mode": budget,
        "planned_panels": len(panels),
        "estimated_generation_calls": {"min": min_calls, "max": max_calls},
        "estimated_output_files": {"min": min_files, "max": max_files},
        "relative_compute": relative,
        "parallel_groups": group_panels(panels),
        "wall_clock_estimate": wall,
        "cost_estimate": cost,
        "repair_budget": repair_budget,
        "notes": [
            "Detail panels should use direct crops/edits when source evidence is adequate.",
            "Independent groups may run in parallel after their required anchors are approved.",
            "Estimates are planning bounds, not a promise of exact runtime or price."
        ]
    }


def self_test() -> None:
    request = load(ROOT / "examples/sample-build-request.json")
    coverage = load(ROOT / "examples/sample-coverage-audit.json")
    plan = load(ROOT / "examples/sample-sheet-plan.json")
    result = estimate(request, coverage, plan, None, None)
    assert result["planned_panels"] == len(plan["panels"])
    assert result["estimated_generation_calls"]["max"] >= result["estimated_generation_calls"]["min"]
    assert result["cost_estimate"]["status"] == "Relative-Only"
    print("plan_preflight self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("build_request", nargs="?", type=Path)
    parser.add_argument("coverage_audit", nargs="?", type=Path)
    parser.add_argument("sheet_plan", nargs="?", type=Path)
    parser.add_argument("output", nargs="?", type=Path)
    parser.add_argument("--seconds-per-call", type=float)
    parser.add_argument("--cost-per-call", type=float)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not all([args.build_request, args.coverage_audit, args.sheet_plan, args.output]):
        parser.error("build_request, coverage_audit, sheet_plan, and output are required")

    result = estimate(
        load(args.build_request),
        load(args.coverage_audit),
        load(args.sheet_plan),
        args.seconds_per_call,
        args.cost_per_call,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
