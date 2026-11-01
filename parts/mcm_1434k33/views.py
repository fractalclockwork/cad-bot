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


# X = flange long / bolts, Y = flange short, Z = shaft (flange-mount)
VIEWS: tuple[ViewSpec, ...] = (
    ViewSpec(
        key="iso",
        filename="iso.png",
        title="Isometric",
        kind="stl3d",
        criteria=(
            "Two-bolt flange housing silhouette is visible",
            "Bearing / shaft opening faces along Z (up)",
            "Flange elongated along X in the horizontal plane",
            "Part is not clipped; coherent solid",
        ),
    ),
    ViewSpec(
        key="front",
        filename="front.png",
        title="Front (XZ)",
        kind="stl3d",
        criteria=(
            "Flange outline with two mount regions along X",
            "Housing sits on Z≈0; height along shaft visible",
            "Geometry is a solid flange housing, not an empty frame",
            "No obvious mesh explosion",
        ),
    ),
    ViewSpec(
        key="top",
        filename="top.png",
        title="Top (XY) — looking along shaft",
        kind="stl3d",
        criteria=(
            "Flange footprint in XY with elongation along X",
            "Shaft bore appears as a circle (axis into the page)",
            "Two mount holes along X",
            "Coherent solid",
        ),
    ),
    ViewSpec(
        key="right",
        filename="right.png",
        title="Right (YZ)",
        kind="stl3d",
        criteria=(
            "Shaft / bearing height along Z is visible",
            "Flange width in Y",
            "Bore runs vertically (along Z), not left/right",
            "Geometry is coherent",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
