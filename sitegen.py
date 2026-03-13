from pathlib import Path
import json
from datetime import date
import shutil
from PIL import Image

root = Path(__file__).resolve().parent
SOURCE_ASSET_ROOT = root / 'assets'
DEPLOY_ROOT = root / 'dist'
DEPLOY_ASSET_ROOT = DEPLOY_ROOT / 'assets'
LEGACY_ROOT_BUILD_DIRS = ('en', 'fr')
LEGACY_ROOT_BUILD_FILES = ('index.html', 'robots.txt', 'sitemap.xml', 'styles.css', 'script.js')
STATIC_ASSET_FILES = ('logo-mark.svg', 'opticable-logo.png')
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
ASSET_VER = '20260312m'
LOGO_LOCKUP_URL = f'/assets/opticable-logo.png?v={ASSET_VER}'
LOGO_UI_URL = f'/assets/logo-ui.webp?v={ASSET_VER}'
LOGO_MARK_URL = f'/assets/logo-mark.svg?v={ASSET_VER}'
STYLES_URL = f'/assets/styles.css?v={ASSET_VER}'
SCRIPT_URL = f'/assets/site.js?v={ASSET_VER}'
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
LOGO_LOCKUP_WIDTH = 1600
LOGO_LOCKUP_HEIGHT = 687
LOGO_UI_WIDTH = 1200
LOGO_UI_HEIGHT = 515
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
WEBSITE_ID = f'{SITE_URL}/#website'
BUSINESS_ID = f'{SITE_URL}/#business'
GENERAL_INQUIRY_LABELS = {'General inquiries', 'Renseignements généraux', 'Renseignements generaux'}
PROJECT_REQUEST_LABELS = {'Project requests', 'Demandes de soumission', 'Demandes de projet'}
PHONE_LABELS = {'Office phone', 'Téléphone du bureau', 'Telephone du bureau'}
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

IMAGE_RESAMPLING = getattr(Image, 'Resampling', Image)
HOME_SOURCE_DIR = root / 'Images' / 'home-sources'
HOME_IMAGE_EXPORTS = (
    {
        'source': SOURCE_ASSET_ROOT / 'opticable-logo.png',
        'target': DEPLOY_ASSET_ROOT / 'logo-ui.webp',
        'resize': (LOGO_UI_WIDTH, LOGO_UI_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
    {
        'source': root / 'Images' / 'source-library' / 'ai-generated' / 'gemini-building.png',
        'target': DEPLOY_ASSET_ROOT / 'home-building.webp',
        'resize': (HOME_BUILDING_WIDTH, HOME_BUILDING_HEIGHT),
        'format': 'WEBP',
        'quality': 84,
    },
    {
        'source': HOME_SOURCE_DIR / 'network-rack.png',
        'target': DEPLOY_ASSET_ROOT / 'home-rack.webp',
        'resize': (HOME_RACK_WIDTH, HOME_RACK_HEIGHT),
        'format': 'WEBP',
        'quality': 84,
    },
    {
        'source': root / 'Images' / 'source-library' / 'Gemini_Generated_Image_fipiq6fipiq6fipi.png',
        'target': DEPLOY_ASSET_ROOT / 'about-panel.webp',
        'resize': (ABOUT_PANEL_WIDTH, ABOUT_PANEL_HEIGHT),
        'format': 'WEBP',
        'quality': 92,
    },
    {
        'source': root / 'Images' / 'source-library' / 'products' / 'intercom-door-station.jpeg',
        'target': DEPLOY_ASSET_ROOT / 'service-intercom.webp',
        'resize': (SERVICE_INTERCOM_WIDTH, SERVICE_INTERCOM_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
    {
        'source': root / 'Images' / 'source-library' / 'patch-and-switch-original.png',
        'target': DEPLOY_ASSET_ROOT / 'service-cabling.webp',
        'resize': (SERVICE_CABLING_WIDTH, SERVICE_CABLING_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
    {
        'source': root / 'Images' / 'source-library' / 'cabling' / 'cablep4.jpg',
        'target': DEPLOY_ASSET_ROOT / 'service-fiber.webp',
        'resize': (SERVICE_FIBER_WIDTH, SERVICE_FIBER_HEIGHT),
        'format': 'WEBP',
        'quality': 92,
    },
    {
        'source': root / 'Images' / 'source-library' / 'Gemini_Infra_reseau.png',
        'target': DEPLOY_ASSET_ROOT / 'service-infrastructure.webp',
        'resize': (SERVICE_INFRASTRUCTURE_WIDTH, SERVICE_INFRASTRUCTURE_HEIGHT),
        'format': 'WEBP',
        'quality': 92,
    },
    {
        'source': root / 'Images' / 'source-library' / 'Gemini_Access_Reader.png',
        'target': DEPLOY_ASSET_ROOT / 'service-access.webp',
        'resize': (SERVICE_ACCESS_WIDTH, SERVICE_ACCESS_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
    {
        'source': root / 'Images' / 'source-library' / 'ai-generated' / 'gemini-wifi-access-point.png',
        'target': DEPLOY_ASSET_ROOT / 'service-wifi.webp',
        'resize': (SERVICE_WIFI_WIDTH, SERVICE_WIFI_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
    {
        'source': root / 'Images' / 'source-library' / 'Gemini_Voip.png',
        'target': DEPLOY_ASSET_ROOT / 'service-voip.webp',
        'resize': (SERVICE_VOIP_WIDTH, SERVICE_VOIP_HEIGHT),
        'format': 'WEBP',
        'quality': 90,
    },
)
RUNTIME_ASSET_COPIES = (
    {
        'source': root / 'Images' / 'source-library' / 'products' / 'Unifi_Bullet_Dual.avif',
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
    'home_title': 'Commercial Technology Infrastructure Contractor | Cameras, Access Control, WiFi | Opticable',
    'home_desc': 'Opticable installs security cameras, access control, intercoms, commercial WiFi, structured cabling, fiber optics, network infrastructure, and IP phone systems for commercial properties.',
    'home_h1': 'Commercial technology specialists for cameras, secure entry, WiFi, and connected building systems.',
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
    'home_title': "Entrepreneur en infrastructures technologiques commerciales | Caméras, contrôle d'accès et WiFi | Opticable",
    'home_desc': "Opticable installe des caméras de sécurité, du contrôle d'accès, des intercoms, du WiFi commercial, du câblage structuré, de la fibre optique, de l'infrastructure réseau et de la téléphonie IP pour les immeubles commerciaux.",
    'home_kicker': 'Technologie commerciale et systèmes du bâtiment',
    'home_h1': "Des spécialistes des technologies commerciales pour les caméras, le contrôle d'accès, le WiFi et les systèmes de bâtiment connectés.",
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
    'security-camera-systems',
    'access-control-systems',
    'commercial-wifi-installation',
    'intercom-systems',
    'structured-cabling',
    'fiber-optic-installation',
    'network-infrastructure',
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
'fr': {'slug': 'installation-fibre-optique', 'name': 'Installation de fibre optique', 'title': 'Installation de fibre optique pour immeubles commerciaux | Opticable', 'desc': 'Installation de fibre optique pour immeubles commerciaux, backbones, colonnes montantes, handoffs internet et connectivite a haute capacite.', 'hero': 'Fibre optique pour backbones, colonnes montantes et connectivite d affaires a haute capacite.', 'intro': 'Opticable installe la fibre optique pour les environnements commerciaux qui exigent un backbone fiable, des extensions de handoff fournisseur ou des liens a plus forte capacite entre etages, suites et salles reseau.', 'summary': 'Backbones fibre, colonnes montantes, extensions de handoff et liens a haute capacite pour proprietes commerciales.', 'includes': ['Cablage backbone fibre entre MDF, IDF, suites et points d equipement', 'Extensions de handoff fournisseur et chemin entre le point de demarcation et la salle reseau', 'Terminaisons fibre, raccordement, organisation des chemins et coordination cote baie'], 'benefits': ['Distribution a plus forte capacite pour la croissance future', 'Liens fiables sur de plus longues distances dans les grands sites', 'Meilleure coordination avec les baies, la commutation et les salles techniques'], 'cases': ['Immeubles de bureaux et proprietes mixtes sur plusieurs etages', 'Extensions du handoff du fournisseur internet vers la salle reseau', 'Renouvellement de backbone lors d ameliorations locatives ou proprietaires'], 'industries': ['Immeubles de bureaux commerciaux', 'Proprietes multi-locatives', 'Sites industriels et entrepots'], 'related': ['network-infrastructure', 'structured-cabling', 'security-camera-systems']},
    },
    'network-infrastructure': {
        'en': {'slug': 'network-infrastructure', 'name': 'Network Infrastructure', 'title': 'Commercial Network Infrastructure and Server Rack Installation | Opticable', 'desc': 'Commercial network infrastructure services including server rack installation, network room build-outs, switching support, and internet infrastructure deployment.', 'hero': 'Network infrastructure, server rack installation, and room build-outs for commercial environments.', 'intro': 'Opticable supports the physical network infrastructure behind business connectivity, equipment rooms, and internet service deployment. Projects can include server rack installation, patching, switch connectivity, demarc extensions, and cleanup of difficult legacy rooms.', 'summary': 'Server racks, network rooms, handoff routing, patching, switching support, and infrastructure cleanup.', 'includes': ['Server rack and cabinet installation with cable management and organized terminations', 'Patch panels, uplink routing, switch connectivity, and demarc-to-rack pathway planning', 'Internet infrastructure deployment and cleanup of crowded or unlabeled network rooms'], 'benefits': ['Better room serviceability after turnover', 'Cleaner handoff between wireless, security, voice, and tenant systems', 'Less rework during future upgrades and expansion'], 'cases': ['New office or retail suite network room setup', 'Demarc extensions and backbone routing for managed buildings', 'Legacy MDF and IDF cleanup before expansion'], 'industries': ['Business offices', 'Property management portfolios', 'Retail and hospitality properties'], 'related': ['structured-cabling', 'fiber-optic-installation', 'ip-phone-systems']},
'fr': {'slug': 'infrastructure-reseau', 'name': 'Infrastructure reseau', 'title': 'Infrastructure reseau commerciale et installation de baies serveurs | Opticable', 'desc': 'Services d infrastructure reseau commerciale incluant l installation de baies serveurs, l amenagement de salles reseau, le soutien a la commutation et le deploiement d infrastructures internet.', 'hero': 'Infrastructure reseau, installation de baies serveurs et amenagement de salles techniques pour environnements commerciaux.', 'intro': 'Opticable soutient l infrastructure physique derriere la connectivite d affaires, les locaux techniques et le deploiement de services internet. Les projets peuvent inclure l installation de baies serveurs, le raccordement, la connectivite des commutateurs, les extensions de demarcation et la remise en ordre de salles difficiles a entretenir.', 'summary': 'Baies serveurs, salles reseau, routage des handoffs, raccordement, soutien aux commutateurs et remise en ordre des infrastructures.', 'includes': ['Installation de baies et cabinets avec gestion du cablage et terminaisons ordonnees', 'Panneaux de raccordement, routage des uplinks, connectivite des commutateurs et chemin entre la demarcation et la baie', 'Deploiement d infrastructures internet et nettoyage de salles reseau surchargees ou non etiquetees'], 'benefits': ['Salles plus faciles a soutenir apres la remise', 'Transition plus propre entre WiFi, securite, voix et systemes des locataires', 'Moins de reprises lors des mises a niveau et des expansions futures'], 'cases': ['Mise en place de salles reseau pour nouveaux bureaux ou commerces', 'Extensions de demarcation et routage backbone pour immeubles geres', 'Nettoyage de MDF et IDF existants avant expansion'], 'industries': ['Bureaux d entreprise', 'Portefeuilles de gestion immobiliere', 'Commerces et hotellerie'], 'related': ['structured-cabling', 'fiber-optic-installation', 'ip-phone-systems']},
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
    'title': 'Installation de fibre optique pour immeubles commerciaux | Opticable',
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
    'access-control-systems',
    'intercom-systems',
    'ip-phone-systems',
):
    services[key]['en']['industries'] = shared_service_types_en
    services[key]['fr']['industries'] = shared_service_types_fr

primary_order = [
    'security-camera-systems',
    'access-control-systems',
    'commercial-wifi-installation',
    'intercom-systems',
]
secondary_order = [
    'structured-cabling',
    'fiber-optic-installation',
    'network-infrastructure',
    'ip-phone-systems',
]
order = primary_order + secondary_order
base_routes = {
    'en': {'home': '/en/', 'services': '/en/services/', 'industries': '/en/industries/', 'about': '/en/about/', 'faq': '/en/faq/', 'contact': '/en/contact/', 'privacy': '/en/privacy/', 'thanks': '/en/thank-you/'},
    'fr': {'home': '/', 'services': '/fr/services/', 'industries': '/fr/secteurs/', 'about': '/fr/a-propos/', 'faq': '/fr/faq/', 'contact': '/fr/contact/', 'privacy': '/fr/confidentialite/', 'thanks': '/fr/merci/'},
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
const cookieBannerKey = 'opticable-cookie-banner-accepted';
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
'''

def write_url(url, content):
    if url == '/':
        path = DEPLOY_ROOT / 'index.html'
    else:
        path = DEPLOY_ROOT / url.strip('/') / 'index.html'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + '\n', encoding='utf-8')


def export_image_variant(spec):
    source = spec['source']
    if not source.exists():
        return
    with Image.open(source) as image:
        if spec.get('crop'):
            image = image.crop(spec['crop'])
        if spec.get('resize'):
            image.thumbnail(spec['resize'], IMAGE_RESAMPLING.LANCZOS)
        if spec['format'] == 'JPEG':
            if image.mode != 'RGB':
                image = image.convert('RGB')
            save_kwargs = {'format': 'JPEG', 'quality': spec['quality'], 'optimize': True, 'progressive': True}
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


def language_tag(lang):
    return T[lang]['locale'].replace('_', '-')


def default_route(page_key):
    return routes['fr'][page_key]


def logo_img(context):
    attrs = [
        f'src="{LOGO_UI_URL}"',
        'alt="Opticable logo"',
        f'width="{LOGO_UI_WIDTH}"',
        f'height="{LOGO_UI_HEIGHT}"',
        'decoding="async"',
    ]
    if context == 'footer':
        attrs.append('loading="lazy"')
    else:
        attrs.append('loading="eager"')
        attrs.append('fetchpriority="high"')
    return f'<img {" ".join(attrs)} />'


def content_img(src, alt, width, height, cls='', eager=False, zoomable=False, lang='en', caption=''):
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
        attrs.append('fetchpriority="high"')
    else:
        attrs.append('loading="lazy"')
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


def resource_hints(page_key):
    hints = []
    if page_key == 'home':
        hints.append(f'<link rel="preload" as="image" href="{HOME_BUILDING_URL}" />')
    if page_key == 'contact':
        hints.append('<link rel="preconnect" href="https://forms.zohopublic.com" crossorigin />')
        hints.append('<link rel="dns-prefetch" href="//forms.zohopublic.com" />')
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


def breadcrumb_nav(items):
    parts = []
    for index, (label, href) in enumerate(items):
        if index:
            parts.append('<span>/</span>')
        if index == len(items) - 1:
            parts.append(f'<span aria-current="page">{esc(label)}</span>')
        else:
            parts.append(f'<a href="{href}">{esc(label)}</a>')
    return f'<nav class="breadcrumb" aria-label="Breadcrumb">{"".join(parts)}</nav>'


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
    page_keys = ('home', 'services', 'industries', 'about', 'faq', 'contact', 'privacy', *order)
    lastmod = date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for lang in ('en', 'fr'):
        for key in page_keys:
            lines.append('  <url>')
            lines.append(f'    <loc>{esc(absolute_url(routes[lang][key]))}</loc>')
            lines.append(f'    <lastmod>{lastmod}</lastmod>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{language_tag("en")}" href="{esc(absolute_url(routes["en"][key]))}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{language_tag("fr")}" href="{esc(absolute_url(routes["fr"][key]))}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{esc(absolute_url(default_route(key)))}" />')
            lines.append('  </url>')
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


def card(title, text, link=None, label='Learn more', cls='card'):
    more = f'<a class="more" href="{link}">{esc(label)}</a>' if link else ''
    return f'<article class="{cls}"><h3>{esc(title)}</h3><p>{esc(text)}</p>{more}</article>'


def service_cards(lang, label, keys=None):
    keys = keys or order
    return ''.join(card(services[key][lang]['name'], services[key][lang]['summary'], routes[lang][key], label) for key in keys)


def render_chips(items):
    return '<div class="chip-list">' + ''.join(f'<span class="chip">{esc(item)}</span>' for item in items) + '</div>'


def render_service_chip_links(lang, keys):
    return '<div class="chip-list service-chip-links">' + ''.join(
        f'<a class="chip" href="{routes[lang][key]}">{esc(services[key][lang]["name"])}</a>'
        for key in keys
    ) + '</div>'


def render_home_points(lang):
    point_keys = (
        'security-camera-systems',
        'access-control-systems',
        'commercial-wifi-installation',
        'ip-phone-systems',
        'structured-cabling',
        'network-infrastructure',
    )
    items = []
    for text, key in zip(T[lang]['home_points'], point_keys):
        items.append(f'<li><a href="{routes[lang][key]}">{esc(text)}</a></li>')
    return f'<ul class="hero-points">{"".join(items)}</ul>'


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
    return (
        f'<section><div class="service-carousel" data-service-carousel>'
        f'<div class="service-carousel-header"><div class="section-heading"><p class="eyebrow">{esc(T[lang]["services"])}</p>'
        f'<h2>{esc(heading)}</h2><p>{esc(T[lang]["related_intro"])}</p></div>'
        f'<div class="service-carousel-controls"><button class="service-carousel-button" type="button" data-carousel-prev aria-label="{esc(ui["prev"])}">&larr;</button>'
        f'<button class="service-carousel-button" type="button" data-carousel-next aria-label="{esc(ui["next"])}">&rarr;</button></div></div>'
        f'<div class="service-carousel-track" data-carousel-track>{cards}</div></div></section>'
    )


def home_visual_panel(lang):
    visual = home_visuals[lang]
    title_html = f'<h2>{esc(visual["title"])}</h2>' if visual['title'] else ''
    return (
        f'<aside class="hero-panel hero-media-panel"><p class="eyebrow">{esc(visual["eyebrow"])}</p>'
        f'{title_html}'
        f'<div class="hero-media-stack">'
        f'<figure class="hero-media-main"><div class="hero-media-frame">{content_img(HOME_BUILDING_URL, visual["top_alt"], HOME_BUILDING_WIDTH, HOME_BUILDING_HEIGHT, "hero-media-main-image", eager=True, zoomable=True, lang=lang, caption=visual["top_title"])}</div>'
        f'<figcaption class="hero-media-caption"><strong>{esc(visual["top_title"])}</strong><span>{esc(visual["top_copy"])}</span></figcaption></figure>'
        f'<figure class="hero-media-main"><div class="hero-media-frame">{content_img(HOME_RACK_URL, visual["main_alt"], HOME_RACK_WIDTH, HOME_RACK_HEIGHT, "hero-media-main-image", eager=True, zoomable=True, lang=lang, caption=visual["main_title"])}</div>'
        f'<figcaption class="hero-media-caption"><strong>{esc(visual["main_title"])}</strong><span>{esc(visual["main_copy"])}</span></figcaption></figure>'
        f'</div></aside>'
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


def schema(lang, page_key, title, desc, faq_items=None, service_name=None, breadcrumb_items=None):
    page_url = absolute_url(routes[lang][page_key])
    catalog = offer_catalog_schema(lang)
    business = {
        '@type': 'ProfessionalService',
        '@id': BUSINESS_ID,
        'name': 'Opticable',
        'url': absolute_url(default_route('home')),
        'logo': absolute_url(LOGO_LOCKUP_URL),
        'image': absolute_url(LOGO_LOCKUP_URL),
        'description': T[lang]['company'],
        'serviceType': [services[k][lang]['name'] for k in order],
        'areaServed': AREA_SERVED_SCHEMA,
        'availableLanguage': [language_tag('en'), language_tag('fr')],
        'openingHoursSpecification': OPENING_HOURS_SPEC,
        'hasOfferCatalog': {'@id': catalog['@id']},
    }
    contact = contact_details(lang)
    if contact.get('general_email'):
        business['email'] = contact['general_email']
    if contact.get('phone'):
        business['telephone'] = contact['phone']
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
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=2)


def header(lang, current, page_key):
    t = T[lang]
    alt = 'fr' if lang == 'en' else 'en'
    nav = []
    for key in ('home', 'services', 'industries', 'about', 'faq', 'contact'):
        current_attr = ' aria-current="page"' if current == key else ''
        nav.append(f'<a href="{routes[lang][key]}"{current_attr}>{esc(t[key])}</a>')
    return f'<header class="site-header"><div class="header-inner"><a class="brand" href="{routes[lang]["home"]}" aria-label="Opticable {esc(t["home"]).lower()}">{logo_img("header")}</a><button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="site-nav">{esc(t["menu"])}</button><nav class="site-nav" id="site-nav" data-site-nav aria-label="Primary navigation">{"".join(nav)}</nav><div class="header-actions"><a class="lang-switch" href="{routes[alt][page_key]}" lang="{language_tag(alt)}">{esc(t["switch"])}</a><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a></div></div></header>'


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
    quick = ''.join(f'<li><a href="{routes[lang][k]}">{esc(t[k])}</a></li>' for k in ('home', 'services', 'about', 'contact', 'privacy'))
    feat = ''.join(f'<li><a href="{routes[lang][k]}">{esc(services[k][lang]["name"])}</a></li>' for k in order[:4])
    contact_items = footer_contact_items(lang)
    return f'<footer class="site-footer"><div class="footer-grid"><div><div class="footer-brand">{logo_img("footer")}</div><p class="footer-note">{esc(t["footer"])}</p></div><div><p class="footer-title">{esc(t["footer_contact_title"])}</p><ul class="footer-contact-list">{contact_items}</ul></div><div><p class="footer-title">{esc(t["contact"])}</p><ul class="footer-links">{quick}</ul></div><div><p class="footer-title">{esc(t["services"])}</p><ul class="footer-services">{feat}</ul></div></div><div class="footer-bottom">&copy; <span data-year></span> Opticable.</div></footer>'


def cta(lang):
    t = T[lang]
    return f'<section class="cta-band"><div><p class="eyebrow">{esc(t["cta_kicker"])}</p><h2>{esc(t["cta_title"])}</h2><p>{esc(t["cta_copy"])}</p></div><div class="cta-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["all_services"])}</a></div></section>'


def page(lang, key, current, title, desc, body, faq_items=None, service_name=None, breadcrumb_items=None, robots='index, follow'):
    t = T[lang]
    canonical_url = absolute_url(routes[lang][key])
    default_url = absolute_url(default_route(key))
    og_image_url = absolute_url(LOGO_LOCKUP_URL)
    return f'<!doctype html><html lang="{language_tag(lang)}"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>{esc(title)}</title><meta name="description" content="{esc(desc)}" /><meta name="robots" content="{esc(robots)}" /><meta name="theme-color" content="#153628" /><link rel="canonical" href="{canonical_url}" /><link rel="alternate" hreflang="{language_tag("en")}" href="{absolute_url(routes["en"][key])}" /><link rel="alternate" hreflang="{language_tag("fr")}" href="{absolute_url(routes["fr"][key])}" /><link rel="alternate" hreflang="x-default" href="{default_url}" /><meta property="og:type" content="website" /><meta property="og:site_name" content="Opticable" /><meta property="og:locale" content="{t["locale"]}" /><meta property="og:title" content="{esc(title)}" /><meta property="og:description" content="{esc(desc)}" /><meta property="og:url" content="{canonical_url}" /><meta property="og:image" content="{og_image_url}" /><meta property="og:image:alt" content="Opticable logo" /><meta property="og:image:width" content="{LOGO_LOCKUP_WIDTH}" /><meta property="og:image:height" content="{LOGO_LOCKUP_HEIGHT}" /><meta name="twitter:card" content="summary_large_image" /><meta name="twitter:title" content="{esc(title)}" /><meta name="twitter:description" content="{esc(desc)}" /><meta name="twitter:image" content="{og_image_url}" /><meta name="twitter:image:alt" content="Opticable logo" /><link rel="icon" type="image/svg+xml" href="{LOGO_MARK_URL}" />{resource_hints(key)}<link rel="stylesheet" href="{STYLES_URL}" /><script type="application/ld+json">{schema(lang, key, title, desc, faq_items, service_name, breadcrumb_items)}</script></head><body><a class="skip-link" href="#content">{esc(t["skip"])}</a><div class="site-shell">{header(lang, current, key)}{cookie_banner(lang)}<main id="content">{body}</main>{footer(lang)}</div>{image_lightbox(lang)}<script src="{SCRIPT_URL}" defer></script></body></html>'


def legacy_redirect_html(target, title, desc, lang='fr'):
    return (
        f'<!doctype html><html lang="{language_tag(lang)}"><head><meta charset="UTF-8" />'
        f'<meta http-equiv="refresh" content="0; url={target}" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />'
        f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}" />'
        f'<meta name="robots" content="noindex, follow" /><meta name="theme-color" content="#153628" />'
        f'<link rel="canonical" href="{absolute_url(target)}" />'
        f'<link rel="alternate" hreflang="{language_tag("fr")}" href="{absolute_url(routes["fr"]["home"])}" />'
        f'<link rel="alternate" hreflang="{language_tag("en")}" href="{absolute_url(routes["en"]["home"])}" />'
        f'<link rel="alternate" hreflang="x-default" href="{absolute_url(default_route("home"))}" />'
        f'<meta property="og:type" content="website" /><meta property="og:site_name" content="Opticable" />'
        f'<meta property="og:locale" content="{T[lang]["locale"]}" /><meta property="og:title" content="{esc(title)}" />'
        f'<meta property="og:description" content="{esc(desc)}" /><meta property="og:url" content="{absolute_url(target)}" />'
        f'<meta property="og:image" content="{absolute_url(LOGO_LOCKUP_URL)}" /><meta property="og:image:alt" content="Opticable logo" />'
        f'<meta property="og:image:width" content="{LOGO_LOCKUP_WIDTH}" /><meta property="og:image:height" content="{LOGO_LOCKUP_HEIGHT}" />'
        f'<meta name="twitter:card" content="summary_large_image" /><meta name="twitter:title" content="{esc(title)}" />'
        f'<meta name="twitter:description" content="{esc(desc)}" /><meta name="twitter:image" content="{absolute_url(LOGO_LOCKUP_URL)}" />'
        f'<meta name="twitter:image:alt" content="Opticable logo" /><link rel="icon" type="image/svg+xml" href="{LOGO_MARK_URL}" />'
        f'<link rel="stylesheet" href="{STYLES_URL}" /></head><body><div class="gateway-shell"><section class="gateway-panel">'
        f'<div><div class="gateway-brand">{logo_img("gateway")}</div><p>{esc(T[lang]["company"])}</p>'
        f'<p class="eyebrow">{esc("Redirection" if lang == "fr" else "Redirect")}</p>'
        f'<h1>{esc(title)}</h1><p>{esc(desc)}</p></div><div class="hero-actions">'
        f'<a class="button button-primary" href="{target}">{esc("Continuer" if lang == "fr" else "Continue")}</a></div></section></div></body></html>'
    )


def process_section(lang):
    items = ''.join(f'<article class="timeline-step"><span>{i:02d}</span><h3>{esc(title)}</h3><p>{esc(copy)}</p></article>' for i, (title, copy) in enumerate(T[lang]['process'], start=1))
    return f'<div class="timeline">{items}</div>'

def clients_section(lang):
    return f'<div class="grid-4">{"".join(card(title, text) for title, text in T[lang]["clients"])}</div>'

def industries_section(lang):
    return f'<div class="grid-3">{"".join(card(title, text) for title, text in industry_cards[lang])}</div>'

def coverage_section(lang):
    t = T[lang]
    return (
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["service_area_eyebrow"])}</p>'
        f'<h2>{esc(t["service_area_title"])}</h2><p>{esc(t["service_area_intro"])}</p></div>'
        f'{render_chips(t["service_area_regions"])}</section>'
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
        block = (
            f'<section><div class="section-heading"><p class="eyebrow">FAQ</p><h2>{esc(title)}</h2><p>{esc(intro)}</p></div>'
            f'<div class="faq-list">{faq_items}</div></section>'
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
(DEPLOY_ASSET_ROOT / 'styles.css').write_text(css.strip() + '\n', encoding='utf-8')
(DEPLOY_ASSET_ROOT / 'site.js').write_text(js.strip() + '\n', encoding='utf-8')

for lang in ('en', 'fr'):
    t = T[lang]
    contact_panel_title = t.get('contact_panel_title', t['contact_info_title'])
    contact_panel_copy = t.get('contact_panel_copy', t['contact_intro'])
    primary_cards = service_cards(lang, t['service_label'], primary_order)
    secondary_cards = service_cards(lang, t['service_label'], secondary_order)
    details = ''.join(f'<div class="detail-item"><strong>{esc(a)}</strong><p>{contact_value_html(a, b)}</p></div>' for a, b in t['contact_cards'])

    home_body = (
        f'<section class="hero hero-media-layout"><div class="hero-copy"><p class="eyebrow">{esc(t["home_kicker"])}</p>'
        f'<h1>{esc(t["home_h1"])}</h1><p>{esc(t["home_intro"])}</p>'
        f'<div class="hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a>'
        f'<a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["all_services"])}</a></div>'
        f'{render_home_points(lang)}</div>'
        f'{home_visual_panel(lang)}</section>'
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["trust_title"])}</p><h2>{esc(t["trust_title"])}</h2><p>{esc(t["company"])}</p></div><div class="grid-4">{"".join(card(a, b) for a, b in t["trust"])}</div></section>'
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(t["priority_title"])}</h2><p>{esc(t["priority_intro"])}</p></div><div class="grid-2">{primary_cards}</div></section>'
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(t["support_title"])}</h2><p>{esc(t["support_intro"])}</p></div><div class="grid-2">{secondary_cards}</div></section>'
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["industries"])}</p><h2>{esc(t["industries_h1"])}</h2><p>{esc(t["industries_intro"])}</p></div>{industries_section(lang)}</section>'
        f'{cta(lang)}'
    )
    write_url(routes[lang]['home'], page(lang, 'home', 'home', t['home_title'], t['home_desc'], home_body))

    services_breadcrumbs = [(t['home'], routes[lang]['home']), (t['services'], routes[lang]['services'])]
    services_body = (
        f'{breadcrumb_nav(services_breadcrumbs)}'
        f'<section class="page-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(t["services"])}</p><h1>{esc(t["services_h1"])}</h1><p>{esc(t["services_intro"])}</p>'
        f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["about"]}">{esc(t["about"])}</a></div></div>'
        f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["tagline"])}</p><h2>{esc(t["company"])}</h2>{render_service_chip_links(lang, services_page_chip_keys)}</aside></section>'
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(t["priority_title"])}</h2><p>{esc(t["priority_intro"])}</p></div><div class="grid-2">{primary_cards}</div></section>'
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(t["support_title"])}</h2><p>{esc(t["support_intro"])}</p></div><div class="grid-2">{secondary_cards}</div></section>'
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(t["extra_title"])}</h2><p>{esc(t["extra_intro"])}</p></div><div class="grid-3">{"".join(card(a, b) for a, b in t["extras"])}</div></section>'
        f'{cta(lang)}'
    )
    write_url(routes[lang]['services'], page(lang, 'services', 'services', t['services_title'], t['services_desc'], services_body, breadcrumb_items=services_breadcrumbs))

    about_breadcrumbs = [(t['home'], routes[lang]['home']), (t['about'], routes[lang]['about'])]
    about_body = (
        f'{breadcrumb_nav(about_breadcrumbs)}'
        f'<section class="page-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(t["about"])}</p><h1>{esc(t["about_h1"])}</h1><p>{esc(t["about_intro"])}</p>'
        f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["services"])}</a></div></div>'
        f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["tagline"])}</p><h2>{esc(t["about_story"])}</h2>{about_panel_media(lang)}</aside></section>'
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["about"])}</p><h2>{esc(t.get("about_section_title", t["about_h1"]))}</h2><p>{esc(t.get("about_section_intro", t["about_story"]))}</p></div><div class="grid-4">{"".join(card(a, b) for a, b in t["about_values"])}</div></section>'
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["industries"])}</p><h2>{esc(t["clients_title"])}</h2><p>{esc(t["clients_intro"])}</p></div>{clients_section(lang)}</section>'
        f'{cta(lang)}'
    )
    write_url(routes[lang]['about'], page(lang, 'about', 'about', t['about_title'], t['about_desc'], about_body, breadcrumb_items=about_breadcrumbs))

    contact_breadcrumbs = [(t['home'], routes[lang]['home']), (t['contact'], routes[lang]['contact'])]
    contact_body = (
        f'{breadcrumb_nav(contact_breadcrumbs)}'
        f'<section class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(t["contact"])}</p><h1>{esc(t["contact_h1"])}</h1><p>{esc(t["contact_intro"])}</p></div></section>'
        f'<section class="contact-layout"><div class="contact-panel contact-sidebar"><h2>{esc(contact_panel_title)}</h2><p>{esc(contact_panel_copy)}</p><div class="detail-list">{details}</div></div>{form_section(lang)}</section>'
        f'{coverage_section(lang)}'
        f'{cta(lang)}'
    )
    write_url(routes[lang]['contact'], page(lang, 'contact', 'contact', t['contact_title'], t['contact_desc'], contact_body, breadcrumb_items=contact_breadcrumbs))

    thanks_breadcrumbs = [(t['home'], routes[lang]['home']), (t['thanks'], routes[lang]['thanks'])]
    thanks_steps_html = ''.join(f'<li>{esc(item)}</li>' for item in t['thanks_steps'])
    thanks_body = (
        f'{breadcrumb_nav(thanks_breadcrumbs)}'
        f'<section class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(t["thanks"])}</p><h1>{esc(t["thanks_h1"])}</h1><p>{esc(t["thanks_intro"])}</p>'
        f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["home"]}">{esc(t["thanks_return_home"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["thanks_view_services"])}</a></div></div></section>'
        f'<section class="two-col"><div class="contact-panel"><p class="eyebrow">{esc(t["thanks"])}</p><h2>{esc(t["thanks_panel_title"])}</h2><p>{esc(t["thanks_panel_copy"])}</p><ul class="check-list">{thanks_steps_html}</ul></div><div class="contact-panel"><p class="eyebrow">{esc(t["contact"])}</p><h2>{esc(t["footer_contact_title"])}</h2><div class="detail-list">{details}</div></div></section>'
    )
    write_url(routes[lang]['thanks'], page(lang, 'thanks', 'contact', t['thanks_title'], t['thanks_desc'], thanks_body, breadcrumb_items=thanks_breadcrumbs, robots='noindex, nofollow'))

    privacy_cards_html = ''.join(card(title, copy) for title, copy in t['privacy_cards'])
    privacy_choices_html = ''.join(f'<li>{esc(item)}</li>' for item in t['privacy_choices'])
    privacy_breadcrumbs = [(t['home'], routes[lang]['home']), (t['privacy'], routes[lang]['privacy'])]
    privacy_body = (
        f'{breadcrumb_nav(privacy_breadcrumbs)}'
        f'<section class="page-hero contact-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(t["privacy"])}</p><h1>{esc(t["privacy_h1"])}</h1><p>{esc(t["privacy_intro"])}</p></div></section>'
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["privacy"])}</p><h2>{esc(t["privacy_cards_title"])}</h2><p>{esc(t["privacy_cards_intro"])}</p></div><div class="privacy-grid">{privacy_cards_html}</div></section>'
        f'<section class="two-col"><div class="contact-panel"><p class="eyebrow">{esc(t["privacy"])}</p><h2>{esc(t["privacy_choices_title"])}</h2><ul class="check-list">{privacy_choices_html}</ul></div><div class="contact-panel"><p class="eyebrow">{esc(t["contact"])}</p><h2>{esc(t["footer_contact_title"])}</h2><p>{esc(t["footer_contact_intro"])}</p><div class="detail-list">{details}</div></div></section>'
    )
    write_url(routes[lang]['privacy'], page(lang, 'privacy', 'privacy', t['privacy_title'], t['privacy_desc'], privacy_body, breadcrumb_items=privacy_breadcrumbs))

    industries_breadcrumbs = [(t['home'], routes[lang]['home']), (t['industries'], routes[lang]['industries'])]
    industries_body = (
        f'{breadcrumb_nav(industries_breadcrumbs)}'
        f'<section class="page-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(t["industries"])}</p><h1>{esc(t["industries_h1"])}</h1><p>{esc(t["industries_intro"])}</p>'
        f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["services"])}</a></div></div>'
        f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["industries"])}</p><h2>{esc(t.get("industries_panel_title", t["company"]))}</h2><p>{esc(t.get("industries_panel_copy", t["industries_intro"]))}</p></aside></section>'
        f'<section><div class="section-heading"><p class="eyebrow">{esc(t["industries"])}</p><h2>{esc(t["industries_h1"])}</h2><p>{esc(t["industries_intro"])}</p></div>{industries_section(lang)}</section>'
        f'{coverage_section(lang)}'
        f'{cta(lang)}'
    )
    write_url(routes[lang]['industries'], page(lang, 'industries', 'industries', t['industries_title'], t['industries_desc'], industries_body, breadcrumb_items=industries_breadcrumbs))

    faq_breadcrumbs = [(t['home'], routes[lang]['home']), ('FAQ', routes[lang]['faq'])]
    faq_body = (
        f'{breadcrumb_nav(faq_breadcrumbs)}'
        f'<section class="page-hero"><div class="page-hero-copy"><p class="eyebrow">FAQ</p><h1>{esc(t["faq_h1"])}</h1><p>{esc(t["faq_intro"])}</p></div>'
        f'<aside class="page-hero-panel"><p class="eyebrow">FAQ</p><h2>{esc(t.get("faq_panel_title", t["faq_h1"]))}</h2><p>{esc(t.get("faq_panel_copy", t["faq_intro"]))}</p></aside></section>'
        f'{faq_sections(lang)}'
        f'{cta(lang)}'
    )
    write_url(routes[lang]['faq'], page(lang, 'faq', 'faq', t['faq_title'], t['faq_desc'], faq_body, faq_items=flat_faq_items(lang), breadcrumb_items=faq_breadcrumbs))

    for key in order:
        s = services[key][lang]
        related = related_services_carousel(lang, key, s['related'], t['service_label'])
        service_breadcrumbs = [(t['home'], routes[lang]['home']), (t['services'], routes[lang]['services']), (s['name'], routes[lang][key])]
        panel_extra = service_panel_media(key, lang) or render_chips([s["name"], services[s["related"][0]][lang]["name"], services[s["related"][1]][lang]["name"]])
        body = (
            f'{breadcrumb_nav(service_breadcrumbs)}'
            f'<section class="page-hero"><div class="page-hero-copy"><p class="eyebrow">{esc(s["name"])}</p><h1>{esc(s["hero"])}</h1><p>{esc(s["intro"])}</p>'
            f'<div class="page-hero-actions"><a class="button button-primary" href="{routes[lang]["contact"]}">{esc(t["quote"])}</a><a class="button button-secondary" href="{routes[lang]["services"]}">{esc(t["all_services"])}</a></div></div>'
            f'<aside class="page-hero-panel"><p class="eyebrow">{esc(t["services"])}</p><h2>{esc(s["summary"])}</h2>{panel_extra}</aside></section>'
            f'<section><div class="section-heading"><p class="eyebrow">{esc("Service overview" if lang == "en" else "Vue d\'ensemble du service")}</p><h2>{esc(s["name"])}</h2><p>{esc(t["overview_intro"])}</p></div><div class="two-col"><div class="contact-panel service-detail-panel"><p class="eyebrow">{esc("Included work" if lang == "en" else "Travaux inclus")}</p><h2>{esc("What the scope can include" if lang == "en" else "Ce qu\'on peut inclure dans les travaux")}</h2><ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in s["includes"])}</ul></div><div class="contact-panel service-detail-panel"><p class="eyebrow">{esc("Benefits" if lang == "en" else "Avantages")}</p><h2>{esc("Benefits" if lang == "en" else "Ce que ce service apporte")}</h2><ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in s["benefits"])}</ul></div></div></section>'
            f'<section><div class="section-heading"><p class="eyebrow">{esc("Typical use cases" if lang == "en" else "Exemples concrets")}</p><h2>{esc("Typical use cases" if lang == "en" else "Cas d\'usage")}</h2><p>{esc(s["summary"])}</p></div><div class="two-col"><div class="contact-panel"><ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in s["cases"])}</ul></div><div class="contact-panel service-apply-panel"><p class="eyebrow">{esc("Industries served" if lang == "en" else "Types d\'immeubles")}</p><h2>{esc("Industries served" if lang == "en" else "Ou ce service s\'applique")}</h2><ul class="check-list">{"".join(f"<li>{esc(item)}</li>" for item in s["industries"])}</ul></div></div></section>'
            f'{related}'
            f'{cta(lang)}'
        )
        write_url(routes[lang][key], page(lang, key, 'services', s['title'], s['desc'], body, service_name=s['name'], breadcrumb_items=service_breadcrumbs))

write_url('/fr/', legacy_redirect_html('/', 'Redirection vers la page d accueil française', "La page d accueil française est maintenant servie directement à la racine du site.", lang='fr'))
(DEPLOY_ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /.playwright-cli/\nDisallow: /output/\nDisallow: /__pycache__/\nSitemap: ' + absolute_url('/sitemap.xml') + '\n', encoding='utf-8')
(DEPLOY_ROOT / 'sitemap.xml').write_text(sitemap_xml(), encoding='utf-8')
