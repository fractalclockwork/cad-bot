#!/usr/bin/env python3
"""Per-view definitions for openbeam_15x100."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViewSpec:
    key: str
    filename: str
    title: str
    kind: str
    criteria: tuple[str, ...]


# Y = length, X/Z = 15×15 section
VIEWS: tuple[ViewSpec, ...] = (
    ViewSpec(
        key="iso",
        filename="iso.png",
        title="Isometric",
        kind="stl3d",
        criteria=(
            "Long square extrusion visible (not a flat plate)",
            "T-slots visible along the faces",
            "Part is not clipped; axes labels readable",
        ),
    ),
    ViewSpec(
        key="front",
        filename="front.png",
        title="Front (XZ) — end view",
        kind="stl3d",
        criteria=(
            "Square ~15×15 cross-section",
            "Center hollow visible",
            "Slot openings on the sides of the square",
        ),
    ),
    ViewSpec(
        key="top",
        filename="top.png",
        title="Top (XY)",
        kind="stl3d",
        criteria=(
            "Beam runs along Y (~100 mm)",
            "Width ~15 mm in X",
            "Longitudinal slot feature visible on the top face",
        ),
    ),
    ViewSpec(
        key="right",
        filename="right.png",
        title="Right (YZ)",
        kind="stl3d",
        criteria=(
            "Beam runs along Y (~100 mm)",
            "Height ~15 mm in Z",
            "Side slot / extrusion profile readable",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
