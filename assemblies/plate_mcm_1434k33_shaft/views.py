#!/usr/bin/env python3
"""Per-view definitions for plate_mcm_1434k33_shaft assembly."""
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
            "Base plate visible under the flange bearing",
            "Shaft passes vertically through the plate and bearing",
            "Flange lies flat on the plate (not edge-on)",
            "Part is not clipped; axes labels readable",
        ),
    ),
    ViewSpec(
        key="front",
        filename="front.png",
        title="Front (XZ)",
        kind="stl3d",
        criteria=(
            "Plate as thin base; flange flat on top",
            "Shaft runs vertically through plate and bore",
            "Bolt-hole pitch visible along X on the flange",
        ),
    ),
    ViewSpec(
        key="top",
        filename="top.png",
        title="Top (XY) — looking along shaft",
        kind="stl3d",
        criteria=(
            "Rectangular plate ~100 × 150",
            "Flange footprint centered on the plate",
            "Shaft appears as a circle through the bore",
        ),
    ),
    ViewSpec(
        key="right",
        filename="right.png",
        title="Right (YZ)",
        kind="stl3d",
        criteria=(
            "Flange flat on the plate",
            "Shaft runs vertically through plate and bore",
            "Plate thickness visible; shaft clearance through plate",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
