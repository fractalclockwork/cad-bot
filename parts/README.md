# Parts

Each solid lives under `parts/<name>/`:

```
parts/<name>/
  README.md
  model.py
  views.py          # stl3d preview criteria
  drawings/         # dims.md (+ images if any)
```

## Conventions

- Name: lowercase, `a-z0-9_-`. Set `PART=<name>`.
- Artifacts: `output/<name>/<name>.step`, `.stl`
- Previews: `output/<name>/previews/`

## Scaffold

```bash
./scripts/new_part.sh my_part
PART=my_part ./scripts/run_pipeline.sh --skip-human
```

Drawing/spec authoring: `skill_5_drawing_to_cadquery`. Assemblies: [`../assemblies/README.md`](../assemblies/README.md).
