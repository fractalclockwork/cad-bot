# tripod_head_openbeam_15 dimensions

**Archive / return-later.** Partial geometry success; **FDM overhang debt**
unresolved. Not a skill_8 exemplar — see
[`docs/postmortems/tripod_head_openbeam_15.md`](../../../docs/postmortems/tripod_head_openbeam_15.md).

Source: natural language (skill_8 attempt) — cube-corner layout + convex-hull joins
Units: mm
Mate: `parts/openbeam_15x100/` (`beam_size=15`)

| Label | Meaning | Value | Param |
| --- | --- | --- | --- |
| — | nominal beam section | 15 | `beam_nominal` |
| — | print clearance (per side) | 0.2 | `print_clearance` |
| — | cradle opening (square) | 15.4 | `cradle_opening` |
| — | cradle wall thickness | 3 | `wall` |
| — | cradle cross-section | 21.4 | `body_size` (= opening + 2×wall) |
| — | cradle length (stop → mouth) | 16 | `cradle_length` |
| — | stop wall / arm length | 3 / 19 | `wall` / `arm_length` |
| — | M3 bolt axis from stop | 7.5 | `bolt_from_stop` |
| — | M3 clearance hole Ø | 3.4 | `bolt_hole_diameter` |
| — | M3 nominal | 3.0 | `bolt_nominal` |
| — | cradle count | 3 | `num_cradles` |
| — | top-view spacing | 120° | about +Z (cube corner projection) |
| — | pairwise axis angle | 90° | cube-corner orthogonality |
| — | leg splay | asin(1/√3) ≈ 35.264° down from horizontal | `splay_deg` (fixed by orthogonality) |
| — | stop / cradle radius | 22 | `hub_radius` (keeps sockets clear of neighbors) |
| — | solid core radius / height | 17 / 30 | `core_radius` / `core_height` |
| — | flat mount pad radius / height | 22 / 6 | `mount_pad_radius` / `mount_pad_height` |
| — | hull anchor sphere radius | 8 | `hull_anchor_radius` |

## Join operation (locked)

**Convex hull** (OpenSCAD-style), not a loft:

Build **one** arm on +X, then rotate copies (identical sockets):

1. `convex_hull(core_proxy, stop_back_proxy)` where:
   - `core_proxy` = sphere of radius `hull_anchor_radius` on the +X core surface
   - `stop_back_proxy` = thin slab at the stop only (does **not** fill the U pocket)
2. Union detailed U-cradle
3. Cut channel (opening + 0.2 clearance) and M3 bolt through walls
4. Spin arm by 0° / 120° / 240° about +Z and union to core + mount pad

`hub_radius` stays large enough that neighboring hulls do not fill other U-pockets.

## Axis convention

- Origin: hub axis at XY origin; finished part seated on **Z = 0**
- **Cube corner**: three mutually orthogonal beam axes; top view **120°**; splay `asin(1/√3)`
- Three identical **U-cradles** at azimuth 0°, 120°, 240° about +Z
- U open toward **−Z local** (after splay ≈ downward) — legs drop in from below
- Flat **mount pad** on +Z
- M3 at section / T-slot center; `bolt_from_stop` = 7.5 mm

## Print notes (FDM)

- Print with **mount pad on the bed** (pad down); cradles splay upward/outward
- Hulls are filled convex blends (printable tapers)
- Cradle opening 15.4 = 15 + 2×0.2; hole Ø3.4
- Single solid — no floating boolean scraps

## Locked intent (skill_8)

- Mate style: U-cradle, open −Z local
- Layout: cube corner
- Join: **convex hull(core_proxy, cradle_envelope)** per leg
- Flat mount pad required
