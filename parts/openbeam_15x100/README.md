# openbeam_15x100 — OpenBeam 15×15 × 100 mm

Assembly-ready OpenBeam-style T-slot extrusion (parametric approximation).

| Param | Value (mm) |
| --- | --- |
| `beam_size` | 15 |
| `beam_length` | 100 |
| `center_bore_diameter` | 2.5 |
| `slot_opening` | 3 |

## Axes

- **Y** — length (−50 … +50)  
- **X / Z** — 15×15 cross-section  

## Run

```bash
PART=openbeam_15x100 ./scripts/run_pipeline.sh --skip-human
PART=openbeam_15x100 ./scripts/open_gallery.sh
```

Model: [`model.py`](model.py). Dims: [`drawings/dims.md`](drawings/dims.md).
