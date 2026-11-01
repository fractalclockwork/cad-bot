#!/usr/bin/env python3
"""Per-view definitions for mcm_1434k33 (McMaster 1434K33 flange bearing)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViewSpec:
    key: str
    filename: str
    title: str
    kind: str
    criteria: tuple[str, ...]


# X = flange long / bolts, Y = shaft, Z = flange short
VIEWS: tuple[ViewSpec, ...] = (
    ViewSpec(
        key="iso",
        filename="iso.png",
        title="Isometric",
        kind="stl3d",
        criteria=(
            "Two-bolt flange housing silhouette is visible",
            "Bearing / shaft opening faces along Y",
            "Flange elongated along X",
            "Part is not clipped; coherent solid",
        ),
    ),
    ViewSpec(
        key="front",
        filename="front.png",
        title="Front (XZ) — looking along shaft",
        kind="stl3d",
        criteria=(
            "Flange outline with two mount regions along X",
            "Shaft bore appears as a circle (axis into the page)",
            "Geometry is a solid flange housing, not an empty frame",
            "No obvious mesh explosion",
        ),
    ),
    ViewSpec(
        key="top",
        filename="top.png",
        title="Top (XY)",
        kind="stl3d",
        criteria=(
            "Flange elongated along X",
            "Shaft direction along Y",
            "Housing footprint clear",
            "Coherent solid",
        ),
    ),
    ViewSpec(
        key="right",
        filename="right.png",
        title="Right (YZ) — side of shaft",
        kind="stl3d",
        criteria=(
            "Shaft / bearing depth along Y is visible",
            "Flange thickness / body in Z",
            "Bore runs left/right (along Y), not into the page",
            "Geometry is coherent",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
