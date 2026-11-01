# mcm_1434k33 — McMaster 1434K33 two-bolt flange bearing

Catalog: [1434K33](https://www.mcmaster.com/1434K33/) mounted roller bearing with two-bolt flange.

Geometry is **CadQuery `importStep`** of the McMaster 3-D STEP (gitignored).

## Vendor STEP (required, not in git)

```text
vendor/mcmaster/1434K33_Mounted Roller Bearing with Two-Bolt Flange.STEP
```

See [`vendor/mcmaster/README.md`](../../vendor/mcmaster/README.md) and `skill_7_mcmaster_to_cadquery`.

## Axes (after framing)

| Axis | Meaning |
| --- | --- |
| X | Flange long / bolt pitch |
| Y | Shaft / bearing |
| Z | Flange short (Zmin ≈ 0) |

## Run

```bash
PART=mcm_1434k33 ./scripts/run_pipeline.sh --skip-human
PART=mcm_1434k33 ./scripts/open_gallery.sh
```
