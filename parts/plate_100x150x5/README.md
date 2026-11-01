# plate_100x150x5 — dual-KP08 mounting plate

100×150×5 mm base plate with four Ø4.8 holes for two KP08 pillow blocks spaced 100 mm apart on center (along Y).

| Param | Value (mm) |
| --- | --- |
| `plate_width` (X) | 100 |
| `plate_depth` (Y) | 150 |
| `plate_thickness` | 5 |
| `bolt_hole_pitch` | 42 |
| `bolt_hole_diameter` | 4.8 |
| `block_spacing` | 100 |

## Axes

- **X** — bolt pitch; bore midline at X=0 (50 mm from each long side)  
- **Y** — shaft / block spacing; centers at Y=±50 (25 mm from each short end)  
- **Z** — thickness; bottom on Z=0  

## Run

```bash
PART=plate_100x150x5 ./scripts/run_pipeline.sh --skip-human
PART=plate_100x150x5 ./scripts/open_gallery.sh
```

Model: [`model.py`](model.py). Views: [`views.py`](views.py). Dims: [`drawings/dims.md`](drawings/dims.md).
