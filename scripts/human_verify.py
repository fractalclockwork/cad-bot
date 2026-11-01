#!/usr/bin/env python3
"""Interactive per-view human verification gate (run with a TTY)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from part_config import ensure_part_layout, load_views, resolve, work_root  # noqa: E402


def fail(msg: str) -> None:
    print(f"HUMAN VERIFY FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def ask_pass(prompt: str) -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in {"y", "yes"}:
            return True
        if ans in {"n", "no"}:
            return False
        print("Please answer y or n.")


def main() -> None:
    paths = ensure_part_layout(resolve())
    views_mod = load_views(paths)
    previews = paths.previews
    review_schema = getattr(views_mod, "REVIEW_SCHEMA_VERSION", 1)

    if not previews.is_dir():
        fail(f"previews missing at {previews}; run Phase D first")

    if not sys.stdin.isatty():
        fail(
            "stdin is not a TTY. Run interactively:\n"
            "  PART=<name> ./scripts/human_verify.sh"
        )

    gallery = previews / "index.html"
    print("=" * 60)
    print(f"Human verification — {paths.name} — one decision per view")
    print(f"Gallery: {gallery}")
    print("Prefer: PART=<name> ./scripts/open_gallery.sh  (localhost; avoids Snap file://)")
    print("=" * 60)

    views_out = []
    all_pass = True
    for view in views_mod.VIEWS:
        path = previews / view.filename
        print()
        print("-" * 60)
        print(f"View: {view.title}  [{view.key}]")
        print(f"File: {path}")
        if not path.is_file():
            print("WARNING: preview file missing")
        print("Criteria:")
        for c in view.criteria:
            print(f"  - {c}")
        ok = ask_pass("Pass this view? [y/n]: ")
        note = ""
        if not ok:
            all_pass = False
            note = input("Optional note (why it failed): ").strip()
        views_out.append(
            {
                "key": view.key,
                "filename": view.filename,
                "title": view.title,
                "status": "pass" if ok else "fail",
                "note": note,
                "criteria": list(view.criteria),
            }
        )

    payload = {
        "schema_version": review_schema,
        "part": paths.name,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "overall": "pass" if all_pass else "fail",
        "views": views_out,
    }
    review_path = paths.review_json
    review_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print()
    print(f"Wrote {review_path}")
    print(f"OVERALL: {payload['overall'].upper()}")

    archive_dir = work_root() / "docs" / "reviews"
    try:
        archive_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        archive_path = archive_dir / f"{paths.name}_human_review_{stamp}_{payload['overall']}.json"
        archive_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Archived {archive_path}")
    except OSError as exc:
        print(f"WARNING: could not archive review: {exc}", file=sys.stderr)

    if not all_pass:
        raise SystemExit(1)
    print("HUMAN VERIFY PASS")


if __name__ == "__main__":
    main()
