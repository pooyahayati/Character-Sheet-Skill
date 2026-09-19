# Privacy, Authorization, and Age Handling

## Scope

This skill works with photographs of real people and can create reusable identity assets. Treat source images and derived identity profiles as sensitive project data.

## Authorization

Before creating a reusable real-person identity asset, the build request records one of:

- `Self`;
- `Authorized-by-Subject`;
- `Licensed-or-Permitted`;
- `Unknown`.

If authorization is `Unknown`, ask the user to confirm they have the right or permission to use the images before producing a reusable final identity package.

Do not infer consent from the photographs themselves.

## Age

Do not infer exact age or adulthood from appearance alone.

Use:

- `Adult-Confirmed`;
- `Minor`;
- `Unknown`.

When age is Minor or Unknown, follow the conservative presentation and body-edit restrictions in `docs/BODY-REVISION-GUARD.md`.

## Data minimization

Use only the images needed for the requested identity task.

Do not copy user source photographs into the public skill repository.

Do not include raw source photos in example assets, documentation, test fixtures, or commits.

Generated example assets must be fictional/non-user-specific.

## Derived data

Character profiles may contain distinctive marks, body proportions, and other identifying visual information.

Keep provenance and uncertainty explicit. Do not infer sensitive traits such as health, ethnicity, religion, sexual orientation, or other sensitive attributes from appearance.

## Public output

Before publishing or sharing a reusable identity package, ensure that authorization is not Unknown and that the user understands which generated assets and structured identity data are included.
