#!/usr/bin/env bash
# Run CadQuery / uv commands inside the cad-bot Compose service.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PART="${PART:-kp08}"
export PART

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker not found on host. Install Docker, then retry." >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: docker compose not available. Install Docker Compose v2+, then retry." >&2
  exit 1
fi

ensure_image() {
  if ! docker image inspect cad-bot:latest >/dev/null 2>&1; then
    echo "Image cad-bot:latest missing — running docker compose build..." >&2
    docker compose build
  fi
}

compose_run() {
  docker compose run --rm -e "PART=${PART}" cad "$@"
}

usage() {
  cat <<'EOF'
Usage: PART=<name> scripts/docker_cad.sh <command> [args...]

Commands:
  build              Build the cad-bot image
  shell              Interactive bash in the container
  uv [args...]       Run uv inside the container
  python [args...]   Run uv run python ...
  run [args...]      docker compose run --rm cad [args...]

Environment:
  PART               Part name under parts/ (default: kp08)
EOF
}

cmd="${1:-}"
shift || true

case "$cmd" in
  build)
    docker compose build
    ;;
  shell)
    ensure_image
    compose_run bash
    ;;
  uv)
    ensure_image
    compose_run uv "$@"
    ;;
  python)
    ensure_image
    compose_run uv run python "$@"
    ;;
  run)
    ensure_image
    compose_run "$@"
    ;;
  ""|-h|--help|help)
    usage
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    usage >&2
    exit 1
    ;;
esac
