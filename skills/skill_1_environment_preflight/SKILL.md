---
name: skill_1_environment_preflight
description: >-
  Validate the cad-bot Docker + uv + CadQuery environment, writable output/,
  and parts/$PART or assemblies/$PART before any geometry synthesis.
---

# Environment Preflight

Run **before** generating or exporting CAD geometry.

## Requirements

- Host: Docker + Docker Compose
- Image: `cad-bot:latest` (`docker compose build`)
- CadQuery via `uv run` inside the container
- `./output/`, `./parts/`, `./assemblies/` mounted; `PART` set (default `kp08`)

## How to run

```bash
PART=kp08 ./scripts/docker_cad.sh build   # if image missing
PART=kp08 ./scripts/run_pipeline.sh --skip-human   # Phase A included
# or:
PART=kp08 docker compose run --rm -e PART cad uv run python /work/scripts/preflight.py
```

## Pass criteria

- `uv` on PATH; `import cadquery` succeeds
- `/work/output` writable; `/work/parts` readable
- Target resolved: `parts/$PART/model.py` **or** `assemblies/$PART/model.py`
- Prints `PREFLIGHT PASS`, exit 0

## On failure

- Missing Docker → install/start Docker; do **not** install CadQuery on the host
- Missing image → `docker compose build`
- Missing target → `./scripts/new_part.sh <name>` or `./scripts/new_assembly.sh <name>` or fix `PART`
