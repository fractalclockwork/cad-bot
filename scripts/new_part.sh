#!/usr/bin/env bash
# Scaffold parts/<name>/ from parts/_template/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="${1:-}"

if [[ -z "$NAME" || "$NAME" == "-h" || "$NAME" == "--help" ]]; then
  echo "Usage: $0 <part-name>"
  echo "  Creates parts/<part-name>/ from parts/_template/"
  exit 0
fi

if [[ "$NAME" =~ [^a-z0-9_-] ]]; then
  echo "ERROR: part name must be lowercase alphanumeric / _ / -" >&2
  exit 1
fi

DEST="$ROOT/parts/$NAME"
if [[ -e "$DEST" ]]; then
  echo "ERROR: already exists: $DEST" >&2
  exit 1
fi

TEMPLATE="$ROOT/parts/_template"
if [[ ! -d "$TEMPLATE" ]]; then
  echo "ERROR: missing template: $TEMPLATE" >&2
  exit 1
fi

cp -a "$TEMPLATE" "$DEST"
# Replace PART_NAME placeholder in text files
while IFS= read -r -d '' f; do
  if grep -q 'PART_NAME' "$f" 2>/dev/null; then
    sed -i "s/PART_NAME/${NAME}/g" "$f"
  fi
done < <(find "$DEST" -type f \( -name '*.py' -o -name '*.md' \) -print0)

echo "Created $DEST"
echo "Next:"
echo "  1. Fill parts/$NAME/drawings/dims.md (+ images)"
echo "  2. Implement parts/$NAME/model.py"
echo "  3. PART=$NAME ./scripts/run_pipeline.sh --skip-human"
