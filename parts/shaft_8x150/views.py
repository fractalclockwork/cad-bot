#!/usr/bin/env python3
"""Per-view definitions for shaft_8x150 auto + human verification."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViewSpec:
    key: str
    filename: str
    title: str
    kind: str  # "stl3d"
    criteria: tuple[str, ...]


# X/Z radial, Y = shaft axis (length)
VIEWS: tuple[ViewSpec, ...] = (
    ViewSpec(
        key="iso",
        filename="iso.png",
        title="Isometric",
        kind="stl3d",
        criteria=(
            "Long thin cylinder is visible (rod, not a disc)",
            "Length is clearly much greater than diameter",
            "Part is not clipped; axes labels readable",
        ),
    ),
    ViewSpec(
        key="front",
        filename="front.png",
        title="Front (XZ) — looking along shaft",
        kind="stl3d",
        criteria=(
            "End view shows a circular cross-section",
            "Diameter fills a small circular disc (not a long rectangle)",
            "No hollow bore — solid shaft end",
        ),
    ),
    ViewSpec(
        key="top",
        filename="top.png",
        title="Top (XY)",
        kind="stl3d",
        criteria=(
            "Shaft runs left/right (or along Y) as a long rectangle/capsule silhouette",
            "Aspect ratio shows ~150 length vs ~8 diameter",
            "Geometry is a single solid rod",
        ),
    ),
    ViewSpec(
        key="right",
        filename="right.png",
        title="Right (YZ) — side of shaft",
        kind="stl3d",
        criteria=(
            "Side view shows a long cylinder / rectangle along Y",
            "Height of the bar matches diameter (~8 mm span in Z)",
            "No pillow-block housing features",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
