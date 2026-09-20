#!/usr/bin/env python3
"""Repository contract validator for Character Sheet Skill."""

from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

SCHEMAS = [
    "schemas/character-profile.schema.json",
    "schemas/reference-analysis.schema.json",
    "schemas/build-request.schema.json",
    "schemas/sheet-manifest.schema.json",
    "schemas/level-contract.schema.json",
    "schemas/sheet-plan.schema.json",
    "schemas/build-report.schema.json",
    "schemas/body-proxy.schema.json",
    "schemas/pose-contract.schema.json",
    "schemas/pose-readiness.schema.json",
    "schemas/generation-route.schema.json",
    "schemas/visual-benchmark.schema.json",
    "schemas/visual-benchmark-result.schema.json",
    "schemas/identity-anchor-bank.schema.json",
    "schemas/cross-panel-identity-matrix.schema.json",
    "schemas/extremity-profile.schema.json",
    "schemas/skin-identity.schema.json",
    "schemas/hair-dynamics.schema.json",
    "schemas/clothing-behavior.schema.json",
    "schemas/camera-lighting-contract.schema.json",
    "schemas/coverage-audit.schema.json",
    "schemas/preflight-plan.schema.json",
    "schemas/quick-build-summary.schema.json",
]

EXAMPLES = [
    ("examples/sample-character-profile.json", "schemas/character-profile.schema.json"),
    ("examples/sample-reference-analysis.json", "schemas/reference-analysis.schema.json"),
    ("examples/sample-build-request.json", "schemas/build-request.schema.json"),
    ("examples/sample-sheet-manifest.json", "schemas/sheet-manifest.schema.json"),
    ("config/level-contract.json", "schemas/level-contract.schema.json"),
    ("config/visual-benchmark.json", "schemas/visual-benchmark.schema.json"),
    ("examples/sample-body-proxy.json", "schemas/body-proxy.schema.json"),
    ("examples/sample-pose-contract.json", "schemas/pose-contract.schema.json"),
    ("examples/sample-generation-route.json", "schemas/generation-route.schema.json"),
    ("examples/sample-pose-readiness.json", "schemas/pose-readiness.schema.json"),
    ("examples/sample-visual-benchmark-result.json", "schemas/visual-benchmark-result.schema.json"),
    ("examples/sample-identity-anchor-bank.json", "schemas/identity-anchor-bank.schema.json"),
    ("examples/sample-cross-panel-identity-matrix.json", "schemas/cross-panel-identity-matrix.schema.json"),
    ("examples/sample-extremity-profile.json", "schemas/extremity-profile.schema.json"),
    ("examples/sample-skin-identity.json", "schemas/skin-identity.schema.json"),
    ("examples/sample-hair-dynamics.json", "schemas/hair-dynamics.schema.json"),
    ("examples/sample-clothing-behavior.json", "schemas/clothing-behavior.schema.json"),
    ("examples/sample-camera-lighting-contract.json", "schemas/camera-lighting-contract.schema.json"),
    ("examples/sample-sheet-plan.json", "schemas/sheet-plan.schema.json"),
    ("examples/sample-coverage-audit.json", "schemas/coverage-audit.schema.json"),
    ("examples/sample-preflight-plan.json", "schemas/preflight-plan.schema.json"),
    ("examples/sample-quick-build-summary.json", "schemas/quick-build-summary.schema.json"),
]


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def validate_release_metadata():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    manifest = load("package-manifest.json")
    if version != manifest.get("version"):
        raise AssertionError(f"VERSION ({version}) != package manifest ({manifest.get('version')})")
    if manifest.get("package_name") != "character-sheet-skill":
        raise AssertionError("Unexpected package name")
    if manifest.get("entrypoint") != "SKILL.md":
        raise AssertionError("Skill package entrypoint must be SKILL.md")
    if not (ROOT / "LICENSE").is_file():
        raise AssertionError("LICENSE is required for release")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## [{version}]" not in changelog:
        raise AssertionError("CHANGELOG does not contain current VERSION")
    install_doc = (ROOT / "docs/INSTALL-CHATGPT-WINDOWS.md").read_text(encoding="utf-8")
    if "Plugins" not in install_doc or "Skills" not in install_doc or "Upload from your computer" not in install_doc:
        raise AssertionError("Windows install guide is incomplete")


def validate_schema_files():
    for rel in SCHEMAS:
        Draft202012Validator.check_schema(load(rel))


def validate_examples():
    for example_rel, schema_rel in EXAMPLES:
        Draft202012Validator(load(schema_rel)).validate(load(example_rel))


def validate_level_contract():
    contract = load("config/level-contract.json")
    layout_scope = load("config/layout-scope-contract.json")
    layout = load("examples/sheet-layout-spec.json")

    if layout.get("level_contract") != "../config/level-contract.json":
        raise AssertionError("sheet-layout-spec must point to the canonical level contract")
    if "levels" in layout:
        raise AssertionError("sheet-layout-spec must not duplicate normative level definitions")

    for name, level in contract["levels"].items():
        req = set(level["required_sections"])
        cond = set(level["conditional_sections"])
        if req & cond:
            raise AssertionError(f"{name}: required and conditional sections overlap: {sorted(req & cond)}")

    if "best_supported_three_quarter" in contract["levels"]["Base"]["required_sections"]:
        raise AssertionError("Base must not require a three-quarter panel")
    if "full_body_front" in contract["levels"]["Advanced"]["required_sections"]:
        raise AssertionError("Advanced body output must remain goal-conditional")
    complete_faces = set(layout_scope["scopes"]["Complete"]["required_face_panels"])
    expected_complete = {
        "Canonical-Face","Face-Front","Face-Three-Quarter-Left","Face-Three-Quarter-Right",
        "Face-Profile-Left","Face-Profile-Right","Eye-Detail","Mouth-Lip-Detail","Hair"
    }
    if not expected_complete.issubset(complete_faces):
        raise AssertionError("Complete layout must include the full canonical face-angle set")
    complete_faces = set(layout_scope["scopes"]["Complete"]["required_face_panels"])
    expected_complete = {
        "Canonical-Face","Face-Front","Face-Three-Quarter-Left","Face-Three-Quarter-Right",
        "Face-Profile-Left","Face-Profile-Right","Eye-Detail","Mouth-Lip-Detail","Hair"
    }
    if not expected_complete.issubset(complete_faces):
        raise AssertionError("Complete layout must include the full canonical face-angle set")


def validate_staged_reference_analysis():
    analysis = load("examples/sample-reference-analysis.json")
    refs = analysis["references"]
    counts = {
        "Full": sum(r["analysis_depth"] == "Full" for r in refs),
        "Compact": sum(r["analysis_depth"] == "Compact" for r in refs),
        "Excluded-Minimal": sum(r["analysis_depth"] == "Excluded-Minimal" for r in refs),
    }
    summary = analysis["set_summary"]
    if summary["total"] != len(refs):
        raise AssertionError("Reference set_summary.total mismatch")
    if summary["full_analysis"] != counts["Full"]:
        raise AssertionError("Reference full_analysis count mismatch")
    if summary["compact_analysis"] != counts["Compact"]:
        raise AssertionError("Reference compact_analysis count mismatch")
    if summary["minimal_excluded"] != counts["Excluded-Minimal"]:
        raise AssertionError("Reference minimal_excluded count mismatch")
    for r in refs:
        role = r["selection"]["role"]
        depth = r["analysis_depth"]
        if role == "Primary" and depth != "Full":
            raise AssertionError(f"Primary reference must use Full analysis: {r['reference_id']}")
        if role == "Excluded" and depth != "Excluded-Minimal":
            raise AssertionError(f"Excluded reference must use minimal analysis: {r['reference_id']}")


def validate_coverage_and_preflight():
    request = load("examples/sample-build-request.json")
    coverage = load("examples/sample-coverage-audit.json")
    preflight = load("examples/sample-preflight-plan.json")
    if coverage["request_id"] != request["request_id"] or preflight["request_id"] != request["request_id"]:
        raise AssertionError("Coverage/preflight request_id mismatch")
    if coverage["requested_level"] != request["requested_level"]:
        raise AssertionError("Coverage requested_level must match build request")
    if coverage["layout_scope"] != request["layout_scope"]:
        raise AssertionError("Coverage layout_scope must match build request")
    if preflight["output_mode"] != request["output_mode"]:
        raise AssertionError("Preflight output_mode must match build request")
    if preflight["budget_mode"] != request["budget_mode"]:
        raise AssertionError("Preflight budget_mode must match build request")
    if coverage["blocking_gaps"] and coverage["generation_allowed"]:
        raise AssertionError("Coverage with blocking gaps cannot allow generation")
    if preflight["estimated_generation_calls"]["min"] > preflight["estimated_generation_calls"]["max"]:
        raise AssertionError("Invalid generation call estimate range")
    if preflight["estimated_output_files"]["min"] > preflight["estimated_output_files"]["max"]:
        raise AssertionError("Invalid output file estimate range")


def validate_reference_links():
    analysis = load("examples/sample-reference-analysis.json")
    profile = load("examples/sample-character-profile.json")
    by_id = {item["reference_id"]: item for item in analysis["references"]}

    all_profile_refs = set(profile["evidence"]["primary_references"])
    all_profile_refs |= set(profile["evidence"]["validation_references"])
    all_profile_refs |= set(profile["evidence"]["excluded_references"])
    all_profile_refs |= set(profile["qc"]["pre_generation_face_gate"]["evidence_used"])

    missing = sorted(x for x in all_profile_refs if x not in by_id)
    if missing:
        raise AssertionError(f"Profile references missing from reference analysis: {missing}")

    for rid in profile["evidence"]["primary_references"]:
        if by_id[rid]["selection"]["role"] != "Primary":
            raise AssertionError(f"{rid} is listed as Primary in profile but not analysis")

    for rid in profile["evidence"]["validation_references"]:
        if by_id[rid]["selection"]["role"] != "Validation":
            raise AssertionError(f"{rid} is listed as Validation in profile but not analysis")

    for item in analysis["references"]:
        if item["target_subject"]["status"] == "Ambiguous" and item["selection"]["role"] != "Excluded":
            raise AssertionError(f"Ambiguous group reference must be Excluded: {item['reference_id']}")


def validate_scenarios():
    matrix = load("tests/scenario-matrix.json")
    ids = [x["id"] for x in matrix["scenarios"]]
    if len(ids) != len(set(ids)):
        raise AssertionError("Scenario IDs must be unique")
    if set(matrix["gate_outcomes"]) != {"PASS", "PASS_WITH_LIMITS", "BLOCK"}:
        raise AssertionError("Unexpected gate outcome set")


def validate_skill_workflow():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    import re
    nums = [int(x) for x in re.findall(r"^## (\\d+)\\. ", text, flags=re.MULTILINE)]
    if nums != list(range(1, len(nums) + 1)):
        raise AssertionError(f"SKILL workflow numbering is not sequential: {nums}")
    required_phrase = "## 2. Normalize the build request"
    if required_phrase not in text:
        raise AssertionError("SKILL must normalize build request before photo intake")

    if "assets/reference-photo-guide.svg" not in text:
        raise AssertionError("SKILL must require the illustrated reference-photo guide")
    if "coverage-audit.json" not in text:
        raise AssertionError("SKILL must require a pre-generation coverage audit")
    if "subject height" not in text.lower():
        raise AssertionError("SKILL must collect subject height in first-turn intake")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "Normalize build request / goal / authorization / age handling" not in readme:
        raise AssertionError("README workflow is missing build-request normalization")


def validate_pose_ready_contracts():
    readiness = load("config/pose-readiness-contract.json")
    routing = load("config/generation-routing.json")
    benchmark = load("config/visual-benchmark.json")
    profile = load("examples/sample-character-profile.json")

    required_readiness = {"Not-Ready", "Basic", "Strong", "Production"}
    if set(readiness.get("levels", {})) != required_readiness:
        raise AssertionError("Pose-readiness contract must define exactly Not-Ready/Basic/Strong/Production")

    ladder = routing.get("escalation_ladder", [])
    if [x.get("level") for x in ladder] != [1, 2, 3, 4, 5]:
        raise AssertionError("Generation escalation ladder must be sequential 1..5")

    route_names = set(routing.get("routes", {}))
    expected_routes = {
        "R1-Identity-Reference","R2-Identity-Plus-2D-Pose","R3-Identity-Plus-3D-Geometry",
        "R4-Identity-Preserving-Local-Edit","R5-Subject-Specific-Adapter","R6-Dedicated-3D-Avatar"
    }
    if route_names != expected_routes:
        raise AssertionError("Generation routing must define R1..R6 canonical routes")

    difficulties = {s["pose_difficulty"] for s in benchmark["scenarios"]}
    expected_difficulties = {
        "P0-Neutral","P1-Simple","P2-Dynamic","P3-Seated-Leaning","P4-Self-Occlusion","P5-Extreme-Articulation"
    }
    if difficulties != expected_difficulties:
        raise AssertionError(f"Visual benchmark must cover all P0-P5 difficulties: {difficulties}")

    expected_dims = {"Identity-Fidelity","Pose-Accuracy","Anatomical-Plausibility","Photorealism"}
    if set(benchmark["dimensions"]) != expected_dims:
        raise AssertionError("Visual benchmark must use the four canonical dimensions")
    for scenario in benchmark["scenarios"]:
        if set(scenario["required_dimensions"]) != expected_dims:
            raise AssertionError(f"{scenario['id']} must test all four visual dimensions")

    pose_assets = profile.get("pose_assets")
    if not pose_assets:
        raise AssertionError("Sample character profile must link pose assets")
    for key in ("body_proxy_file","pose_readiness_file"):
        rel = pose_assets.get(key)
        if rel and not (ROOT / "examples" / rel).exists():
            raise AssertionError(f"Missing sample pose asset: {rel}")


def validate_source_of_truth_separation():
    pose_schema = load("schemas/pose-contract.schema.json")
    if "camera" in pose_schema.get("properties", {}):
        raise AssertionError("Camera state must live only in camera-lighting-contract, not pose-contract")
    if "camera" in pose_schema.get("required", []):
        raise AssertionError("Pose contract must not require camera state")

    profile_schema = load("schemas/character-profile.schema.json")
    pose_assets = profile_schema["properties"]["pose_assets"]["properties"]
    if "anchor_bank" in pose_assets:
        raise AssertionError("Anchor bank source of truth must be production_assets.identity_anchor_bank_file")


def validate_p1_asset_links():
    profile = load("examples/sample-character-profile.json")
    analysis = load("examples/sample-reference-analysis.json")
    by_ref = {x["reference_id"]: x for x in analysis["references"]}
    assets = profile.get("production_assets", {})

    required_files = [
        "identity_anchor_bank_file",
        "cross_panel_identity_matrix_file",
        "extremity_profile_file",
        "skin_identity_file",
        "hair_dynamics_file",
        "default_clothing_behavior_file",
    ]
    for key in required_files:
        rel = assets.get(key)
        if not rel:
            raise AssertionError(f"Sample profile missing P1 asset link: {key}")
        if not (ROOT / "examples" / rel).exists():
            raise AssertionError(f"Missing P1 sample asset: {rel}")

    bank = load("examples/sample-identity-anchor-bank.json")
    for anchor in bank["anchors"]:
        for rid in anchor["source_reference_ids"]:
            if rid not in by_ref:
                raise AssertionError(f"Anchor references unknown source: {rid}")
        if anchor["role"] == "Primary-Anchor" and anchor["approval"] == "BLOCK":
            raise AssertionError(f"BLOCK anchor cannot be Primary: {anchor['anchor_id']}")

    matrix = load("examples/sample-cross-panel-identity-matrix.json")
    for item in matrix["comparisons"]:
        vals = list(item["checks"].values())
        if item["result"] == "PASS" and any(v == "BLOCK" for v in vals):
            raise AssertionError("Cross-panel PASS cannot contain BLOCK subcheck")
        if item["result"] == "PASS_WITH_LIMITS" and any(v == "BLOCK" for v in vals):
            raise AssertionError("Cross-panel PASS_WITH_LIMITS cannot hide BLOCK subcheck")


def validate_visual_benchmark_result_logic():
    suite = load("config/visual-benchmark.json")
    result = load("examples/sample-visual-benchmark-result.json")
    suite_ids = {s["id"] for s in suite["scenarios"]}

    for item in result["scenario_results"]:
        if item["scenario_id"] not in suite_ids:
            raise AssertionError(f"Unknown benchmark scenario: {item['scenario_id']}")
        values = list(item["dimensions"].values())
        if item["overall"] == "PASS" and any(v != "PASS" for v in values):
            raise AssertionError(f"{item['scenario_id']}: overall PASS requires all four dimensions PASS")
        if item["overall"] == "PASS_WITH_LIMITS" and any(v in {"BLOCK", "NOT_TESTED"} for v in values):
            raise AssertionError(f"{item['scenario_id']}: PASS_WITH_LIMITS cannot hide BLOCK/NOT_TESTED")

    if result["overall_pose_readiness"] == "Production":
        by_id = {x["scenario_id"]: x for x in result["scenario_results"]}
        missing = [s["id"] for s in suite["scenarios"] if s["id"] not in by_id]
        if missing:
            raise AssertionError(f"Production pose readiness requires all benchmark scenarios: {missing}")
        for sid, item in by_id.items():
            if item["overall"] in {"BLOCK", "NOT_TESTED"}:
                raise AssertionError(f"Production pose readiness cannot include {item['overall']}: {sid}")


def validate_manifest_rules():
    manifest = load("examples/sample-sheet-manifest.json")
    for panel in manifest["panels"]:
        if panel["gate_result"] == "BLOCK":
            raise AssertionError("BLOCK panel may not appear in a final composition manifest")


def validate_inline_output_examples():
    sheet_plan = {
        "request_id": "REQ-DEMO-001",
        "character_id": "CS-DEMO-001",
        "selected_level": "Base",
        "layout_scope": "Compact",
        "panels": [{
            "panel_id": "canonical-face",
            "panel_type": "Canonical-Face",
            "required": True,
            "evidence_expectation": "Observed-Preferred",
            "source_reference_ids": ["ref-front"],
            "reconstruction_allowed": False,
            "generation_route": "R1-Identity-Reference",
            "pose_contract_file": None,
            "pose_difficulty": "Not-Applicable",
            "identity_anchor_ids": ["anchor-front"],
            "camera_lighting_contract_file": "sample-camera-lighting-contract.json"
        }]
    }
    Draft202012Validator(load("schemas/sheet-plan.schema.json")).validate(sheet_plan)

    build_report = {
        "request_id": "REQ-DEMO-001",
        "character_id": "CS-DEMO-001",
        "profile_version": "1.0",
        "selected_level": "Base",
        "status": "Approved-With-Limits",
        "reference_ids": ["ref-front"],
        "panel_results": [{
            "panel_id": "canonical-face",
            "gate_result": "PASS",
            "included_in_final": True,
            "assessment_method": "Model-Visual-Review"
        }],
        "omitted_panels": [],
        "limitations": ["Example validation report."],
        "revision_parent": None
    }
    Draft202012Validator(load("schemas/build-report.schema.json")).validate(build_report)


def main():
    validate_release_metadata()
    validate_schema_files()
    validate_examples()
    validate_level_contract()
    validate_staged_reference_analysis()
    validate_coverage_and_preflight()
    validate_reference_links()
    validate_scenarios()
    validate_skill_workflow()
    validate_pose_ready_contracts()
    validate_source_of_truth_separation()
    validate_p1_asset_links()
    validate_visual_benchmark_result_logic()
    validate_manifest_rules()
    validate_inline_output_examples()
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
