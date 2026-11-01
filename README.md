# cad-bot

Docker-reproducible **CadQuery** pipeline for parametric mechanical parts: build → export → assert → headless previews → staged human review.

Reference part: [`parts/kp08/`](parts/kp08/) (8 mm bore pillow block).

## Requirements

- Docker + Docker Compose
- Browser (for previews)
- Interactive TTY for human sign-off (Phase E)

CAD tools stay inside the image — nothing installed on the host.

## Quick start

```bash
docker compose build
PART=kp08 ./scripts/run_pipeline.sh --skip-human
PART=kp08 ./scripts/open_gallery.sh   # http://127.0.0.1:8765/
```

Full sign-off (interactive): `PART=kp08 ./scripts/run_pipeline.sh`

Artifacts: `output/<part>/<part>.{step,stl}`, `<part>_profile.dxf`, `previews/`.

## Docs

| Doc | Role |
| --- | --- |
| [`docs/getting-started.md`](docs/getting-started.md) | Clone, build, first KP08 run, gallery |
| [`docs/pipeline.md`](docs/pipeline.md) | Phases A–E, artifact matrix |
| [`docs/verification.md`](docs/verification.md) | Auto + human gates, KP08 lessons |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Add a part / assembly |
| [`AGENTS.md`](AGENTS.md) | Skill index + `PART` conventions |
| [`parts/README.md`](parts/README.md) | Part layout |
| [`assemblies/README.md`](assemblies/README.md) | Future multi-body contract |

## Tooling

| Role | Tool |
| --- | --- |
| CAD | CadQuery 2.4 (uv, Docker) |
| Previews | trimesh + matplotlib + ezdxf |
| Human gate | `human_verify.sh` |
| Orchestrator | `scripts/run_pipeline.sh` |

## License

MIT — see [`LICENSE`](LICENSE).
