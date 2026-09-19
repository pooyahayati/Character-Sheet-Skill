# Gate Decision Contract

## Why this exists

`PASS`, `PASS_WITH_LIMITS`, and `BLOCK` must be reproducible decisions, not vague confidence labels.

This contract defines the minimum logical conditions for each gate.

## Identity fidelity vs evidence confidence

These are separate concepts.

### Identity Fidelity Standard

The minimum acceptable similarity/geometry standard for an identity-preserving panel.

This standard is constant across Base, Advanced, and Full.

### Evidence Confidence

How strongly the source references establish a feature or view.

Evidence confidence can be lower in Base and higher in Full.

Therefore:

> Base may contain more Reconstructed or Unverified information, but any panel presented as identity-preserving must still pass the same critical identity checks.

## Gate result model

Every gate returns:

- `result`: PASS | PASS_WITH_LIMITS | BLOCK
- `critical_checks`: named boolean/ternary checks
- `limitations`: unresolved non-critical items
- `evidence_used`: source reference IDs
- `reason`: compact explanation

## Critical face checks

The following checks are independently evaluated when visible/relevant:

- face silhouette / major geometry;
- left eye identity;
- right eye identity;
- eye spacing;
- nose geometry;
- neutral mouth/lip geometry;
- jaw/chin geometry;
- hairline when visible;
- subject laterality for one-sided features;
- distinctive feature placement when source-supported.

A critical region may be `NOT_EVALUABLE` only when the requested panel does not expose it sufficiently.

## PASS

Return PASS only when:

1. every critical region visible in the requested panel is evaluable;
2. every evaluable critical region passes;
3. no unresolved identity conflict exists;
4. panel laterality is correct;
5. panel evidence state is correctly labeled.

## PASS_WITH_LIMITS

Return PASS_WITH_LIMITS only when:

1. all visible critical identity regions pass;
2. identity is usable;
3. one or more non-critical or unsupported attributes remain Estimated, Reconstructed, Unverified, or omitted.

Examples:

- nails unavailable;
- exact eye color uncertain because of lighting;
- back hair detail reconstructed;
- body proportions unavailable in a face-only Base sheet.

PASS_WITH_LIMITS must not be used to hide a failed eye, nose, lip, jaw, or other critical identity region.

## BLOCK

Return BLOCK when any of the following applies:

- core face geometry cannot be established reliably;
- either eye identity materially fails;
- nose geometry materially fails in a face panel where it is visible;
- mouth/lip identity materially fails;
- jaw/chin identity materially fails;
- unresolved identity conflict exists between references;
- subject laterality for an identity marker is unresolved and the panel would present it canonically;
- a required reference is too distorted/occluded to support the requested canonical claim;
- a panel repeatedly fails identity QC after the repair budget.

## Advisory metrics

If the backend provides facial embeddings, landmarks, segmentation, or geometric measurements, use them as supporting signals.

Do not let one aggregate similarity score override a failed critical local check.

Do not hardcode universal numeric thresholds unless they have been calibrated for the specific backend and reference conditions.

## Gate aggregation

### Pre-generation Face Identity Gate

- PASS: canonical identity evidence is sufficient.
- PASS_WITH_LIMITS: canonical face can be established, but some optional/secondary attributes remain uncertain.
- BLOCK: critical facial identity cannot be established.

### Per-panel gate

- PASS: panel can enter Approved Panel Set.
- PASS_WITH_LIMITS: panel can enter only if its limitations are explicitly represented in metadata/evidence labels.
- BLOCK: panel cannot enter final composition.

### Final character-sheet result

The final sheet may be Approved only if every required panel is PASS or explicitly allowed PASS_WITH_LIMITS.

No BLOCK panel may appear in the final board.
