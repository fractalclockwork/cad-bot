#!/usr/bin/env python3
"""Per-view definitions for mcm_3971n31 (McMaster 3971N31 housing)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ViewSpec:
    key: str
    filename: str
    title: str
    kind: str  # "stl3d"
    criteria: tuple[str, ...]


# X = base length, Y = bearing axis, Z = up
VIEWS: tuple[ViewSpec, ...] = (
    ViewSpec(
        key="iso",
        filename="iso.png",
        title="Isometric",
        kind="stl3d",
        criteria=(
            "Pillow-block / ready-mount housing silhouette is visible",
            "Base along X with upright body is clear",
            "Bearing bore opening faces along Y",
            "Part is not clipped; coherent solid",
        ),
    ),
    ViewSpec(
        key="front",
        filename="front.png",
        title="Front (XZ) — looking along bearing axis",
        kind="stl3d",
        criteria=(
            "Base sits along the bottom of the view",
            "Bearing bore appears as a circle (axis into the page)",
            "Overall height shows base + body",
            "Mounting ends visible along X",
        ),
    ),
    ViewSpec(
        key="top",
        filename="top.png",
        title="Top (XY)",
        kind="stl3d",
        criteria=(
            "Base outline elongated along X",
            "Two mount holes visible in the base when present in the model",
            "Housing footprint; bearing direction along Y",
            "No obvious mesh explosion",
        ),
    ),
    ViewSpec(
        key="right",
        filename="right.png",
        title="Right (YZ) — side of bearing",
        kind="stl3d",
        criteria=(
            "Thin housing width along Y is visible",
            "Body rises above the base",
            "Bearing bore runs left/right (along Y), not into the page",
            "Geometry is coherent",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
