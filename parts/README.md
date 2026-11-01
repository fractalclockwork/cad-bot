# Parts

Each mechanical solid lives under `parts/<name>/`:

```
parts/<name>/
  README.md       # dims, axes, how to run
  model.py        # CadQuery build + asserts + export
  views.py        # preview / human-review criteria
  drawings/       # source images + dims.md
```

## Conventions

- Part name is lowercase, hyphen-ok (`kp08`, `bracket-a`). Set `PART=<name>`.
- Artifacts: `output/<name>/<name>.step`, `.stl`, `<name>_profile.dxf`
- Previews: `output/<name>/previews/`

## Scaffold

```bash
./scripts/new_part.sh my_part
```

Then fill `drawings/dims.md`, implement `model.py`, adjust `views.py`, and run:

```bash
PART=my_part ./scripts/run_pipeline.sh --skip-human
```

For drawing-driven authoring, use `skill_5_drawing_to_cadquery`.
