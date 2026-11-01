---
name: skill_4_human_verify
description: >-
  Staged human verification for each stl3d preview view in parts/ or
  assemblies/ views.py. Records human_review.json; archives under docs/reviews/.
---

# Human Verification (per view)

Use after `skill_3_render_preview` / `assert_previews.py` pass.

Exact criteria live in `parts/<PART>/views.py` or `assemblies/<PART>/views.py` and gallery captions. The interactive 3D panel is an **aid** only — Phase E decisions are per orthographic PNG.

## How to run

```bash
PART=<name> ./scripts/open_gallery.sh
PART=<name> ./scripts/human_verify.sh
PART=<name> docker compose run --rm -e PART cad uv run python /work/scripts/assert_human_review.py
```

Or: `PART=<name> ./scripts/run_pipeline.sh` (A–E). Auto-only: `--skip-human`.

## Pass criteria

- `output/<PART>/previews/human_review.json` exists
- `overall == "pass"`; every required view `status == "pass"`

## On failure

- Fix model/render → re-run Phase D → re-do human review
- Archives: `docs/reviews/<PART>_human_review_…json`
