# Mandatory intake visuals

Before requesting photos, show:

1. `assets/character-sheet-levels-example.svg` — what the output can look like;
2. `assets/reference-photo-guide.svg` — which source-photo angles are required/recommended for Base, Advanced, and Full.

The second guide is mandatory. It prevents users from discovering missing angle requirements only after generation has started.

# Visual Standard

## Purpose

This document defines how Character Sheet outputs should look and how visual structure communicates evidence, identity and editability.

The sheet is a production reference, not a glamour collage. Every layout decision should improve identity reading, proportion reading, comparison across views and future revision.

## Global canvas

Recommended master canvas:

- landscape orientation;
- modular grid;
- neutral light gray or warm gray background;
- generous negative space;
- no decorative textures behind the subject;
- no cinematic lighting that hides structure;
- no extreme depth of field;
- no perspective-heavy camera unless the panel explicitly demonstrates camera variation.

Recommended aspect ratios:

- Base: 4:3 or 3:2 landscape;
- Advanced: 16:10 or 3:2 landscape;
- Full: large landscape board or multi-board set using the same grid system.

## Visual hierarchy

The sheet should read in this order:

1. Canonical Face
2. Eye / Mouth / Smile details
3. Multi-angle face
4. Full-body geometry
5. Hair / hands / nails / distinctive details
6. Color palette
7. Metadata and editability state

The canonical face must always receive the highest visual priority.

## Canonical face panel

The canonical face panel is the visual anchor for the entire sheet.

Requirements:

- frontal or near-frontal neutral pose;
- even, soft studio light;
- neutral head tilt;
- direct or near-direct gaze;
- no exaggerated smile;
- no beauty filter;
- no stylization that alters anatomy;
- enough resolution to inspect eyelids, lip contour, brows, nose, jaw and distinctive features.

The canonical face panel should be larger than any single supporting face-angle panel.

## Eye detail panel

Eye details should show:

- both eyes together for spacing;
- left eye crop;
- right eye crop;
- brow-to-eye relation;
- eyelid crease and corner angles;
- iris appearance when reliable;
- natural asymmetry.

Avoid eye crops so tight that brow-eye spacing or orbital context disappears.

## Mouth / lip panel

Show:

- neutral mouth;
- lip contour;
- cupid's bow;
- mouth corners;
- lower/upper lip relationship.

If smile calibration is available, include it separately instead of mixing it with the neutral mouth reference.

## Smile panel

The smile panel should compare, when references support them:

- neutral;
- soft smile;
- closed-mouth smile;
- open-mouth smile.

The purpose is to document deformation while preserving identity.

Do not invent teeth or gum-line details when they are not visible in source references.

## Face-angle row

Preferred sequence:

1. Front
2. 3/4 Subject Left
3. Left Profile
4. 3/4 Subject Right
5. Right Profile

If an angle is reconstructed rather than observed, track that state in metadata.

Do not mirror one side to fake the opposite side.

## Full-body row

Preferred sequence:

1. Front neutral stance
2. Side neutral stance
3. Back neutral stance

Optional:

- 3/4 front;
- 3/4 back;
- modeling pose examples.

Canonical body views should use neutral stance before editorial/modeling poses.

## Body framing

For body-reference panels:

- camera around torso/waist height when practical;
- avoid close wide-angle framing;
- avoid extreme top-down or low-angle views;
- keep subject scale consistent across front/side/back;
- keep floor line and camera logic visually consistent;
- avoid pose compression that hides actual proportion relationships.

## Default clothing

Use minimal, neutral, non-sexualized clothing that makes anatomy readable.

Preferred properties:

- fitted;
- simple silhouette;
- solid neutral color;
- no large logos;
- no distracting textures;
- no push-up / shaping presentation;
- no seductive or erotic pose language.

For uncertain age, use conservative age-appropriate coverage.

## Modeling pose section

Modeling poses are secondary to canonical anatomy.

Recommended controlled examples:

- Beauty Neutral
- Soft Gaze
- Editorial Neutral
- Soft Smile
- Confident
- Serious
- Side Gaze
- Over-Shoulder

Each modeling pose must preserve:

- canonical face geometry;
- eye identity;
- mouth/lip identity;
- distinctive features;
- body proportion relationships.

## Metadata panel

The metadata panel should be compact and legible.

Recommended groups:

### Character

- Character ID
- Version
- Sheet Level
- Identity Status

### Appearance Defaults

- Skin appearance reference
- Eye color reference
- Hair color
- Hair length
- Hair style
- Nail color
- Nail shape
- Default makeup
- Default clothing

### Body

- Relative height category only if inferable or user-provided;
- shoulder / waist / hip relationships;
- torso / leg relationship;
- user-provided exact measurements when available.

### Evidence

- Observed
- Cross-Validated
- Estimated
- Reconstructed
- Unverified

### Editability

- Identity Locked
- Appearance Editable
- Body Editable

## Color palette

Keep a small palette for:

- skin reference;
- hair;
- eyes;
- nails;
- default clothing.

Color chips are reference aids, not colorimetric truth unless capture conditions are controlled.

## Distinctive Feature Map

Use simple callouts for:

- moles;
- freckles;
- scars;
- dimples;
- hairline features;
- brow irregularities;
- other identity-relevant visible markers.

Callouts must use Subject Left / Subject Right, not image-left / image-right.

## Evidence display rule

The visual sheet should not visually imply that reconstructed information is directly observed.

Recommended treatment:

- Observed / Cross-Validated: normal panel label;
- Reconstructed: add a small "Reconstructed" label;
- Estimated: add a small "Estimated" label;
- Unverified: do not present as canonical truth.

## Revision display

Revised sheets should show:

- current version;
- parent version;
- changed attributes;
- unchanged locked identity.

Small edits should not redesign the whole visual sheet.

## Consistency rules

Across every sheet:

- same person scale within comparable rows;
- same neutral background family;
- same label hierarchy;
- same ordering of face angles;
- same subject-left / subject-right convention;
- same canonical neutral reference;
- no auto-beautification;
- no face slimming, eye enlargement, nose refinement or symmetry correction unless explicitly requested as an edit.

## Failure conditions

A visually attractive sheet still fails if:

- eyes drift;
- lips change;
- smile creates a different identity;
- distinctive features move sides;
- profiles imply a different nose or jaw;
- full-body panels lose facial identity;
- body proportions change between neutral views;
- reconstructed details are presented as facts.


## Pose Readiness Board

When repeated full-body generation in varied poses is part of the production goal, include a diagnostic Pose Readiness Board.

Recommended diagnostics:

- P0 neutral full-body;
- P1 simple 3/4 standing;
- P2 walking / weight shift;
- P3 seated / leaning;
- P4 crossed arms or hand-near-face self-occlusion;
- P5 crouch / deep bend or arms overhead.

The board is diagnostic, not decorative. It should expose:

- identity drift across articulation;
- limb-length drift;
- joint plausibility;
- hand/foot failures;
- contact and occlusion errors;
- camera-induced proportion errors;
- loss of photorealism in difficult poses.

A failed diagnostic panel must remain excluded or visibly marked as failed; it must not be presented as proof of pose readiness.


## Multi-view Identity Anchor Bank

The final production asset should visually distinguish primary identity anchors from generated diagnostic/output panels.

When evidence supports them, maintain approved anchors for:

- front;
- subject-left 3/4;
- subject-right 3/4;
- observed profile;
- eye detail;
- mouth detail;
- calibrated smile.

A frontal anchor must not dominate every target view when a better side-specific anchor exists.

## Skin / Hair / Clothing realism

Neutral reference panels should preserve natural visible skin texture without beauty smoothing.

Hair should retain static identity across panels while moving plausibly with head pose and gravity.

Clothing should fold and stretch with pose, but must not visually redefine the underlying body.

## Camera / Lighting standard

Every production panel has an explicit camera/lighting state.

Neutral canonical views should prefer low-distortion camera logic and identity-neutral lighting.

Diagnostic perspective views may use high/low camera angles, but those perspective effects must not be interpreted as canonical anatomy.
