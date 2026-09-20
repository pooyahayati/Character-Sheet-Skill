# Changelog

All notable changes to Character Sheet Skill are documented here.

## [1.1.0] - 2026-09-20

Real-world test hardening release.

### Intake and reference coverage
- Mandatory illustrated Base / Advanced / Full reference-photo guide before uploads.
- Subject height collected in the first-turn intake; exact height is never inferred from ordinary photos.
- Evidence Level separated from Layout Scope.
- Complete layout now requires deliberate front, both 3/4, and both profile coverage unless reconstructed panels are explicitly accepted.
- Advanced evidence now requires independent non-frontal coverage from both subject sides.
- Executable pre-generation Coverage Audit with exact targeted missing-reference requests.
- Silent Full → Advanced downgrade after generation start is prohibited.

### Efficiency
- Quick-Sheet is now the default user-facing delivery.
- Full Production-Package is opt-in / goal-driven.
- Reference analysis is staged: Full for Primary, Compact for Validation, Minimal for Excluded.
- Dependency-aware parallel generation groups are defined.
- Executable preflight generation-call / file-count / relative-compute estimator.

### Input reliability
- Added reference normalization for EXIF orientation, decoding, resizing, RGB normalization and duplicate hashing.
- Corrupt/unsupported inputs are flagged before generation.

### Output and quality
- Compositor now supports SVG, PNG, JPEG and PDF.
- Added lightweight linked-SVG mode plus embedded-image downscaling/compression.
- Added locale/RTL controls for Persian/Arabic layouts.
- QC gates now record whether assessment used metrics, human review, model visual review, or hybrid evaluation.
- Added integrated cross-file output-package validator.
- Regression suite expanded from 37 to 50 scenarios.

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
