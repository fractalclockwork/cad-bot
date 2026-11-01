# mcm_3971n31 — McMaster 3971N31 ready-mount housing

Catalog: [3971N31](https://www.mcmaster.com/3971N31/) (8 mm bearing OD × 5 mm wide aluminum housing).

Geometry is **CadQuery `importStep`** of the McMaster 3-D STEP (gitignored local
cache) — not a parametric reinvent.

## Vendor STEP (required, not in git)

Login to McMaster → Product Detail → select **3-D STEP** → keep the original
download name under `vendor/mcmaster/`:

```text
vendor/mcmaster/3971N31_Ready-Mount Bearing Housing.STEP
```

(`3971N31.step` is an optional short alias; the loader prefers the McMaster name.)

See [`vendor/mcmaster/README.md`](../../vendor/mcmaster/README.md) and `skill_7_mcmaster_to_cadquery`.

## Axes (after framing)

| Axis | Meaning |
| --- | --- |
| X | Base length / bolt pitch |
| Y | Bearing / shaft |
| Z | Up (base on Z≈0) |

## Run

```bash
PART=mcm_3971n31 ./scripts/run_pipeline.sh --skip-human
PART=mcm_3971n31 ./scripts/open_gallery.sh
```
