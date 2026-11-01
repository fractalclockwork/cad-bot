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

Exemplars: `assemblies/plate_kp08_shaft/` (pillow);
`assemblies/plate_mcm_1434k33_shaft/` (flange thru-plate).

## Pattern

1. Run the **Pre-mate conflict gate** and **Human conflict resolution** (below).
2. Document BOM + mates in `drawings/dims.md` **before** coding (after human lock-in).
3. Lock shared axes (match the parts you compose).
4. In `model.py`:
   - `load_part_module("part_id")` from `scripts/part_config.py`
   - `cq.Assembly` + `cq.Location(cq.Vector(x, y, z))` per instance
   - **New solid instance per occurrence** (do not add the same Shape twice)
5. Export **STEP** (assembly) + **STL** (compound for previews). DXF is not required.
6. Assert: compound `isValid`, volume ≈ sum of part volumes, BB envelope.

### Pre-mate conflict gate (before A/B)

Measure first (vendor STEP / part params): bore axis, mount-hole axes, mount face.
Classify mount type **before** offering choices:

| Type | Axis relationship | Plate mate |
| --- | --- | --- |
| Pillow block (e.g. KP08) | shaft ⊥ bolts | shaft ∥ plate; bolts ∥ plate normal |
| Flange (e.g. 1434K33) | shaft ∥ bolts | shaft **through** plate when flange is on that plate |

Auto pipeline A–D does **not** catch wrong-axis mates — humans do.

### Human conflict resolution (required)

When axes/mates are ambiguous, or user intent conflicts with measured geometry:

1. **Stop coding** — do not guess mates.
2. Ask **1–2 A/B questions**. Every offered option must satisfy measured axis
   relationships. **Never** offer an impossible choice (e.g. flange on a plate
   with shaft ∥ that same plate).
3. In the same answer, list **plate cutouts** required by each option (bolt
   pattern and/or shaft/hub clearance).
4. After the human chooses → lock mates in `drawings/dims.md`, then implement.
5. Gallery / Phase E fail on orientation → **new conflict cycle**: re-measure,
   re-ask with corrected valid options. Do not silently “fix” by guessing.

Example flange A/B (both valid):

- A: flange on plate face, shaft through plate (normal mount) — plate needs
  bolt holes + shaft/hub clearance
- B: flange on a vertical wall, shaft parallel to floor — plate/wall cutouts
  match that face

Exemplars: `assemblies/plate_kp08_shaft/` (pillow);
`assemblies/plate_mcm_1434k33_shaft/` (flange thru-plate).

### Mate checklist

- Sit-on-plate: translate child by `Z = plate_thickness` (plate top).
- Pillow shaft through bore: `Z = plate_thickness + base_center_height` (KP08 `h`); shaft along Y.
- Flange thru-plate: bearing flange on plate; shaft along Z through plate clearance + bore (rotate Y-axis shaft parts as needed).
- Bolt holes: XY of mount pattern must match plate hole pattern.

## Validate

```bash
PART=<assy> ./scripts/run_pipeline.sh --skip-human
PART=<assy> ./scripts/open_gallery.sh   # orbit model.stl + orthographic PNGs
```

## Related

- `skill_2` / `skill_5` — author parts first
- `skill_3` / `skill_4` — previews and human sign-off
- `assemblies/README.md` — contract
