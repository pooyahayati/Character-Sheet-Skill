# Architecture

## Design goal

Build a reusable character identity from real photographs while keeping three concepts separate:

1. **Evidence** — what the user photographs actually establish.
2. **Canonical identity** — the stable representation derived from that evidence.
3. **Generated views** — outputs that may reconstruct unsupported angles but never become new evidence.

The system is face-first and uncertainty-aware.

## End-to-end pipeline

```text
Input
→ Reference Image Selection
→ Coverage Maps
→ Automatic Attribute Extraction
→ Face Identity Gate
→ Laterality Resolution
→ Canonical Character Identity
→ Level Selection
→ Sheet Plan
→ Canonical Face Anchor
→ Canonical Face QC
→ Individual Panel Generation
→ Per-Panel Multi-Gate QC
→ Repair Failed Panels
→ Approved Panel Set
→ Deterministic Composition
→ User Review
→ Approved v1.0
→ Revision / Expansion / Upgrade
```

## Canonical Character Identity

### Face Geometry Core

Stores stable structure independently from expression:

- head silhouette;
- face width/height relationships;
- jaw/chin;
- nose geometry;
- eye placement;
- mouth placement;
- hairline;
- facial proportion fingerprint.

### Facial Proportion Fingerprint

Use normalized ratios rather than invented physical measurements.

Examples:

- inter-eye distance / face width;
- eye width / inter-eye distance;
- nose length / face height;
- mouth width / face width;
- lower-face height / face height.

### Eye Identity

Store left and right eye independently:

- eyelid shape;
- width/height;
- eye-corner angles;
- crease;
- iris appearance;
- brow-eye relationship;
- sclera visibility;
- natural asymmetry.

Gaze is not identity.

### Mouth & Lip Identity

Store:

- mouth width;
- upper/lower lip proportions;
- cupid's bow;
- lip contour;
- mouth corners;
- profile/projection;
- asymmetry.

### Smile / Expression Model

Expression is deformation around a stable identity.

Calibrate only supported states:

- neutral;
- soft smile;
- closed-mouth smile;
- open-mouth smile.

Smile QC checks lips, cheek lift, eye narrowing, nasolabial behavior and visible dental information together.

### Distinctive Feature Map

Track visible identity markers with subject laterality:

- moles;
- freckles;
- scars;
- dimples;
- characteristic skin marks;
- hairline/brow details;
- observed dental details.

### Hair Identity

Separate stable/default reference from editable appearance:

- hairline;
- default parting;
- default length;
- default texture/shape;
- default color.

### Body Geometry

Store visual relationships supported by suitable images:

- head/body ratio;
- shoulder/hip relationship;
- torso/leg relationship;
- waist/hip relationship;
- chest/waist/hip visual relationship;
- overall shape.

Camera and pose effects must be evaluated before extracting body geometry.

## Attribute classes

### Identity Locked

Core facial and identity geometry.

### Appearance Editable

Hair, nails, makeup, clothing and accessories.

### Body Editable

Controlled changes to waist, chest, hips, muscle/softness or overall shape. Body edits use a Body Revision Guard.

## Attribute state model

Do not store evidence provenance, revision state, and editability in one status.

Each attribute has three independent dimensions:

### Evidence basis

`Observed`, `Cross-Validated`, `Estimated`, `Reconstructed`, `Unverified`, or `User-Provided`.

### Revision state

`Original` or `Edited`.

### Lock state

`Identity-Locked`, `Appearance-Editable`, `Body-Editable`, or `Unlocked`.

Generated imagery cannot promote an attribute to Observed or Cross-Validated.

## Sheet levels

Levels represent reference coverage and uncertainty, not artistic quality.

### Base

Reliable face identity with limited broader coverage.

### Advanced

Broader multi-angle facial evidence plus stronger body/detail coverage.

### Full

Broad reliable evidence for relevant face angles, expressions, body views and details with materially lower uncertainty.

A large photo count does not imply Full.

## Level upgrade

New references extend the existing canonical identity:

```text
Base → Advanced → Full
```

Do not restart identity extraction unless the existing canonical identity is found invalid.

## Revision model

The base character is versioned.

Small appearance edits increment a minor version. Major body-geometry or identity-intent changes increment a major version.

Each revision stores:

- parent version;
- requested changes;
- changed attributes;
- preserved locks;
- QC results.

## Default presentation

Use minimal, neutral, anatomically readable and non-sexualized clothing. The sheet should expose useful proportions without erotic framing.


## Production contract

Actual image production follows `docs/PRODUCTION-PIPELINE.md`.

The final board is composed from individually approved panels. Multi-panel board generation in a single image-model call is not an approved production path.

Gate decisions follow `docs/GATE-CONTRACT.md`.
