# skill_8 reference — print clearances + design-spec rules

## Print / fit rules of thumb (FDM ~0.2 mm)

Document chosen values in `dims.md`; do not hardcode magic in the skill alone.

| Situation | Typical approach |
| --- | --- |
| Male part into printed pocket/cradle | +0.2 mm per side on opening (e.g. 15 → 15.4) |
| M3 clearance through printed wall | Ø3.2–3.4 mm (prefer 3.4 unless snug fit requested) |
| M3 tap in print | Prefer heat-set insert or nut capture; avoid relying on plastic threads |
| Clamp wall for M3 cross-bolt | ≥3 mm wall each side of cradle |
| Hole relative to mating end | State min distance from seated end face (e.g. ≥7.5 mm) |
| Bolt vs extrusion T-slot | Axis through section center / opposite slot openings |

`DIM_TOL` in `model.py` is assert slack (often 0.5 mm), **not** print clearance.
Print clearances belong in named params in `dims.md`.

## Design-spec template (before CadQuery)

Write these into `drawings/dims.md` (and ask A/B if any cell is ambiguous):

| Section | Must lock |
| --- | --- |
| Axes | World frame + local feature frames (sketch or bullet diagram) |
| Mates | Mating part, envelope dims, clearance policy |
| Fasteners | Size, count, axis, distance from seated end / slot rule |
| Join ops | Named boolean/construction op **and** operand solids (not prose alone) |
| Openings | Local open direction for pockets/U-cradles |
| Interfaces | Mount faces, flat pads, assembly access |
| Print | Bed face, overhang/support budget, or redesign until acceptable |
| Stop rule | When to re-open A/B vs keep patching (prefer re-spec after repeated Phase E fails) |

## Ambiguous 3D prose (lock ops, don’t invent)

Phrases that look clear in chat are often under-specified. Before `model.py`:

| Phrase class | Failure mode | Lock before coding |
| --- | --- | --- |
| “hull / fuse / connect” | Loft ribbon, gap, or filled pocket from wrong proxy | Named op + operands (e.g. convex hull of `core_proxy` × `stop_proxy`) |
| “flip the U / open up” | +Z vs −Z both plausible | Explicit open direction in local frame |
| “90° / 120° / cube corner” | Planar spacing ≠ mutually orthogonal axes | Pairwise angles + top-view projection + derived splay |
| “hole here” | Empty pocket ≠ through-wall hole | Probe/assert material that must be void (e.g. wall mid) |

Rule: if the user says hull / loft / fillet / neck, write the **boolean or
construction op** and the **operand solids** into `drawings/dims.md` before
`model.py`. Re-open the A/B gate when gallery shows a gap or ribbon instead of
a filled join.

## Cautionary archive (not an exemplar)

[`tripod_head_openbeam_15`](../../docs/postmortems/tripod_head_openbeam_15.md)
is an archived **partial** language→CAD attempt (functional mates, poor FDM
overhangs, heavy iteration). Do not treat it as the skill_8 happy path; use it
only when returning to that deferred redesign.
