# Scenario Validation Suite

This suite tests the skill's decision logic before coupling it to any specific image-generation engine.

A scenario passes when the skill selects appropriate references, preserves uncertainty, chooses a justified sheet level, asks only targeted questions, and refuses to promote generated or ambiguous details into canonical identity.

## Gate outcomes

Every critical pre-generation gate returns one of:

- `PASS` — evidence is adequate for the requested operation.
- `PASS_WITH_LIMITS` — work may continue, but unsupported areas must remain Estimated, Reconstructed, Unverified, or omitted.
- `BLOCK` — the requested operation would compromise facial identity or evidence integrity; request a targeted reference.

A `BLOCK` on core face geometry, critical eye geometry, or unresolved identity conflict blocks canonical sheet generation.

---

## S01 — One excellent frontal portrait

**Input:** one sharp, evenly lit frontal portrait; no body reference.

**Expected:**

- face identity may pass;
- Base is appropriate;
- eyes, nose, lips, hairline and visible distinctive features may be Observed;
- body geometry remains Unverified;
- profile/back/body views are Reconstructed if generated;
- do not ask for hair color, eye shape, lip shape or other clearly visible attributes;
- request additional photos only if the user wants stronger profile/body coverage.

**Pass condition:** the system does not pretend the single photo supports Advanced/Full evidence.

---

## S02 — One close selfie with wide-angle distortion

**Input:** one close phone selfie with visible perspective distortion.

**Expected:**

- useful for eyes/skin/hair details if sharp;
- weak for canonical facial proportions;
- poor for body geometry;
- Face Identity Gate may be PASS_WITH_LIMITS or BLOCK depending on distortion;
- targeted request: a farther neutral frontal photo if geometry is unreliable.

**Pass condition:** distorted facial width/nose projection is not locked as canonical geometry.

---

## S03 — Twenty near-identical frontal selfies

**Input:** 20 clear selfies with nearly identical camera angle and expression.

**Expected:**

- duplicate clustering;
- small Primary Reference Set;
- remaining useful images move to Validation Pool;
- level is not Full merely because count is high;
- profile/body/expression coverage remains missing.

**Pass condition:** count cannot overpower coverage diversity.

---

## S04 — Eight diverse high-quality references

**Input:** front, both 3/4 views, one or both profiles, neutral body front/side, smile references.

**Expected:**

- strong Primary Reference Set;
- likely Advanced or Full depending on body/detail coverage;
- Face Identity Gate PASS;
- smile model calibrated only from actual smile images;
- left/right laterality verified where possible.

**Pass condition:** broad evidence raises the level for coverage reasons, not count alone.

---

## S05 — Mixed time periods and major appearance changes

**Input:** photographs spanning years, with different hair colors, body composition and eyebrow styles.

**Expected:**

- cluster references into appearance epochs;
- stable identity features may use multiple epochs;
- current/default appearance must come from an explicitly selected or inferable target epoch;
- if the intended default epoch is ambiguous, ask one targeted question;
- old body shape must not silently become current body geometry.

**Pass condition:** temporal appearance conflicts do not get averaged into a fictional hybrid.

---

## S06 — Same person plus one wrong-person image

**Input:** a consistent photo set plus one image of another person.

**Expected:**

- mark the inconsistent image as Identity Outlier;
- exclude it from canonical extraction;
- do not let it influence eyes, nose, smile or body;
- ask only if identity conflict cannot be resolved confidently.

**Pass condition:** one outlier cannot corrupt the canonical identity.

---

## S07 — Heavy beauty filter / face reshaping

**Input:** filtered selfies plus at least one unfiltered photo.

**Expected:**

- filter/reshaping risk flagged;
- filtered images may remain secondary for limited features;
- geometry should be anchored to the most reliable unfiltered reference;
- beauty-filter eye enlargement, skin smoothing or face slimming must not become Locked identity.

**Pass condition:** stylization is not mistaken for anatomy.

---

## S08 — Glasses, colored contacts or other occluders

**Input:** some photos with glasses/contacts; some without.

**Expected:**

- accessories and likely temporary appearance elements separated from core identity;
- glasses must not define eye geometry;
- colored-contact conflict prevents eye color from being locked unless resolved;
- glare-obscured eye details receive lower confidence.

**Pass condition:** occluders do not redefine underlying anatomy.

---

## S09 — Only smiling face references

**Input:** clear smiling portraits but no neutral face.

**Expected:**

- identity extraction may proceed where stable;
- neutral mouth/lower-face geometry remains less certain;
- smile behavior can be Observed;
- a canonical neutral face should be PASS_WITH_LIMITS or trigger a targeted neutral-reference request when high fidelity is required.

**Pass condition:** smile deformation is not frozen as neutral geometry.

---

## S10 — Neutral + closed smile + open smile

**Input:** high-quality references for all three.

**Expected:**

- smile calibration stores expression-specific deformation;
- visible teeth can be Observed/Cross-Validated;
- eye narrowing, cheek lift and mouth deformation are modeled jointly;
- base eye/nose/jaw identity remains stable across expressions.

**Pass condition:** each expression looks like the same person rather than separate similar people.

---

## S11 — Mirrored selfie with a one-sided mole

**Input:** mirrored selfie and a non-mirrored corroborating image.

**Expected:**

- resolve Subject Left/Right;
- marker location stored in subject coordinates;
- generated views keep marker on the correct anatomical side.

**Pass condition:** the mole does not flip across panels.

---

## S12 — Full-body photo shot from extreme low angle

**Input:** sharp full-body image with strong perspective.

**Expected:**

- useful for clothing or some visible details;
- poor for canonical leg/torso ratios;
- Camera Distortion Guard prevents locking stretched legs or altered torso proportions.

**Pass condition:** perspective is not treated as anatomy.

---

## S13 — Neutral body references plus modeling poses

**Input:** neutral front/side/back plus editorial poses.

**Expected:**

- neutral views define body geometry;
- editorial views define pose range;
- pose compression/hip rotation does not overwrite canonical proportions.

**Pass condition:** modeling behavior and anatomy remain separate.

---

## S14 — User edits hair color only

**Input:** approved v1.0; request changes black hair to another color.

**Expected:**

- Appearance Editable change only;
- minor version;
- face geometry, hairline, body and other locked attributes preserved;
- rerun relevant face/hair QC.

**Pass condition:** no identity drift from a trivial styling edit.

---

## S15 — User edits waist/chest/body shape

**Input:** approved identity; controlled body revision requested.

**Expected:**

- Body Revision Guard;
- change only requested dimensions/shape relationships;
- preserve face, height reference, unrelated shoulder/limb proportions unless requested;
- major version when structural change is substantial;
- resulting dimensions are Edited, not Observed.

**Pass condition:** body edit does not rewrite history or face identity.

---

## S16 — User provides exact height/measurements

**Input:** photos plus explicit user-provided height/body measurements.

**Expected:**

- exact values stored as User-Provided;
- visual geometry may be checked for consistency but must not overwrite the explicit values without user resolution;
- generated panels use those measurements as constraints when the engine supports them.

**Pass condition:** exact values have provenance and are not confused with image estimates.

---

## S17 — Hands/nails absent

**Input:** excellent face/body coverage but hands are cropped or hidden.

**Expected:**

- Full face/body may still be possible if the chosen Full definition allows missing optional detail;
- nails remain Unverified;
- do not invent a canonical nail shape/color;
- if nails are important to the user's target, request a targeted hand reference.

**Pass condition:** missing minor detail does not contaminate identity.

---

## S18 — Conflicting hair/eyebrow/makeup defaults in same session

**Input:** same person in several deliberately different looks.

**Expected:**

- underlying facial identity remains stable;
- each styling option may be stored as an appearance variant;
- default appearance must be selected rather than averaged;
- no question if the user's requested target look is already explicit.

**Pass condition:** appearance variation is modeled as variation, not identity conflict.

---

## S19 — Suspected synthetic or heavily edited reference

**Input:** one image appears AI-generated or substantially altered while others are photographic.

**Expected:**

- mark as Suspect Reference rather than claiming certainty of synthetic origin;
- reduce its identity weight;
- exclude it if it conflicts with reliable photographs.

**Pass condition:** the skill does not confidently assert an unreliable forensic conclusion.

---

## S20 — Successful Base upgraded later

**Input:** approved Base v1.0; later add profiles/body/smile references.

**Expected:**

- preserve the canonical approved identity;
- validate new evidence against it;
- upgrade coverage without resetting the person;
- contradictions trigger conflict resolution rather than silent overwrite.

**Pass condition:** Base → Advanced/Full is additive and version-aware.

---

# Regression requirements

Any future change to the skill should preserve these properties:

1. Face fidelity never becomes a lower-level tradeoff.
2. Photo count never substitutes for evidence diversity.
3. Generated outputs never become source evidence.
4. Temporary styling never silently becomes anatomy.
5. Expression deformation never silently becomes neutral geometry.
6. Camera perspective never silently becomes body proportion.
7. Subject Left/Right never depends on screen orientation alone.
8. Exact measurements always preserve provenance.
9. Structural edits remain edits, not rewritten observations.
10. A critical local face failure cannot be averaged away by global similarity.
