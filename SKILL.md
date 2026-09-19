---
name: character-sheet-skill
description: Build an identity-consistent, revision-ready Base, Advanced, or Full character sheet from one or more real photographs. Automatically select useful references, preserve facial identity across angles and expressions, model eyes/lips/smile/distinctive features/body proportions, and support controlled versioned edits.
---

# Character Sheet Skill

## Mission

Create a reusable character identity from real photographs and turn it into a high-quality character sheet that remains stable across future poses, angles, expressions, styling changes and revisions.

Do not optimize only for an attractive image. Optimize for identity fidelity, provenance, controllability and future reuse.

## Non-negotiable rule

Character-sheet level controls coverage and detail depth. It must never reduce the facial identity standard.

If facial identity cannot be established reliably, do not produce a lower-quality identity. Request only the targeted reference needed to resolve the blocking uncertainty.

## 1. Start with an expectation preview

Before intake, show or generate a concise example of the expected character-sheet structure so the user understands the target output.

Follow the visual hierarchy in `docs/VISUAL-STANDARD.md` and the level definitions in `docs/LEVEL-SPECS.md`. The preview should compare Base / Advanced / Full while making clear that facial identity fidelity does not decrease in lower levels.

The preview should demonstrate, when applicable:

- face angles;
- full-body views;
- close-up face and eye references;
- hair;
- hands/nails;
- body/proportion notes;
- color palette;
- locked vs editable attributes;
- identity/profile metadata.

The preview is illustrative, not a promise that unsupported views are factual.

## 2. Accept one or many real photographs

Minimum input: one usable photograph.

Do not assume more photos always improve the result. Large collections must pass the Reference Image Selection System before identity extraction.

## 3. Run the Reference Image Selection System

For every input image, assess:

- focus and effective resolution;
- face pixel coverage;
- exposure and lighting;
- motion blur;
- occlusion;
- eye visibility;
- hair/hairline visibility;
- body visibility;
- hand/nail visibility;
- lens and perspective distortion;
- beauty filters or heavy retouching;
- camera angle;
- pose utility;
- expression utility;
- uniqueness vs near-duplicates;
- likely recency/current-appearance relevance;
- identity consistency with the rest of the set.

Classify each image per use case, not only globally. An image may be:

- excellent for eyes;
- good for face geometry;
- poor for body geometry;
- unusable for proportions.

Build:

1. `Primary Reference Set` — highest-value references used to establish the identity.
2. `Validation Pool` — secondary images used to verify generated results.
3. `Excluded Set` — images too unreliable, distorted, filtered, duplicate or identity-inconsistent for the requested use.

Never weight a feature merely by photo count. Weight by independent coverage and reliability.

### Coverage maps

Build internal coverage maps for:

- face angles;
- expressions;
- gaze;
- body angles;
- hands/nails;
- hair;
- distinctive details.

Detect missing coverage before asking for more photos.

## 4. Analyze before asking questions

Extract all reliably observable information first.

For every attribute record:

- `value`;
- `confidence`;
- `consistency`;
- `source_images`;
- `status`.

Allowed status values:

- `Observed`;
- `Cross-Validated`;
- `Estimated`;
- `Reconstructed`;
- `Unverified`;
- `User-Provided`;
- `Edited`;
- `Locked`.

Do not ask the user for information that the references already establish with sufficient confidence.

Ask only when a material feature is ambiguous, contradictory, unobservable or below the required confidence threshold.

## 5. Run the Face Identity Gate

This gate is mandatory for every level.

Establish the strongest supported canonical identity for:

- head/face silhouette;
- facial width/height relationships;
- eye placement;
- brow placement;
- nose geometry;
- mouth/lip geometry;
- jaw/chin;
- hairline;
- natural left/right asymmetry;
- distinctive visible features.

If these are not reliable enough for the requested output, ask for the smallest targeted reference that resolves the problem.

Do not lower the facial standard to make progress.

## 6. Maintain subject laterality

Distinguish `Subject Left` and `Subject Right` from left/right in the displayed image.

Account for mirrored selfies or flipped files before locking:

- moles;
- scars;
- eye asymmetry;
- brow asymmetry;
- hair parting;
- ear differences;
- tattoos or other localized marks.

If laterality cannot be resolved, mark the feature `Unverified` instead of guessing.

## 7. Build the Canonical Character Identity

### Face Geometry Core

Store stable facial geometry separately from expression.

Maintain a normalized `Facial Proportion Fingerprint` using relative ratios rather than invented real-world measurements.

Useful ratios include, when measurable:

- eye distance / face width;
- mouth width / face width;
- nose length / face height;
- eye width / interocular distance;
- brow-to-eye relationship;
- lower-face / full-face height.

### Natural Asymmetry

Do not beautify away meaningful natural asymmetry.

Record relevant differences between left and right eyes, brows, mouth corners, jaw, ears and other visible structures.

### Eye Identity

Track left and right eyes separately:

- width/height relationship;
- upper and lower eyelid shape;
- eye-corner angles;
- crease;
- iris appearance and approximate color when reliable;
- sclera visibility;
- brow-eye spacing;
- natural asymmetry.

Keep gaze direction separate from eye identity.

### Mouth & Lip Identity

Track:

- mouth width;
- upper/lower lip proportions;
- cupid's bow;
- lip contour;
- mouth corners;
- projection/profile;
- natural asymmetry.

Do not invent dental identity.

### Smile / Expression Model

Separate identity from deformation caused by expression.

When references support it, calibrate:

- neutral;
- soft smile;
- closed-mouth smile;
- open-mouth smile.

Smile validation must consider coordinated changes in:

- lips/mouth;
- cheeks;
- eyes;
- nasolabial area;
- visible teeth.

Dental features remain `Unverified` unless actually visible in references.

### Distinctive Feature Map

Record identity-relevant visible details such as:

- moles;
- freckles;
- scars;
- dimples;
- characteristic skin marks;
- unusual brow/hairline details;
- dental details only when observed.

Store position with subject laterality and confidence.

### Hair Identity

Separate:

- hairline;
- default length;
- default shape/texture;
- default parting;
- default color

from later editable hairstyle/color changes.

### Body Geometry

Infer only what the references legitimately support.

Track relative geometry such as:

- shoulder/hip relationship;
- torso-to-leg relationship;
- head-to-body relationship;
- waist/hip relationship;
- chest/waist/hip visual relationships;
- overall body shape.

Before using an image for body geometry, check camera perspective, focal distortion and pose.

Do not claim exact real-world height, weight or circumferences from an ordinary uncalibrated photograph.

When exact measurements are required, use user-provided measurements or trustworthy calibrated references.

## 8. Separate locked and editable attributes

### Identity Locked

Examples:

- face geometry;
- facial proportion fingerprint;
- eye geometry;
- nose;
- base mouth/lip geometry;
- jaw/chin;
- natural asymmetry;
- distinctive identity markers.

### Appearance Editable

Examples:

- hair color;
- hair length;
- hairstyle;
- nail color;
- nail style;
- makeup;
- clothing;
- accessories.

### Body Editable

Examples:

- controlled waist change;
- chest-volume change;
- hip change;
- muscle/softness change;
- overall body-shape adjustment.

Body edits require a Body Revision Guard and must not silently modify unrelated proportions or facial identity.

## 9. Select the character-sheet level

Choose the highest level supported by **coverage and reliability**, not raw image count.

### Base

Use when facial identity is reliable but coverage is limited.

Only lock observed/cross-validated facts. Mark unsupported generated views as `Reconstructed` or `Unverified`.

### Advanced

Use when references provide broader face-angle and body/detail coverage.

Prefer real multi-angle facial evidence and stronger profile support.

If smile consistency is important, require at least one useful smile reference before treating smile behavior as calibrated.

### Full

Use only when face, relevant expressions, body angles and important details have broad enough reliable coverage to reduce uncertainty materially.

Full means lower uncertainty and broader evidence, not merely a larger sheet.

## 10. Create the Sheet Plan

Plan only the panels supported or explicitly reconstructed by the available evidence.

Use `examples/sheet-layout-spec.json` as the machine-readable layout baseline. Keep the canonical face visually dominant, neutral body views ahead of modeling poses, and evidence-state labeling available for reconstructed/estimated content.

Possible panels:

- front face;
- 3/4 left;
- 3/4 right;
- left/right profile;
- full-body front;
- side;
- back;
- close-up eyes;
- close-up mouth/lips;
- smile reference;
- hair/hairline;
- hands/nails;
- color palette;
- body proportion notes;
- locked/editable metadata.

Visually distinguish or internally track observed references vs reconstructed panels.

## 11. Default clothing and presentation

Use minimal, neutral, anatomically readable, non-sexualized clothing.

Avoid sexualized posing or framing.

The purpose of the base sheet is to reveal useful proportions, not eroticize the subject.

If age is unclear or the subject may be a minor, use conservative age-appropriate neutral clothing and do not use revealing presentation.

## 12. Generate with independent controls

Keep these variables conceptually separate:

`Identity + Expression + Gaze + Head Pose + Body Pose + Camera`

A change in one must not silently redefine the others.

For modeling/editorial poses, support controlled variants such as:

- beauty neutral;
- soft gaze;
- editorial neutral;
- soft smile;
- confident;
- serious;
- side gaze;
- over-shoulder.

The pose/expression layer must be validated against the canonical identity.

## 13. Run multi-gate quality control

Do not accept the sheet based on a single global similarity score.

Run independent gates for:

1. Global Identity
2. Face Geometry
3. Facial Proportions
4. Eyes
5. Nose
6. Mouth & Lips
7. Smile / Expression
8. Jaw / Chin
9. Hairline
10. Distinctive Features
11. Natural Asymmetry
12. Body Geometry
13. Pose / Expression Consistency
14. Full-Body Face Fidelity
15. Subject Laterality

Critical local failures override a strong global score.

When a panel fails, repair that panel if possible rather than regenerating the entire sheet.

Use the Validation Pool to compare results against references not used as primary generation anchors.

## 14. Full-body face fidelity rule

A full-body image must pass a separate face check because a small face can lose identity even when the body image appears convincing.

Do not approve a full-body panel if the face has drifted.

## 15. Evidence integrity rule

Generated content is not new evidence.

A reconstructed profile/back view, invented teeth, inferred body measurement or generated distinctive detail must never be promoted to `Observed` merely because the generator produced it.

Only new user references or explicit user-provided facts can resolve unverified evidence.

## 16. User review

After internal QC passes, present the best sheet and a compact summary of:

- selected level;
- high-confidence locked identity;
- editable defaults;
- important estimates/reconstructions;
- remaining uncertainty, if any.

Do not burden the user with every internal score unless useful.

## 17. Versioned revisions

The approved first identity becomes `v1.0`.

Examples:

- hair-color change → `v1.1`;
- nail change → `v1.2`;
- major body-geometry revision → `v2.0`.

For each revision:

1. load the canonical identity;
2. modify only requested attributes;
3. preserve unrelated locked features;
4. rerun relevant local QC gates;
5. rerun final identity QC.

Never rebuild identity from scratch for a simple appearance edit.

## 18. Level upgrades

When new references are supplied later:

`Base → Advanced → Full`

Reuse the canonical identity and add newly validated evidence.

Do not discard the approved base without a reason.

## 19. Large photo-set summary

When many images are supplied, provide a concise summary after selection, for example:

- images reviewed;
- Primary Reference count;
- Validation Pool count;
- Excluded count;
- face coverage;
- eye coverage;
- expression/smile coverage;
- profile coverage;
- body coverage;
- hands/nails coverage;
- exact missing reference needed, if any.

Stop requesting more references once the desired level has sufficient coverage.

## 20. Accuracy and privacy discipline

Do not infer sensitive personal traits from appearance.

Do not label estimates as facts.

Do not claim perfect or error-free reconstruction.

The correct behavior under uncertainty is to preserve uncertainty, request targeted evidence when necessary, or keep the attribute unverified.
