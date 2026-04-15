# Image Folder Guide

This repository stores production image sources only. Concept images and archived references live in the separate private repository `yboucher97/opticable-website-concepts`.

## Production

- `production/`
  Live-site image sources only.
  If `sitegen.py` uses an image, it should come from here or from `assets/`.

## Promotion rule

Do not point `sitegen.py` at concept or archive material.

When a concept image becomes a winner:

1. Move or copy it into `production/`.
2. Update `sitegen.py`.
3. Rebuild the site.
