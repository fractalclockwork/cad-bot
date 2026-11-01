# McMaster 1434K33 — Mounted roller bearing with two-bolt flange

Source: https://www.mcmaster.com/1434K33/
Title: Mounted Roller Bearing with Two-Bolt Flange
Geometry: McMaster 3-D STEP at
`vendor/mcmaster/1434K33_Mounted Roller Bearing with Two-Bolt Flange.STEP`
(gitignored; keep McMaster download filename; manual login download) → CadQuery `importStep`
Units: mm

**Mount type: flange** (shaft ∥ bolts). Framed for flange-on-plate: shaft along **Z**,
not pillow-block Y=shaft.

Envelope after flange-mount framing (from vendor STEP bounding box):

| Attribute | mm | Param / assert |
| --- | --- | --- |
| Flange long (X) | 45.0 | `overall_length` |
| Flange short (Y) | 31.8 | `flange_width` |
| Height along shaft (Z) | 16.8 | `overall_height` |

Mate-critical (measured from framed vendor STEP cylinders/circles):

| Attribute | mm | Param / mate ref |
| --- | --- | --- |
| Mount hole C–C (X) | 30.9 | `mount_pitch` (±15.45) |
| Mount hole diameter | 5.5 | `mount_hole_d` (r=2.75) |
| Bore diameter | 8.8 | `bore_diameter` (r=4.4) |

No boss protrudes below the mount face (Z=0) after framing — plate needs shaft
clearance only (not a hub cutout).

## Axis convention (after framing)

- X: flange long axis / bolt pitch
- Y: flange short axis in the mount plane
- Z: shaft / bore (up from mount face); Zmin ≈ 0
- Origin: XY centered; mount face on Z ≈ 0

## Notes

- Solid comes from McMaster 3-D STEP — do not reinvent parametrically.
- Vendor file must never be committed; only local under `vendor/mcmaster/`.
- Operator requested “1435k33”; on-disk McMaster download is **1434K33** — PART follows the STEP.
- Bore Ø8.8 accepts an Ø8 shaft with radial clearance (loose slip fit).
