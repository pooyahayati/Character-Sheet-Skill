# Skin, Hair Dynamics, and Clothing Deformation

## Skin identity

Use `schemas/skin-identity.schema.json`.

Separate identity-relevant skin appearance from lighting.

Do not infer medical conditions.

Track only visible rendering cues such as tone reference, undertone reference, pores/texture, fine lines, freckles/marks, and regional pigmentation when observable.

Lighting changes must not redefine canonical skin appearance.

## Hair dynamics

Use `schemas/hair-dynamics.schema.json`.

Separate static hair identity from dynamic behavior.

Static identity:

- hairline;
- parting;
- length;
- texture;
- volume;
- default color.

Dynamic behavior:

- fall under gravity;
- interaction with shoulders;
- motion during head turn;
- tendency to occlude face.

Hair must not randomly change length, parting, texture, or volume across poses unless intentionally edited.

## Clothing deformation

Use `schemas/clothing-behavior.schema.json`.

Clothing must deform with pose without redefining the body underneath.

Examples:

- seated pose: compression/folds near hips and knees;
- bent elbow: sleeve compression;
- torso twist: diagonal fabric tension;
- raised arms: fabric lift/stretch.

Do not interpret garment folds, shaping garments, or compression as canonical body geometry.
