# Production Pipeline Contract

## Purpose

This document defines the actual production order for identity-faithful character sheets.

The skill must not ask an image model to create the final multi-panel board in one generation. Multi-panel generation makes identity drift, text errors, proportion drift, and inconsistent camera geometry much harder to detect and repair.

## Required production order

```text
Reference Intake
→ Reference Selection
→ Canonical Identity Profile
→ Canonical Face Anchor
→ Canonical Face QC
→ Individual Face Panels
→ Per-Panel Face QC
→ Individual Body Panels
→ Per-Panel Face + Body QC
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
3. create or select one canonical neutral face anchor;
4. validate it against the source references;
5. mark it Approved only after the critical Face Gates pass.

Downstream generated panels use the approved canonical face anchor plus the relevant original references.

The canonical face anchor is a production control asset. It is not new source evidence.

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

## Reference routing per panel

Every panel receives:

1. the canonical face anchor;
2. the minimal original references relevant to that panel;
3. canonical locked attributes;
4. the requested panel-specific pose/expression/camera instruction;
5. the explicit list of attributes that are allowed to change.

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

### Body panel

Use:

- canonical face anchor;
- body references appropriate for geometry;
- body proportion constraints;
- neutral camera constraints.

## Repair loop

A failed panel is repaired in isolation.

Default repair budget:

- initial generation;
- up to 2 targeted repair attempts.

After 3 total failed attempts on the same critical identity problem:

- do not keep regenerating blindly;
- return `BLOCK` for that panel;
- request the smallest missing reference or change backend strategy.

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
