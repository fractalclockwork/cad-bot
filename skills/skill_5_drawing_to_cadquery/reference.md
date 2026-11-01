# Reference: drawing / spec → CadQuery

## Suggested file layout

```
parts/<part_name>/
  README.md
  model.py
  views.py
  drawings/
    source.png          # optional
    dims.md
output/<part_name>/
  <part_name>.step
  <part_name>.stl
  previews/
```

Scaffold: `./scripts/new_part.sh <part_name>`

DXF profiles are **not** required by the pipeline.

## dims.md template

```markdown
# <part_name> dimensions

Source: parts/<part_name>/drawings/… or written spec
Units: mm

| Label | Meaning | Value | Param |
| --- | --- | --- | --- |
| a | overall length |  | `overall_length` |

## Axis convention

- X:
- Y:
- Z:
```

## Pipeline

```bash
PART=<part_name> ./scripts/run_pipeline.sh --skip-human
PART=<part_name> ./scripts/open_gallery.sh
```

## Assemblies

Use `skill_6_assembly_workflow` and `./scripts/new_assembly.sh`.
