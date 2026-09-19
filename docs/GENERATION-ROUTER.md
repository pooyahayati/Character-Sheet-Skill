# Generation Router and Escalation Ladder

## Goal

Choose the weakest backend capability that can reliably satisfy the requested task, and escalate when identity or anatomy remains unstable.

Do not repeat the same failing generation strategy indefinitely.

## Route classes

### R1 — Identity Reference

Reference-conditioned portrait/view generation.

Use for:

- face portraits;
- modest view changes;
- P0/P1 work where body articulation is not demanding.

### R2 — Identity + 2D Pose

Use identity references plus explicit 2D pose/keypoints and camera control.

Use for:

- simple full-body pose;
- walking/weight shift;
- P1/P2 modeling.

### R3 — Identity + 3D Geometry

Use identity references with 3D skeleton, SMPL-X-like pose, depth, normal, segmentation, or equivalent structural controls.

Preferred for:

- sitting/leaning;
- self-occlusion;
- extreme articulation;
- difficult novel viewpoints;
- P3-P5.

### R4 — Identity-Preserving Local Edit

Use local editing/inpainting for:

- hair;
- nails;
- clothing;
- local body revision;
- isolated panel repair.

### R5 — Subject-Specific Adapter

Use a subject-specific adapter / LoRA / fine-tuned identity module when repeated production needs stronger identity consistency than zero-shot routes provide.

### R6 — Dedicated 3D / Avatar

Use when production requires repeatable arbitrary pose/view control and diffusion-only routing remains unstable.

## Escalation ladder

1. multi-reference identity-conditioned generation;
2. identity adapter + 2D pose/camera control;
3. 3D skeleton/depth/normal/SMPL-X-like control;
4. subject-specific adapter or fine-tuning;
5. dedicated 3D/avatar representation.

Escalate when:

- the same critical failure persists after the local repair budget;
- cross-pose identity consistency fails;
- P3-P5 anatomy repeatedly fails;
- occlusion ordering cannot be controlled;
- required camera/view geometry remains unstable.

## Routing rules

Never route P4/P5 full-body work to text-only or reference-only generation.

A backend lacking reference conditioning cannot produce an approved identity-faithful result.

A route must record required capabilities and why it was selected using `schemas/generation-route.schema.json`.

Backend names are implementation details. The skill routes by capability.
