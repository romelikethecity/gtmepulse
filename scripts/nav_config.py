# scripts/nav_config.py
# Site constants, navigation, and footer configuration.
# Pure data — zero logic, zero imports.

SITE_NAME = "GTME Pulse"
SITE_URL = "https://gtmepulse.com"
SITE_TAGLINE = "Career intelligence for GTM Engineers"
COPYRIGHT_YEAR = "2026"
CURRENT_YEAR = 2026
CSS_VERSION = "9"

CTA_HREF = "/newsletter/"
CTA_LABEL = "Get the Weekly Pulse"

NAV_ITEMS = [
    {
        "href": "/salary/",
        "label": "Salary Data",
        "children": [
            {"href": "/salary/", "label": "Salary Index"},
            {"href": "/salary/by-seniority/", "label": "By Seniority"},
            {"href": "/salary/by-location/", "label": "By Location"},
            {"href": "/salary/by-company-stage/", "label": "By Company Stage"},
            {"href": "/salary/comparisons/", "label": "Comparisons"},
            {"href": "/salary/calculator/", "label": "Salary Calculator"},
        ],
    },
    {"href": "/tools/", "label": "Tools"},
    {"href": "/careers/", "label": "Careers"},
    {"href": "/newsletter/", "label": "Newsletter"},
]

FOOTER_COLUMNS = {
    "Salary Data": [
        {"href": "/salary/", "label": "Salary Index"},
        {"href": "/salary/by-seniority/", "label": "By Seniority"},
        {"href": "/salary/by-location/", "label": "By Location"},
        {"href": "/salary/by-company-stage/", "label": "By Stage"},
        {"href": "/salary/comparisons/", "label": "Comparisons"},
    ],
    "Resources": [
        {"href": "/tools/", "label": "GTM Tools"},
        {"href": "/careers/", "label": "Career Guides"},
        {"href": "/newsletter/", "label": "Newsletter"},
        {"href": "/about/", "label": "About"},
    ],
    "Site": [
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
        {"href": "/salary/methodology/", "label": "Methodology"},
    ],
}
