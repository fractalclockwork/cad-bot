#!/usr/bin/env bash
# Scaffold assemblies/<name>/ from assemblies/_template/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="${1:-}"

if [[ -z "$NAME" || "$NAME" == "-h" || "$NAME" == "--help" ]]; then
  echo "Usage: $0 <assembly-name>"
  echo "  Creates assemblies/<assembly-name>/ from assemblies/_template/"
  exit 0
fi

if [[ "$NAME" =~ [^a-z0-9_-] ]]; then
  echo "ERROR: assembly name must be lowercase alphanumeric / _ / -" >&2
  exit 1
fi

DEST="$ROOT/assemblies/$NAME"
if [[ -e "$DEST" ]]; then
  echo "ERROR: already exists: $DEST" >&2
  exit 1
fi

TEMPLATE="$ROOT/assemblies/_template"
if [[ ! -d "$TEMPLATE" ]]; then
  echo "ERROR: missing template: $TEMPLATE" >&2
  exit 1
fi

cp -a "$TEMPLATE" "$DEST"
while IFS= read -r -d '' f; do
  if grep -q 'ASSY_NAME' "$f" 2>/dev/null; then
    sed -i "s/ASSY_NAME/${NAME}/g" "$f"
  fi
done < <(find "$DEST" -type f \( -name '*.py' -o -name '*.md' \) -print0)

echo "Created $DEST"
echo "Next:"
echo "  1. Fill assemblies/$NAME/drawings/dims.md (BOM + mates)"
echo "  2. Wire parts in assemblies/$NAME/model.py"
echo "  3. PART=$NAME ./scripts/run_pipeline.sh --skip-human"
