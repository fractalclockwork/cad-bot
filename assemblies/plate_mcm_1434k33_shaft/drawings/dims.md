# plate_mcm_1434k33_shaft — assembly mates

Units: mm. Spec-driven (no drawing image).

Thru-plate **flange** mount: shaft ∥ bolts ∥ plate normal (Z).

## BOM

| Qty | Part | Role |
| --- | --- | --- |
| 1 | `plate_100x150x5_mcm_1434k33` | Base plate (bolts + Ø10 shaft clearance) |
| 1 | `mcm_1434k33` | Two-bolt flange roller bearing |
| 1 | `shaft_8x100` | Ø8 × 100 shaft |

## Mates

| Instance | Transform | Notes |
| --- | --- | --- |
| plate | identity | Bottom on Z=0; top at Z=5 |
| mcm_1434k33 | translate (0, 0, 5) | Flange on plate; mount holes over (±15.45, 0) |
| shaft_8x100 | rotate +90° about X (Y→Z), translate (0, 0, 10.9) | Through plate clearance + bore |

Shaft Z center = (plate_thickness + bearing_height) / 2 = (5 + 16.8) / 2 = 10.9.

## Axes

- X: bolt pitch
- Y: flange short / plate depth
- Z: up = shaft (through plate)

## Mate refs

| Param | mm |
| --- | --- |
| plate_thickness | 5 |
| mount_pitch | 30.9 |
| shaft_clearance_d | 10 |
| bearing overall_height | 16.8 |
| bore_diameter | 8.8 (Ø8 shaft clears) |
