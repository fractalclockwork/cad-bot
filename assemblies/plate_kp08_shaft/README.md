# plate_kp08_shaft

First cad-bot assembly: dual KP08 pillow blocks on `plate_100x150x5` with centered `shaft_8x150`.

## BOM

| Qty | Part |
| --- | --- |
| 1 | [`plate_100x150x5`](../../parts/plate_100x150x5/) |
| 2 | [`kp08`](../../parts/kp08/) |
| 1 | [`shaft_8x150`](../../parts/shaft_8x150/) |

## Mates (mm)

- Plate at identity (top Z=5)
- KP08 at `(0, ±50, 5)`
- Shaft at `(0, 0, 20)` — through bore centers

## Run

```bash
PART=plate_kp08_shaft ./scripts/run_pipeline.sh --skip-human
PART=plate_kp08_shaft ./scripts/open_gallery.sh
```

Model: [`model.py`](model.py). Views: [`views.py`](views.py).
