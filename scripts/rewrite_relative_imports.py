#!/usr/bin/env python3
"""Rewrite openapi-generator's absolute `connect_api.*` imports to relative
ones, so the vendored SDK doesn't need to be findable as a top-level package
on sys.path. Run after `openapi-generator generate`, pointed at the generated
connect_api/ package directory.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])

for f in root.rglob("*.py"):
    depth = len(f.relative_to(root).parts) - 1  # connect_api/x.py -> 0, connect_api/api/x.py -> 1
    dots = "." * (depth + 1)
    text = f.read_text()

    # \1 already carries its own leading dot when present, so dots[:-1] avoids double-counting;
    # when \1 is absent (bare "from connect_api import X") fall back to the full dots
    text = re.sub(
        r"\bfrom connect_api(\.[\w.]+)? import",
        lambda m: f"from {dots[:-1]}{m.group(1)} import" if m.group(1) else f"from {dots} import",
        text,
    )
    text = re.sub(
        r"^import connect_api\.(\w+)$",
        lambda m: f"from {dots} import {m.group(1)}",
        text,
        flags=re.M,
    )
    text = re.sub(r"\bconnect_api\.(\w+)\b", r"\1", text)

    f.write_text(text)
