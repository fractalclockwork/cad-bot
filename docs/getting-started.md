# Getting started

## Clone and build

```bash
git clone <repo-url> cad-bot
cd cad-bot
docker compose build
```

## First KP08 run (auto gates only)

```bash
PART=kp08 ./scripts/run_pipeline.sh --skip-human
```

This runs Phases A–D: preflight → CadQuery → artifact asserts → preview renders + ink checks.

Outputs under `output/kp08/`:

| Path | Description |
| --- | --- |
| `kp08.step` / `kp08.stl` | Solid + mesh |
| `kp08_profile.dxf` | Top mounting profile |
| `previews/*.png` | Per-view images |
| `previews/index.html` | Gallery with criteria |

## Preview gallery

Snap/AppArmor Firefox often blocks `file://`. Prefer HTTP:

```bash
PART=kp08 ./scripts/open_gallery.sh
# → http://127.0.0.1:8765/
```

## Human sign-off

```bash
PART=kp08 ./scripts/open_gallery.sh   # leave running
PART=kp08 ./scripts/human_verify.sh   # y/n per view
```

Or one shot: `PART=kp08 ./scripts/run_pipeline.sh` (needs a TTY).

## New part

```bash
./scripts/new_part.sh my_part
# edit parts/my_part/{drawings,model.py,views.py}
PART=my_part ./scripts/run_pipeline.sh --skip-human
```

See [`CONTRIBUTING.md`](../CONTRIBUTING.md) and `skill_5_drawing_to_cadquery`.

## Makefile shortcuts (optional)

```bash
make build
make pipeline-auto    # PART=kp08 --skip-human
make gallery
make new-part NAME=foo
```
