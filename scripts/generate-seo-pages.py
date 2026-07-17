#!/usr/bin/env python3
"""
70NYC SEO page generator — nationwide, NYC area hubs, US states, and blog.

Usage:
  python3 scripts/generate-seo-pages.py all          # everything + sitemap
  python3 scripts/generate-seo-pages.py nationwide   # /nationwide/ (zh + en)
  python3 scripts/generate-seo-pages.py areas        # /areas/ hub + 6 districts
  python3 scripts/generate-seo-pages.py states       # /states/ hub + 51 state pages
  python3 scripts/generate-seo-pages.py cities       # /cities/ hub + priority metros
  python3 scripts/generate-seo-pages.py blog         # /blog/ index (+ posts from BLOG_POSTS)
  python3 scripts/generate-seo-pages.py sitemap      # merge new URLs into sitemap.xml only

Edit content in this file:
  - NATIONWIDE, AREAS, BLOG_POSTS
  - SERVICES (footer / service grid links)
  - SITE (asset cache-bust versions)
  - scripts/us_states_data.py for state metros

New blog post: append to BLOG_POSTS, then run:
  python3 scripts/generate-seo-pages.py blog
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from us_states_data import US_STATES  # noqa: E402
from us_cities_data import US_CITIES  # noqa: E402

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
    ("ai-marketing", "AI 智能营销", "AI Marketing"),
    ("social-media", "社交媒体管理", "Social Media"),
    ("mobile-app", "手机应用开发", "Mobile App Development"),
]

STATIC_SITEMAP_PATHS = ["/services/ai-marketing/"]

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
        "cta_ghost": ("50州+特区落地页", "/states/"),
        "stats": [("全美", "远程协作"), ("13+", "年经验"), ("中英", "双语团队"), ("24h", "内回复")],
        "tags": ["全美网站设计", "远程网站开发", "华人企业SEO", "远程Google Ads", "纽约总部", "全美华人营销"],
        "label": "70NYC Nationwide",
        "section_h2": "远程合作如何运作",
        "topics": [
            ("沟通方式", "Kickoff 用 Zoom/腾讯会议；日常微信、邮件与 Notion/飞书看板同步进度。关键节点（设计稿、上线）视频验收，与纽约本地客户相同标准。"),
            ("交付内容", "响应式网站、CMS 后台、基础 SEO、上线培训文档。可选月度 SEO、Google Ads 代运营与社媒内容——按月报告，数据透明。"),
            ("适合谁", "分店在多地、总部在纽约；或人在外州/海外、目标客户在纽约/全美；需要中英双语网站与搜索覆盖的华人企业。"),
            ("与纽约本地服务的关系", "大纽约六区可预约面谈；外地客户走远程流程。同一团队、同一报价逻辑，不因远程降低交付标准。按州查看：<a href=\"/states/\">美国各州远程服务页</a>。"),
        ],
        "highlights_title": "远程客户常选服务",
        "highlights": ["企业官网改版", "餐馆 / 外卖网站", "本地 SEO + Google Ads", "新店开业推广", "中英双语建站", "上线后运维"],
        "footer_seo": "全美远程：网站设计 · SEO · Google Ads · 社交媒体 · 华人企业数字营销 · 纽约总部远程交付 · 50州+DC",
        "schema_name": "全美远程网站设计与数字营销",
        "schema_desc": "远程网站设计、SEO、Google Ads 与社媒运营，服务全美华人企业。",
        "related": [
            ("/states/", "美国各州服务", "50州+华盛顿特区"),
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
        "cta_ghost": ("All 50 States + DC", "/en/states/"),
        "stats": [("US-wide", "Remote OK"), ("13+", "Years"), ("Bilingual", "EN & 中文"), ("24h", "Reply")],
        "tags": ["Nationwide web design", "Remote development", "Chinese business SEO", "Remote Google Ads", "NYC HQ", "US Chinese marketing"],
        "label": "70NYC Nationwide",
        "section_h2": "How Remote Delivery Works",
        "topics": [
            ("Communication", "Kickoff on Zoom; day-to-day via WeChat, email, and shared boards. Design and launch reviews on video — same checkpoints as NYC clients."),
            ("Deliverables", "Responsive site, CMS, basic SEO, training docs. Optional monthly SEO, Google Ads, and social — transparent reporting."),
            ("Who It's For", "Multi-location brands, owners outside NY serving US customers, and businesses needing bilingual web + search coverage."),
            ("NYC + Remote", "In-person meetings across six NYC areas; everywhere else uses the same remote playbook. Browse <a href=\"/en/states/\">state-by-state remote pages</a>."),
        ],
        "highlights_title": "Popular Remote Services",
        "highlights": ["Corporate site redesign", "Restaurant websites", "Local SEO + Google Ads", "New location launch", "Bilingual websites", "Post-launch care"],
        "footer_seo": "Nationwide remote: web design · SEO · Google Ads · social media · Chinese business marketing · 50 states + DC · delivered from NYC",
        "schema_name": "Nationwide Remote Web Design & Marketing",
        "schema_desc": "Remote web design, SEO, Google Ads, and social for Chinese-owned businesses across the US.",
        "related": [
            ("/en/states/", "US States", "50 states + DC"),
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
        "related_blog": {
            "slug": "manhattan-law-firm-local-seo-2026",
            "zh": {"title": "曼哈顿律所本地 SEO", "span": "律所·诊所·专业服务"},
            "en": {"title": "Manhattan Law Firm Local SEO", "span": "Legal · Professional"},
        },
        "zh": {
            "title": "曼哈顿网站设计｜纽约 Manhattan 网页开发与 SEO｜70NYC",
            "description": "70NYC 为曼哈顿华人企业提供网站设计、SEO、Google Ads 与社媒运营——律所、餐馆、美容、金融等，可预约曼哈顿面谈。",
            "keywords": "曼哈顿网站设计, 曼哈顿SEO, Manhattan web design, 纽约中城网站, 曼哈顿Google Ads, 华人律所网站, 曼哈顿网站制作",
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
            "faq": [
                {
                    "q": "曼哈顿律所或诊所网站需要英文为主还是中英双语？",
                    "a": "视客户群而定：服务主流美国客户以英文为主、中文摘要；华人社区律所/诊所建议核心页中英双语。Google 会分别索引两种语言信号，利于「Manhattan Chinese lawyer」「曼哈顿 律师」等搜索。详见 <a href=\"/blog/manhattan-law-firm-local-seo-2026/\">曼哈顿专业服务本地 SEO 指南</a>。",
                },
                {
                    "q": "曼哈顿网站设计和法拉盛、布鲁克林有什么不同？",
                    "a": "曼哈顿更强调品牌质感、加载速度、清晰的服务边界与合规信息（如律所 disclaimer、医疗隐私说明）。关键词侧重 Midtown/Downtown/Chinatown + 行业，而非社区街道名。",
                },
                {
                    "q": "在曼哈顿做 Google Ads 还是 SEO 先做？",
                    "a": "竞争高的词（如 personal injury、med spa）往往 Ads 更快见效；SEO 与专业内容页是长期资产。我们建议官网 + 本地 SEO 打底，再对高意向词小规模测试 Ads。",
                },
                {
                    "q": "可以在曼哈顿面谈吗？",
                    "a": "可以。我们可在中城、下城或唐人街附近约见，也支持视频评审设计稿。首次咨询免费。",
                },
                {
                    "q": "曼哈顿企业网站一般多久交付？",
                    "a": "标准专业形象站 2–4 周；含多 practice area、团队介绍、案例库或预约系统的律所/诊所站可能 4–6 周，报价阶段会给出里程碑。",
                },
            ],
        },
        "en": {
            "title": "Manhattan Web Design | NYC Website Development & SEO | 70NYC",
            "description": "Web design, SEO, Google Ads, and social for Chinese-owned businesses in Manhattan — law, restaurants, beauty, finance. In-person meetings available.",
            "keywords": "Manhattan web design, Manhattan SEO, NYC Midtown website, Manhattan Google Ads, Chinese law firm website, Manhattan website development",
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
            "faq": [
                {
                    "q": "Should Manhattan law firm sites be English-only or bilingual?",
                    "a": "Depends on clientele: English-primary with Chinese summaries for US-facing firms; core bilingual pages for Chinatown/community practices. Google indexes both for \"Manhattan Chinese lawyer\" and related terms. See our <a href=\"/en/blog/manhattan-law-firm-local-seo-2026/\">Manhattan professional services SEO guide</a>.",
                },
                {
                    "q": "How is Manhattan web design different from Flushing or Brooklyn?",
                    "a": "Manhattan emphasizes brand polish, speed, clear service boundaries, and compliance (legal disclaimers, healthcare privacy). Keywords focus on Midtown/Downtown/Chinatown + practice area — not neighborhood street names.",
                },
                {
                    "q": "Google Ads or SEO first in Manhattan?",
                    "a": "High-competition terms (personal injury, med spa) often need Ads for immediate visibility; SEO and content are long-term assets. We recommend website + local SEO baseline, then test Ads on high-intent keywords.",
                },
                {
                    "q": "Can we meet in Manhattan?",
                    "a": "Yes — Midtown, Downtown, or Chinatown meetings, or video design reviews. First consultation is free.",
                },
                {
                    "q": "How long does a Manhattan business website take?",
                    "a": "Standard professional sites: 2–4 weeks. Law/clinic sites with multiple practice areas, team pages, or booking: 4–6 weeks with milestones at proposal.",
                },
            ],
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
        "related_blog": {
            "slug": "long-island-chinese-business-local-seo-2026",
            "zh": {"title": "长岛本地 SEO 指南", "span": "装修·Great Neck"},
            "en": {"title": "Long Island Local SEO Guide", "span": "Contractors · Nassau"},
        },
        "zh": {
            "title": "长岛网站设计｜Long Island 网站开发与 SEO｜70NYC",
            "description": "70NYC 服务长岛华人企业网站设计、SEO、Google Ads——Great Neck、曼哈西特、Plainview 等，装修、美容、餐饮、专业服务。",
            "keywords": "长岛网站设计, 长岛SEO, Long Island web design, Great Neck网站, 长岛Google Ads, 长岛华人网站, 曼哈西特网站制作",
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
            "faq": [
                {
                    "q": "长岛网站为什么要写明服务范围？",
                    "a": "长岛客户常开车 15–30 分钟到店，Google 也会按距离排序。网站与 GBP 应清晰列出服务城镇（Great Neck、Manhasset、Plainview 等）与半径，减少无效咨询。详见 <a href=\"/blog/long-island-chinese-business-local-seo-2026/\">长岛华人企业本地 SEO 指南</a>。",
                },
                {
                    "q": "长岛装修/美容类客户怎么搜 Google？",
                    "a": "英文：Long Island kitchen remodel、Great Neck contractor、Nassau County dentist。中文：长岛 装修、Great Neck 美容、长岛 华人 律所。落地页应「城镇 + 服务」组合，而不是只写 Long Island。",
                },
                {
                    "q": "长岛企业需要 Google 地图吗？",
                    "a": "需要。即使有实体店面或上门服务区，GBP 仍是本地包核心。上传案例图、服务列表，并收集带项目类型的评价。",
                },
                {
                    "q": "可以在长岛见面吗？",
                    "a": "可以预约 North Shore、Nassau 一带见面，或远程协作。我们理解长岛季节性（如装修春季旺季）并可在方案里排期。",
                },
                {
                    "q": "长岛网站设计预算和曼哈顿差多少？",
                    "a": "页面复杂度决定价格，而非地理位置。案例型装修站通常比单页展示站高；报价会列明页数、双语、SEO 与维护选项，签约前透明锁定。",
                },
            ],
        },
        "en": {
            "title": "Long Island Web Design | NYC Suburbs SEO & Ads | 70NYC",
            "description": "Web design, SEO, and Google Ads for Chinese businesses on Long Island — Great Neck, Manhasset, Plainview, contractors, beauty, professional services.",
            "keywords": "Long Island web design, Long Island SEO, Great Neck website, Nassau web design, Long Island Google Ads, Chinese business Long Island",
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
            "faq": [
                {
                    "q": "Why must Long Island websites show service areas?",
                    "a": "Clients often drive 15–30 minutes; Google ranks partly by distance. Sites and GBP should list towns served (Great Neck, Manhasset, Plainview) to filter unqualified leads. See our <a href=\"/en/blog/long-island-chinese-business-local-seo-2026/\">Long Island local SEO guide</a>.",
                },
                {
                    "q": "How do Long Island customers search on Google?",
                    "a": "English: Long Island kitchen remodel, Great Neck contractor, Nassau County dentist. Chinese: 长岛 装修, Great Neck 美容. Landing pages need town + service — not generic \"Long Island\" alone.",
                },
                {
                    "q": "Do Long Island businesses need Google Maps?",
                    "a": "Yes. Whether storefront or service-area business, GBP drives the local pack. Upload project photos, service lists, and reviews mentioning job type.",
                },
                {
                    "q": "Can we meet on Long Island?",
                    "a": "Yes — North Shore and Nassau meetups, or remote collaboration. We plan around seasonal peaks like spring remodeling.",
                },
                {
                    "q": "How does Long Island web design pricing compare to Manhattan?",
                    "a": "Scope drives price, not geography. Portfolio contractor sites cost more than single-page brochures — proposals list pages, bilingual scope, SEO, and maintenance before sign-off.",
                },
            ],
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
    {
        "slug": "manhattan-law-firm-local-seo-2026",
        "date": "2026-06-19",
        "zh": {
            "title": "曼哈顿律所与专业服务本地 SEO 指南｜华人企业｜70NYC",
            "description": "曼哈顿律所、诊所、金融顾问如何在 Google 获得更高曝光？Midtown/Downtown 关键词、GBP、专业网站结构与评价策略——2026 实操。",
            "keywords": "曼哈顿SEO, 曼哈顿网站设计, 华人律所网站, Manhattan law firm SEO, 曼哈顿Google地图, 纽约中城网站, 曼哈顿诊所SEO",
            "h1": "曼哈顿律所与专业服务怎么做本地 SEO？",
            "intro": "曼哈顿华人律所、移民律师、诊所、医美、金融顾问面临的是<strong>高信任、高竞争</strong>搜索环境。客人搜「Manhattan immigration lawyer」「曼哈顿 离婚 律师」「Midtown med spa」时，不会点看起来不专业的网站。本文针对曼哈顿专业服务，与法拉盛餐馆、布鲁克林装修指南<strong>内容完全不同</strong>。",
            "sections": [
                {
                    "h2": "曼哈顿专业服务客户的搜索习惯",
                    "paragraphs": [
                        "英文搜索常带 neighborhood + specialty：Midtown employment lawyer、Downtown Chinese restaurant、Chinatown accountant。中文：曼哈顿 律师、中城 诊所、纽约 华人 会计。",
                        "与布鲁克林不同，曼哈顿更少「near me 街道名」，更多「行业权威 + 区域名」。网站应为每个 practice area 建独立落地页，而不是一个「关于我们」概括全部。",
                    ],
                },
                {
                    "h2": "律所/诊所网站的 SEO 结构",
                    "paragraphs": ["Google 需要看懂您做什么、服务谁："],
                    "list": [
                        "首页：清晰 value proposition + 电话 + 预约 CTA",
                        "Practice area 页：移民、家庭法、人身伤害等各自 title/H1 含 Manhattan",
                        "团队页：律师/医生资质、语言、教育背景（E-E-A-T 信号）",
                        "FAQ 页：程序、费用区间、首次咨询流程",
                        "联系页：NAP 与 Google Business Profile 完全一致",
                        "合规：律所 disclaimer、医疗 HIPAA 提示（不替代法律意见，但展示专业度）",
                    ],
                },
                {
                    "h2": "Google Business Profile 对曼哈顿专业服务的价值",
                    "paragraphs": [
                        "律所、诊所、医美仍有地图包展示。类别选 Lawyer / Law firm / Medical clinic 等精确项；服务列表写清 practice areas；上传办公室外观与团队照片（需客户授权）。",
                        "评价内容若提到具体服务（「移民案件办得很顺」），比空泛五星更有帮助。严禁虚假评价。",
                    ],
                },
                {
                    "h2": "中英双语如何布局",
                    "paragraphs": [
                        "常见结构：英文 URL 为主路径，中文核心页 mirror 或独立 /zh/  section；hreflang 与 canonical 要正确，避免 duplicate。",
                        "华人客户读中文、法院与合作伙伴可能查英文——双语不是翻译同一页，而是<strong>同一实体的两种受众入口</strong>。我们建站时见 <a href=\"/areas/manhattan/\">曼哈顿网站设计</a> 服务说明。",
                    ],
                },
                {
                    "h2": "曼哈顿 SEO vs Google Ads",
                    "paragraphs": [
                        "人身伤害、医美等 CPC 极高，Ads 可快速测试转化，但需专业落地页与 call tracking。SEO 靠内容深度与评价缓慢积累。",
                        "建议：网站 + 本地 SEO + 精选 practice area 内容；Ads 预算交给有 bar compliance 经验的团队（我们提供 <a href=\"/services/google-ads/\">Google Ads 代运营</a>）。",
                    ],
                },
                {
                    "h2": "常见错误",
                    "paragraphs": [
                        "用 Wix 模板堆砌「纽约最好律师」；practice area 全挤在一页；中文页是英文机翻；电话与 GBP 不一致；没有移动端快速预约。",
                        "修复优先级：NAP 统一 → 拆分 practice area 页 → 收集真实 Google 评价 → 再扩内容营销。",
                    ],
                },
            ],
            "footer_seo": "曼哈顿SEO · 曼哈顿网站设计 · 华人律所网站 · Manhattan law firm SEO · 曼哈顿诊所SEO",
        },
        "en": {
            "title": "Manhattan Law Firm & Professional Services Local SEO 2026 | 70NYC",
            "description": "SEO for Manhattan law firms, clinics, and advisors — practice area pages, GBP, bilingual structure, reviews, and Ads vs organic strategy.",
            "keywords": "Manhattan SEO, Manhattan web design, law firm website NYC, Manhattan law firm SEO, Chinese lawyer Manhattan, Midtown professional services SEO",
            "h1": "Local SEO for Manhattan Law Firms & Professional Services",
            "intro": "Manhattan Chinese law firms, immigration attorneys, clinics, med spas, and financial advisors compete in a <strong>high-trust, high-CPC</strong> search market. This guide is unique to Manhattan professionals — not Flushing restaurants or Brooklyn contractors.",
            "sections": [
                {
                    "h2": "How Manhattan clients search",
                    "paragraphs": [
                        "English: Midtown employment lawyer, Downtown immigration attorney, Chinatown accountant. Chinese: 曼哈顿 律师, 中城 诊所.",
                        "Manhattan searches emphasize specialty + district more than block-level \"near me.\" Build separate landing pages per practice area — not one generic About page.",
                    ],
                },
                {
                    "h2": "SEO site structure for firms and clinics",
                    "paragraphs": ["Help Google understand what you do:"],
                    "list": [
                        "Homepage: clear value prop, phone, booking CTA",
                        "Practice area pages: immigration, family law, PI — each with Manhattan in title/H1",
                        "Team pages: credentials, languages, education (E-E-A-T)",
                        "FAQ: process, fee ranges, consultation flow",
                        "Contact: NAP matches Google Business Profile exactly",
                        "Compliance: legal disclaimers, healthcare privacy notices",
                    ],
                },
                {
                    "h2": "Google Business Profile for professionals",
                    "paragraphs": [
                        "Choose precise categories (Law firm, Lawyer, Medical clinic). List services by practice area; add office and team photos with permission.",
                        "Reviews mentioning specific outcomes help more than generic five stars. Never buy reviews.",
                    ],
                },
                {
                    "h2": "Bilingual layout",
                    "paragraphs": [
                        "Common pattern: English-primary URLs with mirrored or /zh/ Chinese core pages; correct hreflang and canonicals.",
                        "Clients may read Chinese while partners search English — two audience entry points, not machine-translated duplicates. See <a href=\"/en/areas/manhattan/\">Manhattan web design</a>.",
                    ],
                },
                {
                    "h2": "SEO vs Google Ads in Manhattan",
                    "paragraphs": [
                        "PI and med spa keywords have extreme CPC — Ads need compliant landing pages. SEO builds slowly through depth and reviews.",
                        "Stack: website + local SEO + practice content; Ads with experienced compliance-aware management via our <a href=\"/en/services/google-ads/\">Google Ads services</a>.",
                    ],
                },
                {
                    "h2": "Common mistakes",
                    "paragraphs": [
                        "Template sites claiming \"best NYC lawyer\"; all practice areas on one page; Chinese pages as raw translations; NAP mismatches; no mobile booking.",
                        "Fix order: unify NAP → split practice pages → collect real reviews → expand content.",
                    ],
                },
            ],
            "footer_seo": "Manhattan SEO · Manhattan web design · Law firm website NYC · Manhattan professional services SEO",
        },
    },
    {
        "slug": "long-island-chinese-business-local-seo-2026",
        "date": "2026-06-20",
        "zh": {
            "title": "长岛华人企业本地 SEO 指南｜Great Neck·Nassau｜70NYC",
            "description": "长岛华人装修、美容、律所如何在 Google 获客？城镇名关键词、服务半径、GBP 与案例页——Great Neck、Manhasset、Plainview 2026 实操。",
            "keywords": "长岛SEO, 长岛网站设计, Great Neck SEO, Long Island web design, 长岛华人网站, Nassau SEO, 曼哈西特网站, 长岛Google地图",
            "h1": "长岛华人企业怎么做本地 SEO？",
            "intro": "长岛（Long Island）华人商业分布在 North Shore、Nassau、Suffolk——Great Neck、Manhasset、Plainview、Syosset 等。客户习惯<strong>开车 15–30 分钟</strong>，搜索常带城镇名：「Great Neck 装修」「Long Island kitchen remodel」。这与曼哈顿律所、法拉盛餐馆的 SEO 逻辑<strong>完全不同</strong>。",
            "sections": [
                {
                    "h2": "长岛 vs 纽约市：SEO 关键差异",
                    "paragraphs": [
                        "长岛必须强调<strong>服务半径与城镇列表</strong>，而不是单一 neighborhood。网站应有 Service Area 段落或独立城镇落地页（慎用批量模板，每页需有真实案例差异）。",
                        "GBP 类型可能是 storefront 或 service-area business——上门装修队应如实设置 coverage，避免 spam。",
                    ],
                },
                {
                    "h2": "高转化关键词示例",
                    "paragraphs": [
                        "装修：Long Island kitchen remodeling、Great Neck contractor、Nassau County bathroom renovation、长岛 厨房 改造。",
                        "美容/牙科：Manhasset facial、Long Island Invisalign、Great Neck 美甲。专业服务：Long Island estate planning、Plainview 会计。",
                        "每类业务选 3–5 个城镇 + 服务组合写进 title、H1 与 GBP，而非只优化「长岛网站设计」。",
                    ],
                },
                {
                    "h2": "案例页与服务范围页",
                    "paragraphs": [
                        "长岛高客单价行业（装修、景观、医美）靠案例说服。每个项目写清：城镇、Scope、周期，附 before/after 图与文字。",
                        "单独「服务范围」页列出 Nassau/Suffolk 具体 town，并说明是否收费上门评估——减少远距离无效线索。参见 <a href=\"/areas/long-island/\">长岛网站设计</a> 服务页。",
                    ],
                },
                {
                    "h2": "Google 地图与评价策略",
                    "paragraphs": [
                        "完工后邀请客户在 Google 留评，提及项目类型与城镇（「Great Neck 厨房改造很满意」）。回复每条评价。",
                        "照片定期更新：完工照、团队、车辆标识（如有）—— suburban 客户重视「像本地公司」的信号。",
                    ],
                },
                {
                    "h2": "网站速度与移动端",
                    "paragraphs": [
                        "长岛用户多在手机搜索路上或工地。Core Web Vitals 不合格会拖累排名与 Ads 质量分。",
                        "一键电话、表单报价、WeChat 入口放在首屏；停车/预约说明写清楚（诊所、美容尤其重要）。",
                    ],
                },
                {
                    "h2": "与 70NYC 合作的长岛方案",
                    "paragraphs": [
                        "我们服务 Great Neck 至 Suffolk 华人企业，可长岛见面或远程。典型组合：定制案例站 + 城镇 SEO + GBP 优化 + 季节性 Google Ads。",
                        "延伸阅读：<a href=\"/blog/brooklyn-contractor-local-seo-2026/\">布鲁克林承包商 SEO</a>（装修逻辑相近）；<a href=\"/services/seo/\">纽约 SEO 服务</a> 含免费初诊。",
                    ],
                },
            ],
            "footer_seo": "长岛SEO · 长岛网站设计 · Great Neck SEO · Long Island web design · 长岛华人网站",
        },
        "en": {
            "title": "Long Island Chinese Business Local SEO Guide 2026 | Great Neck · Nassau | 70NYC",
            "description": "Local SEO for Long Island Chinese businesses — town-level keywords, service radius, GBP, case studies for Great Neck, Manhasset, Plainview contractors and pros.",
            "keywords": "Long Island SEO, Long Island web design, Great Neck SEO, Nassau County SEO, Chinese business Long Island, Long Island Google Maps",
            "h1": "Local SEO for Long Island Chinese Businesses",
            "intro": "Long Island Chinese businesses span Great Neck, Manhasset, Plainview, Syosset, and across Nassau and Suffolk. Customers drive 15–30 minutes and search with <strong>town names</strong> — distinct from Manhattan law firms or Flushing restaurants.",
            "sections": [
                {
                    "h2": "How Long Island SEO differs from NYC",
                    "paragraphs": [
                        "Emphasize service radius and town lists — not a single neighborhood. Use service area sections or town pages with unique case proof, not empty templates.",
                        "GBP may be storefront or service-area — set honest coverage for traveling contractors.",
                    ],
                },
                {
                    "h2": "High-intent keyword examples",
                    "paragraphs": [
                        "Remodeling: Long Island kitchen remodeling, Great Neck contractor, Nassau bathroom renovation.",
                        "Beauty/dental: Manhasset facial, Long Island Invisalign. Professional: Great Neck estate planning.",
                        "Pick 3–5 town + service pairs for titles, H1s, and GBP — not just \"Long Island web design.\"",
                    ],
                },
                {
                    "h2": "Case studies and service area pages",
                    "paragraphs": [
                        "High-ticket LI trades need proof: town, scope, timeline, before/after with captions.",
                        "Dedicated service area pages list Nassau/Suffolk towns and consultation policies. See our <a href=\"/en/areas/long-island/\">Long Island web design</a> page.",
                    ],
                },
                {
                    "h2": "Maps and reviews",
                    "paragraphs": [
                        "Ask for reviews mentioning job type and town. Reply to all reviews.",
                        "Refresh photos: completed jobs, team, vehicle branding — suburban clients trust local signals.",
                    ],
                },
                {
                    "h2": "Mobile speed matters",
                    "paragraphs": [
                        "Many LI searches happen on phones en route. Poor Core Web Vitals hurt organic and Ads quality scores.",
                        "Click-to-call, quote forms, and WeChat above the fold; clarify parking/booking for clinics and salons.",
                    ],
                },
                {
                    "h2": "Working with 70NYC on Long Island",
                    "paragraphs": [
                        "We serve Great Neck through Suffolk with meetups or remote delivery. Typical stack: portfolio site + town SEO + GBP + seasonal Ads.",
                        "Related: <a href=\"/en/blog/brooklyn-contractor-local-seo-2026/\">Brooklyn contractor SEO</a>; <a href=\"/en/services/seo/\">NYC SEO services</a> includes a free audit checklist.",
                    ],
                },
            ],
            "footer_seo": "Long Island SEO · Long Island web design · Great Neck SEO · Nassau Suffolk local search",
        },
    },
    {
        "slug": "nyc-ai-search-local-seo-2026",
        "date": "2026-06-25",
        "zh": {
            "title": "AI 搜索时代纽约本地 SEO 指南｜ChatGPT·Google AI 概览｜70NYC",
            "description": "ChatGPT、Gemini、Google AI 概览如何引用本地商家？纽约华人企业 2026 本地 SEO + GEO 实操：结构化数据、llms.txt、GBP 与内容策略。",
            "keywords": "AI搜索优化, GEO, 生成式引擎优化, 纽约本地SEO, Google AI概览, ChatGPT本地商家, 华人企业SEO, llms.txt, 结构化数据",
            "h1": "AI 搜索时代，纽约华人企业怎么做本地 SEO？",
            "intro": "越来越多客户通过 <strong>ChatGPT、Gemini、Google AI 概览</strong> 问「法拉盛哪家装修公司好」「曼哈顿律所推荐」——而不只点传统蓝色链接。AI 仍依赖<strong>可抓取、结构清晰、权威一致</strong>的网页与 Google Business Profile。本地 SEO 没有过时，但需要加上 <strong>GEO（Generative Engine Optimization）</strong> 思维。",
            "sections": [
                {
                    "h2": "AI 搜索如何「认识」你的生意",
                    "paragraphs": [
                        "大模型与 AI 概览通常综合：官网服务页、About/Contact、博客深度内容、Google 地图评价、第三方目录（若存在且一致）。",
                        "若网站只有首页几段话、无独立服务页、NAP（名称地址电话）与 GBP 不一致，AI 很难准确引用你——会推荐信息更完整的竞争对手。",
                    ],
                },
                {
                    "h2": "2026 必做：技术基础不变",
                    "paragraphs": [
                        "本地 SEO 核心仍是：GBP 完整优化、移动端体验、Core Web Vitals、区域关键词（曼哈顿/法拉盛/布鲁克林/长岛 + 行业）、真实评价与案例页。",
                        "站内：每服务独立 URL（如 <a href=\"/services/seo/\">SEO 服务页</a>）、FAQ、BreadcrumbList 与 LocalBusiness schema。参见 <a href=\"/blog/nyc-chinese-business-website-seo-mistakes-2026/\">华人网站 SEO 常见错误</a>。",
                    ],
                },
                {
                    "h2": "GEO 新增项：让 AI 读懂实体",
                    "paragraphs": [
                        "<strong>llms.txt</strong>：在网站根目录提供实体摘要与关键 URL（本站在 <a href=\"/llms.txt\">70nyc.com/llms.txt</a>），帮助 AI 爬虫快速定位服务与区域页。",
                        "<strong>结构化数据</strong>：Organization / LocalBusiness 的 name、telephone、areaServed、knowsAbout、hasOfferCatalog；服务页用 Service schema；区域 FAQ 用 FAQPage。",
                        "<strong>清晰段落与标题</strong>：AI 偏好可直接引用的定义句，例如「70NYC 服务法拉盛餐馆的 Google 地图 SEO」——避免纯图片或 JS 隐藏核心信息。",
                    ],
                },
                {
                    "h2": "内容与 E-E-A-T：案例比口号有效",
                    "paragraphs": [
                        "「纽约最好网站公司」对 AI 与人类都无说服力。写具体：服务哪些 borough、典型客户行业、项目周期、可验证成果（流量/咨询增长区间）。",
                        "博客与区域页应互链：如 <a href=\"/blog/flushing-restaurant-google-maps-seo-2026/\">法拉盛餐馆地图 SEO</a> 链回 <a href=\"/areas/flushing/\">法拉盛服务页</a>，形成主题集群。",
                    ],
                },
                {
                    "h2": "AI 营销与 SEO 如何配合",
                    "paragraphs": [
                        "AI 客服/线索跟进（见 <a href=\"/services/ai-marketing/\">AI 智能营销</a>）解决<strong>转化</strong>；SEO/GEO 解决<strong>被找到</strong>。两者叠加：搜索与 AI 推荐带来访问，自动化系统 24h 响应微信/表单咨询。",
                        "勿用 AI 批量生成垃圾页面——Google 与 AI 系统都惩罚低质规模化内容。",
                    ],
                },
                {
                    "h2": "检查清单（可自查）",
                    "paragraphs": [
                        "☑ GBP 与网站 NAP 一致 ☑ 每服务有独立页 ☑ 至少 2–3 篇行业/区域深度文 ☑ schema 与 sitemap 正常 ☑ robots 未屏蔽 GPTBot/Google-Extended ☑ 有 llms.txt 或等效 About 摘要",
                        "需要诊断？<a href=\"/contact/\">联系 70NYC</a> 可免费初聊网站与本地搜索现状；我们服务大纽约华人企业 13+ 年。",
                    ],
                },
            ],
            "footer_seo": "AI搜索优化 · GEO · 纽约本地SEO · Google AI概览 · 华人企业SEO · ChatGPT本地推荐",
        },
        "en": {
            "title": "Local SEO in the AI Search Era NYC 2026 | ChatGPT · Google AI Overviews | 70NYC",
            "description": "How ChatGPT, Gemini, and Google AI Overviews cite local businesses — 2026 local SEO + GEO for NYC Chinese businesses: schema, llms.txt, GBP, content clusters.",
            "keywords": "AI search optimization, GEO, generative engine optimization, NYC local SEO, Google AI Overviews, ChatGPT local business, llms.txt, structured data",
            "h1": "Local SEO for NYC Businesses in the AI Search Era",
            "intro": "Customers increasingly ask <strong>ChatGPT, Gemini, and Google AI Overviews</strong> for \"best Flushing contractor\" or \"Manhattan law firm\" — not only blue links. AI still relies on <strong>crawlable, structured, consistent</strong> websites and Google Business Profile. Local SEO isn't dead; it needs <strong>GEO (Generative Engine Optimization)</strong>.",
            "sections": [
                {
                    "h2": "How AI search \"learns\" your business",
                    "paragraphs": [
                        "Models synthesize: service pages, About/Contact, blog depth, Maps reviews, third-party listings when NAP matches.",
                        "Thin homepages with no service URLs and mismatched GBP data get skipped — competitors with clearer entity signals win citations.",
                    ],
                },
                {
                    "h2": "2026 basics unchanged",
                    "paragraphs": [
                        "Local SEO core: GBP, mobile UX, Core Web Vitals, borough + industry keywords, real reviews and case studies.",
                        "On-site: dedicated URLs per service (e.g. our <a href=\"/en/services/seo/\">SEO page</a>), FAQs, BreadcrumbList and LocalBusiness schema. See <a href=\"/en/blog/nyc-chinese-business-website-seo-mistakes-2026/\">common website SEO mistakes</a>.",
                    ],
                },
                {
                    "h2": "GEO additions for AI entities",
                    "paragraphs": [
                        "<strong>llms.txt</strong>: root-level entity summary and key URLs (<a href=\"/llms.txt\">70nyc.com/llms.txt</a>) for AI crawlers.",
                        "<strong>Structured data</strong>: Organization/LocalBusiness with knowsAbout, hasOfferCatalog; Service schema on service pages; FAQPage on area FAQs.",
                        "<strong>Quotable copy</strong>: clear H2/H3 and definitional sentences AI can cite — not core info locked in images or JS-only widgets.",
                    ],
                },
                {
                    "h2": "Content & E-E-A-T",
                    "paragraphs": [
                        "\"Best NYC agency\" fails for humans and AI. Specify boroughs served, industries, timelines, plausible outcome ranges.",
                        "Interlink blogs and area pages — e.g. <a href=\"/en/blog/flushing-restaurant-google-maps-seo-2026/\">Flushing restaurant Maps SEO</a> → <a href=\"/en/areas/flushing/\">Flushing services</a>.",
                    ],
                },
                {
                    "h2": "AI marketing + SEO together",
                    "paragraphs": [
                        "AI chat and lead follow-up (<a href=\"/en/services/ai-marketing/\">AI marketing</a>) handle <strong>conversion</strong>; SEO/GEO handle <strong>discovery</strong>.",
                        "Avoid mass AI spam pages — search and AI systems penalize low-quality scale.",
                    ],
                },
                {
                    "h2": "Quick checklist",
                    "paragraphs": [
                        "☑ NAP matches GBP ☑ Service pages exist ☑ 2–3 depth articles ☑ schema + sitemap ☑ robots allow AI bots ☑ llms.txt or strong About summary",
                        "<a href=\"/en/contact/\">Contact 70NYC</a> for a free consult on your site and local visibility — 13+ years serving NYC metro businesses.",
                    ],
                },
            ],
            "footer_seo": "AI search optimization · GEO · NYC local SEO · Google AI Overviews · ChatGPT local citations",
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
        <a href="{p}/states/">{"美国各州" if lang == "zh" else "US States"}</a>
        <a href="{p}/cities/">{"重点城市" if lang == "zh" else "Key Cities"}</a>
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
    related.append((f"{p}/states/", "美国各州" if lang == "zh" else "US States", "50 states + DC"))
    related.append((f"{p}/contact/", "免费咨询" if lang == "zh" else "Contact", "24h" if lang == "en" else "24h 内回复"))
    return related


INDUSTRY_LABEL = {
    "restaurants": ("餐馆 / 外卖", "Restaurants & takeout"),
    "healthcare": ("医疗诊所", "Healthcare clinics"),
    "retail": ("零售门店", "Retail"),
    "tourism": ("旅游接待", "Tourism & hospitality"),
    "professional services": ("专业服务", "Professional services"),
    "real estate": ("房产中介", "Real estate"),
    "medical spa": ("医美 / 美容", "Med spa & beauty"),
    "contractors": ("装修承包", "Contractors"),
    "beauty": ("美容美发", "Beauty & salons"),
    "tech": ("科技 / 创业", "Tech & startups"),
    "legal": ("律师事务所", "Law firms"),
    "finance": ("金融财务", "Finance"),
    "education": ("教育培训", "Education"),
    "auto services": ("汽修服务", "Auto services"),
    "agriculture services": ("农业服务", "Agribusiness services"),
    "energy services": ("能源服务", "Energy services"),
    "manufacturing services": ("制造配套", "Manufacturing services"),
    "music business": ("音乐产业", "Music business"),
    "government contractors": ("政府承包商", "Gov contractors"),
    "oil services": ("能源油服", "Energy / oil services"),
    "ngo": ("非营利机构", "NGOs"),
}


def _industry_list(state: dict, lang: str) -> str:
    parts = []
    for key in state["industries"][:4]:
        zh, en = INDUSTRY_LABEL.get(key, (key, key))
        parts.append(zh if lang == "zh" else en)
    return "、".join(parts) if lang == "zh" else ", ".join(parts)


def state_meta(state: dict, lang: str) -> dict:
    p = prefix(lang)
    name = state["name_zh"] if lang == "zh" else state["name_en"]
    cities = state["cities_zh"] if lang == "zh" else state["cities"]
    city_str = "、".join(cities[:4]) if lang == "zh" else ", ".join(cities[:4])
    industries = _industry_list(state, lang)
    code = state["code"]
    note = state.get("note_zh" if lang == "zh" else "note_en", "")

    if lang == "zh":
        title = f"{name}网站设计与SEO｜华人企业远程服务｜70NYC"
        description = (
            f"70NYC 从纽约为{name}华人企业提供远程网站设计、本地 SEO、Google Ads 与 AI 营销。"
            f"覆盖{city_str}等地，流程与纽约客户一致。"
        )
        keywords = (
            f"{name}网站设计, {name}SEO, {name}华人网站, {code} web design, "
            f"{cities[0]}网站设计, {name}Google Ads, 华人企业远程营销"
        )
        lead = (
            f"人在{name}、客户在本地或全美——我们通过视频会议与微信远程交付网站、SEO 与广告。"
            f"重点城市包括 <strong>{city_str}</strong>。"
            f"常见行业：{industries}。"
            + (f" {note}" if note else "")
        )
        topics = [
            (
                f"{name}远程合作怎么做",
                f"Kickoff 用 Zoom；日常微信/邮件同步。设计稿、上线验收视频过稿——与曼哈顿、法拉盛本地客户相同阶段标准。时区以美东为主，可按{name}客户时间安排会议。",
            ),
            (
                "本地 SEO 与 Google 地图",
                f"针对「{cities[0]} + 行业」类关键词优化网站结构、GBP 与评价策略；多城服务范围写清服务半径，避免空模板堆砌。详见 <a href=\"/services/seo/\">SEO 服务</a>。",
            ),
            (
                "适合哪些生意",
                f"{name}华人{industries}等——需要中英双语官网、新店上线、或已有站但搜索曝光不足时，可打包网站 + SEO + <a href=\"/services/google-ads/\">Google Ads</a>。",
            ),
            (
                "与纽约总部的关系",
                f"签约、设计、开发、广告账户均由纽约团队交付；不因远程降低质量。大纽约面谈见 <a href=\"/areas/\">服务区域</a>；其他州见本页与 <a href=\"/nationwide/\">全美远程总览</a>。",
            ),
        ]
        faq = [
            {
                "q": f"人不在纽约，{name}能做网站和 SEO 吗？",
                "a": f"可以。我们通过远程流程服务{name}客户，交付物、验收节点与报价逻辑与纽约本地一致。",
            },
            {
                "q": f"{name}本地 SEO 需要见面吗？",
                "a": "多数项目可全程远程。若需拍摄门店或面谈，可协调当地合作方或您自行提供素材。",
            },
            {
                "q": "多久能上线？",
                "a": "标准企业站通常数周内分阶段交付；含 SEO / Ads 的方案按月迭代。具体以需求评估为准。",
            },
        ]
        return {
            "title": title,
            "description": description,
            "keywords": keywords,
            "breadcrumb": name,
            "eyebrow": f"{name} · {code} · 远程交付",
            "h1": f"{name}华人企业<br><span>网站设计、SEO 与数字营销</span>",
            "lead": lead,
            "topics": topics,
            "highlights": [
                "响应式中英网站",
                f"{cities[0]}本地 SEO",
                "Google Ads 投放",
                "AI 线索跟进",
                "餐馆 / 门店站",
                "按月透明报告",
            ],
            "highlights_title": "常选服务组合",
            "label": f"70NYC · {name}",
            "section_h2": f"服务{name}客户时我们做什么",
            "footer_seo": f"{name}网站设计 · {name}SEO · {city_str} · 华人企业远程营销 · 70NYC",
            "faq": faq,
            "tags": [
                f"{name}网站设计",
                f"{name}SEO",
                f"{cities[0]}网站",
                "华人企业",
                "远程SEO",
                "Google Ads",
            ],
            "cta_primary": ("获取本州方案", f"{p}/contact/"),
            "cta_ghost": ("全美远程总览", f"{p}/nationwide/"),
            "stats": [
                ("远程", "全州可服务"),
                ("13+", "年经验"),
                ("中英", "双语"),
                ("24h", "内回复"),
            ],
        }

    title = f"{name} Web Design & SEO for Chinese Businesses | Remote | 70NYC"
    description = (
        f"70NYC delivers remote web design, local SEO, Google Ads, and AI marketing for Chinese-owned "
        f"businesses in {name} — covering {city_str} and statewide."
    )
    keywords = (
        f"{name} web design, {name} SEO, {code} Chinese business website, "
        f"{cities[0]} web design, {name} Google Ads, remote digital marketing"
    )
    lead = (
        f"Based in New York, we serve {name} clients remotely via video and WeChat. "
        f"Key metros: <strong>{city_str}</strong>. Common industries: {industries}."
        + (f" {note}" if note else "")
    )
    topics = [
        (
            f"How remote work in {name} works",
            f"Kickoff on Zoom; WeChat/email day-to-day. Design and launch reviews on video — same milestones as NYC clients. Meetings scheduled around {name} time zones when needed.",
        ),
        (
            "Local SEO & Google Maps",
            f'We structure pages for "{cities[0]} + service" intent, GBP, and honest service-area coverage — no empty template farms. See our <a href="/en/services/seo/">SEO services</a>.',
        ),
        (
            "Who it's for",
            f"{name} Chinese {industries} and more — bilingual sites, new openings, or low search visibility. Pair with <a href=\"/en/services/google-ads/\">Google Ads</a> when you need faster leads.",
        ),
        (
            "NYC HQ delivery",
            f"Contracts, design, build, and ad accounts run from our New York team. Metro NYC meetings: <a href=\"/en/areas/\">areas</a>. Other states: this page and <a href=\"/en/nationwide/\">nationwide remote</a>.",
        ),
    ]
    faq = [
        {
            "q": f"Can you build sites and SEO for {name} if I'm not in NYC?",
            "a": f"Yes. Remote delivery for {name} uses the same checkpoints and quality bar as local NYC projects.",
        },
        {
            "q": f"Do {name} local SEO projects require on-site visits?",
            "a": "Most work is remote. For photos or walkthroughs, we coordinate local help or use assets you provide.",
        },
        {
            "q": "Typical timeline?",
            "a": "Standard business sites launch in weeks with phased milestones; SEO/Ads continue monthly. Scope depends on your brief.",
        },
    ]
    return {
        "title": title,
        "description": description,
        "keywords": keywords,
        "breadcrumb": name,
        "eyebrow": f"{name} · {code} · Remote",
        "h1": f"{name} Chinese Businesses<br><span>Web Design, SEO & Digital Marketing</span>",
        "lead": lead,
        "topics": topics,
        "highlights": [
            "Bilingual responsive sites",
            f"{cities[0]} local SEO",
            "Google Ads",
            "AI lead follow-up",
            "Restaurant / storefront sites",
            "Monthly reporting",
        ],
        "highlights_title": "Popular stacks",
        "label": f"70NYC · {name}",
        "section_h2": f"What we deliver for {name} clients",
        "footer_seo": f"{name} web design · {name} SEO · {city_str} · Chinese business remote marketing · 70NYC",
        "faq": faq,
        "tags": [
            f"{name} web design",
            f"{name} SEO",
            f"{cities[0]} website",
            "Chinese business",
            "Remote SEO",
            "Google Ads",
        ],
        "cta_primary": ("Get State Proposal", f"{p}/contact/"),
        "cta_ghost": ("Nationwide Overview", f"{p}/nationwide/"),
        "stats": [
            ("Remote", "Statewide"),
            ("13+", "Years"),
            ("Bilingual", "EN / 中文"),
            ("24h", "Reply"),
        ],
    }


def state_related(lang: str, current_slug: str) -> list[tuple[str, str, str]]:
    p = prefix(lang)
    child_cities = [c for c in US_CITIES if c["state_slug"] == current_slug][:3]
    related = [
        (
            f"{p}/cities/{c['slug']}/",
            c["name_zh"] if lang == "zh" else c["name_en"],
            c["code"],
        )
        for c in child_cities
    ]
    idx = next(i for i, s in enumerate(US_STATES) if s["slug"] == current_slug)
    neighbors = []
    for offset in (1, 2, -1):
        n = US_STATES[(idx + offset) % len(US_STATES)]
        if n["slug"] != current_slug and n["slug"] not in {x["slug"] for x in neighbors}:
            neighbors.append(n)
        if len(neighbors) >= 2:
            break
    if len(related) < 2:
        related.extend(
            (
                f"{p}/states/{n['slug']}/",
                n["name_zh"] if lang == "zh" else n["name_en"],
                n["code"],
            )
            for n in neighbors
        )
    related.append((f"{p}/cities/", "重点城市" if lang == "zh" else "Key Cities", "Metros"))
    related.append((f"{p}/states/", "全部州" if lang == "zh" else "All States", "50 + DC"))
    related.append((f"{p}/nationwide/", "全美远程" if lang == "zh" else "Nationwide", "Overview"))
    related.append((f"{p}/contact/", "免费咨询" if lang == "zh" else "Contact", "24h"))
    return related[:6]


def city_meta(city: dict, lang: str) -> dict:
    p = prefix(lang)
    name = city["name_zh"] if lang == "zh" else city["name_en"]
    state_name = city["state_zh"] if lang == "zh" else city["state_en"]
    hoods = city["neighborhoods_zh"] if lang == "zh" else city["neighborhoods_en"]
    hood_str = "、".join(hoods[:4]) if lang == "zh" else ", ".join(hoods[:4])
    industries = _industry_list(city, lang)
    angle = city["angle_zh"] if lang == "zh" else city["angle_en"]
    code = city["code"]
    state_path = f"{p}/states/{city['state_slug']}/"

    if lang == "zh":
        return {
            "title": f"{name}网站设计与SEO｜华人企业远程服务｜{state_name}｜70NYC",
            "description": (
                f"70NYC 从纽约为{name}（{state_name}）华人企业提供远程网站设计、本地 SEO、Google Ads。"
                f"覆盖{hood_str}等区域。{angle}"
            ),
            "keywords": (
                f"{name}网站设计, {name}SEO, {name}华人网站, {hoods[0]}网站设计, "
                f"{state_name}SEO, {code} web design, 华人企业远程营销"
            ),
            "breadcrumb": name,
            "eyebrow": f"{name} · {state_name} · 远程",
            "h1": f"{name}华人企业<br><span>网站设计、本地 SEO 与数字营销</span>",
            "lead": (
                f"服务 <strong>{name}</strong>（{state_name}）华人餐馆、美容、房产、医疗与专业服务。"
                f"重点区域：{hood_str}。{angle} "
                f"远程交付标准与纽约本地一致——详见 <a href=\"{state_path}\">{state_name}服务页</a>。"
            ),
            "topics": [
                (
                    f"{name}本地搜索怎么做",
                    f"用「{hoods[0]} / {name} + 行业」组合写 title、H1 与 GBP；服务多区时列出真实覆盖（如{hood_str}），避免空模板。详见 <a href=\"/services/seo/\">SEO 服务</a>。",
                ),
                (
                    "网站与转化",
                    f"中英双语、一键电话/微信、移动端速度与案例页——对{name}竞争市场尤其重要。可与 <a href=\"/services/web-design/\">网站设计</a>、<a href=\"/services/ai-marketing/\">AI 营销</a> 同步上线。",
                ),
                (
                    "适合行业",
                    f"{name}常见：{industries}。新店开业可用 Google Ads 快速获客，SEO 做长期资产。",
                ),
                (
                    "远程怎么合作",
                    f"Zoom kickoff、微信日常、分阶段验收。签约与交付由纽约团队完成；大纽约面谈见 <a href=\"/areas/\">服务区域</a>。",
                ),
            ],
            "highlights": [
                f"{name}本地 SEO",
                "中英双语网站",
                "Google 地图 / GBP",
                "Google Ads",
                "AI 线索跟进",
                "按月报告",
            ],
            "highlights_title": "常选组合",
            "label": f"70NYC · {name}",
            "section_h2": f"服务{name}客户时的重点",
            "footer_seo": f"{name}网站设计 · {name}SEO · {hood_str} · {state_name}华人企业 · 70NYC",
            "faq": [
                {
                    "q": f"{name}不在纽约，能做网站和 SEO 吗？",
                    "a": f"可以。我们为{name}及周边（{hood_str}）华人企业提供远程交付，流程与报价逻辑与纽约客户一致。",
                },
                {
                    "q": f"{name}本地 SEO 关键词怎么选？",
                    "a": f"优先「{name}/{hoods[0]} + 行业」高意向词，并保持 NAP 与 Google Business Profile 一致。{angle}",
                },
                {
                    "q": "需要多久？",
                    "a": "标准企业站通常数周分阶段上线；SEO 与广告按月优化。以需求评估为准。",
                },
            ],
            "tags": [
                f"{name}网站设计",
                f"{name}SEO",
                hoods[0],
                state_name,
                "华人企业",
                "远程SEO",
            ],
            "cta_primary": ("获取本城方案", f"{p}/contact/"),
            "cta_ghost": (state_name, state_path),
            "stats": [
                ("远程", "本城可服务"),
                ("13+", "年经验"),
                ("中英", "双语"),
                ("24h", "内回复"),
            ],
        }

    return {
        "title": f"{name} Web Design & SEO for Chinese Businesses | {city['state_en']} | 70NYC",
        "description": (
            f"70NYC delivers remote web design, local SEO, and Google Ads for Chinese-owned businesses "
            f"in {name}, {city['state_en']} — covering {hood_str}. {angle}"
        ),
        "keywords": (
            f"{name} web design, {name} SEO, {hoods[0]} website, Chinese business {name}, "
            f"{code} digital marketing, remote SEO"
        ),
        "breadcrumb": name,
        "eyebrow": f"{name} · {city['state_en']} · Remote",
        "h1": f"{name} Chinese Businesses<br><span>Web Design, Local SEO & Marketing</span>",
        "lead": (
            f"Serving Chinese restaurants, salons, real estate, clinics, and professionals in "
            f"<strong>{name}</strong> ({city['state_en']}). Focus areas: {hood_str}. {angle} "
            f"Same delivery bar as NYC — see our <a href=\"{state_path}\">{city['state_en']} page</a>."
        ),
        "topics": [
            (
                f"Local search in {name}",
                f'Optimize titles, H1s, and GBP for "{hoods[0]} / {name} + service" intent; list real coverage ({hood_str}). See <a href="/en/services/seo/">SEO services</a>.',
            ),
            (
                "Website & conversion",
                f"Bilingual UX, click-to-call/WeChat, mobile speed, and case proof matter in {name}. Pair with <a href=\"/en/services/web-design/\">web design</a> and <a href=\"/en/services/ai-marketing/\">AI marketing</a>.",
            ),
            (
                "Industries we see most",
                f"{industries}. Use Ads for launch velocity; SEO for compounding demand.",
            ),
            (
                "How remote delivery works",
                f"Zoom kickoff, WeChat day-to-day, phased acceptance — NYC team. Metro NYC meetings: <a href=\"/en/areas/\">areas</a>.",
            ),
        ],
        "highlights": [
            f"{name} local SEO",
            "Bilingual websites",
            "Google Maps / GBP",
            "Google Ads",
            "AI lead follow-up",
            "Monthly reports",
        ],
        "highlights_title": "Popular stacks",
        "label": f"70NYC · {name}",
        "section_h2": f"What matters for {name} clients",
        "footer_seo": f"{name} web design · {name} SEO · {hood_str} · {city['state_en']} Chinese business · 70NYC",
        "faq": [
            {
                "q": f"Can you serve {name} remotely from NYC?",
                "a": f"Yes. We deliver for {name} and nearby areas ({hood_str}) with the same checkpoints as local NYC projects.",
            },
            {
                "q": f"How do you pick {name} SEO keywords?",
                "a": f'Prioritize "{name}/{hoods[0]} + industry" intent and keep NAP aligned with GBP. {angle}',
            },
            {
                "q": "Typical timeline?",
                "a": "Business sites usually launch in weeks with phases; SEO/Ads continue monthly. Scope depends on your brief.",
            },
        ],
        "tags": [
            f"{name} web design",
            f"{name} SEO",
            hoods[0],
            city["state_en"],
            "Chinese business",
            "Remote SEO",
        ],
        "cta_primary": ("Get City Proposal", f"{p}/contact/"),
        "cta_ghost": (city["state_en"], state_path),
        "stats": [
            ("Remote", "This metro"),
            ("13+", "Years"),
            ("Bilingual", "EN / 中文"),
            ("24h", "Reply"),
        ],
    }


def city_related(lang: str, current_slug: str) -> list[tuple[str, str, str]]:
    p = prefix(lang)
    city = next(c for c in US_CITIES if c["slug"] == current_slug)
    siblings = [c for c in US_CITIES if c["state_slug"] == city["state_slug"] and c["slug"] != current_slug][:2]
    related = [
        (
            f"{p}/cities/{c['slug']}/",
            c["name_zh"] if lang == "zh" else c["name_en"],
            c["code"],
        )
        for c in siblings
    ]
    related.append(
        (
            f"{p}/states/{city['state_slug']}/",
            city["state_zh"] if lang == "zh" else city["state_en"],
            "State",
        )
    )
    related.append((f"{p}/cities/", "全部重点城市" if lang == "zh" else "All Key Cities", "Hub"))
    related.append((f"{p}/contact/", "免费咨询" if lang == "zh" else "Contact", "24h"))
    return related


def generate_cities() -> list[str]:
    urls: list[str] = []
    for lang in ("zh", "en"):
        p = prefix(lang)
        hub_path = f"{p}/cities/"
        if lang == "zh":
            hub = {
                "title": "美国重点城市网站设计与SEO｜洛杉矶·休斯顿·迈阿密·波士顿·西雅图｜70NYC",
                "description": "70NYC 为加州、德州、佛州、宾州、波士顿、西雅图等华人密集城市提供远程网站设计与本地 SEO。按城市查看社区与关键词策略。",
                "breadcrumb": "重点城市",
                "eyebrow": "Priority Metros · 华人市场",
                "h1": "华人密集城市<br><span>网站设计与本地 SEO</span>",
                "lead": "优先覆盖洛杉矶、湾区、尔湾、休斯顿、达拉斯、迈阿密、奥兰多、费城、波士顿、西雅图、贝尔维尤等市场——比州页更细的社区与搜索策略。",
                "section_h2": "选择您的城市",
                "intro": "以下为重点华人市场城市页；各州总览见美国各州页面。",
            }
        else:
            hub = {
                "title": "US City Web Design & SEO | LA · Houston · Miami · Boston · Seattle | 70NYC",
                "description": "Remote web design and local SEO for Chinese-owned businesses in California, Texas, Florida, Pennsylvania, Boston, Seattle, and more priority metros.",
                "breadcrumb": "Key Cities",
                "eyebrow": "Priority Metros · Chinese markets",
                "h1": "Chinese Business Metros<br><span>Web Design & Local SEO</span>",
                "lead": "Priority coverage for Los Angeles, Bay Area, Irvine, Houston, Dallas, Miami, Orlando, Philadelphia, Boston, Seattle, Bellevue — deeper neighborhood and keyword strategy than state pages.",
                "section_h2": "Choose your city",
                "intro": "Priority Chinese-market city pages; see US States for statewide overviews.",
            }
        schema = breadcrumb_schema(lang, [
            ("首页" if lang == "zh" else "Home", f"{DOMAIN}/" if lang == "zh" else f"{DOMAIN}/en/"),
            (hub["breadcrumb"], f"{DOMAIN}{hub_path}"),
        ])
        # Group cards by state for readability
        by_state: dict[str, list] = {}
        for c in US_CITIES:
            by_state.setdefault(c["state_slug"], []).append(c)
        sections = []
        for state_slug, cities in by_state.items():
            st = next(s for s in US_STATES if s["slug"] == state_slug)
            st_label = st["name_zh"] if lang == "zh" else st["name_en"]
            cards = []
            for c in cities:
                label = c["name_zh"] if lang == "zh" else c["name_en"]
                hood = (c["neighborhoods_zh"] if lang == "zh" else c["neighborhoods_en"])[0]
                cards.append(
                    f'          <a class="page-seo-related-card" href="{p}/cities/{c["slug"]}/">\n'
                    f'            <span class="page-seo-related-arrow" aria-hidden="true">→</span>\n'
                    f"            <b>{label}</b>\n"
                    f"            <span>{c['code']} · {hood}</span>\n"
                    f"          </a>"
                )
            sections.append(
                f'        <h3 style="margin:28px 0 12px;font-size:1.05rem">'
                f'<a href="{p}/states/{state_slug}/">{st_label}</a></h3>\n'
                f'        <div class="page-seo-related-grid">\n{chr(10).join(cards)}\n        </div>'
            )
        hub_main = (
            hero_html(lang, {**hub, "tags": [], "stats": []}, [(hub["breadcrumb"], None)], theme_idx=2, show_actions=False)
            + f"""    <section class="page-seo-supplement">
      <div class="page-seo-supplement-inner">
        <div class="page-seo-supplement-head">
          <span class="label">70NYC Cities</span>
          <h2>{hub['section_h2']}</h2>
          <p style="margin-top:12px;color:var(--text-muted)">{hub['intro']}</p>
        </div>
{chr(10).join(sections)}
      </div>
    </section>
"""
            + related_html(
                lang,
                [
                    (f"{p}/states/", "美国各州" if lang == "zh" else "US States", "50+DC"),
                    (f"{p}/nationwide/", "全美远程" if lang == "zh" else "Nationwide", ""),
                    (f"{p}/contact/", "联系" if lang == "zh" else "Contact", ""),
                ],
            )
        )
        footer = (
            "洛杉矶 · 旧金山 · 尔湾 · 休斯顿 · 达拉斯 · 迈阿密 · 费城 · 波士顿 · 西雅图 · 华人企业SEO"
            if lang == "zh"
            else "Los Angeles · SF Bay · Irvine · Houston · Dallas · Miami · Philadelphia · Boston · Seattle · Chinese business SEO"
        )
        out = ROOT / "cities" / "index.html" if lang == "zh" else ROOT / "en" / "cities" / "index.html"
        write_page(out, assemble_page(lang, {**hub, "keywords": ""}, hub_path, hub_main, schema, footer))
        urls.append(f"{DOMAIN}{hub_path}")

    for idx, city in enumerate(US_CITIES):
        for lang in ("zh", "en"):
            meta = city_meta(city, lang)
            p = prefix(lang)
            path = f"{p}/cities/{city['slug']}/"
            crumbs = [
                ("重点城市" if lang == "zh" else "Key Cities", f"{p}/cities/"),
                (meta["breadcrumb"], None),
            ]
            schema = breadcrumb_schema(lang, [
                ("首页" if lang == "zh" else "Home", f"{DOMAIN}/" if lang == "zh" else f"{DOMAIN}/en/"),
                ("重点城市" if lang == "zh" else "Key Cities", f"{DOMAIN}{p}/cities/"),
                (meta["breadcrumb"], f"{DOMAIN}{path}"),
            ])
            schema += "\n" + local_business_schema(
                meta["title"].split("｜")[0] if lang == "zh" else meta["title"].split("|")[0].strip(),
                meta["description"],
                city["name_en"],
            )
            schema += "\n" + faq_page_schema(meta["faq"])
            faq_block = area_faq_html(lang, meta["faq"], meta["breadcrumb"]) + "\n"
            main = (
                hero_html(lang, meta, crumbs, theme_idx=idx)
                + "\n"
                + supplement_html(lang, meta)
                + "\n"
                + faq_block
                + service_grid_html(lang)
                + "\n"
                + related_html(lang, city_related(lang, city["slug"]))
            )
            out = (
                ROOT / "cities" / city["slug"] / "index.html"
                if lang == "zh"
                else ROOT / "en" / "cities" / city["slug"] / "index.html"
            )
            write_page(out, assemble_page(lang, meta, path, main, schema, meta["footer_seo"]))
            urls.append(f"{DOMAIN}{path}")
    return urls


def generate_states() -> list[str]:
    urls: list[str] = []
    for lang in ("zh", "en"):
        p = prefix(lang)
        hub_path = f"{p}/states/"
        if lang == "zh":
            hub = {
                "title": "美国各州网站设计与SEO｜50州+华盛顿特区远程服务｜70NYC",
                "description": "70NYC 从纽约为美国 50 个州及华盛顿特区华人企业提供远程网站设计、本地 SEO、Google Ads 与数字营销。按州查看服务说明与重点城市。",
                "breadcrumb": "美国各州",
                "eyebrow": "50 States + DC · 远程交付",
                "h1": "覆盖美国各州<br><span>华人企业远程网站与 SEO</span>",
                "lead": "从加州、德州、佛州到华盛顿州——选择您所在的州，了解远程合作方式、重点华人城市与本地搜索策略。大纽约面谈请见服务区域页。",
                "section_h2": "选择您的州 / 特区",
                "intro": "以下共 51 个落地页（50 州 + 华盛顿特区）。内容按州定制关键词与城市，交付团队仍为纽约 70NYC。",
            }
        else:
            hub = {
                "title": "US State Web Design & SEO | 50 States + DC Remote | 70NYC",
                "description": "70NYC serves Chinese-owned businesses in all 50 US states and Washington, D.C. with remote web design, local SEO, Google Ads, and digital marketing from New York.",
                "breadcrumb": "US States",
                "eyebrow": "50 States + DC · Remote",
                "h1": "Web Design & SEO<br><span>Across Every US State</span>",
                "lead": "From California and Texas to Florida and Washington — pick your state for remote delivery details, key Chinese metros, and local search notes. NYC in-person: see our area pages.",
                "section_h2": "Choose your state / district",
                "intro": "51 landing pages (50 states + D.C.), each with state-specific cities and keywords — delivered by the same NYC 70NYC team.",
            }
        schema = breadcrumb_schema(lang, [
            ("首页" if lang == "zh" else "Home", f"{DOMAIN}/" if lang == "zh" else f"{DOMAIN}/en/"),
            (hub["breadcrumb"], f"{DOMAIN}{hub_path}"),
        ])
        cards = []
        for st in US_STATES:
            label = st["name_zh"] if lang == "zh" else st["name_en"]
            cities = st["cities_zh"] if lang == "zh" else st["cities"]
            span = f"{st['code']} · {cities[0]}"
            cards.append(
                f'          <a class="page-seo-related-card" href="{p}/states/{st["slug"]}/">\n'
                f'            <span class="page-seo-related-arrow" aria-hidden="true">→</span>\n'
                f"            <b>{label}</b>\n"
                f"            <span>{span}</span>\n"
                f"          </a>"
            )
        hub_main = (
            hero_html(lang, {**hub, "tags": [], "stats": []}, [(hub["breadcrumb"], None)], theme_idx=1, show_actions=False)
            + f"""    <section class="page-seo-supplement">
      <div class="page-seo-supplement-inner">
        <div class="page-seo-supplement-head">
          <span class="label">70NYC States</span>
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
                    (f"{p}/nationwide/", "全美远程" if lang == "zh" else "Nationwide", "Overview"),
                    (f"{p}/cities/", "重点城市" if lang == "zh" else "Key Cities", "Metros"),
                    (f"{p}/areas/", "纽约区域" if lang == "zh" else "NYC Areas", "Metro"),
                    (f"{p}/contact/", "联系" if lang == "zh" else "Contact", ""),
                ],
                "更多" if lang == "zh" else "More",
            )
        )
        footer = (
            "美国50州+特区 · 远程网站设计 · SEO · Google Ads · 华人企业"
            if lang == "zh"
            else "50 US states + DC · remote web design · SEO · Google Ads · Chinese businesses"
        )
        out = ROOT / "states" / "index.html" if lang == "zh" else ROOT / "en" / "states" / "index.html"
        write_page(out, assemble_page(lang, {**hub, "keywords": ""}, hub_path, hub_main, schema, footer))
        urls.append(f"{DOMAIN}{hub_path}")

    for idx, state in enumerate(US_STATES):
        for lang in ("zh", "en"):
            meta = state_meta(state, lang)
            p = prefix(lang)
            path = f"{p}/states/{state['slug']}/"
            crumbs = [
                ("美国各州" if lang == "zh" else "US States", f"{p}/states/"),
                (meta["breadcrumb"], None),
            ]
            schema = breadcrumb_schema(lang, [
                ("首页" if lang == "zh" else "Home", f"{DOMAIN}/" if lang == "zh" else f"{DOMAIN}/en/"),
                ("美国各州" if lang == "zh" else "US States", f"{DOMAIN}{p}/states/"),
                (meta["breadcrumb"], f"{DOMAIN}{path}"),
            ])
            schema += "\n" + local_business_schema(
                meta["title"].split("｜")[0] if lang == "zh" else meta["title"].split("|")[0].strip(),
                meta["description"],
                state["name_en"],
            )
            if meta.get("faq"):
                schema += "\n" + faq_page_schema(meta["faq"])
            faq_block = area_faq_html(lang, meta["faq"], meta["breadcrumb"]) + "\n" if meta.get("faq") else ""
            child_cities = [c for c in US_CITIES if c["state_slug"] == state["slug"]]
            cities_block = ""
            if child_cities:
                city_cards = []
                for c in child_cities:
                    label = c["name_zh"] if lang == "zh" else c["name_en"]
                    hood = (c["neighborhoods_zh"] if lang == "zh" else c["neighborhoods_en"])[0]
                    city_cards.append(
                        f'          <a class="page-seo-related-card" href="{p}/cities/{c["slug"]}/">\n'
                        f'            <span class="page-seo-related-arrow" aria-hidden="true">→</span>\n'
                        f"            <b>{label}</b>\n"
                        f"            <span>{hood}</span>\n"
                        f"          </a>"
                    )
                h2 = "本州重点城市" if lang == "zh" else "Priority cities in this state"
                cities_block = f"""    <section class="page-seo-supplement" aria-label="{h2}">
      <div class="page-seo-supplement-inner">
        <div class="page-seo-supplement-head">
          <span class="label">Cities</span>
          <h2>{h2}</h2>
        </div>
        <div class="page-seo-related-grid">
{chr(10).join(city_cards)}
        </div>
      </div>
    </section>
"""
            main = (
                hero_html(lang, meta, crumbs, theme_idx=idx)
                + "\n"
                + supplement_html(lang, meta)
                + "\n"
                + faq_block
                + cities_block
                + service_grid_html(lang)
                + "\n"
                + related_html(lang, state_related(lang, state["slug"]))
            )
            out = (
                ROOT / "states" / state["slug"] / "index.html"
                if lang == "zh"
                else ROOT / "en" / "states" / state["slug"] / "index.html"
            )
            write_page(out, assemble_page(lang, meta, path, main, schema, meta["footer_seo"]))
            urls.append(f"{DOMAIN}{path}")
    return urls


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
                    (f"{p}/states/", "美国各州" if lang == "zh" else "US States", "50+DC"),
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
    if target in ("all", "states"):
        paths.append("/states/")
        paths.extend(f"/states/{s['slug']}/" for s in US_STATES)
    if target in ("all", "cities"):
        paths.append("/cities/")
        paths.extend(f"/cities/{c['slug']}/" for c in US_CITIES)
    if target in ("all", "blog"):
        paths.append("/blog/")
        paths.extend(f"/blog/{p['slug']}/" for p in BLOG_POSTS)
    if target in ("all", "sitemap"):
        paths.extend(STATIC_SITEMAP_PATHS)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate 70NYC SEO landing pages")
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        choices=["all", "nationwide", "areas", "states", "cities", "blog", "sitemap"],
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
    if args.target in ("all", "states"):
        urls.extend(generate_states())
    if args.target in ("all", "cities"):
        urls.extend(generate_cities())
    if args.target in ("all", "blog"):
        urls.extend(generate_blog())

    update_sitemap(collect_paths_for_sitemap(args.target if args.target != "all" else "all"))
    print(f"\nDone — {len(urls)} HTML file(s) written.")


if __name__ == "__main__":
    main()
