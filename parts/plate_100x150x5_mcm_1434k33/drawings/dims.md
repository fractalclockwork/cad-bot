# plate_100x150x5_mcm_1434k33 dimensions

Source: spec-driven (no drawing image); hole pattern from measured `mcm_1434k33` STEP
Units: mm

| Label | Meaning | Value | Param |
| --- | --- | --- | --- |
| W | plate width (X) | 100 | `plate_width` |
| D | plate depth (Y) | 150 | `plate_depth` |
| t | plate thickness (Z) | 5 | `plate_thickness` |
| e | 1434K33 mount pitch | 30.9 | `bolt_hole_pitch` |
| s | bolt hole diameter | 5.5 | `bolt_hole_diameter` |
| — | shaft clearance diameter | 10 | `shaft_clearance_diameter` |

## Axis convention

- X: bolt pitch (plate width)
- Y: flange short / plate depth
- Z: thickness (up); bottom on Z=0; shaft through plate along Z

## Hole coordinates (plate centered at origin)

Single flange centered at `(0, 0)`. Thru-plate flange mount.

| Hole | X | Y | Dia |
| --- | --- | --- | --- |
| bolt 1 | −15.45 | 0 | 5.5 |
| bolt 2 | +15.45 | 0 | 5.5 |
| shaft clearance | 0 | 0 | 10.0 |

## Notes

Matches measured `mcm_1434k33` mount_pitch / mount_hole_d. Shaft clearance is Ø8 + 2 mm
(no boss below bearing mount face). Do not reuse `plate_100x150x5` (dual-KP08).
