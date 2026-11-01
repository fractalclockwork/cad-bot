#!/usr/bin/env python3
"""Verify headless preview artifacts under ./output/<PART>/previews (STL views)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from part_config import ensure_part_layout, load_views, resolve  # noqa: E402

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MIN_NON_WHITE_RATIO = 0.01
MIN_PNG_BYTES_STL = 15_000


def fail(msg: str) -> None:
    print(f"ASSERT FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def ink_stats(path: Path) -> tuple[float, int]:
    img = Image.open(path).convert("RGB")
    arr = np.asarray(img)
    non_white = int(np.sum(np.any(arr < 250, axis=2)))
    ratio = float(non_white) / float(arr.shape[0] * arr.shape[1])
    return ratio, non_white


def main() -> None:
    paths = ensure_part_layout(resolve())
    views_mod = load_views(paths)
    previews = paths.previews

    if not previews.is_dir():
        fail(f"previews directory missing: {previews}")

    stl_views = [v for v in views_mod.VIEWS if v.kind == "stl3d"]
    if not stl_views:
        fail(f"no stl3d views defined in {paths.views}")

    for view in stl_views:
        path = previews / view.filename
        if not path.is_file() or path.stat().st_size <= 0:
            fail(f"missing/empty preview for view '{view.key}': {path}")
        if path.read_bytes()[:8] != PNG_MAGIC:
            fail(f"not a PNG for view '{view.key}': {path}")
        size = path.stat().st_size
        if size < MIN_PNG_BYTES_STL:
            fail(
                f"view '{view.key}' PNG too small ({size} bytes < {MIN_PNG_BYTES_STL}); "
                "likely blank/white-on-white"
            )
        ratio, non_white = ink_stats(path)
        if ratio < MIN_NON_WHITE_RATIO:
            fail(
                f"view '{view.key}' looks blank "
                f"(non_white_ratio={ratio:.4f} < {MIN_NON_WHITE_RATIO}, pixels={non_white})"
            )
        print(
            f"OK {view.key}: {path.name} ({size} bytes, non_white_ratio={ratio:.3f})"
        )

    model_stl = previews / "model.stl"
    if not model_stl.is_file() or model_stl.stat().st_size <= 0:
        fail(f"missing gallery model.stl: {model_stl}")
    print(f"OK model.stl ({model_stl.stat().st_size} bytes)")

    index = previews / "index.html"
    if not index.is_file() or index.stat().st_size <= 0:
        fail(f"missing gallery: {index}")
    print(f"OK index.html ({index.stat().st_size} bytes)")

    print("PREVIEW MATRIX PASS")


if __name__ == "__main__":
    main()
