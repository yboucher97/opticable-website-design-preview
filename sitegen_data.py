"""Shared site generator data, configuration, and content definitions."""

from pathlib import Path
import json
import os
from functools import lru_cache
import re
from datetime import date, datetime, time
import shutil
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError
from guide_pages import GUIDE_ARTICLES
from resource_pages import (
    CAMPAIGN_LANDING_PAGES,
    CAMPAIGN_LANDING_PAGES_EN,
    DECISION_ARTICLES,
    GUIDE_INDEX_PAGE,
    GUIDE_INDEX_PAGE_EN,
    INDUSTRY_DETAIL_PAGES,
    INDUSTRY_DETAIL_PAGES_EN,
)

root = Path(__file__).resolve().parent
DEFAULT_SITE_URL = 'https://opticable-website-design-preview.yboucher.workers.dev'
SITE_URL = os.environ.get('OPTICABLE_SITE_URL', DEFAULT_SITE_URL).rstrip('/')
DEPLOY_DIR_NAME = os.environ.get('OPTICABLE_DEPLOY_DIR', 'dist').strip() or 'dist'
SITE_ENV = os.environ.get('OPTICABLE_SITE_ENV', 'preview').strip().lower() or 'preview'
FORCE_NOINDEX = os.environ.get('OPTICABLE_FORCE_NOINDEX', '1' if SITE_ENV != 'production' else '').strip().lower() in {'1', 'true', 'yes', 'on'}
TRACKING_ENABLED = os.environ.get('OPTICABLE_ENABLE_TRACKING', '1' if SITE_ENV == 'production' else '0').strip().lower() in {'1', 'true', 'yes', 'on'}
SOURCE_ASSET_ROOT = root / 'assets'
IMAGE_ROOT = root / 'Images'
PRODUCTION_IMAGE_ROOT = IMAGE_ROOT / 'production'
PRODUCTION_BRAND_ROOT = PRODUCTION_IMAGE_ROOT / 'brand'
PRODUCTION_HOME_ROOT = PRODUCTION_IMAGE_ROOT / 'home'
PRODUCTION_ABOUT_ROOT = PRODUCTION_IMAGE_ROOT / 'about'
PRODUCTION_SERVICE_ROOT = PRODUCTION_IMAGE_ROOT / 'services'
PRODUCTION_PROMO_ROOT = PRODUCTION_IMAGE_ROOT / 'promo'
DEPLOY_ROOT = root / DEPLOY_DIR_NAME
DEPLOY_ASSET_ROOT = DEPLOY_ROOT / 'assets'
LEGACY_ROOT_BUILD_DIRS = ('en', 'fr')
LEGACY_ROOT_BUILD_FILES = ('index.html', 'robots.txt', 'sitemap.xml', 'styles.css', 'script.js')
STATIC_ASSET_FILES = ()
ROOT_GENERATED_ASSET_FILES = (
    'logo-ui.webp',
    'home-building.webp',
    'home-rack.webp',
    'about-panel.webp',
    'service-camera.avif',
    'service-intercom.webp',
    'service-cabling.webp',
    'service-fiber.webp',
    'service-infrastructure.webp',
    'service-access.webp',
    'service-wifi.webp',
    'service-voip.webp',
    'styles.css',
    'styles-home-services.css',
    'styles-promo-referral.css',
    'styles-admin-panels.css',
    'styles-articles.css',
    'styles-referral-public.css',
    'styles-referral-portal.css',
    'styles-referral-admin.css',
    'site.js',
    'site-promo-public.js',
    'site-promo-unsubscribe.js',
    'site-promo-admin.js',
    'site-referral-public.js',
    'site-referral-portal.js',
    'site-referral-admin.js',
    'site-referral-admin-detail.js',
)
ASSET_VER = '20260414h'
LEGAL_BUSINESS_NAME = '9453-4757 Québec Inc.'
RBQ_LICENSE_LABEL = 'Licence RBQ : 5864-1648-01'
RBQ_LICENSE_NUMBER = '5864-1648-01'
LOGO_UI_URL = f'/assets/logo-ui.webp?v={ASSET_VER}'
LOGO_UI_WHITE_URL = f'/assets/logo-ui-white.webp?v={ASSET_VER}'
LOGO_UI_SCHEMA_URL = f'/assets/logo-ui-640.webp?v={ASSET_VER}'
FAVICON_32_URL = f'/assets/favicon-32.png?v={ASSET_VER}'
FAVICON_192_URL = f'/assets/favicon-192.png?v={ASSET_VER}'
FAVICON_512_URL = f'/assets/favicon-512.png?v={ASSET_VER}'
APPLE_TOUCH_ICON_URL = f'/assets/apple-touch-icon.png?v={ASSET_VER}'
STYLES_URL = f'/assets/styles.css?v={ASSET_VER}'
HOME_SERVICE_STYLES_URL = f'/assets/styles-home-services.css?v={ASSET_VER}'
PROMO_REFERRAL_STYLES_URL = f'/assets/styles-promo-referral.css?v={ASSET_VER}'
ADMIN_PANEL_STYLES_URL = f'/assets/styles-admin-panels.css?v={ASSET_VER}'
ARTICLE_STYLES_URL = f'/assets/styles-articles.css?v={ASSET_VER}'
REFERRAL_PUBLIC_STYLES_URL = f'/assets/styles-referral-public.css?v={ASSET_VER}'
REFERRAL_PORTAL_STYLES_URL = f'/assets/styles-referral-portal.css?v={ASSET_VER}'
REFERRAL_ADMIN_STYLES_URL = f'/assets/styles-referral-admin.css?v={ASSET_VER}'
SCRIPT_URL = f'/assets/site.js?v={ASSET_VER}'
PROMO_PUBLIC_SCRIPT_URL = f'/assets/site-promo-public.js?v={ASSET_VER}'
PROMO_UNSUBSCRIBE_SCRIPT_URL = f'/assets/site-promo-unsubscribe.js?v={ASSET_VER}'
PROMO_ADMIN_SCRIPT_URL = f'/assets/site-promo-admin.js?v={ASSET_VER}'
REFERRAL_PUBLIC_SCRIPT_URL = f'/assets/site-referral-public.js?v={ASSET_VER}'
REFERRAL_PORTAL_SCRIPT_URL = f'/assets/site-referral-portal.js?v={ASSET_VER}'
REFERRAL_ADMIN_SCRIPT_URL = f'/assets/site-referral-admin.js?v={ASSET_VER}'
REFERRAL_ADMIN_DETAIL_SCRIPT_URL = f'/assets/site-referral-admin-detail.js?v={ASSET_VER}'
WEBMANIFEST_URL = '/site.webmanifest'
GOOGLE_ANALYTICS_TAG_ID = 'G-ZEQXVSZWRL'
GOOGLE_ADS_TAG_ID = 'AW-18043353221'
GOOGLE_ADS_PROMO_CONVERSION_SEND_TO = f'{GOOGLE_ADS_TAG_ID}/d5WVCLvr0JgcEIXx3ptD'
GOOGLE_ADS_QUOTE_CONVERSION_SEND_TO = os.environ.get(
    'OPTICABLE_GOOGLE_ADS_QUOTE_CONVERSION_SEND_TO',
    f'{GOOGLE_ADS_TAG_ID}/-jhJCNG-xJgcEIXx3ptD',
).strip()
GOOGLE_TAG_SNIPPET = (
    (
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={GOOGLE_ANALYTICS_TAG_ID}"></script>'
        '<script>\n'
        '  window.dataLayer = window.dataLayer || [];\n'
        '  function gtag(){dataLayer.push(arguments);}\n'
        "  gtag('js', new Date());\n\n"
        '  // Google Analytics 4\n'
        f"  gtag('config', '{GOOGLE_ANALYTICS_TAG_ID}');\n\n"
        '  // Google Ads\n'
        f"  gtag('config', '{GOOGLE_ADS_TAG_ID}');\n"
        '</script>'
    )
    if TRACKING_ENABLED
    else ''
)
PROMO_CONFIG = json.loads((root / 'promo-config.json').read_text(encoding='utf-8'))
REFERRAL_CONFIG = json.loads((root / 'referral-config.json').read_text(encoding='utf-8'))
REFERRAL_CONTENT = json.loads((root / 'referral-content.json').read_text(encoding='utf-8'))
ZOHO_FORM_CONFIG = {
    'fr': {
        'src': 'https://forms.zohopublic.com/opticable/form/Formulairedemandedesoumission/formperma/i6pIlfoGOFER0OCZ4oUH_KMxVWRZKC9Of8vbyNAjR0g',
        'height': 1120,
        'aria_label': 'Demander une soumission ou une visite des lieux',
    },
    'en': {
        'src': 'https://forms.zohopublic.com/opticable/form/RequestaQuote/formperma/5kpuPyq6HG3cmmNAHG_2cFprnp16uoMzojC7Fxq42xo',
        'height': 1379,
        'aria_label': 'Request a Quote',
    },
}
COOKIE_BANNER_ACCEPT_KEY = 'opticable-cookie-banner-accepted'
HOME_BUILDING_URL = f'/assets/home-building.webp?v={ASSET_VER}'
HOME_RACK_URL = f'/assets/home-rack.webp?v={ASSET_VER}'
ABOUT_PANEL_URL = f'/assets/about-panel.webp?v={ASSET_VER}'
SERVICE_CAMERA_URL = f'/assets/service-camera.avif?v={ASSET_VER}'
SERVICE_INTERCOM_URL = f'/assets/service-intercom.webp?v={ASSET_VER}'
SERVICE_CABLING_URL = f'/assets/service-cabling.webp?v={ASSET_VER}'
SERVICE_FIBER_URL = f'/assets/service-fiber.webp?v={ASSET_VER}'
SERVICE_INFRASTRUCTURE_URL = f'/assets/service-infrastructure.webp?v={ASSET_VER}'
SERVICE_ACCESS_URL = f'/assets/service-access.webp?v={ASSET_VER}'
SERVICE_WIFI_URL = f'/assets/service-wifi.webp?v={ASSET_VER}'
SERVICE_VOIP_URL = f'/assets/service-voip.webp?v={ASSET_VER}'
OG_IMAGE_URL = f'/assets/og-image.png?v={ASSET_VER}'
PROMO_SOCIAL_URL = f'/assets/promo-social.png?v={ASSET_VER}'
OG_IMAGE_MIME_TYPE = 'image/png'
BLOG_SOCIAL_IMAGE_DIR = DEPLOY_ASSET_ROOT / 'blog-social'
LOGO_UI_WIDTH = 1200
LOGO_UI_HEIGHT = 515
FAVICON_32_SIZE = 32
APPLE_TOUCH_ICON_SIZE = 180
FAVICON_192_SIZE = 192
FAVICON_512_SIZE = 512
HOME_BUILDING_WIDTH = 1800
HOME_BUILDING_HEIGHT = 1025
HOME_RACK_WIDTH = 1800
HOME_RACK_HEIGHT = 1026
ABOUT_PANEL_WIDTH = 1200
ABOUT_PANEL_HEIGHT = 1200
SERVICE_CAMERA_WIDTH = 238
SERVICE_CAMERA_HEIGHT = 212
SERVICE_INTERCOM_WIDTH = 786
SERVICE_INTERCOM_HEIGHT = 700
SERVICE_CABLING_WIDTH = 1400
SERVICE_CABLING_HEIGHT = 740
SERVICE_FIBER_WIDTH = 275
SERVICE_FIBER_HEIGHT = 183
SERVICE_INFRASTRUCTURE_WIDTH = 1800
SERVICE_INFRASTRUCTURE_HEIGHT = 1012
SERVICE_ACCESS_WIDTH = 1400
SERVICE_ACCESS_HEIGHT = 797
SERVICE_WIFI_WIDTH = 1200
SERVICE_WIFI_HEIGHT = 1495
SERVICE_VOIP_WIDTH = 1400
SERVICE_VOIP_HEIGHT = 797
OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630
PROMO_SOCIAL_WIDTH = 1200
PROMO_SOCIAL_HEIGHT = 630
BLOG_SOCIAL_IMAGE_WIDTH = 1200
BLOG_SOCIAL_IMAGE_HEIGHT = 630
SITE_TIMEZONE = ZoneInfo('America/Toronto')
IMAGE_DIMENSIONS_BY_URL = {
    HOME_BUILDING_URL: (HOME_BUILDING_WIDTH, HOME_BUILDING_HEIGHT),
    HOME_RACK_URL: (HOME_RACK_WIDTH, HOME_RACK_HEIGHT),
    ABOUT_PANEL_URL: (ABOUT_PANEL_WIDTH, ABOUT_PANEL_HEIGHT),
    SERVICE_CAMERA_URL: (SERVICE_CAMERA_WIDTH, SERVICE_CAMERA_HEIGHT),
    SERVICE_INTERCOM_URL: (SERVICE_INTERCOM_WIDTH, SERVICE_INTERCOM_HEIGHT),
    SERVICE_CABLING_URL: (SERVICE_CABLING_WIDTH, SERVICE_CABLING_HEIGHT),
    SERVICE_FIBER_URL: (SERVICE_FIBER_WIDTH, SERVICE_FIBER_HEIGHT),
    SERVICE_INFRASTRUCTURE_URL: (SERVICE_INFRASTRUCTURE_WIDTH, SERVICE_INFRASTRUCTURE_HEIGHT),
    SERVICE_ACCESS_URL: (SERVICE_ACCESS_WIDTH, SERVICE_ACCESS_HEIGHT),
    SERVICE_WIFI_URL: (SERVICE_WIFI_WIDTH, SERVICE_WIFI_HEIGHT),
    SERVICE_VOIP_URL: (SERVICE_VOIP_WIDTH, SERVICE_VOIP_HEIGHT),
    OG_IMAGE_URL: (OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT),
    PROMO_SOCIAL_URL: (PROMO_SOCIAL_WIDTH, PROMO_SOCIAL_HEIGHT),
}
FONT_CANDIDATES = {
    'display': (
        Path(r'C:\Windows\Fonts\bahnschrift.ttf'),
        Path(r'C:\Windows\Fonts\segoeuib.ttf'),
        Path(r'C:\Windows\Fonts\arialbd.ttf'),
    ),
    'body': (
        Path(r'C:\Windows\Fonts\segoeui.ttf'),
        Path(r'C:\Windows\Fonts\arial.ttf'),
    ),
}
WEBSITE_ID = f'{SITE_URL}/#website'
BUSINESS_ID = f'{SITE_URL}/#business'
GENERAL_INQUIRY_LABELS = {'General inquiries', 'Renseignements généraux', 'Renseignements generaux'}
PROJECT_REQUEST_LABELS = {'Project requests', 'Quote requests', 'Demandes de soumission', 'Demandes de projet'}
PHONE_LABELS = {'Office phone', 'Phone', 'Téléphone du bureau', 'Telephone du bureau', 'Téléphone', 'Telephone'}
LIGHTBOX_UI = {
    'en': {
        'open': 'View larger image',
        'close': 'Close image viewer',
        'dialog': 'Image viewer',
    },
    'fr': {
        'open': "Agrandir l'image",
        'close': "Fermer l'image agrandie",
        'dialog': "Visionneuse d'image",
    },
}
CAROUSEL_UI = {
    'en': {
        'prev': 'Previous services',
        'next': 'Next services',
    },
    'fr': {
        'prev': 'Services précédents',
        'next': 'Services suivants',
    },
}
OPENING_HOURS_SPEC = [
    {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '08:00', 'closes': '17:00'},
    {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Saturday', 'Sunday'], 'opens': '10:00', 'closes': '16:00'},
]
AREA_SERVED_SCHEMA = [
    {'@type': 'AdministrativeArea', 'name': 'Quebec'},
    {'@type': 'City', 'name': 'Montreal'},
    {'@type': 'City', 'name': 'Laval'},
    {'@type': 'City', 'name': 'Longueuil'},
    {'@type': 'AdministrativeArea', 'name': 'South Shore'},
    {'@type': 'AdministrativeArea', 'name': 'North Shore'},
    {'@type': 'AdministrativeArea', 'name': 'Laurentides'},
    {'@type': 'AdministrativeArea', 'name': 'Lanaudiere'},
    {'@type': 'AdministrativeArea', 'name': 'Monteregie'},
    {'@type': 'City', 'name': 'Quebec City'},
]
SCHEMA_AREA_SERVED_NAMES = {
    'en': ['Montreal', 'Laval', 'Longueuil', 'South Shore', 'North Shore', 'Laurentians', 'Quebec'],
    'fr': ['Montréal', 'Laval', 'Longueuil', 'Rive-Sud', 'Rive-Nord', 'Laurentides', 'Québec'],
}
SCHEMA_BUSINESS_DESCRIPTION = {
    'en': 'Installation and management of camera systems, access control, WiFi, and structured cabling for commercial buildings in Quebec.',
    'fr': "Installation et gestion de systèmes de caméras, contrôle d'accès, WiFi et câblage structuré pour immeubles commerciaux au Québec.",
}
SOCIAL_LINKS = (
    {'key': 'facebook', 'label': 'Facebook', 'href': 'https://www.facebook.com/profile.php?id=61578550161916'},
    {'key': 'linkedin', 'label': 'LinkedIn', 'href': 'https://www.linkedin.com/company/opticableinc/'},
    {'key': 'instagram', 'label': 'Instagram', 'href': 'https://www.instagram.com/opticable_inc/'},
)
SOCIAL_PROFILE_URLS = [item['href'] for item in SOCIAL_LINKS]

IMAGE_RESAMPLING = getattr(Image, 'Resampling', Image)


def responsive_variant_url(name, width, ext='webp'):
    return f'/assets/{name}-{width}.{ext}?v={ASSET_VER}'


def proportional_height(width, base_width, base_height):
    return max(1, round(base_height * (width / base_width)))


def responsive_export_specs(source, name, base_width, base_height, widths, quality, image_format='WEBP'):
    ext = image_format.lower()
    specs = []
    for width in widths:
        specs.append({
            'source': source,
            'target': DEPLOY_ASSET_ROOT / f'{name}-{width}.{ext}',
            'resize': (width, proportional_height(width, base_width, base_height)),
            'format': image_format,
            'quality': quality,
        })
    return tuple(specs)


RESPONSIVE_IMAGE_EXPORTS = (
    *responsive_export_specs(PRODUCTION_BRAND_ROOT / 'logo-ui-source.png', 'logo-ui', LOGO_UI_WIDTH, LOGO_UI_HEIGHT, (240, 400, 640), 74),
    *responsive_export_specs(PRODUCTION_BRAND_ROOT / 'logo-ui-source.png', 'logo-ui', LOGO_UI_WIDTH, LOGO_UI_HEIGHT, (240, 400, 640), 52, image_format='AVIF'),
    *responsive_export_specs(PRODUCTION_BRAND_ROOT / 'logo-ui-source-white-text.png', 'logo-ui-white', LOGO_UI_WIDTH, LOGO_UI_HEIGHT, (240, 400, 640), 74),
    *responsive_export_specs(PRODUCTION_BRAND_ROOT / 'logo-ui-source-white-text.png', 'logo-ui-white', LOGO_UI_WIDTH, LOGO_UI_HEIGHT, (240, 400, 640), 52, image_format='AVIF'),
    *responsive_export_specs(PRODUCTION_HOME_ROOT / 'home-building.png', 'home-building', HOME_BUILDING_WIDTH, HOME_BUILDING_HEIGHT, (640, 960, 1400), 74),
    *responsive_export_specs(PRODUCTION_HOME_ROOT / 'home-building.png', 'home-building', HOME_BUILDING_WIDTH, HOME_BUILDING_HEIGHT, (640, 960, 1400), 56, image_format='AVIF'),
    *responsive_export_specs(PRODUCTION_HOME_ROOT / 'network-rack.png', 'home-rack', HOME_RACK_WIDTH, HOME_RACK_HEIGHT, (640, 960, 1400), 74),
    *responsive_export_specs(PRODUCTION_HOME_ROOT / 'network-rack.png', 'home-rack', HOME_RACK_WIDTH, HOME_RACK_HEIGHT, (640, 960, 1400), 56, image_format='AVIF'),
    *responsive_export_specs(PRODUCTION_ABOUT_ROOT / 'about-panel.png', 'about-panel', ABOUT_PANEL_WIDTH, ABOUT_PANEL_HEIGHT, (480, 800), 76),
    *responsive_export_specs(PRODUCTION_ABOUT_ROOT / 'about-panel.png', 'about-panel', ABOUT_PANEL_WIDTH, ABOUT_PANEL_HEIGHT, (480, 800), 56, image_format='AVIF'),
    *responsive_export_specs(PRODUCTION_SERVICE_ROOT / 'intercom.webp', 'service-intercom', SERVICE_INTERCOM_WIDTH, SERVICE_INTERCOM_HEIGHT, (480, 720), 88),
    *responsive_export_specs(PRODUCTION_SERVICE_ROOT / 'structured-cabling.png', 'service-cabling', SERVICE_CABLING_WIDTH, SERVICE_CABLING_HEIGHT, (640, 960), 78),
    *responsive_export_specs(PRODUCTION_SERVICE_ROOT / 'structured-cabling.png', 'service-cabling', SERVICE_CABLING_WIDTH, SERVICE_CABLING_HEIGHT, (640, 960), 58, image_format='AVIF'),
    *responsive_export_specs(PRODUCTION_SERVICE_ROOT / 'network-infrastructure.png', 'service-infrastructure', SERVICE_INFRASTRUCTURE_WIDTH, SERVICE_INFRASTRUCTURE_HEIGHT, (640, 960, 1400), 78),
    *responsive_export_specs(PRODUCTION_SERVICE_ROOT / 'network-infrastructure.png', 'service-infrastructure', SERVICE_INFRASTRUCTURE_WIDTH, SERVICE_INFRASTRUCTURE_HEIGHT, (640, 960, 1400), 58, image_format='AVIF'),
    *responsive_export_specs(PRODUCTION_SERVICE_ROOT / 'access-control.png', 'service-access', SERVICE_ACCESS_WIDTH, SERVICE_ACCESS_HEIGHT, (640, 960), 78),
    *responsive_export_specs(PRODUCTION_SERVICE_ROOT / 'access-control.png', 'service-access', SERVICE_ACCESS_WIDTH, SERVICE_ACCESS_HEIGHT, (640, 960), 56, image_format='AVIF'),
    *responsive_export_specs(PRODUCTION_SERVICE_ROOT / 'commercial-wifi.png', 'service-wifi', SERVICE_WIFI_WIDTH, SERVICE_WIFI_HEIGHT, (480, 768), 78),
    *responsive_export_specs(PRODUCTION_SERVICE_ROOT / 'commercial-wifi.png', 'service-wifi', SERVICE_WIFI_WIDTH, SERVICE_WIFI_HEIGHT, (480, 768), 56, image_format='AVIF'),
    *responsive_export_specs(PRODUCTION_SERVICE_ROOT / 'ip-phone.png', 'service-voip', SERVICE_VOIP_WIDTH, SERVICE_VOIP_HEIGHT, (640, 960), 88),
)

RESPONSIVE_IMAGE_SOURCES = {
    LOGO_UI_URL: [
        (responsive_variant_url('logo-ui', 240), 240),
        (responsive_variant_url('logo-ui', 400), 400),
        (responsive_variant_url('logo-ui', 640), 640),
    ],
    LOGO_UI_WHITE_URL: [
        (responsive_variant_url('logo-ui-white', 240), 240),
        (responsive_variant_url('logo-ui-white', 400), 400),
        (responsive_variant_url('logo-ui-white', 640), 640),
    ],
    HOME_BUILDING_URL: [
        (responsive_variant_url('home-building', 640), 640),
        (responsive_variant_url('home-building', 960), 960),
        (responsive_variant_url('home-building', 1400), 1400),
    ],
    HOME_RACK_URL: [
        (responsive_variant_url('home-rack', 640), 640),
        (responsive_variant_url('home-rack', 960), 960),
        (responsive_variant_url('home-rack', 1400), 1400),
    ],
    ABOUT_PANEL_URL: [
        (responsive_variant_url('about-panel', 480), 480),
        (responsive_variant_url('about-panel', 800), 800),
    ],
    SERVICE_INTERCOM_URL: [
        (responsive_variant_url('service-intercom', 480), 480),
        (responsive_variant_url('service-intercom', 720), 720),
    ],
    SERVICE_CABLING_URL: [
        (responsive_variant_url('service-cabling', 640), 640),
        (responsive_variant_url('service-cabling', 960), 960),
    ],
    SERVICE_INFRASTRUCTURE_URL: [
        (responsive_variant_url('service-infrastructure', 640), 640),
        (responsive_variant_url('service-infrastructure', 960), 960),
        (responsive_variant_url('service-infrastructure', 1400), 1400),
    ],
    SERVICE_ACCESS_URL: [
        (responsive_variant_url('service-access', 640), 640),
        (responsive_variant_url('service-access', 960), 960),
    ],
    SERVICE_WIFI_URL: [
        (responsive_variant_url('service-wifi', 480), 480),
        (responsive_variant_url('service-wifi', 768), 768),
    ],
    SERVICE_VOIP_URL: [
        (responsive_variant_url('service-voip', 640), 640),
        (responsive_variant_url('service-voip', 960), 960),
    ],
}

RESPONSIVE_IMAGE_FORMAT_SOURCES = {
    LOGO_UI_URL: {
        'image/avif': [
            (responsive_variant_url('logo-ui', 240, 'avif'), 240),
            (responsive_variant_url('logo-ui', 400, 'avif'), 400),
            (responsive_variant_url('logo-ui', 640, 'avif'), 640),
        ],
    },
    LOGO_UI_WHITE_URL: {
        'image/avif': [
            (responsive_variant_url('logo-ui-white', 240, 'avif'), 240),
            (responsive_variant_url('logo-ui-white', 400, 'avif'), 400),
            (responsive_variant_url('logo-ui-white', 640, 'avif'), 640),
        ],
    },
    HOME_BUILDING_URL: {
        'image/avif': [
            (responsive_variant_url('home-building', 640, 'avif'), 640),
            (responsive_variant_url('home-building', 960, 'avif'), 960),
            (responsive_variant_url('home-building', 1400, 'avif'), 1400),
        ],
    },
    ABOUT_PANEL_URL: {
        'image/avif': [
            (responsive_variant_url('about-panel', 480, 'avif'), 480),
            (responsive_variant_url('about-panel', 800, 'avif'), 800),
        ],
    },
    HOME_RACK_URL: {
        'image/avif': [
            (responsive_variant_url('home-rack', 640, 'avif'), 640),
            (responsive_variant_url('home-rack', 960, 'avif'), 960),
            (responsive_variant_url('home-rack', 1400, 'avif'), 1400),
        ],
    },
    SERVICE_CABLING_URL: {
        'image/avif': [
            (responsive_variant_url('service-cabling', 640, 'avif'), 640),
            (responsive_variant_url('service-cabling', 960, 'avif'), 960),
        ],
    },
    SERVICE_INFRASTRUCTURE_URL: {
        'image/avif': [
            (responsive_variant_url('service-infrastructure', 640, 'avif'), 640),
            (responsive_variant_url('service-infrastructure', 960, 'avif'), 960),
            (responsive_variant_url('service-infrastructure', 1400, 'avif'), 1400),
        ],
    },
    SERVICE_ACCESS_URL: {
        'image/avif': [
            (responsive_variant_url('service-access', 640, 'avif'), 640),
            (responsive_variant_url('service-access', 960, 'avif'), 960),
        ],
    },
    SERVICE_WIFI_URL: {
        'image/avif': [
            (responsive_variant_url('service-wifi', 480, 'avif'), 480),
            (responsive_variant_url('service-wifi', 768, 'avif'), 768),
        ],
    },
}

RESPONSIVE_IMAGE_DEFAULT_SRC = {
    LOGO_UI_URL: responsive_variant_url('logo-ui', 400),
    LOGO_UI_WHITE_URL: responsive_variant_url('logo-ui-white', 400),
    HOME_BUILDING_URL: responsive_variant_url('home-building', 1400),
    ABOUT_PANEL_URL: responsive_variant_url('about-panel', 800),
    HOME_RACK_URL: responsive_variant_url('home-rack', 1400),
    SERVICE_CABLING_URL: responsive_variant_url('service-cabling', 960),
    SERVICE_INFRASTRUCTURE_URL: responsive_variant_url('service-infrastructure', 1400),
    SERVICE_ACCESS_URL: responsive_variant_url('service-access', 960),
    SERVICE_WIFI_URL: responsive_variant_url('service-wifi', 768),
}

PROMO_PAGE_KEYS = {'promo', 'promo-rules', 'promo-unsubscribe', 'promo-admin'}
REFERRAL_PUBLIC_PAGE_KEYS = {
    'referral-program',
    'referral-program-terms',
    'referral-partner-program',
    'referral-partner-program-terms',
}
REFERRAL_PORTAL_PAGE_KEYS = {
    'referral-portal',
    'referral-access',
}
REFERRAL_ADMIN_PAGE_KEYS = {
    'referral-admin',
}
REFERRAL_PAGE_KEYS = REFERRAL_PUBLIC_PAGE_KEYS | REFERRAL_PORTAL_PAGE_KEYS | REFERRAL_ADMIN_PAGE_KEYS

HOME_IMAGE_EXPORTS = (
    {
        'source': PRODUCTION_BRAND_ROOT / 'logo-ui-source.png',
        'target': DEPLOY_ASSET_ROOT / 'logo-ui.webp',
        'resize': (LOGO_UI_WIDTH, LOGO_UI_HEIGHT),
        'format': 'WEBP',
        'quality': 76,
    },
    {
        'source': PRODUCTION_BRAND_ROOT / 'logo-ui-source-white-text.png',
        'target': DEPLOY_ASSET_ROOT / 'logo-ui-white.webp',
        'resize': (LOGO_UI_WIDTH, LOGO_UI_HEIGHT),
        'format': 'WEBP',
        'quality': 76,
    },
    {
        'source': PRODUCTION_BRAND_ROOT / 'logo-ui-source-white-text.png',
        'target': DEPLOY_ASSET_ROOT / 'og-image.png',
        'resize': (720, 320),
        'canvas': (OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT),
        'background': (13, 23, 18, 255),
        'format': 'PNG',
        'png_colors': 96,
    },
    {
        'source': SOURCE_ASSET_ROOT / 'logo-mark.png',
        'target': DEPLOY_ASSET_ROOT / 'favicon-32.png',
        'resize': (FAVICON_32_SIZE, FAVICON_32_SIZE),
        'canvas': (FAVICON_32_SIZE, FAVICON_32_SIZE),
        'format': 'PNG',
        'png_colors': 16,
    },
    {
        'source': SOURCE_ASSET_ROOT / 'logo-mark.png',
        'target': DEPLOY_ASSET_ROOT / 'apple-touch-icon.png',
        'resize': (APPLE_TOUCH_ICON_SIZE, APPLE_TOUCH_ICON_SIZE),
        'canvas': (APPLE_TOUCH_ICON_SIZE, APPLE_TOUCH_ICON_SIZE),
        'format': 'PNG',
        'png_colors': 32,
    },
    {
        'source': SOURCE_ASSET_ROOT / 'logo-mark.png',
        'target': DEPLOY_ASSET_ROOT / 'favicon-192.png',
        'resize': (FAVICON_192_SIZE, FAVICON_192_SIZE),
        'canvas': (FAVICON_192_SIZE, FAVICON_192_SIZE),
        'format': 'PNG',
        'png_colors': 48,
    },
    {
        'source': SOURCE_ASSET_ROOT / 'logo-mark.png',
        'target': DEPLOY_ASSET_ROOT / 'favicon-512.png',
        'resize': (FAVICON_512_SIZE, FAVICON_512_SIZE),
        'canvas': (FAVICON_512_SIZE, FAVICON_512_SIZE),
        'format': 'PNG',
        'png_colors': 64,
    },
    {
        'source': PRODUCTION_HOME_ROOT / 'home-building.png',
        'target': DEPLOY_ASSET_ROOT / 'home-building.webp',
        'resize': (HOME_BUILDING_WIDTH, HOME_BUILDING_HEIGHT),
        'format': 'WEBP',
        'quality': 76,
    },
    {
        'source': PRODUCTION_HOME_ROOT / 'network-rack.png',
        'target': DEPLOY_ASSET_ROOT / 'home-rack.webp',
        'resize': (HOME_RACK_WIDTH, HOME_RACK_HEIGHT),
        'format': 'WEBP',
        'quality': 76,
    },
    {
        'source': PRODUCTION_ABOUT_ROOT / 'about-panel.png',
        'target': DEPLOY_ASSET_ROOT / 'about-panel.webp',
        'resize': (ABOUT_PANEL_WIDTH, ABOUT_PANEL_HEIGHT),
        'format': 'WEBP',
        'quality': 80,
    },
    {
        'source': PRODUCTION_SERVICE_ROOT / 'intercom.webp',
        'target': DEPLOY_ASSET_ROOT / 'service-intercom.webp',
        'resize': (SERVICE_INTERCOM_WIDTH, SERVICE_INTERCOM_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
    {
        'source': PRODUCTION_SERVICE_ROOT / 'structured-cabling.png',
        'target': DEPLOY_ASSET_ROOT / 'service-cabling.webp',
        'resize': (SERVICE_CABLING_WIDTH, SERVICE_CABLING_HEIGHT),
        'format': 'WEBP',
        'quality': 80,
    },
    {
        'source': PRODUCTION_SERVICE_ROOT / 'fiber-optic.jpg',
        'target': DEPLOY_ASSET_ROOT / 'service-fiber.webp',
        'resize': (SERVICE_FIBER_WIDTH, SERVICE_FIBER_HEIGHT),
        'format': 'WEBP',
        'quality': 92,
    },
    {
        'source': PRODUCTION_SERVICE_ROOT / 'network-infrastructure.png',
        'target': DEPLOY_ASSET_ROOT / 'service-infrastructure.webp',
        'resize': (SERVICE_INFRASTRUCTURE_WIDTH, SERVICE_INFRASTRUCTURE_HEIGHT),
        'format': 'WEBP',
        'quality': 80,
    },
    {
        'source': PRODUCTION_SERVICE_ROOT / 'access-control.png',
        'target': DEPLOY_ASSET_ROOT / 'service-access.webp',
        'resize': (SERVICE_ACCESS_WIDTH, SERVICE_ACCESS_HEIGHT),
        'format': 'WEBP',
        'quality': 80,
    },
    {
        'source': PRODUCTION_SERVICE_ROOT / 'commercial-wifi.png',
        'target': DEPLOY_ASSET_ROOT / 'service-wifi.webp',
        'resize': (SERVICE_WIFI_WIDTH, SERVICE_WIFI_HEIGHT),
        'format': 'WEBP',
        'quality': 80,
    },
    {
        'source': PRODUCTION_SERVICE_ROOT / 'ip-phone.png',
        'target': DEPLOY_ASSET_ROOT / 'service-voip.webp',
        'resize': (SERVICE_VOIP_WIDTH, SERVICE_VOIP_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
    {
        'source': PRODUCTION_PROMO_ROOT / 'promo-roll-source.png',
        'target': DEPLOY_ASSET_ROOT / 'promo-social.png',
        'resize': (PROMO_SOCIAL_WIDTH, PROMO_SOCIAL_HEIGHT),
        'canvas': (PROMO_SOCIAL_WIDTH, PROMO_SOCIAL_HEIGHT),
        'format': 'PNG',
        'png_colors': 128,
    },
    *RESPONSIVE_IMAGE_EXPORTS,
)
RUNTIME_ASSET_COPIES = (
    {
        'source': PRODUCTION_SERVICE_ROOT / 'security-camera.avif',
        'target': DEPLOY_ASSET_ROOT / 'service-camera.avif',
    },
)

T = {
    'en': {
        'lang': 'en', 'locale': 'en_CA', 'switch': 'FR', 'skip': 'Skip to content', 'menu': 'Menu',
        'home': 'Home', 'services': 'Services', 'industries': 'Industries', 'about': 'About', 'faq': 'FAQ', 'contact': 'Contact',
        'tagline': 'Low-voltage infrastructure specialist', 'quote': 'Request a quote', 'all_services': 'View all services',
        'company': 'Opticable installs and manages commercial cabling, fiber, network infrastructure, security, access control, intercom, WiFi, and IP phone systems for businesses and managed properties.',
        'cta_kicker': 'Project Intake', 'cta_title': 'Need a low-voltage contractor for a commercial property, tenant fit-out, or infrastructure upgrade?', 'cta_copy': 'Use the contact page to send a bilingual quote request and explain the services, device counts, or building systems involved.',
        'footer': 'Opticable delivers organized low-voltage infrastructure for businesses, multi-tenant buildings, commercial properties, property managers, and developers.',
        'home_title': 'Low-Voltage Infrastructure Contractor for Commercial Properties | Opticable',
        'home_desc': 'Opticable provides structured cabling, fiber optic installation, network infrastructure, security camera systems, access control, intercom, commercial WiFi, and IP phone systems for commercial clients.',
        'home_kicker': 'Commercial Network and Building Systems',
        'home_h1': 'Commercial low-voltage infrastructure for business, building, and tenant communication systems.',
        'home_intro': 'Opticable designs, installs, and coordinates the physical systems behind connectivity, security, communication, and building operations. The company supports businesses, property managers, developers, and commercial operators who need clean turnover and dependable performance.',
        'home_points': ['Structured cabling, Ethernet, coaxial, and fiber optic installation', 'Server racks, internet infrastructure deployment, and network room organization', 'Security camera systems, access control systems, and intercom systems', 'Commercial WiFi networks, IP phone systems, and VoIP phone line support'],
        'home_panel': 'Built for businesses, multi-tenant buildings, commercial properties, property managers, and developers.',
        'trust_title': 'Why commercial clients use Opticable',
        'trust': [('Commercial-first scope', 'Cabling, devices, rooms, and building systems are planned as one coordinated project.'), ('Cleaner turnover', 'Labeling, pathway organization, and rack work are treated as delivery items, not last-minute cleanup.'), ('Supportable infrastructure', 'Organized installations make moves, adds, upgrades, and troubleshooting easier later.'), ('Bilingual presentation', 'English and French content supports mixed stakeholder teams and broader market visibility.')],
        'services_title': 'Commercial Low-Voltage Services | Opticable', 'services_desc': 'Opticable service pages cover structured cabling, fiber optic installation, network infrastructure, security cameras, access control, intercom, commercial WiFi, and IP phone systems.',
        'services_h1': 'Commercial infrastructure services built around reliability, organized delivery, and easier long-term support.',
        'services_intro': 'Opticable handles the low-voltage scope behind business connectivity, building communication, and tenant-facing systems. Each service page targets specific commercial search intent and explains where the work fits in a larger infrastructure plan.',
        'extra_title': 'Additional capabilities inside larger project scopes',
        'extras': [('Ethernet cable installation', 'Copper cabling for workstations, access points, cameras, phones, and business devices.'), ('Coaxial cable installation', 'Coaxial backbone and specialty runs coordinated with structured cabling and provider handoffs.'), ('Server rack installation', 'Rack layout, cable management, patching, and cleanup inside MDF and IDF environments.'), ('Internet infrastructure deployment', 'Demarc extensions, handoff routing, and switching support for new or renovated commercial spaces.'), ('VoIP phone lines', 'Voice connectivity and handset infrastructure aligned with structured cabling and network hardware.')],
        'about_title': 'About Opticable | Commercial Low-Voltage Infrastructure Specialist', 'about_desc': 'Learn how Opticable supports commercial properties, property managers, developers, and business operators with low-voltage infrastructure services.',
        'about_h1': 'A low-voltage infrastructure specialist focused on commercial properties and managed building environments.',
        'about_intro': 'Opticable is positioned as a contractor that understands how cabling, network rooms, security, access, intercom, wireless, and business communication systems connect at the building level.',
        'about_story': 'Commercial infrastructure work is rarely isolated. Tenant turnovers, security upgrades, network changes, and new development scopes often overlap. Opticable is presented as a partner that can coordinate those connected systems with cleaner technical delivery.',
        'about_values': [('Commercial positioning', 'The site speaks directly to commercial buyers, operators, landlords, and project teams.'), ('Low-voltage depth', 'Service pages explain how data, security, communication, and access systems relate to infrastructure.'), ('Practical content', 'Pages focus on scope, benefits, use cases, and industries served instead of generic marketing filler.'), ('Bilingual support', 'English and French pages support procurement, operations, and project communication needs.')],
        'contact_title': 'Contact Opticable | Request a Commercial Infrastructure Quote', 'contact_desc': 'Contact Opticable to discuss structured cabling, fiber optic installation, network infrastructure, security camera systems, access control, intercom, WiFi, or IP phone projects.',
        'contact_h1': 'Talk to Opticable about your next cabling, network, or building communication project.',
        'industries_title': 'Industries Served | Commercial Infrastructure by Opticable', 'industries_desc': 'Opticable supports businesses, multi-tenant buildings, property managers, commercial properties, contractors, and developers with low-voltage infrastructure services.',
        'industries_h1': 'Low-voltage infrastructure services for the teams that own, manage, build, and operate commercial spaces.',
        'industries_intro': 'Different client types need different outcomes: tenant turnover, project sequencing, scalable connectivity, clean room design, or better building security. Opticable is positioned around those practical requirements.',
        'faq_title': 'Commercial Infrastructure FAQ | Opticable', 'faq_desc': 'Read answers to common questions about structured cabling, fiber optic installation, security camera systems, access control, intercom, WiFi, and network infrastructure.',
        'faq_h1': 'Answers to common questions about commercial cabling and low-voltage infrastructure work.',
        'faq_intro': 'This FAQ helps buyers understand scope, occupied-site work, planning expectations, and the details that speed up quoting and project coordination.',
        'contact_info_title': 'Contact information', 'form_title': 'Request pricing or a site visit',
        'form_labels': {'name': 'Contact name', 'company': 'Company', 'email': 'Email', 'phone': 'Phone', 'property': 'Property type', 'timeline': 'Timeline', 'services': 'Needed services', 'notes': 'Project notes'},
        'form_options': {'property': ['Select one', 'Business office', 'Multi-tenant building', 'Commercial property', 'Retail or hospitality site', 'Industrial or warehouse site', 'Development or construction project'], 'timeline': ['Select one', 'Immediate need', 'Within 30 days', 'Within 1 to 3 months', 'Budgeting or planning phase']},
        'form_services': ['Structured cabling', 'Fiber optic installation', 'Network infrastructure', 'Security camera systems', 'Access control systems', 'Intercom systems', 'Commercial WiFi', 'IP phone systems'],
        'form_placeholder': 'Describe the property, project scope, devices, or network issues that need to be addressed.',
        'process': [('Site review', 'Review pathways, rooms, risers, devices, and building constraints before work begins.'), ('Scope planning', 'Confirm cable counts, equipment locations, occupied-site constraints, and system integration requirements.'), ('Installation', 'Install, terminate, label, and organize infrastructure with clean work practices and coordinated sequencing.'), ('Turnover', 'Support testing, activation, and handoff so the installed systems stay easier to maintain after commissioning.')],
        'clients': [('Businesses', 'Connectivity, security, and communication infrastructure for offices, retail, hospitality, and operational spaces.'), ('Multi-tenant buildings', 'Risers, suites, common areas, and tenant-facing systems in managed or mixed-use properties.'), ('Property managers', 'Repeatable infrastructure standards, building upgrades, and cleaner support across active assets.'), ('Developers and contractors', 'Low-voltage coordination for fit-outs, construction delivery, and project sequencing.')],
    },
    'fr': {
        'lang': 'fr', 'locale': 'fr_CA', 'switch': 'EN', 'skip': 'Aller au contenu', 'menu': 'Menu',
        'home': 'Accueil', 'services': 'Services', 'industries': 'Secteurs', 'about': 'A propos', 'faq': 'FAQ', 'contact': 'Contact',
        'tagline': 'Specialiste des infrastructures basse tension', 'quote': 'Demander une soumission', 'all_services': 'Voir tous les services',
        'company': 'Opticable installe et gere les infrastructures commerciales de cablage, fibre optique, reseau, securite, controle d acces, interphone, WiFi et telephonie IP pour les entreprises et les proprietes gerees.',
        'cta_kicker': 'Demande de projet', 'cta_title': 'Besoin d un entrepreneur basse tension pour une propriete commerciale, un amenagement locatif ou une mise a niveau d infrastructure?', 'cta_copy': 'Utilisez la page contact pour envoyer une demande de soumission bilingue et decrire les services, les quantites d appareils ou les systemes du batiment concernes.',
        'footer': 'Opticable livre des infrastructures basse tension ordonnees pour les entreprises, les immeubles multilogements, les proprietes commerciales, les gestionnaires immobiliers et les promoteurs.',
        'home_title': 'Entrepreneur en infrastructures basse tension pour immeubles commerciaux | Opticable',
        'home_desc': 'Opticable offre le cablage structure, la fibre optique, l infrastructure reseau, les cameras de securite, le controle d acces, l interphone, le WiFi commercial et la telephonie IP pour les clients commerciaux.',
        'home_kicker': 'Reseaux commerciaux et systemes de batiment',
        'home_h1': 'Infrastructures basse tension commerciales pour les systemes de communication des entreprises, des immeubles et des locataires.',
        'home_intro': 'Opticable conçoit, installe et coordonne les systemes physiques derriere la connectivite, la securite, la communication et les operations du batiment. L entreprise s adresse aux entreprises, gestionnaires immobiliers, promoteurs et operateurs commerciaux qui veulent une remise propre et une performance fiable.',
        'home_points': ['Cablage structure, Ethernet, coaxial et fibre optique', 'Baies serveurs, deploiement d infrastructures internet et organisation de salles reseau', 'Systemes de cameras de securite, controle d acces et interphones', 'WiFi commercial, telephonie IP et soutien des lignes VoIP'],
        'home_panel': 'Concu pour les entreprises, les immeubles multilogements, les proprietes commerciales, les gestionnaires immobiliers et les promoteurs.',
        'trust_title': 'Pourquoi les clients commerciaux retiennent Opticable',
        'trust': [('Portee commerciale', 'Le cablage, les appareils, les salles techniques et les systemes du batiment sont planifies comme un seul projet coordonne.'), ('Remise plus propre', 'Le reperage, l organisation des cheminements et le travail en baie sont traites comme des elements de livraison.'), ('Infrastructure facile a soutenir', 'Une installation ordonnee simplifie les ajouts, les mises a niveau et le depannage plus tard.'), ('Presentation bilingue', 'Le contenu en anglais et en francais soutient les equipes mixtes et une meilleure visibilite du site.')],
        'services_title': 'Services commerciaux basse tension | Opticable', 'services_desc': 'Les pages service d Opticable couvrent le cablage structure, la fibre optique, l infrastructure reseau, les cameras de securite, le controle d acces, l interphone, le WiFi commercial et la telephonie IP.',
        'services_h1': 'Des services d infrastructure commerciale concus pour la fiabilite, une livraison ordonnee et un soutien a long terme plus simple.',
        'services_intro': 'Opticable prend en charge la basse tension derriere la connectivite d affaires, la communication du batiment et les systemes relies aux locataires. Chaque page service vise une intention de recherche commerciale precise et explique ou le travail s insere dans un plan d infrastructure plus vaste.',
        'extra_title': 'Capacites additionnelles integrees aux projets',
'extras': [('Installation de cables Ethernet', 'Cablage cuivre pour postes de travail, points d acces WiFi, cameras, telephones et appareils d affaires.'), ('Installation de cables coaxiaux', 'Backbone coaxial et liaisons specialisees coordonnes avec le cablage structure et les handoffs fournisseur.'), ('Installation de baies serveurs', 'Implantation des baies, gestion du cablage, raccordement et remise en ordre du local reseau principal et des points de distribution.'), ('Deploiement d infrastructures internet', 'Extensions de demarcation, routage des handoffs et soutien de commutation pour les espaces commerciaux neufs ou renoves.'), ('Lignes telephoniques VoIP', 'Connectivite voix et infrastructure des postes alignees sur le cablage structure et le reseau.')],
        'about_title': 'A propos d Opticable | Specialiste des infrastructures commerciales basse tension', 'about_desc': 'Decouvrez comment Opticable accompagne les proprietes commerciales, les gestionnaires immobiliers, les promoteurs et les exploitants avec des services d infrastructure basse tension.',
        'about_h1': 'Un specialiste des infrastructures basse tension axe sur les proprietes commerciales et les environnements immobiliers geres.',
        'about_intro': 'Opticable est positionne comme un entrepreneur qui comprend comment le cablage, les salles reseau, la securite, l acces, l interphone, le sans-fil et les systemes de communication d affaires se rejoignent au niveau du batiment.',
        'about_story': 'Les travaux d infrastructure commerciale sont rarement isoles. Les rotations de locataires, les mises a niveau de securite, les changements reseau et les projets neufs se recoupent souvent. Opticable est presente comme un partenaire capable de coordonner ces systemes avec une livraison technique plus propre.',
        'about_values': [('Positionnement commercial', 'Le site parle directement aux acheteurs commerciaux, exploitants, proprietaires et equipes de projet.'), ('Profondeur basse tension', 'Les pages service expliquent comment les systemes de donnees, securite, communication et acces se rattachent a l infrastructure.'), ('Contenu pratique', 'Les pages mettent l accent sur la portee, les avantages, les cas d usage et les secteurs desservis.'), ('Soutien bilingue', 'Les pages en anglais et en francais appuient l approvisionnement, l exploitation et la coordination de projet.')],
        'contact_title': 'Contacter Opticable | Demande de soumission en infrastructure commerciale', 'contact_desc': 'Contactez Opticable pour discuter d un projet de cablage structure, fibre optique, infrastructure reseau, cameras de securite, controle d acces, interphone, WiFi ou telephonie IP.',
        'contact_h1': 'Parlez a Opticable de votre prochain projet de cablage, de reseau ou de communication du batiment.',
        'industries_title': 'Secteurs desservis | Infrastructures commerciales par Opticable', 'industries_desc': 'Opticable accompagne les entreprises, les immeubles multilogements, les gestionnaires immobiliers, les proprietes commerciales, les entrepreneurs et les promoteurs avec des services basse tension.',
        'industries_h1': 'Des services d infrastructures basse tension pour les equipes qui possedent, gerent, construisent et exploitent les espaces commerciaux.',
        'industries_intro': 'Chaque type de client recherche un resultat different : rotation de locataires, sequence de travaux, connectivite evolutive, salles techniques plus propres ou meilleure securite du batiment. Opticable est positionne autour de ces besoins concrets.',
        'faq_title': 'FAQ sur les infrastructures commerciales | Opticable', 'faq_desc': 'Consultez les reponses aux questions frequentes sur le cablage structure, la fibre optique, les cameras de securite, le controle d acces, l interphone, le WiFi et l infrastructure reseau.',
        'faq_h1': 'Reponses aux questions courantes sur le cablage commercial et les travaux d infrastructure basse tension.',
        'faq_intro': 'Cette FAQ aide les acheteurs a comprendre la portee, le travail en site occupe, la planification et les details qui accelerent l estimation et la coordination des projets.',
        'contact_info_title': 'Coordonnees de l entreprise', 'form_title': 'Demander un prix ou une visite de site',
        'form_labels': {'name': 'Nom du contact', 'company': 'Entreprise', 'email': 'Courriel', 'phone': 'Telephone', 'property': 'Type de propriete', 'timeline': 'Echeancier', 'services': 'Services requis', 'notes': 'Notes sur le projet'},
        'form_options': {'property': ['Selectionnez', 'Bureau d entreprise', 'Immeuble multilogement', 'Propriete commerciale', 'Site de commerce ou d hotellerie', 'Site industriel ou entrepot', 'Projet de developpement ou de construction'], 'timeline': ['Selectionnez', 'Besoin immediat', 'Dans les 30 jours', 'Dans 1 a 3 mois', 'Phase de budget ou de planification']},
        'form_services': ['Cablage structure', 'Installation de fibre optique', 'Infrastructure reseau', 'Systemes de cameras de securite', 'Systemes de controle d acces', 'Systemes d interphone', 'WiFi commercial', 'Systemes de telephonie IP'],
        'form_placeholder': 'Decrivez la propriete, la portee des travaux, les appareils ou les problemes reseau a corriger.',
        'process': [('Visite du site', 'Analyser les chemins, les salles, les colonnes montantes, les appareils et les contraintes du batiment avant les travaux.'), ('Planification', 'Valider les quantites de cables, l implantation des equipements, les contraintes d occupation et les besoins d integration.'), ('Installation', 'Installer, terminer, reperer et organiser l infrastructure avec des pratiques propres et une bonne coordination.'), ('Remise', 'Soutenir les essais, l activation et la remise afin que les systemes restent plus simples a entretenir apres la mise en service.')],
        'clients': [('Entreprises', 'Infrastructure de connectivite, securite et communication pour bureaux, commerces, hotellerie et espaces operationnels.'), ('Immeubles multilogements', 'Colonnes montantes, suites, aires communes et systemes relies aux locataires dans des proprietes gerees ou mixtes.'), ('Gestionnaires immobiliers', 'Standards repetables, mises a niveau et meilleur soutien sur des actifs occupes.'), ('Promoteurs et entrepreneurs', 'Coordination basse tension pour amenagements, construction et sequence de livraison.')],
    },
}

T['en'].update({
    'tagline': 'Commercial technology infrastructure specialists',
    'company': 'Opticable installs security cameras, access control, intercoms, commercial WiFi, structured cabling, fiber, and network infrastructure for commercial properties.',
    'cta_title': 'Need a technology specialist for cameras, secure entry, WiFi, or building communications?',
    'cta_copy': 'Send a quote request with the property type, required systems, and target timeline.',
    'footer': 'Opticable serves businesses and managed properties across Quebec, including Montreal, Laval, Longueuil, the South Shore, the North Shore, and the Laurentians.',
    'privacy': 'Privacy',
    'privacy_title': 'Privacy and Cookies | Opticable',
    'privacy_desc': 'How Opticable handles website, quote form, cookie, and browser-storage data.',
    'privacy_h1': 'Privacy, cookies, and third-party services.',
    'privacy_intro': 'This page explains what the website may process, when third-party tools are loaded, and how you can limit or withdraw consent.',
    'privacy_cards_title': 'How the website handles data',
    'privacy_cards_intro': 'The site stays intentionally simple. There is no analytics or advertising tracker on the site today, but some third-party services can still be involved when you choose to use them.',
    'privacy_cards': [
        ('Contact requests', 'When you email, call, or submit a quote request, we can receive the information needed to respond and follow up.'),
        ('Zoho Forms', 'The quote request form is provided by Zoho. When the contact form is displayed or submitted, Zoho can process the information you send under its own service terms, cookies, or similar technologies.'),
        ('Technical cookies', 'Hosting, CDN, security, or anti-bot services, including Cloudflare when used, can place strictly necessary technical cookies to deliver and protect the site.'),
        ('Local browser storage', 'When you accept the site cookie notice, the site stores that preference locally in your browser so the notice does not keep appearing on every page.'),
    ],
    'privacy_choices_title': 'Your choices',
    'privacy_choices': [
        'Use the phone number or email addresses on the site instead of the Zoho form.',
        'Block or clear cookies in your browser settings.',
        'Clear this site’s local browser storage to show the cookie notice again.',
        'Contact Opticable if you have questions about how a quote request is handled.',
    ],
    'footer_contact_title': 'Contact details',
    'footer_contact_intro': 'Reach Opticable directly from any page.',
    'cookie_banner_eyebrow': 'Cookies',
    'cookie_banner_title': 'Cookie notice',
    'cookie_banner_copy': 'This site may use technical cookies or similar technologies through services such as Cloudflare or Zoho when needed to deliver and protect the site.',
    'cookie_banner_accept': 'Accept',
    'thanks': 'Thank you',
    'thanks_title': 'Thank You | Quote Request Received | Opticable',
    'thanks_desc': 'Thank you for your quote request. Opticable will review the information submitted and follow up to discuss your project needs.',
    'thanks_h1': 'We received your quote request.',
    'thanks_intro': 'We received your request and will review the details provided for your camera, access control, intercom, WiFi, cabling, fiber, or network project.',
    'thanks_panel_title': 'What happens next',
    'thanks_panel_copy': 'Our team reviews the project scope, property type, and timeline before following up by email or phone.',
    'thanks_steps': [
        'Review the systems, services, and building details you submitted.',
        'Confirm scope, timing, and any site-visit requirements.',
        'Follow up with the next step for pricing, planning, or coordination.',
    ],
    'thanks_return_home': 'Back to home',
    'thanks_view_services': 'View services',
    'home_title': 'Security Cameras, Access, WiFi and Network | Opticable',
    'home_desc': 'Opticable installs cameras, access control, intercom, commercial WiFi, and network systems for Quebec commercial properties.',
    'home_h1': 'Cameras, Access, WiFi and Network for Commercial Properties',
    'home_intro': 'Opticable helps commercial properties deploy security, entry, wireless, and supporting infrastructure with clean installation and organized turnover.',
    'home_points': [
        'Security camera systems for common areas, perimeters, suites, and operations',
        'Access control and intercom systems for lobbies, entrances, and managed properties',
        'Commercial WiFi for offices, retail, and multi-tenant spaces',
        'IP phone systems, VoIP lines, and office handsets for business operations',
        'Structured cabling and fiber optic links that support those systems',
        'Network infrastructure, server racks, and telecom rooms for building connectivity',
    ],
    'home_panel': 'Security, entry, WiFi, cabling, and network infrastructure for commercial properties.',
    'trust_title': 'Why Opticable',
    'trust': [
        ('Security-focused scope', 'Cameras, entry, wireless, and cabling are planned together.'),
        ('Organized turnover', 'Labeling, pathways, and room layouts are part of delivery.'),
        ('Supportable systems', 'Organized infrastructure makes service and expansion easier.'),
    ],
    'services_title': 'Commercial Technology Services | Opticable',
    'services_desc': 'Opticable service pages cover security cameras, access control, intercom, commercial WiFi, structured cabling, fiber optic installation, network infrastructure, and IP phone systems.',
    'services_h1': 'Commercial technology services organized around security, connectivity, and cleaner long-term support.',
    'services_intro': 'Opticable focuses first on cameras, secure door access, intercoms, and business WiFi. Cabling, fiber, racks, and network rooms support those systems.',
    'extra_title': 'Supporting scope',
    'extra_intro': 'Additional infrastructure services often delivered in the same project.',
    'about_title': 'About Opticable | Commercial Technology Systems Specialist',
    'about_desc': 'Learn how Opticable supports commercial properties, property managers, developers, and businesses with security, access, WiFi, cabling, and network infrastructure services.',
    'about_h1': 'A commercial building technology specialist for managed properties and business environments.',
    'about_intro': 'Opticable works on the systems commercial properties rely on every day: security, entry, wireless, cabling, and network infrastructure.',
    'about_story': 'The company coordinates connected systems so projects stay cleaner and easier to support.',
    'about_section_title': 'How we work',
    'about_section_intro': 'The principles behind our delivery, coordination, and client experience.',
    'about_values': [
        ('Commercial focus', 'Built for businesses, managed properties, and development teams.'),
        ('Integrated systems', 'Security, access, wireless, and infrastructure are planned together.'),
        ('Practical delivery', 'The site stays focused on real scopes, benefits, and use cases.'),
    ],
    'contact_title': 'Contact Opticable | Request a Commercial Technology Quote',
    'contact_desc': 'Contact Opticable about security cameras, access control, intercom, commercial WiFi, cabling, fiber, and network projects across Quebec, including Montreal, Laval, Longueuil, the South Shore, the North Shore, and the Laurentians.',
    'contact_h1': 'Talk to Opticable about your next camera, door access, WiFi, cabling, or network project.',
    'contact_intro': 'Share your property type, target systems, and timeline to request pricing or schedule a site visit anywhere in Quebec.',
    'contact_panel_copy': 'We serve commercial properties across Quebec, including Montreal, Laval, Longueuil, the South Shore, the North Shore, the Laurentians, Lanaudiere, Monteregie, Quebec City, and surrounding areas.',
    'contact_cards': [('General inquiries', 'info@opticable.ca'), ('Project requests', 'quotes@opticable.ca'), ('Office phone', '514-316-7236'), ('Hours', 'Monday to Friday, 8:00 AM to 5:00 PM; Saturday and Sunday, 10:00 AM to 4:00 PM')],
    'form_options': {'property': ['Select one', 'Office', 'Multi-tenant building', 'Multi-unit residential building', 'Condo or strata property', 'Mixed-use building', 'Commercial property', 'Retail or hospitality site', 'Industrial or warehouse site', 'Construction site or temporary site', 'Development or construction project'], 'timeline': ['Select one', 'Immediate need', 'Within 30 days', 'Within 1 to 3 months', 'Budgeting or planning phase']},
    'industries_title': 'Industries Served | Commercial Technology Systems | Opticable',
    'industries_desc': 'Opticable supports businesses, commercial properties, and project teams across Quebec, including Montreal, Laval, Longueuil, the South Shore, the North Shore, the Laurentians, Lanaudiere, Monteregie, and Quebec City.',
    'industries_h1': 'Technology infrastructure services for the teams that own, manage, build, and operate commercial spaces.',
    'industries_intro': 'Opticable works with businesses, multi-tenant properties, property managers, and development teams that need secure, connected buildings.',
    'industries_panel_title': 'Properties, portfolios, and project teams each need a different technology approach.',
    'industries_panel_copy': 'We adapt security, wireless, cabling, and network work to occupied buildings, shared areas, tenant turnover, active operations, and project realities.',
    'service_area_eyebrow': 'Coverage area',
    'service_area_title': 'Serving clients across Quebec.',
    'service_area_intro': 'Opticable serves commercial properties, managed buildings, multi-unit sites, and project teams across Quebec, including Montreal, Laval, Longueuil, the South Shore, the North Shore, the Laurentians, Lanaudiere, Monteregie, Quebec City, and surrounding regions.',
        'service_area_regions': ['Montreal', 'Laval', 'Longueuil', 'South Shore', 'North Shore', 'Laurentians', 'Lanaudiere', 'Monteregie', 'Quebec City', 'And more'],
    'faq_title': 'FAQ | WiFi, Internet, Cameras, Access Control, Intercom, Cabling | Opticable',
    'faq_desc': 'Questions grouped by WiFi, internet, cameras, access control, intercom, cabling, and property value.',
    'faq_h1': 'Questions about WiFi, internet, cameras, access control, intercom, cabling, and property value.',
    'faq_intro': 'Questions are grouped by service so owners and operators can quickly understand what is possible, what adds value, and what can make a property more attractive or more efficient to operate.',
    'faq_panel_title': 'Questions grouped by service and property value.',
    'faq_panel_copy': 'Browse answers by WiFi, internet, cameras, access control, intercom, cabling, and value added for buildings.',
    'clients': [
        ('Businesses', 'Security, connectivity, WiFi, cameras, and communication infrastructure for offices, retail, hospitality, and operational spaces.'),
        ('Multi-tenant buildings', 'Risers, suites, common areas, secure entry systems, and tenant-facing technology in managed properties.'),
        ('Property managers', 'Repeatable building standards, security upgrades, and cleaner support across active assets.'),
        ('Developers and contractors', 'Technology coordination for fit-outs, construction delivery, security systems, and project sequencing.'),
    ],
    'focus_chips': ['Security cameras', 'Door access', 'Commercial WiFi', 'Intercom systems'],
    'priority_title': 'Core services',
    'priority_intro': 'Cameras, access control, intercom, and WiFi come first.',
    'support_title': 'Supporting infrastructure',
    'support_intro': 'Cabling, fiber, racks, and network rooms support the core systems.',
    'service_label': 'View service page',
    'process_title': 'Project process',
    'process_intro': 'A cleaner commercial technology install starts before the first cable run or device mount.',
    'gateway_intro': 'Opticable is a commercial technology infrastructure contractor serving business, property, and development teams. Continue in English or French.',
    'clients_title': 'Who we work with',
    'clients_intro': 'Commercial clients that need secure, connected buildings.',
    'overview_intro': 'Scope, benefits, and common use cases.',
    'related_intro': 'Related services often delivered in the same project.',
})

GUIDE_ARTICLE_HERO_CONFIG = {
    'security-camera-systems': (SERVICE_CAMERA_URL, '52% 50%'),
    'access-control-systems': (SERVICE_ACCESS_URL, '48% 52%'),
    'commercial-wifi-installation': (SERVICE_WIFI_URL, '38% 58%'),
    'structured-cabling': (SERVICE_CABLING_URL, 'center center'),
}


def normalize_article_collection(source_articles):
    normalized = {}
    for key, entry in source_articles.items():
        merged = {field: value for field, value in entry.items() if field not in {'en', 'fr'}}
        for localized_lang in ('en', 'fr'):
            localized = entry.get(localized_lang)
            if not localized:
                continue
            article = dict(localized)
            primary_service = article.pop('primary_service', None)
            if primary_service:
                hero_config = GUIDE_ARTICLE_HERO_CONFIG.get(primary_service)
                if hero_config:
                    hero_image, hero_position = hero_config
                    article.setdefault('hero_image', hero_image)
                    article.setdefault('hero_image_position', hero_position)
            merged[localized_lang] = article
        normalized[key] = merged
    return normalized


GUIDE_ARTICLE_DATA = normalize_article_collection(GUIDE_ARTICLES)
GUIDE_ARTICLE_KEYS = tuple(GUIDE_ARTICLE_DATA.keys())
DECISION_ARTICLE_DATA = normalize_article_collection(DECISION_ARTICLES)
DECISION_ARTICLE_KEYS = tuple(DECISION_ARTICLE_DATA.keys())
ARTICLE_PAGE_KEYS = {'blog', 'articles', *GUIDE_ARTICLE_KEYS, *DECISION_ARTICLE_KEYS}
GUIDE_INDEX_PAGES = {
    'en': GUIDE_INDEX_PAGE_EN,
    'fr': GUIDE_INDEX_PAGE,
}
INDUSTRY_DETAIL_PAGES_BY_LANG = {
    'en': INDUSTRY_DETAIL_PAGES_EN,
    'fr': INDUSTRY_DETAIL_PAGES,
}
CAMPAIGN_LANDING_PAGES_BY_LANG = {
    'en': CAMPAIGN_LANDING_PAGES_EN,
    'fr': CAMPAIGN_LANDING_PAGES,
}
RESOURCE_ARTICLE_KEYS = (
    'camera-system-pricing-commercial-building',
    'access-control-pricing-commercial-building',
    'intercom-pricing-multi-tenant-building',
    'structured-cabling-pricing-office-retail',
    'access-control-vs-intercom',
    'intercom-audio-or-video-commercial-building',
    'commercial-wifi-audit-checklist',
    'cat6a-or-fiber-commercial-building',
    'analog-cctv-to-ip-migration',
    'network-room-rack-cleanup',
    'technology-retrofit-occupied-building',
)
INDUSTRY_DETAIL_KEYS = tuple(INDUSTRY_DETAIL_PAGES.keys())
CAMPAIGN_LANDING_KEYS = tuple(CAMPAIGN_LANDING_PAGES.keys())
MULTIFAMILY_CLUSTER_PAGES = {
    'multifamily-network-infrastructure': {
        'path': '/fr/infrastructure-wifi-immeuble-multilogement/',
        'title': 'WiFi et réseau pour immeubles multilogements | Opticable',
        'desc': "Câblage, fibre, points d’accès WiFi, locaux réseau, caméras et contrôle d’accès pour immeubles multilogements au Québec.",
        'eyebrow': 'Immeubles multilogements',
        'headline': 'Infrastructure WiFi et réseau pour immeubles multilogements',
        'intro': "Un bon WiFi dans un immeuble multilogement commence rarement par le choix d'un point d'accès. Il commence par une base réseau claire: câblage, fibre, commutateurs, alimentation PoE, arrivées Internet, locaux réseau et chemins propres entre les étages.",
        'panel_title': 'La base avant le WiFi',
        'panel_copy': "Quand la base est bien pensée, le WiFi, les caméras, l'intercom, le contrôle d'accès et les autres systèmes du bâtiment restent plus stables, plus simples à faire évoluer et plus cohérents à gérer.",
        'service_keys': ('commercial-wifi-installation', 'network-infrastructure', 'structured-cabling', 'fiber-optic-installation'),
        'guide_keys': ('commercial-wifi-audit-checklist', 'cat6a-or-fiber-commercial-building', 'network-room-rack-cleanup', 'technology-retrofit-occupied-building'),
        'related_keys': ('multifamily-network-10-25', 'multifamily-network-25-100', 'multifamily-network-100-plus'),
        'sections': [
            {
                'eyebrow': 'Base réseau',
                'title': "La base avant les points d'accès WiFi",
                'paragraphs': [
                    "Dans un immeuble multilogement, la qualité du WiFi dépend d'abord de la base filaire qui l'alimente. Si le câblage, le PoE, les commutateurs, les arrivées Internet et les locaux réseau sont improvisés, ajouter des points d'accès ne règle qu'une partie du problème.",
                    "Cette base sert ensuite à relier les points d'accès WiFi, les caméras, l'intercom, le contrôle d'accès, les équipements des aires communes, les locaux administratifs et les besoins futurs du bâtiment.",
                ],
            },
            {
                'eyebrow': 'Immeuble connecté',
                'title': "Ce que l'infrastructure doit pouvoir relier",
                'cards': [
                    ("Points d'accès WiFi et antennes WiFi", "Une couverture cohérente dans les halls, corridors, aires communes, bureaux de gestion et zones techniques."),
                    ("Caméras, intercom et accès", "Des systèmes d'entrée et de sécurité qui partagent une base réseau propre au lieu d'être ajoutés au hasard."),
                    ("Suites, services et espaces communs", "Des liaisons stables pour les zones partagées, les locaux techniques et les besoins de l'exploitation."),
                    ("Croissance future", "Une structure qui permet d'ajouter des équipements, des étages ou de nouvelles zones sans tout reprendre."),
                ],
            },
            {
                'eyebrow': 'Avant la soumission',
                'title': "Ce qu'on valide avant de recommander l'architecture",
                'items': [
                    "Le nombre d'unités, d'étages et d'entrées à desservir",
                    "Le statut du bâtiment: existant, occupé, en rénovation ou en nouveau projet",
                    "L'emplacement du local réseau principal et la place disponible pour l'équipement",
                    "Le besoin de petits locaux réseau d'étage ou d'armoires techniques secondaires",
                    "Les chemins de câbles entre étages et les zones communes à couvrir",
                    "Les arrivées fournisseurs, les contraintes du site et les zones où le WiFi est déjà faible",
                ],
            },
            {
                'eyebrow': 'Langage simple',
                'title': "Local réseau principal, local d'étage et câbles entre étages: qu'est-ce que ça veut dire ?",
                'paragraphs': [
                    "Le local réseau principal est l'endroit où arrivent souvent les services, le cœur de la commutation et le rack principal du bâtiment. Dans les immeubles plus grands, on ajoute ensuite de petits locaux réseau d'étage ou des armoires techniques plus près des zones à desservir.",
                    "Les câbles entre étages relient ce local principal aux autres niveaux. C'est cette colonne vertébrale qui permet ensuite de distribuer proprement le WiFi, les caméras, l'intercom, le contrôle d'accès et les autres technologies du bâtiment.",
                ],
            },
        ],
        'faq_items': [
            ("Est-ce qu'un bon WiFi dépend surtout du point d'accès choisi ?", "Non. Le point d'accès compte, mais la qualité du WiFi dépend aussi du câblage, du PoE, des commutateurs, du positionnement, des matériaux du bâtiment et de l'organisation du réseau."),
            ("Faut-il toujours de la fibre dans un immeuble multilogement ?", "Pas toujours partout, mais elle devient souvent logique pour relier les étages, les zones éloignées ou plusieurs locaux réseau sans subir les limites du cuivre."),
            ("À quoi sert un local réseau d'étage ?", "À rapprocher la distribution réseau des zones desservies quand un seul local principal ne suffit plus. Cela réduit les longueurs de câble et simplifie l'évolution du bâtiment."),
            ("Est-ce pertinent pour un immeuble existant ?", "Oui. Cette logique s'applique autant à un bâtiment occupé qu'à un projet neuf. La différence est surtout dans la façon de phaser les travaux."),
        ],
        'cta_title': "Planifier l'infrastructure de votre immeuble multilogement",
        'cta_copy': "Décrivez le nombre d'unités, les étages, les aires communes et les systèmes à relier. On vous aidera à cadrer une base réseau cohérente avant le reste.",
        'cta_label': 'Obtenir une soumission',
    },
    'multifamily-network-10-25': {
        'path': '/fr/infrastructure-wifi-10-25-unites/',
        'title': 'WiFi et réseau pour immeubles de 10 à 25 unités | Opticable',
        'desc': "Infrastructure WiFi, câblage, fibre et locaux réseau pour immeubles de 10 à 25 unités au Québec.",
        'eyebrow': 'Immeubles de 10 à 25 unités',
        'headline': 'WiFi et réseau pour immeubles de 10 à 25 unités',
        'intro': "Dans un immeuble de 10 à 25 unités, l'objectif n'est pas de surconstruire. Il faut surtout une base simple, propre et claire pour relier l'entrée, les aires communes, le WiFi, les caméras et les autres systèmes sans créer un casse-tête pour la suite.",
        'panel_title': 'Ce qui compte le plus',
        'panel_copy': "Un local réseau principal lisible, de bons chemins de câbles, des points d'accès WiFi bien placés et une portée réaliste pour les zones communes.",
        'service_keys': ('commercial-wifi-installation', 'structured-cabling', 'network-infrastructure', 'intercom-systems'),
        'guide_keys': ('intercom-pricing-multi-tenant-building', 'commercial-wifi-audit-checklist', 'cat6a-or-fiber-commercial-building'),
        'related_keys': ('multifamily-network-infrastructure', 'multifamily-network-25-100', 'multifamily-network-100-plus'),
        'sections': [
            {
                'eyebrow': 'Profil type',
                'title': "Ce qu'on voit souvent à cette taille",
                'paragraphs': [
                    "Un seul local réseau principal peut suffire, parfois avec une petite armoire secondaire si certaines zones sont trop loin. L'erreur fréquente est de laisser chaque ajout se brancher sur l'existant sans logique globale.",
                    "Même à petite ou moyenne échelle, le bâtiment doit pouvoir supporter proprement l'intercom, le contrôle d'accès, les caméras, le WiFi des aires communes et les besoins futurs.",
                ],
            },
            {
                'eyebrow': 'Portées fréquentes',
                'title': "Ce qu'on installe le plus souvent",
                'items': [
                    "Intercom ou intercom vidéo à l'entrée principale",
                    "Contrôle d'accès pour l'entrée, le garage ou les locaux communs",
                    "Caméras dans le hall, les corridors, le stationnement et les points sensibles",
                    "Points d'accès WiFi dans les aires communes, corridors ou salle partagée",
                    "Remise en ordre du local réseau et ajout de quelques liens structurés",
                ],
            },
            {
                'eyebrow': 'Avant de chiffrer',
                'title': "Ce qu'il faut confirmer avant une soumission utile",
                'items': [
                    "Le nombre d'étages et la distance réelle entre les zones à relier",
                    "L'emplacement du local réseau principal et la place disponible dans le rack",
                    "Les zones communes où le WiFi doit être fiable dès le départ",
                    "Les accès à sécuriser, les visiteurs à gérer et les besoins des résidents",
                    "Le statut du bâtiment: existant, occupé, en rénovation ou neuf",
                ],
            },
            {
                'eyebrow': 'Qualité du WiFi',
                'title': "À cette échelle, un bon WiFi reste d'abord une question de base réseau",
                'paragraphs': [
                    "Un petit immeuble n'a pas besoin d'une architecture lourde, mais il a besoin d'un réseau propre. Des points d'accès mal placés ou mal alimentés donnent vite un WiFi inégal, même quand le matériel est correct.",
                    "Une base bien organisée rend aussi beaucoup plus simple l'ajout futur de caméras, d'accès, d'une nouvelle zone commune ou d'un autre étage de service.",
                ],
            },
        ],
        'faq_items': [
            ("Est-ce qu'un seul local réseau suffit toujours ?", "Pas toujours. Cela dépend surtout du nombre d'étages, des distances et des zones à desservir. Parfois une petite armoire secondaire évite beaucoup de compromis."),
            ("Faut-il prévoir la fibre à cette taille ?", "Pas dans tous les cas, mais elle peut devenir logique si les longueurs montent vite ou si certaines zones sont éloignées."),
            ("Le WiFi commun peut-il être ajouté plus tard ?", "Oui, mais il vaut mieux prévoir dès maintenant le câblage, le PoE et les emplacements des points d'accès pour éviter des reprises plus coûteuses."),
        ],
        'cta_title': "Vous planifiez un immeuble de 10 à 25 unités ?",
        'cta_copy': "Parlez-nous du nombre d'étages, des zones communes et des systèmes à relier. On vous aidera à garder l'infrastructure simple et durable.",
        'cta_label': 'Demander une soumission',
    },
    'multifamily-network-25-100': {
        'path': '/fr/infrastructure-wifi-25-100-unites/',
        'title': 'Réseau pour immeubles de 25 à 100 unités | Opticable',
        'desc': "Infrastructure réseau, WiFi, fibre et locaux techniques pour immeubles de 25 à 100 unités au Québec.",
        'eyebrow': 'Immeubles de 25 à 100 unités',
        'headline': 'Infrastructure réseau pour immeubles de 25 à 100 unités',
        'intro': "Entre 25 et 100 unités, l'infrastructure doit déjà gérer plus de densité, plus d'étages, plus de zones communes et plus de systèmes. Le WiFi devient seulement une couche parmi d'autres sur une base réseau qui doit être claire et évolutive.",
        'panel_title': 'Ce qui change à cette taille',
        'panel_copy': "On voit plus souvent un local réseau principal, des armoires ou locaux d'étage, des liens entre niveaux et une vraie logique de distribution entre les zones du bâtiment.",
        'service_keys': ('commercial-wifi-installation', 'network-infrastructure', 'structured-cabling', 'fiber-optic-installation'),
        'guide_keys': ('commercial-wifi-audit-checklist', 'cat6a-or-fiber-commercial-building', 'technology-retrofit-occupied-building'),
        'related_keys': ('multifamily-network-infrastructure', 'multifamily-network-10-25', 'multifamily-network-100-plus'),
        'sections': [
            {
                'eyebrow': 'Structure',
                'title': "Ce qui devient important quand l'immeuble prend de l'ampleur",
                'paragraphs': [
                    "Un seul local réseau central devient souvent insuffisant pour tout desservir proprement. À cette taille, on planifie plus souvent un local principal et un ou plusieurs points de redistribution plus près des étages ou des zones communes.",
                    "Cette structure sert à maintenir des longueurs de câble réalistes, à mieux distribuer le PoE et à garder une logique claire quand on ajoute du WiFi, des caméras, de l'intercom ou du contrôle d'accès.",
                ],
            },
            {
                'eyebrow': 'Portées fréquentes',
                'title': "Ce qu'on prépare souvent dans ce type d'immeuble",
                'cards': [
                    ("WiFi des aires communes", "Plusieurs points d'accès WiFi coordonnés selon les étages, les corridors, les halls, les salles partagées et la densité réelle."),
                    ("Liens entre étages", "Câblage cuivre ou fibre pour relier le local principal aux étages et éviter de tirer chaque service au hasard."),
                    ("Sécurité intégrée", "Caméras, intercom et contrôle d'accès qui utilisent une base réseau cohérente au lieu d'îlots séparés."),
                    ("Évolutivité", "Une structure qui laisse de la marge pour plus d'unités, plus d'équipements ou de nouvelles zones."),
                ],
            },
            {
                'eyebrow': 'Avant la soumission',
                'title': "Les points à confirmer avant de choisir l'architecture",
                'items': [
                    "Le nombre réel d'étages, d'entrées, de zones communes et de stationnements",
                    "Les longueurs probables entre le local principal et les zones de distribution",
                    "La place disponible pour des armoires techniques ou petits locaux réseau d'étage",
                    "Le besoin de fibre ou de liens montants pour soutenir la distribution",
                    "Les systèmes qui doivent partager la même base: WiFi, caméras, intercom, accès et autres technologies",
                ],
            },
            {
                'eyebrow': 'WiFi et qualité',
                'title': "À cette taille, le WiFi doit suivre la structure du bâtiment",
                'paragraphs': [
                    "Le WiFi performant ne vient pas seulement du nombre de points d'accès. Il dépend aussi des chemins de câbles, de la qualité du PoE, de la capacité des commutateurs et de la façon dont les étages sont raccordés.",
                    "Plus l'immeuble grandit, plus le WiFi doit être traité comme un système qui s'appuie sur une vraie infrastructure, pas comme une couche ajoutée à la fin.",
                ],
            },
        ],
        'faq_items': [
            ("Faut-il prévoir des armoires ou locaux d'étage ?", "Souvent oui. Cela dépend des distances, du nombre d'étages et des zones à couvrir, mais c'est fréquent à cette taille."),
            ("La fibre est-elle plus probable dans un immeuble de 25 à 100 unités ?", "Oui. Dès que les longueurs augmentent ou que plusieurs niveaux doivent être reliés proprement, la fibre devient souvent la meilleure base."),
            ("Peut-on faire ça par phases dans un immeuble occupé ?", "Oui. C'est même souvent la bonne approche quand il faut limiter les interruptions pour les occupants et la gestion."),
        ],
        'cta_title': "Vous avez un immeuble de 25 à 100 unités à équiper ?",
        'cta_copy': "Décrivez le nombre d'étages, les zones communes, les accès et l'état actuel du réseau. On vous aidera à cadrer la bonne base technique.",
        'cta_label': 'Obtenir une soumission',
    },
    'multifamily-network-100-plus': {
        'path': '/fr/infrastructure-wifi-100-unites-et-plus/',
        'title': 'WiFi et réseau pour immeubles de 100 unités et plus | Opticable',
        'desc': "WiFi, câblage, fibre, locaux réseau et systèmes connectés pour immeubles de 100 unités et plus au Québec.",
        'eyebrow': 'Immeubles de 100 unités et plus',
        'headline': 'WiFi et infrastructure pour immeubles de 100 unités et plus',
        'intro': "À partir de 100 unités, on ne parle plus seulement d'ajouter du WiFi ou quelques systèmes. On parle d'une architecture de bâtiment: locaux réseau, liens entre étages, capacité, segmentation, équipements communs et planification de croissance.",
        'panel_title': "Ce qu'il faut penser plus tôt",
        'panel_copy': "Plus le bâtiment est grand, plus il faut clarifier tôt le local principal, les distributions d'étage, la fibre, les aires communes, les accès et la logique d'exploitation.",
        'service_keys': ('commercial-wifi-installation', 'network-infrastructure', 'fiber-optic-installation', 'access-control-systems'),
        'guide_keys': ('technology-retrofit-occupied-building', 'network-room-rack-cleanup', 'cat6a-or-fiber-commercial-building'),
        'related_keys': ('multifamily-network-infrastructure', 'multifamily-network-10-25', 'multifamily-network-25-100'),
        'sections': [
            {
                'eyebrow': 'Échelle',
                'title': "Quand l'immeuble devient une vraie architecture réseau",
                'paragraphs': [
                    "À cette taille, il faut penser capacité, maintenance, documentation, redondance pratique, phases de travaux et coordination entre plusieurs zones du bâtiment. Le WiFi, les caméras, l'accès et l'intercom s'appuient tous sur cette même base.",
                    "Un seul choix improvisé au départ peut compliquer des dizaines d'ajouts par la suite. Il vaut mieux clarifier la structure générale avant de multiplier les équipements.",
                ],
            },
            {
                'eyebrow': 'À prévoir tôt',
                'title': "Ce qu'il faut cadrer dès le départ",
                'cards': [
                    ("Local réseau principal", "Le cœur du bâtiment, là où la capacité, la commutation et les arrivées doivent rester lisibles."),
                    ("Locaux ou armoires d'étage", "Des points de redistribution pour éviter des longueurs excessives et simplifier la maintenance."),
                    ("Liens fibre et câbles entre étages", "La colonne vertébrale qui relie proprement les niveaux, les ailes et les zones éloignées."),
                    ("Aires communes et sécurité", "WiFi, caméras, intercom, accès, stationnement et équipements du bâtiment planifiés comme un ensemble."),
                ],
            },
            {
                'eyebrow': 'Erreurs fréquentes',
                'title': "Ce qui coûte cher quand on le repousse trop tard",
                'items': [
                    "Ajouter des points d'accès WiFi sans avoir validé les liens, le PoE et la distribution d'étage",
                    "Laisser plusieurs systèmes partager un local réseau déjà saturé ou mal documenté",
                    "Reporter la fibre ou les liaisons montantes alors que la distance et la capacité l'exigent déjà",
                    "Multiplier les ajouts par phases sans architecture commune pour les aires communes et les accès",
                    "Sous-estimer la documentation nécessaire pour la maintenance future",
                ],
            },
            {
                'eyebrow': 'Nouveau projet ou remise à niveau',
                'title': "Ce qu'on regarde dans un nouveau bâtiment ou une modernisation majeure",
                'paragraphs': [
                    "Dans un nouveau projet, on veut profiter des bonnes phases pour positionner les locaux, les chemins de câbles, les arrivées et les réserves futures. Dans un immeuble existant, on cherche plutôt la meilleure façon de moderniser sans perturber inutilement l'exploitation.",
                    "Dans les deux cas, l'objectif reste le même: une base réseau stable qui rend l'immeuble plus connecté, plus simple à gérer et plus prêt pour les technologies à venir.",
                ],
            },
        ],
        'faq_items': [
            ("Faut-il penser l'infrastructure par phases ?", "Oui. À cette taille, une approche par phases est souvent la plus réaliste, mais elle doit suivre une architecture commune dès le départ."),
            ("Est-ce que tous les systèmes peuvent partager la même base réseau ?", "Oui, si elle est bien planifiée. C'est justement ce qui rend l'exploitation plus claire et évite les ajouts incohérents."),
            ("Pourquoi la documentation devient-elle si importante ?", "Parce qu'un grand immeuble évolue constamment. Sans repérage clair, chaque ajout ou dépannage devient plus long, plus risqué et plus coûteux."),
        ],
        'cta_title': "Vous planifiez un immeuble de 100 unités et plus ?",
        'cta_copy': "Parlez-nous du nombre d'étages, des zones communes, des accès et des systèmes à coordonner. On vous aidera à structurer l'architecture avant les ajouts dispersés.",
        'cta_label': 'Parler du projet',
    },
}
MULTIFAMILY_CLUSTER_PAGES_EN = {
    'multifamily-network-infrastructure': {
        'path': '/en/multifamily-wifi-network-infrastructure/',
        'title': 'Multifamily WiFi and Network Infrastructure | Opticable',
        'desc': 'Cabling, fiber, WiFi access points, network rooms, cameras, and access systems for multifamily buildings in Quebec.',
        'eyebrow': 'Multifamily buildings',
        'headline': 'WiFi and network infrastructure for multifamily buildings',
        'intro': "Good WiFi in a multifamily building rarely starts with the access point model alone. It starts with a clear network foundation: cabling, fiber, switches, PoE, internet handoffs, network rooms, and clean links between floors.",
        'panel_title': 'The foundation before WiFi',
        'panel_copy': 'When that foundation is planned properly, WiFi, cameras, intercom, access control, and the other building systems stay more stable, easier to expand, and simpler to manage together.',
        'service_keys': ('commercial-wifi-installation', 'network-infrastructure', 'structured-cabling', 'fiber-optic-installation'),
        'guide_keys': ('commercial-wifi-audit-checklist', 'cat6a-or-fiber-commercial-building', 'network-room-rack-cleanup', 'technology-retrofit-occupied-building'),
        'related_keys': ('multifamily-network-10-25', 'multifamily-network-25-100', 'multifamily-network-100-plus'),
        'sections': [
            {
                'eyebrow': 'Network foundation',
                'title': 'The base before the WiFi access points',
                'paragraphs': [
                    'In a multifamily building, WiFi quality depends first on the wired base that feeds it. If the cabling, PoE, switches, internet handoffs, and network rooms are improvised, adding access points only fixes part of the problem.',
                    'That same base also supports WiFi access points, cameras, intercom, access control, common-area equipment, management spaces, and future building technology needs.',
                ],
            },
            {
                'eyebrow': 'Connected building',
                'title': 'What the infrastructure needs to connect',
                'cards': [
                    ('WiFi access points and antennas', 'Consistent coverage across lobbies, corridors, common spaces, management areas, and technical zones.'),
                    ('Cameras, intercom, and access', 'Entry and security systems that share a clean network base instead of being added piecemeal.'),
                    ('Suites, services, and common spaces', 'Stable links for shared areas, technical rooms, and the building operations behind them.'),
                    ('Future growth', 'A structure that leaves room for more equipment, more floors, or new shared areas without starting over.'),
                ],
            },
            {
                'eyebrow': 'Before the quote',
                'title': 'What we confirm before recommending the architecture',
                'items': [
                    'The number of units, floors, and entries that need to be served',
                    'Whether the building is existing, occupied, under renovation, or a new project',
                    'Where the main network room is and how much room is available there',
                    'Whether floor-level closets or secondary technical cabinets are needed',
                    'The cable paths between floors and the common spaces that need reliable coverage',
                    'Provider handoffs, site constraints, and the zones where WiFi is already weak',
                ],
            },
            {
                'eyebrow': 'Plain language',
                'title': 'What do main network room, floor closet, and floor-to-floor cabling actually mean?',
                'paragraphs': [
                    'The main network room is usually where the building handoffs arrive, where the core switching lives, and where the main rack is organized. In larger buildings, smaller floor closets or secondary technical cabinets are added closer to the spaces being served.',
                    'The cables between floors link that main room to the other levels. That backbone is what lets WiFi, cameras, intercom, access control, and other building systems be distributed cleanly instead of one by one without structure.',
                ],
            },
        ],
        'faq_items': [
            ('Does good WiFi depend mostly on the access point model?', 'No. The access point matters, but WiFi quality also depends on cabling, PoE, switching, placement, building materials, and how the network is organized.'),
            ('Do multifamily buildings always need fiber?', 'Not everywhere, but fiber often becomes logical for links between floors, distant areas, or multiple network rooms where copper limits become a problem.'),
            ('Why add a floor-level network closet?', 'To bring distribution closer to the served areas when one main room is no longer enough. That keeps cable runs more realistic and future changes easier.'),
            ('Is this relevant for an existing building too?', 'Yes. The same logic applies to occupied buildings and new projects. The main difference is how the work gets phased.'),
        ],
        'cta_title': 'Plan the network foundation of your multifamily building',
        'cta_copy': 'Tell us how many units, floors, common spaces, and systems need to connect. We will help frame a coherent network base before the add-ons pile up.',
        'cta_label': 'Request a quote',
    },
    'multifamily-network-10-25': {
        'path': '/en/wifi-network-infrastructure-10-25-units/',
        'title': 'WiFi and Network Infrastructure for 10 to 25 Units | Opticable',
        'desc': 'WiFi infrastructure, cabling, fiber, and network rooms for 10 to 25 unit multifamily buildings in Quebec.',
        'eyebrow': '10 to 25 units',
        'headline': 'WiFi and network infrastructure for 10 to 25 units',
        'intro': 'In a 10 to 25 unit building, the goal is not to overbuild. The goal is to create a simple, clean foundation that can support the entry, common-area WiFi, cameras, and the other connected systems without becoming messy later.',
        'panel_title': 'What matters most',
        'panel_copy': 'A readable main network room, clean cable paths, well-placed WiFi access points, and a realistic scope for the common areas.',
        'service_keys': ('commercial-wifi-installation', 'structured-cabling', 'network-infrastructure', 'intercom-systems'),
        'guide_keys': ('intercom-pricing-multi-tenant-building', 'commercial-wifi-audit-checklist', 'cat6a-or-fiber-commercial-building'),
        'related_keys': ('multifamily-network-infrastructure', 'multifamily-network-25-100', 'multifamily-network-100-plus'),
        'sections': [
            {
                'eyebrow': 'Typical profile',
                'title': 'What we often see at this size',
                'paragraphs': [
                    'One main network room can often be enough, sometimes with a small secondary cabinet if a few areas are too far away. A common mistake is letting each new system attach itself to whatever already exists with no overall logic.',
                    'Even at this scale, the building still needs a clean base for intercom, access control, cameras, common-area WiFi, and future additions.',
                ],
            },
            {
                'eyebrow': 'Typical scopes',
                'title': 'What gets installed most often',
                'items': [
                    'Intercom or video intercom at the main entry',
                    'Access control for the entry, garage, or shared rooms',
                    'Cameras in the lobby, corridors, parking, and sensitive areas',
                    'WiFi access points in common spaces, corridors, or shared rooms',
                    'Network-room cleanup and a few structured links where needed',
                ],
            },
            {
                'eyebrow': 'Before pricing',
                'title': 'What should be confirmed before a useful quote',
                'items': [
                    'The number of floors and the real distance between the areas to connect',
                    'Where the main network room sits and how much rack space is available',
                    'Which common spaces need reliable WiFi from the start',
                    'Which entries need to be secured and how visitors are handled',
                    'Whether the building is existing, occupied, under renovation, or new',
                ],
            },
            {
                'eyebrow': 'WiFi quality',
                'title': 'At this size, good WiFi is still mostly a network-foundation issue',
                'paragraphs': [
                    'A smaller building does not need heavy architecture, but it still needs clean infrastructure. Poorly placed or poorly powered access points create uneven WiFi even when the hardware itself is fine.',
                    'A clean base also makes future cameras, access control, new common areas, or added building systems much easier to support.',
                ],
            },
        ],
        'faq_items': [
            ('Is one network room always enough?', 'Not always. It depends on the number of floors, the cable lengths, and the spaces that need to be served. Sometimes a small secondary cabinet avoids a lot of compromise.'),
            ('Should fiber be considered at this size?', 'Not in every case, but it can become logical when distances rise quickly or some zones are too far away for a clean copper-only layout.'),
            ('Can the common-area WiFi be added later?', 'Yes, but it is better to plan the cabling, PoE, and access-point locations now so later work does not cost more than it should.'),
        ],
        'cta_title': 'Planning a 10 to 25 unit building?',
        'cta_copy': 'Tell us about the floor count, common areas, and connected systems. We will help keep the infrastructure simple and durable.',
        'cta_label': 'Request a quote',
    },
    'multifamily-network-25-100': {
        'path': '/en/wifi-network-infrastructure-25-100-units/',
        'title': 'Network Infrastructure for 25 to 100 Units | Opticable',
        'desc': 'Network infrastructure, WiFi, fiber, and technical rooms for 25 to 100 unit multifamily buildings in Quebec.',
        'eyebrow': '25 to 100 units',
        'headline': 'Network infrastructure for 25 to 100 units',
        'intro': 'Between 25 and 100 units, the infrastructure already has to manage more density, more floors, more common spaces, and more systems. WiFi becomes one layer on top of a network foundation that needs to stay clear and expandable.',
        'panel_title': 'What changes at this size',
        'panel_copy': 'A main network room, floor cabinets or closets, cleaner vertical links, and a real distribution logic between the building zones become much more common.',
        'service_keys': ('commercial-wifi-installation', 'network-infrastructure', 'structured-cabling', 'fiber-optic-installation'),
        'guide_keys': ('commercial-wifi-audit-checklist', 'cat6a-or-fiber-commercial-building', 'technology-retrofit-occupied-building'),
        'related_keys': ('multifamily-network-infrastructure', 'multifamily-network-10-25', 'multifamily-network-100-plus'),
        'sections': [
            {
                'eyebrow': 'Structure',
                'title': 'What becomes important as the building grows',
                'paragraphs': [
                    'One central room is often no longer enough to serve everything cleanly. At this size, a main network room plus one or more floor-level distribution points becomes much more common.',
                    'That structure keeps cable lengths more realistic, distributes PoE more cleanly, and makes it easier to support WiFi, cameras, intercom, and access control without patchwork additions.',
                ],
            },
            {
                'eyebrow': 'Typical scopes',
                'title': 'What we usually prepare in buildings of this size',
                'cards': [
                    ('Common-area WiFi', 'Multiple WiFi access points coordinated across floors, corridors, lobbies, shared rooms, and the real density of use.'),
                    ('Floor-to-floor links', 'Copper or fiber links between the main room and the served levels, instead of pulling every system ad hoc.'),
                    ('Integrated security systems', 'Cameras, intercom, and access control that share a coherent network base instead of separate islands.'),
                    ('Future growth', 'A structure that leaves room for more units, more equipment, and additional building zones.'),
                ],
            },
            {
                'eyebrow': 'Before the quote',
                'title': 'What should be confirmed before choosing the architecture',
                'items': [
                    'The real number of floors, entries, common spaces, and parking zones',
                    'The likely distances between the main room and the distribution points',
                    'How much room exists for floor cabinets or small technical rooms',
                    'Whether fiber or stronger vertical links are needed for the distribution',
                    'Which systems must share the same base: WiFi, cameras, intercom, access, and the other connected layers',
                ],
            },
            {
                'eyebrow': 'WiFi quality',
                'title': 'At this scale, WiFi has to follow the building structure',
                'paragraphs': [
                    'Good WiFi does not come only from the number of access points. It also depends on cable paths, PoE quality, switch capacity, and how the floors are tied back into the network.',
                    'The larger the building gets, the more WiFi needs to be treated as one system riding on proper infrastructure, not as an afterthought added at the end.',
                ],
            },
        ],
        'faq_items': [
            ('Do floor closets or cabinets become more likely?', 'Yes. Once distances, floor count, and common-space coverage increase, they often become the cleanest way to distribute the network.'),
            ('Is fiber more likely in a 25 to 100 unit building?', 'Yes. As the runs get longer and more levels need to be tied together cleanly, fiber often becomes the right backbone.'),
            ('Can this be phased in an occupied building?', 'Yes. That is often the right approach when management and occupants need disruption kept under control.'),
        ],
        'cta_title': 'Do you need to equip a 25 to 100 unit building?',
        'cta_copy': 'Tell us the floor count, common spaces, access points, and current network state. We will help frame the right technical base.',
        'cta_label': 'Request a quote',
    },
    'multifamily-network-100-plus': {
        'path': '/en/wifi-network-infrastructure-100-plus-units/',
        'title': 'WiFi and Infrastructure for 100+ Unit Buildings | Opticable',
        'desc': 'WiFi, cabling, fiber, network rooms, and connected systems for 100+ unit multifamily buildings in Quebec.',
        'eyebrow': '100+ units',
        'headline': 'WiFi and infrastructure for 100+ unit buildings',
        'intro': 'Once a building reaches 100 units or more, the conversation is no longer only about adding WiFi or a few systems. It becomes a building architecture question: network rooms, floor distribution, capacity, segmentation, common-area equipment, and future growth.',
        'panel_title': 'What needs to be settled earlier',
        'panel_copy': 'The larger the building, the earlier the main room, floor distribution, fiber, common areas, entry systems, and operating logic need to be made clear.',
        'service_keys': ('commercial-wifi-installation', 'network-infrastructure', 'fiber-optic-installation', 'access-control-systems'),
        'guide_keys': ('technology-retrofit-occupied-building', 'network-room-rack-cleanup', 'cat6a-or-fiber-commercial-building'),
        'related_keys': ('multifamily-network-infrastructure', 'multifamily-network-10-25', 'multifamily-network-25-100'),
        'sections': [
            {
                'eyebrow': 'Scale',
                'title': 'When the building becomes a real network architecture',
                'paragraphs': [
                    'At this size, capacity, maintenance, documentation, phased work, and coordination between many building zones all matter. WiFi, cameras, access control, and intercom all depend on the same base.',
                    'One improvised decision early on can complicate dozens of future additions. It is better to clarify the overall structure before equipment begins multiplying.',
                ],
            },
            {
                'eyebrow': 'Plan early',
                'title': 'What should be defined upfront',
                'cards': [
                    ('Main network room', 'The building core where capacity, switching, and handoffs need to stay readable.'),
                    ('Floor closets or cabinets', 'Distribution points that keep cable runs realistic and make support easier later.'),
                    ('Fiber and floor-to-floor cabling', 'The backbone that ties levels, wings, and distant areas together cleanly.'),
                    ('Common areas and security', 'WiFi, cameras, intercom, access, parking, and building systems planned as one environment.'),
                ],
            },
            {
                'eyebrow': 'Common mistakes',
                'title': 'What becomes expensive when it gets pushed too late',
                'items': [
                    'Adding WiFi access points before validating the links, PoE, and floor distribution',
                    'Letting many systems share a network room that is already saturated or poorly documented',
                    'Postponing fiber or vertical links when distance and capacity already demand them',
                    'Rolling out separate phases with no common architecture for common areas and access points',
                    'Underestimating the documentation needed for future support and change',
                ],
            },
            {
                'eyebrow': 'New build or major retrofit',
                'title': 'What we look at in new construction or large upgrades',
                'paragraphs': [
                    'In a new project, the goal is to use the right construction phases to position rooms, pathways, handoffs, and future reserves. In an existing building, the goal is to modernize without disrupting operations more than necessary.',
                    'In both cases, the objective stays the same: a stable network base that makes the building more connected, easier to manage, and ready for the next technology layer.',
                ],
            },
        ],
        'faq_items': [
            ('Should the infrastructure be phased?', 'Yes. At this size, phasing is often the most realistic approach, but the phases should still follow one common architecture from the start.'),
            ('Can all systems share the same network foundation?', 'Yes, if it is planned properly. That is exactly what keeps operations clearer and prevents disconnected add-ons.'),
            ('Why does documentation matter more at this scale?', 'Because a large building keeps changing. Without clear labeling and structure, every addition or troubleshooting visit takes longer and costs more.'),
        ],
        'cta_title': 'Planning a 100+ unit building?',
        'cta_copy': 'Tell us about the floors, common spaces, access systems, and technologies that need to connect. We will help structure the architecture before fragmented additions take over.',
        'cta_label': 'Discuss the project',
    },
}
MULTIFAMILY_CLUSTER_PAGES_BY_LANG = {
    'en': MULTIFAMILY_CLUSTER_PAGES_EN,
    'fr': MULTIFAMILY_CLUSTER_PAGES,
}
MULTIFAMILY_CLUSTER_KEYS = tuple(MULTIFAMILY_CLUSTER_PAGES.keys())
FR_HOME_RESOURCE_KEYS = (
    'camera-system-pricing-commercial-building',
    'access-control-pricing-commercial-building',
    'commercial-wifi-audit-checklist',
    'structured-cabling-pricing-office-retail',
)
FR_CONTACT_RESOURCE_KEYS = (
    'access-control-pricing-commercial-building',
    'intercom-pricing-multi-tenant-building',
    'camera-system-pricing-commercial-building',
    'commercial-wifi-audit-checklist',
    'structured-cabling-pricing-office-retail',
    'technology-retrofit-occupied-building',
)
FR_FAQ_RESOURCE_KEYS = (
    'access-control-vs-intercom',
    'intercom-audio-or-video-commercial-building',
    'commercial-wifi-audit-checklist',
    'cat6a-or-fiber-commercial-building',
    'network-room-rack-cleanup',
    'analog-cctv-to-ip-migration',
)
FR_BLOG_RESOURCE_KEYS = DECISION_ARTICLE_KEYS
FR_HOME_EXTRA_SECTIONS = [
    {
        'eyebrow': 'Avant de nous contacter',
        'title': "Les 4 infos qui nous aident à bien cadrer votre projet",
        'copy': "Le but de cette section est simple : vous montrer quoi nous dire dès le départ pour éviter les allers-retours et obtenir une réponse plus utile.",
        'cards': [
            ("Type d'immeuble", 'Bureau, commerce, immeuble multilogement, entrepôt ou bâtiment à locataires multiples.'),
            ('Zones à traiter', 'Entrées, corridors, stationnement, suites, aires communes, salle technique ou local réseau.'),
            ('Systèmes visés', "Caméras, contrôle d'accès, intercom, WiFi, câblage, fibre ou remise en ordre du rack."),
            ('Contraintes du site', 'Bâtiment occupé, travaux par phases, accès limités, horaires permis ou échéancier serré.'),
        ],
    },
    {
        'eyebrow': 'Exemples concrets',
        'title': "Types de projets qu'on prend en charge",
        'copy': "Cette section sert à montrer rapidement si votre besoin ressemble à un projet qu'on traite souvent. Si oui, on peut habituellement cadrer la prochaine étape assez vite.",
        'items': [
            "Ajout ou remplacement de caméras aux entrées, dans les corridors, le stationnement et les aires communes",
            "Mise à niveau du contrôle d'accès d'un hall, d'une porte arrière, d'un local technique ou d'une zone restreinte",
            "Installation d'un intercom à l'entrée principale d'un immeuble ou d'un espace partagé",
            "Audit WiFi et ajout ou repositionnement de points d'accès dans un bâtiment occupé",
            'Remise en ordre du câblage, du rack ou du local réseau avant une expansion',
            "Lien principal en Cat6A ou en fibre pour relier des étages, des suites ou des zones techniques",
            'Mise à niveau technologique par phases pour limiter les interruptions',
        ],
    },
]
FR_CONTACT_EXTRA_SECTIONS = [
    {
        'eyebrow': 'Avant la demande',
        'title': 'Ce qui accélère vraiment une soumission',
        'copy': "Vous n'avez pas besoin d'un cahier de charges complet, mais quelques détails changent tout.",
        'items': [
            "Le type d'immeuble et son niveau d'occupation",
            "Les systèmes concernés : caméras, contrôle d'accès, intercom, WiFi, câblage, fibre ou local réseau",
            "Les zones à traiter : entrées, corridors, stationnement, suites, quai, salle technique ou aire commune",
            "Le nombre approximatif de portes, de caméras, de points d'accès WiFi ou de prises réseau à ajouter",
            "Les contraintes : horaires permis, accès limités, travaux hors heures ou coordination avec d'autres métiers",
            "L'échéancier : besoin immédiat, budget en préparation ou projet à phaser",
        ],
    },
    {
        'eyebrow': "Après l'envoi",
        'title': 'Ce qui se passe ensuite',
        'copy': "On n'envoie pas un prix générique. On valide d'abord la portée, les contraintes et la bonne prochaine étape.",
        'cards': [
            ('Lecture du contexte', "On vérifie le type d'immeuble, la portée visée et ce qui manque pour chiffrer correctement."),
            ('Retour ciblé', "On revient avec les questions utiles, une visite de site ou une direction claire pour la soumission."),
            ('Portée réaliste', "Les postes critiques, les cheminements et les limites du site sont cadrés avant de confirmer le bon scénario."),
        ],
    },
]
FR_GUIDE_SECTION_COPY = {
    'home': {
        'eyebrow': 'Guides et décisions',
        'title': 'Pages utiles avant de demander une soumission',
        'intro': "Des réponses concrètes pour mieux cadrer le budget, le bon système ou les bonnes prochaines étapes.",
        'cta_href_key': 'guides',
        'cta_label': 'Voir tous les guides',
    },
    'contact': {
        'eyebrow': 'Pages utiles',
        'title': "Vous voulez clarifier le projet avant d'envoyer le formulaire ?",
        'intro': "Ces pages répondent aux questions qui reviennent le plus souvent avant une demande de prix.",
        'cta_href_key': 'guides',
        'cta_label': 'Voir tous les guides',
    },
    'faq': {
        'eyebrow': 'Guides détaillés',
        'title': "Besoin de plus qu'une réponse courte ?",
        'intro': "Voici les pages de référence à consulter quand vous devez comparer des options, cadrer un budget ou préparer un site occupé.",
        'cta_href_key': 'guides',
        'cta_label': 'Voir tous les guides',
    },
    'blog': {
        'eyebrow': 'Pages de décision',
        'title': 'Comparer, budgéter et préparer le bon scénario',
        'intro': "En plus des articles du blogue, voici les pages qui répondent le plus directement aux questions d'achat.",
        'cta_href_key': 'guides',
        'cta_label': 'Voir tous les guides',
    },
}
EN_GUIDE_SECTION_COPY = {
    'home': {
        'eyebrow': 'Guides and decisions',
        'title': 'Helpful pages before requesting a quote',
        'intro': 'Practical answers to clarify budget, system choice, and the right next step.',
        'cta_href_key': 'guides',
        'cta_label': 'View all guides',
    },
    'contact': {
        'eyebrow': 'Helpful pages',
        'title': 'Want to clarify the project before sending the form?',
        'intro': 'These pages answer the questions that come up most often before a quote request.',
        'cta_href_key': 'guides',
        'cta_label': 'View all guides',
    },
    'faq': {
        'eyebrow': 'Detailed guides',
        'title': 'Need more than a short answer?',
        'intro': 'Use these reference pages when you need to compare options, frame a budget, or prepare an occupied site.',
        'cta_href_key': 'guides',
        'cta_label': 'View all guides',
    },
    'blog': {
        'eyebrow': 'Decision pages',
        'title': 'Compare, budget, and prepare the right scope',
        'intro': 'In addition to blog articles, these pages answer the most common buying and planning questions.',
        'cta_href_key': 'guides',
        'cta_label': 'View all guides',
    },
}
GUIDE_SECTION_COPY = {
    'en': EN_GUIDE_SECTION_COPY,
    'fr': FR_GUIDE_SECTION_COPY,
}
FR_SERVICE_GUIDE_KEYS = {
    'security-camera-systems': ('camera-system-pricing-commercial-building', 'analog-cctv-to-ip-migration'),
    'access-control-systems': ('access-control-pricing-commercial-building', 'access-control-vs-intercom'),
    'commercial-wifi-installation': ('commercial-wifi-audit-checklist', 'technology-retrofit-occupied-building'),
    'structured-cabling': ('structured-cabling-pricing-office-retail', 'cat6a-or-fiber-commercial-building', 'network-room-rack-cleanup'),
    'intercom-systems': ('intercom-pricing-multi-tenant-building', 'intercom-audio-or-video-commercial-building', 'access-control-vs-intercom'),
    'network-infrastructure': ('network-room-rack-cleanup', 'cat6a-or-fiber-commercial-building'),
    'fiber-optic-installation': ('cat6a-or-fiber-commercial-building', 'technology-retrofit-occupied-building'),
    'it-services-and-support': ('network-room-rack-cleanup', 'technology-retrofit-occupied-building'),
    'ip-phone-systems': ('structured-cabling-pricing-office-retail', 'technology-retrofit-occupied-building'),
}
FR_SERVICE_INDUSTRY_KEYS = {
    'security-camera-systems': ('industry-office-building', 'industry-multi-tenant-building', 'industry-retail-and-sales-floor'),
    'access-control-systems': ('industry-office-building', 'industry-multi-tenant-building', 'industry-retail-and-sales-floor'),
    'commercial-wifi-installation': ('industry-office-building', 'industry-multi-tenant-building', 'industry-retail-and-sales-floor', 'industry-warehouse-and-industrial'),
    'structured-cabling': ('industry-office-building', 'industry-multi-tenant-building', 'industry-retail-and-sales-floor', 'industry-warehouse-and-industrial'),
    'intercom-systems': ('industry-multi-tenant-building', 'industry-office-building'),
    'network-infrastructure': ('industry-office-building', 'industry-multi-tenant-building', 'industry-retail-and-sales-floor', 'industry-warehouse-and-industrial'),
    'fiber-optic-installation': ('industry-office-building', 'industry-multi-tenant-building', 'industry-warehouse-and-industrial'),
    'it-services-and-support': ('industry-office-building', 'industry-retail-and-sales-floor'),
    'ip-phone-systems': ('industry-office-building', 'industry-retail-and-sales-floor'),
}
MULTIFAMILY_CLUSTER_SERVICE_KEYS = {
    'commercial-wifi-installation': MULTIFAMILY_CLUSTER_KEYS,
    'structured-cabling': MULTIFAMILY_CLUSTER_KEYS,
    'network-infrastructure': MULTIFAMILY_CLUSTER_KEYS,
    'fiber-optic-installation': MULTIFAMILY_CLUSTER_KEYS,
}
FR_SERVICE_CASE_STUDY_KEYS = {
    'security-camera-systems': ('case-office-building', 'case-retail-space'),
    'access-control-systems': ('case-office-building', 'case-multitenant-building'),
    'commercial-wifi-installation': ('case-office-building', 'case-multitenant-building'),
    'structured-cabling': ('case-office-building', 'case-construction-site'),
}

T['fr'].update({
    'about': 'À propos',
    'tagline': 'Spécialistes des infrastructures technologiques commerciales',
    'all_services': 'Voir les services',
    'company': "Opticable installe des caméras de sécurité, des systèmes de contrôle d'accès, des intercoms, du WiFi commercial, du câblage structuré, de la fibre optique et de l'infrastructure réseau pour les immeubles commerciaux.",
    'cta_title': "Besoin d'un spécialiste pour vos caméras, votre contrôle d'accès, votre WiFi ou les communications de votre bâtiment ?",
    'cta_copy': "Envoyez une demande en précisant le type d'immeuble, les systèmes visés et l'échéancier souhaité.",
    'footer': "Opticable dessert les entreprises et les immeubles gérés partout au Québec, notamment à Montréal, Laval, Longueuil, sur la Rive-Sud, la Rive-Nord et dans les Laurentides.",
    'privacy': 'Confidentialité',
    'privacy_title': 'Confidentialité et cookies | Opticable',
    'privacy_desc': "Comment Opticable traite les renseignements transmis via le site, le formulaire Zoho et les technologies comme les cookies ou le stockage local du navigateur.",
    'privacy_h1': 'Confidentialité, cookies et services tiers.',
    'privacy_intro': "Cette page explique quelles données peuvent être traitées via le site, quand des services tiers sont chargés et comment vous pouvez limiter ou retirer votre consentement.",
    'privacy_cards_title': 'Comment le site gère les données',
    'privacy_cards_intro': "Le site reste volontairement simple. Il n'utilise pas d'outil d'analytics ni de pixels publicitaires pour le moment, mais certains services tiers peuvent intervenir quand vous choisissez de les utiliser.",
    'privacy_cards': [
        ('Demandes de contact', "Quand vous nous écrivez, nous appelez ou soumettez une demande, nous recevons les renseignements nécessaires pour répondre et faire le suivi."),
        ('Zoho Forms', "Le formulaire de soumission est fourni par Zoho. Quand le formulaire est affiché ou soumis, Zoho peut traiter les renseignements transmis selon ses propres conditions, cookies ou technologies similaires."),
        ('Cookies techniques', "L'hébergement, le CDN, la sécurité ou l'anti-bot, notamment via Cloudflare lorsqu'il est utilisé, peuvent déposer des cookies strictement nécessaires pour livrer et protéger le site."),
        ('Stockage local', "Quand vous acceptez l'avis relatif aux cookies, le site enregistre ce choix localement dans votre navigateur pour éviter de vous l'afficher à chaque page."),
    ],
    'privacy_choices_title': 'Vos choix',
    'privacy_choices': [
        'Utiliser le téléphone ou les courriels affichés sur le site au lieu du formulaire Zoho.',
        'Bloquer ou supprimer les cookies dans votre navigateur.',
        "Effacer le stockage local du site dans votre navigateur pour réafficher l'avis relatif aux cookies.",
        "Communiquer avec Opticable si vous avez des questions sur le traitement d'une demande de soumission.",
    ],
    'footer_contact_title': 'Coordonnées',
    'footer_contact_intro': "Retrouvez les coordonnées d'Opticable sur toutes les pages.",
    'cookie_banner_eyebrow': 'Cookies',
    'cookie_banner_title': 'Avis relatif aux cookies',
    'cookie_banner_copy': "Ce site peut utiliser des cookies techniques ou des technologies similaires via des services comme Cloudflare ou Zoho lorsqu'ils sont nécessaires pour livrer et protéger le site.",
    'cookie_banner_accept': 'Accepter',
    'thanks': 'Merci',
    'thanks_title': 'Merci | Demande de soumission reçue | Opticable',
    'thanks_desc': "Merci pour votre demande de soumission. Opticable examinera les renseignements transmis et fera un suivi pour discuter de votre projet.",
    'thanks_h1': 'Merci. Votre demande de soumission a été envoyée.',
    'thanks_intro': "Nous avons bien reçu votre demande et nous allons examiner les détails transmis pour votre projet de caméras, contrôle d'accès, intercom, WiFi, câblage, fibre ou réseau.",
    'thanks_panel_title': 'Prochaine étape',
    'thanks_panel_copy': "Notre équipe analyse la portée du projet, le type d'immeuble et l'échéancier avant de faire un suivi par courriel ou par téléphone.",
    'thanks_steps': [
        'Vérifier les systèmes, services et détails du bâtiment transmis.',
        "Confirmer la portée, les délais et le besoin d'une visite de site.",
        'Revenir vers vous avec la prochaine étape pour la soumission, la planification ou la coordination.',
    ],
    'thanks_return_home': "Retour à l'accueil",
    'thanks_view_services': 'Voir les services',
    'home_title': "Caméras, accès, WiFi et réseau commercial | Opticable",
    'home_desc': "Opticable installe caméras, accès, intercom, WiFi commercial et réseau pour immeubles commerciaux au Québec.",
    'home_kicker': 'Technologie commerciale et systèmes du bâtiment',
    'home_h1': "Caméras, accès, WiFi et réseau pour immeubles commerciaux",
    'home_intro': "Opticable aide les immeubles commerciaux à déployer leurs systèmes de sécurité, de contrôle d'accès, de sans-fil et l'infrastructure qui les soutient, avec une installation soignée et une livraison bien organisée.",
    'home_points': [
        'Caméras de sécurité pour les aires communes, les périmètres, les suites et les zones d’exploitation',
        "Contrôle d'accès et intercoms pour halls, entrées et immeubles gérés",
        'WiFi commercial pour bureaux, commerces et immeubles multilogements',
        'Téléphonie IP, lignes VoIP et postes de travail pour bureaux et opérations',
        'Câblage structuré et fibre optique pour appuyer ces systèmes',
        'Infrastructure réseau, racks et locaux techniques pour la connectivité du bâtiment',
    ],
    'home_panel': "Caméras, accès sécurisés, WiFi, câblage et infrastructure réseau pour les immeubles commerciaux.",
    'trust_title': 'Pourquoi Opticable',
    'trust': [
        ('Approche axée sur la sécurité', "Les caméras, le contrôle d'accès, le WiFi et le câblage sont planifiés ensemble."),
        ('Livraison bien structurée', 'Le repérage, les cheminements et les locaux techniques font partie intégrante de la livraison.'),
        ('Systèmes plus faciles à entretenir', "Une infrastructure bien organisée simplifie l'entretien, le service et les ajouts futurs."),
    ],
    'services_title': 'Services technologiques commerciaux | Opticable',
    'services_desc': "Les pages de service d'Opticable couvrent les caméras de sécurité, le contrôle d'accès, les intercoms, le WiFi commercial, le câblage structuré, la fibre optique, l'infrastructure réseau et la téléphonie IP.",
    'services_h1': "Des services technologiques commerciaux pensés pour la sécurité, la connectivité et un soutien plus simple à long terme.",
    'services_intro': "Opticable met d'abord l'accent sur les caméras, le contrôle d'accès, les intercoms et le WiFi d'affaires. Le câblage, la fibre, les racks et les locaux réseau viennent appuyer ces systèmes.",
    'extra_title': 'Services connexes',
    'extra_intro': "Travaux et services souvent inclus dans le même mandat.",
    'extras': [
        ("Câblage Ethernet", "Câblage Ethernet Cat 5e, Cat 6, Cat 6A et Cat 6e pour postes de travail, points d'accès WiFi, caméras, téléphones et appareils d'affaires."),
        ('Câblage coaxial', "Câblage coaxial pour services Internet, distribution spécialisée et équipements commerciaux."),
        ('Racks et armoires réseau', "Racks, gestion des câbles, connexions et remise en ordre dans les locaux techniques MDF et IDF."),
        ('Infrastructure internet', "Prolongements de service, cheminement des arrivées Internet et soutien à la commutation pour les espaces commerciaux."),
        ('Lignes IP et numéros', "Fourniture de lignes IP, de numéros de téléphone et de l'infrastructure téléphonique liée au réseau."),
    ],
    'about_title': "À propos d'Opticable | Mission, qualité et approche clé en main",
    'about_desc': "Découvrez notre mission, notre priorité pour la qualité et le professionnalisme, et notre approche clé en main pour les services en technologie et optimisation.",
    'about_h1': "Nous sommes un partenaire clé en main pour vos besoins en technologie, connectivité, sécurité et optimisation.",
    'about_intro': "Nous sommes une équipe qui conçoit, vend, gère, installe et coordonne des solutions technologiques pour les immeubles commerciaux, les propriétés gérées, les multi-logements et les environnements d'affaires.",
    'about_story': "Notre mission est d'offrir un service fiable, structuré et professionnel, avec un seul point de contact pour simplifier vos projets. Nous priorisons la qualité d'exécution, la clarté des interventions et une approche one-stop qui regroupe vos besoins en sécurité, contrôle d'accès, WiFi, câblage, réseau et optimisation.",
    'about_section_title': 'Notre façon de travailler',
    'about_section_intro': "Les principes qui guident notre exécution, notre service client et notre approche de projet.",
    'about_values': [
        ('Notre mission', "Nous aidons nos clients à avancer avec des solutions technologiques bien pensées, bien installées et plus simples à gérer au quotidien."),
        ('Qualité avant tout', "Nous priorisons une exécution propre, des installations durables et des livraisons qui inspirent confiance."),
        ('Professionnalisme', "Nous travaillons avec rigueur, communication claire et respect des échéanciers, des lieux et des attentes du client."),
        ('Clé en main', "Nous sommes un one-stop pour vos services en technologie et optimisation, afin d'éviter de multiplier les intervenants sur un même projet."),
    ],
    'contact_title': 'Contacter Opticable | Demande de soumission en technologie commerciale',
    'contact_desc': "Contactez Opticable pour vos projets de caméras, de contrôle d'accès, d'intercom, de WiFi, de câblage, de fibre et de réseau partout au Québec, notamment à Montréal, Laval, Longueuil, sur la Rive-Sud, la Rive-Nord et dans les Laurentides.",
    'contact_h1': "Parlez à Opticable de votre prochain projet de caméras, de contrôle d'accès, de WiFi, de câblage ou de réseau.",
    'contact_intro': "Présentez votre type d'immeuble, les systèmes visés et votre échéancier pour obtenir une soumission ou prévoir une visite des lieux partout au Québec.",
    'contact_info_title': 'Coordonnées',
    'contact_panel_title': 'Coordonnées',
    'contact_panel_copy': "Nous desservons tout le Québec, notamment Montréal, Laval, Longueuil, la Rive-Sud, la Rive-Nord, les Laurentides, Lanaudière, la Montérégie, la ville de Québec et les secteurs avoisinants.",
    'form_title': 'Demander une soumission ou une visite des lieux',
    'form_labels': {'name': 'Nom du contact', 'company': 'Entreprise', 'email': 'Courriel', 'phone': 'Téléphone', 'property': 'Type de propriété', 'timeline': 'Échéancier', 'services': 'Services requis', 'notes': 'Notes sur le projet'},
    'form_options': {'property': ['Sélectionnez une option', 'Bureau', 'Immeuble multilogement', 'Multi-logements', 'Condo ou copropriété', 'Immeuble à usage mixte', 'Propriété commerciale', 'Commerce ou hôtellerie', 'Site industriel ou entrepôt', 'Chantier ou site temporaire', 'Projet de développement ou de construction'], 'timeline': ['Sélectionnez une option', 'Besoin immédiat', 'Dans les 30 jours', 'Dans 1 à 3 mois', 'Budget ou planification']},
    'form_services': ['Câblage structuré', 'Fibre optique', 'Infrastructure réseau', 'Caméras de sécurité', "Contrôle d'accès", 'Intercom', 'WiFi commercial', 'Téléphonie IP'],
    'form_placeholder': "Décrivez le type d'immeuble, la portée des travaux, les appareils concernés ou les besoins réseau à prévoir.",
    'contact_cards': [('Renseignements généraux', 'info@opticable.ca'), ('Demandes de soumission', 'soumissions@opticable.ca'), ('Téléphone du bureau', '514-316-7236'), ('Heures', 'Du lundi au vendredi, de 8 h à 17 h; samedi et dimanche, de 10 h à 16 h')],
    'process': [('Évaluation du site', "Nous validons les cheminements, les locaux techniques, les appareils et les contraintes du bâtiment avant le début des travaux."), ('Définition de la portée', "Nous confirmons les quantités, les emplacements, les contraintes d'occupation et les besoins d'intégration."), ('Installation', "Nous installons, terminons, repérons et organisons l'infrastructure selon une séquence propre et coordonnée."), ('Mise en service', "Nous accompagnons les essais, l'activation et la remise pour simplifier le suivi après la livraison.")],
    'industries_title': 'Secteurs desservis | Systèmes technologiques commerciaux | Opticable',
    'industries_desc': "Opticable accompagne les entreprises, immeubles et équipes de projet partout au Québec, notamment à Montréal, Laval, Longueuil, sur la Rive-Sud, la Rive-Nord, dans les Laurentides, Lanaudière, la Montérégie et la ville de Québec.",
    'industries_h1': "Des services d'infrastructure technologique pour les équipes qui possèdent, gèrent, construisent et exploitent les espaces commerciaux.",
    'industries_intro': "Opticable travaille avec les entreprises, les immeubles multilogements, les gestionnaires immobiliers et les équipes de développement qui ont besoin d'immeubles sécurisés et bien connectés.",
    'industries_panel_title': "Des services adaptés aux réalités de chaque immeuble et de chaque site.",
    'industries_panel_copy': "Nous ajustons la sécurité, le WiFi, le câblage et le réseau selon l'occupation, les aires communes, les locataires, l'exploitation et les contraintes du bâtiment.",
    'service_area_eyebrow': 'Territoire desservi',
    'service_area_title': 'Nous desservons les immeubles et projets partout au Québec.',
    'service_area_intro': "Opticable dessert les propriétés commerciales, les immeubles gérés, les multi-logements et les projets partout au Québec, notamment à Montréal, Laval, Longueuil, sur la Rive-Sud, la Rive-Nord, dans les Laurentides, Lanaudière, la Montérégie, la ville de Québec et les régions avoisinantes.",
    'service_area_regions': ['Montréal', 'Laval', 'Longueuil', 'Rive-Sud', 'Rive-Nord', 'Laurentides', 'Lanaudière', 'Montérégie', 'Ville de Québec', 'Et plus encore'],
    'faq_title': "FAQ | WiFi, internet, caméras, contrôle d'accès, intercom et câblage | Opticable",
    'faq_desc': "Questions regroupées par WiFi, internet, caméras, contrôle d'accès, intercom, câblage et valeur ajoutée pour les immeubles.",
    'faq_h1': "Questions fréquentes sur le WiFi, l'internet, les caméras, le contrôle d'accès, l'intercom, le câblage et la valeur ajoutée pour vos immeubles.",
    'faq_intro': "Les questions sont regroupées par service pour comprendre plus vite ce qui est possible, ce qui ajoute de la valeur et ce qui peut rendre un immeuble plus attrayant ou plus économique à exploiter.",
    'faq_panel_title': "Questions classées par service et par valeur ajoutée.",
    'faq_panel_copy': "Consultez les réponses par WiFi, internet, caméras, contrôle d'accès, intercom, câblage et valeur ajoutée pour l'immeuble.",
    'clients': [
        ('Entreprises', "Sécurité, connectivité, WiFi, caméras et communications pour bureaux, commerces, hôtellerie et espaces d'exploitation."),
        ('Immeubles multilogements', "Colonnes montantes, suites, aires communes, systèmes d'entrée sécurisés et technologies destinées aux locataires."),
        ('Gestionnaires immobiliers', "Standards répétables, mises à niveau de sécurité et meilleur soutien dans des immeubles occupés."),
        ('Promoteurs et entrepreneurs', "Coordination technologique pour les aménagements, la livraison des travaux, les systèmes de sécurité et le phasage du projet."),
    ],
    'focus_chips': ['Caméras de sécurité', "Contrôle d'accès", 'WiFi et réseaux sans fil', 'Intercom'],
    'priority_title': 'Services principaux',
    'priority_intro': "Les projets de caméras, de contrôle d'accès, d'intercom et de WiFi passent d'abord.",
    'support_title': 'Infrastructure de soutien',
    'support_intro': "Le câblage, la fibre, les racks et les locaux réseau viennent soutenir les systèmes principaux.",
    'service_label': 'Voir le service',
    'process_title': 'Processus de projet',
    'process_intro': "Une installation technologique commerciale bien exécutée commence avant le premier parcours de câble ou la première fixation d'appareil.",
    'gateway_intro': "Opticable est un entrepreneur en infrastructures technologiques commerciales au service des entreprises, de l'immobilier et du développement. Choisissez votre langue pour continuer.",
    'clients_title': 'Clients servis',
    'clients_intro': 'Les équipes qui possèdent, gèrent ou exploitent des immeubles commerciaux.',
    'overview_intro': "Ce qu'on fait, les avantages et les cas d'usage.",
    'related_intro': 'Services souvent livrés dans le même projet.',
})

industry_cards = {
    'en': [('Businesses', 'Connectivity, security, wireless, and phone systems for offices, retail spaces, hospitality sites, and operational environments.'), ('Multi-tenant buildings', 'Riser work, suite turnover cabling, entry systems, cameras, and common-area infrastructure.'), ('Commercial properties', 'Low-voltage systems that support leasing, occupancy, tenant service, and day-to-day building operations.'), ('Property managers', 'Repeatable building standards, faster support, and cleaner infrastructure across occupied assets.'), ('Developers and contractors', 'Low-voltage coordination for new construction, fit-outs, infrastructure planning, and project delivery.'), ('Industrial and warehouse operators', 'Backbone, WiFi, cameras, access control, and network room work for large operational footprints.')],
    'fr': [('Entreprises', "Connectivité, sécurité, WiFi et téléphonie pour bureaux, commerces, hôtellerie et environnements opérationnels."), ('Immeubles multilogements', "Colonnes montantes, câblage de suites, systèmes d'entrée, caméras et infrastructures d'aires communes."), ('Propriétés commerciales', "Systèmes technologiques qui soutiennent la location, l'occupation, le service aux locataires et l'exploitation courante."), ('Gestionnaires immobiliers', 'Standards répétables, meilleur soutien et infrastructures plus propres sur des actifs occupés.'), ('Promoteurs et entrepreneurs', "Coordination technologique pour construction neuve, aménagements, planification et livraison de projet."), ('Exploitants industriels et d’entrepôts', "Dorsales, WiFi, caméras, contrôle d'accès et locaux réseau pour de grands sites opérationnels.")],
}

faq_groups = {
    'en': [
        ('WiFi', 'Wireless coverage, deployment, and support across different property types.', [
            ('Do you only handle WiFi for offices?', 'No. WiFi can be deployed for offices, retail, common areas, events, multi-unit properties, condo environments, construction sites, and industrial spaces.'),
            ('Can Opticable sell, manage, maintain, install, and cable a WiFi network?', 'Yes. The scope can include product selection, access point cabling, installation, coverage planning, management, and ongoing maintenance.'),
            ('Can you create multiple secure WiFi networks for different uses?', 'Yes. We can segment the wireless environment into separate secure networks for tenants, staff, visitors, operations, cameras, point-of-sale systems, common areas, events, or other specific uses.'),
            ('Can guest WiFi be separated from business or tenant traffic?', 'Yes. Guest access can be isolated from business, tenant, management, camera, and operational traffic through separate wireless networks and segmented network policies.'),
            ('Can WiFi be planned for common areas, outdoor zones, or hard-to-cover spaces?', 'Yes. WiFi projects can be planned for lobbies, corridors, shared amenities, terraces, yards, and other spaces where coverage quality and access experience matter.'),
        ]),
        ('Internet and Network Infrastructure', 'Internet handoffs, network rooms, switching, and site connectivity.', [
            ('Can you extend an internet service handoff to the network room?', 'Yes, but we are not the internet provider. We take the connection delivered at the demarcation point, extend it inside the building, and redistribute it in a segmented and secure way toward network rooms, suites, wireless networks, and operational systems.'),
            ('Can you clean up or reorganize an existing network room?', 'Yes. Existing MDF and IDF rooms can be reorganized, relabeled, and rebuilt so they are easier to support, expand, and troubleshoot.'),
            ('Can one internet service be redistributed to multiple suites or usage groups?', 'Yes. The incoming service can be extended and then distributed across separate suites, tenant spaces, managed areas, and building systems through segmented and secure network design.'),
            ('Can you coordinate the demarcation extension with racks, switching, and patching?', 'Yes. Demarcation work is often coordinated with racks, patch panels, switching, pathways, and room organization so the complete network handoff is cleaner and easier to manage.'),
        ]),
        ('Security Cameras', 'Coverage, recording, remote viewing, and user permissions.', [
            ('Can camera users be limited to specific cameras or zones?', 'Yes. Remote viewing and user permissions can be configured so each person only sees the cameras or areas they are supposed to access.'),
            ('Do you also handle construction cameras and temporary site cameras?', 'Yes. Camera projects can include temporary construction coverage, active-site monitoring, and more permanent surveillance systems.'),
            ('Can cameras be planned for entrances, parking, loading, and common areas?', 'Yes. Camera layouts can be designed around entrances, exits, parking areas, loading zones, corridors, lobbies, and other critical points based on how the property is used.'),
            ('Can recording be kept for different retention periods depending on the project?', 'Yes. Recording settings and storage capacity can be planned around the site, the number of cameras, and the desired retention period.'),
        ]),
        ('Access Control', 'Doors, schedules, remote unlock, and user management.', [
            ('Can doors be opened remotely and scheduled by authorized hours?', 'Yes. Access control systems can be configured for remote unlock, authorized-hour windows, user permissions, and multi-door management.'),
            ('Can access control be coordinated with cameras and intercoms?', 'Yes. Access control is often planned together with cameras, intercoms, and the supporting network so the systems work as one coordinated setup.'),
            ('Can different users or tenant groups have access to different doors?', 'Yes. Permissions can be assigned by person, group, schedule, or area so each user only gets access where and when it is appropriate.'),
            ('Can access control be used for main entries, amenity spaces, and back-of-house doors?', 'Yes. Access control can be deployed across main entrances, shared rooms, service corridors, staff-only areas, and other doors that need controlled entry.'),
        ]),
        ('Intercom', 'Entry communication for lobbies, gates, suites, and controlled access points.', [
            ('Can intercom systems be used for lobbies, gates, suites, and common entries?', 'Yes. Intercom scopes can support visitor communication for building lobbies, controlled doors, gates, suites, and shared access points.'),
            ('Can intercoms be tied to access control and network infrastructure?', 'Yes. Intercom systems can be coordinated with secure entry, cameras, controllers, and the supporting network room infrastructure.'),
            ('Can intercom calls be routed to staff, tenants, or mobile devices?', 'Depending on the selected system, yes. Intercoms can often be set up so calls are answered by reception, building staff, suites, or approved mobile users.'),
            ('Do you offer both audio and video intercom options?', 'Yes. Intercom projects can be planned as audio-only or video-enabled depending on the site, traffic level, and desired visitor experience.'),
        ]),
        ('Structured Cabling', 'The physical backbone behind security, wireless, voice, and business connectivity.', [
            ('What does a structured cabling project usually include?', 'Most scopes include pathways, copper or coaxial runs, terminations, labeling, patch panels, testing, and cleanup of disorganized legacy cabling.'),
            ('Does cabling need to be reviewed before WiFi, cameras, or phone upgrades?', 'In many cases, yes. Reviewing the existing cabling first helps determine what can be reused, what should be replaced, and how to avoid future service issues.'),
            ('What are Cat5e and Cat6 cabling typically used for?', 'Copper categories like Cat5e and Cat6 are commonly used for workstations, phones, access points, cameras, and other connected devices that need dependable Ethernet service inside the property.'),
            ('What is fiber optic cabling typically used for?', 'Fiber is typically used for higher-capacity backbone links, longer distances, risers between floors, and cleaner distribution between suites, telecom rooms, and major equipment areas.'),
            ('What is coaxial cabling typically used for?', 'Coax is still useful for certain internet handoffs, specialty distribution, legacy systems, and service types that are not better served by standard Ethernet cabling.'),
            ('Can existing cabling be relabeled, tested, or cleaned up instead of fully replaced?', 'Yes. In many projects, part of the work involves tracing, relabeling, testing, and reorganizing existing cabling so usable infrastructure can be retained where appropriate.'),
            ('Can structured cabling be installed during renovations, tenant fit-outs, or occupied operations?', 'Yes. Cabling work is often coordinated around renovations, phased fit-outs, and active sites so the infrastructure can be upgraded with less disruption.'),
        ]),
        ('Property Value', 'How these systems improve building appeal, operations, and support costs.', [
            ('How do these services make a property more attractive?', 'Secure entry, reliable WiFi, cleaner cabling, better communication systems, and visible security measures improve the occupant experience and strengthen how a property is perceived.'),
            ('How can these systems be more economical over time?', 'Organized infrastructure reduces emergency fixes, shortens troubleshooting time, and makes tenant turnover, upgrades, and maintenance easier to manage.'),
            ('Why does a one-stop technology approach add value?', 'A single coordinated partner reduces gaps between trades, simplifies communication, and helps projects stay cleaner, faster, and easier to support after delivery.'),
            ('Does including internet and WiFi make a rental more attractive?', 'Yes. When internet access and WiFi are already available, commercial spaces and residential units are often easier to market because the service feels more ready to occupy and more convenient from day one.'),
            ('Can property value improve when these services are included in the lease?', 'Yes. When connectivity and building technology are built into the lease, the offer can become more competitive, support stronger retention, and increase the perceived economic value of the space.'),
        ]),
    ],
    'fr': [
        ('WiFi', 'Couverture, déploiement et soutien des réseaux sans fil selon le type de site.', [
            ('Faites-vous le WiFi seulement pour des bureaux ?', "Non. Nous faisons aussi le WiFi pour les commerces, les aires communes, les événements, les multi-logements, les copropriétés, les chantiers de construction et les sites industriels."),
            ("Faites-vous la vente, la gestion, la maintenance, l'installation et le câblage WiFi ?", "Oui. Le service peut inclure la vente d'équipement, le câblage des points d'accès, l'installation, la planification de couverture, la gestion et la maintenance continue du réseau sans fil."),
            ('Pouvez-vous créer plusieurs réseaux WiFi sécurisés pour des usages différents ?', "Oui. Nous pouvons créer plusieurs réseaux sécurisés et segmentés selon les usages: locataires, personnel, visiteurs, opérations, caméras, points de vente, aires communes, événements ou autres besoins précis du bâtiment."),
            ('Pouvez-vous séparer un WiFi invité du réseau des locataires ou des opérations ?', "Oui. Le WiFi invité peut être isolé du trafic des locataires, des bureaux, de la gestion, des caméras et des opérations grâce à des réseaux distincts et des règles de segmentation adaptées."),
            ('Pouvez-vous planifier le WiFi pour les aires communes, l’extérieur ou les zones difficiles ?', "Oui. Le WiFi peut être planifié pour les halls, corridors, terrasses, cours, salles communes et autres espaces où la qualité de couverture et l’expérience utilisateur comptent."),
        ]),
        ('Internet et réseau', "Arrivées internet, locaux techniques, commutation et infrastructure réseau.", [
            ("Pouvez-vous prolonger l'arrivée Internet jusqu'au local réseau ?", "Oui, mais nous ne sommes pas le fournisseur internet. Nous prenons la connexion livrée au point de démarcation, nous la prolongeons dans l'immeuble, puis nous la redistribuons de façon segmentée et sécurisée vers les locaux réseau, les suites, les réseaux WiFi et les autres usages du bâtiment."),
            ('Pouvez-vous remettre en ordre un local réseau existant ?', "Oui. Nous pouvons réorganiser, repérer et nettoyer un MDF ou un IDF pour qu’il soit plus clair, plus fiable et plus simple à soutenir par la suite."),
            ('Pouvez-vous redistribuer une même arrivée Internet vers plusieurs suites ou usages ?', "Oui. Une même arrivée peut être prolongée puis redistribuée vers plusieurs suites, espaces locatifs, aires gérées et systèmes du bâtiment avec une segmentation claire et sécurisée."),
            ('Pouvez-vous coordonner le point de démarcation avec les racks, les commutateurs et les raccordements ?', "Oui. Le prolongement du point de démarcation peut être coordonné avec les racks, les panneaux de raccordement, la commutation, les cheminements et l’organisation du local réseau pour une installation plus propre."),
        ]),
        ('Caméras de sécurité', "Surveillance, enregistrement, visionnement à distance et gestion des accès utilisateurs.", [
            ('Peut-on voir les caméras à distance et limiter l’accès selon les utilisateurs ?', "Oui. Le visionnement à distance peut être configuré avec des permissions pour limiter certaines personnes à certaines caméras ou à certaines zones seulement."),
            ('Offrez-vous aussi des caméras de chantier et des caméras temporaires ?', "Oui. Nous pouvons installer des caméras de chantier, des caméras temporaires et des systèmes plus permanents selon la durée et le niveau de surveillance recherchés."),
            ('Pouvez-vous planifier des caméras pour les entrées, stationnements, quais et aires communes ?', "Oui. L’implantation peut être pensée selon les entrées, sorties, stationnements, quais de chargement, corridors, halls et autres points importants selon l’usage réel du site."),
            ('Peut-on prévoir différentes durées de conservation pour les enregistrements ?', "Oui. Les paramètres d’enregistrement et la capacité de stockage peuvent être planifiés selon le nombre de caméras, le niveau d’activité du site et la durée de conservation souhaitée."),
        ]),
        ('Contrôle d’accès', "Portes, horaires autorisés, ouverture à distance et gestion des accès.", [
            ('Peut-on ouvrir des portes à distance et contrôler les heures autorisées ?', "Oui. Nous pouvons configurer l’ouverture à distance, les heures autorisées, les utilisateurs, les groupes et les zones selon vos besoins d’exploitation."),
            ('Pouvez-vous coordonner le contrôle d’accès avec les caméras et les intercoms ?', "Oui. Le contrôle d’accès peut être planifié avec les caméras, les intercoms et l’infrastructure réseau pour offrir une gestion plus cohérente des entrées."),
            ('Peut-on donner des accès différents selon les utilisateurs, locataires ou équipes ?', "Oui. Les permissions peuvent être attribuées selon la personne, le groupe, l’horaire ou la zone afin que chacun accède seulement aux portes qui le concernent."),
            ('Le contrôle d’accès peut-il servir aux entrées principales, portes communes et zones de service ?', "Oui. Le contrôle d’accès peut être déployé sur les entrées principales, salles communes, corridors de service, locaux techniques et autres portes qui demandent une gestion contrôlée."),
        ]),
        ('Intercom', "Communication aux entrées, halls, suites, portails et accès contrôlés.", [
            ('L’intercom convient-il aux halls, portails, suites et aires communes ?', "Oui. Les systèmes d’intercom peuvent servir aux halls d’entrée, aux portails, aux suites, aux aires communes et aux accès visiteurs contrôlés."),
            ('L’intercom peut-il être combiné au contrôle d’accès et au réseau ?', "Oui. L’intercom s’intègre souvent au contrôle d’accès, aux caméras et au réseau afin de mieux gérer l’entrée, la communication et les permissions."),
            ('Les appels d’intercom peuvent-ils être dirigés vers le personnel, les locataires ou un mobile ?', "Selon le système retenu, oui. Les appels peuvent souvent être dirigés vers une réception, une équipe de gestion, une suite ou certains utilisateurs mobiles autorisés."),
            ('Offrez-vous des intercoms audio et vidéo ?', "Oui. Les projets d’intercom peuvent être prévus en version audio seulement ou en version vidéo selon le type d’immeuble, le volume de passage et l’expérience recherchée."),
        ]),
        ('Câblage structuré', "La base physique qui soutient le WiFi, les caméras, la téléphonie et les autres systèmes.", [
            ('Que comprend habituellement un projet de câblage structuré ?', "La plupart des projets incluent les cheminements, le câble cuivre ou coaxial, les terminaisons, le repérage, les panneaux de raccordement, les essais et la remise en ordre de l’installation."),
            ('Le câblage doit-il être évalué avant un projet WiFi, caméras ou téléphonie ?', "Souvent oui. Vérifier le câblage existant permet de voir ce qui peut être réutilisé, ce qui doit être remplacé et comment éviter des problèmes ou des coûts imprévus plus tard."),
            ('À quoi servent généralement les câbles cuivre Cat5e et Cat6 ?', "Les câbles cuivre Cat5e et Cat6 servent surtout à relier les postes de travail, téléphones IP, points d'accès WiFi, caméras, équipements de contrôle d'accès et autres appareils réseau qui ont besoin d'une connexion Ethernet fiable dans l'immeuble."),
            ('À quoi sert généralement la fibre optique ?', "La fibre sert surtout aux liaisons principales, aux longues distances, aux colonnes montantes entre étages et aux liens à plus haute capacité entre les suites, les locaux techniques et les équipements majeurs."),
            ('À quoi sert généralement le coaxial ?', "Le coaxial reste utile pour certains services Internet, certaines distributions spécialisées et certains équipements ou environnements où l'on ne remplace pas tout par du cuivre Ethernet."),
            ('Peut-on réidentifier, tester ou remettre en ordre un câblage existant au lieu de tout remplacer ?', "Oui. Dans plusieurs projets, une partie du travail consiste à retracer, réidentifier, tester et réorganiser le câblage existant pour conserver ce qui est encore bon lorsque c’est pertinent."),
            ('Pouvez-vous installer le câblage structuré pendant des rénovations, aménagements ou opérations actives ?', "Oui. Le câblage est souvent coordonné pendant des rénovations, des aménagements locatifs et des sites occupés afin d’améliorer l’infrastructure avec moins d’impact sur les opérations."),
        ]),
        ('Valeur ajoutée pour l’immeuble', "Comment ces services peuvent rendre un immeuble plus attrayant, plus simple à gérer et plus économique à exploiter.", [
            ('Comment ces services rendent-ils un immeuble plus attrayant ?', "Un immeuble mieux sécurisé, mieux connecté et mieux organisé inspire davantage confiance aux locataires, occupants, visiteurs et équipes de gestion."),
            ('Comment ces services peuvent-ils être plus économiques à long terme ?', "Une infrastructure bien pensée réduit les appels d’urgence, accélère le dépannage, simplifie les changements locatifs et évite plusieurs reprises coûteuses."),
            ('Pourquoi une approche clé en main ajoute-t-elle de la valeur ?', "Un seul partenaire pour coordonner la technologie réduit les allers-retours, limite les oublis entre intervenants et aide à livrer un résultat plus propre, plus fluide et plus facile à maintenir."),
            ('La location devient-elle plus attirante quand Internet et le WiFi sont inclus ?', "Oui. Un commerce ou un logement devient souvent plus attrayant quand l'Internet et le WiFi sont déjà en place, parce que l'espace paraît plus prêt à utiliser, plus moderne et plus pratique dès l'entrée."),
            ('La valeur économique peut-elle augmenter si ces services sont inclus dans le bail ?', "Oui. Lorsque l'Internet, le WiFi ou certains services technologiques sont inclus dans le bail, l'offre peut devenir plus compétitive, soutenir une meilleure rétention et augmenter la valeur économique perçue de l'espace."),
        ]),
    ],
}

home_visuals = {
    'en': {
        'eyebrow': 'Installed systems',
        'title': '',
        'top_title': 'Commercial properties and connected building environments',
        'top_copy': 'Technology planning and installation for buildings that need security, connectivity, and reliable day-to-day operation.',
        'top_alt': 'Commercial building exterior with a modern connected technology environment',
        'main_title': 'Network racks, patch panels, and structured cabling',
        'main_copy': 'Clean rack organization, patch panels, backbone, and supporting network infrastructure for commercial properties.',
        'main_alt': 'Commercial network rack with organized structured cabling',
    },
    'fr': {
        'eyebrow': 'Systèmes installés',
        'title': '',
        'top_title': 'Immeubles commerciaux et environnements technologiques connectés',
        'top_copy': "Planification et installation technologique pour les bâtiments qui ont besoin de sécurité, de connectivité et d'une exploitation fiable au quotidien.",
        'top_alt': 'Immeuble commercial avec environnement technologique moderne et connecté',
        'main_title': 'Racks réseau, patch panels et câblage structuré',
        'main_copy': "Organisation propre des racks, des patch panels, du backbone et de l'infrastructure réseau pour les immeubles commerciaux.",
        'main_alt': 'Baie réseau commerciale avec câblage structuré bien organisé',
    },
}
services_page_chip_keys = (
    'structured-cabling',
    'commercial-wifi-installation',
    'network-infrastructure',
    'security-camera-systems',
    'access-control-systems',
    'intercom-systems',
    'fiber-optic-installation',
    'ip-phone-systems',
)
service_panel_visuals = {
    'security-camera-systems': {
        'en': {'src': SERVICE_CAMERA_URL, 'alt': 'Dual bullet commercial security cameras', 'width': SERVICE_CAMERA_WIDTH, 'height': SERVICE_CAMERA_HEIGHT, 'caption': 'Commercial security camera equipment'},
        'fr': {'src': SERVICE_CAMERA_URL, 'alt': 'Caméras de sécurité commerciales à double module', 'width': SERVICE_CAMERA_WIDTH, 'height': SERVICE_CAMERA_HEIGHT, 'caption': 'Équipement de caméras de sécurité commerciales'},
    },
    'intercom-systems': {
        'en': {'src': SERVICE_INTERCOM_URL, 'alt': 'Commercial intercom door station installed for building entry', 'width': SERVICE_INTERCOM_WIDTH, 'height': SERVICE_INTERCOM_HEIGHT, 'caption': 'Commercial entry intercom'},
        'fr': {'src': SERVICE_INTERCOM_URL, 'alt': 'Intercom commercial installé pour entrée d immeuble', 'width': SERVICE_INTERCOM_WIDTH, 'height': SERVICE_INTERCOM_HEIGHT, 'caption': 'Intercom commercial d entrée'},
    },
    'structured-cabling': {
        'en': {'src': SERVICE_CABLING_URL, 'alt': 'Patch panel and switch layout for structured cabling', 'width': SERVICE_CABLING_WIDTH, 'height': SERVICE_CABLING_HEIGHT, 'caption': 'Structured cabling and patch panel layout'},
        'fr': {'src': SERVICE_CABLING_URL, 'alt': 'Patch panels et commutateurs pour câblage structuré', 'width': SERVICE_CABLING_WIDTH, 'height': SERVICE_CABLING_HEIGHT, 'caption': 'Câblage structuré et organisation des patch panels'},
    },
    'fiber-optic-installation': {
        'en': {'src': SERVICE_FIBER_URL, 'alt': 'Fiber optic cable bundle prepared for commercial installation', 'width': SERVICE_FIBER_WIDTH, 'height': SERVICE_FIBER_HEIGHT, 'caption': 'Fiber optic cabling for commercial connectivity'},
        'fr': {'src': SERVICE_FIBER_URL, 'alt': 'Câble de fibre optique préparé pour installation commerciale', 'width': SERVICE_FIBER_WIDTH, 'height': SERVICE_FIBER_HEIGHT, 'caption': 'Fibre optique pour connectivité commerciale'},
    },
    'network-infrastructure': {
        'en': {'src': SERVICE_INFRASTRUCTURE_URL, 'alt': 'Commercial network infrastructure with organized rack and switching layout', 'width': SERVICE_INFRASTRUCTURE_WIDTH, 'height': SERVICE_INFRASTRUCTURE_HEIGHT, 'caption': 'Commercial network infrastructure and rack layout'},
        'fr': {'src': SERVICE_INFRASTRUCTURE_URL, 'alt': 'Infrastructure réseau commerciale avec rack et commutation organisés', 'width': SERVICE_INFRASTRUCTURE_WIDTH, 'height': SERVICE_INFRASTRUCTURE_HEIGHT, 'caption': 'Infrastructure réseau commerciale et organisation de rack'},
    },
    'access-control-systems': {
        'en': {'src': SERVICE_ACCESS_URL, 'alt': 'Commercial access control reader and secure door hardware', 'width': SERVICE_ACCESS_WIDTH, 'height': SERVICE_ACCESS_HEIGHT, 'caption': 'Commercial access reader and secure entry hardware'},
        'fr': {'src': SERVICE_ACCESS_URL, 'alt': 'Lecteur de contrôle d accès commercial et quincaillerie sécurisée', 'width': SERVICE_ACCESS_WIDTH, 'height': SERVICE_ACCESS_HEIGHT, 'caption': 'Lecteur de contrôle d accès et entrée sécurisée'},
    },
    'commercial-wifi-installation': {
        'en': {'src': SERVICE_WIFI_URL, 'alt': 'Commercial WiFi access point installed on ceiling', 'width': SERVICE_WIFI_WIDTH, 'height': SERVICE_WIFI_HEIGHT, 'caption': 'Commercial WiFi access point', 'class_name': 'service-panel-image-wifi'},
        'fr': {'src': SERVICE_WIFI_URL, 'alt': 'Point d accès WiFi commercial installé au plafond', 'width': SERVICE_WIFI_WIDTH, 'height': SERVICE_WIFI_HEIGHT, 'caption': 'Point d accès WiFi commercial', 'class_name': 'service-panel-image-wifi'},
    },
    'ip-phone-systems': {
        'en': {'src': SERVICE_VOIP_URL, 'alt': 'Business VoIP phone setup for office communication', 'width': SERVICE_VOIP_WIDTH, 'height': SERVICE_VOIP_HEIGHT, 'caption': 'Business VoIP and IP phone system'},
        'fr': {'src': SERVICE_VOIP_URL, 'alt': 'Téléphonie VoIP d affaires pour communication de bureau', 'width': SERVICE_VOIP_WIDTH, 'height': SERVICE_VOIP_HEIGHT, 'caption': 'Téléphonie IP et système VoIP d affaires'},
    },
}
services = {
    'structured-cabling': {
        'en': {'slug': 'structured-cabling', 'name': 'Structured Cabling', 'title': 'Structured Cabling Installation for Commercial Properties | Opticable', 'desc': 'Structured cabling installation for offices, multi-tenant buildings, and commercial properties, including Ethernet, coaxial, labeling, and pathway work.', 'hero': 'Structured cabling installation for offices, buildings, and commercial properties.', 'intro': 'Opticable installs the physical cabling foundation behind business connectivity, tenant systems, and low-voltage devices. Structured cabling scopes can include Ethernet cable installation, coaxial cable installation, pathway organization, terminations, and labeling that makes future support easier.', 'summary': 'Copper, Ethernet, coaxial, labeling, patching, and clean cable organization for commercial spaces.', 'includes': ['Cat5e, Cat6, and Cat6A runs for workstations, WiFi access points, cameras, phones, and business devices', 'Coaxial cabling for broadband handoffs, specialty distribution, and related commercial equipment', 'Patch panels, terminations, pathway hardware, labeling, testing, and cleanup of disorganized legacy cable'], 'benefits': ['Cleaner cable plants and easier service access', 'Faster troubleshooting after turnover', 'Better room for expansion, moves, and added devices'], 'cases': ['Tenant improvements and office expansions', 'Retail and hospitality connectivity upgrades', 'Legacy cleanup before wireless or security deployment'], 'industries': ['Business offices', 'Multi-tenant buildings', 'Retail and mixed-use properties'], 'related': ['network-infrastructure', 'fiber-optic-installation', 'commercial-wifi-installation']},
'fr': {'slug': 'cablage-structure', 'name': 'Cablage structure', 'title': 'Installation de cablage structure pour proprietes commerciales | Opticable', 'desc': 'Installation de cablage structure pour bureaux, immeubles multilogements et proprietes commerciales, incluant Ethernet, coaxial, reperage et cheminements.', 'hero': 'Installation de cablage structure pour bureaux, immeubles et proprietes commerciales.', 'intro': 'Opticable installe la fondation physique derriere la connectivite d affaires, les systemes des locataires et les appareils basse tension. La portee peut inclure l installation de cables Ethernet, le cablage coaxial, l organisation des chemins, les terminaisons et le reperage qui facilitent le soutien futur.', 'summary': 'Cuivre, Ethernet, coaxial, reperage, raccordement et organisation propre du cablage pour les espaces commerciaux.', 'includes': ['Parcours Cat5e, Cat6 et Cat6A pour postes, points d acces WiFi, cameras, telephones et appareils d affaires', 'Cablage coaxial pour handoffs internet, distribution specialisee et equipements commerciaux relies', 'Panneaux de raccordement, terminaisons, accessoires de cheminement, reperage, essais et nettoyage des vieux cablages'], 'benefits': ['Infrastructure plus propre et plus facile a servir', 'Depannage plus rapide apres la remise', 'Plus de marge pour les ajouts, deplacements et nouveaux appareils'], 'cases': ['Amenagements locatifs et agrandissements de bureaux', 'Mises a niveau de connectivite pour commerces et hotellerie', 'Nettoyage avant le deploiement du WiFi ou de la securite'], 'industries': ['Bureaux d entreprise', 'Immeubles multilogements', 'Proprietes de commerce et a usage mixte'], 'related': ['network-infrastructure', 'fiber-optic-installation', 'commercial-wifi-installation']},
    },
    'fiber-optic-installation': {
        'en': {'slug': 'fiber-optic-installation', 'name': 'Fiber Optic Installation', 'title': 'Fiber Optic Cable Installation for Commercial Buildings | Opticable', 'desc': 'Fiber optic cable installation for commercial buildings, backbones, risers, internet handoffs, and high-capacity connectivity.', 'hero': 'Fiber optic cabling for backbone capacity, risers, and business-grade connectivity.', 'intro': 'Opticable installs fiber optic cabling for commercial environments that need reliable backbone distribution, ISP handoff extensions, or higher-capacity links between floors, suites, and network rooms.', 'summary': 'Fiber backbones, risers, handoff extensions, and high-capacity links for commercial properties.', 'includes': ['Fiber backbone cabling between MDF, IDF, suites, and major equipment locations', 'Provider handoff extensions and demarc-to-network-room routing', 'Fiber terminations, patching, pathway organization, and rack-side coordination'], 'benefits': ['Higher-capacity distribution for future growth', 'Dependable long-distance links inside larger properties', 'Better coordination with racks, switching, and room design'], 'cases': ['Multi-floor office and mixed-use properties', 'Internet service handoff extensions to network rooms', 'Backbone refreshes during tenant or landlord improvements'], 'industries': ['Commercial office buildings', 'Multi-tenant properties', 'Industrial and warehouse sites'], 'related': ['network-infrastructure', 'structured-cabling', 'security-camera-systems']},
'fr': {'slug': 'installation-fibre-optique', 'name': 'Installation de fibre optique', 'title': 'Fibre optique pour immeubles commerciaux | Opticable', 'desc': 'Installation de fibre optique pour immeubles commerciaux, backbones, colonnes montantes, handoffs internet et connectivite a haute capacite.', 'hero': 'Fibre optique pour backbones, colonnes montantes et connectivite d affaires a haute capacite.', 'intro': 'Opticable installe la fibre optique pour les environnements commerciaux qui exigent un backbone fiable, des extensions de handoff fournisseur ou des liens a plus forte capacite entre etages, suites et salles reseau.', 'summary': 'Backbones fibre, colonnes montantes, extensions de handoff et liens a haute capacite pour proprietes commerciales.', 'includes': ['Cablage backbone fibre entre MDF, IDF, suites et points d equipement', 'Extensions de handoff fournisseur et chemin entre le point de demarcation et la salle reseau', 'Terminaisons fibre, raccordement, organisation des chemins et coordination cote baie'], 'benefits': ['Distribution a plus forte capacite pour la croissance future', 'Liens fiables sur de plus longues distances dans les grands sites', 'Meilleure coordination avec les baies, la commutation et les salles techniques'], 'cases': ['Immeubles de bureaux et proprietes mixtes sur plusieurs etages', 'Extensions du handoff du fournisseur internet vers la salle reseau', 'Renouvellement de backbone lors d ameliorations locatives ou proprietaires'], 'industries': ['Immeubles de bureaux commerciaux', 'Proprietes multilogements', 'Sites industriels et entrepots'], 'related': ['network-infrastructure', 'structured-cabling', 'security-camera-systems']},
    },
    'network-infrastructure': {
        'en': {'slug': 'network-infrastructure', 'name': 'Network Infrastructure', 'title': 'Commercial Network Infrastructure and Server Rack Installation | Opticable', 'desc': 'Commercial network infrastructure services including server rack installation, network room build-outs, switching support, and internet infrastructure deployment.', 'hero': 'Network infrastructure, server rack installation, and room build-outs for commercial environments.', 'intro': 'Opticable supports the physical network infrastructure behind business connectivity, equipment rooms, and internet service deployment. Projects can include server rack installation, patching, switch connectivity, demarc extensions, and cleanup of difficult legacy rooms.', 'summary': 'Server racks, network rooms, handoff routing, patching, switching support, and infrastructure cleanup.', 'includes': ['Server rack and cabinet installation with cable management and organized terminations', 'Patch panels, uplink routing, switch connectivity, and demarc-to-rack pathway planning', 'Internet infrastructure deployment and cleanup of crowded or unlabeled network rooms'], 'benefits': ['Better room serviceability after turnover', 'Cleaner handoff between wireless, security, voice, and tenant systems', 'Less rework during future upgrades and expansion'], 'cases': ['New office or retail suite network room setup', 'Demarc extensions and backbone routing for managed buildings', 'Legacy MDF and IDF cleanup before expansion'], 'industries': ['Business offices', 'Property management portfolios', 'Retail and hospitality properties'], 'related': ['structured-cabling', 'fiber-optic-installation', 'ip-phone-systems']},
'fr': {'slug': 'infrastructure-reseau', 'name': 'Infrastructure reseau', 'title': 'Infrastructure reseau commerciale et installation de baies serveurs | Opticable', 'desc': 'Services d infrastructure reseau commerciale incluant l installation de baies serveurs, l amenagement de salles reseau, le soutien a la commutation et le deploiement d infrastructures internet.', 'hero': 'Infrastructure reseau, installation de baies serveurs et amenagement de salles techniques pour environnements commerciaux.', 'intro': 'Opticable soutient l infrastructure physique derriere la connectivite d affaires, les locaux techniques et le deploiement de services internet. Les projets peuvent inclure l installation de baies serveurs, le raccordement, la connectivite des commutateurs, les extensions de demarcation et la remise en ordre de salles difficiles a entretenir.', 'summary': 'Baies serveurs, salles reseau, routage des handoffs, raccordement, soutien aux commutateurs et remise en ordre des infrastructures.', 'includes': ['Installation de baies et cabinets avec gestion du cablage et terminaisons ordonnees', 'Panneaux de raccordement, routage des uplinks, connectivite des commutateurs et chemin entre la demarcation et la baie', 'Deploiement d infrastructures internet et nettoyage de salles reseau surchargees ou non etiquetees'], 'benefits': ['Salles plus faciles a soutenir apres la remise', 'Transition plus propre entre WiFi, securite, voix et systemes des locataires', 'Moins de reprises lors des mises a niveau et des expansions futures'], 'cases': ['Mise en place de salles reseau pour nouveaux bureaux ou commerces', 'Extensions de demarcation et routage backbone pour immeubles geres', 'Nettoyage de MDF et IDF existants avant expansion'], 'industries': ['Bureaux d entreprise', 'Portefeuilles de gestion immobiliere', 'Commerces et hotellerie'], 'related': ['structured-cabling', 'fiber-optic-installation', 'ip-phone-systems']},
    },
    'managed-it-services': {
        'en': {'slug': 'it-services-and-support', 'name': 'IT Services', 'title': 'IT Services and Device Management | Opticable', 'desc': 'IT support, device management, network maintenance, and technical support for businesses and commercial properties in Quebec.', 'hero': 'IT services and device management for businesses and commercial properties', 'intro': 'Opticable provides IT support, device management, and practical maintenance after installation so business technology environments keep running without interruption.', 'summary': 'Device management, network support, maintenance, and technical support after installation.', 'includes': ['Device inventory, updates, replacements, and lifecycle tracking for workstations and network equipment', 'Technical support for installed systems, including network, WiFi, cameras, and access-control environments', 'Preventive maintenance, configuration updates, and day-to-day administration for business technology environments'], 'benefits': ['Clearer ownership of the installed environment after deployment', 'Faster response when systems need changes, support, or maintenance', 'A more consistent technical standard across active properties and business sites'], 'cases': ['Clients that want to outsource support for their technology environment', 'Property teams that need recurring follow-up across multiple locations', 'Organizations that have systems in place but limited internal IT capacity'], 'industries': ['Business offices', 'Commercial properties', 'Property management portfolios'], 'related': ['network-infrastructure', 'commercial-wifi-installation', 'ip-phone-systems']},
        'fr': {'slug': 'services-informatiques', 'name': 'Services informatiques', 'title': 'Services informatiques et gestion de parc | Opticable', 'desc': "Soutien informatique, gestion de parc et maintenance réseau pour entreprises et immeubles commerciaux au Québec. Montréal, Laval, Longueuil et partout au Québec.", 'hero': 'Services informatiques et gestion de parc pour entreprises et immeubles commerciaux', 'intro': "Opticable assure le soutien informatique, la gestion de parc et la maintenance des environnements technologiques après l'installation. On reste disponibles pour que vos systèmes fonctionnent sans interruption.", 'summary': "Gestion de parc, soutien réseau, maintenance et support technique pour vos environnements après l'installation.", 'includes': ['Gestion de parc informatique, inventaire, mises à jour, remplacement et suivi des équipements', 'Soutien technique sur les systèmes installés, incluant réseau, WiFi, caméras et contrôle d’accès', 'Maintenance préventive, administration des systèmes et support utilisateur continu'], 'benefits': ['Un interlocuteur unique pour la gestion courante de votre environnement technologique', 'Des systèmes mieux suivis après la mise en service', 'Moins de friction quand il faut maintenir, ajuster ou faire évoluer les installations'], 'cases': ["Entreprises qui veulent externaliser la gestion de leur environnement technologique", 'Gestionnaires immobiliers qui ont besoin d’un suivi régulier sur plusieurs immeubles', 'Organisations qui ont des systèmes en place mais plus de ressources internes pour les gérer'], 'industries': ['Entreprises', 'Immeubles commerciaux', 'Portefeuilles immobiliers'], 'related': ['network-infrastructure', 'commercial-wifi-installation', 'ip-phone-systems']},
    },
    'security-camera-systems': {
        'en': {'slug': 'security-camera-systems', 'name': 'Security Camera Systems', 'title': 'Commercial Security Camera System Installation | Opticable', 'desc': 'Commercial security camera system installation with cabling, device connectivity, and network coordination for managed properties and businesses.', 'hero': 'Security camera infrastructure and installation for businesses, buildings, and managed properties.', 'intro': 'Opticable installs the low-voltage and network foundation behind commercial security camera systems. Camera projects are coordinated with cabling, switching, storage locations, and active building conditions.', 'summary': 'Commercial camera cabling, device connectivity, PoE support, and infrastructure planning.', 'includes': ['Cabling and terminations for interior and exterior camera positions', 'PoE-capable connectivity planning with switching and rack coordination', 'Routing to network rooms, storage equipment, or building-wide surveillance infrastructure'], 'benefits': ['More reliable coverage and device connectivity', 'Cleaner integration with the broader network core', 'Easier future expansion for added coverage areas'], 'cases': ['Retail surveillance upgrades', 'Common-area and perimeter camera additions', 'Warehouse and operational monitoring coverage'], 'industries': ['Retail and hospitality', 'Commercial office properties', 'Industrial and warehouse sites'], 'related': ['access-control-systems', 'network-infrastructure', 'structured-cabling']},
        'fr': {'slug': 'systemes-cameras-securite', 'name': 'Systemes de cameras de securite', 'title': 'Installation de systemes de cameras de securite commerciales | Opticable', 'desc': 'Installation de systemes de cameras de securite commerciales avec cablage, connectivite des appareils et coordination reseau pour entreprises et proprietes gerees.', 'hero': 'Infrastructure et installation de cameras de securite pour entreprises, immeubles et proprietes gerees.', 'intro': 'Opticable installe la fondation basse tension et reseau derriere les systemes de cameras de securite commerciales. Les projets sont coordonnes avec le cablage, la commutation, les emplacements de stockage et les conditions des immeubles occupes.', 'summary': 'Cablage de cameras commerciales, connectivite des appareils, soutien PoE et planification d infrastructure.', 'includes': ['Cablage et terminaisons pour positions de cameras interieures et exterieures', 'Planification de la connectivite PoE avec coordination des commutateurs et des baies', 'Routage vers les salles reseau, les equipements de stockage ou l infrastructure de surveillance du batiment'], 'benefits': ['Couverture plus fiable et meilleure connectivite des appareils', 'Integration plus propre avec le coeur du reseau', 'Expansion future simplifiee pour de nouvelles zones de couverture'], 'cases': ['Mises a niveau de surveillance pour commerces', 'Ajout de cameras dans les aires communes et les perimetres', 'Couverture de surveillance dans les entrepots et sites operationnels'], 'industries': ['Commerce et hotellerie', 'Proprietes de bureaux commerciaux', 'Sites industriels et entrepots'], 'related': ['access-control-systems', 'network-infrastructure', 'structured-cabling']},
    },
    'access-control-systems': {
        'en': {'slug': 'access-control-systems', 'name': 'Access Control Systems', 'title': 'Commercial Access Control System Installation | Opticable', 'desc': 'Commercial access control system installation with low-voltage wiring, controller support, and entry planning for business and managed properties.', 'hero': 'Access control system installation for commercial entries, tenant spaces, and managed buildings.', 'intro': 'Opticable installs the low-voltage infrastructure required for commercial access control systems, including reader locations, panel support, door hardware coordination, and network connectivity for secure operations.', 'summary': 'Door reader wiring, panel support, network connectivity, and secure entry infrastructure.', 'includes': ['Low-voltage cabling for readers, electrified hardware, panels, and related door components', 'Controller cabinet support, network connectivity, and pathway coordination', 'Integration planning with intercoms, cameras, and broader security infrastructure'], 'benefits': ['Better entry coordination with building operations', 'Cleaner multi-system integration', 'More supportable installations for future service work'], 'cases': ['Main-entry upgrades for offices and mixed-use properties', 'Suite and common-area access control', 'Restricted-area entry control in operational spaces'], 'industries': ['Office and commercial properties', 'Multi-tenant buildings', 'Industrial facilities'], 'related': ['intercom-systems', 'security-camera-systems', 'network-infrastructure']},
        'fr': {'slug': 'systemes-controle-acces', 'name': 'Systemes de controle d acces', 'title': 'Installation de systemes de controle d acces commerciaux | Opticable', 'desc': 'Installation de systemes commerciaux de controle d acces avec cablage basse tension, soutien des panneaux et planification des entrees pour entreprises et proprietes gerees.', 'hero': 'Installation de systemes de controle d acces pour entrees commerciales, espaces locatifs et immeubles geres.', 'intro': 'Opticable installe l infrastructure basse tension requise pour les systemes commerciaux de controle d acces, incluant les emplacements de lecteurs, le soutien des panneaux, la coordination du materiel de porte et la connectivite reseau pour une exploitation securitaire.', 'summary': 'Cablage de lecteurs, soutien des panneaux, connectivite reseau et infrastructure d entree securisee.', 'includes': ['Cablage basse tension pour lecteurs, materiel electrifie, panneaux et composantes de porte', 'Soutien des cabinets de controle, connectivite reseau et coordination des cheminements', 'Planification de l integration avec les interphones, les cameras et l infrastructure de securite'], 'benefits': ['Coordination d entree plus solide avec l exploitation du batiment', 'Integration multi-systeme plus propre', 'Installations plus faciles a soutenir lors des interventions futures'], 'cases': ['Mises a niveau d entree principale pour bureaux et proprietes mixtes', 'Controle d acces des suites et aires communes', 'Controle des entrees dans les entrepots et zones restreintes'], 'industries': ['Bureaux et proprietes commerciales', 'Immeubles multilogements', 'Installations industrielles'], 'related': ['intercom-systems', 'security-camera-systems', 'network-infrastructure']},
    },
    'intercom-systems': {
        'en': {'slug': 'intercom-systems', 'name': 'Intercom Systems', 'title': 'Commercial Intercom System Installation | Opticable', 'desc': 'Commercial intercom system installation for multi-tenant buildings, office entries, visitor communication, and secure access points.', 'hero': 'Intercom system installation for building entry, visitor communication, and tenant access workflows.', 'intro': 'Opticable installs intercom infrastructure for commercial properties and multi-tenant environments that need clear communication at entry points, gates, lobbies, and controlled access areas.', 'summary': 'Building entry, gate, and tenant communication systems coordinated with access and network infrastructure.', 'includes': ['Lobby, entry, gate, and suite-side intercom cabling and device support', 'Integration planning with access control, cameras, and tenant communication requirements', 'Network and room coordination for intercom controllers or supporting equipment'], 'benefits': ['Clearer visitor communication at entries', 'Better integration with tenant and access workflows', 'Simpler future changes for added suites or entry points'], 'cases': ['Multi-tenant office and mixed-use entry systems', 'Property lobby communication upgrades', 'Gate and controlled-entry intercom additions'], 'industries': ['Multi-tenant commercial buildings', 'Property management portfolios', 'Mixed-use developments'], 'related': ['access-control-systems', 'security-camera-systems', 'structured-cabling']},
        'fr': {'slug': 'systemes-interphone', 'name': 'Systemes d interphone', 'title': 'Installation de systemes d interphone commerciaux | Opticable', 'desc': 'Installation de systemes d interphone commerciaux pour immeubles multilogements, entrees de bureaux, communication des visiteurs et points d acces securises.', 'hero': 'Installation d interphones pour l entree des immeubles, la communication des visiteurs et les parcours d acces des locataires.', 'intro': 'Opticable installe l infrastructure d interphone pour les proprietes commerciales et les environnements multilogements qui exigent une communication claire aux points d entree, aux portails, aux halls et aux zones a acces controle.', 'summary': 'Systemes de communication d entree, de portail et de locataires coordonnes avec l acces et l infrastructure reseau.', 'includes': ['Cablage et soutien d appareils d interphone pour halls, entrees, portails et suites', 'Planification de l integration avec le controle d acces, les cameras et les besoins de communication des locataires', 'Coordination reseau et des salles techniques pour controleurs ou equipements d interphone'], 'benefits': ['Communication visiteur plus claire aux points d entree', 'Meilleure integration avec les parcours des locataires et de l acces', 'Modifications futures simplifiees pour nouvelles suites ou entrees'], 'cases': ['Systemes d entree pour immeubles multilogements et proprietes mixtes', 'Mises a niveau des communications de halls', 'Ajout d interphones a des portails et entrees controlees'], 'industries': ['Immeubles commerciaux multilogements', 'Portefeuilles de gestion immobiliere', 'Developpements mixtes'], 'related': ['access-control-systems', 'security-camera-systems', 'structured-cabling']},
    },
    'commercial-wifi-installation': {
        'en': {'slug': 'commercial-wifi-installation', 'name': 'Commercial WiFi Installation', 'title': 'Commercial WiFi Installation and Access Point Cabling | Opticable', 'desc': 'Commercial WiFi installation including access point cabling, coverage planning, switching support, and wireless infrastructure for business properties.', 'hero': 'Commercial WiFi installation with the cabling and infrastructure wireless networks depend on.', 'intro': 'Opticable helps commercial clients deploy the physical infrastructure behind wireless networks, including access point cabling, mounting support, switching coordination, and coverage planning for active business environments.', 'summary': 'Wireless access point cabling, coverage planning, switching coordination, and infrastructure for business WiFi.', 'includes': ['Cabling for wireless access points in offices, common areas, retail spaces, and larger commercial footprints', 'Coverage-oriented placement coordination tied to building layout and device density', 'Switching, patching, and rack-side support for wireless infrastructure'], 'benefits': ['More dependable wireless coverage', 'Better integration with the network core', 'Room for future device density and added coverage'], 'cases': ['Office WiFi refreshes and tenant expansions', 'Retail guest and staff wireless improvements', 'Wireless rollouts tied to structured cabling or room upgrades'], 'industries': ['Office environments', 'Retail and hospitality', 'Commercial and multi-tenant properties'], 'related': ['structured-cabling', 'network-infrastructure', 'ip-phone-systems']},
'fr': {'slug': 'installation-wifi-commercial', 'name': 'WiFi commercial', 'title': 'Installation de WiFi commercial et cablage de points d acces | Opticable', 'desc': 'Installation de WiFi commercial incluant le cablage des points d acces, la planification de couverture, le soutien a la commutation et l infrastructure sans fil pour proprietes d affaires.', 'hero': 'Installation de WiFi commercial avec le cablage et l infrastructure dont les reseaux sans fil ont besoin.', 'intro': 'Opticable aide les clients commerciaux a deployer l infrastructure physique derriere les reseaux sans fil, incluant le cablage des points d acces WiFi, le soutien au montage, la coordination des commutateurs et la planification de couverture pour des environnements actifs.', 'summary': 'Cablage des points d acces, planification de couverture, coordination des commutateurs et infrastructure pour le WiFi d affaires.', 'includes': ['Cablage pour points d acces sans fil dans les bureaux, aires communes, commerces et grandes superficies commerciales', 'Coordination des emplacements selon la couverture requise, l amenagement du batiment et la densite des appareils', 'Commutation, raccordement et soutien cote baie pour l infrastructure sans fil'], 'benefits': ['Couverture sans fil plus fiable', 'Meilleure integration au coeur reseau', 'Plus de place pour la densite future et les ajouts de couverture'], 'cases': ['Refresh WiFi de bureaux et expansions de locataires', 'Amelioration de la couverture sans fil pour clients et employes', 'Mises en service sans fil liees au cablage structure ou a des upgrades de salles reseau'], 'industries': ['Environnements de bureaux', 'Commerce et hotellerie', 'Proprietes commerciales et multilogements'], 'related': ['structured-cabling', 'network-infrastructure', 'ip-phone-systems']},
    },
    'ip-phone-systems': {
        'en': {'slug': 'ip-phone-systems', 'name': 'IP Phone Systems', 'title': 'IP Phone Systems and VoIP Phone Line Infrastructure | Opticable', 'desc': 'Commercial IP phone system installation and VoIP phone line infrastructure for offices, multi-tenant buildings, and business communication environments.', 'hero': 'IP phone systems and VoIP phone line infrastructure for business communication environments.', 'intro': 'Opticable supports the cabling, device connectivity, and network infrastructure required for commercial IP phone systems and VoIP phone line deployment. Phone infrastructure is planned with structured cabling, switching, and room layouts so it stays easier to support after activation.', 'summary': 'Business phone infrastructure, handset connectivity, VoIP-ready cabling, and network support for office communication.', 'includes': ['Cabling and connectivity for IP handsets, conference phones, and related devices', 'VoIP phone line infrastructure aligned with switching and broader network requirements', 'Phone system changes during office expansions, moves, and room reconfiguration'], 'benefits': ['Dependable phone connectivity', 'Cleaner office deployment for reception, desks, and meeting rooms', 'Simpler future adds, moves, and handset changes'], 'cases': ['Office relocations and workstation reconfiguration', 'Reception and front-desk communication upgrades', 'VoIP migrations requiring updated switching and room organization'], 'industries': ['Business offices', 'Professional services firms', 'Multi-tenant commercial suites'], 'related': ['network-infrastructure', 'structured-cabling', 'commercial-wifi-installation']},
        'fr': {'slug': 'systemes-telephonie-ip', 'name': 'Systemes de telephonie IP', 'title': 'Systemes de telephonie IP et infrastructure de lignes VoIP | Opticable', 'desc': 'Installation commerciale de systemes de telephonie IP et d infrastructure de lignes VoIP pour bureaux, immeubles multilogements et environnements de communication d affaires.', 'hero': 'Systemes de telephonie IP et infrastructure de lignes VoIP pour les environnements de communication d affaires.', 'intro': 'Opticable soutient le cablage, la connectivite des appareils et l infrastructure reseau necessaires a l installation de systemes commerciaux de telephonie IP et de lignes VoIP. La telephonie est planifiee avec le cablage structure, la commutation et l implantation des locaux afin que le systeme reste facile a soutenir.', 'summary': 'Infrastructure de telephonie d affaires, connectivite des postes, cablage pret pour la VoIP et soutien reseau pour la communication des bureaux.', 'includes': ['Cablage et connectivite pour postes IP, telephones de conference et autres appareils de communication', 'Infrastructure de lignes VoIP alignee sur la commutation et les exigences reseau globales', 'Modifications des systemes telephoniques lors d agrandissements, demenagements ou reconfigurations'], 'benefits': ['Connectivite telephonique fiable', 'Deploiement plus propre au bureau pour les receptions et salles de reunion', 'Changements futurs simplifies pour les ajouts et deplacements'], 'cases': ['Relocalisations de bureaux et reconfiguration de postes', 'Modernisation des communications de reception', 'Migrations VoIP avec mise a jour de la commutation et des salles'], 'industries': ['Bureaux d entreprise', 'Firmes de services professionnels', 'Suites commerciales multilogements'], 'related': ['network-infrastructure', 'structured-cabling', 'commercial-wifi-installation']},
    },
}
industry_cards['en'] = [
    ('Businesses', 'Security, WiFi, and communications for offices, retail, and hospitality.'),
    ('Multi-tenant buildings', 'Entry systems, cameras, suite cabling, and common-area infrastructure.'),
    ('Commercial properties', 'Technology systems that support occupancy, tenant service, and building operations.'),
    ('Property managers', 'Repeatable standards, upgrades, and cleaner support across active assets.'),
    ('Developers and contractors', 'Technology coordination for security, wireless, cabling, and infrastructure delivery.'),
]
industry_cards['fr'] = [
    ('Entreprises', 'Sécurité, WiFi et communications pour bureaux, commerces et hôtellerie.'),
    ('Immeubles multilogements', "Systèmes d'entrée, caméras, câblage de suites et infrastructures d'aires communes."),
    ('Immeubles commerciaux', "Systèmes technologiques qui soutiennent l'exploitation, le service aux locataires et l'occupation."),
    ('Gestionnaires immobiliers', 'Standards répétables, mises à niveau et meilleur soutien dans des immeubles occupés.'),
    ('Promoteurs et entrepreneurs', "Coordination technologique pour la sécurité, le sans-fil, le câblage et la livraison des travaux."),
]

services['structured-cabling']['en']['intro'] = 'Opticable installs the physical cabling foundation behind business connectivity, security devices, wireless coverage, and tenant infrastructure systems. Structured cabling scopes can include Ethernet cable installation, coaxial cable installation, pathway organization, terminations, and labeling that makes future support easier.'
services['structured-cabling']['fr'].update({
    'name': 'Câblage structuré',
    'title': 'Installation de câblage structuré pour immeubles commerciaux | Opticable',
    'desc': 'Installation de câblage structuré pour bureaux, immeubles multilogements et immeubles commerciaux, incluant fibre optique, Cat 5e, Cat 6, Cat 6e, Ethernet, coaxial, repérage et cheminements.',
    'hero': 'Câblage structuré pour bureaux, immeubles et espaces commerciaux.',
    'intro': "Opticable installe le câblage qui soutient la connectivité d'affaires, les caméras, le WiFi, la téléphonie, la fibre optique et les autres systèmes technologiques d'un immeuble, avec des parcours Cat 5e, Cat 6 et Cat 6e adaptés au projet.",
    'summary': 'Fibre optique, Cat 5e, Cat 6, Cat 6e, Ethernet, coaxial, raccordement et organisation soignée pour les espaces commerciaux.',
    'includes': ["Liens Cat 5e, Cat 6, Cat 6A et Cat 6e pour postes de travail, points d'accès WiFi, caméras, téléphones et équipements d'affaires", 'Câblage coaxial pour services internet, distribution spécialisée et équipements commerciaux', "Panneaux de raccordement, terminaisons, accessoires de cheminement, repérage, essais et remise en ordre de câbles existants"],
    'benefits': ['Infrastructure plus propre et plus simple à entretenir', 'Dépannage plus rapide après la livraison', 'Meilleure marge pour les ajouts, les déménagements et les nouveaux appareils'],
    'cases': ['Aménagements locatifs et agrandissements de bureaux', "Mises à niveau de connectivité dans les commerces et l'hôtellerie", 'Remise en ordre avant un projet de WiFi ou de sécurité'],
    'industries': ['Bureaux', 'Immeubles multilogements', 'Immeubles commerciaux et propriétés à usage mixte'],
})
services['security-camera-systems']['en'].update({
    'desc': 'Commercial security camera sales, management, and installation with PoE cabling, recording, remote viewing, user permissions, and network coordination for businesses, multi-unit properties, and active job sites.',
    'hero': 'Security camera sales, management, and installation for businesses, buildings, multi-unit properties, and temporary job sites.',
    'intro': 'Opticable sells, manages, and installs commercial security camera systems together with the cabling and network infrastructure that support them. Camera projects are coordinated with recorders, switches, remote viewing, user permissions, and active site conditions so coverage stays dependable day to day, including for construction cameras and temporary job site cameras.',
    'summary': 'Sales, management, and installation of camera systems with PoE, recording, remote viewing, and network coordination.',
    'includes': ['Selection, sales, and installation of interior, exterior, construction, and temporary job site cameras based on site requirements', 'Cabling, terminations, and PoE planning with switch and rack coordination', 'Recorder setup, remote viewing, and routing toward network rooms or site surveillance infrastructure', 'User-permission setup so specific people only have access to the cameras or areas assigned to them'],
    'benefits': ['Helps discourage theft, vandalism, and unauthorized access', 'Improves day-to-day visibility with remote viewing and controlled user access by camera group or area', 'Supports safer environments for staff, tenants, visitors, and active job sites', 'Makes important events easier to review through recording and more organized system management'],
    'cases': ['Retail surveillance upgrades and common-area monitoring', 'Perimeter, entry, parking, and sensitive-area camera additions', 'Warehouse, loading dock, and operational monitoring coverage', 'Construction cameras and temporary job site cameras for active phases, renovations, and temporary security needs'],
    'industries': ['Retail and hospitality', 'Commercial office properties', 'Multi-unit residential, condo, and mixed-use properties', 'Industrial and warehouse sites', 'Construction and temporary job sites'],
})
services['fiber-optic-installation']['fr'].update({
    'name': 'Fibre optique',
    'title': 'Fibre optique pour immeubles commerciaux | Opticable',
    'desc': "Installation de fibre optique pour liaisons principales, colonnes montantes, prolongements de service Internet et liaisons à haute capacité.",
    'hero': 'Fibre optique pour liaisons principales, colonnes montantes et connectivité à haute capacité.',
    'intro': "Opticable installe la fibre optique dans les environnements commerciaux qui ont besoin d'une liaison principale fiable, d'un prolongement du point de démarcation ou de liaisons à forte capacité entre étages, suites et locaux réseau.",
    'summary': 'Liaisons principales en fibre, colonnes montantes, prolongements de service et liaisons à haute capacité.',
    'includes': ["Câblage de fibre entre MDF, IDF, suites et principaux emplacements d'équipement", "Prolongements du point de démarcation vers le local réseau", 'Terminaisons de fibre, connexions, cheminement et coordination au rack'],
    'benefits': ['Plus de capacité pour la croissance future', "Liaisons fiables sur de longues distances à l'intérieur d'un même immeuble", 'Meilleure coordination avec les racks, les commutateurs et les locaux techniques'],
    'cases': ['Immeubles de bureaux et propriétés mixtes sur plusieurs étages', "Prolongements de service Internet jusqu'au local réseau", "Mise à niveau de la liaison principale lors d'un réaménagement locatif ou de travaux côté propriétaire"],
    'industries': ['Immeubles de bureaux', 'Propriétés multilocatives', 'Sites industriels et entrepôts'],
})
services['network-infrastructure']['fr'].update({
    'name': 'Infrastructure réseau',
    'title': 'Infrastructure réseau commerciale et installation de racks | Opticable',
    'desc': "Services d'infrastructure réseau commerciale, incluant l'installation de racks, l'aménagement de locaux réseau, les raccordements et les prolongements Internet.",
    'hero': 'Infrastructure réseau, racks et locaux techniques pour les environnements commerciaux.',
    'intro': "Opticable aménage l'infrastructure physique qui relie les services Internet, les locaux techniques, les racks et les équipements actifs d'un bâtiment commercial.",
    'summary': 'Racks, locaux réseau, raccordements, routage des arrivées Internet et remise en ordre.',
    'includes': ['Installation de racks et d’armoires réseau avec gestion de câbles et terminaisons organisées', "Panneaux de raccordement, liaisons montantes, connectivité des commutateurs et cheminement entre le point de démarcation et le rack", "Déploiement d'infrastructure Internet et remise en ordre de locaux réseau encombrés ou mal identifiés"],
    'benefits': ['Locaux techniques plus faciles à entretenir', 'Meilleure coordination entre WiFi, sécurité, téléphonie et systèmes locatifs', 'Moins de reprise lors des mises à niveau futures'],
    'cases': ['Mise en place de locaux réseau pour nouveaux bureaux ou commerces', 'Prolongements de service et routage principal dans les immeubles gérés', "Remise en ordre de MDF et IDF existants avant expansion"],
    'industries': ['Bureaux', 'Portefeuilles immobiliers', 'Commerces et hôtellerie'],
})
services['security-camera-systems']['fr'].update({
    'name': 'Caméras de sécurité',
    'title': 'Vente, gestion et installation de caméras de sécurité commerciales | Opticable',
    'desc': "Vente, gestion et installation de caméras de sécurité commerciales avec câblage, connectivité PoE, enregistrement, visionnement à distance, permissions utilisateurs et coordination réseau pour entreprises, multi-logements et sites actifs.",
    'hero': 'Vente, gestion et installation de caméras de sécurité pour entreprises, immeubles, multi-logements et chantiers temporaires.',
    'intro': "Opticable vend, gère et installe des caméras de sécurité commerciales, en plus de mettre en place le câblage et l'infrastructure réseau qui les soutiennent. Les projets sont coordonnés avec les enregistreurs, les commutateurs, le visionnement à distance, les accès utilisateurs et les conditions réelles du bâtiment pour offrir une surveillance fiable au quotidien, y compris avec des caméras de chantier et des caméras temporaires.",
    'summary': 'Vente, gestion et installation de caméras, avec PoE, enregistrement, visionnement à distance et coordination réseau pour la surveillance commerciale.',
    'includes': ["Sélection, vente et installation de caméras intérieures, extérieures, de chantier et temporaires selon les besoins du site", 'Câblage, terminaisons et planification PoE avec coordination des commutateurs et des racks', "Configuration des enregistreurs, du routage vers les locaux réseau ou l'infrastructure de surveillance du bâtiment et du visionnement à distance", "Gestion des accès utilisateurs et des permissions pour limiter certaines personnes à certaines caméras ou certaines zones seulement"],
    'benefits': ["Aide à décourager les vols, le vandalisme et les intrusions", "Renforce le sentiment de sécurité des employés, des locataires et des visiteurs", "Permet le visionnement à distance avec des accès utilisateurs contrôlés selon les caméras ou les zones à surveiller", "Permet de revoir des événements importants grâce aux enregistrements et à une gestion plus structurée"],
    'cases': ['Décourager les vols dans les commerces, halls, stationnements et aires communes', "Augmenter le sentiment de sécurité des employés, des locataires et du personnel sur place", "Enregistrer des événements importants pour pouvoir les revoir au besoin", 'Ajouter des caméras au périmètre, aux entrées et dans les zones sensibles', 'Couvrir les entrepôts, quais de chargement et sites opérationnels', 'Installer des caméras de chantier et des caméras temporaires pour la construction, la rénovation ou une surveillance provisoire', 'Remplacer ou moderniser un système existant avec une gestion plus simple'],
    'industries': ['Commerce et hôtellerie', 'Bureaux et propriétés commerciales', 'Multi-logements, copropriétés et immeubles multilogements', 'Sites industriels et entrepôts', 'Chantiers et sites temporaires'],
})
services['access-control-systems']['en']['desc'] = 'Commercial access control system installation with door hardware coordination, controller support, remote unlock capability, authorized-hour scheduling, and entry planning for business and managed properties.'
services['access-control-systems']['en']['intro'] = 'Opticable installs the door access infrastructure required for commercial access control systems, including reader locations, panel support, door hardware coordination, network connectivity, remote unlock capability, and authorized-hour control for secure operations.'
services['access-control-systems']['en']['includes'][0] = 'Infrastructure cabling for readers, electrified hardware, panels, and related door components'
services['access-control-systems']['en']['includes'][2] = 'Remote unlock setup, authorized-hour scheduling, and integration planning with intercoms, cameras, and broader security infrastructure'
services['access-control-systems']['en']['benefits'][0] = 'Better entry control with remote unlock and authorized-hour scheduling tied to building operations'
services['access-control-systems']['fr'].update({
    'name': "Contrôle d'accès",
    'title': "Installation de systèmes de contrôle d'accès commerciaux | Opticable",
    'desc': "Installation de systèmes de contrôle d'accès commerciaux incluant le câblage de porte, les panneaux, l'ouverture à distance, la gestion des heures autorisées et la coordination réseau.",
    'hero': "Contrôle d'accès pour entrées commerciales, suites et immeubles gérés, avec gestion à distance.",
    'intro': "Opticable installe l'infrastructure requise pour les systèmes de contrôle d'accès, incluant les lecteurs, les panneaux, le matériel électrifié, la connectivité réseau, l'ouverture à distance et la gestion des heures autorisées pour une exploitation sécurisée.",
    'summary': "Lecteurs, panneaux, câblage de porte et infrastructure d'entrée sécurisée.",
    'includes': ['Câblage pour lecteurs, matériel électrifié, panneaux et composantes de porte', 'Panneaux de contrôle, connectivité réseau et coordination des cheminements', "Ouverture à distance, gestion des heures autorisées et configuration des accès selon les portes, les utilisateurs ou les zones", 'Planification avec intercoms, caméras et autres systèmes de sécurité'],
    'benefits': ["Meilleure coordination des entrées avec l'exploitation du bâtiment", "Permet l'ouverture à distance et le contrôle des heures autorisées selon les accès à gérer", 'Intégration plus propre entre plusieurs systèmes', 'Installations plus simples à entretenir lors des interventions futures'],
    'cases': ["Mise à niveau d'entrées principales dans les bureaux et les propriétés mixtes", "Contrôle d'accès pour suites et aires communes", "Gestion des portes avec ouverture à distance et horaires autorisés pour employés, locataires ou fournisseurs", 'Entrées sécurisées pour zones restreintes ou opérationnelles'],
    'industries': ['Bureaux et propriétés commerciales', 'Immeubles multilogements', 'Installations industrielles'],
})
services['intercom-systems']['fr'].update({
    'name': 'Intercom',
    'title': "Installation d'intercoms commerciaux | Opticable",
    'desc': "Installation d'intercoms commerciaux pour immeubles multilogements, entrées de bureaux et accès contrôlés.",
    'hero': "Intercoms pour entrées d'immeuble, visiteurs et parcours d'accès des locataires.",
    'intro': "Opticable installe l'infrastructure d'intercom pour les immeubles commerciaux et multilogements qui ont besoin d'une communication claire aux entrées, aux halls, aux portails et aux zones contrôlées.",
    'summary': "Communication à l'entrée, au portail et au hall, coordonnée avec l'accès et le réseau.",
    'includes': ["Câblage et soutien d'appareils pour halls, entrées, portails et suites", "Planification avec contrôle d'accès, caméras et besoins de communication des occupants", "Coordination réseau et locaux techniques pour contrôleurs et équipements d'intercom"],
    'benefits': ['Communication plus claire avec les visiteurs', "Meilleure intégration avec les parcours d'accès", 'Modifications futures simplifiées pour de nouvelles suites ou de nouvelles entrées'],
    'cases': ["Systèmes d'entrée pour immeubles multilogements et propriétés mixtes", 'Mises à niveau des communications de hall', "Ajout d'intercoms à des portails et entrées contrôlées"],
    'industries': ['Immeubles commerciaux multilogements', 'Portefeuilles de gestion immobilière', 'Développements mixtes'],
})
services['commercial-wifi-installation']['en'].update({
    'name': 'WiFi and Wireless Networks',
    'title': 'WiFi Sales, Management, Maintenance, Installation, and Cabling | Opticable',
    'desc': 'Sales, management, maintenance, installation, and cabling for WiFi networks in offices, retail, common areas, events, multi-unit properties, condos, construction sites, and industrial sites.',
    'hero': 'WiFi networks for offices, retail, common areas, events, multi-unit properties, condos, construction sites, and industrial sites.',
    'intro': 'Opticable sells, manages, maintains, installs, and cables WiFi networks for more than standard commercial office environments. The scope can cover common areas, events, retail, multi-unit buildings, condo properties, offices, factories, construction sites, and other sites that need dependable wireless coverage and the infrastructure behind it.',
    'summary': 'Sales, management, maintenance, installation, and cabling for WiFi networks across buildings, shared areas, events, construction sites, and active sites.',
    'includes': ['WiFi sales, installation, and access point cabling for offices, retail, common areas, multi-unit properties, condo buildings, factories, construction sites, and event spaces', 'Coverage planning, access point placement, and wireless design tied to layout, density, and active user demands', 'Switching, patching, rack support, and network coordination for wireless infrastructure', 'Ongoing management and maintenance for wireless networks that need dependable day-to-day performance'],
    'benefits': ['More dependable wireless coverage across different site types and shared-use environments', 'Cleaner coordination between wireless equipment, structured cabling, and the network core', 'Easier long-term support, changes, and expansion as coverage needs evolve'],
    'cases': ['Office WiFi rollouts and expansions', 'Retail and hospitality guest or staff WiFi improvements', 'Common-area WiFi for managed properties and condo buildings', 'Event WiFi and temporary wireless deployments', 'Construction site WiFi and temporary project connectivity', 'Factory, warehouse, and industrial wireless coverage projects'],
    'industries': ['Offices and commercial properties', 'Retail and hospitality', 'Common areas and shared-use spaces', 'Multi-unit, condo, and mixed-use properties', 'Construction sites and temporary project spaces', 'Industrial and warehouse sites', 'Events and temporary wireless deployments'],
})
services['commercial-wifi-installation']['fr'].update({
    'name': 'WiFi et réseaux sans fil',
    'title': "Vente, gestion, maintenance, installation et câblage WiFi | Opticable",
    'desc': "Vente, gestion, maintenance, installation et câblage de réseaux WiFi pour bureaux, commerces, aires communes, événements, multi-logements, copropriétés, chantiers de construction et sites industriels.",
    'hero': "WiFi pour bureaux, commerces, aires communes, événements, multi-logements, copropriétés, chantiers de construction et usines.",
    'intro': "Opticable fait la vente, la gestion, la maintenance, l'installation et le câblage de réseaux WiFi pour plus que les bureaux classiques. Le service peut couvrir les aires communes, les événements, les commerces, les multi-logements, les copropriétés, les bureaux, les usines, les chantiers de construction et d'autres sites qui ont besoin d'une couverture sans fil stable et bien soutenue.",
    'summary': "Vente, gestion, maintenance, installation et câblage WiFi pour bâtiments, espaces communs, événements, chantiers et sites actifs.",
    'includes': ["Vente, installation et câblage de points d'accès WiFi pour bureaux, commerces, aires communes, multi-logements, copropriétés, chantiers de construction, usines et espaces événementiels", "Planification de couverture, positionnement des points d'accès et conception du sans-fil selon l'aménagement, la densité et les usages réels", "Commutateurs, raccordements, soutien au rack et coordination réseau pour l'infrastructure sans fil", "Gestion et maintenance de réseaux WiFi qui doivent rester fiables au quotidien"],
    'benefits': ['Couverture sans fil plus fiable dans plusieurs types de sites et d’espaces partagés', 'Meilleure intégration entre le WiFi, le câblage structuré et le cœur du réseau', "Plus de souplesse pour l'entretien, les changements et l'expansion de la couverture dans le temps"],
    'cases': ['Déploiement ou modernisation du WiFi dans les bureaux et espaces administratifs', 'Amélioration du WiFi pour commerces, hôtellerie et espaces clients', 'WiFi dans les aires communes d’immeubles gérés, multi-logements et copropriétés', 'WiFi pour événements, installations temporaires et besoins ponctuels', 'WiFi pour chantiers de construction et connectivité temporaire de projet', 'Couverture sans fil pour usines, entrepôts et environnements industriels'],
    'industries': ['Bureaux et propriétés commerciales', 'Commerce et hôtellerie', 'Aires communes et espaces partagés', 'Multi-logements, copropriétés et immeubles multilogements', 'Chantiers de construction et espaces de projet temporaires', 'Usines, entrepôts et sites industriels', 'Événements et déploiements temporaires'],
})
services['ip-phone-systems']['fr'].update({
    'name': 'Téléphonie IP et lignes',
    'title': 'Téléphonie IP, lignes VoIP et numéros de téléphone | Opticable',
    'desc': "Installation de systèmes de téléphonie IP avec fourniture de lignes VoIP et de numéros de téléphone pour bureaux, immeubles multilogements et environnements d'affaires.",
    'hero': "Téléphonie IP, lignes VoIP et numéros de téléphone pour les environnements d'affaires.",
    'intro': "Opticable prend en charge le câblage, la connectivité des appareils et l'infrastructure réseau nécessaires aux systèmes de téléphonie IP. Nous fournissons aussi les lignes IP et les numéros de téléphone d'affaires requis pour la mise en service.",
    'summary': "Téléphonie d'affaires, lignes IP, numéros de téléphone et câblage prêt pour la VoIP.",
    'includes': ['Câblage et connectivité pour postes IP, téléphones de conférence et appareils connexes', 'Fourniture et mise en service de lignes VoIP et de numéros de téléphone, alignées avec la commutation et les besoins du réseau', "Changements téléphoniques lors d'agrandissements, de déménagements et de reconfigurations"],
    'benefits': ['Connectivité téléphonique fiable', "Déploiement plus propre pour l'accueil, les postes et les salles de réunion", 'Ajouts et changements plus simples par la suite'],
    'cases': ['Relocalisations de bureaux et reconfiguration de postes', 'Modernisation des communications de réception', 'Migration VoIP avec mise à jour de la commutation et des locaux réseau'],
    'industries': ['Bureaux', 'Firmes de services professionnels', 'Suites commerciales multilocatives'],
})

shared_service_types_en = [
    'Retail and hospitality',
    'Commercial office properties',
    'Multi-unit residential, condo, and mixed-use properties',
    'Industrial and warehouse sites',
]
shared_service_types_fr = [
    'Commerce et hôtellerie',
    'Bureaux et propriétés commerciales',
    'Multi-logements, copropriétés et immeubles multilogements',
    'Sites industriels et entrepôts',
]
for key in (
    'structured-cabling',
    'fiber-optic-installation',
    'network-infrastructure',
    'managed-it-services',
    'access-control-systems',
    'intercom-systems',
    'ip-phone-systems',
):
    services[key]['en']['industries'] = shared_service_types_en
    services[key]['fr']['industries'] = shared_service_types_fr

T['en'].update({
    'tagline': 'Technology infrastructure partner',
    'company': 'Opticable helps businesses design, install, and support the technology infrastructure that keeps their operations connected, secure, and efficient.',
    'home_title': 'Technology Infrastructure Partner for Businesses | Opticable',
    'home_desc': 'Opticable supports businesses with structured cabling, professional WiFi, IT solutions, surveillance systems, access control, and intercom infrastructure.',
    'home_kicker': 'Technology infrastructure for businesses',
    'home_h1': 'Your technology infrastructure partner.',
    'home_intro': 'Opticable supports businesses with the design, installation, and management of technology infrastructure so day-to-day operations stay reliable, secure, and high performing.',
    'home_points': [
        'Structured cabling and backbone infrastructure for connected environments',
        'Professional WiFi built around coverage, performance, and security',
        'IT solutions for servers, workstations, and business systems',
        'Camera surveillance for buildings, teams, and operations',
        'Intercom and access control for secure, well-managed entry points',
    ],
    'featured_title': 'Core services',
    'featured_intro': 'Five core service areas that define the broader Opticable offer for modern business environments.',
    'trust_title': 'Why choose Opticable',
    'trust': [
        ('Technical expertise', 'We plan infrastructure with a practical understanding of connectivity, security, deployment, and long-term support.'),
        ('Tailored solutions', 'Each project is adapted to the site, operational requirements, and growth plans of the client.'),
        ('Installation quality', 'Clean execution, organized cabling, and dependable system turnover remain part of the deliverable.'),
        ('Service and support', 'We stay focused on clear communication, reliable follow-up, and systems that remain easier to manage after installation.'),
    ],
    'services_title': 'Business Technology Services | Opticable',
    'services_desc': 'Opticable provides structured cabling, professional WiFi, IT solutions, camera surveillance, access control, intercom, fiber optic, and IP phone services for business environments.',
    'services_h1': 'Professional technology services for connectivity, security, and business operations.',
    'services_intro': 'Opticable brings together infrastructure, wireless, IT systems, surveillance, and secure-entry services in one clearer technology offering for business clients.',
    'priority_title': 'Core services',
    'priority_intro': 'The first services clients typically need when modernizing connectivity, security, and day-to-day operations.',
    'support_title': 'Complementary services',
    'support_intro': 'Additional systems and supporting layers that complete a more resilient technology environment.',
    'extra_title': 'Project capabilities',
    'extra_intro': 'Common implementation work that often supports a broader technology mandate.',
    'extras': [
        ('Patch panels and rack organization', 'Patching, labeling, cable management, and cleaner telecom rooms that stay easier to support.'),
        ('Wireless optimization', 'Post-install tuning, segmentation, and adjustments that improve reliability and user experience.'),
        ('Infrastructure testing', 'Verification, validation, and documentation that support better turnover and future maintenance.'),
        ('After-install support', 'Follow-up support for changes, additions, troubleshooting, and day-to-day operational needs.'),
    ],
    'about_title': 'About Opticable | Business Technology Expertise',
    'about_desc': 'Learn how Opticable supports businesses with reliable, modern, and practical technology infrastructure solutions.',
    'about_h1': 'Technology expertise in service of business environments.',
    'about_intro': 'Opticable specializes in technology infrastructure solutions for modern organizations. Our mission is to deliver reliable systems that help businesses stay connected, secure, and efficient in a constantly evolving environment.',
    'about_story': 'Our team designs and deploys infrastructure adapted to each client, whether the goal is to modernize an existing network, launch a new facility, or improve operations across a professional property. We work with recognized equipment and focus on solutions that simplify work for our clients and support long-term growth.',
    'about_section_title': 'How we approach projects',
    'about_section_intro': 'A project approach built around reliability, practical planning, and a complete technology partnership.',
    'about_values': [
        ('Business-oriented expertise', 'We approach projects through the operational needs of offices, commercial sites, and managed environments.'),
        ('Reliable systems', 'The objective is dependable connectivity, better security, and technology that performs consistently.'),
        ('Professional execution', 'Planning, installation, documentation, and turnover are treated as part of the service quality.'),
        ('Long-term usefulness', 'Solutions are selected to remain scalable, supportable, and easier to operate over time.'),
    ],
    'contact_title': 'Contact Opticable | Discuss Your Technology Project',
    'contact_desc': 'Talk to Opticable about structured cabling, professional WiFi, IT solutions, surveillance, intercom, and access control for your business.',
    'contact_h1': 'Let us talk about your technology project.',
    'contact_intro': 'Want to improve your network infrastructure, deploy business WiFi, install surveillance, or modernize your technology environment? Opticable is ready to support the next step.',
    'contact_panel_copy': 'Share the site type, your goals, and the systems involved. We can help define the right technical scope for a reliable deployment.',
    'process_title': 'Project process',
    'process_intro': 'A strong technology project starts with the right planning, then moves through clean delivery and practical follow-up.',
    'process': [
        ('Assessment', 'We review the site, the current environment, operational constraints, and the systems that need to work together.'),
        ('Design', 'We define the technical scope, infrastructure approach, device locations, and the right deployment path.'),
        ('Installation', 'We install, configure, organize, and test the infrastructure with a clean and professional workflow.'),
        ('Support', 'We help with turnover, optimization, and the next operational steps after implementation.'),
    ],
    'clients_title': 'Who we support',
    'clients_intro': 'Business environments that need modern, reliable, and supportable technology infrastructure.',
    'clients': [
        ('Businesses and offices', 'Structured cabling, WiFi, IT systems, and secure operations for professional work environments.'),
        ('Commercial properties', 'Technology infrastructure that supports occupancy, tenant service, and building performance.'),
        ('Multi-unit and mixed-use sites', 'Shared-area connectivity, secure entry, surveillance, and practical operational systems.'),
        ('Developers, contractors, and managers', 'Technology planning and delivery that fits project sequencing and building realities.'),
    ],
    'industries_h1': 'Technology infrastructure services for teams that operate, manage, and improve professional environments.',
    'industries_intro': 'Opticable supports business sites, managed properties, and project teams that want modern systems without losing clarity or reliability.',
    'overview_intro': 'Scope, business value, and what implementation can include.',
    'related_intro': 'Related services that often support the same technology roadmap.',
})
T['fr'].update({
    'tagline': 'Partenaire en infrastructure technologique',
    'company': "Opticable accompagne les entreprises dans la conception, l'installation et la gestion de leurs infrastructures technologiques afin d'assurer une connectivite fiable, securisee et performante.",
    'home_title': 'Partenaire en infrastructure technologique pour entreprises | Opticable',
    'home_desc': "Opticable propose le cablage structure, le Wi-Fi professionnel, les solutions informatiques, la videosurveillance, l'intercom et le controle d'acces pour les environnements d'affaires.",
    'home_kicker': 'Infrastructure technologique pour entreprises',
    'home_h1': 'Votre partenaire en infrastructure technologique.',
    'home_intro': "Opticable accompagne les entreprises dans la conception, l'installation et la gestion de leurs infrastructures technologiques afin d'assurer une connectivite fiable, securisee et performante.",
    'home_points': [
        'Cablage structure et infrastructures backbone pour des environnements connectes',
        'Wi-Fi professionnel pense pour la couverture, la performance et la securite',
        'Solutions informatiques pour serveurs, postes de travail et environnements IT',
        'Surveillance par camera pour les batiments, les equipes et les operations',
        "Intercom et controle d'acces pour des entrees mieux gerees et securisees",
    ],
    'featured_title': 'Services cles',
    'featured_intro': "Cinq services cles pour presenter Opticable comme un partenaire technologique plus complet.",
    'trust_title': 'Pourquoi choisir Opticable',
    'trust': [
        ('Expertise technique', "Nous concevons les infrastructures avec une vision pratique de la connectivite, de la securite, du deploiement et du soutien a long terme."),
        ('Solutions sur mesure', "Chaque projet est adapte au site, aux operations et aux objectifs d'evolution du client."),
        ("Qualite d'installation", "Une execution propre, un cablage organise et une remise structuree font partie integrante de la livraison."),
        ('Service et accompagnement', 'Nous privilegions la clarte, le suivi et des systemes qui restent simples a faire evoluer apres installation.'),
    ],
    'services_title': 'Services technologiques pour entreprises | Opticable',
    'services_desc': "Opticable offre le cablage structure, le Wi-Fi professionnel, les solutions informatiques, la surveillance par camera, le controle d'acces, l'intercom, la fibre et la telephonie IP pour les environnements d'affaires.",
    'services_h1': 'Des services technologiques professionnels pour la connectivite, la securite et les operations d affaires.',
    'services_intro': "Opticable regroupe l'infrastructure, le sans-fil, l'informatique, la surveillance et les services d'entree securisee dans une offre plus claire et plus complete pour les clients d'affaires.",
    'priority_title': 'Services principaux',
    'priority_intro': "Les services les plus souvent recherches lorsqu'une entreprise modernise sa connectivite, sa securite et ses operations.",
    'support_title': 'Services complementaires',
    'support_intro': "Les couches et systemes additionnels qui completent un environnement technologique plus solide.",
    'extra_title': 'Capacites de projet',
    'extra_intro': "Des travaux et interventions qui soutiennent frequemment un mandat technologique plus large.",
    'extras': [
        ('Patch panels et organisation de racks', 'Raccordement, etiquetage, gestion des cables et remise en ordre des locaux techniques pour un environnement plus propre.'),
        ('Optimisation sans fil', 'Ajustements, segmentation et affinage apres installation pour ameliorer la fiabilite et l experience utilisateur.'),
        ("Verification de l'infrastructure", 'Validation, essais et documentation pour faciliter la remise et la maintenance future.'),
        ('Soutien apres installation', 'Suivi, ajouts, ajustements et depannage pour soutenir les operations quotidiennes.'),
    ],
    'about_title': "A propos d'Opticable | Expertise technologique pour entreprises",
    'about_desc': "Decouvrez comment Opticable accompagne les organisations avec des solutions d'infrastructure technologique fiables, modernes et utiles.",
    'about_h1': 'Une expertise technologique au service des entreprises',
    'about_intro': "Opticable est une entreprise specialisee dans les solutions d'infrastructure technologique pour les organisations modernes. Notre mission est de fournir des systemes fiables et performants qui permettent aux entreprises de rester connectees, securisees et efficaces dans un environnement technologique en constante evolution.",
    'about_story': "Notre equipe possede l'expertise necessaire pour concevoir et deployer des infrastructures adaptees aux besoins specifiques de chaque client. Qu'il s'agisse de moderniser un reseau existant ou d'implanter une infrastructure complete dans un nouveau batiment, nous assurons une planification rigoureuse et une execution professionnelle. Nous travaillons avec des equipements reconnus afin de garantir la performance, la durabilite et la securite des installations. Notre objectif est simple : offrir des solutions technologiques qui simplifient le travail de nos clients et soutiennent leur croissance.",
    'about_section_title': 'Notre approche',
    'about_section_intro': 'Une direction axee sur la fiabilite, la planification pratique et un accompagnement technologique plus complet.',
    'about_values': [
        ("Expertise orientee affaires", "Nous abordons les projets selon les realites des bureaux, des immeubles commerciaux et des environnements professionnels."),
        ('Systemes fiables', 'Notre objectif est de livrer une connectivite stable, une securite mieux integree et des solutions qui performent dans le temps.'),
        ('Execution professionnelle', "Planification, installation, documentation et remise font partie de la qualite de service attendue."),
        ('Utilite a long terme', 'Les solutions retenues doivent rester evolutives, durables et simples a soutenir au quotidien.'),
    ],
    'contact_title': 'Contacter Opticable | Parlons de votre projet technologique',
    'contact_desc': "Contactez Opticable pour discuter de cablage structure, de Wi-Fi professionnel, de solutions informatiques, de videosurveillance, d'intercom et de controle d'acces.",
    'contact_h1': 'Parlons de votre projet technologique',
    'contact_intro': "Vous souhaitez ameliorer votre infrastructure reseau, installer un systeme de surveillance ou deployer un reseau Wi-Fi performant? L'equipe d'Opticable est prete a vous accompagner dans la realisation de votre projet.",
    'contact_panel_copy': "Presentez votre type de site, vos objectifs et les systemes concernes. Nous pourrons definir la bonne portee technique pour un deploiement adapte a votre environnement.",
    'process_title': 'Processus de projet',
    'process_intro': "Un bon projet technologique commence par une analyse claire, puis avance avec une execution propre et un accompagnement utile.",
    'process': [
        ('Analyse', "Nous evaluons le site, l'existant, les contraintes d'exploitation et les systemes qui doivent fonctionner ensemble."),
        ('Conception', "Nous definissons la portee technique, l'approche d'infrastructure, les emplacements et la bonne strategie de deploiement."),
        ('Installation', "Nous installons, configurons, organisons et testons l'infrastructure selon une methode claire et professionnelle."),
        ('Accompagnement', "Nous soutenons la remise, l'optimisation et les prochaines etapes apres la mise en service."),
    ],
    'clients_title': 'Clientèles accompagnées',
    'clients_intro': "Des environnements d'affaires qui ont besoin de technologies modernes, fiables et faciles à soutenir.",
    'clients': [
        ('Entreprises et bureaux', 'Câblage structuré, Wi-Fi, systèmes informatiques et opérations sécurisées pour les environnements professionnels.'),
        ('Immeubles commerciaux', "Infrastructure technologique qui soutient l'exploitation, le service aux occupants et la performance des bâtiments."),
        ('Sites multi-logements et usages mixtes', 'Connectivité des aires communes, gestion des entrées, surveillance et systèmes utiles au quotidien.'),
        ('Promoteurs, entrepreneurs et gestionnaires', 'Planification technologique et livraison adaptée au phasage des projets et aux réalités du terrain.'),
    ],
    'industries_h1': "Des services d'infrastructure technologique pour les équipes qui exploitent, gèrent et améliorent les environnements professionnels.",
    'industries_intro': "Opticable accompagne les sites d'affaires, les immeubles gérés et les équipes de projet qui veulent des systèmes modernes sans perdre en clarté ni en fiabilité.",
    'overview_intro': "La portée, la valeur d'affaires et ce que l'implantation peut inclure.",
    'related_intro': 'Les services connexes qui soutiennent souvent la même feuille de route technologique.',
})
home_visuals['en'] = {
    'eyebrow': 'Project environments',
    'title': 'Technology systems that feel structured, modern, and supportable.',
    'top_title': 'Professional buildings and connected business environments',
    'top_copy': 'Infrastructure that supports connectivity, secure entry, building operations, and a better client experience.',
    'top_alt': 'Professional building exterior representing a modern connected business environment',
    'main_title': 'Organized racks, patch panels, and IT backbone',
    'main_copy': 'Structured cabling, network racks, and cleaner backbone layouts that remain easier to expand and maintain.',
    'main_alt': 'Organized commercial network rack and structured cabling installation',
}
home_visuals['fr'] = {
    'eyebrow': 'Environnements de projet',
    'title': 'Des systemes technologiques structures, modernes et plus faciles a soutenir.',
    'top_title': 'Immeubles professionnels et environnements d affaires connectes',
    'top_copy': "Une infrastructure qui soutient la connectivite, les entrees securisees, l'exploitation et une meilleure experience utilisateur.",
    'top_alt': "Immeuble professionnel representant un environnement d'affaires connecte",
    'main_title': 'Racks organises, patch panels et backbone IT',
    'main_copy': "Cablage structure, racks reseau et backbone plus propre pour une evolution et un entretien simplifies.",
    'main_alt': 'Rack reseau commercial avec cablage structure bien organise',
}

services['structured-cabling']['en'].update({
    'desc': 'Structured cabling for business environments, including copper, fiber-ready pathways, patch panels, racks, testing, and cleaner room organization.',
    'hero': 'Structured cabling that gives business technology a dependable foundation.',
    'intro': 'Structured cabling is the base layer of a modern technology environment. Opticable designs and installs organized cabling systems for offices, commercial sites, industrial spaces, and institutional settings so networks stay stable and easier to evolve.',
    'summary': 'Structured cabling, patch panels, certification, and rack organization for reliable business connectivity.',
    'includes': [
        'Network cable installation for Cat5e, Cat6, Cat6A, and fiber-connected environments',
        'Patch panels, network racks, cable management, and cleaner telecom room organization',
        'Testing, certification support, upgrades, and optimization of existing infrastructure',
    ],
})
services['structured-cabling']['fr'].update({
    'desc': "Le câblage structuré est la base d'une infrastructure technologique moderne, avec backbone, patch panels, racks, certification et locaux techniques bien organisés.",
    'hero': "Le câblage structuré qui donne une base fiable à votre environnement technologique.",
    'intro': "Le câblage structuré constitue la base de toute infrastructure technologique moderne. Une installation bien pensée stabilise le réseau, améliore la performance des équipements et simplifie les expansions futures. Chez Opticable, nous concevons et installons des systèmes conformes aux standards de l'industrie pour les environnements commerciaux, industriels et institutionnels.",
    'summary': "Câblage structuré, patch panels, certification et organisation des racks pour une connectivité d'affaires fiable.",
    'includes': [
        'Installation de câbles réseau Cat5e, Cat6, Cat6A et liaisons backbone en fibre optique',
        'Patch panels, racks réseau, gestion de câblage et organisation des locaux télécom',
        'Tests, certification, mises à niveau et optimisation des infrastructures existantes',
    ],
})
services['commercial-wifi-installation']['en'].update({
    'name': 'Professional WiFi',
    'title': 'Professional WiFi Design and Installation | Opticable',
    'desc': 'Professional WiFi planning, access point deployment, controller setup, optimization, and wireless support for business environments.',
    'hero': 'Professional WiFi built for performance, coverage, and secure day-to-day use.',
    'intro': 'A strong wireless network is essential to modern business productivity. Opticable designs and deploys professional WiFi for offices, retail sites, warehouses, public spaces, and multi-unit buildings with the infrastructure required to perform reliably.',
    'summary': 'Coverage planning, access point installation, wireless optimization, and secure business WiFi support.',
    'includes': [
        'WiFi coverage analysis and planning for offices, commercial sites, warehouses, and multi-unit buildings',
        'Installation of professional access points with switching, mounting, and controller coordination',
        'Wireless optimization, network security, and after-install support for better day-to-day performance',
    ],
})
services['commercial-wifi-installation']['fr'].update({
    'name': 'Wi-Fi professionnel',
    'title': 'Conception et installation de Wi-Fi professionnel | Opticable',
    'desc': "Analyse, planification, installation et optimisation de réseaux Wi-Fi professionnels pour bureaux, commerces, entrepôts et immeubles multilogements.",
    'hero': 'Un Wi-Fi professionnel pensé pour la performance, la couverture et la sécurité au quotidien.',
    'intro': "Un réseau Wi-Fi performant est essentiel à la productivité des entreprises modernes. Opticable conçoit et déploie des réseaux Wi-Fi professionnels adaptés aux bureaux, commerces, entrepôts, espaces publics et immeubles multilogements.",
    'summary': "Analyse de couverture, installation de points d'accès, optimisation sans fil et support pour réseaux Wi-Fi professionnels.",
    'includes': [
        'Analyse et planification de la couverture Wi-Fi pour bureaux, commerces, entrepôts et immeubles multilogements',
        "Installation de points d'accès professionnels avec coordination des switches, du montage et des contrôleurs",
        'Optimisation, sécurisation des réseaux sans fil et support après installation pour une meilleure performance',
    ],
})
services['network-infrastructure']['en'].update({
    'name': 'IT Solutions',
    'title': 'IT Solutions and Business Infrastructure Support | Opticable',
    'desc': 'IT solutions for business environments, including servers, workstations, network equipment, infrastructure support, and technical assistance.',
    'hero': 'IT solutions that support business systems, connectivity, and operational stability.',
    'intro': 'Business technology relies on more than cabling alone. Opticable supports servers, workstations, network hardware, and day-to-day infrastructure needs so business environments remain stable, efficient, and easier to support.',
    'summary': 'Servers, workstations, network equipment, operational support, and practical IT infrastructure services.',
    'includes': [
        'Installation and management support for servers, workstations, and related business equipment',
        'Deployment of network equipment, switching, racks, and core infrastructure components',
        'Technical assistance, infrastructure support, and baseline security-minded system guidance',
    ],
})
services['network-infrastructure']['fr'].update({
    'name': 'Solutions informatiques',
    'title': "Solutions informatiques et soutien d'infrastructure pour entreprises | Opticable",
    'desc': "Services informatiques pour entreprises incluant serveurs, postes de travail, équipements réseau, soutien d'infrastructure et assistance technique.",
    'hero': "Des solutions informatiques qui soutiennent vos systèmes d'affaires, votre connectivité et la stabilité de vos opérations.",
    'intro': "Les systèmes informatiques sont au cœur des opérations de nombreuses organisations. Opticable offre des services complets pour soutenir la performance, la stabilité et la sécurité des environnements technologiques.",
    'summary': "Serveurs, postes de travail, équipements réseau, soutien opérationnel et infrastructure IT concrète.",
    'includes': [
        "Installation et gestion de serveurs, postes de travail et équipements technologiques d'affaires",
        "Déploiement d'équipements réseau, de switching, de racks et des composantes centrales d'infrastructure",
        "Support technique, soutien d'infrastructure et bonnes pratiques de sécurité informatique",
    ],
})
services['security-camera-systems']['en'].update({
    'name': 'Camera Surveillance',
    'title': 'Business Camera Surveillance Systems | Opticable',
    'desc': 'Business surveillance systems with camera installation, storage planning, remote access, and integration with existing security infrastructure.',
    'hero': 'Camera surveillance systems that protect buildings, staff, and operations.',
    'intro': 'Surveillance systems play a key role in building security and operational visibility. Opticable installs modern camera systems adapted to each environment, with the infrastructure needed for dependable monitoring.',
    'summary': 'Camera installation, storage planning, remote viewing, and security-system integration for business environments.',
})
services['security-camera-systems']['fr'].update({
    'name': 'Surveillance par caméra',
    'title': 'Systèmes de surveillance par caméra pour entreprises | Opticable',
    'desc': "Installation de systèmes de vidéosurveillance avec câblage, stockage, accès à distance et intégration aux systèmes de sécurité existants.",
    'hero': 'Des systèmes de surveillance par caméra pour protéger les bâtiments, les équipes et les opérations.',
    'intro': "Les systèmes de surveillance jouent un rôle clé dans la sécurité des bâtiments, des employés et des opérations. Opticable met en place des solutions modernes de vidéosurveillance adaptées aux besoins de chaque environnement.",
    'summary': "Installation de caméras, gestion du stockage, accès à distance et intégration aux systèmes de sécurité pour les environnements d'affaires.",
})
services['access-control-systems']['en'].update({
    'name': 'Access Control',
    'title': 'Access Control and Secure Entry Systems | Opticable',
    'desc': 'Access control systems with secure entry hardware, reader wiring, controller support, and intercom integration for business environments.',
    'hero': 'Access control systems for secure entry, better visitor flow, and managed building access.',
    'intro': 'Access control helps manage how staff, visitors, and tenants move through professional spaces. Opticable installs secure-entry systems that can integrate with intercoms, cameras, and the wider network environment.',
    'summary': 'Secure entry systems, readers, door hardware, and integrated access workflows for business properties.',
})
services['access-control-systems']['fr'].update({
    'name': "Controle d'acces",
    'title': "Systèmes de contrôle d'accès et entrées sécurisées | Opticable",
    'desc': "Installation de systèmes de contrôle d'accès avec lecteurs, quincaillerie sécurisée, contrôleurs et intégration avec intercoms ou systèmes de sécurité.",
    'hero': "Des systèmes de contrôle d'accès pour des entrées sécurisées et une meilleure gestion des visiteurs.",
    'intro': "Les systèmes d'intercom et de contrôle d'accès permettent de mieux gérer la sécurité et les entrées dans les environnements professionnels et multi-usagers. Opticable propose des solutions fiables, modernes et évolutives pour les portes, les aires communes et les zones sensibles.",
    'summary': "Lecteurs, quincaillerie sécurisée, gestion des accès et intégration avec l'intercom ou les autres systèmes de sécurité.",
})
services['intercom-systems']['en'].update({
    'summary': 'Audio-video intercom systems for visitor communication, tenant workflows, and integrated secure entry.',
})
services['intercom-systems']['fr'].update({
    'name': 'Systemes intercom',
    'summary': "Intercoms audio-vidéo pour la communication visiteurs, les parcours des occupants et les entrées intégrées.",
})
industry_cards['en'] = [
    ('Businesses and offices', 'Connected workspaces with structured cabling, WiFi, IT systems, and practical operational support.'),
    ('Commercial properties', 'Infrastructure that supports occupants, building operations, and secure day-to-day activity.'),
    ('Multi-unit and mixed-use sites', 'Shared-area networks, secure entry, surveillance, and communication systems for modern properties.'),
    ('Property managers', 'Repeatable standards, cleaner support, and easier technology coordination across active portfolios.'),
    ('Developers and contractors', 'Technology planning and delivery that fits construction, fit-out, and phased project realities.'),
    ('Industrial and logistics sites', 'Reliable connectivity, secure access, and infrastructure that supports operational environments.'),
]
industry_cards['fr'] = [
    ('Entreprises et bureaux', 'Espaces de travail connectés avec câblage structuré, Wi-Fi, solutions informatiques et soutien opérationnel concret.'),
    ('Immeubles commerciaux', "Infrastructure qui soutient les occupants, l'exploitation et les activites quotidiennes d'un batiment."),
    ('Sites multi-logements et usages mixtes', 'Réseaux des aires communes, entrées sécurisées, surveillance et systèmes de communication pour propriétés modernes.'),
    ('Gestionnaires immobiliers', 'Standards répétables, meilleur support et coordination technologique plus simple sur des portefeuilles occupés.'),
    ('Promoteurs et entrepreneurs', 'Planification et livraison technologiques adaptées à la construction, aux aménagements et aux projets en phases.'),
    ('Sites industriels et logistiques', 'Connectivité fiable, accès sécurisé et infrastructure utile aux environnements opérationnels.'),
]
HOME_POINT_KEYS = (
    'structured-cabling',
    'commercial-wifi-installation',
    'network-infrastructure',
    'security-camera-systems',
    'access-control-systems',
)
SERVICE_CARD_META = {
    'structured-cabling': {'en': {'badge': 'LAN', 'eyebrow': 'Network foundation'}, 'fr': {'badge': 'LAN', 'eyebrow': 'Fondation reseau'}},
    'commercial-wifi-installation': {'en': {'badge': 'WIFI', 'eyebrow': 'Wireless performance'}, 'fr': {'badge': 'WIFI', 'eyebrow': 'Performance sans fil'}},
    'network-infrastructure': {'en': {'badge': 'IT', 'eyebrow': 'Managed systems'}, 'fr': {'badge': 'IT', 'eyebrow': 'Environnement informatique'}},
    'security-camera-systems': {'en': {'badge': 'CCTV', 'eyebrow': 'Site security'}, 'fr': {'badge': 'CCTV', 'eyebrow': 'Securite des sites'}},
    'access-control-systems': {'en': {'badge': 'ENTRY', 'eyebrow': 'Secure entry'}, 'fr': {'badge': 'ENTRY', 'eyebrow': 'Entrees securisees'}},
    'intercom-systems': {'en': {'badge': 'COMMS', 'eyebrow': 'Visitor communication'}, 'fr': {'badge': 'COMMS', 'eyebrow': 'Communication visiteurs'}},
    'fiber-optic-installation': {'en': {'badge': 'FIBER', 'eyebrow': 'Backbone capacity'}, 'fr': {'badge': 'FIBER', 'eyebrow': 'Capacite backbone'}},
    'ip-phone-systems': {'en': {'badge': 'VOIP', 'eyebrow': 'Business voice'}, 'fr': {'badge': 'VOIP', 'eyebrow': 'Communication vocale'}},
}
HOME_FEATURED_SERVICES = {
    'en': [
        {'key': 'structured-cabling', 'badge': 'LAN', 'title': 'Structured Cabling', 'copy': 'Cat5e, Cat6, Cat6A, fiber, patch panels, network racks, and certification work for dependable connectivity.'},
        {'key': 'commercial-wifi-installation', 'badge': 'WIFI', 'title': 'Professional WiFi', 'copy': 'Coverage planning, access point installation, controller setup, and optimization for offices, retail, warehouses, and multi-unit buildings.'},
        {'key': 'network-infrastructure', 'badge': 'IT', 'title': 'IT Solutions', 'copy': 'Servers, workstations, network equipment, operational support, and practical IT infrastructure for growing business environments.'},
        {'key': 'security-camera-systems', 'badge': 'CCTV', 'title': 'Camera Surveillance', 'copy': 'Modern surveillance systems designed to protect buildings, teams, and daily operations with reliable monitoring access.'},
        {'key': 'access-control-systems', 'badge': 'ENTRY', 'title': 'Intercom and Access Control', 'copy': 'Audio-video intercoms, card readers, secure door workflows, and integrated entry management for professional properties.'},
    ],
    'fr': [
        {'key': 'structured-cabling', 'badge': 'LAN', 'title': 'Cablage structure', 'copy': 'Cat5e, Cat6, Cat6A, fibre optique, patch panels, racks reseau et certification pour une base reseau fiable.'},
        {'key': 'commercial-wifi-installation', 'badge': 'WIFI', 'title': 'Wi-Fi professionnel', 'copy': "Analyse de couverture, installation de points d'accès, configuration des controleurs et optimisation pour bureaux, commerces, entrepots et immeubles multi-logements."},
        {'key': 'network-infrastructure', 'badge': 'IT', 'title': 'Solutions informatiques', 'copy': 'Serveurs, postes de travail, equipements reseau, soutien operationnel et infrastructure IT adaptee aux entreprises en croissance.'},
        {'key': 'security-camera-systems', 'badge': 'CCTV', 'title': 'Surveillance par camera', 'copy': 'Systemes de videosurveillance modernes pour proteger les batiments, les equipes et les operations avec un acces fiable aux images.'},
        {'key': 'access-control-systems', 'badge': 'ENTRY', 'title': "Intercom et controle d'acces", 'copy': 'Intercoms audio-video, lecteurs, gestion des portes et integration des entrees securisees pour les environnements professionnels.'},
    ],
}
T['en'].update({
    'home_kicker': 'Integrated technology infrastructure',
    'home_h1': 'Connect and secure business environments.',
    'home_intro': 'Opticable brings backbone cabling, professional WiFi, IT environments, surveillance, intercom, and secure entry into one clearer technical scope.',
    'home_points': [
        'Backbone cabling and structured pathways for cleaner growth',
        'Professional WiFi with stronger coverage and device strategy',
        'IT environments that support users, workstations, and operations',
        'Surveillance and access layers designed as one system',
        'Field-ready execution with a cleaner handoff into operations',
    ],
    'focus_chips': ['Structured cabling', 'Professional WiFi', 'IT environments', 'Camera systems', 'Secure entry'],
    'featured_title': 'Featured interventions',
    'featured_intro': 'Five high-impact service lines that bring structure, visibility, and control back into the technology environment.',
    'trust_title': 'Execution built for the field',
    'trust': [
        ('Site reading', 'We assess pathways, rooms, doors, coverage constraints, and building realities before proposing the right system mix.'),
        ('Multi-system coordination', 'Cabling, wireless, surveillance, access, and IT support are presented as connected layers, not isolated trades.'),
        ('Installation discipline', 'We emphasize cleaner room layouts, sharper detailing, and a stronger final presentation.'),
        ('Operational follow-through', 'The goal is not just installation, but a site that stays easier to support and evolve after commissioning.'),
    ],
    'services_h1': 'One partner to connect, structure, and secure your environment.',
    'services_intro': 'Opticable organizes its services around clear capability areas while staying focused on business technology infrastructure.',
    'extra_title': 'Operational layers',
    'extra_intro': 'Supporting work that often determines whether a technology environment stays clean, supportable, and scalable.',
    'about_h1': 'A team that connects the field, the infrastructure, and the operation.',
    'about_intro': 'Opticable approaches technology projects as operating environments, not just isolated installations. The objective is to make connectivity, secure entry, visibility, and day-to-day support work together with less friction.',
    'about_story': 'Opticable is positioned as a commercial technology partner with a focused service identity, grounded in practical delivery and approachable client communication.',
    'contact_h1': 'Start the next technology project with a clearer technical direction.',
    'contact_intro': 'Tell us what the site needs to do, what is already in place, and where the friction points are. We can help map the right mix of cabling, wireless, IT, and security layers.',
    'process_title': 'Deployment method',
    'process_intro': 'Analyze the site, shape the technical direction, execute cleanly, then hand off a supportable environment.',
    'clients_intro': 'Professional environments that need stronger technical structure without losing clarity.',
    'division_title': 'Three service poles',
    'division_intro': 'Opticable groups its work into three clear business-facing capability areas.',
})
T['fr'].update({
    'home_kicker': 'Infrastructure technologique intégrée',
    'home_h1': "Connecter et sécuriser les environnements d'affaires.",
    'home_intro': "Opticable regroupe backbone, câblage structuré, Wi-Fi professionnel, environnements IT, vidéosurveillance, intercom et gestion des accès dans une seule portée technique.",
    'home_points': [
        'Backbone et câblage structuré pour une croissance plus propre',
        "Wi-Fi professionnel avec une meilleure logique de couverture et d'usage",
        'Environnements IT qui soutiennent les usagers, les postes et les opérations',
        'Surveillance et accès pensés comme un seul système',
        "Exécution terrain avec une remise plus claire vers l'exploitation",
    ],
    'focus_chips': ['Câblage structuré', 'Wi-Fi professionnel', 'Environnements IT', 'Vidéosurveillance', 'Accès sécurisé'],
    'featured_title': 'Interventions clés',
    'featured_intro': "Cinq lignes de service à fort impact pour remettre de la structure, de la visibilité et du contrôle dans l'environnement technologique.",
    'trust_title': 'Une exécution pensée pour le terrain',
    'trust': [
        ('Lecture du site', "Nous analysons les cheminements, les locaux, les portes, la couverture et les contraintes réelles avant de proposer la bonne combinaison de systèmes."),
        ('Coordination multi-systèmes', "Câblage, sans-fil, surveillance, accès et IT sont présentés comme des couches connectées, pas comme des interventions isolées."),
        ("Discipline d'installation", "Nous mettons l'accent sur des locaux plus propres, un meilleur niveau de détail et une présentation finale plus forte."),
        ('Suivi opérationnel', "L'objectif n'est pas seulement d'installer, mais de livrer un site plus simple à supporter et à faire évoluer après la mise en service."),
    ],
    'services_h1': 'Un seul partenaire pour connecter, structurer et sécuriser votre environnement.',
    'services_intro': "Opticable présente ses services par pôles d'expertise, tout en restant centré sur l'infrastructure technologique pour entreprises.",
    'extra_title': 'Couches de support',
    'extra_intro': "Les travaux de soutien qui déterminent souvent si un environnement technologique reste propre, maintenable et évolutif.",
    'about_h1': "Une équipe qui relie le terrain, l'infrastructure et l'exploitation.",
    'about_intro': "Opticable aborde les projets technologiques comme des environnements d'exploitation, pas comme des installations isolées. Le but est de faire mieux fonctionner la connectivité, les accès, la visibilité et le soutien quotidien.",
    'about_story': "Opticable se positionne comme un partenaire technologique commercial avec une identité de service claire, ancré dans une exécution concrète et une relation client accessible.",
    'contact_h1': 'Lancez votre prochain projet technologique avec une direction plus claire.',
    'contact_intro': "Expliquez ce que le site doit accomplir, ce qui est déjà en place et où se trouvent les points de friction. Nous pouvons structurer le bon mélange de câblage, sans-fil, IT et sécurité.",
    'process_title': 'Méthode de déploiement',
    'process_intro': 'Analyser le site, définir la bonne direction technique, exécuter proprement, puis remettre un environnement plus simple à exploiter.',
    'clients_intro': 'Des environnements professionnels qui ont besoin de plus de structure technique sans perdre en clarté.',
    'division_title': 'Trois pôles de service',
    'division_intro': "Opticable regroupe ses services en trois zones de compétence plus lisibles pour un client d'affaires.",
})
home_visuals['en'] = {
    'eyebrow': 'Operational environments',
    'title': 'A more directional, more architectural presentation of Opticable.',
    'top_title': 'Commercial sites that need cleaner technical leadership',
    'top_copy': 'Positioning built around connectivity, supportability, and secure daily operations instead of isolated trade descriptions.',
    'top_alt': 'Professional property exterior representing a more corporate technology-services brand',
    'main_title': 'Structured backbone, cleaner rooms, stronger visibility',
    'main_copy': 'A visual language that combines field execution, organized infrastructure, and clearer system layering.',
    'main_alt': 'Structured rack and building technology environment with organized infrastructure',
}
home_visuals['fr'] = {
    'eyebrow': 'Environnements opérationnels',
    'title': "Des systèmes installés dans des environnements réels",
    'top_title': 'Immeubles commerciaux et multilogements',
    'top_copy': "Sécurité, accès et connectivité coordonnés dès le départ pour des bâtiments qui doivent fonctionner au quotidien.",
    'top_alt': 'Propriété professionnelle représentant une marque de services technologiques plus corporative',
    'main_title': 'Racks réseau, câblage structuré et locaux techniques',
    'main_copy': "Une infrastructure bien organisée, documentée et prête pour les ajouts futurs.",
    'main_alt': 'Rack structuré et environnement technologique de bâtiment avec infrastructure organisée',
}
SERVICE_CARD_META = {
    'structured-cabling': {'en': {'badge': 'CAB', 'eyebrow': 'Backbone'}, 'fr': {'badge': 'CAB', 'eyebrow': 'Backbone'}},
    'commercial-wifi-installation': {'en': {'badge': 'WIFI', 'eyebrow': 'Wireless layer'}, 'fr': {'badge': 'WIFI', 'eyebrow': 'Couche sans fil'}},
    'network-infrastructure': {'en': {'badge': 'IT', 'eyebrow': 'Operations'}, 'fr': {'badge': 'IT', 'eyebrow': 'Opérations'}},
    'managed-it-services': {'en': {'badge': 'IT', 'eyebrow': 'Managed support'}, 'fr': {'badge': 'IT', 'eyebrow': 'Soutien technique'}},
    'security-camera-systems': {'en': {'badge': 'CCTV', 'eyebrow': 'Visibility'}, 'fr': {'badge': 'CCTV', 'eyebrow': 'Visibilité'}},
    'access-control-systems': {'en': {'badge': 'ACCESS', 'eyebrow': 'Entry control'}, 'fr': {'badge': 'ACCESS', 'eyebrow': "Contrôle d'entrée"}},
    'intercom-systems': {'en': {'badge': 'COMMS', 'eyebrow': 'Entry communication'}, 'fr': {'badge': 'COMMS', 'eyebrow': "Communication d'entrée"}},
    'fiber-optic-installation': {'en': {'badge': 'FIBER', 'eyebrow': 'Capacity'}, 'fr': {'badge': 'FIBER', 'eyebrow': 'Capacité'}},
    'ip-phone-systems': {'en': {'badge': 'VOICE', 'eyebrow': 'Business voice'}, 'fr': {'badge': 'VOICE', 'eyebrow': "Voix d'affaires"}},
}
HOME_FEATURED_SERVICES = {
    'en': [
        {'key': 'structured-cabling', 'badge': 'CAB', 'eyebrow': 'Physical layer', 'title': 'Structured backbone', 'copy': 'The physical layer that keeps the environment organized, expandable, and easier to service.'},
        {'key': 'commercial-wifi-installation', 'badge': 'WIFI', 'eyebrow': 'Wireless network', 'title': 'Wireless performance', 'copy': 'Coverage, placement, and tuning shaped around real users, real density, and real building constraints.'},
        {'key': 'network-infrastructure', 'badge': 'IT', 'eyebrow': 'Managed systems', 'title': 'IT environments', 'copy': 'Servers, workstations, racks, and business systems presented as part of one practical operating stack.'},
        {'key': 'security-camera-systems', 'badge': 'CCTV', 'eyebrow': 'Surveillance', 'title': 'Site visibility', 'copy': 'Modern surveillance systems designed to improve control, traceability, and operational confidence.'},
        {'key': 'access-control-systems', 'badge': 'ACCESS', 'eyebrow': 'Entry management', 'title': 'Secure entry', 'copy': 'Access control, intercom logic, and managed visitor flow for professional environments.'},
    ],
    'fr': [
        {'key': 'structured-cabling', 'badge': 'CAB', 'eyebrow': 'Couche physique', 'title': 'Backbone structuré', 'copy': "La couche physique qui garde l'environnement organisé, évolutif et plus simple à maintenir."},
        {'key': 'commercial-wifi-installation', 'badge': 'WIFI', 'eyebrow': 'Réseau sans fil', 'title': 'Performance sans fil', 'copy': "Couverture, positionnement et optimisation pensés selon les usages réels, la densité et les contraintes du site."},
        {'key': 'network-infrastructure', 'badge': 'IT', 'eyebrow': 'Soutien informatique', 'title': 'Environnements IT', 'copy': "Serveurs, postes, racks et systèmes d'affaires présentés comme une seule pile opérationnelle cohérente."},
        {'key': 'security-camera-systems', 'badge': 'CCTV', 'eyebrow': 'Surveillance', 'title': 'Visibilité du site', 'copy': 'Des systèmes de surveillance modernes pour renforcer le contrôle, la traçabilité et la confiance opérationnelle.'},
        {'key': 'access-control-systems', 'badge': 'ACCESS', 'eyebrow': 'Entrées et visiteurs', 'title': 'Entrées sécurisées', 'copy': "Contrôle d'accès, logique intercom et parcours visiteurs mieux maîtrisés pour les environnements professionnels."},
    ],
}
SERVICE_DIVISION_GROUPS = {
    'en': [
        {'eyebrow': 'Pole 01', 'title': 'Connectivity and backbone', 'copy': 'The infrastructure that gives every other system a cleaner, more stable base.', 'keys': ['structured-cabling', 'fiber-optic-installation', 'commercial-wifi-installation']},
        {'eyebrow': 'Pole 02', 'title': 'IT and operations', 'copy': 'The layers that support users, workstations, telecom rooms, and day-to-day business continuity.', 'keys': ['managed-it-services', 'network-infrastructure', 'ip-phone-systems']},
        {'eyebrow': 'Pole 03', 'title': 'Security and entry', 'copy': 'The systems that control visibility, visitor flow, doors, and secure access across the site.', 'keys': ['security-camera-systems', 'access-control-systems', 'intercom-systems']},
    ],
    'fr': [
        {'eyebrow': 'Pôle 01', 'title': 'Connectivité et backbone', 'copy': "L'infrastructure qui donne aux autres systèmes une base plus propre et plus stable.", 'keys': ['structured-cabling', 'fiber-optic-installation', 'commercial-wifi-installation']},
        {'eyebrow': 'Pôle 02', 'title': 'IT et opérations', 'copy': 'Les couches qui soutiennent les usagers, les postes, les locaux télécom et la continuité des opérations.', 'keys': ['managed-it-services', 'network-infrastructure', 'ip-phone-systems']},
        {'eyebrow': 'Pôle 03', 'title': 'Sécurité et accès', 'copy': 'Les systèmes qui gèrent la visibilité, les visiteurs, les portes et les accès sécurisés sur le site.', 'keys': ['security-camera-systems', 'access-control-systems', 'intercom-systems']},
    ],
}
HOME_PANEL_FACTS = {
    'en': [('Field-led delivery', 'From planning to install'), ('Integrated scope', 'Connectivity, IT, security'), ('Business-ready', 'Built for live operations')],
    'fr': [('Exécution terrain', "De l'analyse à l'installation"), ('Portée intégrée', 'Connectivité, IT, sécurité'), ('Prêt à opérer', "Pensé pour des sites en activité")],
}

T['fr'].update({
    'about': 'À propos',
    'industries': 'Clientèle',
    'tagline': 'Technologie commerciale et systèmes du bâtiment',
    'quote': 'Obtenir une soumission',
    'all_services': 'Voir nos services',
    'company': "Opticable conçoit, installe et gère les systèmes technologiques des immeubles commerciaux, avec un soutien durable après la mise en service.",
    'footer': "Opticable installe et gère les systèmes technologiques des immeubles commerciaux à Montréal, Laval, Longueuil, sur la Rive-Sud, la Rive-Nord, dans les Laurentides et partout au Québec.",
    'home_title': "Caméras, accès, WiFi et câblage commercial | Opticable",
    'home_desc': "Opticable installe et gère caméras, accès, WiFi et câblage structuré pour immeubles commerciaux. Montréal, Laval, Longueuil et partout au Québec.",
    'home_kicker': 'Technologie commerciale et systèmes du bâtiment',
    'home_h1': "Caméras, contrôle d'accès, WiFi et câblage pour des bâtiments mieux gérés",
    'home_intro': "Opticable conçoit, installe et gère les systèmes technologiques des immeubles commerciaux et multilogements au Québec. Un seul partenaire pour la sécurité, l'accès, le WiFi et l'infrastructure réseau, de l'installation au soutien continu.",
    'home_points': [
        'Caméras IP pour entrées, stationnements et aires communes',
        "Contrôle d'accès et intercom pour portes, halls et visiteurs",
        'WiFi commercial pour bureaux, commerces et espaces partagés',
        'Câblage structuré, fibre, racks et locaux réseau',
    ],
    'focus_chips': ['Installation + soutien', 'Écosystème unifié', 'Bâtiments occupés', 'Portefeuilles multi-immeubles'],
    'featured_title': 'Nos services — installation, soutien et infrastructure',
    'featured_intro': "Nous installons, intégrons et gérons les systèmes technologiques des immeubles commerciaux. Un seul partenaire, du premier câble au soutien continu.",
    'trust_title': 'Pourquoi choisir Opticable',
    'home_trust_intro': "Nous ne faisons pas que remettre un équipement. Nous structurons des systèmes qui s'exploitent facilement, qui durent et qu'on peut faire évoluer sans repartir de zéro.",
    'trust': [
        ('Vision globale du bâtiment', "Accès, caméras, WiFi et réseau sont pensés ensemble dès le départ, pas raccordés en pièces détachées après coup."),
        ('Installations propres et durables', "Repérage, racks, finition et documentation sont traités avec rigueur pour livrer un système clair et durable."),
        ("Plus simple à exploiter", "Vos équipes héritent de systèmes mieux organisés, plus faciles à maintenir, à faire évoluer et à soutenir dans le temps."),
    ],
    'services_title': 'Services technologiques pour immeubles commerciaux | Opticable',
    'services_desc': "Installation et soutien de caméras, contrôle d'accès, WiFi, intercom, câblage structuré, fibre et réseau pour immeubles commerciaux au Québec.",
    'services_h1': "Installation et soutien pour les systèmes technologiques du bâtiment",
    'services_intro': "Opticable offre deux volets complémentaires: l'installation des systèmes et le soutien continu après la mise en service. On ne fait pas que livrer les équipements; on aide aussi à les gérer, les maintenir et les faire évoluer.",
    'priority_title': 'Services principaux',
    'priority_intro': "Les systèmes visibles au quotidien: sécurité, accès, communication d'entrée, WiFi et soutien informatique réseau.",
    'support_title': 'Infrastructure de soutien',
    'support_intro': "Le câblage, la fibre, les racks, les locaux techniques et la VoIP donnent la base nécessaire pour que les autres systèmes restent fiables.",
    'extra_title': "Avantages d'un partenaire unique",
    'extra_intro': "Ce qui fait la différence quand l'installation, le soutien et l'organisation de l'infrastructure restent coordonnés par la même équipe.",
    'extras': [
        ("Écosystème unifié", "Les caméras, l'intercom et le contrôle d'accès peuvent partager une seule plateforme de gestion pour surveiller, ouvrir et communiquer."),
        ('Soutien après installation', "On reste disponibles pour la maintenance, les ajustements, l'administration des systèmes et le support technique."),
        ('Documentation utile', "Repérage, organisation des racks et information de remise sont pensés pour les équipes qui devront exploiter le site."),
        ('Coordination de chantier', "On travaille avec les gestionnaires, promoteurs, entrepreneurs généraux et autres corps de métier sans compliquer le calendrier."),
    ],
    'about_title': "À propos d'Opticable | Installation commerciale au Québec",
    'about_desc': "Opticable installe et gère caméras, accès, WiFi et câblage pour immeubles commerciaux. Montréal, Laval et partout au Québec.",
    'about_h1': "Opticable, installateur et partenaire technologique pour les immeubles commerciaux",
    'about_intro': "Opticable est une entreprise québécoise spécialisée dans l'installation et la gestion de systèmes de sécurité, de contrôle d'accès, de WiFi et d'infrastructure réseau pour les immeubles commerciaux. On travaille avec les entreprises, les gestionnaires immobiliers, les promoteurs et les entrepreneurs qui ont besoin que les systèmes soient bien installés et bien gérés, du premier fil jusqu'au soutien continu.",
    'about_story': "On part du bâtiment, pas du catalogue. Chaque projet est analysé selon l'usage réel du site, les accès, les contraintes d'occupation et l'infrastructure déjà en place.",
    'contact_title': 'Contactez Opticable — Soumission et renseignements | Opticable',
    'contact_desc': "Demandez une soumission pour vos caméras, accès, WiFi et câblage commercial. Montréal, Laval, Longueuil et partout au Québec.",
    'contact_h1': 'Demander une soumission ou nous joindre',
    'contact_intro': "Décrivez-nous votre bâtiment, les systèmes visés et votre échéancier. On vous revient rapidement avec les prochaines étapes ou les questions nécessaires pour préciser votre demande.",
    'contact_info_title': 'Coordonnées directes',
    'contact_panel_title': 'Coordonnées directes',
    'contact_panel_copy': '',
    'contact_form_note': "On lit chaque demande et on vous répond dans les meilleurs délais. Pour les projets urgents, appelez-nous directement du lundi au vendredi.",
    'contact_cards': [
        ('Renseignements généraux', 'info@opticable.ca'),
        ('Demandes de soumission', 'soumissions@opticable.ca'),
        ('Téléphone', '514-316-7236'),
        ('Soumissions et renseignements', 'Lundi au vendredi 8 h à 17 h : par téléphone, courriel ou formulaire'),
        ('Fin de semaine', 'Samedi et dimanche 10 h à 16 h : par courriel ou formulaire seulement'),
        ('Support technique', 'Lundi au vendredi 8 h à 17 h · Samedi et dimanche 10 h à 16 h'),
    ],
    'service_area_eyebrow': 'Zone de service',
    'service_area_title': 'Zone de service',
    'service_area_intro': "Opticable dessert les immeubles commerciaux à Montréal, Laval, Longueuil, sur la Rive-Sud, la Rive-Nord, dans les Laurentides et partout au Québec.",
    'service_area_regions': ['Montréal', 'Laval', 'Longueuil', 'Rive-Sud', 'Rive-Nord', 'Laurentides', 'Et partout au Québec'],
    'industries_title': 'Clients, bâtiments et types de projets desservis | Opticable',
    'industries_desc': "Opticable installe et gère sécurité, WiFi et câblage pour bâtiments occupés, bâtiments neufs, nouveaux projets, entreprises et équipes immobilières au Québec.",
    'industries_h1': "Les équipes qui gèrent, construisent, rénovent et exploitent des bâtiments commerciaux",
    'industries_intro': "Opticable intervient dans les bâtiments occupés, les bâtiments neufs, les rénovations, les nouveaux projets, les chantiers actifs et les immeubles déjà en exploitation. Si votre contexte n'est pas listé, décrivez-nous le projet: on vous dira clairement si on peut vous aider.",
    'faq_title': 'Questions fréquentes sur nos services | Opticable',
    'faq_desc': "Réponses aux questions sur l'installation et la gestion de caméras, contrôle d'accès, WiFi et câblage pour immeubles commerciaux au Québec.",
    'faq_h1': 'Vous avez des questions sur nos services ou sur un projet ?',
    'faq_intro': "Voici les questions qu'on nous pose le plus souvent. Si vous ne trouvez pas ce que vous cherchez, contactez-nous directement.",
    'faq_panel_title': 'Questions fréquentes',
    'faq_panel_copy': "Réponses utiles sur les soumissions, l'installation, le soutien technique et les systèmes qu'on gère après la mise en service.",
    'clients_title': 'Des solutions adaptées aux réalités du terrain',
    'clients_intro': "Nous intervenons dans des bâtiments occupés, des bâtiments neufs, des nouveaux projets, des sites multi-usages et des environnements où la continuité des opérations est essentielle.",
    'clients': [
        ('Entreprises, bureaux et commerces', "Sécurité, WiFi, connectivité et systèmes d'entrée pour des opérations qui doivent rester stables au quotidien."),
        ('Immeubles multilogements', "Intercoms, accès, caméras, WiFi et câblage pour les aires communes, les halls et les environnements occupés."),
        ('Immeubles commerciaux à locataires multiples', "Systèmes du bâtiment pensés pour les espaces partagés, les locaux techniques et l'exploitation courante."),
        ('Gestionnaires immobiliers, promoteurs et entrepreneurs', 'Interlocuteur unique pour les mises à niveau, les bâtiments neufs, les nouveaux projets, la standardisation multi-immeubles et la coordination de chantier.'),
    ],
    'process_title': "Notre méthode d'installation",
    'process_intro': "Un projet bien livré commence par une bonne préparation.",
    'process': [
        ("Évaluation du site", "Nous analysons vos besoins, vos accès, vos zones sensibles et l'infrastructure en place."),
        ('Recommandation claire', "Vous recevez une proposition adaptée à votre bâtiment, votre budget et votre échéancier, sans surprise."),
        ('Installation propre', "Nos équipes installent, testent et identifient les composantes avec rigueur. Les lieux sont laissés propres."),
        ('Mise en service et soutien', "Nous validons le fonctionnement complet, vous remettons un système documenté et restons disponibles pour la gestion et le support continu."),
    ],
    'cta_kicker': 'Parlons de votre projet',
    'cta_title': "Besoin d'un partenaire technologique pour votre immeuble ?",
    'cta_copy': "Expliquez-nous votre bâtiment, les systèmes visés et votre échéancier. Nous vous reviendrons avec une proposition claire, adaptée à votre réalité. Opticable dessert les immeubles commerciaux à Montréal, Laval, Longueuil et partout au Québec.",
    'service_label': 'Voir le service',
    'footer_contact_title': 'Coordonnées',
    'footer_contact_intro': 'Joignez Opticable directement.',
    'division_title': 'Installation, soutien et infrastructure',
    'division_intro': "Opticable combine l'installation, la gestion continue et l'infrastructure de soutien pour livrer des systèmes plus cohérents.",
    'gateway_intro': "Opticable accompagne les immeubles commerciaux avec des systèmes de sécurité, d'accès, de WiFi et d'infrastructure réseau mieux coordonnés. Choisissez votre langue pour continuer.",
})

T['en'].update({
    'about': 'About',
    'industries': 'Who we serve',
    'tagline': 'Commercial technology and building systems',
    'quote': 'Request a quote',
    'all_services': 'View all services',
    'company': 'Opticable designs, installs, and manages building technology for commercial properties, with long-term support after commissioning.',
    'footer': 'Opticable installs and supports cameras, access, WiFi, intercom, cabling, and network infrastructure for commercial buildings in Montreal, Laval, Longueuil, and across Quebec.',
    'home_title': 'Commercial Cameras, Access, WiFi and Cabling | Opticable',
    'home_desc': 'Opticable installs cameras, access control, intercom, WiFi, and cabling for commercial buildings in Montreal, Laval, Longueuil, and across Quebec.',
    'home_kicker': 'Commercial technology and building systems',
    'home_h1': 'Commercial cabling, access control, WiFi, surveillance, and intercom for better-managed buildings',
    'home_intro': 'Opticable designs, installs, and manages security, access, WiFi, intercom, and network infrastructure for commercial and multi-tenant buildings across Quebec.',
    'home_points': [
        'IP cameras for entries, parking areas, and common spaces',
        'Access control and intercom for doors, lobbies, and visitors',
        'Commercial WiFi for offices, retail spaces, and shared areas',
        'Structured cabling, fiber, racks, and network rooms',
    ],
    'focus_chips': ['Installation + support', 'Unified ecosystem', 'Occupied buildings', 'Multi-building portfolios'],
    'featured_title': 'Our services, installation, support, and infrastructure',
    'featured_intro': 'We install, integrate, and manage building systems for commercial properties. One partner, from the first cable run through ongoing support.',
    'trust_title': 'Why choose Opticable',
    'home_trust_intro': 'We do not just hand over equipment. We organize systems that are easier to operate, built to last, and easier to expand without starting over.',
    'trust': [
        ('A building-wide view', 'Access control, cameras, WiFi, and the network are planned together from the start, not patched together afterward as separate systems.'),
        ('Clean, durable installations', 'Labeling, racks, finishing, and documentation are handled carefully so the final system is clear and durable.'),
        ('Easier to operate', 'Your team inherits systems that are better organized and easier to maintain, expand, and support over time.'),
    ],
    'services_title': 'Technology services for commercial buildings | Opticable',
    'services_desc': 'Installation and support for cameras, access control, WiFi, intercom, structured cabling, fiber, and network infrastructure for commercial buildings in Quebec.',
    'services_h1': 'Installation and support for building systems',
    'services_intro': 'Opticable offers two complementary sides: system installation and ongoing support after commissioning. We do not just deliver equipment; we also help manage, maintain, and expand it.',
    'priority_title': 'Core services',
    'priority_intro': 'The systems people rely on every day: security, entry, front-door communication, WiFi, and network IT support.',
    'support_title': 'Supporting infrastructure',
    'support_intro': 'Cabling, fiber, racks, technical rooms, and VoIP provide the foundation that keeps the other systems reliable.',
    'extra_title': 'Why a single partner helps',
    'extra_intro': 'What changes when installation, support, and infrastructure coordination stay with the same team.',
    'extras': [
        ('Unified ecosystem', 'Cameras, intercom, and access control can share one management platform to monitor, unlock, and communicate.'),
        ('Support after installation', 'We stay available for maintenance, adjustments, system administration, and technical support.'),
        ('Useful documentation', 'Labeling, rack organization, and handover information are prepared for the teams that will operate the site.'),
        ('Site coordination', 'We work with property managers, developers, general contractors, and other trades without complicating the schedule.'),
    ],
    'about_title': 'About Opticable | Commercial installation in Quebec',
    'about_desc': 'Opticable installs and manages cameras, access control, WiFi, intercom, and cabling for commercial buildings. Montreal, Laval, and across Quebec.',
    'about_h1': 'Opticable, installer and technology partner for commercial buildings',
    'about_intro': 'Opticable is a Quebec company specialized in the installation and management of security, access control, WiFi, intercom, and network infrastructure systems for commercial buildings. We work with businesses, property managers, developers, and contractors that need systems to be installed properly and managed properly, from the first cable through ongoing support.',
    'about_story': 'We start with the building, not the catalog. Every project is reviewed based on how the site is used, how people enter, occupancy constraints, and the infrastructure already in place.',
    'contact_title': 'Contact Opticable — Quotes and information | Opticable',
    'contact_desc': 'Request a quote for cameras, access control, WiFi, intercom, and commercial cabling. Montreal, Laval, Longueuil, and across Quebec.',
    'contact_h1': 'Request a quote or contact us',
    'contact_intro': 'Tell us about your building, the systems you need, and your timeline. We will get back to you quickly with the next steps or the questions needed to clarify your request.',
    'contact_info_title': 'Direct contact details',
    'contact_panel_title': 'Direct contact details',
    'contact_panel_copy': '',
    'contact_form_note': 'We review every request and respond as quickly as possible. For urgent projects, call us directly Monday to Friday.',
    'service_area_eyebrow': 'Service area',
    'service_area_title': 'Service area',
    'service_area_intro': 'Opticable serves commercial buildings in Montreal, Laval, Longueuil, the South Shore, the North Shore, the Laurentians, and across Quebec.',
    'service_area_regions': ['Montreal', 'Laval', 'Longueuil', 'South Shore', 'North Shore', 'Laurentians', 'And across Quebec'],
    'industries_title': 'Clients, Buildings and Project Types We Serve | Opticable',
    'industries_desc': 'Opticable installs and manages security, WiFi, and cabling for occupied buildings, new buildings, new projects, businesses, and property teams across Quebec.',
    'industries_h1': 'The teams that manage, build, renovate, and operate commercial buildings',
    'industries_intro': 'Opticable works in occupied buildings, new buildings, renovations, active construction sites, and properties already in operation. Our clients are the people who need the systems to work without unpleasant surprises.',
    'faq_title': 'Frequently asked questions about our services | Opticable',
    'faq_desc': 'Answers to common questions about installing and managing cameras, access control, WiFi, intercom, and cabling for commercial buildings in Quebec.',
    'faq_h1': 'Do you have questions about our services or a project?',
    'faq_intro': 'Here are the questions we hear most often. If you do not find what you need, contact us directly.',
    'faq_panel_title': 'Frequently asked questions',
    'faq_panel_copy': 'Useful answers about quotes, installation, technical support, and the systems we manage after commissioning.',
    'clients_title': 'Solutions shaped for real site conditions',
    'clients_intro': 'We work in occupied buildings, new buildings, new projects, mixed-use sites, and environments where continuity of operations matters.',
    'clients': [
        ('Businesses, offices, and retail spaces', 'Security, WiFi, connectivity, and entry systems for operations that need to stay stable every day.'),
        ('Multi-tenant buildings', 'Intercom, access control, cameras, WiFi, and cabling for common spaces, lobbies, and occupied environments.'),
        ('Commercial multi-tenant properties', 'Building systems planned for shared spaces, technical rooms, and day-to-day operations.'),
        ('Property managers and developers', 'One partner for upgrades, new building projects, multi-building standardization, and site coordination.'),
    ],
    'process_title': 'Our installation method',
    'process_intro': 'A well-delivered project starts with proper preparation.',
    'process': [
        ('Site evaluation', 'We review your needs, entries, sensitive areas, and the infrastructure already in place.'),
        ('Clear recommendation', 'You receive a proposal suited to your building, budget, and timeline, without surprises.'),
        ('Clean installation', 'Our teams install, test, and identify the components carefully. The site is left clean.'),
        ('Commissioning and support', 'We validate the full system, hand over a documented setup, and stay available for ongoing management and support.'),
    ],
    'cta_kicker': 'Let’s discuss your project',
    'cta_title': 'Need a technology partner for your building?',
    'cta_copy': 'Tell us about your building, the systems you need, and your timeline. We will come back with a clear proposal suited to your reality. Opticable serves commercial buildings in Montreal, Laval, Longueuil, and across Quebec.',
    'service_label': 'View service',
    'footer_contact_title': 'Contact details',
    'footer_contact_intro': 'Contact Opticable directly.',
    'division_title': 'Installation, support, and infrastructure',
    'division_intro': 'Opticable combines system installation, ongoing management, and supporting infrastructure to deliver more coherent systems.',
    'gateway_intro': 'Opticable supports commercial buildings with better-coordinated security, entry, WiFi, intercom, and network infrastructure. Choose your language to continue.',
})

T['en'].update({
    'blog': 'Blog',
    'articles': 'Articles',
    'guides': 'Guides',
    'case_studies': 'Case studies',
    'follow_us': 'Follow us',
    'view_case_study': 'View case study',
    'view_blog_posts': 'View articles',
    'contact_cards': [
        ('General inquiries', 'info@opticable.ca'),
        ('Quote requests', 'quotes@opticable.ca'),
        ('Technical support', 'support@opticable.ca'),
        ('Phone', '514-316-7236'),
        ('Quotes and inquiries', 'Monday to Friday, 8:00 AM to 5:00 PM: by phone, email, or form'),
        ('Weekends', 'Saturday and Sunday, 10:00 AM to 4:00 PM: by email or form only'),
        ('Technical support', 'Monday to Friday, 8:00 AM to 5:00 PM · Saturday and Sunday, 10:00 AM to 4:00 PM'),
    ],
})
T['fr'].update({
    'blog': 'Blogue',
    'articles': 'Articles',
    'guides': 'Guides',
    'case_studies': 'Études de cas',
    'follow_us': 'Suivez-nous',
    'view_case_study': "Voir l'étude de cas",
    'view_blog_posts': 'Voir les articles',
    'contact_cards': [
        ('Renseignements généraux', 'info@opticable.ca'),
        ('Demandes de soumission', 'soumissions@opticable.ca'),
        ('Support technique', 'support@opticable.ca'),
        ('Téléphone', '514-316-7236'),
        ('Soumissions et renseignements', 'Lundi au vendredi 8 h à 17 h : par téléphone, courriel ou formulaire'),
        ('Fin de semaine', 'Samedi et dimanche 10 h à 16 h : par courriel ou formulaire seulement'),
        ('Support technique', 'Lundi au vendredi 8 h à 17 h · Samedi et dimanche 10 h à 16 h'),
    ],
})

PROMO_START = datetime.fromisoformat(PROMO_CONFIG['startAt'])
PROMO_END = datetime.fromisoformat(PROMO_CONFIG['endAt'])
PROMO_ACTIVE = PROMO_START <= datetime.now(PROMO_START.tzinfo) <= PROMO_END
PROMO_SERVICE_KEYS = (
    'security-camera-systems',
    'access-control-systems',
    'commercial-wifi-installation',
    'structured-cabling',
)
PROMO_BLOG_KEYS = ('wifi-power', 'ip-cameras-network-upgrade', 'structured-cabling-foundation')

MONTH_NAMES = {
    'en': ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'),
    'fr': ('janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'),
}

PROMO_PAGE_CONTENT = {
    'en': {
        'label': 'Promo',
        'title': 'Quebec installation quote promo | Opticable',
        'desc': 'Enter your details, get an instant Opticable promo code, and apply it to a new installation quote in Quebec.',
        'hero_eyebrow': 'Quebec promo',
        'h1': 'Roll a promo code for your next installation quote.',
        'intro': 'Enter your details to get one promo code between 5% and 25% off. This is a limited-time offer and the code can be applied manually to an approved new Opticable installation quote in Quebec, up to the campaign cap.',
        'hero_panel_title': 'One entry, one code, your next quote.',
        'hero_panel_copy': 'Use the code on a cameras, access control, WiFi, intercom, structured cabling, or network infrastructure quote for a project in Quebec.',
        'hero_points': [
            'Instant result after one form submission',
            'Code validity linked to the campaign rules',
            'Optional marketing consent kept separate from quote follow-up',
            'Manual code redemption on qualifying new installation quotes',
        ],
        'how_title': 'How the promo works',
        'how_intro': 'Enter your details, get your code, and continue to the quote form.',
        'how_steps': [
            ('Enter your details', 'Add your name and email. Phone and company are optional.'),
            ('Get your code', 'Answer the quick question and receive your promo code.'),
            ('Go to the quote form', 'Open the quote form and paste in your code when you are ready.'),
        ],
        'form_eyebrow': 'Enter once',
        'form_title': 'Get your promo code',
        'form_intro': 'Required fields are limited to what is needed to assign one code and connect it to your quote request.',
        'contact_note': 'After submission, your code will appear here in a popup so you can copy or save it.',
        'fields': {
            'name': 'Name',
            'email': 'Email',
            'phone': 'Phone (optional)',
            'company': 'Company (optional)',
            'skill': 'Skill-testing question',
        },
        'consents': {
            'quebec': 'I confirm the project property is in Quebec.',
            'rules': 'I have read and accept the promo rules and privacy terms.',
            'marketing': 'I agree to receive marketing emails from Opticable. This is optional and not required to enter.',
        },
        'submit': 'Roll my promo code',
        'submit_loading': 'Rolling...',
        'status_loading': 'Loading campaign availability...',
        'status_unavailable': 'The promo is not available right now. You can still request a quote directly.',
        'existing_title': 'Your promo code is ready',
        'existing_copy': 'Copy this code and paste it into your quote request when you are ready.',
        'result_title': 'Your promo code is ready',
        'result_copy': 'Copy this code now and paste it into your quote request.',
        'duplicate_title': 'Your promo code is already assigned',
        'duplicate_copy': 'This email already has a code for the current campaign. Retrieve it below.',
        'result_labels': {
            'discount': 'Discount',
            'code': 'Promo code',
            'expires': 'Valid until',
        },
        'actions': {
            'quote': 'Request your quote!',
            'rules': 'Review the promo rules',
            'rules_inline': 'Promo rules',
            'copy_code': 'Copy code',
            'copied_code': 'Copied',
            'save_code': 'Save code',
            'saved_code': 'Saved',
            'close_modal': 'Close',
        },
        'faq_intro': 'Useful answers before submitting a promo entry.',
        'faqs': [
            ('Does this replace the normal quote review?', 'No. The code is attached to the existing quote process. The team still reviews scope, eligibility, exclusions, and project fit before applying any discount.'),
            ('Can I reroll with the same email?', 'No. The campaign stores one result per email address and returns the original result on later submissions.'),
            ('Do I need to agree to marketing emails to enter?', 'No. Marketing consent is optional and separate from the required campaign confirmations.'),
            ('Can the code be used on support or managed service work?', 'No. The campaign is limited to qualifying new installation quotes and excludes recurring services, support calls, taxes, and already discounted work.'),
        ],
        'rules_title': 'Promo rules | Opticable',
        'rules_desc': 'Official rules for the Opticable Quebec promo campaign, including eligibility, odds, discount limits, and redemption rules.',
        'rules_h1': 'Official promo rules',
        'rules_intro': 'Read these terms before submitting an entry. The promo is intended for Quebec projects and is tied to Opticable’s quote review process.',
        'unsubscribe_title': 'Marketing email unsubscribe | Opticable',
        'unsubscribe_desc': 'Withdraw optional marketing consent for Opticable promotional emails without affecting quote-related follow-up.',
        'unsubscribe_h1': 'Withdraw marketing email consent',
        'unsubscribe_intro': 'Use the same email address you used for the promo entry. Withdrawing marketing consent does not remove service or quote-related operational follow-up.',
        'unsubscribe_button': 'Withdraw marketing consent',
        'unsubscribe_success': 'Marketing consent has been withdrawn for this email address.',
        'unsubscribe_note': 'You can still contact Opticable directly or request a quote after unsubscribing.',
        'reminder_eyebrow': 'Promo code ready',
        'reminder_title': 'Add this code to your quote request.',
        'reminder_copy': 'Your promo code is already saved and ready to use.',
        'cta_eyebrow': 'Promo',
        'cta_title': 'Limited-time offer: lock in a promo code before requesting a quote.',
        'cta_copy': 'Use the promo entry page to collect your one-time code before the campaign ends, then continue into the normal quote flow with a better-qualified lead.',
        'cta_button': 'View the promo page',
    },
    'fr': {
        'label': 'Promo',
        'title': 'Promo pour soumission d’installation au Québec | Opticable',
        'desc': "Entrez vos coordonnées, obtenez un code promo instantané Opticable et appliquez-le à une nouvelle soumission d'installation au Québec.",
        'hero_eyebrow': 'Promo Québec',
        'h1': 'Roulez un code promo pour votre prochaine soumission d’installation.',
        'intro': "Entrez vos coordonnées pour avoir un code promo entre 5 % et 25 %. Il s'agit d'une offre à durée limitée, applicable manuellement à une nouvelle soumission d'installation Opticable admissible au Québec, jusqu'au plafond de la campagne.",
        'hero_panel_title': 'Une entrée, un code, votre prochaine soumission.',
        'hero_panel_copy': "Utilisez ce code pour une demande de caméras, de contrôle d'accès, de WiFi, d'intercom, de câblage structuré ou d'infrastructure réseau liée à un projet au Québec.",
        'hero_points': [
            'Résultat instantané après une seule soumission',
            'Validité du code liée au règlement officiel',
            "Consentement marketing optionnel et séparé du suivi de soumission",
            "Utilisation manuelle du code sur les nouvelles soumissions d'installation admissibles",
        ],
        'how_title': 'Comment la promo fonctionne',
        'how_intro': "Entrez vos coordonnées, obtenez votre code, puis poursuivez vers le formulaire de soumission.",
        'how_steps': [
            ('Entrez vos coordonnées', "Ajoutez votre nom et votre courriel. Le téléphone et l'entreprise sont optionnels."),
            ('Obtenez votre code', "Répondez à la question et recevez votre code promo."),
            ('Passez à la soumission', "Ouvrez le formulaire de soumission et collez votre code quand vous serez prêt."),
        ],
        'form_eyebrow': 'Une seule entrée',
        'form_title': 'Obtenir votre code promo',
        'form_intro': "Les champs requis servent simplement à attribuer un seul code et à le rattacher à votre demande de soumission.",
        'contact_note': "",
        'fields': {
            'name': 'Nom',
            'email': "Courriel",
            'phone': 'Téléphone (optionnel)',
            'company': 'Entreprise (optionnel)',
            'skill': "Question d'habileté",
        },
        'consents': {
            'quebec': "Je confirme que la propriété visée par le projet se trouve au Québec.",
            'rules': "J'ai lu et j'accepte le règlement promo et les modalités de confidentialité.",
            'marketing': "J'accepte de recevoir des courriels marketing d'Opticable. Ce choix est optionnel et non requis pour participer.",
        },
        'submit': 'Obtenir mon code',
        'submit_loading': 'Traitement...',
        'status_loading': 'Chargement de la disponibilité de la campagne...',
        'status_unavailable': "La promo n'est pas disponible pour le moment. Vous pouvez tout de même demander une soumission directement.",
        'existing_title': 'Votre code promo est prêt',
        'existing_copy': 'Copiez ce code et collez-le dans votre demande de soumission quand vous serez prêt.',
        'result_title': 'Votre code promo est prêt',
        'result_copy': "Copiez ce code maintenant et collez-le dans votre demande de soumission.",
        'duplicate_title': 'Votre code promo est déjà attribué',
        'duplicate_copy': "Cette adresse courriel possède déjà un code pour la campagne en cours. Récupérez-le ci-dessous.",
        'result_labels': {
            'discount': 'Rabais',
            'code': 'Code promo',
            'expires': "Valide jusqu'au",
        },
        'actions': {
            'quote': 'Demander votre soumission!',
            'rules': 'Consulter le règlement promo',
            'rules_inline': 'Règlement promo',
            'copy_code': 'Copier le code',
            'copied_code': 'Code copié',
            'save_code': 'Enregistrer le code',
            'saved_code': 'Code enregistré',
            'close_modal': 'Fermer',
        },
        'faq_intro': 'Réponses utiles avant de soumettre une entrée promotionnelle.',
        'faqs': [
            ("Est-ce que cela remplace l'analyse normale de la soumission ?", "Non. Le code est rattaché au processus de soumission existant. L'équipe valide toujours la portée, l'admissibilité, les exclusions et la pertinence du projet avant d'appliquer un rabais."),
            ('Puis-je rerouler avec le même courriel ?', "Non. La campagne conserve un seul résultat par adresse courriel et retourne le résultat original lors des soumissions suivantes."),
            ('Dois-je accepter les courriels marketing pour participer ?', "Non. Le consentement marketing est optionnel et séparé des confirmations obligatoires de la campagne."),
            ("Le code peut-il être appliqué à du soutien ou à des services récurrents ?", "Non. La campagne vise seulement les nouvelles soumissions d'installation admissibles et exclut les services récurrents, les appels de soutien, les taxes et les travaux déjà escomptés."),
        ],
        'rules_title': 'Règlement promo | Opticable',
        'rules_desc': "Règlement officiel de la campagne promo Opticable au Québec, incluant l'admissibilité, les probabilités, les plafonds de rabais et les règles d'utilisation.",
        'rules_h1': 'Règlement officiel de la promo',
        'rules_intro': "Lisez ces conditions avant de soumettre une entrée. La promo vise les projets au Québec et reste rattachée au processus d'analyse des soumissions d'Opticable.",
        'unsubscribe_title': 'Désabonnement des courriels marketing | Opticable',
        'unsubscribe_desc': "Retirez le consentement optionnel aux courriels marketing d'Opticable sans affecter les suivis liés aux soumissions ou aux services.",
        'unsubscribe_h1': 'Retirer le consentement marketing',
        'unsubscribe_intro': "Utilisez la même adresse courriel que celle soumise pour la promo. Le retrait du consentement marketing n'enlève pas les suivis opérationnels liés à une soumission ou à un service.",
        'unsubscribe_button': 'Retirer mon consentement marketing',
        'unsubscribe_success': "Le consentement marketing a été retiré pour cette adresse courriel.",
        'unsubscribe_note': "Vous pouvez toujours contacter Opticable directement ou demander une soumission après le désabonnement.",
        'reminder_eyebrow': 'Code promo prêt',
        'reminder_title': 'Ajoutez ce code dans votre soumission.',
        'reminder_copy': "Votre code promo est déjà prêt à utiliser.",
        'cta_eyebrow': 'Promo',
        'cta_title': 'Offre à durée limitée : obtenez un code avant de demander une soumission.',
        'cta_copy': "Passez par la page promo pour obtenir votre code unique avant la fin de la campagne, puis poursuivez vers le processus normal de soumission.",
        'cta_button': 'Voir la page promo',
    },
}

PROMO_ADMIN_CONTENT = {
    'en': {
        'label': 'Promo admin',
        'title': 'Promo leads admin | Opticable',
        'desc': 'Protected Opticable admin page to review promo leads and export CSV files.',
        'eyebrow': 'Protected promo admin',
        'h1': 'Promo leads dashboard',
        'intro': 'Review the latest promo entries, switch between the current campaign and all campaigns, and export the records as CSV.',
        'panel_title': 'What this page shows',
        'panel_copy': 'This page stays out of search and is protected before it loads. Use it to inspect incoming leads without opening D1 manually.',
        'panel_points': [
            'Latest entries visible in the browser',
            'Toggle between the current campaign and all campaigns',
            'Download a CSV export whenever you need it',
        ],
        'scope_label': 'View',
        'scope_current': 'Current campaign',
        'scope_all': 'All campaigns',
        'refresh': 'Refresh',
        'export_entries': 'Export entries CSV',
        'export_subscribers': 'Export subscribers CSV',
        'delete_selected': 'Delete selected',
        'delete_view': 'Delete current view',
        'delete_view_all': 'Delete all campaigns',
        'select_all': 'Select all visible entries',
        'summary': {
            'entries': 'Entries',
            'marketing': 'Marketing opt-ins',
            'recent': 'Last 7 days',
            'latest': 'Latest entry',
            'current_campaign': 'Current campaign',
            'campaign_window': 'Campaign window',
            'active_view': 'Active view',
        },
        'table': {
            'received': 'Received',
            'select': 'Select',
            'campaign': 'Campaign',
            'name': 'Name',
            'email': 'Email',
            'phone': 'Phone',
            'company': 'Company',
            'discount': 'Discount',
            'code': 'Promo code',
            'expires': 'Valid until',
            'marketing': 'Marketing',
            'attribution': 'Attribution',
        },
        'loading': 'Loading promo entries...',
        'load_error': 'The promo entries could not be loaded right now.',
        'empty': 'No promo entries are available for this view yet.',
        'marketing_yes': 'Opted in',
        'marketing_no': 'No',
        'marketing_out': 'Opted out',
        'none': '—',
        'delete_error': 'The selected promo entries could not be deleted right now.',
        'delete_none': 'Select at least one promo entry first.',
        'delete_selected_confirm': 'Delete the selected promo entries permanently?',
        'delete_view_confirm': 'Delete every promo entry in the current view permanently?',
        'delete_selected_success': 'Selected promo entries were deleted.',
        'delete_view_success': 'The current view was deleted.',
    },
    'fr': {
        'label': 'Admin promo',
        'title': 'Admin des leads promo | Opticable',
        'desc': "Page d'administration protégée d'Opticable pour consulter les leads promo et exporter des fichiers CSV.",
        'eyebrow': 'Admin promo protégé',
        'h1': 'Tableau des leads promo',
        'intro': "Consultez les dernières entrées promo, basculez entre la campagne en cours et l'ensemble des campagnes, puis exportez les données en CSV.",
        'panel_title': 'Ce que cette page affiche',
        'panel_copy': "Cette page reste hors recherche et protégée avant son chargement. Utilisez-la pour consulter les leads entrants sans ouvrir D1 manuellement.",
        'panel_points': [
            "Les dernières entrées visibles dans le navigateur",
            "Un basculement entre la campagne en cours et toutes les campagnes",
            "Un export CSV téléchargeable au besoin",
        ],
        'scope_label': 'Vue',
        'scope_current': 'Campagne en cours',
        'scope_all': 'Toutes les campagnes',
        'refresh': 'Actualiser',
        'export_entries': 'Exporter les entrées CSV',
        'export_subscribers': 'Exporter les abonnés CSV',
        'delete_selected': 'Supprimer la sélection',
        'delete_view': 'Supprimer la vue active',
        'delete_view_all': 'Supprimer toutes les campagnes',
        'select_all': 'Sélectionner toutes les entrées visibles',
        'summary': {
            'entries': 'Entrées',
            'marketing': 'Consentements marketing',
            'recent': '7 derniers jours',
            'latest': 'Dernière entrée',
            'current_campaign': 'Campagne active',
            'campaign_window': 'Période',
            'active_view': 'Vue active',
        },
        'table': {
            'received': 'Reçue le',
            'select': 'Sélection',
            'campaign': 'Campagne',
            'name': 'Nom',
            'email': 'Courriel',
            'phone': 'Téléphone',
            'company': 'Entreprise',
            'discount': 'Rabais',
            'code': 'Code promo',
            'expires': "Valide jusqu'au",
            'marketing': 'Marketing',
            'attribution': 'Attribution',
        },
        'loading': 'Chargement des entrées promo...',
        'load_error': "Les entrées promo n'ont pas pu être chargées pour le moment.",
        'empty': "Aucune entrée promo n'est encore disponible pour cette vue.",
        'marketing_yes': 'Inscrit',
        'marketing_no': 'Non',
        'marketing_out': 'Désabonné',
        'none': '—',
        'delete_error': "Les entrées promo sélectionnées n'ont pas pu être supprimées pour le moment.",
        'delete_none': "Sélectionnez d'abord au moins une entrée promo.",
        'delete_selected_confirm': 'Supprimer définitivement les entrées promo sélectionnées ?',
        'delete_view_confirm': 'Supprimer définitivement toutes les entrées de la vue active ?',
        'delete_selected_success': 'Les entrées promo sélectionnées ont été supprimées.',
        'delete_view_success': 'La vue active a été supprimée.',
    },
}

HOME_POINT_KEYS = (
    'security-camera-systems',
    'access-control-systems',
    'commercial-wifi-installation',
    'structured-cabling',
)

SERVICE_CARD_META['security-camera-systems']['fr'] = {'badge': 'CCTV', 'eyebrow': 'Sécurité'}
SERVICE_CARD_META['access-control-systems']['fr'] = {'badge': 'ACCESS', 'eyebrow': 'Accès'}
SERVICE_CARD_META['commercial-wifi-installation']['fr'] = {'badge': 'WIFI', 'eyebrow': 'Sans fil'}
SERVICE_CARD_META['intercom-systems']['fr'] = {'badge': 'INTERCOM', 'eyebrow': 'Entrées'}
SERVICE_CARD_META['network-infrastructure']['fr'] = {'badge': 'IT', 'eyebrow': 'Support réseau'}
SERVICE_CARD_META['managed-it-services']['fr'] = {'badge': 'IT', 'eyebrow': 'Soutien continu'}
SERVICE_CARD_META['structured-cabling']['fr'] = {'badge': 'CAB', 'eyebrow': 'Câblage'}
SERVICE_CARD_META['fiber-optic-installation']['fr'] = {'badge': 'FIBER', 'eyebrow': 'Backbone'}
SERVICE_CARD_META['ip-phone-systems']['fr'] = {'badge': 'VOIP', 'eyebrow': 'Voix'}

HOME_FEATURED_SERVICES['fr'] = [
    {'key': 'security-camera-systems', 'badge': 'CCTV', 'title': 'Caméras de sécurité', 'copy': "Installation, configuration, visionnement à distance et soutien des caméras IP pour entrées, stationnements et aires communes."},
    {'key': 'access-control-systems', 'badge': 'ACCESS', 'title': "Contrôle d'accès", 'copy': "Lecteurs, serrures, panneaux et câblage de porte pour mieux gérer les entrées, les halls et les zones restreintes."},
    {'key': 'commercial-wifi-installation', 'badge': 'WIFI', 'title': 'WiFi commercial', 'copy': "Planification de couverture, points d'accès professionnels, maintenance et soutien pour bureaux, commerces et espaces partagés."},
    {'key': 'intercom-systems', 'badge': 'INTERCOM', 'title': 'Intercom', 'copy': "Intercom audio ou vidéo pour halls, portails et accès visiteurs, avec intégration au contrôle d'accès et au réseau."},
    {'key': 'managed-it-services', 'badge': 'IT', 'title': 'Services informatiques', 'copy': "Gestion de parc, soutien réseau, maintenance et support technique pour vos environnements après l'installation."},
    {'key': 'ip-phone-systems', 'badge': 'VOIP', 'title': 'Téléphonie IP', 'copy': "Lignes SIP, postes IP, numéros d'affaires et câblage prêt pour la VoIP pour vos bureaux et espaces de travail."},
    {'key': 'structured-cabling', 'badge': 'CAB', 'title': 'Câblage structuré', 'copy': "Cat 5e, Cat 6, Cat 6A, coaxial, patch panels, tests et documentation pour une base réseau propre et durable."},
]

SERVICE_DIVISION_GROUPS['fr'] = [
    {'eyebrow': 'Volet 01', 'title': 'Installation des systèmes', 'copy': "Caméras, contrôle d'accès, intercom et WiFi installés selon la réalité du bâtiment, des accès et des occupants.", 'keys': ['security-camera-systems', 'access-control-systems', 'intercom-systems', 'commercial-wifi-installation']},
    {'eyebrow': 'Volet 02', 'title': 'Infrastructure de soutien', 'copy': 'Câblage structuré, fibre optique, racks, patch panels, téléphonie IP et locaux techniques pour donner une base propre au site.', 'keys': ['structured-cabling', 'fiber-optic-installation', 'network-infrastructure', 'ip-phone-systems']},
    {'eyebrow': 'Volet 03', 'title': 'Gestion et soutien continu', 'copy': "Maintenance, support technique, administration des systèmes et ajustements après la mise en service pour éviter de repartir de zéro.", 'keys': ['security-camera-systems', 'access-control-systems', 'commercial-wifi-installation', 'network-infrastructure']},
]

HOME_PANEL_FACTS['fr'] = [
    ('Installation', 'Systèmes et infrastructure'),
    ('Soutien continu', 'Gestion, maintenance, support'),
    ('Territoire', 'Montréal, Laval, Longueuil et partout au Québec'),
]

home_visuals['en'] = {
    'eyebrow': 'Operating environments',
    'title': 'Systems installed in real operating environments',
    'top_title': 'Commercial and multi-tenant buildings',
    'top_copy': 'Security, entry systems, and connectivity coordinated from the start for buildings that need to operate every day.',
    'top_alt': 'Commercial property representing coordinated security and connectivity systems',
    'main_title': 'Network racks, structured cabling, and technical rooms',
    'main_copy': 'Infrastructure that is organized, documented, and ready for future additions.',
    'main_alt': 'Structured rack and building technology environment with organized infrastructure',
}

SERVICE_CARD_META['security-camera-systems']['en'] = {'badge': 'CCTV', 'eyebrow': 'Security'}
SERVICE_CARD_META['access-control-systems']['en'] = {'badge': 'ACCESS', 'eyebrow': 'Access'}
SERVICE_CARD_META['commercial-wifi-installation']['en'] = {'badge': 'WIFI', 'eyebrow': 'Wireless'}
SERVICE_CARD_META['intercom-systems']['en'] = {'badge': 'INTERCOM', 'eyebrow': 'Entry'}
SERVICE_CARD_META['network-infrastructure']['en'] = {'badge': 'IT', 'eyebrow': 'Network support'}
SERVICE_CARD_META['managed-it-services']['en'] = {'badge': 'IT', 'eyebrow': 'Ongoing support'}
SERVICE_CARD_META['structured-cabling']['en'] = {'badge': 'CAB', 'eyebrow': 'Cabling'}
SERVICE_CARD_META['fiber-optic-installation']['en'] = {'badge': 'FIBER', 'eyebrow': 'Backbone'}
SERVICE_CARD_META['ip-phone-systems']['en'] = {'badge': 'VOIP', 'eyebrow': 'Voice'}

HOME_FEATURED_SERVICES['en'] = [
    {'key': 'security-camera-systems', 'badge': 'CCTV', 'title': 'Security cameras', 'copy': 'Installation, configuration, remote viewing, and support for IP cameras covering entries, parking areas, and common spaces.'},
    {'key': 'access-control-systems', 'badge': 'ACCESS', 'title': 'Access control', 'copy': 'Readers, locks, panels, and door cabling to manage entries, lobbies, and restricted areas more effectively.'},
    {'key': 'commercial-wifi-installation', 'badge': 'WIFI', 'title': 'Commercial WiFi', 'copy': 'Coverage planning, professional access points, maintenance, and support for offices, retail spaces, and shared environments.'},
    {'key': 'intercom-systems', 'badge': 'INTERCOM', 'title': 'Intercom', 'copy': 'Audio or video intercom systems for lobbies, gates, and visitor entry points, integrated with access control and the network.'},
    {'key': 'managed-it-services', 'badge': 'IT', 'title': 'IT services', 'copy': 'Device management, network support, maintenance, and technical support for your environment after installation.'},
    {'key': 'ip-phone-systems', 'badge': 'VOIP', 'title': 'IP telephony', 'copy': 'SIP lines, IP handsets, business numbers, and VoIP-ready cabling for offices and workspaces.'},
    {'key': 'structured-cabling', 'badge': 'CAB', 'title': 'Structured cabling', 'copy': 'Cat 5e, Cat 6, Cat 6A, coaxial, patch panels, testing, and documentation for a clean, durable network foundation.'},
]

SERVICE_DIVISION_GROUPS['en'] = [
    {'eyebrow': 'Service line 01', 'title': 'System installation', 'copy': 'Cameras, access control, intercom, and WiFi installed around the reality of the building, its entries, and its occupants.', 'keys': ['security-camera-systems', 'access-control-systems', 'intercom-systems', 'commercial-wifi-installation']},
    {'eyebrow': 'Service line 02', 'title': 'Supporting infrastructure', 'copy': 'Structured cabling, fiber optic links, racks, patch panels, IP telephony, and technical rooms that give the site a clean foundation.', 'keys': ['structured-cabling', 'fiber-optic-installation', 'network-infrastructure', 'ip-phone-systems']},
    {'eyebrow': 'Service line 03', 'title': 'Ongoing management and support', 'copy': 'Maintenance, technical support, system administration, and post-installation adjustments so you do not have to start from zero when needs change.', 'keys': ['security-camera-systems', 'access-control-systems', 'commercial-wifi-installation', 'network-infrastructure']},
]

HOME_PANEL_FACTS['en'] = [
    ('Installation', 'Systems and infrastructure'),
    ('Ongoing support', 'Management, maintenance, support'),
    ('Territory', 'Montreal, Laval, Longueuil, and across Quebec'),
]

services['security-camera-systems']['en'].update({
    'name': 'Security cameras',
    'title': 'Security cameras for commercial buildings | Opticable',
    'desc': 'Installation and management of IP cameras, NVRs, and surveillance systems for commercial buildings. Montreal, Laval, Longueuil, and across Quebec.',
    'hero': 'Security cameras for commercial buildings and business environments',
    'intro': 'Opticable installs and manages IP camera systems for commercial buildings, multi-tenant properties, and business environments. Every project is planned around your sensitive areas, access points, and operating requirements, with ongoing support after commissioning.',
    'summary': 'IP cameras, PoE, NVRs, remote viewing, and ongoing support to protect sensitive areas, common spaces, perimeters, and entries.',
    'related': ['access-control-systems', 'intercom-systems', 'structured-cabling'],
})
services['access-control-systems']['en'].update({
    'name': 'Access control',
    'title': 'Access control for commercial buildings | Opticable',
    'desc': 'Installation and management of access control, readers, panels, and door cabling for commercial buildings. Montreal, Laval, and across Quebec.',
    'hero': 'Access control for buildings, lobbies, and secured spaces',
    'intro': 'Opticable installs and manages access control systems for commercial buildings, multi-tenant properties, and business environments. Readers, control panels, electronic locks, and door cabling are planned, installed, and supported for reliable long-term entry management.',
    'summary': 'Readers, locks, panels, door cabling, and ongoing access administration for lobbies, entries, and restricted areas.',
    'related': ['intercom-systems', 'security-camera-systems', 'structured-cabling'],
})
services['commercial-wifi-installation']['en'].update({
    'name': 'Commercial WiFi',
    'title': 'Commercial WiFi for Offices and Buildings | Opticable',
    'desc': 'Design, installation, management, and maintenance of commercial WiFi for offices and buildings. Montreal, Laval, Longueuil, and across Quebec.',
    'hero': 'Commercial WiFi for offices, buildings, and shared spaces',
    'intro': 'Opticable designs and installs the building-side WiFi infrastructure that commercial and multi-tenant properties depend on. Access-point placement, coverage logic, cabling, PoE, switching, and the network foundation behind the wireless layer are planned together so the signal stays useful in real building conditions.',
    'summary': 'WiFi quality, access points, coverage planning, cabling, and network foundations for commercial buildings.',
    'related': ['structured-cabling', 'network-infrastructure', 'access-control-systems'],
})
services['intercom-systems']['en'].update({
    'name': 'Intercom',
    'title': 'Intercom systems for commercial buildings | Opticable',
    'desc': 'Installation of audio and video intercom systems for lobbies, gates, and commercial buildings. Montreal, Laval, Longueuil, and across Quebec.',
    'hero': 'Intercom systems for lobbies, gates, and occupied buildings',
    'intro': 'Opticable installs audio and video intercom systems for lobbies, gates, and visitor entries in commercial and multi-tenant buildings. Coordinated with access control, cameras, and the network for entry communication that is reliable, well integrated, and easy to manage.',
    'summary': 'Audio or video intercom systems for lobbies, gates, and visitor entries, integrated with access control and the network.',
    'related': ['access-control-systems', 'security-camera-systems', 'network-infrastructure'],
})
services['structured-cabling']['en'].update({
    'name': 'Structured cabling',
    'title': 'Structured cabling for commercial buildings | Opticable',
    'desc': 'Installation of Cat 6, Cat 6A, coaxial, and fiber-ready structured cabling for commercial buildings. Montreal, Laval, Longueuil, and across Quebec.',
    'hero': 'Structured cabling for commercial buildings and business environments',
    'intro': 'Opticable installs the structured cabling that supports WiFi access points, cameras, access control, intercom, telephony, and the rest of the building network. The goal is a clean, organized, documented foundation that stays easier to support and expand.',
    'summary': 'Cat 5e, Cat 6, Cat 6A, coaxial, patch panels, testing, and documentation for a clean building network base.',
    'related': ['fiber-optic-installation', 'network-infrastructure', 'commercial-wifi-installation'],
})
services['fiber-optic-installation']['en'].update({
    'name': 'Fiber optic',
    'title': 'Fiber Optic for Commercial Buildings | Opticable',
    'desc': 'Fiber optic links, risers, and service extensions for commercial buildings. Montreal, Laval, Longueuil, and across Quebec.',
    'hero': 'Fiber optic installation for commercial buildings and multi-storey sites',
    'intro': 'Opticable installs fiber optic links that tie together the main network room, floor-level cabinets, and the distant parts of a building when copper alone is no longer the cleanest answer. That backbone supports WiFi, security, access, and the rest of the building network.',
    'summary': 'Backbone links between floors, network rooms, and distant zones when capacity or distance outgrows copper.',
    'related': ['structured-cabling', 'network-infrastructure', 'security-camera-systems'],
})
services['network-infrastructure']['en'].update({
    'name': 'Network infrastructure',
    'title': 'Network infrastructure for commercial buildings | Opticable',
    'desc': 'Installation of racks, patch panels, and technical rooms for commercial buildings. Montreal, Laval, Longueuil, and across Quebec.',
    'hero': 'Network infrastructure for commercial buildings, including racks, technical rooms, and internet handoff organization',
    'intro': 'Opticable installs and organizes the network infrastructure of commercial buildings: the main network room, floor-level cabinets when needed, rack organization, patch panels, internet handoffs, and cleanup of existing technical rooms. This is the base that keeps WiFi and the other building systems coherent.',
    'summary': 'Main network rooms, racks, patch panels, handoffs, and clean distribution for building systems that are easier to operate.',
    'related': ['structured-cabling', 'fiber-optic-installation', 'ip-phone-systems'],
})
services['ip-phone-systems']['en'].update({
    'name': 'IP telephony',
    'title': 'IP telephony and VoIP for commercial offices | Opticable',
    'desc': 'IP telephony, VoIP lines, and cabling for commercial offices. Montreal, Laval, Longueuil, and across Quebec.',
    'hero': 'IP telephony and VoIP systems for offices and business spaces',
    'intro': 'Opticable installs the cabling and network infrastructure required for IP telephony systems. Workstations, VoIP lines, business numbers, and structured cabling ready for communication, for offices that need reliable phone service well integrated with the network.',
    'summary': 'Business telephony, SIP lines, handsets, VoIP cabling, and network support for commercial offices.',
    'related': ['network-infrastructure', 'structured-cabling', 'commercial-wifi-installation'],
})
services['managed-it-services']['en'].update({
    'name': 'IT services',
    'title': 'IT services and device management | Opticable',
    'desc': 'IT support, device management, network maintenance, and technical support for businesses and commercial buildings in Quebec.',
    'hero': 'IT services and device management for businesses and commercial buildings',
    'intro': 'Opticable provides IT support, device management, and maintenance for technology environments after installation. We stay available so your systems keep running without interruption.',
    'summary': 'Device management, network support, maintenance, and technical support for your environment after installation.',
    'related': ['network-infrastructure', 'commercial-wifi-installation', 'ip-phone-systems'],
})

faq_groups['en'] = [
    ('About Opticable in general', 'Basic questions about the company, service territory, and what happens after installation.', [
        ('What area do you serve?', 'Opticable mainly works in Montreal, Laval, Longueuil, the South Shore, the North Shore, the Laurentians, and across Quebec. For projects outside these areas, contact us.'),
        ('Is Opticable a licensed company?', 'Yes. Opticable holds RBQ licence 5864-1648-01, issued by the Regie du batiment du Quebec.'),
        ('What types of buildings do you work in?', 'Commercial buildings, multi-tenant properties, offices, retail spaces, hotels, and construction sites. If you are not sure, describe the project and we will tell you honestly whether we can help.'),
        ('Do you supply the equipment or only the installation?', 'Both. We can supply and install, or work with equipment you already have. We can also advise on the right equipment when needed.'),
        ('Do you offer services after installation?', 'Yes. We provide technical support, management, and maintenance after commissioning for cameras, WiFi, access control, intercom, and network systems. We do not just install them and disappear.'),
    ]),
    ('Quotes and project planning', 'What to prepare to get a clear proposal and start a project under the right conditions.', [
        ('How do I get a quote?', 'Fill out the contact form or call us during the week. Tell us what type of building you have, which systems you need, and your timeline. We will get back to you quickly with a clear proposal.'),
        ('How much does an installation cost?', 'Costs depend on the system, square footage, number of points, and access constraints. Every project is different, so contact us for a quote adapted to your situation.'),
        ('Do you handle small projects?', 'Yes. We work on single-system jobs in small spaces as well as full installations in large buildings. Project size is not a reason to say no.'),
        ('What information do you need to prepare a quote?', 'The basics are the building type, approximate address, desired systems, number of zones, doors, or points, timeline, and any special constraints. The more detail you provide, the more accurate the proposal will be.'),
        ('Do you do site visits before quoting?', 'Yes, for larger projects. A visit lets us confirm pathways, constraints, and the existing infrastructure before we issue the final proposal.'),
    ]),
    ('About the installation', 'How field coordination works and what you receive at handoff.', [
        ('How long does a typical installation take?', 'It depends on the project. A camera installation in a retail space can be done in one day. A full project in a multi-tenant building can take several days or several weeks. The schedule is set out in the proposal.'),
        ('Do you work in occupied buildings?', 'Yes. That is our most common reality. We plan the work to minimize interruptions and adapt to the building schedule.'),
        ('Do you coordinate with other contractors on site?', 'Yes. We coordinate with the general contractor, electricians, and other trades so cabling and systems are installed at the right phases.'),
        ('What is included when a project is delivered?', 'All systems are tested and working, components are identified, and the basic documentation is handed over. You receive a system that you, or another technician, can understand without rediscovering everything from zero.'),
    ]),
    ('Specific systems', 'Answers about integrations, remote access, and the technical choices people ask about most often.', [
        ('Can cameras, intercom, and access control work together?', 'Yes. These three systems can belong to the same ecosystem, with one management platform to monitor, control access, and communicate at the entry. That is often the solution we recommend for buildings that want simpler management.'),
        ('Can we view the cameras remotely?', 'Yes. The systems we install allow remote viewing from a computer, tablet, or phone.'),
        ('What is the difference between access control and a simple electric lock?', 'An electric lock opens or closes a door. An access control system manages who can enter, when they can enter, what identification they use, and it keeps an access history.'),
        ('Can an intercom be tied into access control?', 'Yes. A video intercom connected to access control makes it possible to identify a visitor and unlock the door remotely from an indoor station or a mobile device.'),
        ('What cable category do you recommend for a new project?', 'Cat 6 or Cat 6A for the large majority of commercial projects. Cat 6A is preferable for longer distances or environments with a high density of equipment.'),
        ('Do you provide maintenance after installation?', 'Yes. We remain available for post-commissioning work such as adding points, replacing equipment, reconfiguring systems, and technical support.'),
        ('What are your technical support hours?', 'Technical support is available Monday to Friday from 8:00 AM to 5:00 PM and Saturday and Sunday from 10:00 AM to 4:00 PM.'),
    ]),
]

services['security-camera-systems']['fr'].update({
    'name': 'Caméras de sécurité',
    'title': 'Caméras de sécurité pour immeubles commerciaux | Opticable',
    'desc': "Installation et gestion de caméras IP, NVR et surveillance pour immeubles commerciaux. Montréal, Laval, Longueuil et partout au Québec.",
    'hero': "Caméras de sécurité pour immeubles commerciaux et espaces d'affaires",
    'intro': "Opticable installe et gère des systèmes de caméras IP adaptés aux immeubles commerciaux, multilogements et aux environnements d'affaires. Chaque projet est planifié selon vos zones sensibles, vos accès et les exigences de votre exploitation, avec un soutien continu après la mise en service.",
    'summary': 'Caméras IP, PoE, NVR, visionnement à distance et soutien continu pour protéger les zones sensibles, aires communes, périmètres et accès.',
    'related': ['access-control-systems', 'intercom-systems', 'structured-cabling'],
})
services['access-control-systems']['fr'].update({
    'name': "Contrôle d'accès",
    'title': "Contrôle d'accès pour immeubles commerciaux | Opticable",
    'desc': "Installation et gestion de contrôle d'accès, lecteurs, panneaux et câblage de portes pour immeubles commerciaux. Montréal, Laval et partout au Québec.",
    'hero': "Contrôle d'accès pour immeubles, halls d'entrée et espaces sécurisés",
    'intro': "Opticable installe et gère des systèmes de contrôle d'accès pour les immeubles commerciaux, multilogements et les environnements d'affaires. Lecteurs, panneaux de contrôle, serrures électroniques et câblage de portes sont planifiés, installés et soutenus pour des accès fiables et durables.",
    'summary': "Lecteurs, serrures, panneaux, câblage de portes et administration continue des accès pour halls, entrées et zones restreintes.",
    'related': ['intercom-systems', 'security-camera-systems', 'structured-cabling'],
})
services['commercial-wifi-installation']['fr'].update({
    'name': 'WiFi commercial',
    'title': 'Installation WiFi commercial pour immeubles | Opticable',
    'desc': "Installation WiFi commercial, points d'accès, couverture, câblage et base réseau pour bureaux, commerces et immeubles multilogements.",
    'hero': 'WiFi commercial pour bureaux, immeubles et espaces partagés',
    'intro': "Opticable conçoit et installe l'infrastructure WiFi côté bâtiment dont les immeubles commerciaux et multilogements ont besoin. Emplacement des points d'accès, logique de couverture, câblage, PoE, commutateurs et base réseau sont pensés ensemble pour que le WiFi reste utile dans les vraies conditions du site, dans les aires communes comme dans les zones de travail.",
    'summary': 'Qualité du WiFi, points d’accès, couverture, câblage et base réseau pour les immeubles commerciaux.',
    'related': ['structured-cabling', 'network-infrastructure', 'access-control-systems'],
})
services['intercom-systems']['fr'].update({
    'name': 'Intercom',
    'title': "Systèmes d'intercom pour immeubles commerciaux | Opticable",
    'desc': "Installation d'intercoms audio et vidéo pour halls, portails et immeubles commerciaux. Montréal, Laval, Longueuil et partout au Québec.",
    'hero': "Systèmes d'intercom pour halls, portails et immeubles occupés",
    'intro': "Opticable installe des systèmes d'intercom audio et vidéo pour les halls d'entrée, les portails et les accès visiteurs des immeubles commerciaux et multilogements. Coordonnés avec le contrôle d'accès, les caméras et le réseau, pour une communication d'entrée fiable, bien intégrée et facile à gérer.",
    'summary': "Intercom audio ou vidéo pour halls, portails et accès visiteurs, avec intégration au contrôle d'accès et au réseau.",
    'related': ['access-control-systems', 'security-camera-systems', 'network-infrastructure'],
})
services['structured-cabling']['fr'].update({
    'name': 'Câblage structuré',
    'title': 'Câblage structuré pour immeubles commerciaux | Opticable',
    'desc': 'Câblage structuré Cat 6, Cat 6A, coaxial et fibre pour bureaux, commerces et immeubles multilogements.',
    'hero': "Câblage structuré pour immeubles commerciaux et environnements d'affaires",
    'intro': "Opticable installe le câblage structuré qui supporte les points d'accès WiFi, les caméras, le contrôle d'accès, l'intercom, la téléphonie et le reste du réseau du bâtiment. On cadre le local réseau principal, les petits locaux d'étage quand il en faut, les câbles entre les étages et la documentation pour laisser une base propre, organisée et plus simple à faire évoluer.",
    'summary': 'Cat 5e, Cat 6, Cat 6A, coaxial, fibre, patch panels, tests et documentation pour une base réseau propre du local principal jusqu’aux étages.',
    'related': ['fiber-optic-installation', 'network-infrastructure', 'commercial-wifi-installation'],
})
services['fiber-optic-installation']['fr'].update({
    'name': 'Fibre optique',
    'title': 'Fibre optique pour immeubles commerciaux | Opticable',
    'desc': 'Liaisons fibre optique, colonnes montantes et prolongements de service pour immeubles commerciaux. Montréal, Laval, Longueuil et partout au Québec.',
    'hero': 'Installation de fibre optique pour immeubles commerciaux et sites multi-étages',
    'intro': "Opticable installe les liaisons en fibre optique qui relient le local réseau principal, les petits locaux réseau d'étage et les zones plus éloignées quand le cuivre seul n'est plus la meilleure option. Cette base sert ensuite au WiFi, à la sécurité, aux accès et au reste du réseau du bâtiment.",
    'summary': 'Liaisons de backbone entre étages, locaux réseau et zones éloignées quand la distance ou la capacité dépassent le cuivre.',
    'related': ['structured-cabling', 'network-infrastructure', 'security-camera-systems'],
})
services['network-infrastructure']['fr'].update({
    'name': 'Infrastructure réseau',
    'title': 'Infrastructure réseau pour immeubles commerciaux | Opticable',
    'desc': 'Racks, patch panels, local réseau principal, armoires d’étage et arrivées Internet pour immeubles commerciaux et multilogements.',
    'hero': 'Infrastructure réseau pour immeubles commerciaux - racks, locaux techniques et organisation des arrivées',
    'intro': "Opticable installe et organise l'infrastructure réseau des immeubles commerciaux et multilogements : local réseau principal, armoires ou points de redistribution d'étage quand il en faut, racks, patch panels, arrivées Internet, commutateurs et remise en ordre des locaux techniques existants. C'est cette base qui garde le WiFi, les caméras, l'intercom et les autres systèmes cohérents.",
    'summary': 'Local réseau principal, armoires d’étage, racks, patch panels, commutateurs, arrivées Internet et distribution propre pour des systèmes de bâtiment plus simples à exploiter.',
    'related': ['structured-cabling', 'fiber-optic-installation', 'ip-phone-systems'],
})
services['ip-phone-systems']['fr'].update({
    'name': 'Téléphonie IP',
    'title': 'Téléphonie IP et VoIP pour bureaux commerciaux | Opticable',
    'desc': 'Téléphonie IP, lignes VoIP et câblage pour bureaux commerciaux. Montréal, Laval, Longueuil et partout au Québec.',
    'hero': "Téléphonie IP et systèmes VoIP pour bureaux et espaces d'affaires",
    'intro': "Opticable installe le câblage et l'infrastructure réseau nécessaires à vos systèmes de téléphonie IP. Postes de travail, lignes VoIP, numéros d'affaires et câblage structuré prêt pour la communication, pour les bureaux qui veulent une téléphonie fiable et bien intégrée à leur réseau.",
    'summary': "Téléphonie d'affaires, lignes SIP, postes, câblage VoIP et soutien réseau pour les bureaux commerciaux.",
    'related': ['network-infrastructure', 'structured-cabling', 'commercial-wifi-installation'],
})

faq_groups['fr'] = [
    ('Sur Opticable en général', "Questions de base sur l'entreprise, la zone de service et les services offerts après l'installation.", [
        ('Quelle région desservez-vous ?', "Opticable intervient principalement à Montréal, Laval, Longueuil, sur la Rive-Sud, la Rive-Nord et dans les Laurentides, et partout au Québec. Pour les projets situés hors de ces régions, contactez-nous."),
        ("Est-ce qu'Opticable est une entreprise licenciée ?", 'Oui. Opticable détient la licence RBQ 5864-1648-01, délivrée par la Régie du bâtiment du Québec.'),
        ('Avec quels types de bâtiments travaillez-vous ?', "Immeubles commerciaux, multilogements, bureaux, commerces, hôtels et sites en construction. Si vous n'êtes pas sûr, décrivez-nous votre projet et on vous dira franchement si on peut vous aider."),
        ("Est-ce qu'Opticable fournit aussi le matériel ou seulement l'installation ?", "Les deux. On peut fournir et installer, ou travailler avec le matériel que vous avez déjà. On vous conseille sur le choix des équipements si besoin."),
        ("Est-ce qu'Opticable offre des services après l'installation ?", "Oui. On assure le soutien technique, la gestion et la maintenance des systèmes après la mise en service — caméras, WiFi, contrôle d'accès, intercom et réseau. On ne fait pas que les installer."),
    ]),
    ('Sur les soumissions et les projets', "Ce qu'il faut prévoir pour obtenir une proposition claire et lancer un projet dans de bonnes conditions.", [
        ('Comment obtenir une soumission ?', "Remplissez le formulaire de contact ou appelez-nous en semaine. Décrivez le type de bâtiment, les systèmes visés et votre échéancier. On vous revient rapidement avec une proposition claire."),
        ('Combien coûte une installation ?', "Les coûts varient selon le système, la superficie, le nombre de points et les contraintes d'accès. Chaque projet est différent — contactez-nous pour une soumission adaptée à votre situation."),
        ("Est-ce que vous faites des projets de petite envergure ?", "Oui. On intervient sur un seul système dans un petit local comme sur une installation complète dans un grand immeuble. La taille du projet n'est pas un critère d'exclusion."),
        ("Quelle information avez-vous besoin pour préparer une soumission ?", "L'essentiel: type de bâtiment, adresse approximative, systèmes souhaités, nombre de zones, portes ou points, échéancier et contraintes particulières. Plus vous donnez de détails, plus notre proposition sera précise."),
        ("Est-ce que vous faites des visites de site avant de soumissionner ?", "Pour les projets plus importants, oui. Une visite nous permet de valider les cheminements, les contraintes et l'infrastructure existante avant de remettre une proposition finale."),
    ]),
    ("Sur l'installation", "Déroulement, coordination terrain et remise du système après les travaux.", [
        ("Combien de temps dure une installation typique ?", "Ça dépend du projet. Une installation de caméras dans un commerce peut se faire en une journée. Un projet complet dans un immeuble multilogement peut s'étaler sur plusieurs jours ou plusieurs semaines. L'échéancier est établi dans la soumission."),
        ("Est-ce que vous travaillez dans des bâtiments occupés ?", "Oui, c'est notre réalité la plus courante. On planifie les travaux pour minimiser les interruptions et on s'adapte aux horaires de votre immeuble."),
        ('Est-ce que vous coordonnez avec les autres entrepreneurs sur un chantier ?', "Oui. On coordonne avec l'entrepreneur général, les électriciens et les autres corps de métier pour que le câblage et les systèmes soient installés aux bonnes phases."),
        ("Qu'est-ce qui est inclus dans la livraison d'un projet ?", "Tous les systèmes sont testés et fonctionnels, les composantes sont identifiées et la documentation de base est remise. Vous héritez d'un système que vous, ou un autre technicien, pouvez comprendre sans tout redécouvrir."),
    ]),
    ('Sur les systèmes spécifiques', "Réponses sur les intégrations, l'accès à distance et les choix techniques les plus fréquents.", [
        ("Est-ce que les caméras, l'intercom et le contrôle d'accès peuvent fonctionner ensemble ?", "Oui. Ces trois systèmes peuvent faire partie du même écosystème — une seule plateforme de gestion pour surveiller, contrôler les accès et communiquer à l'entrée. C'est souvent la solution qu'on recommande pour les immeubles qui veulent simplifier leur gestion."),
        ("Est-ce qu'on peut accéder aux caméras à distance ?", "Oui. Les systèmes qu'on installe permettent le visionnement à distance depuis un ordinateur, une tablette ou un téléphone."),
        ("Quelle est la différence entre le contrôle d'accès et un simple verrou électronique ?", "Un verrou électronique ouvre ou ferme une porte. Un système de contrôle d'accès gère qui peut entrer, quand, avec quel type d'identification, et conserve un historique des accès."),
        ("Est-ce qu'un intercom peut être relié au contrôle d'accès ?", "Oui. Un intercom vidéo relié au contrôle d'accès permet d'identifier un visiteur et de déverrouiller la porte à distance depuis un poste intérieur ou un appareil mobile."),
        ("Quelle catégorie de câble recommandez-vous pour un nouveau projet ?", "Cat 6 ou Cat 6A pour la grande majorité des projets commerciaux. Le Cat 6A est préférable pour les longues distances ou les environnements à forte densité d'équipements."),
        ("Est-ce que vous faites de la maintenance après l'installation ?", "Oui. On reste disponibles pour les interventions après la mise en service — ajout de points, remplacement d'équipements, reconfiguration et support technique."),
        ("Quelles sont vos heures pour le support technique ?", "Le support technique est offert du lundi au vendredi de 8 h à 17 h et le samedi et dimanche de 10 h à 16 h."),
    ]),
]

FR_ABOUT_SECTIONS = [
    {
        'eyebrow': 'À propos',
        'title': "Ce qu'on fait, concrètement",
        'paragraphs': [
            "On ne vend pas de la technologie pour elle-même. On installe des systèmes qui répondent à un besoin réel et on accompagne nos clients après la mise en service.",
            "Caméras, contrôle d'accès, intercom, WiFi, câblage structuré, fibre optique et infrastructure réseau sont installés de façon coordonnée, avec une livraison cohérente et un soutien disponible.",
        ],
    },
    {
        'eyebrow': 'Notre approche',
        'title': "Notre approche d'installation et de soutien",
        'cards': [
            ("On part du bâtiment, pas du catalogue", "Chaque projet commence par une analyse de votre espace, de vos contraintes et de vos besoins réels."),
            ('On livre proprement', "Câbles identifiés, locaux techniques bien rangés et documentation remise à la fin des travaux."),
            ('On reste disponibles', "Ajouts, modifications, gestion des systèmes et support technique — vous n'avez pas à repartir de zéro si quelque chose change."),
        ],
    },
    {
        'eyebrow': 'Informations légales',
        'title': 'Informations légales et zone de service',
        'paragraphs': [
            "Opticable opère sous le numéro d'entreprise 9453-4757 Québec Inc. et détient la licence RBQ 5864-1648-01.",
            "Nous desservons les immeubles commerciaux à Montréal, Laval, Longueuil, sur la Rive-Sud, la Rive-Nord, dans les Laurentides et partout au Québec.",
        ],
        'details': [
            ("Numéro d'entreprise", '9453-4757 Québec Inc.'),
            ('Licence RBQ', '5864-1648-01'),
            ('Soumissions et renseignements', 'Lundi au vendredi 8 h à 17 h : par téléphone ou courriel/formulaire'),
            ('Fin de semaine', 'Samedi et dimanche 10 h à 16 h : par courriel ou formulaire seulement'),
            ('Support technique', 'Lundi au vendredi 8 h à 17 h · Samedi et dimanche 10 h à 16 h'),
        ],
    },
]

FR_CLIENTELE_SECTIONS = [
    {
        'title': 'Entreprises, bureaux et commerces',
        'copy': "Vous gérez un bureau, un commerce ou un espace d'accueil et vous avez besoin que la sécurité, le WiFi et les communications soient fiables au quotidien.",
        'items': ['Caméras pour entrées et zones intérieures', "Contrôle d'accès pour espaces restreints", 'WiFi dimensionné pour votre espace', 'Câblage et téléphonie IP pour les postes de travail'],
    },
    {
        'title': 'Immeubles multilogements et résidences à accès contrôlé',
        'copy': "Vous gérez un immeuble résidentiel ou mixte et avez besoin de systèmes d'entrée fiables, d'une couverture caméra dans les aires communes et d'une infrastructure qui résiste à l'usage quotidien.",
        'items': ["Intercom vidéo et contrôle d'accès pour halls d'entrée", 'Caméras dans les aires communes et stationnements', 'WiFi pour espaces partagés', 'Câblage de suites et infrastructure des espaces communs'],
    },
    {
        'title': 'Immeubles commerciaux et propriétés à locataires multiples',
        'copy': "Vous possédez ou gérez un immeuble à vocation commerciale avec plusieurs locataires et des systèmes partagés. On installe les systèmes du bâtiment, pas ceux d'un locataire en particulier.",
        'items': ['Caméras pour espaces communs et périmètre', "Contrôle d'accès pour entrées principales", 'Infrastructure réseau des locaux techniques', 'Câblage des espaces loués'],
    },
    {
        'title': 'Gestionnaires immobiliers et équipes multi-immeubles',
        'copy': "Vous gérez plusieurs immeubles et avez besoin d'un partenaire qui comprend vos contraintes: bâtiments occupés, locataires à accommoder, standards à maintenir et budgets à respecter.",
        'items': ['Mises à niveau dans des immeubles en service', 'Standardisation sur un portefeuille', 'Interventions planifiées', 'Interlocuteur unique pour plusieurs projets'],
    },
    {
        'title': 'Bâtiments neufs, rénovations et chantiers actifs',
        'copy': "Vous construisez, rénovez, aménagez ou livrez un nouveau projet et vous avez besoin que les systèmes technologiques soient coordonnés avec les autres corps de métier, sans retard.",
        'items': ['Coordination avec les électriciens, entrepreneurs et autres corps de métier', 'Câblage structuré selon les phases de construction ou de rénovation', "Caméras, contrôle d'accès, intercom, WiFi et réseau livrés selon l'échéancier", 'Documentation complète à la livraison ou à la mise en service'],
    },
]

FR_CLIENTELE_CTA = {
    'title': "Votre type de projet n'est pas listé ici ?",
    'copy': "On peut aussi évaluer les commerces, hôtels, institutions, entrepôts, sites industriels, sites temporaires, chantiers, nouveaux bâtiments et projets spéciaux. Décrivez-nous votre bâtiment ou votre projet.",
    'label': 'Nous contacter',
}

FR_FAQ_CTA = {
    'title': "Votre question n'est pas ici ?",
    'copy': 'Contactez-nous par courriel ou formulaire en tout temps, ou par téléphone du lundi au vendredi.',
    'label': 'Nous contacter',
}

FR_SERVICE_PAGE_CONTENT = {
    'security-camera-systems': {
        'sections': [
            {'eyebrow': 'Caméras de sécurité', 'title': "Ce qu'on installe et gère", 'items': ['Caméras IP et PoE pour zones intérieures et extérieures', 'Enregistreurs NVR avec enregistrement continu ou sur détection', 'Visionnement à distance depuis ordinateur, tablette ou téléphone', 'Caméras extérieures pour stationnements, entrées de livraison et périmètres', 'Caméras intérieures pour aires communes, halls, corridors et zones d’exploitation', 'Gestion, mises à jour, remplacement d’équipements et soutien technique']},
            {'eyebrow': 'Écosystème unifié', 'title': "Écosystème unifié — caméras, intercom et contrôle d'accès", 'paragraphs': ["Les caméras peuvent faire partie du même écosystème que votre intercom et votre contrôle d'accès — une seule plateforme de gestion pour surveiller, contrôler les accès et communiquer à l'entrée. Un seul partenaire, une seule installation cohérente."]},
            {'eyebrow': 'Bâtiments', 'title': 'Pour quels types de bâtiments', 'items': ['Immeubles de bureaux et tours commerciales', 'Immeubles multilogements et résidences à accès contrôlé', 'Commerces, boutiques et espaces de vente', 'Entrepôts et sites industriels', 'Hôtels et hébergements commerciaux']},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ['01 — Évaluation des zones: entrées, angles morts, zones à risque et contraintes d’installation.', '02 — Proposition adaptée: nombre de caméras, matériel, résolution, stockage et câblage détaillés dans la soumission.', '03 — Installation coordonnée: câblage structuré, fixation propre, configuration NVR et test de chaque caméra.', '04 — Remise et soutien: système documenté, formation de base et disponibilité pour la gestion continue.']},
        ],
        'cta': "Vous planifiez un projet de caméras ? Décrivez-nous votre immeuble et vos zones à couvrir. Nous vous reviendrons avec une proposition claire.",
    },
    'access-control-systems': {
        'sections': [
            {'eyebrow': 'Contrôle d’accès', 'title': "Ce qu'on installe et gère", 'items': ["Lecteurs d'accès par carte, badge, code ou biométrie selon le niveau de sécurité", 'Panneaux de contrôle avec gestion centralisée des portes et des utilisateurs', 'Serrures, gâches électriques, aimants et mécanismes adaptés à chaque porte', 'Câblage de portes, boîtiers et raccordements propres dans les cadres et cloisons', 'Gestion multi-portes à partir d’une seule interface', 'Soutien, administration, mises à jour et support technique continu']},
            {'eyebrow': 'Écosystème unifié', 'title': "Écosystème unifié — accès, caméras et intercom", 'paragraphs': ["Le contrôle d'accès peut être intégré aux caméras et à l'intercom au sein d'une seule plateforme de gestion. Une porte bien sécurisée, c'est un lecteur, une caméra et un intercom qui fonctionnent ensemble, pas trois systèmes indépendants gérés séparément."]},
            {'eyebrow': 'Espaces', 'title': "Pour quels types d'espaces", 'items': ["Halls d'entrée principaux et accès visiteurs", 'Entrées de stationnement et accès souterrains', 'Salles de serveurs, locaux techniques et zones restreintes', "Bureaux à accès limité et salles sécurisées", 'Accès locataires dans les immeubles multilogements']},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ['01 — Analyse des accès: portes, zones, niveaux d’accès et contraintes mécaniques.', '02 — Proposition structurée: matériel, câblage, logiciel de gestion et coûts détaillés.', '03 — Installation rigoureuse: câblage propre dans les cadres et murs, lecteurs bien fixés et tests complets.', '04 — Mise en service et formation: configuration des accès, documentation remise et soutien continu.']},
        ],
        'cta': "Vous voulez sécuriser vos accès ? Dites-nous combien de portes, le type d'immeuble et vos contraintes. On s'en occupe.",
    },
    'commercial-wifi-installation': {
        'sections': [
            {'eyebrow': 'WiFi commercial', 'title': "Ce qu'on installe et gère", 'items': ["Points d'accès WiFi professionnels alimentés en PoE", 'Câblage Cat 6 ou Cat 6A depuis le local réseau principal ou l’armoire la plus proche', 'Planification de couverture selon murs, matériaux, densité d’usagers et zones réelles d’usage', 'Commutation, raccordement et soutien des points d’accès en lien avec la base réseau du bâtiment', 'Soutien après installation pour les ajustements, incidents et besoins d’évolution', 'Gestion du sans-fil lorsque le projet inclut un suivi continu']},
            {'eyebrow': 'Fondation', 'title': "Un bon WiFi commence par la base réseau derrière lui", 'paragraphs': ["La majorité des problèmes de WiFi commencent derrière le point d’accès: câblage faible, PoE inégal, capacité limitée des commutateurs, local réseau mal organisé ou emplacements irréalistes. On planifie la couche WiFi avec la base réseau du bâtiment pour un résultat qui tient dans le temps."]},
            {'eyebrow': 'Espaces', 'title': "Pour quels types d'espaces", 'items': ['Bureaux à aire ouverte et espaces de travail partagés', 'Immeubles multilogements - aires communes et couloirs', 'Commerces, restaurants et espaces clients', 'Chantiers de construction actifs', 'Salles de conférence et espaces événementiels', 'Entrepôts et sites industriels']},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ['01 - Analyse du site: superficie, matériaux, nombre d’utilisateurs et vraie structure du bâtiment.', '02 - Plan de couverture: emplacement des points d’accès, matériel recommandé, câblage requis et bon raccordement au local réseau ou au point de redistribution.', '03 - Installation et câblage: tirage des câbles, fixation des points d’accès, configuration réseau et tests de signal.', '04 - Validation, remise et soutien: couverture vérifiée, configuration documentée et recommandations claires si le bâtiment évolue.']},
        ],
        'cta': "Vous avez des zones sans signal ou un réseau qui ne suffit plus ? Décrivez-nous votre espace et vos besoins.",
    },
    'intercom-systems': {
        'sections': [
            {'eyebrow': 'Intercom', 'title': "Ce qu'on installe", 'items': ['Intercom audio pour la communication entre l’entrée et un poste intérieur ou un téléphone', 'Intercom vidéo avec caméra intégrée pour identifier les visiteurs avant d’ouvrir', 'Postes muraux et bornes d’entrée robustes pour halls, réceptions et portails', "Intégration au contrôle d'accès pour déverrouiller depuis un poste intérieur ou un appareil mobile"]},
            {'eyebrow': 'Écosystème unifié', 'title': 'Écosystème unifié — intercom, accès et caméras', 'paragraphs': ["L'intercom, le contrôle d'accès et les caméras peuvent fonctionner au sein d'un même écosystème — une seule plateforme pour identifier un visiteur, contrôler l'accès et surveiller l'entrée. On les installe ensemble, de façon coordonnée, pour une gestion simplifiée."]},
            {'eyebrow': 'Immeubles', 'title': "Pour quels types d'immeubles", 'items': ['Immeubles multilogements avec entrée sécurisée', "Immeubles de bureaux avec réception ou accès visiteurs", 'Commerces avec zones de livraison ou accès restreint', 'Stationnements couverts et accès souterrains', "Portails extérieurs et cours d'immeuble"]},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ["01 — Analyse de l'entrée: type de porte, flux de visiteurs, contraintes mécaniques et infrastructure existante.", '02 — Recommandation claire: audio ou vidéo, intégration au contrôle d’accès et nombre de postes.', '03 — Installation propre: câblage encastré, borne fixée solidement, configuration et tests complets.', '04 — Mise en service: fonctionnement validé et intégration aux autres systèmes confirmée.']},
        ],
        'cta': "Vous cherchez un système d'intercom pour votre entrée ou votre portail ? Parlez-nous de votre immeuble.",
    },
    'structured-cabling': {
        'sections': [
            {'eyebrow': 'Câblage structuré', 'title': "Ce qu'on installe", 'items': ['Câblage cuivre Cat 5e, Cat 6 et Cat 6A pour postes, points d’accès WiFi, caméras IP, lecteurs et équipements réseau', 'Câblage coaxial pour caméras analogiques, antennes et distributions de signal existantes', 'Fibre optique sur courte distance pour relier locaux réseau, étages ou zones éloignées', 'Patch panels pour des arrivées de câbles organisées, identifiées et évolutives']},
            {'eyebrow': 'Usage concret', 'title': 'Ce que ça supporte concrètement', 'items': ['Points d’accès WiFi alimentés en PoE via Cat 6', 'Caméras IP raccordées à l’enregistreur NVR', "Lecteurs de contrôle d'accès câblés au panneau de contrôle", 'Postes de téléphonie IP et équipements de bureau', 'Équipements réseau dans le local technique']},
            {'eyebrow': 'Langage simple', 'title': "À quoi servent le local principal, le local d'étage et les câbles entre étages ?", 'paragraphs': ["Le local réseau principal regroupe souvent le rack principal, la commutation et les arrivées. Le local d'étage ou la petite armoire technique sert de point de redistribution plus près des zones à desservir. Les câbles entre étages relient ces points entre eux pour éviter une distribution improvisée." ]},
            {'eyebrow': 'Qualité', 'title': "Une installation propre, ça veut dire quoi ?", 'paragraphs': ["Câbles identifiés aux deux extrémités, cheminements bien fixés, patch panels organisés et local réseau que n'importe quel technicien peut comprendre sans tout redécouvrir."]},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ['01 - Relevé du site: zones à câbler, cheminements possibles et contraintes du bâtiment.', '02 - Plan de câblage: nombre de points, longueurs, type de câble et organisation du local réseau.', '03 - Installation structurée: tirage, connexion aux patch panels et identification complète de chaque point.', '04 - Test et certification: chaque point est testé et la documentation des points est remise.']},
        ],
        'cta': "Vous avez un projet de câblage ou un réseau à organiser ? Dites-nous la superficie, le nombre de points et le type de bâtiment.",
    },
    'fiber-optic-installation': {
        'sections': [
            {'eyebrow': 'Fibre optique', 'title': "Ce qu'on installe", 'items': ['Liaisons fibre entre le local réseau principal et les armoires ou locaux d’étage', 'Liaisons longue portée entre bâtiments, ailes ou locaux techniques distants', 'Prolongements de service vers une nouvelle zone, un nouvel étage ou un nouvel équipement', 'Fibre monomode ou multimode selon la distance et la bande passante', 'Raccordements, connecteurs LC, SC ou MPO et organisation dans les boîtiers']},
            {'eyebrow': 'Usage', 'title': 'Quand la fibre est nécessaire', 'items': ['Bâtiments de plusieurs étages avec un local réseau par niveau', 'Distances supérieures à 90 mètres entre équipements', 'Liaisons entre bâtiments sur un même site', 'Besoins de bande passante élevée pour caméras et réseau principal', 'Infrastructure existante à prolonger ou remplacer']},
            {'eyebrow': 'Coordination', 'title': 'Coordonné avec le câblage structuré', 'paragraphs': ['La fibre sert de colonne vertébrale entre le local principal, les points de redistribution et les zones éloignées. Le cuivre prend ensuite le relais pour les derniers mètres jusqu’aux appareils. On installe les deux ensemble pour garder un chemin cohérent du local technique jusqu’au point final.']},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ["01 - Analyse de l'infrastructure: points à relier, distances, cheminements et équipements aux deux extrémités.", '02 - Recommandation technique: type de fibre, nombre de brins et type de connecteurs.', '03 - Installation et soudure: passage de la fibre dans les cheminements existants ou nouveaux et connexion des extrémités.', '04 - Test et certification: chaque liaison est testée en atténuation et documentée.']},
        ],
        'cta': "Vous avez besoin d'une liaison fibre entre étages ou entre bâtiments ? Décrivez-nous le projet.",
    },
    'network-infrastructure': {
        'sections': [
            {'eyebrow': 'Infrastructure réseau', 'title': "Ce qu'on installe et organise", 'items': ['Racks et armoires ouverts ou fermés selon les équipements et les besoins d’accès', 'Patch panels pour organiser les arrivées de câbles avec une identification claire', 'Gestion verticale et horizontale des câbles pour des racks lisibles et évolutifs', 'Routage propre des arrivées Internet Bell, Vidéotron, Rogers ou autres', "Remise en ordre de l'existant pour rendre un local technique plus fonctionnel sans tout reconstruire"]},
            {'eyebrow': 'Fondation', 'title': 'La base avant le WiFi et les systèmes connectés', 'paragraphs': ["Le local réseau principal est souvent le point de départ du bâtiment. Dans les immeubles plus grands, on ajoute aussi des armoires ou petits locaux d'étage plus près des zones desservies. C'est cette structure qui garde le WiFi, les caméras, l'intercom, le contrôle d'accès et les autres systèmes plus faciles à coordonner."]},
            {'eyebrow': 'Valeur', 'title': 'Pourquoi un local réseau bien organisé, ça compte', 'paragraphs': ['Un local chaotique coûte du temps à chaque intervention et rend les modifications risquées. Un local bien structuré est moins cher à entretenir sur le long terme et beaucoup plus simple à faire évoluer.']},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ['01 - Évaluation du local: espace disponible, équipements en place, arrivées existantes et besoins futurs.', '02 - Plan d’organisation: disposition des racks, patch panels, gestion des arrivées et documentation avant les travaux.', '03 - Installation ou réorganisation: montage des racks, câblage des panneaux et identification complète.', '04 - Documentation remise: relevé des ports, équipements, arrivées et cheminements.']},
        ],
        'cta': "Votre local réseau a besoin d'attention ? Dites-nous l'état actuel et vos besoins.",
    },
    'ip-phone-systems': {
        'sections': [
            {'eyebrow': 'Téléphonie IP', 'title': "Ce qu'on installe", 'items': ['Câblage pour postes VoIP alimentés en PoE depuis le commutateur réseau', 'Lignes SIP, numéros locaux ou sans frais et intégration avec votre fournisseur', "Postes de téléphonie IP pour espaces de travail, réceptions et zones opérationnelles", 'Infrastructure réseau et commutation adaptées à la téléphonie IP']},
            {'eyebrow': 'Infrastructure', 'title': "La téléphonie, c'est d'abord une question d'infrastructure", 'paragraphs': ["Un système VoIP mal câblé, c'est de la voix qui coupe et des problèmes qu'on attribue au fournisseur alors que c'est le réseau qui est en cause. On installe l'infrastructure correctement dès le départ."]},
            {'eyebrow': 'Besoins', 'title': 'Pour qui', 'items': ['Bureaux en démarrage ou en déménagement', "Entreprises qui migrent d'un système analogique vers la VoIP", 'Immeubles commerciaux qui fournissent la téléphonie aux locataires', 'Espaces de coworking avec plusieurs usagers']},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ['01 — Analyse des besoins: nombre de postes, localisation, type de lignes et infrastructure existante.', '02 — Proposition claire: câblage, matériel, lignes et configuration détaillés.', '03 — Installation et configuration: câblage des postes, configuration des lignes et tests de qualité vocale.', '04 — Mise en service: chaque poste est validé, les numéros sont configurés et le système devient opérationnel.']},
        ],
        'cta': "Vous installez ou remplacez votre téléphonie d'affaires ? Dites-nous le nombre de postes et vos besoins.",
    },
    'managed-it-services': {
        'sections': [
            {'eyebrow': 'Services informatiques et soutien technique', 'title': "Ce qu'on fait", 'items': ['Gestion de parc informatique : inventaire, mises à jour, remplacement et suivi des équipements réseau et postes de travail.', 'Soutien technique : intervention sur les systèmes installés, diagnostic et résolution des problèmes réseau, WiFi, caméras et contrôle d’accès.', 'Maintenance préventive : vérifications périodiques des équipements, des configurations et de la stabilité des systèmes.', 'Administration des systèmes : gestion des accès, mises à jour des configurations et ajustements après la mise en service.', 'Support utilisateur : assistance pour vos équipes sur l’utilisation des systèmes installés.']},
            {'eyebrow': 'Pour qui', 'title': 'Pour qui', 'items': ['Entreprises qui veulent externaliser la gestion de leur environnement réseau et technologique', 'Gestionnaires immobiliers qui ont besoin d’un suivi régulier sur plusieurs immeubles', 'Organisations qui ont des systèmes en place mais plus de ressources internes pour les gérer']},
            {'eyebrow': 'Coordination', 'title': 'Coordonné avec vos systèmes existants', 'paragraphs': ["Que les systèmes aient été installés par Opticable ou par un autre prestataire, on peut en prendre la gestion en charge. On fait d'abord un audit de l'existant, puis on propose un plan de soutien adapté."]},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ["01 — Audit de l'existant : on inventorie vos équipements, configurations et points à améliorer.", '02 — Plan de soutien : on vous propose une formule adaptée à vos besoins et votre budget.', '03 — Prise en charge : on devient votre interlocuteur technique pour la gestion courante.', "04 — Suivi continu : interventions réactives et préventives selon l'entente convenue."]},
        ],
        'cta': 'Vous cherchez un partenaire pour gérer votre environnement technologique ? Décrivez-nous votre situation.',
    },
}

EN_ABOUT_SECTIONS = [
    {
        'eyebrow': 'About',
        'title': 'What we do in practice',
        'paragraphs': [
            'We do not sell technology for its own sake. We install systems that answer a real operational need and we support our clients after commissioning.',
            'Cameras, access control, intercom, WiFi, structured cabling, fiber optic links, and network infrastructure are installed in a coordinated way, with a coherent handoff and support that stays available.',
        ],
    },
    {
        'eyebrow': 'Our approach',
        'title': 'How we install and support systems',
        'cards': [
            ('We start with the building, not the catalog', 'Every project starts with a review of your space, your constraints, and your real operating needs.'),
            ('We deliver clean work', 'Cables are labeled, technical rooms are organized, and documentation is handed over at the end of the work.'),
            ('We stay available', 'Additions, changes, system management, and technical support are handled without forcing you to start from zero when something changes.'),
        ],
    },
    {
        'eyebrow': 'Legal information',
        'title': 'Legal information and service territory',
        'paragraphs': [
            'Opticable operates under business number 9453-4757 Quebec Inc. and holds RBQ licence 5864-1648-01.',
            'We serve commercial buildings in Montreal, Laval, Longueuil, the South Shore, the North Shore, the Laurentians, and across Quebec.',
        ],
        'details': [
            ('Business name', '9453-4757 Quebec Inc.'),
            ('RBQ licence', '5864-1648-01'),
            ('Quotes and inquiries', 'Monday to Friday, 8:00 AM to 5:00 PM: by phone or by email/form'),
            ('Weekends', 'Saturday and Sunday, 10:00 AM to 4:00 PM: by email or form only'),
            ('Technical support', 'Monday to Friday, 8:00 AM to 5:00 PM · Saturday and Sunday, 10:00 AM to 4:00 PM'),
        ],
    },
]

EN_CLIENTELE_SECTIONS = [
    {
        'title': 'Businesses, offices, and retail spaces',
        'copy': 'You manage an office, a retail space, or a reception area and you need security, WiFi, and communications to stay reliable every day.',
        'items': ['Cameras for entries and interior areas', 'Access control for restricted spaces', 'WiFi sized for your space', 'Cabling and IP telephony for workstations'],
    },
    {
        'title': 'Multi-tenant buildings and controlled-entry residences',
        'copy': 'You manage a residential or mixed-use building and need reliable entry systems, camera coverage in common areas, and infrastructure that holds up to daily use.',
        'items': ['Video intercom and access control for lobby entries', 'Cameras in common areas and parking', 'WiFi for shared spaces', 'Suite cabling and common-area infrastructure'],
    },
    {
        'title': 'Commercial buildings and multi-tenant properties',
        'copy': 'You own or manage a commercial property with multiple tenants and shared systems. We install the building systems, not just one tenant system in isolation.',
        'items': ['Cameras for common spaces and the perimeter', 'Access control for main entries', 'Network infrastructure for technical rooms', 'Cabling for leased spaces'],
    },
    {
        'title': 'Property managers and multi-building teams',
        'copy': 'You manage several properties and need a partner that understands the constraints: occupied buildings, tenant accommodation, standards to maintain, and budgets to respect.',
        'items': ['Upgrades in active buildings', 'Portfolio-wide standardization', 'Planned interventions', 'One contact for multiple projects'],
    },
    {
        'title': 'Developers and general contractors',
        'copy': 'You are building or renovating a property and need the building systems coordinated with the other trades, without delays.',
        'items': ['Coordination with electricians and other trades', 'Structured cabling aligned with construction phases', 'Cameras, access control, and intercom delivered on schedule', 'Complete documentation at handoff'],
    },
]

EN_CLIENTELE_CTA = {
    'title': 'Do you have a project type that is not listed here?',
    'copy': 'We also work in hospitality, institutional environments, industrial sites, new construction, and new projects. Tell us about your building or project.',
    'label': 'Contact us',
}

EN_FAQ_CTA = {
    'title': 'Is your question not listed here?',
    'copy': 'Contact us by email or form at any time, or by phone Monday to Friday.',
    'label': 'Contact us',
}

EN_SERVICE_PAGE_CONTENT = {
    'security-camera-systems': {
        'sections': [
            {'eyebrow': 'Security cameras', 'title': 'What we install and manage', 'items': ['IP and PoE cameras for interior and exterior areas', 'NVR recorders with continuous or motion-based recording', 'Remote viewing from a computer, tablet, or phone', 'Exterior cameras for parking areas, delivery entries, and perimeters', 'Interior cameras for common spaces, lobbies, corridors, and operating areas', 'Management, updates, equipment replacement, and technical support']},
            {'eyebrow': 'Unified ecosystem', 'title': 'Unified ecosystem for cameras, intercom, and access control', 'paragraphs': ['Your cameras can belong to the same ecosystem as the intercom and access control system, with one management platform to monitor, manage entry, and communicate at the door. One partner, one coordinated installation.']},
            {'eyebrow': 'Buildings', 'title': 'Where these systems fit', 'items': ['Office buildings and commercial towers', 'Multi-tenant buildings and controlled-entry residences', 'Retail spaces, boutiques, and point-of-sale environments', 'Warehouses and industrial sites', 'Hotels and commercial hospitality properties']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Area review: entries, blind spots, risk zones, and installation constraints.', '02 - Clear proposal: number of cameras, hardware, resolution, storage, and cabling detailed in the quote.', '03 - Coordinated installation: structured cabling, clean mounting, NVR configuration, and testing of every camera.', '04 - Handover and support: documented system, basic training, and availability for ongoing management.']},
        ],
        'cta': 'Planning a camera project? Tell us about your building and the areas you need to cover. We will come back with a clear proposal.',
    },
    'access-control-systems': {
        'sections': [
            {'eyebrow': 'Access control', 'title': 'What we install and manage', 'items': ['Access readers using cards, badges, codes, or biometrics depending on the required security level', 'Control panels with centralized door and user management', 'Locks, electric strikes, magnets, and door hardware suited to each opening', 'Door cabling, enclosures, and clean terminations in frames and partitions', 'Multi-door management from one interface', 'Support, administration, updates, and ongoing technical support']},
            {'eyebrow': 'Unified ecosystem', 'title': 'Unified ecosystem for access, cameras, and intercom', 'paragraphs': ['Access control can be integrated with cameras and intercom in one management platform. A well-secured door is a reader, a camera, and an intercom working together, not three separate systems managed independently.']},
            {'eyebrow': 'Spaces', 'title': 'Where this fits', 'items': ['Main lobbies and visitor entries', 'Parking entrances and underground access points', 'Server rooms, technical rooms, and restricted areas', 'Limited-access offices and secured rooms', 'Tenant access in multi-tenant buildings']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Access review: doors, zones, access levels, and mechanical constraints.', '02 - Structured proposal: hardware, cabling, management software, and costs laid out clearly.', '03 - Careful installation: clean cabling in frames and walls, solid reader mounting, and full testing.', '04 - Commissioning and training: access rules configured, documentation handed over, and ongoing support available.']},
        ],
        'cta': 'Need to secure your entries? Tell us how many doors you have, what kind of building it is, and any constraints. We will take it from there.',
    },
    'commercial-wifi-installation': {
        'sections': [
            {'eyebrow': 'Commercial WiFi', 'title': 'What we install and manage', 'items': ['Professional WiFi access points powered by PoE', 'Cat 6 or Cat 6A support cabling from the main network room or the nearest floor cabinet', 'Coverage planning based on walls, materials, user density, and the actual usage zones', 'Switching, patching, and access-point support tied to the building network foundation', 'Post-installation support for adjustments, incidents, and future growth', 'Wireless management when the project scope includes ongoing follow-up']},
            {'eyebrow': 'Foundation', 'title': 'Good WiFi starts with the network foundation behind it', 'paragraphs': ['Most WiFi problems start behind the access point: weak cabling, inconsistent PoE, limited switch capacity, poor room organization, or unrealistic placement. We plan the WiFi layer together with the building network foundation so the result stays usable over time.']},
            {'eyebrow': 'Spaces', 'title': 'Where it fits', 'items': ['Open offices and shared workspaces', 'Multi-tenant buildings with common areas and corridors', 'Retail spaces, restaurants, and customer-facing areas', 'Active construction sites', 'Conference rooms and event spaces', 'Warehouses and industrial sites']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Site analysis: square footage, materials, expected users, and the actual building layout.', '02 - Coverage plan: access-point locations, recommended hardware, required cabling, and the right network-room or floor-cabinet tie-in.', '03 - Installation and cabling: cable pulls, access-point mounting, network configuration, and signal testing.', '04 - Validation, handoff, and support: verified coverage, documented configuration, and the next-step recommendations if the building grows.']},
        ],
        'cta': 'Do you have dead zones or a wireless network that no longer keeps up? Tell us about the space and what it needs to support.',
    },
    'intercom-systems': {
        'sections': [
            {'eyebrow': 'Intercom', 'title': 'What we install', 'items': ['Audio intercoms for communication between the entry and an indoor station or phone', 'Video intercoms with integrated cameras to identify visitors before unlocking', 'Durable wall stations and entry pedestals for lobbies, reception areas, and gates', 'Integration with access control so doors can be unlocked from an indoor station or mobile device']},
            {'eyebrow': 'Unified ecosystem', 'title': 'Unified ecosystem for intercom, access, and cameras', 'paragraphs': ['Intercom, access control, and cameras can operate inside one ecosystem, with one platform to identify visitors, manage access, and monitor the entry. We install them together in a coordinated way to simplify day-to-day management.']},
            {'eyebrow': 'Buildings', 'title': 'Where it fits', 'items': ['Multi-tenant buildings with secured entry', 'Office buildings with reception desks or visitor access', 'Retail spaces with delivery zones or restricted access', 'Covered parking and underground access points', 'Exterior gates and property courtyards']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Entry review: door type, visitor flow, mechanical constraints, and existing infrastructure.', '02 - Clear recommendation: audio or video, access-control integration, and number of stations.', '03 - Clean installation: concealed cabling, solid mounting, configuration, and full testing.', '04 - Commissioning: operation validated and integration with the other systems confirmed.']},
        ],
        'cta': 'Looking for an intercom system for an entry or gate? Tell us about the building and the type of access you need to manage.',
    },
    'structured-cabling': {
        'sections': [
            {'eyebrow': 'Structured cabling', 'title': 'What we install', 'items': ['Cat 5e, Cat 6, and Cat 6A copper cabling for workstations, WiFi access points, IP cameras, readers, and network equipment', 'Coaxial cabling for analog cameras, antennas, and existing signal distribution systems', 'Short-distance fiber optic links for connecting network rooms, floors, or remote zones', 'Patch panels for cable arrivals that stay organized, labeled, and ready for future growth']},
            {'eyebrow': 'Practical use', 'title': 'What it supports in practice', 'items': ['PoE WiFi access points over Cat 6', 'IP cameras connected back to the NVR', 'Access-control readers wired to the control panel', 'IP phone handsets and office devices', 'Network equipment in the technical room']},
            {'eyebrow': 'Plain language', 'title': 'What the main room, floor closet, and between-floor cabling do', 'paragraphs': ['The main network room is where the core equipment and handoffs usually live. A floor closet or secondary cabinet is a smaller distribution point closer to the spaces being served. The cabling between floors links those points together so devices do not all have to run back in an improvised way.']},
            {'eyebrow': 'Quality', 'title': 'What a clean installation actually means', 'paragraphs': ['Cables labeled at both ends, pathways secured properly, organized patch panels, and a network room that any technician can understand without rediscovering everything from scratch.']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Site survey: areas to cable, available pathways, and building constraints.', '02 - Cabling plan: number of points, run lengths, cable type, and network-room organization.', '03 - Structured installation: cable pulling, patch-panel termination, and full identification of every point.', '04 - Testing and certification: every point is tested and the point list is handed over.']},
        ],
        'cta': 'Do you have a cabling project or a network room that needs to be organized? Tell us the square footage, point count, and building type.',
    },
    'fiber-optic-installation': {
        'sections': [
            {'eyebrow': 'Fiber optic', 'title': 'What we install', 'items': ['Fiber links between the main network room and floor-level closets or cabinets', 'Long-distance links between buildings, wings, or remote technical rooms', 'Service extensions to a new area, a new floor, or new equipment', 'Single-mode or multi-mode fiber depending on distance and bandwidth needs', 'Terminations, LC, SC, or MPO connectors, and organized fiber enclosures']},
            {'eyebrow': 'Use cases', 'title': 'When fiber is needed', 'items': ['Multi-storey buildings with one network room per level', 'Runs longer than 90 meters between equipment', 'Links between buildings on the same property', 'High-bandwidth needs for cameras and the core network', 'Existing infrastructure that needs to be extended or replaced']},
            {'eyebrow': 'Coordination', 'title': 'Coordinated with structured cabling', 'paragraphs': ['Fiber acts as the backbone between the main room, floor closets, and distant zones. Copper then takes over for the last meters to the devices. We install both together so the path stays coherent from the room to the final endpoint.']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Infrastructure review: points to connect, distances, pathways, and equipment at both ends.', '02 - Technical recommendation: fiber type, strand count, and connector type.', '03 - Installation and splicing: fiber run through existing or new pathways and clean termination at both ends.', '04 - Testing and certification: every link is attenuation-tested and documented.']},
        ],
        'cta': 'Do you need a fiber link between floors or between buildings? Describe the project and we will point you in the right direction.',
    },
    'network-infrastructure': {
        'sections': [
            {'eyebrow': 'Network infrastructure', 'title': 'What we install and organize', 'items': ['Open or closed racks and cabinets based on the equipment and service-access needs', 'Patch panels that keep incoming cabling organized and clearly labeled', 'Vertical and horizontal cable management for racks that stay readable and expandable', 'Clean routing of Bell, Videotron, Rogers, or other internet entries', 'Cleanup of existing technical rooms to make them more functional without rebuilding everything']},
            {'eyebrow': 'Foundation', 'title': 'The base before WiFi and the connected building systems', 'paragraphs': ['The main network room is where the building usually starts. In larger properties, floor closets or secondary cabinets are added closer to the served spaces. That structure is what keeps WiFi, cameras, intercom, access control, and future systems easier to coordinate.']},
            {'eyebrow': 'Value', 'title': 'Why an organized network room matters', 'paragraphs': ['A chaotic room costs time every time someone intervenes and makes changes risky. A well-structured room costs less to maintain over time and is much easier to expand.']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Room review: available space, installed equipment, existing internet handoffs, and future needs.', '02 - Organization plan: rack layout, patch panels, internet handoff routing, and documentation before the work starts.', '03 - Installation or reorganization: rack assembly, panel cabling, and full identification.', '04 - Documentation handoff: port maps, equipment list, internet handoffs, and pathways.']},
        ],
        'cta': 'Does your network room need attention? Tell us what is in place today and what needs to improve.',
    },
    'ip-phone-systems': {
        'sections': [
            {'eyebrow': 'IP telephony', 'title': 'What we install', 'items': ['Cabling for VoIP handsets powered by PoE from the network switch', 'SIP lines, local or toll-free numbers, and integration with your provider', 'IP phone handsets for work areas, reception desks, and operating zones', 'Network infrastructure and switching prepared for IP telephony']},
            {'eyebrow': 'Infrastructure', 'title': 'Telephony starts with infrastructure', 'paragraphs': ['A poorly cabled VoIP system creates dropped calls and voice issues that get blamed on the carrier when the real problem is the network. We install the infrastructure correctly from the start.']},
            {'eyebrow': 'Needs', 'title': 'Who this is for', 'items': ['Offices being launched or relocated', 'Businesses moving from analog systems to VoIP', 'Commercial buildings that provide phone service to tenants', 'Coworking environments with multiple users']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Needs review: number of handsets, locations, line type, and existing infrastructure.', '02 - Clear proposal: cabling, hardware, lines, and configuration detailed clearly.', '03 - Installation and configuration: handset cabling, line setup, and voice-quality testing.', '04 - Commissioning: each handset is validated, numbers are configured, and the system becomes operational.']},
        ],
        'cta': 'Installing or replacing your business phone system? Tell us how many handsets you need and what the environment looks like.',
    },
    'managed-it-services': {
        'sections': [
            {'eyebrow': 'IT services and technical support', 'title': 'What we do', 'items': ['Device management: inventory, updates, replacement, and tracking for network equipment and workstations.', 'Technical support: work on installed systems, diagnosis, and resolution of network, WiFi, camera, and access-control issues.', 'Preventive maintenance: recurring checks of equipment, configurations, and system stability.', 'System administration: user access, configuration updates, and adjustments after commissioning.', 'User support: practical assistance for your team on the systems that are already installed.']},
            {'eyebrow': 'Who it is for', 'title': 'Who it is for', 'items': ['Businesses that want to outsource management of their network and technology environment', 'Property managers that need regular follow-up across multiple buildings', 'Organizations that have systems in place but no longer have the internal capacity to manage them']},
            {'eyebrow': 'Coordination', 'title': 'Coordinated with your existing systems', 'paragraphs': ['Whether the systems were installed by Opticable or by another provider, we can take over their management. We begin with an audit of the current environment and then propose a support plan that fits.']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Existing-system audit: we inventory your equipment, configurations, and the points that need improvement.', '02 - Support plan: we propose an arrangement that fits your needs and budget.', '03 - Takeover: we become your technical contact for day-to-day management.', '04 - Ongoing follow-up: reactive and preventive interventions based on the agreed plan.']},
        ],
        'cta': 'Looking for a partner to manage your technology environment? Tell us about the current setup and where the friction is.',
    },
}

ABOUT_SECTIONS_BY_LANG = {'en': EN_ABOUT_SECTIONS, 'fr': FR_ABOUT_SECTIONS}
CLIENTELE_SECTIONS_BY_LANG = {'en': EN_CLIENTELE_SECTIONS, 'fr': FR_CLIENTELE_SECTIONS}
CLIENTELE_CTA_BY_LANG = {'en': EN_CLIENTELE_CTA, 'fr': FR_CLIENTELE_CTA}
FAQ_CTA_BY_LANG = {'en': EN_FAQ_CTA, 'fr': FR_FAQ_CTA}
SERVICE_PAGE_CONTENT_BY_LANG = {'en': EN_SERVICE_PAGE_CONTENT, 'fr': FR_SERVICE_PAGE_CONTENT}

PARTNER_BRANDS = ('Ubiquiti (UniFi)', 'MikroTik', 'Fortinet', 'Hikvision', 'Uniview (UNV)', 'TP-Link Omada', 'Akuvox')
PARTNER_BRANDS_COPY = {
    'en': {
        'eyebrow': 'Equipment',
        'title': 'Brands we install and support',
        'intro': 'We work with commercial-grade equipment recognized across the industry.',
    },
    'fr': {
        'eyebrow': 'Équipements',
        'title': 'Marques que nous installons et supportons',
        'intro': "Nous travaillons avec des équipements de qualité commerciale reconnus dans l'industrie.",
    },
}

BLOG_PAGE = {
    'en': {
        'title': 'Commercial Building Technology Blog | Opticable',
        'desc': 'Advice, guides, and resources about security systems, commercial WiFi, cabling, and network infrastructure for Quebec commercial properties — by Opticable.',
        'eyebrow': 'Resources and guidance',
        'h1': 'Opticable blog — Technology for commercial properties',
        'intro': 'Practical articles about cameras, access control, commercial WiFi, cabling, and network infrastructure for property managers, contractors, and building owners.',
        'empty': 'The first articles are coming soon. In the meantime, review our service pages or contact us directly with your technical questions.',
        'primary_cta': 'View our services',
        'secondary_cta': 'Contact us',
        'listing_title': 'Articles',
        'listing_intro': 'This layout is ready for article cards with title, date, excerpt, and link.',
    },
    'fr': {
        'title': 'Blogue technologie commerciale | Opticable',
        'desc': 'Conseils, guides et ressources sur les systèmes de sécurité, WiFi commercial, câblage et infrastructure réseau pour immeubles commerciaux au Québec — par Opticable.',
        'eyebrow': 'Ressources et conseils',
        'h1': 'Blogue Opticable — Technologie pour immeubles commerciaux',
        'intro': "Des articles pratiques sur les caméras, le contrôle d'accès, le WiFi commercial, le câblage et l'infrastructure réseau pour les gestionnaires, entrepreneurs et propriétaires d'immeubles.",
        'empty': "Les premiers articles arrivent bientôt. En attendant, consultez nos pages de services ou contactez-nous directement pour vos questions techniques.",
        'primary_cta': 'Voir nos services',
        'secondary_cta': 'Nous contacter',
        'listing_title': 'Articles',
        'listing_intro': 'Des ressources pratiques sur le WiFi, le câblage, la sécurité et les systèmes techniques de bâtiment.',
    },
}

BLOG_PAGE['en'] = {
    'title': 'Commercial Building Technology Blog | Opticable',
    'desc': 'Advice, guides, and resources about security systems, commercial WiFi, cabling, and network infrastructure for commercial buildings in Quebec — by Opticable.',
    'eyebrow': 'Resources and guidance',
    'h1': 'Opticable blog — Technology for commercial buildings',
    'intro': 'Practical articles about cameras, access control, commercial WiFi, cabling, and network infrastructure for property managers, contractors, and building owners.',
    'empty': 'The first articles are coming soon. In the meantime, review our service pages or contact us directly with your technical questions.',
    'primary_cta': 'View our services',
    'secondary_cta': 'Contact us',
    'listing_title': 'Articles',
    'listing_intro': 'Practical resources about WiFi, cabling, security, and supporting building infrastructure.',
}

BLOG_HUB_PAGE = {
    'en': {
        'title': 'Blog, Guides and Articles | Opticable',
        'desc': 'Guides, comparisons, pricing pages, and articles for planning camera, access control, intercom, WiFi, and cabling projects.',
        'eyebrow': 'Opticable resources',
        'h1': 'Guides and articles to plan your project',
        'intro': 'Use this page to choose the right type of content for your need. Guides help with decisions, budgets, and preparation. Articles explain field issues, technical choices, and best practices.',
        'chooser_title': 'Choose the right resource',
        'chooser_intro': 'Start with the section that best matches your current step.',
        'chooser_cards': [
            ('Guides', 'Compare options, frame a budget, choose a system, or prepare a quote request.', '/en/guides/', 'View guides'),
            ('Articles', 'Understand field issues, installation logic, and technical best practices.', '/en/blog/articles/', 'View articles'),
        ],
        'guides_title': 'Guides to review before requesting a quote',
        'guides_intro': 'Decision, pricing, comparison, and project-preparation pages.',
        'articles_title': 'Recent articles',
        'articles_intro': 'Explanatory content about systems, common issues, and practical next steps.',
    },
    'fr': {
        'title': 'Blogue, guides et articles | Opticable',
        'desc': "Guides, comparatifs, pages de prix et articles pour mieux planifier un projet de caméras, contrôle d'accès, intercom, WiFi et câblage commercial.",
        'eyebrow': 'Ressources Opticable',
        'h1': 'Guides et articles pour mieux planifier votre projet',
        'intro': "Le but de cette page est simple : vous aider à choisir le bon type de contenu selon votre besoin. Les guides servent à décider et à budgéter. Les articles servent à mieux comprendre un problème, une technologie ou une bonne pratique.",
        'chooser_title': 'Choisir le bon type de contenu',
        'chooser_intro': "Commencez par la section qui correspond le mieux à votre étape actuelle.",
        'chooser_cards': [
            ('Guides', "Pour comparer des options, cadrer un budget, choisir un système ou préparer une demande de soumission.", '/fr/guides/', 'Voir les guides'),
            ('Articles', "Pour mieux comprendre un problème terrain, une logique d'installation ou une bonne pratique technique.", '/fr/blogue/articles/', 'Voir les articles'),
        ],
        'guides_title': 'Guides à consulter avant de demander une soumission',
        'guides_intro': "Des pages orientées décision, prix, comparatif et préparation de projet.",
        'articles_title': 'Articles récents',
        'articles_intro': "Des contenus plus explicatifs pour mieux comprendre les systèmes, les erreurs fréquentes et les bonnes prochaines étapes.",
    },
}

BLOG_ARTICLES_PAGE = {
    'en': {
        'title': 'Blog Articles | Opticable',
        'desc': 'Practical articles about cameras, access control, intercom, commercial WiFi, cabling, and network infrastructure.',
        'eyebrow': 'Articles',
        'h1': 'Opticable blog articles',
        'intro': 'Practical articles to understand field issues, technical choices, and installation best practices in commercial buildings.',
    },
    'fr': {
        'title': 'Articles du blogue | Opticable',
        'desc': "Articles pratiques sur les caméras, le contrôle d'accès, l'intercom, le WiFi commercial, le câblage et l'infrastructure réseau.",
        'eyebrow': 'Articles',
        'h1': 'Articles du blogue Opticable',
        'intro': "Des articles pratiques pour mieux comprendre les problèmes terrain, les choix techniques et les bonnes pratiques d'installation dans les immeubles commerciaux.",
    },
}

BLOG_META_UI = {
    'en': {
        'author': 'Author',
        'published': 'Published',
        'reading_time': 'Reading time',
        'read_article': 'Read the article',
        'view_service': 'View service',
        'myth': 'The myth',
        'reality': 'The reality',
        'article_panel': 'Article overview',
        'minutes': 'min read',
        'related_services': 'Related services',
        'related_services_intro': 'Services that usually support the same problem or project scope.',
        'related_articles': 'Read next',
        'related_articles_intro': 'Related articles that continue the same technical conversation.',
    },
    'fr': {
        'author': 'Auteur',
        'published': 'Publié',
        'reading_time': 'Temps de lecture',
        'read_article': "Lire l'article",
        'view_service': 'Voir le service',
        'myth': 'Le mythe',
        'reality': 'La réalité',
        'article_panel': "Aperçu de l'article",
        'minutes': 'minutes',
        'related_services': 'Services connexes',
        'related_services_intro': 'Services qui reviennent souvent dans le même projet ou le même problème technique.',
        'related_articles': 'À lire ensuite',
        'related_articles_intro': 'Articles liés pour poursuivre sur le même sujet technique.',
    },
}

BLOG_MONTHS = {
    'en': ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'),
    'fr': ('janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'),
}

BLOG_ARTICLES = {
    'wifi-power': {
        'published': '2026-03-24',
        'modified': '2026-03-24',
        'author': 'Yan-Erik B.',
        'related_services': ('commercial-wifi-installation', 'network-infrastructure', 'structured-cabling'),
        'related_articles': ('ip-cameras-network-upgrade', 'structured-cabling-foundation'),
        'en': {
            'path': '/en/blog/why-more-wifi-power-makes-things-worse/',
            'title': 'Why More WiFi Power Makes Things Worse | Opticable',
            'desc': 'Why increasing WiFi access point power rarely fixes coverage, interference, or performance problems in a commercial building.',
            'eyebrow': 'Commercial WiFi',
            'headline': 'Turning up WiFi power usually makes the problem worse.',
            'intro': 'The signal is weak, devices keep dropping, and the connection feels unstable. The reflex is to turn up the WiFi access point power. In many cases, that is the worst thing to do. Here is why, and what actually works.',
            'excerpt': 'Weak signal, dropped devices, unstable performance. Turning up the power sounds logical, but in a real commercial building it often makes the problem worse.',
            'tags': ['Commercial WiFi', 'Network Infrastructure'],
            'hero_image': SERVICE_WIFI_URL,
            'hero_image_position': '38% 58%',
            'summary': [
                ('The reflex to avoid', 'Turning up the power on a single access point to compensate for bad WiFi.'),
                ('The real problem', 'Interference, client congestion, and poor band planning.'),
                ('What works', 'More access points, less power, and a real channel plan.'),
            ],
            'sections': [
                {
                    'eyebrow': 'Basics',
                    'title': 'The basic idea: WiFi is sound in the air',
                    'paragraphs': [
                        'WiFi is radio. A WiFi access point, also called a WiFi antenna or wireless AP, sends and receives signals through the air on specific frequencies. Those frequencies are grouped into bands.',
                        'Think of it like sound. If you talk through a wall, the person on the other side hears you less clearly. If you stand at the far end of a long corridor, same problem. And if everyone in the room talks at the same time, nobody understands each other no matter how loudly they shout.',
                        'WiFi works the same way. It is not a pipe that you simply force more data through. It is a shared conversation in physical space. When the air is too busy, the data does not move well, and increasing transmit power does not solve that.',
                    ],
                    'callout_label': 'Key takeaway',
                    'callout': 'Most WiFi problems come from interference, too many clients on one access point, or poor band selection. Power is not the answer to those problems. It usually makes them worse.',
                },
                {
                    'eyebrow': 'Bands',
                    'title': 'The three WiFi bands and what they actually do',
                    'paragraphs': [
                        'Modern WiFi runs on three frequency bands. Each one behaves differently in the air, similar to low and high frequencies in an audio system. Lower frequencies travel farther but with less precision. Higher frequencies are cleaner and faster but do not move through walls as well. Choosing the right band is already half the job.',
                    ],
                    'table': {
                        'caption': 'Quick comparison of the three WiFi bands',
                        'columns': ('Band', 'Frequency', 'Range', 'Speed', 'Penetration', 'Congestion'),
                        'rows': (
                            ('2.4 GHz', '2.4 GHz', ('Long', 'green'), ('Low', 'amber'), ('High', 'green'), ('Very crowded', 'red')),
                            ('5 GHz', '5 GHz', ('Medium', 'amber'), ('High', 'green'), ('Medium', 'amber'), ('Less crowded', 'green')),
                            ('6 GHz', '6 GHz', ('Short', 'red'), ('Very high', 'green'), ('Low', 'red'), ('Nearly empty', 'green')),
                        ),
                    },
                    'subsections': [
                        {
                            'title': '2.4 GHz: the most crowded band',
                            'paragraphs': [
                                '2.4 GHz travels well through walls and reaches farther. That sounds good. The problem is that almost everything uses it at the same time. Neighbors, low-end IP cameras, cordless phones, microwave ovens, baby monitors, and smart thermostats all compete there.',
                                'There are only three usable non-overlapping channels on that band. In an apartment building or commercial office, those three channels fill up fast. Picture a gym where everybody is shouting over the same three conversations. Your WiFi access point is still talking, but nobody can hear it clearly because the room is already full of noise.',
                                'What happens when you turn up the power in that situation? You just shout louder in the same gym. Your neighbors do the same. Nobody understands better. Everybody interferes with everybody else more.',
                            ],
                        },
                        {
                            'title': '5 GHz: usually the right choice for most applications',
                            'paragraphs': [
                                '5 GHz gives you far more channels, less interference, and much higher throughput. The tradeoff is shorter range and weaker penetration through obstacles.',
                                'That is not a flaw. It is a design constraint you handle by placing access points more intelligently, with better coverage geometry and more appropriate density.',
                            ],
                        },
                        {
                            'title': '6 GHz: WiFi 6E and WiFi 7',
                            'paragraphs': [
                                '6 GHz is the newest band. Right now it is close to empty compared with older bands, which means cleaner airtime and excellent performance.',
                                'But it travels through walls even less effectively than 5 GHz. In a properly designed environment with the right number of access points, it is the highest-performing band available.',
                            ],
                        },
                    ],
                },
                {
                    'eyebrow': 'Power',
                    'title': 'Why turning up the power makes things worse',
                    'comparisons': [
                        {
                            'myth': 'The more powerful my WiFi access point is, the better the signal. Strong signal means a good connection.',
                            'reality': 'A stronger signal from the access point means nothing if your phone or laptop cannot answer back at the same level. WiFi is a two-way conversation. It is only as strong as the weaker side of the link.',
                        },
                        {
                            'myth': 'If a device is far away and drops, I need a more powerful WiFi antenna to reach it.',
                            'reality': 'The device may hear the access point better, but the access point does not hear the device better in return. It is like talking through a megaphone to someone who answers in a normal voice.',
                        },
                        {
                            'myth': 'More power means better coverage for everybody.',
                            'reality': 'More power means more devices attach to the same access point. It gets overloaded and performance drops for everyone. One crowded check-in desk does not become faster just because more people line up at it.',
                        },
                    ],
                    'subsections': [
                        {
                            'title': 'The device that stays stuck to the wrong access point',
                            'paragraphs': [
                                'In a building with multiple WiFi access points, a moving device should attach to whichever access point is actually closest and healthiest. But when a far-away access point is broadcasting too aggressively, the device can stay attached to it even after a better one is nearby.',
                                'That is the sticky client problem. The device stays glued to a weak, distant access point and suffers for no good reason.',
                            ],
                        },
                    ],
                    'quote': 'Shouting louder in a packed gym does not solve the fact that everyone is talking at once.',
                },
                {
                    'eyebrow': 'Interference',
                    'title': 'What really causes WiFi problems',
                    'paragraphs': [
                        'These are the real causes. We see them in commercial buildings and multi-tenant properties all the time.',
                    ],
                    'cards': [
                        ('Two access points on the same channel', 'Two people trying to speak at the same time on the same radio frequency. They talk over each other and client devices have to wait.'),
                        ('Too many devices on one access point', 'One access point shares airtime and throughput across every connected device. When too many clients pile onto it, everyone slows down, even the people standing nearby.'),
                        ('Poor channel planning between access points', 'If neighboring WiFi access points use overlapping channels, they interfere with each other constantly like two radios fighting on the same frequency.'),
                        ('Old devices on the network', 'An old WiFi 4 device on 2.4 GHz can force the whole access point to slow down to speak its language. One weak client can drag down the performance of the entire network.'),
                        ('Obstacles were never evaluated', 'Concrete, steel columns, heavily coated glass, and server rooms all affect signal differently depending on the band. A site review is how you account for that before deployment.'),
                        ('Neighboring WiFi', 'In multi-tenant properties, neighboring WiFi networks create constant background noise on the same channels, especially on 2.4 GHz. Increasing your power affects them more, and they return the favor. Everybody loses.'),
                    ],
                    'callout_tone': 'warning',
                    'callout_label': 'The power paradox',
                    'callout': 'The more area one access point covers, the more devices it attracts, and the more overloaded it becomes. In dense buildings, lowering power and adding access points almost always improves performance. Less power, better distribution.',
                },
                {
                    'eyebrow': 'Solutions',
                    'title': 'What actually fixes WiFi problems',
                    'paragraphs': [
                        'This is what we do in practice when a WiFi network needs to perform properly in a real building.',
                    ],
                    'steps': [
                        ('Site survey before installing anything', 'We review building materials, existing interference sources, target coverage areas, and expected device counts. That lets us place WiFi access points where they actually need to work, not just where cabling is easiest.'),
                        ('More access points, less power per access point', 'Multiple access points at moderate power, correctly spaced and set on distinct channels, spread the client load, reduce interference, and create more even coverage across the building.'),
                        ('A channel plan for the whole building', 'On 5 GHz you have many distinct channels available. Assigning them properly between neighboring access points removes overlap. It is often the configuration change with the biggest immediate impact.'),
                        ('Steering devices to the right band', 'Well-configured access points move capable devices toward 5 GHz or 6 GHz and leave 2.4 GHz for older equipment that still depends on it.'),
                        ('Cabling is the foundation of WiFi', 'A WiFi access point is only as good as the cable feeding it. Poorly installed or overly long Cat 6 runs can limit throughput before the signal even leaves the device.'),
                        ('Hardware designed for commercial environments', 'Consumer WiFi gear is not built to handle 40, 60, or 100 active clients in a dense environment. Commercial access points from platforms like UniFi, TP-Link Omada, or Fortinet include the features that matter.'),
                    ],
                    'callout_label': 'Real example',
                    'callout': 'A 5,000 sq ft office had one access point running at full power and constant complaints about disconnects. Replacing it with four UniFi U6 Pro access points at moderate power, along with an optimized channel plan and certified Cat 6 cabling, resulted in zero dropouts, three times higher speeds at the edges of the floor, and roughly 60 percent less load per access point.',
                    'quote': 'Good WiFi is not tuned by feel. It is planned, measured, and validated.',
                },
            ],
            'cta': {
                'title': 'Is your WiFi underperforming?',
                'copy': 'Before replacing access points or turning up the power, talk to us. We can assess the building, identify the real issue, and recommend a solution that fixes the root cause.',
                'primary_label': 'Request a quote',
                'primary_key': 'contact',
                'secondary_label': 'View WiFi service',
                'secondary_key': 'commercial-wifi-installation',
            },
        },
        'fr': {
            'path': '/fr/blogue/pourquoi-plus-de-puissance-wifi-aggrave-le-probleme/',
            'title': 'Pourquoi plus de puissance WiFi empire les choses | Opticable',
            'desc': "Pourquoi augmenter la puissance d'une borne WiFi règle rarement les problèmes de couverture, d'interférences et de performance dans un immeuble commercial.",
            'eyebrow': 'WiFi commercial',
            'headline': "Monter la puissance du WiFi, c'est souvent aggraver le problème.",
            'intro': "Le signal est faible, les appareils décrochent, la connexion est instable. Le réflexe : monter la puissance du point d'accès WiFi. C'est souvent la pire chose à faire. Voici pourquoi — et ce qui marche vraiment.",
            'excerpt': "Le signal est faible, les appareils décrochent, la connexion est instable. Monter la puissance paraît logique, mais dans un vrai bâtiment commercial, c'est souvent ce qui aggrave le problème.",
            'tags': ['WiFi commercial', 'Infrastructure réseau'],
            'hero_image': SERVICE_WIFI_URL,
            'hero_image_position': '38% 58%',
            'summary': [
                ('Le réflexe à éviter', "Monter la puissance d'une seule borne pour compenser un mauvais WiFi."),
                ('Le vrai problème', "Interférences, congestion de clients et mauvaise planification de bande."),
                ('Ce qui fonctionne', 'Plus de bornes, moins de puissance et un vrai plan de canaux.'),
            ],
            'sections': [
                {
                    'eyebrow': 'Les bases',
                    'title': "La base : le WiFi, c'est du son dans l'air",
                    'paragraphs': [
                        "Le WiFi, c'est de la radio. Un point d'accès WiFi — aussi appelé borne WiFi ou antenne WiFi — envoie et reçoit des signaux dans l'air sur des fréquences précises. Ces fréquences, on les appelle des bandes.",
                        "Pensez-y comme du son. Si vous parlez à travers un mur, la personne de l'autre bord vous entend moins bien. Si vous êtes au bout d'un grand couloir, pareil. Et si tout le monde dans la pièce parle en même temps, plus personne ne se comprend — peu importe combien fort vous criez.",
                        "Le WiFi, c'est exactement ça. Ce n'est pas un tuyau qu'on remplit plus ou moins vite. C'est une conversation dans un espace partagé. Quand l'air est trop occupé, les données ne passent plus — et monter la puissance ne règle rien.",
                    ],
                    'callout_label': 'À retenir',
                    'callout': "La plupart des problèmes WiFi viennent des interférences, d'une surcharge sur un seul point d'accès WiFi ou d'un mauvais choix de bande. La puissance n'est pas la réponse à ces problèmes — elle les empire.",
                },
                {
                    'eyebrow': 'Bandes',
                    'title': 'Les trois bandes WiFi — ce qu’elles font vraiment',
                    'paragraphs': [
                        "Le WiFi moderne fonctionne sur trois bandes de fréquences. Chacune se comporte différemment dans l'air — un peu comme les graves et les aigus dans un système de son. Les graves portent loin mais sont moins précis. Les aigus sont clairs mais ne passent pas bien à travers les murs. Savoir choisir la bonne bande, c'est déjà la moitié du travail.",
                    ],
                    'table': {
                        'caption': 'Comparatif rapide des trois bandes WiFi',
                        'columns': ('Bande', 'Fréquence', 'Portée', 'Débit', 'Pénétration', 'Encombrement'),
                        'rows': (
                            ('2.4 GHz', '2.4 GHz', ('Longue', 'green'), ('Faible', 'amber'), ('Élevée', 'green'), ('Très saturé', 'red')),
                            ('5 GHz', '5 GHz', ('Moyenne', 'amber'), ('Élevé', 'green'), ('Moyenne', 'amber'), ('Moins saturé', 'green')),
                            ('6 GHz', '6 GHz', ('Courte', 'red'), ('Très élevé', 'green'), ('Faible', 'red'), ('Quasiment vide', 'green')),
                        ),
                    },
                    'subsections': [
                        {
                            'title': 'Le 2.4 GHz — la bande la plus surchargée',
                            'paragraphs': [
                                "Le 2.4 GHz passe bien à travers les murs et porte loin. Ça a l'air bon. Le problème, c'est que tout le monde l'utilise en même temps. Les voisins, les caméras IP bas de gamme, les téléphones sans fil, les fours à micro-ondes, les moniteurs pour bébé et les thermostats connectés — tout ça trafique sur le 2.4 GHz.",
                                "Et il y a seulement trois canaux disponibles sur cette bande sans qu'ils se chevauchent. Dans un immeuble à logements ou un immeuble de bureaux, ces trois canaux sont bondés. Imaginez un gymnase où tout le monde parle en même temps sur les mêmes trois sujets. Votre point d'accès WiFi parle, mais personne ne l'entend parce que tout le monde parle en même temps.",
                                "Monter la puissance dans ce contexte, ça fait quoi ? Ça fait que vous criez encore plus fort dans le gymnase. Vos voisins font pareil. Personne ne s'entend mieux — tout le monde se nuit davantage.",
                            ],
                        },
                        {
                            'title': 'Le 5 GHz — le bon choix pour la majorité des usages',
                            'paragraphs': [
                                "Le 5 GHz a beaucoup plus de canaux disponibles, moins d'appareils qui l'encombrent, et des débits bien plus élevés. La contrepartie : il passe moins bien à travers les obstacles et porte moins loin.",
                                "Ce n'est pas un défaut. C'est une caractéristique qu'on gère en positionnant mieux les points d'accès WiFi — plus de bornes, mieux placées.",
                            ],
                        },
                        {
                            'title': 'Le 6 GHz — WiFi 6E et WiFi 7',
                            'paragraphs': [
                                "Le 6 GHz, c'est la bande la plus récente. Pour l'instant, elle est pratiquement vide d'interférences — comme parler dans une salle vide, tout se comprend clairement. Les débits sont exceptionnels.",
                                "Mais elle passe encore moins bien à travers les murs que le 5 GHz. Dans un environnement bien pensé avec le bon nombre de points d'accès WiFi, c'est la bande la plus performante qui soit.",
                            ],
                        },
                    ],
                },
                {
                    'eyebrow': 'Puissance',
                    'title': 'Pourquoi monter la puissance empire les choses',
                    'comparisons': [
                        {
                            'myth': 'Plus ma borne WiFi est puissante, meilleur est le signal. Un signal fort = une bonne connexion.',
                            'reality': "Un fort signal du point d'accès WiFi ne change rien si votre téléphone ou laptop ne peut pas répondre à la même puissance. Une connexion WiFi, c'est une conversation à deux sens. Elle est toujours aussi bonne que le maillon le plus faible.",
                        },
                        {
                            'myth': "Si un appareil est loin et décroche, il faut une antenne WiFi plus puissante pour le rejoindre.",
                            'reality': "L'appareil entend mieux la borne — mais la borne n'entend pas mieux l'appareil pour autant. C'est comme si vous parliez dans un mégaphone à quelqu'un qui répond à voix normale. Vous l'entendez toujours aussi peu.",
                        },
                        {
                            'myth': 'Plus de puissance = meilleure couverture pour tout le monde.',
                            'reality': "Plus de puissance = plus d'appareils qui se connectent à la même borne WiFi. Elle se surcharge, tout le monde ralentit. C'est comme un guichet unique dans un aéroport — plus de monde ne veut pas dire un service plus rapide.",
                        },
                    ],
                    'subsections': [
                        {
                            'title': "L'appareil qui reste pogné sur la mauvaise borne",
                            'paragraphs': [
                                "Dans un bâtiment avec plusieurs points d'accès WiFi, un appareil qui se déplace devrait se connecter à la borne la plus proche. Mais si une borne WiFi lointaine est trop puissante, l'appareil reste accroché à elle même quand une meilleure borne est juste à côté.",
                                "C'est ce qu'on appelle le sticky client — l'appareil est pogné sur un point d'accès WiFi trop loin et ses performances en souffrent inutilement.",
                            ],
                        },
                    ],
                    'quote': "Crier plus fort dans un gymnase bondé ne règle pas le fait que tout le monde parle en même temps.",
                },
                {
                    'eyebrow': 'Interférences',
                    'title': 'Ce qui cause vraiment les problèmes de WiFi',
                    'paragraphs': [
                        "Voici les vrais coupables. On les voit dans presque tous les bâtiments commerciaux et immeubles à logements.",
                    ],
                    'cards': [
                        ('Deux bornes sur le même canal', 'Deux personnes qui essaient de parler en même temps sur la même fréquence radio. Elles se parlent par-dessus et les appareils doivent attendre leur tour.'),
                        ("Trop d'appareils sur un seul point d'accès WiFi", "Un point d'accès partage sa bande passante entre tous les appareils connectés. Quand il y en a trop, tout le monde ralentit — même ceux qui sont juste à côté de la borne."),
                        ('Canaux mal planifiés entre bornes', 'Si deux antennes WiFi voisines utilisent des canaux qui se chevauchent, elles se nuisent en permanence — comme deux radios sur la même fréquence qui jouent en même temps.'),
                        ('Vieux appareils sur le réseau', "Un vieux téléphone ou un thermostat connecté en WiFi 4 sur le 2.4 GHz force toute la borne WiFi à ralentir pour lui parler. Un seul vieux appareil peut tirer les performances de tout le réseau vers le bas."),
                        ('Obstacles pas évalués', "Béton, colonnes métalliques, vitres teintées épaisses, salles de serveurs — chaque matériau bloque le signal différemment selon la bande. L'évaluation du site permet d'anticiper ça."),
                        ('Le WiFi des voisins', "Dans un immeuble à plusieurs locataires, les réseaux WiFi des voisins créent du bruit de fond constant sur les mêmes canaux — surtout en 2.4 GHz. Monter votre puissance les affecte davantage. Ils font pareil pour vous. Tout le monde perd."),
                    ],
                    'callout_tone': 'warning',
                    'callout_label': 'Le paradoxe de la puissance',
                    'callout': "Plus une borne WiFi couvre grand, plus elle attire d'appareils — et plus elle se surcharge. Dans un bâtiment dense, baisser la puissance et ajouter des bornes améliore presque toujours les performances. Moins fort, mieux réparti.",
                },
                {
                    'eyebrow': 'Solutions',
                    'title': 'Ce qui règle vraiment les problèmes de WiFi',
                    'paragraphs': [
                        "Voici ce qu'on fait concrètement pour qu'un réseau WiFi performe dans un vrai bâtiment.",
                    ],
                    'steps': [
                        ("Évaluation du site avant d'installer quoi que ce soit", "On regarde les matériaux de construction, les sources d'interférence existantes, les zones à couvrir et le nombre d'appareils à supporter. Ça permet de positionner les points d'accès WiFi là où ils font vraiment leur travail — pas juste là où c'est pratique à câbler."),
                        ('Plus de bornes, moins de puissance par borne', "Plusieurs points d'accès à puissance modérée, bien positionnés sur des canaux distincts — la charge est distribuée, les interférences tombent, la couverture est uniforme partout dans le bâtiment."),
                        ('Plan de canaux pour tout le bâtiment', "Sur le 5 GHz, on a beaucoup de canaux distincts disponibles. Bien les répartir entre bornes adjacentes élimine les chevauchements. C'est un ajustement de config — zéro matériel supplémentaire — et souvent l'intervention qui a le plus d'impact immédiat."),
                        ('Diriger les appareils vers la bonne bande', "Des bornes bien configurées envoient automatiquement les appareils capables vers le 5 GHz ou 6 GHz, et gardent le 2.4 GHz pour les équipements plus vieux qui n'ont pas le choix."),
                        ("Le câblage, c'est la fondation du WiFi", "Une borne WiFi est aussi bonne que le câble qui l'alimente. Un câble Cat 6 mal tiré ou trop long limite le débit avant même que le signal parte dans l'air."),
                        ('Du matériel fait pour les environnements commerciaux', "Les bornes WiFi grand public ne sont pas conçues pour gérer 40, 60 ou 100 appareils en même temps dans un espace dense. Les points d'accès commerciaux comme UniFi, TP-Link Omada ou Fortinet ont les fonctionnalités qui font la différence."),
                    ],
                    'callout_label': 'Exemple concret',
                    'callout': "Un immeuble de bureaux de 5 000 pi² avec une seule borne WiFi poussée à fond et des plaintes constantes de déconnexions. En la remplaçant par quatre points d'accès UniFi U6 Pro à puissance modérée, avec plan de canaux optimisé et câblage Cat 6 certifié, on obtient zéro déconnexion, des débits trois fois plus élevés aux extrémités du plancher et 60 % de charge en moins par borne.",
                    'quote': "Un bon WiFi, ça ne se règle pas à l'œil. Ça se planifie, ça se mesure, ça se valide.",
                },
            ],
            'cta': {
                'title': 'Votre WiFi performe pas comme il devrait ?',
                'copy': "Avant de changer vos bornes ou de monter la puissance, parlez-nous. On évalue votre situation, on regarde le bâtiment et on vous propose une solution qui règle le vrai problème.",
                'primary_label': 'Obtenir une soumission',
                'primary_key': 'contact',
                'secondary_label': 'Voir le service WiFi',
                'secondary_key': 'commercial-wifi-installation',
            },
        },
    },
    'ip-cameras-network-upgrade': {
        'published': '2026-03-23',
        'modified': '2026-03-24',
        'author': "L'équipe Opticable",
        'related_services': ('security-camera-systems', 'network-infrastructure', 'structured-cabling'),
        'related_articles': ('structured-cabling-foundation', 'wifi-power'),
        'en': {
            'path': '/en/blog/ip-cameras-network-upgrade/',
            'author': 'Opticable Team',
            'title': 'IP Camera Network Upgrade Guide | Opticable',
            'desc': 'Why older CCTV and DVR systems reach their limits quickly, and what an upgrade to IP cameras with a cloud-ready NVR platform actually changes.',
            'eyebrow': 'IP Security',
            'headline': 'Are your security cameras keeping up with your network?',
            'intro': 'Old CCTV and DVR systems had their place. Today, IP cameras on a cloud-ready NVR platform change the equation completely: more control, more flexibility, and centralized management across every site from one interface.',
            'excerpt': 'An IP camera is not just a sharper version of CCTV. It is a real network upgrade for access, management, storage, and multi-site visibility.',
            'tags': ['IP Security', 'Security Cameras', 'Network Infrastructure'],
            'hero_image': SERVICE_CAMERA_URL,
            'hero_image_position': '52% 50%',
            'summary': [
                ('What really changes', 'You move from an isolated DVR to an IP platform managed on your network.'),
                ('What you gain', 'Better image quality, cleaner remote access, centralized management, and easier integrations.'),
                ('What to plan for', 'PoE, Cat 6 cabling, network segmentation, storage, and access rights all need to be designed properly.'),
            ],
            'sections': [
                {
                    'eyebrow': 'Why it matters',
                    'title': 'IP surveillance is not just about video anymore',
                    'paragraphs': [
                        'A security camera is not just an eye pointed at your building. It is a device on your network: equipment that moves traffic, authenticates, records or streams data continuously, and has to fit cleanly into the rest of your infrastructure.',
                        'When the system is designed well, it protects entries, discourages incidents before they happen, and leaves you with usable evidence when something does go wrong. When it is integrated poorly, it adds network noise, blind spots, weak remote access, and unnecessary support overhead.',
                        'Whether you manage a residential building, a retail space, an office, or several sites at once, the question is no longer "do we need cameras?" The real question is "does our current system actually do the job we need it to do today?"',
                    ],
                    'callout_label': 'Key takeaway',
                    'callout': 'Moving to IP cameras is not just about replacing cameras. It is an upgrade to your surveillance network, your remote access model, and your ability to manage the system properly.',
                },
                {
                    'eyebrow': 'Who needs it',
                    'title': 'Who really benefits from moving to IP cameras',
                    'paragraphs': [
                        'There is no single client profile for IP surveillance. Every environment comes with its own requirements for coverage, retention, remote access, and user management.',
                    ],
                    'cards': [
                        ('Residential buildings', 'Entries, parking, corridors, and common areas. Residents want peace of mind; managers want archives and remote access when an incident happens.'),
                        ('Retail and storefronts', 'Cash areas, stock rooms, receiving doors, and the sales floor. Video helps reduce theft, document events, and maintain visibility over operations.'),
                        ('Offices and SMBs', 'Server rooms, reception, restricted spaces, and internal circulation. IP cameras belong inside a real physical-security strategy, not just beside a recorder in a closet.'),
                        ('Industrial and warehouse sites', 'Loading docks, perimeters, inventory zones, and exterior areas. These sites need robust cameras, proper IR coverage, alerts, and a network that can handle multiple video streams at once.'),
                        ('Restaurants and hospitality', 'Kitchens, lobbies, bars, parking areas, and supplier entrances. Video protects the business from outside incidents as well as internal disputes and loss.'),
                        ('Multi-site portfolios', 'As soon as there are multiple buildings, stores, or branches, the difference becomes obvious. One interface replaces a patchwork of separate DVRs that are hard to supervise.'),
                    ],
                },
                {
                    'eyebrow': 'Comparison',
                    'title': 'CCTV / DVR versus IP cameras / cloud NVR',
                    'paragraphs': [
                        'For years, the standard setup was a DVR connected to analog cameras over coax. It worked, but it falls short quickly once you need better image quality, cleaner remote viewing, or management across more than one site.',
                    ],
                    'table': {
                        'caption': 'What actually changes when you move to an IP system',
                        'columns': ('Criteria', 'Analog CCTV / DVR', 'IP cameras / cloud NVR'),
                        'rows': (
                            ('Image', 'Limited resolution on older systems and often far below current expectations.', 'Full HD, 4K, or HDR depending on the model, with much better performance in difficult scenes.'),
                            ('Cabling', 'Coax and separate power, usually disconnected from the rest of the network environment.', 'Cat 6 / PoE, a single cable for data and power, integrated with the existing network.'),
                            ('Access', 'Mostly local access or remote viewing that is awkward to maintain.', 'Native remote viewing on mobile and web, with centralized user management.'),
                            ('Storage', 'One local DVR. If the unit fails or disappears, the footage goes with it.', 'Local NVR, hybrid storage, or cloud redundancy depending on the platform.'),
                            ('Multi-site', 'Each site behaves like a separate island.', 'Multiple sites can roll up into one interface with permissions by location.'),
                            ('Security', 'Updates are rare and firmware is often left untouched for years.', 'Platforms are easier to maintain, with cleaner updates, user roles, and ongoing supervision.'),
                        ),
                    },
                    'quote': 'An old DVR may still record. That does not mean it still meets the needs of an active building.',
                },
                {
                    'eyebrow': 'Management',
                    'title': 'The real value shows up when you have multiple sites',
                    'paragraphs': [
                        'This is where modern IP platforms really separate themselves. Three buildings, five stores, or twenty branches can all be managed through the same dashboard instead of a pile of different logins, local IP addresses, and on-site checks.',
                    ],
                    'steps': [
                        ('Unified dashboard', 'Every camera and every site lives in one interface. You can filter by location, zone, or event without jumping between disconnected systems.'),
                        ('Smart alerts', 'Motion, line crossing, after-hours activity, or video clips can go directly to the right person. The system becomes operationally useful, not just something you review later.'),
                        ('Granular permissions', 'Each user sees only what they should see. The manager for site A does not touch site B, while leadership or centralized security keeps the broader view.'),
                        ('Redundant archives', 'Recordings can stay available even if a local NVR is damaged, stolen, or unreachable. That matters when you need evidence after the fact.'),
                    ],
                    'callout_label': 'Why this matters',
                    'callout': 'When the cameras, the network, access rights, and the users are planned together, you move from a system that only provides evidence after an incident to one that is useful every day.',
                },
                {
                    'eyebrow': 'Network',
                    'title': 'Good IP cameras start with a good network',
                    'paragraphs': [
                        'The best camera on the market will not compensate for a poorly planned network. Before installing anything, you need to look at the PoE budget, uplinks, existing cabling, VLAN segmentation, required retention, and how users will connect to the system.',
                        'A poorly integrated IP camera setup does not just create a mediocre image or a blind spot. It can also saturate a link, pollute production traffic, expose remote access unnecessarily, or make maintenance harder for years afterward.',
                    ],
                    'subsections': [
                        {
                            'title': 'What we validate before deployment',
                            'items': [
                                'The quality of the existing cabling and which routes need to be redone',
                                'Available PoE budget on the switching layer',
                                'Local, remote, or hybrid retention requirements',
                                'Risk zones, blind spots, and lighting conditions',
                                'How camera traffic is separated from the rest of the network',
                            ],
                        },
                        {
                            'title': 'What we put in place next',
                            'items': [
                                'Indoor and outdoor IP cameras suited to the site',
                                'Clean, labeled Cat 6 structured cabling',
                                'NVR or VMS platform configured with user roles',
                                'VLAN and network policies that isolate video traffic',
                                'Secure remote access for authorized users',
                            ],
                        },
                        {
                            'title': 'What we avoid at all costs',
                            'items': [
                                'Putting every camera on a flat network with no segmentation',
                                'Underestimating storage and bandwidth requirements',
                                'Leaving remote access improvised or poorly protected',
                                'Reusing questionable cable segments without validation',
                                'Treating surveillance as if it were separate from the rest of the building systems',
                            ],
                        },
                    ],
                    'quote': 'A badly integrated IP camera does not just create a blind spot. It also creates noise, risk, and unnecessary support.',
                },
                {
                    'eyebrow': 'Opticable',
                    'title': 'The right network, the right team',
                    'paragraphs': [
                        'Opticable installs IP camera systems the same way we deploy network infrastructure: methodically, with validation, and with a focus on making the finished system supportable after commissioning.',
                        'We start with the existing infrastructure: switches, cabling, uplinks, available bandwidth, coverage zones, retention needs, and access requirements. The goal is not to sell boxes. The goal is to deliver a coherent system that actually fits the way your site operates.',
                    ],
                    'cards': [
                        ('IP camera installation', 'Interior and exterior cameras for entries, parking, perimeters, and common areas.'),
                        ('Cat 6 structured cabling', 'Clean pathways, terminations, labeling, and a physical foundation the whole system can rely on.'),
                        ('NVR / VMS configuration', 'Recording, retention, user roles, alerts, and remote viewing configured properly from the start.'),
                        ('VLAN segmentation', 'Separation between camera traffic, workstations, guest WiFi, and critical systems for a healthier network.'),
                        ('Multi-site management', 'One dashboard for multiple buildings, stores, or branches with clear access rights.'),
                        ('Support and maintenance', 'Updates, adjustments, replacements, and follow-up after the system is in service.'),
                    ],
                },
            ],
            'cta': {
                'title': 'Ready to modernize your IP surveillance?',
                'copy': 'Tell us about your building or portfolio. We can review the site, the network, and the security requirements and come back with a solution that actually holds up in practice.',
                'primary_label': 'Request a quote',
                'primary_key': 'contact',
                'secondary_label': 'View camera service',
                'secondary_key': 'security-camera-systems',
            },
        },
        'fr': {
            'path': '/fr/blogue/cameras-ip-mise-a-niveau-reseau/',
            'title': 'Caméras IP et mise à niveau réseau | Opticable',
            'desc': "Pourquoi les vieux systèmes CCTV / DVR atteignent vite leurs limites, et ce qu'une migration vers des caméras IP avec NVR cloud change réellement.",
            'eyebrow': 'Sécurité IP',
            'headline': 'Vos caméras de sécurité sont-elles à la hauteur de votre réseau ?',
            'intro': "Les vieux systèmes CCTV et DVR ont fait leur temps. Aujourd'hui, les caméras IP sur plateforme NVR cloud changent complètement la donne : plus de contrôle, plus de flexibilité, et une gestion centralisée de tous vos sites dans une seule interface.",
            'excerpt': "Une caméra IP n'est pas juste une version plus nette du CCTV. C'est une vraie mise à niveau réseau pour l'accès, la gestion, le stockage et la supervision multi-site.",
            'tags': ['Sécurité IP', 'Caméras de sécurité', 'Infrastructure réseau'],
            'hero_image': SERVICE_CAMERA_URL,
            'hero_image_position': '52% 50%',
            'summary': [
                ('Le vrai changement', "Passer d'un DVR isolé à une plateforme IP gérée sur votre réseau."),
                ('Ce que ça apporte', 'Meilleure image, accès distant, gestion centralisée et intégrations plus propres.'),
                ('Ce qu’il faut prévoir', 'PoE, câblage Cat 6, segmentation réseau, stockage et droits d’accès bien planifiés.'),
            ],
            'sections': [
                {
                    'eyebrow': "Pourquoi c'est important",
                    'title': "La surveillance IP, ce n'est plus juste de la vidéo",
                    'paragraphs': [
                        "Une caméra de sécurité n'est pas seulement un œil pointé sur votre bâtiment. C'est un appareil branché sur votre réseau : un équipement qui transmet du trafic, qui s'authentifie, qui enregistre ou streame des données en continu, et qui doit s'intégrer proprement au reste de votre infrastructure.",
                        "Quand le système est bien pensé, il protège vos accès, décourage les incidents avant qu'ils arrivent, et vous laisse une trace exploitable si quelque chose se passe. Quand il est mal intégré, il ajoute du bruit réseau, des angles morts, des accès distants fragiles et beaucoup de support inutile.",
                        "Que vous gériez un immeuble résidentiel, un commerce, un bureau ou plusieurs sites à la fois, la vraie question n'est plus « est-ce qu'on a besoin de caméras ? ». La vraie question, c'est « est-ce que notre système actuel fait vraiment le travail qu'on lui demande aujourd'hui ? »",
                    ],
                    'callout_label': 'À retenir',
                    'callout': "Migrer vers les caméras IP, ce n'est pas seulement remplacer des caméras. C'est mettre à niveau votre réseau de surveillance, votre accès à distance et votre capacité de gestion.",
                },
                {
                    'eyebrow': "Qui en a besoin",
                    'title': 'Qui a vraiment intérêt à passer aux caméras IP',
                    'paragraphs': [
                        "Il n'y a pas un seul profil de client pour la surveillance IP. Chaque environnement a ses propres contraintes de zones à couvrir, de rétention, d'accès à distance et de nombre d'utilisateurs à gérer.",
                    ],
                    'cards': [
                        ('Immeubles résidentiels', "Entrées, stationnements, corridors et aires communes. Les résidents veulent de la tranquillité d'esprit; les gestionnaires veulent des archives et un accès à distance quand un incident survient."),
                        ('Commerces et détail', 'Caisses, réserves, portes de livraison et plancher de vente. La vidéo sert à réduire le vol, documenter les événements et garder une visibilité sur les opérations.'),
                        ('Bureaux et PME', "Salles serveurs, réception, accès restreints et circulation interne. Les caméras IP s'intègrent à une vraie stratégie de sécurité physique, pas seulement à un enregistreur posé dans un coin."),
                        ('Industries et entrepôts', "Quais, périmètres, inventaire et zones extérieures. Ici, il faut des caméras robustes, du bon éclairage IR, des alertes et un réseau capable d'absorber plusieurs flux vidéo en parallèle."),
                        ('Restaurants et hôtellerie', "Cuisine, hall, bar, stationnements et entrées fournisseurs. La vidéo protège l'établissement autant contre les incidents externes que contre les litiges ou les pertes internes."),
                        ('Portefeuilles multi-sites', "Dès qu'il y a plusieurs immeubles, commerces ou succursales, la différence devient énorme. Une seule interface remplace une collection de DVR séparés et difficiles à suivre."),
                    ],
                },
                {
                    'eyebrow': 'Comparatif',
                    'title': 'CCTV / DVR contre caméras IP / NVR cloud',
                    'paragraphs': [
                        "Pendant longtemps, le standard, c'était un DVR branché à des caméras analogiques sur coaxial. Ça fonctionnait, mais ça répond mal aux besoins actuels dès qu'on veut de la qualité d'image, du visionnement distant propre ou une gestion à l'échelle de plusieurs sites.",
                    ],
                    'table': {
                        'caption': 'Ce qui change concrètement quand on migre vers un système IP',
                        'columns': ('Critère', 'CCTV / DVR analogique', 'Caméras IP / NVR cloud'),
                        'rows': (
                            ('Image', 'Résolution limitée sur les installations plus âgées, souvent loin des standards actuels.', 'Full HD, 4K ou HDR selon le modèle, avec bien meilleure performance dans les scènes difficiles.'),
                            ('Câblage', 'Coaxial et alimentation séparée, infrastructure souvent déconnectée du reste du réseau.', 'Cat 6 / PoE, un seul câble pour les données et l’alimentation, intégré au réseau existant.'),
                            ('Accès', 'Consultation locale ou accès distant complexe à maintenir.', 'Visionnement distant natif sur mobile et web, avec gestion centralisée des utilisateurs.'),
                            ('Stockage', 'DVR local unique : si la machine tombe ou disparaît, les archives partent avec.', 'NVR local, stockage hybride ou redondance cloud selon la plateforme choisie.'),
                            ('Multi-site', 'Chaque site fonctionne comme une île séparée.', 'Tous les sites peuvent remonter dans une seule interface avec des permissions par emplacement.'),
                            ('Sécurité', 'Mises à jour rares et firmwares souvent laissés en place pendant des années.', 'Plateformes plus propres à maintenir, avec mises à jour, rôles utilisateurs et supervision plus rigoureuse.'),
                        ),
                    },
                    'quote': "Un vieux DVR peut encore enregistrer. Ça ne veut pas dire qu'il répond encore aux besoins d'un bâtiment actif.",
                },
                {
                    'eyebrow': 'Gestion',
                    'title': 'La vraie valeur apparaît quand il y a plusieurs sites',
                    'paragraphs': [
                        "C'est là que les plateformes IP modernes font vraiment la différence. Trois immeubles, cinq commerces ou vingt succursales : tout peut être regroupé dans le même tableau de bord, au lieu de multiplier les accès, les mots de passe, les IP locales et les visites sur place.",
                    ],
                    'steps': [
                        ('Dashboard unifié', 'Toutes les caméras, tous les sites, dans une seule interface. Vous filtrez par emplacement, par zone ou par événement sans jongler avec plusieurs systèmes.'),
                        ('Alertes intelligentes', 'Mouvement, franchissement de zone, activité hors horaire ou clip vidéo envoyé directement à la bonne personne. Le système devient exploitable, pas seulement consultable.'),
                        ('Permissions granulaires', "Chaque utilisateur voit ce qu'il doit voir. Le gérant du site A ne touche pas au site B, pendant que la direction ou la sécurité centrale conserve une vue d'ensemble."),
                        ('Archives redondantes', "Les enregistrements peuvent rester disponibles même si un NVR local est endommagé, volé ou inaccessible. C'est une vraie différence quand il faut récupérer une preuve après coup."),
                    ],
                    'callout_label': 'Pourquoi ça compte',
                    'callout': "Quand la caméra, le réseau, les accès et les utilisateurs sont pensés ensemble, vous passez d'un système de preuve après incident à un système de supervision réellement utile au quotidien.",
                },
                {
                    'eyebrow': 'Réseau',
                    'title': 'Une bonne caméra IP commence par un bon réseau',
                    'paragraphs': [
                        "La meilleure caméra du marché ne compensera pas un réseau mal planifié. Avant de poser quoi que ce soit, il faut regarder le budget PoE, les uplinks, le câblage existant, la segmentation VLAN, la rétention vidéo voulue et la façon dont les utilisateurs vont se connecter.",
                        "Une caméra IP mal intégrée, ça ne crée pas seulement une image moyenne ou un angle mort. Ça peut aussi saturer un lien, polluer le trafic de production, exposer un accès distant inutilement ou compliquer toute la maintenance pour les années suivantes.",
                    ],
                    'subsections': [
                        {
                            'title': "Ce qu'on valide avant le déploiement",
                            'items': [
                                'La qualité du câblage existant et les parcours à reprendre',
                                'Le budget PoE disponible sur les commutateurs',
                                'Les besoins de rétention locale, distante ou hybride',
                                'Les zones à risque, angles morts et conditions lumineuses',
                                'La séparation du trafic caméras du reste du réseau',
                            ],
                        },
                        {
                            'title': "Ce qu'on met en place ensuite",
                            'items': [
                                'Caméras IP intérieures et extérieures adaptées au site',
                                'Câblage structuré Cat 6 propre et identifié',
                                'NVR ou plateforme VMS configurée avec profils utilisateurs',
                                'VLAN et politiques réseau pour isoler le trafic vidéo',
                                'Accès distant sécurisé pour les personnes autorisées',
                            ],
                        },
                        {
                            'title': "Ce qu'on évite absolument",
                            'items': [
                                'Brancher toutes les caméras sur un réseau plat sans segmentation',
                                'Sous-estimer le stockage et la bande passante nécessaires',
                                'Laisser un accès distant improvisé ou mal protégé',
                                'Réutiliser des segments de câblage douteux sans validation',
                                'Traiter la surveillance comme un système isolé du reste du bâtiment',
                            ],
                        },
                    ],
                    'quote': "Une caméra IP mal intégrée ne crée pas seulement un angle mort. Elle crée aussi du bruit, du risque et du support inutile.",
                },
                {
                    'eyebrow': 'Opticable',
                    'title': 'Le bon réseau, la bonne équipe',
                    'paragraphs': [
                        "Opticable installe des systèmes de caméras IP comme on déploie une infrastructure réseau : avec méthode, avec validation, et en s'assurant que le tout reste supportable après la mise en service.",
                        "On commence par l'infrastructure existante : commutateurs, câblage, uplinks, bande passante, zones à couvrir, rétention et besoins d'accès. Le but n'est pas de vendre des boîtes. Le but est de livrer un système cohérent qui tient la route dans votre réalité.",
                    ],
                    'cards': [
                        ('Installation de caméras IP', 'Caméras intérieures et extérieures, couverture des accès, stationnements, périmètres et zones communes.'),
                        ('Câblage structuré Cat 6', 'Parcours propres, terminaisons, étiquetage et base physique solide pour l’ensemble du système.'),
                        ('Configuration NVR / VMS', 'Enregistrement, rétention, profils utilisateurs, alertes et visionnement à distance configurés proprement.'),
                        ('Segmentation VLAN', 'Séparation du trafic caméras, postes, WiFi invité et systèmes critiques pour garder un réseau plus sain.'),
                        ('Gestion multi-site', 'Un seul tableau de bord pour plusieurs immeubles, commerces ou succursales avec droits d’accès clairs.'),
                        ('Support et maintenance', 'Mises à jour, ajustements, remplacements et accompagnement après la mise en service.'),
                    ],
                },
            ],
            'cta': {
                'title': 'Prêt à moderniser votre surveillance IP ?',
                'copy': "Parlez-nous de votre bâtiment ou de votre parc immobilier. On analyse votre site, votre réseau et vos besoins de sécurité pour vous proposer une solution qui tient vraiment la route.",
                'primary_label': 'Obtenir une soumission',
                'primary_key': 'contact',
                'secondary_label': 'Voir le service caméras',
                'secondary_key': 'security-camera-systems',
            },
        },
    },
    'structured-cabling-foundation': {
        'published': '2026-03-20',
        'modified': '2026-03-24',
        'author': "L'équipe Opticable",
        'related_services': ('structured-cabling', 'network-infrastructure', 'fiber-optic-installation'),
        'related_articles': ('wifi-power', 'ip-cameras-network-upgrade'),
        'en': {
            'path': '/en/blog/why-structured-cabling-changes-everything/',
            'author': 'Opticable Team',
            'title': 'Why Structured Cabling Changes Everything | Opticable',
            'desc': 'Why structured cabling is still the real foundation of a reliable, supportable network that can grow with your building.',
            'eyebrow': 'Structured Cabling',
            'headline': 'A solid network starts inside the walls.',
            'intro': 'People talk about WiFi, switches, and fiber. They talk much less about the cabling underneath it all. But that physical layer is what determines performance, stability, and how easily the rest of the infrastructure can evolve.',
            'excerpt': 'When cabling is poorly planned, every new device, outage, or expansion costs more. Done properly, it becomes a clean, invisible, durable base for everything else.',
            'tags': ['Structured Cabling', 'Network Infrastructure'],
            'hero_image': SERVICE_CABLING_URL,
            'hero_image_position': '52% 52%',
            'summary': [
                ('The real foundation', 'The physical cabling layer determines the stability and performance of the entire network.'),
                ('The right medium', 'Coax, Cat6, Cat6A, and fiber do not solve the same problems or serve the same role.'),
                ('The long-term return', 'Labeling, certification, and spare capacity prevent expensive wasted time later.'),
            ],
            'sections': [
                {
                    'eyebrow': 'Foundation',
                    'title': 'Network infrastructure is invisible, but critical',
                    'paragraphs': [
                        'When a network works, nobody thinks about it. When it drops, slows down, or behaves unpredictably, everyone notices. Staff gets blocked, cameras lose streams, payments drag, and the issue often traces back to the physical layer.',
                        'The cause is not always the switch or router. Very often it is the cabling itself: a bad termination, a damaged run, a poor patch cord, or a mechanical room that has become unreadable over time.',
                        'Structured cabling is not just copper in a wall. It is a foundation. If that foundation is weak, everything you build on top of it becomes harder to support, slower to troubleshoot, and more expensive to grow.',
                    ],
                    'cards': [
                        ('Intermittent drops', 'The network cuts out for a few seconds and comes back. Often the real issue is a bad physical connection or damaged cable.'),
                        ('Performance below expectation', 'You paid for Gigabit but you are seeing much less. Cable category and component quality can quietly become the bottleneck.'),
                        ('Mechanical room chaos', 'Unlabeled cables, unnecessary slack, and improvised pathways turn every incident into a slow diagnosis.'),
                        ('New additions become painful', 'No free port where it is needed, no spare capacity, and no plan. Every new device becomes a mini-project.'),
                    ],
                    'callout_label': 'Key takeaway',
                    'callout': 'Well-planned cabling is noticeable because nobody has to think about it. Disorganized cabling always gets paid for later in time, money, and stress.',
                },
                {
                    'eyebrow': 'Cable types',
                    'title': 'Coax, Cat6, Cat6A, fiber: which one fits which job',
                    'paragraphs': [
                        'Each cable type has strengths, limits, and a proper role. The right choice depends on distance, bandwidth targets, the devices being supported, and how much growth you want to plan for over the coming years.',
                    ],
                    'table': {
                        'caption': 'Quick comparison of the main cabling types',
                        'columns': ('Type', 'Positioning', 'Bandwidth / use', 'Distance', 'When to choose it'),
                        'rows': (
                            ('Coaxial', ('Legacy', 'red'), 'Analog CCTV, TV distribution', 'Up to 300 m', 'Useful for existing analog systems, but rarely the right answer for a new IP project.'),
                            ('Cat5e', ('Aging', 'amber'), '1 Gbps', '100 m', 'Acceptable for extending an existing install, but rarely the right choice for new work.'),
                            ('Cat6', ('Recommended', 'green'), '1 Gbps, 10 Gbps up to 55 m, PoE', '100 m', 'The current standard for offices, retail, WiFi, VoIP, and IP cameras.'),
                            ('Cat6A', ('Higher capacity', 'green'), '10 Gbps over 100 m', '100 m', 'Useful for copper uplinks, server rooms, and more demanding environments.'),
                            ('Fiber optic', ('Backbone', 'green'), 'High throughput, long-distance links', 'Several kilometers', 'Best for building interconnects and high-capacity backbone links.'),
                        ),
                    },
                    'subsections': [
                        {
                            'title': 'Coax: mostly relevant in legacy environments',
                            'paragraphs': [
                                'Coax still has a place in some analog systems and TV distribution. But once you need IP surveillance, PoE, flexible network design, or future growth, its limitations show up quickly.',
                            ],
                        },
                        {
                            'title': 'Cat5e, Cat6, Cat6A: copper Ethernet at different project levels',
                            'paragraphs': [
                                'Cat5e can still be acceptable in an existing environment, but it is aging badly as a default standard for new installations. Cat6 is still the best cost-to-performance balance for most commercial deployments.',
                                'Cat6A becomes the better fit when you need 10 Gbps over the full 100 meters, better resistance to interference, or more headroom for dense environments like server rooms and copper backbones.',
                            ],
                        },
                        {
                            'title': 'Fiber: for distance, backbone, and long-term growth',
                            'paragraphs': [
                                'When you need to link buildings, build vertical risers in a larger property, or prepare for higher-capacity links, fiber becomes the right tool. It is less forgiving of improvised work, but unmatched for distance and scalability.',
                            ],
                        },
                    ],
                    'quote': 'Choosing the right cable up front costs less than working around the wrong one for the next ten years.',
                },
                {
                    'eyebrow': 'Organization',
                    'title': 'Structured cabling is not just wire in the wall',
                    'paragraphs': [
                        'Running a cable from point A to point B is not enough. Structured cabling is a logical system: labeled patch panels, clean pathways, documented ports, tested runs, and spare capacity planned in advance.',
                    ],
                    'steps': [
                        ('Planning before installation', 'The number of runs, distances, panel locations, and future reserve are decided before the first cable is pulled.'),
                        ('Cable and port identification', 'Every cable, every port, and every wall plate is labeled so a technician can understand the system immediately.'),
                        ('Testing and certification', 'Each run is validated against spec. If the link does not pass properly, it gets redone before handoff.'),
                        ('Planned spare capacity', 'You keep free ports available for new devices, cameras, and future expansion without rebuilding the infrastructure.'),
                        ('Clean routing and mechanical protection', 'Well-managed pathways protect the cabling, simplify inspections, and keep technical rooms readable.'),
                        ('Documentation delivered to the client', 'You end up with a clear infrastructure map, not just an install that only the original technician understands.'),
                    ],
                    'callout_label': 'Why it matters',
                    'callout': 'When the organization is right, adding a device or diagnosing an outage takes minutes instead of hours.',
                },
                {
                    'eyebrow': 'Return',
                    'title': 'Done properly once, paid for once',
                    'paragraphs': [
                        'Structured cabling is often treated like an upfront cost. In practice, it is usually an operational saving. Hours wasted tracing an unlabeled cable, redoing the wrong run, or working around a chaotic network room end up costing more than doing the job properly from the start.',
                    ],
                    'table': {
                        'caption': 'What good cabling changes in practice',
                        'columns': ('Situation', 'Disorganized cabling', 'Structured cabling'),
                        'rows': (
                            ('Add an IP camera or new device', '2 to 4 hours to find a port, improvise a run, and test it.', '15 to 30 minutes with an identified spare port and a clean base already in place.'),
                            ('Diagnose a network outage', 'Several hours with untraced cables and multiple interventions.', 'Fast identification through labels, documented ports, and tested runs.'),
                            ('Change technician or provider', 'The infrastructure has to be rediscovered because it mostly lives in one person’s head.', 'Documentation lets any competent technician take over the environment.'),
                            ('Long-term network performance', 'Gradual degradation and bottlenecks that are harder to explain.', 'More predictable, more stable performance that is easier to upgrade.'),
                            ('Expand or renovate the site', 'Part of the work has to be redone because nothing was planned for growth.', 'Spare capacity lets you add cleanly without disturbing what already works.'),
                        ),
                    },
                    'quote': 'The best cabling is usually the cabling you stop hearing about after installation.',
                },
                {
                    'eyebrow': 'Opticable',
                    'title': 'We install for the next 10 years',
                    'paragraphs': [
                        'At Opticable, structured cabling is not an add-on around other services. It is a core part of how we deliver cleaner, more supportable technology environments.',
                        'We assess the need, choose the right medium, install cleanly, certify the runs, and hand over documentation that remains usable later. The goal is not just to make it work on day one. The goal is to keep the infrastructure clear and useful for years.',
                    ],
                    'cards': [
                        ('Cat6 / Cat6A structured cabling', 'Clean copper infrastructure for workstations, WiFi, IP telephony, cameras, and other network-connected systems.'),
                        ('Fiber optic installation', 'Backbone links, building interconnects, and higher-capacity transport for growing environments.'),
                        ('Panels and technical rooms', 'Rack organization, patch panels, clearer labeling, and technical spaces that are easier to support.'),
                        ('Certification and documentation', 'Validated runs, delivered diagrams, and better continuity for future maintenance.'),
                        ('PoE for cameras and WiFi', 'Power and data over the same clean foundation for modern IP systems.'),
                        ('Audit and remediation', 'Assessment of an existing infrastructure to correct weak points before they become major problems.'),
                    ],
                },
            ],
            'cta': {
                'title': 'Your infrastructure deserves better than temporary fixes',
                'copy': 'Tell us about your project. We will assess the site, explain what we recommend, and show you why.',
                'primary_label': 'Request a quote',
                'primary_key': 'contact',
                'secondary_label': 'View structured cabling service',
                'secondary_key': 'structured-cabling',
            },
        },
        'fr': {
            'path': '/fr/blogue/pourquoi-le-cablage-structure-change-tout/',
            'title': 'Pourquoi le câblage structuré change tout | Opticable',
            'desc': "Pourquoi le câblage structuré reste la vraie fondation d'un réseau performant, supportable et prêt pour les années à venir.",
            'eyebrow': 'Câblage structuré',
            'headline': 'Un réseau solide, ça commence dans les murs.',
            'intro': "On parle souvent de WiFi, de switches et de fibre. On parle beaucoup moins du câblage qui se cache derrière. Pourtant, c'est lui qui détermine la performance, la stabilité et la capacité d'évolution du reste de l'infrastructure.",
            'excerpt': "Quand le câblage est mal planifié, chaque ajout, panne ou expansion coûte plus cher. Bien fait, il devient une base propre, invisible et durable pour tout le reste.",
            'tags': ['Câblage structuré', 'Infrastructure réseau'],
            'hero_image': SERVICE_CABLING_URL,
            'hero_image_position': '52% 52%',
            'summary': [
                ('La vraie base', "Le câblage physique détermine la stabilité et la performance de tout le réseau."),
                ('Le bon choix', 'Cat6, Cat6A et fibre ne jouent pas le même rôle dans un projet sérieux.'),
                ('Le vrai retour', 'Identification, certification et capacité de réserve évitent des heures perdues plus tard.'),
            ],
            'sections': [
                {
                    'eyebrow': 'La base',
                    'title': "L'infrastructure réseau est invisible, mais critique",
                    'paragraphs': [
                        "Quand un réseau fonctionne, personne n'y pense. Quand il tombe, ralentit ou décroche, tout le monde le remarque. Employés bloqués, caméras sans flux, paiements ralentis : le problème finit souvent par remonter à la couche physique.",
                        "La cause n'est pas toujours le switch ou le routeur. Très souvent, c'est le câblage : une terminaison mal faite, un run endommagé, un patch cord de mauvaise qualité ou une salle mécanique devenue illisible avec le temps.",
                        "Le câblage structuré, ce n'est pas juste du cuivre dans un mur. C'est une fondation. Si elle est bancale, tout ce qu'on ajoute par-dessus devient plus fragile, plus lent et plus coûteux à faire évoluer.",
                    ],
                    'cards': [
                        ('Coupures intermittentes', "Le réseau tombe quelques secondes puis revient. Souvent, le vrai problème est une terminaison ou un câble physique dégradé."),
                        ('Débit sous les attentes', "Vous payez pour du Gigabit, mais vous voyez des performances bien plus faibles. La catégorie de câble ou la qualité des composants finit par limiter le résultat."),
                        ('Salle mécanique en chaos', "Câbles non identifiés, longueurs inutiles et chemins improvisés. Au premier incident, le diagnostic prend des heures au lieu de minutes."),
                        ("Ajouts devenus compliqués", "Pas de port libre au bon endroit, aucun spare prévu, aucun plan clair. Chaque nouveau device devient un mini-projet."),
                    ],
                    'callout_label': 'À retenir',
                    'callout': "Un câblage bien planifié se remarque justement parce qu'on n'a plus besoin d'y penser. Un câblage désordonné finit toujours par se payer en temps, en argent et en stress.",
                },
                {
                    'eyebrow': 'Types de câblage',
                    'title': 'Coax, Cat6, Cat6A, fibre : lequel pour quel besoin',
                    'paragraphs': [
                        "Chaque type de câble a ses forces, ses limites et son rôle. Le bon choix dépend de la distance, du débit voulu, du type d'équipement à alimenter et de la marge de croissance qu'on veut garder pour les prochaines années.",
                    ],
                    'table': {
                        'caption': 'Comparatif rapide des principaux types de câblage',
                        'columns': ('Type', 'Positionnement', 'Débit / usage', 'Distance', "Quand le choisir"),
                        'rows': (
                            ('Coaxial', ('Héritage', 'red'), 'CCTV analogique, distribution TV', "Jusqu'à 300 m", 'Pour des installations analogiques existantes, rarement pour un nouveau projet IP.'),
                            ('Cat5e', ('Vieillissant', 'amber'), '1 Gbps', '100 m', 'Acceptable pour compléter un existant, mais rarement le bon choix pour du neuf.'),
                            ('Cat6', ('Recommandé', 'green'), '1 Gbps, 10 Gbps jusqu’à 55 m, PoE', '100 m', 'Le standard actuel pour bureaux, commerces, WiFi, VoIP et caméras IP.'),
                            ('Cat6A', ('Haute capacité', 'green'), '10 Gbps sur 100 m', '100 m', 'Pour des uplinks cuivre, des salles serveurs ou des environnements plus exigeants.'),
                            ('Fibre optique', ('Backbone', 'green'), 'Très haut débit, longues distances', 'Plusieurs kilomètres', 'Pour les interconnexions de bâtiments et les liens backbone.'),
                        ),
                    },
                    'subsections': [
                        {
                            'title': 'Le coaxial : utile surtout dans les environnements hérités',
                            'paragraphs': [
                                "Le coax reste pertinent pour certains systèmes analogiques existants ou pour de la distribution TV. Mais dès qu'on parle de surveillance IP, de PoE, de flexibilité réseau ou de croissance, il montre vite ses limites.",
                            ],
                        },
                        {
                            'title': 'Cat5e, Cat6, Cat6A : le cuivre Ethernet selon le niveau de projet',
                            'paragraphs': [
                                "Le Cat5e peut encore dépanner sur une base existante, mais il vieillit mal comme standard pour de nouvelles installations. Le Cat6 reste aujourd'hui le meilleur équilibre coût / performance pour la majorité des déploiements commerciaux.",
                                "Le Cat6A prend le relais quand il faut garantir du 10 Gbps sur 100 mètres, mieux contrôler les interférences ou préparer un environnement plus dense comme une salle serveurs ou un backbone cuivre.",
                            ],
                        },
                        {
                            'title': 'La fibre : pour la distance, le backbone et la marge de croissance',
                            'paragraphs': [
                                "Quand il faut relier des bâtiments, monter des liens verticaux dans un grand immeuble ou préparer de gros besoins en bande passante, la fibre devient le bon outil. Elle tolère mal l'improvisation, mais elle reste imbattable sur la distance et l'évolutivité.",
                            ],
                        },
                    ],
                    'quote': "Choisir le bon câble au départ coûte moins cher que contourner un mauvais choix pendant les dix années suivantes.",
                },
                {
                    'eyebrow': 'Organisation',
                    'title': "Le câblage structuré, ce n'est pas juste du fil dans le mur",
                    'paragraphs': [
                        "Tirer un câble d'un point A à un point B ne suffit pas. Un câblage structuré, c'est un système logique : panneaux de distribution identifiés, chemins propres, ports documentés, runs testés et capacité de réserve pensée d'avance.",
                    ],
                    'steps': [
                        ("Planification avant l'installation", "Nombre de runs, longueurs, emplacements des panneaux et réserves futures sont définis avant de toucher au premier câble."),
                        ('Identification des câbles et des ports', "Chaque câble, chaque port et chaque prise murale sont identifiés pour qu'un technicien puisse s'y retrouver immédiatement."),
                        ('Tests et certification', "Chaque run est validé selon les specs. Si le lien ne passe pas correctement, il est repris avant la livraison."),
                        ('Capacité de réserve planifiée', "On garde des ports libres pour les nouveaux devices, les caméras ou les expansions à venir sans devoir refaire l'infrastructure."),
                        ('Passage propre et protection mécanique', "Des trajets bien gérés protègent les câbles, facilitent les inspections et gardent la salle technique lisible."),
                        ('Documentation remise au client', "Vous récupérez une vue claire de l'infrastructure, pas seulement une installation que seul l'installateur connaît."),
                    ],
                    'callout_label': 'Ce qui fait la différence',
                    'callout': "Quand l'organisation est bonne, ajouter un device ou diagnostiquer une panne prend des minutes au lieu d'heures.",
                },
                {
                    'eyebrow': 'ROI',
                    'title': 'Bien fait une fois, payé une seule fois',
                    'paragraphs': [
                        "Le câblage structuré est souvent vu comme un coût initial. En pratique, c'est surtout une économie opérationnelle. Les heures perdues à retrouver un câble, à refaire un run mal choisi ou à contourner une salle mécanique confuse finissent par coûter beaucoup plus cher que le travail bien fait dès le départ.",
                    ],
                    'table': {
                        'caption': 'Ce que le bon câblage change concrètement',
                        'columns': ('Situation', 'Câblage désordonné', 'Câblage structuré'),
                        'rows': (
                            ('Ajouter une caméra IP ou un nouveau device', '2 à 4 heures pour trouver un port, improviser un câble et tester.', '15 à 30 minutes avec un port spare identifié et une base déjà propre.'),
                            ('Diagnostiquer une coupure réseau', 'Plusieurs heures avec des câbles non tracés et des interventions multiples.', 'Identification rapide grâce aux repères, aux ports documentés et aux runs testés.'),
                            ('Changer de technicien ou de fournisseur', "L'infrastructure doit être redécouverte parce qu'elle vit surtout dans la tête d'une personne.", "La documentation permet à n'importe quel technicien compétent de reprendre le dossier."),
                            ('Performance réseau à long terme', "Dégradation progressive et goulots d'étranglement plus difficiles à expliquer.", "Performance plus prévisible, plus stable et plus simple à faire évoluer."),
                            ('Expansion ou rénovation du site', "Une partie du travail doit être refaite parce que rien n'avait été prévu d'avance.", "La capacité de réserve permet d'ajouter proprement sans casser l'existant."),
                        ),
                    },
                    'quote': "Le meilleur câblage, c'est souvent celui dont vous n'entendez plus parler après l'installation.",
                },
                {
                    'eyebrow': 'Opticable',
                    'title': 'On installe pour les 10 prochaines années',
                    'paragraphs': [
                        "Chez Opticable, le câblage structuré n'est pas un ajout autour d'autres services. C'est une partie centrale de la façon dont on livre des environnements technologiques propres, supportables et cohérents.",
                        "On analyse les besoins, on choisit le bon média, on installe proprement, on certifie les runs et on remet une documentation exploitable. Le but n'est pas seulement que ça marche au jour un. Le but est que l'infrastructure reste claire et utile pendant des années.",
                    ],
                    'cards': [
                        ('Câblage Cat6 / Cat6A', 'Base cuivre propre pour postes, WiFi, téléphonie IP, caméras et autres équipements réseau.'),
                        ('Installation fibre optique', 'Liens backbone, interconnexions entre bâtiments et capacités élevées pour les environnements qui grandissent.'),
                        ('Panneaux et salles techniques', 'Organisation des racks, panneaux de distribution, repérage clair et environnement plus facile à supporter.'),
                        ('Certification et documentation', 'Validation des runs, remise des schémas et meilleure continuité pour le support futur.'),
                        ('PoE pour caméras et WiFi', 'Alimentation et données sur une même base propre pour les systèmes IP modernes.'),
                        ('Audit et remise en ordre', "Analyse d'une infrastructure existante pour corriger les faiblesses avant qu'elles deviennent un vrai problème."),
                    ],
                },
            ],
            'cta': {
                'title': 'Votre infrastructure mérite mieux que du provisoire',
                'copy': "Parlez-nous de votre projet. On évalue votre site, on vous dit exactement ce qu'on recommande et pourquoi.",
                'primary_label': 'Obtenir une soumission',
                'primary_key': 'contact',
                'secondary_label': 'Voir le service câblage',
                'secondary_key': 'structured-cabling',
            },
        },
    },
}

ARTICLE_PAGE_KEYS |= set(BLOG_ARTICLES.keys())

CASE_STUDY_ORDER = (
    'case-office-building',
    'case-multitenant-building',
    'case-retail-space',
    'case-construction-site',
)
CASE_STUDIES = {
    'en': {
        'parent': {
            'title': 'Case Studies — Typical Projects | Opticable',
            'desc': 'See how Opticable supports office buildings, retail spaces, multi-tenant properties, and construction sites across Quebec.',
            'h1': 'Case studies — How we approach different project types',
            'intro': 'These representative project scenarios show how we approach different building types and operating conditions. Every site is different, but the examples reflect how we scope and coordinate systems in the field.',
            'card_copy': {
                'case-office-building': 'Office building with routing, switching, WiFi access points, cameras, and access control coordinated together.',
                'case-multitenant-building': 'Multi-tenant residential property with video intercom, cameras, WiFi access points, and controlled entry in common areas.',
                'case-retail-space': 'Retail space with cameras, access control, WiFi access points, and routing coordinated together.',
                'case-construction-site': 'Construction project coordinated in phases around cabling, switching, WiFi access points, cameras, and access systems.',
            },
        },
        'items': {
            'case-office-building': {
                'nav': 'Office building',
                'title': 'Case Study — Commercial Office Building | Opticable',
                'desc': 'How Opticable installs and manages security, WiFi, and cabling systems in a commercial office building in Quebec.',
                'h1': 'Typical project — Commercial office building',
                'context': 'Three-storey office building with about 25 workstations, two main entries, indoor and outdoor parking, and a basement server room.',
                'challenges': ['Access control at the main entry and restricted areas such as the server room and archives', 'Stable WiFi coverage for offices and the conference room', 'Camera coverage at entries, parking areas, and main corridors', 'Disorganized legacy cabling in the network room'],
                'work': ['Installation of access control on four doors with badge readers and centralized management', 'Deployment of eight WiFi access points with managed switches and dedicated Cat 6 cabling', 'Installation of 12 IP cameras with remote viewing and coordinated management with the access system', 'Router deployment and full cleanup of the network room with rack, patch panels, and identification of all points', 'Installation of 25 new network drops for workstations'],
                'result': 'The building is fully cabled, secured, and connected through one coordinated operating environment. The property manager supervises cameras and access from a single workflow, and the network room is documented and organized.',
                'systems': 'Router · Managed switches · WiFi access points · IP cameras · Access control',
                'cta_title': 'Does this project look like yours?',
                'cta_copy': 'Tell us about your building.',
            },
            'case-multitenant-building': {
                'nav': 'Multi-tenant building',
                'title': 'Case Study — Multi-Tenant Building | Opticable',
                'desc': 'How Opticable installs intercom, cameras, WiFi, and cabling in a multi-tenant building in Quebec.',
                'h1': 'Typical project — Multi-tenant residential building',
                'context': '24-unit building across four storeys with two secure entries, indoor parking, a laundry room, and a shared room on the ground floor.',
                'challenges': ['Main entry without a working intercom', 'No cameras in common areas', 'No WiFi in corridors and shared spaces', 'Unstructured suite cabling'],
                'work': ['Installation of a video intercom at the main entry with full integration to the access-control system', 'Installation of 10 IP cameras in corridors, entries, and parking areas', 'Deployment of WiFi access points and managed switches in corridors and common areas', 'Router deployment, Cat 6 cabling in shared areas, and organization of the network room'],
                'result': 'The property manager controls entry remotely, reviews cameras from a phone, and manages the intercom and access rights from one coordinated workflow. Residents benefit from reliable WiFi coverage in shared spaces.',
                'systems': 'Router · Managed switches · WiFi access points · IP cameras · Video intercom · Access control',
                'cta_title': 'Do you manage a multi-tenant building?',
                'cta_copy': 'Let’s discuss your project.',
            },
            'case-retail-space': {
                'nav': 'Retail and sales floor',
                'title': 'Case Study — Retail and Sales Space | Opticable',
                'desc': 'How Opticable installs cameras, access control, and WiFi in a retail environment in Quebec.',
                'h1': 'Typical project — Retail and point-of-sale environment',
                'context': 'Retail store across two levels with a sales floor, rear warehouse, management office, and outdoor parking.',
                'challenges': ['No surveillance of the cash area and site entries', 'Unstable WiFi for payment terminals and staff', 'Uncontrolled access to the warehouse', 'Remote viewing needed for the owner'],
                'work': ['Installation of eight IP cameras covering the sales floor, cash area, warehouse, and parking', 'Replacement of the WiFi with three WiFi access points and managed switches, with separate SSIDs for customers and payment terminals', 'Installation of an access-control reader on the warehouse door', 'Router deployment and remote viewing setup on the owner’s mobile phone'],
                'result': 'The owner supervises the store remotely, the WiFi remains stable for operations, and the warehouse stays restricted to authorized staff through the same access and camera management stack.',
                'systems': 'Router · Managed switches · WiFi access points · IP cameras · Access control',
                'cta_title': 'Do you need to secure a retail space?',
                'cta_copy': 'Tell us what you need.',
            },
            'case-construction-site': {
                'nav': 'Construction site',
                'title': 'Case Study — Construction Site | Opticable',
                'desc': 'How Opticable coordinates cabling, cameras, and WiFi on a construction project in Quebec.',
                'h1': 'Typical project — Technology coordination on an active site',
                'context': 'Six-storey commercial building under construction with a general contractor, three delivery phases, and one technical room per floor.',
                'challenges': ['Structured cabling must be installed before walls are closed', 'Coordination with electricians for pathways', 'Technical rooms must be organized early in the build', 'Security systems and WiFi must be ready at handover'],
                'work': ['Cat 6A cabling pulled through all suites before wall closure — Phase 1', 'Deployment of routing, managed switches, racks, and patch panels in six technical rooms — Phase 2', 'Deployment of IP cameras, access control, and WiFi access points aligned with final delivery — Phase 3', 'Complete documentation delivered to the general contractor and owner'],
                'result': 'The technology scope is delivered in line with the construction schedule. No delays are caused by building systems, and the documentation package is clean at handover.',
                'systems': 'Routing · Managed switches · WiFi access points · IP cameras · Access control',
                'cta_title': 'Are you building or renovating a property?',
                'cta_copy': 'Coordinate the systems now.',
            },
        },
    },
    'fr': {
        'parent': {
            'title': 'Études de cas — Projets types | Opticable',
            'desc': 'Découvrez comment Opticable intervient dans les immeubles de bureaux, commerces, multilogements, immeubles multilogements et chantiers de construction au Québec.',
            'h1': 'Études de cas — Comment on intervient selon le projet',
            'intro': "Voici des exemples de projets types représentatifs de nos interventions. Chaque bâtiment est différent — ces scénarios illustrent notre approche et les systèmes qu'on déploie selon le contexte.",
            'card_copy': {
                'case-office-building': 'Immeuble de bureaux avec routage, commutation, points d’accès WiFi, caméras et contrôle d’accès coordonnés ensemble.',
                'case-multitenant-building': 'Immeuble multilogement avec intercom vidéo, caméras, points d’accès WiFi et accès contrôlés dans les aires communes.',
                'case-retail-space': 'Commerce avec caméras, contrôle d’accès, points d’accès WiFi et routage coordonnés ensemble.',
                'case-construction-site': 'Chantier coordonné en phases autour du câblage, de la commutation, du WiFi, des caméras et des accès.',
            },
        },
        'items': {
            'case-office-building': {
                'nav': 'Immeuble de bureaux',
                'title': 'Étude de cas — Immeuble de bureaux commercial | Opticable',
                'desc': "Comment Opticable installe et gère les systèmes de sécurité, WiFi et câblage dans un immeuble de bureaux commercial au Québec.",
                'h1': 'Projet type — Immeuble de bureaux commercial',
                'context': 'Immeuble de bureaux de 3 étages, environ 25 postes de travail, 2 entrées principales, stationnement extérieur et intérieur, salle de serveurs au sous-sol.',
                'challenges': ["Contrôle d'accès à l'entrée principale et aux zones restreintes (salle de serveurs, archives)", 'Couverture WiFi stable pour tous les bureaux et la salle de conférence', 'Caméras sur les entrées, le stationnement et les couloirs principaux', 'Câblage existant désorganisé dans le local réseau'],
                'work': ["Installation d'un contrôle d'accès sur 4 portes avec lecteurs de badge et gestion centralisée", 'Déploiement de 8 points d’accès WiFi avec commutateurs gérés et câblage Cat 6 dédié', 'Installation de 12 caméras IP avec visionnement à distance et gestion coordonnée avec les accès', 'Déploiement du routeur et remise en ordre complète du local réseau : rack, patch panels, identification de tous les points', 'Câblage de 25 nouveaux points réseau pour les postes de travail'],
                'result': "Un bâtiment entièrement câblé, sécurisé et connecté, géré dans une même logique opérationnelle pour les caméras et les accès. Le gestionnaire supervise le site à distance et le local réseau est documenté et propre.",
                'systems': "Routeur · Commutateurs gérés · Points d'accès WiFi · Caméras IP · Contrôle d'accès",
                'cta_title': 'Ce projet ressemble au vôtre ?',
                'cta_copy': 'Décrivez-nous votre bâtiment.',
            },
            'case-multitenant-building': {
                'nav': 'Immeuble multilogement',
                'title': 'Étude de cas — Immeuble multilogement | Opticable',
                'desc': "Comment Opticable installe intercom, caméras, WiFi et câblage dans un immeuble multilogement au Québec.",
                'h1': 'Projet type — Immeuble multilogement résidentiel',
                'context': 'Immeuble de 24 unités, 4 étages, 2 entrées sécurisées, stationnement intérieur, buanderie et salle commune au rez-de-chaussée.',
                'challenges': ["Entrée principale sans intercom fonctionnel", 'Aucune caméra dans les aires communes', 'WiFi inexistant dans les corridors et espaces communs', 'Câblage des suites non structuré'],
                'work': ["Installation d'un intercom vidéo à l'entrée principale avec intégration complète au contrôle d'accès", 'Installation de 10 caméras IP dans les corridors, entrées et stationnement', 'Déploiement de points d’accès WiFi et de commutateurs gérés dans les corridors et espaces communs', 'Déploiement du routeur, câblage Cat 6 dans les aires communes et organisation du local réseau'],
                'result': "Le gestionnaire contrôle l'accès à distance, visualise les caméras depuis son téléphone et gère l'intercom et les accès dans une même logique. Les résidents bénéficient d'une couverture WiFi fiable dans tous les espaces communs.",
                'systems': "Routeur · Commutateurs gérés · Points d'accès WiFi · Caméras IP · Intercom vidéo · Contrôle d'accès",
                'cta_title': 'Vous gérez un immeuble multilogement ?',
                'cta_copy': 'Parlons de votre projet.',
            },
            'case-retail-space': {
                'nav': 'Commerce et espace de vente',
                'title': 'Étude de cas — Commerce et espace de vente | Opticable',
                'desc': "Comment Opticable installe caméras, contrôle d'accès et WiFi dans un commerce au Québec.",
                'h1': 'Projet type — Commerce et espace de vente au détail',
                'context': "Commerce de détail sur 2 niveaux, zone de vente, entrepôt à l'arrière, bureau de gestion et stationnement extérieur.",
                'challenges': ["Aucune surveillance de la zone de caisse et des entrées/sorties", 'WiFi instable pour les terminaux de paiement et les employés', "Accès à l'entrepôt non contrôlé", 'Besoin de visionnement à distance pour le propriétaire'],
                'work': ["Installation de 8 caméras IP couvrant la zone de vente, la caisse, l'entrepôt et le stationnement", 'Remplacement du WiFi par 3 points d’accès WiFi avec commutateurs gérés et SSID séparé pour les clients et les terminaux', "Installation d'un lecteur de contrôle d'accès sur la porte de l'entrepôt", 'Déploiement du routeur et configuration du visionnement à distance sur téléphone mobile pour le propriétaire'],
                'result': "Le propriétaire surveille son commerce à distance, le WiFi est stable pour les opérations et l'entrepôt est accessible uniquement au personnel autorisé via la même pile de gestion que les caméras.",
                'systems': "Routeur · Commutateurs gérés · Points d'accès WiFi · Caméras IP · Contrôle d'accès",
                'cta_title': 'Vous avez un commerce à sécuriser ?',
                'cta_copy': 'Décrivez-nous vos besoins.',
            },
            'case-construction-site': {
                'nav': 'Chantier de construction',
                'title': 'Étude de cas — Chantier de construction | Opticable',
                'desc': "Comment Opticable coordonne le câblage, les caméras et le WiFi sur un chantier de construction au Québec.",
                'h1': 'Projet type — Coordination technologique sur chantier',
                'context': 'Immeuble commercial de 6 étages en construction, entrepreneur général, livraison en 3 phases, local technique par étage.',
                'challenges': ['Câblage structuré à installer avant la fermeture des cloisons', 'Coordination avec les électriciens pour les cheminements', 'Locaux techniques à organiser dès la structure', 'Systèmes de sécurité et WiFi à livrer à la remise des clés'],
                'work': ['Tirage du câblage Cat 6A dans toutes les suites avant la fermeture des murs — Phase 1', 'Déploiement du routage, des commutateurs gérés, des racks et patch panels dans les 6 locaux techniques — Phase 2', "Déploiement des caméras IP, du contrôle d'accès et des points d’accès WiFi coordonné avec la livraison — Phase 3", "Documentation complète remise à l'entrepreneur général et au propriétaire"],
                'result': 'Livraison technologique complète alignée sur le calendrier de construction. Aucun retard lié aux systèmes. Documentation propre remise à la livraison finale.',
                'systems': "Routage · Commutateurs gérés · Points d'accès WiFi · Caméras IP · Contrôle d'accès",
                'cta_title': 'Vous construisez ou rénovez un bâtiment ?',
                'cta_copy': 'Coordonnons les systèmes dès maintenant.',
            },
        },
    },
}

CASE_STUDIES['en'] = {
    'parent': {
        'title': 'Case studies — Typical projects | Opticable',
        'desc': 'See how Opticable works in office buildings, retail spaces, multi-tenant properties, and construction sites across Quebec.',
        'h1': 'Case studies — How we approach different project types',
        'intro': 'Here are representative example projects. Every building is different, but these scenarios illustrate our approach and the systems we deploy based on the context.',
        'card_copy': {
            'case-office-building': 'Office building with routing, switching, WiFi access points, cameras, and access control coordinated together.',
            'case-multitenant-building': 'Multi-tenant property with video intercom, cameras, WiFi access points, and controlled entry in common areas.',
            'case-retail-space': 'Retail space with cameras, access control, WiFi access points, and routing coordinated together.',
            'case-construction-site': 'Construction site coordinated in phases around cabling, switching, WiFi access points, cameras, and access systems.',
        },
    },
    'items': {
        'case-office-building': {
            'nav': 'Office building',
            'title': 'Case study — Commercial office building | Opticable',
            'desc': 'How Opticable installs and manages security, WiFi, and cabling systems in a commercial office building in Quebec.',
            'h1': 'Typical project — Commercial office building',
            'context': 'Three-storey office building with about 25 workstations, two main entries, outdoor and indoor parking, and a server room in the basement.',
            'challenges': ['Access control at the main entry and restricted areas such as the server room and archives', 'Stable WiFi coverage for all offices and the conference room', 'Cameras covering the entries, parking, and main corridors', 'Disorganized legacy cabling in the network room'],
            'work': ['Installation of access control on 4 doors with badge readers and centralized management', 'Deployment of 8 WiFi access points with managed switches and dedicated Cat 6 cabling', 'Installation of 12 IP cameras with remote viewing and coordinated management with the access system', 'Deployment of a router and complete organization of the network room, including rack, patch panels, and full point identification', 'Installation of 25 new network drops for workstations'],
            'result': 'A building that is fully cabled, secured, and connected, managed from one coordinated operating environment for cameras and access. The property manager supervises the site remotely and the network room is documented and clean.',
            'systems': 'Router · Managed switches · WiFi access points · IP cameras · Access control',
            'cta_title': 'Does this project look like yours?',
            'cta_copy': 'Tell us about your building.',
        },
        'case-multitenant-building': {
            'nav': 'Multi-tenant building',
            'title': 'Case study — Multi-tenant building | Opticable',
            'desc': 'How Opticable installs intercom, cameras, WiFi, and cabling in a multi-tenant building in Quebec.',
            'h1': 'Typical project — Multi-tenant residential building',
            'context': '24-unit building across 4 storeys with 2 secured entries, indoor parking, a laundry room, and a shared room on the ground floor.',
            'challenges': ['Main entry without a working intercom', 'No cameras in the common areas', 'No WiFi in corridors and shared spaces', 'Unstructured suite cabling'],
            'work': ['Installation of a video intercom at the main entry with full access-control integration', 'Installation of 10 IP cameras in corridors, entries, and parking areas', 'Deployment of WiFi access points and managed switches in corridors and common areas', 'Deployment of a router, Cat 6 cabling in the common areas, and organization of the network room'],
            'result': 'The manager controls entry remotely, views the cameras from a phone, and manages the intercom and access rights from one coordinated workflow. Residents benefit from reliable WiFi in all shared spaces.',
            'systems': 'Router · Managed switches · WiFi access points · IP cameras · Video intercom · Access control',
            'cta_title': 'Do you manage a multi-tenant building?',
            'cta_copy': 'Let’s discuss your project.',
        },
        'case-retail-space': {
            'nav': 'Retail and sales floor',
            'title': 'Case study — Retail and sales space | Opticable',
            'desc': 'How Opticable installs cameras, access control, and WiFi in a retail environment in Quebec.',
            'h1': 'Typical project — Retail and point-of-sale environment',
            'context': 'Retail space across 2 levels, with a sales floor, rear warehouse, management office, and outdoor parking.',
            'challenges': ['No surveillance over the cash area and entries', 'Unstable WiFi for payment terminals and staff', 'Uncontrolled access to the warehouse', 'Remote viewing required for the owner'],
            'work': ['Installation of 8 IP cameras covering the sales floor, cash area, warehouse, and parking', 'Replacement of the WiFi with 3 WiFi access points and managed switches, with separate SSIDs for customers and payment terminals', 'Installation of an access-control reader on the warehouse door', 'Deployment of a router and setup of remote viewing on the owner mobile phone'],
            'result': 'The owner monitors the store remotely, the WiFi stays stable for operations, and the warehouse remains restricted to authorized staff through the same management stack used for the cameras.',
            'systems': 'Router · Managed switches · WiFi access points · IP cameras · Access control',
            'cta_title': 'Do you have a retail space to secure?',
            'cta_copy': 'Tell us what you need.',
        },
        'case-construction-site': {
            'nav': 'Construction site',
            'title': 'Case study — Construction site | Opticable',
            'desc': 'How Opticable coordinates cabling, cameras, and WiFi on a construction site in Quebec.',
            'h1': 'Typical project — Technology coordination on a job site',
            'context': 'Six-storey commercial building under construction, one general contractor, delivery in 3 phases, and one technical room per floor.',
            'challenges': ['Structured cabling must be installed before the walls are closed', 'Coordination with electricians for pathways', 'Technical rooms need to be organized from the structural phase', 'Security systems and WiFi must be ready at handoff'],
            'work': ['Cat 6A cabling pulled through all suites before wall closure - Phase 1', 'Deployment of routing, managed switches, racks, and patch panels in the 6 technical rooms - Phase 2', 'Deployment of IP cameras, access control, and WiFi access points coordinated with final delivery - Phase 3', 'Complete documentation delivered to the general contractor and the owner'],
            'result': 'Full technology delivery aligned with the construction schedule. No delays caused by the systems, and clean documentation handed over at final delivery.',
            'systems': 'Routing · Managed switches · WiFi access points · IP cameras · Access control',
            'cta_title': 'Are you building or renovating a property?',
            'cta_copy': 'Let’s coordinate the systems now.',
        },
    },
}

primary_order = [
    'security-camera-systems',
    'access-control-systems',
    'commercial-wifi-installation',
    'intercom-systems',
    'network-infrastructure',
    'managed-it-services',
]
secondary_order = [
    'structured-cabling',
    'fiber-optic-installation',
    'ip-phone-systems',
]
order = primary_order + secondary_order
services_page_chip_keys = tuple(primary_order)
HOME_SERVICE_STYLE_PAGE_KEYS = {'home', 'services', 'about', 'industries'} | set(order) | set(INDUSTRY_DETAIL_KEYS)
ARTICLE_STYLE_PAGE_KEYS = (
    ARTICLE_PAGE_KEYS
    | {'home', 'contact', 'faq', 'guides'}
    | set(order)
    | set(INDUSTRY_DETAIL_KEYS)
    | set(MULTIFAMILY_CLUSTER_KEYS)
)
base_routes = {
    'en': {'home': '/en/', 'services': '/en/services/', 'industries': '/en/industries/', 'case-studies': '/en/case-studies/', 'blog': '/en/blog/', 'about': '/en/about/', 'faq': '/en/faq/', 'contact': '/en/contact/', 'privacy': '/en/privacy/', 'promo': '/en/promo/', 'promo-rules': '/en/promo-rules/', 'promo-unsubscribe': '/en/promo/unsubscribe/', 'promo-admin': '/en/admin/promo/', 'referral-program': '/en/referral-program/', 'referral-program-terms': '/en/referral-program/terms/', 'referral-partner-program': '/en/referral-partner-program/', 'referral-partner-program-terms': '/en/referral-partner-program/terms/', 'referral-portal': '/en/referral-portal/', 'referral-access': '/en/referral-portal/access/', 'referral-admin': '/en/admin/referrals/', 'thanks': '/en/thank-you/', 'case-office-building': '/en/case-studies/office-building/', 'case-multitenant-building': '/en/case-studies/multi-tenant-building/', 'case-retail-space': '/en/case-studies/retail-and-sales-floor/', 'case-construction-site': '/en/case-studies/construction-site/'},
    'fr': {'home': '/', 'services': '/fr/services/', 'industries': '/fr/clientele/', 'case-studies': '/fr/etudes-de-cas/', 'blog': '/fr/blogue/', 'about': '/fr/a-propos/', 'faq': '/fr/faq/', 'contact': '/fr/contact/', 'privacy': '/fr/confidentialite/', 'promo': '/fr/promo/', 'promo-rules': '/fr/reglement-promo/', 'promo-unsubscribe': '/fr/promo/desabonnement/', 'promo-admin': '/fr/admin/promo/', 'referral-program': '/fr/programme-reference/', 'referral-program-terms': '/fr/programme-reference/reglement/', 'referral-partner-program': '/fr/programme-partenaires-referents/', 'referral-partner-program-terms': '/fr/programme-partenaires-referents/reglement/', 'referral-portal': '/fr/portail-references/', 'referral-access': '/fr/portail-references/acces/', 'referral-admin': '/fr/admin/references/', 'thanks': '/fr/merci/', 'case-office-building': '/fr/etudes-de-cas/immeuble-de-bureaux/', 'case-multitenant-building': '/fr/etudes-de-cas/immeuble-multilogement/', 'case-retail-space': '/fr/etudes-de-cas/commerce-espace-de-vente/', 'case-construction-site': '/fr/etudes-de-cas/chantier-de-construction/'},
}
routes = {k: dict(v) for k, v in base_routes.items()}
for key in order:
    routes['en'][key] = f"/en/services/{services[key]['en']['slug']}/"
    routes['fr'][key] = f"/fr/services/{services[key]['fr']['slug']}/"

routes['en']['articles'] = '/en/blog/articles/'
routes['fr']['articles'] = '/fr/blogue/articles/'
for lang, guide_index_page in GUIDE_INDEX_PAGES.items():
    routes[lang]['guides'] = guide_index_page['path']
for lang, detail_pages in INDUSTRY_DETAIL_PAGES_BY_LANG.items():
    for key, page_data in detail_pages.items():
        routes[lang][key] = page_data['path']
for lang, cluster_pages in MULTIFAMILY_CLUSTER_PAGES_BY_LANG.items():
    for key, page_data in cluster_pages.items():
        routes[lang][key] = page_data['path']
for lang, landing_pages in CAMPAIGN_LANDING_PAGES_BY_LANG.items():
    for key, page_data in landing_pages.items():
        routes[lang][key] = page_data['path']

css = '''
:root{--bg:#eef3ef;--surface:rgba(255,255,255,.94);--surface-soft:#f7faf7;--line:#d6e1d9;--line-strong:#b9cbbf;--text:#142019;--muted:#5d6d63;--primary:#2f8a58;--primary-dark:#1f6640;--primary-soft:#e2f0e7;--shadow:0 18px 48px rgba(20,35,27,.08);--radius:28px;--max:1200px}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;min-height:100vh;font-family:"Segoe UI Variable Text","Aptos","Segoe UI",sans-serif;color:var(--text);background:radial-gradient(circle at top left,rgba(47,138,88,.12),transparent 24%),linear-gradient(180deg,#f4f7f3 0%,var(--bg) 40%,#edf2ec 100%)}body::before{content:"";position:fixed;inset:0;background-image:linear-gradient(rgba(21,54,40,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(21,54,40,.03) 1px,transparent 1px);background-size:42px 42px;mask-image:linear-gradient(180deg,rgba(0,0,0,.4),transparent 92%);pointer-events:none}img{display:block;max-width:100%}a{text-decoration:none;color:inherit}button,input,select,textarea{font:inherit}button{cursor:pointer}.skip-link{position:absolute;top:-48px;left:18px;z-index:100;padding:12px 16px;border-radius:999px;background:#153628;color:#fff}.skip-link:focus{top:16px}.site-shell,.gateway-shell{width:min(calc(100% - 40px),var(--max));margin:0 auto}.site-shell{padding:24px 0 64px}.gateway-shell{min-height:100vh;display:grid;align-items:center;padding:40px 0}.site-header{position:sticky;top:16px;z-index:40;margin-bottom:28px}.header-inner{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:16px 20px;border:1px solid rgba(255,255,255,.92);border-radius:999px;background:rgba(255,255,255,.88);box-shadow:var(--shadow);backdrop-filter:blur(18px)}.brand,.footer-brand,.gateway-brand{display:inline-flex;align-items:center;gap:14px;min-width:0}.brand{flex-shrink:0}.brand img{width:clamp(74px,5.4vw,96px);height:auto;transform:translateY(-5px)}.footer-brand img{width:clamp(86px,6vw,108px);height:auto;transform:translateY(-4px)}.gateway-brand img{width:min(190px,100%);height:auto;transform:translateY(-8px)}.brand-copy{display:grid;gap:4px}.brand-copy strong,.eyebrow,.timeline-step span,.chip{letter-spacing:.16em;text-transform:uppercase}.brand-copy strong{font-size:.96rem}.brand-copy small{color:var(--muted);font-size:.84rem}.nav-toggle{display:none;align-items:center;justify-content:center;min-height:46px;padding:0 16px;border:1px solid var(--line);border-radius:999px;background:#fff;font-weight:700}.site-nav{display:flex;flex-wrap:wrap;gap:18px}.site-nav a,.footer-links a,.footer-services a,.text-link{color:var(--muted);transition:color .16s ease}.site-nav a:hover,.site-nav a:focus-visible,.site-nav a[aria-current="page"],.footer-links a:hover,.footer-links a:focus-visible,.footer-services a:hover,.footer-services a:focus-visible,.text-link:hover,.text-link:focus-visible{color:var(--primary-dark)}.header-actions{display:flex;align-items:center;gap:12px}.lang-switch,.button{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;font-weight:700}.lang-switch{min-width:52px;min-height:46px;padding:0 14px;border:1px solid var(--line-strong);background:#fff}.button{min-height:50px;padding:0 22px;border:1px solid transparent;transition:transform .16s ease,background-color .16s ease,border-color .16s ease}.button:hover,.button:focus-visible{transform:translateY(-1px)}.button-primary{background:linear-gradient(135deg,var(--primary) 0%,#44a86e 100%);color:#fff}.button-primary:hover,.button-primary:focus-visible{background:linear-gradient(135deg,var(--primary-dark) 0%,var(--primary) 100%)}.button-secondary{background:#fff;border-color:var(--line-strong);color:var(--text)}main section+section{margin-top:28px}.hero,.page-hero,.cta-band,.contact-layout,.gateway-panel,.two-col{display:grid;gap:24px}.hero,.page-hero,.cta-band,.contact-layout,.gateway-panel,.two-col{grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr)}.hero-copy,.hero-panel,.page-hero-copy,.page-hero-panel,.card,.cta-band,.contact-panel,.form-panel,.gateway-panel,.faq-item,.timeline-step{border:1px solid var(--line);background:var(--surface);box-shadow:var(--shadow)}.hero-copy,.hero-panel,.page-hero-copy,.page-hero-panel,.contact-panel,.form-panel,.cta-band,.gateway-panel{padding:34px;border-radius:var(--radius)}.hero-copy h1,.page-hero-copy h1,.section-heading h2,.cta-band h2,.gateway-panel h1{margin:0;font-family:"Segoe UI Variable Display","Aptos Display","Segoe UI",sans-serif;font-weight:760;line-height:1.03;letter-spacing:-.03em}.hero-copy h1{max-width:12ch;font-size:clamp(2.3rem,4.4vw,4.4rem)}.page-hero-copy h1,.section-heading h2,.cta-band h2,.gateway-panel h1{font-size:clamp(2rem,3.4vw,3.35rem)}.hero-copy>p:not(.eyebrow),.page-hero-copy>p:not(.eyebrow),.section-heading p,.contact-panel p,.gateway-panel p,.footer-note{color:var(--muted);line-height:1.72;font-size:1.02rem}.eyebrow{margin:0 0 14px;color:var(--primary-dark);font-size:.8rem;font-weight:700}.service-detail-panel{display:grid;align-content:start;gap:20px}.service-apply-panel{display:grid;align-content:start;gap:24px}.service-detail-panel .eyebrow,.service-detail-panel h2,.service-apply-panel .eyebrow,.service-apply-panel h2{margin:0}.hero-actions,.page-hero-actions,.cta-actions,.form-footer{display:flex;flex-wrap:wrap;gap:14px;align-items:center}.hero-actions,.page-hero-actions{margin-top:28px}.hero-points,.check-list,.footer-links,.footer-services{margin:0;padding:0;list-style:none}.hero-points,.check-list{display:grid;gap:10px}.hero-points li,.check-list li{position:relative;padding-left:22px;color:var(--muted);line-height:1.62}.hero-points li::before,.check-list li::before{content:"";position:absolute;left:0;top:.62em;width:10px;height:10px;border-radius:50%;background:var(--primary)}
'''
js = '''
const navToggle = document.querySelector('[data-nav-toggle]');
const nav = document.querySelector('[data-site-nav]');
if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const expanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!expanded));
    nav.classList.toggle('is-open', !expanded);
  });
  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navToggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    });
  });
}
document.querySelectorAll('[data-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});
const cookieBanner = document.querySelector('[data-cookie-banner]');
const cookieAccept = document.querySelector('[data-cookie-accept]');
const cookieBannerKey = __COOKIE_BANNER_ACCEPT_KEY__;
if (cookieBanner && cookieAccept) {
  let accepted = false;
  try {
    accepted = window.localStorage.getItem(cookieBannerKey) === 'accepted';
  } catch (error) {
    accepted = false;
  }
  if (!accepted) {
    cookieBanner.hidden = false;
  }
  cookieAccept.addEventListener('click', () => {
    try {
      window.localStorage.setItem(cookieBannerKey, 'accepted');
    } catch (error) {}
    cookieBanner.hidden = true;
  });
}
const lightbox = document.querySelector('[data-image-lightbox]');
const lightboxImage = lightbox?.querySelector('[data-lightbox-image]');
const lightboxCaption = lightbox?.querySelector('[data-lightbox-caption]');
const lightboxClose = lightbox?.querySelector('[data-lightbox-close]');
let lastLightboxTrigger = null;
if (lightbox && lightboxImage && lightboxCaption && lightboxClose) {
  const closeLightbox = () => {
    if (lightbox.hidden) return;
    lightbox.hidden = true;
    document.body.classList.remove('lightbox-open');
    lightboxImage.removeAttribute('src');
    lightboxImage.alt = '';
    lightboxImage.style.removeProperty('--lightbox-image-width');
    lightboxImage.style.removeProperty('--lightbox-image-height');
    lightboxCaption.textContent = '';
    if (lastLightboxTrigger) {
      lastLightboxTrigger.focus();
      lastLightboxTrigger = null;
    }
  };
  document.querySelectorAll('[data-lightbox-trigger]').forEach((trigger) => {
    trigger.addEventListener('click', (event) => {
      const src = trigger.getAttribute('data-lightbox-src');
      if (!src) return;
      event.preventDefault();
      lastLightboxTrigger = trigger;
      lightboxImage.src = src;
      lightboxImage.alt = trigger.getAttribute('data-lightbox-alt') || '';
      const lightboxWidth = trigger.getAttribute('data-lightbox-width');
      const lightboxHeight = trigger.getAttribute('data-lightbox-height');
      if (lightboxWidth) {
        lightboxImage.style.setProperty('--lightbox-image-width', lightboxWidth + 'px');
      } else {
        lightboxImage.style.removeProperty('--lightbox-image-width');
      }
      if (lightboxHeight) {
        lightboxImage.style.setProperty('--lightbox-image-height', lightboxHeight + 'px');
      } else {
        lightboxImage.style.removeProperty('--lightbox-image-height');
      }
      lightboxCaption.textContent = trigger.getAttribute('data-lightbox-caption') || lightboxImage.alt;
      lightbox.hidden = false;
      document.body.classList.add('lightbox-open');
      lightboxClose.focus();
    });
  });
  lightboxClose.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) {
      closeLightbox();
    }
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !lightbox.hidden) {
      closeLightbox();
    }
  });
}
document.querySelectorAll('[data-service-carousel]').forEach((carousel) => {
  const track = carousel.querySelector('[data-carousel-track]');
  const prev = carousel.querySelector('[data-carousel-prev]');
  const next = carousel.querySelector('[data-carousel-next]');
  if (!track || !prev || !next) {
    return;
  }
  const getStep = () => {
    const firstCard = track.querySelector('.service-carousel-card');
    const styles = window.getComputedStyle(track);
    const gap = parseFloat(styles.columnGap || styles.gap || '0');
    return (firstCard ? firstCard.getBoundingClientRect().width : track.clientWidth) + gap;
  };
  const updateButtons = () => {
    const maxScroll = Math.max(track.scrollWidth - track.clientWidth - 4, 0);
    prev.disabled = track.scrollLeft <= 4;
    next.disabled = track.scrollLeft >= maxScroll;
  };
  prev.addEventListener('click', () => {
    track.scrollBy({ left: -getStep(), behavior: 'smooth' });
  });
  next.addEventListener('click', () => {
    track.scrollBy({ left: getStep(), behavior: 'smooth' });
  });
  track.addEventListener('scroll', updateButtons, { passive: true });
  window.addEventListener('resize', updateButtons);
  updateButtons();
});
'''
js = js.replace('__COOKIE_BANNER_ACCEPT_KEY__', json.dumps(COOKIE_BANNER_ACCEPT_KEY))

js += '''
const promoStorageKey = 'opticable-promo-entry';
const promoLocaleMap = { en: 'en-CA', fr: 'fr-CA' };
let promoTurnstileScriptPromise = null;
function readPromoEntry() {
  try {
    const raw = window.localStorage.getItem(promoStorageKey);
    return raw ? JSON.parse(raw) : null;
  } catch (error) {
    return null;
  }
}
function writePromoEntry(entry) {
  try {
    window.localStorage.setItem(promoStorageKey, JSON.stringify(entry));
  } catch (error) {}
}
function clearPromoEntry() {
  try {
    window.localStorage.removeItem(promoStorageKey);
  } catch (error) {}
}
function promoDateLabel(value, lang) {
  if (!value) return '';
  try {
    return new Intl.DateTimeFormat(promoLocaleMap[lang] || 'en-CA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      timeZone: 'America/Toronto',
    }).format(new Date(value));
  } catch (error) {
    return value;
  }
}
function promoEntryActive(entry) {
  if (!entry || !entry.promoExpiresAt) return false;
  return new Date(entry.promoExpiresAt).getTime() > Date.now();
}
function promoPayloadCopy(node, selector) {
  const source = node.querySelector(selector);
  if (!source) return {};
  try {
    return JSON.parse(source.textContent || '{}');
  } catch (error) {
    return {};
  }
}
function promoUtms() {
  const url = new URL(window.location.href);
  return {
    utmSource: url.searchParams.get('utm_source') || '',
    utmMedium: url.searchParams.get('utm_medium') || '',
    utmCampaign: url.searchParams.get('utm_campaign') || '',
    utmContent: url.searchParams.get('utm_content') || '',
    utmTerm: url.searchParams.get('utm_term') || '',
  };
}
function trackPromoAnalyticsEvent(eventName, detail) {
  if (!eventName || typeof window === 'undefined') return;
  const payload = {
    event_category: 'promo',
    promo_campaign_id: detail && detail.campaignId ? detail.campaignId : '',
    promo_discount_percent: detail && typeof detail.discountPercent !== 'undefined' ? detail.discountPercent : null,
    promo_locale: detail && detail.locale ? detail.locale : '',
    promo_code: detail && detail.promoCode ? detail.promoCode : '',
    promo_duplicate: detail && detail.duplicate ? 'true' : 'false',
  };
  if (Array.isArray(window.dataLayer)) {
    window.dataLayer.push({ event: eventName, ...payload });
  }
  if (typeof window.gtag === 'function') {
    window.gtag('event', eventName, payload);
    if (detail && detail.googleAdsSendTo) {
      window.gtag('event', 'conversion', { send_to: detail.googleAdsSendTo });
    }
  }
}
function applyPromoResult(shell, copy, payload, stateLabel, title, description) {
  const panel = shell.querySelector('[data-promo-result]');
  if (!panel || !payload) return;
  const state = panel.querySelector('[data-promo-result-state]');
  const titleNode = panel.querySelector('[data-promo-result-title]');
  const copyNode = panel.querySelector('[data-promo-result-copy]');
  const discountNode = panel.querySelector('[data-promo-result-discount]');
  const codeInput = panel.querySelector('[data-promo-result-code-input]');
  const expiryNode = panel.querySelector('[data-promo-result-expiry]');
  const copyButton = panel.querySelector('[data-promo-result-copy-button]');
  const saveButton = panel.querySelector('[data-promo-result-save-button]');
  if (state) {
    state.textContent = stateLabel || '';
    state.hidden = !stateLabel;
  }
  if (titleNode) titleNode.textContent = title || copy.resultTitle || '';
  if (copyNode) copyNode.textContent = description || copy.resultCopy || '';
  if (discountNode) discountNode.textContent = payload.discountLabel || '';
  if (codeInput) codeInput.value = payload.promoCode || '';
  if (expiryNode) expiryNode.textContent = promoDateLabel(payload.promoExpiresAt, payload.locale || shell.dataset.lang || 'en');
  if (copyButton) {
    copyButton.textContent = copyButton.dataset.copyDefault || copyButton.textContent;
  }
  if (saveButton) {
    saveButton.textContent = saveButton.dataset.saveDefault || saveButton.textContent;
  }
  panel.hidden = false;
  document.body.classList.add('lightbox-open');
}
function loadPromoTurnstileScript() {
  if (window.turnstile) {
    return Promise.resolve(window.turnstile);
  }
  if (!promoTurnstileScriptPromise) {
    promoTurnstileScriptPromise = new Promise((resolve, reject) => {
      const existing = document.querySelector('script[data-promo-turnstile-script]');
      if (existing) {
        existing.addEventListener('load', () => resolve(window.turnstile));
        existing.addEventListener('error', reject);
        return;
      }
      const script = document.createElement('script');
      script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
      script.async = true;
      script.defer = true;
      script.dataset.promoTurnstileScript = 'true';
      script.onload = () => resolve(window.turnstile);
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }
  return promoTurnstileScriptPromise;
}
async function initPromoForms() {
  const promoRoots = document.querySelectorAll('[data-promo-root]');
  if (!promoRoots.length) {
    return;
  }
  clearPromoEntry();
  for (const shell of promoRoots) {
    const lang = shell.dataset.lang || 'en';
    const copy = promoPayloadCopy(shell, '[data-promo-copy]');
    const configUrl = shell.dataset.configUrl;
    const entryUrl = shell.dataset.entryUrl;
    const form = shell.querySelector('[data-promo-form]');
    const submit = shell.querySelector('[data-promo-submit]');
    const status = shell.querySelector('[data-promo-status]');
    const errorNode = shell.querySelector('[data-promo-error]');
    const skillShell = shell.querySelector('[data-promo-skill-shell]');
    const skillPrompt = shell.querySelector('[data-promo-skill-prompt]');
    const turnstileMount = shell.querySelector('[data-promo-turnstile]');
    const resultPanel = shell.querySelector('[data-promo-result]');
    if (!configUrl || !entryUrl || !form || !submit || !status || !errorNode || !skillShell || !skillPrompt || !turnstileMount) {
      continue;
    }
    let config = null;
    let turnstileToken = '';
    let widgetId = null;
    const showError = (message) => {
      errorNode.textContent = message || copy.genericError || '';
      errorNode.hidden = !message;
    };
    const showStatus = (message) => {
      status.textContent = message || '';
      status.hidden = !message;
    };
    const closePromoResult = () => {
      if (!resultPanel || resultPanel.hidden) return;
      resultPanel.hidden = true;
      document.body.classList.remove('lightbox-open');
    };
    if (resultPanel) {
      resultPanel.querySelectorAll('[data-promo-result-close]').forEach((button) => {
        button.addEventListener('click', closePromoResult);
      });
      resultPanel.addEventListener('click', (event) => {
        if (event.target === resultPanel) {
          closePromoResult();
        }
      });
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && !resultPanel.hidden) {
          closePromoResult();
        }
      });
      const copyButton = resultPanel.querySelector('[data-promo-result-copy-button]');
      const saveButton = resultPanel.querySelector('[data-promo-result-save-button]');
      const codeInput = resultPanel.querySelector('[data-promo-result-code-input]');
      const titleNode = resultPanel.querySelector('[data-promo-result-title]');
      const discountNode = resultPanel.querySelector('[data-promo-result-discount]');
      const expiryNode = resultPanel.querySelector('[data-promo-result-expiry]');
      let copyResetTimer = null;
      let saveResetTimer = null;
      if (copyButton && codeInput) {
        copyButton.addEventListener('click', async () => {
          const code = codeInput.value || '';
          if (!code) return;
          let copied = false;
          try {
            await navigator.clipboard.writeText(code);
            copied = true;
          } catch (error) {
            codeInput.focus();
            codeInput.select();
            try {
              copied = document.execCommand('copy');
            } catch (fallbackError) {
              copied = false;
            }
          }
          if (!copied) return;
          copyButton.textContent = copyButton.dataset.copySuccess || copyButton.textContent;
          window.clearTimeout(copyResetTimer);
          copyResetTimer = window.setTimeout(() => {
            copyButton.textContent = copyButton.dataset.copyDefault || copyButton.textContent;
          }, 1800);
        });
      }
      if (saveButton && codeInput) {
        saveButton.addEventListener('click', () => {
          const code = (codeInput.value || '').trim();
          if (!code) return;
          const labels = copy.resultLabels || {};
          const lines = [
            titleNode ? titleNode.textContent.trim() : (copy.resultTitle || ''),
            '',
            `${labels.code || 'Promo code'}: ${code}`,
            `${labels.discount || 'Discount'}: ${discountNode ? discountNode.textContent.trim() : ''}`,
            `${labels.expires || 'Valid until'}: ${expiryNode ? expiryNode.textContent.trim() : ''}`,
            '',
            `${copy.saveQuoteLabel || 'Quote page'}: ${new URL(copy.quotePath || '/', window.location.origin).toString()}`,
          ].filter(Boolean);
          try {
            const blob = new Blob(['\\ufeff', lines.join('\\r\\n')], { type: 'text/plain;charset=utf-8' });
            const link = document.createElement('a');
            const objectUrl = URL.createObjectURL(blob);
            link.href = objectUrl;
            link.download = `${copy.saveFilePrefix || 'opticable-promo-code'}-${code.toLowerCase()}.txt`;
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.setTimeout(() => URL.revokeObjectURL(objectUrl), 2000);
            saveButton.textContent = saveButton.dataset.saveSuccess || saveButton.textContent;
            window.clearTimeout(saveResetTimer);
            saveResetTimer = window.setTimeout(() => {
              saveButton.textContent = saveButton.dataset.saveDefault || saveButton.textContent;
            }, 1800);
          } catch (error) {}
        });
      }
    }
    showStatus(copy.statusLoading || '');
    showError('');
    try {
      const response = await fetch(configUrl, { headers: { Accept: 'application/json' } });
      config = await response.json();
    } catch (error) {
      config = { available: false };
    }
    if (!config || !config.available || !config.turnstileSiteKey || !config.challenge) {
      showStatus(copy.statusUnavailable || '');
      submit.disabled = true;
      continue;
    }
    skillShell.hidden = false;
    skillPrompt.textContent = config.challenge.prompt || '';
    const skillTokenField = form.elements.namedItem('skill_token');
    if (skillTokenField) {
      skillTokenField.value = config.challenge.token || '';
    }
    try {
      const turnstile = await loadPromoTurnstileScript();
      widgetId = turnstile.render(turnstileMount, {
        sitekey: config.turnstileSiteKey,
        action: config.turnstileAction || 'promo-entry',
        callback(token) {
          turnstileToken = token || '';
        },
        'expired-callback'() {
          turnstileToken = '';
        },
        'error-callback'() {
          turnstileToken = '';
        },
      });
      submit.disabled = false;
      showStatus('');
    } catch (error) {
      showStatus(copy.statusUnavailable || '');
      showError(copy.turnstileError || copy.genericError || '');
      submit.disabled = true;
      continue;
    }
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      showError('');
      if (!form.reportValidity()) {
        showError(copy.requiredField || '');
        return;
      }
      if (!form.elements.namedItem('quebec_attestation').checked || !form.elements.namedItem('rules_attestation').checked) {
        showError(copy.requiredConsent || '');
        return;
      }
      const email = String(form.elements.namedItem('email').value || '').trim();
      if (!email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
        showError(copy.invalidEmail || '');
        return;
      }
      if (!turnstileToken) {
        showError(copy.turnstileError || '');
        return;
      }
      const payload = {
        locale: lang,
        name: String(form.elements.namedItem('name').value || '').trim(),
        email,
        phone: String(form.elements.namedItem('phone').value || '').trim(),
        company: String(form.elements.namedItem('company').value || '').trim(),
        skillAnswer: String(form.elements.namedItem('skill_answer').value || '').trim(),
        skillToken: String(form.elements.namedItem('skill_token').value || '').trim(),
        turnstileToken,
        quebecAttestation: form.elements.namedItem('quebec_attestation').checked,
        rulesAttestation: form.elements.namedItem('rules_attestation').checked,
        marketingOptIn: form.elements.namedItem('marketing_opt_in').checked,
        landingPath: window.location.pathname,
        landingUrl: window.location.href,
        referrerUrl: document.referrer || '',
        ...promoUtms(),
      };
      submit.disabled = true;
      const previousLabel = submit.textContent;
      submit.textContent = copy.submitLoading || previousLabel;
      try {
        const response = await fetch(entryUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify(payload),
        });
        const result = await response.json();
        if (!response.ok || !result.ok) {
          showError(result.error || copy.genericError || '');
        } else {
          const entry = result.entry || {};
          const stored = {
            campaignId: result.campaignId,
            discountPercent: entry.discountPercent,
            discountLabel: entry.discountLabel,
            promoCode: entry.promoCode,
            promoExpiresAt: entry.promoExpiresAt,
            locale: lang,
          };
          showStatus('');
          applyPromoResult(
            shell,
            copy,
            stored,
            '',
            result.duplicate ? copy.duplicateTitle : copy.resultTitle,
            result.duplicate ? copy.duplicateCopy : copy.resultCopy
          );
          trackPromoAnalyticsEvent(
            result.duplicate ? 'promo_code_retrieved' : 'promo_code_generated',
            {
              campaignId: result.campaignId || '',
              discountPercent: entry.discountPercent,
              promoCode: entry.promoCode || '',
              locale: lang,
              duplicate: Boolean(result.duplicate),
              googleAdsSendTo: result.duplicate ? '' : __GOOGLE_ADS_PROMO_CONVERSION_SEND_TO__,
            }
          );
          if (resultPanel) {
            const focusTarget = resultPanel.querySelector('[data-promo-result-copy-button]') || resultPanel.querySelector('[data-promo-result-close]');
            if (focusTarget) {
              window.setTimeout(() => focusTarget.focus(), 40);
            }
          }
        }
        if (window.turnstile && widgetId !== null) {
          window.turnstile.reset(widgetId);
          turnstileToken = '';
        }
      } catch (error) {
        showError(copy.genericError || '');
      } finally {
        submit.disabled = false;
        submit.textContent = previousLabel;
      }
    });
  }
}
function initPromoUnsubscribe() {
  document.querySelectorAll('[data-promo-unsubscribe]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-promo-unsubscribe-copy]');
    const form = shell.querySelector('[data-promo-unsubscribe-form]');
    const status = shell.querySelector('[data-promo-unsubscribe-status]');
    const errorNode = shell.querySelector('[data-promo-unsubscribe-error]');
    const url = shell.dataset.unsubscribeUrl;
    const lang = shell.dataset.lang || 'en';
    if (!form || !status || !errorNode || !url) return;
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      status.hidden = true;
      errorNode.hidden = true;
      const email = String(form.elements.namedItem('email').value || '').trim();
      if (!email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
        errorNode.textContent = copy.invalidEmail || '';
        errorNode.hidden = false;
        return;
      }
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ email, locale: lang }),
        });
        const result = await response.json();
        if (!response.ok || !result.ok) {
          throw new Error(result.error || copy.genericError || '');
        }
        status.textContent = result.message || copy.success || '';
        status.hidden = false;
        form.reset();
      } catch (error) {
        errorNode.textContent = error.message || copy.genericError || '';
        errorNode.hidden = false;
      }
    });
  });
}
function promoAdminAttribution(entry, copy) {
  const utmBits = [entry.utm_source, entry.utm_medium, entry.utm_campaign].filter(Boolean);
  if (utmBits.length) {
    return utmBits.join(' / ');
  }
  return entry.referrer_host || copy.none || '—';
}
function promoAdminMarketingLabel(entry, copy) {
  if (entry.marketing_opt_out_at) return copy.marketingOut || copy.none || '—';
  if (entry.marketing_opt_in) return copy.marketingYes || copy.none || '—';
  return copy.marketingNo || copy.none || '—';
}
function promoAdminTableCell(value, className) {
  const cell = document.createElement('td');
  if (className) {
    cell.className = className;
  }
  cell.textContent = value == null || value === '' ? '—' : String(value);
  return cell;
}
function initPromoAdmin() {
  document.querySelectorAll('[data-promo-admin]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-promo-admin-copy]');
    const lang = shell.dataset.lang || 'en';
    const entriesUrl = shell.dataset.entriesUrl;
    const exportUrl = shell.dataset.exportUrl;
    const subscribersExportUrl = shell.dataset.subscribersExportUrl;
    const deleteUrl = shell.dataset.deleteUrl;
    const status = shell.querySelector('[data-promo-admin-status]');
    const errorNode = shell.querySelector('[data-promo-admin-error]');
    const refreshButton = shell.querySelector('[data-promo-admin-refresh]');
    const exportLink = shell.querySelector('[data-promo-admin-export]');
    const subscribersExportLink = shell.querySelector('[data-promo-admin-export-subscribers]');
    const deleteSelectedButton = shell.querySelector('[data-promo-admin-delete-selected]');
    const deleteViewButton = shell.querySelector('[data-promo-admin-delete-view]');
    const scopeButtons = shell.querySelectorAll('[data-promo-admin-scope]');
    const selectAll = shell.querySelector('[data-promo-admin-select-all]');
    const tableBody = shell.querySelector('[data-promo-admin-table-body]');
    const emptyNode = shell.querySelector('[data-promo-admin-empty]');
    const totalEntries = shell.querySelector('[data-promo-admin-total]');
    const marketingEntries = shell.querySelector('[data-promo-admin-marketing]');
    const recentEntries = shell.querySelector('[data-promo-admin-recent]');
    const latestEntry = shell.querySelector('[data-promo-admin-latest]');
    const campaignName = shell.querySelector('[data-promo-admin-current-name]');
    const campaignWindow = shell.querySelector('[data-promo-admin-window]');
    const activeView = shell.querySelector('[data-promo-admin-view]');
    if (!entriesUrl || !exportUrl || !subscribersExportUrl || !deleteUrl || !status || !errorNode || !refreshButton || !exportLink || !subscribersExportLink || !deleteSelectedButton || !deleteViewButton || !selectAll || !tableBody) {
      return;
    }
    let currentScope = 'current';
    let activeRows = [];
    const selectedIds = new Set();
    const exportLinks = [exportLink, subscribersExportLink];
    const setStatus = (message) => {
      status.textContent = message || '';
      status.hidden = !message;
    };
    const setError = (message) => {
      errorNode.textContent = message || '';
      errorNode.hidden = !message;
    };
    const syncSelectionUi = () => {
      deleteSelectedButton.disabled = selectedIds.size === 0 || activeRows.length === 0;
      selectAll.checked = activeRows.length > 0 && activeRows.every((entry) => selectedIds.has(entry.id));
      selectAll.indeterminate = selectedIds.size > 0 && !selectAll.checked;
    };
    const resetSelection = () => {
      selectedIds.clear();
      syncSelectionUi();
    };
    const setScope = (scope) => {
      currentScope = scope === 'all' ? 'all' : 'current';
      scopeButtons.forEach((button) => {
        const pressed = button.dataset.promoAdminScope === currentScope;
        button.setAttribute('aria-pressed', pressed ? 'true' : 'false');
      });
      const nextExportUrl = new URL(exportUrl, window.location.origin);
      nextExportUrl.searchParams.set('scope', currentScope);
      exportLink.href = nextExportUrl.toString();
      const nextSubscribersExportUrl = new URL(subscribersExportUrl, window.location.origin);
      nextSubscribersExportUrl.searchParams.set('scope', currentScope);
      subscribersExportLink.href = nextSubscribersExportUrl.toString();
      deleteViewButton.textContent = currentScope === 'all'
        ? (copy.deleteViewAllLabel || copy.deleteViewLabel || deleteViewButton.textContent)
        : (copy.deleteViewLabel || deleteViewButton.textContent);
      resetSelection();
    };
    const renderEntries = (entries) => {
      tableBody.textContent = '';
      activeRows = Array.isArray(entries) ? entries : [];
      if (!activeRows.length) {
        emptyNode.hidden = false;
        resetSelection();
        return;
      }
      emptyNode.hidden = true;
      activeRows.forEach((entry) => {
        const row = document.createElement('tr');
        const selectCell = document.createElement('td');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = selectedIds.has(entry.id);
        checkbox.setAttribute('aria-label', entry.email || entry.name || String(entry.id));
        checkbox.addEventListener('change', () => {
          if (checkbox.checked) {
            selectedIds.add(entry.id);
          } else {
            selectedIds.delete(entry.id);
          }
          syncSelectionUi();
        });
        selectCell.appendChild(checkbox);
        row.appendChild(selectCell);
        row.appendChild(promoAdminTableCell(promoDateLabel(entry.created_at, lang) || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.campaign_id || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.name || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.email || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.phone || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.company || copy.none || '—'));
        row.appendChild(promoAdminTableCell(entry.discount_percent ? `${entry.discount_percent}%` : (copy.none || '—')));
        row.appendChild(promoAdminTableCell(entry.promo_code || copy.none || '—', 'promo-admin-code'));
        row.appendChild(promoAdminTableCell(promoDateLabel(entry.promo_expires_at, lang) || copy.none || '—'));
        row.appendChild(promoAdminTableCell(promoAdminMarketingLabel(entry, copy)));
        row.appendChild(promoAdminTableCell(promoAdminAttribution(entry, copy)));
        tableBody.appendChild(row);
      });
      syncSelectionUi();
    };
    const setBusy = (busy) => {
      refreshButton.disabled = busy;
      deleteViewButton.disabled = busy;
      deleteSelectedButton.disabled = busy || selectedIds.size === 0 || activeRows.length === 0;
      exportLinks.forEach((link) => {
        link.setAttribute('aria-disabled', busy ? 'true' : 'false');
        if (busy) {
          link.classList.add('is-disabled');
        } else {
          link.classList.remove('is-disabled');
        }
      });
      scopeButtons.forEach((button) => {
        button.disabled = busy;
      });
      selectAll.disabled = busy || activeRows.length === 0;
    };
    const deleteEntries = async (mode) => {
      if (mode === 'selected' && selectedIds.size === 0) {
        setError(copy.deleteNone || copy.deleteError || '');
        return;
      }
      const confirmed = window.confirm(mode === 'all' ? (copy.deleteViewConfirm || '') : (copy.deleteSelectedConfirm || ''));
      if (!confirmed) {
        return;
      }
      setError('');
      setStatus(copy.loading || '');
      setBusy(true);
      try {
        const response = await fetch(deleteUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({
            mode,
            scope: currentScope,
            ids: mode === 'selected' ? Array.from(selectedIds) : [],
          }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.deleteError || '');
        }
        resetSelection();
        await loadEntries(mode === 'all' ? (copy.deleteViewSuccess || '') : (copy.deleteSelectedSuccess || ''));
      } catch (error) {
        setError(error.message || copy.deleteError || '');
        setStatus('');
      } finally {
        setBusy(false);
      }
    };
    const loadEntries = async (successMessage = '') => {
      setError('');
      setStatus(successMessage || copy.loading || '');
      setBusy(true);
      try {
        const requestUrl = new URL(entriesUrl, window.location.origin);
        requestUrl.searchParams.set('scope', currentScope);
        requestUrl.searchParams.set('limit', shell.dataset.limit || '200');
        const response = await fetch(requestUrl.toString(), { headers: { Accept: 'application/json' } });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.loadError || '');
        }
        if (totalEntries) totalEntries.textContent = String(payload.summary.totalEntries || 0);
        if (marketingEntries) marketingEntries.textContent = String(payload.summary.marketingActive || 0);
        if (recentEntries) recentEntries.textContent = String(payload.summary.recentEntries || 0);
        if (latestEntry) latestEntry.textContent = payload.summary.latestEntryAt ? promoDateLabel(payload.summary.latestEntryAt, lang) : (copy.none || '—');
        if (campaignName) {
          campaignName.textContent = `${payload.campaign.currentName || ''} (${payload.campaign.currentId || ''})`.trim();
        }
        if (campaignWindow) {
          campaignWindow.textContent = `${promoDateLabel(payload.campaign.startsAt, lang)} - ${promoDateLabel(payload.campaign.endsAt, lang)}`;
        }
        if (activeView) {
          activeView.textContent = currentScope === 'all' ? (copy.scopeAll || '') : (copy.scopeCurrent || '');
        }
        renderEntries(payload.entries || []);
        if (!successMessage) {
          setStatus('');
        }
      } catch (error) {
        activeRows = [];
        emptyNode.hidden = true;
        tableBody.textContent = '';
        resetSelection();
        setError(error.message || copy.loadError || '');
        setStatus('');
      } finally {
        setBusy(false);
        syncSelectionUi();
      }
    };
    scopeButtons.forEach((button) => {
      button.addEventListener('click', () => {
        if (button.dataset.promoAdminScope === currentScope) return;
        setScope(button.dataset.promoAdminScope);
        loadEntries();
      });
    });
    selectAll.addEventListener('change', () => {
      if (selectAll.checked) {
        activeRows.forEach((entry) => selectedIds.add(entry.id));
      } else {
        activeRows.forEach((entry) => selectedIds.delete(entry.id));
      }
      renderEntries(activeRows);
    });
    refreshButton.addEventListener('click', loadEntries);
    deleteSelectedButton.addEventListener('click', () => deleteEntries('selected'));
    deleteViewButton.addEventListener('click', () => deleteEntries('all'));
    setScope(currentScope);
    loadEntries();
  });
}
function referralCurrency(value) {
  if (value == null || value === '') return '—';
  return `${value} CAD`;
}
function referralDate(value, lang) {
  return promoDateLabel(value, lang) || '—';
}
function referralDateTime(value, lang) {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return referralDate(value, lang);
  try {
    return new Intl.DateTimeFormat(lang === 'fr' ? 'fr-CA' : 'en-CA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  } catch {
    return referralDate(value, lang);
  }
}
function referralLabel(group, key, fallback = '—') {
  if (!group || !Object.prototype.hasOwnProperty.call(group, key)) return fallback;
  return group[key];
}
function initReferralApplyForms() {
  document.querySelectorAll('[data-referral-apply]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-referral-apply-copy]');
    const lang = shell.dataset.lang || 'en';
    const form = shell.querySelector('[data-referral-apply-form]');
    const status = shell.querySelector('[data-referral-apply-status]');
    const errorNode = shell.querySelector('[data-referral-apply-error]');
    const linkWrap = shell.querySelector('[data-referral-apply-link]');
    const linkAnchor = shell.querySelector('[data-referral-apply-link-anchor]');
    const url = shell.dataset.applyUrl;
    const portalUrl = shell.dataset.portalUrl || (lang === 'fr' ? '/fr/portail-references/' : '/en/referral-portal/');
    const companyRequired = shell.dataset.companyRequired === 'true';
    const requiresPassword = shell.dataset.requiresPassword === 'true';
    if (!form || !status || !errorNode || !linkWrap || !linkAnchor || !url) return;
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      status.hidden = true;
      errorNode.hidden = true;
      linkWrap.hidden = true;
      const email = String(form.elements.namedItem('email').value || '').trim();
      if (!email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
        errorNode.textContent = copy.invalidEmail || '';
        errorNode.hidden = false;
        return;
      }
      if (!String(form.elements.namedItem('name').value || '').trim()) {
        errorNode.textContent = copy.requiredField || '';
        errorNode.hidden = false;
        return;
      }
      if (companyRequired && !String(form.elements.namedItem('company').value || '').trim()) {
        errorNode.textContent = copy.requiredField || '';
        errorNode.hidden = false;
        return;
      }
      const passwordField = form.elements.namedItem('password');
      const confirmPasswordField = form.elements.namedItem('password_confirm');
      const password = passwordField ? String(passwordField.value || '') : '';
      const confirmPassword = confirmPasswordField ? String(confirmPasswordField.value || '') : '';
      if (requiresPassword) {
        if (password.length < 10) {
          errorNode.textContent = copy.invalidPassword || '';
          errorNode.hidden = false;
          return;
        }
        if (password !== confirmPassword) {
          errorNode.textContent = copy.passwordMismatch || '';
          errorNode.hidden = false;
          return;
        }
      }
      if (!form.elements.namedItem('rules_attestation').checked) {
        errorNode.textContent = copy.requiredConsent || '';
        errorNode.hidden = false;
        return;
      }
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({
            locale: lang,
            accountType: shell.dataset.accountType || 'client',
            name: String(form.elements.namedItem('name').value || '').trim(),
            email,
            phone: String(form.elements.namedItem('phone').value || '').trim(),
            company: String(form.elements.namedItem('company').value || '').trim(),
            website: form.elements.namedItem('website') ? String(form.elements.namedItem('website').value || '').trim() : '',
            notes: form.elements.namedItem('notes') ? String(form.elements.namedItem('notes').value || '').trim() : '',
            password: requiresPassword ? password : '',
            rulesAttestation: form.elements.namedItem('rules_attestation').checked,
          }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        status.textContent = payload.message || (payload.duplicate ? (copy.duplicate || payload.magicLink?.message || '') : (copy.success || payload.magicLink?.message || ''));
        status.hidden = false;
        if (!payload.duplicate && payload.portalUrl) {
          window.setTimeout(() => {
            window.location.assign(payload.portalUrl || portalUrl);
          }, 180);
          return;
        }
        if (payload.magicLink && payload.magicLink.previewLink) {
          linkAnchor.href = payload.magicLink.previewLink;
          linkWrap.hidden = false;
          window.setTimeout(() => {
            window.location.assign(payload.magicLink.previewLink);
          }, 180);
        }
      } catch (error) {
        errorNode.textContent = error.message || copy.genericError || '';
        errorNode.hidden = false;
      }
    });
  });
}
function initReferralPortal() {
  document.querySelectorAll('[data-referral-portal]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-referral-portal-copy]');
    const lang = shell.dataset.lang || 'en';
    const loginUrl = shell.dataset.loginUrl;
    const requestLinkUrl = shell.dataset.requestLinkUrl;
    const passwordUrl = shell.dataset.passwordUrl;
    const portalUrl = shell.dataset.portalUrl;
    const accessUrl = shell.dataset.accessUrl || portalUrl;
    const authBox = shell.querySelector('[data-referral-portal-auth]');
    const loginForm = shell.querySelector('[data-referral-portal-login]');
    const recoveryForm = shell.querySelector('[data-referral-portal-link-form]');
    const status = shell.querySelector('[data-referral-portal-status]');
    const errorNode = shell.querySelector('[data-referral-portal-error]');
    const dashboard = shell.querySelector('[data-referral-portal-dashboard]');
    const shareCopyButton = shell.querySelector('[data-referral-portal-share-copy]');
    const shareStatus = shell.querySelector('[data-referral-portal-share-status]');
    const creditMeta = shell.querySelector('[data-referral-credit-meta]');
    const creditPanel = shell.querySelector('[data-referral-credit-panel]');
    const passwordForm = shell.querySelector('[data-referral-password-form]');
    const passwordStatus = shell.querySelector('[data-referral-password-status]');
    const passwordError = shell.querySelector('[data-referral-password-error]');
    const passwordCurrentWrap = shell.querySelector('[data-referral-password-current-wrap]');
    const passwordSubmit = shell.querySelector('[data-referral-password-submit]');
    if (!loginUrl || !requestLinkUrl || !passwordUrl || !portalUrl || !authBox || !loginForm || !recoveryForm || !status || !errorNode || !dashboard || !creditMeta || !creditPanel || !passwordForm || !passwordStatus || !passwordError || !passwordCurrentWrap || !passwordSubmit) return;
    const labels = copy.labels || {};
    let activeAccount = null;
    const queryState = new URL(window.location.href);
    const authState = queryState.searchParams.get('auth') || '';
    const resetState = queryState.searchParams.get('reset') || '';
    const clearAuthState = () => {
      const current = new URL(window.location.href);
      if (!current.searchParams.has('auth')) return;
      current.searchParams.delete('auth');
      window.history.replaceState({}, '', current.toString());
    };
    const clearResetState = () => {
      const current = new URL(window.location.href);
      if (!current.searchParams.has('reset')) return;
      current.searchParams.delete('reset');
      window.history.replaceState({}, '', current.toString());
    };
    const authMessage = () => {
      if (authState === 'expired') return copy.authExpired || '';
      if (authState === 'used') return copy.authUsed || '';
      if (authState === 'invalid') return copy.authInvalid || '';
      return '';
    };
    const resetMessage = () => {
      if (resetState === 'ready') return copy.resetReady || '';
      return '';
    };
    const viewCopy = (accountType) => {
      const views = copy.views || {};
      return accountType === 'partner' ? (views.partner || {}) : (views.client || {});
    };
    const caseReference = (item) => {
      if (item.quoteReference) return item.quoteReference;
      if (item.referredCompany) return item.referredCompany;
      if (item.referredName) return item.referredName;
      return '—';
    };
    const setInlineMessage = (node, message) => {
      node.textContent = message || '';
      node.hidden = !message;
    };
    const renderTableRows = (target, rows, cells) => {
      target.textContent = '';
      if (!rows.length) {
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.colSpan = cells.length;
        cell.textContent = '—';
        row.appendChild(cell);
        target.appendChild(row);
        return;
      }
      rows.forEach((item) => {
        const row = document.createElement('tr');
        cells.forEach((cellBuilder) => {
          row.appendChild(promoAdminTableCell(cellBuilder(item)));
        });
        target.appendChild(row);
      });
    };
    const showAuth = (show) => {
      authBox.hidden = !show;
      dashboard.hidden = show;
    };
    const populateView = (payload) => {
      const accountType = payload.account.accountType === 'partner' ? 'partner' : 'client';
      const view = viewCopy(accountType);
      shell.classList.toggle('is-partner', accountType === 'partner');
      shell.classList.toggle('is-client', accountType !== 'partner');
      creditMeta.hidden = false;
      creditPanel.hidden = accountType === 'partner';
      shell.querySelector('[data-referral-portal-banner-eyebrow]').textContent = view.bannerEyebrow || '';
      shell.querySelector('[data-referral-portal-banner-title]').textContent = view.bannerTitle || '';
      shell.querySelector('[data-referral-portal-banner-copy]').textContent = view.bannerCopy || '';
      shell.querySelector('[data-referral-help-title]').textContent = view.helpTitle || '';
      const helpList = shell.querySelector('[data-referral-help-list]');
      helpList.textContent = '';
      (view.help || []).forEach((item) => {
        const li = document.createElement('li');
        li.textContent = item;
        helpList.appendChild(li);
      });
      const stats = view.stats || {};
      shell.querySelector('[data-referral-stat-label-total]').textContent = stats.total || '';
      shell.querySelector('[data-referral-stat-label-open]').textContent = stats.open || '';
      shell.querySelector('[data-referral-stat-label-completed]').textContent = stats.completed || '';
      shell.querySelector('[data-referral-stat-label-primary]').textContent = stats.primary || '';
      shell.querySelector('[data-referral-stat-label-secondary]').textContent = stats.secondary || '';
      shell.querySelector('[data-referral-stat-label-tertiary]').textContent = stats.tertiary || '';
      shell.querySelector('[data-referral-stat-total]').textContent = String(payload.stats.totalReferrals || 0);
      shell.querySelector('[data-referral-stat-open]').textContent = String(payload.stats.openReferrals || 0);
      shell.querySelector('[data-referral-stat-completed]').textContent = String(payload.stats.completedReferrals || 0);
      shell.querySelector('[data-referral-portal-referrals-title]').textContent = view.referralsTitle || '';
      shell.querySelector('[data-referral-portal-referrals-intro]').textContent = view.referralsIntro || '';
      shell.querySelector('[data-referral-portal-rewards-title]').textContent = view.rewardsTitle || '';
      shell.querySelector('[data-referral-portal-rewards-intro]').textContent = view.rewardsIntro || '';
      shell.querySelector('[data-referral-portal-amount-label]').textContent = view.amountLabel || '';
      shell.querySelector('[data-referral-portal-summary-note]').textContent = view.summaryNote || '';
      if (accountType === 'partner') {
        shell.querySelector('[data-referral-stat-primary]').textContent = referralCurrency(payload.stats.pendingPayoutCad);
        shell.querySelector('[data-referral-stat-secondary]').textContent = referralCurrency(payload.stats.settledPayoutCad);
        shell.querySelector('[data-referral-stat-tertiary]').textContent = referralCurrency(payload.stats.trackedSubtotalCad);
      } else {
        shell.querySelector('[data-referral-stat-primary]').textContent = referralCurrency(payload.account.walletBalanceCad);
        shell.querySelector('[data-referral-stat-secondary]').textContent = referralCurrency(payload.account.totalEarnedCad);
        shell.querySelector('[data-referral-stat-tertiary]').textContent = referralCurrency('1000.00');
      }
      shell.querySelector('[data-referral-password-title]').textContent = payload.account.hasPassword
        ? (copy.passwordPanel?.changeTitle || '')
        : (copy.passwordPanel?.createTitle || '');
      shell.querySelector('[data-referral-password-intro]').textContent = payload.account.hasPassword
        ? (copy.passwordPanel?.changeIntro || '')
        : (copy.passwordPanel?.createIntro || '');
      passwordSubmit.textContent = payload.account.hasPassword
        ? (copy.passwordPanel?.changeButton || '')
        : (copy.passwordPanel?.createButton || '');
      passwordCurrentWrap.hidden = !payload.account.hasPassword;
    };
    const loadPortal = async () => {
      try {
        status.hidden = true;
        errorNode.hidden = true;
        const response = await fetch(portalUrl, { headers: { Accept: 'application/json' } });
        if (response.status === 401) {
          showAuth(true);
          if (authMessage()) {
            status.hidden = true;
            errorNode.textContent = authMessage();
            errorNode.hidden = false;
          } else {
            status.textContent = copy.notSignedIn || '';
            status.hidden = false;
          }
          return;
        }
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        if (payload.account.passwordResetReady && accessUrl) {
          const target = new URL(accessUrl, window.location.origin);
          window.location.assign(target.toString());
          return;
        }
        activeAccount = payload.account;
        clearAuthState();
        clearResetState();
        showAuth(false);
        shell.querySelector('[data-referral-portal-name]').textContent = payload.account.name || payload.account.email || '—';
        const accountTypeLabel = referralLabel(labels.accountTypes, payload.account.accountType, payload.account.accountType || '—');
        const accountStatusLabel = referralLabel(labels.accountStatuses, payload.account.status, payload.account.status || '—');
        shell.querySelector('[data-referral-portal-meta]').textContent = `${accountTypeLabel} · ${accountStatusLabel} · ${payload.account.email}`;
        populateView(payload);
        shell.querySelector('[data-referral-portal-code]').textContent = payload.account.currentCode || '—';
        shell.querySelector('[data-referral-portal-credit-code]').textContent = payload.account.currentCreditCode || '—';
        shell.querySelector('[data-referral-portal-email]').textContent = payload.account.email || '—';
        const share = shell.querySelector('[data-referral-portal-share]');
        share.textContent = payload.account.shareLink || '—';
        share.href = payload.account.shareLink || shell.dataset.contactUrl || '#';
        share.dataset.shareLink = payload.account.shareLink || '';
        share.title = payload.account.shareLink || '';
        if (shareStatus) {
          shareStatus.textContent = '';
          shareStatus.hidden = true;
        }
        renderTableRows(shell.querySelector('[data-referral-portal-referrals]'), payload.referrals || [], [
          (item) => item.id,
          (item) => caseReference(item),
          (item) => referralLabel(labels.caseStatuses, item.status, item.status || '—'),
          (item) => referralDate(item.createdAt, lang),
          (item) => item.quotedSubtotalCad ? referralCurrency(item.quotedSubtotalCad) : '—',
          (item) => item.rewardAmountCad ? referralCurrency(item.rewardAmountCad) : '—',
        ]);
        renderTableRows(shell.querySelector('[data-referral-portal-rewards]'), payload.rewards || [], [
          (item) => item.id,
          (item) => referralLabel(copy.ledgerStatuses || labels.rewardStatuses, item.status, referralLabel(labels.rewardStatuses, item.status, item.status || '—')),
          (item) => referralCurrency(item.amountCad),
          (item) => referralDate(item.createdAt, lang),
          (item) => item.note || '—',
        ]);
        shell.querySelector('[data-referral-credit-panel-code]').textContent = payload.account.currentCreditCode || '—';
        shell.querySelector('[data-referral-credit-panel-balance]').textContent = referralCurrency(payload.account.walletBalanceCad);
        shell.querySelector('[data-referral-credit-panel-cap]').textContent = referralCurrency('1000.00');
        const creditInstruction = shell.querySelector('[data-referral-credit-panel-instruction]');
        if (creditInstruction) {
          creditInstruction.textContent = (copy.creditPanel && copy.creditPanel.manualCopy) || '';
        }
        setInlineMessage(passwordStatus, '');
        setInlineMessage(passwordError, '');
        passwordForm.reset();
      } catch (error) {
        showAuth(true);
        errorNode.textContent = error.message || copy.genericError || '';
        errorNode.hidden = false;
      }
    };
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      clearAuthState();
      clearResetState();
      setInlineMessage(status, '');
      setInlineMessage(errorNode, '');
      const email = String(loginForm.elements.namedItem('email').value || '').trim();
      const password = String(loginForm.elements.namedItem('password').value || '');
      if (!email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
        setInlineMessage(errorNode, copy.invalidEmail || '');
        return;
      }
      if (password.length < 10) {
        setInlineMessage(errorNode, copy.invalidPassword || '');
        return;
      }
      try {
        const response = await fetch(loginUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ email, password, locale: lang }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.invalidCredentials || copy.genericError || '');
        }
        window.location.assign(payload.portalUrl || window.location.pathname);
      } catch (error) {
        setInlineMessage(errorNode, error.message || copy.invalidCredentials || copy.genericError || '');
      }
    });
    recoveryForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      clearAuthState();
      clearResetState();
      setInlineMessage(status, '');
      setInlineMessage(errorNode, '');
      const email = String(recoveryForm.elements.namedItem('email').value || '').trim();
      if (!email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
        setInlineMessage(errorNode, copy.invalidEmail || '');
        return;
      }
      try {
        const response = await fetch(requestLinkUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ email, locale: lang, redirectPath: accessUrl }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        setInlineMessage(status, payload.message || copy.loginSent || '');
      } catch (error) {
        setInlineMessage(errorNode, error.message || copy.genericError || '');
      }
    });
    passwordForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      setInlineMessage(passwordStatus, '');
      setInlineMessage(passwordError, '');
      const currentPassword = String(passwordForm.elements.namedItem('current_password').value || '');
      const newPassword = String(passwordForm.elements.namedItem('new_password').value || '');
      const confirmPassword = String(passwordForm.elements.namedItem('confirm_password').value || '');
      if (newPassword.length < 10) {
        setInlineMessage(passwordError, copy.invalidPassword || '');
        return;
      }
      if (newPassword !== confirmPassword) {
        setInlineMessage(passwordError, copy.passwordMismatch || '');
        return;
      }
      try {
        const response = await fetch(passwordUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ locale: lang, currentPassword, newPassword }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        setInlineMessage(passwordStatus, payload.message || copy.passwordSaved || '');
        await loadPortal();
      } catch (error) {
        setInlineMessage(passwordError, error.message || copy.genericError || '');
      }
    });
    if (shareCopyButton) {
      shareCopyButton.addEventListener('click', async () => {
        const share = shell.querySelector('[data-referral-portal-share]');
        const value = share?.dataset.shareLink || '';
        if (!value) return;
        try {
          await navigator.clipboard.writeText(value);
          if (shareStatus) setInlineMessage(shareStatus, copy.shareCopied || '');
        } catch {
          if (shareStatus) setInlineMessage(shareStatus, copy.shareCopyError || '');
        }
      });
    }
    loadPortal();
  });
}
function initReferralAccess() {
  document.querySelectorAll('[data-referral-access]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-referral-access-copy]');
    const lang = shell.dataset.lang || 'en';
    const requestLinkUrl = shell.dataset.requestLinkUrl;
    const passwordUrl = shell.dataset.passwordUrl;
    const portalUrl = shell.dataset.portalUrl;
    const portalPageUrl = shell.dataset.portalPageUrl || (lang === 'fr' ? '/fr/portail-references/' : '/en/referral-portal/');
    const accessUrl = shell.dataset.accessUrl || portalPageUrl;
    const status = shell.querySelector('[data-referral-access-status]');
    const errorNode = shell.querySelector('[data-referral-access-error]');
    const readyWrap = shell.querySelector('[data-referral-access-ready]');
    const readyAccount = shell.querySelector('[data-referral-access-account]');
    const requestWrap = shell.querySelector('[data-referral-access-request]');
    const requestForm = shell.querySelector('[data-referral-access-request-form]');
    const passwordForm = shell.querySelector('[data-referral-access-password-form]');
    const passwordStatus = shell.querySelector('[data-referral-access-password-status]');
    const passwordError = shell.querySelector('[data-referral-access-password-error]');
    if (!requestLinkUrl || !passwordUrl || !portalUrl || !status || !errorNode || !readyWrap || !readyAccount || !requestWrap || !requestForm || !passwordForm || !passwordStatus || !passwordError) return;
    const query = new URL(window.location.href);
    const authState = query.searchParams.get('auth') || '';
    const setInlineMessage = (node, message) => {
      node.textContent = message || '';
      node.hidden = !message;
    };
    const authMessage = () => {
      if (authState === 'expired') return copy.authExpired || '';
      if (authState === 'used') return copy.authUsed || '';
      if (authState === 'invalid') return copy.authInvalid || '';
      return '';
    };
    const showReset = (payload) => {
      requestWrap.hidden = true;
      readyWrap.hidden = false;
      const accountType = payload.account.accountType === 'partner'
        ? (lang === 'fr' ? 'Programme de partenaires référents' : 'Referral Partner Program')
        : (lang === 'fr' ? 'Programme de référence' : 'Referral Program');
      readyAccount.textContent = `${payload.account.name || payload.account.email || '—'} · ${accountType} · ${payload.account.email || '—'}`;
    };
    const showRequest = (message = '', isError = false) => {
      readyWrap.hidden = true;
      requestWrap.hidden = false;
      setInlineMessage(status, isError ? '' : message);
      setInlineMessage(errorNode, isError ? message : '');
    };
    const loadAccessState = async () => {
      setInlineMessage(status, '');
      setInlineMessage(errorNode, '');
      try {
        const response = await fetch(portalUrl, { headers: { Accept: 'application/json' } });
        if (response.status === 401) {
          showRequest(authMessage() || copy.notReady || '', Boolean(authMessage()));
          return;
        }
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        if (!payload.account.passwordResetReady) {
          window.location.assign(portalPageUrl);
          return;
        }
        showReset(payload);
      } catch (error) {
        showRequest(error.message || copy.genericError || '', true);
      }
    };
    requestForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      setInlineMessage(status, '');
      setInlineMessage(errorNode, '');
      const email = String(requestForm.elements.namedItem('email').value || '').trim();
      if (!email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {
        setInlineMessage(errorNode, copy.invalidEmail || '');
        return;
      }
      try {
        const response = await fetch(requestLinkUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ email, locale: lang, redirectPath: accessUrl }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        setInlineMessage(status, payload.message || copy.requestSent || '');
      } catch (error) {
        setInlineMessage(errorNode, error.message || copy.genericError || '');
      }
    });
    passwordForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      setInlineMessage(passwordStatus, '');
      setInlineMessage(passwordError, '');
      const newPassword = String(passwordForm.elements.namedItem('new_password').value || '');
      const confirmPassword = String(passwordForm.elements.namedItem('confirm_password').value || '');
      if (newPassword.length < 10) {
        setInlineMessage(passwordError, copy.invalidPassword || '');
        return;
      }
      if (newPassword !== confirmPassword) {
        setInlineMessage(passwordError, copy.passwordMismatch || '');
        return;
      }
      try {
        const response = await fetch(passwordUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ locale: lang, newPassword }),
        });
        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || copy.genericError || '');
        }
        setInlineMessage(passwordStatus, payload.message || copy.passwordSaved || '');
        window.setTimeout(() => {
          window.location.assign(portalPageUrl);
        }, 250);
      } catch (error) {
        setInlineMessage(passwordError, error.message || copy.genericError || '');
      }
    });
    loadAccessState();
  });
}
function initReferralAdmin() {
  document.querySelectorAll('[data-referral-admin]').forEach((shell) => {
    const copy = promoPayloadCopy(shell, '[data-referral-admin-copy]');
    const lang = shell.dataset.lang || 'en';
    const status = shell.querySelector('[data-referral-admin-status]');
    const errorNode = shell.querySelector('[data-referral-admin-error]');
    const refreshButton = shell.querySelector('[data-referral-admin-refresh]');
    const applicationsBody = shell.querySelector('[data-referral-admin-applications]');
    const accountsBody = shell.querySelector('[data-referral-admin-accounts]');
    const casesBody = shell.querySelector('[data-referral-admin-cases]');
    const rewardsBody = shell.querySelector('[data-referral-admin-rewards]');
    const createForm = shell.querySelector('[data-referral-admin-create-form]');
    const applicationStatusFilter = shell.querySelector('[data-referral-filter-applications-status]');
    const applicationSearchFilter = shell.querySelector('[data-referral-filter-applications-search]');
    const accountProgramFilter = shell.querySelector('[data-referral-filter-accounts-program]');
    const accountStatusFilter = shell.querySelector('[data-referral-filter-accounts-status]');
    const accountSearchFilter = shell.querySelector('[data-referral-filter-accounts-search]');
    const caseProgramFilter = shell.querySelector('[data-referral-filter-cases-program]');
    const caseStatusFilter = shell.querySelector('[data-referral-filter-cases-status]');
    const caseSearchFilter = shell.querySelector('[data-referral-filter-cases-search]');
    const rewardTypeFilter = shell.querySelector('[data-referral-filter-rewards-type]');
    const rewardStatusFilter = shell.querySelector('[data-referral-filter-rewards-status]');
    const rewardSearchFilter = shell.querySelector('[data-referral-filter-rewards-search]');
    const detailEmpty = shell.querySelector('[data-referral-admin-detail-empty]');
    const detailWrap = shell.querySelector('[data-referral-admin-detail]');
    const detailName = shell.querySelector('[data-referral-admin-detail-name]');
    const detailMeta = shell.querySelector('[data-referral-admin-detail-meta]');
    const detailProgram = shell.querySelector('[data-referral-admin-detail-program]');
    const detailStatus = shell.querySelector('[data-referral-admin-detail-status]');
    const detailEmail = shell.querySelector('[data-referral-admin-detail-email]');
    const detailPhone = shell.querySelector('[data-referral-admin-detail-phone]');
    const detailCompany = shell.querySelector('[data-referral-admin-detail-company]');
    const detailWebsite = shell.querySelector('[data-referral-admin-detail-website]');
    const detailShareCode = shell.querySelector('[data-referral-admin-detail-share-code]');
    const detailCreditCode = shell.querySelector('[data-referral-admin-detail-credit-code]');
    const detailBalance = shell.querySelector('[data-referral-admin-detail-balance]');
    const detailEarned = shell.querySelector('[data-referral-admin-detail-earned]');
    const detailCreated = shell.querySelector('[data-referral-admin-detail-created]');
    const detailLogin = shell.querySelector('[data-referral-admin-detail-login]');
    const detailNotes = shell.querySelector('[data-referral-admin-detail-notes]');
    const detailCasesBody = shell.querySelector('[data-referral-admin-detail-cases]');
    const detailRewardsBody = shell.querySelector('[data-referral-admin-detail-rewards]');
    const detailAuditBody = shell.querySelector('[data-referral-admin-detail-audit]');
    const detailExportButton = shell.querySelector('[data-referral-admin-detail-export]');
    const detailResetButton = shell.querySelector('[data-referral-admin-detail-reset]');
    const detailDeleteButton = shell.querySelector('[data-referral-admin-detail-delete]');
    const detailCaseForm = shell.querySelector('[data-referral-admin-case-form]');
    const detailCaseSubmit = shell.querySelector('[data-referral-admin-case-submit]');
    const detailCaseCancel = shell.querySelector('[data-referral-admin-case-cancel]');
    const detailCaseState = shell.querySelector('[data-referral-admin-case-state]');
    if (!status || !errorNode || !refreshButton || !applicationsBody || !accountsBody || !casesBody || !rewardsBody || !createForm) return;
    const labels = copy.labels || {};
    let selectedAccountId = null;
    let selectedAccount = null;
    let selectedCaseId = null;
    const setStatus = (message) => {
      status.textContent = message || '';
      status.hidden = !message;
    };
    const setError = (message) => {
      errorNode.textContent = message || '';
      errorNode.hidden = !message;
    };
    const clearMessages = () => {
      setStatus('');
      setError('');
    };
    const adminBaseUrl = (() => {
      const current = new URL(window.location.href);
      current.username = '';
      current.password = '';
      current.hash = '';
      current.search = '';
      return current.toString();
    })();
    const resolveAdminUrl = (value) => {
      try {
        return new URL(value, adminBaseUrl).toString();
      } catch {
        return value;
      }
    };
    const programLabel = (accountType) => referralLabel(labels.programTypes || labels.accountTypes, accountType, referralLabel(labels.accountTypes, accountType, accountType || '—'));
    const accountLabel = (item) => `${item.name || '—'} (${item.email || '—'})`;
    const searchBlob = (...values) => values.filter(Boolean).join(' ').toLowerCase();
    const setDetailEmptyState = (message) => {
      selectedAccount = null;
      selectedCaseId = null;
      if (detailEmpty) {
        detailEmpty.textContent = message || copy.messages?.detailEmpty || '';
        detailEmpty.hidden = false;
      }
      if (detailWrap) detailWrap.hidden = true;
    };
    const parseMetadata = (value) => {
      if (!value) return {};
      try {
        return JSON.parse(value);
      } catch {
        return {};
      }
    };
    const auditNote = (entry) => {
      const metadata = parseMetadata(entry.metadata_json);
      const subtotalLabel = lang === 'fr' ? 'Sous-total' : 'Subtotal';
      const rewardLabel = lang === 'fr' ? 'Récompense' : 'Reward';
      const parts = [];
      if (typeof metadata.previousBalanceCents === 'number' && typeof metadata.nextBalanceCents === 'number') {
        parts.push(`${referralCurrency((metadata.previousBalanceCents / 100).toFixed(2))} → ${referralCurrency((metadata.nextBalanceCents / 100).toFixed(2))}`);
      }
      if (typeof metadata.previousAmountCents === 'number' && typeof metadata.nextAmountCents === 'number') {
        parts.push(`${referralCurrency((metadata.previousAmountCents / 100).toFixed(2))} → ${referralCurrency((metadata.nextAmountCents / 100).toFixed(2))}`);
      }
      if (metadata.referredName) parts.push(metadata.referredName);
      if (metadata.referredCompany) parts.push(metadata.referredCompany);
      if (metadata.quoteReference) parts.push(metadata.quoteReference);
      if (metadata.referralCode) parts.push(metadata.referralCode);
      if (metadata.email) parts.push(metadata.email);
      if (metadata.referredEmail) parts.push(metadata.referredEmail);
      if (typeof metadata.deltaCents === 'number') parts.push(referralCurrency((metadata.deltaCents / 100).toFixed(2)));
      if (typeof metadata.previousSubtotalCents === 'number' && typeof metadata.nextSubtotalCents === 'number') {
        parts.push(`${subtotalLabel}: ${referralCurrency((metadata.previousSubtotalCents / 100).toFixed(2))} → ${referralCurrency((metadata.nextSubtotalCents / 100).toFixed(2))}`);
      } else if (typeof metadata.quotedSubtotalCents === 'number') {
        parts.push(`${subtotalLabel}: ${referralCurrency((metadata.quotedSubtotalCents / 100).toFixed(2))}`);
      } else if (typeof metadata.nextSubtotalCents === 'number') {
        parts.push(`${subtotalLabel}: ${referralCurrency((metadata.nextSubtotalCents / 100).toFixed(2))}`);
      }
      if (typeof metadata.previousRewardAmountCents === 'number' && typeof metadata.nextRewardAmountCents === 'number') {
        parts.push(`${rewardLabel}: ${referralCurrency((metadata.previousRewardAmountCents / 100).toFixed(2))} → ${referralCurrency((metadata.nextRewardAmountCents / 100).toFixed(2))}`);
      } else if (typeof metadata.previousRewardAmountCents === 'number') {
        parts.push(`${rewardLabel}: ${referralCurrency((metadata.previousRewardAmountCents / 100).toFixed(2))}`);
      } else if (typeof metadata.nextRewardAmountCents === 'number') {
        parts.push(`${rewardLabel}: ${referralCurrency((metadata.nextRewardAmountCents / 100).toFixed(2))}`);
      }
      if (typeof metadata.manualRewardAmountCents === 'number') parts.push(`${rewardLabel}: ${referralCurrency((metadata.manualRewardAmountCents / 100).toFixed(2))}`);
      if (metadata.previousStatus || metadata.nextStatus) {
        parts.push(`${referralLabel(labels.caseStatuses, metadata.previousStatus, metadata.previousStatus || '—')} → ${referralLabel(labels.caseStatuses, metadata.nextStatus, metadata.nextStatus || '—')}`);
      } else if (metadata.status) {
        parts.push(referralLabel(labels.caseStatuses, metadata.status, metadata.status));
      }
      if (metadata.note) parts.push(metadata.note);
      if (parts.length) return parts.join(' · ');
      return '—';
    };
    const requestJson = async (url, init = {}) => {
      const response = await fetch(resolveAdminUrl(url), {
        headers: { Accept: 'application/json', ...(init.headers || {}) },
        ...init,
      });
      const payload = await response.json();
      if (!response.ok || !payload.ok) {
        throw new Error(payload.error || copy.genericError || '');
      }
      return payload;
    };
    const applyAccountStatus = async (accountId, statusValue) => {
      return requestJson(shell.dataset.accountStatusUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ accountId, status: statusValue }),
      });
    };
    const adjustAccountBalance = async (accountId, deltaCad, note) => {
      return requestJson(shell.dataset.accountBalanceAdjustUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ accountId, deltaCad, note }),
      });
    };
    const createManualCase = async (payload) => {
      return requestJson(shell.dataset.caseCreateUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload),
      });
    };
    const updateManualCase = async (payload) => {
      return requestJson(shell.dataset.caseUpdateUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload),
      });
    };
    const applyCaseStatus = async (caseId, statusValue, subtotal, quoteReference) => {
      return requestJson(shell.dataset.caseStatusUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ caseId, status: statusValue, quotedSubtotalCad: subtotal, quoteReference }),
      });
    };
    const adjustCaseReward = async (caseId, amountCad, note, clearOverride = false) => {
      return requestJson(shell.dataset.caseRewardAdjustUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ caseId, amountCad, note, clearOverride }),
      });
    };
    const settleReward = async (rewardId) => {
      return requestJson(shell.dataset.rewardSettleUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ rewardId }),
      });
    };
    const changeApplicationStatus = async (applicationId, nextStatus) => {
      return requestJson(shell.dataset.applicationStatusUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ applicationId, status: nextStatus }),
      });
    };
    const deleteApplication = async (applicationId) => {
      return requestJson(shell.dataset.applicationDeleteUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ applicationId }),
      });
    };
    const createAccount = async (payload) => {
      return requestJson(shell.dataset.accountCreateUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(payload),
      });
    };
    const resetAccountAccess = async (accountId) => {
      return requestJson(shell.dataset.accountResetAccessUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ accountId, sendSetupLink: true }),
      });
    };
    const deleteAccount = async (accountId) => {
      return requestJson(shell.dataset.accountDeleteUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ accountId }),
      });
    };
    const deleteCase = async (caseId) => {
      return requestJson(shell.dataset.caseDeleteUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ caseId }),
      });
    };
    const downloadAccount = (accountId) => {
      const url = new URL(resolveAdminUrl(shell.dataset.accountExportUrl));
      url.searchParams.set('accountId', String(accountId));
      window.location.assign(url.toString());
    };
    const fetchAccountDetail = async (accountId) => {
      const url = new URL(resolveAdminUrl(shell.dataset.accountDetailUrl || shell.dataset.accountExportUrl));
      url.searchParams.set('accountId', String(accountId));
      const response = await fetch(url.toString(), { headers: { Accept: 'application/json' } });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || copy.genericError || '');
      }
      return payload;
    };
    const actionStack = () => {
      const wrap = document.createElement('div');
      wrap.className = 'referral-admin-action-stack';
      return wrap;
    };
    const makeButton = (label, className = 'button button-secondary') => {
      const button = document.createElement('button');
      button.className = className;
      button.type = 'button';
      button.textContent = label;
      return button;
    };
    const resetCaseForm = () => {
      selectedCaseId = null;
      if (!detailCaseForm) return;
      detailCaseForm.reset();
      const statusField = detailCaseForm.elements.namedItem('status');
      if (statusField) statusField.value = 'new';
      const referralCodeField = detailCaseForm.elements.namedItem('referral_code');
      if (referralCodeField) referralCodeField.value = selectedAccount?.current_code || '';
      if (detailCaseSubmit) detailCaseSubmit.textContent = copy.actions.saveCase || 'Add project';
      if (detailCaseCancel) detailCaseCancel.hidden = true;
      if (detailCaseState) detailCaseState.textContent = '';
    };
    const beginCaseEdit = (item) => {
      if (!detailCaseForm) return;
      selectedCaseId = Number(item.id);
      const normalizedStatus = item.status === 'won' ? 'accepted' : (item.status || 'new');
      detailCaseForm.elements.namedItem('referral_code').value = item.referral_code || selectedAccount?.current_code || '';
      detailCaseForm.elements.namedItem('referred_name').value = item.referred_name || '';
      detailCaseForm.elements.namedItem('referred_email').value = item.referred_email || '';
      detailCaseForm.elements.namedItem('referred_phone').value = item.referred_phone || '';
      detailCaseForm.elements.namedItem('referred_company').value = item.referred_company || '';
      detailCaseForm.elements.namedItem('quote_reference').value = item.quote_reference || '';
      detailCaseForm.elements.namedItem('status').value = normalizedStatus;
      detailCaseForm.elements.namedItem('quoted_subtotal').value = item.quoted_subtotal_cents == null ? '' : (Number(item.quoted_subtotal_cents || 0) / 100).toFixed(2);
      detailCaseForm.elements.namedItem('manual_reward').value = item.manual_reward_amount_cents == null ? '' : (Number(item.manual_reward_amount_cents || 0) / 100).toFixed(2);
      detailCaseForm.elements.namedItem('note').value = item.referred_project_notes || item.manual_reward_note || '';
      if (detailCaseSubmit) detailCaseSubmit.textContent = copy.actions.updateCase || 'Update project';
      if (detailCaseCancel) detailCaseCancel.hidden = false;
      if (detailCaseState) detailCaseState.textContent = `${copy.labels?.caseIdLabel || 'Project ID'}: ${item.id}`;
      detailCaseForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
    const applyRowFilters = () => {
      Array.from(applicationsBody.querySelectorAll('tr')).forEach((row) => {
        const statusValue = row.dataset.status || '';
        const searchValue = row.dataset.search || '';
        const statusMatch = !applicationStatusFilter || applicationStatusFilter.value === 'all' || statusValue === applicationStatusFilter.value;
        const searchMatch = !applicationSearchFilter || !applicationSearchFilter.value.trim() || searchValue.includes(applicationSearchFilter.value.trim().toLowerCase());
        row.hidden = !(statusMatch && searchMatch);
      });
      Array.from(accountsBody.querySelectorAll('tr')).forEach((row) => {
        const programValue = row.dataset.program || '';
        const statusValue = row.dataset.status || '';
        const searchValue = row.dataset.search || '';
        const programMatch = !accountProgramFilter || accountProgramFilter.value === 'all' || programValue === accountProgramFilter.value;
        const statusMatch = !accountStatusFilter || accountStatusFilter.value === 'all' || statusValue === accountStatusFilter.value;
        const searchMatch = !accountSearchFilter || !accountSearchFilter.value.trim() || searchValue.includes(accountSearchFilter.value.trim().toLowerCase());
        row.hidden = !(programMatch && statusMatch && searchMatch);
      });
      Array.from(casesBody.querySelectorAll('tr')).forEach((row) => {
        const programValue = row.dataset.program || '';
        const statusValue = row.dataset.status || '';
        const searchValue = row.dataset.search || '';
        const programMatch = !caseProgramFilter || caseProgramFilter.value === 'all' || programValue === caseProgramFilter.value;
        const statusMatch = !caseStatusFilter || caseStatusFilter.value === 'all' || statusValue === caseStatusFilter.value;
        const searchMatch = !caseSearchFilter || !caseSearchFilter.value.trim() || searchValue.includes(caseSearchFilter.value.trim().toLowerCase());
        row.hidden = !(programMatch && statusMatch && searchMatch);
      });
      Array.from(rewardsBody.querySelectorAll('tr')).forEach((row) => {
        const typeValue = row.dataset.type || '';
        const statusValue = row.dataset.status || '';
        const searchValue = row.dataset.search || '';
        const typeMatch = !rewardTypeFilter || rewardTypeFilter.value === 'all' || typeValue === rewardTypeFilter.value;
        const statusMatch = !rewardStatusFilter || rewardStatusFilter.value === 'all' || statusValue === rewardStatusFilter.value;
        const searchMatch = !rewardSearchFilter || !rewardSearchFilter.value.trim() || searchValue.includes(rewardSearchFilter.value.trim().toLowerCase());
        row.hidden = !(typeMatch && statusMatch && searchMatch);
      });
    };
    const renderAccountDetail = (payload) => {
      const account = payload.account || {};
      const rollup = payload.rollup || {};
      const rewardRows = payload.rewards || [];
      const auditRows = payload.auditEvents || [];
      const isPartner = account.account_type === 'partner';
      const pendingPayoutCents = rewardRows
        .filter((item) => item.reward_type === 'payout' && item.status === 'earned')
        .reduce((sum, item) => sum + Number(item.amount_cents || 0), 0);
      const totalPayoutCents = rewardRows
        .filter((item) => item.reward_type === 'payout' && (item.status === 'earned' || item.status === 'settled'))
        .reduce((sum, item) => sum + Number(item.amount_cents || 0), 0);
      selectedAccountId = account.id || null;
      selectedAccount = account;
      resetCaseForm();
      if (detailEmpty) detailEmpty.hidden = true;
      if (detailWrap) detailWrap.hidden = false;
      if (detailName) detailName.textContent = account.name || account.email || '—';
      if (detailMeta) detailMeta.textContent = `${programLabel(account.account_type)} · ${referralLabel(labels.accountStatuses, account.status, account.status || '—')} · ${account.email || '—'}`;
      if (detailProgram) detailProgram.textContent = programLabel(account.account_type);
      if (detailStatus) detailStatus.textContent = referralLabel(labels.accountStatuses, account.status, account.status || '—');
      if (detailEmail) detailEmail.textContent = account.email || '—';
      if (detailPhone) detailPhone.textContent = account.phone || '—';
      if (detailCompany) detailCompany.textContent = account.company || '—';
      if (detailWebsite) detailWebsite.textContent = account.website || '—';
      if (detailShareCode) detailShareCode.textContent = account.current_code || '—';
      if (detailCreditCode) detailCreditCode.textContent = account.current_credit_code || '—';
      if (detailBalance) detailBalance.textContent = referralCurrency((Number(rollup.currentOutstandingCents || 0) / 100).toFixed(2));
      if (detailEarned) detailEarned.textContent = isPartner
        ? referralCurrency((Number(rollup.totalEarnedCents || totalPayoutCents) / 100).toFixed(2))
        : referralCurrency((Number(rollup.totalEarnedCents || 0) / 100).toFixed(2));
      if (detailCreated) detailCreated.textContent = referralDate(account.created_at, lang);
      if (detailLogin) detailLogin.textContent = referralDate(account.last_login_at, lang);
      if (detailNotes) detailNotes.textContent = account.notes || '—';
      if (detailCasesBody) {
        detailCasesBody.textContent = '';
        const rows = payload.referralCases || [];
        if (!rows.length) {
          const row = document.createElement('tr');
          const cell = document.createElement('td');
          cell.colSpan = 6;
          cell.textContent = '—';
          row.appendChild(cell);
          detailCasesBody.appendChild(row);
        } else {
          rows.slice(0, 50).forEach((item) => {
            const row = document.createElement('tr');
            row.appendChild(promoAdminTableCell(item.id));
            row.appendChild(promoAdminTableCell(referralLabel(labels.caseStatuses, item.status, item.status || '—')));
            row.appendChild(promoAdminTableCell([
              item.quote_reference || '—',
              item.referred_name || '—',
              item.referred_company || '—',
            ].join(' · ')));
            row.appendChild(promoAdminTableCell(item.quoted_subtotal_cents == null ? '—' : referralCurrency((Number(item.quoted_subtotal_cents || 0) / 100).toFixed(2))));
            row.appendChild(promoAdminTableCell(item.reward_amount_cents == null ? '—' : referralCurrency((Number(item.reward_amount_cents || 0) / 100).toFixed(2))));
            const actionCell = document.createElement('td');
            const stack = actionStack();
            const editButton = makeButton(copy.actions.editCase || 'Edit project');
            editButton.addEventListener('click', () => beginCaseEdit(item));
            stack.appendChild(editButton);
            const adjustButton = makeButton(copy.actions.adjustReward || 'Adjust amount');
            adjustButton.addEventListener('click', async () => {
              const currentValue = item.reward_amount_cents == null ? '' : (Number(item.reward_amount_cents || 0) / 100).toFixed(2);
              const amountRaw = window.prompt(copy.messages?.caseRewardPrompt || copy.genericError || '', currentValue);
              if (amountRaw == null) return;
              const normalized = String(amountRaw).trim().replace(',', '.');
              const note = window.prompt(copy.messages?.caseRewardNotePrompt || '', '') || '';
              try {
                if (!normalized) {
                  await adjustCaseReward(item.id, '', note, true);
                } else {
                  const amount = Number.parseFloat(normalized);
                  if (!Number.isFinite(amount) || amount < 0) {
                    setError(copy.messages?.caseRewardPrompt || copy.genericError || '');
                    return;
                  }
                  await adjustCaseReward(item.id, amount.toFixed(2), note, false);
                }
                setStatus(copy.messages?.caseRewardAdjusted || '');
                await loadAll();
              } catch (error) {
                setError(error.message || copy.genericError || '');
              }
            });
            stack.appendChild(adjustButton);
            const deleteButton = makeButton(copy.actions.delete || 'Delete');
            deleteButton.addEventListener('click', async () => {
              if (!window.confirm(copy.messages?.confirmDeleteCase || 'Delete this project?')) return;
              try {
                await deleteCase(item.id);
                setStatus(copy.messages?.caseDeleted || '');
                await loadAll();
              } catch (error) {
                setError(error.message || copy.genericError || '');
              }
            });
            stack.appendChild(deleteButton);
            actionCell.appendChild(stack);
            row.appendChild(actionCell);
            detailCasesBody.appendChild(row);
          });
        }
      }
      if (detailRewardsBody) {
        detailRewardsBody.textContent = '';
        const rewardLedger = [
          ...rewardRows.map((item) => ({
            id: item.id,
            status: referralLabel(labels.rewardStatuses, item.status, item.status || '—'),
            amount: referralCurrency((Number(item.amount_cents || 0) / 100).toFixed(2)),
            created: referralDateTime(item.created_at, lang),
            note: item.note || '—',
          })),
          ...auditRows
            .filter((item) => item.event_type === 'client_wallet_adjusted')
            .map((item) => {
              const metadata = parseMetadata(item.metadata_json);
              return {
                id: `audit-${item.id}`,
                status: lang === 'fr' ? 'Solde ajusté' : 'Balance adjusted',
                amount: referralCurrency(((Number(metadata.deltaCents || 0)) / 100).toFixed(2)),
                created: referralDateTime(item.created_at, lang),
                note: metadata.note || '—',
              };
            }),
        ];
        if (!rewardLedger.length) {
          const row = document.createElement('tr');
          const cell = document.createElement('td');
          cell.colSpan = 5;
          cell.textContent = '—';
          row.appendChild(cell);
          detailRewardsBody.appendChild(row);
        } else {
          rewardLedger.slice(0, 50).forEach((item) => {
            const row = document.createElement('tr');
            row.appendChild(promoAdminTableCell(item.id));
            row.appendChild(promoAdminTableCell(item.status));
            row.appendChild(promoAdminTableCell(item.amount));
            row.appendChild(promoAdminTableCell(item.created));
            row.appendChild(promoAdminTableCell(item.note));
            detailRewardsBody.appendChild(row);
          });
        }
      }
      if (detailAuditBody) {
        detailAuditBody.textContent = '';
        if (!auditRows.length) {
          const row = document.createElement('tr');
          const cell = document.createElement('td');
          cell.colSpan = 3;
          cell.textContent = '—';
          row.appendChild(cell);
          detailAuditBody.appendChild(row);
        } else {
          auditRows.slice(0, 50).forEach((item) => {
            const row = document.createElement('tr');
            row.appendChild(promoAdminTableCell(referralDateTime(item.created_at, lang)));
            row.appendChild(promoAdminTableCell(item.event_type || '—'));
            row.appendChild(promoAdminTableCell(auditNote(item)));
            detailAuditBody.appendChild(row);
          });
        }
      }
    };
    const openAccountDetail = async (accountId) => {
      try {
        setError('');
        setStatus(copy.messages?.detailLoading || copy.loading || 'Loading…');
        const payload = await fetchAccountDetail(accountId);
        renderAccountDetail(payload);
        setStatus('');
        return payload;
      } catch (error) {
        setError(error.message || copy.genericError || '');
        setStatus('');
        return null;
      }
    };
    const loadAll = async () => {
      setError('');
      setStatus(copy.loading || 'Loading…');
      try {
        const [summaryResponse, applicationsResponse, accountsResponse, casesResponse, rewardsResponse] = await Promise.all([
          fetch(resolveAdminUrl(shell.dataset.summaryUrl), { headers: { Accept: 'application/json' } }),
          fetch(resolveAdminUrl(shell.dataset.applicationsUrl), { headers: { Accept: 'application/json' } }),
          fetch(resolveAdminUrl(shell.dataset.accountsUrl), { headers: { Accept: 'application/json' } }),
          fetch(resolveAdminUrl(shell.dataset.casesUrl), { headers: { Accept: 'application/json' } }),
          fetch(resolveAdminUrl(shell.dataset.rewardsUrl), { headers: { Accept: 'application/json' } }),
        ]);
        const [summaryPayload, applicationsPayload, accountsPayload, casesPayload, rewardsPayload] = await Promise.all([
          summaryResponse.json(),
          applicationsResponse.json(),
          accountsResponse.json(),
          casesResponse.json(),
          rewardsResponse.json(),
        ]);
        if (!summaryResponse.ok || !applicationsResponse.ok || !accountsResponse.ok || !casesResponse.ok || !rewardsResponse.ok) {
          throw new Error(summaryPayload.error || applicationsPayload.error || accountsPayload.error || casesPayload.error || rewardsPayload.error || copy.genericError || '');
        }
        shell.querySelector('[data-referral-summary-active]').textContent = String(summaryPayload.summary.activeAccounts || 0);
        shell.querySelector('[data-referral-summary-pending]').textContent = String(summaryPayload.summary.pendingPartners || 0);
        shell.querySelector('[data-referral-summary-open]').textContent = String(summaryPayload.summary.openCases || 0);
        shell.querySelector('[data-referral-summary-payouts]').textContent = referralCurrency(summaryPayload.summary.pendingPayoutCad);
        applicationsBody.textContent = '';
        (applicationsPayload.applications || []).forEach((item) => {
          const row = document.createElement('tr');
          row.dataset.status = item.status || '';
          row.dataset.search = searchBlob(item.name, item.email, item.company);
          row.appendChild(promoAdminTableCell(item.id));
          row.appendChild(promoAdminTableCell(referralLabel(labels.applicationStatuses, item.status, item.status || '—')));
          row.appendChild(promoAdminTableCell(item.name || '—'));
          row.appendChild(promoAdminTableCell(item.email || '—'));
          row.appendChild(promoAdminTableCell(item.company || '—'));
          row.appendChild(promoAdminTableCell(referralDate(item.created_at, lang)));
          const actionCell = document.createElement('td');
          const stack = actionStack();
          const createButton = makeButton(copy.actions.createAccount || 'Create account');
          createButton.addEventListener('click', async () => {
            try {
              const payload = await createAccount({ applicationId: item.id, status: 'active', sendSetupLink: true });
              setStatus(payload.message || copy.messages?.accountCreated || '');
              await loadAll();
              if (payload?.account?.id) {
                await openAccountDetail(payload.account.id);
              }
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(createButton);
          const rejectButton = makeButton(copy.actions.reject || 'Reject');
          rejectButton.addEventListener('click', async () => {
            try {
              await changeApplicationStatus(item.id, 'rejected');
              setStatus(copy.messages?.applicationUpdated || '');
              loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(rejectButton);
          const voidButton = makeButton(copy.actions.delete || 'Delete');
          voidButton.addEventListener('click', async () => {
            if (!window.confirm(copy.messages?.confirmDeleteApplication || 'Delete this partner application?')) return;
            try {
              await deleteApplication(item.id);
              setStatus(copy.messages?.applicationDeleted || '');
              loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(voidButton);
          actionCell.appendChild(stack);
          row.appendChild(actionCell);
          applicationsBody.appendChild(row);
        });
        accountsBody.textContent = '';
        (accountsPayload.accounts || []).forEach((item) => {
          const row = document.createElement('tr');
          row.dataset.program = item.account_type || '';
          row.dataset.status = item.status || '';
          row.dataset.search = searchBlob(item.name, item.email, item.company, item.current_code, item.current_credit_code);
          row.appendChild(promoAdminTableCell(item.id));
          row.appendChild(promoAdminTableCell(programLabel(item.account_type)));
          const statusCell = document.createElement('td');
          const select = document.createElement('select');
          ['pending', 'active', 'paused', 'rejected'].forEach((value) => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = referralLabel(labels.accountStatuses, value, value);
            option.selected = value === item.status;
            select.appendChild(option);
          });
          statusCell.appendChild(select);
          row.appendChild(statusCell);
          const nameCell = document.createElement('td');
          const nameButton = makeButton(item.name || '—', 'button button-link referral-admin-view-button');
          nameButton.addEventListener('click', async () => {
            await openAccountDetail(item.id);
          });
          nameCell.appendChild(nameButton);
          row.appendChild(nameCell);
          row.appendChild(promoAdminTableCell(item.email || '—'));
          const codeCell = document.createElement('td');
          const codeWrap = document.createElement('div');
          codeWrap.className = 'referral-admin-code-stack';
          const shareCode = document.createElement('p');
          shareCode.className = 'promo-admin-code';
          shareCode.textContent = item.current_code || '—';
          codeWrap.appendChild(shareCode);
          if (item.current_credit_code) {
            const creditCode = document.createElement('p');
            creditCode.className = 'promo-admin-code';
            creditCode.textContent = item.current_credit_code;
            codeWrap.appendChild(creditCode);
          }
          codeCell.appendChild(codeWrap);
          row.appendChild(codeCell);
          row.appendChild(promoAdminTableCell(
            referralCurrency((Number(item.current_outstanding_cents || 0) / 100).toFixed(2))
          ));
          const actionCell = document.createElement('td');
          const stack = actionStack();
          const applyButton = makeButton(copy.actions.apply || 'Apply');
          applyButton.addEventListener('click', async () => {
            try {
              await applyAccountStatus(item.id, select.value);
              setStatus(copy.messages?.accountUpdated || '');
              loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(applyButton);
          if (item.account_type === 'client') {
            const adjustButton = makeButton(copy.actions.adjustCredit || 'Adjust credit');
            adjustButton.addEventListener('click', async () => {
              const amountLabel = copy.messages?.creditAdjustPrompt || copy.genericError || '';
              const amountRaw = window.prompt(amountLabel, '');
              if (amountRaw == null) return;
              const normalized = String(amountRaw).trim().replace(',', '.');
              if (!normalized) return;
              const amount = Number.parseFloat(normalized);
              if (!Number.isFinite(amount) || amount === 0) {
                setError(copy.messages?.creditAdjustPrompt || copy.genericError || '');
                return;
              }
              const note = window.prompt(copy.messages?.creditAdjustNotePrompt || '', '') || '';
              try {
                await adjustAccountBalance(item.id, amount.toFixed(2), note);
                setStatus(copy.messages?.creditAdjusted || '');
                loadAll();
              } catch (error) {
                setError(error.message || copy.genericError || '');
              }
            });
            stack.appendChild(adjustButton);
          }
          const exportButton = makeButton(copy.actions.exportOne || 'Download');
          exportButton.addEventListener('click', () => downloadAccount(item.id));
          stack.appendChild(exportButton);
          const detailButton = makeButton(copy.actions.viewDetails || 'View details');
          detailButton.addEventListener('click', async () => {
            await openAccountDetail(item.id);
          });
          stack.appendChild(detailButton);
          const resetButton = makeButton(copy.actions.resetAccess || 'Reset access');
          resetButton.disabled = item.status !== 'active';
          resetButton.addEventListener('click', async () => {
            try {
              const payload = await resetAccountAccess(item.id);
              setStatus(payload.message || copy.messages?.accessReset || '');
              loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(resetButton);
          const deleteButton = makeButton(copy.actions.delete || 'Delete');
          deleteButton.addEventListener('click', async () => {
            if (!window.confirm(copy.messages?.confirmDeleteAccount || 'Delete this account and all related referral data?')) return;
            try {
              await deleteAccount(item.id);
              setStatus(copy.messages?.accountDeleted || '');
              loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(deleteButton);
          actionCell.appendChild(stack);
          row.appendChild(actionCell);
          accountsBody.appendChild(row);
        });
        casesBody.textContent = '';
        (casesPayload.cases || []).forEach((item) => {
          const normalizedCaseStatus = item.status === 'won' ? 'accepted' : (item.status || '');
          const row = document.createElement('tr');
          row.dataset.program = item.account_type || '';
          row.dataset.status = normalizedCaseStatus;
          row.dataset.search = searchBlob(item.account_name, item.account_email, item.referral_code, item.quote_reference, item.referred_name, item.referred_email, item.referred_company);
          row.appendChild(promoAdminTableCell(item.id));
          row.appendChild(promoAdminTableCell(`${item.account_name || '—'} (${item.account_email || '—'})`));
          row.appendChild(promoAdminTableCell(item.referral_code || '—', 'promo-admin-code'));
          const statusCell = document.createElement('td');
          const statusSelect = document.createElement('select');
          ['new', 'quoted', 'accepted', 'completed_paid', 'member_paid', 'void'].forEach((value) => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = referralLabel(labels.caseStatuses, value, value);
            option.selected = value === normalizedCaseStatus;
            statusSelect.appendChild(option);
          });
          statusCell.appendChild(statusSelect);
          row.appendChild(statusCell);
          const subtotalCell = document.createElement('td');
          const subtotalInput = document.createElement('input');
          subtotalInput.type = 'number';
          subtotalInput.step = '0.01';
          subtotalInput.value = item.quoted_subtotal_cents == null ? '' : (Number(item.quoted_subtotal_cents || 0) / 100).toFixed(2);
          subtotalCell.appendChild(subtotalInput);
          row.appendChild(subtotalCell);
          const refCell = document.createElement('td');
          const refInput = document.createElement('input');
          refInput.value = item.quote_reference || '';
          refCell.appendChild(refInput);
          const refMeta = document.createElement('div');
          refMeta.className = 'form-note';
          refMeta.textContent = [item.referred_name || '—', item.referred_company || '—'].join(' · ');
          refCell.appendChild(refMeta);
          row.appendChild(refCell);
          row.appendChild(promoAdminTableCell(item.reward_amount_cents == null ? '—' : referralCurrency((Number(item.reward_amount_cents || 0) / 100).toFixed(2))));
          const actionCell = document.createElement('td');
          const stack = actionStack();
          const editButton = makeButton(copy.actions.editCase || 'Edit project');
          editButton.addEventListener('click', async () => {
            const payload = await openAccountDetail(item.account_id);
            const match = (payload?.referralCases || []).find((entry) => Number(entry.id) === Number(item.id));
            if (match) beginCaseEdit(match);
          });
          stack.appendChild(editButton);
          const button = document.createElement('button');
          button.className = 'button button-secondary';
          button.type = 'button';
          button.textContent = copy.actions.apply || 'Apply';
          button.addEventListener('click', async () => {
            try {
              await applyCaseStatus(item.id, statusSelect.value, subtotalInput.value, refInput.value);
              await loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(button);
          const adjustRewardButton = makeButton(copy.actions.adjustReward || 'Adjust amount');
          adjustRewardButton.addEventListener('click', async () => {
            const currentValue = item.reward_amount_cents == null ? '' : (Number(item.reward_amount_cents || 0) / 100).toFixed(2);
            const amountRaw = window.prompt(copy.messages?.caseRewardPrompt || copy.genericError || '', currentValue);
            if (amountRaw == null) return;
            const normalized = String(amountRaw).trim().replace(',', '.');
            const note = window.prompt(copy.messages?.caseRewardNotePrompt || '', '') || '';
            try {
              if (!normalized) {
                await adjustCaseReward(item.id, '', note, true);
              } else {
                const amount = Number.parseFloat(normalized);
                if (!Number.isFinite(amount) || amount < 0) {
                  setError(copy.messages?.caseRewardPrompt || copy.genericError || '');
                  return;
                }
                await adjustCaseReward(item.id, amount.toFixed(2), note, false);
              }
              setStatus(copy.messages?.caseRewardAdjusted || '');
              await loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(adjustRewardButton);
          const deleteButton = makeButton(copy.actions.delete || 'Delete');
          deleteButton.addEventListener('click', async () => {
            if (!window.confirm(copy.messages?.confirmDeleteCase || 'Delete this referral case?')) return;
            try {
              await deleteCase(item.id);
              setStatus(copy.messages?.caseDeleted || '');
              await loadAll();
            } catch (error) {
              setError(error.message || copy.genericError || '');
            }
          });
          stack.appendChild(deleteButton);
          actionCell.appendChild(stack);
          row.appendChild(actionCell);
          casesBody.appendChild(row);
        });
        rewardsBody.textContent = '';
        (rewardsPayload.rewards || []).forEach((item) => {
          const row = document.createElement('tr');
          row.dataset.type = item.reward_type || '';
          row.dataset.status = item.status || '';
          row.dataset.search = searchBlob(item.account_name, item.account_email, item.note, item.reward_type);
          row.appendChild(promoAdminTableCell(item.id));
          row.appendChild(promoAdminTableCell(`${item.account_name || '—'} (${item.account_email || '—'})`));
          row.appendChild(promoAdminTableCell(referralLabel(labels.rewardTypes, item.reward_type, item.reward_type || '—')));
          row.appendChild(promoAdminTableCell(referralLabel(labels.rewardStatuses, item.status, item.status || '—')));
          row.appendChild(promoAdminTableCell(referralCurrency((Number(item.amount_cents || 0) / 100).toFixed(2))));
          row.appendChild(promoAdminTableCell(item.note || '—'));
          const actionCell = document.createElement('td');
          if (item.reward_type === 'payout' && item.status === 'earned') {
            const button = document.createElement('button');
            button.className = 'button button-secondary';
            button.type = 'button';
            button.textContent = copy.actions.settle || 'Settle';
            button.addEventListener('click', async () => {
              try {
                await settleReward(item.id);
                loadAll();
              } catch (error) {
                setError(error.message || copy.genericError || '');
              }
            });
            actionCell.appendChild(button);
          } else {
            actionCell.textContent = '—';
          }
          row.appendChild(actionCell);
          rewardsBody.appendChild(row);
        });
        applyRowFilters();
        if (selectedAccountId) {
          await openAccountDetail(selectedAccountId);
        } else {
          setDetailEmptyState(copy.messages?.detailEmpty || '');
        }
        setStatus('');
      } catch (error) {
        setError(error.message || copy.genericError || '');
        setStatus('');
      }
    };
    [
      applicationStatusFilter,
      applicationSearchFilter,
      accountProgramFilter,
      accountStatusFilter,
      accountSearchFilter,
      caseProgramFilter,
      caseStatusFilter,
      caseSearchFilter,
      rewardTypeFilter,
      rewardStatusFilter,
      rewardSearchFilter,
    ].filter(Boolean).forEach((control) => {
      control.addEventListener('input', applyRowFilters);
      control.addEventListener('change', applyRowFilters);
    });
    refreshButton.addEventListener('click', loadAll);
    if (detailExportButton) {
      detailExportButton.addEventListener('click', () => {
        if (!selectedAccountId) return;
        downloadAccount(selectedAccountId);
      });
    }
    if (detailResetButton) {
      detailResetButton.addEventListener('click', async () => {
        if (!selectedAccountId) return;
        try {
          const payload = await resetAccountAccess(selectedAccountId);
          setStatus(payload.message || copy.messages?.accessReset || '');
          await loadAll();
        } catch (error) {
          setError(error.message || copy.genericError || '');
        }
      });
    }
    if (detailDeleteButton) {
      detailDeleteButton.addEventListener('click', async () => {
        if (!selectedAccountId) return;
        if (!window.confirm(copy.messages?.confirmDeleteAccount || 'Delete this account and all related referral data?')) return;
        try {
          await deleteAccount(selectedAccountId);
          selectedAccountId = null;
          setStatus(copy.messages?.accountDeleted || '');
          setDetailEmptyState(copy.messages?.detailEmpty || '');
          await loadAll();
        } catch (error) {
          setError(error.message || copy.genericError || '');
        }
      });
    }
    if (detailCaseForm) {
      detailCaseForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (!selectedAccountId || !selectedAccount) {
          setError(copy.messages?.detailEmpty || copy.genericError || '');
          return;
        }
        const referralCode = String(detailCaseForm.elements.namedItem('referral_code').value || '').trim().toUpperCase();
        const referredName = String(detailCaseForm.elements.namedItem('referred_name').value || '').trim();
        const referredEmail = String(detailCaseForm.elements.namedItem('referred_email').value || '').trim();
        const referredPhone = String(detailCaseForm.elements.namedItem('referred_phone').value || '').trim();
        const referredCompany = String(detailCaseForm.elements.namedItem('referred_company').value || '').trim();
        const quoteReference = String(detailCaseForm.elements.namedItem('quote_reference').value || '').trim();
        const statusValue = String(detailCaseForm.elements.namedItem('status').value || 'new');
        const subtotal = String(detailCaseForm.elements.namedItem('quoted_subtotal').value || '').trim();
        const manualReward = String(detailCaseForm.elements.namedItem('manual_reward').value || '').trim();
        const note = String(detailCaseForm.elements.namedItem('note').value || '').trim();
        if (!referralCode || !referredName || !referredEmail || !referredCompany) {
          setError(copy.messages?.caseCreateRequired || copy.genericError || '');
          return;
        }
        if (statusValue === 'completed_paid' && !subtotal) {
          setError(copy.messages?.caseCreateSubtotalRequired || copy.genericError || '');
          return;
        }
        try {
          let successMessage = '';
          if (selectedCaseId) {
            const payload = await updateManualCase({
              caseId: selectedCaseId,
              accountId: selectedAccountId,
              locale: selectedAccount.locale || lang,
              referralCode,
              referredName,
              referredEmail,
              referredPhone,
              referredCompany,
              quoteReference,
              status: statusValue,
              quotedSubtotalCad: subtotal,
              manualRewardCad: manualReward,
              note,
            });
            successMessage = `${copy.messages?.caseUpdated || ''} #${payload?.referralCase?.id || selectedCaseId} ${quoteReference || referredName || ''}`.trim();
          } else {
            const payload = await createManualCase({
              accountId: selectedAccountId,
              locale: selectedAccount.locale || lang,
              referralCode,
              referredName,
              referredEmail,
              referredPhone,
              referredCompany,
              quoteReference,
              status: statusValue,
              quotedSubtotalCad: subtotal,
              manualRewardCad: manualReward,
              note,
            });
            successMessage = `${copy.messages?.caseCreated || ''} #${payload?.referralCase?.id || ''} ${quoteReference || referredName || ''}`.trim();
          }
          resetCaseForm();
          await loadAll();
          setStatus(successMessage);
        } catch (error) {
          setError(error.message || copy.genericError || '');
        }
      });
    }
    if (detailCaseCancel) {
      detailCaseCancel.addEventListener('click', () => {
        clearMessages();
        resetCaseForm();
      });
    }
    createForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      setError('');
      const accountType = String(createForm.elements.namedItem('account_type').value || 'client');
      const locale = String(createForm.elements.namedItem('locale').value || 'fr');
      const name = String(createForm.elements.namedItem('name').value || '').trim();
      const email = String(createForm.elements.namedItem('email').value || '').trim();
      const phone = String(createForm.elements.namedItem('phone').value || '').trim();
      const company = String(createForm.elements.namedItem('company').value || '').trim();
      const website = String(createForm.elements.namedItem('website').value || '').trim();
      const notes = String(createForm.elements.namedItem('notes').value || '').trim();
      const statusValue = String(createForm.elements.namedItem('status').value || 'active');
      const sendSetupLink = Boolean(createForm.elements.namedItem('send_setup_link').checked);
      if (!name || !email) {
        setError(copy.messages?.createAccountRequired || copy.genericError || '');
        return;
      }
      if (accountType === 'partner' && !company) {
        setError(copy.messages?.createPartnerCompanyRequired || copy.genericError || '');
        return;
      }
      try {
        const payload = await createAccount({
          accountType,
          locale,
          status: statusValue,
          name,
          email,
          phone,
          company,
          website,
          notes,
          sendSetupLink,
        });
        createForm.reset();
        createForm.elements.namedItem('account_type').value = 'client';
        createForm.elements.namedItem('locale').value = locale;
        createForm.elements.namedItem('status').value = 'active';
        createForm.elements.namedItem('send_setup_link').checked = true;
        setStatus(payload.message || copy.messages?.accountCreated || '');
        loadAll();
      } catch (error) {
        setError(error.message || copy.genericError || '');
      }
    });
    setDetailEmptyState(copy.messages?.detailEmpty || '');
    loadAll();
  });
}
async function initSiteConfig() {
  try {
    const response = await fetch('/api/site-config', { headers: { Accept: 'application/json' } });
    const config = await response.json();
    if (!config || !config.analyticsToken || document.querySelector('script[data-cf-beacon-script]')) {
      return;
    }
    const script = document.createElement('script');
    script.defer = true;
    script.src = 'https://static.cloudflareinsights.com/beacon.min.js';
    script.dataset.cfBeaconScript = 'true';
    script.setAttribute('data-cf-beacon', JSON.stringify({ token: config.analyticsToken }));
    document.head.appendChild(script);
  } catch (error) {}
}
initPromoForms();
initPromoUnsubscribe();
initPromoAdmin();
initReferralApplyForms();
initReferralPortal();
initReferralAccess();
initReferralAdmin();
initSiteConfig();
'''

css += '''
.hero-panel,.page-hero-panel,.cta-band{background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(245,250,246,.96)),radial-gradient(circle at top right,rgba(47,138,88,.12),transparent 32%)}.hero-panel h2,.page-hero-panel h2,.contact-panel h2{margin:0;font-family:"Segoe UI Variable Display","Aptos Display","Segoe UI",sans-serif;font-size:clamp(1.7rem,2.6vw,2.6rem);line-height:1.08}.chip-list{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}.chip{display:inline-flex;align-items:center;padding:10px 14px;border:1px solid rgba(47,138,88,.16);border-radius:999px;background:var(--primary-soft);color:var(--primary-dark);font-size:.78rem;font-weight:700}.section-heading{display:grid;gap:12px;margin-bottom:24px}.grid-3,.grid-4,.timeline,.faq-list,.detail-list,.input-grid,.checkbox-group,.footer-grid,.language-cards{display:grid;gap:18px}.grid-3{grid-template-columns:repeat(3,minmax(0,1fr))}.grid-4{grid-template-columns:repeat(4,minmax(0,1fr))}.card{padding:22px;border-radius:24px;background:rgba(247,250,247,.92)}.card h3{margin:0 0 10px;font-size:1.16rem}.card p{margin:0;color:var(--muted);line-height:1.68}.card .more{display:inline-block;margin-top:14px;color:var(--primary-dark);font-weight:700}.breadcrumb{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px;color:var(--muted);font-size:.96rem}.breadcrumb span[aria-current="page"]{color:var(--text)}.timeline{grid-template-columns:repeat(4,minmax(0,1fr))}.timeline-step{padding:24px;border-radius:24px}.timeline-step span{display:inline-block;margin-bottom:18px;color:var(--primary-dark);font-size:.78rem;font-weight:800}.timeline-step h3{margin:0 0 10px;font-size:1.16rem}.timeline-step p{margin:0;color:var(--muted);line-height:1.68}.faq-list{grid-template-columns:repeat(2,minmax(0,1fr))}.faq-item{border-radius:24px;overflow:hidden}.faq-item summary{padding:22px 24px;cursor:pointer;font-weight:700;list-style:none}.faq-item summary::-webkit-details-marker{display:none}.faq-item summary::after{content:"+";float:right;color:var(--primary-dark);font-size:1.3rem;line-height:1}.faq-item[open] summary::after{content:"-"}.faq-item p{margin:0;padding:0 24px 24px;color:var(--muted);line-height:1.68}.contact-panel .note{padding:16px 18px;border-radius:18px;background:var(--primary-soft);color:var(--primary-dark);line-height:1.6}.detail-item{padding:18px;border:1px solid var(--line);border-radius:20px;background:var(--surface-soft)}.detail-item strong{display:block;margin-bottom:8px}form{display:grid;gap:18px}.input-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.field{display:grid;gap:10px;font-weight:700}.field input,.field select,.field textarea{width:100%;padding:14px 16px;border:1px solid var(--line-strong);border-radius:16px;background:#fff;color:var(--text)}.field textarea{min-height:160px;resize:vertical}.checkbox-group{grid-template-columns:repeat(2,minmax(0,1fr));margin:0;padding:18px;border:1px solid var(--line);border-radius:20px;background:var(--surface-soft)}.checkbox-group legend{padding:0 8px;font-weight:700}.checkbox-group label{display:flex;align-items:center;gap:10px;font-weight:600}.checkbox-group input{width:18px;height:18px;accent-color:var(--primary)}.form-note{margin:0;color:var(--muted);line-height:1.6}.zoho-form-shell{display:grid;gap:0;align-content:stretch;padding-top:0;padding-bottom:0}.zoho-form-shell .footer-note{margin:0}.zoho-form-embed{width:100%}.zoho-form-embed iframe{display:block;width:100%;min-height:1120px;border:0;border-radius:20px;background:#fff}.site-footer{margin-top:44px;padding-top:26px;border-top:1px solid var(--line-strong)}.footer-grid{grid-template-columns:1.2fr .8fr 1fr;align-items:start}.footer-title{margin:0 0 14px;font-size:.92rem;letter-spacing:.16em;text-transform:uppercase;color:var(--primary-dark)}.footer-links,.footer-services{display:grid;gap:10px}.footer-bottom{margin-top:24px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted)}.language-card{padding:24px;border:1px solid var(--line);border-radius:24px;background:rgba(247,250,247,.92)}.language-card h2{margin:0 0 10px;font-size:1.28rem}.language-card p{margin:0 0 18px;color:var(--muted);line-height:1.62}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible{outline:3px solid rgba(47,138,88,.28);outline-offset:2px}@media (max-width:1100px){.hero,.page-hero,.cta-band,.contact-layout,.gateway-panel,.two-col,.footer-grid{grid-template-columns:1fr}.grid-4{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:920px){.site-header{position:static}.header-inner{display:grid;justify-items:start;border-radius:30px}.nav-toggle{display:inline-flex}.site-nav{display:none;width:100%;flex-direction:column;align-items:flex-start;padding-top:10px}.site-nav.is-open{display:flex}.header-actions{width:100%;flex-wrap:wrap}.grid-3,.timeline,.input-grid,.checkbox-group{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:740px){.site-shell,.gateway-shell{width:min(calc(100% - 24px),var(--max))}.hero-copy,.hero-panel,.page-hero-copy,.page-hero-panel,.contact-panel,.form-panel,.cta-band,.gateway-panel{padding:24px}.hero-copy h1{font-size:clamp(2rem,11vw,3rem)}.page-hero-copy h1,.section-heading h2,.cta-band h2,.gateway-panel h1{font-size:clamp(1.85rem,8vw,2.6rem)}.grid-3,.grid-4,.faq-list,.timeline,.input-grid,.checkbox-group{grid-template-columns:1fr}.contact-layout{padding:24px}.zoho-form-shell{padding-top:0;padding-bottom:0}}@media (prefers-reduced-motion: reduce){html{scroll-behavior:auto}*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
'''

css += '''
:root{
  --max:1440px;
  --muted:#4a5b52;
  --section-surface:rgba(255,255,255,.76);
  --section-line:rgba(185,203,191,.78);
}
body{
  font-family:"Aptos","Segoe UI","Helvetica Neue",Arial,sans-serif;
  line-height:1.58;
  -webkit-font-smoothing:antialiased;
  text-rendering:optimizeLegibility;
}
h1,h2,h3,p,li{
  hyphens:none;
  overflow-wrap:normal;
  word-break:normal;
}
main{
  display:grid;
  gap:26px;
}
main section{
  position:relative;
  padding:30px;
  border:1px solid var(--section-line);
  border-radius:34px;
  background:linear-gradient(180deg,var(--section-surface),rgba(247,250,247,.58));
  box-shadow:0 16px 40px rgba(20,35,27,.06);
  overflow:hidden;
}
main section::before{
  content:"";
  position:absolute;
  left:28px;
  right:28px;
  top:0;
  height:1px;
  background:linear-gradient(90deg,transparent,rgba(47,138,88,.34) 18%,rgba(47,138,88,.1) 50%,transparent 82%);
}
main section+section{
  margin-top:0;
}
.site-shell,.gateway-shell{
  width:min(calc(100% - 32px),var(--max));
}
.site-shell{
  padding:24px 0 60px;
}
.header-inner{
  gap:22px;
}
.site-nav{
  gap:18px;
}
.brand img{
  width:clamp(118px,8vw,152px);
  transform:translate(8px,-6px);
}
.footer-brand img{
  width:clamp(164px,11vw,218px);
  transform:translateY(-1px);
}
.gateway-brand img{
  width:min(280px,100%);
  transform:translateY(-2px);
}
.hero,.page-hero{
  grid-template-columns:minmax(0,1.48fr) minmax(280px,.68fr);
}
.hero{
  align-items:stretch;
}
.page-hero{
  align-items:stretch;
}
.hero.hero-media-layout{
  grid-template-columns:minmax(0,1.24fr) minmax(360px,.94fr);
}
.contact-layout{
  grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr);
  align-items:stretch;
  padding:32px;
  border:1px solid var(--line);
  border-radius:var(--radius);
  background:var(--surface);
  box-shadow:var(--shadow);
}
.contact-hero{
  grid-template-columns:minmax(0,1fr);
  align-items:start;
}
.contact-layout>.contact-panel,
.contact-layout>.form-panel{
  padding:0;
  border:0;
  background:transparent;
  box-shadow:none;
  min-height:100%;
}
.contact-sidebar{
  display:grid;
  grid-template-rows:auto auto 1fr;
  align-content:start;
  gap:18px;
}
.contact-sidebar h2,
.contact-sidebar>p{
  margin:0;
}
.contact-sidebar .detail-list{
  grid-auto-rows:1fr;
  height:100%;
  align-content:stretch;
}
.contact-sidebar .detail-item{
  display:flex;
  flex-direction:column;
  justify-content:center;
  min-height:100%;
}
.hero-copy,.hero-panel,.page-hero-copy,.page-hero-panel,.contact-panel,.form-panel,.cta-band,.gateway-panel{
  padding:38px;
}
.page-hero-copy{
  display:flex;
  flex-direction:column;
  justify-content:flex-start;
  min-height:100%;
}
.page-hero-panel{
  display:flex;
  flex-direction:column;
  justify-content:flex-start;
  min-height:100%;
}
.hero-copy h1{
  max-width:none;
  font-size:clamp(1.58rem,1.95vw,2.3rem);
  line-height:1.12;
}
.page-hero-copy h1{
  max-width:none;
  font-size:clamp(1.56rem,1.72vw,2.1rem);
  line-height:1.16;
}
.section-heading h2,.cta-band h2,.gateway-panel h1{
  max-width:none;
  font-size:clamp(1.46rem,1.6vw,1.98rem);
  line-height:1.18;
}
.hero-panel h2,.page-hero-panel h2{
  max-width:none;
  font-size:clamp(1.08rem,1.18vw,1.36rem);
  line-height:1.28;
}
.service-chip-links .chip{
  transition:transform .16s ease,background-color .16s ease,border-color .16s ease,color .16s ease;
}
.service-chip-links .chip:hover,
.service-chip-links .chip:focus-visible{
  transform:translateY(-1px);
  background:#d6eadf;
  border-color:rgba(31,102,64,.22);
  color:var(--primary-dark);
}
.hero-media-panel{
  display:grid;
  align-content:start;
  gap:16px;
  padding:24px;
}
.hero-media-panel h2{
  font-size:clamp(1rem,1.1vw,1.24rem);
  line-height:1.28;
}
.hero-media-stack{
  display:grid;
  gap:16px;
}
.hero-media-main{
  display:grid;
  gap:12px;
  margin:0;
  padding:12px;
  border:1px solid rgba(47,138,88,.14);
  border-radius:26px;
  background:rgba(255,255,255,.86);
}
.hero-media-frame{
  overflow:hidden;
  border-radius:18px;
  background:linear-gradient(180deg,#eff5f0,#e3ece5);
}
.hero-media-main-image{
  width:100%;
  height:auto;
  aspect-ratio:1800/1026;
  object-fit:cover;
}
.hero-media-caption{
  display:grid;
  gap:4px;
}
.hero-media-caption strong{
  font-family:"Aptos Display","Segoe UI Variable Display","Segoe UI",sans-serif;
  font-weight:700;
}
.hero-media-caption strong{
  font-size:.95rem;
  line-height:1.3;
}
.hero-media-caption span{
  color:var(--muted);
  font-size:.84rem;
  line-height:1.55;
}
.service-panel-visual{
  margin:22px 0 0;
}
.service-panel-frame{
  overflow:hidden;
  border-radius:20px;
  background:linear-gradient(180deg,#eff5f0,#e3ece5);
}
.service-panel-frame .image-lightbox-trigger{
  display:block;
}
.service-panel-image{
  width:100%;
  height:auto;
  max-height:320px;
  object-fit:contain;
}
.about-panel-visual{
  margin:22px 0 0;
}
.about-panel-frame{
  overflow:hidden;
  border-radius:20px;
  background:linear-gradient(180deg,#eff5f0,#e3ece5);
}
.about-panel-frame .image-lightbox-trigger{
  display:block;
}
.about-panel-image{
  width:100%;
  height:auto;
  max-height:280px;
  object-fit:cover;
}
.service-panel-image-wifi{
  max-height:292px;
}
.service-carousel{
  display:grid;
  gap:20px;
}
.service-carousel-header{
  display:flex;
  align-items:flex-end;
  justify-content:space-between;
  gap:20px;
}
.service-carousel-controls{
  display:flex;
  gap:10px;
  flex-shrink:0;
}
.service-carousel-button{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  width:48px;
  height:48px;
  border:1px solid var(--line-strong);
  border-radius:999px;
  background:#fff;
  color:var(--primary-dark);
  font-size:1.05rem;
  font-weight:700;
  transition:transform .16s ease,background-color .16s ease,border-color .16s ease,color .16s ease,opacity .16s ease;
}
.service-carousel-button:hover,
.service-carousel-button:focus-visible{
  transform:translateY(-1px);
  background:var(--primary-soft);
  border-color:rgba(31,102,64,.22);
}
.service-carousel-button[disabled]{
  opacity:.45;
  cursor:default;
  transform:none;
}
.service-carousel-track{
  display:grid;
  grid-auto-flow:column;
  grid-auto-columns:calc((100% - 40px) / 3);
  gap:20px;
  overflow-x:auto;
  overscroll-behavior-x:contain;
  scroll-snap-type:x mandatory;
  scrollbar-width:none;
  padding-bottom:4px;
}
.service-carousel-track::-webkit-scrollbar{
  display:none;
}
.service-carousel-card{
  scroll-snap-align:start;
  height:100%;
}
.service-carousel-card.card{
  height:100%;
}
.hero-copy h1,.page-hero-copy h1,.section-heading h2,.cta-band h2,.gateway-panel h1,.hero-panel h2,.page-hero-panel h2{
  font-family:"Aptos Display","Segoe UI Variable Display","Segoe UI",sans-serif;
  font-weight:700;
  letter-spacing:-.022em;
  text-wrap:balance;
}
.hero-copy>p:not(.eyebrow),.page-hero-copy>p:not(.eyebrow),.section-heading p,.contact-panel p,.gateway-panel p,.footer-note,.card p,.timeline-step p,.faq-item p,.detail-item p,.form-note{
  max-width:68ch;
  line-height:1.78;
  font-size:1.02rem;
  text-wrap:pretty;
}
.section-heading{
  gap:12px;
  margin-bottom:22px;
  max-width:none;
}
.section-heading p{
  max-width:68ch;
}
.hero-actions,.page-hero-actions{
  margin-top:22px;
}
.chip-list{
  gap:8px;
  margin-top:20px;
}
.hero-points{
  grid-template-columns:repeat(2,minmax(240px,1fr));
  gap:14px 24px;
  margin-top:52px;
}
.hero-points a{
  display:inline-block;
  color:inherit;
  transition:color .16s ease,transform .16s ease;
}
.hero-points a:hover,
.hero-points a:focus-visible{
  color:var(--primary-dark);
  transform:translateX(2px);
  text-decoration:underline;
  text-underline-offset:4px;
}
.feature-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
  gap:20px;
}
.feature-card,
.service-card{
  position:relative;
  overflow:hidden;
}
.feature-card::before,
.service-card::before{
  content:"";
  position:absolute;
  inset:0;
  background:
    radial-gradient(circle at top right,rgba(47,138,88,.15),transparent 38%),
    linear-gradient(180deg,rgba(255,255,255,.72),rgba(244,249,245,.96));
  pointer-events:none;
}
.feature-card>*,
.service-card>*{
  position:relative;
}
.feature-card{
  min-height:100%;
  gap:14px;
}
.feature-card-header,
.service-card-header{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:14px;
}
.feature-kicker,
.service-card-kicker{
  margin:0;
  color:var(--primary-dark);
  font-size:.76rem;
  font-weight:700;
  letter-spacing:.14em;
  text-transform:uppercase;
}
.feature-badge,
.service-card-badge{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-width:56px;
  padding:9px 12px;
  border:1px solid rgba(47,138,88,.16);
  border-radius:999px;
  background:rgba(226,240,231,.92);
  color:var(--primary-dark);
  font-size:.72rem;
  font-weight:800;
  letter-spacing:.1em;
  text-transform:uppercase;
}
.feature-card p,
.service-card p{
  max-width:none;
}
.service-card{
  gap:14px;
  background:linear-gradient(180deg,rgba(249,252,249,.94),rgba(242,247,243,.98));
}
.service-card h3{
  font-size:1.2rem;
}
.timeline{
  grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
}
.grid-2{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:20px;
}
.grid-3,.grid-4{
  grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
  gap:20px;
}
.card,.timeline-step,.faq-item,.contact-panel,.form-panel{
  border-radius:26px;
}
.card{
  padding:26px;
  display:flex;
  flex-direction:column;
  gap:10px;
}
.card h3{
  margin:0;
  font-size:1.16rem;
  line-height:1.34;
  text-wrap:balance;
}
.card .more{
  display:flex;
  align-items:center;
  width:100%;
  min-height:44px;
  margin-top:auto;
  padding-top:8px;
}
.breadcrumb{
  margin-bottom:16px;
}
.site-footer{
  margin-top:36px;
  padding-top:22px;
}
.footer-grid{
  grid-template-columns:1.2fr 1fr .78fr .92fr;
  gap:22px;
}
.footer-contact-list{
  margin:14px 0 0;
  padding:0;
  list-style:none;
  display:grid;
  gap:14px;
}
.footer-contact-list li{
  display:grid;
  gap:4px;
}
.footer-legal{
  margin:16px 0 0;
  color:var(--muted);
  font-size:.94rem;
  line-height:1.65;
}
.footer-contact-list strong{
  font-size:.94rem;
  color:var(--text);
}
.footer-contact-list a{
  color:var(--muted);
}
.cookie-banner{
  position:fixed;
  right:24px;
  bottom:24px;
  z-index:90;
  width:min(460px,calc(100vw - 32px));
  display:grid;
  gap:16px;
  padding:22px;
  border:1px solid var(--line);
  border-radius:24px;
  background:rgba(255,255,255,.97);
  box-shadow:0 22px 48px rgba(20,35,27,.18);
  backdrop-filter:blur(14px);
}
.cookie-banner[hidden]{
  display:none;
}
.cookie-banner-copy{
  display:grid;
  gap:10px;
}
.cookie-banner-copy strong,
.cookie-banner-copy p{
  margin:0;
}
.cookie-banner-actions{
  display:flex;
  flex-wrap:wrap;
  gap:12px;
  align-items:center;
}
.image-lightbox-trigger{
  display:block;
  width:100%;
  padding:0;
  border:0;
  background:transparent;
  color:inherit;
  text-align:inherit;
  cursor:zoom-in;
}
.image-lightbox-trigger img{
  transition:transform .22s ease,filter .22s ease;
}
.image-lightbox-trigger:hover img,
.image-lightbox-trigger:focus-visible img{
  transform:scale(1.02);
  filter:saturate(1.04);
}
.hero-media-frame .image-lightbox-trigger{
  height:100%;
}
.lightbox-overlay{
  position:fixed;
  inset:0;
  z-index:130;
  display:grid;
  place-items:center;
  padding:24px;
  background:rgba(13,22,17,.82);
  backdrop-filter:blur(10px);
}
.lightbox-overlay[hidden]{
  display:none;
}
.lightbox-dialog{
  position:relative;
  width:min(1120px,100%);
  max-height:100%;
  display:grid;
  gap:14px;
}
.lightbox-stage{
  margin:0;
  display:grid;
  gap:12px;
}
.lightbox-image{
  width:auto;
  max-width:min(100%,var(--lightbox-image-width,100%));
  max-height:min(82vh,var(--lightbox-image-height,920px));
  object-fit:contain;
  border-radius:24px;
  background:rgba(255,255,255,.98);
  box-shadow:0 24px 54px rgba(0,0,0,.28);
  justify-self:center;
}
.lightbox-caption{
  margin:0;
  color:#f3f7f4;
  font-size:.98rem;
  line-height:1.6;
}
.lightbox-close{
  justify-self:end;
  width:48px;
  min-width:48px;
  min-height:48px;
  padding:0;
  border:1px solid rgba(255,255,255,.2);
  border-radius:999px;
  background:rgba(18,28,22,.82);
  color:#fff;
  font-size:1.9rem;
  line-height:1;
}
.lightbox-open{
  overflow:hidden;
}
.privacy-grid{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:20px;
}
.site-nav a,.footer-links a,.footer-services a,.footer-contact-list a,.detail-item strong,.button,.lang-switch,.chip{
  white-space:nowrap;
}
:root{
  --bg:#edf0ea;
  --surface:rgba(255,255,255,.96);
  --surface-soft:#f3f6f1;
  --line:#d1d8d0;
  --line-strong:#98a79b;
  --text:#121814;
  --muted:#5a665d;
  --primary:#4ddc7a;
  --primary-dark:#0d1b13;
  --primary-soft:#e5f9ea;
  --shadow:0 28px 80px rgba(8,18,12,.08);
  --radius:32px;
}
body{
  background:
    radial-gradient(circle at 10% 0%,rgba(77,220,122,.16),transparent 24%),
    radial-gradient(circle at 100% 14%,rgba(13,27,19,.08),transparent 22%),
    linear-gradient(180deg,#f6f8f3 0%,#edf0ea 48%,#eef2eb 100%);
}
body::before{
  background-image:radial-gradient(rgba(12,28,18,.08) 1px,transparent 1px);
  background-size:24px 24px;
  opacity:.34;
}
.header-inner{
  padding:18px 22px;
  border-radius:28px;
  border-color:rgba(77,220,122,.16);
  background:rgba(13,27,19,.92);
  box-shadow:0 24px 80px rgba(5,11,8,.28);
}
.brand-copy strong{
  color:#f6fbf7;
}
.brand-copy small{
  color:rgba(232,240,235,.68);
}
.site-nav a,.footer-links a,.footer-services a,.footer-contact-list a,.text-link{
  color:rgba(235,242,236,.72);
}
.site-nav a:hover,.site-nav a:focus-visible,.site-nav a[aria-current="page"],.footer-links a:hover,.footer-links a:focus-visible,.footer-services a:hover,.footer-services a:focus-visible,.text-link:hover,.text-link:focus-visible,.footer-contact-list a:hover,.footer-contact-list a:focus-visible{
  color:#9bffb9;
}
.lang-switch{
  border-color:rgba(255,255,255,.12);
  background:#132019;
  color:#f6fbf7;
}
.button{
  min-height:56px;
  padding:0 24px;
  border-radius:18px;
  font-weight:800;
}
.button-primary{
  background:linear-gradient(135deg,#5ce482 0%,#31ba61 100%);
  color:#09110c;
  box-shadow:0 14px 34px rgba(77,220,122,.28);
}
.button-primary:hover,.button-primary:focus-visible{
  background:linear-gradient(135deg,#77ef9a 0%,#42ca72 100%);
}
.hero-copy .button-secondary,.page-hero-copy .button-secondary,.cta-band .button-secondary{
  background:transparent;
  border-color:rgba(255,255,255,.14);
  color:#f5fbf7;
}
.hero,.page-hero{
  gap:28px;
}
.hero.hero-media-layout{
  grid-template-columns:minmax(0,1.18fr) minmax(320px,.82fr);
}
.hero-copy,.page-hero-copy,.cta-band{
  background:linear-gradient(160deg,#0d1712 0%,#14231b 68%,#1b3023 100%);
  border:1px solid rgba(77,220,122,.14);
  box-shadow:0 28px 90px rgba(5,10,8,.24);
}
.hero-copy h1,.page-hero-copy h1,.cta-band h2{
  color:#f5fbf7;
  font-size:clamp(2.2rem,4vw,4.15rem);
  line-height:1;
}
.page-hero-copy h1{
  font-size:clamp(1.95rem,3vw,3rem);
}
.hero-copy>p:not(.eyebrow),.page-hero-copy>p:not(.eyebrow),.cta-band p{
  color:rgba(233,241,236,.78);
}
.hero-copy .eyebrow,.page-hero-copy .eyebrow,.cta-band .eyebrow,.division-card .eyebrow,.contact-sidebar .eyebrow{
  color:#8dffb0;
}
.hero-focus-cloud{
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  margin-top:18px;
}
.hero-focus-chip{
  display:inline-flex;
  align-items:center;
  padding:10px 14px;
  border:1px solid rgba(77,220,122,.18);
  border-radius:999px;
  background:rgba(255,255,255,.07);
  color:#eef5f0;
  font-size:.8rem;
  font-weight:700;
  letter-spacing:.03em;
}
.hero-points{
  gap:12px;
  margin-top:30px;
}
.hero-points li{
  padding:14px 16px;
  padding-left:16px;
  border:1px solid rgba(255,255,255,.1);
  border-radius:18px;
  background:rgba(255,255,255,.05);
  color:#eef5f0;
}
.hero-points li::before{
  display:none;
}
.hero-points a{
  color:#eef5f0;
}
.hero-panel,.page-hero-panel{
  background:linear-gradient(180deg,rgba(255,255,255,.98),rgba(243,247,243,.96));
  border:1px solid rgba(13,27,19,.08);
}
.hero-media-panel{
  padding:26px;
}
.hero-media-main{
  padding:14px;
  border-radius:28px;
  background:#fff;
  border:1px solid rgba(13,27,19,.08);
}
.hero-media-main:nth-child(1){
  transform:translateX(18px);
}
.hero-media-main:nth-child(2){
  transform:translateX(-18px);
}
.hero-signal-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:12px;
  margin-top:18px;
}
.hero-signal-card{
  display:grid;
  gap:6px;
  padding:16px;
  border:1px solid rgba(13,27,19,.08);
  border-radius:20px;
  background:#fff;
}
.hero-signal-card strong{
  font-size:.9rem;
  line-height:1.3;
}
.hero-signal-card span{
  color:var(--muted);
  font-size:.84rem;
  line-height:1.45;
}
.division-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:20px;
}
.division-card{
  padding:28px;
  border-radius:30px;
  border:1px solid rgba(77,220,122,.12);
  background:linear-gradient(180deg,#0f1712 0%,#16241b 100%);
  box-shadow:0 24px 70px rgba(7,13,10,.22);
}
.division-card h3{
  margin:0;
  color:#f5fbf7;
  font-size:1.36rem;
  line-height:1.18;
}
.division-card p{
  max-width:none;
  color:rgba(236,243,238,.76);
}
.division-card .chip-list{
  margin-top:18px;
}
.division-card .chip{
  background:rgba(255,255,255,.08);
  border-color:rgba(77,220,122,.18);
  color:#eef5f0;
}
.feature-card,.service-card,.card,.contact-panel,.form-panel,.faq-item{
  border:1px solid rgba(13,27,19,.08);
  box-shadow:0 20px 60px rgba(10,18,13,.08);
}
.feature-card,.service-card{
  border-radius:30px;
}
.service-card{
  background:linear-gradient(180deg,#ffffff,#f4f7f3);
}
.timeline-step{
  background:linear-gradient(180deg,#0f1712,#17251c);
  border:1px solid rgba(77,220,122,.12);
  box-shadow:0 22px 70px rgba(6,12,9,.22);
}
.timeline-step span,.timeline-step h3{
  color:#f5fbf7;
}
.timeline-step p{
  color:rgba(236,243,238,.76);
}
.contact-layout{
  background:linear-gradient(180deg,rgba(255,255,255,.94),rgba(241,246,241,.96));
  border:1px solid rgba(13,27,19,.08);
}
.contact-sidebar{
  padding:34px;
  border-radius:28px;
  border:1px solid rgba(77,220,122,.14);
  background:linear-gradient(160deg,#0f1712,#16241b);
  box-shadow:0 24px 70px rgba(6,12,9,.22);
}
.contact-sidebar h2,.contact-sidebar>p{
  color:#f5fbf7;
}
.contact-sidebar .detail-item{
  border-color:rgba(255,255,255,.08);
  background:rgba(255,255,255,.04);
}
.contact-sidebar .detail-item strong{
  color:#f5fbf7;
}
.contact-sidebar .detail-item p,.contact-sidebar .detail-item a{
  color:rgba(236,243,238,.76);
}
.site-footer{
  margin-top:48px;
  padding-top:0;
  border-top:0;
}
.footer-grid{
  padding:32px;
  border:1px solid rgba(77,220,122,.12);
  border-radius:30px;
  background:linear-gradient(160deg,#0f1712,#16241b);
}
.footer-title,.footer-contact-list strong{
  color:#f5fbf7;
}
.footer-note,.footer-links a,.footer-services a,.footer-contact-list a,.footer-legal,.footer-bottom{
  color:rgba(235,242,236,.72);
}
.footer-bottom{
  border-top:1px solid rgba(255,255,255,.08);
}
@media (max-width:1280px){
  :root{
    --max:1360px;
  }
  .hero,.page-hero{
    grid-template-columns:minmax(0,1.3fr) minmax(280px,.72fr);
  }
  .hero.hero-media-layout{
    grid-template-columns:minmax(0,1.12fr) minmax(340px,.88fr);
  }
  .division-grid{
    grid-template-columns:repeat(2,minmax(0,1fr));
  }
}
@media (max-width:1100px){
  .hero,.page-hero,.contact-layout,.cta-band,.gateway-panel,.two-col,.footer-grid{
    grid-template-columns:1fr;
  }
  .hero.hero-media-layout{
    grid-template-columns:1fr;
  }
  .hero-points,.grid-2{
    grid-template-columns:1fr;
  }
  .hero-media-main:nth-child(1),
  .hero-media-main:nth-child(2){
    transform:none;
  }
  .division-grid,.hero-signal-grid{
    grid-template-columns:1fr;
  }
  .service-carousel-track{
    grid-auto-columns:calc((100% - 20px) / 2);
  }
  .site-nav a,.footer-links a,.footer-services a,.detail-item strong{
    white-space:normal;
  }
}
@media (max-width:920px){
  main{
    gap:20px;
  }
  main section{
    padding:24px;
    border-radius:28px;
  }
  .grid-3,.grid-4,.grid-2,.timeline,.input-grid,.checkbox-group,.privacy-grid{
    grid-template-columns:1fr;
  }
  .hero-copy h1{
    font-size:clamp(1.85rem,5.7vw,2.35rem);
  }
  .page-hero-copy h1{
    font-size:clamp(1.62rem,4.8vw,1.98rem);
  }
  .cookie-banner{
    position:static;
    right:auto;
    bottom:auto;
    width:100%;
    margin:0 0 18px;
    box-shadow:var(--shadow);
  }
  .lightbox-overlay{
    padding:16px;
  }
}
@media (max-width:740px){
  .hero-copy,.hero-panel,.page-hero-copy,.page-hero-panel,.contact-panel,.form-panel,.cta-band,.gateway-panel{
    padding:28px;
  }
  main section{
    padding:22px;
  }
  main section::before{
    left:22px;
    right:22px;
  }
  .lightbox-image{
    border-radius:18px;
  }
  .lightbox-caption{
    font-size:.92rem;
  }
  .service-carousel-header{
    align-items:flex-start;
    flex-direction:column;
  }
  .service-carousel-controls{
    width:100%;
  }
  .service-carousel-button{
    flex:1 1 0;
  }
  .service-carousel-track{
    grid-auto-columns:100%;
  }
}
:root{
  --bg:#dfe5dd;
  --surface:#f7faf6;
  --surface-soft:#edf2ed;
  --line:#c6cfc6;
  --line-strong:#8da190;
  --text:#0f1511;
  --muted:#58655c;
  --primary:#58df84;
  --primary-dark:#0a120d;
  --primary-soft:#e1f6e7;
  --shadow:0 20px 60px rgba(7,14,10,.12);
  --radius:8px;
}
body{
  background:
    linear-gradient(180deg,#e4e9e2 0%,#dfe5dd 100%);
}
body::before{
  background-image:
    linear-gradient(rgba(10,20,14,.05) 1px,transparent 1px),
    linear-gradient(90deg,rgba(10,20,14,.05) 1px,transparent 1px);
  background-size:56px 56px;
  opacity:.2;
}
.site-shell,.gateway-shell{
  width:100%;
  max-width:none;
}
.site-shell{
  padding:0 0 72px;
}
.site-header{
  top:0;
  margin-bottom:0;
}
.header-inner{
  padding:18px clamp(22px,4vw,64px);
  border-top:0;
  border-left:0;
  border-right:0;
  border-radius:0;
  background:rgba(10,17,13,.96);
  box-shadow:0 14px 40px rgba(4,8,6,.24);
}
.site-nav{
  gap:26px;
}
.site-nav a,.footer-links a,.footer-services a,.footer-contact-list a,.text-link{
  color:rgba(236,242,238,.72);
}
.site-nav a:hover,.site-nav a:focus-visible,.site-nav a[aria-current="page"],.footer-links a:hover,.footer-links a:focus-visible,.footer-services a:hover,.footer-services a:focus-visible,.text-link:hover,.text-link:focus-visible,.footer-contact-list a:hover,.footer-contact-list a:focus-visible{
  color:#a6ffbf;
}
.nav-toggle,.lang-switch,.button,.chip{
  border-radius:6px;
}
.nav-toggle,.lang-switch,.button{
  min-height:54px;
  font-weight:800;
  letter-spacing:.04em;
}
.nav-toggle,.lang-switch{
  border-color:rgba(255,255,255,.14);
  background:#111a14;
  color:#f5fbf7;
}
.button-primary{
  background:#58df84;
  color:#09110c;
  box-shadow:none;
}
.button-primary:hover,.button-primary:focus-visible{
  background:#7aee9f;
}
.button-secondary{
  background:#f7faf6;
  border-color:#0f1913;
  color:#0f1913;
}
.hero-copy .button-secondary,.page-hero-copy .button-secondary,.cta-band .button-secondary{
  background:transparent;
  border-color:rgba(255,255,255,.16);
  color:#f5fbf7;
}
main{
  gap:0;
  grid-template-columns:minmax(0,1fr);
}
main > *{
  min-width:0;
}
main section{
  padding:clamp(38px,5vw,78px) clamp(20px,4vw,72px);
  border:0;
  border-radius:0;
  box-shadow:none;
  background:transparent;
  overflow:visible;
}
main section::before{
  display:none;
}
.section-shell,.layout-shell,.footer-shell{
  width:min(100%,1400px);
  margin:0 auto;
}
@supports selector(:has(*)){
  .section-shell:not(.blog-article-shell):has(> .section-heading){
    display:grid;
    grid-template-columns:minmax(220px,.62fr) minmax(0,1.38fr);
    gap:clamp(24px,3.6vw,58px);
    align-items:start;
  }
  .section-shell:not(.blog-article-shell):has(> .section-heading) > *{
    grid-column:2;
    min-width:0;
  }
  .section-shell:not(.blog-article-shell):has(> .section-heading) > .section-heading{
    grid-column:1;
    position:sticky;
    top:104px;
    align-self:start;
    margin-bottom:0;
  }
  @media (max-width:980px){
    .section-shell:not(.blog-article-shell):has(> .section-heading){
      display:block;
    }
    .section-shell:not(.blog-article-shell):has(> .section-heading) > .section-heading{
      position:static;
      margin-bottom:28px;
    }
  }
}
.breadcrumb{
  width:min(100%,1400px);
  margin:0 auto;
  padding:18px clamp(20px,4vw,72px) 24px;
  color:#617067;
}
.hero-band,.page-hero-band,.division-section,.process-section,.cta-section{
  background:#0b120d;
}
.featured-section,.priority-section,.service-overview-section,.industries-section,.privacy-section,.about-values-section,.thanks-section{
  background:#f7faf6;
}
.support-section,.extra-section,.clients-section,.coverage-section,.service-cases-section,.privacy-choices-section,.contact-band,.carousel-section,.faq-section,.trust-section{
  background:#e8ede7;
}
.hero,.page-hero,.contact-layout,.cta-band,.two-col,.footer-grid{
  display:grid;
  gap:22px;
}
.hero > *,.page-hero > *,.contact-layout > *,.cta-band > *,.two-col > *,.footer-grid > *{
  min-width:0;
}
.hero,.page-hero{
  grid-template-columns:minmax(0,1.14fr) minmax(340px,.86fr);
  align-items:stretch;
}
.hero.hero-media-layout{
  grid-template-columns:minmax(0,1.2fr) minmax(360px,.8fr);
  gap:30px;
}
.contact-layout{
  grid-template-columns:minmax(320px,.88fr) minmax(0,1.12fr);
  align-items:start;
  padding:0;
  border:0;
  background:transparent;
  box-shadow:none;
}
.cta-band,.two-col{
  grid-template-columns:repeat(2,minmax(0,1fr));
}
.contact-hero{
  grid-template-columns:1fr;
}
:root{
  --muted:#38483d;
}
.hero-copy,.page-hero-copy{
  display:grid;
  align-content:start;
  gap:16px;
  padding:0;
  border:0;
  border-radius:0;
  background:transparent;
  box-shadow:none;
}
.hero-copy,.page-hero-copy,.hero-panel,.page-hero-panel,.promo-hero-grid > *,.referral-nav > *,.referral-steps-section .timeline > *,.input-grid > *,.checkbox-group > *,.field,form > *{
  min-width:0;
}
.hero-copy h1,.page-hero-copy h1,.section-heading h2,.cta-band h2{
  margin:0;
  line-height:.98;
  letter-spacing:-.035em;
}
.hero-copy h1{
  max-width:18ch;
  font-size:clamp(2.35rem,4vw,4rem);
  color:#f5fbf7;
}
.page-hero-copy h1,.section-heading h2,.cta-band h2{
  font-size:clamp(1.9rem,3vw,2.85rem);
}
.page-hero-copy h1,.cta-band h2{
  color:#f5fbf7;
}
.page-home .hero-copy h1{
  max-width:18ch;
}
.page-about .page-hero-copy{
  gap:14px;
}
.page-about .page-hero-copy h1{
  max-width:18ch;
  font-size:clamp(1.7rem,2.25vw,2.15rem);
  line-height:1.08;
}
.hero-copy>p:not(.eyebrow),.page-hero-copy>p:not(.eyebrow),.cta-band p{
  color:rgba(235,242,237,.78);
  max-width:66ch;
}
.section-heading{
  display:grid;
  gap:14px;
  margin-bottom:28px;
  align-content:start;
  padding-top:18px;
  border-top:3px solid rgba(88,223,132,.7);
}
.section-heading p{
  max-width:34ch;
  color:#415247;
  font-size:1rem;
  line-height:1.74;
}
.section-heading h2{
  max-width:11ch;
  font-size:clamp(2.1rem,3vw,3.2rem);
  line-height:.98;
}
.feature-card h3,.service-card h3,.card h3,.contact-panel h2,.detail-item strong,.faq-item summary{
  color:#132019;
}
.feature-card p,.service-card p,.card p,.faq-item p,.detail-item p,.detail-item a,.contact-panel:not(.contact-sidebar) p,.contact-panel:not(.contact-sidebar) .text-link,.form-note{
  color:#344439;
}
.trust-section .section-heading p,.featured-section .section-heading p,.priority-section .section-heading p,.support-section .section-heading p,.extra-section .section-heading p,.about-values-section .section-heading p,.clients-section .section-heading p,.coverage-section .section-heading p,.service-overview-section .section-heading p,.service-cases-section .section-heading p,.carousel-section .section-heading p,.faq-section .section-heading p,.privacy-section .section-heading p,.privacy-choices-section .section-heading p,.industries-section .section-heading p,.thanks-section .section-heading p{
  color:var(--muted);
}
.division-section .section-heading h2,.process-section .section-heading h2{
  color:#f5fbf7;
}
.division-section .section-heading p:not(.eyebrow),.process-section .section-heading p:not(.eyebrow){
  color:rgba(235,242,237,.74);
}
.hero-copy .eyebrow,.page-hero-copy .eyebrow,.division-card .eyebrow,.contact-sidebar .eyebrow,.cta-band .eyebrow,.process-section .timeline-step span{
  color:#92ffb2;
}
.hero-actions,.page-hero-actions,.cta-actions{
  gap:12px;
}
.cta-band{
  grid-template-columns:minmax(0,1.18fr) minmax(280px,.82fr);
  gap:32px;
  align-items:stretch;
  padding:40px;
}
.cta-band > :first-child{
  display:grid;
  align-content:start;
  gap:14px;
}
.cta-band .cta-actions{
  display:grid;
  align-content:end;
  gap:14px;
  padding:22px 0 0 28px;
  border-left:1px solid rgba(255,255,255,.14);
}
.cta-band .cta-actions .button{
  width:100%;
  justify-content:center;
}
.hero-focus-cloud{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:12px;
  margin-top:26px;
}
.hero-focus-chip{
  padding:14px 16px;
  border:1px solid rgba(88,223,132,.18);
  border-radius:6px;
  background:rgba(255,255,255,.06);
  font-size:.8rem;
  font-weight:800;
  letter-spacing:.08em;
}
.hero-points{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:12px;
  margin-top:22px;
}
.hero-points li{
  min-height:100%;
  padding:18px 18px 18px 20px;
  border:1px solid rgba(255,255,255,.12);
  border-left:4px solid #58df84;
  border-radius:0;
  background:rgba(255,255,255,.04);
  color:#edf5ef;
}
.hero-points li::before{
  display:none;
}
.hero-points a{
  color:#edf5ef;
}
.hero-points a:hover,
.hero-points a:focus-visible{
  color:#f5fbf7;
  transform:translateX(2px);
  text-decoration:none;
}
.hero-panel,.page-hero-panel,.contact-panel,.form-panel,.faq-item{
  border-radius:8px;
  border:1px solid rgba(12,20,15,.12);
  box-shadow:none;
}
.hero-panel,.page-hero-panel{
  padding:28px;
  background:#f7faf6;
}
.hero-media-panel{
  display:grid;
  gap:18px;
}
.hero-media-stack{
  display:grid;
  gap:16px;
}
.hero-media-main{
  padding:14px;
  border-radius:8px;
  border:1px solid rgba(12,20,15,.12);
  background:#fff;
}
.hero-media-main:nth-child(1),.hero-media-main:nth-child(2){
  transform:none;
}
.hero-signal-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:0;
  border-top:1px solid rgba(12,20,15,.12);
  border-left:1px solid rgba(12,20,15,.12);
}
.hero-signal-card{
  padding:18px;
  border-right:1px solid rgba(12,20,15,.12);
  border-bottom:1px solid rgba(12,20,15,.12);
  border-radius:0;
  background:#eef3ef;
}
.division-grid,.process-section .timeline{
  gap:0;
}
.division-grid{
  grid-template-columns:repeat(3,minmax(0,1fr));
  border-top:1px solid rgba(255,255,255,.14);
  border-left:1px solid rgba(255,255,255,.14);
}
.division-card{
  padding:30px;
  border-right:1px solid rgba(255,255,255,.14);
  border-bottom:1px solid rgba(255,255,255,.14);
  border-radius:0;
  background:rgba(255,255,255,.02);
  box-shadow:none;
}
.division-card h3{
  margin:0;
  color:#f5fbf7;
  font-size:1.42rem;
  line-height:1.1;
}
.division-card p{
  color:rgba(235,242,237,.78);
}
.division-card .chip-list{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:12px;
  align-items:stretch;
}
.division-card .chip{
  justify-content:flex-start;
  border-radius:4px;
  background:rgba(255,255,255,.06);
  border-color:rgba(88,223,132,.16);
  color:#eef5f0;
}
.division-card .chip,.service-chip-links .chip{
  white-space:normal;
  align-items:flex-start;
  min-height:100%;
  line-height:1.35;
}
.page-services .page-hero-panel .service-chip-links{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:10px;
  margin-top:18px;
}
.page-services .page-hero-panel .service-chip-links .chip{
  justify-content:flex-start;
  padding:12px 14px;
  background:#fff;
  border-color:rgba(12,20,15,.12);
  color:#132019;
}
.page-services .page-hero-panel .service-chip-links .chip:last-child:nth-child(odd){
  grid-column:1/-1;
}
.feature-card,.service-card,.card,.contact-panel,.form-panel,.faq-item{
  border-radius:8px;
  border:1px solid rgba(12,20,15,.12);
  box-shadow:none;
}
.feature-card,.service-card,.card,.contact-panel,.form-panel{
  background:#f8fbf8;
}
.form-panel{
  position:relative;
  overflow:hidden;
}
.form-panel::before{
  content:"";
  position:absolute;
  inset:0 0 auto 0;
  height:5px;
  background:linear-gradient(90deg,#2f8a58 0%,#7ad296 56%,rgba(122,210,150,0) 100%);
}
.feature-card,.service-card{
  min-height:100%;
}
.feature-card::before,.service-card::before{
  background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(241,245,241,.98));
}
.feature-badge,.service-card-badge,.chip{
  border-radius:4px;
}
.feature-badge,.service-card-badge{
  background:#122118;
  color:#95ffb4;
}
.timeline{
  grid-template-columns:repeat(4,minmax(0,1fr));
}
.timeline-step{
  padding:26px;
  border-radius:0;
  border-right:1px solid rgba(255,255,255,.14);
  border-bottom:1px solid rgba(255,255,255,.14);
  box-shadow:none;
  background:rgba(255,255,255,.02);
}
.timeline-step h3,.timeline-step span{
  color:#f5fbf7;
}
.timeline-step p{
  color:rgba(235,242,237,.78);
}
.contact-sidebar{
  padding:34px;
  border-radius:8px;
  background:linear-gradient(180deg,#09100c,#0f1812);
  border:1px solid rgba(88,223,132,.18);
  box-shadow:none;
  display:grid;
  align-content:start;
  min-width:0;
  position:relative;
  z-index:1;
}
.contact-sidebar h2,.contact-sidebar>p,.contact-sidebar .detail-item strong{
  color:#f5fbf7;
}
.contact-sidebar .detail-item{
  border-radius:6px;
  border-color:rgba(255,255,255,.1);
  background:rgba(255,255,255,.05);
}
.contact-sidebar .detail-item p,.contact-sidebar .detail-item a{
  color:rgba(242,248,244,.88);
}
.page-contact .contact-sidebar{
  background:#fbfcfa;
  border-color:rgba(12,20,15,.12);
}
.page-contact .contact-sidebar .eyebrow{
  color:var(--primary-dark);
}
.page-contact .contact-sidebar h2,.page-contact .contact-sidebar>p,.page-contact .contact-sidebar .detail-item strong{
  color:#132019;
}
.page-contact .contact-sidebar .detail-item{
  border-color:rgba(12,20,15,.12);
  background:#fff;
}
.page-contact .contact-sidebar .detail-item p,.page-contact .contact-sidebar .detail-item a{
  color:#344439;
}
.detail-item,.field input,.field select,.field textarea,.checkbox-group,.contact-panel .note,.zoho-form-embed iframe{
  border-radius:6px;
}
.contact-band .contact-layout{
  align-items:start;
}
.contact-band .contact-panel:not(.contact-sidebar){
  background:#fbfcfa;
}
.contact-band .contact-layout > *{
  min-width:0;
}
.contact-band .form-panel{
  position:relative;
  z-index:0;
}
.page-contact .contact-band{
  background:
    radial-gradient(circle at top left,rgba(47,138,88,.1),transparent 26%),
    linear-gradient(180deg,#e6ede7 0%,#edf3ed 52%,#e7ede7 100%);
}
.page-contact .contact-shell{
  width:min(100%,1480px);
}
.page-contact .contact-layout{
  grid-template-columns:minmax(390px,.96fr) minmax(0,1.04fr);
  gap:30px;
}
.page-contact .contact-sidebar{
  padding:42px;
  border-radius:20px;
  border:1px solid rgba(19,32,25,.12);
  background:
    radial-gradient(circle at top right,rgba(47,138,88,.12),transparent 36%),
    linear-gradient(180deg,rgba(255,255,255,.98),rgba(245,249,245,.98));
  box-shadow:0 24px 80px rgba(12,20,15,.08);
  overflow:hidden;
}
.page-contact .contact-sidebar::before{
  content:"";
  position:absolute;
  inset:0 0 auto 0;
  height:6px;
  background:linear-gradient(90deg,#2f8a58 0%,#7ad296 52%,rgba(122,210,150,0) 100%);
}
.page-contact .contact-sidebar h2{
  font-size:clamp(1.58rem,1.9vw,2.1rem);
  letter-spacing:-.03em;
}
.page-contact .contact-sidebar>p{
  max-width:48ch;
  color:#415247;
}
.page-contact .contact-sidebar-stack{
  display:grid;
  gap:18px;
}
.page-contact .contact-direct-grid{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:14px;
}
.page-contact .contact-hours-grid{
  display:grid;
  gap:14px;
}
.page-contact .contact-form-column{
  display:grid;
  gap:28px;
}
.page-contact .contact-sidebar .contact-detail-card{
  padding:20px 20px 22px;
  min-height:100%;
  border-radius:16px;
  position:relative;
}
.page-contact .contact-sidebar .contact-detail-card strong{
  display:block;
  margin-bottom:10px;
  white-space:normal;
  font-size:1.02rem;
  line-height:1.14;
}
.page-contact .contact-sidebar .contact-detail-card p,
.page-contact .contact-sidebar .contact-detail-card a{
  max-width:none;
  font-size:1.01rem;
  line-height:1.72;
}
.page-contact .contact-sidebar .contact-detail-card-direct{
  border:1px solid rgba(12,20,15,.08);
  background:linear-gradient(180deg,#ffffff,#f8fbf8);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.9);
}
.page-contact .contact-sidebar .contact-detail-card-direct::after{
  content:"";
  position:absolute;
  left:18px;
  right:18px;
  bottom:0;
  height:1px;
  background:linear-gradient(90deg,rgba(47,138,88,.18),rgba(47,138,88,0));
}
.page-contact .contact-sidebar .contact-detail-card-hours{
  border:1px solid rgba(47,138,88,.18);
  background:linear-gradient(180deg,#f3f8f4,#ebf3ed);
}
.page-contact .contact-sidebar .contact-detail-card-hours strong{
  color:#1f6640;
}
.page-contact .contact-sidebar .contact-detail-card-note{
  border:1px solid rgba(21,54,40,.14);
  background:linear-gradient(180deg,#ffffff,#f3f7f4);
}
.page-contact .contact-sidebar .contact-detail-card-note p{
  margin:0;
  color:#415247;
}
@media (max-width:1200px){
  .page-contact .contact-layout{
    grid-template-columns:1fr;
  }
}
@media (max-width:760px){
  .page-contact .contact-form-column{
    order:-1;
  }
  .page-contact .contact-sidebar{
    order:1;
  }
  .page-contact .contact-sidebar{
    padding:28px;
  }
  .page-contact .contact-direct-grid{
    grid-template-columns:1fr;
  }
}
.service-carousel-track{
  grid-auto-columns:calc((100% - 36px) / 3);
}
.site-footer{
  margin-top:0;
  padding-top:0;
  border-top:0;
  background:#0b120d;
}
.footer-shell{
  padding:0 clamp(20px,4vw,72px);
}
.footer-grid{
  grid-template-columns:minmax(220px,1.05fr) minmax(320px,1.3fr) minmax(160px,.78fr) minmax(170px,.88fr) minmax(220px,1.02fr);
  align-items:start;
  gap:24px 28px;
  padding:40px 0 18px;
  border:0;
  border-radius:0;
  background:transparent;
  box-shadow:none;
}
.footer-column{
  min-width:0;
}
.footer-column-brand{
  display:grid;
  align-content:start;
  gap:12px;
}
.footer-brand-copy{
  display:grid;
  gap:12px;
}
.footer-grid,.footer-bottom{
  color:rgba(235,242,237,.72);
}
.footer-title,.footer-brand strong,.footer-contact-list strong{
  color:#f5fbf7;
}
.footer-brand img{
  transform:none;
}
.footer-title{
  margin:0 0 10px;
  font-size:.78rem;
  font-weight:800;
  letter-spacing:.18em;
}
.footer-note{
  margin:0;
  max-width:34ch;
  color:rgba(235,242,237,.78);
  font-size:.95rem;
  line-height:1.62;
}
.footer-legal{
  margin:0;
  padding-top:12px;
  border-top:1px solid rgba(255,255,255,.1);
  color:rgba(235,242,237,.64);
  line-height:1.56;
}
.footer-bottom{
  margin-top:0;
  padding:16px 0 28px;
  border-top:1px solid rgba(255,255,255,.08);
  color:rgba(235,242,237,.62);
  font-size:.92rem;
}
@media (max-width:1180px){
  .hero,.page-hero,.contact-layout,.cta-band,.two-col,.footer-grid{
    grid-template-columns:1fr;
  }
  .hero.hero-media-layout{
    grid-template-columns:1fr;
  }
  .division-grid,.timeline{
    grid-template-columns:1fr;
  }
  .grid-4{
    grid-template-columns:repeat(2,minmax(0,1fr));
  }
  .hero-signal-grid{
    grid-template-columns:1fr;
  }
  .service-carousel-track{
    grid-auto-columns:calc((100% - 18px) / 2);
  }
}
@media (max-width:860px){
  .header-inner{
    display:grid;
    justify-items:start;
    gap:14px;
    padding:16px 22px;
  }
  .nav-toggle{
    display:inline-flex;
  }
  .site-nav{
    display:none;
    width:100%;
    flex-direction:column;
    gap:14px;
    padding-top:10px;
  }
  .site-nav.is-open{
    display:flex;
  }
  .header-actions{
    width:100%;
    flex-wrap:wrap;
  }
  main section{
    padding:32px 18px;
  }
  .breadcrumb{
    padding-left:18px;
    padding-right:18px;
  }
  .hero-focus-cloud,.hero-points,.grid-2,.grid-3,.grid-4,.faq-list,.privacy-grid,.division-card .chip-list{
    grid-template-columns:1fr;
  }
  .page-home .hero-copy h1{
    font-size:clamp(2rem,9vw,2.85rem);
  }
  .page-hero-copy h1{
    font-size:clamp(1.74rem,7vw,2.2rem);
  }
  .page-about .page-hero-copy h1{
    max-width:none;
    font-size:clamp(1.58rem,6.2vw,1.9rem);
    line-height:1.1;
  }
  .service-carousel-track{
    grid-auto-columns:100%;
  }
  .footer-shell{
    padding:0 18px;
  }
  .button{
    white-space:normal;
    text-align:center;
    max-width:100%;
  }
}
'''

css += '''
.nav-item{
  position:relative;
}
.nav-link{
  display:inline-flex;
  align-items:center;
  min-height:40px;
}
.nav-item-has-children .nav-link::after{
  content:"";
  width:8px;
  height:8px;
  margin-left:8px;
  border-right:1.5px solid currentColor;
  border-bottom:1.5px solid currentColor;
  transform:translateY(-1px) rotate(45deg);
  opacity:.68;
}
.nav-submenu{
  position:absolute;
  top:calc(100% + 10px);
  left:0;
  min-width:260px;
  display:grid;
  gap:8px;
  padding:14px;
  border:1px solid rgba(12,20,15,.12);
  border-radius:12px;
  background:rgba(255,255,255,.98);
  box-shadow:0 18px 40px rgba(18,29,22,.12);
  opacity:0;
  visibility:hidden;
  transform:translateY(6px);
  transition:opacity .16s ease,transform .16s ease,visibility .16s ease;
  z-index:60;
}
.nav-submenu a{
  display:block;
  padding:10px 12px;
  border-radius:8px;
  color:#132019;
  font-size:.96rem;
  font-weight:600;
  line-height:1.4;
  white-space:normal;
}
.nav-submenu a:hover,.nav-submenu a:focus-visible,.nav-submenu a[aria-current="page"]{
  background:var(--primary-soft);
}
.nav-submenu-wide{
  min-width:620px;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:10px 12px;
}
.nav-item-has-children:hover .nav-submenu,.nav-item-has-children:focus-within .nav-submenu{
  opacity:1;
  visibility:visible;
  transform:translateY(0);
}
.brand-badge-grid{
  display:grid;
  grid-template-columns:repeat(6,minmax(0,1fr));
  gap:14px;
}
.brand-badge{
  display:flex;
  align-items:center;
  justify-content:center;
  min-height:82px;
  padding:18px;
  border:1px solid rgba(12,20,15,.12);
  border-radius:8px;
  background:linear-gradient(180deg,#fbfcfb,#f1f5f1);
  text-align:center;
}
.brand-badge span{
  color:#2b3830;
  font-size:1rem;
  font-weight:700;
  letter-spacing:.04em;
}
.footer-grid{
  grid-template-columns:minmax(220px,1.05fr) minmax(320px,1.3fr) minmax(160px,.78fr) minmax(170px,.88fr) minmax(220px,1.02fr);
}
@media (max-width:1180px){
  .footer-grid{
    grid-template-columns:repeat(2,minmax(0,1fr));
    gap:20px 24px;
  }
  .footer-column-brand,
  .footer-column-contact{
    grid-column:1 / -1;
  }
}
.footer-contact-list{
  display:grid;
  gap:0;
  margin:0;
  padding:0;
  list-style:none;
}
.footer-contact-list li{
  display:grid;
  gap:8px;
  padding:10px 0;
  border-top:1px solid rgba(255,255,255,.08);
}
.footer-contact-list li:first-child{
  padding-top:0;
  border-top:0;
}
.footer-contact-list span,.footer-contact-list a,.footer-links a,.footer-services a,.social-link{
  color:rgba(235,242,237,.76);
}
.footer-contact-list strong{
  font-size:.74rem;
  font-weight:800;
  letter-spacing:.12em;
  text-transform:uppercase;
}
.footer-contact-list span{
  line-height:1.64;
}
.footer-socials{
  display:grid;
  gap:3px;
}
.footer-links,
.footer-services{
  display:grid;
  gap:2px;
}
.footer-contact-list a,
.footer-links a,
.footer-services a,
.social-link{
  display:inline-flex;
  align-items:center;
  width:100%;
  min-height:0;
  padding:4px 0;
  line-height:1.42;
}
.social-link{
  gap:10px;
}
.social-link svg{
  width:18px;
  height:18px;
  flex:0 0 18px;
}
.social-link:hover,.social-link:focus-visible{
  color:#f5fbf7;
}
.blog-grid{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:18px;
}
.blog-empty-card{
  display:grid;
  gap:18px;
  grid-column:1/-1;
}
.blog-grid-single{
  grid-template-columns:1fr;
}
.blog-article-card{
  display:grid;
  gap:26px;
  align-items:start;
}
.blog-grid-single .blog-article-card{
  grid-template-columns:minmax(0,1.18fr) minmax(280px,.82fr);
  padding:30px;
}
.blog-article-card-main,
.blog-article-card-side{
  display:grid;
  align-content:start;
  gap:16px;
}
.blog-grid-single .blog-article-card-main h3{
  font-size:clamp(1.5rem,2vw,2rem);
  line-height:1.16;
}
.blog-article-card-main{
  position:relative;
  overflow:hidden;
  padding:28px;
  border:1px solid rgba(12,20,15,.08);
  border-radius:22px;
  background:linear-gradient(180deg,#fbfdfb,#eef5ef);
  min-height:100%;
  color:inherit;
  text-decoration:none;
  cursor:pointer;
  transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease;
}
.blog-article-card-main::before{
  content:"";
  position:absolute;
  inset:0;
  background-image:
    linear-gradient(120deg,rgba(255,255,255,.94) 0%,rgba(248,251,248,.9) 46%,rgba(255,255,255,.78) 100%),
    var(--blog-card-image,none);
  background-position:center,var(--blog-card-image-position,center center);
  background-size:auto,cover;
  background-repeat:no-repeat;
  transform:scale(1.02);
}
.blog-article-card-main > *{
  position:relative;
  z-index:1;
}
.blog-article-card-main:hover,
.blog-article-card-main:focus-visible{
  transform:translateY(-2px);
  border-color:rgba(31,102,64,.22);
  box-shadow:0 22px 54px rgba(12,20,15,.12);
}
.blog-article-card-main p{
  max-width:58ch;
}
.blog-article-card-main h3{
  transition:color .18s ease;
}
.blog-article-card-main:hover h3,
.blog-article-card-main:focus-visible h3{
  color:var(--primary-dark);
}
.blog-article-card .chip-list{
  margin-top:0;
}
.blog-card-surface-link{
  display:inline-flex;
  align-items:center;
  gap:10px;
  margin-top:auto;
  padding-top:10px;
  color:var(--primary-dark);
  font-size:.8rem;
  font-weight:800;
  letter-spacing:.12em;
  text-transform:uppercase;
}
.blog-card-surface-link::after{
  content:"->";
  font-size:.95rem;
}
.blog-card-meta,
.blog-article-readout{
  display:grid;
  gap:10px;
}
.blog-article-readout{
  grid-template-columns:repeat(2,minmax(0,1fr));
}
.blog-article-readout .blog-meta-item:last-child{
  grid-column:1 / -1;
}
.blog-meta-item{
  display:grid;
  gap:6px;
  padding:14px 16px;
  border:1px solid rgba(12,20,15,.1);
  border-radius:16px;
  background:linear-gradient(180deg,#ffffff,#f2f7f2);
  min-width:0;
}
.blog-meta-item strong{
  color:var(--text);
  font-size:.72rem;
  font-weight:800;
  letter-spacing:.12em;
  line-height:1.1;
  text-transform:uppercase;
}
.blog-meta-item span{
  color:var(--muted);
  font-size:.96rem;
  line-height:1.38;
}
.blog-card-link{
  width:100%;
  justify-content:center;
  margin-top:4px;
}
.blog-article-panel{
  display:grid;
  align-content:start;
  gap:20px;
  position:relative;
  overflow:hidden;
}
.blog-article-panel::before{
  content:"";
  position:absolute;
  inset:0 0 auto 0;
  height:5px;
  background:linear-gradient(90deg,#2f8a58 0%,#7ad296 56%,rgba(122,210,150,0) 100%);
}
.blog-article-panel > *{
  position:relative;
}
.blog-article-shell{
  width:min(100%,1300px);
}
.blog-article-hero-band{
  position:relative;
  overflow:hidden;
  isolation:isolate;
}
.blog-article-hero-band::before{
  content:"";
  position:absolute;
  inset:0;
  background-image:
    linear-gradient(90deg,rgba(7,12,10,1) 0%,rgba(7,12,10,.94) 34%,rgba(7,12,10,.72) 58%,rgba(7,12,10,.92) 100%),
    radial-gradient(circle at top right,rgba(122,210,150,.12),transparent 34%),
    var(--blog-hero-image,none);
  background-position:center,top right,var(--blog-hero-position,center center);
  background-size:auto,auto,cover;
  background-repeat:no-repeat;
  filter:saturate(.82) brightness(.9);
  transform:scale(1.03);
  z-index:-2;
}
.blog-article-hero-band::after{
  content:"";
  position:absolute;
  inset:0;
  background:
    linear-gradient(180deg,rgba(7,12,10,.2),rgba(7,12,10,.06) 30%,rgba(7,12,10,.18) 100%),
    radial-gradient(circle at left center,rgba(7,12,10,.14),transparent 38%);
  z-index:-1;
}
.blog-article-hero{
  grid-template-columns:minmax(0,1.12fr) minmax(320px,.88fr);
  gap:36px;
  align-items:stretch;
}
.blog-article-hero .page-hero-copy h1{
  max-width:12ch;
  font-size:clamp(2.4rem,3.8vw,4rem);
  line-height:.96;
}
.blog-article-hero .page-hero-copy > p:not(.eyebrow){
  max-width:50ch;
  font-size:1.16rem;
  line-height:1.92;
  padding-left:24px;
  border-left:4px solid rgba(122,210,150,.58);
  color:rgba(245,251,247,.84);
}
.blog-article-hero .page-hero-copy{
  padding:16px 0;
  position:relative;
  isolation:isolate;
}
.blog-article-hero .page-hero-copy::after{
  content:"";
  position:absolute;
  top:18px;
  right:18px;
  bottom:18px;
  width:min(430px,48%);
  border-radius:28px;
  background-image:
    linear-gradient(90deg,rgba(7,12,10,.28) 0%,rgba(7,12,10,.58) 100%),
    var(--blog-hero-image,none);
  background-position:center,var(--blog-hero-position,center center);
  background-size:auto,cover;
  background-repeat:no-repeat;
  opacity:.34;
  filter:saturate(.78);
  mask-image:linear-gradient(90deg,transparent 0%,rgba(0,0,0,.3) 18%,#000 100%);
  z-index:-1;
}
.blog-summary-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
  gap:20px;
}
.blog-summary-section,
.blog-article-section,
.blog-article-cta{
  padding:28px 32px;
}
.blog-summary-section+.blog-article-section,
.blog-article-section+.blog-article-section,
.blog-article-section+.blog-article-cta{
  margin-top:10px;
}
.blog-summary-card{
  min-height:100%;
  background:linear-gradient(180deg,#fbfdfb,#eef5ef);
}
.blog-summary-card h3{
  margin:0;
  font-size:1.34rem;
  line-height:1.12;
}
.blog-summary-card p:last-child{
  margin:0;
}
.blog-section-stack{
  display:grid;
  gap:22px;
  position:relative;
  padding-top:24px;
}
.blog-section-stack::before{
  content:"";
  position:absolute;
  top:0;
  left:0;
  right:0;
  height:1px;
  background:linear-gradient(90deg,rgba(12,20,15,.18),rgba(12,20,15,.06));
}
.blog-section-stack .section-heading{
  gap:10px;
  margin-bottom:10px;
  padding-top:0;
  border-top:0;
}
.blog-section-intro{
  display:grid;
  gap:14px;
}
.blog-section-intro.blog-section-intro-split{
  grid-template-columns:minmax(0,1.22fr) minmax(300px,.78fr);
  align-items:start;
  gap:14px;
}
.blog-section-intro.blog-section-intro-split .blog-prose-panel p{
  max-width:none;
}
.blog-prose-panel{
  display:grid;
  gap:22px;
  padding:32px 34px;
}
.blog-prose-panel p{
  margin:0;
  max-width:62ch;
  color:#314036;
  font-size:1.12rem;
  line-height:1.94;
}
.blog-prose-panel ul,
.blog-prose-panel ol,
.blog-subsection ul,
.blog-subsection ol{
  display:grid;
  gap:12px;
  margin:0;
  padding-left:1.3rem;
  color:#314036;
  font-size:1.06rem;
  line-height:1.84;
}
.blog-prose-panel li,
.blog-subsection li{
  max-width:62ch;
}
.blog-subsection-stack,
.blog-comparison-list,
.blog-step-grid{
  display:grid;
  gap:14px;
}
.blog-subsection-stack{
  grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
}
.blog-comparison-list{
  grid-template-columns:1fr;
}
.blog-table-panel{
  display:grid;
  gap:16px;
  padding:0;
  overflow:hidden;
}
.blog-table-head{
  padding:22px 26px 0;
}
.blog-table-head h3{
  margin:0;
  font-size:1.34rem;
}
.blog-table-head p{
  margin:10px 0 0;
  color:var(--muted);
}
.blog-table-scroll{
  overflow-x:auto;
  padding:0 12px 12px;
}
.blog-table{
  width:100%;
  min-width:760px;
  border-collapse:separate;
  border-spacing:0;
}
.blog-table th,
.blog-table td{
  padding:22px 24px;
  border-right:1px solid rgba(12,20,15,.08);
  border-bottom:1px solid rgba(12,20,15,.08);
  text-align:left;
  vertical-align:top;
}
.blog-table thead th{
  background:#132019;
  color:#f5fbf7;
  font-size:.84rem;
  font-weight:800;
  letter-spacing:.12em;
  text-transform:uppercase;
}
.blog-table thead th:first-child{
  border-top-left-radius:18px;
}
.blog-table thead th:last-child{
  border-top-right-radius:18px;
  border-right:0;
}
.blog-table tbody th{
  width:16%;
  background:#edf4ee;
  color:#153628;
  font-size:1rem;
  font-weight:800;
}
.blog-table tbody td{
  color:var(--muted);
  background:#fbfdfb;
  line-height:1.72;
}
.blog-pill{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  padding:4px 10px;
  border-radius:999px;
  font-size:.76rem;
  font-weight:800;
  letter-spacing:.08em;
  text-transform:uppercase;
  white-space:nowrap;
}
.blog-pill-green{
  color:#1f6640;
  background:rgba(34,197,94,.1);
  border:1px solid rgba(34,197,94,.18);
}
.blog-pill-amber{
  color:#a15f00;
  background:rgba(245,158,11,.12);
  border:1px solid rgba(245,158,11,.2);
}
.blog-pill-red{
  color:#c63f3f;
  background:rgba(239,68,68,.09);
  border:1px solid rgba(239,68,68,.16);
}
.blog-table tbody tr:nth-child(even) td{
  background:#f4f8f4;
}
.blog-table tbody td:last-child,
.blog-table tbody th:last-child{
  border-right:0;
}
.blog-subsection-stack,
.blog-comparison-list,
.blog-step-grid{
  display:grid;
  gap:18px;
}
.blog-subsection,
.blog-compare-card,
.blog-step-card{
  display:grid;
  gap:12px;
}
.blog-detail-card,
.blog-subsection,
.blog-step-card,
.blog-compare-card{
  min-height:100%;
}
.blog-detail-card{
  background:linear-gradient(180deg,#fbfdfb,#eef4ef);
}
.blog-subsection h3,
.blog-step-card h3{
  margin:0;
  font-size:1.3rem;
  line-height:1.12;
}
.blog-compare-card .grid-2{
  gap:0;
  border:1px solid rgba(12,20,15,.08);
  border-radius:22px;
  overflow:hidden;
}
.blog-compare-side{
  display:grid;
  gap:10px;
  padding:20px 22px;
  min-height:100%;
}
.blog-compare-side strong{
  color:var(--primary-dark);
  font-size:.76rem;
  font-weight:800;
  letter-spacing:.12em;
  text-transform:uppercase;
}
.blog-compare-side p,
.blog-subsection p,
.blog-step-card p{
  margin:0;
  color:var(--muted);
  font-size:1.05rem;
  line-height:1.84;
}
.blog-compare-side:first-child{
  background:rgba(239,68,68,.05);
  border-right:1px solid rgba(239,68,68,.14);
}
.blog-compare-side:last-child{
  background:rgba(34,197,94,.06);
}
.blog-compare-side:first-child strong{
  color:#d95b5b;
}
.blog-compare-side:last-child strong{
  color:#1f6640;
}
.blog-compare-side:last-child p{
  color:var(--muted);
}
.blog-step-card .eyebrow{
  margin-bottom:0;
}
.blog-callout{
  padding:28px 30px;
  border-left:4px solid #58df84;
  border-color:rgba(47,138,88,.18);
  background:
    radial-gradient(circle at top right,rgba(47,138,88,.12),transparent 36%),
    linear-gradient(180deg,#ffffff,#eff6f0);
}
.blog-callout-warning{
  border-color:rgba(245,158,11,.24);
  background:
    radial-gradient(circle at top right,rgba(245,158,11,.08),transparent 40%),
    linear-gradient(180deg,rgba(255,247,230,.96),rgba(255,251,241,.96));
}
.blog-callout-label{
  margin:0 0 10px;
  color:#1f6640;
  font-size:.8rem;
  font-weight:800;
  letter-spacing:.14em;
  text-transform:uppercase;
}
.blog-callout-warning .blog-callout-label{
  color:#b36a00;
}
.blog-callout p{
  margin:0;
  color:var(--text);
  font-size:1.12rem;
  line-height:1.82;
}
.blog-quote{
  padding:22px 0;
  background:transparent;
  border:0;
  border-top:2px solid rgba(47,138,88,.45);
  border-bottom:2px solid rgba(47,138,88,.45);
  border-radius:0;
  box-shadow:none;
}
.blog-quote p{
  margin:0;
  color:#153628;
  font-family:"Segoe UI Variable Display","Aptos Display","Segoe UI",sans-serif;
  font-size:clamp(1.4rem,2.5vw,2rem);
  font-weight:760;
  line-height:1.18;
  letter-spacing:-.02em;
  text-align:center;
}
.case-study-systems{
  margin-top:18px;
}
@media (max-width:1180px){
  .brand-badge-grid,.blog-grid{
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
  .nav-submenu-wide{
    min-width:520px;
  }
}
@media (max-width:860px){
  .nav-item-has-children .nav-link::after{
    display:none;
  }
  .nav-submenu{
    position:static;
    min-width:0;
    grid-template-columns:1fr;
    gap:10px;
    padding:4px 0 0 12px;
    border:0;
    border-left:1px solid rgba(235,242,237,.14);
    border-radius:0;
    background:transparent;
    box-shadow:none;
    opacity:1;
    visibility:visible;
    transform:none;
  }
  .nav-submenu a{
    color:rgba(235,242,237,.76);
    padding:10px 12px;
    border-radius:10px;
    background:rgba(255,255,255,.02);
  }
  .nav-submenu a:hover,
  .nav-submenu a:focus-visible,
  .nav-submenu a[aria-current="page"]{
    color:#153628;
    background:rgba(240,248,242,.96);
  }
  .site-nav:not(.is-open) .nav-submenu{
    display:none;
  }
}
@media (max-width:740px){
  html,
  body{
    max-width:100%;
    overflow-x:hidden;
  }
  .brand-badge-grid,.blog-grid{
    grid-template-columns:1fr;
  }
  .footer-grid{
    grid-template-columns:1fr;
    gap:16px;
  }
  .footer-contact-list,
  .footer-links,
  .footer-services,
  .footer-socials{
    gap:6px;
  }
  .footer-shell{
    padding:0 18px;
  }
  .blog-card-meta,
  .blog-article-readout{
    grid-template-columns:1fr;
  }
  .blog-table{
    min-width:640px;
  }
  .social-link{
    width:100%;
  }
  .promo-consent-links{
    gap:8px;
  }
  .promo-consent-links a{
    justify-content:center;
    padding:8px 12px;
    line-height:1.3;
    text-align:center;
    white-space:normal;
  }
  .promo-consent-separator{
    display:none;
  }
}
'''

