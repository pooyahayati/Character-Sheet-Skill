# Output Contract

## Purpose

A successful build produces structured identity data and approved visual assets, not only one flattened image.

## Output modes

### Quick-Sheet — default

Use for normal users who primarily want the visual character sheet.

Minimum delivery:

```text
character-output/
  final/
    character-sheet.png
    character-sheet-preview.jpg
  panels/
    <approved essential panels>
  build-summary.json
```

Keep internal structured artifacts only as needed for execution; do not force all of them into the user-facing delivery.

### Production-Package — explicit / reusable workflow

Use when the user requests reusable machine-readable identity assets, repeated future generation, or full production provenance.

## Production-Package structure

```text
character-output/
  build-request.json
  reference-analysis.json
  character-profile.json
  identity-anchor-bank.json
  cross-panel-identity-matrix.json
  extremity-profile.json
  skin-identity.json
  hair-dynamics.json
  clothing-behavior.json
  body-proxy.json
  pose-readiness.json
  pose-contracts/
  camera-lighting-contracts/
  generation-routes/
  sheet-plan.json
  panels/
    canonical-face.<ext>
    ...
  sheet-manifest.json
  final/
    character-sheet.svg
  visual-benchmark-result.json
  build-report.json
```

For Quick-Sheet, PNG and JPEG preview are required delivery formats when the environment supports raster rendering. SVG remains useful as a canonical editable composition but should not be the only user-facing deliverable. PDF is optional.

## File roles

- `build-request.json`: requested goal, level and required details.
- `reference-analysis.json`: per-photo analysis and selection role.
- `character-profile.json`: canonical identity and editable attributes.
- `identity-anchor-bank.json`: approved view-specific identity anchors.
- `cross-panel-identity-matrix.json`: pairwise consistency across approved outputs.
- `extremity-profile.json`: left/right hand and foot identity evidence.
- `skin-identity.json`: lighting-independent visible skin rendering cues.
- `hair-dynamics.json`: static hair identity plus pose-dependent behavior.
- `clothing-behavior.json`: garment deformation rules that must not redefine body geometry.
- `body-proxy.json`: canonical body/skeleton/depth/normal control asset when pose production requires it.
- `pose-readiness.json`: independent pose readiness assessment.
- `pose-contracts/`: structured pose/contact/occlusion targets.
- `camera-lighting-contracts/`: explicit camera and lighting state per production panel.
- `generation-routes/`: capability route chosen for each demanding panel.
- `sheet-plan.json`: required and conditional panels for this build.
- `panels/`: individually generated and approved panel assets.
- `sheet-manifest.json`: deterministic composition coordinates and evidence labels.
- `final/character-sheet.svg`: canonical composed board.
- `visual-benchmark-result.json`: pose-production benchmark result when run.
- `build-report.json`: selected level, pose readiness, limitations, blocked/omitted panels and QC summary.

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
- `schemas/body-proxy.schema.json`
- `schemas/pose-contract.schema.json`
- `schemas/pose-readiness.schema.json`
- `schemas/generation-route.schema.json`
- `schemas/visual-benchmark.schema.json`
- `schemas/visual-benchmark-result.schema.json`
- `schemas/identity-anchor-bank.schema.json`
- `schemas/cross-panel-identity-matrix.schema.json`
- `schemas/extremity-profile.schema.json`
- `schemas/skin-identity.schema.json`
- `schemas/hair-dynamics.schema.json`
- `schemas/clothing-behavior.schema.json`
- `schemas/camera-lighting-contract.schema.json`

Every structured output should validate before the final package is approved.
