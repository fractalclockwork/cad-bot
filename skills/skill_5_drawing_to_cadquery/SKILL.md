---
name: skill_5_drawing_to_cadquery
description: >-
  Turn images of dimensioned mechanical drawings into parametric CadQuery parts
  under parts/<name>/ (Docker + uv). Use when the user attaches or points at a
  drawing photo/PNG/PDF page, asks to model from a print, or extract dims.
---

# Drawing Image → CadQuery Part / Assembly

Build parametric CadQuery under `parts/<name>/`, then validate via the PART-aware pipeline.

**Never** install CadQuery on the host. Use `docker compose` + `uv run`.

## When to use

- Dimensioned drawing attached; “model this” / “match this drawing”
- Starting a **new** part (not only KP08)

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| Drawing images | yes | Orthographic views with dim labels |
| Part name | yes | lowercase; `PART=<name>` |
| Units | default mm | Confirm if inch |

Save images under `parts/<name>/drawings/`.

## Workflow

### 1. Read the drawing(s)

Identify views, holes/bores, envelopes, center heights. **Do not invent missing dims.**

### 2. Dimension table

Write `parts/<name>/drawings/dims.md` **before** CadQuery:

| Drawing label | Meaning | Value | Maps to param |
| --- | --- | --- | --- |
| e | mounting hole C–C | 42 | `bolt_hole_pitch` |

Rules (from KP08): hole pitch ≠ overall length unless the drawing says so; keep letter labels in asserts.

### 3. Lock axes

Document X/Y/Z in `model.py` and `views.py` before modeling. Typical: X = bolt pitch, Y = shaft, Z = up.

### 4. Author CadQuery

```bash
./scripts/new_part.sh <name>   # or edit parts/<name>/
```

Implement `parts/<name>/model.py`:

1. Top-level params from the dim table
2. Fluent CadQuery only
3. `assert_geometry()` for drawing-critical dims
4. Export `output/<name>/<name>.{step,stl}` and intentional `_profile.dxf`

Assemblies: see `assemblies/README.md` — compose `parts/*` solids with explicit transforms.

### 5. Auto validation

```bash
PART=<name> ./scripts/run_pipeline.sh --skip-human
```

### 6. Human verification

Update `parts/<name>/views.py` criteria (bore appearance per view). Run `skill_4_human_verify`.
Archive fails under `docs/reviews/`. Note lessons in `docs/verification.md`.

## Anti-patterns (KP08)

| Mistake | Fix |
| --- | --- |
| Overall length as hole pitch | Read **e** separately from **a** |
| Shaft on wrong axis | Lock Y = shaft first |
| Center hole on XY mount DXF | Flange holes only |
| Auto ink checks only | Always plan human Phase E |

## Checklist

- [ ] `parts/<name>/drawings/dims.md` + images
- [ ] Axes in docstring + views
- [ ] `model.py` asserts + exports
- [ ] `PART=<name> ./scripts/run_pipeline.sh --skip-human`
- [ ] Human review when signing off

## Related

`skill_1` … `skill_4`; exemplar `parts/kp08/`.
