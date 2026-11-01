# McMaster 3971N31 — Ready-Mount bearing housing (catalog dims)

Source: https://www.mcmaster.com/3971N31/
Title: Ready-Mount Bearing Housing with Base Mount (2014 Aluminum)
Geometry: McMaster 3-D STEP at
`vendor/mcmaster/3971N31_Ready-Mount Bearing Housing.STEP` (gitignored; keep
McMaster download filename; manual login download) → CadQuery `importStep`
Units: mm (inch fractions converted)

| Attribute | Catalog value | mm | Param / assert |
| --- | --- | --- | --- |
| For bearing OD | 8 mm | 8.0 | `bearing_od` |
| For bearing width | 5 mm | 5.0 | `housing_width` (Y) |
| Center height | 9.5 mm | 9.5 | `center_height` |
| Overall height | 19 mm | 19.0 | `overall_height` |
| Overall length | 37 mm | 37.0 | `overall_length` |
| Mount hole dia | 1/8" | 3.175 | `mount_hole_d` |
| Hole C–C | 29 mm | 29.0 | `mount_pitch` |

## Axis convention (after framing)

- X: base length / bolt-hole pitch
- Y: bearing / shaft axis
- Z: up from mounting plane
- Origin: shaft axis at Y midplane; base on Z ≈ 0; shaft center ≈ (0, 0, 9.5)

## Notes

- Solid comes from McMaster 3-D STEP — do not reinvent parametrically.
- Vendor file must never be committed; only local under `vendor/mcmaster/`.
