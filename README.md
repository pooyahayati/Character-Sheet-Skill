# Character Sheet Skill

A reusable AI skill for building identity-consistent, revision-ready character sheets from real photographs.

![Base, Advanced, and Full character-sheet reference](assets/character-sheet-levels-example.svg)

The bundled preview is a fictional visual template. It communicates output structure, not evidence about any real person.

The skill is designed around a strict principle:

> Character-sheet depth and evidence confidence may change, but the minimum facial identity acceptance standard must not be downgraded.

It can start from a single usable photograph, scale to large photo sets, automatically select the most useful references, build a structured identity profile, generate Base / Advanced / Full character sheets, and keep later edits from unintentionally redefining the person.

## What this skill is designed to preserve

- Face geometry and facial proportions
- Left/right eye identity, eyelids, iris appearance, brow-eye relationship and natural asymmetry
- Nose, jaw, lips and mouth geometry
- Smile behavior when supported by reference images
- Hairline and default hair characteristics
- Distinctive visible features such as moles, freckles, scars or dimples
- Body proportions and shape within the limits supported by the references
- Subject-left vs subject-right feature placement
- Identity consistency across poses, expressions, camera angles and revisions

## Core workflow

```text
Start
→ Show expected character-sheet preview
→ Collect one or more photos
→ Reference Image Selection System
→ Automatic visual analysis
→ Face Identity Gate
→ Coverage analysis
→ Select Base / Advanced / Full
→ Build Canonical Character Identity
→ Create Sheet Plan
→ Approve Canonical Face Anchor
→ Generate panels individually
→ Per-panel multi-gate quality control
→ Repair failed panels only
→ Deterministic composition
→ User approval
→ Approved Character v1.0
→ Revision / Expansion / Level Upgrade
```

## Visual output standard

The production layout and panel hierarchy are defined in:

- `docs/VISUAL-STANDARD.md`
- `docs/LEVEL-SPECS.md`
- `examples/sheet-layout-spec.json`

The canonical face is always the strongest visual anchor. Modeling poses are secondary. Reconstructed or estimated information must never be visually presented as directly observed evidence.

## Build request and level choice

The skill normalizes the production goal before selecting a level. Explicit Base / Advanced / Full requests are respected when supported; Auto selects the smallest sufficient level.

The normative level rules live in `config/level-contract.json`.

## Character-sheet levels

### Base

For limited but usable reference coverage. A good facial reference is mandatory.

Typical output includes the strongest supported facial views, close-up face and eye references, basic body reference, default hair, color palette, observed attributes, editable defaults and uncertainty labels.

### Advanced

For broader multi-angle reference coverage.

Adds stronger left/right angle coverage, better profile reconstruction, full-body views where supported, improved body geometry, hair details, expression references and hand/nail information when visible.

### Full

For broad, high-quality reference coverage with low uncertainty.

Adds comprehensive face-angle coverage, expression and smile calibration, full-body front/side/back references, distinctive-feature mapping, detailed body-proportion references, hair, hands/nails and a richer reusable identity profile.

**Important:** the number of photos alone never determines the level. Coverage, reliability, diversity and image quality do.

## Reference Image Selection System

When many images are provided, the skill does not treat every image equally. It:

- scores image quality and identity reliability;
- detects near-duplicates;
- clusters face angles and expressions;
- maps body/detail coverage;
- detects heavy filters, distortion and misleading perspectives;
- separates current appearance from older or conflicting appearance;
- identifies identity outliers;
- chooses a Primary Reference Set;
- retains useful remaining images as a Validation Pool.

A photograph can be excellent for eyes but unsuitable for body proportions. Utility is evaluated per feature, not only per image.

## Identity model

The character profile separates:

- `Identity Locked` — core identity features;
- `Appearance Editable` — hair color/length/style, nails, makeup, clothing and similar appearance variables;
- `Body Editable` — controlled body-shape edits that require stronger consistency checks.

The internal identity representation includes:

- Face Geometry Core
- Facial Proportion Fingerprint
- Natural Asymmetry
- Eye Identity
- Mouth & Lip Identity
- Smile / Expression Model
- Distinctive Feature Map
- Hair Identity
- Body Geometry
- Editable Appearance

## Attribute state model

Every extracted attribute keeps three independent dimensions:

- evidence basis: `Observed`, `Cross-Validated`, `Estimated`, `Reconstructed`, `Unverified`, or `User-Provided`;
- revision state: `Original` or `Edited`;
- lock state: `Identity-Locked`, `Appearance-Editable`, `Body-Editable`, or `Unlocked`.

This allows a feature to be simultaneously, for example, `Cross-Validated` and `Identity-Locked`.

The skill must never turn an estimate into a fact merely because it appeared in a generated image.

## Minimal questioning

The skill analyzes the references before asking questions.

If a feature can be extracted and internally validated with sufficient confidence, it should not ask the user for that information. It asks only when the information is important and ambiguous, conflicting, unobservable or insufficiently supported.

## Face-first quality gates

A generated sheet is not accepted on global similarity alone. Independent gates verify:

- face geometry;
- facial proportions;
- eyes;
- nose;
- mouth and lips;
- smile behavior;
- jaw;
- hairline;
- distinctive features;
- natural asymmetry;
- body geometry;
- expression / pose consistency;
- full-body face fidelity.

A severe failure in a critical region cannot be hidden by a high overall similarity score.

## Body measurements and proportions

The skill may infer **relative visual proportions** from suitable references.

It must not claim exact real-world height, weight, chest, waist, hip or other physical measurements from ordinary photographs unless the user provides the measurement or the image has a trustworthy scale/calibration reference.

Camera distortion, focal length, pose and perspective must be considered before using an image for body geometry.

## Default character-sheet clothing

The default sheet uses minimal, neutral, anatomically readable, non-sexualized clothing that keeps body proportions visible without presenting the subject sexually.

## Revision-ready by design

The first approved sheet becomes the canonical base character.

Small appearance changes may create versions such as `v1.1`, while major structural changes may create `v2.0`. Later edits should change only the requested attributes, followed by identity and body consistency checks.

A Base sheet can later be upgraded to Advanced or Full as new references are supplied without rebuilding the identity from scratch.

## Privacy and body revisions

Real-person builds record authorization and age handling. Raw user photographs must not be committed to this public repository. Controlled body edits follow `docs/BODY-REVISION-GUARD.md`, including protected invariants and adult-confirmation requirements for sexualized secondary-characteristic edits.

See `docs/PRIVACY-CONSENT.md`.

## Production

The production path is explicitly panel-by-panel. The skill first approves a Canonical Face Anchor, then generates and validates each panel independently, and finally composes the approved panels deterministically.

See:

- `docs/PRODUCTION-PIPELINE.md`
- `docs/GATE-CONTRACT.md`
- `schemas/sheet-manifest.schema.json`
- `scripts/compose_sheet.py`

## Validation

Validation is executable in CI. `scripts/validate_repo.py` checks schemas, examples, cross-file reference integrity, the canonical level contract, group-photo exclusion behavior, and scenario uniqueness. The deterministic compositor is smoke-tested on every push and pull request.

The repository also includes a scenario-based regression suite covering single-photo intake, large duplicate sets, mixed time periods, identity outliers, filters, occluders, smile-only references, mirrored laterality, perspective distortion, modeling poses and revision workflows.

See:

- `tests/SCENARIO-VALIDATION.md`
- `tests/scenario-matrix.json`

## Repository structure

```text
SKILL.md
README.md
assets/
  character-sheet-levels-example.svg
docs/
  ARCHITECTURE.md
  QUALITY-CONTROL.md
  REFERENCE-SELECTION.md
  VISUAL-STANDARD.md
  LEVEL-SPECS.md
  EXAMPLE-SHEET-LAYOUT.md
  PRODUCTION-PIPELINE.md
  GATE-CONTRACT.md
config/
  level-contract.json
schemas/
  build-request.schema.json
  reference-analysis.schema.json
  character-profile.schema.json
  level-contract.schema.json
  sheet-plan.schema.json
  sheet-manifest.schema.json
  build-report.schema.json
scripts/
  compose_sheet.py
  validate_repo.py
examples/
  sample-build-request.json
  sample-reference-analysis.json
  sample-character-profile.json
  sample-sheet-manifest.json
  sheet-layout-spec.json
tests/
  SCENARIO-VALIDATION.md
  scenario-matrix.json
```

## Author

**Pooya Hayati | پویا حیاتی**

https://Pooyahayati.com
