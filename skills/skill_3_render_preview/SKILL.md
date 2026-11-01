---
name: skill_3_render_preview
description: >-
  Headless multi-view PNG/SVG previews from part STL/DXF inside Docker.
  Reads parts/$PART/views.py; writes output/$PART/previews/.
---

# Render Preview Workflow

Use after CadQuery exports (and preferably artifact asserts). Docker + `uv run` only.

## Inputs

- `output/<PART>/<PART>.stl`
- `output/<PART>/<PART>_profile.dxf`
- `parts/<PART>/views.py`

## How to run

```bash
PART=kp08 docker compose run --rm -e PART cad uv run python /work/scripts/render_previews.py
PART=kp08 docker compose run --rm -e PART cad uv run python /work/scripts/assert_previews.py
```

## Outputs (`output/<PART>/previews/`)

Filenames come from `views.py` (KP08: `iso.png`, `front.png`, `top.png`, `right.png`, `profile.png`).
Also `<PART>_profile.svg` and `index.html`.

## Auto pass criteria

- Each view PNG: magic, size ≥ 15KB, non-white ratio ≥ 1%
- SVG has `<path>`; gallery HTML present

## Gallery on host

```bash
PART=kp08 ./scripts/open_gallery.sh   # http://127.0.0.1:8765/
```

Next: `skill_4_human_verify`.
