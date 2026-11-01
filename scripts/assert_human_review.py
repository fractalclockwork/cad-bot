#!/usr/bin/env python3
"""Assert that human review JSON exists and every view passed."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from part_config import ensure_part_layout, load_views, resolve  # noqa: E402


def fail(msg: str) -> None:
    print(f"ASSERT FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    paths = ensure_part_layout(resolve())
    views_mod = load_views(paths)
    review_schema = getattr(views_mod, "REVIEW_SCHEMA_VERSION", 1)
    review_path = paths.review_json

    if not review_path.is_file():
        fail(
            f"missing {review_path}. Run PART={paths.name} ./scripts/human_verify.sh "
            "after reviewing previews."
        )

    data = json.loads(review_path.read_text(encoding="utf-8"))
    if int(data.get("schema_version", -1)) != review_schema:
        fail(
            f"unsupported human_review schema_version={data.get('schema_version')}; "
            f"expected {review_schema}"
        )

    if data.get("overall") != "pass":
        fail(f"human review overall={data.get('overall')!r} (expected 'pass')")

    by_key = {row["key"]: row for row in data.get("views", [])}
    for view in views_mod.VIEWS:
        row = by_key.get(view.key)
        if row is None:
            fail(f"human review missing view '{view.key}'")
        if row.get("status") != "pass":
            note = row.get("note") or ""
            fail(
                f"view '{view.key}' status={row.get('status')!r} "
                f"(expected 'pass') note={note!r}"
            )
        print(f"OK human:{view.key} pass")

    print(f"OK reviewed_at={data.get('reviewed_at')}")
    print("HUMAN REVIEW PASS")


if __name__ == "__main__":
    main()
