# shaft_8x100 — Ø8 × 100 mm plain shaft

Spec-driven solid for use with `mcm_1434k33` in `plate_mcm_1434k33_shaft`.

| Param | Value (mm) |
| --- | --- |
| `shaft_diameter` | 8 |
| `shaft_length` | 100 |

## Axes

- **Y** — shaft axis (length), same as bearing bore
- **X / Z** — radial

Cylinder centered at origin (−50 … +50 on Y).

## Run

```bash
PART=shaft_8x100 ./scripts/run_pipeline.sh --skip-human
PART=shaft_8x100 ./scripts/open_gallery.sh
```

Model: [`model.py`](model.py). Views: [`views.py`](views.py). Dims: [`drawings/dims.md`](drawings/dims.md).
