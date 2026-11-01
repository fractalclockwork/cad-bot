# shaft_8x150 — Ø8 × 150 mm plain shaft

Spec-driven solid for use with KP08 in a later assembly.

| Param | Value (mm) |
| --- | --- |
| `shaft_diameter` | 8 |
| `shaft_length` | 150 |

## Axes

- **Y** — shaft axis (length), same as KP08 bore  
- **X / Z** — radial  

Cylinder centered at origin (−75 … +75 on Y).

## Run

```bash
PART=shaft_8x150 ./scripts/run_pipeline.sh --skip-human
PART=shaft_8x150 ./scripts/open_gallery.sh
```

Model: [`model.py`](model.py). Views: [`views.py`](views.py). Dims: [`drawings/dims.md`](drawings/dims.md).
