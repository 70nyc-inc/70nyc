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
        "zh": {
            "title": "布鲁克林网站设计｜Brooklyn 网站开发与 SEO｜70NYC",
            "description": "70NYC 为布鲁克林华人企业提供网站设计、SEO、Google Ads——日落公园、本森贺、班森贺等社区，餐馆、装修、美容、零售。",
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
        },
        "en": {
            "title": "Brooklyn Web Design | NYC Website & SEO | 70NYC",
            "description": "Web design, SEO, and Google Ads for Chinese businesses in Brooklyn — Sunset Park, Bensonhurst, restaurants, contractors, beauty, retail.",
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
BLOG_POSTS: list[dict[str, Any]] = [
    # Example:
    # {
    #     "slug": "nyc-restaurant-website-tips",
    #     "date": "2026-06-08",
    #     "zh": {
    #         "title": "纽约餐馆网站必做的 5 件事｜70NYC",
    #         "description": "...",
    #         "h1": "纽约餐馆网站必做的 5 件事",
    #         "paragraphs": ["段落1", "段落2"],
    #     },
    #     "en": { ... },
    # },
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
    lang_switch = (
        f'<a class="lang-switch" href="/en{bare}?lang=en" hreflang="en">EN</a>'
        if lang == "zh"
        else f'<a class="lang-switch" href="{bare}?lang=zh" hreflang="zh-CN">中文</a>'
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
  <meta property="og:type" content="website" />
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
    others = [a for a in AREAS if a["slug"] != current_slug][:2]
    related = [
        (f"{p}/areas/{a['slug']}/", a[lang]["breadcrumb"], a[lang]["eyebrow"].split("·")[0].strip())
        for a in others
    ]
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
            meta_full = {
                **meta,
                "label": f"70NYC {meta['breadcrumb']}",
                "section_h2": "本地服务说明" if lang == "zh" else "Local Service Overview",
                "highlights_title": "常见行业" if lang == "zh" else "Common Industries",
                "cta_primary": ("获取本区方案", f"{p}/contact/") if lang == "zh" else ("Get Area Proposal", f"{p}/contact/"),
                "cta_ghost": ("全美远程", f"{p}/nationwide/") if lang == "zh" else ("Nationwide Remote", f"{p}/nationwide/"),
                "stats": [
                    ("13+", "年经验" if lang == "zh" else "Years"),
                    ("面谈", "本区可约" if lang == "zh" else "Local meetings"),
                    ("5", "大核心服务" if lang == "zh" else "Core services"),
                    ("中英", "双语" if lang == "zh" else "Bilingual"),
                ],
            }
            main = (
                hero_html(lang, meta_full, crumbs, theme_idx=idx)
                + "\n"
                + supplement_html(lang, meta_full)
                + "\n"
                + service_grid_html(lang)
                + "\n"
                + related_html(lang, area_related(lang, area["slug"]))
            )
            out = ROOT / "areas" / area["slug"] / "index.html" if lang == "zh" else ROOT / "en" / "areas" / area["slug"] / "index.html"
            write_page(out, assemble_page(lang, meta_full, path, main, schema, meta["footer_seo"]))
            urls.append(f"{DOMAIN}{path}")
    return urls


def blog_article_html(lang: str, post: dict, meta: dict) -> str:
    p = prefix(lang)
    path = f"{p}/blog/{post['slug']}/"
    crumbs = [
        ("博客" if lang == "zh" else "Blog", f"{p}/blog/"),
        (meta["h1"], None),
    ]
    paragraphs = "".join(f"          <p>{para}</p>\n" for para in meta.get("paragraphs", []))
    schema = breadcrumb_schema(lang, [
        ("首页" if lang == "zh" else "Home", f"{DOMAIN}/" if lang == "zh" else f"{DOMAIN}/en/"),
        ("博客" if lang == "zh" else "Blog", f"{DOMAIN}{p}/blog/"),
        (meta["h1"], f"{DOMAIN}{path}"),
    ])
    hero_meta = {
        "eyebrow": post["date"],
        "h1": meta["h1"],
        "lead": meta["description"],
        "tags": [],
        "stats": [],
    }
    main = (
        hero_html(lang, hero_meta, crumbs, theme_idx=3, show_actions=False)
        + f"""    <section class="page-seo-supplement">
      <div class="page-seo-supplement-inner">
        <div class="page-seo-article-body" style="max-width:720px">
{paragraphs}          <p><a class="btn btn-primary" href="{p}/contact/">{"联系我们" if lang == "zh" else "Contact Us"} →</a></p>
        </div>
      </div>
    </section>
"""
        + related_html(
            lang,
            [(f"{p}/blog/", "返回博客" if lang == "zh" else "Back to Blog", ""), (f"{p}/services/", "服务" if lang == "zh" else "Services", "")],
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
