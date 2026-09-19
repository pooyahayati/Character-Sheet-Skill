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

Compare normalized proportions to the canonical fingerprint.

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
