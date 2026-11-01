#!/usr/bin/env python3
"""Per-view definitions for tripod_head_openbeam_15_legs."""
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
        "iso",
        "iso.png",
        "Isometric",
        "stl3d",
        (
            "Head hub with three equal OpenBeam legs",
            "Cube-corner splay: legs mutually orthogonal, 120° in top view",
            "Assembly not clipped",
        ),
    ),
    ViewSpec(
        "front",
        "front.png",
        "Front (−Y)",
        "stl3d",
        (
            "Legs pitch downward from hub at cube-corner splay",
            "Beam ends seated in U-cradles against the stop",
        ),
    ),
    ViewSpec(
        "top",
        "top.png",
        "Top (+Z)",
        "stl3d",
        (
            "Three legs at 120° around hub (cube-corner top view)",
            "Equal radial reach; no leg missing a socket",
        ),
    ),
    ViewSpec(
        "right",
        "right.png",
        "Right (+X)",
        "stl3d",
        (
            "Leg along +X cradle seated at stop (flush to stop face)",
            "Beam T-slot orientation matches bolt / section-center axis",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
