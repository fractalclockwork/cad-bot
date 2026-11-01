# plate_150x150x5 — 150×150×5 mm mounting plate

Plain base plate for a later KP08 + shaft assembly.

| Param | Value (mm) |
| --- | --- |
| `plate_width` | 150 |
| `plate_depth` | 150 |
| `plate_thickness` | 5 |

## Axes

- **X / Y** — plate plane  
- **Z** — thickness; bottom on Z=0, top at Z=5  

## Run

```bash
PART=plate_150x150x5 ./scripts/run_pipeline.sh --skip-human
PART=plate_150x150x5 ./scripts/open_gallery.sh
```

Model: [`model.py`](model.py). Views: [`views.py`](views.py). Dims: [`drawings/dims.md`](drawings/dims.md).
