from pathlib import Path
import json
from functools import lru_cache
import re
from datetime import date, datetime, time
import shutil
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError

root = Path(__file__).resolve().parent
SOURCE_ASSET_ROOT = root / 'assets'
IMAGE_ROOT = root / 'Images'
PRODUCTION_IMAGE_ROOT = IMAGE_ROOT / 'production'
PRODUCTION_BRAND_ROOT = PRODUCTION_IMAGE_ROOT / 'brand'
PRODUCTION_HOME_ROOT = PRODUCTION_IMAGE_ROOT / 'home'
PRODUCTION_ABOUT_ROOT = PRODUCTION_IMAGE_ROOT / 'about'
PRODUCTION_SERVICE_ROOT = PRODUCTION_IMAGE_ROOT / 'services'
DEPLOY_ROOT = root / 'dist'
DEPLOY_ASSET_ROOT = DEPLOY_ROOT / 'assets'
LEGACY_ROOT_BUILD_DIRS = ('en', 'fr')
LEGACY_ROOT_BUILD_FILES = ('index.html', 'robots.txt', 'sitemap.xml', 'styles.css', 'script.js')
STATIC_ASSET_FILES = ('logo-mark.png', 'opticable-logo.png')
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
    'site.js',
)
SITE_URL = 'https://opticable.ca'
ASSET_VER = '20260317a'
LEGAL_BUSINESS_NAME = '9453-4757 Québec Inc.'
RBQ_LICENSE_LABEL = 'Licence RBQ : 5864-1648-01'
RBQ_LICENSE_NUMBER = '5864-1648-01'
LOGO_LOCKUP_URL = f'/assets/opticable-logo.png?v={ASSET_VER}'
LOGO_UI_URL = f'/assets/logo-ui.webp?v={ASSET_VER}'
LOGO_UI_WHITE_URL = f'/assets/logo-ui-white.webp?v={ASSET_VER}'
LOGO_MARK_URL = f'/assets/logo-mark.png?v={ASSET_VER}'
FAVICON_32_URL = f'/assets/favicon-32.png?v={ASSET_VER}'
APPLE_TOUCH_ICON_URL = f'/assets/apple-touch-icon.png?v={ASSET_VER}'
STYLES_URL = f'/assets/styles.css?v={ASSET_VER}'
SCRIPT_URL = f'/assets/site.js?v={ASSET_VER}'
WEBMANIFEST_URL = '/site.webmanifest'
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
OG_IMAGE_MIME_TYPE = 'image/png'
BLOG_SOCIAL_IMAGE_DIR = DEPLOY_ASSET_ROOT / 'blog-social'
LOGO_LOCKUP_WIDTH = 1600
LOGO_LOCKUP_HEIGHT = 687
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
HOME_IMAGE_EXPORTS = (
    {
        'source': PRODUCTION_BRAND_ROOT / 'logo-ui-source.png',
        'target': DEPLOY_ASSET_ROOT / 'logo-ui.webp',
        'resize': (LOGO_UI_WIDTH, LOGO_UI_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
    {
        'source': PRODUCTION_BRAND_ROOT / 'logo-ui-source-white-text.png',
        'target': DEPLOY_ASSET_ROOT / 'logo-ui-white.webp',
        'resize': (LOGO_UI_WIDTH, LOGO_UI_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
    {
        'source': PRODUCTION_BRAND_ROOT / 'logo-ui-source-white-text.png',
        'target': DEPLOY_ASSET_ROOT / 'og-image.png',
        'resize': (720, 320),
        'canvas': (OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT),
        'background': (13, 23, 18, 255),
        'format': 'PNG',
    },
    {
        'source': PRODUCTION_BRAND_ROOT / 'logo-ui-source-white-text.png',
        'target': DEPLOY_ASSET_ROOT / 'og-image.webp',
        'resize': (720, 320),
        'canvas': (OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT),
        'background': (13, 23, 18, 255),
        'format': 'WEBP',
        'quality': 92,
    },
    {
        'source': SOURCE_ASSET_ROOT / 'logo-mark.png',
        'target': DEPLOY_ASSET_ROOT / 'favicon-32.png',
        'resize': (FAVICON_32_SIZE, FAVICON_32_SIZE),
        'canvas': (FAVICON_32_SIZE, FAVICON_32_SIZE),
        'format': 'PNG',
    },
    {
        'source': SOURCE_ASSET_ROOT / 'logo-mark.png',
        'target': DEPLOY_ASSET_ROOT / 'apple-touch-icon.png',
        'resize': (APPLE_TOUCH_ICON_SIZE, APPLE_TOUCH_ICON_SIZE),
        'canvas': (APPLE_TOUCH_ICON_SIZE, APPLE_TOUCH_ICON_SIZE),
        'format': 'PNG',
    },
    {
        'source': SOURCE_ASSET_ROOT / 'logo-mark.png',
        'target': DEPLOY_ASSET_ROOT / 'favicon-192.png',
        'resize': (FAVICON_192_SIZE, FAVICON_192_SIZE),
        'canvas': (FAVICON_192_SIZE, FAVICON_192_SIZE),
        'format': 'PNG',
    },
    {
        'source': SOURCE_ASSET_ROOT / 'logo-mark.png',
        'target': DEPLOY_ASSET_ROOT / 'favicon-512.png',
        'resize': (FAVICON_512_SIZE, FAVICON_512_SIZE),
        'canvas': (FAVICON_512_SIZE, FAVICON_512_SIZE),
        'format': 'PNG',
    },
    {
        'source': PRODUCTION_HOME_ROOT / 'home-building.png',
        'target': DEPLOY_ASSET_ROOT / 'home-building.webp',
        'resize': (HOME_BUILDING_WIDTH, HOME_BUILDING_HEIGHT),
        'format': 'WEBP',
        'quality': 84,
    },
    {
        'source': PRODUCTION_HOME_ROOT / 'network-rack.png',
        'target': DEPLOY_ASSET_ROOT / 'home-rack.webp',
        'resize': (HOME_RACK_WIDTH, HOME_RACK_HEIGHT),
        'format': 'WEBP',
        'quality': 84,
    },
    {
        'source': PRODUCTION_ABOUT_ROOT / 'about-panel.png',
        'target': DEPLOY_ASSET_ROOT / 'about-panel.webp',
        'resize': (ABOUT_PANEL_WIDTH, ABOUT_PANEL_HEIGHT),
        'format': 'WEBP',
        'quality': 92,
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
        'quality': 90,
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
        'quality': 92,
    },
    {
        'source': PRODUCTION_SERVICE_ROOT / 'access-control.png',
        'target': DEPLOY_ASSET_ROOT / 'service-access.webp',
        'resize': (SERVICE_ACCESS_WIDTH, SERVICE_ACCESS_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
    {
        'source': PRODUCTION_SERVICE_ROOT / 'commercial-wifi.png',
        'target': DEPLOY_ASSET_ROOT / 'service-wifi.webp',
        'resize': (SERVICE_WIFI_WIDTH, SERVICE_WIFI_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
    {
        'source': PRODUCTION_SERVICE_ROOT / 'ip-phone.png',
        'target': DEPLOY_ASSET_ROOT / 'service-voip.webp',
        'resize': (SERVICE_VOIP_WIDTH, SERVICE_VOIP_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
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
        'placeholder': 'Placeholder business contact details are included below and should be replaced with live company information before launch.',
        'form_note': 'Demo form only. Connect this form to your inbox, CRM, or form backend before launch.',
        'success': 'Thanks, {name}. Your request is ready to be connected to a live inbox or CRM workflow.',
        'success_generic': 'Your request is ready to be connected to a live inbox or CRM workflow.',
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
        'contact_intro': 'The contact page is structured for real commercial lead capture. Replace the placeholder business details below and connect the form to your preferred inbox or CRM for production use.',
        'industries_title': 'Industries Served | Commercial Infrastructure by Opticable', 'industries_desc': 'Opticable supports businesses, multi-tenant buildings, property managers, commercial properties, contractors, and developers with low-voltage infrastructure services.',
        'industries_h1': 'Low-voltage infrastructure services for the teams that own, manage, build, and operate commercial spaces.',
        'industries_intro': 'Different client types need different outcomes: tenant turnover, project sequencing, scalable connectivity, clean room design, or better building security. Opticable is positioned around those practical requirements.',
        'faq_title': 'Commercial Infrastructure FAQ | Opticable', 'faq_desc': 'Read answers to common questions about structured cabling, fiber optic installation, security camera systems, access control, intercom, WiFi, and network infrastructure.',
        'faq_h1': 'Answers to common questions about commercial cabling and low-voltage infrastructure work.',
        'faq_intro': 'This FAQ helps buyers understand scope, occupied-site work, planning expectations, and the details that speed up quoting and project coordination.',
        'contact_info_title': 'Contact information', 'form_title': 'Request pricing or a site walk',
        'form_labels': {'name': 'Contact name', 'company': 'Company', 'email': 'Email', 'phone': 'Phone', 'property': 'Property type', 'timeline': 'Timeline', 'services': 'Needed services', 'notes': 'Project notes'},
        'form_options': {'property': ['Select one', 'Business office', 'Multi-tenant building', 'Commercial property', 'Retail or hospitality site', 'Industrial or warehouse site', 'Development or construction project'], 'timeline': ['Select one', 'Immediate need', 'Within 30 days', 'Within 1 to 3 months', 'Budgeting or planning phase']},
        'form_services': ['Structured cabling', 'Fiber optic installation', 'Network infrastructure', 'Security camera systems', 'Access control systems', 'Intercom systems', 'Commercial WiFi', 'IP phone systems'],
        'form_placeholder': 'Describe the property, project scope, devices, or network issues that need to be addressed.',
        'contact_cards': [('General inquiries', 'info@opticable.example'), ('Project requests', 'quotes@opticable.example'), ('Office phone', '+1 (555) 010-0148'), ('Hours', 'Monday to Friday, 8:00 AM to 5:00 PM')],
        'process': [('Site review', 'Review pathways, rooms, risers, devices, and building constraints before work begins.'), ('Scope planning', 'Confirm cable counts, equipment locations, occupied-site constraints, and system integration requirements.'), ('Installation', 'Install, terminate, label, and organize infrastructure with clean work practices and coordinated sequencing.'), ('Turnover', 'Support testing, activation, and handoff so the installed systems stay easier to maintain after go-live.')],
        'clients': [('Businesses', 'Connectivity, security, and communication infrastructure for offices, retail, hospitality, and operational spaces.'), ('Multi-tenant buildings', 'Risers, suites, common areas, and tenant-facing systems in managed or mixed-use properties.'), ('Property managers', 'Repeatable infrastructure standards, building upgrades, and cleaner support across active assets.'), ('Developers and contractors', 'Low-voltage coordination for fit-outs, construction delivery, and project sequencing.')],
    },
    'fr': {
        'lang': 'fr', 'locale': 'fr_CA', 'switch': 'EN', 'skip': 'Aller au contenu', 'menu': 'Menu',
        'home': 'Accueil', 'services': 'Services', 'industries': 'Secteurs', 'about': 'A propos', 'faq': 'FAQ', 'contact': 'Contact',
        'tagline': 'Specialiste des infrastructures basse tension', 'quote': 'Demander une soumission', 'all_services': 'Voir tous les services',
        'company': 'Opticable installe et gere les infrastructures commerciales de cablage, fibre optique, reseau, securite, controle d acces, interphone, WiFi et telephonie IP pour les entreprises et les proprietes gerees.',
        'cta_kicker': 'Demande de projet', 'cta_title': 'Besoin d un entrepreneur basse tension pour une propriete commerciale, un amenagement locatif ou une mise a niveau d infrastructure?', 'cta_copy': 'Utilisez la page contact pour envoyer une demande de soumission bilingue et decrire les services, les quantites d appareils ou les systemes du batiment concernes.',
        'footer': 'Opticable livre des infrastructures basse tension ordonnees pour les entreprises, les immeubles multi-locatifs, les proprietes commerciales, les gestionnaires immobiliers et les promoteurs.',
        'placeholder': 'Les coordonnees ci-dessous sont des exemples et doivent etre remplacees par les coordonnees reelles de l entreprise avant la mise en ligne.',
        'form_note': 'Formulaire de demonstration seulement. Connectez ce formulaire a votre boite courriel, CRM ou service de formulaires avant la mise en ligne.',
        'success': 'Merci, {name}. Votre demande est prete a etre reliee a une boite courriel ou a un CRM en production.',
        'success_generic': 'Votre demande est prete a etre reliee a une boite courriel ou a un CRM en production.',
        'home_title': 'Entrepreneur en infrastructures basse tension pour immeubles commerciaux | Opticable',
        'home_desc': 'Opticable offre le cablage structure, la fibre optique, l infrastructure reseau, les cameras de securite, le controle d acces, l interphone, le WiFi commercial et la telephonie IP pour les clients commerciaux.',
        'home_kicker': 'Reseaux commerciaux et systemes de batiment',
        'home_h1': 'Infrastructures basse tension commerciales pour les systemes de communication des entreprises, des immeubles et des locataires.',
        'home_intro': 'Opticable conçoit, installe et coordonne les systemes physiques derriere la connectivite, la securite, la communication et les operations du batiment. L entreprise s adresse aux entreprises, gestionnaires immobiliers, promoteurs et operateurs commerciaux qui veulent une remise propre et une performance fiable.',
        'home_points': ['Cablage structure, Ethernet, coaxial et fibre optique', 'Baies serveurs, deploiement d infrastructures internet et organisation de salles reseau', 'Systemes de cameras de securite, controle d acces et interphones', 'WiFi commercial, telephonie IP et soutien des lignes VoIP'],
        'home_panel': 'Concu pour les entreprises, les immeubles multi-locatifs, les proprietes commerciales, les gestionnaires immobiliers et les promoteurs.',
        'trust_title': 'Pourquoi les clients commerciaux retiennent Opticable',
        'trust': [('Portee commerciale', 'Le cablage, les appareils, les salles techniques et les systemes du batiment sont planifies comme un seul projet coordonne.'), ('Remise plus propre', 'Le reperage, l organisation des cheminements et le travail en baie sont traites comme des elements de livraison.'), ('Infrastructure facile a soutenir', 'Une installation ordonnee simplifie les ajouts, les mises a niveau et le depannage plus tard.'), ('Presentation bilingue', 'Le contenu en anglais et en francais soutient les equipes mixtes et une meilleure visibilite du site.')],
        'services_title': 'Services commerciaux basse tension | Opticable', 'services_desc': 'Les pages service d Opticable couvrent le cablage structure, la fibre optique, l infrastructure reseau, les cameras de securite, le controle d acces, l interphone, le WiFi commercial et la telephonie IP.',
        'services_h1': 'Des services d infrastructure commerciale concus pour la fiabilite, une livraison ordonnee et un soutien a long terme plus simple.',
        'services_intro': 'Opticable prend en charge la basse tension derriere la connectivite d affaires, la communication du batiment et les systemes relies aux locataires. Chaque page service vise une intention de recherche commerciale precise et explique ou le travail s insere dans un plan d infrastructure plus vaste.',
        'extra_title': 'Capacites additionnelles integrees aux projets',
'extras': [('Installation de cables Ethernet', 'Cablage cuivre pour postes de travail, bornes WiFi, cameras, telephones et appareils d affaires.'), ('Installation de cables coaxiaux', 'Backbone coaxial et liaisons specialisees coordonnes avec le cablage structure et les handoffs fournisseur.'), ('Installation de baies serveurs', 'Implantation des baies, gestion du cablage, raccordement et remise en ordre des salles MDF et IDF.'), ('Deploiement d infrastructures internet', 'Extensions de demarcation, routage des handoffs et soutien de commutation pour les espaces commerciaux neufs ou renoves.'), ('Lignes telephoniques VoIP', 'Connectivite voix et infrastructure des postes alignees sur le cablage structure et le reseau.')],
        'about_title': 'A propos d Opticable | Specialiste des infrastructures commerciales basse tension', 'about_desc': 'Decouvrez comment Opticable accompagne les proprietes commerciales, les gestionnaires immobiliers, les promoteurs et les exploitants avec des services d infrastructure basse tension.',
        'about_h1': 'Un specialiste des infrastructures basse tension axe sur les proprietes commerciales et les environnements immobiliers geres.',
        'about_intro': 'Opticable est positionne comme un entrepreneur qui comprend comment le cablage, les salles reseau, la securite, l acces, l interphone, le sans-fil et les systemes de communication d affaires se rejoignent au niveau du batiment.',
        'about_story': 'Les travaux d infrastructure commerciale sont rarement isoles. Les rotations de locataires, les mises a niveau de securite, les changements reseau et les projets neufs se recoupent souvent. Opticable est presente comme un partenaire capable de coordonner ces systemes avec une livraison technique plus propre.',
        'about_values': [('Positionnement commercial', 'Le site parle directement aux acheteurs commerciaux, exploitants, proprietaires et equipes de projet.'), ('Profondeur basse tension', 'Les pages service expliquent comment les systemes de donnees, securite, communication et acces se rattachent a l infrastructure.'), ('Contenu pratique', 'Les pages mettent l accent sur la portee, les avantages, les cas d usage et les secteurs desservis.'), ('Soutien bilingue', 'Les pages en anglais et en francais appuient l approvisionnement, l exploitation et la coordination de projet.')],
        'contact_title': 'Contacter Opticable | Demande de soumission en infrastructure commerciale', 'contact_desc': 'Contactez Opticable pour discuter d un projet de cablage structure, fibre optique, infrastructure reseau, cameras de securite, controle d acces, interphone, WiFi ou telephonie IP.',
        'contact_h1': 'Parlez a Opticable de votre prochain projet de cablage, de reseau ou de communication du batiment.',
        'contact_intro': 'La page contact est structuree pour de vraies demandes commerciales. Remplacez les coordonnees exemple ci-dessous et reliez le formulaire a votre boite courriel ou a votre CRM avant la mise en ligne.',
        'industries_title': 'Secteurs desservis | Infrastructures commerciales par Opticable', 'industries_desc': 'Opticable accompagne les entreprises, les immeubles multi-locatifs, les gestionnaires immobiliers, les proprietes commerciales, les entrepreneurs et les promoteurs avec des services basse tension.',
        'industries_h1': 'Des services d infrastructures basse tension pour les equipes qui possedent, gerent, construisent et exploitent les espaces commerciaux.',
        'industries_intro': 'Chaque type de client recherche un resultat different : rotation de locataires, sequence de travaux, connectivite evolutive, salles techniques plus propres ou meilleure securite du batiment. Opticable est positionne autour de ces besoins concrets.',
        'faq_title': 'FAQ sur les infrastructures commerciales | Opticable', 'faq_desc': 'Consultez les reponses aux questions frequentes sur le cablage structure, la fibre optique, les cameras de securite, le controle d acces, l interphone, le WiFi et l infrastructure reseau.',
        'faq_h1': 'Reponses aux questions courantes sur le cablage commercial et les travaux d infrastructure basse tension.',
        'faq_intro': 'Cette FAQ aide les acheteurs a comprendre la portee, le travail en site occupe, la planification et les details qui accelerent l estimation et la coordination des projets.',
        'contact_info_title': 'Coordonnees de l entreprise', 'form_title': 'Demander un prix ou une visite de site',
        'form_labels': {'name': 'Nom du contact', 'company': 'Entreprise', 'email': 'Courriel', 'phone': 'Telephone', 'property': 'Type de propriete', 'timeline': 'Echeancier', 'services': 'Services requis', 'notes': 'Notes sur le projet'},
        'form_options': {'property': ['Selectionnez', 'Bureau d entreprise', 'Immeuble multi-locatif', 'Propriete commerciale', 'Site de commerce ou d hotellerie', 'Site industriel ou entrepot', 'Projet de developpement ou de construction'], 'timeline': ['Selectionnez', 'Besoin immediat', 'Dans les 30 jours', 'Dans 1 a 3 mois', 'Phase de budget ou de planification']},
        'form_services': ['Cablage structure', 'Installation de fibre optique', 'Infrastructure reseau', 'Systemes de cameras de securite', 'Systemes de controle d acces', 'Systemes d interphone', 'WiFi commercial', 'Systemes de telephonie IP'],
        'form_placeholder': 'Decrivez la propriete, la portee des travaux, les appareils ou les problemes reseau a corriger.',
        'contact_cards': [('Renseignements generaux', 'info@opticable.example'), ('Demandes de projet', 'soumissions@opticable.example'), ('Telephone du bureau', '+1 (555) 010-0148'), ('Heures', 'Du lundi au vendredi, de 8 h a 17 h')],
        'process': [('Visite du site', 'Analyser les chemins, les salles, les colonnes montantes, les appareils et les contraintes du batiment avant les travaux.'), ('Planification', 'Valider les quantites de cables, l implantation des equipements, les contraintes d occupation et les besoins d integration.'), ('Installation', 'Installer, terminer, reperer et organiser l infrastructure avec des pratiques propres et une bonne coordination.'), ('Remise', 'Soutenir les essais, l activation et la remise afin que les systemes restent plus simples a entretenir apres la mise en service.')],
        'clients': [('Entreprises', 'Infrastructure de connectivite, securite et communication pour bureaux, commerces, hotellerie et espaces operationnels.'), ('Immeubles multi-locatifs', 'Colonnes montantes, suites, aires communes et systemes relies aux locataires dans des proprietes gerees ou mixtes.'), ('Gestionnaires immobiliers', 'Standards repetables, mises a niveau et meilleur soutien sur des actifs occupes.'), ('Promoteurs et entrepreneurs', 'Coordination basse tension pour amenagements, construction et sequence de livraison.')],
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
    'privacy_desc': 'How Opticable handles personal information submitted through the website, the Zoho quote form, and supporting technologies such as cookies and local browser storage.',
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
    'thanks_h1': 'Thank you. Your quote request has been sent.',
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
    'about_h1': 'A commercial technology systems specialist for managed properties and business environments.',
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
    'placeholder': "Coordonnées pour les demandes générales, les soumissions et les visites des lieux.",
    'form_note': "Formulaire de démonstration. Reliez-le à une boîte courriel, à un CRM ou à votre outil de formulaires avant la mise en ligne.",
    'success': "Merci, {name}. Votre demande peut maintenant être acheminée vers une boîte courriel ou un CRM en production.",
    'success_generic': "Votre demande peut maintenant être acheminée vers une boîte courriel ou un CRM en production.",
    'home_title': "Caméras, accès, WiFi et réseau commercial | Opticable",
    'home_desc': "Opticable installe caméras, accès, intercom, WiFi commercial et réseau pour immeubles commerciaux au Québec.",
    'home_kicker': 'Technologie commerciale et systèmes du bâtiment',
    'home_h1': "Caméras, accès, WiFi et réseau pour immeubles commerciaux",
    'home_intro': "Opticable aide les immeubles commerciaux à déployer leurs systèmes de sécurité, de contrôle d'accès, de sans-fil et l'infrastructure qui les soutient, avec une installation soignée et une livraison bien organisée.",
    'home_points': [
        'Caméras de sécurité pour les aires communes, les périmètres, les suites et les zones d’exploitation',
        "Contrôle d'accès et intercoms pour halls, entrées et immeubles gérés",
        'WiFi commercial pour bureaux, commerces et immeubles multilocatifs',
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
    'form_options': {'property': ['Sélectionnez une option', 'Bureau', 'Immeuble multilocatif', 'Multi-logements', 'Condo ou copropriété', 'Immeuble à usage mixte', 'Propriété commerciale', 'Commerce ou hôtellerie', 'Site industriel ou entrepôt', 'Chantier ou site temporaire', 'Projet de développement ou de construction'], 'timeline': ['Sélectionnez une option', 'Besoin immédiat', 'Dans les 30 jours', 'Dans 1 à 3 mois', 'Budget ou planification']},
    'form_services': ['Câblage structuré', 'Fibre optique', 'Infrastructure réseau', 'Caméras de sécurité', "Contrôle d'accès", 'Intercom', 'WiFi commercial', 'Téléphonie IP'],
    'form_placeholder': "Décrivez le type d'immeuble, la portée des travaux, les appareils concernés ou les besoins réseau à prévoir.",
    'contact_cards': [('Renseignements généraux', 'info@opticable.ca'), ('Demandes de soumission', 'soumissions@opticable.ca'), ('Téléphone du bureau', '514-316-7236'), ('Heures', 'Du lundi au vendredi, de 8 h à 17 h; samedi et dimanche, de 10 h à 16 h')],
    'process': [('Évaluation du site', "Nous validons les cheminements, les locaux techniques, les appareils et les contraintes du bâtiment avant le début des travaux."), ('Définition de la portée', "Nous confirmons les quantités, les emplacements, les contraintes d'occupation et les besoins d'intégration."), ('Installation', "Nous installons, terminons, repérons et organisons l'infrastructure selon une séquence propre et coordonnée."), ('Mise en service', "Nous accompagnons les essais, l'activation et la remise pour simplifier le suivi après la livraison.")],
    'industries_title': 'Secteurs desservis | Systèmes technologiques commerciaux | Opticable',
    'industries_desc': "Opticable accompagne les entreprises, immeubles et équipes de projet partout au Québec, notamment à Montréal, Laval, Longueuil, sur la Rive-Sud, la Rive-Nord, dans les Laurentides, Lanaudière, la Montérégie et la ville de Québec.",
    'industries_h1': "Des services d'infrastructure technologique pour les équipes qui possèdent, gèrent, construisent et exploitent les espaces commerciaux.",
    'industries_intro': "Opticable travaille avec les entreprises, les immeubles multilocatifs, les gestionnaires immobiliers et les équipes de développement qui ont besoin d'immeubles sécurisés et bien connectés.",
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
        ('Immeubles multilocatifs', "Colonnes montantes, suites, aires communes, systèmes d'entrée sécurisés et technologies destinées aux locataires."),
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
    'fr': [('Entreprises', "Connectivité, sécurité, WiFi et téléphonie pour bureaux, commerces, hôtellerie et environnements opérationnels."), ('Immeubles multilocatifs', "Colonnes montantes, câblage de suites, systèmes d'entrée, caméras et infrastructures d'aires communes."), ('Propriétés commerciales', "Systèmes technologiques qui soutiennent la location, l'occupation, le service aux locataires et l'exploitation courante."), ('Gestionnaires immobiliers', 'Standards répétables, meilleur soutien et infrastructures plus propres sur des actifs occupés.'), ('Promoteurs et entrepreneurs', "Coordination technologique pour construction neuve, aménagements, planification et livraison de projet."), ('Exploitants industriels et d’entrepôts', "Dorsales, WiFi, caméras, contrôle d'accès et locaux réseau pour de grands sites opérationnels.")],
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
            ("Faites-vous la vente, la gestion, la maintenance, l'installation et le câblage WiFi ?", "Oui. Le service peut inclure la vente d'équipement, le câblage des bornes, l'installation, la planification de couverture, la gestion et la maintenance continue du réseau sans fil."),
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
            ('À quoi servent généralement les câbles cuivre Cat5e et Cat6 ?', "Les câbles cuivre Cat5e et Cat6 servent surtout à relier les postes de travail, téléphones IP, bornes WiFi, caméras, équipements de contrôle d'accès et autres appareils réseau qui ont besoin d'une connexion Ethernet fiable dans l'immeuble."),
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
'fr': {'slug': 'cablage-structure', 'name': 'Cablage structure', 'title': 'Installation de cablage structure pour proprietes commerciales | Opticable', 'desc': 'Installation de cablage structure pour bureaux, immeubles multi-locatifs et proprietes commerciales, incluant Ethernet, coaxial, reperage et cheminements.', 'hero': 'Installation de cablage structure pour bureaux, immeubles et proprietes commerciales.', 'intro': 'Opticable installe la fondation physique derriere la connectivite d affaires, les systemes des locataires et les appareils basse tension. La portee peut inclure l installation de cables Ethernet, le cablage coaxial, l organisation des chemins, les terminaisons et le reperage qui facilitent le soutien futur.', 'summary': 'Cuivre, Ethernet, coaxial, reperage, raccordement et organisation propre du cablage pour les espaces commerciaux.', 'includes': ['Parcours Cat5e, Cat6 et Cat6A pour postes, bornes WiFi, cameras, telephones et appareils d affaires', 'Cablage coaxial pour handoffs internet, distribution specialisee et equipements commerciaux relies', 'Panneaux de raccordement, terminaisons, accessoires de cheminement, reperage, essais et nettoyage des vieux cablages'], 'benefits': ['Infrastructure plus propre et plus facile a servir', 'Depannage plus rapide apres la remise', 'Plus de marge pour les ajouts, deplacements et nouveaux appareils'], 'cases': ['Amenagements locatifs et agrandissements de bureaux', 'Mises a niveau de connectivite pour commerces et hotellerie', 'Nettoyage avant le deploiement du WiFi ou de la securite'], 'industries': ['Bureaux d entreprise', 'Immeubles multi-locatifs', 'Proprietes de commerce et a usage mixte'], 'related': ['network-infrastructure', 'fiber-optic-installation', 'commercial-wifi-installation']},
    },
    'fiber-optic-installation': {
        'en': {'slug': 'fiber-optic-installation', 'name': 'Fiber Optic Installation', 'title': 'Fiber Optic Cable Installation for Commercial Buildings | Opticable', 'desc': 'Fiber optic cable installation for commercial buildings, backbones, risers, internet handoffs, and high-capacity connectivity.', 'hero': 'Fiber optic cabling for backbone capacity, risers, and business-grade connectivity.', 'intro': 'Opticable installs fiber optic cabling for commercial environments that need reliable backbone distribution, ISP handoff extensions, or higher-capacity links between floors, suites, and network rooms.', 'summary': 'Fiber backbones, risers, handoff extensions, and high-capacity links for commercial properties.', 'includes': ['Fiber backbone cabling between MDF, IDF, suites, and major equipment locations', 'Provider handoff extensions and demarc-to-network-room routing', 'Fiber terminations, patching, pathway organization, and rack-side coordination'], 'benefits': ['Higher-capacity distribution for future growth', 'Dependable long-distance links inside larger properties', 'Better coordination with racks, switching, and room design'], 'cases': ['Multi-floor office and mixed-use properties', 'Internet service handoff extensions to network rooms', 'Backbone refreshes during tenant or landlord improvements'], 'industries': ['Commercial office buildings', 'Multi-tenant properties', 'Industrial and warehouse sites'], 'related': ['network-infrastructure', 'structured-cabling', 'security-camera-systems']},
'fr': {'slug': 'installation-fibre-optique', 'name': 'Installation de fibre optique', 'title': 'Fibre optique pour immeubles commerciaux | Opticable', 'desc': 'Installation de fibre optique pour immeubles commerciaux, backbones, colonnes montantes, handoffs internet et connectivite a haute capacite.', 'hero': 'Fibre optique pour backbones, colonnes montantes et connectivite d affaires a haute capacite.', 'intro': 'Opticable installe la fibre optique pour les environnements commerciaux qui exigent un backbone fiable, des extensions de handoff fournisseur ou des liens a plus forte capacite entre etages, suites et salles reseau.', 'summary': 'Backbones fibre, colonnes montantes, extensions de handoff et liens a haute capacite pour proprietes commerciales.', 'includes': ['Cablage backbone fibre entre MDF, IDF, suites et points d equipement', 'Extensions de handoff fournisseur et chemin entre le point de demarcation et la salle reseau', 'Terminaisons fibre, raccordement, organisation des chemins et coordination cote baie'], 'benefits': ['Distribution a plus forte capacite pour la croissance future', 'Liens fiables sur de plus longues distances dans les grands sites', 'Meilleure coordination avec les baies, la commutation et les salles techniques'], 'cases': ['Immeubles de bureaux et proprietes mixtes sur plusieurs etages', 'Extensions du handoff du fournisseur internet vers la salle reseau', 'Renouvellement de backbone lors d ameliorations locatives ou proprietaires'], 'industries': ['Immeubles de bureaux commerciaux', 'Proprietes multi-locatives', 'Sites industriels et entrepots'], 'related': ['network-infrastructure', 'structured-cabling', 'security-camera-systems']},
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
        'fr': {'slug': 'systemes-controle-acces', 'name': 'Systemes de controle d acces', 'title': 'Installation de systemes de controle d acces commerciaux | Opticable', 'desc': 'Installation de systemes commerciaux de controle d acces avec cablage basse tension, soutien des panneaux et planification des entrees pour entreprises et proprietes gerees.', 'hero': 'Installation de systemes de controle d acces pour entrees commerciales, espaces locatifs et immeubles geres.', 'intro': 'Opticable installe l infrastructure basse tension requise pour les systemes commerciaux de controle d acces, incluant les emplacements de lecteurs, le soutien des panneaux, la coordination du materiel de porte et la connectivite reseau pour une exploitation securitaire.', 'summary': 'Cablage de lecteurs, soutien des panneaux, connectivite reseau et infrastructure d entree securisee.', 'includes': ['Cablage basse tension pour lecteurs, materiel electrifie, panneaux et composantes de porte', 'Soutien des cabinets de controle, connectivite reseau et coordination des cheminements', 'Planification de l integration avec les interphones, les cameras et l infrastructure de securite'], 'benefits': ['Coordination d entree plus solide avec l exploitation du batiment', 'Integration multi-systeme plus propre', 'Installations plus faciles a soutenir lors des interventions futures'], 'cases': ['Mises a niveau d entree principale pour bureaux et proprietes mixtes', 'Controle d acces des suites et aires communes', 'Controle des entrees dans les entrepots et zones restreintes'], 'industries': ['Bureaux et proprietes commerciales', 'Immeubles multi-locatifs', 'Installations industrielles'], 'related': ['intercom-systems', 'security-camera-systems', 'network-infrastructure']},
    },
    'intercom-systems': {
        'en': {'slug': 'intercom-systems', 'name': 'Intercom Systems', 'title': 'Commercial Intercom System Installation | Opticable', 'desc': 'Commercial intercom system installation for multi-tenant buildings, office entries, visitor communication, and secure access points.', 'hero': 'Intercom system installation for building entry, visitor communication, and tenant access workflows.', 'intro': 'Opticable installs intercom infrastructure for commercial properties and multi-tenant environments that need clear communication at entry points, gates, lobbies, and controlled access areas.', 'summary': 'Building entry, gate, and tenant communication systems coordinated with access and network infrastructure.', 'includes': ['Lobby, entry, gate, and suite-side intercom cabling and device support', 'Integration planning with access control, cameras, and tenant communication requirements', 'Network and room coordination for intercom controllers or supporting equipment'], 'benefits': ['Clearer visitor communication at entries', 'Better integration with tenant and access workflows', 'Simpler future changes for added suites or entry points'], 'cases': ['Multi-tenant office and mixed-use entry systems', 'Property lobby communication upgrades', 'Gate and controlled-entry intercom additions'], 'industries': ['Multi-tenant commercial buildings', 'Property management portfolios', 'Mixed-use developments'], 'related': ['access-control-systems', 'security-camera-systems', 'structured-cabling']},
        'fr': {'slug': 'systemes-interphone', 'name': 'Systemes d interphone', 'title': 'Installation de systemes d interphone commerciaux | Opticable', 'desc': 'Installation de systemes d interphone commerciaux pour immeubles multi-locatifs, entrees de bureaux, communication des visiteurs et points d acces securises.', 'hero': 'Installation d interphones pour l entree des immeubles, la communication des visiteurs et les parcours d acces des locataires.', 'intro': 'Opticable installe l infrastructure d interphone pour les proprietes commerciales et les environnements multi-locatifs qui exigent une communication claire aux points d entree, aux portails, aux halls et aux zones a acces controle.', 'summary': 'Systemes de communication d entree, de portail et de locataires coordonnes avec l acces et l infrastructure reseau.', 'includes': ['Cablage et soutien d appareils d interphone pour halls, entrees, portails et suites', 'Planification de l integration avec le controle d acces, les cameras et les besoins de communication des locataires', 'Coordination reseau et des salles techniques pour controleurs ou equipements d interphone'], 'benefits': ['Communication visiteur plus claire aux points d entree', 'Meilleure integration avec les parcours des locataires et de l acces', 'Modifications futures simplifiees pour nouvelles suites ou entrees'], 'cases': ['Systemes d entree pour immeubles multi-locatifs et proprietes mixtes', 'Mises a niveau des communications de halls', 'Ajout d interphones a des portails et entrees controlees'], 'industries': ['Immeubles commerciaux multi-locatifs', 'Portefeuilles de gestion immobiliere', 'Developpements mixtes'], 'related': ['access-control-systems', 'security-camera-systems', 'structured-cabling']},
    },
    'commercial-wifi-installation': {
        'en': {'slug': 'commercial-wifi-installation', 'name': 'Commercial WiFi Installation', 'title': 'Commercial WiFi Installation and Access Point Cabling | Opticable', 'desc': 'Commercial WiFi installation including access point cabling, coverage planning, switching support, and wireless infrastructure for business properties.', 'hero': 'Commercial WiFi installation with the cabling and infrastructure wireless networks depend on.', 'intro': 'Opticable helps commercial clients deploy the physical infrastructure behind wireless networks, including access point cabling, mounting support, switching coordination, and coverage planning for active business environments.', 'summary': 'Wireless access point cabling, coverage planning, switching coordination, and infrastructure for business WiFi.', 'includes': ['Cabling for wireless access points in offices, common areas, retail spaces, and larger commercial footprints', 'Coverage-oriented placement coordination tied to building layout and device density', 'Switching, patching, and rack-side support for wireless infrastructure'], 'benefits': ['More dependable wireless coverage', 'Better integration with the network core', 'Room for future device density and added coverage'], 'cases': ['Office WiFi refreshes and tenant expansions', 'Retail guest and staff wireless improvements', 'Wireless rollouts tied to structured cabling or room upgrades'], 'industries': ['Office environments', 'Retail and hospitality', 'Commercial and multi-tenant properties'], 'related': ['structured-cabling', 'network-infrastructure', 'ip-phone-systems']},
'fr': {'slug': 'installation-wifi-commercial', 'name': 'WiFi commercial', 'title': 'Installation de WiFi commercial et cablage de bornes | Opticable', 'desc': 'Installation de WiFi commercial incluant le cablage des bornes, la planification de couverture, le soutien a la commutation et l infrastructure sans fil pour proprietes d affaires.', 'hero': 'Installation de WiFi commercial avec le cablage et l infrastructure dont les reseaux sans fil ont besoin.', 'intro': 'Opticable aide les clients commerciaux a deployer l infrastructure physique derriere les reseaux sans fil, incluant le cablage des bornes WiFi, le soutien au montage, la coordination des commutateurs et la planification de couverture pour des environnements actifs.', 'summary': 'Cablage des bornes, planification de couverture, coordination des commutateurs et infrastructure pour le WiFi d affaires.', 'includes': ['Cablage pour bornes sans fil dans les bureaux, aires communes, commerces et grandes superficies commerciales', 'Coordination des emplacements selon la couverture requise, l amenagement du batiment et la densite des appareils', 'Commutation, raccordement et soutien cote baie pour l infrastructure sans fil'], 'benefits': ['Couverture sans fil plus fiable', 'Meilleure integration au coeur reseau', 'Plus de place pour la densite future et les ajouts de couverture'], 'cases': ['Refresh WiFi de bureaux et expansions de locataires', 'Amelioration de la couverture sans fil pour clients et employes', 'Mises en service sans fil liees au cablage structure ou a des upgrades de salles reseau'], 'industries': ['Environnements de bureaux', 'Commerce et hotellerie', 'Proprietes commerciales et multi-locatives'], 'related': ['structured-cabling', 'network-infrastructure', 'ip-phone-systems']},
    },
    'ip-phone-systems': {
        'en': {'slug': 'ip-phone-systems', 'name': 'IP Phone Systems', 'title': 'IP Phone Systems and VoIP Phone Line Infrastructure | Opticable', 'desc': 'Commercial IP phone system installation and VoIP phone line infrastructure for offices, multi-tenant buildings, and business communication environments.', 'hero': 'IP phone systems and VoIP phone line infrastructure for business communication environments.', 'intro': 'Opticable supports the cabling, device connectivity, and network infrastructure required for commercial IP phone systems and VoIP phone line deployment. Phone infrastructure is planned with structured cabling, switching, and room layouts so it stays easier to support after activation.', 'summary': 'Business phone infrastructure, handset connectivity, VoIP-ready cabling, and network support for office communication.', 'includes': ['Cabling and connectivity for IP handsets, conference phones, and related devices', 'VoIP phone line infrastructure aligned with switching and broader network requirements', 'Phone system changes during office expansions, moves, and room reconfiguration'], 'benefits': ['Dependable phone connectivity', 'Cleaner office deployment for reception, desks, and meeting rooms', 'Simpler future adds, moves, and handset changes'], 'cases': ['Office relocations and workstation reconfiguration', 'Reception and front-desk communication upgrades', 'VoIP migrations requiring updated switching and room organization'], 'industries': ['Business offices', 'Professional services firms', 'Multi-tenant commercial suites'], 'related': ['network-infrastructure', 'structured-cabling', 'commercial-wifi-installation']},
        'fr': {'slug': 'systemes-telephonie-ip', 'name': 'Systemes de telephonie IP', 'title': 'Systemes de telephonie IP et infrastructure de lignes VoIP | Opticable', 'desc': 'Installation commerciale de systemes de telephonie IP et d infrastructure de lignes VoIP pour bureaux, immeubles multi-locatifs et environnements de communication d affaires.', 'hero': 'Systemes de telephonie IP et infrastructure de lignes VoIP pour les environnements de communication d affaires.', 'intro': 'Opticable soutient le cablage, la connectivite des appareils et l infrastructure reseau necessaires a l installation de systemes commerciaux de telephonie IP et de lignes VoIP. La telephonie est planifiee avec le cablage structure, la commutation et l implantation des locaux afin que le systeme reste facile a soutenir.', 'summary': 'Infrastructure de telephonie d affaires, connectivite des postes, cablage pret pour la VoIP et soutien reseau pour la communication des bureaux.', 'includes': ['Cablage et connectivite pour postes IP, telephones de conference et autres appareils de communication', 'Infrastructure de lignes VoIP alignee sur la commutation et les exigences reseau globales', 'Modifications des systemes telephoniques lors d agrandissements, demenagements ou reconfigurations'], 'benefits': ['Connectivite telephonique fiable', 'Deploiement plus propre au bureau pour les receptions et salles de reunion', 'Changements futurs simplifies pour les ajouts et deplacements'], 'cases': ['Relocalisations de bureaux et reconfiguration de postes', 'Modernisation des communications de reception', 'Migrations VoIP avec mise a jour de la commutation et des salles'], 'industries': ['Bureaux d entreprise', 'Firmes de services professionnels', 'Suites commerciales multi-locatives'], 'related': ['network-infrastructure', 'structured-cabling', 'commercial-wifi-installation']},
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
    ('Immeubles multilocatifs', "Systèmes d'entrée, caméras, câblage de suites et infrastructures d'aires communes."),
    ('Immeubles commerciaux', "Systèmes technologiques qui soutiennent l'exploitation, le service aux locataires et l'occupation."),
    ('Gestionnaires immobiliers', 'Standards répétables, mises à niveau et meilleur soutien dans des immeubles occupés.'),
    ('Promoteurs et entrepreneurs', "Coordination technologique pour la sécurité, le sans-fil, le câblage et la livraison des travaux."),
]

services['structured-cabling']['en']['intro'] = 'Opticable installs the physical cabling foundation behind business connectivity, security devices, wireless coverage, and tenant technology systems. Structured cabling scopes can include Ethernet cable installation, coaxial cable installation, pathway organization, terminations, and labeling that makes future support easier.'
services['structured-cabling']['fr'].update({
    'name': 'Câblage structuré',
    'title': 'Installation de câblage structuré pour immeubles commerciaux | Opticable',
    'desc': 'Installation de câblage structuré pour bureaux, immeubles multilocatifs et immeubles commerciaux, incluant fibre optique, Cat 5e, Cat 6, Cat 6e, Ethernet, coaxial, repérage et cheminements.',
    'hero': 'Câblage structuré pour bureaux, immeubles et espaces commerciaux.',
    'intro': "Opticable installe le câblage qui soutient la connectivité d'affaires, les caméras, le WiFi, la téléphonie, la fibre optique et les autres systèmes technologiques d'un immeuble, avec des parcours Cat 5e, Cat 6 et Cat 6e adaptés au projet.",
    'summary': 'Fibre optique, Cat 5e, Cat 6, Cat 6e, Ethernet, coaxial, raccordement et organisation soignée pour les espaces commerciaux.',
    'includes': ["Liens Cat 5e, Cat 6, Cat 6A et Cat 6e pour postes de travail, points d'accès WiFi, caméras, téléphones et équipements d'affaires", 'Câblage coaxial pour services internet, distribution spécialisée et équipements commerciaux', "Panneaux de raccordement, terminaisons, accessoires de cheminement, repérage, essais et remise en ordre de câbles existants"],
    'benefits': ['Infrastructure plus propre et plus simple à entretenir', 'Dépannage plus rapide après la livraison', 'Meilleure marge pour les ajouts, les déménagements et les nouveaux appareils'],
    'cases': ['Aménagements locatifs et agrandissements de bureaux', "Mises à niveau de connectivité dans les commerces et l'hôtellerie", 'Remise en ordre avant un projet de WiFi ou de sécurité'],
    'industries': ['Bureaux', 'Immeubles multilocatifs', 'Immeubles commerciaux et propriétés à usage mixte'],
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
    'industries': ['Commerce et hôtellerie', 'Bureaux et propriétés commerciales', 'Multi-logements, copropriétés et immeubles multilocatifs', 'Sites industriels et entrepôts', 'Chantiers et sites temporaires'],
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
    'industries': ['Bureaux et propriétés commerciales', 'Immeubles multilocatifs', 'Installations industrielles'],
})
services['intercom-systems']['fr'].update({
    'name': 'Intercom',
    'title': "Installation d'intercoms commerciaux | Opticable",
    'desc': "Installation d'intercoms commerciaux pour immeubles multilocatifs, entrées de bureaux et accès contrôlés.",
    'hero': "Intercoms pour entrées d'immeuble, visiteurs et parcours d'accès des locataires.",
    'intro': "Opticable installe l'infrastructure d'intercom pour les immeubles commerciaux et multilocatifs qui ont besoin d'une communication claire aux entrées, aux halls, aux portails et aux zones contrôlées.",
    'summary': "Communication à l'entrée, au portail et au hall, coordonnée avec l'accès et le réseau.",
    'includes': ["Câblage et soutien d'appareils pour halls, entrées, portails et suites", "Planification avec contrôle d'accès, caméras et besoins de communication des occupants", "Coordination réseau et locaux techniques pour contrôleurs et équipements d'intercom"],
    'benefits': ['Communication plus claire avec les visiteurs', "Meilleure intégration avec les parcours d'accès", 'Modifications futures simplifiées pour de nouvelles suites ou de nouvelles entrées'],
    'cases': ["Systèmes d'entrée pour immeubles multilocatifs et propriétés mixtes", 'Mises à niveau des communications de hall', "Ajout d'intercoms à des portails et entrées contrôlées"],
    'industries': ['Immeubles commerciaux multilocatifs', 'Portefeuilles de gestion immobilière', 'Développements mixtes'],
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
    'includes': ["Vente, installation et câblage de points d'accès WiFi pour bureaux, commerces, aires communes, multi-logements, copropriétés, chantiers de construction, usines et espaces événementiels", "Planification de couverture, positionnement des bornes et conception du sans-fil selon l'aménagement, la densité et les usages réels", "Commutateurs, raccordements, soutien au rack et coordination réseau pour l'infrastructure sans fil", "Gestion et maintenance de réseaux WiFi qui doivent rester fiables au quotidien"],
    'benefits': ['Couverture sans fil plus fiable dans plusieurs types de sites et d’espaces partagés', 'Meilleure intégration entre le WiFi, le câblage structuré et le cœur du réseau', "Plus de souplesse pour l'entretien, les changements et l'expansion de la couverture dans le temps"],
    'cases': ['Déploiement ou modernisation du WiFi dans les bureaux et espaces administratifs', 'Amélioration du WiFi pour commerces, hôtellerie et espaces clients', 'WiFi dans les aires communes d’immeubles gérés, multi-logements et copropriétés', 'WiFi pour événements, installations temporaires et besoins ponctuels', 'WiFi pour chantiers de construction et connectivité temporaire de projet', 'Couverture sans fil pour usines, entrepôts et environnements industriels'],
    'industries': ['Bureaux et propriétés commerciales', 'Commerce et hôtellerie', 'Aires communes et espaces partagés', 'Multi-logements, copropriétés et immeubles multilocatifs', 'Chantiers de construction et espaces de projet temporaires', 'Usines, entrepôts et sites industriels', 'Événements et déploiements temporaires'],
})
services['ip-phone-systems']['fr'].update({
    'name': 'Téléphonie IP et lignes',
    'title': 'Téléphonie IP, lignes VoIP et numéros de téléphone | Opticable',
    'desc': "Installation de systèmes de téléphonie IP avec fourniture de lignes VoIP et de numéros de téléphone pour bureaux, immeubles multilocatifs et environnements d'affaires.",
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
    'Multi-logements, copropriétés et immeubles multilocatifs',
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
    'featured_intro': 'A concept built around five services that define the broader Opticable offer for modern business environments.',
    'trust_title': 'Why choose Opticable',
    'trust': [
        ('Technical expertise', 'We plan infrastructure with a practical understanding of connectivity, security, deployment, and long-term support.'),
        ('Tailored solutions', 'Each project is adapted to the site, operational requirements, and growth plans of the client.'),
        ('Installation quality', 'Clean execution, organized cabling, and dependable system turnover remain part of the deliverable.'),
        ('Service and support', 'We stay focused on clear communication, reliable follow-up, and systems that remain easier to manage after install.'),
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
    'about_section_intro': 'A concept built around reliability, practical planning, and a more complete technology partnership.',
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
    'contact_panel_copy': 'Share the site type, your goals, and the systems involved. We can help define the right technical scope for a business-ready deployment.',
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
    'featured_intro': "Cinq services au coeur du concept 01 pour presenter Opticable comme un partenaire technologique plus complet.",
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
    'desc': "Analyse, planification, installation et optimisation de réseaux Wi-Fi professionnels pour bureaux, commerces, entrepôts et immeubles multilocatifs.",
    'hero': 'Un Wi-Fi professionnel pensé pour la performance, la couverture et la sécurité au quotidien.',
    'intro': "Un réseau Wi-Fi performant est essentiel à la productivité des entreprises modernes. Opticable conçoit et déploie des réseaux Wi-Fi professionnels adaptés aux bureaux, commerces, entrepôts, espaces publics et immeubles multilocatifs.",
    'summary': 'Analyse de couverture, installation de bornes, optimisation sans fil et support pour réseaux Wi-Fi professionnels.',
    'includes': [
        'Analyse et planification de la couverture Wi-Fi pour bureaux, commerces, entrepôts et immeubles multilocatifs',
        "Installation de bornes professionnelles avec coordination des switches, du montage et des contrôleurs",
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
        {'key': 'commercial-wifi-installation', 'badge': 'WIFI', 'title': 'Wi-Fi professionnel', 'copy': 'Analyse de couverture, installation de bornes, configuration des controleurs et optimisation pour bureaux, commerces, entrepots et immeubles multi-logements.'},
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
        ('Installation discipline', 'The concept emphasizes cleaner room layouts, sharper detailing, and a stronger final presentation.'),
        ('Operational follow-through', 'The goal is not just installation, but a site that stays easier to support and evolve after go-live.'),
    ],
    'services_h1': 'One partner to connect, structure, and secure your environment.',
    'services_intro': 'Concept 02 presents Opticable through stronger service poles, inspired by enterprise service-group websites while staying focused on business technology infrastructure.',
    'extra_title': 'Operational layers',
    'extra_intro': 'Supporting work that often determines whether a technology environment stays clean, supportable, and scalable.',
    'about_h1': 'A team that connects the field, the infrastructure, and the operation.',
    'about_intro': 'Opticable approaches technology projects as operating environments, not just isolated installations. The objective is to make connectivity, secure entry, visibility, and day-to-day support work together with less friction.',
    'about_story': 'This concept frames Opticable as a commercial technology partner with a more directional visual identity: closer to a specialized group of technical services, but still grounded in practical delivery and approachable client communication.',
    'contact_h1': 'Start the next technology project with a clearer technical direction.',
    'contact_intro': 'Tell us what the site needs to do, what is already in place, and where the friction points are. We can help map the right mix of cabling, wireless, IT, and security layers.',
    'process_title': 'Deployment method',
    'process_intro': 'Analyze the site, shape the technical direction, execute cleanly, then hand off a supportable environment.',
    'clients_intro': 'Professional environments that need stronger technical structure without losing clarity.',
    'division_title': 'Three service poles',
    'division_intro': 'Inspired by service-group websites, the concept groups Opticable into three clearer business-facing capability areas.',
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
        ("Discipline d'installation", "Le concept met l'accent sur des locaux plus propres, un meilleur niveau de détail et une présentation finale plus forte."),
        ('Suivi opérationnel', "L'objectif n'est pas seulement d'installer, mais de livrer un site plus simple à supporter et à faire évoluer après la mise en service."),
    ],
    'services_h1': 'Un seul partenaire pour connecter, structurer et sécuriser votre environnement.',
    'services_intro': "Le concept 02 présente Opticable par pôles d'expertise, inspirés des groupes de services techniques, tout en restant centré sur l'infrastructure technologique pour entreprises.",
    'extra_title': 'Couches de support',
    'extra_intro': "Les travaux de soutien qui déterminent souvent si un environnement technologique reste propre, maintenable et évolutif.",
    'about_h1': "Une équipe qui relie le terrain, l'infrastructure et l'exploitation.",
    'about_intro': "Opticable aborde les projets technologiques comme des environnements d'exploitation, pas comme des installations isolées. Le but est de faire mieux fonctionner la connectivité, les accès, la visibilité et le soutien quotidien.",
    'about_story': "Ce concept positionne Opticable comme un partenaire technologique commercial avec une identité plus directionnelle, plus proche d'un groupe de services spécialisés, mais toujours ancré dans une exécution concrète et une relation client accessible.",
    'contact_h1': 'Lancez votre prochain projet technologique avec une direction plus claire.',
    'contact_intro': "Expliquez ce que le site doit accomplir, ce qui est déjà en place et où se trouvent les points de friction. Nous pouvons structurer le bon mélange de câblage, sans-fil, IT et sécurité.",
    'process_title': 'Méthode de déploiement',
    'process_intro': 'Analyser le site, définir la bonne direction technique, exécuter proprement, puis remettre un environnement plus simple à exploiter.',
    'clients_intro': 'Des environnements professionnels qui ont besoin de plus de structure technique sans perdre en clarté.',
    'division_title': 'Trois pôles de service',
    'division_intro': "Inspiré des sites de groupes de services, le concept regroupe Opticable en trois zones de compétence plus lisibles pour un client d'affaires.",
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
    'top_title': 'Immeubles commerciaux et multilocatifs',
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
    'home_intro': "Opticable conçoit, installe et gère les systèmes technologiques des immeubles commerciaux et multilocatifs au Québec. Un seul partenaire pour la sécurité, l'accès, le WiFi et l'infrastructure réseau, de l'installation au soutien continu.",
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
    'industries_title': 'Clients et types de projets desservis | Opticable',
    'industries_desc': "Opticable installe et gère sécurité, WiFi et câblage pour entreprises, gestionnaires immobiliers et immeubles multilocatifs. Montréal et partout au Québec.",
    'industries_h1': "Les équipes qui gèrent, construisent et exploitent des immeubles commerciaux",
    'industries_intro': "Opticable intervient dans des bâtiments occupés, des chantiers actifs et des immeubles en exploitation. Nos clients sont ceux qui ont besoin que les systèmes fonctionnent, sans mauvaises surprises.",
    'faq_title': 'Questions fréquentes sur nos services | Opticable',
    'faq_desc': "Réponses aux questions sur l'installation et la gestion de caméras, contrôle d'accès, WiFi et câblage pour immeubles commerciaux au Québec.",
    'faq_h1': 'Vous avez des questions sur nos services ou sur un projet ?',
    'faq_intro': "Voici les questions qu'on nous pose le plus souvent. Si vous ne trouvez pas ce que vous cherchez, contactez-nous directement.",
    'faq_panel_title': 'Questions fréquentes',
    'faq_panel_copy': "Réponses utiles sur les soumissions, l'installation, le soutien technique et les systèmes qu'on gère après la mise en service.",
    'clients_title': 'Des solutions adaptées aux réalités du terrain',
    'clients_intro': "Nous intervenons dans des bâtiments occupés, des sites multi-usages et des environnements où la continuité des opérations est essentielle.",
    'clients': [
        ('Entreprises, bureaux et commerces', "Sécurité, WiFi, connectivité et systèmes d'entrée pour des opérations qui doivent rester stables au quotidien."),
        ('Immeubles multilocatifs', "Intercoms, accès, caméras, WiFi et câblage pour les aires communes, les halls et les environnements occupés."),
        ('Immeubles commerciaux à locataires multiples', "Systèmes du bâtiment pensés pour les espaces partagés, les locaux techniques et l'exploitation courante."),
        ('Gestionnaires immobiliers et promoteurs', 'Interlocuteur unique pour les mises à niveau, la standardisation multi-immeubles et la coordination de chantier.'),
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
    'company': 'Opticable designs, installs, and manages technology systems for commercial buildings, with long-term support after commissioning.',
    'footer': 'Opticable installs and manages technology systems for commercial buildings in Montreal, Laval, Longueuil, the South Shore, the North Shore, the Laurentians, and across Quebec.',
    'home_title': 'Commercial Cameras, Access, WiFi and Cabling | Opticable',
    'home_desc': 'Opticable installs and manages cameras, access control, intercom, WiFi, and structured cabling for commercial buildings. Montreal, Laval, Longueuil, and across Quebec.',
    'home_kicker': 'Commercial technology and building systems',
    'home_h1': 'Commercial cabling, access control, WiFi, surveillance, and intercom for better-managed buildings',
    'home_intro': 'Opticable designs, installs, and manages technology systems for commercial and multi-tenant buildings across Quebec. One partner for security, entry, WiFi, intercom, and network infrastructure, from installation through ongoing support.',
    'home_points': [
        'IP cameras for entries, parking areas, and common spaces',
        'Access control and intercom for doors, lobbies, and visitors',
        'Commercial WiFi for offices, retail spaces, and shared areas',
        'Structured cabling, fiber, racks, and network rooms',
    ],
    'focus_chips': ['Installation + support', 'Unified ecosystem', 'Occupied buildings', 'Multi-building portfolios'],
    'featured_title': 'Our services, installation, support, and infrastructure',
    'featured_intro': 'We install, integrate, and manage technology systems for commercial buildings. One partner, from the first cable run through ongoing support.',
    'trust_title': 'Why choose Opticable',
    'home_trust_intro': 'We do not just hand over equipment. We organize systems that are easier to operate, built to last, and easier to expand without starting over.',
    'trust': [
        ('A building-wide view', 'Access control, cameras, WiFi, and the network are planned together from the start, not patched together afterward as separate systems.'),
        ('Clean, durable installations', 'Labeling, racks, finishing, and documentation are handled carefully so the final system is clear and durable.'),
        ('Easier to operate', 'Your team inherits systems that are better organized and easier to maintain, expand, and support over time.'),
    ],
    'services_title': 'Technology services for commercial buildings | Opticable',
    'services_desc': 'Installation and support for cameras, access control, WiFi, intercom, structured cabling, fiber, and network infrastructure for commercial buildings in Quebec.',
    'services_h1': 'Installation and support for building technology systems',
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
    'industries_title': 'Clients and project types we serve | Opticable',
    'industries_desc': 'Opticable installs and manages security, WiFi, and cabling for businesses, property managers, and multi-tenant buildings. Montreal and across Quebec.',
    'industries_h1': 'The teams that manage, build, and operate commercial buildings',
    'industries_intro': 'Opticable works in occupied buildings, active construction sites, and properties already in operation. Our clients are the people who need the systems to work without unpleasant surprises.',
    'faq_title': 'Frequently asked questions about our services | Opticable',
    'faq_desc': 'Answers to common questions about installing and managing cameras, access control, WiFi, intercom, and cabling for commercial buildings in Quebec.',
    'faq_h1': 'Do you have questions about our services or a project?',
    'faq_intro': 'Here are the questions we hear most often. If you do not find what you need, contact us directly.',
    'faq_panel_title': 'Frequently asked questions',
    'faq_panel_copy': 'Useful answers about quotes, installation, technical support, and the systems we manage after commissioning.',
    'clients_title': 'Solutions shaped for real site conditions',
    'clients_intro': 'We work in occupied buildings, mixed-use sites, and environments where continuity of operations matters.',
    'clients': [
        ('Businesses, offices, and retail spaces', 'Security, WiFi, connectivity, and entry systems for operations that need to stay stable every day.'),
        ('Multi-tenant buildings', 'Intercom, access control, cameras, WiFi, and cabling for common spaces, lobbies, and occupied environments.'),
        ('Commercial multi-tenant properties', 'Building systems planned for shared spaces, technical rooms, and day-to-day operations.'),
        ('Property managers and developers', 'One partner for upgrades, multi-building standardization, and site coordination.'),
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
    {'key': 'commercial-wifi-installation', 'badge': 'WIFI', 'title': 'WiFi commercial', 'copy': "Planification de couverture, bornes professionnelles, maintenance et soutien pour bureaux, commerces et espaces partagés."},
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
    'top_alt': 'Commercial property representing coordinated building technology systems',
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
    'intro': 'Opticable designs, installs, and manages professional WiFi networks for commercial and multi-tenant buildings. Stable signal, properly sized coverage, and the wired infrastructure needed behind the access points, without dead zones or overload, with technical support available.',
    'summary': 'Coverage planning, professional access points, maintenance, and support for wireless networks in commercial buildings.',
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
    'intro': 'Opticable installs the structured cabling that supports your security, wireless, network, and communication systems. A clean, well-organized, documented installation that makes maintenance and future additions easier.',
    'summary': 'Cat 5e, Cat 6, Cat 6A, coaxial, patch panels, testing, and documentation for a clean, durable network foundation.',
    'related': ['fiber-optic-installation', 'network-infrastructure', 'commercial-wifi-installation'],
})
services['fiber-optic-installation']['en'].update({
    'name': 'Fiber optic',
    'title': 'Fiber optic installation for commercial buildings | Opticable',
    'desc': 'Fiber optic links, risers, and service extensions for commercial buildings. Montreal, Laval, Longueuil, and across Quebec.',
    'hero': 'Fiber optic installation for commercial buildings and multi-storey sites',
    'intro': 'Opticable installs fiber optic links that serve as the backbone of your network infrastructure. Risers between floors, service extensions, and high-capacity links for buildings where copper is no longer enough.',
    'summary': 'Backbone links, risers, service extensions, and high-capacity fiber runs for commercial buildings.',
    'related': ['structured-cabling', 'network-infrastructure', 'security-camera-systems'],
})
services['network-infrastructure']['en'].update({
    'name': 'Network infrastructure',
    'title': 'Network infrastructure for commercial buildings | Opticable',
    'desc': 'Installation of racks, patch panels, and technical rooms for commercial buildings. Montreal, Laval, Longueuil, and across Quebec.',
    'hero': 'Network infrastructure for commercial buildings, including racks, technical rooms, and internet-entry organization',
    'intro': 'Opticable installs and organizes the network infrastructure of commercial buildings: racks, patch panels, internet-entry management, and cleanup of existing technical rooms. Well-structured infrastructure is what keeps your systems reliable and easier to maintain.',
    'summary': 'Racks, patch panels, technical rooms, internet-entry management, and network support for environments that are easier to operate.',
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
    'intro': "Opticable installe et gère des systèmes de caméras IP adaptés aux immeubles commerciaux, multilocatifs et aux environnements d'affaires. Chaque projet est planifié selon vos zones sensibles, vos accès et les exigences de votre exploitation, avec un soutien continu après la mise en service.",
    'summary': 'Caméras IP, PoE, NVR, visionnement à distance et soutien continu pour protéger les zones sensibles, aires communes, périmètres et accès.',
    'related': ['access-control-systems', 'intercom-systems', 'structured-cabling'],
})
services['access-control-systems']['fr'].update({
    'name': "Contrôle d'accès",
    'title': "Contrôle d'accès pour immeubles commerciaux | Opticable",
    'desc': "Installation et gestion de contrôle d'accès, lecteurs, panneaux et câblage de portes pour immeubles commerciaux. Montréal, Laval et partout au Québec.",
    'hero': "Contrôle d'accès pour immeubles, halls d'entrée et espaces sécurisés",
    'intro': "Opticable installe et gère des systèmes de contrôle d'accès pour les immeubles commerciaux, multilocatifs et les environnements d'affaires. Lecteurs, panneaux de contrôle, serrures électroniques et câblage de portes sont planifiés, installés et soutenus pour des accès fiables et durables.",
    'summary': "Lecteurs, serrures, panneaux, câblage de portes et administration continue des accès pour halls, entrées et zones restreintes.",
    'related': ['intercom-systems', 'security-camera-systems', 'structured-cabling'],
})
services['commercial-wifi-installation']['fr'].update({
    'name': 'WiFi commercial',
    'title': 'Installation WiFi commercial pour bureaux et immeubles | Opticable',
    'desc': 'Conception, installation, gestion et maintenance de WiFi commercial pour bureaux et immeubles. Montréal, Laval, Longueuil et partout au Québec.',
    'hero': 'WiFi commercial pour bureaux, immeubles et espaces partagés',
    'intro': "Opticable conçoit, installe et assure la gestion des réseaux WiFi professionnels pour les immeubles commerciaux et multilocatifs. Signal stable, couverture bien dimensionnée et infrastructure câblée qui supporte les bornes, sans angle mort, sans surcharge, avec un soutien technique disponible.",
    'summary': 'Planification de couverture, bornes d’accès professionnelles, maintenance et soutien pour les réseaux sans fil des immeubles commerciaux.',
    'related': ['structured-cabling', 'network-infrastructure', 'access-control-systems'],
})
services['intercom-systems']['fr'].update({
    'name': 'Intercom',
    'title': "Systèmes d'intercom pour immeubles commerciaux | Opticable",
    'desc': "Installation d'intercoms audio et vidéo pour halls, portails et immeubles commerciaux. Montréal, Laval, Longueuil et partout au Québec.",
    'hero': "Systèmes d'intercom pour halls, portails et immeubles occupés",
    'intro': "Opticable installe des systèmes d'intercom audio et vidéo pour les halls d'entrée, les portails et les accès visiteurs des immeubles commerciaux et multilocatifs. Coordonnés avec le contrôle d'accès, les caméras et le réseau, pour une communication d'entrée fiable, bien intégrée et facile à gérer.",
    'summary': "Intercom audio ou vidéo pour halls, portails et accès visiteurs, avec intégration au contrôle d'accès et au réseau.",
    'related': ['access-control-systems', 'security-camera-systems', 'network-infrastructure'],
})
services['structured-cabling']['fr'].update({
    'name': 'Câblage structuré',
    'title': 'Câblage structuré pour immeubles commerciaux | Opticable',
    'desc': 'Installation de câblage structuré Cat 6, Cat 6A, coaxial et fibre optique pour immeubles commerciaux. Montréal, Laval, Longueuil et partout au Québec.',
    'hero': "Câblage structuré pour immeubles commerciaux et environnements d'affaires",
    'intro': "Opticable installe le câblage structuré qui supporte vos systèmes de sécurité, de sans-fil, de réseau et de communication. Une installation propre, bien organisée et documentée, qui simplifie l'entretien et les ajouts futurs.",
    'summary': 'Cat 5e, Cat 6, Cat 6A, coaxial, patch panels, tests et documentation pour une base réseau propre et durable.',
    'related': ['fiber-optic-installation', 'network-infrastructure', 'commercial-wifi-installation'],
})
services['fiber-optic-installation']['fr'].update({
    'name': 'Fibre optique',
    'title': 'Fibre optique pour immeubles commerciaux | Opticable',
    'desc': 'Liaisons fibre optique, colonnes montantes et prolongements de service pour immeubles commerciaux. Montréal, Laval, Longueuil et partout au Québec.',
    'hero': 'Installation de fibre optique pour immeubles commerciaux et sites multi-étages',
    'intro': "Opticable installe les liaisons en fibre optique qui servent de colonne vertébrale à votre infrastructure réseau. Backbone entre étages, prolongements de service et liaisons haute capacité, pour les bâtiments où le cuivre ne suffit plus.",
    'summary': 'Backbone, colonnes montantes, prolongements de service et liaisons haute capacité pour immeubles commerciaux.',
    'related': ['structured-cabling', 'network-infrastructure', 'security-camera-systems'],
})
services['network-infrastructure']['fr'].update({
    'name': 'Infrastructure réseau',
    'title': 'Infrastructure réseau pour immeubles commerciaux | Opticable',
    'desc': 'Installation de racks, patch panels et locaux techniques pour immeubles commerciaux. Montréal, Laval, Longueuil et partout au Québec.',
    'hero': 'Infrastructure réseau pour immeubles commerciaux — racks, locaux techniques et organisation des arrivées',
    'intro': "Opticable installe et organise l'infrastructure réseau des immeubles commerciaux: racks, patch panels, gestion des arrivées Internet et remise en ordre des locaux techniques existants. Une infrastructure bien structurée, c'est ce qui rend vos systèmes fiables et plus faciles à maintenir.",
    'summary': 'Racks, patch panels, locaux techniques, gestion des arrivées Internet et soutien réseau pour des environnements plus simples à exploiter.',
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
        ('Avec quels types de bâtiments travaillez-vous ?', "Immeubles commerciaux, multilocatifs, bureaux, commerces, hôtels et sites en construction. Si vous n'êtes pas sûr, décrivez-nous votre projet et on vous dira franchement si on peut vous aider."),
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
        ("Combien de temps dure une installation typique ?", "Ça dépend du projet. Une installation de caméras dans un commerce peut se faire en une journée. Un projet complet dans un immeuble multilocatif peut s'étaler sur plusieurs jours ou plusieurs semaines. L'échéancier est établi dans la soumission."),
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
        'title': 'Immeubles multilocatifs et résidences à accès contrôlé',
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
        'title': 'Promoteurs et entrepreneurs généraux en construction',
        'copy': "Vous construisez ou rénovez un bâtiment et avez besoin que les systèmes technologiques soient coordonnés avec les autres corps de métier, sans retard.",
        'items': ['Coordination avec les électriciens et autres corps de métier', 'Câblage structuré selon les phases de construction', "Caméras, contrôle d'accès et intercom livrés à temps", 'Documentation complète à la livraison'],
    },
]

FR_CLIENTELE_CTA = {
    'title': "Votre type de projet n'est pas listé ici ?",
    'copy': "On intervient aussi en hôtellerie, institutionnel et sites industriels. Décrivez-nous votre bâtiment.",
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
            {'eyebrow': 'Bâtiments', 'title': 'Pour quels types de bâtiments', 'items': ['Immeubles de bureaux et tours commerciales', 'Immeubles multilocatifs et résidences à accès contrôlé', 'Commerces, boutiques et espaces de vente', 'Entrepôts et sites industriels', 'Hôtels et hébergements commerciaux']},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ['01 — Évaluation des zones: entrées, angles morts, zones à risque et contraintes d’installation.', '02 — Proposition adaptée: nombre de caméras, matériel, résolution, stockage et câblage détaillés dans la soumission.', '03 — Installation coordonnée: câblage structuré, fixation propre, configuration NVR et test de chaque caméra.', '04 — Remise et soutien: système documenté, formation de base et disponibilité pour la gestion continue.']},
        ],
        'cta': "Vous planifiez un projet de caméras ? Décrivez-nous votre immeuble et vos zones à couvrir. Nous vous reviendrons avec une proposition claire.",
    },
    'access-control-systems': {
        'sections': [
            {'eyebrow': 'Contrôle d’accès', 'title': "Ce qu'on installe et gère", 'items': ["Lecteurs d'accès par carte, badge, code ou biométrie selon le niveau de sécurité", 'Panneaux de contrôle avec gestion centralisée des portes et des utilisateurs', 'Serrures, gâches électriques, aimants et mécanismes adaptés à chaque porte', 'Câblage de portes, boîtiers et raccordements propres dans les cadres et cloisons', 'Gestion multi-portes à partir d’une seule interface', 'Soutien, administration, mises à jour et support technique continu']},
            {'eyebrow': 'Écosystème unifié', 'title': "Écosystème unifié — accès, caméras et intercom", 'paragraphs': ["Le contrôle d'accès peut être intégré aux caméras et à l'intercom au sein d'une seule plateforme de gestion. Une porte bien sécurisée, c'est un lecteur, une caméra et un intercom qui fonctionnent ensemble, pas trois systèmes indépendants gérés séparément."]},
            {'eyebrow': 'Espaces', 'title': "Pour quels types d'espaces", 'items': ["Halls d'entrée principaux et accès visiteurs", 'Entrées de stationnement et accès souterrains', 'Salles de serveurs, locaux techniques et zones restreintes', "Bureaux à accès limité et salles sécurisées", 'Accès locataires dans les immeubles multilocatifs']},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ['01 — Analyse des accès: portes, zones, niveaux d’accès et contraintes mécaniques.', '02 — Proposition structurée: matériel, câblage, logiciel de gestion et coûts détaillés.', '03 — Installation rigoureuse: câblage propre dans les cadres et murs, lecteurs bien fixés et tests complets.', '04 — Mise en service et formation: configuration des accès, documentation remise et soutien continu.']},
        ],
        'cta': "Vous voulez sécuriser vos accès ? Dites-nous combien de portes, le type d'immeuble et vos contraintes. On s'en occupe.",
    },
    'commercial-wifi-installation': {
        'sections': [
            {'eyebrow': 'WiFi commercial', 'title': "Ce qu'on installe et gère", 'items': ["Bornes d'accès WiFi professionnelles alimentées en PoE", 'Câblage de soutien Cat 6 ou Cat 6A depuis le local réseau', 'Planification de couverture selon murs, matériaux, zones d’usage et bande passante', 'Gestion et maintenance: surveillance, mises à jour et ajout de couverture', 'Services informatiques réseau et administration du sans-fil', 'Soutien après installation pour les ajustements, incidents et besoins d’évolution']},
            {'eyebrow': 'Infrastructure', 'title': "Un WiFi bien installé, c'est d'abord un bon câblage", 'paragraphs': ["La majorité des problèmes de WiFi viennent de l'infrastructure câblée derrière les bornes. On s'occupe des deux — câblage structuré et WiFi — pour un résultat stable sur le long terme."]},
            {'eyebrow': 'Espaces', 'title': "Pour quels types d'espaces", 'items': ['Bureaux à aire ouverte et espaces de travail partagés', 'Immeubles multilocatifs — aires communes et couloirs', 'Commerces, restaurants et espaces clients', 'Chantiers de construction actifs', 'Salles de conférence et espaces événementiels', 'Entrepôts et sites industriels']},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ['01 — Analyse du site: superficie, matériaux, nombre d’utilisateurs et usages prévus.', '02 — Plan de couverture: emplacement des bornes, matériel recommandé et câblage nécessaire.', '03 — Installation et câblage: tirage des câbles, fixation des bornes, configuration réseau et tests de signal.', '04 — Validation, remise et soutien: couverture vérifiée, configuration documentée et gestion continue disponible.']},
        ],
        'cta': "Vous avez des zones sans signal ou un réseau qui ne suffit plus ? Décrivez-nous votre espace et vos besoins.",
    },
    'intercom-systems': {
        'sections': [
            {'eyebrow': 'Intercom', 'title': "Ce qu'on installe", 'items': ['Intercom audio pour la communication entre l’entrée et un poste intérieur ou un téléphone', 'Intercom vidéo avec caméra intégrée pour identifier les visiteurs avant d’ouvrir', 'Postes muraux et bornes d’entrée robustes pour halls, réceptions et portails', "Intégration au contrôle d'accès pour déverrouiller depuis un poste intérieur ou un appareil mobile"]},
            {'eyebrow': 'Écosystème unifié', 'title': 'Écosystème unifié — intercom, accès et caméras', 'paragraphs': ["L'intercom, le contrôle d'accès et les caméras peuvent fonctionner au sein d'un même écosystème — une seule plateforme pour identifier un visiteur, contrôler l'accès et surveiller l'entrée. On les installe ensemble, de façon coordonnée, pour une gestion simplifiée."]},
            {'eyebrow': 'Immeubles', 'title': "Pour quels types d'immeubles", 'items': ['Immeubles multilocatifs avec entrée sécurisée', "Immeubles de bureaux avec réception ou accès visiteurs", 'Commerces avec zones de livraison ou accès restreint', 'Stationnements couverts et accès souterrains', "Portails extérieurs et cours d'immeuble"]},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ["01 — Analyse de l'entrée: type de porte, flux de visiteurs, contraintes mécaniques et infrastructure existante.", '02 — Recommandation claire: audio ou vidéo, intégration au contrôle d’accès et nombre de postes.', '03 — Installation propre: câblage encastré, borne fixée solidement, configuration et tests complets.', '04 — Mise en service: fonctionnement validé et intégration aux autres systèmes confirmée.']},
        ],
        'cta': "Vous cherchez un système d'intercom pour votre entrée ou votre portail ? Parlez-nous de votre immeuble.",
    },
    'structured-cabling': {
        'sections': [
            {'eyebrow': 'Câblage structuré', 'title': "Ce qu'on installe", 'items': ['Câblage cuivre Cat 5e, Cat 6 et Cat 6A pour postes, bornes WiFi, caméras IP, lecteurs et équipements réseau', 'Câblage coaxial pour caméras analogiques, antennes et distributions de signal existantes', 'Fibre optique sur courte distance pour relier locaux réseau, étages ou zones éloignées', 'Patch panels pour des arrivées de câbles organisées, identifiées et évolutives']},
            {'eyebrow': 'Usage concret', 'title': 'Ce que ça supporte concrètement', 'items': ['Bornes WiFi alimentées en PoE via Cat 6', 'Caméras IP raccordées à l’enregistreur NVR', "Lecteurs de contrôle d'accès câblés au panneau de contrôle", 'Postes de téléphonie IP et équipements de bureau', 'Équipements réseau dans le local technique']},
            {'eyebrow': 'Qualité', 'title': "Une installation propre, ça veut dire quoi ?", 'paragraphs': ["Câbles identifiés aux deux extrémités, cheminements bien fixés, patch panels organisés et local réseau que n'importe quel technicien peut comprendre sans tout redécouvrir."]},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ['01 — Relevé du site: zones à câbler, cheminements possibles et contraintes du bâtiment.', '02 — Plan de câblage: nombre de points, longueurs, type de câble et organisation du local réseau.', '03 — Installation structurée: tirage, connexion aux patch panels et identification complète de chaque point.', '04 — Test et certification: chaque point est testé et la documentation des points est remise.']},
        ],
        'cta': "Vous avez un projet de câblage ou un réseau à organiser ? Dites-nous la superficie, le nombre de points et le type de bâtiment.",
    },
    'fiber-optic-installation': {
        'sections': [
            {'eyebrow': 'Fibre optique', 'title': "Ce qu'on installe", 'items': ['Colonnes montantes et backbone vertical entre les locaux réseau de chaque étage', 'Liaisons longue portée entre bâtiments, ailes ou locaux techniques distants', 'Prolongements de service vers une nouvelle zone, un nouvel étage ou un nouvel équipement', 'Fibre monomode ou multimode selon la distance et la bande passante', 'Raccordements, connecteurs LC, SC ou MPO et organisation dans les boîtiers']},
            {'eyebrow': 'Usage', 'title': 'Quand la fibre est nécessaire', 'items': ['Bâtiments de plusieurs étages avec un local réseau par niveau', 'Distances supérieures à 90 mètres entre équipements', 'Liaisons entre bâtiments sur un même site', 'Besoins de bande passante élevée pour caméras et réseau principal', 'Infrastructure existante à prolonger ou remplacer']},
            {'eyebrow': 'Coordination', 'title': 'Coordonné avec le câblage structuré', 'paragraphs': ['La fibre constitue le backbone — le cuivre prend le relais pour les derniers mètres. On installe les deux en coordination pour une infrastructure cohérente du local technique jusqu’au point final.']},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ["01 — Analyse de l'infrastructure: points à relier, distances, cheminements et équipements aux deux extrémités.", '02 — Recommandation technique: type de fibre, nombre de brins et type de connecteurs.', '03 — Installation et soudure: passage de la fibre dans les cheminements existants ou nouveaux et connexion des extrémités.', '04 — Test et certification: chaque liaison est testée en atténuation et documentée.']},
        ],
        'cta': "Vous avez besoin d'une liaison fibre entre étages ou entre bâtiments ? Décrivez-nous le projet.",
    },
    'network-infrastructure': {
        'sections': [
            {'eyebrow': 'Infrastructure réseau', 'title': "Ce qu'on installe et organise", 'items': ['Racks et armoires ouverts ou fermés selon les équipements et les besoins d’accès', 'Patch panels pour organiser les arrivées de câbles avec une identification claire', 'Gestion verticale et horizontale des câbles pour des racks lisibles et évolutifs', 'Routage propre des arrivées Internet Bell, Vidéotron, Rogers ou autres', "Remise en ordre de l'existant pour rendre un local technique plus fonctionnel sans tout reconstruire"]},
            {'eyebrow': 'Valeur', 'title': 'Pourquoi un local réseau bien organisé, ça compte', 'paragraphs': ['Un local chaotique coûte du temps à chaque intervention et rend les modifications risquées. Un local bien structuré est moins cher à entretenir sur le long terme et beaucoup plus simple à faire évoluer.']},
            {'eyebrow': 'Déroulement', 'title': 'Comment ça se passe', 'items': ['01 — Évaluation du local: espace disponible, équipements en place, arrivées existantes et besoins futurs.', '02 — Plan d’organisation: disposition des racks, patch panels, gestion des arrivées et documentation avant les travaux.', '03 — Installation ou réorganisation: montage des racks, câblage des panneaux et identification complète.', '04 — Documentation remise: relevé des ports, équipements, arrivées et cheminements.']},
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
        'copy': 'You are building or renovating a property and need the technology systems coordinated with the other trades, without delays.',
        'items': ['Coordination with electricians and other trades', 'Structured cabling aligned with construction phases', 'Cameras, access control, and intercom delivered on schedule', 'Complete documentation at handoff'],
    },
]

EN_CLIENTELE_CTA = {
    'title': 'Do you have a project type that is not listed here?',
    'copy': 'We also work in hospitality, institutional environments, and industrial sites. Tell us about your building.',
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
            {'eyebrow': 'Unified ecosystem', 'title': 'Unified ecosystem for cameras, intercom, and access control', 'paragraphs': ['Your cameras can belong to the same ecosystem as the intercom and access control system, with one management platform to monitor, manage entry, and communicate at the door. One partner, one coherent installation.']},
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
            {'eyebrow': 'Commercial WiFi', 'title': 'What we install and manage', 'items': ['Professional WiFi access points powered by PoE', 'Cat 6 or Cat 6A support cabling from the network room', 'Coverage planning based on walls, materials, usage zones, and bandwidth needs', 'Management and maintenance: monitoring, updates, and coverage expansion', 'Network IT services and wireless administration', 'Post-installation support for adjustments, incidents, and future changes']},
            {'eyebrow': 'Infrastructure', 'title': 'Good WiFi starts with good cabling', 'paragraphs': ['Most WiFi problems come from the wired infrastructure behind the access points. We handle both the structured cabling and the WiFi layer so the result stays stable over time.']},
            {'eyebrow': 'Spaces', 'title': 'Where it fits', 'items': ['Open offices and shared workspaces', 'Multi-tenant buildings with common areas and corridors', 'Retail spaces, restaurants, and customer-facing areas', 'Active construction sites', 'Conference rooms and event spaces', 'Warehouses and industrial sites']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Site analysis: square footage, materials, expected users, and actual usage.', '02 - Coverage plan: access-point locations, recommended hardware, and required cabling.', '03 - Installation and cabling: cable pulls, access-point mounting, network configuration, and signal testing.', '04 - Validation, handoff, and support: verified coverage, documented configuration, and ongoing management if needed.']},
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
            {'eyebrow': 'Quality', 'title': 'What a clean installation actually means', 'paragraphs': ['Cables labeled at both ends, pathways secured properly, organized patch panels, and a network room that any technician can understand without rediscovering everything from scratch.']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Site survey: areas to cable, available pathways, and building constraints.', '02 - Cabling plan: number of points, run lengths, cable type, and network-room organization.', '03 - Structured installation: cable pulling, patch-panel termination, and full identification of every point.', '04 - Testing and certification: every point is tested and the point list is handed over.']},
        ],
        'cta': 'Do you have a cabling project or a network room that needs to be organized? Tell us the square footage, point count, and building type.',
    },
    'fiber-optic-installation': {
        'sections': [
            {'eyebrow': 'Fiber optic', 'title': 'What we install', 'items': ['Risers and vertical backbones between the network rooms on each floor', 'Long-distance links between buildings, wings, or remote technical rooms', 'Service extensions to a new area, a new floor, or new equipment', 'Single-mode or multi-mode fiber depending on distance and bandwidth needs', 'Terminations, LC, SC, or MPO connectors, and organized fiber enclosures']},
            {'eyebrow': 'Use cases', 'title': 'When fiber is needed', 'items': ['Multi-storey buildings with one network room per level', 'Runs longer than 90 meters between equipment', 'Links between buildings on the same property', 'High-bandwidth needs for cameras and the core network', 'Existing infrastructure that needs to be extended or replaced']},
            {'eyebrow': 'Coordination', 'title': 'Coordinated with structured cabling', 'paragraphs': ['Fiber acts as the backbone and copper takes over for the last meters. We install both in coordination so the infrastructure stays coherent from the technical room all the way to the final device.']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Infrastructure review: points to connect, distances, pathways, and equipment at both ends.', '02 - Technical recommendation: fiber type, strand count, and connector type.', '03 - Installation and splicing: fiber run through existing or new pathways and clean termination at both ends.', '04 - Testing and certification: every link is attenuation-tested and documented.']},
        ],
        'cta': 'Do you need a fiber link between floors or between buildings? Describe the project and we will point you in the right direction.',
    },
    'network-infrastructure': {
        'sections': [
            {'eyebrow': 'Network infrastructure', 'title': 'What we install and organize', 'items': ['Open or closed racks and cabinets based on the equipment and service-access needs', 'Patch panels that keep incoming cabling organized and clearly labeled', 'Vertical and horizontal cable management for racks that stay readable and expandable', 'Clean routing of Bell, Videotron, Rogers, or other internet entries', 'Cleanup of existing technical rooms to make them more functional without rebuilding everything']},
            {'eyebrow': 'Value', 'title': 'Why an organized network room matters', 'paragraphs': ['A chaotic room costs time every time someone intervenes and makes changes risky. A well-structured room costs less to maintain over time and is much easier to expand.']},
            {'eyebrow': 'Process', 'title': 'How the work is handled', 'items': ['01 - Room review: available space, installed equipment, existing internet entries, and future needs.', '02 - Organization plan: rack layout, patch panels, internet-entry routing, and documentation before the work starts.', '03 - Installation or reorganization: rack assembly, panel cabling, and full identification.', '04 - Documentation handoff: port maps, equipment list, internet entries, and pathways.']},
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
        'title': 'Blog — Commercial technology and building systems | Opticable',
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
    'title': 'Blog — Commercial technology and building systems | Opticable',
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
            'title': 'Why Turning Up WiFi Power Usually Makes Things Worse | Opticable',
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
            'title': 'Pourquoi monter la puissance du WiFi empire les choses | Opticable',
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
            'title': 'IP Cameras: Why Your Surveillance Network Needs an Upgrade | Opticable',
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
                        'Opticable installs IP camera systems the same way we deploy network infrastructure: methodically, with validation, and with a focus on making the finished system supportable after go-live.',
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
            'title': 'Caméras IP : pourquoi votre réseau de surveillance mérite une mise à niveau | Opticable',
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
                'case-office-building': 'Office building with MikroTik routing, Omada WiFi and switching, and a UniFi management stack for cameras and access.',
                'case-multitenant-building': 'Multi-tenant residential property with UniFi Access, UniFi cameras, and Omada WiFi in common areas.',
                'case-retail-space': 'Retail space with a unified UniFi security platform, Omada WiFi, and MikroTik routing.',
                'case-construction-site': 'Construction project coordinated in phases around MikroTik routing, Omada switching, and a unified UniFi security stack.',
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
                'work': ['Installation of UniFi Access on four doors with badge readers and centralized management', 'Deployment of eight TP-Link Omada access points with Omada switching and dedicated Cat 6 cabling', 'Installation of 12 UniFi cameras with remote viewing and management from the same platform as access control', 'MikroTik router deployment and full cleanup of the network room with rack, patch panels, and identification of all points', 'Installation of 25 new network drops for workstations'],
                'result': 'The building is fully cabled, secured, and connected through a single operational stack. The property manager supervises cameras and access from one management platform, and the network room is documented and organized.',
                'systems': 'MikroTik (routeur) · TP-Link Omada (WiFi et commutateurs) · UniFi Cameras · UniFi Access',
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
                'work': ['Installation of a UniFi Access video intercom at the main entry with centralized access-control integration', 'Installation of 10 UniFi cameras in corridors, entries, and parking areas', 'Deployment of TP-Link Omada access points and Omada switches in corridors and common areas', 'MikroTik router deployment, Cat 6 cabling in shared areas, and organization of the network room'],
                'result': 'The property manager controls entry remotely, reviews cameras from a phone, and manages the intercom and access rights from the same UniFi platform. Residents benefit from WiFi coverage in shared spaces.',
                'systems': 'MikroTik (routeur) · TP-Link Omada (WiFi et commutateurs) · UniFi Cameras · UniFi Access',
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
                'work': ['Installation of eight UniFi cameras covering the sales floor, cash area, warehouse, and parking', 'Replacement of the WiFi with three TP-Link Omada access points and Omada switches, with separate SSIDs for customers and payment terminals', 'Installation of a UniFi Access reader on the warehouse door', 'MikroTik router deployment and remote viewing setup on the owner’s mobile phone'],
                'result': 'The owner supervises the store remotely, the WiFi remains stable for operations, and the warehouse stays restricted to authorized staff through the same access and camera management stack.',
                'systems': 'MikroTik (routeur) · TP-Link Omada (WiFi et commutateurs) · UniFi Cameras · UniFi Access',
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
                'work': ['Cat 6A cabling pulled through all suites before wall closure — Phase 1', 'MikroTik routing, Omada switching, and rack and patch-panel installation in six technical rooms — Phase 2', 'Deployment of UniFi cameras, UniFi Access, and TP-Link Omada WiFi aligned with final delivery — Phase 3', 'Complete documentation delivered to the general contractor and owner'],
                'result': 'The technology scope is delivered in line with the construction schedule. No delays are caused by building systems, and the documentation package is clean at handover.',
                'systems': 'MikroTik (routeur) · TP-Link Omada (WiFi et commutateurs) · UniFi Cameras · UniFi Access',
                'cta_title': 'Are you building or renovating a property?',
                'cta_copy': 'Coordinate the systems now.',
            },
        },
    },
    'fr': {
        'parent': {
            'title': 'Études de cas — Projets types | Opticable',
            'desc': 'Découvrez comment Opticable intervient dans les immeubles de bureaux, commerces, multilocatifs et chantiers de construction au Québec.',
            'h1': 'Études de cas — Comment on intervient selon le projet',
            'intro': "Voici des exemples de projets types représentatifs de nos interventions. Chaque bâtiment est différent — ces scénarios illustrent notre approche et les systèmes qu'on déploie selon le contexte.",
            'card_copy': {
                'case-office-building': 'Immeuble de bureaux avec routeur MikroTik, WiFi et commutateurs Omada, et gestion unifiée UniFi pour caméras et accès.',
                'case-multitenant-building': 'Immeuble multilocatif avec UniFi Access, caméras UniFi et WiFi Omada dans les aires communes.',
                'case-retail-space': 'Commerce avec plateforme de sécurité UniFi, WiFi Omada et routage MikroTik.',
                'case-construction-site': 'Chantier coordonné en phases autour de MikroTik, Omada et d’une pile de sécurité UniFi unifiée.',
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
                'work': ["Installation de UniFi Access sur 4 portes avec lecteurs de badge et gestion centralisée", 'Déploiement de 8 bornes TP-Link Omada avec commutateurs Omada et câblage Cat 6 dédié', 'Installation de 12 caméras UniFi avec visionnement à distance et gestion depuis la même plateforme que les accès', 'Déploiement du routeur MikroTik et remise en ordre complète du local réseau : rack, patch panels, identification de tous les points', 'Câblage de 25 nouveaux points réseau pour les postes de travail'],
                'result': "Un bâtiment entièrement câblé, sécurisé et connecté, géré depuis une seule interface pour les caméras et les accès. Le gestionnaire supervise le site à distance et le local réseau est documenté et propre.",
                'systems': "MikroTik (routeur) · TP-Link Omada (WiFi et commutateurs) · UniFi Cameras · UniFi Access",
                'cta_title': 'Ce projet ressemble au vôtre ?',
                'cta_copy': 'Décrivez-nous votre bâtiment.',
            },
            'case-multitenant-building': {
                'nav': 'Immeuble multilocatif',
                'title': 'Étude de cas — Immeuble multilocatif | Opticable',
                'desc': "Comment Opticable installe intercom, caméras, WiFi et câblage dans un immeuble multilocatif au Québec.",
                'h1': 'Projet type — Immeuble multilocatif résidentiel',
                'context': 'Immeuble de 24 unités, 4 étages, 2 entrées sécurisées, stationnement intérieur, buanderie et salle commune au rez-de-chaussée.',
                'challenges': ["Entrée principale sans intercom fonctionnel", 'Aucune caméra dans les aires communes', 'WiFi inexistant dans les corridors et espaces communs', 'Câblage des suites non structuré'],
                'work': ["Installation d'un intercom vidéo UniFi Access à l'entrée principale avec intégration complète au contrôle d'accès", 'Installation de 10 caméras UniFi dans les corridors, entrées et stationnement', 'Déploiement de bornes TP-Link Omada et de commutateurs Omada dans les corridors et espaces communs', 'Déploiement du routeur MikroTik, câblage Cat 6 dans les aires communes et organisation du local réseau'],
                'result': "Le gestionnaire contrôle l'accès à distance, visualise les caméras depuis son téléphone et gère l'intercom et les accès depuis la même plateforme UniFi. Les résidents bénéficient du WiFi dans tous les espaces communs.",
                'systems': 'MikroTik (routeur) · TP-Link Omada (WiFi et commutateurs) · UniFi Cameras · UniFi Access',
                'cta_title': 'Vous gérez un immeuble multilocatif ?',
                'cta_copy': 'Parlons de votre projet.',
            },
            'case-retail-space': {
                'nav': 'Commerce et espace de vente',
                'title': 'Étude de cas — Commerce et espace de vente | Opticable',
                'desc': "Comment Opticable installe caméras, contrôle d'accès et WiFi dans un commerce au Québec.",
                'h1': 'Projet type — Commerce et espace de vente au détail',
                'context': "Commerce de détail sur 2 niveaux, zone de vente, entrepôt à l'arrière, bureau de gestion et stationnement extérieur.",
                'challenges': ["Aucune surveillance de la zone de caisse et des entrées/sorties", 'WiFi instable pour les terminaux de paiement et les employés', "Accès à l'entrepôt non contrôlé", 'Besoin de visionnement à distance pour le propriétaire'],
                'work': ["Installation de 8 caméras UniFi couvrant la zone de vente, la caisse, l'entrepôt et le stationnement", 'Remplacement du WiFi par 3 bornes TP-Link Omada avec commutateurs Omada et SSID séparé pour les clients et les terminaux', "Installation d'un lecteur UniFi Access sur la porte de l'entrepôt", 'Déploiement du routeur MikroTik et configuration du visionnement à distance sur téléphone mobile pour le propriétaire'],
                'result': "Le propriétaire surveille son commerce à distance, le WiFi est stable pour les opérations et l'entrepôt est accessible uniquement au personnel autorisé via la même pile de gestion que les caméras.",
                'systems': 'MikroTik (routeur) · TP-Link Omada (WiFi et commutateurs) · UniFi Cameras · UniFi Access',
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
                'work': ['Tirage du câblage Cat 6A dans toutes les suites avant la fermeture des murs — Phase 1', 'Déploiement du routage MikroTik, des commutateurs Omada, des racks et patch panels dans les 6 locaux techniques — Phase 2', 'Déploiement des caméras UniFi, de UniFi Access et du WiFi TP-Link Omada coordonné avec la livraison — Phase 3', "Documentation complète remise à l'entrepreneur général et au propriétaire"],
                'result': 'Livraison technologique complète alignée sur le calendrier de construction. Aucun retard lié aux systèmes. Documentation propre remise à la livraison finale.',
                'systems': 'MikroTik (routeur) · TP-Link Omada (WiFi et commutateurs) · UniFi Cameras · UniFi Access',
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
            'case-office-building': 'Office building with MikroTik routing, Omada WiFi and switching, and a unified UniFi stack for cameras and access.',
            'case-multitenant-building': 'Multi-tenant property with UniFi Access, UniFi cameras, and Omada WiFi in the common areas.',
            'case-retail-space': 'Retail space with a unified UniFi security platform, Omada WiFi, and MikroTik routing.',
            'case-construction-site': 'Construction site coordinated in phases around MikroTik, Omada, and a unified UniFi security stack.',
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
            'work': ['Installation of UniFi Access on 4 doors with badge readers and centralized management', 'Deployment of 8 TP-Link Omada access points with Omada switching and dedicated Cat 6 cabling', 'Installation of 12 UniFi cameras with remote viewing and management from the same platform as access control', 'Deployment of a MikroTik router and complete organization of the network room, including rack, patch panels, and full point identification', 'Installation of 25 new network drops for workstations'],
            'result': 'A building that is fully cabled, secured, and connected, managed from one interface for cameras and access. The property manager supervises the site remotely and the network room is documented and clean.',
            'systems': 'MikroTik (router) · TP-Link Omada (WiFi and switches) · UniFi Cameras · UniFi Access',
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
            'work': ['Installation of a UniFi Access video intercom at the main entry with full access-control integration', 'Installation of 10 UniFi cameras in corridors, entries, and parking areas', 'Deployment of TP-Link Omada access points and Omada switches in corridors and common areas', 'Deployment of a MikroTik router, Cat 6 cabling in the common areas, and organization of the network room'],
            'result': 'The manager controls entry remotely, views the cameras from a phone, and manages the intercom and access rights from the same UniFi platform. Residents benefit from WiFi in all shared spaces.',
            'systems': 'MikroTik (router) · TP-Link Omada (WiFi and switches) · UniFi Cameras · UniFi Access',
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
            'work': ['Installation of 8 UniFi cameras covering the sales floor, cash area, warehouse, and parking', 'Replacement of the WiFi with 3 TP-Link Omada access points and Omada switches, with separate SSIDs for customers and payment terminals', 'Installation of a UniFi Access reader on the warehouse door', 'Deployment of a MikroTik router and setup of remote viewing on the owner mobile phone'],
            'result': 'The owner monitors the store remotely, the WiFi stays stable for operations, and the warehouse remains restricted to authorized staff through the same management stack used for the cameras.',
            'systems': 'MikroTik (router) · TP-Link Omada (WiFi and switches) · UniFi Cameras · UniFi Access',
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
            'work': ['Cat 6A cabling pulled through all suites before wall closure - Phase 1', 'Deployment of MikroTik routing, Omada switches, racks, and patch panels in the 6 technical rooms - Phase 2', 'Deployment of UniFi cameras, UniFi Access, and TP-Link Omada WiFi coordinated with final delivery - Phase 3', 'Complete documentation delivered to the general contractor and the owner'],
            'result': 'Full technology delivery aligned with the construction schedule. No delays caused by the systems, and clean documentation handed over at final delivery.',
            'systems': 'MikroTik (router) · TP-Link Omada (WiFi and switches) · UniFi Cameras · UniFi Access',
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
base_routes = {
    'en': {'home': '/en/', 'services': '/en/services/', 'industries': '/en/industries/', 'case-studies': '/en/case-studies/', 'blog': '/en/blog/', 'about': '/en/about/', 'faq': '/en/faq/', 'contact': '/en/contact/', 'privacy': '/en/privacy/', 'thanks': '/en/thank-you/', 'case-office-building': '/en/case-studies/office-building/', 'case-multitenant-building': '/en/case-studies/multi-tenant-building/', 'case-retail-space': '/en/case-studies/retail-and-sales-floor/', 'case-construction-site': '/en/case-studies/construction-site/'},
    'fr': {'home': '/', 'services': '/fr/services/', 'industries': '/fr/clientele/', 'case-studies': '/fr/etudes-de-cas/', 'blog': '/fr/blogue/', 'about': '/fr/a-propos/', 'faq': '/fr/faq/', 'contact': '/fr/contact/', 'privacy': '/fr/confidentialite/', 'thanks': '/fr/merci/', 'case-office-building': '/fr/etudes-de-cas/immeuble-de-bureaux/', 'case-multitenant-building': '/fr/etudes-de-cas/immeuble-multilocatif/', 'case-retail-space': '/fr/etudes-de-cas/commerce-espace-de-vente/', 'case-construction-site': '/fr/etudes-de-cas/chantier-de-construction/'},
}
routes = {k: dict(v) for k, v in base_routes.items()}
for key in order:
    routes['en'][key] = f"/en/services/{services[key]['en']['slug']}/"
    routes['fr'][key] = f"/fr/services/{services[key]['fr']['slug']}/"

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
  margin-top:auto;
  padding-top:4px;
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
  gap:12px;
  margin-bottom:28px;
}
.section-heading p{
  max-width:72ch;
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
  gap:12px;
}
.page-contact .contact-form-column{
  display:grid;
  gap:24px;
}
.page-contact .contact-sidebar .contact-detail-card{
  padding:18px 18px 20px;
  min-height:100%;
  border-radius:16px;
  position:relative;
}
.page-contact .contact-sidebar .contact-detail-card strong{
  display:block;
  margin-bottom:10px;
  white-space:normal;
  line-height:1.18;
}
.page-contact .contact-sidebar .contact-detail-card p,
.page-contact .contact-sidebar .contact-detail-card a{
  max-width:none;
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
@media (max-width:1200px){
  .page-contact .contact-layout{
    grid-template-columns:1fr;
  }
}
@media (max-width:760px){
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
  grid-template-columns:1.1fr .9fr .8fr .8fr;
  align-items:start;
  gap:24px;
  padding:48px 0 24px;
  border:0;
  border-radius:0;
  background:transparent;
  box-shadow:none;
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
.footer-bottom{
  margin-top:0;
  padding:22px 0 40px;
  border-top:1px solid rgba(255,255,255,.08);
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
  grid-template-columns:1.1fr .95fr .85fr .9fr 1.05fr;
}
.footer-contact-list{
  display:grid;
  gap:12px;
  margin:0;
  padding:0;
  list-style:none;
}
.footer-contact-list li{
  display:grid;
  gap:6px;
}
.footer-contact-list span,.footer-contact-list a,.footer-links a,.footer-services a,.social-link{
  color:rgba(235,242,237,.72);
}
.footer-socials{
  display:grid;
  gap:10px;
}
.social-link{
  display:inline-flex;
  align-items:center;
  gap:10px;
  width:max-content;
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
  width:min(100%,1480px);
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
  grid-template-columns:minmax(0,1.34fr) minmax(320px,.66fr);
  gap:24px;
  align-items:stretch;
}
.blog-article-hero .page-hero-copy h1{
  max-width:15ch;
  font-size:clamp(2.05rem,3.2vw,3.1rem);
}
.blog-article-hero .page-hero-copy > p:not(.eyebrow){
  max-width:58ch;
  font-size:1.08rem;
  padding-left:18px;
  border-left:3px solid rgba(122,210,150,.58);
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
  gap:14px;
}
.blog-summary-section,
.blog-article-section,
.blog-article-cta{
  padding:18px 22px;
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
  font-size:1.22rem;
  line-height:1.16;
}
.blog-summary-card p:last-child{
  margin:0;
}
.blog-section-stack{
  display:grid;
  gap:14px;
  position:relative;
  padding-top:18px;
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
  gap:8px;
  margin-bottom:8px;
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
  gap:14px;
  padding:22px 24px;
}
.blog-prose-panel p{
  margin:0;
  max-width:78ch;
  color:var(--muted);
  font-size:1.03rem;
  line-height:1.78;
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
  font-size:1.24rem;
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
  padding:18px 20px;
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
  line-height:1.55;
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
  font-size:1.22rem;
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
  line-height:1.72;
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
  font-size:1.06rem;
  line-height:1.7;
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
  .brand-badge-grid,.blog-grid{
    grid-template-columns:1fr;
  }
  .blog-card-meta,
  .blog-article-readout{
    grid-template-columns:1fr;
  }
  .blog-table{
    min-width:640px;
  }
  .social-link{
    width:auto;
  }
}
'''

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


def deploy_asset_path_from_url(url):
    path = url.split('?', 1)[0]
    if not path.startswith('/'):
        return None
    return DEPLOY_ROOT / path.lstrip('/')


@lru_cache(maxsize=None)
def load_font(size, family='body'):
    candidates = FONT_CANDIDATES['display'] if family == 'display' else FONT_CANDIDATES['body']
    for font_path in candidates:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def text_width(draw, text, font):
    return draw.textbbox((0, 0), text, font=font)[2]


def ellipsize_text(draw, text, font, max_width):
    cleaned = ' '.join(text.split())
    if text_width(draw, cleaned, font) <= max_width:
        return cleaned
    words = cleaned.split()
    while words:
        candidate = ' '.join(words).rstrip(' ,.;:') + '…'
        if text_width(draw, candidate, font) <= max_width:
            return candidate
        words.pop()
    return '…'


def wrap_text_lines(draw, text, font, max_width, max_lines=None):
    words = text.split()
    if not words:
        return []
    lines = []
    current = words[0]
    for word in words[1:]:
        tentative = f'{current} {word}'
        if text_width(draw, tentative, font) <= max_width:
            current = tentative
        else:
            lines.append(current)
            current = word
    lines.append(current)
    if max_lines and len(lines) > max_lines:
        trailing = ' '.join(lines[max_lines - 1:])
        lines = lines[:max_lines - 1] + [ellipsize_text(draw, trailing, font, max_width)]
    return lines


def parse_image_position(position):
    parts = (position or 'center center').split()
    if len(parts) != 2:
        return (0.5, 0.5)

    def parse_part(value):
        value = value.strip().lower()
        named = {
            'left': 0.0,
            'center': 0.5,
            'right': 1.0,
            'top': 0.0,
            'bottom': 1.0,
        }
        if value in named:
            return named[value]
        if value.endswith('%'):
            try:
                return max(0.0, min(1.0, float(value[:-1]) / 100.0))
            except ValueError:
                return 0.5
        return 0.5

    return (parse_part(parts[0]), parse_part(parts[1]))


def blog_social_image_url(article_key, lang):
    return f'/assets/blog-social/{article_key}-{lang}.png?v={ASSET_VER}'


def blog_social_image_path(article_key, lang):
    return BLOG_SOCIAL_IMAGE_DIR / f'{article_key}-{lang}.png'


def export_blog_social_image(article_key, lang, article):
    target = blog_social_image_path(article_key, lang)
    source_path = deploy_asset_path_from_url(article.get('hero_image') or OG_IMAGE_URL)
    fallback_path = deploy_asset_path_from_url(OG_IMAGE_URL)
    if source_path is None or not source_path.exists():
        source_path = fallback_path
    if source_path is None or not source_path.exists():
        return

    try:
        with Image.open(source_path) as background:
            if (
                fallback_path
                and fallback_path.exists()
                and (background.width < BLOG_SOCIAL_IMAGE_WIDTH // 2 or background.height < BLOG_SOCIAL_IMAGE_HEIGHT // 2)
            ):
                with Image.open(fallback_path) as fallback:
                    background = fallback.convert('RGBA')
            else:
                background = background.convert('RGBA')
            canvas = ImageOps.fit(
                background,
                (BLOG_SOCIAL_IMAGE_WIDTH, BLOG_SOCIAL_IMAGE_HEIGHT),
                IMAGE_RESAMPLING.LANCZOS,
                centering=parse_image_position(article.get('hero_image_position', 'center center')),
            )
    except (FileNotFoundError, UnidentifiedImageError):
        if fallback_path is None or not fallback_path.exists():
            return
        with Image.open(fallback_path) as fallback:
            canvas = ImageOps.fit(
                fallback.convert('RGBA'),
                (BLOG_SOCIAL_IMAGE_WIDTH, BLOG_SOCIAL_IMAGE_HEIGHT),
                IMAGE_RESAMPLING.LANCZOS,
            )

    overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(BLOG_SOCIAL_IMAGE_WIDTH):
        blend = x / max(1, BLOG_SOCIAL_IMAGE_WIDTH - 1)
        alpha = int(228 - (blend * 150))
        draw.line((x, 0, x, BLOG_SOCIAL_IMAGE_HEIGHT), fill=(7, 12, 10, max(0, alpha)))
    draw.rounded_rectangle((74, 60, 408, 112), radius=20, fill=(18, 45, 30, 216), outline=(122, 210, 150, 88), width=2)
    draw.rounded_rectangle((74, 134, 718, 566), radius=30, fill=(10, 18, 14, 116))

    eyebrow_font = load_font(26, 'body')
    headline_font = load_font(72, 'display')
    body_font = load_font(31, 'body')
    small_font = load_font(22, 'body')

    draw.text((100, 75), article.get('eyebrow', 'Opticable').upper(), font=eyebrow_font, fill=(198, 239, 214, 255))

    headline_lines = wrap_text_lines(draw, article['headline'], headline_font, 560, max_lines=4)
    y = 164
    for line in headline_lines:
        draw.text((96, y), line, font=headline_font, fill=(248, 252, 249, 255))
        y += 78

    max_excerpt_lines = max(0, min(3, (548 - (y + 14)) // 40))
    excerpt_lines = wrap_text_lines(draw, article.get('excerpt') or article.get('desc', ''), body_font, 560, max_lines=max_excerpt_lines)
    if excerpt_lines:
        y += 14
        for line in excerpt_lines:
            draw.text((98, y), line, font=body_font, fill=(214, 227, 218, 245))
            y += 40

    footer_text = 'Opticable Blog' if lang == 'en' else 'Blogue Opticable'
    if article.get('tags'):
        footer_text += '  |  ' + '  |  '.join(article['tags'][:2])
    draw.text((98, 584), footer_text, font=small_font, fill=(176, 214, 188, 255))

    image = Image.alpha_composite(canvas, overlay)
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target, format='PNG', optimize=True)
    IMAGE_DIMENSIONS_BY_URL[blog_social_image_url(article_key, lang)] = (BLOG_SOCIAL_IMAGE_WIDTH, BLOG_SOCIAL_IMAGE_HEIGHT)


def export_blog_social_images():
    for article_key, entry in BLOG_ARTICLES.items():
        for lang in ('en', 'fr'):
            localized = entry.get(lang)
            if not localized:
                continue
            export_blog_social_image(article_key, lang, localized)


def export_image_variant(spec):
    source = spec['source']
    if not source.exists():
        return
    with Image.open(source) as image:
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')
        if spec.get('crop'):
            image = image.crop(spec['crop'])
        if spec.get('resize') and spec.get('canvas'):
            image = ImageOps.contain(image, spec['resize'], IMAGE_RESAMPLING.LANCZOS)
        elif spec.get('resize'):
            image.thumbnail(spec['resize'], IMAGE_RESAMPLING.LANCZOS)
        if spec.get('canvas'):
            background = spec.get('background', (255, 255, 255, 0))
            canvas = Image.new('RGBA', spec['canvas'], background)
            offset = ((canvas.width - image.width) // 2, (canvas.height - image.height) // 2)
            mask = image if 'A' in image.getbands() else None
            canvas.paste(image, offset, mask)
            image = canvas
        if spec['format'] == 'JPEG':
            if image.mode != 'RGB':
                image = image.convert('RGB')
            save_kwargs = {'format': 'JPEG', 'quality': spec['quality'], 'optimize': True, 'progressive': True}
        elif spec['format'] == 'PNG':
            save_kwargs = {'format': 'PNG', 'optimize': True}
        else:
            save_kwargs = {'format': 'WEBP', 'quality': spec['quality'], 'method': 6}
        spec['target'].parent.mkdir(parents=True, exist_ok=True)
        image.save(spec['target'], **save_kwargs)


def export_home_images():
    for spec in HOME_IMAGE_EXPORTS:
        export_image_variant(spec)


def reset_deploy_dir():
    shutil.rmtree(DEPLOY_ROOT, ignore_errors=True)
    DEPLOY_ASSET_ROOT.mkdir(parents=True, exist_ok=True)


def copy_static_assets():
    for name in STATIC_ASSET_FILES:
        source = SOURCE_ASSET_ROOT / name
        if not source.exists():
            continue
        shutil.copy2(source, DEPLOY_ASSET_ROOT / name)
    for spec in RUNTIME_ASSET_COPIES:
        source = spec['source']
        if not source.exists():
            continue
        shutil.copy2(source, spec['target'])


def remove_legacy_root_build():
    for name in LEGACY_ROOT_BUILD_DIRS:
        shutil.rmtree(root / name, ignore_errors=True)
    for name in LEGACY_ROOT_BUILD_FILES:
        path = root / name
        if path.exists():
            path.unlink()
    for name in ROOT_GENERATED_ASSET_FILES:
        path = SOURCE_ASSET_ROOT / name
        if path.exists():
            path.unlink()


def esc(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'))


def absolute_url(path):
    if path.startswith(('http://', 'https://')):
        return path
    if path == '/':
        return SITE_URL + '/'
    return f'{SITE_URL}{path}'


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
    attrs = [
        f'src="{src}"',
        'alt="Opticable logo"',
        f'width="{LOGO_UI_WIDTH}"',
        f'height="{LOGO_UI_HEIGHT}"',
        'decoding="async"',
    ]
    if context == 'footer':
        attrs.append('loading="lazy"')
    else:
        attrs.append('loading="eager"')
    return f'<img {" ".join(attrs)} />'


def content_img(src, alt, width, height, cls='', eager=False, high_priority=False, zoomable=False, lang='en', caption=''):
    attrs = [
        f'src="{src}"',
        f'alt="{esc(alt)}"',
        f'width="{width}"',
        f'height="{height}"',
        'decoding="async"',
    ]
    if cls:
        attrs.append(f'class="{cls}"')
    if eager:
        attrs.append('loading="eager"')
    else:
        attrs.append('loading="lazy"')
    if high_priority:
        attrs.append('fetchpriority="high"')
    img_html = f'<img {" ".join(attrs)} />'
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
        hints.append(f'<link rel="preload" as="image" href="{HOME_RACK_URL}" />')
    if page_key == 'contact':
        hints.append('<link rel="preconnect" href="https://forms.zohopublic.com" crossorigin />')
        hints.append('<link rel="dns-prefetch" href="//forms.zohopublic.com" />')
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
    page_keys = (
        'home',
        'services',
        *order,
        'industries',
        'case-studies',
        *CASE_STUDY_ORDER,
        'blog',
        'about',
        'faq',
        'contact',
    )
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
        f'<figure class="hero-media-main"><div class="hero-media-frame">{content_img(HOME_BUILDING_URL, visual["top_alt"], HOME_BUILDING_WIDTH, HOME_BUILDING_HEIGHT, "hero-media-main-image", zoomable=True, lang=lang, caption=visual["top_title"])}</div>'
        f'<figcaption class="hero-media-caption"><strong>{esc(visual["top_title"])}</strong><span>{esc(visual["top_copy"])}</span></figcaption></figure>'
        f'<figure class="hero-media-main"><div class="hero-media-frame">{content_img(HOME_RACK_URL, visual["main_alt"], HOME_RACK_WIDTH, HOME_RACK_HEIGHT, "hero-media-main-image", eager=True, high_priority=True, zoomable=True, lang=lang, caption=visual["main_title"])}</div>'
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
        f'<div class="section-heading"><p class="eyebrow">{esc(T[lang]["process_title"])}</p>'
        f'<h2>{esc(T[lang]["process_title"])}</h2><p>{esc(T[lang]["process_intro"])}</p></div>'
        f'<div class="timeline">{items}</div>',
        'process-section',
    )


def split_list_items(items):
    if len(items) <= 4:
        return [items]
    midpoint = (len(items) + 1) // 2
    return [items[:midpoint], items[midpoint:]]


def render_custom_content_section(section):
    heading = f'<div class="section-heading"><p class="eyebrow">{esc(section["eyebrow"])}</p><h2>{esc(section["title"])}</h2>'
    if section.get('copy'):
        heading += f'<p>{esc(section["copy"])}</p>'
    heading += '</div>'

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


def blog_article_paths(article_key):
    entry = BLOG_ARTICLES.get(article_key, {})
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
            f' style="--blog-card-image:url({esc(article["hero_image"])});'
            f'--blog-card-image-position:{esc(article.get("hero_image_position", "center center"))};"'
        )
    return (
        f'<article class="card blog-article-card">'
        f'<a class="blog-article-card-main" href="{article["path"]}" aria-label="{esc(ui["read_article"])}: {esc(article["headline"])}"{main_style}>'
        f'{render_chips(article["tags"])}<h3>{esc(article["headline"])}</h3><p>{esc(article["excerpt"])}</p><span class="blog-card-surface-link">{esc(ui["read_article"])}</span></a>'
        f'<aside class="blog-article-card-side">{render_blog_meta(article, lang)}<a class="button button-primary blog-card-link" href="{article["path"]}">{esc(ui["read_article"])}</a></aside>'
        f'</article>'
    )


def render_blog_listing(lang, blog_data):
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
        f'<div class="section-heading"><p class="eyebrow">{esc(section["eyebrow"])}</p><h2>{esc(section["title"])}</h2></div>'
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
            f' style="--blog-hero-image:url({esc(article["hero_image"])});'
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
        + band_section(
            f'<div><p class="eyebrow">{esc(T[lang]["blog"])}</p><h2>{esc(cta["title"])}</h2><p>{esc(cta["copy"])}</p></div>'
            f'<div class="cta-actions"><a class="button button-primary" href="{primary_href}">{esc(cta["primary_label"])}</a>'
            f'<a class="button button-secondary" href="{secondary_href}">{esc(cta["secondary_label"])}</a></div>',
            'blog-article-cta',
            'layout-shell blog-article-shell cta-band',
        )
    )
    return breadcrumb_items, body


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


def social_meta_values(lang, key, title, desc, canonical_url, article_meta=None):
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
    return meta


def schema(lang, page_key, title, desc, faq_items=None, service_name=None, breadcrumb_items=None, page_url=None, article_meta=None):
    page_url = page_url or absolute_url(routes[lang][page_key])
    catalog = offer_catalog_schema(lang)
    business = {
        '@type': 'LocalBusiness',
        '@id': BUSINESS_ID,
        'name': 'Opticable',
        'legalName': LEGAL_BUSINESS_NAME,
        'url': absolute_url(default_route('home')),
        'logo': absolute_url(LOGO_UI_URL),
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
                    'url': absolute_url(LOGO_UI_URL),
                    'width': LOGO_UI_WIDTH,
                    'height': LOGO_UI_HEIGHT,
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
    nav = [
        simple_nav_link(lang, 'home', current),
        nav_dropdown(lang, 'services', current, order, wide=True),
        nav_dropdown(lang, 'industries', current, ('case-studies',)),
        simple_nav_link(lang, 'about', current),
        simple_nav_link(lang, 'faq', current),
        simple_nav_link(lang, 'blog', current),
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
    quick = ''.join(f'<li><a href="{routes[lang][k]}">{esc(label_for_key(lang, k))}</a></li>' for k in ('home', 'services', 'industries', 'case-studies', 'blog', 'about', 'faq', 'contact', 'privacy'))
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
        f'<link rel="icon" type="image/png" href="{LOGO_MARK_URL}" />'
        f'<link rel="icon" type="image/png" sizes="32x32" href="{FAVICON_32_URL}" />'
        f'<link rel="apple-touch-icon" sizes="180x180" href="{APPLE_TOUCH_ICON_URL}" />'
        f'<link rel="manifest" href="{WEBMANIFEST_URL}" />'
    )


def stylesheet_link_tags():
    return f'<link rel="stylesheet" href="{STYLES_URL}" />'


def page(lang, key, current, title, desc, body, faq_items=None, service_name=None, breadcrumb_items=None, robots='index, follow, max-image-preview:large', canonical_path=None, include_alternates=True, resource_key=None, schema_page_url=None, alternate_paths=None, lang_switch_href=None, article_meta=None, preload_image_url=None):
    t = T[lang]
    canonical_url = absolute_url(canonical_path or routes[lang][key])
    social_meta = social_meta_values(lang, key, title, desc, canonical_url, article_meta=article_meta)
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
    return f'<!doctype html><html lang="{language_tag(lang)}"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>{esc(title)}</title><meta name="description" content="{esc(desc)}" /><meta name="robots" content="{esc(robots)}" /><meta name="theme-color" content="#153628" />{icon_link_tags()}<link rel="canonical" href="{canonical_url}" />{alternate_tags}<meta property="og:type" content="{esc(social_meta["og_type"])}" /><meta property="og:site_name" content="Opticable" /><meta property="og:locale" content="{t["locale"]}" />{og_locale_alternates}<meta property="og:title" content="{esc(social_meta["og_title"])}" /><meta property="og:description" content="{esc(social_meta["og_description"])}" /><meta property="og:url" content="{esc(social_meta["og_url"])}" /><meta property="og:image" content="{social_meta["og_image"]}" /><meta property="og:image:type" content="{esc(social_meta["og_image_type"])}" /><meta property="og:image:alt" content="{esc(social_meta["og_image_alt"])}" /><meta property="og:image:width" content="{social_meta["og_image_width"]}" /><meta property="og:image:height" content="{social_meta["og_image_height"]}" /><meta name="twitter:card" content="{esc(social_meta["twitter_card"])}" /><meta name="twitter:title" content="{esc(social_meta["twitter_title"])}" /><meta name="twitter:description" content="{esc(social_meta["twitter_description"])}" /><meta name="twitter:image" content="{social_meta["og_image"]}" /><meta name="twitter:image:alt" content="{esc(social_meta["og_image_alt"])}" />{article_meta_tags}{resource_hints(resource_key or key, preload_image_url=preload_image_url)}{stylesheet_link_tags()}<script type="application/ld+json">{schema(lang, key, title, desc, faq_items, service_name, breadcrumb_items, page_url=schema_page_url or canonical_url, article_meta=article_meta)}</script></head><body class="{body_class}"><a class="skip-link" href="#content">{esc(t["skip"])}</a><div class="site-shell">{header(lang, current, key, lang_switch_href)}{cookie_banner(lang)}<main id="content">{body}</main>{footer(lang)}</div>{image_lightbox(lang)}<script src="{SCRIPT_URL}" defer></script></body></html>'
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

remove_legacy_root_build()
reset_deploy_dir()
copy_static_assets()
export_home_images()
export_blog_social_images()
(DEPLOY_ASSET_ROOT / 'styles.css').write_text(css.strip() + '\n', encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'site.js').write_text(js.strip() + '\n', encoding='utf-8')

for lang in ('en', 'fr'):
    t = T[lang]
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
            f'<div class="contact-layout"><div class="contact-panel contact-sidebar"><h2>{esc(contact_panel_title)}</h2>{f"<p>{esc(contact_panel_copy)}</p>" if contact_panel_copy else ""}{contact_page_details}</div><div class="contact-form-column">{form_section(lang)}{f"<div class=\"contact-panel\"><p>{esc(t['contact_form_note'])}</p></div>" if t.get("contact_form_note") else ""}</div></div>',
            'contact-band',
            'section-shell contact-shell',
        )
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
    )
    write_url(routes[lang]['thanks'], page(lang, 'thanks', 'contact', t['thanks_title'], t['thanks_desc'], thanks_body, breadcrumb_items=thanks_breadcrumbs, robots='noindex, nofollow'))

    privacy_cards_html = ''.join(card(title, copy) for title, copy in t['privacy_cards'])
    privacy_choices_html = ''.join(f'<li>{esc(item)}</li>' for item in t['privacy_choices'])
    privacy_breadcrumbs = [(t['home'], routes[lang]['home']), (t['privacy'], routes[lang]['privacy'])]
    privacy_body = (
        breadcrumb_nav(privacy_breadcrumbs)
        + band_section(
            f'<div class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(t["privacy"])}</p><h1>{esc(t["privacy_h1"])}</h1><p>{esc(t["privacy_intro"])}</p></div></div>',
            'hero-band page-hero-band',
            'layout-shell',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(t["privacy"])}</p><h2>{esc(t["privacy_cards_title"])}</h2><p>{esc(t["privacy_cards_intro"])}</p></div><div class="privacy-grid">{privacy_cards_html}</div>',
            'privacy-section',
        )
        + band_section(
            f'<div class="two-col"><div class="contact-panel"><p class="eyebrow">{esc(t["privacy"])}</p><h2>{esc(t["privacy_choices_title"])}</h2><ul class="check-list">{privacy_choices_html}</ul></div><div class="contact-panel"><p class="eyebrow">{esc(t["contact"])}</p><h2>{esc(t["footer_contact_title"])}</h2><p>{esc(t["footer_contact_intro"])}</p><div class="detail-list">{details}</div></div></div>',
            'privacy-choices-section',
        )
    )
    write_url(routes[lang]['privacy'], page(lang, 'privacy', 'privacy', t['privacy_title'], t['privacy_desc'], privacy_body, breadcrumb_items=privacy_breadcrumbs))

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
        + (inline_cta_band(custom_faq_cta['title'], custom_faq_cta['copy'], routes[lang]['contact'], custom_faq_cta['label']) if custom_faq_cta else cta(lang))
    )
    write_url(routes[lang]['faq'], page(lang, 'faq', 'faq', t['faq_title'], t['faq_desc'], faq_body, faq_items=flat_faq_items(lang), breadcrumb_items=faq_breadcrumbs))

    blog_data = BLOG_PAGE[lang]
    blog_breadcrumbs = [(t['home'], routes[lang]['home']), (t['blog'], routes[lang]['blog'])]
    blog_body = (
        breadcrumb_nav(blog_breadcrumbs)
        + band_section(
            f'<div class="page-hero-copy"><p class="eyebrow">{esc(blog_data["eyebrow"])}</p><h1>{esc(blog_data["h1"])}</h1><p>{esc(blog_data["intro"])}</p></div>'
            f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["blog"])}</p><h2>{esc(blog_data["listing_title"])}</h2><p>{esc(blog_data["listing_intro"])}</p></aside>',
            'hero-band page-hero-band',
            'layout-shell page-hero',
        )
        + band_section(
            f'<div class="section-heading"><p class="eyebrow">{esc(t["blog"])}</p><h2>{esc(blog_data["listing_title"])}</h2><p>{esc(blog_data["listing_intro"])}</p></div>'
            f'{render_blog_listing(lang, blog_data)}',
            'blog-listing-section',
        )
    )
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
                'blog',
                article['title'],
                article['desc'],
                article_body,
                breadcrumb_items=article_breadcrumbs,
                canonical_path=article['path'],
                include_alternates=article_has_pair,
                resource_key='blog',
                schema_page_url=absolute_url(article['path']),
                alternate_paths=article_paths if article_has_pair else None,
                lang_switch_href=article_paths.get('fr' if lang == 'en' else 'en'),
                article_meta=article_meta,
                preload_image_url=article.get('hero_image'),
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
                + inline_cta_band(custom_service_page_content[key]['cta'], t['service_area_intro'], routes[lang]['contact'], t['quote'])
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
    'home',
    'home',
    'Page introuvable | Opticable',
    "La page demandée est introuvable. Retournez à l’accueil, aux services ou à la page contact d’Opticable.",
    not_found_body,
    robots='noindex, follow',
    canonical_path='/404.html',
    include_alternates=False,
    resource_key='404',
)

robots_lines = ['User-agent: *', 'Allow: /', '']
robots_lines.append('Sitemap: ' + absolute_url('/sitemap.xml'))
(DEPLOY_ROOT / 'robots.txt').write_text('\n'.join(robots_lines) + '\n', encoding='utf-8')
(DEPLOY_ROOT / 'sitemap.xml').write_text(sitemap_xml(), encoding='utf-8')
(DEPLOY_ROOT / 'site.webmanifest').write_text(webmanifest_json(), encoding='utf-8')
(DEPLOY_ROOT / 'ads.txt').write_text('# Opticable does not authorize any third-party digital sellers.\n', encoding='utf-8')
(DEPLOY_ROOT / '404.html').write_text(not_found_html.strip() + '\n', encoding='utf-8')
