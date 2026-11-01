# McMaster 1434K33 — Mounted roller bearing with two-bolt flange

Source: https://www.mcmaster.com/1434K33/
Title: Mounted Roller Bearing with Two-Bolt Flange
Geometry: McMaster 3-D STEP at
`vendor/mcmaster/1434K33_Mounted Roller Bearing with Two-Bolt Flange.STEP`
(gitignored; keep McMaster download filename; manual login download) → CadQuery `importStep`
Units: mm

Envelope after framing (from vendor STEP bounding box):

| Attribute | mm | Param / assert |
| --- | --- | --- |
| Flange long (X) | 45.0 | `overall_length` |
| Shaft depth (Y) | 16.8 | `shaft_depth` |
| Flange short / height (Z) | 31.8 | `flange_width` |

## Axis convention (after framing)

- X: flange long axis / bolt pitch
- Y: shaft / bearing axis
- Z: flange short axis (framed with Zmin ≈ 0)

## Notes

- Solid comes from McMaster 3-D STEP — do not reinvent parametrically.
- Vendor file must never be committed; only local under `vendor/mcmaster/`.
- Operator requested “1435k33”; on-disk McMaster download is **1434K33** — PART follows the STEP.
