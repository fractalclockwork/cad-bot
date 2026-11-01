# plate_100x150x5_mcm_1434k33 — 1434K33 thru-plate mounting plate

100×150×5 mm base plate with two Ø5.5 bolt holes (pitch 30.9 mm) and a centered Ø10 shaft clearance for one McMaster 1434K33 flange bearing (shaft through the plate).

| Param | Value (mm) |
| --- | --- |
| `plate_width` (X) | 100 |
| `plate_depth` (Y) | 150 |
| `plate_thickness` | 5 |
| `bolt_hole_pitch` | 30.9 |
| `bolt_hole_diameter` | 5.5 |
| `shaft_clearance_diameter` | 10 |

## Axes

- **X** — bolt pitch; midline at X=0
- **Y** — flange short / plate depth
- **Z** — thickness; bottom on Z=0; shaft along Z through plate

## Run

```bash
PART=plate_100x150x5_mcm_1434k33 ./scripts/run_pipeline.sh --skip-human
PART=plate_100x150x5_mcm_1434k33 ./scripts/open_gallery.sh
```

Model: [`model.py`](model.py). Views: [`views.py`](views.py). Dims: [`drawings/dims.md`](drawings/dims.md).
