# tripod_head_openbeam_15 — archived partial (deferred)

**Status: partial success — do not use as a workflow or FDM exemplar.**

Cube-corner hub with three U-cradles for OpenBeam 15×15 eventually reached
functional channels and M3 through-holes, but **printability is unresolved**
(pad-down + splayed cradles → overhangs). Iterative agentic redesign is stopped;
return after stronger design-spec / FDM gates.

Post-mortem: [`docs/postmortems/tripod_head_openbeam_15.md`](../../docs/postmortems/tripod_head_openbeam_15.md).

| Param | Value (mm / deg) |
| --- | --- |
| `cradle_opening` | 15.4 (+0.2/side on 15) |
| `wall` | 3 |
| `cradle_length` | 16 |
| `bolt_from_stop` | 7.5 |
| `bolt_hole_diameter` | 3.4 |
| `splay_deg` | asin(1/√3) ≈ 35.264 |
| `hub_radius` | 22 |
| `core_radius` / `core_height` | 17 / 30 |
| `mount_pad_radius` / `mount_pad_height` | 22 / 6 |
| `hull_anchor_radius` | 8 |

Mate stock: [`openbeam_15x100`](../openbeam_15x100/).

## Print (known debt)

Intended pad-down orientation leaves large overhangs on splayed cradles —
**not** signed off for filament printing. Redesign orientation/geometry before
claiming FDM-ready.

## Run (archive / debug only)

```bash
PART=tripod_head_openbeam_15 ./scripts/run_pipeline.sh --skip-human
PART=tripod_head_openbeam_15 ./scripts/open_gallery.sh
```

Model: [`model.py`](model.py). Dims: [`drawings/dims.md`](drawings/dims.md).
