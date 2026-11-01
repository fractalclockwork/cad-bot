# Verification

Auto gates plus staged human review. Lessons from KP08 round-1 are kept here so the next part reuses the same process.

## Gates

| Phase | Type | Pass rule |
| --- | --- | --- |
| A | Auto | Docker image, uv, CadQuery, writable `output/`, part present |
| B | Auto | `isValid`, volume > 0, BB dims, **axis convention asserts** |
| C | Auto | STEP/STL/DXF size + entity/facet checks |
| D | Auto | PNG magic, min size, **non-white ink ratio**; gallery HTML |
| E | Human | `human_review.json` overall=pass and every view `status=pass` |

```bash
PART=kp08 ./scripts/run_pipeline.sh              # A–E
PART=kp08 ./scripts/run_pipeline.sh --skip-human # A–D
PART=kp08 ./scripts/human_verify.sh              # E alone
```

## View matrix

Canonical source: `parts/<PART>/views.py` (not shared scripts).

For KP08:

| Key | File | Intent |
| --- | --- | --- |
| `iso` | `iso.png` | 3D context |
| `front` | `front.png` | Look along shaft → bore is a **circle** |
| `top` | `top.png` | Mounting layout → **two** bolt holes |
| `right` | `right.png` | Side → bore runs **left/right** |
| `profile` | `profile.png` | 2D XY base → **two** holes only |

## Gate history (KP08)

| Gate | Status | Notes |
| --- | --- | --- |
| V0 toolchain | PASS | CadQuery 2.4, uv image |
| V1 preflight | PASS | |
| V2 geometry | PASS | Drawing-matched dims |
| V3 artifacts | PASS | |
| V4 previews | PASS | Ink-density asserts; black-on-white DXF |
| V5 human | Implemented | Phase E; archive under `docs/reviews/` |

## KP08 human round-1 (FAIL → design change)

Archive: `docs/reviews/kp08_human_review_20261101T143629Z_fail.json`

| View | Human | Root cause |
| --- | --- | --- |
| iso / front / right | fail | Shaft along **X**; needed **Y** |
| top | pass | Base layout OK |
| profile | fail | Spurious center hole on XY DXF |

### Corrections

1. Axes: X = bolt pitch, Y = shaft, Z = up — asserted in model.
2. Boss + bore along Y.
3. Profile DXF = capsule + two flange holes only.
4. View criteria updated to name expected bore appearance per view.

### Drawing dims (front elevation)

| Label | Meaning | Value | Param |
| --- | --- | --- | --- |
| a | overall length | 55 | `overall_length` |
| e | hole C–C | 42 | `bolt_hole_pitch` |
| s | hole Ø | 4.8 | `bolt_hole_diameter` |
| h | center height | 15 | `base_center_height` |
| g | base thickness | 5 | `base_thickness` |
| w | overall height | 29 | `overall_height` |

Lesson: **hole pitch ≠ overall length**; bind drawing letters before first human review.

## Process refinements (next part)

1. Lock X/Y/Z in model docstring and `views.py` before modeling.
2. Separate mounting drawing from shaft section in DXF.
3. Human criteria must name bore appearance per view.
4. Archive every `human_review.json` under `docs/reviews/<part>_…`.
5. Re-run Phase E after any geometry change.
6. Prefer one failed human round → explicit design delta before regenerating.

## Archive policy

`human_verify.py` writes live `output/<part>/previews/human_review.json` and copies to
`docs/reviews/<part>_human_review_<UTC>_<pass|fail>.json`.
