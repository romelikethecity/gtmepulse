#!/usr/bin/env python3
"""
inject_content_figures.py
Injects content SVG figures into generated HTML pages that don't already have them.
Maps page directories to the appropriate SVG from assets/images/content/.
Run AFTER build.py generates the output/ directory.
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")

# Map directory prefixes to SVG files and default captions
DIR_TO_SVG = {
    "tools": ("tools-stack.svg", "Tool adoption rates across 228 GTM Engineering practitioners"),
    "salary": ("salary-data.svg", "GTM Engineer salary ranges by seniority, location, and company stage"),
    "glossary": ("glossary-terms.svg", "Key GTM engineering terms and acronyms defined"),
    "insights": ("insights-analysis.svg", "Job market growth, salary trends, and market intelligence"),
    "comparisons": ("comparisons-versus.svg", "Head-to-head analysis of roles, approaches, and strategies"),
    "jobs": ("jobs-board.svg", "Live GTM Engineer job postings updated twice weekly"),
    "best-gtm-engineer-resources": ("benchmarks-data.svg", "Survey-backed performance benchmarks from 228 practitioners"),
    "benchmarks": ("benchmarks-data.svg", "Survey-backed performance benchmarks from 228 practitioners"),
    "newsletter": ("newsletter-digest.svg", "Weekly job market data, salary shifts, and tool intel"),
    "careers": ("career-path.svg", "GTM Engineer career trajectory from entry to lead level"),
    "blog": ("blog-editorial.svg", "Data-driven opinion and analysis on GTM engineering"),
    "top-voices": ("insights-analysis.svg", "GTM Engineering thought leaders and community voices"),
}


def get_page_title(html):
    """Extract the page title from the <title> tag or first <h1>."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        # Strip any inner HTML tags
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    m = re.search(r'<title>(.*?)</title>', html)
    if m:
        title = m.group(1).split('|')[0].split(' - ')[0].strip()
        return title
    return ""


def build_figure_html(svg_filename, alt_text, caption):
    """Build the figure HTML block."""
    return f'''<figure class="content-figure">
    <img src="/assets/images/content/{svg_filename}" alt="{alt_text}" width="1200" height="630" loading="eager">
    <figcaption>{caption}</figcaption>
</figure>'''


def inject_figure(html, figure_html):
    """Inject figure after the first <h2> tag. Falls back to after hero section or first </header>."""
    # Try after first <h2>...</h2>
    m = re.search(r'(</h2>)', html)
    if m:
        insert_pos = m.end()
        return html[:insert_pos] + '\n' + figure_html + '\n' + html[insert_pos:]

    # Fallback: after hero section
    m = re.search(r'(</section>)', html)
    if m:
        insert_pos = m.end()
        return html[:insert_pos] + '\n' + figure_html + '\n' + html[insert_pos:]

    return html


def get_dir_prefix(rel_path):
    """Get the top-level directory from a relative path."""
    parts = rel_path.split(os.sep)
    if len(parts) > 1:
        return parts[0]
    return ""


def process_file(filepath, rel_path):
    """Process a single HTML file. Returns True if modified."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already has a content-figure
    if 'content-figure' in html:
        return False

    # Determine which SVG to use based on directory
    dir_prefix = get_dir_prefix(rel_path)
    if dir_prefix not in DIR_TO_SVG:
        return False

    svg_filename, default_caption = DIR_TO_SVG[dir_prefix]

    # Build alt text from page title
    page_title = get_page_title(html)
    alt_text = f"{page_title} - {default_caption}" if page_title else default_caption

    figure_html = build_figure_html(svg_filename, alt_text, default_caption)
    new_html = inject_figure(html, figure_html)

    if new_html == html:
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return True


def main():
    injected = 0
    skipped = 0
    no_match = 0

    for root, dirs, files in os.walk(OUTPUT_DIR):
        # Skip assets directory
        if 'assets' in root.split(os.sep):
            continue
        for fname in files:
            if fname != 'index.html':
                continue
            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, OUTPUT_DIR)

            dir_prefix = get_dir_prefix(rel_path)
            if dir_prefix not in DIR_TO_SVG:
                no_match += 1
                continue

            if process_file(filepath, rel_path):
                injected += 1
            else:
                skipped += 1

    print(f"=== Content Figure Injection Complete ===")
    print(f"  Injected: {injected} pages")
    print(f"  Skipped (already has figure): {skipped}")
    print(f"  No match (not a content dir): {no_match}")


if __name__ == "__main__":
    main()
