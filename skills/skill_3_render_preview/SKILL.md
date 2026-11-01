---
name: skill_3_render_preview
description: >-
  Headless STL multi-view PNGs plus interactive gallery (Three.js model.stl)
  for a part or assembly. Reads views.py under parts/ or assemblies/.
---

# Render Preview Workflow

Use after CadQuery exports (and preferably artifact asserts). Docker + `uv run` only.

## Inputs

- `output/<PART>/<PART>.stl`
- `parts/<PART>/views.py` **or** `assemblies/<PART>/views.py` (`stl3d` views)

## How to run

```bash
PART=<name> docker compose run --rm -e PART cad uv run python /work/scripts/render_previews.py
PART=<name> docker compose run --rm -e PART cad uv run python /work/scripts/assert_previews.py
```

Or via `./scripts/run_pipeline.sh` Phase D.

## Outputs (`output/<PART>/previews/`)

| Artifact | Notes |
| --- | --- |
| `iso.png`, `front.png`, … | From `stl3d` entries in `views.py` |
| `model.stl` | Copy for interactive viewer |
| `index.html` | Gallery: Three.js orbit + orthographic cards |

## Auto pass criteria (`assert_previews.py`)

- Each **stl3d** PNG: magic, size ≥ 15KB, non-white ratio ≥ 1%
- `model.stl` and `index.html` present

## Gallery on host

```bash
PART=<name> ./scripts/open_gallery.sh   # http://127.0.0.1:8765/
```

Prefer this over `file://` (Snap Firefox). Next: `skill_4_human_verify`.
