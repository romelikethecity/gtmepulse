#!/usr/bin/env python3
"""
Generate and send the GTME Pulse weekly data email.

Compares this week's job data to last week's and produces a zero-writing-effort
email with market numbers, salary snapshots, tool trends, and hiring signals.

Usage:
    python scripts/generate_weekly_email.py --preview          # Generate HTML preview
    python scripts/generate_weekly_email.py --send             # Send to all subscribers
    python scripts/generate_weekly_email.py --add-subscriber EMAIL
    python scripts/generate_weekly_email.py --list-subscribers
"""

import argparse
import json
import os
import sys
from datetime import datetime
from collections import Counter

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PREVIOUS_SNAPSHOT_FILE = os.path.join(DATA_DIR, 'previous_market_snapshot.json')

# Brand constants (from tokens.css)
BRAND = {
    'bg': '#0D0D0D',
    'surface': '#1A1A1A',
    'accent': '#FF4F1F',
    'accent_light': '#FF7A52',
    'accent_dark': '#CC3F19',
    'text': '#E8E8E8',
    'muted': '#666666',
    'green': '#22c55e',
    'red': '#ef4444',
    'border': '#2A1A16',
}

FROM_EMAIL = "The GTME Pulse <insights@gtmepulse.com>"
SITE_URL = "https://gtmepulse.com"

# Tool display name overrides
TOOL_DISPLAY = {
    'Hubspot': 'HubSpot', 'Zoominfo': 'ZoomInfo', 'Salesloft': 'SalesLoft',
    'Linkedin Sales Navigator': 'LinkedIn Sales Navigator', 'N8N': 'n8n',
    'Openai': 'OpenAI', 'Salesforce Cpq': 'Salesforce CPQ',
    'Leandata': 'LeanData', 'Phantombuster': 'PhantomBuster',
}


def load_json_safe(path):
    """Load a JSON file, returning None if missing or invalid."""
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def load_current_data():
    """Load current market intelligence and comp analysis. Graceful if missing."""
    mi = load_json_safe(os.path.join(DATA_DIR, 'market_intelligence.json'))
    ca = load_json_safe(os.path.join(DATA_DIR, 'comp_analysis.json'))
    jobs_raw = load_json_safe(os.path.join(DATA_DIR, 'jobs.json')) or []
    jobs = jobs_raw.get('jobs', jobs_raw) if isinstance(jobs_raw, dict) else jobs_raw

    # Defaults for missing data
    if mi is None:
        mi = {'total_jobs': 0, 'tools': {}, 'hiring_signals': {}}
    if ca is None:
        ca = {'salary_stats': {'median': 0, 'avg': 0}, 'by_seniority': {}, 'disclosure_rate': 0}

    return mi, ca, jobs


def load_previous_snapshot():
    """Load previous week's snapshot for diff calculation."""
    return load_json_safe(PREVIOUS_SNAPSHOT_FILE)


def save_current_as_snapshot(market_intel, comp_analysis, jobs):
    """Save current data as snapshot for next week's diff."""
    salary_history = []
    prev = load_json_safe(PREVIOUS_SNAPSHOT_FILE)
    if prev:
        salary_history = prev.get('salary_history', [])

    current_median = comp_analysis.get('salary_stats', {}).get('median', 0)
    salary_history.append({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'median': current_median,
    })
    salary_history = salary_history[-52:]

    snapshot = {
        'saved_at': datetime.now().isoformat(),
        'total_jobs': market_intel.get('total_jobs', 0),
        'tools': market_intel.get('tools', {}),
        'salary_median': current_median,
        'salary_avg': comp_analysis.get('salary_stats', {}).get('avg', 0),
        'by_seniority': comp_analysis.get('by_seniority', {}),
        'company_counts': dict(Counter(j.get('company', '') for j in jobs).most_common(50)),
        'hiring_signals': market_intel.get('hiring_signals', {}),
        'salary_history': salary_history,
    }
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PREVIOUS_SNAPSHOT_FILE, 'w') as f:
        json.dump(snapshot, f, indent=2)


# ---------------------------------------------------------------------------
# Diff computation
# ---------------------------------------------------------------------------

def compute_diff(current_mi, current_ca, current_jobs, previous):
    """Compute week-over-week changes."""
    diff = {}

    current_total = current_mi.get('total_jobs', 0)
    prev_total = previous.get('total_jobs', current_total) if previous else current_total
    diff['total_jobs'] = current_total
    diff['job_change'] = current_total - prev_total

    current_median = current_ca.get('salary_stats', {}).get('median', 0)
    prev_median = previous.get('salary_median', current_median) if previous else current_median
    diff['salary_median'] = current_median
    diff['salary_change'] = current_median - prev_median

    # Seniority salary changes
    diff['seniority'] = {}
    current_sen = current_ca.get('by_seniority', {})
    prev_sen = previous.get('by_seniority', {}) if previous else {}
    for level in ['Entry', 'Mid', 'Senior', 'Lead', 'Staff', 'Manager', 'Director', 'VP']:
        curr = current_sen.get(level, {})
        prev_s = prev_sen.get(level, {})
        curr_med = curr.get('median', 0)
        prev_med = prev_s.get('median', 0)
        if curr_med > 0:
            diff['seniority'][level] = {
                'median': curr_med,
                'change': curr_med - prev_med if prev_med > 0 else 0,
                'count': curr.get('count', 0),
            }

    # Tool trends — filter to actual GTM stack products, not languages/techniques
    # Build a set of non-tool names to exclude from the trends display
    EXCLUDED_TOOLS = {
        # Languages / general tech (skills, not products)
        'Python', 'Rust', 'Javascript', 'Typescript', 'Sql', 'R',
        # AI techniques (concepts, not products)
        'Rag', 'Embeddings', 'Prompt Engineering', 'Fine Tuning',
        # Infrastructure (too generic)
        'Aws', 'Gcp', 'Azure',
        # Vector DBs / frameworks (infra, not GTM tools)
        'Pinecone', 'Weaviate', 'Pgvector', 'Langchain', 'Llamaindex',
    }
    current_tools = current_mi.get('tools', {})
    prev_tools = previous.get('tools', {}) if previous else {}
    tool_changes = []
    skill_changes = []
    for tool, count in current_tools.items():
        prev_count = prev_tools.get(tool, 0)
        change = count - prev_count
        entry = {'name': tool, 'count': count, 'change': change}
        if tool in EXCLUDED_TOOLS:
            if abs(change) > 0 or count >= 3:
                skill_changes.append(entry)
        else:
            if abs(change) > 0 or count >= 5:
                tool_changes.append(entry)
    tool_changes.sort(key=lambda x: -x['count'])
    skill_changes.sort(key=lambda x: -x['count'])
    diff['tools'] = tool_changes[:10]
    diff['skills'] = skill_changes[:5]

    # Top companies
    company_counts = Counter(j.get('company', '') for j in current_jobs if j.get('company'))
    top_companies = company_counts.most_common(5)
    prev_companies = previous.get('company_counts', {}) if previous else {}

    diff['top_companies'] = []
    for company, count in top_companies:
        prev_count = prev_companies.get(company, 0)
        co_jobs = [j for j in current_jobs if j.get('company') == company]
        salary_jobs = [j for j in co_jobs if j.get('max_amount') and j['max_amount'] > 0]
        avg_mid = 0
        if salary_jobs:
            avg_mid = int(sum((j.get('min_amount', 0) + j['max_amount']) / 2 for j in salary_jobs) / len(salary_jobs))
        remote_count = sum(1 for j in co_jobs if j.get('is_remote'))

        diff['top_companies'].append({
            'name': company,
            'count': count,
            'change': count - prev_count,
            'avg_midpoint': avg_mid,
            'remote': remote_count,
        })

    diff['signals'] = current_mi.get('hiring_signals', {})
    diff['disclosure_rate'] = current_ca.get('disclosure_rate', 0)

    # Top paying roles (title-level salary data)
    diff['top_paying_roles'] = current_ca.get('top_paying_roles', [])[:5]

    # Location breakdown
    location_counts = Counter()
    for j in current_jobs:
        loc = j.get('location', '')
        if not loc:
            continue
        # Normalize to city-level
        if j.get('is_remote'):
            location_counts['Remote'] += 1
        elif 'San Francisco' in loc or 'SF' in loc:
            location_counts['San Francisco'] += 1
        elif 'New York' in loc or 'NYC' in loc:
            location_counts['New York'] += 1
        elif 'Austin' in loc:
            location_counts['Austin'] += 1
        elif 'Boston' in loc:
            location_counts['Boston'] += 1
        elif 'Denver' in loc:
            location_counts['Denver'] += 1
        elif 'Los Angeles' in loc or 'LA' in loc:
            location_counts['Los Angeles'] += 1
        elif 'Chicago' in loc:
            location_counts['Chicago'] += 1
        elif 'Seattle' in loc:
            location_counts['Seattle'] += 1
        else:
            location_counts['Other'] += 1
    diff['locations'] = location_counts.most_common(6)

    # Remote rate
    remote_count = sum(1 for j in current_jobs if j.get('is_remote'))
    diff['remote_pct'] = round(remote_count / len(current_jobs) * 100) if current_jobs else 0

    return diff


# ---------------------------------------------------------------------------
# Email HTML generation
# ---------------------------------------------------------------------------

def trend_arrow(val):
    """Return a colored arrow for a value change."""
    if val > 0:
        return f'<span style="color: {BRAND["green"]};">&#9650; +{val:,}</span>'
    elif val < 0:
        return f'<span style="color: {BRAND["red"]};">&#9660; {val:,}</span>'
    else:
        return f'<span style="color: {BRAND["muted"]};">&#9472; flat</span>'


def trend_arrow_salary(val):
    """Arrow for salary changes (in dollars)."""
    if val > 0:
        return f'<span style="color: {BRAND["green"]};">&#9650; +${val:,}</span>'
    elif val < 0:
        return f'<span style="color: {BRAND["red"]};">&#9660; -${abs(val):,}</span>'
    else:
        return f'<span style="color: {BRAND["muted"]};">&#9472; flat</span>'


def generate_email_html(diff, date_str):
    """Generate the full branded GTME Pulse email HTML."""

    has_data = diff['total_jobs'] > 0

    if not has_data:
        # Graceful degradation: no data available
        return f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body style="margin: 0; padding: 0; background: {BRAND['bg']}; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['bg']};">
<tr><td align="center" style="padding: 20px 10px;">
<table width="600" cellpadding="0" cellspacing="0" style="max-width: 600px; width: 100%;">

    <!-- Header -->
    <tr><td style="padding: 24px 24px 20px;">
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td width="44" valign="middle">
                    <div style="width: 40px; height: 40px; display: inline-block;">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="40" height="40"><rect width="36" height="36" rx="8" fill="#FF4F1F"/><polyline points="7,18 12,18 15,11 18,25 21,13 24,21 27,18 29,18" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </div>
                </td>
                <td valign="middle" style="padding-left: 12px;">
                    <span style="font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 600;"><span style="color: {BRAND['text']};">GTME</span><span style="color: {BRAND['accent']};">Pulse</span></span>
                </td>
            </tr>
        </table>
    </td></tr>

    <tr><td style="padding: 24px; text-align: center;">
        <h1 style="margin: 0 0 16px; font-size: 24px; color: {BRAND['text']}; font-family: 'Sora', sans-serif;">No new data this week</h1>
        <p style="margin: 0; font-size: 15px; color: {BRAND['accent_dark']}; line-height: 1.6;">The scraper hasn't collected new job data yet. Check back next Monday for fresh GTM Engineer market intelligence.</p>
    </td></tr>

    <tr><td style="padding: 16px 24px; border-top: 1px solid {BRAND['border']}; text-align: center;">
        <p style="margin: 0; font-size: 12px; color: {BRAND['muted']};">
            <a href="{SITE_URL}" style="color: {BRAND['accent']}; text-decoration: none;">GTME Pulse</a> &middot; Career intelligence for GTM Engineers
        </p>
    </td></tr>

</table>
</td></tr>
</table>
</body>
</html>'''

    # Seniority rows
    seniority_rows = ""
    for level in ['VP', 'Director', 'Lead', 'Staff', 'Senior', 'Mid', 'Entry']:
        data = diff['seniority'].get(level, {})
        if data.get('median', 0) > 0:
            seniority_rows += f'''
            <tr>
                <td style="padding: 8px 12px; color: {BRAND['text']}; border-bottom: 1px solid {BRAND['border']};">{level}</td>
                <td style="padding: 8px 12px; color: {BRAND['accent_light']}; font-weight: 600; border-bottom: 1px solid {BRAND['border']};">${data['median']:,}</td>
                <td style="padding: 8px 12px; border-bottom: 1px solid {BRAND['border']};">{trend_arrow_salary(data['change'])}</td>
                <td style="padding: 8px 12px; color: {BRAND['muted']}; border-bottom: 1px solid {BRAND['border']};">{data['count']}</td>
            </tr>'''

    # Tool rows
    tool_rows = ""
    for tool in diff['tools'][:10]:
        pct = round(tool['count'] / diff['total_jobs'] * 100, 1) if diff['total_jobs'] > 0 else 0
        display_name = TOOL_DISPLAY.get(tool['name'], tool['name'])
        tool_rows += f'''
        <tr>
            <td style="padding: 6px 12px; color: {BRAND['text']}; border-bottom: 1px solid {BRAND['border']};">{display_name}</td>
            <td style="padding: 6px 12px; color: {BRAND['accent_light']}; border-bottom: 1px solid {BRAND['border']};">{tool['count']:,} ({pct}%)</td>
            <td style="padding: 6px 12px; border-bottom: 1px solid {BRAND['border']};">{trend_arrow(tool['change'])}</td>
        </tr>'''

    # Company rows
    company_rows = ""
    for co in diff['top_companies'][:5]:
        sal_str = f"${int(co['avg_midpoint']/1000)}K" if co['avg_midpoint'] > 0 else "-"
        remote_str = f"{co['remote']} remote" if co['remote'] > 0 else "on-site"
        company_rows += f'''
        <tr>
            <td style="padding: 8px 12px; border-bottom: 1px solid {BRAND['border']};">
                <a href="{SITE_URL}/companies/{co['name'].lower().replace(' ', '-').replace('.', '')[:60]}/" style="color: {BRAND['accent_light']}; text-decoration: none;">{co['name']}</a>
            </td>
            <td style="padding: 8px 12px; color: {BRAND['accent_light']}; font-weight: 600; border-bottom: 1px solid {BRAND['border']};">{co['count']}</td>
            <td style="padding: 8px 12px; color: {BRAND['muted']}; border-bottom: 1px solid {BRAND['border']};">{sal_str}</td>
            <td style="padding: 8px 12px; color: {BRAND['muted']}; border-bottom: 1px solid {BRAND['border']};">{remote_str}</td>
        </tr>'''

    # Top paying roles rows
    top_roles_rows = ""
    for role in diff.get('top_paying_roles', [])[:5]:
        sal_min = role.get('salary_min', 0)
        sal_max = role.get('salary_max', 0)
        if sal_max > 0:
            range_str = f"${int(sal_min/1000)}K-${int(sal_max/1000)}K"
        else:
            range_str = "-"
        company = role.get('company', '') or 'Stealth'
        title = role.get('title', '')
        # Truncate long titles
        if len(title) > 40:
            title = title[:37] + '...'
        top_roles_rows += f'''
        <tr>
            <td style="padding: 8px 12px; color: {BRAND['text']}; border-bottom: 1px solid {BRAND['border']}; font-size: 13px;">{title}</td>
            <td style="padding: 8px 12px; color: {BRAND['muted']}; border-bottom: 1px solid {BRAND['border']}; font-size: 13px;">{company}</td>
            <td style="padding: 8px 12px; color: {BRAND['accent_light']}; font-weight: 600; border-bottom: 1px solid {BRAND['border']}; font-size: 13px; white-space: nowrap;">{range_str}</td>
        </tr>'''

    # Skill/tech rows (languages, AI techniques — separate from GTM tools)
    skill_rows = ""
    SKILL_DISPLAY = {'Rag': 'RAG', 'Aws': 'AWS', 'Gcp': 'GCP', 'Openai': 'OpenAI', 'Langchain': 'LangChain', 'Llamaindex': 'LlamaIndex'}
    for skill in diff.get('skills', [])[:5]:
        s_pct = round(skill['count'] / diff['total_jobs'] * 100, 1) if diff['total_jobs'] > 0 else 0
        s_name = SKILL_DISPLAY.get(skill['name'], skill['name'])
        skill_rows += f'''
        <tr>
            <td style="padding: 6px 12px; color: {BRAND['text']}; border-bottom: 1px solid {BRAND['border']};">{s_name}</td>
            <td style="padding: 6px 12px; color: {BRAND['accent_light']}; border-bottom: 1px solid {BRAND['border']};">{skill['count']:,} ({s_pct}%)</td>
            <td style="padding: 6px 12px; border-bottom: 1px solid {BRAND['border']};">{trend_arrow(skill['change'])}</td>
        </tr>'''

    # Location rows
    location_rows = ""
    for loc_name, loc_count in diff.get('locations', []):
        loc_pct = round(loc_count / diff['total_jobs'] * 100) if diff['total_jobs'] > 0 else 0
        # Bar width as percentage of max
        max_count = diff['locations'][0][1] if diff.get('locations') else 1
        bar_width = round(loc_count / max_count * 100)
        location_rows += f'''
        <tr>
            <td style="padding: 6px 12px; color: {BRAND['text']}; border-bottom: 1px solid {BRAND['border']};">{loc_name}</td>
            <td style="padding: 6px 12px; border-bottom: 1px solid {BRAND['border']}; width: 50%;">
                <div style="background: {BRAND['border']}; border-radius: 4px; height: 8px; width: 100%;">
                    <div style="background: {BRAND['accent']}; border-radius: 4px; height: 8px; width: {bar_width}%;"></div>
                </div>
            </td>
            <td style="padding: 6px 12px; color: {BRAND['muted']}; border-bottom: 1px solid {BRAND['border']}; white-space: nowrap;">{loc_count} ({loc_pct}%)</td>
        </tr>'''

    # Hiring signals
    growth = diff['signals'].get('Growth Hire', 0)
    turnaround = diff['signals'].get('Turnaround', 0)
    immediate = diff['signals'].get('Immediate', 0)
    growth_pct = round(growth / diff['total_jobs'] * 100) if diff['total_jobs'] > 0 else 0
    turnaround_pct = round(turnaround / diff['total_jobs'] * 100) if diff['total_jobs'] > 0 else 0

    html = f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body style="margin: 0; padding: 0; background: {BRAND['bg']}; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['bg']};">
<tr><td align="center" style="padding: 20px 10px;">
<table width="600" cellpadding="0" cellspacing="0" style="max-width: 600px; width: 100%;">

    <!-- Header with Logo -->
    <tr><td style="padding: 24px 24px 20px;">
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td width="44" valign="middle">
                    <div style="width: 40px; height: 40px; display: inline-block;">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="40" height="40"><rect width="36" height="36" rx="8" fill="#FF4F1F"/><polyline points="7,18 12,18 15,11 18,25 21,13 24,21 27,18 29,18" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </div>
                </td>
                <td valign="middle" style="padding-left: 12px;">
                    <span style="font-family: 'Sora', sans-serif; font-size: 18px; font-weight: 600;"><span style="color: {BRAND['text']};">GTME</span><span style="color: {BRAND['accent']};">Pulse</span></span>
                </td>
            </tr>
        </table>
    </td></tr>

    <!-- Title -->
    <tr><td style="padding: 0 24px 16px; border-bottom: 2px solid {BRAND['accent']};">
        <h1 style="margin: 0 0 6px; font-size: 32px; font-weight: 700; color: {BRAND['text']}; font-family: 'Sora', sans-serif; letter-spacing: -0.5px;">GTM ENGINEER MARKET PULSE</h1>
        <p style="margin: 0; font-size: 14px; color: {BRAND['muted']};">Week of {date_str} &middot; {diff['total_jobs']:,} active roles &middot; {diff['disclosure_rate']}% salary disclosure</p>
    </td></tr>

    <!-- Active Roles + Median Salary -->
    <tr><td style="padding: 24px 24px 12px;">
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td width="50%" style="padding-right: 6px;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['surface']}; border-radius: 8px;">
                        <tr><td style="padding: 16px 20px;">
                            <div style="font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase; letter-spacing: 1px;">Active Roles</div>
                            <div style="font-size: 32px; font-weight: 700; color: {BRAND['accent']}; font-family: 'Sora', sans-serif; margin-top: 4px;">{diff['total_jobs']:,}</div>
                            <div style="font-size: 13px; margin-top: 6px;">{trend_arrow(diff['job_change'])} <span style="color: {BRAND['muted']};">vs last week</span></div>
                        </td></tr>
                    </table>
                </td>
                <td width="50%" style="padding-left: 6px;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['surface']}; border-radius: 8px;">
                        <tr><td style="padding: 16px 20px;">
                            <div style="font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase; letter-spacing: 1px;">Median Salary</div>
                            <div style="font-size: 32px; font-weight: 700; color: {BRAND['green']}; font-family: 'Sora', sans-serif; margin-top: 4px;">${int(diff['salary_median']/1000)}K</div>
                            <div style="font-size: 13px; margin-top: 6px;">{trend_arrow_salary(diff['salary_change'])} <span style="color: {BRAND['muted']};">vs last week</span></div>
                        </td></tr>
                    </table>
                </td>
            </tr>
        </table>
    </td></tr>

    <!-- Signal Strip -->
    <tr><td style="padding: 0 24px 24px;">
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td width="33%" style="padding: 10px; background: {BRAND['surface']}; border-radius: 8px; text-align: center;">
                    <div style="font-size: 24px; font-weight: 700; color: {BRAND['green']};">{growth_pct}%</div>
                    <div style="font-size: 11px; color: {BRAND['muted']}; margin-top: 2px;">Growth Hires</div>
                </td>
                <td width="4"></td>
                <td width="33%" style="padding: 10px; background: {BRAND['surface']}; border-radius: 8px; text-align: center;">
                    <div style="font-size: 24px; font-weight: 700; color: {BRAND['accent']};">{turnaround_pct}%</div>
                    <div style="font-size: 11px; color: {BRAND['muted']}; margin-top: 2px;">Turnaround</div>
                </td>
                <td width="4"></td>
                <td width="33%" style="padding: 10px; background: {BRAND['surface']}; border-radius: 8px; text-align: center;">
                    <div style="font-size: 24px; font-weight: 700; color: {BRAND['accent_light']};">{diff['remote_pct']}%</div>
                    <div style="font-size: 11px; color: {BRAND['muted']}; margin-top: 2px;">Remote</div>
                </td>
            </tr>
        </table>
    </td></tr>

    <!-- Salary Snapshot -->
    {f"""<tr><td style="padding: 0 24px 24px;">
        <h2 style="margin: 0 0 12px; font-size: 16px; color: {BRAND['accent']}; text-transform: uppercase; letter-spacing: 1px; font-family: 'Sora', sans-serif;">Salary Snapshot</h2>
        <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['surface']}; border-radius: 8px;">
            <tr>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Level</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Median</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">vs Last</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Roles</th>
            </tr>
            {seniority_rows}
        </table>
    </td></tr>""" if seniority_rows else ""}

    <!-- Top Paying Roles -->
    {f"""<tr><td style="padding: 0 24px 24px;">
        <h2 style="margin: 0 0 12px; font-size: 16px; color: {BRAND['accent']}; text-transform: uppercase; letter-spacing: 1px; font-family: 'Sora', sans-serif;">Top Paying Roles</h2>
        <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['surface']}; border-radius: 8px;">
            <tr>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Title</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Company</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Range</th>
            </tr>
            {top_roles_rows}
        </table>
        <p style="font-size: 12px; color: {BRAND['muted']}; margin: 8px 0 0;">
            <a href="{SITE_URL}/salary/" style="color: {BRAND['accent']}; text-decoration: none;">Full salary benchmarks &rarr;</a>
        </p>
    </td></tr>""" if top_roles_rows else ""}

    <!-- Tool Trends -->
    {f"""<tr><td style="padding: 0 24px 24px;">
        <h2 style="margin: 0 0 12px; font-size: 16px; color: {BRAND['accent']}; text-transform: uppercase; letter-spacing: 1px; font-family: 'Sora', sans-serif;">Tool Trends</h2>
        <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['surface']}; border-radius: 8px;">
            <tr>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Tool</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Mentions</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">vs Last</th>
            </tr>
            {tool_rows}
        </table>
        <p style="font-size: 12px; color: {BRAND['muted']}; margin: 8px 0 0;">
            <a href="{SITE_URL}/tools/" style="color: {BRAND['accent']}; text-decoration: none;">Full tool reviews &rarr;</a>
        </p>
    </td></tr>""" if tool_rows else ""}

    <!-- Skills & Tech -->
    {f"""<tr><td style="padding: 0 24px 24px;">
        <h2 style="margin: 0 0 12px; font-size: 16px; color: {BRAND['accent']}; text-transform: uppercase; letter-spacing: 1px; font-family: 'Sora', sans-serif;">Skills &amp; Tech</h2>
        <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['surface']}; border-radius: 8px;">
            <tr>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Skill</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Mentions</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">vs Last</th>
            </tr>
            {skill_rows}
        </table>
    </td></tr>""" if skill_rows else ""}

    <!-- Top Companies -->
    {f"""<tr><td style="padding: 0 24px 24px;">
        <h2 style="margin: 0 0 12px; font-size: 16px; color: {BRAND['accent']}; text-transform: uppercase; letter-spacing: 1px; font-family: 'Sora', sans-serif;">Top Companies Hiring</h2>
        <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['surface']}; border-radius: 8px;">
            <tr>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Company</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Roles</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Avg Salary</th>
                <th style="padding: 10px 12px; text-align: left; font-size: 11px; color: {BRAND['muted']}; text-transform: uppercase;">Remote</th>
            </tr>
            {company_rows}
        </table>
    </td></tr>""" if company_rows else ""}

    <!-- Where the Jobs Are -->
    {f"""<tr><td style="padding: 0 24px 24px;">
        <h2 style="margin: 0 0 12px; font-size: 16px; color: {BRAND['accent']}; text-transform: uppercase; letter-spacing: 1px; font-family: 'Sora', sans-serif;">Where the Jobs Are</h2>
        <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['surface']}; border-radius: 8px;">
            {location_rows}
        </table>
    </td></tr>""" if location_rows else ""}

    <!-- Signal Watch -->
    <tr><td style="padding: 0 24px 24px;">
        <h2 style="margin: 0 0 12px; font-size: 16px; color: {BRAND['accent']}; text-transform: uppercase; letter-spacing: 1px; font-family: 'Sora', sans-serif;">Signal Watch</h2>
        <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['surface']}; border-radius: 8px;">
            <tr><td style="padding: 12px 16px; color: {BRAND['text']}; font-size: 14px; line-height: 2.0;">
                {f'<strong style="color: {BRAND["accent_light"]};">{growth:,}</strong> growth hires ({growth_pct}% of market) &middot; ' if growth else ''}
                {f'<strong>{turnaround:,}</strong> turnaround roles &middot; ' if turnaround else ''}
                {f'<strong>{immediate:,}</strong> immediate fill &middot; ' if immediate else ''}
                <strong style="color: {BRAND['accent_light']};">{diff['disclosure_rate']}%</strong> disclose salary &middot;
                <strong style="color: {BRAND['accent_light']};">{diff['remote_pct']}%</strong> offer remote
            </td></tr>
        </table>
    </td></tr>

    <!-- CTA -->
    <tr><td style="padding: 0 24px 24px; text-align: center;">
        <a href="{SITE_URL}/jobs/" style="display: inline-block; background: {BRAND['accent']}; color: #ffffff; padding: 14px 36px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 15px; font-family: 'Sora', sans-serif;">Browse All GTME Jobs</a>
        <p style="font-size: 13px; color: {BRAND['muted']}; margin: 14px 0 0;">
            <a href="{SITE_URL}/salary/" style="color: {BRAND['muted']}; text-decoration: underline;">Salary benchmarks</a> &middot;
            <a href="{SITE_URL}/tools/" style="color: {BRAND['muted']}; text-decoration: underline;">Tool reviews</a> &middot;
            <a href="{SITE_URL}/careers/" style="color: {BRAND['muted']}; text-decoration: underline;">Career guides</a>
        </p>
    </td></tr>

    <!-- Forward CTA -->
    <tr><td style="padding: 0 24px 24px;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background: {BRAND['surface']}; border-radius: 8px; border: 1px solid {BRAND['border']};">
            <tr><td style="padding: 20px 24px; text-align: center;">
                <p style="margin: 0 0 8px; font-size: 16px; font-weight: 600; color: {BRAND['text']}; font-family: 'Sora', sans-serif;">Know a GTM Engineer?</p>
                <p style="margin: 0 0 16px; font-size: 14px; color: {BRAND['muted']};">Forward this email to anyone building automated pipelines.</p>
                <p style="margin: 0; font-size: 13px; color: {BRAND['muted']};">
                    Not subscribed? <a href="{SITE_URL}/newsletter/" style="color: {BRAND['accent']}; text-decoration: underline; font-weight: 600;">Sign up here</a> - free, every Monday.
                </p>
            </td></tr>
        </table>
    </td></tr>

    <!-- Footer -->
    <tr><td style="padding: 16px 24px; border-top: 1px solid {BRAND['border']}; text-align: center;">
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td align="center" style="padding-bottom: 8px;">
                    <div style="width: 28px; height: 28px; display: inline-block;">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36" width="28" height="28"><rect width="36" height="36" rx="8" fill="#FF4F1F"/><polyline points="7,18 12,18 15,11 18,25 21,13 24,21 27,18 29,18" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </div>
                </td>
            </tr>
            <tr><td align="center">
                <p style="margin: 0; font-size: 12px; color: {BRAND['muted']}; line-height: 1.8;">
                    <a href="{SITE_URL}" style="color: {BRAND['accent']}; text-decoration: none; font-weight: 600;">GTME Pulse</a> &middot; Career intelligence for GTM Engineers<br>
                    Data from {diff['total_jobs']:,} active job postings, updated every Monday.<br>
                    <a href="{SITE_URL}/newsletter/" style="color: {BRAND['muted']}; text-decoration: underline;">Subscribe</a> &middot;
                    <a href="{SITE_URL}" style="color: {BRAND['muted']}; text-decoration: underline;">gtmepulse.com</a>
                </p>
            </td></tr>
        </table>
    </td></tr>

</table>
</td></tr>
</table>
</body>
</html>'''

    return html


# ---------------------------------------------------------------------------
# Subscriber management
# ---------------------------------------------------------------------------

D1_WORKER_URL = "https://newsletter-subscribe.rome-workers.workers.dev"
D1_LIST_SLUG = "gtme-pulse"


def load_subscribers_from_d1():
    """Load active subscribers from D1 via the universal newsletter worker."""
    import requests as req

    api_secret = os.environ.get('NEWSLETTER_API_SECRET', '')
    if not api_secret:
        print("Warning: NEWSLETTER_API_SECRET not set, skipping D1")
        return []

    try:
        resp = req.get(
            f"{D1_WORKER_URL}/subscribers/{D1_LIST_SLUG}",
            headers={"Authorization": f"Bearer {api_secret}"},
        )
        resp.raise_for_status()
        data = resp.json()
        return [{"email": s["email"]} for s in data if isinstance(s, dict)]
    except Exception as e:
        print(f"Error fetching from D1: {e}")
        return []


def load_subscribers_from_resend(api_key):
    """Load all subscribed contacts from Resend Audiences API (fallback)."""
    import requests as req

    audience_id = os.environ.get('RESEND_AUDIENCE_ID', '')
    if not audience_id:
        return []

    contacts = []
    url = f"https://api.resend.com/audiences/{audience_id}/contacts?limit=100"
    headers = {"Authorization": f"Bearer {api_key}"}

    while url:
        try:
            resp = req.get(url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"Error fetching contacts from Resend: {e}")
            break

        for contact in data.get("data", []):
            if not contact.get("unsubscribed", False):
                contacts.append({"email": contact["email"]})

        if data.get("has_more"):
            last_id = data["data"][-1]["id"]
            url = f"https://api.resend.com/audiences/{audience_id}/contacts?limit=100&after={last_id}"
        else:
            url = None

    return contacts


def add_subscriber_resend(api_key, email):
    """Add a subscriber via Resend Audiences API."""
    import requests as req

    audience_id = os.environ.get('RESEND_AUDIENCE_ID', '')
    if not audience_id:
        print("Error: RESEND_AUDIENCE_ID not set")
        return False

    try:
        resp = req.post(
            f"https://api.resend.com/audiences/{audience_id}/contacts",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"email": email, "unsubscribed": False},
        )
        resp.raise_for_status()
        print(f"Added: {email}")
        return True
    except Exception as e:
        print(f"Error adding {email}: {e}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='GTME Pulse weekly email')
    parser.add_argument('--preview', action='store_true', help='Generate HTML preview')
    parser.add_argument('--send', action='store_true', help='Send to all subscribers via Resend')
    parser.add_argument('--add-subscriber', type=str, metavar='EMAIL', help='Add subscriber')
    parser.add_argument('--list-subscribers', action='store_true', help='List all subscribers')
    parser.add_argument('--resend-key', type=str, help='Resend API key (or set RESEND_API_KEY)')
    parser.add_argument('--save-snapshot', action='store_true', help='Save current data as baseline for next diff')
    args = parser.parse_args()

    api_key = args.resend_key or os.environ.get('RESEND_API_KEY', '')

    if args.add_subscriber:
        if not api_key:
            print("Error: Resend API key required. Use --resend-key or set RESEND_API_KEY")
            sys.exit(1)
        add_subscriber_resend(api_key, args.add_subscriber)
        return

    if args.list_subscribers:
        d1_subs = load_subscribers_from_d1()
        resend_subs = load_subscribers_from_resend(api_key) if api_key else []
        seen = set()
        all_subs = []
        for s in d1_subs + resend_subs:
            if s['email'] not in seen:
                seen.add(s['email'])
                all_subs.append(s)
        print(f"Subscribers ({len(all_subs)}) [D1: {len(d1_subs)}, Resend: {len(resend_subs)}]:")
        for s in all_subs:
            print(f"  {s['email']}")
        return

    # Load data
    market_intel, comp_analysis, jobs = load_current_data()
    previous = load_previous_snapshot()

    # Compute diff
    diff = compute_diff(market_intel, comp_analysis, jobs, previous)

    # Generate email
    date_str = datetime.now().strftime('%B %d, %Y')
    if diff['total_jobs'] > 0 and diff['salary_median'] > 0:
        subject = f"GTM Engineer Market Pulse: {diff['total_jobs']:,} roles, ${int(diff['salary_median']/1000)}K median"
    else:
        subject = "GTM Engineer Market Pulse - Weekly Update"
    html = generate_email_html(diff, date_str)

    if args.save_snapshot:
        save_current_as_snapshot(market_intel, comp_analysis, jobs)
        print(f"Snapshot saved to {PREVIOUS_SNAPSHOT_FILE}")
        return

    if args.preview:
        preview_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'email_preview.html')
        with open(preview_path, 'w') as f:
            f.write(html)
        print(f"Preview saved to: {preview_path}")
        print(f"Subject: {subject}")
        print(f"Open: file://{preview_path}")
        return

    if args.send:
        if not api_key:
            print("Error: Resend API key required. Use --resend-key or set RESEND_API_KEY")
            sys.exit(1)

        try:
            import resend
        except ImportError:
            print("Error: 'resend' package not installed. Run: pip install resend")
            sys.exit(1)

        resend.api_key = api_key

        # Load from D1 (primary) + Resend (fallback), dedupe
        print("Fetching subscribers from D1...")
        d1_subs = load_subscribers_from_d1()
        print(f"  D1: {len(d1_subs)} subscribers")
        resend_subs = load_subscribers_from_resend(api_key)
        print(f"  Resend: {len(resend_subs)} subscribers")

        seen = set()
        subs = []
        for s in d1_subs + resend_subs:
            if s['email'] not in seen:
                seen.add(s['email'])
                subs.append(s)

        if not subs:
            print("No subscribers found. Sign up at gtmepulse.com/newsletter/")
            return

        print(f"Sending to {len(subs)} subscribers...")
        sent = 0
        for sub in subs:
            try:
                resend.Emails.send({
                    "from": FROM_EMAIL,
                    "to": [sub['email']],
                    "subject": subject,
                    "html": html,
                })
                sent += 1
                print(f"  Sent: {sub['email']}")
            except Exception as e:
                print(f"  Failed: {sub['email']} - {e}")

        print(f"\nSent {sent}/{len(subs)} emails")

        # Save snapshot for next week's diff
        save_current_as_snapshot(market_intel, comp_analysis, jobs)
        print("Snapshot saved for next week's comparison")
        return

    # Default: show help
    parser.print_help()


if __name__ == '__main__':
    main()
