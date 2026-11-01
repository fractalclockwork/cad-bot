#!/usr/bin/env bash
# Serve output/<PART>/previews on http://127.0.0.1:8765 (avoids Snap Firefox file:// blocks).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PART="${PART:-kp08}"
PORT="${GALLERY_PORT:-8765}"
DIR="$ROOT/output/$PART/previews"

if [[ ! -d "$DIR" ]]; then
  echo "ERROR: $DIR missing. Run PART=$PART ./scripts/run_pipeline.sh --skip-human first." >&2
  exit 1
fi

URL="http://127.0.0.1:${PORT}/"
echo "PART=$PART"
echo "Serving $DIR"
echo "Open: $URL"
echo "(Ctrl-C to stop)"
cd "$DIR"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
