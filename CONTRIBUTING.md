# Contributing

## Add a part

1. Scaffold: `./scripts/new_part.sh <name>`
2. Drop drawing images into `parts/<name>/drawings/` and fill `dims.md`
3. Lock axes (X/Y/Z) in `model.py` docstring and `views.py` criteria
4. Implement `build_part()`, `assert_geometry()`, exports using `PART` naming
5. Run: `PART=<name> ./scripts/run_pipeline.sh --skip-human`
6. Gallery: `PART=<name> ./scripts/open_gallery.sh`
7. Human: `PART=<name> ./scripts/human_verify.sh`

For drawing-driven authoring, follow **`skill_5_drawing_to_cadquery`**.

Checklist:

- [ ] Dimension table in `drawings/dims.md`
- [ ] Axis convention documented
- [ ] Parametric CadQuery with drawing-bound asserts
- [ ] Artifacts under `output/<name>/`
- [ ] `views.py` criteria match expected bore/hole appearance
- [ ] Auto gates A–D pass; Phase E for sign-off

## Add an assembly

See [`assemblies/README.md`](assemblies/README.md). Keep solids in `parts/`;
compose transforms in `assemblies/<name>/model.py` when that layout lands.

## Conventions

- No CadQuery on the host — Docker + `uv` only
- Shared scripts must not hardcode part names (only default `PART=kp08`)
- Do not commit generated `output/` contents (keep `.gitkeep`)
