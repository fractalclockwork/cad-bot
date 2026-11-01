#!/usr/bin/env bash
# Phase A→E: preflight → CadQuery → CAD asserts → previews → human review gate.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PART="${PART:-kp08}"
export PART

SKIP_HUMAN=0
for arg in "$@"; do
  case "$arg" in
    --skip-human) SKIP_HUMAN=1 ;;
    -h|--help)
      echo "Usage: PART=<name> $0 [--skip-human]"
      echo "  PART           part under parts/ or assembly under assemblies/ (default: kp08)"
      echo "  --skip-human   skip interactive Phase E (CI / auto checks only)"
      exit 0
      ;;
  esac
done

compose_run() {
  docker compose run --rm -e "PART=${PART}" cad "$@"
}

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker not found on host. Install Docker, then retry." >&2
  exit 1
fi
if ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: docker compose not available. Install Docker Compose v2+, then retry." >&2
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker daemon not reachable. Start Docker, then retry." >&2
  exit 1
fi

MODEL=""
KIND=""
if [[ -d "$ROOT/parts/$PART" ]]; then
  MODEL="/work/parts/${PART}/model.py"
  KIND="part"
elif [[ -d "$ROOT/assemblies/$PART" ]]; then
  MODEL="/work/assemblies/${PART}/model.py"
  KIND="assembly"
else
  echo "ERROR: PART=$PART not found under parts/ or assemblies/" >&2
  exit 1
fi

echo "==> PART=$PART ($KIND)"
echo "==> Ensuring image cad-bot:latest"
docker compose build

echo "==> Phase A: environment preflight"
compose_run uv run python /work/scripts/preflight.py

echo "==> Phase B: CadQuery geometry + export"
compose_run uv run python "$MODEL" "/work/output/${PART}"

echo "==> Phase C: artifact verification matrix"
compose_run uv run python /work/scripts/assert_artifacts.py

echo "==> Phase D: headless preview renders + auto preview asserts"
compose_run uv run python /work/scripts/render_previews.py
compose_run uv run python /work/scripts/assert_previews.py

if [[ "$SKIP_HUMAN" -eq 1 ]]; then
  echo "==> Phase E: human review SKIPPED (--skip-human)"
  echo "WARNING: release/sign-off requires PART=$PART ./scripts/human_verify.sh" >&2
else
  echo "==> Phase E: staged human verification (each view)"
  echo "Gallery: PART=$PART ./scripts/open_gallery.sh"
  if [[ ! -t 0 ]]; then
    echo "ERROR: Phase E needs an interactive TTY. Re-run in a terminal, or pass --skip-human." >&2
    exit 1
  fi
  PART="$PART" ./scripts/human_verify.sh
  compose_run uv run python /work/scripts/assert_human_review.py
fi

echo "PIPELINE PASS (PART=$PART)"
