---
name: skill_5_drawing_to_cadquery
description: >-
  Author a new CadQuery part under parts/<name>/ from dimensioned drawings or a
  written spec (Docker + uv). Use for new solids; for assemblies use skill_6.
---

# Drawing / Spec → CadQuery Part

Build under `parts/<name>/`, then validate with the PART-aware pipeline.

**Never** install CadQuery on the host.

## When to use

- Dimensioned drawing attached, or clear numeric **spec** (e.g. Ø8×150 shaft)
- New **part** (not assembly → `skill_6`)

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| Drawing images **or** written dims | yes | Spec-driven: still fill `dims.md` |
| Part name | yes | lowercase; `PART=<name>` |
| Units | default mm | Confirm if inch |

Save images under `parts/<name>/drawings/` when present.

## Workflow

### 1. Read source

Drawing: views, holes/bores, envelopes. Spec: table of params. **Do not invent missing dims.**

### 2. Dimension table

Write `parts/<name>/drawings/dims.md` **before** CadQuery (drawing- or spec-driven).

### 3. Lock axes

Document X/Y/Z in `model.py` and `views.py` before modeling.

### 4. Author

```bash
./scripts/new_part.sh <name>
```

Implement `build_part()`, `assert_geometry()`, export **STEP + STL**.

### 5. Validate

```bash
PART=<name> ./scripts/run_pipeline.sh --skip-human
PART=<name> ./scripts/open_gallery.sh
```

### 6. Human verification

Update `views.py` criteria; `skill_4` when signing off.

## Anti-patterns (KP08)

| Mistake | Fix |
| --- | --- |
| Overall length as hole pitch | Read **e** separately from **a** |
| Shaft on wrong axis | Lock Y = shaft first |
| Auto ink checks only | Plan human Phase E for orientation |

## Checklist

- [ ] `drawings/dims.md` (+ images if any)
- [ ] Axes documented
- [ ] STEP/STL via pipeline A–D
- [ ] Assemblies deferred to skill_6

## Related

`skill_1`–`skill_4`; `skill_6` for assemblies; McMaster URL → `skill_7_mcmaster_to_cadquery`;
exemplar `parts/kp08/`.
