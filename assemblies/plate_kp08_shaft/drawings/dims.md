# plate_kp08_shaft — assembly mates

Units: mm. Spec-driven (no drawing image).

## BOM

| Qty | Part | Role |
| --- | --- | --- |
| 1 | `plate_100x150x5` | Base plate |
| 2 | `kp08` | Pillow blocks |
| 1 | `shaft_8x150` | Ø8 shaft |

## Mates

| Instance | Translation (X, Y, Z) | Notes |
| --- | --- | --- |
| plate | (0, 0, 0) | Bottom on Z=0; top at Z=5 |
| kp08_pos | (0, +50, 5) | On plate; bolts at (±21, +50) |
| kp08_neg | (0, −50, 5) | On plate; bolts at (±21, −50) |
| shaft | (0, 0, 20) | Z = 5 + KP08 h(15); through both bores |

## Axes

- X: bolt pitch
- Y: shaft / block spacing
- Z: up
