# Visual Benchmark Suite

## Purpose

Software/schema tests cannot prove that a generated person still looks like the same real person in difficult poses.

The visual benchmark is the production QA layer for pose-ready characters.

The normative suite is `config/visual-benchmark.json`.

## Four independent dimensions

Every benchmark image is evaluated on:

1. `Identity-Fidelity`
2. `Pose-Accuracy`
3. `Anatomical-Plausibility`
4. `Photorealism`

Do not average these into one score.

A blocking failure in Identity-Fidelity or Anatomical-Plausibility blocks the scenario.

## Scenario ladder

The suite covers P0 through P5:

- neutral full body;
- simple 3/4 standing;
- walking/weight shift;
- seated;
- self-occluding crossed arms;
- hand near face;
- deep bend/crouch;
- arms overhead;
- over-shoulder;
- low-angle full body.

## Benchmark references

Use only:

- fictional benchmark identities created for testing; or
- real identities with appropriate authorization.

Do not commit private user reference photos to this public repository.

## Photorealism dimension

Inspect:

- skin and lip texture;
- eyes/reflections;
- hair strands and hairline;
- teeth when visible;
- hands;
- cloth texture and deformation;
- shadows and contact shadows;
- depth consistency;
- camera/lens coherence;
- absence of obvious generative artifacts.

Photorealism cannot compensate for identity or anatomy failure.

## Result

Store results with `schemas/visual-benchmark-result.schema.json`.

A character reaches `Production` pose readiness only after the required benchmark scenarios pass according to `config/pose-readiness-contract.json`.

The current repository validates the benchmark configuration in CI. Actual image generation/evaluation remains an integration test and requires a connected image backend.
