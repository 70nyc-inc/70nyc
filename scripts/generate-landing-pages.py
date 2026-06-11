#!/usr/bin/env python3
"""One-shot generator: extract sections from index.html / en/index.html into SEO landing pages."""
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
            "form_redirect": "https://70nyc.com/contact/?success=1#contact",
        },
        "en": {
            "title": "Contact 70NYC | Free NYC Web Design Consultation",
            "description": "Get a free consultation for NYC web design, SEO, and Google Ads. Call 386-316-1848 — serving Manhattan, Flushing, Brooklyn, and Long Island.",
            "nav_label": "Contact",
            "breadcrumb": "Contact Us",
            "hreflang_zh": "https://70nyc.com/contact/",
            "form_subject": "70NYC Website Inquiry (English)",
            "form_redirect": "https://70nyc.com/en/contact/?success=1#contact",
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
    ("home", "/en/", "Home"),
    ("services", "/en/services/", "Services"),
    ("process", "/en/process/", "Process"),
    ("about", "/en/about/", "About"),
    ("faq", "/en/faq/", "FAQ"),
    ("contact", "/en/contact/", "Contact"),
]

SEO_CONTENT: dict[str, dict[str, dict]] = {
    "services": {
        "zh": {
            "keywords": "纽约网站设计, 纽约网站公司, 纽约网站设计师, 曼哈顿网站设计, 法拉盛网站设计, 布鲁克林网站设计, 长岛网站设计, 网页设计, 网站开发, SEO优化, Google Ads, 社交媒体营销, 手机应用开发",
            "eyebrow": "大纽约 · 华人企业专属",
            "h1": "让纽约客户<br><span>先找到您，再选择您</span>",
            "lead": "网站、搜索、广告与社媒不是单点任务——我们按行业与区域定制增长组合，把每一分预算导向真实咨询与成交。",
            "stats": [("13+", "年本地经验"), ("100+", "交付项目"), ("20+", "服务行业"), ("8", "大纽约区域")],
            "tags": ["曼哈顿网站设计", "法拉盛网站设计", "布鲁克林网站设计", "长岛网站设计", "纽约华人网站制作", "餐馆网站设计"],
            "topics": [
                ("适合谁", "首次建站、改版升级、或多渠道获客遇到瓶颈的华人企业——餐馆、美容、装修、法律、医疗、教育、电商等。"),
                ("我们如何配合", "先厘清客户从哪里来，再决定网站结构、本地 SEO、Google Ads 与社媒如何分工，避免「只建站、不带量」。"),
                ("区域与语言", "曼哈顿、法拉盛、布鲁克林、长岛及大纽约可面谈；中英双语团队，全美及海外远程协作流程一致。"),
            ],
            "highlights": ["Google Partner 认证", "按月透明数据报告", "阶段交付物可验收", "可单项或打包合作", "上线后持续优化", "无隐藏费用"],
            "related_title": "继续探索",
            "related": [("/process/", "项目流程", "四步标准交付"), ("/about/", "关于我们", "团队与案例"), ("/faq/", "项目 FAQ", "合作常见问题"), ("/contact/", "联系我们", "免费咨询")],
        },
        "en": {
            "keywords": "NYC web design, New York web design, Manhattan web design, Flushing web design, Brooklyn web design, Long Island web design, website development, SEO, Google Ads, social media marketing, mobile app development",
            "eyebrow": "Greater NYC · Local Businesses",
            "h1": "Get Found in NYC.<br><span>Then Get Chosen.</span>",
            "lead": "Web, search, ads, and social work best as a system — we build channel mixes by industry and neighborhood so spend drives real inquiries.",
            "stats": [("13+", "Years local"), ("100+", "Projects"), ("20+", "Industries"), ("8", "NYC regions")],
            "tags": ["Manhattan web design", "Flushing web design", "Brooklyn web design", "Long Island web design", "NYC website company", "Restaurant websites"],
            "topics": [
                ("Who It's For", "New sites, redesigns, or businesses stuck on growth — restaurants, beauty, construction, legal, healthcare, education, e-commerce."),
                ("How We Work", "We map where customers come from first, then align site structure, local SEO, Google Ads, and social — not just a pretty homepage."),
                ("Areas & Language", "Meetings across Manhattan, Flushing, Brooklyn, Long Island, and the metro; bilingual team with the same process nationwide."),
            ],
            "highlights": ["Google Partner certified", "Transparent monthly reports", "Phase-based deliverables", "À la carte or bundled", "Post-launch optimization", "No hidden fees"],
            "related_title": "Keep Exploring",
            "related": [("/en/process/", "Our Process", "4-step delivery"), ("/en/about/", "About Us", "Team & cases"), ("/en/faq/", "FAQ", "Common questions"), ("/en/contact/", "Contact", "Free consult")],
        },
    },
    "about": {
        "zh": {
            "keywords": "纽约网站设计公司, 纽约华人网站设计, 纽约数字营销, 曼哈顿网站公司, 法拉盛网站设计师, 布鲁克林网站制作, 长岛网站开发, Google Partner",
            "eyebrow": "纽约本地 · 自 2012",
            "h1": "不只做网站，<br><span>更懂华人生意怎么增长</span>",
            "lead": "13 年扎根大纽约，我们陪客户从第一张官网走到搜索排名、广告投放与社媒运营——用数据说话，做长期伙伴。",
            "stats": [("13+", "年深耕"), ("100+", "成功项目"), ("300%+", "案例增长"), ("Google", "Partner")],
            "tags": ["纽约网站设计公司", "纽约华人网站设计", "曼哈顿网站公司", "法拉盛网站设计师", "布鲁克林网站制作", "长岛网站开发"],
            "topics": [
                ("我们的差异", "懂中文沟通、懂本地消费习惯、懂各行业获客路径——不是模板建站，而是按生意目标设计方案。"),
                ("行业积累", "餐饮、美容、装修、法律、医疗、教育、电商等 20+ 垂直领域，沉淀可复用的增长方法论。"),
                ("合作方式", "透明报价、阶段验收、月度复盘；可选维护、SEO 与广告代运营，让网站持续带来线索。"),
            ],
            "highlights": ["纽约办公室可面谈", "中英双语无障碍", "真实案例可验证", "Google Partner", "全美远程协作", "长期运维支持"],
            "related_title": "相关页面",
            "related": [("/services/", "我们的服务", "网站设计与营销"), ("/process/", "项目流程", "标准交付步骤"), ("/faq/", "项目 FAQ", "合作常见问题"), ("/contact/", "联系我们", "预约免费咨询")],
        },
        "en": {
            "keywords": "NYC web design company, New York digital marketing, Manhattan web agency, Flushing web designer, Brooklyn website development, Long Island web design, Google Partner",
            "eyebrow": "Based in NYC · Since 2012",
            "h1": "More Than a Website.<br><span>A Growth Partner.</span>",
            "lead": "13 years in the NYC market — from first launch to search, ads, and social — we measure what matters and stay for the long run.",
            "stats": [("13+", "Years"), ("100+", "Projects"), ("300%+", "Case growth"), ("Google", "Partner")],
            "tags": ["NYC web design company", "Manhattan web agency", "Flushing web designer", "Brooklyn web development", "Long Island web design", "NYC digital marketing"],
            "topics": [
                ("What Sets Us Apart", "Bilingual communication, local buying behavior, and vertical playbooks — strategy first, not template sites."),
                ("Industry Depth", "20+ sectors including restaurants, beauty, construction, legal, healthcare, education, and e-commerce."),
                ("How We Partner", "Transparent quotes, phase sign-offs, monthly reviews — plus optional maintenance, SEO, and ad management."),
            ],
            "highlights": ["NYC office — meetings welcome", "Bilingual team", "Verifiable case studies", "Google Partner", "Nationwide remote", "Ongoing support"],
            "related_title": "Related Pages",
            "related": [("/en/services/", "Services", "Web design & marketing"), ("/en/process/", "Process", "Delivery steps"), ("/en/faq/", "FAQ", "Common questions"), ("/en/contact/", "Contact", "Free consultation")],
        },
    },
    "process": {
        "zh": {
            "keywords": "纽约网站设计流程, 网站开发流程, 纽约网站制作步骤, 网页设计交付, 网站项目排期, 曼哈顿网站公司",
            "eyebrow": "标准交付 · 全程透明",
            "h1": "四步上线，<br><span>每一步都可追踪</span>",
            "lead": "从第一次沟通到网站上线与运维，每个阶段都有书面交付物与验收节点——您始终知道进度、成本与下一步。",
            "stats": [("2–4", "周标准交付"), ("4", "大阶段"), ("100%", "报价透明"), ("24h", "内响应咨询")],
            "tags": ["纽约网站设计流程", "网站开发流程", "网页设计交付", "网站项目排期", "纽约网站制作", "网站上线运维"],
            "topics": [
                ("为什么分阶段", "降低返工与超支风险：需求、设计、开发范围在上线前锁定，变更先评估再执行。"),
                ("您需要参与多少", "关键节点确认即可——首次访谈、设计稿、上线验收；日常素材我们可协助补齐。"),
                ("上线之后", "培训、文档、维护套餐与效果优化可选，网站不是「交付即结束」。"),
            ],
            "highlights": ["需求 Brief 书面化", "设计稿确认后开发", "含 SEO 基础配置", "移动端适配", "后台操作培训", "可选年度维护"],
            "related_title": "下一步",
            "related": [("/services/", "我们的服务", "了解服务项目"), ("/about/", "关于我们", "认识团队"), ("/faq/", "项目 FAQ", "周期与报价"), ("/contact/", "联系我们", "获取方案")],
        },
        "en": {
            "keywords": "NYC web design process, website development workflow, web project delivery, site launch timeline, New York website company",
            "eyebrow": "Standard Delivery · Full Visibility",
            "h1": "Four Steps to Launch.<br><span>Nothing Hidden.</span>",
            "lead": "From first call to go-live and beyond — every phase has written deliverables and sign-off so you always know status, cost, and what's next.",
            "stats": [("2–4", "Week delivery"), ("4", "Phases"), ("100%", "Clear pricing"), ("24h", "Response time")],
            "tags": ["Web design process", "Development workflow", "Project delivery", "Launch timeline", "NYC website company", "Ongoing support"],
            "topics": [
                ("Why Phases Matter", "Scope, design, and build are locked before launch — changes are quoted first to avoid rework and overruns."),
                ("Your Time Commitment", "Key checkpoints only: kickoff, design approval, launch review — we help fill material gaps."),
                ("After Launch", "Training, docs, maintenance plans, and optimization — your site keeps working for you."),
            ],
            "highlights": ["Written project brief", "Build after design sign-off", "Basic SEO included", "Mobile-ready", "Admin training", "Optional annual care"],
            "related_title": "Next Steps",
            "related": [("/en/services/", "Services", "What we offer"), ("/en/about/", "About", "Meet the team"), ("/en/faq/", "FAQ", "Timeline & pricing"), ("/en/contact/", "Contact", "Get a proposal")],
        },
    },
    "faq": {
        "zh": {
            "keywords": "纽约网站设计 FAQ, 网站制作周期, 网站设计报价, 网站开发交付, 网站维护, 华人网站设计公司",
            "eyebrow": "合作前必读",
            "h1": "建站之前，<br><span>先把这些问题想清楚</span>",
            "lead": "周期、报价、修改范围与上线后支持——我们汇总客户最常问的决定性问题，帮您更快判断是否适合合作。",
            "stats": [("7", "个常见问题"), ("2–4", "周典型周期"), ("0", "隐藏费用"), ("1", "次沟通可启动")],
            "tags": ["网站设计报价", "网站制作周期", "网站开发交付", "网站维护服务", "纽约网站设计公司", "华人网站制作"],
            "topics": [
                ("还没准备好素材？", "没关系——首次沟通后我们会整理需求清单，帮您补齐 Logo、文案与功能项。"),
                ("担心价格不透明？", "需求确认后提供明细报价，各阶段交付物写进合同，签约前价格锁定。"),
                ("上线后没人管？", "含技术支持期；可选年度维护、SEO 与广告代运营，持续优化效果。"),
            ],
            "highlights": ["首次沟通免费", "明细报价单", "合理设计修改", "源代码按约交付", "远程协作成熟", "全美客户均可"],
            "related_title": "还需要了解",
            "related": [("/services/", "我们的服务", "服务项目总览"), ("/process/", "项目流程", "四步交付"), ("/about/", "关于我们", "团队介绍"), ("/contact/", "联系我们", "提交咨询")],
        },
        "en": {
            "keywords": "NYC web design FAQ, website timeline, web design pricing, project deliverables, website maintenance, New York website company",
            "eyebrow": "Before You Commit",
            "h1": "Questions Worth<br><span>Asking First.</span>",
            "lead": "Timelines, pricing, revision scope, and post-launch support — the decisions that matter most, answered upfront.",
            "stats": [("7", "Common topics"), ("2–4", "Week typical"), ("0", "Hidden fees"), ("1", "Call to start")],
            "tags": ["Web design pricing", "Project timeline", "Deliverables", "Website maintenance", "NYC web design", "Website company"],
            "topics": [
                ("Not Ready with Assets?", "No problem — after the first call we build a requirements list and help fill gaps."),
                ("Worried About Pricing?", "Itemized quotes after scope is clear — deliverables in writing, price locked before signing."),
                ("After Launch?", "Support period included; optional maintenance, SEO, and ad management for ongoing growth."),
            ],
            "highlights": ["Free first consultation", "Itemized quotes", "Reasonable design revisions", "Source per contract", "Remote-ready workflow", "Clients nationwide"],
            "related_title": "Learn More",
            "related": [("/en/services/", "Services", "Full service list"), ("/en/process/", "Process", "4-step delivery"), ("/en/about/", "About", "Our team"), ("/en/contact/", "Contact", "Submit inquiry")],
        },
    },
    "contact": {
        "zh": {
            "keywords": "联系纽约网站设计, 纽约网站公司电话, 曼哈顿网站设计咨询, 法拉盛网站制作, 布鲁克林网站开发, 长岛网站设计, 免费咨询",
            "eyebrow": "免费咨询 · 无销售压力",
            "h1": "聊聊您的生意，<br><span>我们给出可执行方案</span>",
            "lead": "一通电话或一张表单即可开始——了解目标与客户来源后，24 小时内回复初步思路、周期预估与服务建议。",
            "stats": [("386", "316-1848"), ("24h", "内回复"), ("中英", "双语"), ("全美", "可远程")],
            "tags": ["联系纽约网站设计", "纽约网站公司", "曼哈顿网站设计咨询", "法拉盛网站制作", "布鲁克林网站开发", "长岛网站设计"],
            "topics": [
                ("第一次沟通聊什么", "您的行业、现有线上渠道、目标客户与预算方向——不需要技术背景。"),
                ("见面还是远程", "曼哈顿、法拉盛、布鲁克林、长岛可预约面谈；外地客户用视频、微信 / WhatsApp 同样高效。"),
                ("咨询之后呢", "收到需求摘要与参考方向，再决定是否进入正式报价——全程自愿，无捆绑销售。"),
            ],
            "highlights": ["电话 386-316-1848", "表单下方直接提交", "免费需求梳理", "可参考同行业案例", "透明报价流程", "签约前无义务"],
            "related_title": "提交咨询前可了解",
            "related": [("/services/", "我们的服务", "网站设计与营销"), ("/process/", "项目流程", "合作步骤"), ("/faq/", "项目 FAQ", "常见问题"), ("/about/", "关于我们", "团队与案例")],
        },
        "en": {
            "keywords": "contact NYC web design, New York website company phone, Manhattan web design consultation, Flushing website development, Brooklyn web design, Long Island website, free consult",
            "eyebrow": "Free Consult · No Pressure",
            "h1": "Tell Us Your Goals.<br><span>We'll Map a Plan.</span>",
            "lead": "One call or a short form is enough — we reply within 24 hours with initial direction, timeline guidance, and service recommendations.",
            "stats": [("386", "316-1848"), ("24h", "Reply"), ("EN/ZH", "Bilingual"), ("US-wide", "Remote OK")],
            "tags": ["Contact NYC web design", "New York website company", "Manhattan consultation", "Flushing web development", "Brooklyn web design", "Free consult"],
            "topics": [
                ("First Conversation", "Your industry, current channels, target customers, and budget direction — no tech background needed."),
                ("In Person or Remote", "Meetings across the NYC metro; video, WeChat, or WhatsApp works just as well elsewhere."),
                ("What Happens Next", "A summary and direction — you decide if you want a formal quote. No obligation."),
            ],
            "highlights": ["Call 386-316-1848", "Form below", "Free needs review", "Relevant case references", "Transparent quoting", "No obligation to sign"],
            "related_title": "Before You Reach Out",
            "related": [("/en/services/", "Services", "Web & marketing"), ("/en/process/", "Process", "How we work"), ("/en/faq/", "FAQ", "Common questions"), ("/en/about/", "About", "Team & cases")],
        },
    },
}


HERO_DECO = {
    "services": '<div class="page-seo-hero-deco page-seo-hero-deco--orbit" aria-hidden="true"></div>',
    "about": '<div class="page-seo-hero-deco page-seo-hero-deco--stars" aria-hidden="true"></div>',
    "process": '<div class="page-seo-hero-deco page-seo-hero-deco--grid" aria-hidden="true"></div>',
    "faq": '<div class="page-seo-hero-deco page-seo-hero-deco--bokeh" aria-hidden="true"></div>',
    "contact": '<div class="page-seo-hero-deco page-seo-hero-deco--horizon" aria-hidden="true"></div>',
}


def seo_intro_html(lang: str, slug: str, seo: dict, breadcrumb: str) -> str:
    home_href = "/" if lang == "zh" else "/en/"
    home_label = "首页" if lang == "zh" else "Home"
    contact_href = "#contact" if slug == "contact" else ("/contact/" if lang == "zh" else "/en/contact/")
    cta_label = "预约免费咨询" if lang == "zh" else "Book Free Consult"
    tags = "".join(f"<span>{t}</span>" for t in seo["tags"])
    stats = "".join(
        f'<div class="page-seo-stat"><b>{val}</b><span>{label}</span></div>'
        for val, label in seo["stats"]
    )
    deco = HERO_DECO.get(slug, "")
    return f"""    <div class="page-seo-hero page-seo-hero--{slug}">
      <div class="page-seo-hero-bg" aria-hidden="true"></div>
      <div class="page-seo-hero-glow" aria-hidden="true"></div>
      {deco}
      <div class="page-seo-hero-inner">
        <nav class="page-seo-breadcrumb" aria-label="{'面包屑导航' if lang == 'zh' else 'Breadcrumb'}">
          <ol>
            <li><a href="{home_href}">{home_label}</a></li>
            <li aria-current="page">{breadcrumb}</li>
          </ol>
        </nav>
        <div class="page-seo-hero-focus">
          <span class="page-seo-eyebrow">{seo['eyebrow']}</span>
          <h1>{seo['h1']}</h1>
          <p class="page-seo-lead">{seo['lead']}</p>
          <div class="page-seo-hero-actions">
            <a class="btn btn-primary" href="{contact_href}">{cta_label} →</a>
          </div>
        </div>
        <div class="page-seo-stats" aria-label="{'关键数据' if lang == 'zh' else 'Key figures'}">{stats}</div>
        <div class="page-seo-keywords" aria-label="{'服务关键词' if lang == 'zh' else 'Keywords'}">{tags}</div>
      </div>
    </div>
"""


def seo_supplement_html(lang: str, seo: dict) -> str:
    aside_label = "为什么选择 70NYC" if lang == "zh" else "Why 70NYC"
    section_title = "延伸阅读" if lang == "zh" else "More Context"
    highlights = "".join(f"<li>{h}</li>" for h in seo["highlights"])
    cards = []
    for i, (title, body) in enumerate(seo["topics"], 1):
        cards.append(
            f'          <article class="page-seo-topic-card">\n'
            f'            <span class="page-seo-topic-num">0{i}</span>\n'
            f"            <h3>{title}</h3>\n"
            f"            <p>{body}</p>\n"
            f"          </article>"
        )
    grid = "\n".join(cards)
    return f"""    <section class="page-seo-supplement" aria-label="{'页面详细介绍' if lang == 'zh' else 'Page overview'}">
      <div class="page-seo-supplement-inner">
        <div class="page-seo-supplement-head">
          <span class="label">70NYC</span>
          <h2>{section_title}</h2>
        </div>
        <div class="page-seo-topic-grid">
{grid}
        </div>
        <aside class="page-seo-supplement-aside">
          <b>{aside_label}</b>
          <ul class="page-seo-highlight-list">{highlights}</ul>
        </aside>
      </div>
    </section>
"""


def seo_related_html(lang: str, seo: dict) -> str:
    cards = []
    for href, title, desc in seo["related"]:
        cards.append(
            f'        <a class="page-seo-related-card" href="{href}">\n'
            f'          <span class="page-seo-related-arrow" aria-hidden="true">→</span>\n'
            f"          <b>{title}</b>\n"
            f"          <span>{desc}</span>\n"
            f"        </a>"
        )
    grid = "\n".join(cards)
    return f"""    <nav class="page-seo-related" aria-label="{'相关页面' if lang == 'zh' else 'Related pages'}">
      <div class="page-seo-related-inner">
        <span class="label">{seo['related_title']}</span>
        <div class="page-seo-related-grid">
{grid}
        </div>
      </div>
    </nav>
"""


def extract_section(html: str, section_id: str) -> str:
    pattern = rf'(<section[^>]*\bid="{re.escape(section_id)}"[^>]*>)(.*?)(</section>)'
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        raise ValueError(f"Section id={section_id!r} not found")
    return match.group(0)


def patch_section(body: str, lang: str, slug: str) -> str:
    prefix = "/en" if lang == "en" else ""
    body = body.replace('src="assets/', 'src="/assets/')
    body = body.replace("src='assets/", "src='/assets/")
    body = body.replace("href=\"#contact\"", f'href="{prefix}/contact/"')
    body = body.replace("href='#contact'", f"href='{prefix}/contact/'")
    if slug == "contact":
        if lang == "zh":
            body = body.replace(
                'value="https://70nyc.com/?success=1#contact"',
                'value="https://70nyc.com/contact/?success=1#contact"',
            )
        else:
            body = body.replace(
                'value="https://70nyc.com/en/?success=1#contact"',
                'value="https://70nyc.com/en/contact/?success=1#contact"',
            )
    return body


def nav_html(nav_items, active: str, lang: str, slug: str) -> str:
    links = []
    for key, href, label in nav_items:
        cls = ' class="active"' if key == active else ""
        data = f' data-nav="{key}"' if key != active or True else ""
        links.append(f'      <a href="{href}"{data}{cls}>{label}</a>')
    zh_path = "/" if slug == "home" else f"/{slug}/"
    en_path = "/en/" if slug == "home" else f"/en/{slug}/"
    lang_switch = (
        f'<a class="lang-switch" href="{en_path}?lang=en" hreflang="en">EN</a>'
        if lang == "zh"
        else f'<a class="lang-switch" href="{zh_path}?lang=zh" hreflang="zh-CN">中文</a>'
    )
    consult_href = "#contact" if slug == "contact" else ("/contact/" if lang == "zh" else "/en/contact/")
    consult_label = "免费咨询" if lang == "zh" else "Free Consult"
    logo_small = "纽约数字营销专家" if lang == "zh" else "NYC Digital Marketing"
    home_href = "/" if lang == "zh" else "/en/"
    menu_label = "打开菜单" if lang == "zh" else "Open menu"
    return f"""  <header class="site-header" id="header">
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
        <a href="/services/web-design/">网页设计与网站开发</a>
        <a href="/services/mobile-app/">手机应用开发与设计</a>
        <a href="/services/google-ads/">专业广告推广服务</a>
        <a href="/services/seo/">SEO 优化</a>
        <a href="/services/social-media/">社交媒体管理</a>
        <a href="/areas/">服务区域</a>
        <a href="/nationwide/">全美远程</a>
        <a href="/process/">项目流程</a>
        <a href="/sitemap/">网站地图</a>
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
        <p>NYC web design and development team — web design, mobile apps, graphic design, restaurant websites, advertising, and SEO for local businesses.</p>
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
        <a href="/en/services/web-design/">Web Design &amp; Development</a>
        <a href="/en/services/mobile-app/">Mobile App Development</a>
        <a href="/en/services/google-ads/">Digital Advertising</a>
        <a href="/en/services/seo/">SEO</a>
        <a href="/en/services/social-media/">Social Media</a>
        <a href="/en/areas/">Service Areas</a>
        <a href="/en/nationwide/">Nationwide Remote</a>
        <a href="/en/process/">Process</a>
        <a href="/en/sitemap/">Sitemap</a>
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
      {"@type": "Question", "name": "What do I need before we begin?", "acceptedAnswer": {"@type": "Answer", "text": "Usually just a business overview, reference websites, existing logo/images, and core features you need. We prepare a requirements doc after the first call and help fill any gaps — no need to have everything ready upfront."}},
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

    seo = SEO_CONTENT[slug][lang]
    intro_block = seo_intro_html(lang, slug, seo, meta["breadcrumb"])
    supplement_block = seo_supplement_html(lang, seo)
    related_block = seo_related_html(lang, seo)

    return f"""<!doctype html>
<html lang="{html_lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{meta['title']}</title>
  <meta name="description" content="{meta['description']}" />
  <meta name="keywords" content="{seo['keywords']}" />
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
  <meta property="og:image" content="https://70nyc.com/assets/nyc-hero.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="https://70nyc.com/assets/nyc-hero.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,700;0,9..40,900;1,9..40,400&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/style.css?v=4" />
  <script src="/assets/lang-detect.js?v=4"></script>
{extra_schema}
</head>
<body class="page-sub">
{nav_html(nav_items, active, lang, slug)}

  <main>
{intro_block}
{section_html}
{supplement_block}
{related_block}
  </main>

{footer_html(lang)}

  <script src="/assets/main.js?v=8"></script>
</body>
</html>
"""


def main() -> None:
    zh_html = (ROOT / "index.html").read_text(encoding="utf-8")
    en_html = (ROOT / "en" / "index.html").read_text(encoding="utf-8")

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
