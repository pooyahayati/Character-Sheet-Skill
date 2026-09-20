#!/usr/bin/env python3
"""Compute the mandatory pre-generation Coverage Audit.

Usage:
    python scripts/audit_coverage.py build-request.json reference-analysis.json coverage-audit.json
    python scripts/audit_coverage.py ... --accept-lower-level
    python scripts/audit_coverage.py ... --accept-reconstruction
    python scripts/audit_coverage.py --self-test
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVEL_RANK = {"None": 0, "Base": 1, "Advanced": 2, "Full": 3}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def usable_refs(analysis: dict) -> list[dict]:
    return [
        r for r in analysis["references"]
        if r["selection"]["role"] != "Excluded"
        and r.get("normalization", {}).get("status") not in {"Corrupt", "Unsupported"}
    ]


def state(refs: list[dict], predicate) -> str:
    matches = [r for r in refs if predicate(r)]
    if not matches:
        return "Missing"
    if any(r["selection"]["role"] == "Primary" for r in matches):
        return "Strong"
    return "Usable"


def pose_value(r: dict, key: str) -> str:
    return (r.get("pose") or {}).get(key, "Unknown")


def utility_good(r: dict, key: str) -> bool:
    if r.get("analysis_depth") == "Full":
        return (r.get("utility") or {}).get(key) in {"Excellent", "Good"}
    return key in set(r.get("utility_summary") or [])


def build_coverage(request: dict, analysis: dict) -> dict:
    refs = usable_refs(analysis)
    coverage = {
        "face_front": state(refs, lambda r: pose_value(r, "face_view") == "Front"),
        "face_3q_left": state(refs, lambda r: pose_value(r, "face_view") == "Three-Quarter-Subject-Left"),
        "face_3q_right": state(refs, lambda r: pose_value(r, "face_view") == "Three-Quarter-Subject-Right"),
        "profile_left": state(refs, lambda r: pose_value(r, "face_view") == "Profile-Subject-Left"),
        "profile_right": state(refs, lambda r: pose_value(r, "face_view") == "Profile-Subject-Right"),
        "neutral_expression": state(refs, lambda r: r.get("expression") == "Neutral"),
        "smile": state(refs, lambda r: r.get("expression") in {"Soft-Smile", "Closed-Mouth-Smile", "Open-Mouth-Smile"}),
        "body_front": state(refs, lambda r: pose_value(r, "body_view") == "Front"),
        "body_side": state(refs, lambda r: pose_value(r, "body_view") in {"Side-Subject-Left", "Side-Subject-Right"}),
        "body_back": state(refs, lambda r: pose_value(r, "body_view") == "Back"),
        "hands": state(refs, lambda r: utility_good(r, "hands_nails")),
        "feet": state(refs, lambda r: utility_good(r, "feet")),
    }
    return coverage


def supported_level(c: dict) -> str:
    if c["face_front"] == "Missing":
        return "None"
    if c["face_3q_left"] != "Missing" and c["face_3q_right"] != "Missing":
        if c["profile_left"] != "Missing" or c["profile_right"] != "Missing":
            return "Full"
        return "Advanced"
    return "Base"


def request_for(key: str, priority: str) -> dict:
    mapping = {
        "face_front": ("front neutral face", "Add one sharp neutral front/near-front face photo at eye level with low perspective distortion."),
        "face_3q_left": ("3/4 subject-left face", "Add one independent sharp subject-left 3/4 face photo."),
        "face_3q_right": ("3/4 subject-right face", "Add one independent sharp subject-right 3/4 face photo."),
        "profile_left": ("subject-left profile", "Add one clear subject-left profile with the full head visible."),
        "profile_right": ("subject-right profile", "Add one clear subject-right profile with the full head visible."),
        "neutral_expression": ("neutral expression", "Add one neutral-expression face photo."),
        "smile": ("smile reference", "Add one natural smile reference if smile/expression consistency matters."),
        "body_front": ("full-body front", "Add one neutral full-body front photo with feet visible."),
        "body_side": ("full-body side", "Add one low-distortion neutral full-body side photo with feet visible."),
        "body_back": ("full-body back", "Add one neutral full-body back photo if a complete/canonical body board is required."),
        "hands": ("hands", "Add clear hand references if hand identity is required."),
        "feet": ("feet", "Add clear foot references if foot identity is required."),
    }
    label, instruction = mapping[key]
    return {
        "reference_type": label,
        "reason": f"{key} coverage is missing for the requested target.",
        "priority": priority,
        "instruction": instruction,
    }


def audit(request: dict, analysis: dict, accept_lower: bool, accept_reconstruction: bool) -> dict:
    c = build_coverage(request, analysis)
    supported = supported_level(c)
    requested = request["requested_level"]
    layout = request.get("layout_scope", "Auto")
    if layout == "Auto":
        layout = "Complete" if request.get("output_mode") == "Production-Package" else "Compact"

    blocking_keys: list[str] = []
    nonblocking_keys: list[str] = []

    target = supported if requested == "Auto" else requested

    if target in {"Base", "Advanced", "Full"} and c["face_front"] == "Missing":
        blocking_keys.append("face_front")
    if target in {"Advanced", "Full"}:
        for key in ("face_3q_left", "face_3q_right"):
            if c[key] == "Missing":
                blocking_keys.append(key)
    if target == "Full" and c["profile_left"] == "Missing" and c["profile_right"] == "Missing":
        blocking_keys.append("profile_left")

    body_needed = "Body" in request.get("required_details", []) or request.get("goal") == "Modeling-Reference"
    if body_needed and target in {"Advanced", "Full"}:
        if c["body_front"] == "Missing":
            blocking_keys.append("body_front")
        if c["body_side"] == "Missing":
            blocking_keys.append("body_side")

    complete_missing = []
    if layout == "Complete":
        for key in ("face_front", "face_3q_left", "face_3q_right", "profile_left", "profile_right"):
            if c[key] == "Missing":
                complete_missing.append(key)
        if body_needed:
            for key in ("body_front", "body_side", "body_back"):
                if c[key] == "Missing":
                    complete_missing.append(key)

    if complete_missing:
        if accept_reconstruction:
            for key in complete_missing:
                if key not in nonblocking_keys:
                    nonblocking_keys.append(key)
        else:
            for key in complete_missing:
                if key not in blocking_keys:
                    blocking_keys.append(key)

    if requested != "Auto" and LEVEL_RANK[supported] < LEVEL_RANK[requested]:
        if accept_lower and supported != "None":
            # Level gaps remain visible, but no longer block solely because of requested level.
            required_for_supported = {"face_front"}
            if supported in {"Advanced", "Full"}:
                required_for_supported |= {"face_3q_left", "face_3q_right"}
            blocking_keys = [k for k in blocking_keys if k in required_for_supported or k in complete_missing]
            resolution = "User-Accepted-Lower-Level"
        else:
            resolution = "Blocked-Pending-References"
    else:
        resolution = "Matched-Request"

    reconstruction_policy = "Not-Needed"
    if complete_missing:
        reconstruction_policy = (
            "User-Accepted-Reconstructed-Panels"
            if accept_reconstruction else "Pending-User-Decision"
        )

    # Useful but non-blocking recommendations.
    if supported == "Advanced" and c["profile_left"] == "Missing" and c["profile_right"] == "Missing":
        if "profile_left" not in blocking_keys:
            nonblocking_keys.append("profile_left")
    if "Smile" in request.get("required_details", []) and c["smile"] == "Missing":
        if "smile" not in blocking_keys:
            blocking_keys.append("smile")
    if "Hands-Nails" in request.get("required_details", []) and c["hands"] == "Missing":
        blocking_keys.append("hands")
    if "Feet" in request.get("required_details", []) and c["feet"] == "Missing":
        blocking_keys.append("feet")

    blocking_keys = list(dict.fromkeys(blocking_keys))
    nonblocking_keys = [k for k in dict.fromkeys(nonblocking_keys) if k not in blocking_keys]

    requests = [request_for(k, "Required") for k in blocking_keys]
    requests += [request_for(k, "Recommended") for k in nonblocking_keys]

    allowed = not blocking_keys and resolution != "Blocked-Pending-References"
    return {
        "schema_version": "1.0",
        "request_id": request["request_id"],
        "requested_level": requested,
        "supported_level": supported,
        "layout_scope": layout,
        "coverage": c,
        "blocking_gaps": blocking_keys,
        "nonblocking_gaps": nonblocking_keys,
        "targeted_reference_requests": requests,
        "generation_allowed": allowed,
        "resolution": resolution if allowed or resolution == "User-Accepted-Lower-Level" else "Blocked-Pending-References",
        "reconstruction_policy": reconstruction_policy,
        "decision_reason": (
            f"Highest evidence-supported level: {supported}. "
            f"Layout scope: {layout}. "
            + ("Generation may proceed." if allowed else "Required coverage must be resolved before generation.")
        ),
    }


def self_test() -> None:
    req = load(ROOT / "examples/sample-build-request.json")
    analysis = load(ROOT / "examples/sample-reference-analysis.json")
    result = audit(req, analysis, False, False)
    assert result["supported_level"] == "Advanced"
    assert result["generation_allowed"] is True
    assert result["coverage"]["face_3q_left"] != "Missing"
    assert result["coverage"]["face_3q_right"] != "Missing"

    complete_req = dict(req)
    complete_req["layout_scope"] = "Complete"
    blocked = audit(complete_req, analysis, False, False)
    assert blocked["generation_allowed"] is False
    assert "profile_left" in blocked["blocking_gaps"] or "profile_right" in blocked["blocking_gaps"]
    print("audit_coverage self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("build_request", nargs="?", type=Path)
    parser.add_argument("reference_analysis", nargs="?", type=Path)
    parser.add_argument("output", nargs="?", type=Path)
    parser.add_argument("--accept-lower-level", action="store_true")
    parser.add_argument("--accept-reconstruction", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not all([args.build_request, args.reference_analysis, args.output]):
        parser.error("build_request, reference_analysis, and output are required")

    result = audit(
        load(args.build_request),
        load(args.reference_analysis),
        args.accept_lower_level,
        args.accept_reconstruction,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
