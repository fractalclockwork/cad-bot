# openbeam_15x100 dimensions

Source: OpenBeam 15×15 mm T-slot extrusion (spec-driven approximation)
Units: mm

| Label | Meaning | Value | Param |
| --- | --- | --- | --- |
| — | outer section | 15 × 15 | `beam_size` |
| L | length | 100 | `beam_length` |
| — | center hollow (M3 tap) | Ø2.5 | `center_bore_diameter` |
| — | slot opening | 3 | `slot_opening` |
| — | nut pocket width | 5.5 | `nut_pocket_width` |

## Axis convention

- X: section width
- Y: extrusion length (−50 … +50)
- Z: section height

Assembly-ready: centered at origin; length along Y (same as `shaft_8x150` axis convention).

## Notes

Parametric OpenBeam-style profile (four T-slots + center bore). Not a vendor DXF import.
Refs: MakerBeam/OpenBeam 15×15 specs (M3 slots, M3-sized core).
