# Camera and Lighting Contract

Use `schemas/camera-lighting-contract.schema.json`.

Camera and lighting are independent production variables. They must not be allowed to redefine identity.

## Camera

Track:

- yaw / pitch / roll;
- camera height;
- subject-distance class;
- focal class;
- crop;
- perspective strength.

Wide or low-angle views may be production-valid but are weak evidence for canonical body proportions.

When comparing identity across panels, account for the camera contract before declaring geometry drift.

## Lighting

Track:

- lighting setup;
- key direction;
- contrast;
- color bias;
- identity neutrality.

Neutral identity references should prefer high identity-neutrality lighting.

Strong directional light can alter apparent jaw, nose, eye sockets, skin tone, and body contour. Do not lock those lighting effects into canonical identity.

## Photorealism

Lighting must remain physically coherent with:

- shadows;
- contact shadows;
- eye highlights;
- fabric response;
- hair highlights;
- environmental context.

Photorealism failure is independent from identity accuracy.
