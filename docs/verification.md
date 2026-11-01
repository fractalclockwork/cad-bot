# Verification

Auto gates plus staged human review. Phase/artifact tables live in [`pipeline.md`](pipeline.md); this file records **how to judge** and lessons learned.

## Gates (summary)

| Phase | Type | Pass rule |
| --- | --- | --- |
| A–C | Auto | Env + solid/assembly + STEP/STL |
| D | Auto | Orthographic PNG ink/size; gallery + `model.stl` |
| E | Human | Per-view y/n in `human_review.json` |

Interactive 3D in the gallery is an **aid** — Phase E still uses orthographic PNG criteria.

```bash
PART=kp08 ./scripts/run_pipeline.sh --skip-human
PART=plate_kp08_shaft ./scripts/run_pipeline.sh --skip-human
```

## Part lessons (KP08)

- Lock axes before modeling: X = bolt pitch, Y = shaft, Z = up.
- Hole pitch (**e**) ≠ overall length (**a**) unless the drawing says so.
- Auto PNG ink checks do not catch wrong-axis designs — plan Phase E.
- Archive every review under `docs/reviews/`.

View intent (KP08): front → bore as circle; top → two bolt holes; right → bore along Y.

## Assembly lessons (`plate_kp08_shaft`)

- Compose only via `parts/*/build_part()` + explicit `cq.Location` mates.
- Sit-on-plate: child `Z = plate_thickness`.
- Shaft through bore: `Z = plate_thickness + base_center_height`.
- Assert volume ≈ sum of part volumes; BB matches envelope.
- New solid instance per occurrence (do not reuse one Shape twice in `cq.Assembly`).

See `skill_6_assembly_workflow`.

## Archive policy

`human_verify.py` writes `output/<name>/previews/human_review.json` and copies to
`docs/reviews/<name>_human_review_<UTC>_<pass|fail>.json`.
