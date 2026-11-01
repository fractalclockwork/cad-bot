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
PART=plate_mcm_1434k33_shaft ./scripts/run_pipeline.sh --skip-human
```

## Part lessons (KP08)

- Lock axes before modeling: X = bolt pitch, Y = shaft, Z = up.
- Hole pitch (**e**) ≠ overall length (**a**) unless the drawing says so.
- Auto PNG ink checks do not catch wrong-axis designs — plan Phase E.
- Archive every review under `docs/reviews/`.

View intent (KP08): front → bore as circle; top → two bolt holes; right → bore along Y.

## Human conflict resolution (assemblies)

Auto A–D does not catch wrong-axis mates. **Humans** resolve mate conflicts:

1. Measure bore vs mount-hole axes; classify pillow vs flange.
2. If ambiguous or intent conflicts with geometry → stop coding; ask 1–2 A/B with **only valid** options; list plate cutouts in the same turn.
3. Lock chosen mates in `drawings/dims.md`, then implement.
4. Gallery / Phase E orientation fail → new conflict cycle (re-ask; never silent-guess).

See skill_6 **Human conflict resolution**.

## Assembly lessons (`plate_kp08_shaft`)

- Compose only via `parts/*/build_part()` + explicit `cq.Location` mates.
- Sit-on-plate: child `Z = plate_thickness`.
- Shaft through bore: `Z = plate_thickness + base_center_height`.
- Assert volume ≈ sum of part volumes; BB matches envelope.
- New solid instance per occurrence (do not reuse one Shape twice in `cq.Assembly`).

## Assembly lessons (`plate_mcm_1434k33_shaft` — flange)

- Measure bore vs mount-hole axes **before** A/B mate questions (skill_6 pre-mate gate).
- Flange units have shaft ∥ bolts: flange on a plate ⇒ shaft **through** that plate (along Z), not parallel to it.
- Plate needs bolt holes **and** shaft (or hub) clearance; do not copy pillow-block hole-only plates.
- Do not offer geometrically impossible A/B options (e.g. flange bolted to plate with shaft ∥ plate).
- First wrong mate (shaft ∥ plate) was rejected in human/gallery review; corrected via a new A/B cycle to thru-plate.

See `skill_6_assembly_workflow`.

## Archived partial: `tripod_head_openbeam_15`

Functional sockets/bolts after heavy churn, but **not** print-ready (overhangs)
and **not** a language→CAD exemplar. See
[`postmortems/tripod_head_openbeam_15.md`](postmortems/tripod_head_openbeam_15.md).
Return only after stronger design-spec / FDM gates.

## Archive policy

`human_verify.py` writes `output/<name>/previews/human_review.json` and copies to
`docs/reviews/<name>_human_review_<UTC>_<pass|fail>.json`.
