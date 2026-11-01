# Reference: drawing → CadQuery

## Suggested file layout for a new part

```
parts/<part_name>/
  README.md
  model.py
  views.py
  drawings/
    source.png          # or multiple views
    dims.md             # dimension table
output/<part_name>/
  <part_name>.step
  <part_name>.stl
  <part_name>_profile.dxf   # only if 2D intent is clear
  previews/
```

Scaffold: `./scripts/new_part.sh <part_name>`

## dims.md template

```markdown
# <part_name> dimensions

Source: parts/<part_name>/drawings/source.png
Units: mm

| Label | Meaning | Value | Param |
| --- | --- | --- | --- |
| a | overall length |  | `overall_length` |
| e | hole center distance |  | `bolt_hole_pitch` |
| s | hole diameter |  | `bolt_hole_diameter` |
| h | center height |  | `base_center_height` |
| g | base thickness |  | `base_thickness` |
| w | overall height |  | `overall_height` |

## Axis convention

- X:
- Y:
- Z:

## Derived

- flange_radius = (a - e) / 2   # only if holes centered in rounded ends
```

## Pipeline

```bash
PART=<part_name> ./scripts/run_pipeline.sh --skip-human
PART=<part_name> ./scripts/open_gallery.sh
```

## Assemblies

See `assemblies/README.md`. Keep solids in `parts/`; compose in `assemblies/<name>/model.py`.
