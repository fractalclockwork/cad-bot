# Getting started

## Clone and build

```bash
git clone <repo-url> cad-bot
cd cad-bot
docker compose build
```

## First part run (KP08, auto gates)

```bash
PART=kp08 ./scripts/run_pipeline.sh --skip-human
```

Phases A–D: preflight → CadQuery → STEP/STL asserts → STL previews + gallery.

Outputs under `output/kp08/`:

| Path | Description |
| --- | --- |
| `kp08.step` / `kp08.stl` | Solid + mesh |
| `previews/*.png` | Orthographic views |
| `previews/model.stl` | Interactive gallery mesh |
| `previews/index.html` | Gallery |

## First assembly run

```bash
PART=plate_kp08_shaft ./scripts/run_pipeline.sh --skip-human
```

Same pipeline; `PART` resolves under `assemblies/` when not in `parts/`.

## Preview gallery

Prefer HTTP (Snap Firefox often blocks `file://`):

```bash
PART=kp08 ./scripts/open_gallery.sh
# → http://127.0.0.1:8765/  (orbit 3D + PNG cards)
```

## Human sign-off

```bash
PART=kp08 ./scripts/open_gallery.sh   # leave running
PART=kp08 ./scripts/human_verify.sh   # y/n per orthographic view
```

Or: `PART=kp08 ./scripts/run_pipeline.sh` (needs a TTY).

## New part / assembly

```bash
./scripts/new_part.sh my_part
PART=my_part ./scripts/run_pipeline.sh --skip-human

./scripts/new_assembly.sh my_assy
PART=my_assy ./scripts/run_pipeline.sh --skip-human
```

See [`CONTRIBUTING.md`](../CONTRIBUTING.md), `skill_5_drawing_to_cadquery`, `skill_6_assembly_workflow`.

## Makefile

```bash
make build
make pipeline-auto          # PART=kp08 --skip-human
make gallery
make new-part NAME=foo
make new-assembly NAME=bar
```
