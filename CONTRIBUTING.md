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

Checklist: dims.md · axes · STEP/STL · stl3d views · pipeline A–D

## Add an assembly

1. Ensure each solid exists under `parts/` with `build_part()`
2. `./scripts/new_assembly.sh <name>`
3. BOM + mates in `assemblies/<name>/drawings/dims.md`
4. Wire `load_part_module` + `cq.Location` in `model.py`
5. `PART=<name> ./scripts/run_pipeline.sh --skip-human`
6. Gallery / optional human review

Follow **`skill_6_assembly_workflow`**. Exemplar: `assemblies/plate_kp08_shaft/`.

Checklist: BOM/mates · shared axes · volume/BB asserts · STEP/STL · pipeline A–D

## Conventions

- No CadQuery on the host — Docker + `uv` only
- Shared scripts: no hardcoded part names (only default `PART=kp08`)
- Do not commit generated `output/` (keep `.gitkeep`)
- DXF is not a pipeline requirement
