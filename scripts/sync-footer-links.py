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


ZH_BLOG = '        <a href="/blog/">博客</a>\n'
EN_BLOG = '        <a href="/en/blog/">Blog</a>\n'


ZH_AI = '        <a href="/services/ai-marketing/">AI 智能营销</a>\n'
EN_AI = '        <a href="/en/services/ai-marketing/">AI Marketing</a>\n'
ZH_STATES = '        <a href="/states/">美国各州</a>\n'
EN_STATES = '        <a href="/en/states/">US States</a>\n'


def patch(text: str) -> tuple[str, bool]:
    changed = False
    if 'href="/services/ai-marketing/"' not in text and 'href="/services/seo/">SEO 优化</a>' in text:
        old = '        <a href="/services/seo/">SEO 优化</a>\n        <a href="/services/social-media/">社交媒体管理</a>'
        if old in text:
            text = text.replace(old, '        <a href="/services/seo/">SEO 优化</a>\n' + ZH_AI + '        <a href="/services/social-media/">社交媒体管理</a>', 1)
            changed = True
    if 'href="/en/services/ai-marketing/"' not in text and 'href="/en/services/seo/">SEO</a>' in text:
        old = '        <a href="/en/services/seo/">SEO</a>\n        <a href="/en/services/social-media/">Social Media</a>'
        if old in text:
            text = text.replace(old, '        <a href="/en/services/seo/">SEO</a>\n' + EN_AI + '        <a href="/en/services/social-media/">Social Media</a>', 1)
            changed = True
    if 'href="/states/"' not in text and 'href="/nationwide/"' in text:
        old = '        <a href="/nationwide/">全美远程</a>\n'
        if old in text:
            text = text.replace(old, old + ZH_STATES, 1)
            changed = True
    if 'href="/en/states/"' not in text and 'href="/en/nationwide/"' in text:
        old = '        <a href="/en/nationwide/">Nationwide Remote</a>\n'
        if old in text:
            text = text.replace(old, old + EN_STATES, 1)
            changed = True
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
    if 'href="/blog/"' not in text and 'aria-label="我们的服务"' in text:
        old = '        <a href="/sitemap/">网站地图</a>'
        if old in text:
            text = text.replace(old, ZH_BLOG + old, 1)
            changed = True
    if 'href="/en/blog/"' not in text and 'aria-label="Services"' in text:
        for label in ("Sitemap",):
            old = f'        <a href="/en/sitemap/">{label}</a>'
            if old in text:
                text = text.replace(old, EN_BLOG + old, 1)
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
