#!/usr/bin/env python3
"""
70NYC SEO page generator — nationwide, NYC area hubs, and blog.

Usage:
  python3 scripts/generate-seo-pages.py all          # everything + sitemap
  python3 scripts/generate-seo-pages.py nationwide   # /nationwide/ (zh + en)
  python3 scripts/generate-seo-pages.py areas        # /areas/ hub + 6 districts
  python3 scripts/generate-seo-pages.py blog         # /blog/ index (+ posts from BLOG_POSTS)
  python3 scripts/generate-seo-pages.py sitemap      # merge new URLs into sitemap.xml only

Edit content in this file:
  - NATIONWIDE, AREAS, BLOG_POSTS
  - SERVICES (footer / service grid links)
  - SITE (asset cache-bust versions)

New blog post: append to BLOG_POSTS, then run:
  python3 scripts/generate-seo-pages.py blog
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://70nyc.com"

SITE = {
    "style_css": "v=7",
    "main_js": "v=10",
    "lang_detect_js": "v=4",
    "og_image": f"{DOMAIN}/assets/nyc-hero.png",
}

GTAG_SNIPPET = (Path(__file__).resolve().parent / "gtag-snippet.html").read_text(encoding="utf-8")

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

SERVICES = [
    ("web-design", "网页设计与网站开发", "Web Design & Development"),
    ("seo", "SEO 优化", "SEO"),
    ("google-ads", "专业广告推广", "Digital Advertising"),
    ("social-media", "社交媒体管理", "Social Media"),
    ("mobile-app", "手机应用开发", "Mobile App Development"),
]

HERO_THEMES = ["services", "about", "process", "faq", "contact"]
HERO_DECOS = ["orbit", "stars", "grid", "bokeh", "horizon"]

NATIONWIDE = {
    "slug": "nationwide",
    "zh": {
        "title": "全美远程网站设计与数字营销｜华人企业｜70NYC",
        "description": "70NYC 总部位于纽约，通过远程协作为全美及海外华人企业提供网站设计、SEO、Google Ads 与社交媒体服务——流程与本地客户一致。",
        "breadcrumb_parent": None,
        "breadcrumb": "全美远程服务",
        "eyebrow": "Nationwide Remote · 华人企业",
        "h1": "不在纽约，<br><span>也能获得同样的专业交付</span>",
        "lead": "视频会议、微信 / WhatsApp 与项目管理工具——我们从纽约为加州、德州、佛州、华盛顿州等各地的华人餐馆、美容、装修、法律、医疗企业提供网站设计、SEO 与 Google Ads，流程透明、阶段可验收。",
        "cta_primary": ("获取远程方案", "/contact/"),
        "cta_ghost": ("纽约服务区域", "/areas/"),
        "stats": [("全美", "远程协作"), ("13+", "年经验"), ("中英", "双语团队"), ("24h", "内回复")],
        "tags": ["全美网站设计", "远程网站开发", "华人企业SEO", "远程Google Ads", "纽约总部", "全美华人营销"],
        "label": "70NYC Nationwide",
        "section_h2": "远程合作如何运作",
        "topics": [
            ("沟通方式", "Kickoff 用 Zoom/腾讯会议；日常微信、邮件与 Notion/飞书看板同步进度。关键节点（设计稿、上线）视频验收，与纽约本地客户相同标准。"),
            ("交付内容", "响应式网站、CMS 后台、基础 SEO、上线培训文档。可选月度 SEO、Google Ads 代运营与社媒内容——按月报告，数据透明。"),
            ("适合谁", "分店在多地、总部在纽约；或人在外州/海外、目标客户在纽约/全美；需要中英双语网站与搜索覆盖的华人企业。"),
            ("与纽约本地服务的关系", "大纽约六区可预约面谈；外地客户走远程流程。同一团队、同一报价逻辑，不因远程降低交付标准。"),
        ],
        "highlights_title": "远程客户常选服务",
        "highlights": ["企业官网改版", "餐馆 / 外卖网站", "本地 SEO + Google Ads", "新店开业推广", "中英双语建站", "上线后运维"],
        "footer_seo": "全美远程：网站设计 · SEO · Google Ads · 社交媒体 · 华人企业数字营销 · 纽约总部远程交付",
        "schema_name": "全美远程网站设计与数字营销",
        "schema_desc": "远程网站设计、SEO、Google Ads 与社媒运营，服务全美华人企业。",
        "related": [
            ("/areas/", "纽约服务区域", "曼哈顿·法拉盛等"),
            ("/services/web-design/", "网站设计", "定制建站"),
            ("/services/seo/", "SEO 优化", "自然流量"),
            ("/contact/", "免费咨询", "24h 内回复"),
        ],
    },
    "en": {
        "title": "Nationwide Remote Web Design & Marketing | Chinese Businesses | 70NYC",
        "description": "70NYC is NYC-based and serves Chinese-owned businesses nationwide with remote web design, SEO, Google Ads, and social media — same process as local clients.",
        "breadcrumb_parent": None,
        "breadcrumb": "Nationwide Remote",
        "eyebrow": "Nationwide Remote",
        "h1": "Not in NYC?<br><span>Same Team, Same Standards.</span>",
        "lead": "Video calls, WeChat/WhatsApp, and shared project boards — we deliver websites, SEO, and Google Ads for restaurants, salons, contractors, and clinics across CA, TX, FL, WA, and beyond from our New York HQ.",
        "cta_primary": ("Get Remote Proposal", "/en/contact/"),
        "cta_ghost": ("NYC Service Areas", "/en/areas/"),
        "stats": [("US-wide", "Remote OK"), ("13+", "Years"), ("Bilingual", "EN & 中文"), ("24h", "Reply")],
        "tags": ["Nationwide web design", "Remote development", "Chinese business SEO", "Remote Google Ads", "NYC HQ", "US Chinese marketing"],
        "label": "70NYC Nationwide",
        "section_h2": "How Remote Delivery Works",
        "topics": [
            ("Communication", "Kickoff on Zoom; day-to-day via WeChat, email, and shared boards. Design and launch reviews on video — same checkpoints as NYC clients."),
            ("Deliverables", "Responsive site, CMS, basic SEO, training docs. Optional monthly SEO, Google Ads, and social — transparent reporting."),
            ("Who It's For", "Multi-location brands, owners outside NY serving US customers, and businesses needing bilingual web + search coverage."),
            ("NYC + Remote", "In-person meetings across six NYC areas; everywhere else uses the same remote playbook. One team, one quality bar."),
        ],
        "highlights_title": "Popular Remote Services",
        "highlights": ["Corporate site redesign", "Restaurant websites", "Local SEO + Google Ads", "New location launch", "Bilingual websites", "Post-launch care"],
        "footer_seo": "Nationwide remote: web design · SEO · Google Ads · social media · Chinese business marketing · delivered from NYC",
        "schema_name": "Nationwide Remote Web Design & Marketing",
        "schema_desc": "Remote web design, SEO, Google Ads, and social for Chinese-owned businesses across the US.",
        "related": [
            ("/en/areas/", "NYC Areas", "Manhattan · Flushing…"),
            ("/en/services/web-design/", "Web Design", "Custom builds"),
            ("/en/services/seo/", "SEO", "Organic growth"),
            ("/en/contact/", "Contact", "Reply within 24h"),
        ],
    },
}

AREAS_HUB = {
    "zh": {
        "title": "纽约服务区域｜曼哈顿·法拉盛·布鲁克林·长岛｜70NYC",
        "description": "70NYC 服务纽约曼哈顿、法拉盛、布鲁克林、布朗克斯、史泰登岛、长岛等区域，提供网站设计、SEO、Google Ads 与社媒运营。",
        "breadcrumb": "服务区域",
        "eyebrow": "Greater NYC",
        "h1": "纽约六大区域<br><span>本地团队，就近服务</span>",
        "lead": "曼哈顿、法拉盛、布鲁克林、布朗克斯、史泰登岛、长岛——我们熟悉各区华人商业生态，可面谈亦可远程，按区域定制获客方案。",
        "section_h2": "选择您的区域",
        "intro": "点击下列区域了解本地服务详情，或查看全美远程协作方式。",
    },
    "en": {
        "title": "NYC Service Areas | Manhattan · Flushing · Brooklyn · Long Island | 70NYC",
        "description": "70NYC serves Manhattan, Flushing, Brooklyn, the Bronx, Staten Island, and Long Island with web design, SEO, Google Ads, and social media.",
        "breadcrumb": "Service Areas",
        "eyebrow": "Greater NYC",
        "h1": "Six NYC Areas.<br><span>Local Team, Local Insight.</span>",
        "lead": "Manhattan, Flushing, Brooklyn, the Bronx, Staten Island, and Long Island — we know each market and meet in person or work remotely with area-specific growth plans.",
        "section_h2": "Choose Your Area",
        "intro": "Select a region below for local service details, or see our nationwide remote option.",
    },
}

AREAS = [
    {
        "slug": "manhattan",
        "area_served": "Manhattan",
        "zh": {
            "title": "曼哈顿网站设计｜纽约 Manhattan 网页开发与 SEO｜70NYC",
            "description": "70NYC 为曼哈顿华人企业提供网站设计、SEO、Google Ads 与社媒运营——律所、餐馆、美容、金融等，可预约曼哈顿面谈。",
            "breadcrumb": "曼哈顿",
            "eyebrow": "Manhattan · 曼哈顿",
            "h1": "曼哈顿网站设计<br><span>专业形象匹配纽约核心商圈</span>",
            "lead": "曼哈顿客户对品牌质感与响应速度要求更高——我们为中城、下城、唐人街及周边华人企业提供定制官网、本地 SEO 与 Google Ads，支持中英双语。",
            "tags": ["曼哈顿网站设计", "Manhattan web design", "纽约中城网站", "曼哈顿SEO", "曼哈顿Google Ads", "华人律所网站"],
            "topics": [
                ("典型客户", "律所、诊所、金融顾问、精品餐馆、高端美容、地产中介——需要传递专业信任与清晰服务边界。"),
                ("本地获客", "「Manhattan + 行业」搜索、Google Maps、落地页转化优化；与 Midtown、Downtown 客户搜索习惯对齐。"),
                ("交付方式", "曼哈顿可约办公室或咖啡厅面谈；设计评审与上线验收支持现场或视频。"),
                ("服务组合", "官网 + 本地 SEO 是基础；高竞争行业可叠加 Google Ads 与 LinkedIn/Instagram 内容。"),
            ],
            "highlights": ["律所形象站", "诊所预约站", "精品餐饮", "高端沙龙", "地产经纪", "中英双语"],
            "footer_seo": "曼哈顿网站设计 · Manhattan web design · 曼哈顿SEO · 曼哈顿Google Ads · 纽约中城网站开发",
        },
        "en": {
            "title": "Manhattan Web Design | NYC Website Development & SEO | 70NYC",
            "description": "Web design, SEO, Google Ads, and social for Chinese-owned businesses in Manhattan — law, restaurants, beauty, finance. In-person meetings available.",
            "breadcrumb": "Manhattan",
            "eyebrow": "Manhattan NYC",
            "h1": "Manhattan Web Design<br><span>Built for NYC's Core Markets</span>",
            "lead": "Manhattan buyers expect polish and speed — we build bilingual sites, local SEO, and Google Ads for law firms, clinics, restaurants, and salons across Midtown, Downtown, and Chinatown.",
            "tags": ["Manhattan web design", "NYC Midtown website", "Manhattan SEO", "Manhattan Google Ads", "Chinese business Manhattan", "Law firm websites"],
            "topics": [
                ("Who We Serve", "Law, healthcare, finance, fine dining, premium beauty, real estate — brands that must earn trust fast."),
                ("Local Acquisition", "Manhattan + industry keywords, Maps presence, landing pages tuned to Midtown/Downtown search behavior."),
                ("How We Meet", "In-person across Manhattan or video reviews — same deliverables and timelines."),
                ("Typical Stack", "Website + local SEO first; competitive verticals add Google Ads and social content."),
            ],
            "highlights": ["Law firm sites", "Clinic booking", "Fine dining", "Premium salons", "Real estate", "Bilingual EN/中文"],
            "footer_seo": "Manhattan web design · NYC website development · Manhattan SEO · Manhattan Google Ads · Midtown web design",
        },
    },
    {
        "slug": "flushing",
        "area_served": "Flushing",
        "zh": {
            "title": "法拉盛网站设计｜法拉盛 SEO·谷歌广告｜皇后区华人企业｜70NYC",
            "description": "70NYC 服务法拉盛及皇后区华人企业——餐馆、美容、装修、教育等，网站设计、本地 SEO、Google Ads 与小红书/Instagram 运营。",
            "breadcrumb": "法拉盛",
            "eyebrow": "Flushing · 法拉盛",
            "h1": "法拉盛网站设计<br><span>懂皇后区华人生意的增长伙伴</span>",
            "lead": "法拉盛是纽约华人商业最密集的区域之一——我们帮助 Main St、罗斯福大道周边餐馆、美容院、装修公司用网站、地图 SEO 与广告获取周边社区客户。",
            "tags": ["法拉盛网站设计", "Flushing web design", "法拉盛SEO", "皇后区网站", "法拉盛Google Ads", "法拉盛华人网站"],
            "topics": [
                ("典型客户", "餐馆、奶茶店、美容美甲、装修建材、补习班、诊所——依赖口碑与「附近」搜索。"),
                ("本地获客", "Google 地图、中文+英文关键词、小红书与 Instagram 联动；覆盖法拉盛、白石镇等周边。"),
                ("交付方式", "法拉盛可面谈；熟悉本地消费习惯，文案与视觉不「翻译腔」。"),
                ("服务组合", "餐馆/美容建议网站 + 本地 SEO + Google Ads；装修类加强案例页与表单转化。"),
            ],
            "highlights": ["餐馆网站", "美容沙龙", "装修案例站", "教育培训机构", "诊所形象站", "小红书运营"],
            "footer_seo": "法拉盛网站设计 · Flushing web design · 法拉盛SEO · 皇后区网站开发 · 法拉盛Google Ads",
        },
        "en": {
            "title": "Flushing Web Design | Queens SEO & Google Ads | 70NYC",
            "description": "Web design, local SEO, Google Ads, and social for Chinese businesses in Flushing and Queens — restaurants, beauty, construction, education.",
            "breadcrumb": "Flushing",
            "eyebrow": "Flushing Queens",
            "h1": "Flushing Web Design<br><span>Growth for Queens Chinese Businesses</span>",
            "lead": "Flushing's dense Chinese commercial corridor needs sites and search that match how locals actually find services — we cover Main St, Roosevelt Ave, and nearby neighborhoods.",
            "tags": ["Flushing web design", "Queens SEO", "Flushing Google Ads", "Chinese business Flushing", "Queens website", "Restaurant websites"],
            "topics": [
                ("Who We Serve", "Restaurants, bubble tea, salons, contractors, tutoring, clinics — heavy reliance on word-of-mouth and near-me search."),
                ("Local Acquisition", "Google Maps, bilingual keywords, 小红书 + Instagram; reach Flushing, Whitestone, and nearby."),
                ("Meetings", "On-site in Flushing; copy and design that feel local, not translated."),
                ("Typical Stack", "Site + local SEO + ads for F&B/beauty; contractors need portfolio + lead forms."),
            ],
            "highlights": ["Restaurant sites", "Salons", "Contractor portfolios", "Tutoring centers", "Clinic sites", "小红书 content"],
            "footer_seo": "Flushing web design · Queens web development · Flushing SEO · Flushing Google Ads · Queens Chinese business",
        },
    },
    {
        "slug": "brooklyn",
        "area_served": "Brooklyn",
        "related_blog": {
            "slug": "brooklyn-contractor-local-seo-2026",
            "zh": {"title": "布鲁克林本地 SEO 指南", "span": "装修·地图·获客"},
            "en": {"title": "Brooklyn Local SEO Guide", "span": "Contractors · Maps"},
        },
        "zh": {
            "title": "布鲁克林网站设计｜Brooklyn 网站开发与 SEO｜70NYC",
            "description": "70NYC 为布鲁克林华人企业提供网站设计、SEO、Google Ads——日落公园、本森贺、班森贺等社区，餐馆、装修、美容、零售。",
            "keywords": "布鲁克林网站设计, 布鲁克林SEO, 日落公园网站, Brooklyn web design, 布鲁克林Google Ads, 布鲁克林华人网站, 本森贺网站制作",
            "breadcrumb": "布鲁克林",
            "eyebrow": "Brooklyn · 布鲁克林",
            "h1": "布鲁克林网站设计<br><span>连接多元社区与线上客流</span>",
            "lead": "布鲁克林社区差异大——我们为日落公园、本森贺等华人聚集区定制网站与本地搜索策略，让客户在 Google 上先找到您。",
            "tags": ["布鲁克林网站设计", "Brooklyn web design", "日落公园网站", "布鲁克林SEO", "Brooklyn Google Ads", "布鲁克林华人网站"],
            "topics": [
                ("典型客户", "餐馆、超市、装修、汽车服务、美容、子女教育——服务半径多在布鲁克林区内。"),
                ("本地获客", "Brooklyn + 行业词、地图包、移动端体验优化；多语言覆盖中英客户。"),
                ("交付方式", "布鲁克林可约面谈；按社区调整案例与关键词，不套曼哈顿模板。"),
                ("服务组合", "网站 + SEO 打底；旺季可加 Google Ads；零售/餐饮可加社媒内容。"),
            ],
            "highlights": ["社区餐馆", "装修承包商", "汽车美容", "华人超市", "课后班", "双语网站"],
            "footer_seo": "布鲁克林网站设计 · Brooklyn web design · 日落公园网站 · 布鲁克林SEO · Brooklyn Google Ads",
            "faq": [
                {
                    "q": "布鲁克林网站设计项目一般多久能上线？",
                    "a": "标准企业官网通常 2–4 周：需求与设计确认、开发、测试上线。含多语言、预约系统或大量案例页的装修/餐饮站，会在报价阶段给出分区排期。日落公园、本森贺客户可约布鲁克林面谈加速确认。",
                },
                {
                    "q": "日落公园、本森贺的餐馆适合先做网站还是 Google 地图？",
                    "a": "两者都要，但顺序建议：先认领并完善 Google Business Profile（地图），同时上线移动端友好的网站与菜单页。地图带来「附近」流量，网站负责转化与品牌信任。详见我们的 <a href=\"/blog/brooklyn-contractor-local-seo-2026/\">布鲁克林本地 SEO 指南</a>。",
                },
                {
                    "q": "布鲁克林网站设计和曼哈顿模板有什么不同？",
                    "a": "布鲁克林社区更依赖「Brooklyn + 社区名 + 行业」长尾词（如 Sunset Park contractor、本森贺 装修），而不是曼哈顿式的品牌大词。我们会按服务半径写落地页，案例图标注具体社区，而不是套用曼哈顿天际线模板。",
                },
                {
                    "q": "只做中文网站能服务布鲁克林华人客户吗？",
                    "a": "可以，但建议至少核心页面（首页、联系、服务）提供英文版本或英文摘要。布鲁克林很多年轻客户与房东、供应商用英文沟通，双语站点有助于 Google 覆盖更多搜索，也减少「只中文」带来的信任门槛。",
                },
                {
                    "q": "70NYC 在布鲁克林可以面谈吗？",
                    "a": "可以。我们在布鲁克林、皇后区及曼哈顿均可预约见面；也可视频/微信远程协作。首次咨询免费，会根据您的社区与行业给出网站 + SEO + 广告的组合建议。",
                },
            ],
        },
        "en": {
            "title": "Brooklyn Web Design | NYC Website & SEO | 70NYC",
            "description": "Web design, SEO, and Google Ads for Chinese businesses in Brooklyn — Sunset Park, Bensonhurst, restaurants, contractors, beauty, retail.",
            "keywords": "Brooklyn web design, Brooklyn SEO, Sunset Park website, Brooklyn Google Ads, Chinese business Brooklyn, Bensonhurst web design",
            "breadcrumb": "Brooklyn",
            "eyebrow": "Brooklyn NYC",
            "h1": "Brooklyn Web Design<br><span>Reach Neighborhood Customers Online</span>",
            "lead": "Brooklyn neighborhoods differ — we tailor sites and local search for Sunset Park, Bensonhurst, and other Chinese business corridors so Google leads find you first.",
            "tags": ["Brooklyn web design", "Sunset Park website", "Brooklyn SEO", "Brooklyn Google Ads", "Chinese business Brooklyn", "NYC contractor sites"],
            "topics": [
                ("Who We Serve", "Restaurants, markets, contractors, auto, beauty, education — mostly Brooklyn-radius customers."),
                ("Local Acquisition", "Brooklyn + service keywords, map pack, mobile UX; bilingual EN/中文 coverage."),
                ("Meetings", "Brooklyn meetups available; area-specific cases, not Manhattan templates."),
                ("Typical Stack", "Site + SEO baseline; seasonal Google Ads; retail/F&B adds social."),
            ],
            "highlights": ["Neighborhood restaurants", "Contractors", "Auto services", "Markets", "Tutoring", "Bilingual sites"],
            "footer_seo": "Brooklyn web design · Sunset Park website · Brooklyn SEO · Brooklyn Google Ads · NYC Chinese business",
            "faq": [
                {
                    "q": "How long does a Brooklyn web design project take?",
                    "a": "Standard business sites typically launch in 2–4 weeks: discovery, design sign-off, build, and QA. Contractor or restaurant sites with bilingual menus or booking may take longer — we provide a phased timeline at proposal. Sunset Park and Bensonhurst clients can meet locally to speed approvals.",
                },
                {
                    "q": "For Sunset Park restaurants, start with a website or Google Maps?",
                    "a": "Both — but prioritize claiming and optimizing Google Business Profile while launching a mobile-friendly site with menu pages. Maps drives near-me traffic; your site converts trust into calls. See our <a href=\"/en/blog/brooklyn-contractor-local-seo-2026/\">Brooklyn local SEO guide</a>.",
                },
                {
                    "q": "How is Brooklyn web design different from Manhattan templates?",
                    "a": "Brooklyn wins on neighborhood long-tail keywords (Sunset Park contractor, Bensonhurst renovation) rather than skyline-brand terms. We build area-specific landing copy and label portfolio photos by community — not recycled Manhattan layouts.",
                },
                {
                    "q": "Can a Chinese-only site work for Brooklyn customers?",
                    "a": "Yes for some audiences, but we recommend English summaries on core pages (home, services, contact). Many Brooklyn customers, landlords, and vendors search in English — bilingual sites expand reach and improve Google coverage.",
                },
                {
                    "q": "Can we meet in Brooklyn with 70NYC?",
                    "a": "Yes — we schedule meetings in Brooklyn, Queens, and Manhattan, or work remotely via video/WeChat. First consultation is free; we recommend a web + SEO + ads stack based on your neighborhood and industry.",
                },
            ],
        },
    },
    {
        "slug": "long-island",
        "area_served": "Long Island",
        "zh": {
            "title": "长岛网站设计｜Long Island 网站开发与 SEO｜70NYC",
            "description": "70NYC 服务长岛华人企业网站设计、SEO、Google Ads——Great Neck、曼哈西特、Plainview 等，装修、美容、餐饮、专业服务。",
            "breadcrumb": "长岛",
            "eyebrow": "Long Island · 长岛",
            "h1": "长岛网站设计<br><span>郊区华人企业的专业线上门面</span>",
            "lead": "长岛客户往往车行15–30分钟到店——网站与本地 SEO 要清晰展示服务范围、案例与预约方式，我们服务 North Shore、Nassau、Suffolk 华人商业。",
            "tags": ["长岛网站设计", "Long Island web design", "长岛SEO", "Great Neck网站", "长岛Google Ads", "长岛华人网站"],
            "topics": [
                ("典型客户", "装修、景观、美容、牙医、律所、餐饮——依赖区域口碑与 Google 推荐。"),
                ("本地获客", "Long Island + 城镇名 + 行业词；地图与落地页标明服务半径与停车/预约信息。"),
                ("交付方式", "长岛可约见面或远程；理解郊区客流与季节性需求（如装修旺季）。"),
                ("服务组合", "案例型网站 + 本地 SEO；高客单价服务可加 Google Ads 与评价管理引导。"),
            ],
            "highlights": ["装修公司", "美容牙科", "专业服务", "景观园艺", "家庭餐馆", "服务范围说明"],
            "footer_seo": "长岛网站设计 · Long Island web design · 长岛SEO · Great Neck网站 · Long Island Google Ads",
        },
        "en": {
            "title": "Long Island Web Design | NYC Suburbs SEO & Ads | 70NYC",
            "description": "Web design, SEO, and Google Ads for Chinese businesses on Long Island — Great Neck, Manhasset, Plainview, contractors, beauty, professional services.",
            "breadcrumb": "Long Island",
            "eyebrow": "Long Island NY",
            "h1": "Long Island Web Design<br><span>Professional Sites for Suburban Clients</span>",
            "lead": "Long Island customers often drive 15–30 minutes — your site and local SEO must show service area, proof, and booking clearly. We serve North Shore, Nassau, and Suffolk Chinese businesses.",
            "tags": ["Long Island web design", "Great Neck website", "Long Island SEO", "Nassau web design", "Long Island Google Ads", "Chinese business LI"],
            "topics": [
                ("Who We Serve", "Contractors, landscaping, beauty, dental, legal, dining — regional reputation and Google referrals."),
                ("Local Acquisition", "Long Island + town + industry keywords; maps and pages with service radius and parking/booking info."),
                ("Meetings", "LI meetups or remote; we understand suburban traffic and seasonal peaks."),
                ("Typical Stack", "Portfolio site + local SEO; high-ticket services add Google Ads and review strategy."),
            ],
            "highlights": ["Contractors", "Beauty & dental", "Professional firms", "Landscaping", "Family restaurants", "Service area pages"],
            "footer_seo": "Long Island web design · Great Neck website · Long Island SEO · Nassau Suffolk web development · LI Google Ads",
        },
    },
    {
        "slug": "bronx",
        "area_served": "Bronx",
        "zh": {
            "title": "布朗克斯网站设计｜Bronx 网站开发与 SEO｜70NYC",
            "description": "70NYC 为布朗克斯华人企业提供网站设计、SEO、Google Ads——餐馆、零售、装修、社区服务，支持面谈与远程。",
            "breadcrumb": "布朗克斯",
            "eyebrow": "Bronx · 布朗克斯",
            "h1": "布朗克斯网站设计<br><span>服务社区型华人生意</span>",
            "lead": "布朗克斯社区商业重口碑与回头客——我们帮助餐馆、小零售、装修队建立可信赖的网站与 Google 存在感，让新客户也能找到您。",
            "tags": ["布朗克斯网站设计", "Bronx web design", "布朗克斯SEO", "Bronx Google Ads", "布朗克斯华人网站", "纽约Bronx网站"],
            "topics": [
                ("典型客户", "餐馆、便利店、装修、清洁、车行、社区诊所——服务周边固定客群。"),
                ("本地获客", "Bronx 本地词 + 手机友好网站；地图信息与营业时间准确一致。"),
                ("交付方式", "布朗克斯可约见面；报价与功能务实，按真实预算分期上线。"),
                ("服务组合", "精简官网 + 地图 SEO 往往即可见效；需要快速客流时加 Google Ads。"),
            ],
            "highlights": ["社区餐馆", "零售门店", "装修小队", "车行保养", "社区服务", "移动端优先"],
            "footer_seo": "布朗克斯网站设计 · Bronx web design · 布朗克斯SEO · Bronx Google Ads · 布朗克斯网站制作",
        },
        "en": {
            "title": "Bronx Web Design | NYC Website Development & SEO | 70NYC",
            "description": "Web design, SEO, and Google Ads for Chinese businesses in the Bronx — restaurants, retail, contractors, community services.",
            "breadcrumb": "Bronx",
            "eyebrow": "Bronx NYC",
            "h1": "Bronx Web Design<br><span>Trusted Sites for Community Businesses</span>",
            "lead": "Bronx businesses live on repeat customers and referrals — we build credible websites and Google presence so new neighbors can discover you too.",
            "tags": ["Bronx web design", "Bronx SEO", "Bronx Google Ads", "Chinese business Bronx", "NYC Bronx website", "Community restaurants"],
            "topics": [
                ("Who We Serve", "Restaurants, corner retail, contractors, cleaning, auto, clinics — neighborhood-based clientele."),
                ("Local Acquisition", "Bronx local keywords + mobile-first site; accurate hours and map data."),
                ("Meetings", "Bronx meetups; practical scopes and phased launch by budget."),
                ("Typical Stack", "Lean site + map SEO often enough; Google Ads when you need faster leads."),
            ],
            "highlights": ["Community dining", "Retail", "Small contractors", "Auto shops", "Local services", "Mobile-first"],
            "footer_seo": "Bronx web design · Bronx SEO · Bronx Google Ads · NYC Chinese business Bronx · Bronx website company",
        },
    },
    {
        "slug": "staten-island",
        "area_served": "Staten Island",
        "zh": {
            "title": "史泰登岛网站设计｜Staten Island SEO·网站开发｜70NYC",
            "description": "70NYC 服务史泰登岛华人企业——网站设计、本地 SEO、Google Ads，餐馆、装修、美容、专业服务，可远程或预约见面。",
            "breadcrumb": "史泰登岛",
            "eyebrow": "Staten Island · 史泰登岛",
            "h1": "史泰登岛网站设计<br><span>岛上华人企业的数字增长</span>",
            "lead": "史泰登岛市场相对独立——本地搜索竞争低于曼哈顿，做好网站与地图 SEO 更容易脱颖而出；我们熟悉岛上华人商业节奏。",
            "tags": ["史泰登岛网站设计", "Staten Island web design", "史泰登岛SEO", "Staten Island Google Ads", "史泰登岛华人网站"],
            "topics": [
                ("典型客户", "餐馆、装修、美容、会计/保险、子女教育——客户多来自岛内与近郊。"),
                ("本地获客", "Staten Island 地域词竞争较低，适合先做 SEO 再按需投放广告。"),
                ("交付方式", "可约岛上见面或全程远程；与纽约主团队同一交付标准。"),
                ("服务组合", "网站 + 本地 SEO 性价比高；装修/美容可加前后对比案例页。"),
            ],
            "highlights": ["岛内餐馆", "装修服务", "美容美发", "保险会计", "课后辅导", "本地SEO优先"],
            "footer_seo": "史泰登岛网站设计 · Staten Island web design · 史泰登岛SEO · Staten Island Google Ads",
        },
        "en": {
            "title": "Staten Island Web Design | NYC SEO & Web Development | 70NYC",
            "description": "Web design, local SEO, and Google Ads for Chinese businesses on Staten Island — restaurants, contractors, beauty, professional services.",
            "breadcrumb": "Staten Island",
            "eyebrow": "Staten Island NYC",
            "h1": "Staten Island Web Design<br><span>Digital Growth on the Island</span>",
            "lead": "Staten Island is its own market — local search is less crowded than Manhattan, so a solid site and map SEO can stand out faster. We match the island's business pace.",
            "tags": ["Staten Island web design", "Staten Island SEO", "Staten Island Google Ads", "Chinese business SI", "NYC island website"],
            "topics": [
                ("Who We Serve", "Restaurants, contractors, beauty, accounting/insurance, tutoring — mostly island and nearby."),
                ("Local Acquisition", "Lower competition for SI geo terms — SEO first, ads when ready."),
                ("Meetings", "On-island or fully remote; same NYC team standards."),
                ("Typical Stack", "Site + local SEO is high ROI; contractors/beauty add before-after galleries."),
            ],
            "highlights": ["Island restaurants", "Contractors", "Salons", "Insurance & accounting", "Tutoring", "SEO-first"],
            "footer_seo": "Staten Island web design · Staten Island SEO · Staten Island Google Ads · NYC Chinese business",
        },
    },
]

# Append posts here, then run: python3 scripts/generate-seo-pages.py blog
# Each post: unique slug, zh + en, optional keywords, intro, sections[{h2, paragraphs}], paragraphs.
BLOG_POSTS: list[dict[str, Any]] = [
    {
        "slug": "flushing-restaurant-google-maps-seo-2026",
        "date": "2026-06-15",
        "zh": {
            "title": "法拉盛餐馆 Google 地图排名指南：2026 本地 SEO 实操｜70NYC",
            "description": "法拉盛餐馆如何在 Google 地图与本地搜索获得更高曝光？GBP 设置、中英关键词、评价策略与网站配合——皇后区华人餐饮本地 SEO 完整指南。",
            "keywords": "法拉盛SEO, 法拉盛餐馆Google地图, 法拉盛本地搜索, Google Business Profile, 皇后区餐馆SEO, 法拉盛网站设计, 华人餐馆营销, 法拉盛Google排名",
            "h1": "法拉盛餐馆怎么做 Google 地图排名？",
            "intro": "在法拉盛做餐饮，客人往往先在 Google 搜「法拉盛 川菜」「Flushing dim sum near me」，或在地图里找「附近的餐馆」。本地 SEO 不是可有可无的营销选项——它直接决定午餐高峰有没有新客走进门。本文按 2026 年 Google 本地搜索规则，拆解法拉盛餐馆从 Google Business Profile（GBP）到网站、评价的可执行步骤。",
            "sections": [
                {
                    "h2": "为什么法拉盛餐馆必须优先做 Google 地图 SEO",
                    "paragraphs": [
                        "法拉盛（Flushing）是全美华人密度最高的商业区之一：Main Street、罗斯福大道、39th Avenue 周边餐馆林立，竞争不靠「有没有网站」，而靠「在地图第几位、评价够不够、照片吸不吸引人」。",
                        "Google 本地包（Local Pack）通常只展示 3 家餐馆。排名靠前意味着手机用户点「导航」或「电话」的概率成倍上升。对早茶、火锅、烧烤、奶茶、私厨等品类，<strong>法拉盛 SEO</strong> 的核心战场就是 Google 地图 + 本地自然结果，而不是泛泛的「纽约网站设计」大词。",
                        "华人客人常用中文搜索，非华人或第二代客人常用英文——同一店铺需要中英双语信息一致，否则 Google 难以判断该展示哪个版本，曝光会被稀释。",
                    ],
                },
                {
                    "h2": "Google Business Profile：法拉盛餐馆必查 12 项",
                    "paragraphs": [
                        "GBP 是免费且权重最高的本地信号。新建或认领后，请逐项核对：",
                    ],
                    "list": [
                        "商家名称：与招牌一致，勿堆砌关键词（如「最好火锅 法拉盛 法拉盛 法拉盛」会被处罚）",
                        "主类别：选最贴近的 Primary category（Restaurant、Chinese restaurant 等）",
                        "地址与服务范围：实体店填准确地址；仅外卖/私厨需如实设置服务区域",
                        "营业时间：含节假日、春节等特殊时段；错误营业时间会导致差评与跳出",
                        "电话：与网站、Yelp、Instagram 一致，利于 Google 信任同一实体",
                        "网站链接：指向移动端加载快的页面，最好含菜单或订位入口",
                        "菜单：上传 PDF 或使用 GBP 菜单功能；中文菜名 + 英文翻译",
                        "属性：是否 Halal、素食、外带、堂食、无障碍等",
                        "照片：门面、招牌、热门菜、环境、团队——至少 15 张高质量图",
                        "产品/服务：特色菜、套餐、午餐特价",
                        "问答（Q&A）：自己先写「是否可订位」「是否可刷卡」等常见问题",
                        "帖子（Posts）：每周更新促销、新菜、营业时间变更",
                    ],
                },
                {
                    "h2": "法拉盛本地关键词：中文、英文与「附近搜索」",
                    "paragraphs": [
                        "关键词研究不必复杂，从真实客人怎么搜开始：",
                        "中文示例：法拉盛 餐馆、法拉盛 川菜、法拉盛 早茶、皇后区 火锅、法拉盛 外卖、法拉盛 包厢。英文示例：Flushing Chinese restaurant、best dim sum Flushing NY、Flushing hot pot、restaurants near Main St Flushing。",
                        "把这些词自然写进 GBP 简介、网站标题与 H1/H2、菜单页 meta description——避免同一段文字复制粘贴到十个页面。若你正在规划新站，可参考我们的 <a href=\"/areas/flushing/\">法拉盛网站设计</a> 与 <a href=\"/services/seo/\">纽约 SEO 优化</a> 服务，从建站阶段就把本地关键词结构做好。",
                        "「Near me」类搜索依赖设备定位，无法靠页面硬塞关键词解决；Google 看的是<strong>距离、相关性、知名度</strong>。知名度主要来自评价数量/质量、点击率和品牌搜索（客人直接搜店名）。",
                    ],
                },
                {
                    "h2": "评价与照片：本地排名真正的杠杆",
                    "paragraphs": [
                        "在法拉盛，一条带图的中文五星评价，往往比十篇博客更能拉动地图排名。建议：",
                    ],
                    "list": [
                        "用餐后 24 小时内礼貌邀请满意客人留 Google 评价（可放桌卡 QR）",
                        "每条评价都认真回复，中英文皆可，展示老板/经理真实在场",
                        "勿买假评、勿批量刷评——Google 2024–2026 持续打击，可能导致 GBP 暂停",
                        "定期更新菜品照片；搜索结果显示有图商家点击率明显更高",
                        "把 Yelp、小红书上的口碑同步引导至 Google（合法合规前提下）",
                    ],
                },
                {
                    "h2": "网站如何配合 Google 地图（而不重复造轮子）",
                    "paragraphs": [
                        "GBP 负责「在地图里被找到」，网站负责「被找到之后说服客人下单或到店」。理想组合：",
                    ],
                    "list": [
                        "网站加载速度 &lt; 3 秒（手机），菜单一页可读，电话一键拨打",
                        "独立菜单页或在线订位/外卖链接，与 GBP 菜单信息一致",
                        "嵌入 Google 地图与同款 NAP（Name/Address/Phone）",
                        "本地落地页：例如强调「法拉盛 Main St」「皇后区外卖范围」",
                        "Schema 本地商家结构化数据，帮助 Google 关联网站与 GBP",
                    ],
                },
                {
                    "h2": "法拉盛餐馆 SEO 常见错误",
                    "paragraphs": [
                        "我们服务皇后区餐饮客户时，最常见的问题包括：GBP 与网站电话不一致；用旧 HostGator 博客子域名导致 Google 索引混乱；只投 Google Ads 不做自然本地 SEO（广告停投流量即断）；菜单只有图片无文字，Google 无法读懂菜品关键词。",
                        "另一个误区是只优化「纽约网站设计」这类全国大词——对法拉盛餐馆来说，<strong>「法拉盛 + 品类」</strong> 的转化远高于泛词。先把本地做透，再考虑曼哈顿或全纽约品牌扩张。",
                    ],
                },
                {
                    "h2": "下一步：需要专业协助时",
                    "paragraphs": [
                        "70NYC 团队常驻纽约，熟悉法拉盛、白石镇、贝赛等周边社区，提供 <a href=\"/services/web-design/\">网站设计</a>、<a href=\"/services/seo/\">本地 SEO</a>、Google Ads 与社交媒体一体化方案。可先免费沟通：现有 GBP 截图、网站链接、主要竞品——我们会在 24 小时内给出可执行的优先改进清单。",
                    ],
                },
            ],
            "footer_seo": "法拉盛SEO · 法拉盛餐馆Google地图 · 皇后区本地搜索 · 法拉盛网站设计 · 华人餐馆营销",
        },
        "en": {
            "title": "Flushing Restaurant Google Maps Ranking Guide: 2026 Local SEO | 70NYC",
            "description": "How Flushing restaurants rank on Google Maps and local search — GBP setup, bilingual keywords, reviews, and website tips for Queens Chinese dining.",
            "keywords": "Flushing SEO, Flushing restaurant Google Maps, Flushing local search, Google Business Profile, Queens restaurant SEO, Flushing web design, Chinese restaurant marketing",
            "h1": "How Flushing Restaurants Rank on Google Maps",
            "intro": "In Flushing, diners often search Google for \"Flushing Sichuan food,\" \"dim sum near me,\" or browse the map for nearby restaurants. Local SEO is not optional — it decides whether new customers walk in during lunch rush. This guide covers actionable steps for Flushing restaurants in 2026, from Google Business Profile (GBP) to reviews and your website.",
            "sections": [
                {
                    "h2": "Why Flushing restaurants must prioritize Google Maps SEO",
                    "paragraphs": [
                        "Flushing is one of the densest Chinese commercial corridors in the U.S. — Main Street, Roosevelt Avenue, and 39th Avenue are packed with restaurants. Competition is won by map position, review quality, and photos — not by having any website at all.",
                        "Google's Local Pack usually shows only three restaurants. Top placement dramatically increases taps on Directions and Call. For dim sum, hot pot, BBQ, bubble tea, and private kitchens, <strong>Flushing SEO</strong> lives in Google Maps and local organic results — not broad \"NYC web design\" keywords.",
                        "Chinese-speaking guests search in Chinese; English speakers and second-generation customers search in English. Your business needs consistent bilingual listings, or Google may split or dilute your visibility.",
                    ],
                },
                {
                    "h2": "Google Business Profile: 12 must-check items for Flushing restaurants",
                    "paragraphs": ["GBP is free and the strongest local signal. After claiming your listing, verify:"],
                    "list": [
                        "Business name matches signage — no keyword stuffing",
                        "Primary category fits (Restaurant, Chinese restaurant, etc.)",
                        "Address and service area accurate for dine-in vs delivery-only",
                        "Hours including holidays and Lunar New Year",
                        "Phone matches website, Yelp, and social profiles",
                        "Website links to a fast mobile page with menu or reservations",
                        "Menu uploaded with Chinese names + English translations",
                        "Attributes: dine-in, takeout, halal, vegetarian, accessibility",
                        "Photos: storefront, dishes, interior, team — 15+ quality images",
                        "Products/services: specials and lunch deals",
                        "Q&A: answer reservation, parking, and payment questions proactively",
                        "Weekly Posts for promos, new dishes, hour changes",
                    ],
                },
                {
                    "h2": "Flushing local keywords: Chinese, English, and \"near me\"",
                    "paragraphs": [
                        "Start with how real customers search:",
                        "Chinese examples: 法拉盛 餐馆, 法拉盛 川菜, 法拉盛 早茶, 皇后区 火锅. English: Flushing Chinese restaurant, best dim sum Flushing NY, Flushing hot pot, restaurants near Main St Flushing.",
                        "Use these naturally in GBP descriptions, page titles, and menu meta text — never duplicate the same block across ten pages. Planning a new site? See our <a href=\"/en/areas/flushing/\">Flushing web design</a> and <a href=\"/en/services/seo/\">NYC SEO</a> services to build local keyword structure from day one.",
                        "\"Near me\" queries rely on device location — Google ranks by <strong>distance, relevance, and prominence</strong>. Prominence comes from reviews, engagement, and branded searches.",
                    ],
                },
                {
                    "h2": "Reviews and photos: the real ranking levers",
                    "paragraphs": ["In Flushing, one photo review in Chinese often moves the needle more than ten generic blog posts. Best practices:"],
                    "list": [
                        "Invite happy guests within 24 hours (table QR cards work well)",
                        "Reply to every review in Chinese or English — show ownership",
                        "Never buy fake reviews — Google penalties can suspend GBP",
                        "Refresh dish photos regularly; listings with photos earn more clicks",
                        "Guide satisfied guests from Yelp or social to Google (compliantly)",
                    ],
                },
                {
                    "h2": "How your website supports Google Maps",
                    "paragraphs": ["GBP gets you found; your website converts. Ideal setup:"],
                    "list": [
                        "Mobile load under 3 seconds; readable menu; click-to-call",
                        "Menu or ordering page consistent with GBP menu data",
                        "Embedded map and matching NAP (name, address, phone)",
                        "Local landing copy mentioning Flushing Main St or delivery zone",
                        "LocalBusiness schema linking site and GBP",
                    ],
                },
                {
                    "h2": "Common Flushing restaurant SEO mistakes",
                    "paragraphs": [
                        "We often see: phone mismatches between GBP and website; legacy blog subdomains confusing Google; ads-only strategy with no organic local SEO; image-only menus with no indexable text.",
                        "Another mistake is targeting only broad keywords like \"NYC web design.\" For Flushing restaurants, <strong>Flushing + cuisine type</strong> converts far better. Dominate local first, then expand brand reach.",
                    ],
                },
                {
                    "h2": "Need hands-on help?",
                    "paragraphs": [
                        "70NYC serves Flushing, Whitestone, Bayside, and greater Queens with <a href=\"/en/services/web-design/\">web design</a>, <a href=\"/en/services/seo/\">local SEO</a>, Google Ads, and social media. Share your GBP link and website for a free priority checklist within 24 hours.",
                    ],
                },
            ],
            "footer_seo": "Flushing SEO · Flushing restaurant Google Maps · Queens local search · Flushing web design",
        },
    },
    {
        "slug": "nyc-chinese-business-website-seo-mistakes-2026",
        "date": "2026-06-16",
        "zh": {
            "title": "纽约华人企业网站 SEO 七大误区｜2026 避坑指南｜70NYC",
            "description": "纽约华人网站设计做完却搜不到？剖析双语不一致、旧域名、关键词堆砌、缺本地页等 7 大 SEO 误区，附可立即执行的修复清单。",
            "keywords": "纽约华人网站设计, 华人企业SEO, 纽约网站SEO, 华人网站制作, 法拉盛网站设计, 曼哈顿网站公司, 纽约网站设计错误",
            "h1": "纽约华人企业网站 SEO 七大误区",
            "intro": "很多法拉盛、曼哈顿、布鲁克林的华人老板已经花了钱做网站，却在 Google 搜「纽约华人网站设计」或自己的服务关键词时找不到自己。问题往往不在「没做 SEO」，而在几个可修复的结构性错误。以下是我们 13 年服务纽约华人企业时最常遇到的 7 个误区。",
            "sections": [
                {
                    "h2": "误区 1：中英文信息不一致（NAP 混乱）",
                    "paragraphs": [
                        "网站写 917 号码，Google 地图是 386，Yelp 又是第三个——Google 无法确认是同一商家，本地排名直接受损。华人企业常有一个中文站、一个英文 Facebook 页，地址缩写还不一致（Flushing vs 法拉盛）。",
                        "修复：全平台统一 Name / Address / Phone，网站 footer 与 <a href=\"/contact/\">联系页</a> 必须与 Google Business Profile 完全一致。",
                    ],
                },
                {
                    "h2": "误区 2：只优化「纽约网站设计」大词",
                    "paragraphs": [
                        "大词竞争极端激烈，新站很难短期进首页。华人装修公司、餐馆、律所应优先「法拉盛 装修 网站」「曼哈顿 中餐馆 订位」等<strong>区域 + 行业</strong>长尾。",
                        "修复：为每个主力服务区域建独立落地页——参考我们的 <a href=\"/areas/\">纽约服务区域</a> 结构，而不是把所有关键词堆在首页 footer。",
                    ],
                },
                {
                    "h2": "误区 3：网站迁移后没有 301 重定向",
                    "paragraphs": [
                        "从 WordPress、Wix 或旧 HostGator 换到新站，若旧 URL 全部 404，Google 索引里仍是旧链接，权重断档。这在 2025–2026 年 GSC 里表现为大量「已抓取未索引」和旧「麒麟纽约创意」页面。",
                        "修复：旧路径 301 到新服务页或 <a href=\"/blog/\">博客</a>；在 Search Console 提交新 sitemap。",
                    ],
                },
                {
                    "h2": "误区 4：菜单/案例只有图片，没有文字",
                    "paragraphs": [
                        "餐馆网站整页 JPG 菜单、装修公司只有施工前后对比图——Google 无法提取「Kitchen remodeling Flushing」等关键词，图片 SEO 几乎为零。",
                        "修复：每道招牌菜、每个服务项配文字说明 + alt 属性；案例页写清地点、面积、工期。",
                    ],
                },
                {
                    "h2": "误区 5：blog 子域名与主站分裂",
                    "paragraphs": [
                        "blog.70nyc.com 在 HostGator，主站在 Cloudflare——Google 视为两个站点，博客权重传不到主域。",
                        "修复：统一到 <code>70nyc.com/blog/</code>，子域名 301 到主站博客；每篇聚焦一个长尾词，勿复制 area 页原文。",
                    ],
                },
                {
                    "h2": "误区 6：忽视 Google 地图与评价",
                    "paragraphs": [
                        "网站 SEO 做得再细，GBP 未认领、零评价，本地包仍进不去。华人服务行业（美容、餐饮、装修）极度依赖地图前三。",
                        "修复：认领 GBP、每周发 Post、系统收集 Google 评价；详见 <a href=\"/blog/flushing-restaurant-google-maps-seo-2026/\">法拉盛餐馆 Google 地图指南</a>。",
                    ],
                },
                {
                    "h2": "误区 7：只做网站，不做内链与更新",
                    "paragraphs": [
                        "上线后三年不改一个字，首页从不链向服务子页或博客——Google 认为站点不活跃。",
                        "修复：首页 → 服务页 → area 页 → 博客互链；每季度更新案例或一篇洞察。需要审计？<a href=\"/services/seo/\">纽约 SEO 优化</a> 服务含免费初诊清单。",
                    ],
                },
            ],
            "footer_seo": "纽约华人网站设计 · 华人企业SEO · 纽约网站SEO · 法拉盛网站设计 · 曼哈顿网站公司",
        },
        "en": {
            "title": "7 NYC Chinese Business Website SEO Mistakes to Avoid in 2026 | 70NYC",
            "description": "Why your NYC Chinese business website doesn't rank — bilingual NAP issues, migration 404s, keyword stuffing, missing local pages, and fixes.",
            "keywords": "NYC Chinese web design, Chinese business SEO, NYC website SEO, Flushing web design, Manhattan website company",
            "h1": "7 Website SEO Mistakes NYC Chinese Businesses Make",
            "intro": "Many Flushing, Manhattan, and Brooklyn owners invested in a website but still don't show up on Google. The issue is usually structural — and fixable. Here are seven mistakes we see most often after 13 years serving Chinese-owned businesses in New York.",
            "sections": [
                {
                    "h2": "Mistake 1: Inconsistent bilingual NAP data",
                    "paragraphs": [
                        "Different phone numbers on your site, Google Maps, and Yelp confuse Google about whether you're one business. Mixed Chinese/English address formats make it worse.",
                        "Fix: Unify name, address, and phone everywhere — especially your <a href=\"/en/contact/\">contact page</a> and Google Business Profile.",
                    ],
                },
                {
                    "h2": "Mistake 2: Targeting only broad keywords",
                    "paragraphs": [
                        "\"NYC web design\" is extremely competitive. Contractors, restaurants, and law firms should prioritize <strong>neighborhood + service</strong> long-tail terms first.",
                        "Fix: Build dedicated area landing pages — see our <a href=\"/en/areas/\">service areas</a> structure instead of keyword-stuffing the homepage footer.",
                    ],
                },
                {
                    "h2": "Mistake 3: No 301 redirects after migration",
                    "paragraphs": [
                        "Switching from WordPress or HostGator without redirects leaves 404s and splits index equity — a common 2025–2026 Search Console pattern.",
                        "Fix: 301 old URLs to new service or <a href=\"/en/blog/\">blog</a> pages; resubmit sitemap.xml.",
                    ],
                },
                {
                    "h2": "Mistake 4: Image-only menus and portfolios",
                    "paragraphs": [
                        "JPEG menus and before/after galleries with no text give Google nothing to index for \"kitchen remodeling Flushing\" or similar queries.",
                        "Fix: Add descriptive copy and alt text for every service and dish.",
                    ],
                },
                {
                    "h2": "Mistake 5: Split blog subdomain",
                    "paragraphs": [
                        "Hosting blog.70nyc.com separately from your main domain treats content as two sites — blog authority won't pass to your primary domain.",
                        "Fix: Consolidate on <code>70nyc.com/blog/</code> with 301 redirects from the old subdomain.",
                    ],
                },
                {
                    "h2": "Mistake 6: Ignoring Google Maps and reviews",
                    "paragraphs": [
                        "Perfect on-page SEO still won't crack the Local Pack with an unclaimed GBP and zero reviews.",
                        "Fix: Claim GBP, post weekly, collect reviews — see our <a href=\"/en/blog/flushing-restaurant-google-maps-seo-2026/\">Flushing Google Maps guide</a>.",
                    ],
                },
                {
                    "h2": "Mistake 7: Launch and forget",
                    "paragraphs": [
                        "Sites unchanged for years with no internal links to services or blog posts signal inactivity to Google.",
                        "Fix: Interlink home → services → areas → blog; update quarterly. Need an audit? See <a href=\"/en/services/seo/\">NYC SEO services</a>.",
                    ],
                },
            ],
            "footer_seo": "NYC Chinese web design · Chinese business SEO · Flushing web design · Manhattan website company",
        },
    },
    {
        "slug": "flushing-web-design-guide-2026",
        "date": "2026-06-17",
        "zh": {
            "title": "法拉盛网站设计怎么选？2026 华人企业建站指南｜70NYC",
            "description": "法拉盛网站设计、网站制作如何选团队？对比模板站 vs 定制站、中英双语、移动端、SEO 基础、本地案例与报价透明度——皇后区华人企业实用指南。",
            "keywords": "法拉盛网站设计, 法拉盛网站制作, 法拉盛网站公司, 皇后区网站设计, 法拉盛网页设计, 纽约华人网站设计, Flushing web design",
            "h1": "法拉盛网站设计怎么选？",
            "intro": "在法拉盛找「网站设计」或「网站制作」，搜索结果从 $299 模板到 $15,000 定制都有。皇后区华人企业——餐馆、美容、装修、教育、诊所——真正需要的不是最便宜的，而是<strong>能在 Google 被找到、能带咨询、能代表品牌</strong>的网站。本文帮你用 10 分钟做决策。",
            "sections": [
                {
                    "h2": "法拉盛企业建站前先问 4 个问题",
                    "paragraphs": [
                        "① 客人 mainly 从 Google 地图、微信还是朋友介绍来？② 需不需要中英双语？③ 要不要在线订位、外卖、表单报价？④ 谁负责日后改菜单/价格？",
                        "答案决定你是要展示型官网、餐馆系统，还是带 SEO 结构的营销站——不是越贵越好，而是<strong>匹配获客渠道</strong>。",
                    ],
                },
                {
                    "h2": "模板站 vs 定制站：法拉盛老板该怎么选",
                    "paragraphs": [
                        "模板站（Wix、Squarespace、低价 WordPress 主题）上线快、前期便宜，但往往 PageSpeed 一般、SEO 结构弱、难做本地化 landing page。",
                        "定制站适合：竞争激烈的品类（装修、律所、医美）、需要品牌差异化、或要对接 Google Ads 转化追踪。70NYC 标准交付 2–4 周，含移动端、基础 <a href=\"/services/seo/\">SEO 设置</a> 与培训。",
                    ],
                    "list": [
                        "选模板：预算紧、短期活动页、已有很强口碑转介绍",
                        "选定制：依赖 Google 获客、多服务线、要中英双语专业形象",
                        "不论哪种：必须移动端优先——法拉盛客人多在地铁上搜",
                    ],
                },
                {
                    "h2": "优质法拉盛网站设计的 6 个必检项",
                    "paragraphs": ["签约前打开对方提供的案例站，用手机检查："],
                    "list": [
                        "3 秒内可交互（Core Web Vitals 合格）",
                        "电话一键拨打、微信/表单清晰可见",
                        "中文无乱码、英文不机翻——体现专业度",
                        "有独立服务页或区域页（利于「法拉盛 + 行业」排名）",
                        "Google Analytics / Search Console 可访问",
                        "合同写明源码/域名归属与你方所有",
                    ],
                },
                {
                    "h2": "网站与 Google 地图、广告如何配合",
                    "paragraphs": [
                        "法拉盛网站设计不应孤立存在。GBP 里的网站链接应指向转化最好的页面；Google Ads 落地页需与 organic 站信息一致，避免 Quality Score 低。",
                        "我们常见高效组合：定制站 + 本地 SEO + 地图优化（参见 <a href=\"/blog/flushing-restaurant-google-maps-seo-2026/\">餐馆地图 SEO 文</a>）+ 小规模 Search 广告测关键词。",
                    ],
                },
                {
                    "h2": "报价参考：法拉盛网站制作一般花在哪里",
                    "paragraphs": [
                        "展示型华人企业官网：通常含策略、UI、开发、上线测试——根据页数与是否双语浮动。餐馆含菜单/订位功能更高。",
                        "警惕「一次性 $299 全包」：往往不含 SEO、不含维护、域名不在你名下。问清<strong>年费、修改次数、是否含 SSL</strong>。",
                    ],
                },
                {
                    "h2": "为什么法拉盛客户找 70NYC",
                    "paragraphs": [
                        "我们团队在皇后区有多年项目经验，可面谈（Main St / 罗斯福大道周边），熟悉华人审美与转化习惯——不是把国内模板直接翻译。",
                        "查看 <a href=\"/areas/flushing/\">法拉盛服务页</a> 与 <a href=\"/services/web-design/\">网站设计服务</a>，或致电 386-316-1848 获取免费方案与周期估算。",
                    ],
                },
            ],
            "footer_seo": "法拉盛网站设计 · 法拉盛网站制作 · 法拉盛网站公司 · 皇后区网站设计 · 纽约华人网站设计",
        },
        "en": {
            "title": "How to Choose Flushing Web Design in 2026 | NYC Chinese Business Guide | 70NYC",
            "description": "Flushing web design guide — template vs custom, bilingual sites, mobile speed, SEO basics, pricing transparency for Queens Chinese businesses.",
            "keywords": "Flushing web design, Flushing website development, Queens web design, Flushing web design company, NYC Chinese web design",
            "h1": "How to Choose Flushing Web Design",
            "intro": "Searching for web design in Flushing returns everything from $299 templates to $15,000 custom builds. Queens Chinese businesses — restaurants, salons, contractors, schools, clinics — need a site that ranks on Google, generates inquiries, and represents your brand. This guide helps you decide in ten minutes.",
            "sections": [
                {
                    "h2": "Four questions before you hire",
                    "paragraphs": [
                        "Where do customers find you — Google Maps, WeChat, or referrals? Do you need bilingual content? Online booking or quotes? Who updates menus and prices later?",
                        "Answers determine whether you need a brochure site, restaurant platform, or SEO-ready marketing site — not simply the lowest price.",
                    ],
                },
                {
                    "h2": "Template vs custom for Flushing businesses",
                    "paragraphs": [
                        "Templates launch fast and cost less upfront but often score poorly on speed and local SEO structure.",
                        "Custom builds fit competitive categories (contractors, law, med spa), brand differentiation, and Google Ads tracking. 70NYC typically delivers in 2–4 weeks with mobile-first design and baseline <a href=\"/en/services/seo/\">SEO setup</a>.",
                    ],
                    "list": [
                        "Choose template: tight budget, short campaigns, strong referral flow",
                        "Choose custom: Google-driven leads, multiple services, bilingual brand image",
                        "Either way: mobile-first — most Flushing searches happen on phones",
                    ],
                },
                {
                    "h2": "Six must-check items in any proposal",
                    "paragraphs": ["Review case studies on your phone before signing:"],
                    "list": [
                        "Interactive within ~3 seconds (solid Core Web Vitals)",
                        "Click-to-call, WeChat, or forms above the fold",
                        "Natural Chinese and English — not machine-translated",
                        "Dedicated service or area pages for local rankings",
                        "Access to Analytics and Search Console",
                        "Contract states you own domain and deliverables",
                    ],
                },
                {
                    "h2": "Align website, Maps, and ads",
                    "paragraphs": [
                        "Your GBP website link should point to your best converting page. Ad landing pages must match organic site NAP data.",
                        "Effective Flushing stacks: custom site + local SEO + Maps optimization + small Search campaigns to test keywords.",
                    ],
                },
                {
                    "h2": "What Flushing web design typically costs",
                    "paragraphs": [
                        "Brochure sites vary by page count and bilingual scope; restaurant menus and booking add complexity.",
                        "Beware $299 all-in offers that exclude SEO, maintenance, and domain ownership — clarify annual fees and revision limits.",
                    ],
                },
                {
                    "h2": "Why Flushing clients work with 70NYC",
                    "paragraphs": [
                        "We've built projects across Queens with in-person meetings near Main St and Roosevelt Ave — design that fits Chinese-owned businesses, not translated generic templates.",
                        "See our <a href=\"/en/areas/flushing/\">Flushing service page</a> and <a href=\"/en/services/web-design/\">web design services</a>, or call 386-316-1848 for a free scope estimate.",
                    ],
                },
            ],
            "footer_seo": "Flushing web design · Flushing website development · Queens web design · NYC Chinese web design",
        },
    },
    {
        "slug": "brooklyn-contractor-local-seo-2026",
        "date": "2026-06-18",
        "zh": {
            "title": "布鲁克林华人装修/承包商 Google 地图 SEO 指南｜70NYC",
            "description": "日落公园、本森贺装修公司与承包商如何在 Google 地图和本地搜索获客？GBP、案例页、评价与布鲁克林网站设计配合——2026 实操指南。",
            "keywords": "布鲁克林SEO, 布鲁克林网站设计, 日落公园装修, Brooklyn contractor SEO, 布鲁克林Google地图, 本森贺网站, 华人装修公司SEO",
            "h1": "布鲁克林装修与承包商怎么做本地 SEO？",
            "intro": "布鲁克林华人装修、水电、厨房改造、屋顶工程大量集中在日落公园（Sunset Park）、本森贺（Bensonhurst）、班森贺（Bay Ridge）等社区。客人搜「Brooklyn kitchen remodel」「布鲁克林 装修公司 附近」时，Google 本地包只显示 3 家——不进前三，电话就少了。本文针对<strong>布鲁克林承包商与装修队</strong>，不是通用纽约大词。",
            "sections": [
                {
                    "h2": "布鲁克林装修客户怎么搜 Google",
                    "paragraphs": [
                        "中文：布鲁克林 装修、日落公园 厨房改造、本森贺 水电工、布鲁克林 屋顶、班森贺 装修公司。英文：Brooklyn contractor near me、Sunset Park kitchen renovation、Bensonhurst plumber、Brooklyn home remodeling。",
                        "这些词比「纽约网站设计」更接近成交。网站 title、H1 和 GBP 简介应分别覆盖<strong>Brooklyn + 社区 + 服务</strong>，而不是只写公司中文名。",
                    ],
                },
                {
                    "h2": "Google Business Profile：承包商必做项",
                    "paragraphs": ["装修类 GBP 比餐馆更依赖信任信号："],
                    "list": [
                        "Primary category 选 General contractor / Kitchen remodeler 等最贴近项",
                        "服务区域如实填写布鲁克林各社区，勿虚假扩展到曼哈顿",
                        "上传执照、保险、Before/After 案例图（带简短文字说明）",
                        "服务列表写清：厨房、浴室、屋顶、地下室、商业装修",
                        "每周 Post 更新完工案例或季节性促销（春季装修旺季）",
                        "电话、网站与 <a href=\"/areas/brooklyn/\">布鲁克林服务页</a> 完全一致",
                    ],
                },
                {
                    "h2": "案例页：布鲁克林 SEO 的核心资产",
                    "paragraphs": [
                        "一页 PDF 作品集不够——Google 需要可索引文字。每个案例建议独立段落：「Sunset Park 厨房改造 · 3 周完工 · 橱柜+台面+电气」，附 3–5 张图与 alt 描述。",
                        "这比堆「布鲁克林网站设计」关键词更有效。我们建站时会按社区建案例筛选或标签，方便客人找「本区做过类似项目」的承包商。",
                    ],
                },
                {
                    "h2": "评价：装修行业排名加速器",
                    "paragraphs": [
                        "布鲁克林华人装修很多靠口碑，但 Google 只认公开评价。完工后 48 小时内邀请客户留评，附上项目类型（厨房/浴室）。",
                        "回复每条评价（中英皆可），展示售后负责。切勿刷评——Google 对 contractor 类别审核更严。",
                    ],
                },
                {
                    "h2": "网站 + 地图 + 广告的常见组合",
                    "paragraphs": [
                        "打底：移动端网站 + 案例页 + GBP 优化 + 本地 SEO。旺季：Google Ads 投「Brooklyn kitchen remodel」等词，落地页与 organic 站同一电话。",
                        "若预算有限，优先<strong>网站速度 + 案例文字 + GBP</strong>，再考虑广告。需要 <a href=\"/services/web-design/\">布鲁克林网站设计</a> 或 <a href=\"/services/seo/\">SEO 代运营</a> 可预约免费咨询。",
                    ],
                },
                {
                    "h2": "与法拉盛、曼哈顿竞品的差异",
                    "paragraphs": [
                        "布鲁克林客人更在意「有没有做过我们社区」「能不能说粤语/普通话」「报价是否透明」。网站应突出服务半径、社区案例和表单报价——而不是曼哈顿式的品牌大片。",
                        "延伸阅读：<a href=\"/blog/flushing-restaurant-google-maps-seo-2026/\">法拉盛餐馆地图 SEO</a>（餐饮逻辑类似，可对照 GBP 做法）。",
                    ],
                },
            ],
            "footer_seo": "布鲁克林SEO · 布鲁克林网站设计 · 日落公园装修 · Brooklyn contractor SEO · 本森贺网站",
        },
        "en": {
            "title": "Brooklyn Contractor Google Maps & Local SEO Guide 2026 | 70NYC",
            "description": "How Brooklyn Chinese contractors rank on Google Maps — Sunset Park, Bensonhurst remodeling SEO, GBP, portfolio pages, and reviews.",
            "keywords": "Brooklyn SEO, Brooklyn web design, Sunset Park contractor, Brooklyn Google Maps, Bensonhurst remodeling SEO, Chinese contractor Brooklyn",
            "h1": "Local SEO for Brooklyn Contractors & Remodelers",
            "intro": "Chinese-owned remodeling, plumbing, kitchen, and roofing crews cluster in Sunset Park, Bensonhurst, and Bay Ridge. When customers search \"Brooklyn kitchen remodel near me,\" Google shows only three map results. This guide focuses on <strong>Brooklyn contractors</strong> — not generic NYC keywords.",
            "sections": [
                {
                    "h2": "How Brooklyn customers search",
                    "paragraphs": [
                        "Chinese: 布鲁克林 装修, 日落公园 厨房改造, 本森贺 水电. English: Brooklyn contractor near me, Sunset Park kitchen renovation, Bensonhurst plumber.",
                        "These terms convert better than \"NYC web design.\" Titles, H1s, and GBP descriptions should target <strong>Brooklyn + neighborhood + service</strong>.",
                    ],
                },
                {
                    "h2": "Google Business Profile for contractors",
                    "paragraphs": ["Trust signals matter more than for restaurants:"],
                    "list": [
                        "Pick accurate primary categories (General contractor, Kitchen remodeler)",
                        "Set honest service areas — don't fake Manhattan coverage",
                        "Upload license, insurance, and before/after photos with captions",
                        "List services: kitchen, bath, roof, basement, commercial",
                        "Weekly Posts for completed jobs or seasonal promos",
                        "Match phone and website with your <a href=\"/en/areas/brooklyn/\">Brooklyn service page</a>",
                    ],
                },
                {
                    "h2": "Portfolio pages as SEO assets",
                    "paragraphs": [
                        "A PDF portfolio isn't enough — Google needs indexable text. Each project: \"Sunset Park kitchen remodel · 3 weeks · cabinets + counters + electrical\" with alt text on photos.",
                        "We build neighborhood-tagged case studies so prospects find contractors who've worked nearby.",
                    ],
                },
                {
                    "h2": "Reviews accelerate rankings",
                    "paragraphs": [
                        "Brooklyn remodeling runs on referrals, but Google ranks on public reviews. Ask within 48 hours of completion; mention project type in replies.",
                        "Never buy reviews — contractor categories face strict Google enforcement.",
                    ],
                },
                {
                    "h2": "Website + Maps + Ads stack",
                    "paragraphs": [
                        "Baseline: mobile site + case studies + GBP + local SEO. Peak season: Google Ads on \"Brooklyn kitchen remodel\" with matching landing pages.",
                        "Budget tight? Prioritize site speed, written case studies, and GBP before ads. See <a href=\"/en/services/web-design/\">Brooklyn web design</a> and <a href=\"/en/services/seo/\">SEO services</a>.",
                    ],
                },
                {
                    "h2": "Brooklyn vs Manhattan positioning",
                    "paragraphs": [
                        "Brooklyn clients care about neighborhood proof, bilingual communication, and transparent quotes — not Manhattan-style brand films.",
                        "Related: <a href=\"/en/blog/flushing-restaurant-google-maps-seo-2026/\">Flushing restaurant Maps SEO</a> (similar GBP playbook).",
                    ],
                },
            ],
            "footer_seo": "Brooklyn SEO · Brooklyn web design · Sunset Park contractor · Bensonhurst remodeling",
        },
    },
]


# ── Shared HTML builders ─────────────────────────────────────────────────────

def prefix(lang: str) -> str:
    return "" if lang == "zh" else "/en"


def nav_html(lang: str, active: str = "", page_path: str = "/") -> str:
    items = NAV_ZH if lang == "zh" else NAV_EN
    links = []
    for key, href, label in items:
        cls = ' class="active"' if key == active else ""
        links.append(f'      <a href="{href}" data-nav="{key}"{cls}>{label}</a>')
    p = prefix(lang)
    home = "/" if lang == "zh" else "/en/"
    bare = page_path.removeprefix("/en")
    en_href = "/en/" if bare in ("", "/") else f"/en{bare}"
    zh_href = "/" if bare in ("", "/") else bare
    lang_switch = (
        f'<a class="lang-switch" href="{en_href}" hreflang="en">EN</a>'
        if lang == "zh"
        else f'<a class="lang-switch" href="{zh_href}" hreflang="zh-CN">中文</a>'
    )
    consult = f"{p}/contact/"
    consult_label = "免费咨询" if lang == "zh" else "Free Consult"
    logo_small = "纽约数字营销专家" if lang == "zh" else "NYC Digital Marketing"
    menu_label = "打开菜单" if lang == "zh" else "Open menu"
    return f"""  <header class="site-header" id="header">
    <a class="logo" href="{home}"><span>70</span>NYC<small>{logo_small}</small></a>
    <button class="menu-toggle" id="menuToggle" aria-label="{menu_label}" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav" id="nav">
{chr(10).join(links)}
    </nav>
    <div class="header-cta">
      {lang_switch}
      <a class="phone" href="tel:3863161848">386-316-1848</a>
      <a class="btn btn-gold" href="{consult}">{consult_label}</a>
    </div>
  </header>"""


def footer_html(lang: str, footer_seo: str) -> str:
    p = prefix(lang)
    service_links = "\n".join(
        f'        <a href="{p}/services/{slug}/">{zh if lang == "zh" else en}</a>'
        for slug, zh, en in SERVICES
    )
    if lang == "zh":
        areas_label, nationwide_label = "服务区域", "全美远程"
        about_col, services_col = "关于我们", "关于我们的服务"
        sitemap_label = "网站地图"
        brand = "纽约网站设计公司与网站开发团队，为华人企业提供网页设计、手机应用开发、平面设计、餐馆网站、专业广告推广及 SEO 服务。"
        about_links = """        <a href="/about/">了解我们</a>
        <a href="/about/">我们的团队</a>
        <a href="/contact/">联系我们</a>
        <a href="/faq/">常见问题</a>"""
    else:
        areas_label, nationwide_label = "Service Areas", "Nationwide Remote"
        about_col, services_col = "About", "Services"
        sitemap_label = "Sitemap"
        brand = "NYC web design and development team — web design, mobile apps, graphic design, restaurant websites, advertising, and SEO for local businesses."
        about_links = """        <a href="/en/about/">About Us</a>
        <a href="/en/about/">Our Team</a>
        <a href="/en/contact/">Contact</a>
        <a href="/en/faq/">FAQ</a>"""
    return f"""  <footer class="footer">
    <div class="footer-main">
      <div class="footer-brand">
        <div class="logo"><span>70</span>NYC<small>{"纽约数字营销专家" if lang == "zh" else "NYC Digital Marketing"}</small></div>
        <p>{brand}</p>
      </div>
      <nav class="footer-col" aria-label="{about_col}">
        <b>{about_col}</b>
{about_links}
      </nav>
      <nav class="footer-col" aria-label="{services_col}">
        <b>{services_col}</b>
{service_links}
        <a href="{p}/areas/">{areas_label}</a>
        <a href="{p}/nationwide/">{nationwide_label}</a>
        <a href="{p}/process/">{"项目流程" if lang == "zh" else "Our Process"}</a>
        <a href="{p}/blog/">{"博客" if lang == "zh" else "Blog"}</a>
        <a href="{p}/sitemap/">{sitemap_label}</a>
      </nav>
    </div>
    <p class="footer-seo">
      {"服务区域：" if lang == "zh" else "Areas served: "}{footer_seo}
    </p>
    <div class="footer-bottom">
      <address>386-316-1848 · info@70nyc.com · New York, NY</address>
    </div>
  </footer>"""


def service_grid_html(lang: str) -> str:
    p = prefix(lang)
    title = "我们的服务" if lang == "zh" else "Our Services"
    cards = []
    for slug, zh, en in SERVICES:
        label = zh if lang == "zh" else en
        cards.append(
            f'          <a class="page-seo-related-card" href="{p}/services/{slug}/">\n'
            f'            <span class="page-seo-related-arrow" aria-hidden="true">→</span>\n'
            f"            <b>{label}</b>\n"
            f'            <span>{"了解详情" if lang == "zh" else "Learn more"}</span>\n'
            f"          </a>"
        )
    return f"""    <section class="page-seo-supplement" aria-label="{title}">
      <div class="page-seo-supplement-inner">
        <div class="page-seo-supplement-head">
          <span class="label">70NYC</span>
          <h2>{title}</h2>
        </div>
        <div class="page-seo-related-grid" style="margin-top:24px">
{chr(10).join(cards)}
        </div>
      </div>
    </section>
"""


def head_html(lang: str, meta: dict, canonical_path: str, extra_schema: str = "") -> str:
    html_lang = "zh-CN" if lang == "zh" else "en"
    canonical = f"{DOMAIN}{canonical_path}"
    p = prefix(lang)
    path_no_en = canonical_path.removeprefix("/en")
    hreflang_zh = f"{DOMAIN}{path_no_en}"
    hreflang_en = f"{DOMAIN}/en{path_no_en}"
    keywords = meta.get("keywords", "")
    kw_line = f'\n  <meta name="keywords" content="{keywords}" />' if keywords else ""
    return f"""<!doctype html>
<html lang="{html_lang}">
<head>
{GTAG_SNIPPET}  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{meta['title']}</title>
  <meta name="description" content="{meta['description']}" />{kw_line}
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" hreflang="zh-CN" href="{hreflang_zh}" />
  <link rel="alternate" hreflang="en" href="{hreflang_en}" />
  <link rel="alternate" hreflang="x-default" href="{DOMAIN}/" />
  <meta property="og:locale" content="{"zh_CN" if lang == "zh" else "en_US"}" />
  <meta property="og:title" content="{meta['title']}" />
  <meta property="og:description" content="{meta['description']}" />
  <meta property="og:type" content="{meta.get("og_type", "website")}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE['og_image']}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{SITE['og_image']}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,700;0,9..40,900;1,9..40,400&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/style.css?{SITE['style_css']}" />
  <script src="/assets/lang-detect.js?{SITE['lang_detect_js']}"></script>
{extra_schema}
</head>
<body class="page-sub">
"""


def breadcrumb_schema(lang: str, crumbs: list[tuple[str, str]]) -> str:
    items = []
    for i, (name, url) in enumerate(crumbs, 1):
        items.append(
            f'      {{"@type": "ListItem", "position": {i}, "name": "{name}", "item": "{url}"}}'
        )
    return f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
{",".join(items)}
    ]
  }}
  </script>
"""


def local_business_schema(name: str, desc: str, area: str) -> str:
    return f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "{name}",
    "provider": {{"@type": "LocalBusiness", "name": "70NYC", "telephone": "+1-386-316-1848"}},
    "areaServed": ["{area}", "New York"],
    "description": "{desc}"
  }}
  </script>
"""


def hero_html(
    lang: str,
    meta: dict,
    crumbs: list[tuple[str, str | None]],
    theme_idx: int = 0,
    *,
    show_actions: bool = True,
) -> str:
    p = prefix(lang)
    home_label = "首页" if lang == "zh" else "Home"
    home_href = "/" if lang == "zh" else "/en/"
    crumb_items = [f'<li><a href="{home_href}">{home_label}</a></li>']
    for label, href in crumbs:
        if href:
            crumb_items.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            crumb_items.append(f'<li aria-current="page">{label}</li>')
    theme = HERO_THEMES[theme_idx % len(HERO_THEMES)]
    deco = HERO_DECOS[theme_idx % len(HERO_DECOS)]
    tags = "".join(f"<span>{t}</span>" for t in meta.get("tags", []))
    stats = meta.get("stats", [])
    stats_html = "".join(
        f'<div class="page-seo-stat"><b>{a}</b><span>{b}</span></div>' for a, b in stats
    )
    actions = ""
    if show_actions:
        cta_p = meta.get("cta_primary")
        cta_g = meta.get("cta_ghost")
        if cta_p:
            label, href = cta_p
            ghost = ""
            if cta_g:
                gl, gh = cta_g
                ghost = f'\n            <a class="btn btn-ghost" href="{gh}">{gl}</a>'
            actions = f"""          <div class="page-seo-hero-actions">
            <a class="btn btn-primary" href="{href}">{label} →</a>{ghost}
          </div>
"""
    stats_block = ""
    if stats_html:
        stats_block = f'        <div class="page-seo-stats" aria-label="{"关键数据" if lang == "zh" else "Key figures"}">{stats_html}</div>\n'
    tags_block = ""
    if tags:
        tags_block = f'        <div class="page-seo-keywords" aria-label="{"服务关键词" if lang == "zh" else "Keywords"}">{tags}</div>\n'
    return f"""    <div class="page-seo-hero page-seo-hero--{theme}">
      <div class="page-seo-hero-bg" aria-hidden="true"></div>
      <div class="page-seo-hero-glow" aria-hidden="true"></div>
      <div class="page-seo-hero-deco page-seo-hero-deco--{deco}" aria-hidden="true"></div>
      <div class="page-seo-hero-inner">
        <nav class="page-seo-breadcrumb" aria-label="{"面包屑导航" if lang == "zh" else "Breadcrumb"}">
          <ol>
{chr(10).join("            " + c for c in crumb_items)}
          </ol>
        </nav>
        <div class="page-seo-hero-focus">
          <span class="page-seo-eyebrow">{meta['eyebrow']}</span>
          <h1>{meta['h1']}</h1>
          <p class="page-seo-lead">{meta['lead']}</p>
{actions}        </div>
{stats_block}{tags_block}      </div>
    </div>
"""


def supplement_html(lang: str, meta: dict) -> str:
    cards = []
    for i, (title, body) in enumerate(meta["topics"], 1):
        cards.append(
            f"""          <article class="page-seo-topic-card">
            <span class="page-seo-topic-num">0{i}</span>
            <h3>{title}</h3>
            <p>{body}</p>
          </article>"""
        )
    highlights = "".join(f"<li>{h}</li>" for h in meta["highlights"])
    aside_title = meta.get("highlights_title", "为什么选择 70NYC" if lang == "zh" else "Why 70NYC")
    return f"""    <section class="page-seo-supplement" aria-label="{meta.get('section_h2', '')}">
      <div class="page-seo-supplement-inner">
        <div class="page-seo-supplement-head">
          <span class="label">{meta.get('label', '70NYC')}</span>
          <h2>{meta['section_h2']}</h2>
        </div>
        <div class="page-seo-topic-grid">
{chr(10).join(cards)}
        </div>
        <aside class="page-seo-supplement-aside">
          <b>{aside_title}</b>
          <ul class="page-seo-highlight-list">{highlights}</ul>
        </aside>
      </div>
    </section>
"""


def area_faq_html(lang: str, faqs: list[dict], area_name: str) -> str:
    items = []
    for i, item in enumerate(faqs):
        open_attr = " open" if i == 0 else ""
        items.append(
            f"""          <details class="faq-item"{open_attr}>
            <summary>{item["q"]}</summary>
            <p>{item["a"]}</p>
          </details>"""
        )
    title = "常见问题" if lang == "zh" else "FAQ"
    h2 = f"{area_name}网站设计常见问题" if lang == "zh" else f"{area_name} Web Design FAQ"
    return f"""    <section class="page-seo-supplement page-seo-area-faq" aria-label="{title}">
      <div class="page-seo-supplement-inner">
        <div class="page-seo-supplement-head">
          <span class="label">FAQ</span>
          <h2>{h2}</h2>
        </div>
        <div class="faq-list">
{chr(10).join(items)}
        </div>
      </div>
    </section>
"""


def faq_page_schema(faqs: list[dict]) -> str:
    entities = []
    for item in faqs:
        q = item["q"].replace('"', '\\"')
        a = re.sub(r"<[^>]+>", "", item["a"]).replace('"', '\\"')
        entities.append(
            f'      {{"@type": "Question", "name": "{q}", "acceptedAnswer": {{"@type": "Answer", "text": "{a}"}}}}'
        )
    return f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{",".join(entities)}
    ]
  }}
  </script>
"""


def related_html(lang: str, related: list[tuple[str, str, str]], title: str | None = None) -> str:
    cards = []
    for href, b, span in related:
        cards.append(
            f"""          <a class="page-seo-related-card" href="{href}">
            <span class="page-seo-related-arrow" aria-hidden="true">→</span>
            <b>{b}</b>
            <span>{span}</span>
          </a>"""
        )
    label = title or ("继续探索" if lang == "zh" else "Keep Exploring")
    return f"""    <nav class="page-seo-related" aria-label="{"相关页面" if lang == "zh" else "Related pages"}">
      <div class="page-seo-related-inner">
        <span class="label">{label}</span>
        <div class="page-seo-related-grid">
{chr(10).join(cards)}
        </div>
      </div>
    </nav>
"""


def write_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def assemble_page(
    lang: str,
    meta: dict,
    canonical_path: str,
    main_html: str,
    schema: str,
    footer_seo: str,
    active_nav: str = "",
) -> str:
    return (
        head_html(lang, meta, canonical_path, schema)
        + nav_html(lang, active_nav, canonical_path)
        + "\n\n  <main>\n"
        + main_html
        + "\n  </main>\n\n"
        + footer_html(lang, footer_seo)
        + f"\n\n  <script src=\"/assets/main.js?{SITE['main_js']}\"></script>\n</body>\n</html>\n"
    )


# ── Generators ───────────────────────────────────────────────────────────────

def generate_nationwide() -> list[str]:
    urls = []
    for lang in ("zh", "en"):
        meta = NATIONWIDE[lang]
        p = prefix(lang)
        path = f"{p}/nationwide/"
        crumbs = [(meta["breadcrumb"], None)]
        schema = breadcrumb_schema(lang, [
            ("首页" if lang == "zh" else "Home", f"{DOMAIN}/" if lang == "zh" else f"{DOMAIN}/en/"),
            (meta["breadcrumb"], f"{DOMAIN}{path}"),
        ])
        schema += "\n" + local_business_schema(
            meta["schema_name"], meta["schema_desc"], "United States"
        )
        main = (
            hero_html(lang, meta, crumbs, theme_idx=1)
            + "\n"
            + supplement_html(lang, meta)
            + "\n"
            + service_grid_html(lang)
            + "\n"
            + related_html(lang, meta["related"])
        )
        out = ROOT / "nationwide" / "index.html" if lang == "zh" else ROOT / "en" / "nationwide" / "index.html"
        write_page(out, assemble_page(lang, meta, path, main, schema, meta["footer_seo"]))
        urls.append(f"{DOMAIN}{path}")
    return urls


def area_related(lang: str, current_slug: str) -> list[tuple[str, str, str]]:
    p = prefix(lang)
    area = next(a for a in AREAS if a["slug"] == current_slug)
    others = [a for a in AREAS if a["slug"] != current_slug][:2]
    related = []
    rb = area.get("related_blog")
    if rb:
        m = rb[lang]
        related.append((f"{p}/blog/{rb['slug']}/", m["title"], m["span"]))
    related.extend(
        (f"{p}/areas/{a['slug']}/", a[lang]["breadcrumb"], a[lang]["eyebrow"].split("·")[0].strip())
        for a in others
    )
    related.append((f"{p}/nationwide/", "全美远程" if lang == "zh" else "Nationwide", "Remote US-wide"))
    related.append((f"{p}/contact/", "免费咨询" if lang == "zh" else "Contact", "24h" if lang == "en" else "24h 内回复"))
    return related


def generate_areas() -> list[str]:
    urls = []
    for lang in ("zh", "en"):
        hub = AREAS_HUB[lang]
        p = prefix(lang)
        hub_path = f"{p}/areas/"
        schema = breadcrumb_schema(lang, [
            ("首页" if lang == "zh" else "Home", f"{DOMAIN}/" if lang == "zh" else f"{DOMAIN}/en/"),
            (hub["breadcrumb"], f"{DOMAIN}{hub_path}"),
        ])
        cards = []
        for area in AREAS:
            m = area[lang]
            cards.append(
                f'          <a class="page-seo-related-card" href="{p}/areas/{area["slug"]}/">\n'
                f'            <span class="page-seo-related-arrow" aria-hidden="true">→</span>\n'
                f"            <b>{m['breadcrumb']}</b>\n"
                f"            <span>{m['eyebrow']}</span>\n"
                f"          </a>"
            )
        hub_main = (
            hero_html(lang, {**hub, "tags": [], "stats": []}, [(hub["breadcrumb"], None)], theme_idx=0, show_actions=False)
            + f"""    <section class="page-seo-supplement">
      <div class="page-seo-supplement-inner">
        <div class="page-seo-supplement-head">
          <span class="label">70NYC Areas</span>
          <h2>{hub['section_h2']}</h2>
          <p style="margin-top:12px;color:var(--text-muted)">{hub['intro']}</p>
        </div>
        <div class="page-seo-related-grid">
{chr(10).join(cards)}
        </div>
      </div>
    </section>
"""
            + related_html(
                lang,
                [
                    (f"{p}/nationwide/", "全美远程" if lang == "zh" else "Nationwide", "Remote"),
                    (f"{p}/services/", "服务总览" if lang == "zh" else "All Services", ""),
                    (f"{p}/contact/", "联系" if lang == "zh" else "Contact", ""),
                ],
                "更多" if lang == "zh" else "More",
            )
        )
        hub_meta = {**hub, "keywords": ""}
        out = ROOT / "areas" / "index.html" if lang == "zh" else ROOT / "en" / "areas" / "index.html"
        footer = "纽约六大区域 · 曼哈顿 · 法拉盛 · 布鲁克林 · 长岛 · 布朗克斯 · 史泰登岛" if lang == "zh" else "NYC areas · Manhattan · Flushing · Brooklyn · Long Island · Bronx · Staten Island"
        write_page(out, assemble_page(lang, hub_meta, hub_path, hub_main, schema, footer))
        urls.append(f"{DOMAIN}{hub_path}")

    for idx, area in enumerate(AREAS):
        for lang in ("zh", "en"):
            meta = area[lang]
            p = prefix(lang)
            path = f"{p}/areas/{area['slug']}/"
            crumbs = [
                ("服务区域" if lang == "zh" else "Service Areas", f"{p}/areas/"),
                (meta["breadcrumb"], None),
            ]
            schema = breadcrumb_schema(lang, [
                ("首页" if lang == "zh" else "Home", f"{DOMAIN}/" if lang == "zh" else f"{DOMAIN}/en/"),
                ("服务区域" if lang == "zh" else "Service Areas", f"{DOMAIN}{p}/areas/"),
                (meta["breadcrumb"], f"{DOMAIN}{path}"),
            ])
            schema += "\n" + local_business_schema(
                f"{'纽约' if lang == 'zh' else ''}{meta['breadcrumb']}{'网站设计' if lang == 'zh' else ' Web Design'}",
                meta["description"],
                area["area_served"],
            )
            if meta.get("faq"):
                schema += "\n" + faq_page_schema(meta["faq"])
            meta_full = {
                **meta,
                "label": f"70NYC {meta['breadcrumb']}",
                "section_h2": "本地服务说明" if lang == "zh" else "Local Service Overview",
                "highlights_title": "常见行业" if lang == "zh" else "Common Industries",
                "keywords": meta.get("keywords", ""),
                "cta_primary": ("获取本区方案", f"{p}/contact/") if lang == "zh" else ("Get Area Proposal", f"{p}/contact/"),
                "cta_ghost": ("全美远程", f"{p}/nationwide/") if lang == "zh" else ("Nationwide Remote", f"{p}/nationwide/"),
                "stats": [
                    ("13+", "年经验" if lang == "zh" else "Years"),
                    ("面谈", "本区可约" if lang == "zh" else "Local meetings"),
                    ("5", "大核心服务" if lang == "zh" else "Core services"),
                    ("中英", "双语" if lang == "zh" else "Bilingual"),
                ],
            }
            faq_block = area_faq_html(lang, meta["faq"], meta["breadcrumb"]) + "\n" if meta.get("faq") else ""
            main = (
                hero_html(lang, meta_full, crumbs, theme_idx=idx)
                + "\n"
                + supplement_html(lang, meta_full)
                + "\n"
                + faq_block
                + service_grid_html(lang)
                + "\n"
                + related_html(lang, area_related(lang, area["slug"]))
            )
            out = ROOT / "areas" / area["slug"] / "index.html" if lang == "zh" else ROOT / "en" / "areas" / area["slug"] / "index.html"
            write_page(out, assemble_page(lang, meta_full, path, main, schema, meta["footer_seo"]))
            urls.append(f"{DOMAIN}{path}")
    return urls


def blog_posting_schema(lang: str, post: dict, meta: dict, path: str) -> str:
    canonical = f"{DOMAIN}{path}"
    headline = meta["h1"].replace('"', '\\"')
    desc = meta["description"].replace('"', '\\"')
    return f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{headline}",
    "description": "{desc}",
    "datePublished": "{post['date']}",
    "dateModified": "{post['date']}",
    "inLanguage": "{"zh-CN" if lang == "zh" else "en-US"}",
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "{canonical}"}},
    "author": {{"@type": "Organization", "name": "70NYC", "url": "{DOMAIN}/"}},
    "publisher": {{
      "@type": "Organization",
      "name": "70NYC",
      "logo": {{"@type": "ImageObject", "url": "{SITE['og_image']}"}}
    }},
    "image": "{SITE['og_image']}"
  }}
  </script>
"""


def blog_body_html(lang: str, meta: dict, p: str) -> str:
    blocks: list[str] = []
    if meta.get("intro"):
        blocks.append(f'          <p class="page-seo-article-lead">{meta["intro"]}</p>')
    for section in meta.get("sections", []):
        blocks.append(f'          <h2>{section["h2"]}</h2>')
        for para in section.get("paragraphs", []):
            blocks.append(f"          <p>{para}</p>")
        if section.get("list"):
            items = "".join(f"\n            <li>{item}</li>" for item in section["list"])
            blocks.append(f"          <ul class=\"page-seo-article-list\">{items}\n          </ul>")
    for para in meta.get("paragraphs", []):
        blocks.append(f"          <p>{para}</p>")
    cta = "联系我们" if lang == "zh" else "Contact Us"
    blocks.append(f'          <p><a class="btn btn-primary" href="{p}/contact/">{cta} →</a></p>')
    return "\n".join(blocks) + "\n"


def blog_article_html(lang: str, post: dict, meta: dict) -> str:
    p = prefix(lang)
    path = f"{p}/blog/{post['slug']}/"
    crumbs = [
        ("博客" if lang == "zh" else "Blog", f"{p}/blog/"),
        (meta["h1"], None),
    ]
    meta.setdefault("title", meta["h1"] + "｜70NYC")
    meta["og_type"] = "article"
    schema = breadcrumb_schema(lang, [
        ("首页" if lang == "zh" else "Home", f"{DOMAIN}/" if lang == "zh" else f"{DOMAIN}/en/"),
        ("博客" if lang == "zh" else "Blog", f"{DOMAIN}{p}/blog/"),
        (meta["h1"], f"{DOMAIN}{path}"),
    ])
    schema += "\n" + blog_posting_schema(lang, post, meta, path)
    hero_meta = {
        "eyebrow": post["date"],
        "h1": meta["h1"],
        "lead": meta["description"],
        "tags": [],
        "stats": [],
    }
    body = blog_body_html(lang, meta, p)
    main = (
        hero_html(lang, hero_meta, crumbs, theme_idx=3, show_actions=False)
        + f"""    <section class="page-seo-supplement">
      <div class="page-seo-supplement-inner">
        <article class="page-seo-article-body">
{body}        </article>
      </div>
    </section>
"""
        + related_html(
            lang,
            [
                (f"{p}/areas/flushing/", "法拉盛服务" if lang == "zh" else "Flushing Services", ""),
                (f"{p}/services/seo/", "SEO 优化" if lang == "zh" else "SEO Services", ""),
                (f"{p}/blog/", "返回博客" if lang == "zh" else "Back to Blog", ""),
            ],
        )
    )
    footer = meta.get("footer_seo", "70NYC Blog")
    return assemble_page(lang, meta, path, main, schema, footer)


def generate_blog() -> list[str]:
    urls = []
    for lang in ("zh", "en"):
        p = prefix(lang)
        hub_path = f"{p}/blog/"
        hub_meta = {
            "title": "70NYC 博客｜纽约网站设计·SEO·营销洞察" if lang == "zh" else "70NYC Blog | NYC Web Design & Marketing Insights",
            "description": "70NYC 博客：纽约网站设计、SEO、Google Ads 与华人企业数字营销实践与案例。" if lang == "zh" else "70NYC blog — NYC web design, SEO, Google Ads, and digital marketing for local businesses.",
            "eyebrow": "Blog",
            "h1": "博客与洞察" if lang == "zh" else "Blog & Insights",
            "lead": "案例拆解、行业指南与本地搜索实践——持续更新。" if lang == "zh" else "Case studies, industry guides, and local search playbooks — updated over time.",
            "breadcrumb": "博客" if lang == "zh" else "Blog",
        }
        schema = breadcrumb_schema(lang, [
            ("首页" if lang == "zh" else "Home", f"{DOMAIN}/" if lang == "zh" else f"{DOMAIN}/en/"),
            (hub_meta["breadcrumb"], f"{DOMAIN}{hub_path}"),
        ])
        if BLOG_POSTS:
            items = []
            for post in BLOG_POSTS:
                m = post[lang]
                items.append(
                    f'          <a class="page-seo-related-card" href="{p}/blog/{post["slug"]}/">\n'
                    f'            <span class="page-seo-related-arrow" aria-hidden="true">→</span>\n'
                    f"            <b>{m['h1']}</b>\n"
                    f"            <span>{post['date']}</span>\n"
                    f"          </a>"
                )
            list_html = f"""        <div class="page-seo-related-grid">
{chr(10).join(items)}
        </div>"""
        else:
            empty = "文章即将发布，欢迎先浏览我们的服务页面或预约免费咨询。" if lang == "zh" else "Articles coming soon — explore our services or book a free consult."
            list_html = f'        <p style="color:var(--text-muted);margin-top:16px">{empty}</p>'
        hub_main = (
            hero_html(lang, {**hub_meta, "tags": [], "stats": []}, [(hub_meta["breadcrumb"], None)], theme_idx=4, show_actions=False)
            + f"""    <section class="page-seo-supplement">
      <div class="page-seo-supplement-inner">
        <div class="page-seo-supplement-head">
          <span class="label">70NYC Blog</span>
          <h2>{"最新文章" if lang == "zh" else "Latest Posts"}</h2>
        </div>
{list_html}
      </div>
    </section>
"""
            + related_html(lang, [(f"{p}/services/", "服务" if lang == "zh" else "Services", ""), (f"{p}/contact/", "联系" if lang == "zh" else "Contact", "")])
        )
        out = ROOT / "blog" / "index.html" if lang == "zh" else ROOT / "en" / "blog" / "index.html"
        write_page(out, assemble_page(lang, hub_meta, hub_path, hub_main, schema, "70NYC Blog"))
        urls.append(f"{DOMAIN}{hub_path}")

    for post in BLOG_POSTS:
        for lang in ("zh", "en"):
            p = prefix(lang)
            path = f"{p}/blog/{post['slug']}/"
            meta = post[lang]
            meta.setdefault("title", meta["h1"] + "｜70NYC")
            out = ROOT / "blog" / post["slug"] / "index.html" if lang == "zh" else ROOT / "en" / "blog" / post["slug"] / "index.html"
            write_page(out, blog_article_html(lang, post, meta))
            urls.append(f"{DOMAIN}{path}")
    return urls


def sitemap_entry(zh_path: str, priority: str = "0.82") -> str:
    en_path = f"/en{zh_path}" if zh_path != "/" else "/en/"
    if not zh_path.endswith("/"):
        zh_path += "/"
        en_path = f"/en{zh_path}"
    return f"""  <url>
    <loc>{DOMAIN}{zh_path}</loc>
    <xhtml:link rel="alternate" hreflang="zh-CN" href="{DOMAIN}{zh_path}" />
    <xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}{en_path}" />
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>
  <url>
    <loc>{DOMAIN}{en_path}</loc>
    <xhtml:link rel="alternate" hreflang="zh-CN" href="{DOMAIN}{zh_path}" />
    <xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}{en_path}" />
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>
"""


def update_sitemap(extra_paths: list[str]) -> None:
    sitemap = ROOT / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    added = 0
    for path in extra_paths:
        path = path.replace(DOMAIN, "")
        if not path.endswith("/"):
            path += "/"
        if f"<loc>{DOMAIN}{path}</loc>" in text:
            continue
        block = sitemap_entry(path)
        text = text.replace("</urlset>", block + "</urlset>")
        added += 1
        print(f"Sitemap + {path}")
    if added:
        sitemap.write_text(text, encoding="utf-8")
    else:
        print("Sitemap unchanged (URLs already present)")


def collect_paths_for_sitemap(target: str) -> list[str]:
    paths = []
    if target in ("all", "nationwide"):
        paths.extend(["/nationwide/"])
    if target in ("all", "areas"):
        paths.append("/areas/")
        paths.extend(f"/areas/{a['slug']}/" for a in AREAS)
    if target in ("all", "blog"):
        paths.append("/blog/")
        paths.extend(f"/blog/{p['slug']}/" for p in BLOG_POSTS)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate 70NYC SEO landing pages")
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        choices=["all", "nationwide", "areas", "blog", "sitemap"],
        help="Which pages to generate (default: all)",
    )
    args = parser.parse_args()

    if args.target == "sitemap":
        update_sitemap(collect_paths_for_sitemap("all"))
        return

    urls: list[str] = []
    if args.target in ("all", "nationwide"):
        urls.extend(generate_nationwide())
    if args.target in ("all", "areas"):
        urls.extend(generate_areas())
    if args.target in ("all", "blog"):
        urls.extend(generate_blog())

    update_sitemap(collect_paths_for_sitemap(args.target if args.target != "all" else "all"))
    print(f"\nDone — {len(urls)} HTML file(s) written.")


if __name__ == "__main__":
    main()
