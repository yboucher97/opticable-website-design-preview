def _article(path, title, desc, eyebrow, headline, intro, excerpt, tags, primary_service, summary, sections, faq_items, cta):
    return {
        "path": path,
        "title": title,
        "desc": desc,
        "eyebrow": eyebrow,
        "headline": headline,
        "intro": intro,
        "excerpt": excerpt,
        "tags": tags,
        "primary_service": primary_service,
        "summary": summary,
        "sections": sections,
        "faq_items": faq_items,
        "cta": cta,
    }


def _cta(title, copy, primary_label, primary_key, secondary_label, secondary_key):
    return {
        "title": title,
        "copy": copy,
        "primary_label": primary_label,
        "primary_key": primary_key,
        "secondary_label": secondary_label,
        "secondary_key": secondary_key,
    }


EN_GUIDE_ARTICLES = {}

EN_GUIDE_ARTICLES["camera-system-pricing-commercial-building"] = _article(
    "/en/guides/camera-system-pricing-commercial-building/",
    "Commercial Camera System Pricing | Opticable",
    "Typical commercial camera system pricing, what changes the quote, and what to confirm before asking for a realistic price.",
    "Buying guide",
    "How much does a camera system cost for a commercial building?",
    "A simple commercial camera scope often starts around C$3,500 to C$7,500. Larger systems with more cameras, PoE switching, NVR storage, exterior zones, cabling, and commissioning often move into the C$8,000 to C$25,000+ range. The real price depends on camera count, cable paths, building access, retention, and site conditions.",
    "Commercial camera pricing is not only about camera count. Cabling, PoE, storage, mounting, access, and commissioning drive the real quote.",
    ["Security cameras", "Commercial building", "Pricing"],
    "security-camera-systems",
    [
        ("Typical range", "Small scopes often start around C$3,500 to C$7,500; larger systems can reach C$8,000 to C$25,000+."),
        ("Cost drivers", "Camera count, cable paths, exterior areas, NVR storage, PoE capacity, and building access."),
        ("Best next step", "Ask for a quote that separates cameras, cabling, recording, retention, commissioning, and site constraints."),
    ],
    [
        {
            "eyebrow": "Direct answer",
            "title": "Think in complete system scope",
            "paragraphs": [
                "A camera system quote should cover the full installed system, not only the devices. The scope usually includes cameras, cable runs, PoE power, recording, storage, mounting, configuration, testing, and user handoff.",
                "A few cameras at one entrance are not the same project as multiple doors, corridors, stairwells, parking areas, and a technical room. The more the building conditions matter, the less useful a simple per-camera price becomes.",
            ],
            "callout_label": "Budget note",
            "callout": "For planning, budget the installed system rather than the camera price alone.",
        },
        {
            "eyebrow": "Budget",
            "title": "Common project ranges",
            "table": {
                "caption": "Indicative ranges for commercial camera systems",
                "columns": ("Scope", "Typical work", "Indicative budget", "When it applies"),
                "rows": (
                    ("Simple scope", "4 to 6 cameras, entrance and common area", "C$3,500 to C$7,500", "Small office, retail space, or limited coverage"),
                    ("Intermediate scope", "8 to 16 cameras, interior and exterior zones", "C$8,000 to C$15,000", "Several entrances, parking, corridors, or sensitive zones"),
                    ("Extended scope", "16+ cameras and heavier retention", "C$15,000 to C$25,000+", "Larger commercial, multi-tenant, or multi-zone buildings"),
                ),
            },
        },
        {
            "eyebrow": "Variables",
            "title": "What moves the quote",
            "cards": [
                ("Camera count", "More cameras require more cable, ports, power, storage, configuration, and testing."),
                ("Cable paths", "Long paths, finished ceilings, drilling, and occupied areas increase labour."),
                ("Retention", "More days of footage and higher resolution change recorder and storage requirements."),
                ("Exterior coverage", "Parking and outdoor entrances require suitable mounts, weather protection, and positioning."),
                ("Building access", "Evening work, tenant coordination, and restricted rooms add planning time."),
                ("Integration", "Access control, intercom, or network limits can expand the technical scope."),
            ],
        },
        {
            "eyebrow": "Preparation",
            "title": "What to confirm before requesting a quote",
            "steps": [
                ("List the zones", "Entrances, corridors, parking, loading areas, stairwells, technical rooms, or common spaces."),
                ("Confirm floors and access points", "Doors, levels, and technical rooms affect cable paths and labour."),
                ("Decide on retention", "Know roughly how many days of footage you want to keep."),
                ("Expect a site visit", "A visit confirms paths, PoE capacity, mounting locations, and real constraints."),
            ],
        },
    ],
    [
        ("Can you price only by camera?", "Not reliably. A camera count does not capture cabling, storage, mounting, labour, access, or commissioning."),
        ("Is an NVR always required?", "Most commercial projects need a recording plan. The recorder, retention period, and user access should be defined before quoting."),
        ("Why do two similar buildings cost different amounts?", "Cable paths, ceilings, exterior areas, working hours, and technical-room conditions can be completely different."),
        ("How do I get a reliable quote?", "Send the building type, zones to cover, number of floors, key entrances, and timing. A site visit is usually the best basis."),
    ],
    _cta("Want a realistic camera system quote?", "Tell us about the building, areas to cover, and timeline. We will help define the right scope before pricing.", "Request a quote", "contact", "See camera systems", "security-camera-systems"),
)

EN_GUIDE_ARTICLES["access-control-vs-intercom"] = _article(
    "/en/guides/access-control-vs-intercom/",
    "Access Control vs Intercom | Opticable",
    "The difference between access control and intercom systems, when each one is useful, and when both should work together.",
    "Comparison guide",
    "Access control or intercom: what does your building actually need?",
    "Access control manages who is allowed through a door. An intercom manages how a visitor requests entry. In many commercial and multi-tenant buildings, the right solution is both: access control for authorized users and an intercom for visitors, deliveries, and exceptions.",
    "Access control and intercoms solve different problems. The strongest entrance setup often combines both.",
    ["Access control", "Intercom", "Entrances"],
    "access-control-systems",
    [
        ("Access control", "Best for staff, residents, tenants, and authorized users who should open doors without calling someone."),
        ("Intercom", "Best for visitors, deliveries, and situations where someone must verify before opening."),
        ("Combined system", "Often the best approach for shared entrances, multi-tenant buildings, and commercial sites."),
    ],
    [
        {
            "eyebrow": "Difference",
            "title": "They do not solve the same problem",
            "paragraphs": [
                "Access control answers who is allowed to open a door, at what time, and with what credential. It is about permissions, schedules, users, and history.",
                "An intercom answers how someone without a credential requests entry, and who decides whether to unlock the door. It is about visitor handling and verification.",
            ],
            "callout_label": "Simple rule",
            "callout": "Use access control for known users. Use an intercom for visitors and exceptions.",
        },
        {
            "eyebrow": "Use cases",
            "title": "When each option fits",
            "table": {
                "caption": "Access control versus intercom",
                "columns": ("Need", "Best fit", "Why"),
                "rows": (
                    ("Employees or tenants need daily access", "Access control", "Users enter with credentials and schedules."),
                    ("Visitors need to request entry", "Intercom", "Someone can answer, verify, and unlock."),
                    ("Shared main entrance", "Both", "Known users enter directly while visitors use the intercom."),
                    ("Back door or technical room", "Access control", "Visitor communication is usually not needed."),
                ),
            },
        },
        {
            "eyebrow": "Design",
            "title": "What to decide before quoting",
            "cards": [
                ("Door count", "Count main entrances, back doors, garages, and restricted rooms separately."),
                ("Visitor flow", "Clarify who answers visitors and what happens outside business hours."),
                ("Credentials", "Badges, fobs, mobile credentials, PINs, and schedules change the system design."),
                ("Remote management", "Some buildings need managers to update users or unlock remotely."),
                ("Camera coverage", "Video at the door may be useful even when the intercom is audio-only."),
                ("Existing hardware", "Door hardware and wiring can strongly affect installation complexity."),
            ],
        },
    ],
    [
        ("Can an intercom replace access control?", "Usually no. It helps visitors request entry, but it does not replace controlled daily access for authorized users."),
        ("Can access control unlock from an intercom?", "Often yes, if the system is designed and wired for it."),
        ("Do all doors need both systems?", "No. Main entrances often need both, while back doors and technical rooms may only need access control."),
        ("What should I send for a quote?", "Send the number of doors, entrance type, visitor flow, existing hardware, and whether remote management is needed."),
    ],
    _cta("Need help choosing the right entrance setup?", "Describe the building, entrances, and how visitors are handled today. We will help identify the cleanest scope.", "Request a quote", "contact", "See access control", "access-control-systems"),
)

EN_GUIDE_ARTICLES["commercial-wifi-audit-checklist"] = _article(
    "/en/guides/commercial-wifi-audit-checklist/",
    "Commercial WiFi Audit Checklist | Opticable",
    "A practical checklist for reviewing commercial WiFi coverage, reliability, capacity, cabling, and access point placement.",
    "Checklist",
    "Commercial WiFi audit checklist before adding access points",
    "Weak commercial WiFi is not always solved by adding more access points. Coverage, interference, cabling, switching, user density, mounting, and configuration all affect the result. A basic audit separates signal problems from network, capacity, or installation problems.",
    "Before adding access points, confirm coverage, interference, cabling, switch capacity, placement, and user density.",
    ["Commercial WiFi", "Audit", "Checklist"],
    "commercial-wifi-installation",
    [
        ("Coverage", "Map where WiFi is weak, unstable, or overloaded."),
        ("Infrastructure", "Check cabling, PoE, switching, VLANs, and uplinks."),
        ("Placement", "Access point location and mounting matter as much as model selection."),
    ],
    [
        {
            "eyebrow": "Before adding hardware",
            "title": "Start with the real symptom",
            "paragraphs": [
                "A WiFi complaint can mean weak signal, overloaded access points, poor roaming, bad cabling, interference, incorrect configuration, or an internet issue.",
                "A commercial space also changes over time. Shelving, walls, equipment, users, tenants, and point-of-sale systems can make a design that once worked feel unreliable today.",
            ],
            "callout_label": "Audit first",
            "callout": "Adding access points without checking cabling and placement can make a bad WiFi environment harder to manage.",
        },
        {
            "eyebrow": "Checklist",
            "title": "What to verify",
            "steps": [
                ("Mark weak zones", "Identify rooms, aisles, offices, counters, or common areas where service drops."),
                ("Check AP locations", "Look for devices hidden above ceilings, mounted too low, or blocked by materials."),
                ("Confirm cabling and PoE", "A bad cable or underpowered switch can look like a WiFi problem."),
                ("Review client types", "POS terminals, scanners, phones, laptops, guests, and staff do not all behave the same."),
                ("Check interference", "Metal, concrete, neighbouring networks, and equipment can affect performance."),
            ],
        },
        {
            "eyebrow": "Common causes",
            "title": "Problems we see often",
            "cards": [
                ("Wrong placement", "Access points were installed where cabling was easy, not where coverage was needed."),
                ("Too many SSIDs", "A cluttered configuration creates overhead and confusion."),
                ("Old cabling", "The network drop feeding the access point is unstable or not tested."),
                ("Insufficient PoE", "The switch cannot properly power the device or newer model."),
                ("Dense zones", "Meeting rooms, counters, or waiting areas need capacity planning."),
                ("No documentation", "Nobody knows which access point serves which area."),
            ],
        },
    ],
    [
        ("Do I always need more access points?", "No. Sometimes the problem is placement, cabling, switch power, interference, or configuration."),
        ("Can you work in occupied spaces?", "Yes. Commercial WiFi work is often planned around operating hours and active users."),
        ("Should guest WiFi be separate?", "Usually yes. Guest access should be separated from business systems when appropriate."),
        ("What helps you quote faster?", "Send floor areas, weak zones, access point count, network-room photos, and the devices that depend on WiFi."),
    ],
    _cta("Need a clearer WiFi plan?", "Tell us where WiFi fails and what systems depend on it. We will help identify whether the issue is coverage, cabling, or configuration.", "Request a WiFi review", "contact", "See commercial WiFi", "commercial-wifi-installation"),
)

EN_GUIDE_ARTICLES["cat6a-or-fiber-commercial-building"] = _article(
    "/en/guides/cat6a-or-fiber-commercial-building/",
    "Cat6A or Fiber for a Commercial Building | Opticable",
    "How to choose between Cat6A and fiber for commercial cabling, uplinks, floors, equipment rooms, and longer network runs.",
    "Decision guide",
    "Cat6A or fiber: which makes sense for your commercial building?",
    "Cat6A is often the right choice for horizontal drops to workstations, cameras, access points, and many devices. Fiber becomes more logical for longer distances, risers, links between telecom rooms, higher capacity backbones, and areas where copper limitations become a problem.",
    "Cat6A and fiber are not interchangeable. The right choice depends on distance, capacity, equipment rooms, and the role of the cable.",
    ["Cat6A", "Fiber optic", "Commercial cabling"],
    "structured-cabling",
    [
        ("Cat6A", "Best for many device drops and shorter structured cabling runs."),
        ("Fiber", "Best for backbone links, long distances, floors, telecom rooms, and higher capacity."),
        ("Design point", "Choose based on the role of the link, not only the cable price."),
    ],
    [
        {
            "eyebrow": "Simple distinction",
            "title": "Use each cable for the right role",
            "paragraphs": [
                "Cat6A is a strong choice for many commercial device connections because it supports high speeds over typical horizontal runs and can carry PoE.",
                "Fiber is usually the better backbone choice when you need to link floors, closets, buildings, long distances, or higher capacity paths.",
            ],
            "callout_label": "Rule of thumb",
            "callout": "Use Cat6A for many device drops. Use fiber for backbone, distance, and capacity.",
        },
        {
            "eyebrow": "Comparison",
            "title": "Where each option fits",
            "table": {
                "caption": "Cat6A versus fiber in commercial buildings",
                "columns": ("Situation", "Typical choice", "Reason"),
                "rows": (
                    ("Workstations, phones, cameras, access points", "Cat6A", "Supports device connections and PoE."),
                    ("Between telecom rooms or floors", "Fiber", "Better for backbone capacity and distance."),
                    ("Long run beyond copper limits", "Fiber", "Avoids practical copper distance limits."),
                    ("Device that needs PoE", "Cat6A", "Power and data can run on the same cable."),
                ),
            },
        },
        {
            "eyebrow": "Variables",
            "title": "What affects the decision",
            "cards": [
                ("Distance", "Copper has practical distance limits; fiber handles longer links better."),
                ("PoE needs", "Most PoE devices still need copper at the device end."),
                ("Telecom rooms", "More closets or floors can make fiber backbone planning more important."),
                ("Future capacity", "Fiber can protect the backbone from near-term growth issues."),
                ("Path conditions", "Conduit, risers, trays, and building access shape the install."),
                ("Budget timing", "The cheapest cable today may not be the cheapest infrastructure plan later."),
            ],
        },
    ],
    [
        ("Is fiber always better?", "No. Fiber is excellent for backbone and distance, but Cat6A remains practical for many endpoint drops."),
        ("Can fiber power devices?", "Not directly like PoE copper. Devices that need PoE usually require copper at the endpoint."),
        ("Should I install both?", "Many buildings use both: fiber between rooms or floors, Cat6A from closets to devices."),
        ("What information helps quote the work?", "Endpoints, distances, floors, existing pathways, rack locations, and devices being connected."),
    ],
    _cta("Need help choosing Cat6A, fiber, or both?", "Send the building layout, endpoint list, and distance concerns. We will help define the right cabling scope.", "Request a cabling quote", "contact", "See structured cabling", "structured-cabling"),
)

EN_GUIDE_ARTICLES["technology-retrofit-occupied-building"] = _article(
    "/en/guides/technology-retrofit-occupied-building/",
    "Technology Retrofit in an Occupied Building | Opticable",
    "How to plan cameras, access control, WiFi, cabling, and network upgrades in an occupied commercial building.",
    "Planning guide",
    "How to plan a technology retrofit in an occupied building",
    "Upgrading cameras, access control, intercom, WiFi, cabling, or network infrastructure in an occupied building requires more than a parts list. The plan must account for access, working hours, tenants, dust, noise, outages, temporary conditions, and a clean handoff.",
    "In occupied buildings, the work sequence matters as much as the equipment. Access, hours, communication, and phasing need to be planned.",
    ["Retrofit", "Occupied building", "Planning"],
    "structured-cabling",
    [
        ("Main issue", "The building stays active while technology systems are upgraded."),
        ("Planning focus", "Access, phasing, communication, outage windows, and safe work areas."),
        ("Best result", "A clear sequence that limits disruption and leaves systems documented."),
    ],
    [
        {
            "eyebrow": "Reality",
            "title": "The site stays in operation",
            "paragraphs": [
                "A retrofit is different from a new build because people, tenants, systems, and daily operations are already in place.",
                "The best plan protects operations while still giving the installer enough access to do the work properly.",
            ],
            "callout_label": "Important",
            "callout": "A good retrofit quote explains how the work will happen, not only what will be installed.",
        },
        {
            "eyebrow": "Before work starts",
            "title": "What to lock down",
            "cards": [
                ("Access", "Who opens ceilings, rooms, closets, electrical spaces, and restricted areas."),
                ("Working windows", "Daytime, evening, weekend, or phased work depending on building use."),
                ("Communication", "Who must be notified before work, outages, or temporary access changes."),
                ("Coordination", "How the work aligns with electricians, maintenance, security, or general contractors."),
                ("Pathways", "Which routes are available and which areas are off limits."),
                ("Handoff", "Testing, labels, documentation, and user training expectations."),
            ],
        },
        {
            "eyebrow": "Common scopes",
            "title": "Projects often handled this way",
            "steps": [
                ("Camera upgrades", "Replace old cameras while keeping key areas covered during transition."),
                ("Access-control expansion", "Add doors without disrupting authorized users more than necessary."),
                ("WiFi improvements", "Move or add access points while maintaining coverage for active users."),
                ("Network-room cleanup", "Clean up the rack before adding new services or equipment."),
                ("Cabling additions", "Add drops, pathways, or backbone links in phases."),
            ],
        },
    ],
    [
        ("Can this be done without closing the building?", "Often yes, but access, hours, and affected zones must be planned carefully."),
        ("Why is a site visit important?", "Cable paths, ceilings, closets, tenant constraints, and access rules cannot be evaluated reliably by email alone."),
        ("Can the work be phased?", "Yes. Phasing by floor, entrance, zone, or working window is often the best approach."),
        ("What helps you scope it?", "Building type, occupancy, systems involved, sensitive areas, permitted hours, and preferred phasing."),
    ],
    _cta("Planning a retrofit in an active building?", "Tell us which systems need to be upgraded and what constraints matter on site. We will help shape a practical sequence.", "Plan my project", "contact", "See structured cabling", "structured-cabling"),
)
EN_DECISION_ARTICLES = {}

EN_DECISION_ARTICLES["access-control-pricing-commercial-building"] = _article(
    "/en/guides/access-control-pricing-commercial-building/",
    "Commercial Access Control Pricing | Opticable",
    "Typical access control pricing for commercial doors, what changes the quote, and what to prepare before requesting pricing.",
    "Pricing guide",
    "How much does access control cost for a commercial building?",
    "A simple single-door commercial access-control scope often falls around C$2,500 to C$5,500. Multi-door systems with centralized management, schedules, intercom coordination, or occupied-building constraints can quickly move into the C$6,000 to C$20,000+ range.",
    "Access control pricing depends on doors, hardware, cabling, controller design, programming, and site conditions more than on the reader alone.",
    ["Access control", "Pricing", "Commercial doors"],
    "access-control-systems",
    [
        ("Typical range", "Simple doors often start around C$2,500 to C$5,500; multi-door systems can reach C$6,000 to C$20,000+."),
        ("Cost drivers", "Door count, electrified hardware, cabling, schedules, visitors, and occupied-site constraints."),
        ("Quote quality", "A useful quote separates doors, readers, locks, panels, programming, and cabling work."),
    ],
    [
        {
            "eyebrow": "Budget",
            "title": "Think in controlled doors, not readers",
            "paragraphs": [
                "A reader is only one part of access control. Each controlled door may require locking hardware, power, cabling, controller capacity, request-to-exit devices, fire-alarm coordination, programming, testing, and user setup.",
                "That is why two projects with the same number of readers can have very different budgets. Door conditions and management requirements matter.",
            ],
            "callout_label": "Key point",
            "callout": "The correct pricing unit is usually the controlled door, not the wall reader.",
        },
        {
            "eyebrow": "Ranges",
            "title": "Common budget ranges",
            "table": {
                "caption": "Indicative commercial access-control budgets",
                "columns": ("Scope", "Typical work", "Indicative budget", "When it applies"),
                "rows": (
                    ("Single door", "Reader, lock or strike, basic programming", "C$2,500 to C$5,500", "Small office, retail back door, or restricted room"),
                    ("Small system", "2 to 4 doors with centralized management", "C$6,000 to C$12,000", "Main entrance, internal restricted areas, or small commercial site"),
                    ("Larger scope", "4+ doors, schedules, visitors, integrations", "C$12,000 to C$20,000+", "Commercial, multi-tenant, or multi-zone buildings"),
                ),
            },
        },
        {
            "eyebrow": "Variables",
            "title": "What changes the quote",
            "cards": [
                ("Door hardware", "Strikes, maglocks, electrified locks, door operators, and aluminum doors require different work."),
                ("Cabling", "Some doors are easy to cable; others need planning, drilling, or finished-wall work."),
                ("Controller design", "Panels, power supplies, network locations, and spare capacity affect the system."),
                ("User management", "Schedules, groups, badges, mobile credentials, and reporting add setup time."),
                ("Integrations", "Intercoms, cameras, fire alarm, and garage doors can expand the scope."),
                ("Site constraints", "Working hours, occupied spaces, and access limits affect labour and coordination."),
            ],
        },
    ],
    [
        ("Can you add access control to one door only?", "Yes. A single-door scope is common when the need is clear."),
        ("Can it work with an intercom?", "Yes, but it should be planned as one entrance workflow."),
        ("Does every door need new hardware?", "Not always. Existing hardware must be reviewed to confirm what can be reused."),
        ("What makes pricing unreliable?", "Quoting without seeing the door hardware, cable path, controller location, and management requirements."),
    ],
    _cta("Need access-control pricing for your building?", "Send the door list, photos, and how users should access the building. We will help define a realistic scope.", "Request a quote", "contact", "See access control", "access-control-systems"),
)

EN_DECISION_ARTICLES["intercom-pricing-multi-tenant-building"] = _article(
    "/en/guides/intercom-pricing-multi-tenant-building/",
    "Intercom Pricing for Multi-Tenant Buildings | Opticable",
    "What affects intercom pricing for multi-tenant and commercial buildings, including audio, video, door release, cabling, and access integration.",
    "Pricing guide",
    "How much does an intercom cost for a multi-tenant building?",
    "Intercom pricing depends on the entrance, number of units or contacts, audio versus video, door release, cabling, network availability, and whether the intercom must integrate with access control. A simple replacement may be straightforward, while a full entrance modernization can become a larger building project.",
    "Intercom costs vary by entrance type, user count, audio or video needs, cabling, door release, and access-control integration.",
    ["Intercom", "Multi-tenant", "Pricing"],
    "intercom-systems",
    [
        ("Main factor", "The entrance workflow drives the design more than the intercom panel alone."),
        ("Cost drivers", "User count, cabling, video, door release, network access, and access-control integration."),
        ("Best quote", "Define who answers visitors, how doors unlock, and how users are managed."),
    ],
    [
        {
            "eyebrow": "Scope",
            "title": "The entrance workflow matters most",
            "paragraphs": [
                "An intercom is not only a panel at the front door. It is a workflow for visitors, deliveries, occupants, staff, and managers.",
                "The quote changes depending on audio, video, remote management, mobile calling, door release, and access-control coordination.",
            ],
            "callout_label": "Planning note",
            "callout": "Start by defining how visitors should be handled, then select the hardware.",
        },
        {
            "eyebrow": "Budget factors",
            "title": "What drives intercom cost",
            "cards": [
                ("Audio or video", "Video usually adds network, device, and configuration requirements."),
                ("User count", "More suites, tenants, or contacts require more setup and management."),
                ("Door release", "Unlocking hardware and wiring must be compatible and safe."),
                ("Existing cabling", "Old cabling can be useful or become a constraint depending on the system."),
                ("Access integration", "Intercom and access control should be coordinated when both are present."),
                ("Management model", "Remote changes, directories, and schedules affect setup."),
            ],
        },
        {
            "eyebrow": "Typical situations",
            "title": "Common project types",
            "table": {
                "caption": "Intercom scope examples",
                "columns": ("Situation", "Typical scope", "Main concern"),
                "rows": (
                    ("Old panel replacement", "New entrance panel and door release review", "Existing wiring and user directory"),
                    ("Video upgrade", "Video-capable panel and user workflow", "Network, devices, and privacy expectations"),
                    ("Shared commercial entrance", "Intercom plus access-control coordination", "Visitors versus authorized users"),
                    ("Multi-tenant building", "Directory, call routing, and management", "Keeping users simple to maintain"),
                ),
            },
        },
    ],
    [
        ("Is video always required?", "No. Video is useful in many shared entrances, but audio may be enough for simpler sites."),
        ("Can it work with access control?", "Yes. Shared entrances often work best when both systems are planned together."),
        ("Can an old intercom be replaced without rewiring everything?", "Sometimes. Existing wiring must be reviewed before deciding."),
        ("What speeds up a quote?", "Entrance photos, number of users, current system model, door hardware, and desired visitor workflow."),
    ],
    _cta("Need to modernize a building entrance?", "Tell us about the entrance, users, and current intercom. We will help define the right replacement or upgrade path.", "Request an intercom quote", "contact", "See intercom systems", "intercom-systems"),
)

EN_DECISION_ARTICLES["intercom-audio-or-video-commercial-building"] = _article(
    "/en/guides/intercom-audio-or-video-commercial-building/",
    "Audio or Video Intercom for Commercial Buildings | Opticable",
    "How to decide between audio and video intercom systems for commercial and multi-tenant entrances.",
    "Decision guide",
    "Audio or video intercom: which is right for your commercial entrance?",
    "Audio intercom can be enough when visitors are known and the entrance risk is low. Video becomes more useful when occupants need to see who is at the door, deliveries are frequent, the entrance is shared, or the building wants stronger verification before unlocking.",
    "Audio is simpler and often cheaper. Video adds verification and context when the entrance risk or visitor flow justifies it.",
    ["Intercom", "Video intercom", "Commercial entrances"],
    "intercom-systems",
    [
        ("Audio", "Simpler choice for low-risk entrances and known visitors."),
        ("Video", "Better when visual confirmation matters before unlocking."),
        ("Decision", "Base the choice on visitor flow, risk, and who answers the door."),
    ],
    [
        {
            "eyebrow": "Decision",
            "title": "Match the system to the entrance risk",
            "paragraphs": [
                "The right choice is not audio versus video in general. It depends on what happens at that entrance every day.",
                "If the building handles unknown visitors, deliveries, after-hours traffic, or shared entrances, video can add useful confirmation.",
            ],
            "callout_label": "Core question",
            "callout": "What would the person answering need to know before unlocking the door?",
        },
        {
            "eyebrow": "Comparison",
            "title": "Audio versus video",
            "table": {
                "caption": "Commercial intercom choice",
                "columns": ("Option", "Best for", "Tradeoff"),
                "rows": (
                    ("Audio", "Known visitors and simple entrances", "Lower complexity but less verification"),
                    ("Video", "Shared or higher-risk entrances", "More context but more design considerations"),
                    ("Video plus access", "Buildings with staff, tenants, and visitors", "Best workflow but requires coordination"),
                ),
            },
        },
        {
            "eyebrow": "Variables",
            "title": "What should influence the choice",
            "cards": [
                ("Visitor type", "Known visitors, deliveries, unknown visitors, and contractors create different risks."),
                ("Who answers", "Reception, tenants, managers, or remote staff may need different workflows."),
                ("Lighting and location", "Video quality depends on camera position, lighting, and entrance layout."),
                ("Door release", "Unlocking must be safe and coordinated with door hardware."),
                ("Privacy expectations", "Video should be used where it makes operational sense."),
                ("Future management", "The system should remain easy to update as tenants or staff change."),
            ],
        },
    ],
    [
        ("Is video always more secure?", "It can improve verification, but only when placement, lighting, and workflow are designed properly."),
        ("Can audio be upgraded later?", "Sometimes, but it is better to plan for future video if it is likely."),
        ("Does video require better network infrastructure?", "Often yes. Video systems usually depend more on network quality and configuration."),
        ("What should I send for a quote?", "Entrance photos, visitor types, who answers, door hardware, and whether access control is involved."),
    ],
    _cta("Unsure whether audio or video makes sense?", "Describe the entrance and visitor flow. We will help identify the practical option before quoting.", "Talk about my entrance", "contact", "See intercom systems", "intercom-systems"),
)

EN_DECISION_ARTICLES["structured-cabling-pricing-office-retail"] = _article(
    "/en/guides/structured-cabling-pricing-office-retail/",
    "Structured Cabling Pricing for Offices and Retail | Opticable",
    "What affects structured cabling pricing for offices, retail spaces, network drops, rack cleanup, patching, testing, and documentation.",
    "Pricing guide",
    "How much does structured cabling cost in an office or retail space?",
    "Structured cabling cost depends on the number of drops, cable paths, ceiling access, wall finishes, rack condition, patching, testing, and required documentation. A few new network drops can be modest, while a full cleanup or multi-drop project becomes a larger infrastructure scope.",
    "Structured cabling pricing depends much more on paths, drops, rack condition, testing, and finish quality than on cable alone.",
    ["Structured cabling", "Network drops", "Pricing"],
    "structured-cabling",
    [
        ("Small additions", "A few network drops may be simple when paths are accessible."),
        ("Larger scopes", "Multiple drops, patch panels, rack work, testing, and cleanup increase cost."),
        ("Quote quality", "A good cabling quote separates drops, pathways, patching, testing, labels, and documentation."),
    ],
    [
        {
            "eyebrow": "Cost drivers",
            "title": "The cable is only one part of the job",
            "paragraphs": [
                "Most of the cost comes from labour: finding routes, opening access, pulling cable, terminating, patching, testing, labelling, and leaving the network area clean.",
                "A few drops in an accessible office are not the same as rewiring a retail space, cleaning up a rack, and adding many tested runs during business operations.",
            ],
            "callout_label": "Key point",
            "callout": "Structured cabling should be priced as a complete installed and tested path, not as cable by the metre.",
        },
        {
            "eyebrow": "Budget",
            "title": "Common budget ranges",
            "table": {
                "caption": "Indicative structured cabling budgets",
                "columns": ("Scope", "Typical work", "Indicative budget", "When it applies"),
                "rows": (
                    ("Small additions", "A few network drops", "C$500 to C$2,500", "Accessible paths and limited scope"),
                    ("Intermediate scope", "Several drops, patching, and better organization", "C$3,000 to C$8,000", "Growing office, retail, or work area"),
                    ("Fuller scope", "Drops, rack, patch panels, cleanup, testing", "C$8,000 to C$15,000+", "Larger project or existing environment to reorganize"),
                ),
            },
        },
        {
            "eyebrow": "Variables",
            "title": "What changes the quote",
            "cards": [
                ("Number of drops", "Each drop adds pathfinding, cable, termination, patching, and testing."),
                ("Accessibility", "Open ceilings, finished walls, long paths, and occupied spaces change labour."),
                ("Rack condition", "A messy rack often must be stabilized before new work is added."),
                ("Cable category", "Cat6 and Cat6A have different handling and pathway requirements."),
                ("Finish level", "Labels, testing, patching, and documentation affect the final result."),
                ("Operating hours", "Retail or active offices may require phased or off-hour work."),
            ],
        },
    ],
    [
        ("Can you add only a few drops?", "Yes. Small targeted additions are common when the route is accessible."),
        ("Do you test and label the drops?", "Yes, proper testing and labelling should be part of a professional cabling scope."),
        ("Should the rack be cleaned before adding more drops?", "Often yes, especially if support or future expansion is already difficult."),
        ("What helps you quote faster?", "Drop count, photos of the rack, site type, ceiling access, and expected work hours."),
    ],
    _cta("Need structured cabling pricing?", "Send the drop list, rack photos, and site constraints. We will help define a clean, testable scope.", "Request a cabling quote", "contact", "See structured cabling", "structured-cabling"),
)

EN_DECISION_ARTICLES["analog-cctv-to-ip-migration"] = _article(
    "/en/guides/analog-cctv-to-ip-migration/",
    "Analog CCTV to IP Camera Migration | Opticable",
    "How to plan a migration from analog CCTV to IP cameras, including cabling, PoE, storage, network readiness, and phased upgrades.",
    "Migration guide",
    "How to migrate an analog CCTV system to IP cameras",
    "Migrating from analog CCTV to IP cameras is not only a camera replacement. The project usually touches cabling, power, network switching, storage, recorder design, remote access, and sometimes camera locations. A phased plan helps preserve coverage while the system is upgraded.",
    "Analog-to-IP camera migration should account for cabling, PoE, network capacity, storage, coverage, and transition planning.",
    ["IP cameras", "CCTV migration", "Security cameras"],
    "security-camera-systems",
    [
        ("Not just cameras", "The network, cabling, PoE, and recorder design matter."),
        ("Phasing", "Important areas should remain covered during the transition."),
        ("Result", "A cleaner IP system with better management, storage planning, and future flexibility."),
    ],
    [
        {
            "eyebrow": "Upgrade scope",
            "title": "What changes when moving to IP",
            "paragraphs": [
                "Analog cameras typically rely on coaxial cabling and older recording systems. IP cameras usually rely on network cabling, PoE switching, IP addressing, video storage, and network design.",
                "That means the migration should review more than camera models. The supporting infrastructure must be ready.",
            ],
            "callout_label": "Important",
            "callout": "A migration is an infrastructure project, not only a camera swap.",
        },
        {
            "eyebrow": "Checklist",
            "title": "What to review before migration",
            "steps": [
                ("List existing cameras", "Identify critical zones, weak views, and cameras that can be removed or relocated."),
                ("Review cabling", "Decide whether existing cable can be reused or new network cabling is required."),
                ("Confirm PoE switching", "IP cameras need reliable power and network ports."),
                ("Plan storage", "Retention, resolution, and camera count determine recording requirements."),
                ("Maintain coverage", "Sequence work so key areas are not left blind longer than necessary."),
            ],
        },
        {
            "eyebrow": "Migration choices",
            "title": "Possible upgrade paths",
            "cards": [
                ("Full replacement", "Replace cameras, recorder, cabling, and network support in one planned scope."),
                ("Phased replacement", "Upgrade high-priority areas first, then continue by zone."),
                ("Hybrid bridge", "Some sites temporarily keep part of the analog system while IP is deployed."),
                ("Coverage redesign", "Use the migration to correct old blind spots and poor camera angles."),
                ("Storage upgrade", "Set realistic retention based on business needs."),
                ("Network cleanup", "Prepare switching, rack space, and labels before adding video load."),
            ],
        },
    ],
    [
        ("Can existing coax be reused?", "Sometimes through adapters or hybrid systems, but new network cabling is often cleaner long term."),
        ("Do all cameras need to be replaced at once?", "No. A phased approach can work when coverage and system compatibility are planned."),
        ("Will IP cameras overload the network?", "They can if switching, segmentation, and storage are not planned properly."),
        ("What helps assess the migration?", "Camera count, recorder model, cable photos, key areas, retention needs, and network-room photos."),
    ],
    _cta("Planning to replace an older camera system?", "Tell us what you have today and which areas matter most. We will help plan a clean migration path.", "Plan a camera upgrade", "contact", "See camera systems", "security-camera-systems"),
)

EN_DECISION_ARTICLES["network-room-rack-cleanup"] = _article(
    "/en/guides/network-room-rack-cleanup/",
    "Network Room and Rack Cleanup | Opticable",
    "When to clean up a network room or rack before adding cameras, access control, WiFi, cabling, or other commercial systems.",
    "Infrastructure guide",
    "When should you clean up the network room or rack?",
    "A messy network room is not only cosmetic. It can slow troubleshooting, hide bad cabling, make new systems harder to add, and increase risk during upgrades. Cleaning up the rack before adding cameras, access control, WiFi, or new drops often saves time later.",
    "Rack cleanup makes future camera, WiFi, access control, and cabling work easier to support and safer to modify.",
    ["Network room", "Rack cleanup", "Infrastructure"],
    "network-infrastructure",
    [
        ("When to do it", "Before adding new systems, expanding cabling, or troubleshooting recurring issues."),
        ("What it improves", "Readability, support speed, cable management, labels, and future expansion."),
        ("Practical result", "A cleaner technical base for cameras, WiFi, phones, access, and networking."),
    ],
    [
        {
            "eyebrow": "Why it matters",
            "title": "Messy infrastructure becomes technical debt",
            "paragraphs": [
                "A rack can become difficult to support after years of small additions, emergency fixes, undocumented cables, and equipment changes.",
                "At some point, every new project becomes slower because nobody can confidently identify what is connected where.",
            ],
            "callout_label": "Practical test",
            "callout": "If one cable move feels risky because nobody knows what it does, the rack needs attention.",
        },
        {
            "eyebrow": "Symptoms",
            "title": "Signs cleanup should come first",
            "cards": [
                ("No labels", "Cables, patch panels, and switch ports cannot be identified quickly."),
                ("Loose equipment", "Devices are stacked, hanging, or installed without a clear layout."),
                ("Overloaded patching", "Short fixes and old patches make troubleshooting slow."),
                ("No free capacity", "Adding cameras or access points requires guessing what can be reused."),
                ("Poor airflow", "Equipment heat and clutter increase reliability risk."),
                ("Unknown ownership", "Nobody knows which vendor or system uses which cable."),
            ],
        },
        {
            "eyebrow": "Scope",
            "title": "What cleanup can include",
            "steps": [
                ("Document what exists", "Identify switches, patch panels, circuits, UPS, and active equipment."),
                ("Trace critical links", "Find connections that support internet, phones, cameras, access, and WiFi."),
                ("Re-patch cleanly", "Shorten, group, and label patch cables where possible."),
                ("Remove dead clutter", "Retire clearly unused cables or devices when safe to do so."),
                ("Prepare for growth", "Leave the rack easier to expand and support."),
            ],
        },
    ],
    [
        ("Do you need to replace everything?", "No. Cleanup often focuses on organizing, labelling, tracing, and stabilizing what should remain."),
        ("Can cleanup be done before a camera or WiFi project?", "Yes, and it is often the right sequence."),
        ("Is this only for large sites?", "No. Small racks can become just as difficult to support when they are undocumented."),
        ("What should I send first?", "Clear photos of the rack, patch panels, switches, floor or wall area, and the project you want to add next."),
    ],
    _cta("Is your network room blocking the next project?", "Send rack photos and describe what you need to add. We will help decide whether cleanup should come first.", "Request an assessment", "contact", "See network infrastructure", "network-infrastructure"),
)
GUIDE_INDEX_PAGE_EN = {
    "path": "/en/guides/",
    "title": "Technology Planning Guides | Opticable",
    "desc": "Guides, pricing pages, and comparisons for planning cameras, access control, intercom, WiFi, cabling, and network infrastructure projects.",
    "eyebrow": "Opticable guides",
    "headline": "Guides to plan your building technology project",
    "intro": "These pages help clarify budget, system choice, site preparation, and next steps before requesting a quote.",
    "panel_title": "Who these guides help",
    "panel_copy": "For property managers, owners, businesses, and project teams that want a clearer scope before a site visit or quote request.",
    "listing_title": "Guides, comparisons, and decision pages",
    "listing_intro": "Practical resources to frame budgets, compare options, and prepare the right next step.",
    "cta_title": "Want to validate your project with us?",
    "cta_copy": "Describe the building, target systems, and site constraints. We will help confirm what to check before the quote.",
}

CAMPAIGN_LANDING_PAGES_EN = {
    "lp-commercial-door-access": {
        "path": "/en/lp/commercial-door-access/",
        "title": "Commercial Door Access Quote | Opticable",
        "desc": "Request a quote for commercial door access control, readers, locks, and entrance security.",
        "eyebrow": "Access control",
        "headline": "Commercial door access control for active buildings",
        "intro": "Secure entrances, back doors, technical rooms, and restricted areas with a scope built around your site conditions.",
        "panel_title": "Useful before quoting",
        "panel_copy": "Door count, hardware photos, access schedule, and building constraints help us prepare a realistic scope.",
        "cta_label": "Request a quote",
        "service_key": "access-control-systems",
        "items": ["Reader, lock, strike, or maglock review", "Door and cable-path validation", "User groups, schedules, and access rules", "Coordination with intercom, cameras, or fire requirements when needed"],
        "benefits": [("Door-first approach", "We look at the door hardware and access workflow before choosing equipment."), ("Clear scope", "The quote separates hardware, cabling, programming, and commissioning."), ("Commercial focus", "The project is planned around occupied buildings and active operations.")],
        "cta_title": "Need commercial door access control?",
        "cta_copy": "Send the door list, photos, and access goals. We will help define the right scope.",
    },
    "lp-multitenant-intercom": {
        "path": "/en/lp/multi-tenant-intercom/",
        "title": "Multi-Tenant Intercom Quote | Opticable",
        "desc": "Request a quote for intercom or video intercom systems for multi-tenant and shared commercial entrances.",
        "eyebrow": "Intercom",
        "headline": "Intercom systems for multi-tenant entrances",
        "intro": "Modernize visitor entry with an intercom workflow that matches occupants, managers, deliveries, and shared entrances.",
        "panel_title": "Useful before quoting",
        "panel_copy": "Entrance photos, user count, existing system details, and door-release requirements help scope the work.",
        "cta_label": "Request a quote",
        "service_key": "intercom-systems",
        "items": ["Audio or video intercom options", "Directory and call-routing setup", "Door-release and access-control coordination", "Planning for occupied common areas"],
        "benefits": [("Entrance workflow", "We define how visitors request entry before selecting the hardware."), ("Management clarity", "Users, directories, and updates are considered from the start."), ("Integrated thinking", "Intercom, access control, cameras, and network needs are reviewed together.")],
        "cta_title": "Need a multi-tenant intercom quote?",
        "cta_copy": "Describe the entrance, user count, and current system. We will help shape the replacement path.",
    },
    "lp-commercial-wifi-audit": {
        "path": "/en/lp/commercial-wifi-audit/",
        "title": "Commercial WiFi Audit Quote | Opticable",
        "desc": "Request a commercial WiFi review for weak coverage, unstable access points, cabling issues, and network limitations.",
        "eyebrow": "Commercial WiFi",
        "headline": "Commercial WiFi review before adding more access points",
        "intro": "Identify whether your WiFi issue comes from coverage, access point placement, cabling, switch capacity, interference, or configuration.",
        "panel_title": "Useful before quoting",
        "panel_copy": "Weak zones, access point count, network-room photos, and critical business devices help frame the review.",
        "cta_label": "Request a review",
        "service_key": "commercial-wifi-installation",
        "items": ["Coverage and weak-zone review", "Access point placement and mounting check", "Cabling, PoE, switching, and uplink review", "Guest, staff, and operational network considerations"],
        "benefits": [("Problem-first review", "We identify the likely cause before recommending more hardware."), ("Infrastructure check", "Cabling, PoE, switching, and rack conditions are part of the review."), ("Operational focus", "POS, staff, guest, and business devices are considered separately.")],
        "cta_title": "Need a commercial WiFi audit?",
        "cta_copy": "Tell us where WiFi fails and what depends on it. We will help identify the right next step.",
    },
}
INDUSTRY_DETAIL_PAGES_EN = {
    "industry-office-building": {
        "path": "/en/industries/office-buildings/",
        "title": "Technology Systems for Office Buildings | Opticable",
        "desc": "Cameras, access control, WiFi, cabling, and network infrastructure for office buildings and professional spaces.",
        "eyebrow": "Industries",
        "headline": "Technology for office buildings",
        "intro": "Office buildings need systems that are simple to operate, easy to expand, and practical in occupied spaces. The most common needs involve entrances, WiFi, meeting rooms, technical rooms, network cleanup, and tenant changes.",
        "panel_title": "What we see most often",
        "panel_copy": "Entrances to secure, technical rooms to control, uneven WiFi coverage, network rooms to clean up, and new workstations or tenants to connect.",
        "service_keys": ("access-control-systems", "commercial-wifi-installation", "security-camera-systems", "structured-cabling"),
        "guide_keys": ("access-control-pricing-commercial-building", "structured-cabling-pricing-office-retail", "network-room-rack-cleanup"),
        "sections": [
            {"eyebrow": "Common systems", "title": "What we install most often", "items": ["Access control for main entrances, server rooms, and restricted areas", "Cameras at entrances, corridors, loading areas, and sensitive zones", "Commercial WiFi for offices, meeting rooms, and common areas", "Network drops for workstations, IP phones, access points, and equipment", "Rack and network-room cleanup before expansion"]},
            {"eyebrow": "Constraints", "title": "Typical office-building constraints", "cards": [("Occupied building", "Work often needs to happen without disrupting occupants or operations."), ("Floor-by-floor access", "Pathways, ceilings, and technical rooms can vary from one floor to another."), ("Mixed stakeholders", "Management, IT, occupants, and ownership often have different priorities."), ("Ongoing changes", "Moves, expansions, and tenant changes keep the site evolving.")]},
            {"eyebrow": "Typical projects", "title": "Scopes we see often", "items": ["Securing the main entrance and server room", "Improving WiFi in meeting rooms and denser work areas", "Adding cameras to parking, entrances, and corridors", "Increasing network drops for new workstations", "Cleaning up a network room that has become hard to support", "Preparing a floor or suite for a new tenant"]},
        ],
        "faq_items": [("Do you work in active offices?", "Yes. Planning usually accounts for permitted hours, sensitive zones, and occupant impact."), ("Can you handle only part of the building?", "Yes. We can scope one entrance, one floor, one technical room, or a larger project."), ("Do you clean up network rooms too?", "Yes. It is often the right first step before adding systems."), ("How should I request a quote?", "Send the number of floors, target zones, systems involved, and access constraints.")],
        "cta_title": "Do you manage an office building?",
        "cta_copy": "Describe the zones, systems, and site constraints. We will help define the right next step.",
        "cta_label": "Request a quote",
    },
    "industry-multi-tenant-building": {
        "path": "/en/industries/multi-tenant-buildings/",
        "title": "Technology Systems for Multi-Tenant Buildings | Opticable",
        "desc": "Intercom, access control, cameras, common-area WiFi, and cabling for multi-tenant commercial buildings.",
        "eyebrow": "Industries",
        "headline": "Technology for multi-tenant buildings",
        "intro": "In a multi-tenant building, priorities usually revolve around entrances, visitors, common areas, parking, and remote management. Systems must stay clear for the manager without making daily use harder for occupants.",
        "panel_title": "Needs that come up often",
        "panel_copy": "Intercom or video intercom, access control for entrances, cameras in common areas, shared WiFi, and a simple building-management workflow.",
        "service_keys": ("intercom-systems", "access-control-systems", "security-camera-systems", "commercial-wifi-installation"),
        "guide_keys": ("intercom-pricing-multi-tenant-building", "intercom-audio-or-video-commercial-building", "access-control-pricing-commercial-building"),
        "sections": [
            {"eyebrow": "Common systems", "title": "What we see most often", "items": ["Intercom or video intercom at the main entrance", "Access control for entrances, parking, or shared rooms", "Cameras in lobbies, corridors, stairwells, and parking areas", "WiFi for common areas or building services", "Cabling and technical-room cleanup"]},
            {"eyebrow": "Constraints", "title": "What makes these buildings different", "cards": [("Occupied property", "Work must fit around residents, tenants, and daily building use."), ("Shared entrances", "Visitors, occupants, suppliers, and maintenance need a clear access workflow."), ("Remote management", "Managers often want to verify, unlock, or update users remotely."), ("Common areas", "Lobbies, corridors, parking, and service rooms each need a different logic.")]},
            {"eyebrow": "Typical projects", "title": "Scopes we see often", "items": ["Replacing an unreliable old intercom panel", "Adding access control at the main entrance and garage", "Installing cameras in lobbies, corridors, and parking areas", "Adding WiFi in corridors or shared rooms", "Controlling access to technical or service rooms", "Modernizing old systems in phases"]},
        ],
        "faq_items": [("Can you work only on the main entrance?", "Yes. A targeted entrance project is common."), ("Can intercom and access control work together?", "Yes. That is often the cleanest setup for shared entrances."), ("Do you work in occupied common areas?", "Yes. Work is planned to limit interruptions."), ("What helps with a quote?", "Number of entrances, building type, systems involved, and current problems.")],
        "cta_title": "Do you manage a multi-tenant building?",
        "cta_copy": "Describe the entrance, shared areas, and systems involved. We will help define the right scope.",
        "cta_label": "Request a quote",
    },
    "industry-retail-and-sales-floor": {
        "path": "/en/industries/retail-and-sales-floor/",
        "title": "Technology for Retail and Sales Floors | Opticable",
        "desc": "Cameras, WiFi, access control, and structured cabling for retail stores, shops, and sales floors.",
        "eyebrow": "Industries",
        "headline": "Technology for retail and sales floors",
        "intro": "Retail systems need to support operations first: point of sale, back office, receiving, stable WiFi, and clear security. Work often needs to happen quickly and around peak business hours.",
        "panel_title": "Typical priorities",
        "panel_copy": "Cameras at entrances and cash areas, stable WiFi for operations, controlled access to back areas, and clean cabling for point-of-sale systems.",
        "service_keys": ("security-camera-systems", "commercial-wifi-installation", "access-control-systems", "structured-cabling"),
        "guide_keys": ("analog-cctv-to-ip-migration", "structured-cabling-pricing-office-retail", "commercial-wifi-audit-checklist"),
        "sections": [
            {"eyebrow": "Common systems", "title": "What we install most often", "items": ["Cameras at entrances, cash areas, sales floor, and back-of-house spaces", "Commercial WiFi for terminals, employees, and guest areas when needed", "Access control for storage, offices, or back doors", "Network drops for POS, workstations, and operational equipment", "Rack or small network-room cleanup"]},
            {"eyebrow": "Constraints", "title": "What changes the installation plan", "cards": [("Operating hours", "The store often needs to remain functional during work."), ("Critical zones", "POS, back office, receiving, and cash areas need special attention."), ("Operational WiFi", "Unstable WiFi can quickly affect payments and daily work."), ("Compact spaces", "Small sites can still have dense equipment and traffic.")]},
            {"eyebrow": "Typical projects", "title": "Scopes we see often", "items": ["Adding cameras at checkout, entrances, and parking", "Fixing unstable WiFi for terminals and staff", "Securing back-of-house or storage areas", "Adding network drops for new equipment", "Migrating an old surveillance system to IP", "Cleaning up an improvised rack or network corner"]},
        ],
        "faq_items": [("Can you work outside business hours?", "Yes, when the site requires it."), ("Can you handle only WiFi or only cameras?", "Yes. Scopes can be targeted or combined."), ("Can networks be separated when needed?", "Yes. Guest, staff, POS, and operational networks can be separated when appropriate."), ("What should I send for a quote?", "Store type, target zones, systems involved, and scheduling constraints.")],
        "cta_title": "Do you operate a store or sales floor?",
        "cta_copy": "Describe the sales area, back-of-house space, and systems to correct. We will help define the right scope.",
        "cta_label": "Request a quote",
    },
    "industry-warehouse-and-industrial": {
        "path": "/en/industries/warehouses-and-industrial-sites/",
        "title": "Technology for Warehouses and Light Industrial Sites | Opticable",
        "desc": "Cameras, access control, WiFi, fiber, and network infrastructure for warehouses and light industrial environments.",
        "eyebrow": "Industries",
        "headline": "Technology for warehouses and light industrial sites",
        "intro": "Warehouses and light industrial sites often need perimeter coverage, dock visibility, restricted-area access, operational WiFi, and stronger network links between work areas. Site conditions strongly shape the technical scope.",
        "panel_title": "What comes up most often",
        "panel_copy": "Cameras around docks and perimeter, controlled access for sensitive zones, WiFi for operations, and stronger backbone links between technical areas.",
        "service_keys": ("security-camera-systems", "access-control-systems", "commercial-wifi-installation", "fiber-optic-installation"),
        "guide_keys": ("analog-cctv-to-ip-migration", "commercial-wifi-audit-checklist", "cat6a-or-fiber-commercial-building"),
        "sections": [
            {"eyebrow": "Common systems", "title": "What we deploy most often", "items": ["Cameras at perimeter points, docks, doors, and traffic areas", "Access control for offices, electrical rooms, technical rooms, and sensitive zones", "Commercial WiFi for operations, docks, and hard-to-cover areas", "Network or fiber links between technical zones, offices, and distant areas", "Rack and network-infrastructure cleanup"]},
            {"eyebrow": "Constraints", "title": "Site realities", "cards": [("Distance", "Links are often longer than in a typical office."), ("Materials", "Metal, concrete, height, and open structures affect coverage and pathways."), ("Operational security", "Sensitive zones, inventory, and docks need a clear access and camera plan."), ("Continuity", "The site often remains active while work is performed.")]},
            {"eyebrow": "Typical projects", "title": "Scopes we see often", "items": ["Adding cameras at docks, doors, and parking areas", "Securing technical or restricted-access zones", "Improving weak WiFi in larger work areas", "Adding fiber or Cat6A links between site zones", "Modernizing old camera or access systems", "Cleaning up a crowded or undocumented network room"]},
        ],
        "faq_items": [("Do you only work in offices and retail?", "No. We also handle warehouse and light industrial scopes when they match our services."), ("When should fiber be considered?", "When distance, capacity, or site layout makes copper less practical."), ("Is warehouse WiFi different?", "Often yes. Height, metal, interference, and movement change the design."), ("What helps with a quote?", "Site type, target zones, approximate distances, and systems involved.")],
        "cta_title": "Do you operate a warehouse or light industrial site?",
        "cta_copy": "Describe the areas to secure, cover, or connect. We will help define a realistic site scope.",
        "cta_label": "Request a quote",
    },
}

for _collection in (EN_GUIDE_ARTICLES, EN_DECISION_ARTICLES):
    for _item in _collection.values():
        _item["author"] = "Opticable Team"
