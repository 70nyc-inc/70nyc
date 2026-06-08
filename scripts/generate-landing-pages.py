#!/usr/bin/env python3
"""One-shot generator: extract sections from index.html / en.html into SEO landing pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    {
        "slug": "services",
        "section_id": "services",
        "zh": {
            "title": "70NYC 服务｜纽约网站设计、SEO、Google Ads、社媒营销",
            "description": "70NYC 提供纽约网站设计与开发、SEO 优化、Google Ads 投放、AI 智能营销、社交媒体运营与手机应用开发，一站式数字营销解决方案。",
            "nav_label": "服务",
            "breadcrumb": "我们的服务",
            "hreflang_en": "https://70nyc.com/en/services/",
        },
        "en": {
            "title": "70NYC Services | NYC Web Design, SEO, Google Ads & Social Media",
            "description": "Web design, SEO, Google Ads, AI marketing, social media, and mobile app development for New York businesses — full-service digital marketing by 70NYC.",
            "nav_label": "Services",
            "breadcrumb": "Our Services",
            "hreflang_zh": "https://70nyc.com/services/",
        },
    },
    {
        "slug": "process",
        "section_id": "process",
        "zh": {
            "title": "70NYC 项目流程｜纽约网站设计四步标准交付",
            "description": "从需求调研、设计确认、开发上线到交付运维，70NYC 纽约网站设计团队提供透明可追踪的四步标准项目流程。",
            "nav_label": "流程",
            "breadcrumb": "项目流程",
            "hreflang_en": "https://70nyc.com/en/process/",
        },
        "en": {
            "title": "70NYC Process | NYC Web Design Delivery in 4 Steps",
            "description": "Discovery, design, build, and support — 70NYC's transparent four-step web design and development process for New York businesses.",
            "nav_label": "Process",
            "breadcrumb": "Our Process",
            "hreflang_zh": "https://70nyc.com/process/",
        },
    },
    {
        "slug": "about",
        "section_id": "about",
        "zh": {
            "title": "关于 70NYC｜纽约华人数字营销与网站设计团队",
            "description": "70NYC 是纽约本地网站设计与数字营销团队，13+ 年服务曼哈顿、法拉盛、布鲁克林、长岛华人企业，Google Partner 认证。",
            "nav_label": "关于我们",
            "breadcrumb": "关于我们",
            "hreflang_en": "https://70nyc.com/en/about/",
        },
        "en": {
            "title": "About 70NYC | NYC Web Design & Digital Marketing Team",
            "description": "Meet 70NYC — a New York web design and digital marketing team serving local businesses for 13+ years. Google Partner certified.",
            "nav_label": "About",
            "breadcrumb": "About Us",
            "hreflang_zh": "https://70nyc.com/about/",
        },
    },
    {
        "slug": "faq",
        "section_id": "faq",
        "zh": {
            "title": "70NYC 项目 FAQ｜网站设计合作常见问题",
            "description": "关于纽约网站设计项目启动、周期、报价、修改、交付与运维的常见问题解答，帮助您更快做出合作决定。",
            "nav_label": "FAQ",
            "breadcrumb": "项目 FAQ",
            "hreflang_en": "https://70nyc.com/en/faq/",
            "faq_schema": True,
        },
        "en": {
            "title": "70NYC FAQ | NYC Web Design Project Questions",
            "description": "Frequently asked questions about timelines, pricing, revisions, deliverables, and support for 70NYC web design projects in New York.",
            "nav_label": "FAQ",
            "breadcrumb": "Project FAQ",
            "hreflang_zh": "https://70nyc.com/faq/",
            "faq_schema": True,
        },
    },
    {
        "slug": "contact",
        "section_id": "contact",
        "zh": {
            "title": "联系 70NYC｜纽约网站设计免费咨询",
            "description": "联系 70NYC 获取纽约网站设计、SEO 与 Google Ads 免费咨询。电话 386-316-1848，曼哈顿·法拉盛·布鲁克林·长岛均可服务。",
            "nav_label": "联系我们",
            "breadcrumb": "免费咨询",
            "hreflang_en": "https://70nyc.com/en/contact/",
            "form_subject": "70NYC 网站咨询（中文）",
            "form_redirect": "https://70nyc.com/contact/?success=1",
        },
        "en": {
            "title": "Contact 70NYC | Free NYC Web Design Consultation",
            "description": "Get a free consultation for NYC web design, SEO, and Google Ads. Call 386-316-1848 — serving Manhattan, Flushing, Brooklyn, and Long Island.",
            "nav_label": "Contact",
            "breadcrumb": "Contact Us",
            "hreflang_zh": "https://70nyc.com/contact/",
            "form_subject": "70NYC Website Inquiry (English)",
            "form_redirect": "https://70nyc.com/en/contact/?success=1",
        },
    },
]

NAV_ZH = [
    ("home", "/", "首页"),
    ("services", "/services/", "服务"),
    ("process", "/process/", "流程"),
    ("about", "/about/", "关于我们"),
    ("faq", "/faq/", "FAQ"),
    ("contact", "/contact/", "联系我们"),
]

NAV_EN = [
    ("home", "/en.html", "Home"),
    ("services", "/en/services/", "Services"),
    ("process", "/en/process/", "Process"),
    ("about", "/en/about/", "About"),
    ("faq", "/en/faq/", "FAQ"),
    ("contact", "/en/contact/", "Contact"),
]


def extract_section(html: str, section_id: str) -> str:
    pattern = rf'(<section[^>]*\bid="{re.escape(section_id)}"[^>]*>)(.*?)(</section>)'
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        raise ValueError(f"Section id={section_id!r} not found")
    return match.group(0)


def patch_section(body: str, lang: str, slug: str) -> str:
    prefix = "/en" if lang == "en" else ""
    body = body.replace('src="assets/', 'src="/assets/')
    body = body.replace("href=\"#contact\"", f'href="{prefix}/contact/"')
    body = body.replace("href='#contact'", f"href='{prefix}/contact/'")
    if slug == "contact":
        if lang == "zh":
            body = body.replace(
                'value="https://70nyc.com/?success=1#contact"',
                'value="https://70nyc.com/contact/?success=1"',
            )
        else:
            body = body.replace(
                'value="https://70nyc.com/en.html?success=1#contact"',
                'value="https://70nyc.com/en/contact/?success=1"',
            )
    return body


LIGHT_HEADER_SLUGS = {"services", "faq"}


def nav_html(nav_items, active: str, lang: str, slug: str) -> str:
    links = []
    for key, href, label in nav_items:
        cls = ' class="active"' if key == active else ""
        data = f' data-nav="{key}"' if key != active or True else ""
        links.append(f'      <a href="{href}"{data}{cls}>{label}</a>')
    lang_switch = (
        '<a class="lang-switch" href="/en.html" hreflang="en">EN</a>'
        if lang == "zh"
        else '<a class="lang-switch" href="/" hreflang="zh-CN">中文</a>'
    )
    consult_href = "/contact/" if lang == "zh" else "/en/contact/"
    consult_label = "免费咨询" if lang == "zh" else "Free Consult"
    logo_small = "纽约数字营销专家" if lang == "zh" else "NYC Digital Marketing"
    home_href = "/" if lang == "zh" else "/en.html"
    menu_label = "打开菜单" if lang == "zh" else "Open menu"
    header_mod = " scrolled on-light" if slug in LIGHT_HEADER_SLUGS else " scrolled"
    return f"""  <header class="site-header{header_mod}" id="header">
    <a class="logo" href="{home_href}"><span>70</span>NYC<small>{logo_small}</small></a>
    <button class="menu-toggle" id="menuToggle" aria-label="{menu_label}" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav" id="nav">
{chr(10).join(links)}
    </nav>
    <div class="header-cta">
      {lang_switch}
      <a class="phone" href="tel:3863161848">386-316-1848</a>
      <a class="btn btn-gold" href="{consult_href}">{consult_label}</a>
    </div>
  </header>"""


def footer_html(lang: str) -> str:
    if lang == "zh":
        return """  <footer class="footer">
    <div class="footer-main">
      <div class="footer-brand">
        <div class="logo"><span>70</span>NYC<small>纽约数字营销专家</small></div>
        <p>纽约网站设计公司与网站开发团队，为华人企业提供网页设计、手机应用开发、平面设计、餐馆网站、专业广告推广及 SEO 服务。</p>
      </div>
      <nav class="footer-col" aria-label="关于我们">
        <b>关于我们</b>
        <a href="/about/">了解我们</a>
        <a href="/about/">我们的团队</a>
        <a href="/contact/">联系我们</a>
        <a href="/faq/">常见问题</a>
      </nav>
      <nav class="footer-col" aria-label="我们的服务">
        <b>关于我们的服务</b>
        <a href="/services/#web">网页设计与网站开发</a>
        <a href="/services/#app">手机应用开发与设计</a>
        <a href="/services/#ads">专业广告推广服务</a>
        <a href="/services/#seo">SEO 优化</a>
        <a href="/services/#social">社交媒体管理</a>
        <a href="/process/">项目流程</a>
        <a href="/sitemap.xml">网站地图</a>
      </nav>
    </div>
    <p class="footer-seo">
      服务区域：纽约网站设计 · 纽约网站公司 · 纽约网站设计师 · 纽约华人网站设计 · 纽约网站制作 ·
      曼哈顿网站设计 · 曼哈顿网站公司 · 曼哈顿网站设计师 ·
      法拉盛网站设计 · 法拉盛网站公司 · 法拉盛网站设计师 ·
      布鲁克林网站设计 · 布鲁克林网站公司 · 布鲁克林网站设计师 ·
      长岛网站设计 · 长岛网站公司 · 长岛网站设计师
    </p>
    <div class="footer-bottom">
      <address>386-316-1848 · info@70nyc.com · New York, NY</address>
    </div>
  </footer>"""
    return """  <footer class="footer">
    <div class="footer-main">
      <div class="footer-brand">
        <div class="logo"><span>70</span>NYC<small>NYC Digital Marketing</small></div>
        <p>New York web design and development agency — web design, mobile apps, restaurant websites, graphic design, advertising, and SEO for local businesses.</p>
      </div>
      <nav class="footer-col" aria-label="About">
        <b>About</b>
        <a href="/en/about/">About Us</a>
        <a href="/en/about/">Our Team</a>
        <a href="/en/contact/">Contact</a>
        <a href="/en/faq/">FAQ</a>
      </nav>
      <nav class="footer-col" aria-label="Services">
        <b>Our Services</b>
        <a href="/en/services/#web">Web Design &amp; Development</a>
        <a href="/en/services/#app">Mobile App Development</a>
        <a href="/en/services/#ads">Digital Advertising</a>
        <a href="/en/services/#seo">SEO</a>
        <a href="/en/services/#social">Social Media</a>
        <a href="/en/process/">Process</a>
        <a href="/sitemap.xml">Sitemap</a>
      </nav>
    </div>
    <p class="footer-seo">
      Areas served: NYC web design · Manhattan web design · Flushing web design · Brooklyn web design · Long Island web design · New York website company
    </p>
    <div class="footer-bottom">
      <address>386-316-1848 · info@70nyc.com · New York, NY</address>
    </div>
  </footer>"""


def breadcrumb_schema(name: str, url: str, lang: str) -> str:
    home_name = "首页" if lang == "zh" else "Home"
    home_url = "https://70nyc.com/" if lang == "zh" else "https://70nyc.com/en/"
    return f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "{home_name}", "item": "{home_url}"}},
      {{"@type": "ListItem", "position": 2, "name": "{name}", "item": "{url}"}}
    ]
  }}
  </script>"""


def faq_schema_html() -> str:
    return """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {"@type": "Question", "name": "项目启动前，我需要准备什么？", "acceptedAnswer": {"@type": "Answer", "text": "通常只需提供：业务简介、参考网站、现有 Logo/图片素材，以及您希望网站具备的核心功能。我们会在首次沟通后整理需求文档，帮您补齐缺失项，无需一次性准备齐全。"}},
      {"@type": "Question", "name": "网站项目一般多久可以交付？", "acceptedAnswer": {"@type": "Answer", "text": "标准企业官网通常 2–4 周：第 1 周需求与设计确认，第 2–3 周开发，第 4 周测试上线。含电商、预约系统或多语言等功能的项目，会在方案阶段给出详细排期。"}},
      {"@type": "Question", "name": "项目费用如何计算？", "acceptedAnswer": {"@type": "Answer", "text": "根据页面数量、功能复杂度、是否需要 SEO/广告/社媒配套来报价。我们会在需求确认后提供明细报价单，包含各阶段交付物，无隐藏费用，签约前价格透明锁定。"}},
      {"@type": "Question", "name": "设计稿确认后还能修改吗？", "acceptedAnswer": {"@type": "Answer", "text": "设计确认阶段支持合理范围内的修改，重大结构调整会在开发前完成。开发阶段的小幅文案、图片替换可正常处理；超出合同范围的新增功能，我们会先评估工时与费用再执行。"}},
      {"@type": "Question", "name": "上线后会提供哪些交付物？", "acceptedAnswer": {"@type": "Answer", "text": "包含：已上线网站、后台管理账号、源代码（按合同约定）、操作培训，以及 SEO 基础配置文档。如需广告账户或社媒账号搭建，也会一并移交并附操作说明。"}},
      {"@type": "Question", "name": "上线后是否提供维护服务？", "acceptedAnswer": {"@type": "Answer", "text": "是的。所有项目包含上线后技术支持期，并可选择年度维护套餐，涵盖安全更新、内容修改、性能监控与故障响应。我们也提供按月 SEO 优化和广告代运营服务。"}},
      {"@type": "Question", "name": "不在纽约可以合作吗？", "acceptedAnswer": {"@type": "Answer", "text": "可以。我们总部位于纽约，大纽约地区可安排面谈；全美及海外客户通过视频会议、微信/WhatsApp 和项目管理工具协作，流程与本地客户完全一致。"}}
    ]
  }
  </script>"""


def faq_schema_html_en() -> str:
    return """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {"@type": "Question", "name": "What do I need before starting a project?", "acceptedAnswer": {"@type": "Answer", "text": "Usually just a business overview, reference websites, existing logo/images, and core features you need. We prepare a requirements doc after the first call and help fill any gaps — no need to have everything ready upfront."}},
      {"@type": "Question", "name": "How long does a website project take?", "acceptedAnswer": {"@type": "Answer", "text": "A standard business site is typically 2–4 weeks: week 1 discovery and design, weeks 2–3 development, week 4 testing and launch. Projects with e-commerce, booking, or multilingual features get a detailed timeline during planning."}},
      {"@type": "Question", "name": "How is pricing calculated?", "acceptedAnswer": {"@type": "Answer", "text": "Based on page count, feature complexity, and whether SEO/ads/social packages are included. We provide an itemized quote after requirements are confirmed — transparent pricing locked before signing."}},
      {"@type": "Question", "name": "Can I change things after design approval?", "acceptedAnswer": {"@type": "Answer", "text": "Reasonable revisions are supported during design approval; major structural changes are completed before development. Minor copy and image swaps during build are fine; out-of-scope features are quoted before work begins."}},
      {"@type": "Question", "name": "What do I receive at launch?", "acceptedAnswer": {"@type": "Answer", "text": "Live website, admin credentials, source code (per contract), training, and basic SEO setup docs. Ad accounts or social setups are handed off with instructions when included."}},
      {"@type": "Question", "name": "Do you offer maintenance after launch?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. All projects include post-launch support, with optional annual maintenance for security updates, content changes, monitoring, and incident response. Monthly SEO and ad management are also available."}},
      {"@type": "Question", "name": "Can we work together if I'm not in NYC?", "acceptedAnswer": {"@type": "Answer", "text": "Absolutely. We're based in New York with in-person meetings in the metro area; clients nationwide and overseas collaborate via video, WeChat/WhatsApp, and project tools — same process as local clients."}}
    ]
  }
  </script>"""


def build_page(lang: str, page: dict, meta: dict, section_html: str) -> str:
    slug = page["slug"]
    prefix = "" if lang == "zh" else "/en"
    canonical = f"https://70nyc.com{prefix}/{slug}/"
    html_lang = "zh-CN" if lang == "zh" else "en"
    hreflang_zh = "https://70nyc.com/" if slug == "home" else f"https://70nyc.com/{slug}/"
    hreflang_en = "https://70nyc.com/en/" if lang == "en" else meta.get("hreflang_en", f"https://70nyc.com/en/{slug}/")
    if lang == "en":
        hreflang_zh = meta.get("hreflang_zh", f"https://70nyc.com/{slug}/")
        hreflang_en = canonical

    og_locale = "zh_CN" if lang == "zh" else "en_US"
    og_alt = "en_US" if lang == "zh" else "zh_CN"
    nav_items = NAV_ZH if lang == "zh" else NAV_EN
    active = slug

    extra_schema = breadcrumb_schema(meta["breadcrumb"], canonical, lang)
    if meta.get("faq_schema"):
        extra_schema += "\n" + (faq_schema_html() if lang == "zh" else faq_schema_html_en())

    return f"""<!doctype html>
<html lang="{html_lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{meta['title']}</title>
  <meta name="description" content="{meta['description']}" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" hreflang="zh-CN" href="{hreflang_zh if lang == 'zh' else meta.get('hreflang_zh', f'https://70nyc.com/{slug}/')}" />
  <link rel="alternate" hreflang="en" href="{hreflang_en}" />
  <link rel="alternate" hreflang="x-default" href="https://70nyc.com/" />
  <meta property="og:locale" content="{og_locale}" />
  <meta property="og:locale:alternate" content="{og_alt}" />
  <meta property="og:title" content="{meta['title']}" />
  <meta property="og:description" content="{meta['description']}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,700;0,9..40,900;1,9..40,400&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/style.css" />
  <script src="/assets/lang-detect.js"></script>
{extra_schema}
</head>
<body class="page-sub">
{nav_html(nav_items, active, lang, slug)}

  <main>
{section_html}
  </main>

{footer_html(lang)}

  <script src="/assets/main.js"></script>
</body>
</html>
"""


def main() -> None:
    zh_html = (ROOT / "index.html").read_text(encoding="utf-8")
    en_html = (ROOT / "en.html").read_text(encoding="utf-8")

    for page in PAGES:
        slug = page["slug"]
        sid = page["section_id"]

        zh_section = patch_section(extract_section(zh_html, sid), "zh", slug)
        en_section = patch_section(extract_section(en_html, sid), "en", slug)

        zh_out = ROOT / slug / "index.html"
        en_out = ROOT / "en" / slug / "index.html"
        zh_out.write_text(build_page("zh", page, page["zh"], zh_section), encoding="utf-8")
        en_out.write_text(build_page("en", page, page["en"], en_section), encoding="utf-8")
        print(f"Wrote {zh_out.relative_to(ROOT)}")
        print(f"Wrote {en_out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
