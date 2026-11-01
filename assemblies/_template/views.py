#!/usr/bin/env python3
"""Preview / human-review views for assembly ASSY_NAME — edit criteria."""
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
    ViewSpec("iso", "iso.png", "Isometric", "stl3d", ("All BOM solids visible and not clipped",)),
    ViewSpec("front", "front.png", "Front", "stl3d", ("Front view matches mate intent",)),
    ViewSpec("top", "top.png", "Top", "stl3d", ("Top view shows expected layout",)),
    ViewSpec("right", "right.png", "Right", "stl3d", ("Side view shows expected stack / shaft",)),
)

REVIEW_SCHEMA_VERSION = 1
