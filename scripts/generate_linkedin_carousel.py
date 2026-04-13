#!/usr/bin/env python3
"""
Generate LinkedIn carousel images from weekly GTME Pulse data.

Creates 6 branded PNG slides (1080x1350) + optional PDF.

Slides:
1. Cover: "GTME Pulse" + narrative hook + key stats
2. Top tools by demand (with Rising/Falling/New tags)
3. Salary by role
4. Key insight (growth tools if previous data, else remote vs onsite gap)
5. Top hiring companies
6. CTA: gtmepulse.com/newsletter

Usage:
    python scripts/generate_linkedin_carousel.py              # Generate PNGs
    python scripts/generate_linkedin_carousel.py --pdf        # Also combine into PDF
"""

import argparse
import json
import os
import sys
from datetime import datetime
from collections import Counter

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

W, H = 1080, 1350

# Brand colors (Dark + Orange accent)
NAVY = (13, 13, 13)               # #0D0D0D
CARD = (26, 26, 26)               # #1A1A1A
ACCENT = (255, 79, 31)            # #FF4F1F
ACCENT_DIM = (204, 63, 25)        # #CC3F19
GOLD = (245, 158, 11)             # #F59E0B
GREEN = (34, 197, 94)             # #22C55E
RED = (239, 68, 68)               # #EF4444
WHITE = (232, 232, 232)           # #E8E8E8
GRAY_200 = (226, 232, 240)
GRAY_400 = (148, 163, 184)
GRAY_500 = (100, 116, 139)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
SITE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'site', 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'carousel')
PREVIOUS_SNAPSHOT_FILE = os.path.join(DATA_DIR, 'previous_market_snapshot.json')

SKILL_DISPLAY = {
    'Rag': 'RAG', 'Aws': 'AWS', 'Gcp': 'GCP',
    'Power Bi': 'Power BI', 'Hubspot': 'HubSpot', 'Salesforce': 'Salesforce',
    'Clay': 'Clay', 'Openai': 'OpenAI', 'Zoominfo': 'ZoomInfo',
    'Salesloft': 'SalesLoft', 'Docusign': 'DocuSign',
}


# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

def get_font(size, bold=False):
    candidates = []
    if bold:
        candidates = [
            '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
            '/System/Library/Fonts/Helvetica.ttc',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        ]
    else:
        candidates = [
            '/System/Library/Fonts/Supplemental/Arial.ttf',
            '/System/Library/Fonts/Helvetica.ttc',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_rounded_rect(draw, xy, fill, radius=16):
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def draw_bar(draw, x, y, width, height, color):
    if width > 0:
        draw.rounded_rectangle((x, y, x + width, y + height), radius=height // 2, fill=color)


def draw_tag(draw, x, y, text, color):
    """Draw a small colored tag pill."""
    font_tag = get_font(14, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font_tag)
    tag_w = bbox[2] - bbox[0] + 14
    tag_h = bbox[3] - bbox[1] + 8
    # Blend tag color with navy for dimmed background
    tag_bg = tuple(c // 5 + NAVY[i] * 4 // 5 for i, c in enumerate(color))
    draw_rounded_rect(draw, (x, y, x + tag_w, y + tag_h), fill=tag_bg, radius=4)
    draw.text((x + 7, y + 2), text, fill=color, font=font_tag)
    return tag_w


def slide_header(draw, title, subtitle=None):
    font_title = get_font(42, bold=True)
    draw.text((60, 60), title, fill=WHITE, font=font_title)
    draw.rectangle((60, 120, 200, 124), fill=GOLD)
    y = 140
    if subtitle:
        font_sub = get_font(24)
        draw.text((60, y), subtitle, fill=GRAY_400, font=font_sub)
        y += 40
    return y + 20


def slide_footer(draw, page_num, total_pages):
    font_footer = get_font(20)
    font_brand = get_font(22, bold=True)
    draw.rectangle((60, H - 100, W - 60, H - 99), fill=GRAY_500)
    draw.text((60, H - 80), "GTME PULSE", fill=ACCENT, font=font_brand)
    page_text = f"{page_num}/{total_pages}"
    bbox = draw.textbbox((0, 0), page_text, font=font_footer)
    draw.text((W - 60 - (bbox[2] - bbox[0]), H - 76), page_text, fill=GRAY_400, font=font_footer)
    draw.text((60, H - 52), "gtmepulse.com", fill=GRAY_500, font=get_font(16))


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data():
    with open(os.path.join(DATA_DIR, 'market_intelligence.json')) as f:
        mi = json.load(f)
    with open(os.path.join(DATA_DIR, 'comp_analysis.json')) as f:
        ca = json.load(f)
    jobs = []
    jobs_path = os.path.join(SITE_DATA_DIR, 'jobs.json')
    if not os.path.exists(jobs_path):
        jobs_path = os.path.join(DATA_DIR, 'jobs.json')
    if os.path.exists(jobs_path):
        with open(jobs_path) as f:
            data = json.load(f)
            if isinstance(data, list):
                jobs = data
            elif isinstance(data, dict):
                jobs = data.get('jobs', data.get('data', []))
    prev = None
    if os.path.exists(PREVIOUS_SNAPSHOT_FILE):
        with open(PREVIOUS_SNAPSHOT_FILE) as f:
            prev = json.load(f)
    return mi, ca, jobs, prev


# ---------------------------------------------------------------------------
# Narrative signal generation for carousel
# ---------------------------------------------------------------------------

def generate_carousel_signals(mi, ca, prev):
    """Generate narrative hooks for carousel slides."""
    signals = {
        'cover_hook': '',
        'has_previous': False,
    }

    total_jobs = mi['total_jobs']
    tools = mi.get('tools', {})
    prev_tools = prev.get('tools', {}) if prev else {}
    has_previous = bool(prev_tools)
    signals['has_previous'] = has_previous

    # Top tool dominance
    sorted_tools = sorted(tools.items(), key=lambda x: -x[1])
    if sorted_tools:
        top_name = SKILL_DISPLAY.get(sorted_tools[0][0], sorted_tools[0][0])
        top_pct = round(sorted_tools[0][1] / total_jobs * 100, 1)
        signals['cover_hook'] = f"{top_name} appears in {top_pct}% of all GTM Engineer jobs."

    # If we have previous data, find biggest mover for hook
    if has_previous:
        biggest_pct_change = 0
        biggest_tool = None
        for name, count in tools.items():
            pc = prev_tools.get(name, 0)
            if pc > 20:
                pct_change = ((count - pc) / pc) * 100
                if pct_change > biggest_pct_change:
                    biggest_pct_change = pct_change
                    biggest_tool = name
        if biggest_tool and biggest_pct_change > 3:
            display = SKILL_DISPLAY.get(biggest_tool, biggest_tool)
            signals['cover_hook'] = f"{display} grew {biggest_pct_change:.0f}% this week."

    # Remote gap data
    by_remote = ca.get('by_remote', {})
    onsite = by_remote.get('onsite', {})
    remote = by_remote.get('remote', {})
    signals['onsite_median'] = onsite.get('median', 0)
    signals['remote_median'] = remote.get('median', 0)
    signals['onsite_count'] = onsite.get('count', 0)
    signals['remote_count'] = remote.get('count', 0)
    if signals['onsite_median'] > 0 and signals['remote_median'] > 0:
        # Positive = remote pays more, negative = onsite pays more
        signals['remote_gap_pct'] = round(
            (signals['remote_median'] - signals['onsite_median']) / signals['onsite_median'] * 100
        )
    else:
        signals['remote_gap_pct'] = 0

    # Overall median from salary_stats
    salary_stats = ca.get('salary_stats', {})
    signals['median_salary'] = salary_stats.get('median', 0)

    return signals


# ---------------------------------------------------------------------------
# Slide generators
# ---------------------------------------------------------------------------

def make_cover(mi, ca, date_str, total_pages, signals):
    """Slide 1: Cover with narrative hook + key stats."""
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    font_big = get_font(56, bold=True)
    font_sub = get_font(28)
    font_hook = get_font(26, bold=True)
    font_stat_num = get_font(72, bold=True)
    font_stat_label = get_font(22)

    # Title
    draw.text((60, 120), "GTME", fill=ACCENT, font=font_big)
    draw.text((60, 190), "PULSE", fill=WHITE, font=font_big)
    draw.rectangle((60, 270, 200, 276), fill=GOLD)
    draw.text((60, 300), f"Week of {date_str}", fill=GRAY_400, font=font_sub)

    # Narrative hook
    hook = signals.get('cover_hook', '')
    if hook:
        # Word wrap at ~40 chars
        words = hook.split()
        lines = []
        current = ''
        for w in words:
            test = f"{current} {w}".strip()
            if len(test) > 42 and current:
                lines.append(current)
                current = w
            else:
                current = test
        if current:
            lines.append(current)

        y_hook = 350
        for line in lines[:2]:
            draw.text((60, y_hook), line, fill=WHITE, font=font_hook)
            y_hook += 36

    # Stat cards
    total_jobs = mi['total_jobs']
    salary_stats = ca.get('salary_stats', {})
    median_sal = salary_stats.get('median', 0)
    disclosure = ca.get('disclosure_rate', 0)

    card_w = (W - 120 - 30) // 3
    y_card = 460

    for i, (val, label) in enumerate([
        (f"{total_jobs:,}", "Jobs Analyzed"),
        (f"${int(median_sal/1000)}K" if median_sal > 0 else "N/A", "Median Salary"),
        (f"{disclosure}%", "Disclose Pay"),
    ]):
        x = 60 + i * (card_w + 15)
        draw_rounded_rect(draw, (x, y_card, x + card_w, y_card + 180), fill=CARD)
        bbox = draw.textbbox((0, 0), val, font=font_stat_num)
        text_w = bbox[2] - bbox[0]
        draw.text((x + (card_w - text_w) // 2, y_card + 30), val, fill=ACCENT, font=font_stat_num)
        bbox = draw.textbbox((0, 0), label, font=font_stat_label)
        text_w = bbox[2] - bbox[0]
        draw.text((x + (card_w - text_w) // 2, y_card + 120), label, fill=GRAY_400, font=font_stat_label)

    draw.text((60, H - 200), "Swipe for the full breakdown", fill=GRAY_200, font=font_sub)
    draw.text((60, H - 155), "Tools \u2022 Salaries \u2022 Companies \u2022 Trends", fill=GRAY_400, font=font_stat_label)

    slide_footer(draw, 1, total_pages)
    return img


def make_tools_slide(mi, prev, total_pages):
    """Slide 2: Top tools by demand with Rising/Falling/New tags."""
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    y = slide_header(draw, "Top Tools in Demand", f"From {mi['total_jobs']:,} GTM Engineer job postings")

    font_tool = get_font(26, bold=True)
    font_count = get_font(22)
    font_change = get_font(18)

    tools = mi.get('tools', {})
    prev_tools = prev.get('tools', {}) if prev else {}
    has_previous = bool(prev_tools)
    sorted_tools = sorted(tools.items(), key=lambda x: -x[1])[:10]
    max_count = sorted_tools[0][1] if sorted_tools else 1

    for i, (name, count) in enumerate(sorted_tools):
        display_name = SKILL_DISPLAY.get(name, name)
        pct = round(count / mi['total_jobs'] * 100, 1)
        prev_count = prev_tools.get(name, 0)
        change = count - prev_count

        draw_rounded_rect(draw, (60, y, W - 60, y + 90), fill=CARD)

        rank_font = get_font(20, bold=True)
        draw.text((80, y + 10), f"#{i+1}", fill=GOLD, font=rank_font)
        draw.text((130, y + 8), display_name, fill=WHITE, font=font_tool)

        # Draw Rising/Falling/New tag next to tool name
        if has_previous:
            name_bbox = draw.textbbox((0, 0), display_name, font=font_tool)
            tag_x = 130 + (name_bbox[2] - name_bbox[0]) + 12
            if prev_count == 0 and count > 0:
                draw_tag(draw, tag_x, y + 10, "NEW", GOLD)
            elif change > 0 and prev_count > 0 and (change / prev_count) > 0.01:
                draw_tag(draw, tag_x, y + 10, "RISING", GREEN)
            elif change < 0 and prev_count > 0 and (abs(change) / prev_count) > 0.01:
                draw_tag(draw, tag_x, y + 10, "FALLING", RED)

        count_text = f"{count:,} mentions ({pct}%)"
        draw.text((130, y + 45), count_text, fill=GRAY_400, font=font_count)

        if has_previous:
            if change > 0:
                change_text, change_color = f"+{change}", GREEN
            elif change < 0:
                change_text, change_color = f"{change}", RED
            else:
                change_text, change_color = "=", GRAY_400
            bbox = draw.textbbox((0, 0), change_text, font=font_change)
            draw.text((W - 80 - (bbox[2] - bbox[0]), y + 35), change_text, fill=change_color, font=font_change)

        bar_w = int(count / max_count * (W - 200))
        draw_bar(draw, 130, y + 75, bar_w, 6, ACCENT)

        y += 100

    slide_footer(draw, 2, total_pages)
    return img


def make_salary_slide(ca, prev, total_pages):
    """Slide 3: Salary by role (top paying roles from comp_analysis)."""
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    y = slide_header(draw, "Top Paying Roles", "From posted compensation data")

    font_role = get_font(24, bold=True)
    font_company = get_font(20)
    font_num = get_font(32, bold=True)
    font_detail = get_font(20)

    top_roles = ca.get('top_paying_roles', [])[:8]
    if not top_roles:
        font_msg = get_font(24)
        draw.text((60, y + 40), "Salary data available next week.", fill=GRAY_400, font=font_msg)
        slide_footer(draw, 3, total_pages)
        return img

    max_sal = max((r.get('salary_max', 0) for r in top_roles), default=200000)

    for role in top_roles:
        title = role.get('title', 'Unknown')
        company = role.get('company', '')
        sal_min = role.get('salary_min', 0)
        sal_max = role.get('salary_max', 0)
        seniority = role.get('seniority', '')

        # Truncate long titles
        if len(title) > 38:
            title = title[:35] + '...'

        draw_rounded_rect(draw, (60, y, W - 60, y + 110), fill=CARD)
        draw.text((80, y + 12), title, fill=GRAY_200, font=font_role)

        # Company name
        if company:
            draw.text((80, y + 42), company, fill=GRAY_400, font=font_company)

        # Salary range
        if sal_min > 0 and sal_max > 0:
            sal_text = f"${int(sal_min/1000)}K-${int(sal_max/1000)}K"
        elif sal_max > 0:
            sal_text = f"Up to ${int(sal_max/1000)}K"
        else:
            sal_text = "N/A"
        bbox = draw.textbbox((0, 0), sal_text, font=font_num)
        draw.text((W - 80 - (bbox[2] - bbox[0]), y + 20), sal_text, fill=ACCENT, font=font_num)

        # Seniority tag
        if seniority and seniority != 'Unknown':
            bbox_s = draw.textbbox((0, 0), seniority, font=font_detail)
            draw.text((W - 80 - (bbox_s[2] - bbox_s[0]), y + 60), seniority, fill=GRAY_400, font=font_detail)

        bar_w = int(sal_max / max_sal * (W - 200)) if max_sal > 0 else 0
        draw_bar(draw, 80, y + 92, bar_w, 8, ACCENT)

        y += 125

    slide_footer(draw, 3, total_pages)
    return img


def make_insight_slide(mi, ca, prev, signals, total_pages):
    """Slide 4: Key insight (growth tools if previous data, else remote gap)."""
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    has_previous = signals.get('has_previous', False)

    if has_previous:
        # Growth tools slide
        y = slide_header(draw, "Fastest Growing Tools", "Week-over-week change in job mentions")

        font_tool = get_font(28, bold=True)
        font_change = get_font(24)
        font_detail = get_font(20)

        tools = mi.get('tools', {})
        prev_tools = prev.get('tools', {}) if prev else {}

        growth = []
        for name, count in tools.items():
            prev_count = prev_tools.get(name, 0)
            if prev_count >= 10:
                change = count - prev_count
                pct_change = (change / prev_count) * 100
                if change > 0:
                    growth.append({'name': name, 'count': count, 'change': change, 'pct': pct_change})

        growth.sort(key=lambda x: -x['pct'])

        for item in growth[:8]:
            display_name = SKILL_DISPLAY.get(item['name'], item['name'])

            draw_rounded_rect(draw, (60, y, W - 60, y + 100), fill=CARD)
            draw.text((80, y + 12), display_name, fill=WHITE, font=font_tool)

            change_text = f"+{item['change']:,} mentions (+{item['pct']:.0f}%)"
            draw.text((80, y + 52), change_text, fill=GREEN, font=font_change)

            now_text = f"Now: {item['count']:,}"
            bbox = draw.textbbox((0, 0), now_text, font=font_detail)
            draw.text((W - 80 - (bbox[2] - bbox[0]), y + 38), now_text, fill=GRAY_400, font=font_detail)

            y += 115

    else:
        # Remote vs Onsite salary comparison
        y = slide_header(draw, "The Remote Salary Gap", "Median GTM Engineer salary by work arrangement")

        font_big_num = get_font(64, bold=True)
        font_label = get_font(24)
        font_detail = get_font(22)
        font_gap = get_font(36, bold=True)
        font_context = get_font(20)

        onsite_med = signals.get('onsite_median', 0)
        remote_med = signals.get('remote_median', 0)
        onsite_count = signals.get('onsite_count', 0)
        remote_count = signals.get('remote_count', 0)
        gap_pct = signals.get('remote_gap_pct', 0)  # positive = remote pays more

        # Two large stat cards
        card_w = (W - 120 - 20) // 2

        # Onsite card
        x1 = 60
        draw_rounded_rect(draw, (x1, y, x1 + card_w, y + 200), fill=CARD)
        draw.text((x1 + 20, y + 20), "ONSITE", fill=GRAY_400, font=get_font(16, bold=True))
        onsite_text = f"${int(onsite_med/1000)}K" if onsite_med > 0 else "N/A"
        onsite_color = ACCENT if gap_pct <= 0 else GRAY_200
        draw.text((x1 + 20, y + 55), onsite_text, fill=onsite_color, font=font_big_num)
        draw.text((x1 + 20, y + 140), f"{onsite_count:,} roles", fill=GRAY_400, font=font_detail)

        # Remote card
        x2 = 60 + card_w + 20
        draw_rounded_rect(draw, (x2, y, x2 + card_w, y + 200), fill=CARD)
        draw.text((x2 + 20, y + 20), "REMOTE", fill=GRAY_400, font=get_font(16, bold=True))
        remote_text = f"${int(remote_med/1000)}K" if remote_med > 0 else "N/A"
        remote_color = ACCENT if gap_pct > 0 else GOLD
        draw.text((x2 + 20, y + 55), remote_text, fill=remote_color, font=font_big_num)
        draw.text((x2 + 20, y + 140), f"{remote_count:,} roles", fill=GRAY_400, font=font_detail)

        y += 240

        # Gap indicator, handle both directions
        if onsite_med > 0 and remote_med > 0:
            diff_k = abs(int((remote_med - onsite_med) / 1000))
            abs_pct = abs(gap_pct)

            if gap_pct > 0:
                gap_text = f"Remote pays {abs_pct}% more"
                draw.text((60, y), gap_text, fill=GREEN, font=font_gap)
            elif gap_pct < 0:
                gap_text = f"Onsite pays {abs_pct}% more"
                draw.text((60, y), gap_text, fill=GOLD, font=font_gap)
            else:
                draw.text((60, y), "Salary parity across arrangements", fill=GRAY_200, font=font_gap)
            y += 60

            draw.text((60, y), f"That's ~${diff_k}K/year in base salary.", fill=GRAY_200, font=font_detail)
            y += 50

            # Add context about volume
            total_roles = onsite_count + remote_count
            onsite_pct = round(onsite_count / total_roles * 100) if total_roles > 0 else 0
            remote_pct = round(remote_count / total_roles * 100) if total_roles > 0 else 0
            draw.text((60, y), f"{onsite_pct}% of roles are onsite \u2022 {remote_pct}% remote", fill=GRAY_400, font=font_detail)
            y += 70

        # Hybrid data if available
        by_remote = ca.get('by_remote', {})
        hybrid = by_remote.get('hybrid', {})
        hybrid_med = hybrid.get('median', 0)
        hybrid_count = hybrid.get('count', 0)
        if hybrid_med > 0 and hybrid_count > 0:
            draw_rounded_rect(draw, (60, y, W - 60, y + 120), fill=CARD)
            draw.text((80, y + 15), "HYBRID", fill=GRAY_400, font=get_font(16, bold=True))
            hybrid_text = f"${int(hybrid_med/1000)}K"
            draw.text((80, y + 45), hybrid_text, fill=ACCENT, font=get_font(48, bold=True))
            hybrid_detail = f"{hybrid_count:,} roles"
            bbox = draw.textbbox((0, 0), hybrid_detail, font=font_detail)
            draw.text((W - 80 - (bbox[2] - bbox[0]), y + 55), hybrid_detail, fill=GRAY_400, font=font_detail)
            y += 150

        # By-seniority insight
        by_seniority = ca.get('by_seniority', {})
        if by_seniority:
            y += 20
            draw.text((60, y), "By seniority:", fill=GRAY_400, font=font_context)
            y += 35
            for level in ['Senior', 'Mid', 'Junior']:
                data = by_seniority.get(level, {})
                med = data.get('median', 0)
                cnt = data.get('count', 0)
                if med > 0 and cnt > 0:
                    line = f"\u2022  {level}: ${int(med/1000)}K median ({cnt:,} roles)"
                    draw.text((60, y), line, fill=GRAY_200, font=font_context)
                    y += 35

    slide_footer(draw, 4, total_pages)
    return img


def make_companies_slide(jobs, prev, total_pages):
    """Slide 5: Top hiring companies."""
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    y = slide_header(draw, "Top Companies Hiring", "Most active GTM Engineer employers this week")

    font_company = get_font(26, bold=True)
    font_detail = get_font(20)
    font_roles = get_font(36, bold=True)
    font_label = get_font(16)

    company_counts = Counter(j.get('company', '') for j in jobs if j.get('company'))
    prev_companies = prev.get('company_counts', {}) if prev else {}
    top = company_counts.most_common(8)
    max_count = top[0][1] if top else 1

    if not top:
        font_msg = get_font(24)
        draw.text((60, y + 40), "Company data available with jobs.json.", fill=GRAY_400, font=font_msg)
        slide_footer(draw, 5, total_pages)
        return img

    for company, count in top:
        prev_count = prev_companies.get(company, 0)
        change = count - prev_count

        co_jobs = [j for j in jobs if j.get('company') == company]
        salary_jobs = [j for j in co_jobs if j.get('max_amount') and j['max_amount'] > 0]
        avg_sal = 0
        if salary_jobs:
            avg_sal = int(sum((j.get('min_amount', 0) + j['max_amount']) / 2 for j in salary_jobs) / len(salary_jobs))

        draw_rounded_rect(draw, (60, y, W - 60, y + 110), fill=CARD)
        draw.text((80, y + 12), company, fill=WHITE, font=font_company)

        roles_text = str(count)
        bbox = draw.textbbox((0, 0), roles_text, font=font_roles)
        draw.text((W - 100 - (bbox[2] - bbox[0]), y + 10), roles_text, fill=ACCENT, font=font_roles)
        draw.text((W - 100 - (bbox[2] - bbox[0]), y + 55), "roles", fill=GRAY_400, font=font_label)

        details = []
        if avg_sal > 0:
            details.append(f"${int(avg_sal/1000)}K avg")
        if change > 0:
            details.append(f"+{change} vs last week")
        detail_text = " \u2022 ".join(details) if details else ""
        draw.text((80, y + 50), detail_text, fill=GRAY_400, font=font_detail)

        bar_w = int(count / max_count * (W - 200))
        draw_bar(draw, 80, y + 90, bar_w, 8, ACCENT)

        y += 126

    slide_footer(draw, 5, total_pages)
    return img


def make_cta_slide(mi, signals, total_pages):
    """Slide 6: CTA slide with dynamic data."""
    img = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    font_big = get_font(48, bold=True)
    font_med = get_font(28)
    font_url = get_font(32, bold=True)
    font_bullet = get_font(24)

    y = 200
    draw.text((60, y), "Career intelligence", fill=WHITE, font=font_big)
    y += 70
    draw.text((60, y), "for GTM Engineers.", fill=ACCENT, font=font_big)

    y += 120
    draw.rectangle((60, y, 200, y + 4), fill=GOLD)
    y += 30

    # Dynamic bullets from data
    total_jobs = mi['total_jobs']
    tools = mi.get('tools', {})
    sorted_tools = sorted(tools.items(), key=lambda x: -x[1])
    top_tool_name = SKILL_DISPLAY.get(sorted_tools[0][0], sorted_tools[0][0]) if sorted_tools else "HubSpot"
    top_tool_pct = round(sorted_tools[0][1] / total_jobs * 100, 1) if sorted_tools else 0
    median_k = int(signals.get('median_salary', 0) / 1000) if signals.get('median_salary', 0) > 0 else 120

    bullets = [
        f"Salary data from {total_jobs:,} GTM Engineer postings",
        f"Top tool: {top_tool_name} ({top_tool_pct}% of jobs)",
        f"Median GTM Engineer salary: ${median_k}K",
        "Tools tracked weekly with trends",
        "Free weekly email, every Monday",
    ]
    for bullet in bullets:
        draw.text((80, y), f"\u2022  {bullet}", fill=GRAY_200, font=font_bullet)
        y += 42

    y += 40
    draw_rounded_rect(draw, (60, y, W - 60, y + 80), fill=ACCENT)
    url_text = "gtmepulse.com/newsletter"
    bbox = draw.textbbox((0, 0), url_text, font=font_url)
    text_w = bbox[2] - bbox[0]
    draw.text(((W - text_w) // 2, y + 22), url_text, fill=NAVY, font=font_url)

    y += 120
    draw.text((60, y), "Follow for weekly GTM Engineer market data", fill=GRAY_400, font=font_med)

    slide_footer(draw, total_pages, total_pages)
    return img


# ---------------------------------------------------------------------------
# LinkedIn post text generator
# ---------------------------------------------------------------------------

def generate_post_text(mi, ca, jobs, prev, date_str):
    """Generate a LinkedIn post text file with rotating hooks."""
    total_jobs = mi['total_jobs']
    tools = mi.get('tools', {})
    sorted_tools = sorted(tools.items(), key=lambda x: -x[1])
    prev_tools = prev.get('tools', {}) if prev else {}
    salary_stats = ca.get('salary_stats', {})
    median = salary_stats.get('median', 0)
    median_k = int(median / 1000) if median > 0 else 0
    disclosure = ca.get('disclosure_rate', 0)

    # Growth hire percentage from market intelligence
    growth_pct = mi.get('growth_hire_pct', 0)
    equity_pct = mi.get('equity_pct', 0)

    # Top 3 tool display names
    top_tools = []
    for name, _ in sorted_tools[:3]:
        top_tools.append(SKILL_DISPLAY.get(name, name))

    # Build candidate hooks
    candidates = []

    # Salary change hook
    if prev:
        prev_salary = prev.get('salary_stats', {}).get('median', 0)
        if prev_salary > 0 and median > 0 and prev_salary != median:
            candidates.append(f"GTM Engineer median salary shifted to ${median_k}K")

    # Biggest tool mover hook
    if prev_tools:
        biggest_increase = 0
        biggest_tool = None
        for name, count in tools.items():
            pc = prev_tools.get(name, 0)
            if pc > 0:
                increase = count - pc
                if increase > biggest_increase:
                    biggest_increase = increase
                    biggest_tool = name
        if biggest_tool and biggest_increase > 0:
            display = SKILL_DISPLAY.get(biggest_tool, biggest_tool)
            candidates.append(f"{display} surged +{biggest_increase} mentions")

    # Total jobs hook
    candidates.append(f"{total_jobs:,} GTM Engineer roles tracked this week")

    # Hiring signal hook
    if growth_pct > 60:
        candidates.append(f"{growth_pct}% of GTME openings are growth hires")

    # Equity hook
    if equity_pct > 50:
        candidates.append(f"{equity_pct}% of GTM Engineer roles offer equity")

    # Default hook (always present as fallback)
    candidates.append(f"{total_jobs:,} active GTM Engineer roles this week")

    # Rotate weekly
    week_num = datetime.now().isocalendar()[1]
    hook = candidates[week_num % len(candidates)]

    # Build post body
    tools_line = ", ".join(top_tools) if top_tools else "N/A"
    post = f"""{hook}

This week's GTME Pulse ({total_jobs:,} roles):

\u2192 Median salary: ${median_k}K
\u2192 Top tools: {tools_line}
\u2192 {growth_pct}% growth hires
\u2192 {disclosure}% disclose pay

Swipe for the full breakdown \u2193

#GTMEngineer #GoToMarket #B2BSales #SalesOps #CareerData"""

    path = os.path.join(OUTPUT_DIR, 'post.txt')
    with open(path, 'w') as f:
        f.write(post)
    print(f"  Post: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Generate LinkedIn carousel images')
    parser.add_argument('--pdf', action='store_true', help='Also combine slides into a PDF')
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    mi, ca, jobs, prev = load_data()
    date_str = datetime.now().strftime('%B %d, %Y')
    signals = generate_carousel_signals(mi, ca, prev)

    total_pages = 6
    slides = [
        make_cover(mi, ca, date_str, total_pages, signals),
        make_tools_slide(mi, prev, total_pages),
        make_salary_slide(ca, prev, total_pages),
        make_insight_slide(mi, ca, prev, signals, total_pages),
        make_companies_slide(jobs, prev, total_pages),
        make_cta_slide(mi, signals, total_pages),
    ]

    paths = []
    for i, slide in enumerate(slides, 1):
        path = os.path.join(OUTPUT_DIR, f'slide-{i:02d}.png')
        slide.save(path, 'PNG', quality=95)
        paths.append(path)
        print(f"  Saved: {path}")

    if args.pdf:
        pdf_path = os.path.join(OUTPUT_DIR, 'gtme-pulse-carousel.pdf')
        rgb_slides = [s.convert('RGB') for s in slides]
        rgb_slides[0].save(pdf_path, 'PDF', save_all=True,
                           append_images=rgb_slides[1:], resolution=150)
        print(f"  PDF: {pdf_path}")

    generate_post_text(mi, ca, jobs, prev, date_str)

    print(f"\n{len(slides)} carousel slides generated in {OUTPUT_DIR}/")
    if signals.get('cover_hook'):
        print(f"  Cover hook: {signals['cover_hook']}")


if __name__ == '__main__':
    main()
