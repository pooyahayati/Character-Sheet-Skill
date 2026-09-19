# Quality Control

## Principle

Identity is multi-dimensional. Never approve a sheet using only one global face-similarity score.

Critical local failures override a strong global result.

## Gate outcomes

The normative gate logic is defined in `docs/GATE-CONTRACT.md`.

Each gate stores:

- result: `PASS` | `PASS_WITH_LIMITS` | `BLOCK`;
- named critical checks;
- limitations;
- evidence used;
- reason.

Do not collapse these states into one average score.

A critical local `BLOCK` cannot be cancelled by a good global score.

## QC gates

### 1. Global Identity Gate

Check overall recognizability against multiple references.

### 2. Face Geometry Gate

Check head silhouette, face width/height, jaw/chin and stable structure.

### 3. Facial Proportion Gate

Compare only proportions whose `measurement_context` is appropriate for the comparison.

Each stored facial proportion must record:

- source view;
- geometry validity;
- distortion risk;
- normalization method;
- source image.

Do not compare a three-quarter/profile-derived ratio directly to a frontal canonical ratio as though the camera geometry were equivalent.

Ratios with `geometry_validity: Invalid` cannot participate in canonical proportion QC. `Limited` ratios are advisory only.

### 4. Eye Gate

Validate each eye independently:

- shape;
- eyelids;
- eye-corner angles;
- brow-eye distance;
- iris appearance;
- natural asymmetry.

Ignore gaze differences unless gaze was part of the requested output.

### 5. Nose Gate

Check bridge, width, length, tip, nostril relationship and profile.

### 6. Mouth & Lip Gate

Check mouth width, lip proportions, cupid's bow, corners and profile.

### 7. Smile / Expression Gate

When only smiling references exist, explicitly check whether neutral lower-face geometry is actually supported. Do not infer a canonical neutral mouth solely by undoing a smile without marking uncertainty.



When smiling, validate coordinated deformation across:

- lips;
- cheeks;
- eyes;
- nasolabial area;
- visible teeth.

Do not treat neutral-face geometry drift as acceptable merely because the image is smiling.

### 8. Jaw / Chin Gate

Validate lower-face shape independently from expression.

### 9. Hairline Gate

Hair style may change. Hairline identity should remain stable unless intentionally edited.

### 10. Distinctive Feature Gate

Check identity markers and subject-left/right placement.

### 11. Natural Asymmetry Gate

Ensure the generator has not beautified away meaningful asymmetry.

### 12. Body Geometry Gate

Check supported proportions independently from pose.

### 13. Pose / Expression Consistency Gate

Confirm that requested pose, expression, gaze, head pose and camera changes have not altered identity.

### 14. Full-Body Face Fidelity Gate

Zoom/evaluate the face inside each full-body panel separately.

A convincing full-body composition does not compensate for facial drift.

### 15. Laterality Gate

Check subject-left and subject-right features, especially after selfie/mirror references.

### 16. Pose Accuracy Gate

Compare the generated panel against its pose contract:

- major joint configuration;
- head orientation;
- weight distribution;
- contact points;
- camera/view constraints.

### 17. Physical Plausibility / Anatomy Gate

Follow `docs/PHYSICAL-PLAUSIBILITY.md`. Check joint continuity, limb-length consistency, balance, contacts, hand/foot anatomy, and impossible interpenetration.

Critical anatomy failure is BLOCK.

### 18. Occlusion Gate

Validate explicit front/back ordering from the pose contract. Wrong self-occlusion is a structural failure.

### 19. Cross-Pose Identity Gate

Compare the person across neutral, dynamic, seated, self-occluding, and extreme poses. The body shape and facial identity must remain canonical under articulation.

### 20. Photorealism Gate

When production realism is part of the goal, inspect skin/hair/eye/teeth/hand/fabric rendering, lighting/shadows, contact shadows, depth coherence, camera coherence, and obvious generative artifacts.

Photorealism cannot compensate for identity or anatomy failure.

### 21. Cross-Panel Identity Consistency Gate

Use `schemas/cross-panel-identity-matrix.schema.json`.

Compare required panel pairs across view, expression, full-body framing, and pose. A set of individually plausible images fails if face geometry, body shape, distinctive markers, hair identity, or extremity identity drift across the set.

A BLOCK comparison prevents final composition.

### 22. Skin Identity Consistency Gate

Compare visible skin rendering to the canonical `skin-identity.json` while accounting for the lighting contract.

Do not treat lighting-induced shadows or color shifts as permanent skin identity changes.

### 23. Hair Dynamics Gate

Validate that pose/head-turn motion changes hair naturally while preserving static identity: hairline, parting, length, texture, color, and baseline volume.

### 24. Clothing Deformation Gate

Validate garment folds, stretch, compression, and lift against the clothing behavior contract.

Clothing deformation must not silently change canonical waist, hip, chest, shoulder, or limb geometry.

### 25. Camera / Lighting Coherence Gate

Validate each panel against its camera-lighting contract.

Check:

- perspective and foreshortening;
- head/body scale appropriate to focal class;
- crop and camera height;
- key-light direction;
- shadows/contact shadows;
- eye highlights;
- color bias.

Camera or lighting differences must not be misdiagnosed as identity drift.

## Camera distortion guard

Before validating body shape, evaluate:

- camera distance;
- likely focal distortion;
- viewpoint;
- foreshortening;
- body rotation;
- weight shift;
- pose-induced compression.

Do not compare raw pixel widths across incompatible camera conditions as if they were anatomy.

## Body measurement rule

Ordinary images support relative proportions, not exact physical measurements.

Exact height, weight, chest, waist, hip or similar measurements require:

- explicit user-provided values; or
- reliable scale/calibration evidence.

## Panel repair strategy

When one panel fails:

1. identify the failed gate;
2. preserve successful panels;
3. regenerate or edit only the failing panel;
4. rerun local gates;
5. rerun final global identity validation.

Use the repair budget in `docs/PRODUCTION-PIPELINE.md`: one initial attempt plus up to 2 targeted repairs. If the same critical identity failure persists, return `BLOCK`.

Do not regenerate the complete sheet to repair one panel.

## Validation Pool use

After primary generation, compare outputs to secondary references that were not generation anchors.

This helps detect overfitting to one photograph or one expression.

## Appearance-epoch consistency

Before approval, verify that mutable defaults (hair, brows, makeup, body state, facial hair and similar appearance layers) come from the intended appearance epoch and have not been averaged across incompatible periods.

## Occluder check

Verify that glasses, contacts, strong makeup, facial hair or other occluders have not been mistaken for underlying eye/face/lip/jaw geometry.

## Approval conditions

A sheet can be approved only when:

- Face Identity Gate passed before generation;
- critical eye/face/mouth gates pass;
- unsupported details remain labeled appropriately;
- full-body panels pass their own face checks;
- significant subject laterality is correct;
- body geometry is not based on obviously misleading references;
- no generated reconstruction has been promoted to evidence.

## User-facing QC summary

Keep it compact:

- selected level;
- identity status;
- high-confidence locked features;
- important reconstructed/estimated areas;
- unresolved uncertainties;
- any targeted reference that would materially improve the sheet.
