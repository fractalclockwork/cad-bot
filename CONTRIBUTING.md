# Contributing

## Add a part

1. `./scripts/new_part.sh <name>`
2. Fill `parts/<name>/drawings/dims.md` (drawing or written spec)
3. Lock axes in `model.py` / `views.py`
4. Implement `build_part()`, asserts, export STEP + STL
5. `PART=<name> ./scripts/run_pipeline.sh --skip-human`
6. `PART=<name> ./scripts/open_gallery.sh`
7. Optional sign-off: `PART=<name> ./scripts/human_verify.sh`

Drawing/spec authoring: **`skill_5_drawing_to_cadquery`**.

### Add a part from a McMaster-Carr URL

1. **Log into McMaster** in a browser; Product Detail → select **3-D STEP** → download by hand into `vendor/mcmaster/`, **keeping McMaster’s original filename** (e.g. `3971N31_Ready-Mount Bearing Housing.STEP`; gitignored — never commit). Do not automate CAD download or use the Product API.
2. Follow **`skill_7_mcmaster_to_cadquery`**: PART id `mcm_<lowercase_partnum>`, `importStep` + axis frame by **mount type** (pillow Y=shaft vs flange Z=shaft), catalog dims for asserts
3. `PART=mcm_… ./scripts/run_pipeline.sh --skip-human`
4. Confirm `git status` does not stage vendor STEP files

Exemplars: `parts/mcm_3971n31/` (pillow / base-mount), `parts/mcm_1434k33/` (two-bolt flange).

Checklist: dims.md · axes · STEP/STL · stl3d views · pipeline A–D

## Add an assembly

1. Ensure each solid exists under `parts/` with `build_part()`
2. **Pre-mate gate + human conflict resolution** (skill_6): measure bore vs mount-hole axes; classify pillow vs flange; if ambiguous or intent conflicts with geometry, **stop and ask** 1–2 A/B questions — every option must be geometrically valid; list plate cutouts in the same turn
3. `./scripts/new_assembly.sh <name>`
4. After human lock-in: BOM + mates in `assemblies/<name>/drawings/dims.md`
5. Wire `load_part_module` + `cq.Location` in `model.py`
6. `PART=<name> ./scripts/run_pipeline.sh --skip-human`
7. Gallery / optional human review — orientation fail → new conflict cycle (re-ask; do not silent-guess)

Follow **`skill_6_assembly_workflow`**.

Exemplars:

| Mount | Assembly |
| --- | --- |
| Pillow | `assemblies/plate_kp08_shaft/` |
| Flange thru-plate | `assemblies/plate_mcm_1434k33_shaft/` |

Checklist: human A/B if needed · BOM/mates · shared axes · volume/BB asserts · STEP/STL · pipeline A–D

## Conventions

- No CadQuery on the host — Docker + `uv` only
- Shared scripts: no hardcoded part names (only default `PART=kp08`)
- Do not commit generated `output/` (keep `.gitkeep`)
- DXF is not a pipeline requirement
