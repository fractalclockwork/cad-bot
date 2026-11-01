# tripod_head_openbeam_15_legs — BOM + mates

Fit-check assembly: verified cube-corner head + three equal OpenBeam legs.
Units: mm

## BOM

| Qty | Part | Notes |
| --- | --- | --- |
| 1 | `tripod_head_openbeam_15` | cube-corner U-cradle hub (archived partial; not FDM-signed) |
| 3 | `openbeam_15x100` | equal length 100 mm |

## Mates

| Instance | Placement |
| --- | --- |
| head | identity (already seated on Z=0) |
| leg_0 / leg_1 / leg_2 | `cradle_azimuths()` → 0° / 120° / 240° |

Per leg (driven by head helpers — do not hardcode splay):

- Axis = `cradle_axis_direction(az)` (cube corner: pairwise 90°, top 120°, splay `asin(1/√3)`)
- −Y end of OpenBeam (native length along Y) seated on cradle **stop**
- Section oriented so ±X T-slot faces align with M3 bolt (cradle lateral / section center)
- Beam center = `cradle_stop_center(az)` + axis × (`beam_length` / 2)
- `splay_deg` = `head_mod.splay_deg` (not a free 30°)

## Axes

Shared with head: hub +Z; cube-corner cradles (120° top view, mutually orthogonal).
