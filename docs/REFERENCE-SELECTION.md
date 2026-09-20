# Reference Image Selection System

## Purpose

Large photo sets must be curated before identity extraction. More images can reduce quality when they are duplicates, distorted, filtered, outdated or contradictory.

## Structured record

Use staged records with `schemas/reference-analysis.schema.json`.

- Primary references: full analysis.
- Validation references: compact/delta analysis.
- Excluded references: minimal reason/status record.

Do not duplicate dozens of fields for every near-identical or excluded image.

## Multi-person images

If `person_count > 1`, resolve the target person before identity extraction.

Allowed target states:

- `User-Selected`;
- `Resolved-by-Context`.

If the target remains `Ambiguous`, the image must be `Excluded`. Do not guess based on prominence, gender presentation, clothing, or similarity alone.

## Pre-analysis normalization

Before image-level assessment, normalize references using `scripts/normalize_references.py` when available.

Normalization must address:

- EXIF orientation;
- decodability/corruption;
- RGB/sRGB-compatible conversion;
- oversized dimensions;
- JPEG/PNG normalization;
- exact and normalized hashes;
- duplicate grouping.

## Per-image assessment

After triage, evaluate Primary images fully for:

- focus;
- effective resolution;
- face pixel coverage;
- lighting/exposure;
- motion blur;
- occlusion;
- eye visibility;
- hair/hairline visibility;
- body visibility;
- hands/nails visibility;
- camera angle;
- pose usefulness;
- expression usefulness;
- lens/perspective distortion;
- likely beauty filter or heavy retouching;
- uniqueness;
- identity consistency;
- current-appearance relevance.

## Per-feature utility

Do not classify an image only as good/bad.

A single image may be:

```text
Face Geometry: Excellent
Eyes: Excellent
Hair: Good
Body Geometry: Poor
Hands/Nails: Not Available
```

Use each image only for the features it supports.

## Duplicate clustering

Detect exact and near-duplicate images and cluster similar shots.

Repeated frontal selfies must not overpower a single high-quality profile reference merely by count.

Choose the best representative(s) from each cluster.

## Coverage maps

Maintain coverage for:

### Face angles

- front;
- 3/4 subject-left;
- 3/4 subject-right;
- left profile;
- right profile;
- useful high/low angle references.

### Expressions

- neutral;
- soft smile;
- closed-mouth smile;
- open-mouth smile;
- serious/editorial;
- side gaze where useful.

### Body

- full-body front;
- side;
- back;
- 3/4;
- neutral stance.

Dynamic modeling poses can be useful for pose behavior but should receive lower weight for canonical body proportions.

### Details

- eyes;
- hair/hairline;
- mouth/lips;
- hands/nails;
- distinctive features.

## Distortion and misleading references

Flag images that can mislead geometry:

- close wide-angle selfies;
- extreme high/low camera angles;
- aggressive perspective;
- strong body posing;
- heavy beauty filters;
- reshaping filters;
- unusually heavy retouching;
- shape-altering clothing;
- old references with major appearance differences.

Do not necessarily discard them. Restrict them to features they can still support.

## Appearance epoch clustering

When images span different time periods or intentionally different looks, cluster them before resolving defaults.

Examples:

- old vs current hair;
- body-composition changes;
- eyebrow changes;
- facial-hair changes;
- makeup eras;
- cosmetic styling changes.

Use multi-epoch evidence for stable identity only where compatible. Never average mutable appearance into a fictional hybrid.

If the intended current/default epoch is ambiguous, ask one targeted question.

## Occluders and temporary appearance layers

Treat items that obscure or alter visible anatomy cautiously:

- glasses and glare;
- colored contacts;
- strong makeup;
- facial hair that obscures jaw/lips;
- hats/hair covering hairline;
- temporary swelling or transient skin changes.

An occluded feature receives lower confidence or uses another reference. The occluder itself may be stored as an editable appearance variant.

## Suspect synthetic/heavily edited references

If an image appears synthetic or strongly altered, label it `Suspect Reference` instead of asserting forensic certainty.

Reduce its identity weight. Exclude it when it conflicts with reliable photographic references.

## Reference conflicts

Detect conflicts such as:

- multiple hair colors;
- major hairstyle differences;
- visible weight/body changes;
- different eyebrow styling;
- substantially different makeup;
- old vs current appearance.

Separate stable identity from current editable appearance.

If a conflict affects a locked feature and cannot be resolved from evidence, ask the user a targeted question.

## Identity outliers

When one or more images appear inconsistent with the rest of the set, classify them as `Identity Outlier` and exclude them from canonical extraction unless the user resolves the conflict.

## Selection outputs

### Primary Reference Set

Smallest high-value set with strong independent coverage.

### Validation Pool

Useful images not used as primary anchors. Use them to catch overfitting and identity drift.

### Excluded Set

Unreliable, duplicate, overly distorted, heavily filtered or identity-inconsistent images.

## Reference Utility Score

An internal ranking may combine:

```text
Image Quality
+ Identity Reliability
+ Pose Utility
+ Expression Utility
+ Detail Visibility
+ Coverage Uniqueness
- Distortion Risk
- Filter Risk
- Duplication
```

Do not expose arbitrary numeric scores unless they help the user.

## Mandatory pre-generation Coverage Audit

Before any image generation, emit a structured Coverage Audit using `schemas/coverage-audit.schema.json`.

Generation is blocked when the requested evidence level lacks required coverage.

For Advanced, independent subject-left and subject-right non-frontal face evidence is required.

For Full, both-side non-frontal evidence plus observed profile coverage is required according to the level contract.

Do not silently reconstruct a missing required angle to avoid asking for a reference.

## Sufficiency detection

Stop asking for more references once the requested level has sufficient coverage.

If more evidence is needed, request the smallest targeted missing reference.

Example:

> Add one clear subject-right profile in even lighting. Current frontal and left-side coverage is already sufficient.

## Large-set user summary

For large inputs, report compactly:

- total reviewed;
- primary references;
- validation references;
- excluded images;
- face coverage;
- eye coverage;
- smile/expression coverage;
- profile coverage;
- body coverage;
- hands/nails coverage;
- exact missing references, if any.
