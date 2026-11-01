#!/usr/bin/env bash
# Host wrapper: interactive human review for each preview view.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PART="${PART:-kp08}"
export PART
PREVIEWS="$ROOT/output/$PART/previews"

if [[ ! -d "$PREVIEWS" ]]; then
  echo "ERROR: $PREVIEWS missing. Run PART=$PART ./scripts/run_pipeline.sh through Phase D first." >&2
  exit 1
fi

if [[ ! -t 0 ]]; then
  echo "ERROR: need an interactive terminal." >&2
  exit 1
fi

echo "PART=$PART"
echo "Gallery: prefer PART=$PART ./scripts/open_gallery.sh"
echo "Or open: $PREVIEWS/index.html"
exec docker compose run --rm -it -e "PART=${PART}" cad uv run python /work/scripts/human_verify.py
