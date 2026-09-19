# Base / Advanced / Full Output Specifications

The normative machine-readable level contract is:

`config/level-contract.json`

This document explains that contract. If wording here conflicts with the JSON contract, the JSON contract wins.

## Shared rule

All levels use the same critical facial identity acceptance standard.

Levels change evidence breadth, supported claims, and uncertainty.

## Base

Base requires a usable front or near-front face that can pass the critical Face Identity Gate.

Required sheet content:

- canonical face;
- eye detail;
- mouth/lip detail;
- hair reference;
- metadata;
- color palette.

A 3/4 view, profile, body panel, smile panel, or distinctive-feature panel is conditional. Do not require a 3/4 reference merely to create Base.

Unsupported generated angles are Reconstructed, not Observed.

## Advanced

Advanced requires:

- a usable front/near-front reference;
- at least one independent non-frontal face reference.

Both 3/4 output panels may be generated for production utility, but any side that is not directly supported must be labeled Reconstructed.

Body is conditional on the production goal. Do not require a body reference for a face-only Advanced request.

Expression/smile evidence is required only when expression or modeling behavior is part of the goal.

## Full

Full is the canonical long-term level for the requested goal.

For face coverage it requires:

- front/near-front evidence;
- independent subject-left non-frontal evidence;
- independent subject-right non-frontal evidence;
- at least one observed profile.

When expressions/modeling are required, Full additionally needs neutral plus at least one useful non-neutral expression reference.

When body is required, Full needs at least body-front and side evidence. A back view may be reconstructed, but it cannot be claimed as canonical observed evidence without an observed back reference.

Hands/nails are required only when relevant to the production goal.

## Upgrade behavior

Upgrades add validated evidence to the approved canonical identity.

`Base → Advanced → Full`

Do not rebuild the person from scratch.

## Goal-aware selection

If the user requests a specific lower level, honor it.

If the requested level is `Auto`, choose the smallest level that satisfies the production goal with adequate evidence.

If a requested higher level is unsupported, identify the exact missing evidence and offer the highest supported level without lowering facial identity fidelity.
