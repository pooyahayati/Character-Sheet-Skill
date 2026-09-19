# Pose-Ready Character Contract

## Purpose

The Character Sheet is not only a presentation board. It is the visible interface to a reusable identity asset that must remain stable under new body poses, viewpoints, expressions, and camera conditions.

Pose readiness is tracked separately from the Base / Advanced / Full sheet level.

## Pose-readiness levels

### Not-Ready

Critical identity is unresolved or there is not enough body/pose evidence for controlled pose generation.

### Basic

Suitable for neutral and simple standing poses.

Requires:

- approved critical facial identity;
- at least neutral/simple body evidence when body output is required;
- no blocking failures in P0/P1 benchmark scenarios.

### Strong

Suitable for common standing, walking, and seated poses.

Requires:

- approved identity;
- body proxy with at least a usable skeleton;
- P0-P3 benchmark scenarios without blocking failures;
- body geometry and full-body face fidelity gates.

### Production

Suitable for demanding arbitrary-pose production.

Requires:

- approved identity;
- 3D body proxy or equivalent depth/normal geometry control;
- P0-P5 visual benchmark coverage;
- Physical Plausibility Gate;
- self-occlusion validation;
- cross-pose identity consistency.

A character can be Full but not Production Pose-Ready.

## Canonical 3D Body Proxy

Use `schemas/body-proxy.schema.json`.

The proxy is engine-neutral. Preferred representations, in descending structural power, are:

1. SMPL-X-compatible;
2. SMPL-compatible;
3. canonical 3D skeleton;
4. depth + normal proxy;
5. 2D skeleton only.

The proxy is a control asset, not evidence. It must never promote reconstructed anatomy to Observed.

Exact real-world body scale requires user calibration or a trustworthy calibrated reference.

## Pose difficulty

- `P0-Neutral`: neutral stance / A-pose-like reference.
- `P1-Simple`: simple standing, modest head/arm changes.
- `P2-Dynamic`: walking, weight shift, moderate asymmetry.
- `P3-Seated-Leaning`: sitting, leaning, strong pelvis/spine change.
- `P4-Self-Occlusion`: crossed arms/legs, hand near face, limbs hiding torso.
- `P5-Extreme-Articulation`: crouching, arms overhead, deep bend, unusual joint configuration.

Difficulty controls required generation capabilities and QC severity.

## Pose Readiness Board

When pose-ready production is part of the goal, add a diagnostic board with:

- neutral full-body front;
- side or 3/4;
- A-pose-like arm separation;
- walking/weight shift;
- seated;
- arms crossed;
- hand near face;
- crouching/deep bend;
- arms raised;
- over-shoulder turn.

These are diagnostic poses, not glamour poses. They expose identity drift, limb-length drift, joint failures, occlusion failures, hand errors, and camera-induced proportion changes.

## Required structured assets

A pose-ready package may include:

- canonical identity profile;
- canonical body proxy;
- pose contracts;
- depth/normal/segmentation controls when available;
- approved panel set;
- pose-readiness assessment;
- visual benchmark result.

Generated proxy assets remain production controls, not new source evidence.


## Source-of-truth separation

`Pose Contract` owns articulation, joint targets, contacts, and occlusion expectations.

`Camera and Lighting Contract` owns viewpoint, focal/perspective state, crop, and lighting.

Do not duplicate camera state inside the pose contract. The pose contract may require `Camera-Control` capability, but the camera values themselves live only in `camera-lighting-contract.json`.

The canonical multi-view anchor bank lives in `production_assets.identity_anchor_bank_file`, not in the pose-assets block.
