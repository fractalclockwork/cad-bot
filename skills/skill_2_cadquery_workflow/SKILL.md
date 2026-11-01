---
name: skill_2_cadquery_workflow
description: >-
  Generate, assert, and export a parametric CadQuery part inside Docker (uv run).
  Exemplars: parts/kp08, parts/shaft_8x150, parts/plate_100x150x5 → STEP + STL.
---

# CadQuery Workflow (Part)

Use after `skill_1_environment_preflight`. **Never** call host CadQuery.

## Layout

- Script: `parts/<PART>/model.py` (`build_part`, `assert_geometry`, export)
- Scaffold: `./scripts/new_part.sh <name>`
- Dims/axes: `parts/<PART>/drawings/dims.md` + README
- Simple exemplars: `shaft_8x150`, `plate_100x150x5`; rich exemplar: `kp08`

## How to run

Prefer the full pipeline:

```bash
PART=<name> ./scripts/run_pipeline.sh --skip-human
```

Or Phase B alone:

```bash
PART=<name> docker compose run --rm -e PART \
  cad uv run python /work/parts/<name>/model.py /work/output/<name>
```

## Assertions (inside the model)

- `shape.val().isValid()`; volume > 0; non-empty BoundingBox
- Drawing- or spec-critical dims within tolerance

## Exports (required)

| File | Path |
| --- | --- |
| STEP | `output/<PART>/<PART>.step` |
| STL | `output/<PART>/<PART>.stl` |

DXF profile export is **not** part of the default verification path (optional leftover in some exemplars).

## On failure

- Invalid solid → re-check selectors/booleans
- Empty export → check `PART` output dir
