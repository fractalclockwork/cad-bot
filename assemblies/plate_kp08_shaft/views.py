#!/usr/bin/env python3
"""Per-view definitions for plate_kp08_shaft assembly."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViewSpec:
    key: str
    filename: str
    title: str
    kind: str
    criteria: tuple[str, ...]


VIEWS: tuple[ViewSpec, ...] = (
    ViewSpec(
        key="iso",
        filename="iso.png",
        title="Isometric",
        kind="stl3d",
        criteria=(
            "Base plate visible under two pillow blocks",
            "Shaft passes through both KP08 bores along Y",
            "Blocks sit on the plate (not floating)",
            "Part is not clipped; axes labels readable",
        ),
    ),
    ViewSpec(
        key="front",
        filename="front.png",
        title="Front (XZ) — looking along shaft",
        kind="stl3d",
        criteria=(
            "Plate as thin base; KP08 housing above it",
            "Shaft appears as a circle through the bore",
            "Overall stack plate + block height",
        ),
    ),
    ViewSpec(
        key="top",
        filename="top.png",
        title="Top (XY)",
        kind="stl3d",
        criteria=(
            "Rectangular plate ~100 × 150",
            "Two KP08 footprints spaced along Y",
            "Shaft runs along Y through both blocks",
        ),
    ),
    ViewSpec(
        key="right",
        filename="right.png",
        title="Right (YZ) — side of shaft",
        kind="stl3d",
        criteria=(
            "Two pillow blocks along Y on the plate",
            "Shaft runs left/right through both bores",
            "Plate thickness visible at the bottom",
        ),
    ),
    ViewSpec(
        key="profile",
        filename="profile.png",
        title="2D top profile (DXF)",
        kind="dxf2d",
        criteria=(
            "Black linework on white background",
            "Plate rectangle with four mounting holes",
            "Center mark / shaft indication at origin",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
