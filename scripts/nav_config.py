# scripts/nav_config.py
# Site constants, navigation, and footer configuration.
# Pure data — zero logic, zero imports.

SITE_NAME = "GTME Pulse"
SITE_URL = "https://gtmepulse.com"
SITE_TAGLINE = "Career intelligence for GTM Engineers"
COPYRIGHT_YEAR = "2026"
CURRENT_YEAR = 2026
CSS_VERSION = "17"

CTA_HREF = "/newsletter/"
CTA_LABEL = "Get the Weekly Pulse"

SIGNUP_WORKER_URL = "https://newsletter-subscribe.rome-workers.workers.dev/subscribe"

GA_MEASUREMENT_ID = "G-KFWVZ2V6YL"
GOOGLE_SITE_VERIFICATION = ""  # Set to verification filename (e.g., "google1234abcd.html") to generate file
GOOGLE_SITE_VERIFICATION_META = ""  # Set to verification code for meta tag method (alternative to HTML file)

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
    {
        "href": "/tools/",
        "label": "Tools",
        "children": [
            {"href": "/tools/", "label": "Tools Index"},
            {"href": "/tools/tech-stack-benchmark/", "label": "Tech Stack Benchmark"},
            {"href": "/tools/category/data-enrichment/", "label": "Tool Categories"},
            {"href": "/tools/clay-review/", "label": "Tool Reviews"},
        ],
    },
    {
        "href": "/careers/",
        "label": "Careers",
        "children": [
            {"href": "/careers/", "label": "Career Guides"},
            {"href": "/careers/how-to-become-gtm-engineer/", "label": "How to Become a GTME"},
            {"href": "/careers/job-growth/", "label": "Job Market Growth"},
        ],
    },
    {"href": "/glossary/", "label": "Glossary"},
    {
        "href": "/benchmarks/",
        "label": "Resources",
        "children": [
            {"href": "/benchmarks/", "label": "Benchmarks"},
            {"href": "/comparisons/", "label": "Comparisons"},
            {"href": "/blog/", "label": "Blog"},
            {"href": "/insights/", "label": "Insights"},
            {"href": "/jobs/", "label": "Job Board"},
        ],
    },
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
        {"href": "/tools/tech-stack-benchmark/", "label": "Tech Stack Benchmark"},
        {"href": "/tools/frustrations/", "label": "Tool Frustrations"},
        {"href": "/tools/category/data-enrichment/", "label": "Tool Categories"},
        {"href": "/benchmarks/", "label": "Industry Benchmarks"},
        {"href": "/comparisons/", "label": "Comparisons"},
        {"href": "/benchmarks/50-stats/", "label": "50 Key Statistics"},
        {"href": "/careers/", "label": "Career Guides"},
        {"href": "/careers/how-to-become-gtm-engineer/", "label": "How to Become a GTME"},
        {"href": "/careers/job-growth/", "label": "Job Market Growth"},
        {"href": "/careers/agency-pricing/", "label": "Agency Pricing"},
        {"href": "/glossary/", "label": "Glossary"},
        {"href": "/jobs/", "label": "Job Board"},
        {"href": "/blog/", "label": "Blog"},
        {"href": "/insights/", "label": "Insights"},
        {"href": "/newsletter/", "label": "Newsletter"},
        {"href": "/about/", "label": "About"},
    ],
    "Site": [
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
        {"href": "/salary/methodology/", "label": "Methodology"},
    ],
}
