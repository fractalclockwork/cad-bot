#!/usr/bin/env python3
"""Per-view definitions for plate_100x150x5 auto + human verification."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViewSpec:
    key: str
    filename: str
    title: str
    kind: str  # "stl3d"
    criteria: tuple[str, ...]


# X = bolt pitch, Y = shaft / block spacing, Z = up
VIEWS: tuple[ViewSpec, ...] = (
    ViewSpec(
        key="iso",
        filename="iso.png",
        title="Isometric",
        kind="stl3d",
        criteria=(
            "Rectangular plate is visible (not square 150×150)",
            "Four mounting holes visible as two pairs",
            "Part is not clipped; axes labels readable",
        ),
    ),
    ViewSpec(
        key="front",
        filename="front.png",
        title="Front (XZ)",
        kind="stl3d",
        criteria=(
            "Thin horizontal slab (~5 mm thick)",
            "Width spans ~100 mm in X",
            "No pillow-block housing body — plate only",
        ),
    ),
    ViewSpec(
        key="top",
        filename="top.png",
        title="Top (XY)",
        kind="stl3d",
        criteria=(
            "Rectangle ~100 × 150 (narrower in X than Y)",
            "Exactly four holes in two pairs along Y",
            "Pairs ~100 mm apart on center; holes ~42 mm apart in X within each pair",
        ),
    ),
    ViewSpec(
        key="right",
        filename="right.png",
        title="Right (YZ)",
        kind="stl3d",
        criteria=(
            "Thin slab; depth spans ~150 mm in Y",
            "Bottom on Z=0",
            "Hole openings may appear along the length",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
