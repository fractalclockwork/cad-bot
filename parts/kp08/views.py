#!/usr/bin/env python3
"""Per-view definitions for KP08 auto + human verification."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViewSpec:
    key: str
    filename: str
    title: str
    kind: str  # "stl3d"
    criteria: tuple[str, ...]


# X = bolt pitch, Y = shaft axis, Z = up
VIEWS: tuple[ViewSpec, ...] = (
    ViewSpec(
        key="iso",
        filename="iso.png",
        title="Isometric",
        kind="stl3d",
        criteria=(
            "Capsule base with two bolt flanges along X is visible",
            "Central housing/boss is visible above the base",
            "Shaft bore opening faces along Y (not punched vertically through the base)",
            "Part is not clipped; axes labels readable",
        ),
    ),
    ViewSpec(
        key="front",
        filename="front.png",
        title="Front (XZ) — looking along shaft",
        kind="stl3d",
        criteria=(
            "Base sits along the bottom of the view",
            "Shaft bore appears as a clear circle through the boss (axis into the page)",
            "Overall height shows base + boss (not a flat plate only)",
            "Left/right flange ends are visible along X",
        ),
    ),
    ViewSpec(
        key="top",
        filename="top.png",
        title="Top (XY)",
        kind="stl3d",
        criteria=(
            "Capsule / dog-bone base outline is clear",
            "Exactly two bolt holes visible in the base (no third vertical hole at center)",
            "Boss/housing footprint centered; shaft direction along Y",
            "No obvious mesh explosion or missing halves",
        ),
    ),
    ViewSpec(
        key="right",
        filename="right.png",
        title="Right (YZ) — side of shaft",
        kind="stl3d",
        criteria=(
            "Base thickness is visible as a horizontal slab",
            "Boss/housing rises above the base",
            "Shaft bore runs left/right in this view (along Y), not into the page",
            "Geometry is coherent (not an empty frame)",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
