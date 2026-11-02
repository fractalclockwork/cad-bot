# cad-bot

Docker-reproducible **CadQuery** pipeline for parametric parts and assemblies: build → export → assert → headless previews (plus interactive STL) → staged human review.

Reference part: [`parts/kp08/`](parts/kp08/). First assembly: [`assemblies/plate_kp08_shaft/`](assemblies/plate_kp08_shaft/).

## Requirements

- Docker + Docker Compose
- Browser for the preview gallery
- Interactive TTY for human sign-off (Phase E)

CAD tools stay in the image — nothing installed on the host.

## Quick start

```bash
docker compose build
PART=kp08 ./scripts/run_pipeline.sh --skip-human
PART=kp08 ./scripts/open_gallery.sh          # http://127.0.0.1:8765/

PART=plate_kp08_shaft ./scripts/run_pipeline.sh --skip-human   # assembly
```

Artifacts: `output/<name>/<name>.{step,stl}` and `previews/` (orthographic PNGs + `model.stl`).

## Docs (reading order)

| Doc | Role |
| --- | --- |
| [`docs/getting-started.md`](docs/getting-started.md) | Clone, first runs, gallery |
| [`docs/pipeline.md`](docs/pipeline.md) | Phases A–E, artifact matrix |
| [`docs/verification.md`](docs/verification.md) | Gates + lessons (parts & assemblies) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Add a part or assembly |
| [`AGENTS.md`](AGENTS.md) | Skill index + `PART` rules |
| [`parts/README.md`](parts/README.md) / [`assemblies/README.md`](assemblies/README.md) | Layout conventions |
| [`roadmap/README.md`](roadmap/README.md) | Feature roadmap (CadQuery proving ground → build123d endgate) |

## Tooling

| Role | Tool |
| --- | --- |
| CAD | CadQuery 2.4 (uv, Docker) |
| Previews | trimesh + matplotlib; Three.js gallery |
| Human gate | `human_verify.sh` |
| Orchestrator | `scripts/run_pipeline.sh` |

## License

MIT — see [`LICENSE`](LICENSE).
