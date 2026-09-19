# Physical Plausibility and Anatomy Gate

## Purpose

An output can preserve facial identity and still fail as a realistic human image. Full-body and pose-ready panels therefore require an independent physical plausibility gate.

## Critical checks

When visible/relevant, evaluate:

- head/neck attachment;
- shoulder girdle continuity;
- elbow direction and plausible range;
- wrist continuity;
- hand structure and finger count/joints;
- spine and pelvis relationship;
- hip joint plausibility;
- knee direction and plausible range;
- ankle/foot continuity;
- limb-length consistency with the canonical body proxy;
- left/right scale consistency;
- center of mass / balance;
- foot-ground or body-object contacts;
- absence of impossible interpenetration;
- self-occlusion ordering;
- foreshortening consistent with camera;
- full-body face identity.

## Contact checks

If the pose contract declares a contact, verify it.

Examples:

- foot on floor;
- hand on knee;
- hip on chair;
- back against wall.

Floating or penetrating contacts are failures when they contradict the pose contract.

## Occlusion checks

Use explicit front/back expectations from the pose contract.

Examples:

- forearm in front of torso;
- hand in front of face;
- crossed front leg in front of rear leg.

Incorrect depth ordering is a pose/anatomy failure, not merely a visual preference.

## Hands

Hands are critical anatomy for P3-P5.

A hand failure includes:

- wrong finger count;
- fused fingers;
- impossible joint direction;
- inconsistent left/right hand scale;
- hand disconnected from wrist;
- implausible object/contact interaction.

## Gate behavior

A critical anatomy failure is `BLOCK` for a required pose panel.

Do not average anatomical failure away with a high identity or photorealism score.

When available, use 3D skeleton/depth/normal/segmentation as supporting controls and diagnostics.
