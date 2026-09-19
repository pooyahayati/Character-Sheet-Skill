# Output Contract

## Purpose

A successful build produces structured identity data and approved visual assets, not only one flattened image.

## Required output package

```text
character-output/
  build-request.json
  reference-analysis.json
  character-profile.json
  sheet-plan.json
  panels/
    canonical-face.<ext>
    ...
  sheet-manifest.json
  final/
    character-sheet.svg
  build-report.json
```

Additional PNG/PDF renders are optional derivatives of the canonical SVG.

## File roles

- `build-request.json`: requested goal, level and required details.
- `reference-analysis.json`: per-photo analysis and selection role.
- `character-profile.json`: canonical identity and editable attributes.
- `sheet-plan.json`: required and conditional panels for this build.
- `panels/`: individually generated and approved panel assets.
- `sheet-manifest.json`: deterministic composition coordinates and evidence labels.
- `final/character-sheet.svg`: canonical composed board.
- `build-report.json`: selected level, limitations, blocked/omitted panels and QC summary.

## Naming

Use stable semantic panel names. Do not use random names as the primary identifier.

Examples:

- `face-front-neutral`
- `face-three-quarter-subject-left`
- `face-profile-subject-right`
- `expression-soft-smile`
- `body-front-neutral`

## Approval

Only panel assets whose gate is PASS or explicitly permitted PASS_WITH_LIMITS may be packaged as approved panels.

BLOCK panels remain diagnostic artifacts and must not appear in the final sheet.

## Provenance

The build report must preserve:

- canonical profile version;
- build request ID;
- reference IDs used;
- panel gate outcomes;
- reconstructed/unverified areas;
- revision parent when applicable.


## Schemas

- `schemas/build-request.schema.json`
- `schemas/reference-analysis.schema.json`
- `schemas/character-profile.schema.json`
- `schemas/sheet-plan.schema.json`
- `schemas/sheet-manifest.schema.json`
- `schemas/build-report.schema.json`

Every structured output should validate before the final package is approved.
