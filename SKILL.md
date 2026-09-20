---
name: character-sheet-skill
description: Build a photorealistic, identity-consistent, pose-ready Base, Advanced, or Full character sheet from real photographs. Select reliable references, preserve the same person across views, expressions, camera angles and body poses, model face/body/skin/hair/extremity identity, and support controlled versioned edits.
---

# Character Sheet Skill

## Mission

Create a reusable character identity from real photographs and turn it into a high-quality character sheet backed by a pose-ready canonical asset that remains stable across future poses, angles, expressions, camera conditions, styling changes and revisions.

Do not optimize only for an attractive image. Optimize for identity fidelity, provenance, controllability and future reuse.

## Non-negotiable rule

Character-sheet level controls coverage, evidence depth, and uncertainty. It must never reduce the minimum facial identity acceptance standard.

Do not confuse fidelity standard with evidence confidence:

- the identity-fidelity acceptance criteria stay constant across Base / Advanced / Full;
- the amount of source evidence and confidence may be lower in Base and higher in Full.

If facial identity cannot be established reliably enough to pass the critical gates, do not produce a lower-quality canonical identity. Request only the targeted reference needed to resolve the blocking uncertainty.

Use `docs/GATE-CONTRACT.md` as the decision contract.

## 1. Start with an expectation preview

Before intake, show two things:

1. the expected character-sheet output structure;
2. the illustrated reference-photo guide in `assets/reference-photo-guide.svg`.

The reference-photo guide is mandatory. For `Auto`, show the Base / Advanced / Full comparison. For an explicit level, emphasize that level while still explaining what additional coverage unlocks higher confidence.

Follow the visual hierarchy in `docs/VISUAL-STANDARD.md` and the level definitions in `docs/LEVEL-SPECS.md`. The preview should compare Base / Advanced / Full while making clear that facial identity fidelity does not decrease in lower levels.

Use `assets/character-sheet-levels-example.svg` as the bundled output preview and `assets/reference-photo-guide.svg` as the bundled intake/reference preview when a static reference is appropriate. If the environment supports generating a preview dynamically, it may generate an equivalent fictional example that follows the same layout and evidence rules.

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

## 2. Normalize the build request

Before choosing a level, normalize the user's actual production goal using `schemas/build-request.schema.json` and `docs/REQUEST-CONTRACT.md`.

Collect the first-turn intake in one compact step before deep image analysis.

Record:

- goal;
- requested evidence level: Auto / Base / Advanced / Full;
- layout scope: Auto / Compact / Complete;
- output mode: Quick-Sheet / Production-Package;
- budget mode: Economy / Balanced / Maximum-Fidelity;
- subject height in centimeters when known;
- if height is unknown, explicitly ask once and record `Asked-Unknown` rather than inferring it;
- details required for the production task;
- intended appearance epoch when relevant;
- subject authorization;
- age handling.

Do not infer height from ordinary photographs. For body or pose-ready work, ask for height at the beginning because it materially improves scale consistency.

Do not automatically choose the highest level available. If level is Auto, choose the smallest level that satisfies the production goal with adequate evidence.

For a reusable real-person identity package, follow `docs/PRIVACY-CONSENT.md`. If authorization is Unknown, resolve permission before final reusable output.

Do not infer adulthood from appearance. Body edits or presentation involving sexualized secondary characteristics require `Adult-Confirmed`; otherwise follow the conservative restrictions in `docs/BODY-REVISION-GUARD.md`.

## 3. Accept and normalize one or many real photographs

Minimum input: one usable photograph.

Before reference scoring or generation, normalize source files using `scripts/normalize_references.py` when executable tools are available:

- apply EXIF orientation;
- convert to a standard RGB/sRGB-compatible representation;
- verify image decoding;
- resize excessively large files to a controlled maximum dimension;
- normalize JPEG/PNG handling;
- compute exact and normalized hashes;
- flag corrupt or duplicate inputs.

If script execution is unavailable, perform the same checks conceptually and do not send obviously corrupt/misoriented source files to generation.

Do not assume more photos always improve the result. Large collections must pass the Reference Image Selection System before identity extraction.

## 4. Run the Reference Image Selection System

Represent per-image analysis using `schemas/reference-analysis.schema.json`.

Use staged analysis to control cost.

1. Triage all images cheaply for decodability, duplicate cluster, gross view, quality, and exclusion risk.
2. Run full feature-level analysis only on Primary references.
3. Use compact/delta analysis for Validation references.
4. Keep Excluded references minimal: reason + duplicate/outlier/corruption status.

For fully analyzed Primary images, assess:

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

If an image contains multiple people, do not guess the target. The target must be Single-Subject, User-Selected, or explicitly Resolved-by-Context. Ambiguous group images are Excluded from identity extraction until resolved.

### Coverage audit — mandatory before generation

After reference selection, create `coverage-audit.json` using `schemas/coverage-audit.schema.json`.

The audit must determine:

- requested level;
- highest evidence-supported level;
- layout scope;
- face-angle coverage;
- expression coverage;
- body coverage;
- hands/feet coverage;
- blocking gaps;
- non-blocking gaps;
- exact targeted reference requests.

No image generation may start while `generation_allowed=false`.

If an explicit Base / Advanced / Full target is missing required evidence, ask for the smallest targeted reference set before generating reconstructed substitutes.

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

### Appearance epochs and temporary occluders

When references span visibly different time periods or deliberately different looks, cluster them into `Appearance Epochs` or appearance variants instead of averaging them.

Stable facial identity may use evidence across epochs, but current/default hair, brows, makeup, body state and other mutable appearance must come from the intended target epoch.

If the target epoch is not inferable from the user's request or references, ask one targeted question.

Treat glasses, colored contacts, strong makeup, facial hair, temporary skin changes and similar occluders/appearance layers separately from underlying geometry when possible. Do not let an occluder redefine anatomy.

If a reference appears synthetic or heavily altered, mark it `Suspect Reference` rather than making a definitive forensic claim. Reduce its weight or exclude it when it conflicts with reliable photographs.

## 5. Analyze before asking questions

Extract all reliably observable information first.

For every attribute record, keep evidence, revision, and editability as separate dimensions:

- `value`;
- `confidence`;
- `consistency`;
- `source_images`;
- `evidence_basis`: Observed | Cross-Validated | Estimated | Reconstructed | Unverified | User-Provided;
- `revision_state`: Original | Edited;
- `lock_state`: Identity-Locked | Appearance-Editable | Body-Editable | Unlocked.

Never collapse these dimensions into one status field. A feature may simultaneously be Cross-Validated, Original, and Identity-Locked.

Do not ask the user for information that the references already establish with sufficient confidence.

Ask only when a material feature is ambiguous, contradictory, unobservable or below the required confidence threshold.

## 6. Run the Face Identity Gate

This gate is mandatory for every level.

Every critical gate returns one of:

- `PASS`;
- `PASS_WITH_LIMITS`;
- `BLOCK`.

The result must follow `docs/GATE-CONTRACT.md`, including named critical checks, evidence used, limitations, and a reason. Do not derive a gate result from one aggregate similarity score.

A `BLOCK` on core face geometry, either eye, mouth/lips, jaw/chin, or unresolved identity conflict blocks canonical sheet generation.

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

A clear smiling face may support identity, but smile deformation must not be frozen as neutral mouth/lower-face geometry. When high-fidelity neutral geometry is required and only smiling references exist, use `PASS_WITH_LIMITS` or request one neutral reference.

Do not lower the facial standard to make progress.

## 7. Maintain subject laterality

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

## 8. Build the Canonical Character Identity

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

### Hair Identity and Dynamics

Use `schemas/hair-dynamics.schema.json` and `docs/SKIN-HAIR-CLOTH.md`.

Separate static hair identity from pose-dependent behavior.

Static identity includes:

- hairline;
- default length;
- default shape/texture;
- default parting;
- default color;
- default volume.

Dynamic behavior includes:

- gravity response;
- shoulder interaction;
- motion during head rotation;
- tendency to occlude the face.

Do not let pose generation randomly change hair length, parting, texture, or volume unless explicitly edited.

### Skin Identity

Use `schemas/skin-identity.schema.json`.

Track visible rendering cues that materially affect identity realism, such as:

- tone reference;
- undertone reference;
- natural texture;
- regional pores/fine lines;
- freckles and visible marks;
- localized pigmentation.

Keep skin identity independent from lighting. Do not infer medical or other sensitive traits.

### Hand and Foot Identity

Use `schemas/extremity-profile.schema.json` and `docs/EXTREMITY-IDENTITY.md`.

When evidence exists, track left/right hands and feet separately. Hand/foot anatomy remains a critical realism check even when detailed identity evidence is unavailable.

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

### Canonical Body Proxy and Pose Readiness

When the production goal includes repeated full-body or modeling poses, build a canonical body control asset using `schemas/body-proxy.schema.json` and `docs/POSE-READINESS.md`.

Prefer the strongest representation the available evidence/backend supports:

`SMPL-X-Compatible → SMPL-Compatible → 3D Skeleton → Depth/Normal Proxy → 2D Skeleton`.

The proxy is a production control asset, not new evidence.

Track pose readiness independently from Base / Advanced / Full as `Not-Ready`, `Basic`, `Strong`, or `Production`.

A `Full` sheet is not automatically `Production` pose-ready.

## 9. Separate locked and editable attributes

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

Body edits must follow `docs/BODY-REVISION-GUARD.md` and must not silently modify unrelated proportions or facial identity.

Record previous value, new value, revision request, protected invariants, and post-edit QC.

## 10. Select evidence level and layout scope

Use `config/level-contract.json` as the normative level definition.

Choose the evidence level from the build request and Coverage Audit.

Keep two concepts independent:

- `Evidence Level`: Base / Advanced / Full — how strongly the source references support identity claims;
- `Layout Scope`: Compact / Complete — how broad the visual board is.

A Complete layout may contain reconstructed/limited panels while still being Advanced evidence. Never call it Full merely because the board looks complete.

Choose the level from the build request and evidence:

- if the user requested Base / Advanced / Full explicitly, honor that target when supported;
- if requested level is Auto, choose the smallest level that satisfies the production goal;
- if the requested level is unsupported, identify the exact missing evidence and offer the highest supported level.

Never choose a level from raw image count.

### Base

Use when facial identity is reliable but coverage is limited.

Only lock observed/cross-validated facts. Mark unsupported generated views as `Reconstructed` or `Unverified`.

### Advanced

Use when references provide broader multi-angle coverage.

Require independent subject-left and subject-right non-frontal facial references for multi-angle approval. Do not reconstruct the missing opposite 3/4 as if Advanced evidence were complete.

Prefer stronger observed profile support.

If smile consistency is important, require at least one useful smile reference before treating smile behavior as calibrated.

### Full

Use only when face, relevant expressions, body angles and the details that matter to the intended use have broad enough reliable coverage to reduce uncertainty materially.

Full means lower uncertainty and broader evidence, not merely a larger sheet.

Optional details such as hands/nails do not automatically block Full when they are irrelevant to the requested use. Keep them Unverified or request a targeted reference only when they are required by the user or production goal.

## 11. Create the preflight plan and Sheet Plan

Before generation, create `preflight-plan.json` using `schemas/preflight-plan.schema.json`.

Tell the user, compactly:

- planned panel count;
- estimated generation-call range;
- estimated output-file range;
- relative compute level;
- repair budget;
- which panels can run in parallel;
- wall-clock estimate only when backed by measured backend history;
- monetary estimate only when backend pricing is actually available.

Do not fabricate time or currency estimates.

Then plan only the panels supported or explicitly reconstructed by the available evidence.

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

For any pose-dependent panel, create a `Pose Contract` using `schemas/pose-contract.schema.json`. Record pose difficulty, joint targets, required contacts, occlusion ordering, and required structural controls.

Create a separate `Camera and Lighting Contract` using `schemas/camera-lighting-contract.schema.json`. Camera and lighting are production variables, not identity.

When clothing is visible in body/pose panels, use `schemas/clothing-behavior.schema.json` so garment deformation follows pose without redefining canonical body geometry.

## 12. Default clothing and presentation

Use minimal, neutral, anatomically readable, non-sexualized clothing.

Avoid sexualized posing or framing.

The purpose of the base sheet is to reveal useful proportions, not eroticize the subject.

If age is unclear or the subject may be a minor, use conservative age-appropriate neutral clothing and do not use revealing presentation.

## 13. Generate with independent controls

Follow `docs/PRODUCTION-PIPELINE.md`.

Do not generate the entire multi-panel character sheet in one image-model call.

Production order must be panel-based and dependency-aware. Independent approved panel groups should be generated in parallel when the execution environment supports parallel calls.

Production order:

1. establish and approve a Multi-view Identity Anchor Bank using `schemas/identity-anchor-bank.schema.json`;
2. select the nearest relevant approved anchor(s) for each target view instead of always forcing a frontal anchor;
3. generate/edit each face, body, detail, expression, and modeling panel independently;
4. run per-panel QC;
5. repair failed panels in isolation;
6. build the Cross-panel Identity Matrix;
7. compose only Approved and cross-panel-consistent panels using deterministic layout.

A production backend must support reference-conditioned generation or editing. If it cannot condition on the user's references, the skill may create a plan but must not approve the result as identity-faithful.

Route each panel using `docs/GENERATION-ROUTER.md`, `config/generation-routing.json`, and `schemas/generation-route.schema.json`.

For P3-P5 body poses, prefer 3D/depth/normal/SMPL-X-like structural control. Never treat text-only or reference-only generation as sufficient for demanding self-occluding/extreme body poses.

When repeated critical failures persist, escalate capability rather than repeating the same route. Apply the repair budget per route; return BLOCK only after a required evidence gap is identified or the appropriate escalation path is exhausted.

Keep these variables conceptually separate:

`Identity + Expression + Gaze + Head Pose + Body Pose + Camera + Lighting + Clothing Deformation + Hair Dynamics`

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

## 14. Run multi-gate quality control

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
16. Pose Accuracy
17. Physical Plausibility / Anatomy
18. Occlusion Ordering
19. Hand / Foot Anatomy when visible
20. Cross-Pose Identity Consistency
21. Photorealism
22. Cross-Panel Identity Consistency
23. Skin Identity Consistency
24. Hair Dynamics Consistency
25. Clothing Deformation
26. Camera / Lighting Coherence

Critical local failures override a strong global score.

When a panel fails, repair that panel rather than regenerating the entire sheet.

Use the repair budget in `docs/PRODUCTION-PIPELINE.md`. Respect the user's budget mode; do not automatically spend the maximum repair budget in Economy/Quick-Sheet mode. Repeated critical failure becomes `BLOCK` and requires better evidence or a different backend strategy.

Use the Validation Pool to compare results against references not used as primary generation anchors.

After all required panels pass local QC, build `schemas/cross-panel-identity-matrix.schema.json`. Required pairwise comparisons must verify that the approved panel set still represents one consistent person across view, expression, camera, and pose changes. A BLOCK pair prevents final composition.

Full-body and pose-ready panels must also follow `docs/PHYSICAL-PLAUSIBILITY.md`. Critical anatomy or contact failures are BLOCK even when face identity is strong.

## 15. Full-body face fidelity rule

A full-body image must pass a separate face check because a small face can lose identity even when the body image appears convincing.

Do not approve a full-body panel if the face has drifted.

## 16. Evidence integrity rule

Generated content is not new evidence.

A reconstructed profile/back view, invented teeth, inferred body measurement or generated distinctive detail must never be promoted to `Observed` merely because the generator produced it.

Only new user references or explicit user-provided facts can resolve unverified evidence.

## 17. Deterministic composition

After all required panels are Approved, compose the final board deterministically.

Do not ask the image model to render labels, metadata, borders, evidence badges, or the final multi-panel layout.

Use:

- `schemas/sheet-manifest.schema.json`
- `scripts/compose_sheet.py`

The final composition may contain only PASS or explicitly allowed PASS_WITH_LIMITS panels. BLOCK panels are forbidden.

Package approved outputs according to `docs/OUTPUT-CONTRACT.md`, including the build request, reference analysis, canonical profile, optional body proxy, pose contracts, pose-readiness assessment, sheet plan, approved panel assets, composition manifest, final SVG, visual benchmark result when run, and build report.

## 18. Pose-ready visual benchmark

When the goal requires reusable production across varied poses, run the benchmark defined in `config/visual-benchmark.json` and `docs/VISUAL-BENCHMARK.md`.

Evaluate each required scenario independently on:

- Identity-Fidelity;
- Pose-Accuracy;
- Anatomical-Plausibility;
- Photorealism.

Do not average a failed dimension away. A blocking identity or anatomy failure blocks that benchmark scenario.

Store results using `schemas/visual-benchmark-result.schema.json` and derive pose readiness using `config/pose-readiness-contract.json`.

## 19. User review

After internal QC passes, present the best sheet and a compact summary of:

- selected level;
- high-confidence locked identity;
- editable defaults;
- important estimates/reconstructions;
- remaining uncertainty, if any.

Do not burden the user with every internal score unless useful.

## 20. Versioned revisions

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

## 21. Level upgrades

When new references are supplied later:

`Base → Advanced → Full`

Reuse the canonical identity and add newly validated evidence.

Do not discard the approved base without a reason.

## 22. Large photo-set summary

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

## 23. Accuracy and privacy discipline

Do not infer sensitive personal traits from appearance.

Do not label estimates as facts.

Do not claim perfect or error-free reconstruction.

The correct behavior under uncertainty is to preserve uncertainty, request targeted evidence when necessary, or keep the attribute unverified.
