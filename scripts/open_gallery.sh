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

# Always clear a prior gallery http.server on this port (stale agent/shell runs).
if pgrep -f "python3 -m http.server ${PORT}" >/dev/null 2>&1; then
  echo "Port ${PORT} busy; stopping prior python3 http.server"
  pkill -f "python3 -m http.server ${PORT}" 2>/dev/null || true
  # Wait until the port is free (up to ~2s)
  for _ in 1 2 3 4 5 6 7 8; do
    if ! ss -tln 2>/dev/null | grep -qE ":${PORT}\\s"; then
      break
    fi
    sleep 0.25
  done
fi

echo "PART=$PART"
echo "Serving $DIR"
echo "Open: $URL"
echo "(Ctrl-C to stop)"
cd "$DIR"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
