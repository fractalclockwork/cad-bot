# plate_mcm_1434k33_shaft

Thru-plate flange assembly: McMaster 1434K33 on `plate_100x150x5_mcm_1434k33` with `shaft_8x100` along Z through the plate and bore.

## BOM

| Qty | Part |
| --- | --- |
| 1 | [`plate_100x150x5_mcm_1434k33`](../../parts/plate_100x150x5_mcm_1434k33/) |
| 1 | [`mcm_1434k33`](../../parts/mcm_1434k33/) |
| 1 | [`shaft_8x100`](../../parts/shaft_8x100/) |

## Mates (mm)

- Plate at identity (top Z=5)
- Bearing at `(0, 0, 5)` — flange on plate, shaft along Z
- Shaft rotated Y→Z, centered at Z=10.9 — through plate clearance + bore

## Run

```bash
PART=plate_mcm_1434k33_shaft ./scripts/run_pipeline.sh --skip-human
PART=plate_mcm_1434k33_shaft ./scripts/open_gallery.sh
```

Model: [`model.py`](model.py). Views: [`views.py`](views.py).
