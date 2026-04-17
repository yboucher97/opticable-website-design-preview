"""Generator entrypoint.

`sitegen_data.py` holds the large shared configuration and content layer.
This file keeps the build/render pipeline and write steps.
"""

from sitegen_data import *
from sitegen_media import (
    blog_social_image_url,
    copy_static_assets,
    export_blog_social_images,
    export_home_images,
    remove_legacy_root_build,
    reset_deploy_dir,
)

def normalize_output_content(content):
    return content.strip() + '\n'


def deploy_path_for_url(url):
    if url == '/':
        return DEPLOY_ROOT / 'index.html'
    return DEPLOY_ROOT / url.strip('/') / 'index.html'


def load_previous_page_contents():
    pages = {}
    if not DEPLOY_ROOT.exists():
        return pages
    for path in DEPLOY_ROOT.rglob('index.html'):
        rel = path.relative_to(DEPLOY_ROOT).as_posix()
        url = '/' if rel == 'index.html' else '/' + rel.removesuffix('index.html')
        pages[url] = normalize_output_content(path.read_text(encoding='utf-8'))
    return pages


def load_previous_sitemap_lastmods():
    sitemap_path = DEPLOY_ROOT / 'sitemap.xml'
    if not sitemap_path.exists():
        return {}
    try:
        root_node = ET.fromstring(sitemap_path.read_text(encoding='utf-8'))
    except ET.ParseError:
        return {}
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    lastmods = {}
    for url_node in root_node.findall('sm:url', ns):
        loc_node = url_node.find('sm:loc', ns)
        lastmod_node = url_node.find('sm:lastmod', ns)
        if loc_node is None or lastmod_node is None or not loc_node.text or not lastmod_node.text:
            continue
        lastmods[loc_node.text] = lastmod_node.text
    return lastmods


BUILD_DATE = date.today().isoformat()
PREVIOUS_PAGE_CONTENTS = load_previous_page_contents()
PREVIOUS_SITEMAP_LASTMODS = load_previous_sitemap_lastmods()
GENERATED_PAGE_LASTMODS = {}


def write_url(url, content):
    path = deploy_path_for_url(url)
    normalized = normalize_output_content(content)
    page_url = absolute_url(url)
    GENERATED_PAGE_LASTMODS[page_url] = (
        BUILD_DATE
        if PREVIOUS_PAGE_CONTENTS.get(url) != normalized
        else PREVIOUS_SITEMAP_LASTMODS.get(page_url, BUILD_DATE)
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(normalized, encoding='utf-8')


def esc(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'))


def absolute_url(path):
    if path.startswith(('http://', 'https://')):
        return path
    if path == '/':
        return SITE_URL + '/'
    return f'{SITE_URL}{path}'


def effective_robots_value(robots):
    if not FORCE_NOINDEX:
        return robots
    return 'noindex, nofollow, noarchive'


def promo_publicly_indexable():
    return not FORCE_NOINDEX and PROMO_ACTIVE


def asset_mime_type(url):
    path = url.split('?', 1)[0].lower()
    if path.endswith('.png'):
        return 'image/png'
    if path.endswith('.jpg') or path.endswith('.jpeg'):
        return 'image/jpeg'
    if path.endswith('.webp'):
        return 'image/webp'
    if path.endswith('.avif'):
        return 'image/avif'
    return 'image/png'


def image_dimensions_for_url(url):
    return IMAGE_DIMENSIONS_BY_URL.get(url, (OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT))


def image_meta_for_url(url, alt=''):
    width, height = image_dimensions_for_url(url)
    return {
        'url': absolute_url(url),
        'width': width,
        'height': height,
        'mime_type': asset_mime_type(url),
        'alt': alt or 'Opticable preview image',
    }


def iso_datetime_for_date(value, hour=9):
    parsed = date.fromisoformat(value)
    return datetime.combine(parsed, time(hour, 0), tzinfo=SITE_TIMEZONE).isoformat()


def language_tag(lang):
    return T[lang]['locale'].replace('_', '-')


def default_route(page_key):
    return routes['fr'][page_key]


def logo_img(context):
    src = LOGO_UI_WHITE_URL if context in {'header', 'footer', 'gateway'} else LOGO_UI_URL
    display_src = RESPONSIVE_IMAGE_DEFAULT_SRC.get(src, src)
    display_sizes = '(min-width: 1200px) 240px, (min-width: 768px) 200px, 160px'
    attrs = [
        f'src="{display_src}"',
        'alt="Opticable logo"',
        f'width="{LOGO_UI_WIDTH}"',
        f'height="{LOGO_UI_HEIGHT}"',
        'decoding="async"',
    ]
    responsive_sources = RESPONSIVE_IMAGE_SOURCES.get(src, [])
    if responsive_sources:
        srcset_value = ', '.join(f'{url} {variant_width}w' for url, variant_width in responsive_sources)
        attrs.append(f'srcset="{esc(srcset_value)}"')
        attrs.append(f'sizes="{display_sizes}"')
    if context == 'footer':
        attrs.append('loading="lazy"')
    else:
        attrs.append('loading="eager"')
    img_html = f'<img {" ".join(attrs)} />'
    picture_sources = RESPONSIVE_IMAGE_FORMAT_SOURCES.get(src, {})
    if picture_sources:
        source_tags = []
        for mime_type, variants in picture_sources.items():
            srcset_value = ', '.join(f'{url} {variant_width}w' for url, variant_width in variants)
            source_tags.append(
                f'<source type="{mime_type}" srcset="{esc(srcset_value)}" sizes="{esc(display_sizes)}" />'
            )
        return f'<picture>{"".join(source_tags)}{img_html}</picture>'
    return img_html


def blog_card_image_url(src):
    overrides = {
        SERVICE_CABLING_URL: responsive_variant_url('service-cabling', 640),
        SERVICE_INFRASTRUCTURE_URL: responsive_variant_url('service-infrastructure', 640),
        SERVICE_ACCESS_URL: responsive_variant_url('service-access', 640),
        SERVICE_WIFI_URL: responsive_variant_url('service-wifi', 768),
        ABOUT_PANEL_URL: responsive_variant_url('about-panel', 800),
    }
    return overrides.get(src, RESPONSIVE_IMAGE_DEFAULT_SRC.get(src, src))


def blog_hero_image_url(src):
    overrides = {
        SERVICE_CABLING_URL: responsive_variant_url('service-cabling', 960),
        SERVICE_INFRASTRUCTURE_URL: responsive_variant_url('service-infrastructure', 960),
        SERVICE_ACCESS_URL: responsive_variant_url('service-access', 960),
        SERVICE_WIFI_URL: responsive_variant_url('service-wifi', 768),
        ABOUT_PANEL_URL: responsive_variant_url('about-panel', 800),
    }
    return overrides.get(src, src)


def content_img(src, alt, width, height, cls='', eager=False, high_priority=False, zoomable=False, lang='en', caption='', sizes=''):
    display_src = RESPONSIVE_IMAGE_DEFAULT_SRC.get(src, src)
    display_sizes = sizes or "(min-width: 1024px) 44vw, 100vw"
    attrs = [
        f'src="{display_src}"',
        f'alt="{esc(alt)}"',
        f'width="{width}"',
        f'height="{height}"',
        'decoding="async"',
    ]
    responsive_sources = RESPONSIVE_IMAGE_SOURCES.get(src, [])
    if responsive_sources:
        srcset_value = ', '.join(f'{url} {variant_width}w' for url, variant_width in responsive_sources)
        attrs.append(f'srcset="{esc(srcset_value)}"')
        attrs.append(f'sizes="{esc(display_sizes)}"')
    if cls:
        attrs.append(f'class="{cls}"')
    if eager:
        attrs.append('loading="eager"')
    else:
        attrs.append('loading="lazy"')
    if high_priority:
        attrs.append('fetchpriority="high"')
    img_html = f'<img {" ".join(attrs)} />'
    picture_sources = RESPONSIVE_IMAGE_FORMAT_SOURCES.get(src, {})
    if picture_sources:
        source_tags = []
        for mime_type, variants in picture_sources.items():
            srcset_value = ', '.join(f'{url} {variant_width}w' for url, variant_width in variants)
            source_tags.append(
                f'<source type="{mime_type}" srcset="{esc(srcset_value)}" sizes="{esc(display_sizes)}" />'
            )
        img_html = f'<picture>{"".join(source_tags)}{img_html}</picture>'
    if not zoomable:
        return img_html
    ui = LIGHTBOX_UI.get(lang, LIGHTBOX_UI['en'])
    trigger_label = f'{ui["open"]}: {alt}'
    trigger_attrs = [
        'class="image-lightbox-trigger"',
        f'href="{esc(src)}"',
        'data-lightbox-trigger',
        f'data-lightbox-src="{esc(src)}"',
        f'data-lightbox-alt="{esc(alt)}"',
        f'data-lightbox-caption="{esc(caption or alt)}"',
        f'data-lightbox-width="{width}"',
        f'data-lightbox-height="{height}"',
        f'aria-label="{esc(trigger_label)}"',
    ]
    return f'<a {" ".join(trigger_attrs)}>{img_html}</a>'


def resource_hints(page_key, preload_image_url=None):
    hints = []
    if page_key == 'home':
        home_rack_avif_sources = RESPONSIVE_IMAGE_FORMAT_SOURCES.get(HOME_RACK_URL, {}).get('image/avif', [])
        home_rack_sources = home_rack_avif_sources or RESPONSIVE_IMAGE_SOURCES.get(HOME_RACK_URL, [])
        home_rack_srcset = ', '.join(f'{url} {variant_width}w' for url, variant_width in home_rack_sources)
        home_rack_preload = home_rack_sources[-1][0] if home_rack_sources else RESPONSIVE_IMAGE_DEFAULT_SRC.get(HOME_RACK_URL, HOME_RACK_URL)
        preload_type_attr = ' type="image/avif"' if home_rack_avif_sources else ''
        if home_rack_srcset:
            hints.append(
                f'<link rel="preload" as="image" href="{home_rack_preload}"{preload_type_attr} '
                f'imagesrcset="{esc(home_rack_srcset)}" imagesizes="(min-width: 1024px) 44vw, 100vw" />'
            )
        else:
            hints.append(f'<link rel="preload" as="image" href="{home_rack_preload}"{preload_type_attr} />')
    if page_key == 'contact':
        hints.append('<link rel="preconnect" href="https://forms.zohopublic.com" crossorigin />')
        hints.append('<link rel="dns-prefetch" href="//forms.zohopublic.com" />')
    if page_key == 'promo':
        hints.append('<link rel="preconnect" href="https://challenges.cloudflare.com" crossorigin />')
        hints.append('<link rel="dns-prefetch" href="//challenges.cloudflare.com" />')
    if preload_image_url:
        hints.append(f'<link rel="preload" as="image" href="{esc(preload_image_url)}" />')
    return ''.join(hints)


def tel_href(phone):
    digits = ''.join(ch for ch in phone if ch.isdigit() or ch == '+')
    if not digits:
        return ''
    if digits.startswith('+'):
        return digits
    if len(digits) == 10:
        return f'+1{digits}'
    if len(digits) == 11 and digits.startswith('1'):
        return f'+{digits}'
    return digits


def contact_details(lang):
    details = {}
    for label, value in T[lang]['contact_cards']:
        if label in GENERAL_INQUIRY_LABELS:
            details['general_email'] = value
        elif label in PROJECT_REQUEST_LABELS:
            details['project_email'] = value
        elif label in PHONE_LABELS:
            details['phone'] = value
    return details


def contact_value_html(label, value):
    if '@' in value:
        return f'<a class="text-link" href="mailto:{esc(value)}">{esc(value)}</a>'
    if label in PHONE_LABELS:
        href = tel_href(value)
        if href:
            return f'<a class="text-link" href="tel:{href}">{esc(value)}</a>'
    return esc(value)


def detail_item_html(label, value, extra_class=''):
    class_name = 'detail-item'
    if extra_class:
        class_name += f' {extra_class}'
    return f'<div class="{class_name}"><strong>{esc(label)}</strong><p>{contact_value_html(label, value)}</p></div>'


def contact_sidebar_details_html(lang):
    direct_items = []
    schedule_items = []
    for label, value in T[lang]['contact_cards']:
        if '@' in value or label in PHONE_LABELS:
            direct_items.append(detail_item_html(label, value, 'contact-detail-card contact-detail-card-direct'))
        else:
            schedule_items.append(detail_item_html(label, value, 'contact-detail-card contact-detail-card-hours'))
    contact_note = T[lang].get('contact_form_note')
    if contact_note:
        schedule_items.append(f'<div class="detail-item contact-detail-card contact-detail-card-note"><p>{esc(contact_note)}</p></div>')
    parts = []
    if direct_items:
        parts.append(f'<div class="contact-direct-grid">{"".join(direct_items)}</div>')
    if schedule_items:
        parts.append(f'<div class="contact-hours-grid">{"".join(schedule_items)}</div>')
    return f'<div class="contact-sidebar-stack">{"".join(parts)}</div>'


def breadcrumb_nav(items):
    parts = []
    for index, (label, href) in enumerate(items):
        if index:
            parts.append('<span>/</span>')
        if index == len(items) - 1:
            parts.append(f'<span aria-current="page">{esc(label)}</span>')
        else:
            parts.append(f'<a href="{href}">{esc(label)}</a>')
    return f'<nav class="breadcrumb section-shell" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def band_section(inner, section_class='', shell_class='section-shell'):
    attrs = f' class="{section_class}"' if section_class else ''
    return f'<section{attrs}><div class="{shell_class}">{inner}</div></section>'


def section_heading_html(eyebrow, title, copy=None, cls='section-heading'):
    eyebrow_html = ''
    if eyebrow and eyebrow.strip().casefold() != title.strip().casefold():
        eyebrow_html = f'<p class="eyebrow">{esc(eyebrow)}</p>'
    copy_html = f'<p>{esc(copy)}</p>' if copy else ''
    return f'<div class="{cls}">{eyebrow_html}<h2>{esc(title)}</h2>{copy_html}</div>'


def breadcrumb_schema(items, page_url):
    return {
        '@type': 'BreadcrumbList',
        '@id': page_url + '#breadcrumb',
        'itemListElement': [
            {'@type': 'ListItem', 'position': index, 'name': label, 'item': absolute_url(href)}
            for index, (label, href) in enumerate(items, start=1)
        ],
    }


def sitemap_xml():
    page_keys = [
        'home',
        'services',
        *order,
        'industries',
        'case-studies',
        *CASE_STUDY_ORDER,
        'blog',
        'articles',
        'guides',
        'about',
        'faq',
        'contact',
        'privacy',
        *INDUSTRY_DETAIL_KEYS,
        *MULTIFAMILY_CLUSTER_KEYS,
        'referral-program',
        'referral-program-terms',
        'referral-partner-program',
        'referral-partner-program-terms',
    ]
    if promo_publicly_indexable():
        page_keys.extend((
            'promo',
            'promo-rules',
        ))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for lang in ('en', 'fr'):
        for key in page_keys:
            page_url = absolute_url(routes[lang][key])
            lines.append('  <url>')
            lines.append(f'    <loc>{esc(page_url)}</loc>')
            lines.append(f'    <lastmod>{GENERATED_PAGE_LASTMODS.get(page_url, PREVIOUS_SITEMAP_LASTMODS.get(page_url, BUILD_DATE))}</lastmod>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{language_tag("en")}" href="{esc(absolute_url(routes["en"][key]))}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{language_tag("fr")}" href="{esc(absolute_url(routes["fr"][key]))}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{esc(absolute_url(default_route(key)))}" />')
            lines.append('  </url>')
    for lang in ('en', 'fr'):
        for article in blog_articles_for_lang(lang):
            page_url = absolute_url(article['path'])
            article_paths = blog_article_paths(article['key'])
            lines.append('  <url>')
            lines.append(f'    <loc>{esc(page_url)}</loc>')
            lines.append(f'    <lastmod>{GENERATED_PAGE_LASTMODS.get(page_url, PREVIOUS_SITEMAP_LASTMODS.get(page_url, BUILD_DATE))}</lastmod>')
            if article_paths.get('en'):
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{language_tag("en")}" href="{esc(absolute_url(article_paths["en"]))}" />')
            if article_paths.get('fr'):
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{language_tag("fr")}" href="{esc(absolute_url(article_paths["fr"]))}" />')
            default_article_path = article_paths.get('fr') or article_paths.get('en')
            if default_article_path:
                lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{esc(absolute_url(default_article_path))}" />')
            lines.append('  </url>')
    for lang in ('en', 'fr'):
        for article in [*guide_articles_for_lang(lang), *decision_articles_for_lang(lang)]:
            page_url = absolute_url(article['path'])
            article_paths = resource_article_paths(article['key'])
            lines.append('  <url>')
            lines.append(f'    <loc>{esc(page_url)}</loc>')
            lines.append(f'    <lastmod>{GENERATED_PAGE_LASTMODS.get(page_url, PREVIOUS_SITEMAP_LASTMODS.get(page_url, BUILD_DATE))}</lastmod>')
            if article_paths.get('en'):
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{language_tag("en")}" href="{esc(absolute_url(article_paths["en"]))}" />')
            if article_paths.get('fr'):
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{language_tag("fr")}" href="{esc(absolute_url(article_paths["fr"]))}" />')
            default_article_path = article_paths.get('fr') or article_paths.get('en')
            if default_article_path:
                lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{esc(absolute_url(default_article_path))}" />')
            lines.append('  </url>')
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


def webmanifest_json():
    return json.dumps(
        {
            'name': 'Opticable',
            'short_name': 'Opticable',
            'start_url': '/',
            'scope': '/',
            'display': 'standalone',
            'background_color': '#0f1413',
            'theme_color': '#153628',
            'icons': [
                {'src': '/assets/favicon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                {'src': '/assets/favicon-512.png', 'sizes': '512x512', 'type': 'image/png'},
            ],
        },
        ensure_ascii=False,
        indent=2,
    ) + '\n'


def card(title, text, link=None, label='Learn more', cls='card'):
    more = f'<a class="more" href="{link}">{esc(label)}</a>' if link else ''
    return f'<article class="{cls}"><h3>{esc(title)}</h3><p>{esc(text)}</p>{more}</article>'


def social_icon_svg(key):
    icons = {
        'facebook': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 8H16V5h-2.5C10.9 5 9 6.9 9 9.5V12H6.5v3H9V21h3v-6h3.1l.5-3H12V9.8c0-1.1.5-1.8 1.5-1.8Z"/></svg>',
        'linkedin': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.3 8.8a1.8 1.8 0 1 1 0-3.6 1.8 1.8 0 0 1 0 3.6Zm-1.4 2h2.9V19H4.9v-8.2Zm4.7 0h2.8v1.1h.1c.4-.7 1.3-1.4 2.8-1.4 3 0 3.6 2 3.6 4.6V19H16v-3.3c0-1.6 0-3.5-2.1-3.5s-2.4 1.7-2.4 3.4V19H8.6v-8.2Z"/></svg>',
        'instagram': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="4.5" width="15" height="15" rx="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="3.4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.2" cy="6.9" r="1.1" fill="currentColor"/></svg>',
    }
    return icons[key]


def label_for_key(lang, key):
    t = T[lang]
    if key in t:
        return t[key]
    alt_key = key.replace('-', '_')
    if alt_key in t:
        return t[alt_key]
    if key in services:
        return services[key][lang]['name']
    return key


def nav_dropdown(lang, key, current, child_keys, wide=False):
    current_attr = ' aria-current="page"' if current == key or current in child_keys else ''
    submenu_parts = []
    for child_key in child_keys:
        child_attr = ' aria-current="page"' if current == child_key else ''
        submenu_parts.append(f'<a href="{routes[lang][child_key]}"{child_attr}>{esc(label_for_key(lang, child_key))}</a>')
    submenu = ''.join(submenu_parts)
    submenu_class = 'nav-submenu nav-submenu-wide' if wide else 'nav-submenu'
    return (
        f'<div class="nav-item nav-item-has-children"><a class="nav-link" href="{routes[lang][key]}"{current_attr}>'
        f'{esc(label_for_key(lang, key))}</a><div class="{submenu_class}">{submenu}</div></div>'
    )


def nav_dropdown_links(label, href, current_active, items, wide=False):
    current_attr = ' aria-current="page"' if current_active else ''
    submenu_parts = []
    for item in items:
        child_attr = ' aria-current="page"' if item.get('current') else ''
        submenu_parts.append(f'<a href="{item["href"]}"{child_attr}>{esc(item["label"])}</a>')
    submenu = ''.join(submenu_parts)
    submenu_class = 'nav-submenu nav-submenu-wide' if wide else 'nav-submenu'
    return (
        f'<div class="nav-item nav-item-has-children"><a class="nav-link" href="{href}"{current_attr}>'
        f'{esc(label)}</a><div class="{submenu_class}">{submenu}</div></div>'
    )



def blog_nav_item(lang, current):
    return nav_dropdown(lang, 'blog', current, ('articles', 'guides'))

def simple_nav_link(lang, key, current):
    current_attr = ' aria-current="page"' if current == key else ''
    return f'<a class="nav-link" href="{routes[lang][key]}"{current_attr}>{esc(label_for_key(lang, key))}</a>'


def footer_social_links(lang):
    links = []
    for item in SOCIAL_LINKS:
        links.append(
            f'<a class="social-link" href="{item["href"]}" target="_blank" rel="noopener noreferrer" '
            f'aria-label="{esc(item["label"])}">{social_icon_svg(item["key"])}<span>{esc(item["label"])}</span></a>'
        )
    return ''.join(links)


def partner_brands_section(lang):
    copy = PARTNER_BRANDS_COPY[lang]
    badges = ''.join(f'<div class="brand-badge"><span>{esc(name)}</span></div>' for name in PARTNER_BRANDS)
    return band_section(
        f'<div class="section-heading"><p class="eyebrow">{esc(copy["eyebrow"])}</p>'
        f'<h2>{esc(copy["title"])}</h2><p>{esc(copy["intro"])}</p></div>'
        f'<div class="brand-badge-grid">{badges}</div>',
        'brand-section',
    )


def case_study_cards(lang, current_key=None):
    parent = CASE_STUDIES[lang]['parent']
    cards = []
    for key in CASE_STUDY_ORDER:
        if current_key and key == current_key:
            continue
        cards.append(card(CASE_STUDIES[lang]['items'][key]['nav'], parent['card_copy'][key], routes[lang][key], T[lang]['view_case_study']))
    return ''.join(cards)


def feature_card(title, text, link, label, badge, eyebrow):
    kicker = ''
    if eyebrow and eyebrow.strip().casefold() != title.strip().casefold():
        kicker = f'<p class="feature-kicker">{esc(eyebrow)}</p>'
    return (
        f'<article class="card feature-card"><div class="feature-card-header">'
        f'<div>{kicker}<h3>{esc(title)}</h3></div>'
        f'<span class="feature-badge">{esc(badge)}</span></div>'
        f'<p>{esc(text)}</p><a class="more" href="{link}">{esc(label)}</a></article>'
    )


def service_card(lang, key, label):
    meta = SERVICE_CARD_META[key][lang]
    service_name = services[key][lang]["name"]
    kicker = ''
    if meta["eyebrow"] and meta["eyebrow"].strip().casefold() != service_name.strip().casefold():
        kicker = f'<p class="service-card-kicker">{esc(meta["eyebrow"])}</p>'
    return (
        f'<article class="card service-card"><div class="service-card-header">'
        f'<div>{kicker}<h3>{esc(service_name)}</h3></div>'
        f'<span class="service-card-badge">{esc(meta["badge"])}</span></div>'
        f'<p>{esc(services[key][lang]["summary"])}</p>'
        f'<a class="more" href="{routes[lang][key]}">{esc(label)}</a></article>'
    )


def service_cards(lang, label, keys=None):
    keys = keys or order
    return ''.join(service_card(lang, key, label) for key in keys)


def render_chips(items):
    return '<div class="chip-list">' + ''.join(f'<span class="chip">{esc(item)}</span>' for item in items) + '</div>'


def render_service_chip_links(lang, keys, extra_class=''):
    class_name = 'chip-list service-chip-links'
    if extra_class:
        class_name += f' {extra_class}'
    return f'<div class="{class_name}">' + ''.join(
        f'<a class="chip" href="{routes[lang][key]}">{esc(services[key][lang]["name"])}</a>'
        for key in keys
    ) + '</div>'


def render_home_points(lang):
    items = []
    for text, key in zip(T[lang]['home_points'], HOME_POINT_KEYS):
        items.append(f'<li><a href="{routes[lang][key]}">{esc(text)}</a></li>')
    return f'<ul class="hero-points">{"".join(items)}</ul>'


def render_focus_chips(lang):
    items = T[lang].get('focus_chips', [])
    if not items:
        return ''
    return '<div class="hero-focus-cloud">' + ''.join(f'<span class="hero-focus-chip">{esc(item)}</span>' for item in items) + '</div>'


def localized_datetime_label(value, lang, include_time=False):
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value)
    else:
        parsed = value
    month_name = MONTH_NAMES[lang][parsed.month - 1]
    if lang == 'fr':
        date_label = f'{parsed.day} {month_name} {parsed.year}'
        if include_time:
            return f'{date_label} à {parsed.strftime("%H:%M")} (heure de Toronto)'
        return date_label
    date_label = f'{month_name} {parsed.day}, {parsed.year}'
    if include_time:
        return f'{date_label} at {parsed.strftime("%I:%M %p").lstrip("0")} Toronto time'
    return date_label


def promo_discount_range_label(lang):
    discounts = sorted(item['percent'] for item in PROMO_CONFIG['discounts'])
    if lang == 'fr':
        return f'{discounts[0]} % à {discounts[-1]} %'
    return f'{discounts[0]}% to {discounts[-1]}%'


def promo_cap_label():
    return f'${PROMO_CONFIG["discountCapCad"]:,} CAD'


def promo_limited_time_label(lang):
    return 'Limited-time offer' if lang == 'en' else 'Offre à durée limitée'


def promo_deadline_label(lang):
    if lang == 'fr':
        return f"Jusqu'au {localized_datetime_label(PROMO_END, lang)}"
    return f'Ends {localized_datetime_label(PROMO_END, lang)}'


def promo_odds_rows(lang):
    rows = []
    for item in PROMO_CONFIG['discounts']:
        chance_label = f'{item["weight"]} %' if lang == 'fr' else f'{item["weight"]}%'
        rows.append(
            f'<tr><th scope="row">{item["percent"]}%</th><td>{esc(chance_label)}</td></tr>'
        )
    return ''.join(rows)


def promo_rules_summary(lang):
    if lang == 'fr':
        return [
            ('Période de la campagne', f'Du {localized_datetime_label(PROMO_START, lang, True)} au {localized_datetime_label(PROMO_END, lang, True)}.'),
            ('Admissibilité', "Les entrées doivent concerner un projet situé au Québec."),
            ('Valeur de la promo', f'Rabais entre {promo_discount_range_label(lang)} sur le sous-total avant taxes, jusqu’à {promo_cap_label()} par soumission admissible.'),
            ('Limites', "Une seule entrée par adresse courriel et par campagne. Les services récurrents, appels de soutien, taxes et travaux déjà escomptés sont exclus."),
        ]
    return [
        ('Campaign period', f'From {localized_datetime_label(PROMO_START, lang, True)} through {localized_datetime_label(PROMO_END, lang, True)}.'),
        ('Eligibility', 'Entries must relate to a project in Quebec.'),
        ('Promo value', f'Discounts range from {promo_discount_range_label(lang)} on the pre-tax quoted subtotal, capped at {promo_cap_label()} per qualifying quote.'),
        ('Limits', 'One entry per email address per campaign. Recurring services, support calls, taxes, and already discounted work are excluded.'),
    ]


def promo_result_panel(lang):
    copy = PROMO_PAGE_CONTENT[lang]
    labels = copy['result_labels']
    return (
        f'<div class="promo-result-overlay" data-promo-result hidden>'
        f'<section class="promo-result-dialog contact-panel" role="dialog" aria-modal="true" aria-labelledby="promo-result-title-{lang}">'
        f'<button class="promo-result-close" type="button" data-promo-result-close aria-label="{esc(copy["actions"]["close_modal"])}">&times;</button>'
        f'<p class="eyebrow" data-promo-result-state></p>'
        f'<h2 id="promo-result-title-{lang}" data-promo-result-title>{esc(copy["result_title"])}</h2>'
        f'<p class="promo-result-copy" data-promo-result-copy>{esc(copy["result_copy"])}</p>'
        f'<div class="promo-result-code-shell">'
        f'<strong>{esc(labels["code"])}</strong>'
        f'<div class="promo-result-code-row">'
        f'<input class="promo-result-code-input" data-promo-result-code-input type="text" readonly value="" />'
        f'<div class="promo-result-code-actions">'
        f'<button class="button button-primary promo-copy-button" type="button" data-promo-result-copy-button data-copy-default="{esc(copy["actions"]["copy_code"])}" data-copy-success="{esc(copy["actions"]["copied_code"])}">{esc(copy["actions"]["copy_code"])}</button>'
        f'<button class="button button-secondary promo-save-button" type="button" data-promo-result-save-button data-save-default="{esc(copy["actions"]["save_code"])}" data-save-success="{esc(copy["actions"]["saved_code"])}">{esc(copy["actions"]["save_code"])}</button>'
        f'</div>'
        f'</div></div>'
        f'<div class="promo-result-grid promo-result-grid-compact">'
        f'<div class="detail-item"><strong>{esc(labels["discount"])}</strong><p data-promo-result-discount></p></div>'
        f'<div class="detail-item"><strong>{esc(labels["expires"])}</strong><p data-promo-result-expiry></p></div>'
        f'</div>'
        f'<div class="promo-result-actions">'
        f'<a class="button button-secondary" data-promo-result-contact href="{routes[lang]["contact"]}">{esc(copy["actions"]["quote"])}</a>'
        f'<a class="text-link promo-result-rules-link" href="{routes[lang]["promo-rules"]}">{esc(copy["actions"]["rules"])}</a>'
        f'</div></section></div>'
    )


def promo_form_shell(lang):
    copy = PROMO_PAGE_CONTENT[lang]
    contact_note_html = f'<p class="form-note">{esc(copy["contact_note"])}</p>' if copy.get('contact_note') else ''
    form_copy = {
        'statusLoading': copy['status_loading'],
        'statusUnavailable': copy['status_unavailable'],
        'submitLoading': copy['submit_loading'],
        'existingTitle': copy['existing_title'],
        'existingCopy': copy['existing_copy'],
        'resultTitle': copy['result_title'],
        'resultCopy': copy['result_copy'],
        'duplicateTitle': copy['duplicate_title'],
        'duplicateCopy': copy['duplicate_copy'],
        'invalidEmail': 'Use a valid email address.' if lang == 'en' else 'Utilisez une adresse courriel valide.',
        'requiredField': 'Complete all required fields.' if lang == 'en' else 'Remplissez tous les champs obligatoires.',
        'requiredConsent': 'Confirm the required eligibility and rules checkboxes.' if lang == 'en' else "Confirmez les cases obligatoires liées à l'admissibilité et au règlement.",
        'requiredSkill': 'Answer the skill-testing question.' if lang == 'en' else "Répondez à la question d'habileté.",
        'turnstileError': 'The security check could not be validated. Reload the page and try again.' if lang == 'en' else "La vérification de sécurité a échoué. Rechargez la page et réessayez.",
        'genericError': 'The promo entry could not be completed. Please try again or use the quote page directly.' if lang == 'en' else "L'entrée promo n'a pas pu être traitée. Réessayez ou utilisez directement la page de soumission.",
        'challengeLabel': copy['fields']['skill'],
        'resultLabels': copy['result_labels'],
        'quotePath': routes[lang]['contact'],
        'saveQuoteLabel': 'Quote page' if lang == 'en' else 'Page de soumission',
        'saveFilePrefix': 'opticable-promo-code' if lang == 'en' else 'code-promo-opticable',
    }
    fields = copy['fields']
    consents = copy['consents']
    return (
        f'<div class="form-panel promo-form-shell" data-promo-root data-lang="{lang}" data-config-url="/api/promo/config?lang={lang}" data-entry-url="/api/promo/entry">'
        f'<script type="application/json" data-promo-copy>{json.dumps(form_copy, ensure_ascii=False)}</script>'
        f'<p class="eyebrow">{esc(copy["form_eyebrow"])}</p><h2>{esc(copy["form_title"])}</h2><p>{esc(copy["form_intro"])}</p>'
        f'<div class="promo-inline-status" data-promo-status>{esc(copy["status_loading"])}</div>'
        f'<div class="promo-inline-error" data-promo-error hidden></div>'
        f'<form class="promo-entry-form" data-promo-form novalidate>'
        f'<div class="input-grid">'
        f'<label class="field"><span>{esc(fields["name"])}</span><input name="name" autocomplete="name" required /></label>'
        f'<label class="field"><span>{esc(fields["email"])}</span><input name="email" type="email" autocomplete="email" required /></label>'
        f'<label class="field"><span>{esc(fields["phone"])}</span><input name="phone" type="tel" autocomplete="tel" /></label>'
        f'<label class="field"><span>{esc(fields["company"])}</span><input name="company" autocomplete="organization" /></label>'
        f'</div>'
        f'<div class="promo-skill-shell" data-promo-skill-shell hidden>'
        f'<p class="promo-skill-prompt" data-promo-skill-prompt></p>'
        f'<label class="field"><span>{esc(fields["skill"])}</span><input name="skill_answer" inputmode="numeric" required /></label>'
        f'<input name="skill_token" type="hidden" />'
        f'</div>'
        f'<div class="promo-turnstile-shell"><div class="promo-turnstile" data-promo-turnstile></div></div>'
        f'<div class="promo-checklist">'
        f'<label><input name="quebec_attestation" type="checkbox" required /> <span>{esc(consents["quebec"])}</span></label>'
        f'<label><input name="rules_attestation" type="checkbox" required />'
        f'<span class="promo-consent-copy"><span class="promo-consent-text">{esc(consents["rules"])}</span>'
        f'<span class="promo-consent-links"><a href="{routes[lang]["promo-rules"]}">{esc(copy["actions"].get("rules_inline", copy["actions"]["rules"]))}</a><span class="promo-consent-separator" aria-hidden="true">·</span><a href="{routes[lang]["privacy"]}">{esc(T[lang]["privacy"])}</a></span>'
        f'</span></label>'
        f'<label><input name="marketing_opt_in" type="checkbox" /> <span>{esc(consents["marketing"])}</span></label>'
        f'</div>'
        f'<button class="button button-primary promo-submit" type="submit" data-promo-submit disabled>{esc(copy["submit"])}</button>'
        f'</form>'
        f'{contact_note_html}'
        f'{promo_result_panel(lang)}'
        f'</div>'
    )


def promo_rules_body(lang):
    copy = PROMO_PAGE_CONTENT[lang]
    summary_cards = ''.join(card(title, text) for title, text in promo_rules_summary(lang))
    if lang == 'fr':
        sections = (
            ('Promoteur', f'{PROMO_CONFIG["sponsor"]["legalName"]}, faisant affaire sous le nom Opticable.'),
            ('Admissibilité', "La campagne est ouverte aux personnes majeures qui soumettent une entrée liée à un projet situé au Québec. Les projets hors Québec sont exclus."),
            ('Aucun achat requis', "Aucun achat n'est requis pour participer. Une bonne réponse à la question d'habileté et le respect du présent règlement sont nécessaires pour conserver le résultat attribué."),
            ('Probabilités de gain', "Les probabilités dépendent de la grille pondérée ci-dessous. Chaque entrée valide obtient un seul résultat pour la campagne."),
            ('Utilisation du code', "Le code promo doit être mentionné dans la demande de soumission Opticable avant l'expiration. Le rabais, s'il est applicable, est calculé sur le sous-total avant taxes d'une nouvelle soumission d'installation admissible et demeure plafonné à " + promo_cap_label() + '.'),
            ('Exclusions', "Les taxes, appels de soutien, services récurrents, contrats déjà signés, travaux déjà réduits, matériel acheté séparément et autres services exclus par la soumission ne sont pas admissibles."),
            ('Consentement et confidentialité', "Les renseignements saisis servent à administrer la campagne, à prévenir les abus, à faire le suivi commercial et, seulement si vous y consentez, à l'envoi de communications marketing. Le retrait du consentement marketing n'affecte pas les suivis liés aux soumissions ou aux services."),
            ('Différends', "Le règlement et l'administration de la campagne sont régis par les lois applicables au Québec et au Canada. En cas de divergence, la version publiée sur le site Opticable prévaut pour cette campagne."),
        )
    else:
        sections = (
            ('Sponsor', f'{PROMO_CONFIG["sponsor"]["legalName"]}, carrying on business as Opticable.'),
            ('Eligibility', 'The campaign is open to adults submitting an entry tied to a project in Quebec. Non-Quebec projects are excluded.'),
            ('No purchase required', 'No purchase is required to enter. A correct answer to the skill-testing question and compliance with these rules are required to keep the assigned result.'),
            ('Odds', 'The odds follow the weighted distribution below. Each valid email address receives one result for the campaign.'),
            ('Code redemption', 'The promo code must be mentioned in the Opticable quote request before expiry. If applicable, the discount is calculated on the pre-tax subtotal of a qualifying new installation quote and remains capped at ' + promo_cap_label() + '.'),
            ('Exclusions', 'Taxes, support calls, recurring services, already signed work, already discounted scopes, separately purchased material, and other excluded services are not eligible.'),
            ('Consent and privacy', 'Submitted information is used to administer the campaign, prevent abuse, support commercial follow-up, and, only if you opt in, send marketing communications. Withdrawing marketing consent does not affect quote or service follow-up.'),
            ('Disputes', 'The rules and campaign administration are governed by applicable Quebec and Canadian law. The version published on the Opticable website governs this campaign.'),
        )
    section_html = ''.join(
        f'<article class="contact-panel"><h2>{esc(title)}</h2><p>{esc(text)}</p></article>'
        for title, text in sections
    )
    odds_heading = 'Weighted promo distribution' if lang == 'en' else 'Répartition pondérée de la promo'
    odds_copy = 'Assigned immediately after validation.' if lang == 'en' else 'Attribuée immédiatement après validation.'
    return (
        band_section(
            f'<div class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(copy["label"])}</p><h1>{esc(copy["rules_h1"])}</h1><p>{esc(copy["rules_intro"])}</p></div></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(copy["label"])}</p><h2>{esc(copy["rules_h1"])}</h2><p>{esc(copy["rules_desc"])}</p></div><div class="grid-2">{summary_cards}</div>',
            'promo-rules-summary-section',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(copy["label"])}</p><h2>{esc(odds_heading)}</h2><p>{esc(odds_copy)}</p></div>'
            f'<div class="contact-panel promo-odds-panel"><table class="promo-odds-table"><thead><tr><th>{"Discount" if lang == "en" else "Rabais"}</th><th>{"Chance" if lang == "en" else "Probabilité"}</th></tr></thead><tbody>{promo_odds_rows(lang)}</tbody></table></div>',
            'promo-rules-odds-section',
        )
        + band_section(f'<div class="grid-2">{section_html}</div>', 'promo-rules-section')
    )


def promo_unsubscribe_form(lang):
    copy = PROMO_PAGE_CONTENT[lang]
    payload = {
        'success': copy['unsubscribe_success'],
        'invalidEmail': 'Use a valid email address.' if lang == 'en' else 'Utilisez une adresse courriel valide.',
        'genericError': 'The request could not be completed. Please try again.' if lang == 'en' else "La demande n'a pas pu être traitée. Réessayez.",
    }
    return (
        f'<div class="form-panel promo-unsubscribe-shell" data-promo-unsubscribe data-lang="{lang}" data-unsubscribe-url="/api/promo/unsubscribe">'
        f'<script type="application/json" data-promo-unsubscribe-copy>{json.dumps(payload, ensure_ascii=False)}</script>'
        f'<p class="eyebrow">{esc(copy["label"])}</p><h2>{esc(copy["unsubscribe_h1"])}</h2><p>{esc(copy["unsubscribe_intro"])}</p>'
        f'<form class="promo-unsubscribe-form" data-promo-unsubscribe-form novalidate>'
        f'<label class="field"><span>{esc(copy["fields"]["email"])}</span><input name="email" type="email" autocomplete="email" required /></label>'
        f'<button class="button button-primary" type="submit">{esc(copy["unsubscribe_button"])}</button>'
        f'</form>'
        f'<div class="promo-inline-status" data-promo-unsubscribe-status hidden></div>'
        f'<div class="promo-inline-error" data-promo-unsubscribe-error hidden></div>'
        f'<p class="form-note">{esc(copy["unsubscribe_note"])}</p></div>'
    )


def promo_admin_shell(lang):
    copy = PROMO_ADMIN_CONTENT[lang]
    payload = {
        'loading': copy['loading'],
        'loadError': copy['load_error'],
        'marketingYes': copy['marketing_yes'],
        'marketingNo': copy['marketing_no'],
        'marketingOut': copy['marketing_out'],
        'scopeCurrent': copy['scope_current'],
        'scopeAll': copy['scope_all'],
        'none': copy['none'],
        'deleteError': copy['delete_error'],
        'deleteNone': copy['delete_none'],
        'deleteSelectedConfirm': copy['delete_selected_confirm'],
        'deleteViewConfirm': copy['delete_view_confirm'],
        'deleteSelectedSuccess': copy['delete_selected_success'],
        'deleteViewSuccess': copy['delete_view_success'],
        'deleteViewLabel': copy['delete_view'],
        'deleteViewAllLabel': copy['delete_view_all'],
    }
    summary = copy['summary']
    table = copy['table']
    return (
        f'<div class="form-panel promo-admin-shell" data-promo-admin data-lang="{lang}" data-entries-url="/api/promo/admin/entries?lang={lang}" data-export-url="/api/promo/admin/export.csv" data-subscribers-export-url="/api/promo/admin/subscribers.csv" data-delete-url="/api/promo/admin/delete" data-limit="200">'
        f'<script type="application/json" data-promo-admin-copy>{json.dumps(payload, ensure_ascii=False)}</script>'
        f'<div class="promo-admin-toolbar">'
        f'<div class="promo-admin-scope" role="group" aria-label="{esc(copy["scope_label"])}">'
        f'<button class="button button-secondary" type="button" data-promo-admin-scope="current" aria-pressed="true">{esc(copy["scope_current"])}</button>'
        f'<button class="button button-secondary" type="button" data-promo-admin-scope="all" aria-pressed="false">{esc(copy["scope_all"])}</button>'
        f'</div>'
        f'<div class="promo-admin-actions">'
        f'<button class="button button-secondary" type="button" data-promo-admin-refresh>{esc(copy["refresh"])}</button>'
        f'<button class="button button-secondary" type="button" data-promo-admin-delete-selected disabled>{esc(copy["delete_selected"])}</button>'
        f'<button class="button button-secondary" type="button" data-promo-admin-delete-view>{esc(copy["delete_view"])}</button>'
        f'<a class="button button-primary" data-promo-admin-export-subscribers href="/api/promo/admin/subscribers.csv?scope=current">{esc(copy["export_subscribers"])}</a>'
        f'<a class="button button-secondary" data-promo-admin-export href="/api/promo/admin/export.csv?scope=current">{esc(copy["export_entries"])}</a>'
        f'</div></div>'
        f'<div class="promo-inline-status" data-promo-admin-status>{esc(copy["loading"])}</div>'
        f'<div class="promo-inline-error" data-promo-admin-error hidden></div>'
        f'<div class="promo-admin-summary">'
        f'<div class="detail-item"><strong>{esc(summary["entries"])}</strong><p data-promo-admin-total>0</p></div>'
        f'<div class="detail-item"><strong>{esc(summary["marketing"])}</strong><p data-promo-admin-marketing>0</p></div>'
        f'<div class="detail-item"><strong>{esc(summary["recent"])}</strong><p data-promo-admin-recent>0</p></div>'
        f'<div class="detail-item"><strong>{esc(summary["latest"])}</strong><p data-promo-admin-latest>{esc(copy["none"])}</p></div>'
        f'</div>'
        f'<div class="promo-admin-meta">'
        f'<div class="detail-item"><strong>{esc(summary["current_campaign"])}</strong><p data-promo-admin-current-name>{esc(copy["none"])}</p></div>'
        f'<div class="detail-item"><strong>{esc(summary["campaign_window"])}</strong><p data-promo-admin-window>{esc(copy["none"])}</p></div>'
        f'<div class="detail-item"><strong>{esc(summary["active_view"])}</strong><p data-promo-admin-view>{esc(copy["scope_current"])}</p></div>'
        f'</div>'
        f'<div class="promo-admin-table-shell"><table class="promo-admin-table"><thead><tr>'
        f'<th><label class="promo-admin-select-all"><input type="checkbox" data-promo-admin-select-all aria-label="{esc(copy["select_all"])}" /> <span>{esc(table["select"])}</span></label></th>'
        f'<th>{esc(table["received"])}</th>'
        f'<th>{esc(table["campaign"])}</th>'
        f'<th>{esc(table["name"])}</th>'
        f'<th>{esc(table["email"])}</th>'
        f'<th>{esc(table["phone"])}</th>'
        f'<th>{esc(table["company"])}</th>'
        f'<th>{esc(table["discount"])}</th>'
        f'<th>{esc(table["code"])}</th>'
        f'<th>{esc(table["expires"])}</th>'
        f'<th>{esc(table["marketing"])}</th>'
        f'<th>{esc(table["attribution"])}</th>'
        f'</tr></thead><tbody data-promo-admin-table-body></tbody></table></div>'
        f'<div class="promo-admin-empty" data-promo-admin-empty hidden>{esc(copy["empty"])}</div>'
        f'</div>'
    )


def referral_program_copy(lang, program_key):
    key = 'partnerProgram' if program_key == 'partner' else 'clientProgram'
    copy = dict(REFERRAL_CONTENT[key][lang])
    if program_key == 'client':
        if lang == 'fr':
            copy['faqs'] = [
                *copy['faqs'],
                ("Comment utiliser mon crédit ?", "Votre portail affiche votre code membre et votre solde disponible. Pour appliquer un crédit, appelez Opticable, donnez votre code membre et confirmez le montant à utiliser. Opticable valide ensuite le montant et le déduit de votre solde."),
            ]
            copy['terms_sections'] = [
                *copy['terms_sections'],
                ("Code membre et utilisation du crédit", "Le portail client affiche un code membre réservé au titulaire du compte. Pour appliquer un crédit, le titulaire doit communiquer avec Opticable. Après validation, Opticable déduit le montant approuvé du solde disponible."),
                ("Sous-total admissible", "Les rabais et crédits sont calculés seulement sur le sous-total admissible avant taxes approuvé par Opticable. Les taxes, permis, frais de livraison, frais de financement, appels d'urgence, services récurrents, soutien, maintenance, garanties, travaux déjà escomptés et éléments refacturés au coût peuvent être exclus."),
                ("Code au premier contact", "Le code de référence doit être fourni lors de la première demande de soumission ou du premier échange commercial. Un code ne peut pas être appliqué rétroactivement à une demande déjà connue, déjà ouverte, déjà soumissionnée, déjà signée ou déjà en cours."),
                ("Un seul code par projet", "Un seul code de référence, partenaire, promo ou crédit membre peut être appliqué à un même projet, sauf approbation écrite d'Opticable."),
                ("Définition de projet réalisé et payé", "Un projet est considéré réalisé et payé seulement lorsque les travaux sont substantiellement terminés, que la facture est émise, que la facture est payée en totalité et qu'aucun solde, différend, remboursement, annulation, rétrofacturation ou retenue n'est ouvert."),
                ("Période de retenue", "Opticable peut appliquer une période de retenue allant jusqu'à 30 jours après le paiement complet avant de rendre un crédit utilisable, afin de protéger le programme contre les remboursements, différends, annulations ou ajustements de projet."),
                ("Aucune valeur monétaire", "Les crédits client n'ont aucune valeur monétaire, ne sont pas transférables, ne peuvent pas être échangés contre de l'argent et ne peuvent pas servir à payer les taxes."),
                ("Protection contre les abus", "Opticable peut refuser, suspendre, renverser ou annuler un crédit en cas de doublon, fausse information, auto-référence, abus entre entreprises liées, conflit d'intérêts, sollicitation trompeuse, pourriel ou tentative de manipulation du programme."),
                ("Décision finale", "Opticable conserve la discrétion finale pour déterminer l'admissibilité, le sous-total admissible, les exclusions, les doublons, les montants de crédit et le respect des règles du programme."),
                ("Modification du programme", "Opticable peut modifier, suspendre ou terminer le programme en tout temps. Les crédits gagnés de bonne foi demeurent admissibles selon les règles applicables, mais peuvent être refusés ou renversés en cas d'erreur, non-paiement, remboursement, fraude ou abus."),
                ("Droit applicable", "Le programme est régi par les lois applicables du Québec et du Canada."),
            ]
        else:
            copy['faqs'] = [
                *copy['faqs'],
                ("How do I use my available credit?", "Your portal shows your member code and your available balance. To apply credit, call Opticable, provide your member code, and confirm the amount to use. Opticable then validates it and deducts it from your balance."),
            ]
            copy['terms_sections'] = [
                *copy['terms_sections'],
                ("Member code and credit use", "The client portal shows a member-only code reserved for the account holder. To apply credit, the account holder must contact Opticable. After validation, Opticable deducts the approved amount from the available balance."),
                ("Eligible subtotal", "Discounts and credits are calculated only on the eligible pre-tax subtotal approved by Opticable. Taxes, permits, shipping, financing fees, emergency calls, recurring services, support, maintenance, warranty work, already-discounted work, and pass-through items may be excluded."),
                ("Code on first contact", "The referral code must be provided during the first quote request or first sales conversation. A code cannot be applied retroactively to a request already known, already open, already quoted, already signed, or already in progress."),
                ("One code per project", "Only one referral, partner, promo, or member credit code may be applied to the same project unless Opticable approves otherwise in writing."),
                ("Completed and paid definition", "A project is considered completed and paid only when the work is substantially completed, the invoice is issued, the invoice is fully paid, and there is no open balance, dispute, refund, cancellation, chargeback, or holdback."),
                ("Hold period", "Opticable may apply a hold period of up to 30 days after full payment before making credit usable, to protect the program against refunds, disputes, cancellations, or project adjustments."),
                ("No cash value", "Client credits have no cash value, are not transferable, cannot be exchanged for money, and cannot be used to pay taxes."),
                ("Abuse protection", "Opticable may refuse, pause, reverse, or void a credit in cases of duplication, false information, self-referrals, same-company abuse, conflicts of interest, misleading solicitation, spam, or attempts to manipulate the program."),
                ("Final decision", "Opticable has final discretion to determine eligibility, eligible subtotal, exclusions, duplicate leads, credit amounts, and whether the program rules were respected."),
                ("Program changes", "Opticable may modify, pause, or end the program at any time. Credits earned in good faith remain eligible under the applicable rules, but may still be refused or reversed for error, non-payment, refund, fraud, or abuse."),
                ("Governing law", "The program is governed by the applicable laws of Quebec and Canada."),
            ]
    else:
        if lang == 'fr':
            copy.update({
                'intro': "Ce programme s'adresse aux entreprises et aux professionnels capables de recommander plusieurs projets qualifiés. Chaque demande est validée avant la création du compte partenaire.",
                'steps_intro': "Vous soumettez d'abord une demande. Après validation, Opticable crée le compte, le code et l'accès portail.",
                'form_intro': "Transmettez les coordonnées de votre entreprise pour révision. Opticable valide d'abord la demande, puis crée le compte partenaire si elle est approuvée.",
            })
            copy['steps'] = [
                ("Faites une demande", "Présentez votre entreprise et le type de références visé."),
                ("Compte créé après approbation", "Après validation, Opticable crée le compte partenaire, le code et l'accès portail."),
                ("Utilisez le code au premier contact", "Le nouveau client doit utiliser le code lors de la première demande de soumission."),
                ("Gagnez un paiement", "Le paiement est gagné seulement après la réalisation et le paiement complet du projet référé."),
            ]
            updated_faqs = []
            for title, text in copy['faqs']:
                if title == "Ai-je accès à un portail ?":
                    updated_faqs.append((title, "Oui, après l'approbation de la demande et la création du compte partenaire par Opticable."))
                else:
                    updated_faqs.append((title, text))
            copy['faqs'] = updated_faqs
            updated_terms = []
            for title, text in copy['terms_sections']:
                if title == "Approbation":
                    updated_terms.append((title, "Chaque demande partenaire est validée avant la création du compte partenaire."))
                else:
                    updated_terms.append((title, text))
            copy['terms_sections'] = updated_terms
            copy['faqs'] = [
                *copy['faqs'],
                ("Comment retirer une commission ?", "Communiquez avec Opticable pour confirmer le montant à régler. Une fois le virement transmis, Opticable marque la commission comme réglée dans votre portail."),
            ]
            copy['terms_sections'] = [
                *copy['terms_sections'],
                ("Règlement des commissions", "Les commissions ne sont pas retirées automatiquement dans le portail. Le partenaire doit communiquer avec Opticable pour demander le règlement, puis Opticable confirme le transfert et met le dossier à jour."),
                ("Sous-total admissible", "Les commissions sont calculées seulement sur le sous-total admissible avant taxes approuvé par Opticable. Les taxes, permis, frais de livraison, frais de financement, appels d'urgence, services récurrents, soutien, maintenance, garanties, travaux déjà escomptés et éléments refacturés au coût peuvent être exclus."),
                ("Code au premier contact", "Le code partenaire doit être fourni lors de la première demande de soumission ou du premier échange commercial. Un code ne peut pas être appliqué rétroactivement à une demande déjà connue, déjà ouverte, déjà soumissionnée, déjà signée ou déjà en cours."),
                ("Un seul code par projet", "Un seul code de référence, partenaire, promo ou crédit membre peut être appliqué à un même projet, sauf approbation écrite d'Opticable."),
                ("Statut indépendant", "Le partenaire demeure indépendant. Il n'est pas un employé, agent, mandataire, courtier, représentant légal ou associé d'Opticable."),
                ("Aucune autorité d'engager Opticable", "Le partenaire ne peut pas promettre de prix, rabais, délais, disponibilités, garanties, spécifications techniques ou conditions contractuelles au nom d'Opticable."),
                ("Conformité et conflits d'intérêts", "Le partenaire doit confirmer qu'il est autorisé à recevoir une commission de référence et doit divulguer toute restriction d'employeur, règle d'approvisionnement, règle de copropriété ou de gestion, situation publique ou conflit d'intérêts pouvant interdire ou limiter le paiement."),
                ("Facturation, taxes et renseignements de paiement", "Le partenaire est responsable de ses taxes, déclarations, factures et obligations d'affaires. Opticable peut exiger le nom légal, le nom d'entreprise, l'adresse, les numéros de taxes, une facture, un reçu ou une confirmation de paiement avant d'émettre un règlement."),
                ("Appels d'offres et dossiers contrôlés", "Les appels d'offres publics, processus d'approvisionnement formels, dossiers gouvernementaux et situations de soumission contrôlée sont exclus, sauf si la compensation est clairement permise, divulguée et approuvée."),
                ("Signature d'une entente", "Opticable peut exiger une entente partenaire signée électroniquement avant l'activation du compte, l'utilisation du code ou le versement d'une commission."),
                ("Définition de projet réalisé et payé", "Un projet est considéré réalisé et payé seulement lorsque les travaux sont substantiellement terminés, que la facture est émise, que la facture est payée en totalité et qu'aucun solde, différend, remboursement, annulation, rétrofacturation ou retenue n'est ouvert."),
                ("Période de retenue", "Opticable peut appliquer une période de retenue allant jusqu'à 30 jours après le paiement complet avant de régler une commission, afin de protéger le programme contre les remboursements, différends, annulations ou ajustements de projet."),
                ("Confidentialité et portail", "Le portail peut afficher les statuts, sous-totaux, codes et montants de commission liés au partenaire, mais Opticable n'est pas tenue de divulguer les détails privés complets du client ou du projet référé."),
                ("Protection contre les abus", "Opticable peut refuser, suspendre, renverser ou annuler une commission en cas de doublon, fausse information, auto-référence, abus entre entreprises liées, conflit d'intérêts, sollicitation trompeuse, pourriel, usage non autorisé de la marque ou tentative de manipulation du programme."),
                ("Décision finale", "Opticable conserve la discrétion finale pour déterminer l'admissibilité, le sous-total admissible, les exclusions, les doublons, les montants de commission et le respect des règles du programme."),
                ("Modification du programme", "Opticable peut modifier, suspendre ou terminer le programme en tout temps. Les commissions gagnées de bonne foi demeurent admissibles selon les règles applicables, mais peuvent être refusées ou renversées en cas d'erreur, non-paiement, remboursement, fraude ou abus."),
                ("Droit applicable", "Le programme est régi par les lois applicables du Québec et du Canada."),
            ]
        else:
            copy['faqs'] = [
                *copy['faqs'],
                ("How do I withdraw a commission?", "Contact Opticable to confirm the amount to settle. Once the transfer is sent, Opticable marks the commission as settled in your portal."),
            ]
            copy['terms_sections'] = [
                *copy['terms_sections'],
                ("Commission settlement", "Commissions are not withdrawn automatically from the portal. The partner must contact Opticable to request settlement, then Opticable confirms the transfer and updates the portal."),
                ("Eligible subtotal", "Commissions are calculated only on the eligible pre-tax subtotal approved by Opticable. Taxes, permits, shipping, financing fees, emergency calls, recurring services, support, maintenance, warranty work, already-discounted work, and pass-through items may be excluded."),
                ("Code on first contact", "The partner code must be provided during the first quote request or first sales conversation. A code cannot be applied retroactively to a request already known, already open, already quoted, already signed, or already in progress."),
                ("One code per project", "Only one referral, partner, promo, or member credit code may be applied to the same project unless Opticable approves otherwise in writing."),
                ("Independent status", "The partner remains independent. The partner is not an employee, agent, mandatary, broker, legal representative, or legal partner of Opticable."),
                ("No authority to bind Opticable", "The partner cannot promise pricing, discounts, timelines, availability, warranties, technical specifications, or contract terms on behalf of Opticable."),
                ("Compliance and conflicts of interest", "The partner must confirm they are allowed to receive referral compensation and must disclose any employer restriction, procurement rule, condominium or management rule, public-sector situation, or conflict of interest that could prohibit or limit payment."),
                ("Invoices, taxes, and payment details", "The partner is responsible for its own taxes, declarations, invoices, and business obligations. Opticable may require legal name, business name, address, tax numbers, invoice, receipt, or payment confirmation before issuing settlement."),
                ("Tenders and controlled files", "Public tenders, formal procurement processes, government files, and controlled bidding situations are excluded unless compensation is clearly allowed, disclosed, and approved."),
                ("Signed agreement", "Opticable may require an electronically signed partner agreement before account activation, code use, or commission payment."),
                ("Completed and paid definition", "A project is considered completed and paid only when the work is substantially completed, the invoice is issued, the invoice is fully paid, and there is no open balance, dispute, refund, cancellation, chargeback, or holdback."),
                ("Hold period", "Opticable may apply a hold period of up to 30 days after full payment before settling a commission, to protect the program against refunds, disputes, cancellations, or project adjustments."),
                ("Confidentiality and portal", "The portal may show statuses, subtotals, codes, and commission amounts linked to the partner, but Opticable does not need to disclose complete private client or project details for the referred file."),
                ("Abuse protection", "Opticable may refuse, pause, reverse, or void a commission in cases of duplication, false information, self-referrals, same-company abuse, conflicts of interest, misleading solicitation, spam, unauthorized brand use, or attempts to manipulate the program."),
                ("Final decision", "Opticable has final discretion to determine eligibility, eligible subtotal, exclusions, duplicate leads, commission amounts, and whether the program rules were respected."),
                ("Program changes", "Opticable may modify, pause, or end the program at any time. Commissions earned in good faith remain eligible under the applicable rules, but may still be refused or reversed for error, non-payment, refund, fraud, or abuse."),
                ("Governing law", "The program is governed by the applicable laws of Quebec and Canada."),
            ]
    return copy


def referral_portal_copy(lang):
    copy = dict(REFERRAL_CONTENT['portal'][lang])
    if lang == 'fr':
        copy.update({
            'label': 'Portail de référence',
            'title': 'Portail de référence | Opticable',
            'desc': 'Portail Opticable pour consulter votre code, vos références, vos crédits ou commissions avec connexion par courriel et mot de passe.',
            'eyebrow': 'Portail de référence',
            'h1': 'Connexion au portail de référence.',
            'intro': "Connectez-vous avec votre courriel et votre mot de passe pour consulter votre code, vos références, vos crédits ou vos commissions. Au besoin, réinitialisez votre mot de passe depuis cette page.",
            'login_title': 'Connexion permanente',
            'login_intro': 'Utilisez le courriel associé à votre compte et votre mot de passe.',
            'login_button': 'Se connecter',
            'logged_out_note': 'Si vous perdez votre mot de passe, demandez un courriel de réinitialisation depuis le portail.',
            'logout_label': 'Se déconnecter',
        })
    else:
        copy.update({
            'h1': 'Access your referral portal.',
            'intro': 'Sign in with your email and password to review your code, your referrals, your credits, or your commission ledger. If needed, request a password reset email from the portal.',
            'login_title': 'Permanent access',
            'login_intro': 'Use the email address linked to your account and your password.',
            'login_button': 'Sign in',
            'logged_out_note': 'If you lose your password, request a password reset email from the portal.',
        })
    return copy


def referral_access_copy(lang):
    if lang == 'fr':
        return {
            'label': 'Accès au portail de référence',
            'title': 'Créer ou réinitialiser votre mot de passe | Opticable',
            'desc': 'Page Opticable dédiée à la création initiale du mot de passe et à la réinitialisation du mot de passe pour le portail de référence.',
            'eyebrow': 'Accès sécurisé',
            'h1': 'Créez ou réinitialisez votre mot de passe.',
            'intro': 'Cette page sert uniquement à configurer un nouveau mot de passe après une approbation partenaire ou une demande de réinitialisation.',
        }
    return {
        'label': 'Referral portal access',
        'title': 'Create or reset your password | Opticable',
        'desc': 'Dedicated Opticable page for first-time password setup and password reset for the referral portal.',
        'eyebrow': 'Secure access',
        'h1': 'Create or reset your password.',
        'intro': 'This page is only used to set a new password after partner approval or a password reset request.',
    }


def referral_admin_copy(lang):
    return REFERRAL_CONTENT['admin'][lang]


def referral_nav_items(lang):
    return [
        {
            'key': 'client',
            'label': referral_program_copy(lang, 'client')['label'],
            'href': routes[lang]['referral-program'],
            'copy': (
                'For clients and contacts who want future Opticable credit.'
                if lang == 'en' else
                'Pour les clients et contacts qui veulent accumuler un crédit Opticable.'
            ),
        },
        {
            'key': 'partner',
            'label': referral_program_copy(lang, 'partner')['label'],
            'href': routes[lang]['referral-partner-program'],
            'copy': (
                'For businesses and professionals sending repeat referrals.'
                if lang == 'en' else
                'Pour les entreprises et professionnels qui recommandent des projets récurrents.'
            ),
        },
        {
            'key': 'portal',
            'label': referral_portal_copy(lang)['label'],
            'href': routes[lang]['referral-portal'],
            'copy': (
                'Review your code, share link, referrals, and rewards.'
                if lang == 'en' else
                'Pour consulter votre code, votre lien de partage, vos références et vos récompenses.'
            ),
        },
        {
            'key': 'contact',
            'label': T[lang]['quote'],
            'href': routes[lang]['contact'],
            'copy': (
                'Use your referral code in the quote request.'
                if lang == 'en' else
                'Pour utiliser votre code de référence dans la demande de soumission.'
            ),
        },
    ]


def referral_nav_shell(lang, current_key):
    title = 'Navigate the referral pages' if lang == 'en' else 'Naviguer entre les pages de référence'
    items = ''.join(
        f'<a class="referral-nav-card{" is-current" if item["key"] == current_key else ""}" href="{item["href"]}"'
        f'{" aria-current=\"page\"" if item["key"] == current_key else ""}>'
        f'<strong>{esc(item["label"])}</strong><span>{esc(item["copy"])}</span></a>'
        for item in referral_nav_items(lang)
    )
    return f'<nav class="referral-nav" aria-label="{esc(title)}">{items}</nav>'


def referral_program_form_shell(lang, program_key):
    copy = referral_program_copy(lang, program_key)
    account_type = 'partner' if program_key == 'partner' else 'client'
    form_intro = (
        (
            'Create your account, choose a password, and open your portal right away.'
            if lang == 'en' else
            'Créez votre compte, choisissez un mot de passe et ouvrez votre portail immédiatement.'
        ) if program_key == 'client' else (
            'Submit your business details for review. Opticable will validate the request first, then create the partner account if approved.'
            if lang == 'en' else
            'Transmettez les coordonnées de votre entreprise pour révision. Opticable valide d’abord la demande, puis crée le compte partenaire si elle est approuvée.'
        )
    )
    fields = {
        'name': 'Full name' if lang == 'en' else 'Nom complet',
        'email': 'Email address' if lang == 'en' else 'Adresse courriel',
        'phone': 'Phone number' if lang == 'en' else 'Téléphone',
        'company': 'Company' if lang == 'en' else 'Entreprise',
        'website': 'Website' if lang == 'en' else 'Site web',
        'notes': 'How would you like to work with Opticable?' if lang == 'en' else 'Comment souhaitez-vous travailler avec Opticable ?',
        'password': 'Password' if lang == 'en' else 'Mot de passe',
        'password_confirm': 'Confirm password' if lang == 'en' else 'Confirmer le mot de passe',
    }
    payload = {
        'invalidEmail': 'Use a valid email address.' if lang == 'en' else 'Utilisez une adresse courriel valide.',
        'requiredField': 'Complete all required fields.' if lang == 'en' else 'Remplissez tous les champs obligatoires.',
        'requiredConsent': 'Accept the program terms before continuing.' if lang == 'en' else 'Acceptez les conditions du programme avant de continuer.',
        'invalidPassword': 'Use a password with at least 10 characters.' if lang == 'en' else 'Utilisez un mot de passe d’au moins 10 caractères.',
        'passwordMismatch': 'The two passwords must match.' if lang == 'en' else 'Les deux mots de passe doivent correspondre.',
        'genericError': 'The request could not be completed right now.' if lang == 'en' else "La demande n'a pas pu être complétée pour le moment.",
        'success': (
            'Your portal is ready. Opening it now.'
            if lang == 'en' else
            'Votre portail est prêt. Ouverture en cours.'
        ) if program_key == 'client' else (
            'Your partner application has been sent. Opticable will review it and contact you.'
            if lang == 'en' else
            'Votre demande partenaire a été transmise. Opticable la révisera et communiquera avec vous.'
        ),
        'duplicate': (
            'An account already exists for this email. Use the portal login or request a password reset email.'
            if lang == 'en' else
            'Un compte existe déjà pour cette adresse. Utilisez la connexion du portail ou demandez un courriel de réinitialisation.'
        ) if program_key == 'client' else (
            'A partner application or partner account already exists for this email. Opticable will review it.'
            if lang == 'en' else
            'Une demande partenaire ou un compte partenaire existe déjà pour cette adresse. Opticable la révisera.'
        ),
        'previewLabel': 'Go to the portal' if lang == 'en' else 'Accéder au portail',
    }
    terms_key = 'referral-partner-program-terms' if program_key == 'partner' else 'referral-program-terms'
    consent_label = (
        'I have read the program terms and privacy policy.'
        if lang == 'en' else
        "J'ai lu les conditions du programme et la politique de confidentialité."
    )
    website_field = (
        f'<label class="field"><span>{esc(fields["website"])}</span><input name="website" inputmode="url" autocomplete="url" /></label>'
        if program_key == 'partner' else ''
    )
    notes_field = (
        f'<label class="field"><span>{esc(fields["notes"])}</span><textarea name="notes"></textarea></label>'
        if program_key == 'partner' else ''
    )
    password_fields = (
        f'<label class="field"><span>{esc(fields["password"])}</span><input name="password" type="password" autocomplete="new-password" minlength="10" required /></label>'
        f'<label class="field"><span>{esc(fields["password_confirm"])}</span><input name="password_confirm" type="password" autocomplete="new-password" minlength="10" required /></label>'
    ) if program_key == 'client' else ''
    company_required = ' required' if program_key == 'partner' else ''
    company_required_copy = ' data-company-required="true"' if program_key == 'partner' else ''
    return (
        f'<div class="form-panel referral-apply-shell" data-referral-apply data-lang="{lang}" data-account-type="{account_type}" data-requires-password="{str(program_key == "client").lower()}" data-apply-url="/api/referrals/apply" data-portal-url="{routes[lang]["referral-portal"]}"{company_required_copy}>'
        f'<script type="application/json" data-referral-apply-copy>{json.dumps(payload, ensure_ascii=False)}</script>'
        f'<p class="eyebrow">{esc(copy["label"])}</p><h2>{esc(copy["form_title"])}</h2><p>{esc(form_intro)}</p>'
        f'<form class="referral-apply-form" data-referral-apply-form novalidate>'
        f'<div class="input-grid">'
        f'<label class="field"><span>{esc(fields["name"])}</span><input name="name" autocomplete="name" required /></label>'
        f'<label class="field"><span>{esc(fields["email"])}</span><input name="email" type="email" autocomplete="email" required /></label>'
        f'<label class="field"><span>{esc(fields["phone"])}</span><input name="phone" type="tel" autocomplete="tel" /></label>'
        f'<label class="field"><span>{esc(fields["company"])}</span><input name="company" autocomplete="organization"{company_required} /></label>'
        f'{website_field}'
        f'{password_fields}'
        f'</div>'
        f'{notes_field}'
        f'<div class="promo-checklist referral-checklist">'
        f'<label><input name="rules_attestation" type="checkbox" required />'
        f'<span class="promo-consent-copy"><span class="promo-consent-text">{esc(consent_label)}</span>'
        f'<span class="promo-consent-links"><a href="{routes[lang][terms_key]}">{esc(copy["terms_title"])}</a><span class="promo-consent-separator" aria-hidden="true">·</span><a href="{routes[lang]["privacy"]}">{esc(T[lang]["privacy"])}</a></span>'
        f'</span></label>'
        f'</div>'
        f'<button class="button button-primary" type="submit">{esc(copy["form_title"])}</button>'
        f'</form>'
        f'<div class="promo-inline-status" data-referral-apply-status hidden></div>'
        f'<div class="promo-inline-error" data-referral-apply-error hidden></div>'
        f'<div class="referral-magic-link" data-referral-apply-link hidden><a class="button button-secondary" data-referral-apply-link-anchor href="{routes[lang]["referral-portal"]}">{esc(payload["previewLabel"])}</a></div>'
        f'</div>'
    )


def referral_terms_body(lang, program_key):
    copy = referral_program_copy(lang, program_key)
    route_key = 'referral-partner-program' if program_key == 'partner' else 'referral-program'
    terms_route_key = 'referral-partner-program-terms' if program_key == 'partner' else 'referral-program-terms'
    breadcrumbs = [
        (T[lang]['home'], routes[lang]['home']),
        (copy['label'], routes[lang][route_key]),
        (copy['terms_title'], routes[lang][terms_route_key]),
    ]
    cards = ''.join(card(title, text) for title, text in copy['terms_sections'])
    return (
        breadcrumb_nav(breadcrumbs)
        + band_section(
            f'<div class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(copy["label"])}</p><h1>{esc(copy["terms_title"])}</h1><p>{esc(copy["terms_intro"])}</p></div></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(referral_nav_shell(lang, program_key), 'referral-nav-section')
        + band_section(f'<div class="grid-2">{cards}</div>', 'referral-terms-section')
    )


def referral_program_page_body(lang, program_key):
    copy = referral_program_copy(lang, program_key)
    other_key = 'partner' if program_key == 'client' else 'client'
    other_copy = referral_program_copy(lang, other_key)
    program_class = 'is-partner-program' if program_key == 'partner' else 'is-client-program'
    route_key = 'referral-partner-program' if program_key == 'partner' else 'referral-program'
    breadcrumbs = [(T[lang]['home'], routes[lang]['home']), (copy['label'], routes[lang][route_key])]
    steps = ''.join(
        f'<article class="timeline-step"><span>{index:02d}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>'
        for index, (title, text) in enumerate(copy['steps'], 1)
    )
    faq_html = ''.join(
        f'<details class="faq-item" open><summary>{esc(question)}</summary><p>{esc(answer)}</p></details>'
        for question, answer in copy['faqs']
    )
    comparison_list = ''.join(f'<li>{esc(item)}</li>' for item in copy['comparison_points'])
    portal_cta = 'Open the portal' if lang == 'en' else 'Ouvrir le portail'
    other_cta = (
        'See the Referral Partner Program'
        if (lang == 'en' and program_key == 'client') else
        ('See the Referral Program' if lang == 'en' else (
            'Voir le programme de partenaires référents'
            if program_key == 'client' else
            'Voir le programme de référence'
        ))
    )
    faq_title = 'Frequently asked questions' if lang == 'en' else 'Questions fréquentes'
    terms_cta = 'Read the terms' if lang == 'en' else 'Lire les conditions'
    terms_route = routes[lang]['referral-partner-program-terms' if program_key == 'partner' else 'referral-program-terms']
    return (
        f'<div class="referral-program-page {program_class}">'
        + breadcrumb_nav(breadcrumbs)
        + band_section(
            f'<div class="promo-hero-grid"><div class="page-hero-copy"><p class="eyebrow">{esc(copy["eyebrow"])}</p><h1>{esc(copy["h1"])}</h1><p>{esc(copy["intro"])}</p>'
            f'<div class="page-hero-actions"><a class="button button-primary" href="#referral-apply-{program_key}-{lang}">{esc(copy["form_title"])}</a><a class="button button-secondary" href="{routes[lang]["referral-portal"]}">{esc(portal_cta)}</a></div></div>'
            f'<aside class="page-hero-panel promo-visual-panel referral-program-visual"><p class="eyebrow">{esc(copy["comparison_title"])}</p><h2>{esc(copy["label"])}</h2><p>{esc(copy["comparison_copy"])}</p><ul class="check-list">{comparison_list}</ul><a class="button button-secondary" href="{routes[lang]["referral-partner-program" if program_key == "client" else "referral-program"]}">{esc(other_cta)}</a></aside></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(referral_nav_shell(lang, program_key), 'referral-nav-section')
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(copy["label"])}</p><h2>{esc(copy["steps_title"])}</h2><p>{esc(copy["steps_intro"])}</p></div><div class="timeline">{steps}</div>',
            'referral-steps-section',
        )
        + band_section(
            f'<div class="two-col"><div id="referral-apply-{program_key}-{lang}">{referral_program_form_shell(lang, program_key)}</div><div class="contact-panel referral-program-compare"><p class="eyebrow">{esc(other_copy["label"])}</p><h2>{esc(other_copy["label"])}</h2><p>{esc(other_copy["comparison_copy"])}</p><ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in other_copy["comparison_points"])}</ul><div class="hero-actions"><a class="button button-secondary" href="{routes[lang]["referral-partner-program" if program_key == "client" else "referral-program"]}">{esc(other_cta)}</a><a class="button button-secondary" href="{routes[lang]["contact"]}">{esc(T[lang]["quote"])}</a></div></div></div>',
            'referral-form-section',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">FAQ</p><h2>{esc(faq_title)}</h2><p>{esc(copy["faq_intro"])}</p></div><div class="faq-list">{faq_html}</div><div class="hero-actions"><a class="button button-secondary" href="{terms_route}">{esc(terms_cta)}</a></div>',
            'referral-faq-section',
        )
        + '</div>'
    )


def referral_portal_shell(lang):
    copy = referral_portal_copy(lang)
    portal_label = 'Referral Portal' if lang == 'en' else 'Portail de référence'
    portal_h1 = 'Access your referral portal.' if lang == 'en' else 'Connectez-vous à votre portail de référence.'
    portal_intro = (
        'Use your permanent portal login to review your code, your referrals, your credits, or your commission ledger.'
        if lang == 'en' else
        'Utilisez votre accès permanent pour consulter votre code, vos références, vos crédits ou votre registre de commissions.'
    )
    logout_label = 'Sign out' if lang == 'en' else 'Se déconnecter'
    payload = {
        'invalidEmail': 'Use a valid email address.' if lang == 'en' else 'Utilisez une adresse courriel valide.',
        'invalidPassword': 'Use a password with at least 10 characters.' if lang == 'en' else 'Utilisez un mot de passe d’au moins 10 caractères.',
        'passwordMismatch': 'The two passwords must match.' if lang == 'en' else 'Les deux mots de passe doivent correspondre.',
        'genericError': 'The portal request could not be completed right now.' if lang == 'en' else "La demande du portail n'a pas pu être traitée pour le moment.",
        'invalidCredentials': 'The email address or password is invalid.' if lang == 'en' else 'Le courriel ou le mot de passe est invalide.',
        'loginSent': 'If an account exists for this address, a password reset email has just been sent. Check your junk folder if needed.' if lang == 'en' else "Si un compte existe pour cette adresse, un courriel de réinitialisation du mot de passe vient d’être envoyé. Vérifiez aussi vos courriels indésirables au besoin.",
        'notSignedIn': 'Sign in with your email and password. If needed, request a password reset below.' if lang == 'en' else 'Connectez-vous avec votre courriel et votre mot de passe. Au besoin, utilisez la réinitialisation du mot de passe ci-dessous.',
        'authExpired': 'This reset link has expired. Request a new password reset email below.' if lang == 'en' else "Ce lien de réinitialisation a expiré. Demandez un nouveau courriel de réinitialisation ci-dessous.",
        'authUsed': 'This reset link has already been used. Request a new password reset email if needed.' if lang == 'en' else "Ce lien de réinitialisation a déjà été utilisé. Demandez un nouveau courriel de réinitialisation au besoin.",
        'authInvalid': 'This reset link is invalid. Request a new password reset email below.' if lang == 'en' else "Ce lien de réinitialisation est invalide. Demandez un nouveau courriel de réinitialisation ci-dessous.",
        'resetReady': 'Choose your new password below to finish restoring access.' if lang == 'en' else 'Choisissez votre nouveau mot de passe ci-dessous pour terminer la réinitialisation.',
        'shareCopied': 'Share link copied.' if lang == 'en' else 'Lien de partage copié.',
        'shareCopyError': 'Unable to copy the link automatically.' if lang == 'en' else "Impossible de copier le lien automatiquement.",
        'passwordSaved': 'Your password has been saved.' if lang == 'en' else 'Votre mot de passe a été enregistré.',
        'labels': {
            'accountTypes': {
                'client': 'Client' if lang == 'en' else 'Client',
                'partner': 'Partner' if lang == 'en' else 'Partenaire',
            },
            'programTypes': {
                'client': 'Referral Program' if lang == 'en' else 'Programme de référence',
                'partner': 'Referral Partner Program' if lang == 'en' else 'Programme de partenaires référents',
            },
            'accountStatuses': {
                'pending': 'Pending' if lang == 'en' else 'En attente',
                'active': 'Active' if lang == 'en' else 'Actif',
                'paused': 'Paused' if lang == 'en' else 'En pause',
                'rejected': 'Rejected' if lang == 'en' else 'Refusé',
            },
            'caseStatuses': {
                'new': 'New' if lang == 'en' else 'Nouveau',
                'quoted': 'Quoted' if lang == 'en' else 'Soumission envoyée',
                'won': 'Accepted' if lang == 'en' else 'Acceptée',
                'accepted': 'Accepted' if lang == 'en' else 'Acceptée',
                'completed_paid': 'Installed + paid' if lang == 'en' else 'Installé et payé',
                'member_paid': 'Member paid' if lang == 'en' else 'Membre payé',
                'void': 'Void' if lang == 'en' else 'Annulée',
            },
            'rewardStatuses': {
                'pending': 'Pending' if lang == 'en' else 'En attente',
                'earned': 'Earned' if lang == 'en' else 'Gagné',
                'settled': 'Settled' if lang == 'en' else 'Réglé',
                'void': 'Void' if lang == 'en' else 'Annulé',
            },
            'creditStatuses': {
                'reserved': 'Reserved' if lang == 'en' else 'Réservé',
                'applied': 'Applied' if lang == 'en' else 'Appliqué',
                'released': 'Released' if lang == 'en' else 'Libéré',
                'void': 'Void' if lang == 'en' else 'Annulé',
            },
        },
        'auth': {
            'loginEyebrow': 'Sign in' if lang == 'en' else 'Connexion',
            'loginTitle': 'Sign in to your portal' if lang == 'en' else 'Se connecter au portail',
            'loginIntro': 'Use the email address linked to your referral account and your password.' if lang == 'en' else 'Utilisez le courriel lié à votre compte et votre mot de passe.',
            'recoveryEyebrow': 'Password reset' if lang == 'en' else 'Mot de passe oublié',
            'recoveryTitle': 'Forgot your password?' if lang == 'en' else 'Réinitialiser votre mot de passe',
            'recoveryIntro': 'Enter the email linked to your account. If the account exists, Opticable will send you a password reset email.' if lang == 'en' else 'Entrez le courriel lié à votre compte. Si le compte existe, Opticable vous enverra un courriel de réinitialisation du mot de passe.',
            'emailLabel': 'Email address' if lang == 'en' else 'Adresse courriel',
            'passwordLabel': 'Password' if lang == 'en' else 'Mot de passe',
            'loginButton': 'Sign in' if lang == 'en' else 'Se connecter',
            'recoveryButton': 'Send reset email' if lang == 'en' else 'Envoyer le courriel de réinitialisation',
        },
        'portal': {
            'currentCode': 'Referral code' if lang == 'en' else 'Code de partage',
            'creditCode': 'Member code' if lang == 'en' else 'Code membre',
            'shareLink': 'Share link' if lang == 'en' else 'Lien de partage',
            'contactEmail': 'Portal email' if lang == 'en' else 'Courriel du portail',
            'copyButton': 'Copy' if lang == 'en' else 'Copier',
            'contactCta': 'Request a quote' if lang == 'en' else 'Demander une soumission',
        },
        'creditPanel': {
            'eyebrow': 'Client credit' if lang == 'en' else 'Crédit client',
            'title': 'Apply your credit with Opticable' if lang == 'en' else 'Appliquez votre crédit avec Opticable',
            'intro': 'Call Opticable, provide your member code, and confirm the amount you want applied. Opticable validates the amount and deducts it from your balance.' if lang == 'en' else 'Communiquez avec Opticable, donnez votre code membre et confirmez le montant à appliquer. Opticable valide ensuite le montant et le déduit de votre solde.',
            'availableLabel': 'Available balance' if lang == 'en' else 'Solde disponible',
            'capLabel': 'Maximum applicable' if lang == 'en' else 'Maximum applicable',
            'selectedCodeLabel': 'Member code' if lang == 'en' else 'Code membre',
            'manualTitle': 'How this works' if lang == 'en' else 'Fonctionnement',
            'manualCopy': 'This code is not for public quote forms. Keep it for direct discussions with Opticable when you want to apply part of your available balance.' if lang == 'en' else 'Ce code ne sert pas dans les formulaires publics. Gardez-le pour vos échanges directs avec Opticable lorsque vous souhaitez appliquer une partie de votre solde disponible.',
        },
        'passwordPanel': {
            'eyebrow': 'Account security' if lang == 'en' else 'Sécurité du compte',
            'createTitle': 'Create your permanent password' if lang == 'en' else 'Créez votre mot de passe permanent',
            'changeTitle': 'Change your password' if lang == 'en' else 'Modifiez votre mot de passe',
            'createIntro': 'Use a password of at least 10 characters to activate your permanent portal access.' if lang == 'en' else 'Utilisez un mot de passe d’au moins 10 caractères pour activer votre accès permanent au portail.',
            'changeIntro': 'Keep a permanent password for your portal. If you lose it, request a password reset email from the sign-in screen.' if lang == 'en' else 'Conservez un mot de passe permanent pour votre portail. Si vous le perdez, demandez un courriel de réinitialisation depuis l’écran de connexion.',
            'resetTitle': 'Choose your new password' if lang == 'en' else 'Choisissez votre nouveau mot de passe',
            'resetIntro': 'This secure reset session lets you choose a new permanent password without entering the current one.' if lang == 'en' else 'Cette session sécurisée vous permet de choisir un nouveau mot de passe permanent sans entrer l’ancien.',
            'currentLabel': 'Current password' if lang == 'en' else 'Mot de passe actuel',
            'newLabel': 'New password' if lang == 'en' else 'Nouveau mot de passe',
            'confirmLabel': 'Confirm new password' if lang == 'en' else 'Confirmer le nouveau mot de passe',
            'createButton': 'Save my password' if lang == 'en' else 'Enregistrer mon mot de passe',
            'changeButton': 'Update my password' if lang == 'en' else 'Mettre à jour mon mot de passe',
            'resetButton': 'Save the new password' if lang == 'en' else 'Enregistrer le nouveau mot de passe',
        },
        'views': {
            'client': {
                'bannerEyebrow': 'Referral Program' if lang == 'en' else 'Programme de référence',
                'bannerTitle': 'Track your Opticable credit clearly.' if lang == 'en' else 'Suivez votre crédit Opticable clairement.',
                'bannerCopy': 'This portal shows the referrals tied to your code, the eligible subtotals, and the balance you can apply later with Opticable. A project must reach CAD 5,000 before taxes to earn credit, and a maximum of CAD 1,000 can be applied to one quote or project.' if lang == 'en' else 'Ce portail affiche les références liées à votre code, les sous-totaux admissibles et le solde que vous pourrez appliquer plus tard avec Opticable. Un projet doit atteindre 5 000 $ avant taxes pour générer un crédit, et un maximum de 1 000 $ peut être appliqué à une même soumission ou à un même projet.',
                'stats': {
                    'total': 'Linked cases' if lang == 'en' else 'Dossiers liés',
                    'open': 'Active cases' if lang == 'en' else 'Dossiers en cours',
                    'completed': 'Completed + paid' if lang == 'en' else 'Dossiers payés',
                    'primary': 'Available credit' if lang == 'en' else 'Crédit disponible',
                    'secondary': 'Total earned' if lang == 'en' else 'Total gagné',
                    'tertiary': 'Maximum applicable' if lang == 'en' else 'Maximum applicable',
                },
                'summaryNote': 'The cards above summarize your current position. The tables below show each linked case and each credit movement line by line.' if lang == 'en' else 'Les bulles ci-dessus résument votre situation actuelle. Les tableaux ci-dessous détaillent chaque dossier lié à votre code et chaque mouvement de crédit.',
                'helpTitle': 'What you can see here' if lang == 'en' else 'Ce que vous voyez ici',
                'help': [
                    'Every linked case comes from a quote or project that used your code.' if lang == 'en' else 'Chaque dossier lié provient d’une soumission ou d’un projet ayant utilisé votre code.',
                    'Available credit is the amount you can still ask Opticable to apply on a future quote or project.' if lang == 'en' else 'Le crédit disponible correspond au montant que vous pouvez encore demander à Opticable d’appliquer sur une future soumission ou un futur projet.',
                    'Use the member code shown in this portal only when speaking directly with Opticable. It is not a public referral code.' if lang == 'en' else 'Utilisez le code membre affiché dans ce portail uniquement lors d’un échange direct avec Opticable. Ce n’est pas un code public de référence.',
                    'The share link opens the quote page, but the referred contact must still enter your referral code on the first quote request.' if lang == 'en' else 'Le lien de partage ouvre la page de soumission, mais le contact référé doit tout de même entrer votre code de référence lors de la première demande.',
                    'A project must reach CAD 5,000 before taxes to earn credit, and a maximum of CAD 1,000 can be applied to one quote or project even if your balance is higher.' if lang == 'en' else 'Un projet doit atteindre 5 000 $ avant taxes pour générer un crédit, et un maximum de 1 000 $ peut être appliqué à une même soumission ou à un même projet, même si votre solde est plus élevé.',
                ],
                'referralsTitle': 'Linked cases' if lang == 'en' else 'Dossiers liés à votre code',
                'referralsIntro': 'Each line below corresponds to a quote or project tied to your public referral code.' if lang == 'en' else 'Chaque ligne ci-dessous correspond à une soumission ou à un projet rattaché à votre code de référence public.',
                'rewardsTitle': 'Credit ledger' if lang == 'en' else 'Mouvements de crédit',
                'rewardsIntro': 'This ledger shows credit earned through referrals and balance adjustments confirmed in your portal.' if lang == 'en' else 'Ce registre montre les crédits gagnés grâce aux références et les ajustements de solde confirmés dans votre portail.',
                'amountLabel': 'Credit' if lang == 'en' else 'Crédit',
            },
            'partner': {
                'bannerEyebrow': 'Referral Partner Program' if lang == 'en' else 'Programme de partenaires référents',
                'bannerTitle': 'Track your commissions and referred projects.' if lang == 'en' else 'Suivez vos commissions et vos projets référés.',
                'bannerCopy': 'This portal shows the referred cases tied to your code, the tracked subtotals, and the commission amounts earned or pending. Once Opticable confirms the transfer, the commission is marked as settled here.' if lang == 'en' else 'Ce portail affiche les dossiers référés liés à votre code, les sous-totaux suivis et les montants de commission gagnés ou en attente. Après confirmation du transfert par Opticable, la commission est marquée comme réglée ici.',
                'stats': {
                    'total': 'Linked cases' if lang == 'en' else 'Dossiers liés',
                    'open': 'Active cases' if lang == 'en' else 'Dossiers en cours',
                    'completed': 'Completed + paid' if lang == 'en' else 'Dossiers payés',
                    'primary': 'Pending commissions' if lang == 'en' else 'Commissions en attente',
                    'secondary': 'Settled commissions' if lang == 'en' else 'Commissions réglées',
                    'tertiary': 'Tracked subtotal' if lang == 'en' else 'Sous-total suivi',
                },
                'summaryNote': 'The cards above summarize your active file count, pending commissions, and tracked subtotals. The tables below show the linked cases and the commission ledger.' if lang == 'en' else 'Les bulles ci-dessus résument vos dossiers actifs, vos commissions en attente et les sous-totaux suivis. Les tableaux ci-dessous détaillent les dossiers liés et le registre des commissions.',
                'helpTitle': 'What you can see here' if lang == 'en' else 'Ce que vous voyez ici',
                'help': [
                    'Tracked subtotal shows the total value currently associated with the cases tied to your code.' if lang == 'en' else 'Le sous-total suivi représente la valeur actuellement associée aux dossiers liés à votre code.',
                    'Pending commissions are earned but not yet marked as settled.' if lang == 'en' else 'Les commissions en attente sont gagnées, mais pas encore réglées.',
                    'Use the member code shown here only when speaking directly with Opticable about a payout or an account adjustment. It is not a public referral code.' if lang == 'en' else 'Utilisez le code membre affiché ici uniquement lors d’un échange direct avec Opticable au sujet d’un règlement ou d’un ajustement. Ce n’est pas un code public de référence.',
                    'The share link opens the quote page, but the referred contact must still enter your referral code on the first quote request.' if lang == 'en' else 'Le lien de partage ouvre la page de soumission, mais le contact référé doit tout de même entrer votre code de référence lors de la première demande.',
                    'To request a payout, contact Opticable directly. Once the transfer is sent, Opticable marks the commission as settled in this portal.' if lang == 'en' else 'Pour demander un règlement, communiquez directement avec Opticable. Une fois le transfert envoyé, Opticable marque la commission comme réglée dans ce portail.',
                    'The commission ledger stays separate from the referred-client quote details.' if lang == 'en' else 'Le registre des commissions demeure distinct des détails complets de la soumission du client référé.',
                ],
                'referralsTitle': 'Linked cases' if lang == 'en' else 'Dossiers liés à votre code',
                'referralsIntro': 'Each line below corresponds to a quote or project tied to your public referral code.' if lang == 'en' else 'Chaque ligne ci-dessous correspond à une soumission ou à un projet rattaché à votre code de référence public.',
                'rewardsTitle': 'Commission ledger' if lang == 'en' else 'Registre des commissions',
                'rewardsIntro': 'This ledger shows earned commissions and the amounts already marked as settled in your portal.' if lang == 'en' else 'Ce registre montre les commissions gagnées et les montants déjà marqués comme réglés dans votre portail.',
                'amountLabel': 'Commission' if lang == 'en' else 'Commission',
            },
        },
        'tables': {
            'case': 'Case' if lang == 'en' else 'Dossier',
            'reference': 'Reference' if lang == 'en' else 'Référence',
            'status': 'Status' if lang == 'en' else 'Statut',
            'created': 'Created' if lang == 'en' else 'Créé',
            'subtotal': 'Subtotal' if lang == 'en' else 'Sous-total',
            'amount': 'Amount' if lang == 'en' else 'Montant',
            'note': 'Note' if lang == 'en' else 'Note',
        },
            'ledgerStatuses': {
                'credit_earned': 'Credit earned' if lang == 'en' else 'Crédit gagné',
                'credit_settled': 'Credit settled' if lang == 'en' else 'Crédit réglé',
                'credit_void': 'Credit voided' if lang == 'en' else 'Crédit annulé',
                'balance_adjusted': 'Balance adjusted' if lang == 'en' else 'Solde ajusté',
            },
    }
    login_label = 'Sign in' if lang == 'en' else 'Se connecter'
    return (
        f'<div class="form-panel referral-portal-shell" data-referral-portal data-lang="{lang}" data-login-url="/api/referrals/auth/login" data-request-link-url="/api/referrals/auth/request-reset" data-password-url="/api/referrals/auth/password" data-portal-url="/api/referrals/portal" data-access-url="{routes[lang]["referral-access"]}" data-logout-url="/api/referrals/auth/logout?lang={lang}" data-contact-url="{routes[lang]["contact"]}">'
        f'<script type="application/json" data-referral-portal-copy>{json.dumps(payload, ensure_ascii=False)}</script>'
        f'<div class="referral-portal-auth" data-referral-portal-auth>'
        f'<p class="eyebrow">{esc(portal_label)}</p><h2>{esc(portal_h1)}</h2><p>{esc(portal_intro)}</p>'
        f'<div class="two-col referral-auth-grid">'
        f'<div class="contact-panel referral-auth-card">'
        f'<p class="eyebrow">{esc(payload["auth"]["loginEyebrow"])}</p><h2>{esc(payload["auth"]["loginTitle"])}</h2><p>{esc(payload["auth"]["loginIntro"])}</p>'
        f'<form class="referral-portal-login-form" data-referral-portal-login novalidate>'
        f'<label class="field"><span>{esc(payload["auth"]["emailLabel"])}</span><input name="email" type="email" autocomplete="email" required /></label>'
        f'<label class="field"><span>{esc(payload["auth"]["passwordLabel"])}</span><input name="password" type="password" autocomplete="current-password" required /></label>'
        f'<button class="button button-primary" type="submit">{esc(login_label)}</button>'
        f'</form></div>'
        f'<div class="contact-panel referral-auth-card">'
        f'<p class="eyebrow">{esc(payload["auth"]["recoveryEyebrow"])}</p><h2>{esc(payload["auth"]["recoveryTitle"])}</h2><p>{esc(payload["auth"]["recoveryIntro"])}</p>'
        f'<form class="referral-portal-login-form" data-referral-portal-link-form novalidate>'
        f'<label class="field"><span>{esc(payload["auth"]["emailLabel"])}</span><input name="email" type="email" autocomplete="email" required /></label>'
        f'<button class="button button-secondary" type="submit">{esc(payload["auth"]["recoveryButton"])}</button>'
        f'</form></div>'
        f'</div>'
        f'<div class="promo-inline-status" data-referral-portal-status hidden></div><div class="promo-inline-error" data-referral-portal-error hidden></div>'
        f'</div>'
        f'<div class="referral-portal-dashboard" data-referral-portal-dashboard hidden>'
        f'<div class="referral-portal-header"><div class="referral-portal-copy"><p class="eyebrow">{esc(portal_label)}</p><h2 data-referral-portal-name></h2><p data-referral-portal-meta></p></div><a class="button button-secondary" data-referral-portal-logout href="/api/referrals/auth/logout?lang={lang}">{esc(logout_label)}</a></div>'
        f'<div class="contact-panel referral-program-banner"><p class="eyebrow" data-referral-portal-banner-eyebrow>—</p><h2 data-referral-portal-banner-title>—</h2><p data-referral-portal-banner-copy>—</p><div class="hero-actions"><a class="button button-secondary" href="{routes[lang]["contact"]}">{esc(payload["portal"]["contactCta"])}</a></div></div>'
        f'<div class="promo-admin-summary referral-portal-stats">'
        f'<div class="detail-item"><strong data-referral-stat-label-total>{esc(payload["tables"]["case"])}</strong><p data-referral-stat-total>0</p></div>'
        f'<div class="detail-item"><strong data-referral-stat-label-open>—</strong><p data-referral-stat-open>0</p></div>'
        f'<div class="detail-item"><strong data-referral-stat-label-completed>—</strong><p data-referral-stat-completed>0</p></div>'
        f'<div class="detail-item"><strong data-referral-stat-label-primary>—</strong><p data-referral-stat-primary>0.00</p></div>'
        f'<div class="detail-item"><strong data-referral-stat-label-secondary>—</strong><p data-referral-stat-secondary>0.00</p></div>'
        f'<div class="detail-item"><strong data-referral-stat-label-tertiary>—</strong><p data-referral-stat-tertiary>0.00</p></div>'
        f'</div>'
        f'<p class="form-note referral-summary-note" data-referral-portal-summary-note>—</p>'
        f'<div class="promo-admin-meta referral-portal-meta-grid">'
        f'<div class="detail-item"><strong>{esc(payload["portal"]["currentCode"])}</strong><p class="promo-admin-code" data-referral-portal-code>—</p></div>'
        f'<div class="detail-item" data-referral-credit-meta hidden><strong>{esc(payload["portal"]["creditCode"])}</strong><p class="promo-admin-code" data-referral-portal-credit-code>—</p></div>'
        f'<div class="detail-item referral-share-item"><strong>{esc(payload["portal"]["shareLink"])}</strong><div class="referral-share-row"><a class="text-link referral-share-link" data-referral-portal-share href="{routes[lang]["contact"]}">—</a><button class="button button-secondary referral-copy-button" type="button" data-referral-portal-share-copy>{esc(payload["portal"]["copyButton"])}</button></div><span class="referral-inline-note" data-referral-portal-share-status hidden></span></div>'
        f'<div class="detail-item"><strong>{esc(payload["portal"]["contactEmail"])}</strong><p data-referral-portal-email>—</p></div>'
        f'</div>'
        f'<div class="contact-panel referral-portal-help"><h2 data-referral-help-title>—</h2><ul class="check-list referral-help-list" data-referral-help-list></ul></div>'
        f'<div class="contact-panel referral-credit-panel" data-referral-credit-panel hidden><p class="eyebrow">{esc(payload["creditPanel"]["eyebrow"])}</p><h2>{esc(payload["creditPanel"]["title"])}</h2><p>{esc(payload["creditPanel"]["intro"])}</p><div class="promo-admin-meta referral-credit-meta"><div class="detail-item"><strong>{esc(payload["creditPanel"]["selectedCodeLabel"])}</strong><p class="promo-admin-code" data-referral-credit-panel-code>—</p></div><div class="detail-item"><strong>{esc(payload["creditPanel"]["availableLabel"])}</strong><p data-referral-credit-panel-balance>0.00</p></div><div class="detail-item"><strong>{esc(payload["creditPanel"]["capLabel"])}</strong><p data-referral-credit-panel-cap>1000.00</p></div></div><div class="detail-item"><strong>{esc(payload["creditPanel"]["manualTitle"])}</strong><p data-referral-credit-panel-instruction>{esc(payload["creditPanel"]["manualCopy"])}</p></div></div>'
        f'<div class="two-col referral-portal-grids"><div class="contact-panel"><h2 data-referral-portal-referrals-title>—</h2><p class="form-note referral-section-intro" data-referral-portal-referrals-intro>—</p><div class="promo-admin-table-shell"><table class="promo-admin-table referral-mini-table referral-portal-cases-table"><thead><tr><th>{esc(payload["tables"]["case"])}</th><th>{esc(payload["tables"]["reference"])}</th><th>{esc(payload["tables"]["status"])}</th><th>{esc(payload["tables"]["created"])}</th><th>{esc(payload["tables"]["subtotal"])}</th><th data-referral-portal-amount-label>{esc(payload["tables"]["amount"])}</th></tr></thead><tbody data-referral-portal-referrals></tbody></table></div></div><div class="contact-panel"><h2 data-referral-portal-rewards-title>—</h2><p class="form-note referral-section-intro" data-referral-portal-rewards-intro>—</p><div class="promo-admin-table-shell"><table class="promo-admin-table referral-mini-table referral-portal-rewards-table"><thead><tr><th>ID</th><th>{esc(payload["tables"]["status"])}</th><th>{esc(payload["tables"]["amount"])}</th><th>{esc(payload["tables"]["created"])}</th><th>{esc(payload["tables"]["note"])}</th></tr></thead><tbody data-referral-portal-rewards></tbody></table></div></div></div>'
        f'<div class="contact-panel referral-portal-security"><p class="eyebrow">{esc(payload["passwordPanel"]["eyebrow"])}</p><h2 data-referral-password-title>—</h2><p data-referral-password-intro>—</p><form class="referral-password-form" data-referral-password-form novalidate><div class="input-grid referral-password-grid"><label class="field" data-referral-password-current-wrap hidden><span>{esc(payload["passwordPanel"]["currentLabel"])}</span><input name="current_password" type="password" autocomplete="current-password" /></label><label class="field"><span>{esc(payload["passwordPanel"]["newLabel"])}</span><input name="new_password" type="password" autocomplete="new-password" minlength="10" required /></label><label class="field"><span>{esc(payload["passwordPanel"]["confirmLabel"])}</span><input name="confirm_password" type="password" autocomplete="new-password" minlength="10" required /></label></div><button class="button button-primary" type="submit" data-referral-password-submit>{esc(payload["passwordPanel"]["createButton"])}</button></form><div class="promo-inline-status" data-referral-password-status hidden></div><div class="promo-inline-error" data-referral-password-error hidden></div></div>'
        f'</div></div>'
    )


def referral_access_shell(lang):
    copy = referral_access_copy(lang)
    payload = {
        'invalidEmail': 'Use a valid email address.' if lang == 'en' else 'Utilisez une adresse courriel valide.',
        'invalidPassword': 'Use a password with at least 10 characters.' if lang == 'en' else 'Utilisez un mot de passe d’au moins 10 caractères.',
        'passwordMismatch': 'The two passwords must match.' if lang == 'en' else 'Les deux mots de passe doivent correspondre.',
        'genericError': 'The access request could not be completed right now.' if lang == 'en' else "La demande d'accès n'a pas pu être traitée pour le moment.",
        'passwordSaved': 'Your password has been saved. Opening your portal now.' if lang == 'en' else 'Votre mot de passe a été enregistré. Ouverture du portail en cours.',
        'notReady': 'This page must be opened from a valid setup or reset email. You can request a new password reset email below.' if lang == 'en' else 'Cette page doit être ouverte à partir d’un courriel valide de configuration ou de réinitialisation. Vous pouvez demander un nouveau courriel ci-dessous.',
        'authExpired': 'This setup or reset link has expired. Request a new password reset email below.' if lang == 'en' else 'Ce lien de configuration ou de réinitialisation a expiré. Demandez un nouveau courriel de réinitialisation ci-dessous.',
        'authUsed': 'This setup or reset link has already been used. Request a new password reset email if needed.' if lang == 'en' else 'Ce lien de configuration ou de réinitialisation a déjà été utilisé. Demandez un nouveau courriel de réinitialisation au besoin.',
        'authInvalid': 'This setup or reset link is invalid. Request a new password reset email below.' if lang == 'en' else 'Ce lien de configuration ou de réinitialisation est invalide. Demandez un nouveau courriel de réinitialisation ci-dessous.',
        'requestSent': 'If an account exists for this address, a password reset email has just been sent. Check your junk folder if needed.' if lang == 'en' else "Si un compte existe pour cette adresse, un courriel de réinitialisation du mot de passe vient d’être envoyé. Vérifiez aussi vos courriels indésirables au besoin.",
        'accountReady': 'Create the password that will be linked to this account.' if lang == 'en' else 'Créez le mot de passe qui sera associé à ce compte.',
        'requestEyebrow': 'Need a new email?' if lang == 'en' else 'Besoin d’un nouveau courriel ?',
        'requestTitle': 'Request a new reset email' if lang == 'en' else 'Demander un nouveau courriel de réinitialisation',
        'requestIntro': 'Enter the email address linked to your referral account and we will send a fresh password reset email if the account exists.' if lang == 'en' else 'Entrez le courriel associé à votre compte de référence et nous enverrons un nouveau courriel de réinitialisation si le compte existe.',
        'emailLabel': 'Email address' if lang == 'en' else 'Adresse courriel',
        'requestButton': 'Send the reset email' if lang == 'en' else 'Envoyer le courriel de réinitialisation',
        'passwordEyebrow': 'Password setup' if lang == 'en' else 'Configuration du mot de passe',
        'passwordTitle': 'Choose your new password' if lang == 'en' else 'Choisissez votre nouveau mot de passe',
        'passwordIntro': 'This password will be required for future portal sign-ins.' if lang == 'en' else 'Ce mot de passe sera requis pour les prochaines connexions au portail.',
        'newPasswordLabel': 'New password' if lang == 'en' else 'Nouveau mot de passe',
        'confirmPasswordLabel': 'Confirm the new password' if lang == 'en' else 'Confirmer le nouveau mot de passe',
        'passwordButton': 'Save the password' if lang == 'en' else 'Enregistrer le mot de passe',
        'openPortal': 'Open the portal' if lang == 'en' else 'Ouvrir le portail',
        'signedInAs': 'Account ready' if lang == 'en' else 'Compte prêt',
    }
    return (
        f'<div class="form-panel referral-access-shell" data-referral-access data-lang="{lang}" data-request-link-url="/api/referrals/auth/request-reset" data-password-url="/api/referrals/auth/password" data-portal-url="/api/referrals/portal" data-portal-page-url="{routes[lang]["referral-portal"]}" data-access-url="{routes[lang]["referral-access"]}">'
        f'<script type="application/json" data-referral-access-copy>{json.dumps(payload, ensure_ascii=False)}</script>'
        f'<div class="contact-panel referral-access-card">'
        f'<p class="eyebrow">{esc(copy["eyebrow"])}</p><h2>{esc(copy["h1"])}</h2><p>{esc(copy["intro"])}</p>'
        f'<div class="promo-inline-status" data-referral-access-status hidden></div><div class="promo-inline-error" data-referral-access-error hidden></div>'
        f'<div class="referral-access-ready" data-referral-access-ready hidden>'
        f'<p class="form-note" data-referral-access-account>—</p>'
        f'<form class="referral-password-form" data-referral-access-password-form novalidate>'
        f'<div class="input-grid referral-password-grid">'
        f'<label class="field"><span>{esc(payload["newPasswordLabel"])}</span><input name="new_password" type="password" autocomplete="new-password" minlength="10" required /></label>'
        f'<label class="field"><span>{esc(payload["confirmPasswordLabel"])}</span><input name="confirm_password" type="password" autocomplete="new-password" minlength="10" required /></label>'
        f'</div>'
        f'<button class="button button-primary" type="submit">{esc(payload["passwordButton"])}</button>'
        f'</form>'
        f'<div class="promo-inline-status" data-referral-access-password-status hidden></div><div class="promo-inline-error" data-referral-access-password-error hidden></div>'
        f'</div>'
        f'<div class="referral-access-request" data-referral-access-request>'
        f'<p class="eyebrow">{esc(payload["requestEyebrow"])}</p><h3>{esc(payload["requestTitle"])}</h3><p>{esc(payload["requestIntro"])}</p>'
        f'<form class="referral-portal-login-form" data-referral-access-request-form novalidate>'
        f'<label class="field"><span>{esc(payload["emailLabel"])}</span><input name="email" type="email" autocomplete="email" required /></label>'
        f'<button class="button button-secondary" type="submit">{esc(payload["requestButton"])}</button>'
        f'</form>'
        f'<div class="hero-actions"><a class="button button-secondary" href="{routes[lang]["referral-portal"]}">{esc(payload["openPortal"])}</a></div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )


def referral_admin_shell(lang):
    copy = referral_admin_copy(lang)
    payload = {
        'genericError': 'The referral admin request could not be completed.' if lang == 'en' else "La demande d'administration des références n'a pas pu être traitée.",
        'loading': 'Loading…' if lang == 'en' else 'Chargement…',
        'summary': {
            'activeAccounts': 'Active accounts' if lang == 'en' else 'Comptes actifs',
            'pendingPartners': 'Pending partner applications' if lang == 'en' else 'Demandes partenaires en attente',
            'openCases': 'Open cases' if lang == 'en' else 'Dossiers ouverts',
            'pendingPayouts': 'Pending payouts' if lang == 'en' else 'Paiements en attente',
        },
        'labels': {
            'accountTypes': {
                'client': 'Client' if lang == 'en' else 'Client',
                'partner': 'Partner' if lang == 'en' else 'Partenaire',
            },
            'accountStatuses': {
                'pending': 'Pending' if lang == 'en' else 'En attente',
                'active': 'Active' if lang == 'en' else 'Actif',
                'paused': 'Paused' if lang == 'en' else 'En pause',
                'rejected': 'Rejected' if lang == 'en' else 'Refusé',
            },
            'caseStatuses': {
                'new': 'New' if lang == 'en' else 'Nouveau',
                'quoted': 'Quoted' if lang == 'en' else 'Soumission envoyée',
                'won': 'Accepted' if lang == 'en' else 'Acceptée',
                'accepted': 'Accepted' if lang == 'en' else 'Acceptée',
                'completed_paid': 'Installed + paid' if lang == 'en' else 'Installé et payé',
                'member_paid': 'Member paid' if lang == 'en' else 'Membre payé',
                'void': 'Void' if lang == 'en' else 'Annulé',
            },
            'rewardTypes': {
                'credit': 'Credit' if lang == 'en' else 'Crédit',
                'payout': 'Payout' if lang == 'en' else 'Paiement',
            },
            'rewardStatuses': {
                'pending': 'Pending' if lang == 'en' else 'En attente',
                'earned': 'Earned' if lang == 'en' else 'Gagné',
                'settled': 'Settled' if lang == 'en' else 'Réglé',
                'void': 'Void' if lang == 'en' else 'Annulé',
            },
            'applicationStatuses': {
                'pending': 'Pending review' if lang == 'en' else 'À réviser',
                'reviewed': 'Reviewed' if lang == 'en' else 'Révisée',
                'approved': 'Approved' if lang == 'en' else 'Approuvée',
                'rejected': 'Rejected' if lang == 'en' else 'Refusée',
                'void': 'Deleted' if lang == 'en' else 'Supprimée',
            },
            'caseIdLabel': 'Project ID' if lang == 'en' else 'Projet ID',
        },
        'actions': {
            'refresh': 'Refresh' if lang == 'en' else 'Actualiser',
            'exportAccounts': 'Export accounts CSV' if lang == 'en' else 'Exporter comptes CSV',
            'exportCases': 'Export cases CSV' if lang == 'en' else 'Exporter dossiers CSV',
            'exportRewards': 'Export rewards CSV' if lang == 'en' else 'Exporter récompenses CSV',
            'apply': 'Apply' if lang == 'en' else 'Appliquer',
            'adjustCredit': 'Adjust credit' if lang == 'en' else 'Ajuster le crédit',
            'adjustReward': 'Adjust credit / commission' if lang == 'en' else 'Ajuster crédit / commission',
            'settle': 'Settle' if lang == 'en' else 'Régler',
            'createAccount': 'Create account' if lang == 'en' else 'Créer le compte',
            'reject': 'Reject' if lang == 'en' else 'Refuser',
            'delete': 'Delete' if lang == 'en' else 'Supprimer',
            'exportOne': 'Download file' if lang == 'en' else 'Télécharger la fiche',
            'resetAccess': 'Send password reset' if lang == 'en' else 'Envoyer la réinitialisation',
            'saveAccount': 'Add account' if lang == 'en' else 'Ajouter le compte',
            'viewDetails': 'View details' if lang == 'en' else 'Voir la fiche',
            'saveCase': 'Add project' if lang == 'en' else 'Ajouter le projet',
            'updateCase': 'Update project' if lang == 'en' else 'Mettre à jour le projet',
            'cancelEdit': 'Cancel' if lang == 'en' else 'Annuler',
            'editCase': 'Edit project' if lang == 'en' else 'Modifier le projet',
        },
        'messages': {
            'accountCreated': 'Account created successfully.' if lang == 'en' else 'Compte créé avec succès.',
            'applicationUpdated': 'Partner application updated.' if lang == 'en' else 'Demande partenaire mise à jour.',
            'applicationDeleted': 'Partner application deleted.' if lang == 'en' else 'Demande partenaire supprimée.',
            'confirmDeleteApplication': 'Delete this partner application?' if lang == 'en' else 'Supprimer cette demande partenaire ?',
            'accountUpdated': 'Account updated.' if lang == 'en' else 'Compte mis à jour.',
            'accessReset': 'A password reset email was sent if the account is active.' if lang == 'en' else "Un courriel de réinitialisation du mot de passe a été envoyé si le compte est actif.",
            'confirmDeleteAccount': 'Delete this account and all related referral data?' if lang == 'en' else 'Supprimer ce compte et toutes les données de référence liées ?',
            'accountDeleted': 'Account deleted.' if lang == 'en' else 'Compte supprimé.',
            'confirmDeleteCase': 'Delete this project and its linked reward data?' if lang == 'en' else 'Supprimer ce projet et ses récompenses liées ?',
            'caseDeleted': 'Project deleted.' if lang == 'en' else 'Projet supprimé.',
            'creditAdjusted': 'Client credit balance adjusted.' if lang == 'en' else 'Le solde du crédit client a été ajusté.',
            'creditAdjustPrompt': 'Enter a positive amount to add or a negative amount to deduct.' if lang == 'en' else 'Entrez un montant positif pour ajouter ou négatif pour déduire.',
            'creditAdjustNotePrompt': 'Optional note saved in the admin audit trail.' if lang == 'en' else 'Note optionnelle conservée dans le journal admin.',
            'caseCreated': 'Manual project added.' if lang == 'en' else 'Projet manuel ajouté.',
            'caseUpdated': 'Project updated.' if lang == 'en' else 'Projet mis à jour.',
            'caseCreateRequired': 'Referral code, name, email, and company are required.' if lang == 'en' else 'Le code de référence, le nom, le courriel et l’entreprise sont obligatoires.',
            'caseCreateSubtotalRequired': 'A completed and paid project needs a subtotal.' if lang == 'en' else 'Un projet réalisé et payé doit avoir un sous-total.',
            'caseRewardAdjusted': 'Project amount updated.' if lang == 'en' else 'Montant du projet mis à jour.',
            'caseRewardPrompt': 'Enter the final credit or commission amount for this project. Use 0 to zero it out. Leave blank to return to automatic calculation.' if lang == 'en' else 'Entrez le montant final du crédit ou de la commission pour ce projet. Utilisez 0 pour le mettre à zéro. Laissez vide pour revenir au calcul automatique.',
            'caseRewardNotePrompt': 'Optional note saved with this project amount.' if lang == 'en' else 'Note optionnelle enregistrée avec ce montant de projet.',
            'createAccountRequired': 'Name and email are required.' if lang == 'en' else 'Le nom et le courriel sont obligatoires.',
            'createPartnerCompanyRequired': 'Company is required for a partner account.' if lang == 'en' else 'L’entreprise est obligatoire pour un compte partenaire.',
            'detailLoading': 'Loading the account detail…' if lang == 'en' else 'Chargement de la fiche compte…',
            'detailEmpty': 'Select an account to load the full detail, linked cases, rewards, and audit trail.' if lang == 'en' else 'Sélectionnez un compte pour charger la fiche complète, les dossiers liés, les récompenses et le journal d’activité.',
        }
    }
    create_title = 'Add an account manually' if lang == 'en' else 'Ajouter un compte manuellement'
    create_intro = (
        'Create a client or partner account directly from the admin without using the public forms.'
        if lang == 'en' else
        'Créez un compte client ou partenaire directement depuis l’admin sans passer par les formulaires publics.'
    )
    applications_title = 'Partner applications' if lang == 'en' else 'Demandes partenaires'
    applications_intro = (
        'Review pending requests, approve them by creating the real account, or close the request.'
        if lang == 'en' else
        'Révisez les demandes en attente, approuvez-les en créant le vrai compte, ou fermez la demande.'
    )
    accounts_title = 'Accounts' if lang == 'en' else 'Comptes'
    accounts_intro = (
        'Each row can be exported individually, have its access reset, or be deleted.'
        if lang == 'en' else
        'Chaque ligne peut être exportée séparément, réinitialisée ou supprimée.'
    )
    return (
        f'<div class="form-panel referral-admin-shell" data-referral-admin data-lang="{lang}" data-summary-url="/api/referrals/admin/summary" data-applications-url="/api/referrals/admin/applications" data-accounts-url="/api/referrals/admin/accounts" data-cases-url="/api/referrals/admin/cases" data-rewards-url="/api/referrals/admin/rewards" data-account-status-url="/api/referrals/admin/account-status" data-account-balance-adjust-url="/api/referrals/admin/account-balance-adjust" data-case-create-url="/api/referrals/admin/referral-create" data-case-update-url="/api/referrals/admin/referral-update" data-case-reward-adjust-url="/api/referrals/admin/referral-reward-adjust" data-case-status-url="/api/referrals/admin/referral-status" data-case-delete-url="/api/referrals/admin/referral-delete" data-reward-settle-url="/api/referrals/admin/reward-settle" data-export-url="/api/referrals/admin/export.csv" data-account-create-url="/api/referrals/admin/account-create" data-account-reset-access-url="/api/referrals/admin/account-reset-access" data-account-delete-url="/api/referrals/admin/account-delete" data-application-status-url="/api/referrals/admin/application-status" data-application-delete-url="/api/referrals/admin/application-delete" data-account-export-url="/api/referrals/admin/account-export" data-account-detail-url="/api/referrals/admin/account-export" data-referral-admin-detail-script="{REFERRAL_ADMIN_DETAIL_SCRIPT_URL}">'
        f'<script type="application/json" data-referral-admin-copy>{json.dumps(payload, ensure_ascii=False)}</script>'
        f'<div class="promo-admin-toolbar"><div class="promo-admin-actions"><button class="button button-secondary" type="button" data-referral-admin-refresh>{esc(payload["actions"]["refresh"])}</button><a class="button button-secondary" data-referral-export-accounts href="/api/referrals/admin/export.csv?kind=accounts">{esc(payload["actions"]["exportAccounts"])}</a><a class="button button-secondary" data-referral-export-cases href="/api/referrals/admin/export.csv?kind=cases">{esc(payload["actions"]["exportCases"])}</a><a class="button button-secondary" data-referral-export-rewards href="/api/referrals/admin/export.csv?kind=rewards">{esc(payload["actions"]["exportRewards"])}</a></div></div>'
        f'<div class="promo-inline-status" data-referral-admin-status hidden></div><div class="promo-inline-error" data-referral-admin-error hidden></div>'
        f'<div class="promo-admin-summary">'
        f'<div class="detail-item"><strong>{esc(payload["summary"]["activeAccounts"])}</strong><p data-referral-summary-active>0</p></div>'
        f'<div class="detail-item"><strong>{esc(payload["summary"]["pendingPartners"])}</strong><p data-referral-summary-pending>0</p></div>'
        f'<div class="detail-item"><strong>{esc(payload["summary"]["openCases"])}</strong><p data-referral-summary-open>0</p></div>'
        f'<div class="detail-item"><strong>{esc(payload["summary"]["pendingPayouts"])}</strong><p data-referral-summary-payouts>0.00</p></div>'
        f'</div>'
        f'<div class="referral-admin-grids">'
        f'<div class="contact-panel"><p class="eyebrow">{esc(copy["label"])}</p><h2>{esc(create_title)}</h2><p>{esc(create_intro)}</p>'
        f'<form class="referral-admin-create-form" data-referral-admin-create-form novalidate>'
        f'<div class="input-grid referral-admin-form-grid">'
        f'<label class="field"><span>{"Account type" if lang == "en" else "Type de compte"}</span><select name="account_type"><option value="client">{"Client" if lang == "en" else "Client"}</option><option value="partner">{"Partner" if lang == "en" else "Partenaire"}</option></select></label>'
        f'<label class="field"><span>{"Language" if lang == "en" else "Langue"}</span><select name="locale"><option value="fr">Français</option><option value="en">English</option></select></label>'
        f'<label class="field"><span>{"Status" if lang == "en" else "Statut"}</span><select name="status"><option value="active">{"Active" if lang == "en" else "Actif"}</option><option value="pending">{"Pending" if lang == "en" else "En attente"}</option><option value="paused">{"Paused" if lang == "en" else "En pause"}</option><option value="rejected">{"Rejected" if lang == "en" else "Refusé"}</option></select></label>'
        f'<label class="field"><span>{"Full name" if lang == "en" else "Nom complet"}</span><input name="name" type="text" autocomplete="name" required /></label>'
        f'<label class="field"><span>{"Email address" if lang == "en" else "Adresse courriel"}</span><input name="email" type="email" autocomplete="email" required /></label>'
        f'<label class="field"><span>{"Phone number" if lang == "en" else "Téléphone"}</span><input name="phone" type="tel" autocomplete="tel" /></label>'
        f'<label class="field"><span>{"Company" if lang == "en" else "Entreprise"}</span><input name="company" type="text" autocomplete="organization" /></label>'
        f'<label class="field"><span>{"Website" if lang == "en" else "Site web"}</span><input name="website" type="url" inputmode="url" /></label>'
        f'</div>'
        f'<label class="field"><span>{"Notes" if lang == "en" else "Notes"}</span><textarea name="notes"></textarea></label>'
        f'<label class="referral-admin-checkbox"><input name="send_setup_link" type="checkbox" checked /><span>{"Send a setup link by email immediately" if lang == "en" else "Envoyer immédiatement un lien de configuration par courriel"}</span></label>'
        f'<div class="hero-actions"><button class="button button-primary" type="submit">{esc(payload["actions"]["saveAccount"])}</button></div>'
        f'</form></div>'
        f'<div class="contact-panel"><h2>{esc(applications_title)}</h2><p>{esc(applications_intro)}</p><div class="referral-admin-filters"><label class="field"><span>{"Status" if lang == "en" else "Statut"}</span><select data-referral-filter-applications-status><option value="all">{"All" if lang == "en" else "Tous"}</option><option value="pending">{"Pending review" if lang == "en" else "À réviser"}</option><option value="reviewed">{"Reviewed" if lang == "en" else "Révisée"}</option><option value="approved">{"Approved" if lang == "en" else "Approuvée"}</option><option value="rejected">{"Rejected" if lang == "en" else "Refusée"}</option><option value="void">{"Deleted" if lang == "en" else "Supprimée"}</option></select></label><label class="field"><span>{"Search" if lang == "en" else "Recherche"}</span><input type="search" data-referral-filter-applications-search /></label></div><div class="promo-admin-table-shell"><table class="promo-admin-table referral-admin-table"><thead><tr><th>ID</th><th>{"Status" if lang == "en" else "Statut"}</th><th>{"Name" if lang == "en" else "Nom"}</th><th>{"Email" if lang == "en" else "Courriel"}</th><th>{"Company" if lang == "en" else "Entreprise"}</th><th>{"Created" if lang == "en" else "Créée"}</th><th>{"Action" if lang == "en" else "Action"}</th></tr></thead><tbody data-referral-admin-applications></tbody></table></div></div>'
        f'<div class="contact-panel"><h2>{esc(accounts_title)}</h2><p>{esc(accounts_intro)}</p><div class="referral-admin-filters"><label class="field"><span>{"Program" if lang == "en" else "Programme"}</span><select data-referral-filter-accounts-program><option value="all">{"All" if lang == "en" else "Tous"}</option><option value="client">{"Referral Program" if lang == "en" else "Programme de référence"}</option><option value="partner">{"Referral Partner Program" if lang == "en" else "Programme de partenaires référents"}</option></select></label><label class="field"><span>{"Status" if lang == "en" else "Statut"}</span><select data-referral-filter-accounts-status><option value="all">{"All" if lang == "en" else "Tous"}</option><option value="pending">{"Pending" if lang == "en" else "En attente"}</option><option value="active">{"Active" if lang == "en" else "Actif"}</option><option value="paused">{"Paused" if lang == "en" else "En pause"}</option><option value="rejected">{"Rejected" if lang == "en" else "Refusé"}</option></select></label><label class="field"><span>{"Search" if lang == "en" else "Recherche"}</span><input type="search" data-referral-filter-accounts-search /></label></div><div class="promo-admin-table-shell"><table class="promo-admin-table referral-admin-table"><thead><tr><th>ID</th><th>{"Program" if lang == "en" else "Programme"}</th><th>{"Status" if lang == "en" else "Statut"}</th><th>{"Name" if lang == "en" else "Nom"}</th><th>{"Email" if lang == "en" else "Courriel"}</th><th>{"Code(s)" if lang == "en" else "Code(s)"}</th><th>{"Balance" if lang == "en" else "Solde"}</th><th>{"Action" if lang == "en" else "Action"}</th></tr></thead><tbody data-referral-admin-accounts></tbody></table></div></div>'
        f'<div class="contact-panel"><h2>{"Projects / referral cases" if lang == "en" else "Projets / dossiers de référence"}</h2><div class="referral-admin-filters"><label class="field"><span>{"Program" if lang == "en" else "Programme"}</span><select data-referral-filter-cases-program><option value="all">{"All" if lang == "en" else "Tous"}</option><option value="client">{"Referral Program" if lang == "en" else "Programme de référence"}</option><option value="partner">{"Referral Partner Program" if lang == "en" else "Programme de partenaires référents"}</option></select></label><label class="field referral-status-filter-field"><span>{"Status" if lang == "en" else "Statut"}</span><select data-referral-filter-cases-status><option value="all">{"All" if lang == "en" else "Tous"}</option><option value="new">{"New" if lang == "en" else "Nouveau"}</option><option value="quoted">{"Quoted" if lang == "en" else "Soumission envoyée"}</option><option value="accepted">{"Accepted" if lang == "en" else "Acceptée"}</option><option value="completed_paid">{"Installed + paid" if lang == "en" else "Installé et payé"}</option><option value="member_paid">{"Member paid" if lang == "en" else "Membre payé"}</option><option value="void">{"Void" if lang == "en" else "Annulé"}</option></select></label><label class="field"><span>{"Search" if lang == "en" else "Recherche"}</span><input type="search" data-referral-filter-cases-search /></label></div><div class="promo-admin-table-shell"><table class="promo-admin-table referral-admin-table referral-admin-cases-table"><thead><tr><th>ID</th><th>{"Account" if lang == "en" else "Compte"}</th><th>{"Code" if lang == "en" else "Code"}</th><th>{"Status" if lang == "en" else "Statut"}</th><th>{"Subtotal" if lang == "en" else "Sous-total"}</th><th>{"Quote ref" if lang == "en" else "Réf. soumission"}</th><th>{"Reward" if lang == "en" else "Récompense"}</th><th>{"Action" if lang == "en" else "Action"}</th></tr></thead><tbody data-referral-admin-cases></tbody></table></div></div>'
        f'<div class="contact-panel"><h2>{"Rewards" if lang == "en" else "Récompenses"}</h2><div class="referral-admin-filters"><label class="field"><span>{"Type" if lang == "en" else "Type"}</span><select data-referral-filter-rewards-type><option value="all">{"All" if lang == "en" else "Tous"}</option><option value="credit">{"Credit" if lang == "en" else "Crédit"}</option><option value="payout">{"Payout" if lang == "en" else "Paiement"}</option></select></label><label class="field"><span>{"Status" if lang == "en" else "Statut"}</span><select data-referral-filter-rewards-status><option value="all">{"All" if lang == "en" else "Tous"}</option><option value="pending">{"Pending" if lang == "en" else "En attente"}</option><option value="earned">{"Earned" if lang == "en" else "Gagné"}</option><option value="settled">{"Settled" if lang == "en" else "Réglé"}</option><option value="void">{"Void" if lang == "en" else "Annulé"}</option></select></label><label class="field"><span>{"Search" if lang == "en" else "Recherche"}</span><input type="search" data-referral-filter-rewards-search /></label></div><div class="promo-admin-table-shell"><table class="promo-admin-table referral-admin-table"><thead><tr><th>ID</th><th>{"Account" if lang == "en" else "Compte"}</th><th>{"Type" if lang == "en" else "Type"}</th><th>{"Status" if lang == "en" else "Statut"}</th><th>{"Amount" if lang == "en" else "Montant"}</th><th>{"Note" if lang == "en" else "Note"}</th><th>{"Action" if lang == "en" else "Action"}</th></tr></thead><tbody data-referral-admin-rewards></tbody></table></div></div>'
        f'<div class="contact-panel referral-admin-detail-panel"><p class="eyebrow">{"Account detail" if lang == "en" else "Fiche compte"}</p><h2>{"Selected account" if lang == "en" else "Compte sélectionné"}</h2><p data-referral-admin-detail-empty>{esc(payload["messages"]["detailEmpty"])}</p><div data-referral-admin-detail hidden><div class="referral-admin-detail-header"><div><h3 data-referral-admin-detail-name>—</h3><p data-referral-admin-detail-meta>—</p></div><div class="referral-admin-action-stack"><button class="button button-secondary" type="button" data-referral-admin-detail-export>{esc(payload["actions"]["exportOne"])}</button><button class="button button-secondary" type="button" data-referral-admin-detail-reset>{esc(payload["actions"]["resetAccess"])}</button><button class="button button-secondary" type="button" data-referral-admin-detail-delete>{esc(payload["actions"]["delete"])}</button></div></div><div class="promo-admin-meta referral-admin-detail-grid"><div class="detail-item"><strong>{"Programme" if lang == "en" else "Programme"}</strong><p data-referral-admin-detail-program>—</p></div><div class="detail-item"><strong>{"Status" if lang == "en" else "Statut"}</strong><p data-referral-admin-detail-status>—</p></div><div class="detail-item"><strong>{"Email" if lang == "en" else "Courriel"}</strong><p data-referral-admin-detail-email>—</p></div><div class="detail-item"><strong>{"Phone" if lang == "en" else "Téléphone"}</strong><p data-referral-admin-detail-phone>—</p></div><div class="detail-item"><strong>{"Company" if lang == "en" else "Entreprise"}</strong><p data-referral-admin-detail-company>—</p></div><div class="detail-item"><strong>{"Website" if lang == "en" else "Site web"}</strong><p data-referral-admin-detail-website>—</p></div><div class="detail-item"><strong>{"Referral code" if lang == "en" else "Code de référence"}</strong><p class="promo-admin-code" data-referral-admin-detail-share-code>—</p></div><div class="detail-item"><strong>{"Member code" if lang == "en" else "Code membre"}</strong><p class="promo-admin-code" data-referral-admin-detail-credit-code>—</p></div><div class="detail-item"><strong>{"Wallet / pending" if lang == "en" else "Solde / attente"}</strong><p data-referral-admin-detail-balance>—</p></div><div class="detail-item"><strong>{"Total earned" if lang == "en" else "Total gagné"}</strong><p data-referral-admin-detail-earned>—</p></div><div class="detail-item"><strong>{"Created" if lang == "en" else "Créé"}</strong><p data-referral-admin-detail-created>—</p></div><div class="detail-item"><strong>{"Last login" if lang == "en" else "Dernière connexion"}</strong><p data-referral-admin-detail-login>—</p></div></div><div class="detail-item"><strong>{"Notes" if lang == "en" else "Notes"}</strong><p data-referral-admin-detail-notes>—</p></div><div class="contact-panel referral-admin-projects-panel"><div class="referral-admin-section-header"><p class="eyebrow">{"Projects" if lang == "en" else "Projets"}</p><h3>{"Manage linked projects" if lang == "en" else "Gérer les projets liés"}</h3><p>{"Add a project to this account, then edit, adjust, or delete it directly from the list below." if lang == "en" else "Ajoutez un projet à ce compte, puis modifiez-le, ajustez-le ou supprimez-le directement dans la liste ci-dessous."}</p></div><form class="referral-admin-case-form" data-referral-admin-case-form novalidate><div class="input-grid referral-admin-form-grid"><label class="field"><span>{"Referral code" if lang == "en" else "Code de référence"}</span><input name="referral_code" type="text" required /></label><label class="field"><span>{"Contact name" if lang == "en" else "Nom du contact"}</span><input name="referred_name" type="text" required /></label><label class="field"><span>{"Contact email" if lang == "en" else "Courriel du contact"}</span><input name="referred_email" type="email" required /></label><label class="field"><span>{"Phone" if lang == "en" else "Téléphone"}</span><input name="referred_phone" type="tel" /></label><label class="field"><span>{"Company" if lang == "en" else "Entreprise"}</span><input name="referred_company" type="text" required /></label><label class="field"><span>{"Quote reference" if lang == "en" else "Réf. soumission"}</span><input name="quote_reference" type="text" /></label><label class="field referral-status-field"><span>{"Status" if lang == "en" else "Statut"}</span><select name="status"><option value="new">{"New" if lang == "en" else "Nouveau"}</option><option value="quoted">{"Quoted" if lang == "en" else "Soumission envoyée"}</option><option value="accepted">{"Accepted" if lang == "en" else "Acceptée"}</option><option value="completed_paid">{"Installed + paid" if lang == "en" else "Installé et payé"}</option><option value="member_paid">{"Member paid" if lang == "en" else "Membre payé"}</option><option value="void">{"Void" if lang == "en" else "Annulé"}</option></select></label><label class="field"><span>{"Subtotal (CAD)" if lang == "en" else "Sous-total (CAD)"}</span><input name="quoted_subtotal" type="number" min="0" step="0.01" /></label><label class="field"><span>{"Manual credit / commission" if lang == "en" else "Crédit / commission manuel"}</span><input name="manual_reward" type="number" min="0" step="0.01" /></label></div><label class="field"><span>{"Internal note" if lang == "en" else "Note interne"}</span><textarea name="note"></textarea></label><p class="form-note" data-referral-admin-case-state></p><div class="hero-actions"><button class="button button-primary" type="submit" data-referral-admin-case-submit>{esc(payload["actions"]["saveCase"])}</button><button class="button button-secondary" type="button" data-referral-admin-case-cancel hidden>{esc(payload["actions"]["cancelEdit"])}</button></div></form><div class="promo-admin-table-shell"><table class="promo-admin-table referral-mini-table referral-detail-cases-table"><thead><tr><th>ID</th><th>{"Status" if lang == "en" else "Statut"}</th><th>{"Reference" if lang == "en" else "Référence"}</th><th>{"Subtotal" if lang == "en" else "Sous-total"}</th><th>{"Reward" if lang == "en" else "Récompense"}</th><th>{"Action" if lang == "en" else "Action"}</th></tr></thead><tbody data-referral-admin-detail-cases></tbody></table></div></div><div class="contact-panel"><h3>{"Rewards and balance changes" if lang == "en" else "Récompenses et ajustements"}</h3><div class="promo-admin-table-shell"><table class="promo-admin-table referral-mini-table"><thead><tr><th>ID</th><th>{"Status" if lang == "en" else "Statut"}</th><th>{"Amount" if lang == "en" else "Montant"}</th><th>{"Created" if lang == "en" else "Créé"}</th><th>{"Note" if lang == "en" else "Note"}</th></tr></thead><tbody data-referral-admin-detail-rewards></tbody></table></div></div><div class="contact-panel"><h3>{"Audit trail" if lang == "en" else "Journal d’activité"}</h3><div class="promo-admin-table-shell"><table class="promo-admin-table referral-mini-table"><thead><tr><th>{"Created" if lang == "en" else "Créé"}</th><th>{"Event" if lang == "en" else "Événement"}</th><th>{"Note" if lang == "en" else "Note"}</th></tr></thead><tbody data-referral-admin-detail-audit></tbody></table></div></div></div></div>'
        f'</div></div>'
    )


def referral_contact_form_stack(lang):
    return f'<div class="referral-contact-stack">{form_section(lang)}</div>'


def promo_cta_band(lang):
    copy = PROMO_PAGE_CONTENT[lang]
    return band_section(
        f'<div><p class="eyebrow">{esc(copy["cta_eyebrow"])}</p><h2>{esc(copy["cta_title"])}</h2><p>{esc(copy["cta_copy"])}</p></div>'
        f'{render_chips([promo_limited_time_label(lang), promo_deadline_label(lang), promo_discount_range_label(lang), promo_cap_label()])}'
        f'<div class="cta-actions"><a class="button button-primary" href="{routes[lang]["promo"]}">{esc(copy["cta_button"])}</a><a class="button button-secondary" href="{routes[lang]["contact"]}">{esc(T[lang]["quote"])}</a></div>',
        'promo-cta-section',
        'layout-shell cta-band promo-cta-band',
    )


def hero_signal_grid(lang):
    items = ''.join(
        f'<article class="hero-signal-card"><strong>{esc(title)}</strong><span>{esc(text)}</span></article>'
        for title, text in HOME_PANEL_FACTS[lang]
    )
    return f'<div class="hero-signal-grid">{items}</div>'


def service_panel_media(key, lang):
    visual = service_panel_visuals.get(key, {}).get(lang)
    if not visual:
        return ''
    image_class = 'service-panel-image'
    if visual.get('class_name'):
        image_class += f' {visual["class_name"]}'
    image = content_img(
        visual['src'],
        visual['alt'],
        visual['width'],
        visual['height'],
        image_class,
        zoomable=True,
        lang=lang,
        caption=visual['caption'],
        sizes='(min-width: 1100px) 40vw, 100vw',
    )
    return f'<figure class="service-panel-visual"><div class="service-panel-frame">{image}</div></figure>'


def about_panel_media(lang):
    visual = {
        'en': {
            'alt': 'Commercial technology building and connectivity illustration',
            'caption': 'Commercial technology infrastructure and connectivity',
        },
        'fr': {
            'alt': 'Illustration de bâtiment commercial et de connectivité technologique',
            'caption': 'Infrastructures technologiques commerciales et connectivité',
        },
    }[lang]
    image = content_img(
        ABOUT_PANEL_URL,
        visual['alt'],
        ABOUT_PANEL_WIDTH,
        ABOUT_PANEL_HEIGHT,
        'about-panel-image',
        eager=True,
        zoomable=True,
        lang=lang,
        caption=visual['caption'],
        sizes='(min-width: 1100px) 36vw, 100vw',
    )
    return f'<figure class="about-panel-visual"><div class="about-panel-frame">{image}</div></figure>'


def related_services_carousel(lang, current_key, preferred_keys, label):
    heading = 'Related services' if lang == 'en' else 'Services connexes'
    ordered = []
    for key in [*preferred_keys, *order]:
        if key == current_key or key in ordered:
            continue
        ordered.append(key)
    cards = ''.join(
        card(
            services[key][lang]['name'],
            services[key][lang]['summary'],
            routes[lang][key],
            label,
            cls='card service-carousel-card',
        )
        for key in ordered
    )
    ui = CAROUSEL_UI[lang]
    return band_section(
        f'<div class="service-carousel" data-service-carousel>'
        f'<div class="service-carousel-header"><div class="section-heading"><p class="eyebrow">{esc(T[lang]["services"])}</p>'
        f'<h2>{esc(heading)}</h2><p>{esc(T[lang]["related_intro"])}</p></div>'
        f'<div class="service-carousel-controls"><button class="service-carousel-button" type="button" data-carousel-prev aria-label="{esc(ui["prev"])}">&larr;</button>'
        f'<button class="service-carousel-button" type="button" data-carousel-next aria-label="{esc(ui["next"])}">&rarr;</button></div></div>'
        f'<div class="service-carousel-track" data-carousel-track>{cards}</div></div>',
        'carousel-section',
    )


def home_visual_panel(lang):
    visual = home_visuals[lang]
    title_html = f'<h2>{esc(visual["title"])}</h2>' if visual['title'] else ''
    return (
        f'<aside class="hero-panel hero-media-panel"><p class="eyebrow">{esc(visual["eyebrow"])}</p>'
        f'{title_html}'
        f'<div class="hero-media-stack">'
        f'<figure class="hero-media-main"><div class="hero-media-frame">{content_img(HOME_BUILDING_URL, visual["top_alt"], HOME_BUILDING_WIDTH, HOME_BUILDING_HEIGHT, "hero-media-main-image", zoomable=True, lang=lang, caption=visual["top_title"], sizes="(min-width: 1100px) 42vw, 100vw")}</div>'
        f'<figcaption class="hero-media-caption"><strong>{esc(visual["top_title"])}</strong><span>{esc(visual["top_copy"])}</span></figcaption></figure>'
        f'<figure class="hero-media-main"><div class="hero-media-frame">{content_img(HOME_RACK_URL, visual["main_alt"], HOME_RACK_WIDTH, HOME_RACK_HEIGHT, "hero-media-main-image", eager=True, high_priority=True, zoomable=True, lang=lang, caption=visual["main_title"], sizes="(min-width: 1100px) 42vw, 100vw")}</div>'
        f'<figcaption class="hero-media-caption"><strong>{esc(visual["main_title"])}</strong><span>{esc(visual["main_copy"])}</span></figcaption></figure>'
        f'</div>{hero_signal_grid(lang)}</aside>'
    )


def home_featured_services_section(lang):
    t = T[lang]
    cards = ''.join(
        feature_card(item['title'], item['copy'], routes[lang][item['key']], t['service_label'], item['badge'], item.get('eyebrow', ''))
        for item in HOME_FEATURED_SERVICES[lang]
    )
    return band_section(
        f'<div class="section-heading"><p class="eyebrow">{esc(t["services"])}</p>'
        f'<h2>{esc(t["featured_title"])}</h2><p>{esc(t["featured_intro"])}</p></div>'
        f'<div class="feature-grid">{cards}</div>',
        'featured-section',
    )


def service_divisions_section(lang):
    t = T[lang]
    cards = ''.join(
        f'<article class="division-card"><p class="eyebrow">{esc(item["eyebrow"])}</p>'
        f'<h3>{esc(item["title"])}</h3><p>{esc(item["copy"])}</p>'
        f'{render_service_chip_links(lang, item["keys"])}</article>'
        for item in SERVICE_DIVISION_GROUPS[lang]
    )
    return band_section(
        f'<div class="section-heading"><p class="eyebrow">{esc(t["services"])}</p>'
        f'<h2>{esc(t["division_title"])}</h2><p>{esc(t["division_intro"])}</p></div>'
        f'<div class="division-grid">{cards}</div>',
        'division-section',
    )


def process_section(lang):
    items = ''.join(
        f'<article class="timeline-step"><span>{index:02d}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>'
        for index, (title, text) in enumerate(T[lang]['process'], 1)
    )
    return band_section(
        section_heading_html(T[lang]["process_title"], T[lang]["process_title"], T[lang]["process_intro"])
        + f'<div class="timeline">{items}</div>',
        'process-section',
    )


def split_list_items(items):
    if len(items) <= 4:
        return [items]
    midpoint = (len(items) + 1) // 2
    return [items[:midpoint], items[midpoint:]]


def render_custom_content_section(section):
    heading = section_heading_html(section.get('eyebrow', ''), section['title'], section.get('copy'))

    blocks = []
    if section.get('paragraphs'):
        paragraphs = ''.join(f'<p>{esc(text)}</p>' for text in section['paragraphs'])
        blocks.append(f'<div class="contact-panel">{paragraphs}</div>')
    if section.get('details'):
        details = ''.join(f'<div class="detail-item"><strong>{esc(label)}</strong><p>{contact_value_html(label, value)}</p></div>' for label, value in section['details'])
        blocks.append(f'<div class="contact-panel"><div class="detail-list">{details}</div></div>')
    if section.get('cards'):
        grid_class = 'grid-4' if len(section['cards']) == 4 else 'grid-3'
        blocks.append(f'<div class="{grid_class}">{"".join(card(title, text) for title, text in section["cards"])}</div>')
    if section.get('items'):
        groups = split_list_items(section['items'])
        if len(groups) == 1:
            item_html = ''.join(f'<li>{esc(item)}</li>' for item in groups[0])
            blocks.append(f'<div class="contact-panel"><ul class="check-list">{item_html}</ul></div>')
        else:
            panels = ''.join(
                f'<div class="contact-panel"><ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in group)}</ul></div>'
                for group in groups
            )
            blocks.append(f'<div class="two-col">{panels}</div>')
    return band_section(heading + ''.join(blocks), 'content-section')


def format_blog_date(value, lang):
    parsed = date.fromisoformat(value)
    month = BLOG_MONTHS[lang][parsed.month - 1]
    if lang == 'fr':
        return f'{parsed.day} {month} {parsed.year}'
    return f'{month} {parsed.day}, {parsed.year}'


def blog_word_count(text):
    return len(re.findall(r"[0-9A-Za-zÀ-ÿ]+(?:['’\-][0-9A-Za-zÀ-ÿ]+)*", text))


def blog_word_count_for_article(article):
    pieces = []
    for key, value in article.items():
        if key in {'path', 'primary_key', 'secondary_key'}:
            continue
        if isinstance(value, str):
            pieces.append(value)
        elif isinstance(value, dict):
            pieces.extend(_collect_blog_text(value))
        elif isinstance(value, (list, tuple)):
            pieces.extend(_collect_blog_text(value))
    return blog_word_count(' '.join(pieces))


def blog_minutes_for_article(article):
    words = blog_word_count_for_article(article)
    return max(1, (words + 219) // 220)


def _collect_blog_text(value):
    parts = []
    if isinstance(value, str):
        parts.append(value)
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in {'path', 'primary_key', 'secondary_key'}:
                continue
            parts.extend(_collect_blog_text(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            parts.extend(_collect_blog_text(item))
    return parts


def blog_articles_for_lang(lang):
    articles = []
    for key, entry in BLOG_ARTICLES.items():
        localized = entry.get(lang)
        if not localized:
            continue
        merged = {
            'key': key,
            'published': entry['published'],
            'modified': entry.get('modified', entry['published']),
            'author': entry['author'],
            'related_services': entry.get('related_services', ()),
            'related_articles': entry.get('related_articles', ()),
            **localized,
        }
        articles.append(merged)
    return sorted(articles, key=lambda item: item['published'], reverse=True)


def guide_articles_for_lang(lang):
    articles = []
    for key, entry in GUIDE_ARTICLE_DATA.items():
        localized = entry.get(lang)
        if not localized:
            continue
        merged = {
            'key': key,
            'published': entry['published'],
            'modified': entry.get('modified', entry['published']),
            'author': entry['author'],
            'reading_minutes': entry.get('reading_minutes'),
            'related_services': entry.get('related_services', ()),
            'related_articles': entry.get('related_articles', ()),
            'related_resources': entry.get('related_resources', ()),
            **localized,
        }
        articles.append(merged)
    return sorted(articles, key=lambda item: item['published'], reverse=True)


def decision_articles_for_lang(lang):
    articles = []
    for key, entry in DECISION_ARTICLE_DATA.items():
        localized = entry.get(lang)
        if not localized:
            continue
        merged = {
            'key': key,
            'published': entry['published'],
            'modified': entry.get('modified', entry['published']),
            'author': entry['author'],
            'reading_minutes': entry.get('reading_minutes'),
            'related_services': entry.get('related_services', ()),
            'related_articles': entry.get('related_articles', ()),
            'related_resources': entry.get('related_resources', ()),
            **localized,
        }
        articles.append(merged)
    return sorted(articles, key=lambda item: item['published'], reverse=True)


def resource_article_lookup(lang):
    resource_map = {}
    resource_map.update(blog_article_lookup(lang))
    resource_map.update(guide_article_lookup(lang))
    resource_map.update(decision_article_lookup(lang))
    return resource_map

def blog_article_paths(article_key):
    entry = BLOG_ARTICLES.get(article_key, {})
    return {
        localized_lang: localized['path']
        for localized_lang in ('en', 'fr')
        if (localized := entry.get(localized_lang)) and localized.get('path')
    }


def resource_article_paths(article_key):
    entry = GUIDE_ARTICLE_DATA.get(article_key) or DECISION_ARTICLE_DATA.get(article_key) or {}
    return {
        localized_lang: localized['path']
        for localized_lang in ('en', 'fr')
        if (localized := entry.get(localized_lang)) and localized.get('path')
    }


def schema_author_entity(name):
    normalized = name.casefold()
    if 'opticable' in normalized or 'team' in normalized or 'équipe' in normalized or 'equipe' in normalized:
        return {'@type': 'Organization', 'name': name}
    return {'@type': 'Person', 'name': name}


def blog_article_seo_data(article, lang):
    social_image = image_meta_for_url(blog_social_image_url(article['key'], lang), article.get('headline', article.get('title', 'Opticable article')))
    published = article['published']
    modified = article.get('modified', published)
    words = blog_word_count_for_article(article)
    minutes = blog_minutes_for_article(article)
    section = article.get('eyebrow') or next(iter(article.get('tags', [])), '')
    return {
        'headline': article['headline'],
        'description': article.get('desc') or article.get('excerpt') or article.get('intro', ''),
        'author': article['author'],
        'published': published,
        'modified': modified,
        'published_iso': iso_datetime_for_date(published, 9),
        'modified_iso': iso_datetime_for_date(modified, 15),
        'image': social_image,
        'social_image': social_image,
        'section': section,
        'tags': article.get('tags', []),
        'word_count': words,
        'time_required': f'PT{minutes}M',
        'in_language': language_tag(lang),
    }


def blog_read_time_label(minutes, lang):
    return f'{minutes} {BLOG_META_UI[lang]["minutes"]}'


def render_blog_meta(article, lang, cls='blog-card-meta'):
    ui = BLOG_META_UI[lang]
    minutes = blog_minutes_for_article(article)
    items = (
        (ui['author'], article['author']),
        (ui['published'], format_blog_date(article['published'], lang)),
        (ui['reading_time'], blog_read_time_label(minutes, lang)),
    )
    return (
        f'<div class="{cls}">'
        f'{"".join(f"<div class=\"blog-meta-item\"><strong>{esc(label)}</strong><span>{esc(value)}</span></div>" for label, value in items)}'
        f'</div>'
    )


def render_blog_article_card(article, lang):
    ui = BLOG_META_UI[lang]
    main_style = ''
    if article.get('hero_image'):
        main_style = (
            f' style="--blog-card-image:url({esc(blog_card_image_url(article["hero_image"]))});'
            f'--blog-card-image-position:{esc(article.get("hero_image_position", "center center"))};"'
        )
    return (
        f'<article class="card blog-article-card">'
        f'<a class="blog-article-card-main" href="{article["path"]}" aria-label="{esc(ui["read_article"])}: {esc(article["headline"])}"{main_style}>'
        f'{render_chips(article["tags"])}<h3>{esc(article["headline"])}</h3><p>{esc(article["excerpt"])}</p><span class="blog-card-surface-link">{esc(ui["read_article"])}</span></a>'
        f'<aside class="blog-article-card-side">{render_blog_meta(article, lang)}<a class="button button-primary blog-card-link" href="{article["path"]}">{esc(ui["read_article"])}</a></aside>'
        f'</article>'
    )


def blog_article_lookup(lang):
    return {article['key']: article for article in blog_articles_for_lang(lang)}


def guide_article_lookup(lang):
    return {article['key']: article for article in guide_articles_for_lang(lang)}


def decision_article_lookup(lang):
    return {article['key']: article for article in decision_articles_for_lang(lang)}


def render_resource_cards_for_keys(lang, article_keys):
    article_map = resource_article_lookup(lang)
    seen = set()
    cards = []
    for key in article_keys:
        if key in seen or key not in article_map:
            continue
        seen.add(key)
        cards.append(render_blog_article_card(article_map[key], lang))
    if not cards:
        return ''
    grid_class = 'blog-grid blog-grid-single' if len(cards) == 1 else 'blog-grid'
    return f'<div class="{grid_class}">{"".join(cards)}</div>'


def render_blog_cards_for_keys(lang, article_keys):
    article_map = blog_article_lookup(lang)
    cards = [render_blog_article_card(article_map[key], lang) for key in article_keys if key in article_map]
    if not cards:
        return ''
    grid_class = 'blog-grid blog-grid-single' if len(cards) == 1 else 'blog-grid'
    return f'<div class="{grid_class}">{"".join(cards)}</div>'


def render_decision_cards_for_keys(lang, article_keys):
    article_map = decision_article_lookup(lang)
    cards = [render_blog_article_card(article_map[key], lang) for key in article_keys if key in article_map]
    if not cards:
        return ''
    grid_class = 'blog-grid blog-grid-single' if len(cards) == 1 else 'blog-grid'
    return f'<div class="{grid_class}">{"".join(cards)}</div>'


def guide_cards_section(lang, section_copy, article_keys):
    cards = render_resource_cards_for_keys(lang, article_keys)
    if not cards:
        return ''
    cta_href = section_copy.get('cta_href')
    if not cta_href and section_copy.get('cta_href_key'):
        cta_href = routes[lang].get(section_copy['cta_href_key'])
    cta_html = ''
    if cta_href and section_copy.get('cta_label'):
        cta_html = f'<div class="cta-actions"><a class="button button-secondary" href="{cta_href}">{esc(section_copy["cta_label"])}</a></div>'
    return band_section(
        f'<div class="section-heading"><p class="eyebrow">{esc(section_copy["eyebrow"])}</p>'
        f'<h2>{esc(section_copy["title"])}</h2><p>{esc(section_copy["intro"])}</p></div>'
        f'{cards}{cta_html}',
        'blog-listing-section',
    )


def industry_detail_pages_for_lang(lang):
    return INDUSTRY_DETAIL_PAGES_BY_LANG.get(lang, {})


def industry_detail_cards_section(lang, section_copy, page_keys):
    detail_pages = industry_detail_pages_for_lang(lang)
    cards = []
    for key in page_keys:
        page_data = detail_pages.get(key)
        if not page_data:
            continue
        cards.append(
            card(
                page_data['headline'],
                page_data.get('panel_copy', page_data['intro']),
                page_data['path'],
                section_copy.get('label', 'Voir cette page'),
            )
        )
    if not cards:
        return ''
    grid_class = 'grid-2' if len(cards) == 2 else 'grid-4' if len(cards) == 4 else 'grid-3'
    cta_html = ''
    if section_copy.get('cta_href') and section_copy.get('cta_label'):
        cta_html = f'<div class="cta-actions"><a class="button button-secondary" href="{section_copy["cta_href"]}">{esc(section_copy["cta_label"])}</a></div>'
    return band_section(
        f'{section_heading_html(section_copy["eyebrow"], section_copy["title"], section_copy["intro"])}'
        f'<div class="{grid_class}">{"".join(cards)}</div>{cta_html}',
        'content-section',
    )


def multifamily_cluster_pages_for_lang(lang):
    return MULTIFAMILY_CLUSTER_PAGES_BY_LANG.get(lang, {})


def multifamily_cluster_cards_section(lang, section_copy, page_keys):
    cluster_pages = multifamily_cluster_pages_for_lang(lang)
    cards = []
    for key in page_keys:
        page_data = cluster_pages.get(key)
        if not page_data:
            continue
        cards.append(
            card(
                page_data['headline'],
                page_data.get('panel_copy', page_data['intro']),
                page_data['path'],
                section_copy.get('label', 'Voir cette page' if lang == 'fr' else 'View this page'),
            )
        )
    if not cards:
        return ''
    grid_class = 'grid-2' if len(cards) == 2 else 'grid-4' if len(cards) == 4 else 'grid-3'
    cta_html = ''
    if section_copy.get('cta_href') and section_copy.get('cta_label'):
        cta_html = f'<div class="cta-actions"><a class="button button-secondary" href="{section_copy["cta_href"]}">{esc(section_copy["cta_label"])}</a></div>'
    return band_section(
        f'{section_heading_html(section_copy["eyebrow"], section_copy["title"], section_copy["intro"])}'
        f'<div class="{grid_class}">{"".join(cards)}</div>{cta_html}',
        'content-section',
    )


def industry_multifamily_cluster_section(lang, page_key):
    if page_key != 'industry-multi-tenant-building':
        return ''
    if lang == 'fr':
        section_copy = {
            'eyebrow': 'Réseau et WiFi',
            'title': "Explorer l'infrastructure multilogement selon la taille du projet",
            'intro': "Ces pages détaillent ce qui change entre un petit immeuble, un immeuble intermédiaire et une plus grande architecture multilogement.",
            'label': 'Voir cette page',
        }
    else:
        section_copy = {
            'eyebrow': 'WiFi and network',
            'title': 'Explore the multifamily infrastructure by building size',
            'intro': 'These pages explain what changes between smaller buildings, mid-size properties, and larger multifamily environments.',
            'label': 'View this page',
        }
    return multifamily_cluster_cards_section(lang, section_copy, MULTIFAMILY_CLUSTER_KEYS)


def service_multifamily_cluster_section(lang, service_key):
    page_keys = MULTIFAMILY_CLUSTER_SERVICE_KEYS.get(service_key, ())
    if not page_keys:
        return ''
    if lang == 'fr':
        section_copy = {
            'eyebrow': 'Immeubles multilogements',
            'title': 'Pages liées au WiFi et à la base réseau des immeubles multilogements',
            'intro': "Ces pages expliquent comment ce service s'intègre dans un immeuble multilogement selon la taille du bâtiment.",
            'label': 'Voir cette page',
        }
    else:
        section_copy = {
            'eyebrow': 'Multifamily buildings',
            'title': 'Pages tied to multifamily WiFi and network foundations',
            'intro': 'These pages show how this service fits multifamily buildings at different building sizes.',
            'label': 'View this page',
        }
    return multifamily_cluster_cards_section(lang, section_copy, page_keys)


def case_study_cards_subset(lang, case_keys):
    parent = CASE_STUDIES[lang]['parent']
    return ''.join(
        card(CASE_STUDIES[lang]['items'][key]['nav'], parent['card_copy'][key], routes[lang][key], T[lang]['view_case_study'])
        for key in case_keys
        if key in CASE_STUDIES[lang]['items']
    )


def service_case_study_section(lang, service_key):
    if lang != 'fr':
        return ''
    case_keys = FR_SERVICE_CASE_STUDY_KEYS.get(service_key, ())
    cards = case_study_cards_subset(lang, case_keys)
    if not cards:
        return ''
    return band_section(
        f'<div class="section-heading"><p class="eyebrow">{esc(T[lang]["case_studies"])}</p>'
        f'<h2>Preuves de terrain liées à ce service</h2><p>Des projets types qui montrent comment la portée se traduit sur un vrai site.</p></div>'
        f'<div class="grid-2">{cards}</div>',
        'case-study-preview-section',
    )


def service_guide_section(lang, service_key):
    guide_keys = FR_SERVICE_GUIDE_KEYS.get(service_key, ())
    if not guide_keys:
        return ''
    primary_service_name = services[service_key][lang]['name']
    if lang == 'fr':
        section_copy = {
            'eyebrow': 'Guide utile',
            'title': f'Pages utiles avant votre demande sur {primary_service_name.lower()}',
            'intro': "Ces pages répondent aux questions qui reviennent le plus souvent avant une visite de site ou une soumission.",
            'cta_href_key': 'guides',
            'cta_label': 'Voir tous les guides',
        }
    else:
        section_copy = {
            'eyebrow': 'Useful guides',
            'title': f'Helpful pages before your {primary_service_name.lower()} request',
            'intro': 'These pages answer common planning, pricing, and decision questions before a site visit or quote.',
            'cta_href_key': 'guides',
            'cta_label': 'View all guides',
        }
    return guide_cards_section(lang, section_copy, guide_keys)


def service_industry_section(lang, service_key):
    page_keys = FR_SERVICE_INDUSTRY_KEYS.get(service_key, ())
    if not page_keys:
        return ''
    if lang == 'fr':
        section_copy = {
            'eyebrow': 'Types d’immeubles',
            'title': 'Où ce service revient le plus souvent',
            'intro': "Ces pages montrent dans quels types d'immeubles ce service revient le plus souvent et comment il s'intègre au projet.",
            'label': 'Voir cette clientèle',
            'cta_href': routes[lang]['industries'],
            'cta_label': 'Voir toute la clientèle',
        }
    else:
        section_copy = {
            'eyebrow': 'Building types',
            'title': 'Where this service is most often used',
            'intro': 'These pages show the building types where this service is commonly part of the project.',
            'label': 'View this industry',
            'cta_href': routes[lang]['industries'],
            'cta_label': 'View all industries',
        }
    return industry_detail_cards_section(
        lang,
        section_copy,
        page_keys,
    )

def render_blog_listing(lang, blog_data, articles=None):
    if articles is None:
        articles = blog_articles_for_lang(lang)
    if not articles:
        return (
            f'<div class="blog-grid"><article class="card blog-empty-card"><p>{esc(blog_data["empty"])}</p>'
            f'<div class="cta-actions"><a class="button button-primary" href="{routes[lang]["services"]}">{esc(blog_data["primary_cta"])}</a>'
            f'<a class="button button-secondary" href="{routes[lang]["contact"]}">{esc(blog_data["secondary_cta"])}</a></div></article></div>'
        )
    grid_class = 'blog-grid blog-grid-single' if len(articles) == 1 else 'blog-grid'
    return f'<div class="{grid_class}">{"".join(render_blog_article_card(article, lang) for article in articles)}</div>'


def render_blog_summary(article):
    summary_items = article.get('summary', [])
    if not summary_items:
        return ''
    cards = ''.join(
        f'<article class="card blog-summary-card"><p class="eyebrow">{esc(label)}</p><h3>{esc(title)}</h3></article>'
        for label, title in summary_items
    )
    return f'<div class="blog-summary-grid">{cards}</div>'


def render_blog_related_services(article, lang):
    service_keys = [key for key in article.get('related_services', ()) if key in services]
    if not service_keys:
        return ''
    ui = BLOG_META_UI[lang]
    cards = ''.join(
        card(services[key][lang]['name'], services[key][lang]['summary'], routes[lang][key], ui['view_service'])
        for key in service_keys[:3]
    )
    return band_section(
        f'<div class="section-heading"><p class="eyebrow">{esc(T[lang]["services"])}</p>'
        f'<h2>{esc(ui["related_services"])}</h2><p>{esc(ui["related_services_intro"])}</p></div>'
        f'<div class="grid-3">{cards}</div>',
        'blog-related-services-section',
        'section-shell blog-article-shell',
    )


def render_blog_related_articles(article, lang):
    articles_by_key = {item['key']: item for item in blog_articles_for_lang(lang)}
    ordered = []
    for key in [*article.get('related_articles', ()), *(articles_by_key.keys())]:
        if key == article['key'] or key in ordered or key not in articles_by_key:
            continue
        ordered.append(key)
    related = [articles_by_key[key] for key in ordered[:3]]
    if not related:
        return ''
    ui = BLOG_META_UI[lang]
    cards = ''.join(card(item['headline'], item['excerpt'], item['path'], ui['read_article']) for item in related)
    return band_section(
        f'<div class="section-heading"><p class="eyebrow">{esc(T[lang]["blog"])}</p>'
        f'<h2>{esc(ui["related_articles"])}</h2><p>{esc(ui["related_articles_intro"])}</p></div>'
        f'<div class="grid-3">{cards}</div>',
        'blog-related-articles-section',
        'section-shell blog-article-shell',
    )


def render_blog_table_cell(cell):
    if isinstance(cell, (tuple, list)) and len(cell) == 2:
        value, tone = cell
        return f'<span class="blog-pill blog-pill-{esc(tone)}">{esc(value)}</span>'
    return esc(cell)


def render_blog_table(table):
    if not table:
        return ''
    columns = ''.join(f'<th scope="col">{esc(column)}</th>' for column in table['columns'])
    rows = []
    for row in table['rows']:
        cells = [f'<th scope="row">{esc(row[0])}</th>']
        cells.extend(f'<td>{render_blog_table_cell(cell)}</td>' for cell in row[1:])
        rows.append(f'<tr>{"".join(cells)}</tr>')
    head = ''
    if table.get('caption'):
        head = f'<div class="blog-table-head"><h3>{esc(table["caption"])}</h3></div>'
    return (
        f'<div class="contact-panel blog-table-panel">{head}'
        f'<div class="blog-table-scroll"><table class="blog-table"><thead><tr>{columns}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div></div>'
    )


def render_blog_callout(section):
    if not section.get('callout'):
        return ''
    class_name = 'contact-panel blog-callout'
    if section.get('callout_tone') == 'warning':
        class_name += ' blog-callout-warning'
    label = f'<p class="blog-callout-label">{esc(section["callout_label"])}</p>' if section.get('callout_label') else ''
    return f'<div class="{class_name}">{label}<p>{esc(section["callout"])}</p></div>'


def render_blog_subsection(subsection):
    items = ''
    if subsection.get('items'):
        items = f'<ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in subsection["items"])}</ul>'
    paragraphs = ''.join(f'<p>{esc(text)}</p>' for text in subsection.get('paragraphs', []))
    return f'<article class="contact-panel blog-subsection"><h3>{esc(subsection["title"])}</h3>{paragraphs}{items}</article>'


def render_blog_comparison(pair, lang):
    ui = BLOG_META_UI[lang]
    return (
        f'<article class="contact-panel blog-compare-card">'
        f'<div class="grid-2">'
        f'<div class="blog-compare-side"><strong>{esc(ui["myth"])}</strong><p>{esc(pair["myth"])}</p></div>'
        f'<div class="blog-compare-side"><strong>{esc(ui["reality"])}</strong><p>{esc(pair["reality"])}</p></div>'
        f'</div>'
        f'</article>'
    )


def render_blog_steps(steps):
    cards = []
    for index, (title, text) in enumerate(steps, start=1):
        cards.append(
            f'<article class="card blog-step-card"><p class="eyebrow">{index:02d}</p><h3>{esc(title)}</h3><p>{esc(text)}</p></article>'
        )
    return f'<div class="grid-3 blog-step-grid">{"".join(cards)}</div>'


def render_blog_article_section(section, lang):
    blocks = [
        section_heading_html(section["eyebrow"], section["title"])
    ]
    callout_rendered = False
    if section.get('paragraphs'):
        prose = f'<div class="contact-panel blog-prose-panel">{"".join(f"<p>{esc(text)}</p>" for text in section["paragraphs"])}</div>'
        if section.get('callout'):
            blocks.append(
                f'<div class="blog-section-intro blog-section-intro-split">{prose}'
                f'{render_blog_callout(section)}</div>'
            )
            callout_rendered = True
        else:
            blocks.append(f'<div class="blog-section-intro">{prose}</div>')
    if section.get('table'):
        blocks.append(render_blog_table(section['table']))
    if section.get('cards'):
        grid_class = 'grid-2' if len(section['cards']) == 2 else 'grid-3'
        blocks.append(f'<div class="{grid_class}">{"".join(card(title, text, cls="card blog-detail-card") for title, text in section["cards"])}</div>')
    if section.get('comparisons'):
        blocks.append(f'<div class="blog-comparison-list">{"".join(render_blog_comparison(item, lang) for item in section["comparisons"])}</div>')
    if section.get('subsections'):
        blocks.append(f'<div class="blog-subsection-stack">{"".join(render_blog_subsection(item) for item in section["subsections"])}</div>')
    if section.get('steps'):
        blocks.append(render_blog_steps(section['steps']))
    if section.get('callout') and not callout_rendered:
        blocks.append(render_blog_callout(section))
    if section.get('quote'):
        blocks.append(f'<div class="contact-panel blog-quote"><p>{esc(section["quote"])}</p></div>')
    return band_section(f'<div class="blog-section-stack">{"".join(blocks)}</div>', 'blog-article-section', 'section-shell blog-article-shell')


def render_blog_article_faq(article, lang):
    faq_items = article.get('faq_items', [])
    if not faq_items:
        return ''
    details = ''.join(
        f'<details class="faq-item" open><summary>{esc(question)}</summary><p>{esc(answer)}</p></details>'
        for question, answer in faq_items
    )
    title = 'Questions fréquentes' if lang == 'fr' else 'Frequently asked questions'
    intro = "Des réponses rapides avant de passer à la visite de site ou à la soumission." if lang == 'fr' else 'Short answers before the site visit or quote step.'
    return band_section(
        f'<div class="section-heading"><p class="eyebrow">FAQ</p><h2>{esc(title)}</h2><p>{esc(intro)}</p></div>'
        f'<div class="faq-list">{details}</div>',
        'blog-article-faq-section',
        'section-shell blog-article-shell',
    )


def render_decision_related_resources(article, lang):
    decision_map = decision_article_lookup(lang)
    ordered = []
    for key in [*article.get('related_resources', ()), *(decision_map.keys())]:
        if key == article['key'] or key in ordered or key not in decision_map:
            continue
        ordered.append(key)
    related = [decision_map[key] for key in ordered[:3]]
    if not related:
        return ''
    ui_label = 'Guides' if lang == 'fr' else 'Guides'
    title = 'Guides connexes' if lang == 'fr' else 'Related guides'
    intro = "D'autres pages utiles pour cadrer le projet avant la visite de site ou la soumission." if lang == 'fr' else 'Additional guides to clarify the project before the quote step.'
    cards = ''.join(card(item['headline'], item['excerpt'], item['path'], 'Lire le guide' if lang == 'fr' else 'Read the guide') for item in related)
    return band_section(
        f'<div class="section-heading"><p class="eyebrow">{esc(ui_label)}</p><h2>{esc(title)}</h2><p>{esc(intro)}</p></div>'
        f'<div class="grid-3">{cards}</div>',
        'blog-related-articles-section',
        'section-shell blog-article-shell',
    )

def render_blog_article_page(article, lang):
    ui = BLOG_META_UI[lang]
    breadcrumb_items = [
        (T[lang]['home'], routes[lang]['home']),
        (T[lang]['blog'], routes[lang]['blog']),
        (article['headline'], article['path']),
    ]
    hero_style = ''
    if article.get('hero_image'):
        hero_style = (
            f' style="--blog-hero-image:url({esc(blog_hero_image_url(article["hero_image"]))});'
            f'--blog-hero-position:{esc(article.get("hero_image_position", "center center"))};"'
        )
    meta_panel = (
        f'<aside class="page-hero-panel blog-article-panel"><p class="eyebrow">{esc(ui["article_panel"])}</p>'
        f'<h2>{esc(article["headline"])}</h2>{render_chips(article["tags"])}'
        f'{render_blog_meta(article, lang, "blog-article-readout")}</aside>'
    )
    cta = article.get('cta', {})
    primary_href = routes[lang][cta['primary_key']] if cta.get('primary_key') else routes[lang]['contact']
    secondary_href = routes[lang][cta['secondary_key']] if cta.get('secondary_key') else routes[lang]['services']
    body = (
        breadcrumb_nav(breadcrumb_items)
        + f'<section class="hero-band page-hero-band blog-article-hero-band"{hero_style}>'
        + f'<div class="layout-shell blog-article-shell page-hero blog-article-hero">'
        + f'<div class="page-hero-copy"><p class="eyebrow">{esc(article["eyebrow"])}</p><h1>{esc(article["headline"])}</h1><p>{esc(article["intro"])}</p></div>'
        + meta_panel
        + '</div></section>'
        + (band_section(render_blog_summary(article), 'blog-summary-section', 'section-shell blog-article-shell') if article.get('summary') else '')
        + ''.join(render_blog_article_section(section, lang) for section in article['sections'])
        + render_blog_related_services(article, lang)
        + render_blog_related_articles(article, lang)
        + promo_cta_band(lang)
        + band_section(
            f'<div><p class="eyebrow">{esc(T[lang]["blog"])}</p><h2>{esc(cta["title"])}</h2><p>{esc(cta["copy"])}</p></div>'
            f'<div class="cta-actions"><a class="button button-primary" href="{primary_href}">{esc(cta["primary_label"])}</a>'
            f'<a class="button button-secondary" href="{secondary_href}">{esc(cta["secondary_label"])}</a></div>',
            'blog-article-cta',
            'layout-shell blog-article-shell cta-band',
        )
    )
    return breadcrumb_items, body


def render_standalone_article_page(article, lang, hub_label, hub_href):
    ui = BLOG_META_UI[lang]
    breadcrumb_items = [
        (T[lang]['home'], routes[lang]['home']),
        (hub_label, hub_href),
        (article['headline'], article['path']),
    ]
    hero_style = ''
    if article.get('hero_image'):
        hero_style = (
            f' style="--blog-hero-image:url({esc(blog_hero_image_url(article["hero_image"]))});'
            f'--blog-hero-position:{esc(article.get("hero_image_position", "center center"))};"'
        )
    meta_panel = (
        f'<aside class="page-hero-panel blog-article-panel"><p class="eyebrow">{esc(ui["article_panel"])}</p>'
        f'<h2>{esc(article["headline"])}</h2>{render_chips(article["tags"])}'
        f'{render_blog_meta(article, lang, "blog-article-readout")}</aside>'
    )
    cta = article.get('cta', {})
    primary_href = routes[lang][cta['primary_key']] if cta.get('primary_key') else routes[lang]['contact']
    secondary_href = routes[lang][cta['secondary_key']] if cta.get('secondary_key') else routes[lang]['services']
    body = (
        breadcrumb_nav(breadcrumb_items)
        + f'<section class="hero-band page-hero-band blog-article-hero-band"{hero_style}>'
        + f'<div class="layout-shell blog-article-shell page-hero blog-article-hero">'
        + f'<div class="page-hero-copy"><p class="eyebrow">{esc(article["eyebrow"])}</p><h1>{esc(article["headline"])}</h1><p>{esc(article["intro"])}</p></div>'
        + meta_panel
        + '</div></section>'
        + (band_section(render_blog_summary(article), 'blog-summary-section', 'section-shell blog-article-shell') if article.get('summary') else '')
        + ''.join(render_blog_article_section(section, lang) for section in article['sections'])
        + render_blog_article_faq(article, lang)
        + render_blog_related_services(article, lang)
        + render_decision_related_resources(article, lang)
        + render_blog_related_articles(article, lang)
        + band_section(
            f'<div><p class="eyebrow">{esc(hub_label)}</p><h2>{esc(cta["title"])}</h2><p>{esc(cta["copy"])}</p></div>'
            f'<div class="cta-actions"><a class="button button-primary" href="{primary_href}">{esc(cta["primary_label"])}</a>'
            f'<a class="button button-secondary" href="{secondary_href}">{esc(cta["secondary_label"])}</a></div>',
            'blog-article-cta',
            'layout-shell blog-article-shell cta-band',
        )
    )
    return breadcrumb_items, body


def resource_service_cards_section(lang, title, intro, service_keys):
    return band_section(
        f'<div class="section-heading"><p class="eyebrow">{esc(T[lang]["services"])}</p><h2>{esc(title)}</h2><p>{esc(intro)}</p></div>'
        f'<div class="grid-2">{service_cards(lang, T[lang]["service_label"], service_keys)}</div>',
        'support-section',
    )


def render_industry_detail_page(page_key, page_data, lang):
    hub_label = T[lang]['industries']
    hub_href = routes[lang]['industries']
    if lang == 'fr':
        guide_copy = {
            'eyebrow': 'Guides',
            'title': 'Pages utiles pour ce type de bâtiment',
            'intro': 'Des pages utiles pour cadrer les budgets, les choix techniques et la prochaine étape.',
            'cta_href_key': 'guides',
            'cta_label': 'Voir tous les guides',
        }
        service_title = "Services les plus liés à ce type de projet"
        service_intro = "Les services qui reviennent le plus souvent dans ce type d'immeuble."
    else:
        guide_copy = {
            'eyebrow': 'Guides',
            'title': 'Helpful pages for this type of building',
            'intro': 'Useful pages to frame budgets, technical choices, and the next step.',
            'cta_href_key': 'guides',
            'cta_label': 'View all guides',
        }
        service_title = 'Services most often connected to this project type'
        service_intro = 'The services that come up most often in this type of building.'
    breadcrumbs = [
        (T[lang]['home'], routes[lang]['home']),
        (hub_label, hub_href),
        (page_data['headline'], page_data['path']),
    ]
    guide_section = guide_cards_section(
        lang,
        guide_copy,
        page_data.get('guide_keys', ()),
    )
    body = (
        breadcrumb_nav(breadcrumbs)
        + band_section(
            f'<div class="page-hero-copy"><p class="eyebrow">{esc(page_data["eyebrow"])}</p><h1>{esc(page_data["headline"])}</h1><p>{esc(page_data["intro"])}</p>'
            f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(T[lang]["quote"])}</a><a class="button button-secondary" href="{hub_href}">{esc(hub_label)}</a></div></div>'
            f'<aside class="page-hero-panel"><p class="eyebrow">{esc(hub_label)}</p><h2>{esc(page_data["panel_title"])}</h2><p>{esc(page_data["panel_copy"])}</p></aside>',
            'hero-band page-hero-band',
            'layout-shell page-hero',
        )
        + ''.join(render_custom_content_section(section) for section in page_data['sections'])
        + industry_multifamily_cluster_section(lang, page_key)
        + resource_service_cards_section(lang, service_title, service_intro, page_data['service_keys'])
        + guide_section
        + inline_cta_band(page_data['cta_title'], page_data['cta_copy'], routes[lang]['contact'], page_data['cta_label'])
    )
    return breadcrumbs, body


def render_multifamily_cluster_page(page_key, page_data, lang):
    hub_page = INDUSTRY_DETAIL_PAGES_BY_LANG[lang]['industry-multi-tenant-building']
    hub_label = hub_page['headline']
    hub_href = hub_page['path']
    if lang == 'fr':
        guide_copy = {
            'eyebrow': 'Guides',
            'title': "Pages utiles avant de choisir l'architecture",
            'intro': "Des guides pour cadrer le WiFi, le câblage, la fibre et les choix de base avant la soumission.",
            'cta_href_key': 'guides',
            'cta_label': 'Voir tous les guides',
        }
        service_title = 'Services liés à cette architecture'
        service_intro = "Les services qui reviennent le plus souvent quand on structure l'infrastructure d'un immeuble multilogement."
        related_copy = {
            'eyebrow': 'Comparer',
            'title': "Comparer selon la taille de l'immeuble",
            'intro': "Les besoins changent avec le nombre d'unités, les étages, les zones communes et la complexité des systèmes à relier.",
            'label': 'Voir cette page',
            'cta_href': hub_href,
            'cta_label': 'Voir la page multilogement',
        }
    else:
        guide_copy = {
            'eyebrow': 'Guides',
            'title': 'Helpful pages before choosing the architecture',
            'intro': 'Guides that help frame WiFi, cabling, fiber, and the core decisions before the quote stage.',
            'cta_href_key': 'guides',
            'cta_label': 'View all guides',
        }
        service_title = 'Services tied to this architecture'
        service_intro = 'The services that most often come up when a multifamily building network foundation is being structured.'
        related_copy = {
            'eyebrow': 'Compare',
            'title': 'Compare by building size',
            'intro': 'Needs change with the number of units, the floor count, the common spaces, and the system complexity.',
            'label': 'View this page',
            'cta_href': hub_href,
            'cta_label': 'View the multifamily hub',
        }
    breadcrumbs = [
        (T[lang]['home'], routes[lang]['home']),
        (T[lang]['industries'], routes[lang]['industries']),
        (hub_label, hub_href),
        (page_data['headline'], page_data['path']),
    ]
    guide_section = guide_cards_section(lang, guide_copy, page_data.get('guide_keys', ()))
    related_keys = tuple(key for key in page_data.get('related_keys', ()) if key != page_key)
    related_section = multifamily_cluster_cards_section(lang, related_copy, related_keys) if related_keys else ''
    article_like = {'faq_items': page_data.get('faq_items', ())}
    body = (
        breadcrumb_nav(breadcrumbs)
        + band_section(
            f'<div class="page-hero-copy"><p class="eyebrow">{esc(page_data["eyebrow"])}</p><h1>{esc(page_data["headline"])}</h1><p>{esc(page_data["intro"])}</p>'
            f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(T[lang]["quote"])}</a><a class="button button-secondary" href="{hub_href}">{esc(hub_label)}</a></div></div>'
            f'<aside class="page-hero-panel"><p class="eyebrow">{esc(hub_label)}</p><h2>{esc(page_data["panel_title"])}</h2><p>{esc(page_data["panel_copy"])}</p></aside>',
            'hero-band page-hero-band',
            'layout-shell page-hero',
        )
        + ''.join(render_custom_content_section(section) for section in page_data['sections'])
        + related_section
        + resource_service_cards_section(lang, service_title, service_intro, page_data.get('service_keys', ()))
        + guide_section
        + render_blog_article_faq(article_like, lang)
        + inline_cta_band(page_data['cta_title'], page_data['cta_copy'], routes[lang]['contact'], page_data['cta_label'])
    )
    return breadcrumbs, body


def render_campaign_landing_page(page_data, lang):
    service_href = routes[lang][page_data['service_key']]
    service_label = 'Voir le service' if lang == 'fr' else 'View service'
    scope_eyebrow = 'Portée' if lang == 'fr' else 'Scope'
    scope_title = "Ce type de demande comprend souvent" if lang == 'fr' else 'This type of request often includes'
    benefit_eyebrow = 'Pourquoi Opticable' if lang == 'fr' else 'Why Opticable'
    benefit_title = "Ce qu'on apporte dans ce type de mandat" if lang == 'fr' else 'What we bring to this type of project'
    body = (
        band_section(
            f'<div class="page-hero-copy"><p class="eyebrow">{esc(page_data["eyebrow"])}</p><h1>{esc(page_data["headline"])}</h1><p>{esc(page_data["intro"])}</p>'
            f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(page_data["cta_label"])}</a><a class="button button-secondary" href="{service_href}">{esc(service_label)}</a></div></div>'
            f'<aside class="page-hero-panel"><p class="eyebrow">{esc(page_data["eyebrow"])}</p><h2>{esc(page_data["panel_title"])}</h2><p>{esc(page_data["panel_copy"])}</p></aside>',
            'hero-band page-hero-band',
            'layout-shell page-hero',
        )
        + render_custom_content_section({'eyebrow': scope_eyebrow, 'title': scope_title, 'items': page_data['items']})
        + render_custom_content_section({'eyebrow': benefit_eyebrow, 'title': benefit_title, 'cards': page_data['benefits']})
        + inline_cta_band(page_data['cta_title'], page_data['cta_copy'], routes[lang]['contact'], page_data['cta_label'])
    )
    return body

def inline_cta_band(title, copy, href, label):
    return band_section(
        f'<div><p class="eyebrow">{esc(label)}</p><h2>{esc(title)}</h2><p>{esc(copy)}</p></div>'
        f'<div class="cta-actions"><a class="button button-primary" href="{href}">{esc(label)}</a></div>',
        'inline-cta-section',
        'layout-shell cta-band',
    )


def offer_catalog_schema(lang):
    catalog_id = absolute_url(routes[lang]['services']) + '#catalog'
    items = []
    for key in order:
        service_name = services[key][lang]['name']
        service_url = absolute_url(routes[lang][key])
        items.append({
            '@type': 'Offer',
            'url': service_url,
            'itemOffered': {
                '@type': 'Service',
                'name': service_name,
                'serviceType': service_name,
                'description': services[key][lang]['summary'],
                'url': service_url,
                'provider': {'@id': BUSINESS_ID},
                'areaServed': AREA_SERVED_SCHEMA,
            },
        })
    return {
        '@type': 'OfferCatalog',
        '@id': catalog_id,
        'name': T[lang]['services'],
        'itemListElement': items,
    }


def social_meta_values(lang, key, title, desc, canonical_url, article_meta=None, image_url=None, image_alt=''):
    meta = {
        'og_title': title,
        'og_description': desc,
        'twitter_title': title,
        'twitter_description': desc,
        'og_url': canonical_url,
        'og_type': 'website',
        'og_image': absolute_url(OG_IMAGE_URL),
        'og_image_type': OG_IMAGE_MIME_TYPE,
        'og_image_width': OG_IMAGE_WIDTH,
        'og_image_height': OG_IMAGE_HEIGHT,
        'og_image_alt': 'Opticable preview image',
        'twitter_card': 'summary_large_image',
        'meta_author': '',
        'article_published_time': '',
        'article_modified_time': '',
        'article_section': '',
        'article_tags': (),
    }
    if lang == 'fr' and key == 'home':
        meta.update({
            'og_title': "Caméras, accès, WiFi et câblage commercial | Opticable",
            'og_description': "Installation et gestion de systèmes technologiques pour immeubles commerciaux au Québec. Montréal, Laval, Longueuil et partout au Québec.",
            'twitter_title': "Caméras, accès, WiFi et câblage commercial | Opticable",
            'twitter_description': "Installation et gestion de systèmes pour immeubles commerciaux au Québec.",
            'og_url': absolute_url('/'),
        })
    if article_meta:
        meta.update({
            'og_type': 'article',
            'og_image': article_meta['social_image']['url'],
            'og_image_type': article_meta['social_image']['mime_type'],
            'og_image_width': article_meta['social_image']['width'],
            'og_image_height': article_meta['social_image']['height'],
            'og_image_alt': article_meta['headline'],
            'meta_author': article_meta['author'],
            'article_published_time': article_meta['published_iso'],
            'article_modified_time': article_meta['modified_iso'],
            'article_section': article_meta['section'],
            'article_tags': tuple(article_meta['tags']),
        })
    elif image_url:
        image = image_meta_for_url(image_url, image_alt or title)
        meta.update({
            'og_image': image['url'],
            'og_image_type': image['mime_type'],
            'og_image_width': image['width'],
            'og_image_height': image['height'],
            'og_image_alt': image['alt'],
        })
    return meta


def quote_lead_tracking_snippet(lang):
    payload = {
        'event_category': 'quote',
        'event_label': 'zoho_quote_redirect',
        'lead_source': 'zoho_quote_form',
        'quote_locale': lang,
    }
    payload_json = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
    ads_conversion = ''
    if GOOGLE_ADS_QUOTE_CONVERSION_SEND_TO:
        ads_conversion = (
            f"window.gtag('event','conversion',{{send_to:"
            f"{json.dumps(GOOGLE_ADS_QUOTE_CONVERSION_SEND_TO)}}});"
        )
    return (
        '<script>'
        '(function(){'
        f'var payload={payload_json};'
        "if(Array.isArray(window.dataLayer)){window.dataLayer.push(Object.assign({event:'quote_request_submitted'},payload));}"
        "if(typeof window.gtag==='function'){window.gtag('event','generate_lead',payload);"
        f'{ads_conversion}'
        '}'
        '})();'
        '</script>'
    )


def schema(lang, page_key, title, desc, faq_items=None, service_name=None, breadcrumb_items=None, page_url=None, article_meta=None, page_image_url=None, page_image_alt=''):
    page_url = page_url or absolute_url(routes[lang][page_key])
    catalog = offer_catalog_schema(lang)
    schema_logo_width, schema_logo_height = image_dimensions_for_url(LOGO_UI_SCHEMA_URL)
    business = {
        '@type': 'LocalBusiness',
        '@id': BUSINESS_ID,
        'name': 'Opticable',
        'legalName': LEGAL_BUSINESS_NAME,
        'url': absolute_url(default_route('home')),
        'logo': absolute_url(LOGO_UI_SCHEMA_URL),
        'image': absolute_url(OG_IMAGE_URL),
        'description': SCHEMA_BUSINESS_DESCRIPTION[lang],
        'serviceType': [services[k][lang]['name'] for k in order],
        'areaServed': SCHEMA_AREA_SERVED_NAMES[lang],
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Montréal', 'addressRegion': 'QC', 'addressCountry': 'CA'},
        'availableLanguage': [language_tag('en'), language_tag('fr')],
        'openingHoursSpecification': OPENING_HOURS_SPEC,
        'hasOfferCatalog': {'@id': catalog['@id']},
        'telephone': '514-316-7236',
        'email': 'info@opticable.ca',
        'hasCredential': f'Licence RBQ {RBQ_LICENSE_NUMBER}',
        'sameAs': SOCIAL_PROFILE_URLS,
        'identifier': [{'@type': 'PropertyValue', 'name': 'RBQ License', 'value': RBQ_LICENSE_NUMBER}],
    }
    contact = contact_details(lang)
    contact_points = []
    if contact.get('general_email'):
        point = {'@type': 'ContactPoint', 'contactType': 'customer service', 'email': contact['general_email'], 'availableLanguage': [language_tag('en'), language_tag('fr')]}
        if contact.get('phone'):
            point['telephone'] = contact['phone']
        contact_points.append(point)
    if contact.get('project_email'):
        point = {'@type': 'ContactPoint', 'contactType': 'sales', 'email': contact['project_email'], 'availableLanguage': [language_tag('en'), language_tag('fr')]}
        if contact.get('phone'):
            point['telephone'] = contact['phone']
        contact_points.append(point)
    if contact_points:
        business['contactPoint'] = contact_points
    page_types = ['WebPage', 'ContactPage'] if page_key == 'contact' else 'WebPage'
    page = {
        '@type': page_types,
        '@id': page_url + '#webpage',
        'url': page_url,
        'name': title,
        'description': desc,
        'inLanguage': language_tag(lang),
        'isPartOf': {'@id': WEBSITE_ID},
        'about': {'@id': BUSINESS_ID},
    }
    if page_key == 'services':
        page['mainEntity'] = {'@id': catalog['@id']}
    graph = [
        {'@type': 'WebSite', '@id': WEBSITE_ID, 'url': absolute_url('/'), 'name': 'Opticable', 'inLanguage': [language_tag('en'), language_tag('fr')]},
        business,
        catalog,
    ]
    if breadcrumb_items:
        crumb = breadcrumb_schema(breadcrumb_items, page_url)
        graph.append(crumb)
        page['breadcrumb'] = {'@id': crumb['@id']}
    graph.append(page)
    if service_name:
        graph.append({'@type': 'Service', '@id': page_url + '#service', 'name': service_name, 'description': desc, 'serviceType': service_name, 'provider': {'@id': BUSINESS_ID}, 'url': page_url, 'areaServed': AREA_SERVED_SCHEMA})
    if faq_items:
        graph.append({'@type': 'FAQPage', '@id': page_url + '#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq_items]})
    if page_image_url:
        page['primaryImageOfPage'] = {
            '@type': 'ImageObject',
            'url': absolute_url(page_image_url),
            'width': image_dimensions_for_url(page_image_url)[0],
            'height': image_dimensions_for_url(page_image_url)[1],
            'caption': page_image_alt or title,
        }
    if article_meta:
        article_image = {
            '@type': 'ImageObject',
            'url': article_meta['image']['url'],
            'width': article_meta['image']['width'],
            'height': article_meta['image']['height'],
        }
        page['mainEntity'] = {'@id': page_url + '#article'}
        page['primaryImageOfPage'] = article_image
        article = {
            '@type': 'BlogPosting',
            '@id': page_url + '#article',
            'mainEntityOfPage': {'@id': page_url + '#webpage'},
            'headline': article_meta['headline'],
            'description': article_meta['description'],
            'url': page_url,
            'inLanguage': article_meta['in_language'],
            'author': schema_author_entity(article_meta['author']),
            'publisher': {
                '@type': 'Organization',
                '@id': BUSINESS_ID,
                'name': 'Opticable',
                'logo': {
                    '@type': 'ImageObject',
                    'url': absolute_url(LOGO_UI_SCHEMA_URL),
                    'width': schema_logo_width,
                    'height': schema_logo_height,
                },
            },
            'datePublished': article_meta['published_iso'],
            'dateModified': article_meta['modified_iso'],
            'image': article_image,
            'wordCount': article_meta['word_count'],
            'timeRequired': article_meta['time_required'],
            'isAccessibleForFree': True,
        }
        if article_meta.get('section'):
            article['articleSection'] = article_meta['section']
        if article_meta.get('tags'):
            article['keywords'] = article_meta['tags']
        graph.append(article)
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=2)


def header(lang, current, page_key, lang_switch_href=None):
    t = T[lang]
    alt = 'fr' if lang == 'en' else 'en'
    switch_href = lang_switch_href or routes[alt][page_key]
    referral_program_keys = {'referral-program', 'referral-program-terms'}
    referral_partner_keys = {'referral-partner-program', 'referral-partner-program-terms'}
    referral_portal_keys = {'referral-portal', 'referral-access'}
    referral_nav = nav_dropdown_links(
        'Referrals & Partners' if lang == 'en' else 'Références et partenaires',
        routes[lang]['referral-program'],
        current in referral_program_keys or current in referral_partner_keys or current in referral_portal_keys,
        (
            {
                'href': routes[lang]['referral-program'],
                'label': 'Referral Program' if lang == 'en' else 'Programme de référence',
                'current': current in referral_program_keys,
            },
            {
                'href': routes[lang]['referral-partner-program'],
                'label': 'Business Partners' if lang == 'en' else "Partenaires d'affaires",
                'current': current in referral_partner_keys,
            },
            {
                'href': routes[lang]['referral-portal'],
                'label': 'Member Portal' if lang == 'en' else 'Espace membre',
                'current': current in referral_portal_keys,
            },
        ),
    )
    nav = [
        simple_nav_link(lang, 'home', current),
        nav_dropdown(lang, 'services', current, order, wide=True),
        nav_dropdown(lang, 'industries', current, ('case-studies',)),
        referral_nav,
        simple_nav_link(lang, 'about', current),
        simple_nav_link(lang, 'faq', current),
        blog_nav_item(lang, current),
        simple_nav_link(lang, 'contact', current),
    ]
    return f'<header class="site-header"><div class="header-inner"><a class="brand" href="{routes[lang]["home"]}" aria-label="Opticable {esc(t["home"]).lower()}">{logo_img("header")}</a><button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="site-nav">{esc(t["menu"])}</button><nav class="site-nav" id="site-nav" data-site-nav aria-label="Primary navigation">{"".join(nav)}</nav><div class="header-actions"><a class="lang-switch" href="{switch_href}" lang="{language_tag(alt)}">{esc(t["switch"])}</a><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a></div></div></header>'


def footer_contact_items(lang):
    return ''.join(
        f'<li><strong>{esc(label)}</strong><span>{contact_value_html(label, value)}</span></li>'
        for label, value in T[lang]['contact_cards']
    )


def cookie_banner(lang):
    t = T[lang]
    return (
        f'<aside class="cookie-banner" data-cookie-banner hidden><div class="cookie-banner-copy">'
        f'<p class="eyebrow">{esc(t["cookie_banner_eyebrow"])}</p><strong>{esc(t["cookie_banner_title"])}</strong>'
        f'<p>{esc(t["cookie_banner_copy"])}</p></div><div class="cookie-banner-actions">'
        f'<a class="button button-secondary" href="{routes[lang]["privacy"]}">{esc(t["privacy"])}</a>'
        f'<button class="button button-primary" type="button" data-cookie-accept>{esc(t["cookie_banner_accept"])}</button></div></aside>'
    )


def image_lightbox(lang):
    ui = LIGHTBOX_UI.get(lang, LIGHTBOX_UI['en'])
    return (
        f'<div class="lightbox-overlay" data-image-lightbox hidden>'
        f'<div class="lightbox-dialog" role="dialog" aria-modal="true" aria-label="{esc(ui["dialog"])}">'
        f'<button class="lightbox-close" type="button" data-lightbox-close aria-label="{esc(ui["close"])}">&times;</button>'
        f'<figure class="lightbox-stage"><img class="lightbox-image" data-lightbox-image alt="" /><figcaption class="lightbox-caption" data-lightbox-caption></figcaption></figure>'
        f'</div></div>'
    )


def footer(lang):
    t = T[lang]
    quick_keys = ['home', 'services', 'industries', 'case-studies', 'blog']
    quick_keys.extend(('articles', 'guides'))
    quick_keys.extend(['about', 'faq', 'contact', 'privacy'])
    quick = ''.join(
        f'<li><a href="{routes[lang][k]}">{esc(label_for_key(lang, k))}</a></li>'
        for k in quick_keys
    )
    feat = ''.join(f'<li><a href="{routes[lang][k]}">{esc(services[k][lang]["name"])}</a></li>' for k in order)
    contact_items = footer_contact_items(lang)
    social_items = footer_social_links(lang)
    legal = f'<p class="footer-legal">{esc(LEGAL_BUSINESS_NAME)}<br />{esc(RBQ_LICENSE_LABEL)}</p>'
    return (
        f'<footer class="site-footer"><div class="footer-shell"><div class="footer-grid"><div><div class="footer-brand">{logo_img("footer")}</div><p class="footer-note">{esc(t["footer"])}</p>{legal}</div><div><p class="footer-title">{esc(t["footer_contact_title"])}</p><ul class="footer-contact-list">{contact_items}</ul></div><div><p class="footer-title">{esc(t["follow_us"])}</p><div class="footer-socials">{social_items}</div></div><div><p class="footer-title">{esc(t["menu"])}</p><ul class="footer-links">{quick}</ul></div><div><p class="footer-title">{esc(t["services"])}</p><ul class="footer-services">{feat}</ul></div></div><div class="footer-bottom">&copy; <span data-year></span> Opticable.</div></div></footer>'
    )


def cta(lang):
    t = T[lang]
    return band_section(
        f'<div><p class="eyebrow">{esc(t["cta_kicker"])}</p><h2>{esc(t["cta_title"])}</h2><p>{esc(t["cta_copy"])}</p></div><div class="cta-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["all_services"])}</a></div>',
        'cta-section',
        'layout-shell cta-band',
    )


def icon_link_tags():
    return (
        f'<link rel="icon" type="image/png" sizes="32x32" href="{FAVICON_32_URL}" />'
        f'<link rel="icon" type="image/png" sizes="192x192" href="{FAVICON_192_URL}" />'
        f'<link rel="icon" type="image/png" sizes="512x512" href="{FAVICON_512_URL}" />'
        f'<link rel="apple-touch-icon" sizes="180x180" href="{APPLE_TOUCH_ICON_URL}" />'
        f'<link rel="manifest" href="{WEBMANIFEST_URL}" />'
    )


def stylesheet_link_tags(page_key):
    tags = [f'<link rel="stylesheet" href="{STYLES_URL}" />']
    if page_key in HOME_SERVICE_STYLE_PAGE_KEYS:
        tags.append(f'<link rel="stylesheet" href="{HOME_SERVICE_STYLES_URL}" />')
    if page_key in ARTICLE_STYLE_PAGE_KEYS:
        tags.append(f'<link rel="stylesheet" href="{ARTICLE_STYLES_URL}" />')
    if page_key in PROMO_PAGE_KEYS or page_key in REFERRAL_PAGE_KEYS:
        tags.append(f'<link rel="stylesheet" href="{PROMO_REFERRAL_STYLES_URL}" />')
    if page_key == 'promo-admin' or page_key in REFERRAL_PORTAL_PAGE_KEYS or page_key in REFERRAL_ADMIN_PAGE_KEYS:
        tags.append(f'<link rel="stylesheet" href="{ADMIN_PANEL_STYLES_URL}" />')
    if page_key in REFERRAL_PUBLIC_PAGE_KEYS or page_key in REFERRAL_PORTAL_PAGE_KEYS:
        tags.append(f'<link rel="stylesheet" href="{REFERRAL_PUBLIC_STYLES_URL}" />')
    if page_key in REFERRAL_PORTAL_PAGE_KEYS:
        tags.append(f'<link rel="stylesheet" href="{REFERRAL_PORTAL_STYLES_URL}" />')
    if page_key in REFERRAL_ADMIN_PAGE_KEYS:
        tags.append(f'<link rel="stylesheet" href="{REFERRAL_ADMIN_STYLES_URL}" />')
    return ''.join(tags)


def script_tags(page_key):
    tags = [f'<script src="{SCRIPT_URL}" defer></script>']
    if page_key == 'promo':
        tags.append(f'<script src="{PROMO_PUBLIC_SCRIPT_URL}" defer></script>')
    if page_key == 'promo-unsubscribe':
        tags.append(f'<script src="{PROMO_UNSUBSCRIBE_SCRIPT_URL}" defer></script>')
    if page_key == 'promo-admin':
        tags.append(f'<script src="{PROMO_ADMIN_SCRIPT_URL}" defer></script>')
    if page_key in REFERRAL_PUBLIC_PAGE_KEYS:
        tags.append(f'<script src="{REFERRAL_PUBLIC_SCRIPT_URL}" defer></script>')
    if page_key in REFERRAL_PORTAL_PAGE_KEYS:
        tags.append(f'<script src="{REFERRAL_PORTAL_SCRIPT_URL}" defer></script>')
    if page_key in REFERRAL_ADMIN_PAGE_KEYS:
        tags.append(f'<script src="{REFERRAL_ADMIN_SCRIPT_URL}" defer></script>')
    return ''.join(tags)


def page(lang, key, current, title, desc, body, faq_items=None, service_name=None, breadcrumb_items=None, robots='index, follow, max-image-preview:large', canonical_path=None, include_alternates=True, resource_key=None, schema_page_url=None, alternate_paths=None, lang_switch_href=None, article_meta=None, preload_image_url=None, social_image_url=None, social_image_alt=''):
    t = T[lang]
    canonical_url = absolute_url(canonical_path or routes[lang][key])
    robots_value = effective_robots_value(robots)
    social_meta = social_meta_values(lang, key, title, desc, canonical_url, article_meta=article_meta, image_url=social_image_url, image_alt=social_image_alt)
    alternate_tags = ''
    og_locale_alternates = ''
    if include_alternates:
        alternate_paths = alternate_paths or {}
        en_alternate = absolute_url(alternate_paths.get('en') or routes['en'][key])
        fr_alternate = absolute_url(alternate_paths.get('fr') or routes['fr'][key])
        default_url = absolute_url(alternate_paths.get('fr') or default_route(key))
        alternate_tags = (
            f'<link rel="alternate" hreflang="{language_tag("en")}" href="{en_alternate}" />'
            f'<link rel="alternate" hreflang="{language_tag("fr")}" href="{fr_alternate}" />'
            f'<link rel="alternate" hreflang="x-default" href="{default_url}" />'
        )
        other_lang = 'fr' if lang == 'en' else 'en'
        other_path = alternate_paths.get(other_lang)
        if other_path:
            og_locale_alternates = f'<meta property="og:locale:alternate" content="{T[other_lang]["locale"]}" />'
    article_meta_tags = ''
    if article_meta:
        article_meta_tags = (
            f'<meta name="author" content="{esc(article_meta["author"])}" />'
            f'<meta property="article:published_time" content="{esc(article_meta["published_iso"])}" />'
            f'<meta property="article:modified_time" content="{esc(article_meta["modified_iso"])}" />'
            f'<meta property="og:updated_time" content="{esc(article_meta["modified_iso"])}" />'
        )
        if article_meta.get('section'):
            article_meta_tags += f'<meta property="article:section" content="{esc(article_meta["section"])}" />'
        article_meta_tags += ''.join(f'<meta property="article:tag" content="{esc(tag)}" />' for tag in article_meta['tags'])
    body_class = f'lang-{lang} page-{key}'
    return f'<!doctype html><html lang="{language_tag(lang)}"><head>{GOOGLE_TAG_SNIPPET}<meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>{esc(title)}</title><meta name="description" content="{esc(desc)}" /><meta name="robots" content="{esc(robots_value)}" /><meta name="theme-color" content="#153628" />{icon_link_tags()}<link rel="canonical" href="{canonical_url}" />{alternate_tags}<meta property="og:type" content="{esc(social_meta["og_type"])}" /><meta property="og:site_name" content="Opticable" /><meta property="og:locale" content="{t["locale"]}" />{og_locale_alternates}<meta property="og:title" content="{esc(social_meta["og_title"])}" /><meta property="og:description" content="{esc(social_meta["og_description"])}" /><meta property="og:url" content="{esc(social_meta["og_url"])}" /><meta property="og:image" content="{social_meta["og_image"]}" /><meta property="og:image:type" content="{esc(social_meta["og_image_type"])}" /><meta property="og:image:alt" content="{esc(social_meta["og_image_alt"])}" /><meta property="og:image:width" content="{social_meta["og_image_width"]}" /><meta property="og:image:height" content="{social_meta["og_image_height"]}" /><meta name="twitter:card" content="{esc(social_meta["twitter_card"])}" /><meta name="twitter:title" content="{esc(social_meta["twitter_title"])}" /><meta name="twitter:description" content="{esc(social_meta["twitter_description"])}" /><meta name="twitter:image" content="{social_meta["og_image"]}" /><meta name="twitter:image:alt" content="{esc(social_meta["og_image_alt"])}" />{article_meta_tags}{resource_hints(resource_key or key, preload_image_url=preload_image_url)}{stylesheet_link_tags(key)}<script type="application/ld+json">{schema(lang, key, title, desc, faq_items, service_name, breadcrumb_items, page_url=schema_page_url or canonical_url, article_meta=article_meta, page_image_url=social_image_url, page_image_alt=social_image_alt)}</script></head><body class="{body_class}"><a class="skip-link" href="#content">{esc(t["skip"])}</a><div class="site-shell">{header(lang, current, key, lang_switch_href)}{cookie_banner(lang)}<main id="content">{body}</main>{footer(lang)}</div>{image_lightbox(lang)}{script_tags(key)}</body></html>'
def clients_section(lang):
    return f'<div class="grid-4">{"".join(card(title, text) for title, text in T[lang]["clients"])}</div>'

def industries_section(lang):
    return f'<div class="grid-3">{"".join(card(title, text) for title, text in industry_cards[lang])}</div>'

def coverage_section(lang):
    t = T[lang]
    return band_section(
        f'<div class="section-heading"><p class="eyebrow">{esc(t["service_area_eyebrow"])}</p>'
        f'<h2>{esc(t["service_area_title"])}</h2><p>{esc(t["service_area_intro"])}</p></div>'
        f'{render_chips(t["service_area_regions"])}',
        'coverage-section',
    )

def flat_faq_items(lang):
    return [(q, a) for _, _, items in faq_groups[lang] for q, a in items]


def faq_sections(lang):
    sections = []
    for title, intro, items in faq_groups[lang]:
        faq_items = ''.join(
            f'<details class="faq-item" open><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
            for q, a in items
        )
        block = band_section(
            f'<div class="section-heading"><p class="eyebrow">FAQ</p><h2>{esc(title)}</h2><p>{esc(intro)}</p></div>'
            f'<div class="faq-list">{faq_items}</div>',
            'faq-section',
        )
        sections.append(block)
    return ''.join(sections)

def form_section(lang):
    form_config = ZOHO_FORM_CONFIG[lang]
    container_id = f'zf_div_quote_{lang}'
    iframe_src = json.dumps(form_config['src'] + '?zf_rszfm=1')
    iframe_height = json.dumps(f"{form_config['height']}px")
    aria_label = json.dumps(form_config['aria_label'])
    script = (
        "<script type=\"text/javascript\">"
        "(function(){"
        "try{"
        f"var ifrmSrc={iframe_src};"
        f"var mount=document.getElementById('{container_id}');"
        "if(!mount){return;}"
        "var f=document.createElement('iframe');"
        "try{"
        "if(typeof ZFAdvLead!=='undefined'&&typeof zfutm_zfAdvLead!=='undefined'){"
        "for(var prmIdx=0;prmIdx<ZFAdvLead.utmPNameArr.length;prmIdx++){"
        "var utmPm=ZFAdvLead.utmPNameArr[prmIdx];"
        "utmPm=(ZFAdvLead.isSameDomian&&(ZFAdvLead.utmcustPNameArr.indexOf(utmPm)===-1))?'zf_'+utmPm:utmPm;"
        "var utmVal=zfutm_zfAdvLead.zfautm_gC_enc(ZFAdvLead.utmPNameArr[prmIdx]);"
        "if(typeof utmVal!=='undefined'&&utmVal!==''){ifrmSrc+=(ifrmSrc.indexOf('?')>0?'&':'?')+utmPm+'='+utmVal;}"
        "}"
        "}"
        "if(typeof ZFLead!=='undefined'&&typeof zfutm_zfLead!=='undefined'){"
        "for(var leadIdx=0;leadIdx<ZFLead.utmPNameArr.length;leadIdx++){"
        "var leadPm=ZFLead.utmPNameArr[leadIdx];"
        "var leadVal=zfutm_zfLead.zfutm_gC_enc(ZFLead.utmPNameArr[leadIdx]);"
        "if(typeof leadVal!=='undefined'&&leadVal!==''){ifrmSrc+=(ifrmSrc.indexOf('?')>0?'&':'?')+leadPm+'='+leadVal;}"
        "}"
        "}"
        "}catch(e){}"
        "f.src=ifrmSrc;"
        "f.style.border='none';"
        f"f.style.height={iframe_height};"
        "f.style.width='100%';"
        "f.style.transition='all 0.5s ease';"
        "f.setAttribute('allow','geolocation');"
        f"f.setAttribute('aria-label',{aria_label});"
        "mount.appendChild(f);"
        "window.addEventListener('message',function(event){"
        "var evntData=event.data;"
        "if(evntData&&evntData.constructor===String){"
        "var zf_ifrm_data=evntData.split('|');"
        "if(zf_ifrm_data.length===2||zf_ifrm_data.length===3){"
        "var zf_perma=zf_ifrm_data[0];"
        "var zf_ifrm_ht_nw=(parseInt(zf_ifrm_data[1],10)+15)+'px';"
        "var iframe=mount.getElementsByTagName('iframe')[0];"
        "if(iframe&&iframe.src.indexOf('formperma')>0&&iframe.src.indexOf(zf_perma)>0){"
        "var prevIframeHeight=iframe.style.height;"
        "var zf_tout=false;"
        "if(zf_ifrm_data.length===3){iframe.scrollIntoView();zf_tout=true;}"
        "if(prevIframeHeight!==zf_ifrm_ht_nw){"
        "if(zf_tout){setTimeout(function(){iframe.style.height=zf_ifrm_ht_nw;},500);}else{iframe.style.height=zf_ifrm_ht_nw;}"
        "}"
        "}"
        "}"
        "}"
        "},false);"
        "}catch(e){}"
        "})();"
        "</script>"
    )
    return f'<div class="form-panel zoho-form-shell"><div id="{container_id}" class="zoho-form-embed"></div>{script}</div>'

css += '''
.promo-hero-grid,.promo-services-grid,.promo-related-grid,.promo-result-grid{display:grid;gap:18px}
.promo-hero-grid{grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr)}
.promo-visual-panel{display:grid;gap:18px}
.promo-how-section .timeline{grid-template-columns:repeat(3,minmax(0,1fr));align-items:stretch}
.promo-how-section .timeline-step{min-width:0;border:1px solid rgba(255,255,255,.12);border-radius:24px;background:linear-gradient(180deg,#122018,#1b2c22)}
.promo-how-section .timeline-step span,.promo-how-section .timeline-step h3{color:#f6fbf8;white-space:normal;overflow-wrap:anywhere}
.promo-how-section .timeline-step p{color:rgba(241,247,243,.9);white-space:normal;overflow-wrap:anywhere}
.promo-inline-status,.promo-inline-error{padding:14px 16px;border-radius:18px;font-weight:700}
.promo-inline-status{background:var(--primary-soft);color:var(--primary-dark)}
.promo-inline-error{background:#fff2f2;color:#8b2020;border:1px solid rgba(139,32,32,.16)}
.promo-form-shell,.promo-unsubscribe-shell{display:grid;gap:18px}
.promo-entry-form,.promo-unsubscribe-form{display:grid;gap:18px}
.promo-skill-shell,.promo-turnstile-shell{padding:18px;border:1px solid var(--line);border-radius:20px;background:rgba(247,250,247,.92)}
.promo-skill-prompt{margin:0;color:var(--primary-dark);font-weight:700}
.promo-checklist{display:grid;gap:12px}
.promo-checklist label{display:flex;gap:12px;align-items:flex-start;color:var(--muted);line-height:1.55}
.promo-checklist input{margin-top:4px;width:18px;height:18px;accent-color:var(--primary)}
.promo-checklist a{color:var(--primary-dark);font-weight:700}
.promo-consent-copy{display:grid;gap:8px}
.promo-consent-text{display:block}
.promo-consent-links{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.promo-consent-links a{display:inline-flex;align-items:center;min-height:34px;padding:0 12px;border-radius:999px;background:rgba(21,54,40,.08);border:1px solid rgba(21,54,40,.12);white-space:nowrap}
.promo-consent-separator{color:rgba(21,54,40,.5);font-weight:700}
.promo-submit[disabled]{opacity:.64;cursor:not-allowed}
.promo-result-overlay{position:fixed;inset:0;z-index:140;display:grid;place-items:center;padding:24px;background:rgba(13,22,17,.78);backdrop-filter:blur(10px)}
.promo-result-overlay[hidden]{display:none}
.promo-result-dialog{position:relative;width:min(620px,100%);display:grid;gap:18px;padding:28px}
.promo-result-close{position:absolute;top:18px;right:18px;width:42px;height:42px;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--text);font-size:1.6rem;line-height:1}
.promo-result-copy{margin:0;color:var(--muted);line-height:1.55}
.promo-result-code-shell{display:grid;gap:10px;padding:16px;border:1px solid var(--line);border-radius:20px;background:var(--surface-soft)}
.promo-result-code-shell strong{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--primary-dark)}
.promo-result-code-row{display:grid;grid-template-columns:1fr;gap:12px;align-items:start}
.promo-result-code-actions{display:flex;flex-wrap:wrap;gap:10px}
.promo-result-code-input{width:100%;padding:14px 16px;border:1px solid var(--line-strong);border-radius:16px;background:#fff;color:var(--primary-dark);font-size:clamp(.96rem,2.4vw,1.08rem);font-weight:800;letter-spacing:.04em;text-transform:uppercase;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;text-align:center}
.promo-copy-button,.promo-save-button{min-width:148px}
.promo-result-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
.promo-result-grid-compact{grid-template-columns:repeat(2,minmax(0,1fr))}
.promo-code{font-size:1.1rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--primary-dark)}
.promo-result-actions{display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.promo-result-rules-link{font-weight:700;color:var(--primary-dark)}
.promo-rules-summary-section .grid-2,.promo-rules-section .grid-2{display:grid;gap:18px;grid-template-columns:repeat(2,minmax(0,1fr))}
.promo-odds-panel{overflow-x:auto}
.promo-odds-table{width:100%;border-collapse:collapse}
.promo-odds-table th,.promo-odds-table td{padding:14px 12px;border-bottom:1px solid var(--line);text-align:left}
.promo-odds-table thead th{font-size:.86rem;letter-spacing:.12em;text-transform:uppercase;color:var(--primary-dark)}
.promo-reminder-panel{display:grid;gap:12px;padding:20px 22px;border-radius:22px}
.promo-reminder-copy{display:grid;gap:4px}
.promo-reminder-title{margin:0;font-family:"Segoe UI Variable Display","Aptos Display","Segoe UI",sans-serif;font-size:1.22rem;line-height:1.15}
.promo-reminder-text{margin:0;font-size:.95rem;line-height:1.45;color:var(--muted)}
.promo-reminder-grid{gap:12px}
.promo-reminder-panel .detail-item{padding:12px 14px;border-radius:16px}
.promo-reminder-panel .detail-item strong{margin-bottom:4px;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--primary-dark)}
.promo-reminder-panel .detail-item p{margin:0;line-height:1.35}
.promo-reminder-panel .promo-code{font-size:1rem;letter-spacing:.04em}
.promo-reminder-actions{display:flex;justify-content:flex-start}
.promo-reminder-link{font-weight:700;color:var(--primary-dark)}
.promo-cta-band{border-color:rgba(47,138,88,.22)}
.promo-services-grid,.promo-related-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
.promo-admin-shell{display:grid;gap:20px}
.promo-admin-toolbar{display:flex;flex-wrap:wrap;justify-content:space-between;gap:16px;align-items:center}
.promo-admin-scope{display:flex;flex-wrap:wrap;gap:10px}
.promo-admin-scope .button[aria-pressed="true"]{background:var(--primary-dark);border-color:var(--primary-dark);color:#fff}
.promo-admin-actions{display:flex;flex-wrap:wrap;gap:10px}
.promo-admin-summary,.promo-admin-meta{display:grid;gap:18px}
.promo-admin-summary{grid-template-columns:repeat(4,minmax(0,1fr))}
.promo-admin-meta{grid-template-columns:repeat(3,minmax(0,1fr))}
.promo-admin-meta .detail-item p,.promo-admin-summary .detail-item p{margin:0;line-height:1.4;color:var(--text)}
.promo-admin-select-all{display:inline-flex;align-items:center;gap:10px;font-weight:700}
.promo-admin-select-all input,.promo-admin-table tbody input[type="checkbox"]{width:18px;height:18px;accent-color:var(--primary)}
.promo-admin-table-shell{overflow:auto;border:1px solid var(--line);border-radius:24px;background:#fff}
.promo-admin-table{width:100%;min-width:1180px;border-collapse:collapse}
.promo-admin-table th,.promo-admin-table td{padding:14px 16px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.promo-admin-table thead th{position:sticky;top:0;background:var(--surface-soft);font-size:.76rem;letter-spacing:.14em;text-transform:uppercase;color:var(--primary-dark);z-index:1}
.promo-admin-table tbody tr:nth-child(even){background:rgba(247,250,247,.6)}
.promo-admin-code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.promo-admin-empty{padding:20px 22px;border:1px dashed var(--line-strong);border-radius:20px;background:var(--surface-soft);color:var(--muted)}
.promo-admin-actions .is-disabled{pointer-events:none;opacity:.6}
@media (max-width:920px){
  .promo-hero-grid,.promo-how-section .timeline,.promo-result-grid,.promo-rules-summary-section .grid-2,.promo-rules-section .grid-2,.promo-services-grid,.promo-related-grid,.promo-admin-summary,.promo-admin-meta{grid-template-columns:1fr}
  .promo-reminder-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
}
@media (max-width:640px){
  .promo-result-dialog{padding:24px 20px}
  .promo-result-code-row{grid-template-columns:1fr}
  .promo-result-code-actions{display:grid;grid-template-columns:1fr}
  .promo-copy-button,.promo-save-button{width:100%}
  .promo-reminder-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .promo-reminder-grid .detail-item:nth-child(2){grid-column:1/-1}
  .promo-admin-toolbar,.promo-admin-actions,.promo-admin-scope{display:grid;grid-template-columns:1fr}
}
'''

css += '''
.referral-checklist{margin-top:4px}
.referral-program-page{display:grid;gap:0;grid-template-columns:minmax(0,1fr)}
.referral-program-page > *{min-width:0}
.referral-magic-link{display:grid;gap:10px}
.referral-nav{display:grid;gap:14px;grid-template-columns:repeat(4,minmax(0,1fr))}
.referral-nav-card{display:grid;gap:8px;padding:18px 20px;border:1px solid rgba(21,54,40,.14);border-radius:22px;background:#fff;color:var(--text);text-decoration:none;box-shadow:0 18px 34px rgba(10,31,23,.06)}
.referral-nav-card strong{color:var(--primary-dark);font-size:.98rem}
.referral-nav-card span{color:var(--muted);line-height:1.5}
.referral-nav-card:hover,.referral-nav-card:focus-visible{border-color:rgba(47,138,88,.32);box-shadow:0 20px 38px rgba(10,31,23,.10)}
.referral-nav-card.is-current{background:linear-gradient(135deg,rgba(21,54,40,.98),rgba(32,78,57,.96));border-color:rgba(21,54,40,.96);color:#fff}
.referral-nav-card.is-current strong,.referral-nav-card.is-current span{color:#fff}
.referral-steps-section .timeline{grid-template-columns:repeat(4,minmax(0,1fr))}
.referral-steps-section .timeline-step{min-width:0;border:1px solid rgba(255,255,255,.12)!important;border-radius:24px;background:linear-gradient(180deg,#122018,#1b2c22)!important;color:#f6fbf8!important;box-shadow:0 18px 34px rgba(10,31,23,.16)!important}
.referral-steps-section .timeline-step span,.referral-steps-section .timeline-step h3{color:#f6fbf8!important;white-space:normal;overflow-wrap:anywhere}
.referral-steps-section .timeline-step p{color:rgba(241,247,243,.9)!important;white-space:normal;overflow-wrap:anywhere}
.referral-program-page .referral-program-visual,.referral-program-page .referral-program-compare{border:1px solid rgba(21,54,40,.10)}
.referral-program-page.is-client-program .referral-program-visual{background:linear-gradient(135deg,#173826,#2b6c49);color:#f5fbf7}
.referral-program-page.is-client-program .referral-program-visual p,.referral-program-page.is-client-program .referral-program-visual li{color:rgba(245,251,247,.92)!important}
.referral-program-page.is-client-program .referral-program-visual .eyebrow{color:#bfe5cb}
.referral-program-page.is-client-program .referral-program-visual h2{color:#fff!important}
.referral-program-page.is-client-program .referral-program-compare strong,.referral-program-page.is-client-program .referral-program-compare .eyebrow{color:#1f6640}
.referral-program-page.is-partner-program .referral-program-visual{background:linear-gradient(135deg,#16263d,#264c7b);color:#f7faff}
.referral-program-page.is-partner-program .referral-program-visual p,.referral-program-page.is-partner-program .referral-program-visual li{color:rgba(247,250,255,.92)!important}
.referral-program-page.is-partner-program .referral-program-visual .eyebrow{color:#c4dbff}
.referral-program-page.is-partner-program .referral-program-visual h2{color:#fff!important}
.referral-program-page.is-partner-program .referral-program-compare strong,.referral-program-page.is-partner-program .referral-program-compare .eyebrow{color:#16365b}
.referral-program-page.is-partner-program .referral-steps-section .timeline-step{background:linear-gradient(180deg,#16263d,#203552)!important}
.referral-program-page.is-partner-program .referral-nav-card:hover,.referral-program-page.is-partner-program .referral-nav-card:focus-visible{border-color:rgba(38,76,123,.32);box-shadow:0 20px 38px rgba(20,38,61,.10)}
.referral-program-page.is-partner-program .referral-nav-card.is-current{background:linear-gradient(135deg,rgba(22,38,61,.98),rgba(38,76,123,.96));border-color:rgba(22,38,61,.96)}
.referral-contact-stack,.referral-admin-grids,.referral-portal-grids{display:grid;gap:20px}
.referral-access-shell{display:grid;gap:20px;background:#fff;color:var(--text)}
.referral-access-card{display:grid;gap:16px}
.referral-access-ready,.referral-access-request{display:grid;gap:16px}
.referral-contact-stack{align-content:start}
.referral-portal-shell,.referral-admin-shell{display:grid;gap:20px}
.referral-apply-shell,.referral-portal-shell,.referral-admin-shell{background:#fff;color:var(--text)}
.referral-apply-shell h2,.referral-portal-shell h2,.referral-admin-shell h2,.referral-access-shell h2,.referral-access-shell h3{color:var(--text)}
.referral-apply-shell p,.referral-portal-shell p,.referral-admin-shell p,.referral-access-shell p{color:inherit}
.referral-portal-header{display:flex;flex-wrap:wrap;align-items:flex-start;justify-content:space-between;gap:16px}
.referral-portal-copy{display:grid;gap:6px}
.referral-portal-copy h2{margin:0;font-family:"Segoe UI Variable Display","Aptos Display","Segoe UI",sans-serif}
.referral-portal-copy p{margin:0;color:var(--muted)}
.referral-auth-grid,.referral-admin-grids,.referral-portal-grids{display:grid;gap:20px}
.referral-auth-card,.referral-program-banner,.referral-portal-help,.referral-portal-security{display:grid;gap:12px}
.referral-program-banner{border:1px solid rgba(21,54,40,.10);background:linear-gradient(135deg,#173826,#254f39);color:#f5fbf7}
.referral-program-banner p{color:rgba(245,251,247,.92)!important}
.referral-program-banner .eyebrow{color:#bfe5cb}
.referral-program-banner h2{color:#fff!important}
.referral-portal-shell.is-client .referral-program-banner{background:linear-gradient(135deg,#173826,#2b6c49)}
.referral-portal-shell.is-partner .referral-program-banner{background:linear-gradient(135deg,#16263d,#264c7b)}
.referral-portal-shell.is-partner .referral-program-banner .eyebrow{color:#c4dbff}
.referral-portal-shell.is-partner .detail-item{border-color:rgba(38,76,123,.22)}
.referral-portal-shell.is-partner .detail-item strong{color:#16365b}
.referral-portal-shell.is-client .detail-item strong{color:#1f6640}
.referral-portal-stats{grid-template-columns:repeat(6,minmax(0,1fr))}
.referral-portal-meta-grid{grid-template-columns:repeat(4,minmax(0,1fr))}
.referral-portal-grids{grid-template-columns:1fr}
.referral-portal-stats .detail-item,.referral-portal-meta-grid .detail-item,.referral-credit-meta .detail-item{min-width:0}
.referral-portal-stats .detail-item strong,.referral-portal-meta-grid .detail-item strong,.referral-credit-meta .detail-item strong{line-height:1.35;overflow-wrap:anywhere}
.referral-summary-note,.referral-section-intro{margin:0}
.referral-share-item{grid-column:span 2}
.referral-portal-help{display:grid;gap:12px}
.referral-help-list{display:grid;gap:10px}
.referral-credit-panel{display:grid;gap:16px}
.referral-credit-meta{grid-template-columns:repeat(3,minmax(0,1fr))}
.referral-credit-grid{grid-template-columns:minmax(0,280px)}
.referral-share-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:start}
.referral-share-link{display:block;min-width:0;overflow-wrap:anywhere;word-break:break-word}
.referral-copy-button{min-width:112px}
.referral-inline-note{display:block;margin-top:8px;color:var(--muted);font-size:.92rem}
.referral-password-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
.referral-admin-form-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
.referral-status-field{grid-column:span 2}
.referral-status-field select,.referral-status-filter-field select{min-width:220px}
.referral-admin-checkbox{display:flex;align-items:flex-start;gap:10px;padding:14px 16px;border:1px solid var(--line);border-radius:16px;background:var(--surface-soft);font-weight:600}
.referral-admin-checkbox input{width:18px;height:18px;accent-color:var(--primary);margin-top:2px}
.referral-admin-action-stack,.referral-admin-code-stack{display:grid;gap:8px}
.referral-admin-action-stack .button{width:100%}
.referral-admin-view-button{padding:0;border:0;background:none;color:var(--primary-dark);font-weight:700;text-align:left}
.referral-admin-view-button:hover,.referral-admin-view-button:focus-visible{text-decoration:underline}
.referral-admin-code-stack .promo-admin-code{margin:0}
.referral-admin-filters{display:grid;gap:16px;grid-template-columns:repeat(3,minmax(0,1fr));margin-bottom:18px}
.referral-admin-detail-panel{display:grid;gap:18px}
.referral-admin-detail-header{display:flex;flex-wrap:wrap;align-items:flex-start;justify-content:space-between;gap:16px}
.referral-admin-detail-header h3{margin:0}
.referral-admin-detail-header p{margin:0;color:var(--muted)}
.referral-admin-section-header{display:grid;gap:6px}
.referral-admin-section-header h3,.referral-admin-section-header p{margin:0}
.referral-admin-section-header p{color:var(--muted)}
.referral-admin-projects-panel{display:grid;gap:18px}
.referral-admin-detail-grid{grid-template-columns:repeat(4,minmax(0,1fr))}
.referral-admin-detail-tables{align-items:start}
.referral-admin-grids{grid-template-columns:1fr}
.referral-mini-table,.referral-admin-table{min-width:1320px}
.referral-portal-cases-table th:nth-child(3),.referral-portal-cases-table td:nth-child(3){min-width:170px}
.referral-admin-cases-table th:nth-child(4),.referral-admin-cases-table td:nth-child(4){min-width:170px}
.referral-detail-cases-table th:nth-child(2),.referral-detail-cases-table td:nth-child(2){min-width:170px}
.referral-portal-grids .contact-panel,.referral-admin-detail-panel .contact-panel,.referral-admin-shell > .contact-panel{overflow:hidden}
.referral-mini-table th,.referral-admin-table th{white-space:nowrap}
.referral-mini-table td,.referral-admin-table td{white-space:nowrap}
.referral-mini-table td .form-note,.referral-admin-table td .form-note{white-space:normal;min-width:220px}
.referral-mini-table td p,.referral-admin-table td p{margin:0}
.referral-admin-table input,.referral-admin-table select{width:100%;padding:10px 12px;border:1px solid var(--line-strong);border-radius:14px;background:#fff}
@media (max-width:920px){
  .referral-nav,.referral-steps-section .timeline,.referral-portal-stats,.referral-portal-meta-grid,.referral-credit-meta,.referral-password-grid,.referral-admin-form-grid,.referral-admin-filters,.referral-admin-detail-grid{grid-template-columns:1fr}
  .referral-share-item{grid-column:auto}
  .referral-share-row{grid-template-columns:1fr}
}
'''

remove_legacy_root_build()
reset_deploy_dir()
copy_static_assets()
export_home_images()
export_blog_social_images()
js = js.replace('__GOOGLE_ADS_PROMO_CONVERSION_SEND_TO__', json.dumps(GOOGLE_ADS_PROMO_CONVERSION_SEND_TO))
css_split_marker = '.promo-hero-grid,.promo-services-grid,.promo-related-grid,.promo-result-grid{display:grid;gap:18px}'
css_split_index = css.find(css_split_marker)
if css_split_index < 0:
    raise RuntimeError('Could not split promo/referral CSS bundle')
base_css = css[:css_split_index].strip() + '\n'
article_css_marker = '.blog-grid{'
article_css_end_marker = '.case-study-systems{'
article_css_index = base_css.find(article_css_marker)
article_css_end_index = base_css.find(article_css_end_marker, article_css_index)
if article_css_index < 0 or article_css_end_index < 0:
    raise RuntimeError('Could not split article CSS bundle')
article_css = base_css[article_css_index:article_css_end_index].strip() + '\n'
article_css += '''
@media (max-width:1180px){
  .blog-grid{
    grid-template-columns:repeat(2,minmax(0,1fr));
  }
  .blog-grid-single .blog-article-card,
  .blog-article-hero,
  .blog-section-intro.blog-section-intro-split{
    grid-template-columns:1fr;
  }
  .blog-summary-grid{
    grid-template-columns:repeat(2,minmax(0,1fr));
  }
  .blog-summary-section,
  .blog-article-section,
  .blog-article-cta{
    padding:18px;
  }
}
@media (max-width:740px){
  .blog-grid{
    grid-template-columns:1fr;
  }
  .blog-card-meta,
  .blog-article-readout{
    grid-template-columns:1fr;
  }
  .blog-table{
    min-width:640px;
  }
}
'''.strip() + '\n'
base_css = (base_css[:article_css_index] + base_css[article_css_end_index:]).strip() + '\n'
home_service_css_blocks = []
for start_marker, end_marker, error_text in (
    (
        '.hero-media-panel{',
        '.hero-copy h1,.page-hero-copy h1,.section-heading h2,.cta-band h2,.gateway-panel h1,.hero-panel h2,.page-hero-panel h2{',
        'Could not split home/service visual CSS bundle',
    ),
    (
        '.hero-media-panel{',
        '.feature-card,.service-card,.card,.contact-panel,.form-panel,.faq-item{',
        'Could not split home/service division CSS bundle',
    ),
    (
        '.hero-media-panel{',
        '.timeline{',
        'Could not split home/service rich card CSS bundle',
    ),
):
    start_index = base_css.find(start_marker)
    end_index = base_css.find(end_marker, start_index)
    if start_index < 0 or end_index < 0:
        raise RuntimeError(error_text)
    home_service_css_blocks.append(base_css[start_index:end_index].strip())
    base_css = (base_css[:start_index] + base_css[end_index:]).strip() + '\n'
home_service_css = '\n'.join(block for block in home_service_css_blocks if block) + '\n'
interactive_css = css[css_split_index:]
referral_admin_utility_marker = '.promo-admin-toolbar{'
referral_public_css_marker = '.referral-program-page{'
referral_private_css_marker = '.referral-portal-shell,.referral-admin-shell{'
referral_admin_css_marker = '.referral-admin-table{'
admin_utility_index = interactive_css.find(referral_admin_utility_marker)
referral_public_css_index = interactive_css.find(referral_public_css_marker, admin_utility_index)
referral_private_css_index = interactive_css.find(referral_private_css_marker, referral_public_css_index)
referral_admin_css_index = interactive_css.find(referral_admin_css_marker, referral_private_css_index)
if (
    admin_utility_index < 0
    or referral_public_css_index < 0
    or referral_private_css_index < 0
    or referral_admin_css_index < 0
):
    raise RuntimeError('Could not split promo/referral CSS bundle into page-group styles')
promo_referral_css = interactive_css[:admin_utility_index].strip() + '\n'
referral_admin_utility_css = interactive_css[admin_utility_index:referral_public_css_index]
referral_public_css = interactive_css[referral_public_css_index:referral_private_css_index].strip() + '\n'
referral_private_css = interactive_css[referral_private_css_index:referral_admin_css_index]
referral_admin_only_css = interactive_css[referral_admin_css_index:]
admin_panel_css = referral_admin_utility_css.strip() + '\n'
referral_portal_css = referral_private_css.strip() + '\n'
referral_admin_css = referral_admin_only_css.strip() + '\n'

promo_helper_marker = 'function promoPayloadCopy(node, selector) {'
promo_public_marker = 'async function initPromoForms() {'
promo_unsubscribe_marker = 'function initPromoUnsubscribe() {'
promo_admin_helper_marker = 'function promoAdminAttribution(entry, copy) {'
referral_section_marker = 'function referralCurrency(value) {'
helper_index = js.find(promo_helper_marker)
promo_public_index = js.find(promo_public_marker, helper_index)
promo_unsubscribe_index = js.find(promo_unsubscribe_marker, promo_public_index)
promo_admin_helper_index = js.find(promo_admin_helper_marker, promo_unsubscribe_index)
referral_index = js.find(referral_section_marker, promo_admin_helper_index)
if (
    helper_index < 0
    or promo_public_index < 0
    or promo_unsubscribe_index < 0
    or promo_admin_helper_index < 0
    or referral_index < 0
):
    raise RuntimeError('Could not split JavaScript bundles')
base_js = js[:helper_index].strip() + '\n'
shared_promo_helper_js = js[helper_index:promo_public_index]
promo_public_block = js[promo_public_index:promo_unsubscribe_index]
promo_unsubscribe_block = js[promo_unsubscribe_index:promo_admin_helper_index]
promo_admin_block = js[promo_admin_helper_index:referral_index]
referral_all_js = js[referral_index:]
referral_apply_marker = 'function initReferralApplyForms() {'
referral_portal_marker = 'function initReferralPortal() {'
referral_admin_marker = 'function initReferralAdmin() {'
site_config_marker = 'async function initSiteConfig() {'
apply_index = referral_all_js.find(referral_apply_marker)
portal_index = referral_all_js.find(referral_portal_marker, apply_index)
admin_index = referral_all_js.find(referral_admin_marker, portal_index)
site_config_index = referral_all_js.find(site_config_marker, admin_index)
if apply_index < 0 or portal_index < 0 or admin_index < 0 or site_config_index < 0:
    raise RuntimeError('Could not split referral JavaScript bundles')
referral_helper_js = referral_all_js[:apply_index]
referral_public_block = referral_all_js[apply_index:portal_index]
referral_portal_block = referral_all_js[portal_index:admin_index]
referral_admin_block = referral_all_js[admin_index:site_config_index]
site_config_js = referral_all_js[site_config_index:]

for init_call in (
    'initPromoForms();',
    'initPromoUnsubscribe();',
    'initPromoAdmin();',
    'initReferralApplyForms();',
    'initReferralPortal();',
    'initReferralAccess();',
    'initReferralAdmin();',
    'initSiteConfig();',
):
    base_js = base_js.replace(init_call + '\n', '')
    shared_promo_helper_js = shared_promo_helper_js.replace(init_call + '\n', '')
    promo_public_block = promo_public_block.replace(init_call + '\n', '')
    promo_unsubscribe_block = promo_unsubscribe_block.replace(init_call + '\n', '')
    promo_admin_block = promo_admin_block.replace(init_call + '\n', '')
    referral_helper_js = referral_helper_js.replace(init_call + '\n', '')
    referral_public_block = referral_public_block.replace(init_call + '\n', '')
    referral_portal_block = referral_portal_block.replace(init_call + '\n', '')
    referral_admin_block = referral_admin_block.replace(init_call + '\n', '')
    site_config_js = site_config_js.replace(init_call + '\n', '')

admin_detail_state_marker = (
    "    let selectedAccountId = null;\n"
    "    let selectedAccount = null;\n"
    "    let selectedCaseId = null;\n"
)
admin_detail_logic_start_marker = '    const resetCaseForm = () => {'
admin_detail_logic_end_marker = '    const loadAll = async () => {'
admin_detail_listener_start_marker = '    if (detailExportButton) {'
admin_detail_listener_end_marker = "    createForm.addEventListener('submit', async (event) => {"
admin_detail_state_index = referral_admin_block.find(admin_detail_state_marker)
admin_detail_logic_start_index = referral_admin_block.find(admin_detail_logic_start_marker)
admin_detail_logic_end_index = referral_admin_block.find(admin_detail_logic_end_marker, admin_detail_logic_start_index)
admin_detail_listener_start_index = referral_admin_block.find(admin_detail_listener_start_marker, admin_detail_logic_end_index)
admin_detail_listener_end_index = referral_admin_block.find(admin_detail_listener_end_marker, admin_detail_listener_start_index)
if (
    admin_detail_state_index < 0
    or admin_detail_logic_start_index < 0
    or admin_detail_logic_end_index < 0
    or admin_detail_listener_start_index < 0
    or admin_detail_listener_end_index < 0
):
    raise RuntimeError('Could not split referral admin detail JavaScript bundle')
admin_detail_logic_block = referral_admin_block[admin_detail_logic_start_index:admin_detail_logic_end_index]
admin_detail_listener_block = referral_admin_block[admin_detail_listener_start_index:admin_detail_listener_end_index]
for source, placeholder in (
    ('selectedAccountId', '__REFERRAL_ADMIN_SELECTED_ACCOUNT_ID__'),
    ('selectedCaseId', '__REFERRAL_ADMIN_SELECTED_CASE_ID__'),
    ('selectedAccount', '__REFERRAL_ADMIN_SELECTED_ACCOUNT__'),
):
    admin_detail_logic_block = admin_detail_logic_block.replace(source, placeholder)
    admin_detail_listener_block = admin_detail_listener_block.replace(source, placeholder)
for placeholder, target in (
    ('__REFERRAL_ADMIN_SELECTED_ACCOUNT_ID__', 'state.selectedAccountId'),
    ('__REFERRAL_ADMIN_SELECTED_CASE_ID__', 'state.selectedCaseId'),
    ('__REFERRAL_ADMIN_SELECTED_ACCOUNT__', 'state.selectedAccount'),
):
    admin_detail_logic_block = admin_detail_logic_block.replace(placeholder, target)
    admin_detail_listener_block = admin_detail_listener_block.replace(placeholder, target)
referral_admin_detail_js = (
    "window.createReferralAdminDetailTools = function createReferralAdminDetailTools(config) {\n"
    "  const {\n"
    "    copy,\n"
    "    lang,\n"
    "    labels,\n"
    "    state,\n"
    "    detailEmpty,\n"
    "    detailWrap,\n"
    "    detailName,\n"
    "    detailMeta,\n"
    "    detailProgram,\n"
    "    detailStatus,\n"
    "    detailEmail,\n"
    "    detailPhone,\n"
    "    detailCompany,\n"
    "    detailWebsite,\n"
    "    detailShareCode,\n"
    "    detailCreditCode,\n"
    "    detailBalance,\n"
    "    detailEarned,\n"
    "    detailCreated,\n"
    "    detailLogin,\n"
    "    detailNotes,\n"
    "    detailCasesBody,\n"
    "    detailRewardsBody,\n"
    "    detailAuditBody,\n"
    "    detailExportButton,\n"
    "    detailResetButton,\n"
    "    detailDeleteButton,\n"
    "    detailCaseForm,\n"
    "    detailCaseSubmit,\n"
    "    detailCaseCancel,\n"
    "    detailCaseState,\n"
    "    setStatus,\n"
    "    setError,\n"
    "    clearMessages,\n"
    "    resetAccountAccess,\n"
    "    deleteAccount,\n"
    "    createManualCase,\n"
    "    updateManualCase,\n"
    "    adjustCaseReward,\n"
    "    deleteCase,\n"
    "    downloadAccount,\n"
    "    fetchAccountDetail,\n"
    "    actionStack,\n"
    "    makeButton,\n"
    "    programLabel,\n"
    "    parseMetadata,\n"
    "    auditNote,\n"
    "    loadAll,\n"
    "  } = config;\n"
    "  const setDetailEmptyState = (message) => {\n"
    "    state.selectedAccount = null;\n"
    "    state.selectedCaseId = null;\n"
    "    if (detailEmpty) {\n"
    "      detailEmpty.textContent = message || copy.messages?.detailEmpty || '';\n"
    "      detailEmpty.hidden = false;\n"
    "    }\n"
    "    if (detailWrap) detailWrap.hidden = true;\n"
    "  };\n"
    f"{admin_detail_logic_block}"
    f"{admin_detail_listener_block}"
    "  return { beginCaseEdit, openAccountDetail, resetCaseForm, renderAccountDetail, setDetailEmptyState };\n"
    "};\n"
)
referral_admin_loader_js = (
    "    const loadAdminDetailScript = (src) => new Promise((resolve, reject) => {\n"
    "      const existing = document.querySelector(`[data-referral-admin-detail-src=\"${src}\"]`);\n"
    "      const handleLoad = () => resolve();\n"
    "      const handleError = () => reject(new Error(copy.genericError || ''));\n"
    "      if (existing) {\n"
    "        if (existing.dataset.loaded === 'true') {\n"
    "          resolve();\n"
    "          return;\n"
    "        }\n"
    "        existing.addEventListener('load', handleLoad, { once: true });\n"
    "        existing.addEventListener('error', handleError, { once: true });\n"
    "        return;\n"
    "      }\n"
    "      const script = document.createElement('script');\n"
    "      script.src = src;\n"
    "      script.defer = true;\n"
    "      script.dataset.referralAdminDetailSrc = src;\n"
    "      script.addEventListener('load', () => {\n"
    "        script.dataset.loaded = 'true';\n"
    "        resolve();\n"
    "      }, { once: true });\n"
    "      script.addEventListener('error', handleError, { once: true });\n"
    "      document.head.appendChild(script);\n"
    "    });\n"
    "    const ensureReferralAdminDetailTools = async () => {\n"
    "      if (referralAdminDetailTools) return referralAdminDetailTools;\n"
    "      if (!referralAdminDetailToolsPromise) {\n"
    "        referralAdminDetailToolsPromise = (async () => {\n"
    "          const scriptUrl = shell.dataset.referralAdminDetailScript || '';\n"
    "          if (!scriptUrl) {\n"
    "            throw new Error(copy.genericError || '');\n"
    "          }\n"
    "          if (typeof window.createReferralAdminDetailTools !== 'function') {\n"
    "            await loadAdminDetailScript(scriptUrl);\n"
    "          }\n"
    "          if (typeof window.createReferralAdminDetailTools !== 'function') {\n"
    "            throw new Error(copy.genericError || '');\n"
    "          }\n"
    "          referralAdminDetailTools = window.createReferralAdminDetailTools({\n"
    "            copy,\n"
    "            lang,\n"
    "            labels,\n"
    "            state: {\n"
    "              get selectedAccountId() { return selectedAccountId; },\n"
    "              set selectedAccountId(value) { selectedAccountId = value; },\n"
    "              get selectedAccount() { return selectedAccount; },\n"
    "              set selectedAccount(value) { selectedAccount = value; },\n"
    "              get selectedCaseId() { return selectedCaseId; },\n"
    "              set selectedCaseId(value) { selectedCaseId = value; },\n"
    "            },\n"
    "            detailEmpty,\n"
    "            detailWrap,\n"
    "            detailName,\n"
    "            detailMeta,\n"
    "            detailProgram,\n"
    "            detailStatus,\n"
    "            detailEmail,\n"
    "            detailPhone,\n"
    "            detailCompany,\n"
    "            detailWebsite,\n"
    "            detailShareCode,\n"
    "            detailCreditCode,\n"
    "            detailBalance,\n"
    "            detailEarned,\n"
    "            detailCreated,\n"
    "            detailLogin,\n"
    "            detailNotes,\n"
    "            detailCasesBody,\n"
    "            detailRewardsBody,\n"
    "            detailAuditBody,\n"
    "            detailExportButton,\n"
    "            detailResetButton,\n"
    "            detailDeleteButton,\n"
    "            detailCaseForm,\n"
    "            detailCaseSubmit,\n"
    "            detailCaseCancel,\n"
    "            detailCaseState,\n"
    "            setStatus,\n"
    "            setError,\n"
    "            clearMessages,\n"
    "            resetAccountAccess,\n"
    "            deleteAccount,\n"
    "            createManualCase,\n"
    "            updateManualCase,\n"
    "            adjustCaseReward,\n"
    "            deleteCase,\n"
    "            downloadAccount,\n"
    "            fetchAccountDetail,\n"
    "            actionStack,\n"
    "            makeButton,\n"
    "            programLabel,\n"
    "            parseMetadata,\n"
    "            auditNote,\n"
    "            loadAll: async () => loadAll(),\n"
    "          });\n"
    "          return referralAdminDetailTools;\n"
    "        })().catch((error) => {\n"
    "          referralAdminDetailToolsPromise = null;\n"
    "          throw error;\n"
    "        });\n"
    "      }\n"
    "      return referralAdminDetailToolsPromise;\n"
    "    };\n"
    "    const openAccountDetail = async (accountId) => {\n"
    "      try {\n"
    "        const tools = await ensureReferralAdminDetailTools();\n"
    "        return await tools.openAccountDetail(accountId);\n"
    "      } catch (error) {\n"
    "        setError(error.message || copy.genericError || '');\n"
    "        setStatus('');\n"
    "        return null;\n"
    "      }\n"
    "    };\n"
)
referral_admin_block = (
    referral_admin_block[:admin_detail_logic_start_index]
    + referral_admin_loader_js
    + referral_admin_block[admin_detail_logic_end_index:admin_detail_listener_start_index]
    + referral_admin_block[admin_detail_listener_end_index:]
)
referral_admin_block = referral_admin_block.replace(
    admin_detail_state_marker,
    admin_detail_state_marker
    + "    let referralAdminDetailTools = null;\n"
    + "    let referralAdminDetailToolsPromise = null;\n",
    1,
)
referral_admin_block = referral_admin_block.replace(
    "            const payload = await openAccountDetail(item.account_id);\n"
    "            const match = (payload?.referralCases || []).find((entry) => Number(entry.id) === Number(item.id));\n"
    "            if (match) beginCaseEdit(match);\n",
    "            const payload = await openAccountDetail(item.account_id);\n"
    "            const match = (payload?.referralCases || []).find((entry) => Number(entry.id) === Number(item.id));\n"
    "            if (match) {\n"
    "              const detailTools = await ensureReferralAdminDetailTools();\n"
    "              detailTools.beginCaseEdit(match);\n"
    "            }\n",
    1,
)

base_js = base_js.strip() + '\n' + site_config_js.strip() + '\ninitSiteConfig();\n'
promo_public_js = shared_promo_helper_js.strip() + '\n' + promo_public_block.strip() + '\ninitPromoForms();\n'
promo_unsubscribe_js = shared_promo_helper_js.strip() + '\n' + promo_unsubscribe_block.strip() + '\ninitPromoUnsubscribe();\n'
promo_admin_js = shared_promo_helper_js.strip() + '\n' + promo_admin_block.strip() + '\ninitPromoAdmin();\n'
referral_public_js = referral_helper_js.strip() + '\n' + referral_public_block.strip() + '\ninitReferralApplyForms();\n'
referral_portal_js = referral_helper_js.strip() + '\n' + referral_portal_block.strip() + '\ninitReferralPortal();\ninitReferralAccess();\n'
referral_admin_js = referral_helper_js.strip() + '\n' + referral_admin_block.strip() + '\ninitReferralAdmin();\n'

(DEPLOY_ASSET_ROOT / 'styles.css').write_text(base_css, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'styles-home-services.css').write_text(home_service_css, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'styles-promo-referral.css').write_text(promo_referral_css, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'styles-admin-panels.css').write_text(admin_panel_css, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'styles-articles.css').write_text(article_css, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'styles-referral-public.css').write_text(referral_public_css, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'styles-referral-portal.css').write_text(referral_portal_css, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'styles-referral-admin.css').write_text(referral_admin_css, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'site.js').write_text(base_js, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'site-promo-public.js').write_text(promo_public_js, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'site-promo-unsubscribe.js').write_text(promo_unsubscribe_js, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'site-promo-admin.js').write_text(promo_admin_js, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'site-referral-public.js').write_text(referral_public_js, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'site-referral-portal.js').write_text(referral_portal_js, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'site-referral-admin.js').write_text(referral_admin_js, encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'site-referral-admin-detail.js').write_text(referral_admin_detail_js, encoding='utf-8')

for lang in ('en', 'fr'):
    t = T[lang]
    promo_copy = PROMO_PAGE_CONTENT[lang]
    promo_admin_copy = PROMO_ADMIN_CONTENT[lang]
    custom_about_sections = ABOUT_SECTIONS_BY_LANG.get(lang)
    custom_clientele_sections = CLIENTELE_SECTIONS_BY_LANG.get(lang)
    custom_clientele_cta = CLIENTELE_CTA_BY_LANG.get(lang)
    custom_faq_cta = FAQ_CTA_BY_LANG.get(lang)
    custom_service_page_content = SERVICE_PAGE_CONTENT_BY_LANG.get(lang, {})
    contact_panel_title = t.get('contact_panel_title', t['contact_info_title'])
    contact_panel_copy = t.get('contact_panel_copy', t['contact_intro'])
    primary_cards = service_cards(lang, t['service_label'], primary_order)
    secondary_cards = service_cards(lang, t['service_label'], secondary_order)
    details = ''.join(detail_item_html(a, b) for a, b in t['contact_cards'])
    contact_page_details = contact_sidebar_details_html(lang)
    blog_guides_html = guide_cards_section(lang, GUIDE_SECTION_COPY[lang]['blog'], FR_BLOG_RESOURCE_KEYS)
    if lang == 'fr':
        privacy_cards = [
            *t['privacy_cards'],
            ('Base promo Opticable', "Les données soumises dans la promo sont conservées dans une base de données Cloudflare D1 afin d'administrer la campagne, de prévenir les abus, de journaliser les consentements et d'associer un code promo à une seule adresse courriel."),
            ('Programme de référence Opticable', "Les comptes de référence, les codes, les dossiers et les récompenses sont conservés afin d'administrer la plateforme, de valider l'admissibilité et de suivre les crédits ou paiements associés."),
            ('Accès au portail de référence', "Quand le portail de référence est utilisé, un courriel sécurisé de réinitialisation peut être émis afin de rétablir l'accès au compte."),
            ('Cloudflare Turnstile', "Turnstile est utilisé pour réduire les soumissions automatisées avant l'attribution d'un résultat promo."),
            ('Cloudflare Web Analytics', "Si l'outil est activé pour le site, Cloudflare Web Analytics peut mesurer des visites agrégées sans recourir à des pixels publicitaires."),
        ]
        privacy_choices = [
            *t['privacy_choices'],
            "Ne cochez pas le consentement marketing si vous souhaitez seulement recevoir un suivi lié à votre demande de soumission.",
            "Utilisez la page de désabonnement promo pour retirer ultérieurement votre consentement marketing sans affecter les suivis opérationnels.",
        ]
        privacy_cards_intro = "Le site reste volontairement simple. Il n'utilise pas de pixels publicitaires, mais certains services d'infrastructure, de mesure ou de formulaires peuvent traiter des données limitées quand ils sont activés ou quand vous choisissez de les utiliser."
    else:
        privacy_cards = [
            *t['privacy_cards'],
            ('Opticable promo database', 'Promo entries are stored in a Cloudflare D1 database so the campaign can be administered, abuse can be reduced, consent choices can be logged, and one promo code can be tied to one email address.'),
            ('Opticable referral program', 'Referral accounts, codes, cases, and rewards are stored so the platform can be administered, eligibility can be reviewed, and related credits or payouts can be tracked.'),
            ('Referral portal access', 'When the referral portal is used, secure password reset emails can be issued so account access can be restored without exposing the existing password.'),
            ('Cloudflare Turnstile', 'Turnstile is used to reduce automated submissions before a promo result is assigned.'),
            ('Cloudflare Web Analytics', 'If enabled for the site, Cloudflare Web Analytics may measure aggregated visits without using advertising pixels.'),
        ]
        privacy_choices = [
            *t['privacy_choices'],
            'Leave marketing consent unchecked if you only want quote-related follow-up.',
            'Use the promo unsubscribe page later to withdraw marketing consent without affecting operational quote or service follow-up.',
        ]
        privacy_cards_intro = 'The site stays intentionally simple. It does not use advertising trackers, but some infrastructure, measurement, and form services may still process limited data when they are enabled or when you choose to use them.'

    home_body = (
        band_section(
            f'<div class="hero-copy"><p class="eyebrow">{esc(t["home_kicker"])}</p>'
            f'<h1>{esc(t["home_h1"])}</h1><p>{esc(t["home_intro"])}</p>'
            f'<div class="hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a>'
            f'<a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["all_services"])}</a></div>'
            f'{render_focus_chips(lang)}'
            f'{render_home_points(lang)}</div>'
            f'{home_visual_panel(lang)}',
            'hero-band',
            'layout-shell hero hero-media-layout',
        )
        + (service_divisions_section(lang) if lang != 'fr' else '')
        + home_featured_services_section(lang)
        + industry_detail_cards_section(lang, {'eyebrow': 'Clientèle' if lang == 'fr' else 'Industries', 'title': 'Types d’immeubles servis' if lang == 'fr' else 'Building types we serve', 'intro': 'Des pages plus précises selon le type de bâtiment, les contraintes et les systèmes souvent liés.' if lang == 'fr' else 'More specific pages by building type, site constraints, and commonly connected systems.', 'label': 'Voir cette clientèle' if lang == 'fr' else 'View this industry', 'cta_href': routes[lang]['industries'], 'cta_label': 'Voir toute la clientèle' if lang == 'fr' else 'View all industries'}, INDUSTRY_DETAIL_KEYS)
        + guide_cards_section(lang, GUIDE_SECTION_COPY[lang]['home'], FR_HOME_RESOURCE_KEYS)
        + promo_cta_band(lang)
        + partner_brands_section(lang)
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(t["trust_title"])}</p><h2>{esc(t["trust_title"])}</h2><p>{esc(t.get("home_trust_intro", t["company"]))}</p></div><div class="grid-4">{"".join(card(a, b) for a, b in t["trust"])}</div>',
            'trust-section',
        )
        + process_section(lang)
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(t["industries"])}</p><h2>{esc(t["clients_title"])}</h2><p>{esc(t["clients_intro"])}</p></div>{clients_section(lang)}',
            'clients-section',
        )
        + cta(lang)
    )
    write_url(routes[lang]['home'], page(lang, 'home', 'home', t['home_title'], t['home_desc'], home_body))

    services_breadcrumbs = [(t['home'], routes[lang]['home']), (t['services'], routes[lang]['services'])]
    services_body = (
        breadcrumb_nav(services_breadcrumbs)
        + band_section(
            f'<div class="page-hero-copy"><p class="eyebrow">{esc(t["services"])}</p><h1>{esc(t["services_h1"])}</h1><p>{esc(t["services_intro"])}</p>'
            f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["about"]}">{esc(t["about"])}</a></div></div>'
            f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["tagline"])}</p><h2>{esc(t["company"])}</h2>{render_service_chip_links(lang, services_page_chip_keys, "service-chip-links-compact")}</aside>',
            'hero-band page-hero-band',
            'layout-shell page-hero',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(t["priority_title"])}</h2><p>{esc(t["priority_intro"])}</p></div><div class="grid-2">{primary_cards}</div>',
            'priority-section',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(t["support_title"])}</h2><p>{esc(t["support_intro"])}</p></div><div class="grid-2">{secondary_cards}</div>',
            'support-section',
        )
        + process_section(lang)
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(t["extra_title"])}</h2><p>{esc(t["extra_intro"])}</p></div><div class="grid-3">{"".join(card(a, b) for a, b in t["extras"])}</div>',
            'extra-section',
        )
        + cta(lang)
    )
    write_url(routes[lang]['services'], page(lang, 'services', 'services', t['services_title'], t['services_desc'], services_body, breadcrumb_items=services_breadcrumbs))

    about_breadcrumbs = [(t['home'], routes[lang]['home']), (t['about'], routes[lang]['about'])]
    if custom_about_sections:
        about_body = (
            breadcrumb_nav(about_breadcrumbs)
            + band_section(
                f'<div class="page-hero-copy"><p class="eyebrow">{esc(t["about"])}</p><h1>{esc(t["about_h1"])}</h1><p>{esc(t["about_intro"])}</p>'
                f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["services"])}</a></div></div>'
                f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["tagline"])}</p><h2>{esc(t["about_story"])}</h2>{about_panel_media(lang)}</aside>',
                'hero-band page-hero-band',
                'layout-shell page-hero',
            )
            + ''.join(render_custom_content_section(section) for section in custom_about_sections)
            + cta(lang)
        )
    else:
        about_body = (
            breadcrumb_nav(about_breadcrumbs)
            + band_section(
                f'<div class="page-hero-copy"><p class="eyebrow">{esc(t["about"])}</p><h1>{esc(t["about_h1"])}</h1><p>{esc(t["about_intro"])}</p>'
                f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["services"])}</a></div></div>'
                f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["tagline"])}</p><h2>{esc(t["about_story"])}</h2>{about_panel_media(lang)}</aside>',
                'hero-band page-hero-band',
                'layout-shell page-hero',
            )
            + band_section(
                f'<div class="section-heading"><p class="eyebrow">{esc(t["about"])}</p><h2>{esc(t.get("about_section_title", t["about_h1"]))}</h2><p>{esc(t.get("about_section_intro", t["about_story"]))}</p></div><div class="grid-4">{"".join(card(a, b) for a, b in t["about_values"])}</div>',
                'about-values-section',
            )
            + process_section(lang)
            + band_section(
                f'<div class="section-heading"><p class="eyebrow">{esc(t["industries"])}</p><h2>{esc(t["clients_title"])}</h2><p>{esc(t["clients_intro"])}</p></div>{clients_section(lang)}',
                'clients-section',
            )
            + cta(lang)
        )
    write_url(routes[lang]['about'], page(lang, 'about', 'about', t['about_title'], t['about_desc'], about_body, breadcrumb_items=about_breadcrumbs))

    contact_breadcrumbs = [(t['home'], routes[lang]['home']), (t['contact'], routes[lang]['contact'])]
    contact_body = (
        breadcrumb_nav(contact_breadcrumbs)
        + band_section(
            f'<div class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(t["contact"])}</p><h1>{esc(t["contact_h1"])}</h1><p>{esc(t["contact_intro"])}</p></div></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(
            f'<div class="contact-layout"><div class="contact-panel contact-sidebar"><h2>{esc(contact_panel_title)}</h2>{f"<p>{esc(contact_panel_copy)}</p>" if contact_panel_copy else ""}{contact_page_details}</div><div class="contact-form-column">{referral_contact_form_stack(lang)}</div></div>',
            'contact-band',
            'section-shell contact-shell',
        )
        + (''.join(render_custom_content_section(section) for section in FR_CONTACT_EXTRA_SECTIONS) if lang == 'fr' else '')
        + guide_cards_section(lang, GUIDE_SECTION_COPY[lang]['contact'], FR_CONTACT_RESOURCE_KEYS)
        + coverage_section(lang)
        + cta(lang)
    )
    write_url(routes[lang]['contact'], page(lang, 'contact', 'contact', t['contact_title'], t['contact_desc'], contact_body, breadcrumb_items=contact_breadcrumbs))

    thanks_breadcrumbs = [(t['home'], routes[lang]['home']), (t['thanks'], routes[lang]['thanks'])]
    thanks_steps_html = ''.join(f'<li>{esc(item)}</li>' for item in t['thanks_steps'])
    thanks_body = (
        breadcrumb_nav(thanks_breadcrumbs)
        + band_section(
            f'<div class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(t["thanks"])}</p><h1>{esc(t["thanks_h1"])}</h1><p>{esc(t["thanks_intro"])}</p>'
            f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["home"]}">{esc(t["thanks_return_home"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["thanks_view_services"])}</a></div></div></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(
            f'<div class="two-col"><div class="contact-panel"><p class="eyebrow">{esc(t["thanks"])}</p><h2>{esc(t["thanks_panel_title"])}</h2><p>{esc(t["thanks_panel_copy"])}</p><ul class="check-list">{thanks_steps_html}</ul></div><div class="contact-panel"><p class="eyebrow">{esc(t["contact"])}</p><h2>{esc(t["footer_contact_title"])}</h2><div class="detail-list">{details}</div></div></div>',
            'thanks-section',
        )
        + quote_lead_tracking_snippet(lang)
    )
    write_url(routes[lang]['thanks'], page(lang, 'thanks', 'contact', t['thanks_title'], t['thanks_desc'], thanks_body, breadcrumb_items=thanks_breadcrumbs, robots='noindex, nofollow'))

    privacy_cards_html = ''.join(card(title, copy) for title, copy in privacy_cards)
    privacy_choices_html = ''.join(f'<li>{esc(item)}</li>' for item in privacy_choices)
    privacy_breadcrumbs = [(t['home'], routes[lang]['home']), (t['privacy'], routes[lang]['privacy'])]
    privacy_body = (
        breadcrumb_nav(privacy_breadcrumbs)
        + band_section(
            f'<div class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(t["privacy"])}</p><h1>{esc(t["privacy_h1"])}</h1><p>{esc(t["privacy_intro"])}</p></div></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(t["privacy"])}</p><h2>{esc(t["privacy_cards_title"])}</h2><p>{esc(privacy_cards_intro)}</p></div><div class="privacy-grid">{privacy_cards_html}</div>',
            'privacy-section',
        )
        + band_section(
            f'<div class="two-col"><div class="contact-panel"><p class="eyebrow">{esc(t["privacy"])}</p><h2>{esc(t["privacy_choices_title"])}</h2><ul class="check-list">{privacy_choices_html}</ul></div><div class="contact-panel"><p class="eyebrow">{esc(t["contact"])}</p><h2>{esc(t["footer_contact_title"])}</h2><p>{esc(t["footer_contact_intro"])}</p><div class="detail-list">{details}</div></div></div>',
            'privacy-choices-section',
        )
    )
    write_url(routes[lang]['privacy'], page(lang, 'privacy', 'privacy', t['privacy_title'], t['privacy_desc'], privacy_body, breadcrumb_items=privacy_breadcrumbs))

    promo_breadcrumbs = [(t['home'], routes[lang]['home']), (promo_copy['label'], routes[lang]['promo'])]
    promo_service_cards = ''.join(card(services[key][lang]['name'], services[key][lang]['summary'], routes[lang][key], t['service_label']) for key in PROMO_SERVICE_KEYS)
    promo_article_cards = ''.join(
        card(article['headline'], article['excerpt'], article['path'], BLOG_META_UI[lang]['read_article'])
        for article in blog_articles_for_lang(lang)
        if article['key'] in PROMO_BLOG_KEYS
    )
    promo_steps = ''.join(
        f'<article class="timeline-step"><span>{index:02d}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>'
        for index, (title, text) in enumerate(promo_copy['how_steps'], 1)
    )
    promo_faq_items = promo_copy['faqs']
    promo_faq_html = ''.join(
        f'<details class="faq-item" open><summary>{esc(question)}</summary><p>{esc(answer)}</p></details>'
        for question, answer in promo_faq_items
    )
    promo_body = (
        breadcrumb_nav(promo_breadcrumbs)
        + band_section(
            f'<div class="promo-hero-grid"><div class="page-hero-copy"><p class="eyebrow">{esc(promo_copy["hero_eyebrow"])}</p><h1>{esc(promo_copy["h1"])}</h1><p>{esc(promo_copy["intro"])}</p>'
            f'<div class="page-hero-actions"><a class="button button-primary" href="#promo-entry">{esc(promo_copy["submit"])}</a><a class="button button-secondary" href="{routes[lang]["promo-rules"]}">{esc(promo_copy["actions"]["rules"])}</a></div>'
            f'{render_chips([promo_limited_time_label(lang), promo_deadline_label(lang), promo_discount_range_label(lang), promo_cap_label()])}</div>'
            f'<aside class="page-hero-panel promo-visual-panel"><p class="eyebrow">{esc(promo_copy["label"])}</p><h2>{esc(promo_copy["hero_panel_title"])}</h2><p>{esc(promo_copy["hero_panel_copy"])}</p>'
            f'<ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in promo_copy["hero_points"])}</ul></aside></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(promo_copy["label"])}</p><h2>{esc(promo_copy["how_title"])}</h2><p>{esc(promo_copy["how_intro"])}</p></div><div class="timeline">{promo_steps}</div>',
            'promo-how-section',
        )
        + band_section(
            f'<div class="two-col"><div id="promo-entry">{promo_form_shell(lang)}</div><div class="contact-panel"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(t["services_title"])}</h2><p>{esc(t["services_intro"])}</p><div class="promo-services-grid">{promo_service_cards}</div></div></div>',
            'promo-form-section',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(t["blog"])}</p><h2>{esc(BLOG_META_UI[lang]["related_articles"])}</h2><p>{esc(BLOG_META_UI[lang]["related_articles_intro"])}</p></div><div class="promo-related-grid">{promo_article_cards}</div>',
            'promo-related-section',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">FAQ</p><h2>{esc(t["faq_h1"])}</h2><p>{esc(promo_copy["faq_intro"])}</p></div><div class="faq-list">{promo_faq_html}</div>',
            'promo-faq-section',
        )
        + cta(lang)
    )
    write_url(
        routes[lang]['promo'],
        page(
            lang,
            'promo',
            'contact',
            promo_copy['title'],
            promo_copy['desc'],
            promo_body,
            faq_items=promo_faq_items,
            breadcrumb_items=promo_breadcrumbs,
            robots='index, follow, max-image-preview:large' if promo_publicly_indexable() else 'noindex, follow',
            social_image_url=PROMO_SOCIAL_URL,
            social_image_alt=promo_copy['h1'],
        ),
    )

    promo_rules_breadcrumbs = [*promo_breadcrumbs, (promo_copy['rules_h1'], routes[lang]['promo-rules'])]
    write_url(
        routes[lang]['promo-rules'],
        page(
            lang,
            'promo-rules',
            'contact',
            promo_copy['rules_title'],
            promo_copy['rules_desc'],
            breadcrumb_nav(promo_rules_breadcrumbs) + promo_rules_body(lang),
            breadcrumb_items=promo_rules_breadcrumbs,
            robots='index, follow, max-image-preview:large' if promo_publicly_indexable() else 'noindex, follow',
            social_image_url=PROMO_SOCIAL_URL,
            social_image_alt=promo_copy['rules_h1'],
        ),
    )

    promo_unsubscribe_breadcrumbs = [*promo_breadcrumbs, (promo_copy['unsubscribe_h1'], routes[lang]['promo-unsubscribe'])]
    promo_unsubscribe_body = (
        breadcrumb_nav(promo_unsubscribe_breadcrumbs)
        + band_section(
            f'<div class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(promo_copy["label"])}</p><h1>{esc(promo_copy["unsubscribe_h1"])}</h1><p>{esc(promo_copy["unsubscribe_intro"])}</p></div></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(f'<div class="two-col"><div>{promo_unsubscribe_form(lang)}</div><div class="contact-panel"><p class="eyebrow">{esc(t["contact"])}</p><h2>{esc(t["footer_contact_title"])}</h2><p>{esc(t["footer_contact_intro"])}</p><div class="detail-list">{details}</div></div></div>', 'promo-unsubscribe-section')
    )
    write_url(
        routes[lang]['promo-unsubscribe'],
        page(
            lang,
            'promo-unsubscribe',
            'contact',
            promo_copy['unsubscribe_title'],
            promo_copy['unsubscribe_desc'],
            promo_unsubscribe_body,
            breadcrumb_items=promo_unsubscribe_breadcrumbs,
            robots='noindex, follow',
            social_image_url=PROMO_SOCIAL_URL,
            social_image_alt=promo_copy['unsubscribe_h1'],
        ),
    )

    promo_admin_breadcrumbs = [*promo_breadcrumbs, (promo_admin_copy['label'], routes[lang]['promo-admin'])]
    promo_admin_body = (
        breadcrumb_nav(promo_admin_breadcrumbs)
        + band_section(
            f'<div class="promo-hero-grid"><div class="page-hero-copy"><p class="eyebrow">{esc(promo_admin_copy["eyebrow"])}</p><h1>{esc(promo_admin_copy["h1"])}</h1><p>{esc(promo_admin_copy["intro"])}</p></div>'
            f'<aside class="page-hero-panel promo-visual-panel"><p class="eyebrow">{esc(promo_admin_copy["label"])}</p><h2>{esc(promo_admin_copy["panel_title"])}</h2><p>{esc(promo_admin_copy["panel_copy"])}</p><ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in promo_admin_copy["panel_points"])}</ul></aside></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(promo_admin_shell(lang), 'promo-admin-section')
    )
    write_url(
        routes[lang]['promo-admin'],
        page(
            lang,
            'promo-admin',
            'contact',
            promo_admin_copy['title'],
            promo_admin_copy['desc'],
            promo_admin_body,
            breadcrumb_items=promo_admin_breadcrumbs,
            robots='noindex, nofollow',
            social_image_url=PROMO_SOCIAL_URL,
            social_image_alt=promo_admin_copy['h1'],
        ),
    )

    referral_program_copy_current = referral_program_copy(lang, 'client')
    referral_program_breadcrumbs = [(t['home'], routes[lang]['home']), (referral_program_copy_current['label'], routes[lang]['referral-program'])]
    write_url(
        routes[lang]['referral-program'],
        page(
            lang,
            'referral-program',
            'contact',
            referral_program_copy_current['title'],
            referral_program_copy_current['desc'],
            referral_program_page_body(lang, 'client'),
            faq_items=referral_program_copy_current['faqs'],
            breadcrumb_items=referral_program_breadcrumbs,
        ),
    )

    referral_program_terms_copy = referral_program_copy_current
    referral_program_terms_breadcrumbs = [*referral_program_breadcrumbs, (referral_program_terms_copy['terms_title'], routes[lang]['referral-program-terms'])]
    write_url(
        routes[lang]['referral-program-terms'],
        page(
            lang,
            'referral-program-terms',
            'contact',
            referral_program_terms_copy['terms_title'],
            referral_program_terms_copy.get('terms_desc', referral_program_terms_copy['desc']),
            referral_terms_body(lang, 'client'),
            breadcrumb_items=referral_program_terms_breadcrumbs,
        ),
    )

    referral_partner_copy_current = referral_program_copy(lang, 'partner')
    referral_partner_breadcrumbs = [(t['home'], routes[lang]['home']), (referral_partner_copy_current['label'], routes[lang]['referral-partner-program'])]
    write_url(
        routes[lang]['referral-partner-program'],
        page(
            lang,
            'referral-partner-program',
            'contact',
            referral_partner_copy_current['title'],
            referral_partner_copy_current['desc'],
            referral_program_page_body(lang, 'partner'),
            faq_items=referral_partner_copy_current['faqs'],
            breadcrumb_items=referral_partner_breadcrumbs,
        ),
    )

    referral_partner_terms_breadcrumbs = [*referral_partner_breadcrumbs, (referral_partner_copy_current['terms_title'], routes[lang]['referral-partner-program-terms'])]
    write_url(
        routes[lang]['referral-partner-program-terms'],
        page(
            lang,
            'referral-partner-program-terms',
            'contact',
            referral_partner_copy_current['terms_title'],
            referral_partner_copy_current.get('terms_desc', referral_partner_copy_current['desc']),
            referral_terms_body(lang, 'partner'),
            breadcrumb_items=referral_partner_terms_breadcrumbs,
        ),
    )

    portal_copy = referral_portal_copy(lang)
    portal_breadcrumbs = [(t['home'], routes[lang]['home']), (portal_copy['label'], routes[lang]['referral-portal'])]
    portal_body = (
        breadcrumb_nav(portal_breadcrumbs)
        + band_section(
            f'<div class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(portal_copy["eyebrow"])}</p><h1>{esc(portal_copy["h1"])}</h1><p>{esc(portal_copy["intro"])}</p></div></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(referral_nav_shell(lang, 'portal'), 'referral-nav-section')
        + band_section(referral_portal_shell(lang), 'referral-portal-section')
    )
    write_url(
        routes[lang]['referral-portal'],
        page(
            lang,
            'referral-portal',
            'contact',
            portal_copy['title'],
            portal_copy['desc'],
            portal_body,
            breadcrumb_items=portal_breadcrumbs,
            robots='noindex, nofollow',
        ),
    )

    access_copy = referral_access_copy(lang)
    access_breadcrumbs = [(t['home'], routes[lang]['home']), (portal_copy['label'], routes[lang]['referral-portal']), (access_copy['label'], routes[lang]['referral-access'])]
    access_body = (
        breadcrumb_nav(access_breadcrumbs)
        + band_section(
            f'<div class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(access_copy["eyebrow"])}</p><h1>{esc(access_copy["h1"])}</h1><p>{esc(access_copy["intro"])}</p></div></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(referral_access_shell(lang), 'referral-access-section')
    )
    write_url(
        routes[lang]['referral-access'],
        page(
            lang,
            'referral-access',
            'contact',
            access_copy['title'],
            access_copy['desc'],
            access_body,
            breadcrumb_items=access_breadcrumbs,
            robots='noindex, nofollow',
        ),
    )

    admin_copy = referral_admin_copy(lang)
    admin_breadcrumbs = [(t['home'], routes[lang]['home']), (admin_copy['label'], routes[lang]['referral-admin'])]
    admin_body = (
        breadcrumb_nav(admin_breadcrumbs)
        + band_section(
            f'<div class="promo-hero-grid"><div class="page-hero-copy"><p class="eyebrow">{esc(admin_copy["eyebrow"])}</p><h1>{esc(admin_copy["h1"])}</h1><p>{esc(admin_copy["intro"])}</p></div><aside class="page-hero-panel promo-visual-panel"><p class="eyebrow">{esc(admin_copy["label"])}</p><h2>{esc(admin_copy["label"])}</h2><p>{esc(admin_copy["intro"])}</p><ul class="check-list"><li>{"Approve partner applications" if lang == "en" else "Approuver les demandes partenaires"}</li><li>{"Move cases through each stage" if lang == "en" else "Faire avancer les dossiers à chaque étape"}</li><li>{"Track credits and payouts" if lang == "en" else "Suivre les crédits et les paiements"}</li></ul></aside></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(referral_admin_shell(lang), 'referral-admin-section')
    )
    write_url(
        routes[lang]['referral-admin'],
        page(
            lang,
            'referral-admin',
            'contact',
            admin_copy['title'],
            admin_copy['desc'],
            admin_body,
            breadcrumb_items=admin_breadcrumbs,
            robots='noindex, nofollow',
        ),
    )

    industries_breadcrumbs = [(t['home'], routes[lang]['home']), (t['industries'], routes[lang]['industries'])]
    case_parent = CASE_STUDIES[lang]['parent']
    case_preview = band_section(
        f'<div class="section-heading"><p class="eyebrow">{esc(t["case_studies"])}</p><h2>{esc(case_parent["h1"])}</h2><p>{esc(case_parent["intro"])}</p></div><div class="grid-2">{case_study_cards(lang)}</div>',
        'case-study-preview-section',
    )
    if custom_clientele_sections and custom_clientele_cta:
        client_sections_html = ''.join(
            render_custom_content_section({
                'eyebrow': t['industries'],
                'title': section['title'],
                'copy': section['copy'],
                'items': section['items'],
            })
            for section in custom_clientele_sections
        )
        industries_body = (
            breadcrumb_nav(industries_breadcrumbs)
            + band_section(
                f'<div class="page-hero-copy"><p class="eyebrow">{esc(t["industries"])}</p><h1>{esc(t["industries_h1"])}</h1><p>{esc(t["industries_intro"])}</p>'
                f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["services"])}</a></div></div>'
                f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["industries"])}</p><h2>{esc(t["company"])}</h2><p>{esc(t["clients_intro"])}</p></aside>',
                'hero-band page-hero-band',
                'layout-shell page-hero',
            )
            + industry_detail_cards_section(
                lang,
                {
                    'eyebrow': 'Clientèle' if lang == 'fr' else 'Who we serve',
                    'title': 'Pages par type de bâtiment ou de projet' if lang == 'fr' else 'Pages by building and project type',
                    'intro': 'Choisissez le contexte qui ressemble le plus à votre bâtiment occupé, bâtiment neuf, rénovation, chantier actif ou projet à venir.' if lang == 'fr' else 'Choose the context closest to your occupied building, new building, renovation, or active project.',
                    'label': 'Voir cette clientèle' if lang == 'fr' else 'View this type',
                    'cta_href': '',
                    'cta_label': '',
                },
                INDUSTRY_DETAIL_KEYS,
            )
            + client_sections_html
            + case_preview
            + inline_cta_band(custom_clientele_cta['title'], custom_clientele_cta['copy'], routes[lang]['contact'], custom_clientele_cta['label'])
        )
    else:
        industries_body = (
            breadcrumb_nav(industries_breadcrumbs)
            + band_section(
                f'<div class="page-hero-copy"><p class="eyebrow">{esc(t["industries"])}</p><h1>{esc(t["industries_h1"])}</h1><p>{esc(t["industries_intro"])}</p>'
                f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["services"])}</a></div></div>'
                f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["industries"])}</p><h2>{esc(t.get("industries_panel_title", t["company"]))}</h2><p>{esc(t.get("industries_panel_copy", t["industries_intro"]))}</p></aside>',
                'hero-band page-hero-band',
                'layout-shell page-hero',
            )
            + band_section(
                f'<div class="section-heading"><p class="eyebrow">{esc(t["industries"])}</p><h2>{esc(t["industries_h1"])}</h2><p>{esc(t["industries_intro"])}</p></div>{industries_section(lang)}',
                'industries-section',
            )
            + case_preview
            + coverage_section(lang)
            + cta(lang)
        )
    write_url(routes[lang]['industries'], page(lang, 'industries', 'industries', t['industries_title'], t['industries_desc'], industries_body, breadcrumb_items=industries_breadcrumbs))

    case_studies_breadcrumbs = [(t['home'], routes[lang]['home']), (t['case_studies'], routes[lang]['case-studies'])]
    case_studies_body = (
        breadcrumb_nav(case_studies_breadcrumbs)
        + band_section(
            f'<div class="page-hero-copy"><p class="eyebrow">{esc(t["case_studies"])}</p><h1>{esc(case_parent["h1"])}</h1><p>{esc(case_parent["intro"])}</p></div>'
            f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["industries"])}</p><h2>{esc(t["company"])}</h2><p>{esc(t["clients_intro"])}</p></aside>',
            'hero-band page-hero-band',
            'layout-shell page-hero',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(t["case_studies"])}</p><h2>{esc(case_parent["h1"])}</h2><p>{esc(case_parent["intro"])}</p></div><div class="grid-2">{case_study_cards(lang)}</div>',
            'case-studies-section',
        )
        + cta(lang)
    )
    write_url(routes[lang]['case-studies'], page(lang, 'case-studies', 'case-studies', case_parent['title'], case_parent['desc'], case_studies_body, breadcrumb_items=case_studies_breadcrumbs))

    for case_key in CASE_STUDY_ORDER:
        case_item = CASE_STUDIES[lang]['items'][case_key]
        case_breadcrumbs = [(t['home'], routes[lang]['home']), (t['case_studies'], routes[lang]['case-studies']), (case_item['nav'], routes[lang][case_key])]
        case_body = (
            breadcrumb_nav(case_breadcrumbs)
            + band_section(
                f'<div class="page-hero-copy"><p class="eyebrow">{esc(t["case_studies"])}</p><h1>{esc(case_item["h1"])}</h1><p>{esc(case_item["context"])}</p></div>'
                f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(case_item["systems"])}</h2><p>{esc(case_item["result"])}</p></aside>',
                'hero-band page-hero-band',
                'layout-shell page-hero',
            )
            + render_custom_content_section({'eyebrow': 'Contexte' if lang == 'fr' else 'Context', 'title': 'Contexte' if lang == 'fr' else 'Context', 'paragraphs': [case_item['context']]})
            + render_custom_content_section({'eyebrow': 'Défis identifiés' if lang == 'fr' else 'Challenges', 'title': 'Défis identifiés' if lang == 'fr' else 'Challenges identified', 'items': case_item['challenges']})
            + render_custom_content_section({'eyebrow': "Ce qu'on a fait" if lang == 'fr' else 'Scope', 'title': "Ce qu'on a fait" if lang == 'fr' else 'What we delivered', 'items': case_item['work']})
            + band_section(
                f'<div class="section-heading"><p class="eyebrow">{"Résultat" if lang == "fr" else "Outcome"}</p><h2>{"Résultat" if lang == "fr" else "Result"}</h2><p>{esc(case_item["result"])}</p></div>'
                f'<div class="contact-panel case-study-systems"><p class="eyebrow">{"Systèmes utilisés" if lang == "fr" else "Systems used"}</p><h2>{esc(case_item["systems"])}</h2>{render_chips([item.strip() for item in case_item["systems"].split("·")])}</div>',
                'case-study-result-section',
            )
            + inline_cta_band(case_item['cta_title'], case_item['cta_copy'], routes[lang]['contact'], t['quote'])
            + band_section(
                f'<div class="section-heading"><p class="eyebrow">{esc(t["case_studies"])}</p><h2>{esc("Autres études de cas" if lang == "fr" else "Related case studies")}</h2><p>{esc(case_parent["intro"])}</p></div><div class="grid-2">{case_study_cards(lang, current_key=case_key)}</div>',
                'case-study-related-section',
            )
        )
        write_url(routes[lang][case_key], page(lang, case_key, 'case-studies', case_item['title'], case_item['desc'], case_body, breadcrumb_items=case_breadcrumbs))

    faq_breadcrumbs = [(t['home'], routes[lang]['home']), ('FAQ', routes[lang]['faq'])]
    faq_body = (
        breadcrumb_nav(faq_breadcrumbs)
        + band_section(
            f'<div class="page-hero-copy"><p class="eyebrow">FAQ</p><h1>{esc(t["faq_h1"])}</h1><p>{esc(t["faq_intro"])}</p></div>'
            f'<aside class="page-hero-panel"><p class="eyebrow">FAQ</p><h2>{esc(t.get("faq_panel_title", t["faq_h1"]))}</h2><p>{esc(t.get("faq_panel_copy", t["faq_intro"]))}</p></aside>',
            'hero-band page-hero-band',
            'layout-shell page-hero',
        )
        + faq_sections(lang)
        + guide_cards_section(lang, GUIDE_SECTION_COPY[lang]['faq'], FR_FAQ_RESOURCE_KEYS)
        + (inline_cta_band(custom_faq_cta['title'], custom_faq_cta['copy'], routes[lang]['contact'], custom_faq_cta['label']) if custom_faq_cta else cta(lang))
    )
    write_url(routes[lang]['faq'], page(lang, 'faq', 'faq', t['faq_title'], t['faq_desc'], faq_body, faq_items=flat_faq_items(lang), breadcrumb_items=faq_breadcrumbs))

    blog_data = BLOG_PAGE[lang]
    blog_breadcrumbs = [(t['home'], routes[lang]['home']), (t['blog'], routes[lang]['blog'])]
    if lang in BLOG_HUB_PAGE:
        blog_hub_data = BLOG_HUB_PAGE[lang]
        shortcut_label = 'Raccourcis' if lang == 'fr' else 'Shortcuts'
        all_articles_label = 'Voir tous les articles' if lang == 'fr' else 'View all articles'
        if lang == 'fr':
            blog_multifamily_copy = {
                'eyebrow': 'Immeubles multilogements',
                'title': 'WiFi et base réseau pour immeubles multilogements',
                'intro': "Des pages plus ciblées pour comprendre ce qui change selon la taille de l'immeuble.",
                'label': 'Voir cette page',
            }
        else:
            blog_multifamily_copy = {
                'eyebrow': 'Multifamily buildings',
                'title': 'WiFi and network foundations for multifamily buildings',
                'intro': 'Targeted pages that explain what changes as the building size grows.',
                'label': 'View this page',
            }
        chooser_cards = ''.join(
            card(title, copy, href, label)
            for title, copy, href, label in blog_hub_data['chooser_cards']
        )
        latest_articles_html = render_blog_listing(lang, blog_data, blog_articles_for_lang(lang)[:3])
        blog_body = (
            breadcrumb_nav(blog_breadcrumbs)
            + band_section(
                f'<div class="page-hero-copy"><p class="eyebrow">{esc(blog_hub_data["eyebrow"])}</p><h1>{esc(blog_hub_data["h1"])}</h1><p>{esc(blog_hub_data["intro"])}</p>'
                f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["guides"]}">{esc(t["guides"])}</a><a class="button button-secondary" href="{routes[lang]["articles"]}">{esc(t["articles"])}</a></div></div>'
                f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["blog"])}</p><h2>{esc(blog_hub_data["chooser_title"])}</h2><p>{esc(blog_hub_data["chooser_intro"])}</p></aside>',
                'hero-band page-hero-band',
                'layout-shell page-hero',
            )
            + band_section(
                f'{section_heading_html(shortcut_label, blog_hub_data["chooser_title"], blog_hub_data["chooser_intro"])}<div class="grid-2">{chooser_cards}</div>',
                'content-section',
            )
            + blog_guides_html
            + multifamily_cluster_cards_section(lang, blog_multifamily_copy, MULTIFAMILY_CLUSTER_KEYS)
            + band_section(
                f'<div class="section-heading"><p class="eyebrow">{esc(t["articles"])}</p><h2>{esc(blog_hub_data["articles_title"])}</h2><p>{esc(blog_hub_data["articles_intro"])}</p></div>'
                f'{latest_articles_html}<div class="cta-actions"><a class="button button-secondary" href="{routes[lang]["articles"]}">{esc(all_articles_label)}</a></div>',
                'blog-listing-section',
            )
            + promo_cta_band(lang)
            + cta(lang)
        )
        write_url(
            routes[lang]['blog'],
            page(lang, 'blog', 'blog', blog_hub_data['title'], blog_hub_data['desc'], blog_body, breadcrumb_items=blog_breadcrumbs),
        )

        articles_data = BLOG_ARTICLES_PAGE[lang]
        articles_breadcrumbs = [(t['home'], routes[lang]['home']), (t['blog'], routes[lang]['blog']), (t['articles'], routes[lang]['articles'])]
        articles_body = (
            breadcrumb_nav(articles_breadcrumbs)
            + band_section(
                f'<div class="page-hero-copy"><p class="eyebrow">{esc(articles_data["eyebrow"])}</p><h1>{esc(articles_data["h1"])}</h1><p>{esc(articles_data["intro"])}</p></div>'
                f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["blog"])}</p><h2>{esc(blog_data["listing_title"])}</h2><p>{esc(blog_data["listing_intro"])}</p></aside>',
                'hero-band page-hero-band',
                'layout-shell page-hero',
            )
            + band_section(
                render_blog_listing(lang, blog_data),
                'blog-listing-section',
            )
            + cta(lang)
        )
        write_url(
            routes[lang]['articles'],
            page(
                lang,
                'articles',
                'articles',
                articles_data['title'],
                articles_data['desc'],
                articles_body,
                breadcrumb_items=articles_breadcrumbs,
                include_alternates=True,
                canonical_path=routes[lang]['articles'],
                alternate_paths={'en': routes['en']['articles'], 'fr': routes['fr']['articles']},
                lang_switch_href=routes['fr' if lang == 'en' else 'en']['articles'],
            ),
        )
    else:
        blog_body = (
            breadcrumb_nav(blog_breadcrumbs)
            + band_section(
                f'<div class="page-hero-copy"><p class="eyebrow">{esc(blog_data["eyebrow"])}</p><h1>{esc(blog_data["h1"])}</h1><p>{esc(blog_data["intro"])}</p></div>'
                f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["blog"])}</p><h2>{esc(blog_data["listing_title"])}</h2><p>{esc(blog_data["listing_intro"])}</p></aside>',
                'hero-band page-hero-band',
                'layout-shell page-hero',
            )
            + band_section(
                render_blog_listing(lang, blog_data),
                'blog-listing-section',
            )
        )
        blog_body += promo_cta_band(lang)
        write_url(routes[lang]['blog'], page(lang, 'blog', 'blog', blog_data['title'], blog_data['desc'], blog_body, breadcrumb_items=blog_breadcrumbs))
    for article in blog_articles_for_lang(lang):
        article_paths = blog_article_paths(article['key'])
        article_has_pair = bool(article_paths.get('en') and article_paths.get('fr'))
        article_breadcrumbs, article_body = render_blog_article_page(article, lang)
        article_meta = blog_article_seo_data(article, lang)
        write_url(
            article['path'],
            page(
                lang,
                'blog',
                'articles' if lang == 'fr' else 'blog',
                article['title'],
                article['desc'],
                article_body,
                faq_items=article.get('faq_items'),
                breadcrumb_items=article_breadcrumbs,
                canonical_path=article['path'],
                include_alternates=article_has_pair,
                resource_key='blog',
                schema_page_url=absolute_url(article['path']),
                alternate_paths=article_paths if article_has_pair else None,
                lang_switch_href=article_paths.get('fr' if lang == 'en' else 'en'),
                article_meta=article_meta,
                preload_image_url=blog_hero_image_url(article.get('hero_image')) if article.get('hero_image') else None,
            ),
        )
    if lang in GUIDE_INDEX_PAGES:
        guide_index_page = GUIDE_INDEX_PAGES[lang]
        guide_cards = render_resource_cards_for_keys(lang, RESOURCE_ARTICLE_KEYS)
        if lang == 'fr':
            guide_multifamily_copy = {
                'eyebrow': 'Immeubles multilogements',
                'title': 'WiFi et réseau pour immeubles multilogements',
                'intro': "Des pages dédiées pour comprendre la base réseau selon la taille de l'immeuble.",
                'label': 'Voir cette page',
            }
        else:
            guide_multifamily_copy = {
                'eyebrow': 'Multifamily buildings',
                'title': 'WiFi and network pages for multifamily buildings',
                'intro': 'Dedicated pages that explain the network foundation by building size.',
                'label': 'View this page',
            }
        guide_listing_title = guide_index_page.get('listing_title', 'Guides')
        guide_listing_intro = guide_index_page.get('listing_intro', '')
        guide_cta_title = guide_index_page.get('cta_title', "Vous voulez valider votre projet avec nous ?" if lang == 'fr' else 'Want to validate your project with us?')
        guide_cta_copy = guide_index_page.get('cta_copy', "Décrivez votre bâtiment, les systèmes visés et les contraintes du site. On vous dira quoi confirmer avant la soumission." if lang == 'fr' else 'Describe the building, systems, and site constraints. We will help confirm what to check before the quote.')
        guides_breadcrumbs = [(t['home'], routes[lang]['home']), ('Guides', routes[lang]['guides'])]
        guides_body = (
            breadcrumb_nav(guides_breadcrumbs)
            + band_section(
                f'<div class="page-hero-copy"><p class="eyebrow">{esc(guide_index_page["eyebrow"])}</p><h1>{esc(guide_index_page["headline"])}</h1><p>{esc(guide_index_page["intro"])}</p>'
                f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["services"])}</a></div></div>'
                f'<aside class="page-hero-panel"><p class="eyebrow">Guides</p><h2>{esc(guide_index_page["panel_title"])}</h2><p>{esc(guide_index_page["panel_copy"])}</p></aside>',
                'hero-band page-hero-band',
                'layout-shell page-hero',
            )
            + band_section(
                f'<div class="section-heading"><p class="eyebrow">Guides</p><h2>{esc(guide_listing_title)}</h2><p>{esc(guide_listing_intro)}</p></div>'
                f'{guide_cards}',
                'blog-listing-section',
            )
            + multifamily_cluster_cards_section(lang, guide_multifamily_copy, MULTIFAMILY_CLUSTER_KEYS)
            + inline_cta_band(guide_cta_title, guide_cta_copy, routes[lang]['contact'], t['quote'])
        )
        write_url(
            routes[lang]['guides'],
            page(
                lang,
                'guides',
                'guides',
                guide_index_page['title'],
                guide_index_page['desc'],
                guides_body,
                breadcrumb_items=guides_breadcrumbs,
                include_alternates=True,
                canonical_path=routes[lang]['guides'],
                alternate_paths={'en': routes['en']['guides'], 'fr': routes['fr']['guides']},
                lang_switch_href=routes['fr' if lang == 'en' else 'en']['guides'],
            ),
        )
        for article in [*guide_articles_for_lang(lang), *decision_articles_for_lang(lang)]:
            article_breadcrumbs, article_body = render_standalone_article_page(article, lang, 'Guides', routes[lang]['guides'])
            article_meta = blog_article_seo_data(article, lang)
            article_paths = resource_article_paths(article['key'])
            article_has_pair = bool(article_paths.get('en') and article_paths.get('fr'))
            write_url(
                article['path'],
                page(
                    lang,
                    'guides',
                    'guides',
                    article['title'],
                    article['desc'],
                    article_body,
                    faq_items=article.get('faq_items'),
                    breadcrumb_items=article_breadcrumbs,
                    canonical_path=article['path'],
                    include_alternates=article_has_pair,
                    resource_key='blog',
                    schema_page_url=absolute_url(article['path']),
                    alternate_paths=article_paths if article_has_pair else None,
                    lang_switch_href=article_paths.get('fr' if lang == 'en' else 'en') if article_has_pair else routes['fr' if lang == 'en' else 'en']['guides'],
                    article_meta=article_meta,
                    preload_image_url=blog_hero_image_url(article.get('hero_image')) if article.get('hero_image') else None,
                ),
            )
        for key, detail_page in industry_detail_pages_for_lang(lang).items():
            industry_breadcrumbs, industry_body = render_industry_detail_page(key, detail_page, lang)
            write_url(
                detail_page['path'],
                page(
                    lang,
                    key,
                    'industries',
                    detail_page['title'],
                    detail_page['desc'],
                    industry_body,
                    faq_items=detail_page.get('faq_items'),
                    breadcrumb_items=industry_breadcrumbs,
                    canonical_path=detail_page['path'],
                    include_alternates=True,
                    alternate_paths={
                        'en': INDUSTRY_DETAIL_PAGES_BY_LANG['en'][key]['path'],
                        'fr': INDUSTRY_DETAIL_PAGES_BY_LANG['fr'][key]['path'],
                    },
                    lang_switch_href=INDUSTRY_DETAIL_PAGES_BY_LANG['fr' if lang == 'en' else 'en'][key]['path'],
                ),
            )
        for key, cluster_page in multifamily_cluster_pages_for_lang(lang).items():
            cluster_breadcrumbs, cluster_body = render_multifamily_cluster_page(key, cluster_page, lang)
            write_url(
                cluster_page['path'],
                page(
                    lang,
                    key,
                    'industries',
                    cluster_page['title'],
                    cluster_page['desc'],
                    cluster_body,
                    faq_items=cluster_page.get('faq_items'),
                    breadcrumb_items=cluster_breadcrumbs,
                    canonical_path=cluster_page['path'],
                    include_alternates=True,
                    alternate_paths={
                        'en': MULTIFAMILY_CLUSTER_PAGES_BY_LANG['en'][key]['path'],
                        'fr': MULTIFAMILY_CLUSTER_PAGES_BY_LANG['fr'][key]['path'],
                    },
                    lang_switch_href=MULTIFAMILY_CLUSTER_PAGES_BY_LANG['fr' if lang == 'en' else 'en'][key]['path'],
                ),
            )
        for key, landing_page in CAMPAIGN_LANDING_PAGES_BY_LANG[lang].items():
            landing_body = render_campaign_landing_page(landing_page, lang)
            write_url(
                landing_page['path'],
                page(
                    lang,
                    key,
                    '',
                    landing_page['title'],
                    landing_page['desc'],
                    landing_body,
                    canonical_path=landing_page['path'],
                    include_alternates=True,
                    alternate_paths={
                        'en': CAMPAIGN_LANDING_PAGES_BY_LANG['en'][key]['path'],
                        'fr': CAMPAIGN_LANDING_PAGES_BY_LANG['fr'][key]['path'],
                    },
                    robots='noindex, nofollow',
                    lang_switch_href=CAMPAIGN_LANDING_PAGES_BY_LANG['fr' if lang == 'en' else 'en'][key]['path'],
                ),
            )

    for key in order:
        s = services[key][lang]
        related = related_services_carousel(lang, key, s['related'], t['service_label'])
        service_breadcrumbs = [(t['home'], routes[lang]['home']), (t['services'], routes[lang]['services']), (s['name'], routes[lang][key])]
        panel_extra = service_panel_media(key, lang) or render_chips([s["name"], services[s["related"][0]][lang]["name"], services[s["related"][1]][lang]["name"]])
        if key in custom_service_page_content:
            service_sections_html = ''.join(render_custom_content_section(section) for section in custom_service_page_content[key]['sections'])
            body = (
                breadcrumb_nav(service_breadcrumbs)
                + band_section(
                    f'<div class="page-hero-copy"><p class="eyebrow">{esc(s["name"])}</p><h1>{esc(s["hero"])}</h1><p>{esc(s["intro"])}</p>'
                    f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["all_services"])}</a></div></div>'
                    f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(s["summary"])}</h2>{panel_extra}</aside>',
                    'hero-band page-hero-band',
                    'layout-shell page-hero',
                )
                + service_sections_html
                + service_industry_section(lang, key)
                + service_multifamily_cluster_section(lang, key)
                + service_case_study_section(lang, key)
                + service_guide_section(lang, key)
                + inline_cta_band(custom_service_page_content[key]['cta'], t['service_area_intro'], routes[lang]['contact'], t['quote'])
                + promo_cta_band(lang)
                + related
            )
        else:
            body = (
                breadcrumb_nav(service_breadcrumbs)
                + band_section(
                    f'<div class="page-hero-copy"><p class="eyebrow">{esc(s["name"])}</p><h1>{esc(s["hero"])}</h1><p>{esc(s["intro"])}</p>'
                    f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["all_services"])}</a></div></div>'
                    f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(s["summary"])}</h2>{panel_extra}</aside>',
                    'hero-band page-hero-band',
                    'layout-shell page-hero',
                )
                + band_section(
                    f'<div class="section-heading"><p class="eyebrow">{esc("Service overview" if lang == "en" else "Vue d\'ensemble du service")}</p><h2>{esc(s["name"])}</h2><p>{esc(t["overview_intro"])}</p></div><div class="two-col"><div class="contact-panel service-detail-panel"><p class="eyebrow">{esc("Included work" if lang == "en" else "Travaux inclus")}</p><h2>{esc("What the scope can include" if lang == "en" else "Ce qu\'on peut inclure dans les travaux")}</h2><ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in s["includes"])}</ul></div><div class="contact-panel service-detail-panel"><p class="eyebrow">{esc("Benefits" if lang == "en" else "Avantages")}</p><h2>{esc("Benefits" if lang == "en" else "Ce que ce service apporte")}</h2><ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in s["benefits"])}</ul></div></div>',
                    'service-overview-section',
                )
                + band_section(
                    f'<div class="section-heading"><p class="eyebrow">{esc("Typical use cases" if lang == "en" else "Exemples concrets")}</p><h2>{esc("Typical use cases" if lang == "en" else "Cas d\'usage")}</h2><p>{esc(s["summary"])}</p></div><div class="two-col"><div class="contact-panel"><ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in s["cases"])}</ul></div><div class="contact-panel service-apply-panel"><p class="eyebrow">{esc("Industries served" if lang == "en" else "Types d\'immeubles")}</p><h2>{esc("Industries served" if lang == "en" else "Où ce service s\'applique")}</h2><ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in s["industries"])}</ul></div></div>',
                    'service-cases-section',
                )
                + service_industry_section(lang, key)
                + service_multifamily_cluster_section(lang, key)
                + service_case_study_section(lang, key)
                + service_guide_section(lang, key)
                + promo_cta_band(lang)
                + related
                + cta(lang)
            )
        write_url(routes[lang][key], page(lang, key, 'services', s['title'], s['desc'], body, service_name=s['name'], breadcrumb_items=service_breadcrumbs))

not_found_body = (
    '<section class="page-hero contact-hero"><div class="page-hero-copy">'
    '<p class="eyebrow">Erreur 404</p>'
    '<h1>Page introuvable</h1>'
    '<p>La page demandée n’existe plus, a été déplacée ou l’URL est invalide.</p>'
    f'<div class="page-hero-actions"><a class="button button-primary" href="{routes["fr"]["home"]}">Retour à l’accueil</a>'
    f'<a class="button button-secondary" href="{routes["fr"]["services"]}">Voir les services</a></div></div>'
    '<div class="contact-panel"><p class="eyebrow">Besoin d’aide</p><h2>Parlez-nous de votre projet</h2>'
    '<p>Si vous cherchiez un service précis, utilisez la page contact pour nous décrire le bâtiment, les systèmes visés ou l’échéancier.</p>'
    f'<a class="button button-secondary" href="{routes["fr"]["contact"]}">Nous joindre</a></div></section>'
)
not_found_html = page(
    'fr',
    '404',
    '',
    'Page introuvable | Opticable',
    "La page demandée est introuvable. Retournez à l’accueil, aux services ou à la page contact d’Opticable.",
    not_found_body,
    robots='noindex, follow',
    canonical_path='/404.html',
    include_alternates=False,
    resource_key='404',
    lang_switch_href=routes['en']['home'],
)

if FORCE_NOINDEX:
    robots_lines = ['User-agent: *', 'Disallow: /', '']
else:
    robots_lines = ['User-agent: *', 'Allow: /', '']
    robots_lines.append('Sitemap: ' + absolute_url('/sitemap.xml'))
(DEPLOY_ROOT / 'robots.txt').write_text('\n'.join(robots_lines) + '\n', encoding='utf-8')
(DEPLOY_ROOT / 'sitemap.xml').write_text(sitemap_xml(), encoding='utf-8')
(DEPLOY_ROOT / 'site.webmanifest').write_text(webmanifest_json(), encoding='utf-8')
(DEPLOY_ROOT / 'ads.txt').write_text('# Opticable does not authorize any third-party digital sellers.\n', encoding='utf-8')
(DEPLOY_ROOT / '404.html').write_text(not_found_html.strip() + '\n', encoding='utf-8')
