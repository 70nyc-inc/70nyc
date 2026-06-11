#!/usr/bin/env python3
"""Insert /areas/ and /nationwide/ footer links across all HTML pages."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ZH_BLOCK = """        <a href="/areas/">服务区域</a>
        <a href="/nationwide/">全美远程</a>
"""
EN_BLOCK = """        <a href="/en/areas/">Service Areas</a>
        <a href="/en/nationwide/">Nationwide Remote</a>
"""


def patch(text: str) -> tuple[str, bool]:
    changed = False
    if 'href="/areas/"' not in text:
        old = '        <a href="/services/social-media/">社交媒体管理</a>\n        <a href="/process/">项目流程</a>'
        if old in text:
            text = text.replace(
                old,
                '        <a href="/services/social-media/">社交媒体管理</a>\n' + ZH_BLOCK + '        <a href="/process/">项目流程</a>',
                1,
            )
            changed = True
    if 'href="/en/areas/"' not in text:
        for proc in ("Our Process", "Process"):
            old = f'        <a href="/en/services/social-media/">Social Media</a>\n        <a href="/en/process/">{proc}</a>'
            if old in text:
                text = text.replace(
                    old,
                    f'        <a href="/en/services/social-media/">Social Media</a>\n' + EN_BLOCK + f'        <a href="/en/process/">{proc}</a>',
                    1,
                )
                changed = True
                break
    return text, changed


def main() -> None:
    n = 0
    for path in ROOT.rglob("*.html"):
        if path.name == "404.html":
            continue
        raw = path.read_text(encoding="utf-8")
        new, changed = patch(raw)
        if changed:
            path.write_text(new, encoding="utf-8")
            print(path.relative_to(ROOT))
            n += 1
    print(f"Updated {n} file(s)")


if __name__ == "__main__":
    main()
