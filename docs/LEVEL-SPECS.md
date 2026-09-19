# Base / Advanced / Full Output Specifications

## Shared rule

All levels share the same facial identity standard.

Level changes affect breadth of coverage, evidence depth and uncertainty — never the minimum acceptable face fidelity.

---

# Base

## Intended use

Create a reliable starting identity from limited but usable references.

## Minimum evidence target

- at least one strong face reference;
- enough facial detail to pass Face Identity Gate;
- body information optional.

## Required visual blocks

### Canonical Identity

- large neutral canonical face;
- front face;
- best supported 3/4 face;
- eye detail;
- mouth/lip detail;
- hairline/default hair reference.

### Body

If supported:

- one full-body front reference.

If not supported:

- omit or mark a generated body as Reconstructed.

### Metadata

- Character ID;
- Version;
- Base level;
- locked identity;
- editable appearance defaults;
- evidence states;
- uncertainty summary.

## Recommended sheet footprint

One compact board.

## Base must not pretend to know

- exact real-world measurements;
- unsupported profiles;
- back-view details;
- smile behavior without references;
- unseen dental details;
- unseen body details.

---

# Advanced

## Intended use

Create a production-ready character reference with useful multi-angle and body coverage.

## Evidence target

Prefer:

- strong front face;
- at least one independent 3/4 or profile reference;
- useful expression reference;
- useful body reference;
- better left/right coverage than Base.

## Required visual blocks

### Canonical Identity

Everything in Base, plus:

- 3/4 Subject Left;
- 3/4 Subject Right;
- at least one profile when support exists;
- eye left/right detail;
- mouth/lip detail;
- neutral vs smile comparison when calibrated.

### Body

Prefer:

- full-body front;
- side;
- optional back if supported;
- proportion summary.

### Details

When visible:

- hands/nails;
- distinctive feature map;
- hair detail.

### Metadata

Add:

- coverage summary;
- reconstructed regions;
- reference confidence;
- current appearance defaults.

## Recommended sheet footprint

One large board or two coordinated boards.

---

# Full

## Intended use

Create the canonical long-term visual identity reference for repeated production.

## Evidence target

Broad, reliable, diverse coverage with materially reduced uncertainty.

Typical useful evidence includes:

- front;
- both 3/4 views;
- profile coverage;
- expression/smile references;
- full-body front/side/back or equivalent reliable body information;
- key detail references.

Photo count alone is irrelevant.

Full is goal-aware: a missing optional detail does not block Full when that detail is irrelevant to the intended production use. Missing required details remain Unverified and trigger a targeted request only when necessary.

## Required visual blocks

### Face Master Board

- large canonical neutral face;
- front;
- 3/4 Subject Left;
- left profile;
- 3/4 Subject Right;
- right profile;
- eye identity;
- brows;
- nose reference;
- mouth/lips;
- smile states;
- hairline;
- distinctive feature map;
- natural asymmetry notes.

### Body Master Board

- front neutral;
- side neutral;
- back neutral;
- optional 3/4 neutral;
- relative proportion map;
- body geometry notes;
- hands/nails when relevant and supported;
- hair length/shape reference.

### Modeling / Expression Board

Controlled examples such as:

- Beauty Neutral;
- Soft Gaze;
- Editorial Neutral;
- Soft Smile;
- Confident;
- Serious;
- Side Gaze;
- Over-Shoulder.

This board is for pose/expression range, not for redefining identity.

### Metadata / Revision Board

- Character ID;
- Version;
- parent version;
- sheet level;
- canonical defaults;
- locked attributes;
- editable attributes;
- evidence coverage;
- unverified fields;
- revision history.

## Recommended footprint

A coordinated multi-board system.

---

# Upgrade behavior

## Base → Advanced

Do not rebuild from scratch.

Add new validated evidence and expand only unsupported or low-confidence areas.

## Advanced → Full

Retain canonical identity and approved version history.

Expand:

- face-angle evidence;
- smile/expression calibration;
- body coverage;
- detail coverage;
- confidence.

---

# Preview behavior

At skill startup, show a compact visual preview that communicates:

- what Base looks like;
- what Advanced adds;
- what Full adds;
- that facial identity fidelity remains constant across all levels.

The preview should be a fictional example or a clearly non-user-specific template.

Never imply that every uploaded photo set can support Full.
