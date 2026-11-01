# Pipeline

Orchestrator: `PART=<name> ./scripts/run_pipeline.sh [--skip-human]`

Default `PART=kp08`. `PART` names a directory under `parts/` **or** `assemblies/` (`parts/` wins if both exist).

## Phases

| Phase | Script | Pass rule |
| --- | --- | --- |
| A | `preflight.py` | uv, CadQuery, writable `output/`, model under parts or assemblies |
| B | `…/model.py` | Valid geometry, asserts, export STEP + STL |
| C | `assert_artifacts.py` | `output/<PART>/{name}.step` and `{name}.stl` |
| D | `render_previews.py` + `assert_previews.py` | stl3d PNGs; `model.stl`; gallery HTML |
| E | `human_verify.py` + `assert_human_review.py` | Every view `status=pass` (skip with `--skip-human`) |

```
parts/<name>/ or assemblies/<name>/
        ↓
PART=name run_pipeline  →  output/<name>/ + previews/
        ↓
skill_4 human verify    →  docs/reviews/<name>_…
```

## Artifact matrix

| Artifact | Path |
| --- | --- |
| STEP | `output/<name>/<name>.step` |
| STL | `output/<name>/<name>.stl` |
| Orthographic PNGs | `output/<name>/previews/{iso,front,…}.png` |
| Interactive 3D | `output/<name>/previews/model.stl` |
| Gallery | `output/<name>/previews/index.html` |
| Human review | `output/<name>/previews/human_review.json` |

Views: `stl3d` entries in `parts/<PART>/views.py` or `assemblies/<PART>/views.py`. DXF is not a pipeline gate.

## Helpers

| Script | Role |
| --- | --- |
| `docker_cad.sh` | Pass-through `PART` into compose |
| `open_gallery.sh` | HTTP serve previews on `:8765` |
| `new_part.sh` / `new_assembly.sh` | Scaffold templates |
