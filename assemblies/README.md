# Assemblies

Multi-body models compose solids from [`parts/`](../parts/).

## Planned layout

```
assemblies/<name>/
  README.md
  model.py          # imports / places parts/*.model solids
  views.py          # assembly preview criteria
  drawings/         # assembly views / BOM notes
```

## Contract (for the next assembly)

1. Keep each solid as a part under `parts/<part>/model.py` with `build_part()`.
2. Assembly `model.py` imports those builders (or loads STEP) and applies explicit
   transforms; document mates in comments.
3. Export `output/<assy>/<assy>.step` (compound) and optional per-part copies.
4. Run with `PART=<assy>` only after assembly scripts share the part pipeline
   contract — until then, prefer composing parts manually in a dedicated module.

No assemblies ship in v1; this directory reserves the convention.
