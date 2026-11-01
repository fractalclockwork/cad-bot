---
name: skill_6_assembly_workflow
description: >-
  Compose existing parts into an assembly under assemblies/<name>/ with explicit
  mates (cq.Assembly + cq.Location). Use when the user asks for an assembly, BOM
  placement, or to mount parts together (e.g. plate + KP08 + shaft).
---

# Assembly Workflow

Prerequisites: each solid already has `parts/<part>/model.py` with `build_part()`.
Run skill_1 with `PART=<assy>` after scaffolding.

**Never** install CadQuery on the host. Docker + `uv run` only.

## Layout

```
assemblies/<name>/
  README.md
  model.py
  views.py
  drawings/dims.md    # BOM + mate table
```

Scaffold: `./scripts/new_assembly.sh <name>`

Exemplar: `assemblies/plate_kp08_shaft/`

## Pattern

1. Document BOM + mates in `drawings/dims.md` **before** coding.
2. Lock shared axes (match the parts you compose).
3. In `model.py`:
   - `load_part_module("part_id")` from `scripts/part_config.py`
   - `cq.Assembly` + `cq.Location(cq.Vector(x, y, z))` per instance
   - **New solid instance per occurrence** (do not add the same Shape twice)
4. Export **STEP** (assembly) + **STL** (compound for previews). DXF is not required.
5. Assert: compound `isValid`, volume ≈ sum of part volumes, BB envelope.

### Mate checklist

- Sit-on-plate: translate child by `Z = plate_thickness` (plate top).
- Shaft through bore: `Z = plate_thickness + base_center_height` (KP08 `h`).
- Bolt holes: XY of pillow block must match plate hole pattern.

## Validate

```bash
PART=<assy> ./scripts/run_pipeline.sh --skip-human
PART=<assy> ./scripts/open_gallery.sh   # orbit model.stl + orthographic PNGs
```

## Related

- `skill_2` / `skill_5` — author parts first
- `skill_3` / `skill_4` — previews and human sign-off
- `assemblies/README.md` — contract
