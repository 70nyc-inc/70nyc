#!/usr/bin/env python3
"""Remove ?lang=zh|en from lang-switch hrefs across static HTML."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERN = re.compile(r"\?lang=(?:zh|en)(?=\")")


def main() -> None:
    n = 0
    for path in ROOT.rglob("*.html"):
        raw = path.read_text(encoding="utf-8")
        new = PATTERN.sub("", raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            print(path.relative_to(ROOT))
            n += 1
    print(f"Stripped lang query from {n} file(s)")


if __name__ == "__main__":
    main()
