# Body Revision Guard

## Purpose

Body edits are controlled revisions to an approved character, not a re-estimation of the person's real body.

## Preconditions

Before a body edit:

1. load the approved canonical profile;
2. identify the exact requested body attributes;
3. record the pre-edit values/relationships;
4. determine age handling from the build request;
5. establish protected invariants.

## Protected invariants

Unless explicitly requested, preserve:

- face geometry and all Identity-Locked facial features;
- height reference;
- head-to-body relationship;
- shoulder width;
- limb-length relationships;
- hand/foot scale;
- posture baseline;
- unrelated chest/waist/hip relationships;
- distinctive identity features.

## Edit scope

Translate the request into the smallest possible set of editable attributes.

Examples:

- waist only;
- hip shape only;
- muscle definition only;
- overall silhouette;
- chest volume only for an Adult-Confirmed subject and neutral, non-sexualized presentation.

Do not infer or claim new real-world measurements after an edit.

Edited body attributes use:

- `revision_state: Edited`;
- `lock_state: Body-Editable`;
- provenance pointing to the revision request, not to the source photos as if the edit were observed.

## Age and sexualization guard

Do not infer adulthood from appearance alone.

If `age_handling` is `Minor` or `Unknown`:

- use conservative, age-appropriate clothing;
- do not perform edits intended to enlarge, emphasize, or sexualize breasts/chest, hips, buttocks, or other sexualized secondary characteristics;
- do not use erotic or seductive presentation.

General non-sexual edits such as neutral pose, clothing fit, or broad non-sexual silhouette adjustments may proceed only when appropriate and clearly non-sexual.

Edits involving sexualized secondary characteristics require `Adult-Confirmed`.

## QC after edit

Run:

1. face identity gates;
2. body geometry gate;
3. protected-invariant comparison;
4. full-body face fidelity;
5. requested-change verification.

A body revision fails if unrelated protected geometry changes materially.

## Versioning

A cosmetic/minor body adjustment may increment a minor version when it does not materially redefine the canonical silhouette.

A substantial structural body revision increments the major version.

Always record parent version, changed attributes, previous values, new values, and QC result.
