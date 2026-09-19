# Request and Goal Contract

## Rule

Determine the user's production goal before selecting a sheet level.

Do not automatically choose the highest level merely because the reference set can support it.

## Request normalization

Represent the request with `schemas/build-request.schema.json`.

Important fields:

- production goal;
- requested level: Auto / Base / Advanced / Full;
- details actually required for the job;
- intended appearance epoch when relevant;
- subject authorization;
- age handling.

## Level choice

If the user explicitly asks for Base, do not silently upgrade to Full.

If requested level is Auto, choose the smallest level that satisfies the requested production goal with adequate evidence.

If the requested level is unsupported, explain exactly which evidence is missing and offer the highest supported level without lowering facial fidelity.

## Group photographs

If a reference contains multiple people:

- never guess the target subject when ambiguous;
- use the image only after the target is unambiguously selected by the user or resolved from explicit context;
- otherwise classify the image as Excluded for identity extraction.

## Minimal questioning

Do not ask about details already visible and reliable.

Questions are justified when they resolve:

- target person in a group photo;
- target appearance epoch;
- required production detail;
- authorization ambiguity that blocks intended use;
- age ambiguity when a requested body edit or presentation requires adult confirmation.
