#!/usr/bin/env python3
"""Per-view definitions for plate_150x150x5 auto + human verification."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViewSpec:
    key: str
    filename: str
    title: str
    kind: str  # "stl3d" | "dxf2d"
    criteria: tuple[str, ...]


# X/Y = plate plane, Z = thickness (up)
VIEWS: tuple[ViewSpec, ...] = (
    ViewSpec(
        key="iso",
        filename="iso.png",
        title="Isometric",
        kind="stl3d",
        criteria=(
            "Flat square plate is visible (slab, not a rod or housing)",
            "Thickness is small relative to width/depth",
            "Part is not clipped; axes labels readable",
        ),
    ),
    ViewSpec(
        key="front",
        filename="front.png",
        title="Front (XZ)",
        kind="stl3d",
        criteria=(
            "Side elevation shows a thin horizontal bar (thickness ~5 mm in Z)",
            "Width spans ~150 mm in X",
            "No shaft bore or bolt flanges",
        ),
    ),
    ViewSpec(
        key="top",
        filename="top.png",
        title="Top (XY)",
        kind="stl3d",
        criteria=(
            "Square outline ~150 × 150 mm",
            "Plain face — no holes in this revision",
            "Centered, axis-aligned square",
        ),
    ),
    ViewSpec(
        key="right",
        filename="right.png",
        title="Right (YZ)",
        kind="stl3d",
        criteria=(
            "Side elevation shows a thin horizontal bar",
            "Depth spans ~150 mm in Y",
            "Bottom edge sits on Z=0",
        ),
    ),
    ViewSpec(
        key="profile",
        filename="profile.png",
        title="2D top profile (DXF)",
        kind="dxf2d",
        criteria=(
            "Black linework on white background",
            "Closed square / rectangle outline (~150 × 150)",
            "No bolt-hole circles (plain plate revision)",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
