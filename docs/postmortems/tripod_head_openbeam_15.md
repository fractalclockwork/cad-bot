# Post-mortem: `tripod_head_openbeam_15`

**Status: partial success — deferred.** Do **not** cite this part as a skill_8
or FDM workflow exemplar. Geometry eventually reached functional sockets and
M3 through-holes, but printability (overhangs) was never locked, and the path
here was iterative agentic churn with diminishing returns. Return later after
stronger design-spec gates exist.

| | |
| --- | --- |
| Part | [`parts/tripod_head_openbeam_15/`](../../parts/tripod_head_openbeam_15/) |
| Assembly (premature) | [`assemblies/tripod_head_openbeam_15_legs/`](../../assemblies/tripod_head_openbeam_15_legs/) |
| Reviews | [`docs/reviews/tripod_head_openbeam_15_*.json`](../reviews/) |

## Verdict

| Claim | Reality |
| --- | --- |
| Functional mates | Eventually yes: identical U-cradles, clear channels, M3 through walls |
| Print-ready FDM | **No** — pad-down + splayed cradles leave severe overhangs; not gated pre-build |
| Proper language→CAD workflow | **No** — thin A/B, late geometry teaching, false-green asserts, multi-cycle patching |
| Teaching exemplar | **Forbidden** — archive only; revisit after process fixes |

## What was achieved

- Cube-corner layout: pairwise 90° axes, 120° top view, splay `asin(1/√3)`
- One +X arm (hull stop-proxy + U → channel → bolt) then rotate copies
- Flat mount pad; pipeline A–D green; human stopped at “looks fine” (geometry), not print sign-off

## What remains wrong for FDM

Printing with the mount pad on the bed puts splayed U-cradles at ~35° with
large unsupported faces. Print orientation and overhang/support budget were
never written into `dims.md` before CadQuery. A return pass must redesign
orientation and/or geometry for filament printing — not more pocket/bolt
tweaks.

## Friction timeline (chat 2026-11-01)

### 1. Thin A/B before first CadQuery

Only two hard A/B questions before first CadQuery (meaning of “7.5 mm”; attach
style). “Cube corner,” splay, mount pad, print bed face, and join method were
soft asides or invented defaults — not gated. Opening ask already required a
printable part (~0.2 mm) and resolve-conflicts-before-build; that rule was
stated and then violated in practice.

### 2. Layout drift

First builds used −X/−Y/−Z cube arms, then planar **120° + invented free
splay 30°** (“locked unless you object”) without a real human A/B. Human had
to re-teach (~10:16): top view 120° **and** pairwise 90° (cube corner viewed
toward center). Splay is fixed by geometry (`asin(1/√3)`), not a free
“printable” knob — the 30° invent ironically claimed to avoid overhangs.

### 3. Bolt semantics late

“7.5 mm from the socketed end” was partially locked, but T-slot centerline
alignment and wall-through readability failed Phase E before asserts caught
them.

### 4. Scope creep

An assembly was built and gallery-checked before the part was signed off.
User note: assembly was not requested yet — part first, then assembly.

### 5. Ambiguous 3D verbs

“Flip the U” and “hull between core and sockets” drove loft/ribbon joins and
wrong hull proxies — plans sometimes proceeded without waiting for A/B answers
on op + operands. A full cradle-envelope proxy filled pockets and buried
bolts; stop-back proxy + post-hull cuts were needed. Identical arms required
build-once-then-rotate, not per-azimuth remeshed hulls. Other late invents:
`hub_radius` ~14→22 (neighbor interference), cradle length 12→16, core/pad
added only after the user required a flat mount.

### 6. False greens

- Asserts treated empty pocket center as “bolt present.”
- M3 cutter on an XZ workplane used local offsets that parked the cylinder
  off the arm (**0 volume removed**); walls stayed solid until a world-XY
  placement fix (~53 mm³ then removed).
- Preview/image captions disagreed with point-in-solid probes; stale human
  passes were not invalidated on geometry change.
- Legs assembly archived as pass while the head was still failing verification.

| Review | Result | Signal |
| --- | --- | --- |
| `…T182920Z_pass.json` | pass | Early criteria; later invalidated by redesign |
| `…_legs_…T183229Z_pass.json` | pass | Assembly signed during head churn |
| `…T190456Z_pass.json` | pass | Hull/drop-in criteria; later invalidated |
| `…T191511Z_fail.json` | fail | right: “no bolt holes” |

### 7. Tooling friction

Gallery `EADDRINUSE` / stale `http.server` instances blocked review loops
(`open_gallery.sh` later hardened to kill the prior listener).

### 8. Diminishing returns

After sockets and bolts were functionally clear, further agentic
gallery→fail→patch cycles added friction without improving the real gap
(printability + upfront spec). Stop criterion should have been plan/postmortem
sooner.

## Root cause (process)

CadQuery started before a written **design spec** covering both kinematics
(mates, axes, join ops) and **FDM constraints** (bed face, overhangs,
supports). Language A/B was treated as sufficient when it only locked a
subset of critical decisions.

## How we should have specified earlier

Lock in `drawings/dims.md` **before** `model.py`:

1. Axes diagram (world + local cradle frame)
2. Mate style and mating part dims (with print clearance)
3. Fastener size, axis, and distance from seated end / T-slot rule
4. Join op + **named proxy solids** (not prose “hull”)
5. Feature open direction (U open ± local axis)
6. Mount / interface faces
7. **Print bed face + overhang/support plan** (or redesign until support-free
   enough for the stated printer)
8. Iteration stop rule (e.g. after N Phase E fails → re-spec, don’t patch)

## Prioritized follow-ups (later; not this archive pass)

1. **skill_8 design-spec template** — axes, mates, fasteners, join ops, bed
   face, overhang budget — mandatory before CadQuery
2. **Assert hygiene** — probes must hit material that should be void (e.g.
   wall mid for bolts), not already-empty pockets; expected cuts should remove
   nonzero volume
3. **Process** — part human pass before assembly; after repeated Phase E
   failures → plan/postmortem instead of more patches; never “defaults locked
   unless you object” for critical 3D geometry; invalidate archived human
   passes when the solid changes
4. **Return to this part** only after (1) and an explicit printability redesign

## Return-later backlog

- Redesign for FDM (orientation and/or cradle geometry to kill overhangs)
- Re-run part Phase E with print criteria in `views.py`
- Only then revisit `assemblies/tripod_head_openbeam_15_legs/`
