# Assemblies

Multi-body models compose solids from [`parts/`](../parts/).

## Layout

```
assemblies/<name>/
  README.md
  model.py
  views.py
  drawings/dims.md
```

Scaffold: `./scripts/new_assembly.sh <name>` (from `_template/`).

## Contract

1. Keep each solid under `parts/<part>/model.py` with `build_part()`.
2. Assembly loads builders via `part_config.load_part_module` and applies `cq.Location` mates; document in `drawings/dims.md`.
3. Export `output/<assy>/<assy>.step` and `.stl` (DXF not required).
4. Run `PART=<assy> ./scripts/run_pipeline.sh` — resolves `assemblies/` when not in `parts/`.

## Exemplar

[`plate_kp08_shaft/`](plate_kp08_shaft/) — plate_100x150x5 + 2× kp08 + shaft_8x150.

See **`skill_6_assembly_workflow`**.
