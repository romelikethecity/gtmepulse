# scripts/build.py
# Main build pipeline: generates all pages, sitemap, robots, CNAME.
# Data + page generators live here. HTML shell lives in templates.py.
# Site constants live in nav_config.py.

import os
import sys
import re
import shutil
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import *
import templates
from templates import (get_page_wrapper, write_page, get_homepage_schema,
                       get_breadcrumb_schema, breadcrumb_html, newsletter_cta_html,
                       ALL_PAGES)

# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")

# Wire up templates module
templates.OUTPUT_DIR = OUTPUT_DIR


# ---------------------------------------------------------------------------
# Banned words list (from CLAUDE.md writing standards)
# ---------------------------------------------------------------------------

BANNED_WORDS = [
    "robust", "leverage", "synergy", "holistic", "cutting-edge", "seamless",
    "game-changer", "paradigm shift", "revolutionary",
    "genuinely", "truly", "really", "actually", "quite", "extremely",
    "unlock", "unleash", "enhance", "exceed", "empower", "supercharge",
    "harness", "spearhead", "delve",
    "landscape", "tapestry", "frontier", "resonates", "positioning",
]


# ---------------------------------------------------------------------------
# Page generators
# ---------------------------------------------------------------------------

def build_homepage():
    """Generate the homepage with Organization+WebSite schema."""
    title = "GTM Engineer Salary, Tools, and Career Data"
    description = (
        "Salary benchmarks, tool reviews, and career intelligence for GTM Engineers."
        " Practitioner-built data from 3,000+ B2B SaaS job postings, updated weekly."
    )

    body = '''<section class="page-header">
    <h1>Career Intelligence and Salary Data for GTM Engineers</h1>
    <p class="page-header-subtitle">Salary benchmarks, tool stack reviews, and job market analysis for the fastest-growing role in B2B SaaS.</p>
    <div class="stat-grid">
        <div class="stat-block">
            <span class="stat-number">3,000+</span>
            <span class="stat-label">Roles Tracked</span>
        </div>
        <div class="stat-block">
            <span class="stat-number">$132K-$250K</span>
            <span class="stat-label">Salary Range</span>
        </div>
        <div class="stat-block">
            <span class="stat-number">205%</span>
            <span class="stat-label">YoY Growth</span>
        </div>
    </div>
</section>
'''
    body += newsletter_cta_html()

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/",
        body_content=body,
        active_path="/",
        extra_head=get_homepage_schema(),
        body_class="page-home",
    )
    write_page("index.html", page)
    print(f"  Built: index.html")


def build_about_page():
    """Generate the about page with BreadcrumbList schema."""
    title = "About GTME Pulse: Independent GTM Engineer Data"
    description = (
        "GTME Pulse offers vendor-neutral salary benchmarks, tool stack reviews,"
        " and career guides for GTM Engineers. Real data from 3,000+ B2B SaaS job posts."
    )

    crumbs = [("Home", "/"), ("About", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>About GTME Pulse: Independent GTM Engineer Data</h1>
</section>
<div class="container">
    <p>GTME Pulse is an independent resource for GTM Engineers. We track salary data, review tools, and analyze the job market so you don't have to piece it together from LinkedIn posts and vendor blogs.</p>
    <p>Every data point comes from real job postings. We scrape, normalize, and cross-reference thousands of listings across B2B SaaS companies, from seed-stage startups to public enterprises.</p>
    <p>No vendor affiliations drive our rankings. No pay-to-play reviews. When we say a tool is good, it's because practitioners use it and the data backs it up.</p>
    <h2>What you'll find here</h2>
    <ul>
        <li><strong>Salary benchmarks</strong> broken down by seniority, location, and company stage</li>
        <li><strong>Tool reviews</strong> from someone who has built GTM systems, not just written about them</li>
        <li><strong>Career guides</strong> for breaking into and advancing in GTM Engineering</li>
        <li><strong>Weekly data</strong> on hiring trends, salary shifts, and tool adoption</li>
    </ul>
    <p>Built by <strong>Rome Thorndike</strong>.</p>
</div>
'''

    page = get_page_wrapper(
        title=title,
        description=description,
        canonical_path="/about/",
        body_content=body,
        active_path="/about/",
        extra_head=get_breadcrumb_schema(crumbs),
        body_class="page-inner",
    )
    write_page("about/index.html", page)
    print(f"  Built: about/index.html")


# ---------------------------------------------------------------------------
# Meta file generators
# ---------------------------------------------------------------------------

def build_sitemap():
    """Generate sitemap.xml from ALL_PAGES list."""
    urls = ""
    for page_path in ALL_PAGES:
        # Convert file paths to clean URLs
        clean = page_path.replace("index.html", "")
        if not clean.startswith("/"):
            clean = "/" + clean
        if not clean.endswith("/"):
            clean += "/"
        # Root is just /
        if clean == "//":
            clean = "/"

        urls += f"""  <url>
    <loc>{SITE_URL}{clean}</loc>
    <lastmod>{BUILD_DATE}</lastmod>
  </url>
"""

    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>
'''

    sitemap_path = os.path.join(OUTPUT_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"  Built: sitemap.xml ({len(ALL_PAGES)} URLs)")


def build_robots():
    """Generate robots.txt with sitemap reference."""
    content = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    robots_path = os.path.join(OUTPUT_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Built: robots.txt")


# ---------------------------------------------------------------------------
# Content standards validator
# ---------------------------------------------------------------------------

def validate_pages():
    """Scan all HTML files in output/ and check content standards."""
    warnings = []

    for root, dirs, files in os.walk(OUTPUT_DIR):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            filepath = os.path.join(root, fname)
            rel = os.path.relpath(filepath, OUTPUT_DIR)

            with open(filepath, "r", encoding="utf-8") as f:
                html = f.read()

            # Check title length (50-60 chars)
            title_match = re.search(r"<title>(.*?)</title>", html)
            if title_match:
                title_text = title_match.group(1)
                tlen = len(title_text)
                if tlen < 50 or tlen > 60:
                    warnings.append(f"{rel}: title length {tlen} (want 50-60): \"{title_text}\"")
            else:
                warnings.append(f"{rel}: missing <title> tag")

            # Check meta description length (150-158 chars)
            desc_match = re.search(r'<meta name="description" content="(.*?)"', html)
            if desc_match:
                desc_text = desc_match.group(1)
                dlen = len(desc_text)
                if dlen < 150 or dlen > 158:
                    warnings.append(f"{rel}: description length {dlen} (want 150-158): \"{desc_text}\"")
            else:
                warnings.append(f"{rel}: missing meta description")

            # Check H1 count
            h1_count = len(re.findall(r"<h1[^>]*>", html))
            if h1_count != 1:
                warnings.append(f"{rel}: found {h1_count} H1 tags (want exactly 1)")

            # Check for em-dash (U+2014)
            if "\u2014" in html:
                warnings.append(f"{rel}: contains em-dash character (U+2014)")

            # Check for banned words
            html_lower = html.lower()
            for word in BANNED_WORDS:
                # Match whole words only to avoid false positives
                pattern = r'\b' + re.escape(word) + r'\b'
                if re.search(pattern, html_lower):
                    warnings.append(f"{rel}: contains banned word \"{word}\"")

    if warnings:
        print(f"\n  Content validation: {len(warnings)} warning(s)")
        for w in warnings:
            print(f"    WARNING: {w}")
    else:
        print(f"\n  Content validation: all clear")

    return warnings


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    print(f"=== GTME Pulse Build ({BUILD_DATE}) ===\n")

    # 1. Clean output directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    print("  Cleaned output/")

    # 2. Copy assets
    shutil.copytree(ASSETS_DIR, os.path.join(OUTPUT_DIR, "assets"))
    print("  Copied assets/")

    # 3. Build pages
    print("\n  Building pages...")
    build_homepage()
    build_about_page()

    # 4. Build meta files
    print("\n  Building meta files...")
    build_sitemap()
    build_robots()

    # 5. Write CNAME
    cname_path = os.path.join(OUTPUT_DIR, "CNAME")
    with open(cname_path, "w", encoding="utf-8") as f:
        f.write("gtmepulse.com\n")
    print("  Built: CNAME")

    # 6. Validate content standards
    validate_pages()

    # 7. Summary
    print(f"\n=== Build complete: {len(ALL_PAGES)} pages ===")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Preview: cd output && python3 -m http.server 8090")


if __name__ == "__main__":
    main()
