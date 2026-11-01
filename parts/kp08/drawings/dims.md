# KP08 dimensions (front elevation)

Source: `parts/kp08/drawings/front_elevation.png`
Units: mm

| Label | Meaning | Value | Param |
| --- | --- | --- | --- |
| a | overall length | 55 | `overall_length` |
| e | mounting hole C–C | 42 | `bolt_hole_pitch` |
| s | hole diameter | 4.8 | `bolt_hole_diameter` |
| h | shaft center height | 15 | `base_center_height` |
| g | base thickness | 5 | `base_thickness` |
| w | overall height | 29 | `overall_height` |
| — | shaft bore diameter | 8 | `bore_diameter` |

## Axis convention

- X: bolt pitch / long base
- Y: shaft axis
- Z: up from mounting plane

## Derived

- `flange_radius = (a - e) / 2 = 6.5` (holes centered in rounded ends)
- `boss_od = 2 * (w - h) = 28`
