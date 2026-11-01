# Pipeline

Orchestrator: `PART=<name> ./scripts/run_pipeline.sh [--skip-human]`

Default `PART=kp08`. Compose receives `PART` for every container step.

## Phases

| Phase | Script | Pass rule |
| --- | --- | --- |
| A | `preflight.py` | uv, CadQuery, writable `output/`, `parts/<PART>/model.py` |
| B | `parts/<PART>/model.py` | Valid solid, drawing-bound asserts, export |
| C | `assert_artifacts.py` | `output/<PART>/{part}.step|.stl|{part}_profile.dxf` |
| D | `render_previews.py` + `assert_previews.py` | PNG magic, size, ink ratio; SVG; gallery |
| E | `human_verify.py` + `assert_human_review.py` | Every view `status=pass` (skipped with `--skip-human`) |

```
parts/<name>/drawings  →  skill_5 (author)  →  parts/<name>/model.py
        ↓
PART=name run_pipeline  →  output/<name>/artifacts + previews
        ↓
skill_4 human verify    →  docs/reviews/<name>_…
```

## Artifact matrix

| Artifact | Path |
| --- | --- |
| STEP | `output/<part>/<part>.step` |
| STL | `output/<part>/<part>.stl` |
| Profile DXF | `output/<part>/<part>_profile.dxf` |
| Previews | `output/<part>/previews/{iso,front,…}.png` |
| Gallery | `output/<part>/previews/index.html` |
| Human review | `output/<part>/previews/human_review.json` |

Views and criteria come from `parts/<PART>/views.py` (loaded via `scripts/part_config.py`).

## Helpers

| Script | Role |
| --- | --- |
| `docker_cad.sh` | Pass-through `PART` into compose |
| `open_gallery.sh` | HTTP serve previews on `:8765` |
| `new_part.sh` | Scaffold from `parts/_template/` |
