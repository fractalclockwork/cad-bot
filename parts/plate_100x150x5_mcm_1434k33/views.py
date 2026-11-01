#!/usr/bin/env python3
"""Per-view definitions for plate_100x150x5_mcm_1434k33 auto + human verification."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViewSpec:
    key: str
    filename: str
    title: str
    kind: str  # "stl3d"
    criteria: tuple[str, ...]


# X = bolt pitch, Y = plate depth, Z = up (shaft through plate)
VIEWS: tuple[ViewSpec, ...] = (
    ViewSpec(
        key="iso",
        filename="iso.png",
        title="Isometric",
        kind="stl3d",
        criteria=(
            "Rectangular plate is visible (not square 150×150)",
            "Two bolt holes plus a larger center clearance hole",
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
            "No bearing housing body — plate only",
        ),
    ),
    ViewSpec(
        key="top",
        filename="top.png",
        title="Top (XY)",
        kind="stl3d",
        criteria=(
            "Rectangle ~100 × 150 (narrower in X than Y)",
            "Two bolt holes on the midline (~30.9 mm apart in X)",
            "Centered larger shaft clearance hole between the bolts",
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
            "Hole openings may appear near mid-length",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
