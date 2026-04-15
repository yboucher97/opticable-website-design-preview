# Repository Instructions

## Asset model

This repository is the production website source only. Concept previews and archived generated snapshots are stored in the separate private repository `yboucher97/opticable-website-concepts`.

- `assets/`
  Production runtime brand assets that are copied directly into the live build.

- `Images/production/`
  Production-only raw image sources used by `sitegen.py` for the live site.
  Only approved winners belong here.

- `dist/assets/`
  Generated output only. Never place source images here manually.

## Concept previews

Do not add concept previews, concept image candidates, or archived generated snapshots to this production repository.

Use `yboucher97/opticable-website-concepts` for:

- concept briefs and feedback
- concept preview builds
- generated candidates
- manual concept uploads
- selected concept assets
- archived generated site snapshots

## Default behavior

If the user asks for a new concept and does not specify a concept number, default to `concept-01`.

If the user asks for generated candidate images, manual concept files, or selected concept assets, work in the concept repository instead of this production repository.

## Promotion rules

When a concept asset becomes a winner for production:

1. Copy or move it into `Images/production/`.
2. Update `sitegen.py` to reference the new production path.
3. Rebuild the site.

Production folders should contain winners only.
