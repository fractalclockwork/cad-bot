---
name: skill_4_human_verify
description: >-
  Staged human verification for each preview view defined in parts/$PART/views.py.
  Records output/$PART/previews/human_review.json and archives under docs/reviews/.
---

# Human Verification (per view)

Use after `skill_3_render_preview` and `assert_previews.py` pass.

Exact criteria live in `parts/<PART>/views.py` and gallery captions.

## How to run

```bash
PART=kp08 ./scripts/open_gallery.sh    # preferred over file://
PART=kp08 ./scripts/human_verify.sh
PART=kp08 docker compose run --rm -e PART cad uv run python /work/scripts/assert_human_review.py
```

Or: `PART=kp08 ./scripts/run_pipeline.sh` (Phases A–E).

Auto-only (not for sign-off): `--skip-human`.

## Pass criteria

- `output/<PART>/previews/human_review.json` exists
- `overall == "pass"`; every view `status == "pass"`

## On failure

- Fix model/render for failed views → re-run Phase D → re-do human review
- Archives land in `docs/reviews/<PART>_human_review_…json`
