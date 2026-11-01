# plate_100x150x5 dimensions

Source: spec-driven (no drawing image)
Units: mm

| Label | Meaning | Value | Param |
| --- | --- | --- | --- |
| W | plate width (X) | 100 | `plate_width` |
| D | plate depth (Y) | 150 | `plate_depth` |
| t | plate thickness (Z) | 5 | `plate_thickness` |
| e | KP08 bolt pitch | 42 | `bolt_hole_pitch` |
| s | hole diameter | 4.8 | `bolt_hole_diameter` |
| — | block center spacing (Y) | 100 | `block_spacing` |

## Axis convention

- X: bolt pitch (plate width)
- Y: shaft / KP08 spacing (plate depth)
- Z: thickness (up); bottom on Z=0

## Hole coordinates (plate centered at origin)

Block centers at `(0, ±50)`. End margin to centers = 25 mm.

| Hole | X | Y |
| --- | --- | --- |
| 1 | −21 | +50 |
| 2 | +21 | +50 |
| 3 | −21 | −50 |
| 4 | +21 | −50 |

Bore midline at X=0 → 50 mm from each long side.

## Notes

Matches KP08 flange pattern (`parts/kp08`). Plain plate otherwise — no other cutouts.
