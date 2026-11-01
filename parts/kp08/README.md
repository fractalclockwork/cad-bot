# KP08 — 8 mm bore pillow block

Reference part for the cad-bot pipeline.

## Drawing

See [`drawings/`](drawings/) (`front_elevation.png`, `dims.md`).

| Label | Meaning | Value (mm) | Param |
| --- | --- | --- | --- |
| a | overall length | 55 | `overall_length` |
| e | mounting hole C–C | 42 | `bolt_hole_pitch` |
| s | hole diameter | 4.8 | `bolt_hole_diameter` |
| h | shaft center height | 15 | `base_center_height` |
| g | base thickness | 5 | `base_thickness` |
| w | overall height | 29 | `overall_height` |
| — | shaft bore | 8 | `bore_diameter` |

## Axes

- **X** — bolt pitch / long base  
- **Y** — shaft axis  
- **Z** — up from mounting plane  

## Run

```bash
PART=kp08 ./scripts/run_pipeline.sh --skip-human
PART=kp08 ./scripts/open_gallery.sh
```

Model: [`model.py`](model.py). Views: [`views.py`](views.py).
