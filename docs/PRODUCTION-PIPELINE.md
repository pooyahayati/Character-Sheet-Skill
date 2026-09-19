# Production Pipeline Contract

## Purpose

This document defines the actual production order for identity-faithful character sheets.

The skill must not ask an image model to create the final multi-panel board in one generation. Multi-panel generation makes identity drift, text errors, proportion drift, and inconsistent camera geometry much harder to detect and repair.

## Required production order

```text
Reference Intake
→ Reference Selection
→ Canonical Identity Profile
→ Canonical Body Proxy when pose production is required
→ Pose Readiness Target
→ Multi-view Identity Anchor Bank
→ Anchor Bank QC
→ Individual Face Panels
→ Per-Panel Face QC
→ Pose Contract + Generation Route
→ Individual Body / Pose Panels
→ Per-Panel Face + Pose + Anatomy QC
→ Detail Panels
→ Modeling / Expression Panels
→ Per-Panel QC
→ Approved Panel Set
→ Deterministic Composition
→ Final Sheet QC
```

## Backend capability requirement

A production backend must support reference-conditioned image generation or editing from supplied images.

If the available backend can only perform text-to-image generation and cannot condition on the user's reference images, the skill may produce a Sheet Plan but must not approve the output as identity-faithful.

## Canonical Face Anchor

Before generating profile, 3/4, body, expression, or modeling panels:

1. choose the strongest facial references;
2. build the canonical identity profile;
3. approve a neutral frontal anchor;
4. add evidence-supported 3/4/profile/detail anchors when available;
5. validate every anchor against the original source references;
6. store the bank using `schemas/identity-anchor-bank.schema.json`.

Downstream panels use the nearest relevant approved anchor(s), plus the relevant original references.

A reconstructed anchor remains Reconstructed and cannot become stronger evidence than its source references.

The anchor bank is a production control asset. It is not new source evidence.

## Panel isolation rule

Generate or edit each logical panel independently.

Examples:

- front neutral face;
- subject-left 3/4;
- subject-right 3/4;
- left profile;
- right profile;
- neutral body front;
- neutral body side;
- neutral body back;
- soft smile;
- closed smile;
- open smile;
- hands/nails;
- modeling poses.

Never rely on a single model call to create the entire character-sheet board.

## Pose and structural control

For pose-dependent panels, create a pose/camera contract before generation.

Use:

- `schemas/pose-contract.schema.json`;
- `schemas/body-proxy.schema.json`;
- `config/pose-readiness-contract.json`.

P3-P5 panels should use 3D/depth/normal/SMPL-X-like structural controls when supported.

## Generation routing

Route by capability, not vendor/model name.

Use `docs/GENERATION-ROUTER.md` and `config/generation-routing.json`.

Repeated critical failure triggers escalation to a stronger route instead of blind repetition.

## Reference routing per panel

Every panel receives:

1. nearest relevant approved identity anchor(s);
2. the minimal original references relevant to that panel;
3. canonical locked attributes;
4. pose contract when relevant;
5. camera-lighting contract;
6. clothing behavior contract when relevant;
7. skin/hair/extremity assets when visible/relevant;
8. the explicit list of attributes that are allowed to change.

Examples:

### Profile panel

Use:

- canonical face anchor;
- real profile reference when available;
- strongest front/3/4 references;
- locked nose/jaw/eye/mouth geometry.

### Smile panel

Use:

- canonical neutral anchor;
- actual smile references;
- locked eye/nose/jaw identity;
- calibrated smile-expression information.

### Body / pose panel

Use:

- canonical face anchor;
- body references appropriate for geometry;
- canonical body proxy when available;
- explicit pose contract;
- body proportion constraints;
- camera contract;
- contact and occlusion expectations;
- route-appropriate structural controls.

## Repair loop

A failed panel is repaired in isolation.

Default repair budget:

- initial generation;
- up to 2 targeted repair attempts.

After the route-local repair budget is exhausted:

1. determine whether evidence is missing or the generation capability is insufficient;
2. if evidence is adequate and a stronger route exists, escalate using `config/generation-routing.json`;
3. reset only the route-local repair budget for the stronger route;
4. if required evidence is missing, request the smallest targeted reference;
5. return `BLOCK` only when the evidence gap cannot be resolved in the current build or the required route ladder is exhausted.

Never loop indefinitely across routes.

## Cross-panel identity validation

Before deterministic composition:

1. compare approved panels using `schemas/cross-panel-identity-matrix.schema.json`;
2. include front ↔ 3/4, neutral ↔ expression, canonical face ↔ full-body face, and neutral body ↔ dynamic body comparisons when those panels exist;
3. reject any required pair with a BLOCK consistency result;
4. repair the drifting panel rather than averaging identities across the set.

## Deterministic composition

Only Approved panels may enter the final sheet.

Labels, panel borders, evidence-state badges, metadata, color chips, version information, and layout must be produced by deterministic composition, not by the image generator.

The reference implementation is:

`scripts/compose_sheet.py`

Input:

`sheet-manifest.json`

Output:

a self-contained `SVG` board.

A renderer may convert the SVG to PNG/PDF later, but the composition itself must remain deterministic.

## Final sheet QC

After composition, verify:

- no panel image was accidentally swapped;
- subject-left / subject-right labels match the panel;
- evidence-state labels are correct;
- reconstructed panels are visibly marked;
- metadata matches the canonical profile version;
- the composed board contains only Approved panels.

Composition does not re-evaluate identity; identity must already have passed per-panel QC.
