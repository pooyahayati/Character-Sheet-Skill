# Multi-view Identity Anchor Bank

A single frontal anchor is not sufficient for reliable novel-view generation.

Use `schemas/identity-anchor-bank.schema.json` to maintain approved identity anchors for the views actually supported by evidence.

Preferred bank:

- neutral front;
- subject-left 3/4;
- subject-right 3/4;
- observed profile when available;
- eye detail;
- mouth detail;
- calibrated smile;
- body-front/side/back when body identity matters.

Only PASS or explicitly accepted PASS_WITH_LIMITS anchors may drive downstream production.

A reconstructed anchor must remain marked Reconstructed and must not silently become authoritative evidence.

For each new panel, choose the nearest relevant anchors rather than always forcing a frontal anchor.

## Cross-panel matrix

Use `schemas/cross-panel-identity-matrix.schema.json`.

Required comparisons should include, when panels exist:

- front ↔ left 3/4;
- front ↔ right 3/4;
- 3/4 ↔ profile;
- neutral ↔ smile;
- canonical face ↔ full-body face;
- neutral body ↔ dynamic body;
- left-side ↔ right-side outputs.

A panel set fails consistency when individually plausible panels collectively describe different face geometry, body shape, distinctive markers, or extremity identity.
