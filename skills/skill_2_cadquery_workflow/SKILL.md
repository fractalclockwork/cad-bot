---
name: skill_2_cadquery_workflow
description: >-
  Generate, assert, and export a parametric CadQuery part inside Docker (uv run).
  KP08 exemplar: parts/kp08/model.py → output/kp08/{step,stl,profile.dxf}.
---

# CadQuery Workflow (Primary)

Use only after `skill_1_environment_preflight` passes. **Never** call host CadQuery — Docker + `uv run` only.

## Model layout

- Part script: `parts/<PART>/model.py`
- KP08 exemplar: `parts/kp08/model.py` (dims in `parts/kp08/README.md` / `drawings/dims.md`)
- Axes (KP08): **X** = bolt pitch, **Y** = shaft, **Z** = up
- Profile DXF = intended 2D plane only (KP08: top mount, two flange holes)

## How to run

```bash
PART=kp08 docker compose run --rm -e PART \
  cad uv run python /work/parts/kp08/model.py /work/output/kp08
```

Or full pipeline Phase B via `./scripts/run_pipeline.sh`.

## Assertions (inside the model)

- `shape.val().isValid()`; volume > 0; non-empty BoundingBox
- Drawing-critical dims within tolerance

## Exports

| File | Path |
| --- | --- |
| STEP | `output/<PART>/<PART>.step` |
| STL | `output/<PART>/<PART>.stl` |
| Profile DXF | `output/<PART>/<PART>_profile.dxf` |

## On failure

- Invalid solid → re-check selectors/booleans
- Empty export → regenerate; check `PART` output dir
