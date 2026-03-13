# scripts/nav_config.py
# Site constants, navigation, and footer configuration.
# Pure data — zero logic, zero imports.

SITE_NAME = "GTME Pulse"
SITE_URL = "https://gtmepulse.com"
SITE_TAGLINE = "Career intelligence for GTM Engineers"
COPYRIGHT_YEAR = "2026"
CURRENT_YEAR = 2026
CSS_VERSION = "10"

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
            {"href": "/salary/coding-premium/", "label": "Coding Premium"},
            {"href": "/salary/equity/", "label": "Equity Data"},
            {"href": "/salary/agency-fees/", "label": "Agency Fees"},
        ],
    },
    {"href": "/tools/", "label": "Tools"},
    {
        "href": "/careers/",
        "label": "Careers",
        "children": [
            {"href": "/careers/", "label": "Career Guides"},
            {"href": "/careers/how-to-become-gtm-engineer/", "label": "How to Become a GTME"},
            {"href": "/careers/job-growth/", "label": "Job Market Growth"},
            {"href": "/careers/agency-pricing/", "label": "Agency Pricing"},
        ],
    },
    {"href": "/newsletter/", "label": "Newsletter"},
]

FOOTER_COLUMNS = {
    "Salary Data": [
        {"href": "/salary/", "label": "Salary Index"},
        {"href": "/salary/by-seniority/", "label": "By Seniority"},
        {"href": "/salary/by-location/", "label": "By Location"},
        {"href": "/salary/by-company-stage/", "label": "By Stage"},
        {"href": "/salary/comparisons/", "label": "Comparisons"},
        {"href": "/salary/coding-premium/", "label": "Coding Premium"},
        {"href": "/salary/equity/", "label": "Equity Data"},
    ],
    "Resources": [
        {"href": "/tools/", "label": "GTM Tools"},
        {"href": "/careers/", "label": "Career Guides"},
        {"href": "/careers/how-to-become-gtm-engineer/", "label": "How to Become a GTME"},
        {"href": "/careers/job-growth/", "label": "Job Market Growth"},
        {"href": "/careers/agency-pricing/", "label": "Agency Pricing"},
        {"href": "/newsletter/", "label": "Newsletter"},
        {"href": "/about/", "label": "About"},
    ],
    "Site": [
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
        {"href": "/salary/methodology/", "label": "Methodology"},
    ],
}
