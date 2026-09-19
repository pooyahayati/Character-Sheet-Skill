# Changelog

All notable changes to Character Sheet Skill are documented here.

## [1.0.0] - 2026-09-20

First production-ready release.

### Identity
- Multi-view identity anchor bank.
- Independent facial-region identity gates.
- Natural asymmetry, distinctive features, smile/expression calibration.
- Evidence provenance, revision state, and lock state separated.

### Pose-ready production
- Canonical body proxy with SMPL-X/SMPL/3D skeleton/depth-normal/2D fallback representations.
- Pose difficulty ladder P0-P5.
- Pose readiness levels: Not-Ready, Basic, Strong, Production.
- Explicit pose, camera/lighting, contact, and occlusion contracts.
- Capability-based generation router with escalation ladder.

### Realism
- Physical plausibility and anatomy gate.
- Hand/foot identity profile.
- Skin identity independent from lighting.
- Hair static identity and dynamics.
- Clothing deformation contract.
- Cross-panel identity matrix.
- Photorealism and camera/lighting coherence gates.

### Quality and tooling
- Base / Advanced / Full level contract.
- 37 regression scenarios.
- JSON Schema validation for structured artifacts.
- Deterministic SVG character-sheet compositor.
- GitHub Actions validation.
- Installable ZIP packaging workflow.
