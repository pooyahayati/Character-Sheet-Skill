# Reference Image Selection System

## Purpose

Large photo sets must be curated before identity extraction. More images can reduce quality when they are duplicates, distorted, filtered, outdated or contradictory.

## Per-image assessment

Evaluate each image for:

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
