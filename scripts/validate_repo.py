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
]

EXAMPLES = [
    ("examples/sample-character-profile.json", "schemas/character-profile.schema.json"),
    ("examples/sample-reference-analysis.json", "schemas/reference-analysis.schema.json"),
    ("examples/sample-build-request.json", "schemas/build-request.schema.json"),
    ("examples/sample-sheet-manifest.json", "schemas/sheet-manifest.schema.json"),
    ("config/level-contract.json", "schemas/level-contract.schema.json"),
]


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def validate_schema_files():
    for rel in SCHEMAS:
        Draft202012Validator.check_schema(load(rel))


def validate_examples():
    for example_rel, schema_rel in EXAMPLES:
        Draft202012Validator(load(schema_rel)).validate(load(example_rel))


def validate_level_contract():
    contract = load("config/level-contract.json")
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

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "Normalize build request / goal / authorization / age handling" not in readme:
        raise AssertionError("README workflow is missing build-request normalization")


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
        "panels": [{
            "panel_id": "canonical-face",
            "panel_type": "Canonical-Face",
            "required": True,
            "evidence_expectation": "Observed-Preferred",
            "source_reference_ids": ["ref-front"],
            "reconstruction_allowed": False
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
            "included_in_final": True
        }],
        "omitted_panels": [],
        "limitations": ["Example validation report."],
        "revision_parent": None
    }
    Draft202012Validator(load("schemas/build-report.schema.json")).validate(build_report)


def main():
    validate_schema_files()
    validate_examples()
    validate_level_contract()
    validate_reference_links()
    validate_scenarios()
    validate_skill_workflow()
    validate_manifest_rules()
    validate_inline_output_examples()
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
