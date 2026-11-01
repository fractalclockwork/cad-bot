#!/usr/bin/env python3
"""Diagnose why Firefox may fail to open output/previews/index.html."""
from __future__ import annotations

import json
import os
import shutil
import time
from pathlib import Path

# #region agent log
_DEBUG_LOG = Path("/home/plastic/src/cad-bot/.cursor/debug-17e637.log")


def _dbg(hypothesis_id: str, location: str, message: str, data: dict | None = None) -> None:
    payload = {
        "sessionId": "17e637",
        "runId": "gallery-access",
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data or {},
        "timestamp": int(time.time() * 1000),
    }
    _DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
    with _DEBUG_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload) + "\n")
# #endregion


ROOT = Path("/home/plastic/src/cad-bot")
INDEX = ROOT / "output" / "previews" / "index.html"


def main() -> None:
    firefox = shutil.which("firefox") or ""
    snap_ff = Path("/snap/bin/firefox")
    firefox_head = ""
    if firefox and Path(firefox).is_file():
        try:
            firefox_head = Path(firefox).read_text(encoding="utf-8", errors="ignore")[:200]
        except OSError as exc:
            firefox_head = f"<read-error {exc}>"

    # #region agent log
    _dbg(
        "A",
        "diagnose_gallery_access.py:firefox",
        "Firefox install fingerprint",
        {
            "which_firefox": firefox,
            "snap_bin_exists": snap_ff.exists(),
            "firefox_is_snap_wrapper": "snap/bin/firefox" in firefox_head,
            "firefox_head": firefox_head.replace("\n", " | "),
        },
    )
    # #endregion

    st = INDEX.stat() if INDEX.exists() else None
    # #region agent log
    _dbg(
        "B",
        "diagnose_gallery_access.py:file",
        "Gallery index access from this user",
        {
            "path": str(INDEX),
            "exists": INDEX.exists(),
            "readable": os.access(INDEX, os.R_OK),
            "mode": oct(st.st_mode & 0o777) if st else None,
            "uid": st.st_uid if st else None,
            "gid": st.st_gid if st else None,
            "size": st.st_size if st else None,
            "file_url": INDEX.resolve().as_uri(),
        },
    )
    # #endregion

    home = Path.home()
    # #region agent log
    _dbg(
        "C",
        "diagnose_gallery_access.py:home_mode",
        "Home directory mode (snap traversal)",
        {
            "home": str(home),
            "home_mode": oct(home.stat().st_mode & 0o777),
            "under_home": str(INDEX.resolve()).startswith(str(home.resolve())),
        },
    )
    # #endregion

    # #region agent log
    _dbg(
        "D",
        "diagnose_gallery_access.py:conclusion",
        "Likely cause ranking",
        {
            "prefer_http_localhost": True,
            "reason": (
                "Snap Firefox often blocks file:// to project paths; "
                "serve previews via localhost HTTP instead"
            ),
        },
    )
    # #endregion

    print("Diagnostic written to", _DEBUG_LOG)
    print("index:", INDEX.resolve())
    print("file URL:", INDEX.resolve().as_uri())
    print("readable:", os.access(INDEX, os.R_OK))
    print("firefox:", firefox, "snap:", snap_ff.exists())


if __name__ == "__main__":
    main()
