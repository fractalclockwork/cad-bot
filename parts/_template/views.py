#!/usr/bin/env python3
"""Preview / human-review views for this part — edit criteria."""
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
    ViewSpec("iso", "iso.png", "Isometric", "stl3d", ("Part visible and not clipped",)),
    ViewSpec("front", "front.png", "Front", "stl3d", ("Front view matches drawing intent",)),
    ViewSpec("top", "top.png", "Top", "stl3d", ("Top view matches drawing intent",)),
    ViewSpec("right", "right.png", "Right", "stl3d", ("Right view matches drawing intent",)),
)

REVIEW_SCHEMA_VERSION = 1
