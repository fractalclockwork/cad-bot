#!/usr/bin/env python3
"""Per-view definitions for tripod_head_openbeam_15."""
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
            "Flat mount pad on solid core; three U-cradles fused by filled convex hulls",
            "No floating sockets or hairline bridges — continuous solid post→U",
            "U openings face downward (drop-in); part not clipped",
        ),
    ),
    ViewSpec(
        "front",
        "front.png",
        "Front (−Y)",
        "stl3d",
        (
            "Cradle(s) pitched ~35° down; U open downward for leg drop-in",
            "Convex hull blend from post into cradle is a filled taper, not a loft ribbon",
            "M3 hole through cradle walls readable or clearly implied",
        ),
    ),
    ViewSpec(
        "top",
        "top.png",
        "Top (+Z)",
        "stl3d",
        (
            "Flat circular mount pad; three cradles at 120° (cube-corner top view)",
            "Hulls visible as filled sectors; U-pockets clear of neighbors",
            "Radial symmetry obvious",
        ),
    ),
    ViewSpec(
        "right",
        "right.png",
        "Right (+X)",
        "stl3d",
        (
            "Cradle on +X shows stop, pocket depth, and solid hull into the core",
            "Bolt hole ~7.5 mm from stop through section / T-slot center",
            "Mount pad flat on top",
        ),
    ),
)

REVIEW_SCHEMA_VERSION = 1
