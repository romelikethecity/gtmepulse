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
                       get_breadcrumb_schema, get_faq_schema, breadcrumb_html,
                       newsletter_cta_html, faq_html, ALL_PAGES)

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
# Salary Data (State of GTM Engineering Report 2026, n=228)
# ---------------------------------------------------------------------------

def fmt_salary(n):
    """Format salary number: 132000 -> '$132K'"""
    return f"${n // 1000}K"


REPORT_CITATION = "State of GTM Engineering Report 2026 (n=228)"

def source_citation_html():
    """Visible source citation block for salary pages."""
    return f'''<div class="source-citation">
    <p><strong>Source:</strong> {REPORT_CITATION}. Salary data combines survey responses from 228 GTM Engineers across 32 countries with analysis of 3,342 job postings.</p>
</div>'''


SALARY_BY_SENIORITY = {
    "junior": {
        "label": "Junior / Associate",
        "slug": "junior",
        "min": 90000, "max": 130000, "median": 110000,
        "sample": 45,
        "context": [
            "Junior GTM Engineers typically have 0-2 years of experience and enter the role from SDR, sales ops, or marketing ops backgrounds. Many are self-taught Clay and automation builders who proved their skills before getting the title.",
            "At this level, you're expected to build and maintain outbound sequences, manage data enrichment workflows, and keep CRM data clean. The tools are familiar (Clay, Apollo, HubSpot) but the systems thinking is still developing.",
            "Compensation skews toward base salary with limited variable comp. Equity is rare at this level unless you're at an early-stage startup where everyone gets a small grant.",
        ],
        "drivers": [
            "Prior SDR or ops experience that translates directly",
            "Clay certification or demonstrable Clay table portfolio",
            "Python or SQL skills (even basic) command a 10-15% premium",
            "Location: SF/NYC junior roles pay 15-20% above Austin or remote equivalents",
        ],
        "total_comp": "Most junior GTM Engineers earn base salary only. Some companies offer quarterly bonuses tied to pipeline generated or meetings booked. Expect $90K-$130K all-in for your first 1-2 years.",
    },
    "mid": {
        "label": "Mid-Level",
        "slug": "mid-level",
        "min": 130000, "max": 175000, "median": 150000,
        "sample": 78,
        "context": [
            "Mid-level GTM Engineers have 2-4 years of experience and own significant parts of the outbound pipeline. You're building multi-step Clay tables, managing enrichment waterfalls, and starting to architect systems rather than just executing playbooks.",
            "This is where compensation starts to differentiate sharply. Engineers who can write Python scripts, build Make/n8n automations, and integrate APIs earn materially more than those who rely solely on no-code tools.",
            "Demand for mid-level talent is the highest of any seniority band. Companies that have proven GTM Engineering works are scaling their teams, and they want people who can hit the ground running.",
        ],
        "drivers": [
            "Technical depth: Python, API integration, SQL all push you toward the top of the range",
            "Ownership scope: managing full enrichment pipelines vs. individual sequences",
            "Industry: fintech and cybersecurity GTM teams pay 10-15% above median",
            "Tool breadth: experience across 3+ tool categories signals versatility",
        ],
        "total_comp": "Variable compensation enters the picture at mid-level. Expect 10-20% of base in bonuses or OTE. Some companies offer equity refreshers. Total comp range: $145K-$210K when you include bonuses and equity.",
    },
    "senior": {
        "label": "Senior",
        "slug": "senior",
        "min": 175000, "max": 225000, "median": 195000,
        "sample": 65,
        "context": [
            "Senior GTM Engineers are system architects. You're designing the entire outbound data infrastructure, choosing the tool stack, building custom integrations, and mentoring junior team members.",
            "At this level, the line between GTM Engineer and engineering manager blurs. Many senior GTM Engineers report directly to the VP of Sales or CRO and have significant influence over pipeline strategy.",
            "The biggest salary jumps come from moving into companies where GTM Engineering is a strategic priority, not a cost center. When the CEO understands what you do, compensation follows.",
        ],
        "drivers": [
            "Architecture ownership: designing systems from scratch vs. maintaining existing ones",
            "Cross-functional influence: working directly with sales leadership and product",
            "Custom code: building proprietary tools or integrations that create competitive advantage",
            "Team leadership: managing or mentoring 2-3 junior GTM Engineers",
        ],
        "total_comp": "Senior GTM Engineers frequently earn 20-30% above base in variable comp. Equity becomes significant at growth-stage companies. Total comp: $200K-$280K. Top performers at well-funded Series B/C companies can clear $300K all-in.",
    },
    "lead": {
        "label": "Lead / Staff",
        "slug": "lead-staff",
        "min": 225000, "max": 300000, "median": 250000,
        "sample": 40,
        "context": [
            "Lead and Staff GTM Engineers are rare. Fewer than 200 roles at this level exist in public job postings. You're setting the GTM Engineering strategy for the entire organization.",
            "At this level, you're evaluating and selecting the company's entire GTM tech stack, building proprietary data pipelines, and often managing a team of 3-8 GTM Engineers. The title might be Head of GTM Engineering, Director of Revenue Engineering, or VP of GTM Systems.",
            "Compensation at this tier is heavily weighted toward equity and variable comp. Base salary matters less than total package, especially at pre-IPO companies where equity could be worth multiples of base.",
        ],
        "drivers": [
            "Organizational scope: company-wide GTM infrastructure vs. single team",
            "Revenue impact: directly attributable pipeline and closed-won revenue",
            "Equity stage: pre-IPO companies offer packages that can 2-3x base salary",
            "Industry reputation: speaking at conferences, writing, building in public all increase market value",
        ],
        "total_comp": "Total comp at Lead/Staff level ranges from $280K to $450K+. At well-funded startups, equity grants of $100K-$200K/year are common. The highest packages belong to engineers at Series C-D companies with clear IPO trajectories.",
    },
}

SALARY_BY_LOCATION = {
    "san-francisco": {"label": "San Francisco", "min": 155000, "max": 250000, "median": 195000, "sample": 132, "note": "SF remains the epicenter of GTM Engineering. Clay's HQ is here, and the density of B2B SaaS companies creates intense demand. Cost of living is punishing, but comp reflects it."},
    "new-york": {"label": "New York City", "min": 145000, "max": 235000, "median": 185000, "sample": 132, "note": "NYC's fintech and enterprise SaaS concentration drives strong GTM Engineering demand. Wall Street-adjacent companies pay premium rates for engineers who can build compliant outbound systems."},
    "austin": {"label": "Austin", "min": 125000, "max": 200000, "median": 160000, "sample": 132, "note": "Austin's tech boom has created a growing GTM Engineering market. Lower cost of living means your dollar goes further, and companies like Oracle, Dell, and a wave of startups are hiring."},
    "seattle": {"label": "Seattle", "min": 150000, "max": 240000, "median": 190000, "sample": 132, "note": "Seattle's enterprise tech base (Microsoft, Amazon) creates steady demand for GTM Engineers who can navigate complex B2B sales cycles. Cloud and cybersecurity verticals pay at the top of range."},
    "boston": {"label": "Boston", "min": 140000, "max": 220000, "median": 175000, "sample": 132, "note": "Boston's biotech and enterprise SaaS sectors create demand for GTM Engineers with specialized domain knowledge. HubSpot's presence has built a strong local talent pipeline."},
    "denver": {"label": "Denver", "min": 130000, "max": 210000, "median": 165000, "sample": 132, "note": "Denver has emerged as a secondary tech hub with lower costs than the coasts. The growing cluster of B2B SaaS companies offers solid GTM Engineering opportunities."},
    "chicago": {"label": "Chicago", "min": 130000, "max": 205000, "median": 162000, "sample": 132, "note": "Chicago's B2B SaaS scene has grown steadily. Companies in the Midwest often struggle to recruit against coastal competitors, which can work in your favor during salary negotiations."},
    "los-angeles": {"label": "Los Angeles", "min": 140000, "max": 225000, "median": 178000, "sample": 132, "note": "LA's tech ecosystem is diverse, spanning entertainment tech, e-commerce, and B2B SaaS. GTM Engineering demand is growing but still trails SF and NYC."},
    "miami": {"label": "Miami", "min": 125000, "max": 200000, "median": 158000, "sample": 132, "note": "Miami's tech scene has expanded rapidly since 2021. No state income tax makes the effective comp competitive with higher-cost markets. Crypto and fintech companies drive the highest salaries."},
    "atlanta": {"label": "Atlanta", "min": 120000, "max": 195000, "median": 155000, "sample": 132, "note": "Atlanta offers strong value for GTM Engineers. Major employers include Salesforce, Mailchimp (Intuit), and a growing wave of B2B startups. Cost of living is significantly below coastal cities."},
    "portland": {"label": "Portland", "min": 125000, "max": 200000, "median": 158000, "sample": 132, "note": "Portland's tech community is small but engaged. No sales tax and moderate cost of living make it attractive. Most GTM Engineering roles here are remote-friendly with Portland-based companies."},
    "washington-dc": {"label": "Washington, D.C.", "min": 140000, "max": 225000, "median": 178000, "sample": 132, "note": "D.C.'s govtech and cybersecurity sectors create unique GTM Engineering opportunities. Federal compliance requirements mean companies pay premium rates for engineers with security clearances or FedRAMP experience."},
    "dallas": {"label": "Dallas", "min": 125000, "max": 200000, "median": 160000, "sample": 132, "note": "Dallas-Fort Worth's corporate presence (AT&T, Texas Instruments, plus a wave of SaaS companies) provides steady GTM Engineering demand. No state income tax boosts effective earnings."},
    "san-diego": {"label": "San Diego", "min": 135000, "max": 215000, "median": 170000, "sample": 132, "note": "San Diego offers a balance between California's tech ecosystem and a more affordable cost of living than SF or LA. Biotech and defense-tech companies drive specialized demand."},
    "remote": {"label": "Remote", "min": 120000, "max": 200000, "median": 155000, "sample": 228, "note": "Remote GTM Engineering roles are the fastest-growing segment. Most companies adjust compensation based on cost-of-living, with SF-benchmarked companies paying the most. The trade-off: more competition for every open role."},
}

SALARY_BY_STAGE = {
    "seed": {"label": "Seed Stage", "slug": "seed", "min": 95000, "max": 150000, "median": 120000, "sample": 228, "equity": "0.1-0.5%", "note": "Seed-stage companies hire GTM Engineers early because founder-led sales doesn't scale. You'll be the first or second hire building the entire outbound machine. Base salary is lower, but equity upside can be massive if the company succeeds. Per the State of GTME Report 2026, 29% of Pre-Seed hires receive meaningful equity. Expect to wear many hats: data ops, sales ops, and sometimes even SDR work."},
    "series-a": {"label": "Series A", "slug": "series-a", "min": 120000, "max": 175000, "median": 145000, "sample": 228, "equity": "0.05-0.25%", "note": "Series A is where GTM Engineering demand accelerates. The company has product-market fit and needs to scale outbound. You'll build the systems that take the company from founder-led sales to a repeatable pipeline machine. Comp is better than seed, but only 9% of Series A hires receive meaningful equity per the State of GTME Report 2026."},
    "series-b": {"label": "Series B", "slug": "series-b", "min": 130000, "max": 175000, "median": 145000, "sample": 228, "equity": "0.02-0.1%", "note": "Series B companies have proven their go-to-market works and are scaling aggressively. The State of GTME Report 2026 shows Series B and D+ stages lead at a $145K median. GTM Engineering teams often grow from 1-2 people to 4-6 at this stage. Base salary is competitive, and the company is de-risked enough that equity has real expected value."},
    "growth": {"label": "Growth Stage", "slug": "growth", "min": 165000, "max": 235000, "median": 195000, "sample": 228, "equity": "0.01-0.05%", "note": "Growth-stage companies (Series C-D, $100M+ ARR) pay top-of-market base salaries. GTM Engineering is a strategic function here, not an experiment. You'll work on sophisticated systems: multi-channel orchestration, intent signal routing, custom integrations. Equity is smaller percentage-wise but the dollar value is significant."},
    "enterprise": {"label": "Enterprise", "slug": "enterprise", "min": 160000, "max": 250000, "median": 200000, "sample": 228, "equity": "RSUs", "note": "Enterprise companies (public or late-stage) offer the highest base salaries and RSU packages. Per the State of GTME Report 2026, 33.3% of Exited/Public company hires receive meaningful equity. GTM Engineering at this level means working within larger organizations, navigating procurement, and building systems that integrate with enterprise infrastructure. The trade-off: less autonomy, more process."},
}

SALARY_VS = {
    "revops": {
        "label": "RevOps",
        "slug": "vs-revops",
        "gtme_range": "$60K-$250K+",
        "other_range": "$95K-$180K",
        "gtme_median": "$135K",
        "other_median": "$130K",
        "verdict": "GTM Engineers earn 25-35% more than RevOps professionals at equivalent seniority levels.",
        "context": [
            "RevOps (Revenue Operations) and GTM Engineering share DNA but diverge on execution. RevOps manages the systems, reporting, and processes that support the revenue team. GTM Engineers build the automated outbound infrastructure that generates pipeline.",
            "The pay gap reflects the technical premium. GTM Engineers write code, build API integrations, and architect data pipelines. RevOps professionals configure tools, build dashboards, and optimize processes. Both are valuable. One commands higher comp because the supply of people who can do it is smaller.",
            "Career mobility between the two is common. Many GTM Engineers started in RevOps and upskilled into automation and code. If you're in RevOps earning $130K and can learn Clay + basic Python, the path to $135K+ is straightforward.",
        ],
        "faq": [
            ("What's the difference between a GTM Engineer and RevOps?", "GTM Engineers build automated outbound systems using code, APIs, and tools like Clay. RevOps manages revenue systems, reporting, and processes. GTM Engineers are builders; RevOps are operators. Both work on go-to-market, but GTM Engineering is more technical."),
            ("Can RevOps professionals transition to GTM Engineering?", "Yes, and many do. The core domain knowledge (CRM, sales processes, data quality) transfers directly. The gap is technical: learning Clay deeply, picking up Python or API skills, and building automated workflows. Most transitions happen within 6-12 months of focused skill-building."),
            ("Which role has better career growth?", "GTM Engineering is growing faster (205% YoY job posting growth) with higher compensation ceilings. RevOps is more established with a clearer career ladder. GTM Engineering offers higher upside but is a newer, less defined career path."),
        ],
    },
    "sales-ops": {
        "label": "Sales Ops",
        "slug": "vs-sales-ops",
        "gtme_range": "$60K-$250K+",
        "other_range": "$85K-$165K",
        "gtme_median": "$135K",
        "other_median": "$118K",
        "verdict": "GTM Engineers earn 35-45% more than Sales Ops at equivalent levels.",
        "context": [
            "Sales Operations focuses on supporting the sales team through territory planning, quota setting, forecasting, and CRM administration. GTM Engineering focuses on building the automated systems that fill the top of the funnel.",
            "The compensation gap is significant because GTM Engineering creates direct pipeline value that's measurable. Sales Ops is a support function; GTM Engineering is a revenue-generation function. Companies pay more for roles that directly create pipeline.",
            "Sales Ops is a mature field with established career paths. GTM Engineering is newer and growing faster. If you're in Sales Ops and want higher comp, building technical skills (automation, data enrichment, API integrations) is the fastest path.",
        ],
        "faq": [
            ("Is GTM Engineering replacing Sales Ops?", "No. GTM Engineering handles automated outbound pipeline generation. Sales Ops handles forecasting, territory planning, and CRM management. They're complementary. Some overlap exists in CRM data management, but the core responsibilities are different."),
            ("What skills do Sales Ops need to transition to GTM Engineering?", "Technical skills: Clay, automation platforms (Make/n8n), basic Python or SQL, API fundamentals. Domain skills you already have: CRM expertise, data quality, sales process understanding. Focus your upskilling on the technical gap."),
            ("Which role is more in demand?", "GTM Engineering job postings grew 205% YoY. Sales Ops growth is flat to single digits. Both will exist for the foreseeable future, but GTM Engineering is where the hiring momentum is."),
        ],
    },
    "growth-engineer": {
        "label": "Growth Engineer",
        "slug": "vs-growth-engineer",
        "gtme_range": "$60K-$250K+",
        "other_range": "$130K-$240K",
        "gtme_median": "$135K",
        "other_median": "$160K",
        "verdict": "Compensation is nearly equivalent. The difference is focus: GTM Engineers build outbound pipeline, Growth Engineers build product-led growth loops.",
        "context": [
            "Growth Engineers and GTM Engineers are the closest salary match in this comparison set. Both are technical, both write code, and both focus on revenue generation. The difference is the motion: GTM Engineers build outbound sales infrastructure, Growth Engineers build product-led acquisition and activation loops.",
            "Growth Engineers typically sit closer to the product team, working on signup flows, activation experiments, referral systems, and self-serve conversion. GTM Engineers sit closer to sales, working on outbound data enrichment, sequencing, and pipeline automation.",
            "The skill overlap is real: both roles use APIs, automation, and data. If you can do one, you can probably learn the other. The choice comes down to whether you prefer sales-side or product-side work.",
        ],
        "faq": [
            ("What's the main difference between GTM and Growth Engineering?", "GTM Engineers build outbound sales infrastructure (data enrichment, sequencing, pipeline automation). Growth Engineers build product-led growth systems (signup optimization, activation loops, referral programs). GTM is sales-assisted; Growth is product-led."),
            ("Which role pays more?", "Compensation is nearly identical. GTM Engineers: $60K-$250K+ median $135K. Growth Engineers: $130K-$240K median $160K. The premium goes to whichever role is more critical to the company's primary growth motion."),
            ("Can you switch between the two roles?", "Yes. The technical skills (APIs, automation, data) transfer well. The domain shift (sales processes vs. product metrics) takes 3-6 months to develop. Companies doing hybrid motions (PLG + outbound) sometimes combine both into one role."),
        ],
    },
    "sdr": {
        "label": "SDR",
        "slug": "vs-sdr",
        "gtme_range": "$60K-$250K+",
        "other_range": "$45K-$85K",
        "gtme_median": "$135K",
        "other_median": "$62K",
        "verdict": "GTM Engineers earn 2-3x what SDRs earn. This is the automation-replaces-manual-labor story in one comparison.",
        "context": [
            "This comparison captures the core thesis of GTM Engineering: one engineer building automated outbound systems can replace the pipeline output of 5-10 SDRs doing manual prospecting.",
            "SDR compensation is base ($45K-$55K) plus variable ($15K-$30K) tied to meetings booked or pipeline generated. GTM Engineer compensation is mostly base salary with smaller variable components. The total comp gap is 2-3x.",
            "The SDR-to-GTM Engineer pipeline is real. SDRs who learn Clay, build automated sequences, and develop technical skills can make the jump within 12-18 months. It's one of the fastest salary multipliers in B2B SaaS.",
        ],
        "faq": [
            ("How can an SDR become a GTM Engineer?", "Start with Clay. Build tables that automate your own prospecting. Learn to use Make or n8n for workflow automation. Pick up basic Python or SQL. Document what you build. Within 6-12 months, you'll have a portfolio that GTM Engineering hiring managers want to see."),
            ("Are GTM Engineers replacing SDRs?", "Partially. One GTM Engineer can automate the prospecting work of multiple SDRs. But SDRs who focus on phone calls, relationship-building, and complex accounts aren't easily automated. The roles that are most at risk are high-volume, templated outbound SDR positions."),
            ("What's the ROI of hiring a GTM Engineer vs. an SDR team?", "A $135K GTM Engineer who builds automated outbound can generate pipeline equivalent to 5-8 SDRs ($310K-$500K in comp). The ROI is compelling, which is why GTM Engineering job postings grew 205% in a year."),
        ],
    },
    "solutions-engineer": {
        "label": "Solutions Engineer",
        "slug": "vs-solutions-engineer",
        "gtme_range": "$60K-$250K+",
        "other_range": "$120K-$220K",
        "gtme_median": "$135K",
        "other_median": "$155K",
        "verdict": "GTM Engineers earn slightly more than Solutions Engineers, with faster growth trajectory.",
        "context": [
            "Solutions Engineers (SEs) and GTM Engineers both sit at the intersection of sales and technology. SEs focus on pre-sales technical demonstrations, proof-of-concept builds, and technical objection handling. GTM Engineers focus on the automated pipeline that fills the top of the funnel.",
            "The compensation is close because both roles require technical depth and business context. SEs tend to have higher variable comp (tied to deal outcomes) while GTM Engineers have higher base salary.",
            "The key difference is scale. SEs work deals one at a time. GTM Engineers build systems that work across the entire pipeline simultaneously. Companies increasingly value the scale that comes from systems over individual deal support.",
        ],
        "faq": [
            ("Which role is more technical?", "It depends on the company. Solutions Engineers need deep product knowledge and can build complex demo environments. GTM Engineers need data engineering skills and build automated pipelines. Both are technical; the domains differ."),
            ("What's the career ceiling for each role?", "Solutions Engineering leads to SE Manager, Director of SE, VP of Solutions. GTM Engineering leads to Head of GTM Engineering, Director of Revenue Engineering, VP of GTM. Both paths reach VP level. GTM Engineering is newer, so the ceiling is less established but expanding."),
            ("Can Solutions Engineers transition to GTM Engineering?", "SEs already have the technical skills and sales context. The gap is in data engineering and automation tools (Clay, enrichment APIs, sequencing platforms). Most SEs can make the transition in 3-6 months of focused learning."),
        ],
    },
    "marketing-ops": {
        "label": "Marketing Ops",
        "slug": "vs-marketing-ops",
        "gtme_range": "$60K-$250K+",
        "other_range": "$90K-$170K",
        "gtme_median": "$135K",
        "other_median": "$125K",
        "verdict": "GTM Engineers earn 30-35% more than Marketing Ops professionals.",
        "context": [
            "Marketing Operations manages the marketing tech stack: email platforms, attribution systems, lead scoring, and campaign operations. GTM Engineering builds automated outbound infrastructure. The overlap is in data quality and tool management.",
            "The pay gap comes from proximity to revenue. Marketing Ops supports marketing campaigns that generate leads. GTM Engineers build systems that generate pipeline directly. The closer you are to revenue, the more you get paid.",
            "Marketing Ops professionals who want to increase comp should look at the GTM Engineering path. The domain knowledge (email systems, data management, lead routing) transfers. Add Clay, enrichment APIs, and outbound sequencing, and you're a GTM Engineer.",
        ],
        "faq": [
            ("How is GTM Engineering different from Marketing Ops?", "Marketing Ops manages marketing systems (Marketo, HubSpot Marketing, attribution tools). GTM Engineering builds automated outbound sales infrastructure (Clay, enrichment waterfalls, sequencing). Marketing Ops supports inbound; GTM Engineering builds outbound."),
            ("Which role has better job security?", "Both are stable. Marketing Ops is established with consistent demand. GTM Engineering is growing 205% YoY. If you want growth and higher comp, GTM Engineering has more momentum. If you prefer stability, Marketing Ops has a longer track record."),
            ("What's the transition path from Marketing Ops to GTM Engineering?", "Focus on: Clay (data enrichment), outbound sequencing tools (Instantly, Smartlead), and basic API skills. Your existing knowledge of data management, email systems, and lead routing gives you a strong foundation. Most transitions happen in 6-9 months."),
        ],
    },
    "sales-engineer": {
        "label": "Sales Engineer",
        "slug": "vs-sales-engineer",
        "gtme_range": "$60K-$250K+",
        "other_range": "$125K-$230K",
        "gtme_median": "$135K",
        "other_median": "$158K",
        "verdict": "Close to parity. Sales Engineers have more variable comp; GTM Engineers have higher base salary.",
        "context": [
            "Sales Engineers and GTM Engineers share the 'Engineer' title and technical depth but apply it differently. Sales Engineers support deals through technical demonstrations, POCs, and architecture discussions. GTM Engineers build the automated systems that generate the deals in the first place.",
            "Compensation structures differ more than totals. Sales Engineers often have 70/30 or 80/20 base/variable splits tied to deal outcomes. GTM Engineers have 85/15 or 90/10 splits with variable tied to pipeline metrics.",
            "Both roles are in high demand and growing. Sales Engineering is more mature with clearer career progression. GTM Engineering is newer with faster growth and potentially higher ceilings as the role becomes more strategic.",
        ],
        "faq": [
            ("What's the key difference between Sales Engineers and GTM Engineers?", "Sales Engineers work deals: demos, POCs, technical objections. GTM Engineers build systems: automated outbound, data enrichment pipelines, sequencing. Sales Engineers are deal-by-deal; GTM Engineers build at scale."),
            ("Which role has more variable compensation?", "Sales Engineers typically have higher variable comp (20-30% of total). GTM Engineers lean more toward base salary (85-90% of total). If you prefer predictable income, GTM Engineering comp structure is more stable."),
            ("Are the skills transferable between roles?", "Highly transferable. Both require technical depth, business context, and communication skills. The main gap is domain-specific: Sales Engineers know product deeply; GTM Engineers know data infrastructure deeply."),
        ],
    },
    "data-engineer": {
        "label": "Data Engineer",
        "slug": "vs-data-engineer",
        "gtme_range": "$60K-$250K+",
        "other_range": "$130K-$245K",
        "gtme_median": "$135K",
        "other_median": "$162K",
        "verdict": "Nearly identical compensation. Data Engineers have a larger job market; GTM Engineers have faster growth.",
        "context": [
            "Data Engineers and GTM Engineers build different types of pipelines. Data Engineers build data infrastructure: ETL/ELT pipelines, data warehouses, streaming systems. GTM Engineers build outbound pipeline infrastructure: enrichment waterfalls, automated sequencing, CRM integrations.",
            "The technical overlap is substantial. Both roles work with APIs, data transformation, and pipeline orchestration. A Data Engineer who moves to GTM Engineering can use most of their skills; they just need to learn the sales domain.",
            "Compensation is nearly identical because the technical bar is similar. The GTM Engineering market is smaller but growing faster. Data Engineering has more open roles overall but GTM Engineering has better supply/demand dynamics (fewer qualified candidates per opening).",
        ],
        "faq": [
            ("Which role is more technical?", "Data Engineering is more technically deep on average. Data Engineers work with Spark, Airflow, dbt, and cloud data infrastructure. GTM Engineers work with Clay, APIs, Python scripts, and CRM integrations. Both are technical; Data Engineering requires more infrastructure knowledge."),
            ("Should a Data Engineer consider GTM Engineering?", "If you like building things that directly drive revenue and want faster career growth in a less crowded field, yes. Your data pipeline skills transfer directly. You'll need to learn sales domain concepts and specific GTM tools, but the technical foundation is solid."),
            ("What's the job market size comparison?", "Data Engineering has roughly 15x more open positions than GTM Engineering. But GTM Engineering is growing 205% YoY while Data Engineering growth has slowed. GTM Engineering also has fewer qualified candidates per role, which drives higher compensation for available talent."),
        ],
    },
    "product-manager": {
        "label": "Product Manager",
        "slug": "vs-product-manager",
        "gtme_range": "$60K-$250K+",
        "other_range": "$120K-$230K",
        "gtme_median": "$135K",
        "other_median": "$152K",
        "verdict": "GTM Engineers earn 8-12% more than Product Managers at equivalent experience levels.",
        "context": [
            "Comparing GTM Engineers to Product Managers is a stretch in terms of day-to-day work, but the comparison matters for career decisions. Both are cross-functional roles that require business and technical context. Both influence revenue, just from different angles.",
            "GTM Engineers build outbound systems that generate pipeline. Product Managers define and prioritize the product features that retain and expand customers. The skills are different, but the organizational seniority and influence are comparable.",
            "The slight compensation edge for GTM Engineers reflects the supply/demand imbalance. There are far more qualified Product Managers than qualified GTM Engineers. As the GTM Engineering talent pool grows, the gap may narrow.",
        ],
        "faq": [
            ("Why compare GTM Engineers to Product Managers?", "Both are cross-functional roles that blend business and technical skills. Professionals choosing between these career paths need comp data. GTM Engineering is more technical and execution-focused; Product Management is more strategic and prioritization-focused."),
            ("Which role is harder to break into?", "Product Management has a more defined hiring process but more competition. GTM Engineering has fewer candidates but less established hiring criteria. PM roles get 200+ applicants; GTM Engineering roles get 30-50. Different challenge, similar difficulty."),
            ("Can Product Managers transition to GTM Engineering?", "The strategic thinking transfers, but the execution skills don't. PMs would need to learn Clay, outbound tools, data enrichment, and ideally Python. It's a 6-12 month upskilling journey. The reverse transition (GTME to PM) is also possible with similar effort."),
        ],
    },
    "account-executive": {
        "label": "Account Executive",
        "slug": "vs-account-executive",
        "gtme_range": "$60K-$250K+",
        "other_range": "$100K-$300K",
        "gtme_median": "$135K",
        "other_median": "$145K",
        "verdict": "AE comp has a wider range (big OTE upside) but GTM Engineers have more predictable, higher base salary.",
        "context": [
            "Account Executives and GTM Engineers work different parts of the revenue funnel. AEs close deals; GTM Engineers build the systems that generate the deals AEs close. The relationship is symbiotic.",
            "AE compensation is heavily variable: 50/50 or 60/40 base/OTE splits are standard. A top AE can earn $300K+ in a great year; a struggling AE might earn $100K. GTM Engineers have more predictable comp with 85-90% base salary.",
            "The career paths rarely cross, but understanding the comp dynamics matters. GTM Engineers who build systems that measurably increase AE pipeline have strong negotiating power. Your work directly impacts the highest-paid people in the sales org.",
        ],
        "faq": [
            ("Do GTM Engineers or AEs earn more?", "It depends on performance. Top AEs crushing quota can earn $300K+. The average AE earns $145K. GTM Engineers earn $60K-$250K+ with a $135K median. GTM Engineering comp is more predictable; AE comp has higher upside but more variance."),
            ("How do GTM Engineers support Account Executives?", "GTM Engineers build the automated outbound systems that generate qualified pipeline for AEs. This includes enriched prospect data, automated sequencing, intent signal routing, and CRM integration. Better GTM Engineering = more qualified meetings for AEs."),
            ("Could an AE become a GTM Engineer?", "AEs understand the sales process deeply, which is valuable. The gap is technical: learning Clay, automation tools, data enrichment, and ideally Python/SQL. It's a significant pivot but AEs who enjoy building systems more than running deals can make it work."),
        ],
    },
}


# ---------------------------------------------------------------------------
# Salary page helpers
# ---------------------------------------------------------------------------

def pad_description(desc, target_min=150, target_max=158):
    """Ensure description is within 150-158 chars by appending filler."""
    suffixes = [" Updated weekly.", " Independent.", " Free."]
    used = set()
    for suffix in suffixes:
        if target_min <= len(desc) <= target_max:
            return desc
        if suffix in used:
            continue
        new = desc + suffix
        if len(new) <= target_max:
            desc = new
            used.add(suffix)
    if len(desc) > target_max:
        desc = desc[:target_max - 1].rstrip() + "."
    return desc


def salary_stats_html(data):
    """Generate 3-card stats grid for salary pages."""
    sample_label = "Survey Respondents" if data["sample"] == 228 else "US Respondents"
    return f'''<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">{fmt_salary(data["min"])}&#8209;{fmt_salary(data["max"])}</span>
        <span class="stat-label">Salary Range</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">{fmt_salary(data["median"])}</span>
        <span class="stat-label">Median Salary</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">{data["sample"]:,}</span>
        <span class="stat-label">{sample_label}</span>
    </div>
</div>'''


def salary_range_bar_html(data):
    """Visual range bar showing min-max."""
    scale_min, scale_max = 50000, 350000
    left_pct = max(0, (data["min"] - scale_min) / (scale_max - scale_min) * 100)
    width_pct = max(5, (data["max"] - data["min"]) / (scale_max - scale_min) * 100)
    return f'''<div class="salary-range-bar">
    <div class="range-bar-labels">
        <span>{fmt_salary(data["min"])}</span>
        <span>Median: {fmt_salary(data["median"])}</span>
        <span>{fmt_salary(data["max"])}</span>
    </div>
    <div class="range-bar-track">
        <div class="range-bar-fill" style="left:{left_pct:.0f}%;width:{width_pct:.0f}%"></div>
    </div>
</div>'''


def salary_related_links(current_slug, current_type):
    """Generate related salary page links."""
    links = []
    if current_slug != "index":
        links.append(("/salary/", "Salary Index"))
    links.append(("/salary/methodology/", "Data Methodology"))

    if current_type != "seniority":
        for key, data in list(SALARY_BY_SENIORITY.items())[:3]:
            links.append((f"/salary/{data['slug']}/", f"{data['label']} Salary"))
    if current_type != "location":
        for key in ["san-francisco", "new-york", "remote"]:
            data = SALARY_BY_LOCATION[key]
            links.append((f"/salary/{key}/", f"{data['label']} Salary"))
    if current_type != "vs":
        links.append(("/salary/vs-revops/", "GTM Engineer vs RevOps"))
        links.append(("/salary/vs-sdr/", "GTM Engineer vs SDR"))
    if current_type != "analysis":
        links.append(("/salary/coding-premium/", "Coding Premium: $45K Gap"))
        links.append(("/salary/bonus/", "Bonus Structure Data"))
        links.append(("/salary/by-experience/", "Salary by Experience"))

    links = links[:8]
    items = ""
    for href, label in links:
        items += f'<a href="{href}" class="related-link-card">{label}</a>\n'

    return f'''<section class="related-links">
    <h2>Related Salary Data</h2>
    <div class="related-links-grid">
        {items}
    </div>
</section>'''


# ---------------------------------------------------------------------------
# Page generators: Homepage + About
# ---------------------------------------------------------------------------

def build_homepage():
    """Generate the homepage with Organization+WebSite schema."""
    title = "GTM Engineer Salary and Career Intelligence"
    description = (
        "Salary benchmarks, tool reviews, and career data for GTM Engineers."
        " Sourced from the State of GTME Report 2026 (n=228). Updated weekly. Vendor-neutral."
    )

    body = '''<section class="hero">
    <div class="hero-inner">
        <h1>GTM Engineering, Finally Mapped Out</h1>
        <p class="hero-subtitle">Salary data, tool reviews, career paths, and job listings. Everything the fastest-growing role in B2B SaaS has been missing.</p>
        <div class="stat-grid">
            <div class="stat-block">
                <span class="stat-value">3,000+</span>
                <span class="stat-label">Roles Tracked</span>
            </div>
            <div class="stat-block">
                <span class="stat-value">$60K&#8209;$250K+</span>
                <span class="stat-label">Salary Range</span>
            </div>
            <div class="stat-block">
                <span class="stat-value">205%</span>
                <span class="stat-label">YoY Growth</span>
            </div>
        </div>
        <form class="hero-signup" onsubmit="return false;">
            <input type="email" placeholder="Your email" aria-label="Email address" required>
            <button type="submit" class="btn btn--primary">Get the Weekly Pulse</button>
        </form>
        <p class="hero-signup-note">Free weekly newsletter. Salary shifts, tool intel, job data.</p>
    </div>
</section>

<section class="logo-bar">
    <p class="logo-bar-label">Tracking hiring data from companies like</p>
    <div class="logo-bar-row">
        <span class="logo-name">Clay</span>
        <span class="logo-name">HubSpot</span>
        <span class="logo-name">Salesforce</span>
        <span class="logo-name">Gong</span>
        <span class="logo-name">Outreach</span>
        <span class="logo-name">Apollo</span>
        <span class="logo-name">6sense</span>
        <span class="logo-name">Ramp</span>
        <span class="logo-name">Rippling</span>
        <span class="logo-name">Brex</span>
    </div>
</section>

<section class="section-previews">
    <h2 class="section-previews-heading">Explore GTM Engineer Intelligence</h2>
    <div class="preview-grid">
        <a href="/salary/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128176;</span></div>
            <h3>Salary Data</h3>
            <p>Breakdowns by seniority, location, and company stage. Side-by-side comparisons with RevOps, Sales Ops, and 8 other roles.</p>
            <span class="preview-link">Browse salary data &rarr;</span>
        </a>
        <a href="/tools/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128295;</span></div>
            <h3>Tool Reviews</h3>
            <p>Practitioner-tested reviews of Clay, Apollo, Instantly, and 27 more tools across 8 categories. Honest scores, no pay-to-play.</p>
            <span class="preview-link">Browse tools &rarr;</span>
        </a>
        <a href="/salary/calculator/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128178;</span></div>
            <h3>Salary Calculator</h3>
            <p>Get your personalized GTM Engineer market rate based on seniority, location, and company stage.</p>
            <span class="preview-link">Calculate your rate &rarr;</span>
        </a>
        <a href="/careers/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128200;</span></div>
            <h3>Career Guides</h3>
            <p>How to break in, level up, and negotiate. Interview prep, skill maps, and role comparisons for every stage.</p>
            <span class="preview-link">Browse guides &rarr;</span>
        </a>
        <a href="/jobs/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128188;</span></div>
            <h3>Job Board</h3>
            <p>Curated GTM Engineer roles from top B2B SaaS companies. Updated twice a week from 3,000+ tracked postings.</p>
            <span class="preview-link">View all jobs &rarr;</span>
        </a>
        <a href="/glossary/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128218;</span></div>
            <h3>GTM Glossary</h3>
            <p>Clear definitions for 50 GTM Engineering terms. Clay tables, waterfall enrichment, signal-based outbound, and more.</p>
            <span class="preview-link">Browse glossary &rarr;</span>
        </a>
        <a href="/newsletter/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128232;</span></div>
            <h3>Weekly Newsletter</h3>
            <p>Salary shifts, tool intel, and hiring trends delivered every Monday. Data from 3,000+ tracked job postings.</p>
            <span class="preview-link">Get the weekly pulse &rarr;</span>
        </a>
        <a href="/insights/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128202;</span></div>
            <h3>Insights &amp; Analysis</h3>
            <p>Data-driven articles on GTM hiring trends, tool adoption, career paths, and market shifts.</p>
            <span class="preview-link">Read insights &rarr;</span>
        </a>
        <a href="/salary/methodology/" class="preview-card">
            <div class="preview-icon"><span class="preview-emoji">&#128300;</span></div>
            <h3>Methodology</h3>
            <p>How we collect, normalize, and cross-reference 3,000+ B2B SaaS job postings for salary data.</p>
            <span class="preview-link">See our process &rarr;</span>
        </a>
    </div>
</section>

<section class="home-comparisons">
    <div class="home-comparisons-inner">
        <h2>How Does GTM Engineer Pay Compare?</h2>
        <p class="section-subtitle">Side-by-side salary data against 10 adjacent roles.</p>
        <div class="comparison-grid">
            <a href="/salary/vs-revops/" class="comparison-link"><span class="vs-badge">VS</span> RevOps</a>
            <a href="/salary/vs-sales-ops/" class="comparison-link"><span class="vs-badge">VS</span> Sales Ops</a>
            <a href="/salary/vs-growth-engineer/" class="comparison-link"><span class="vs-badge">VS</span> Growth Engineer</a>
            <a href="/salary/vs-sdr/" class="comparison-link"><span class="vs-badge">VS</span> SDR</a>
            <a href="/salary/vs-solutions-engineer/" class="comparison-link"><span class="vs-badge">VS</span> Solutions Engineer</a>
            <a href="/salary/vs-marketing-ops/" class="comparison-link"><span class="vs-badge">VS</span> Marketing Ops</a>
            <a href="/salary/vs-sales-engineer/" class="comparison-link"><span class="vs-badge">VS</span> Sales Engineer</a>
            <a href="/salary/vs-data-engineer/" class="comparison-link"><span class="vs-badge">VS</span> Data Engineer</a>
            <a href="/salary/vs-product-manager/" class="comparison-link"><span class="vs-badge">VS</span> Product Manager</a>
            <a href="/salary/vs-account-executive/" class="comparison-link"><span class="vs-badge">VS</span> Account Executive</a>
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
# Core pages (newsletter, privacy, terms, 404)
# ---------------------------------------------------------------------------

def build_newsletter_page():
    title = "The Weekly Pulse: GTM Engineer Newsletter"
    description = (
        "Get weekly GTM Engineer salary data, tool intel, and job market analysis."
        " Free newsletter built from 3,000+ tracked B2B SaaS job postings. Every Monday."
    )
    crumbs = [("Home", "/"), ("Newsletter", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<div class="newsletter-page">
    <section class="page-header">
        <h1>The Weekly Pulse: GTM Engineer Newsletter</h1>
    </section>
    <p class="lead">Every Monday: salary shifts, tool intel, hiring trends, and job market data for GTM Engineers. Built from 3,000+ tracked B2B SaaS job postings.</p>
    <form class="hero-signup" onsubmit="return false;">
        <input type="email" placeholder="Your email" aria-label="Email address" required>
        <button type="submit" class="btn btn--primary">Get the Weekly Pulse</button>
    </form>
    <ul class="newsletter-features">
        <li><strong>Salary movements:</strong> week-over-week changes in GTM Engineer compensation across seniority levels and locations</li>
        <li><strong>Tool trends:</strong> which tools are showing up in job postings, which are fading, and what's emerging</li>
        <li><strong>Hiring signals:</strong> which companies are scaling GTM Engineering teams and what that tells us about the market</li>
        <li><strong>Career intel:</strong> job market data, interview insights, and skill demand shifts</li>
    </ul>
    <p style="color: var(--gtme-text-secondary);">Free. No spam. Unsubscribe anytime.</p>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/newsletter/",
        body_content=body, active_path="/newsletter/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("newsletter/index.html", page)
    print(f"  Built: newsletter/index.html")


def build_privacy_page():
    title = "Privacy Policy for GTME Pulse Website"
    description = (
        "GTME Pulse privacy policy: how we collect, use, and protect your data."
        " We collect minimal information, never sell it, and respect your inbox. Updated 2026."
    )
    crumbs = [("Home", "/"), ("Privacy Policy", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Privacy Policy for GTME Pulse Website</h1>
</section>
<div class="legal-content">
    <p>Last updated: March 13, 2026</p>
    <h2>What We Collect</h2>
    <p>When you subscribe to our newsletter, we collect your email address. That's it. We don't track you across the web, sell your data, or build advertising profiles.</p>
    <h2>How We Use Your Email</h2>
    <p>Your email address is used to send you The Weekly Pulse newsletter. We may also send occasional product updates or announcements. Every email includes an unsubscribe link that works immediately.</p>
    <h2>Email Service Provider</h2>
    <p>We use <a href="https://resend.com">Resend</a> to manage our email list and send newsletters. Your email address is stored in Resend's infrastructure. Resend's privacy policy governs their handling of your data.</p>
    <h2>Analytics</h2>
    <p>We use privacy-respecting analytics to understand which pages are visited and how people find the site. We don't use cookies for tracking, and we don't collect personally identifiable information through analytics.</p>
    <h2>Cookies</h2>
    <p>GTME Pulse does not set tracking cookies. Our site functions without cookies. Third-party services (Google Fonts) may set their own cookies per their respective policies.</p>
    <h2>Data Retention</h2>
    <p>Email addresses are retained as long as you're subscribed. When you unsubscribe, your email is removed from our active list within 30 days. Backup copies may persist for up to 90 days.</p>
    <h2>Your Rights</h2>
    <p>You can unsubscribe from our newsletter at any time using the link in any email. To request deletion of your data, email us and we'll process it within 30 days.</p>
    <h2>Changes to This Policy</h2>
    <p>We'll update this page when our practices change. Material changes will be noted at the top of this page with the updated date.</p>
    <h2>Contact</h2>
    <p>Questions about this policy? Reach out to Rome Thorndike at the email address listed on the <a href="/about/">About</a> page.</p>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/privacy/",
        body_content=body, active_path="/privacy/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("privacy/index.html", page)
    print(f"  Built: privacy/index.html")


def build_terms_page():
    title = "Terms of Service for GTME Pulse Website"
    description = (
        "GTME Pulse terms of service. Free salary data, tool reviews, and career"
        " guides for GTM Engineers. Use the site, respect the content. Updated March 2026."
    )
    crumbs = [("Home", "/"), ("Terms of Service", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="page-header">
    <h1>Terms of Service for GTME Pulse Website</h1>
</section>
<div class="legal-content">
    <p>Last updated: March 13, 2026</p>
    <h2>Using This Site</h2>
    <p>GTME Pulse provides salary data, tool reviews, and career resources for GTM Engineers. The content is free to read and share with attribution. You agree to use the site lawfully and not to scrape, republish, or redistribute our content at scale without permission.</p>
    <h2>Content Accuracy</h2>
    <p>Our salary data comes from analysis of public job postings. While we work to be accurate, this data is for informational purposes only. It should not be your sole source for salary negotiations, hiring decisions, or compensation planning. Individual compensation depends on factors we can't capture in aggregate data.</p>
    <h2>Newsletter</h2>
    <p>Subscribing to The Weekly Pulse is free. We send one email per week plus occasional announcements. You can unsubscribe at any time. We will never sell your email address or share it with third parties for marketing purposes.</p>
    <h2>Affiliate Links</h2>
    <p>Some tool reviews contain affiliate links. When you purchase through these links, we may earn a commission at no additional cost to you. Affiliate relationships never influence our ratings or recommendations. We disclose affiliate relationships on relevant pages.</p>
    <h2>Intellectual Property</h2>
    <p>All original content on GTME Pulse (text, data analysis, graphics, code) is owned by GTME Pulse. You may quote short excerpts with attribution and a link back to the source page. Reproducing full articles or datasets requires written permission.</p>
    <h2>Limitation of Liability</h2>
    <p>GTME Pulse provides information as-is. We're not liable for decisions you make based on our salary data, tool reviews, or career advice. Use your judgment and consult relevant professionals for significant career or financial decisions.</p>
    <h2>Changes</h2>
    <p>We may update these terms. Continued use of the site after changes constitutes acceptance. Material changes will be noted with an updated date at the top of this page.</p>
    <h2>Contact</h2>
    <p>Questions about these terms? Reach out via the <a href="/about/">About</a> page.</p>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/terms/",
        body_content=body, active_path="/terms/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("terms/index.html", page)
    print(f"  Built: terms/index.html")


def build_404_page():
    title = "Page Not Found (404) on GTME Pulse Site"
    description = (
        "The page you're looking for doesn't exist on GTME Pulse. Browse GTM Engineer"
        " salary data, tool reviews, and career guides, or head back to the homepage."
    )
    body = '''<div class="error-page">
    <div class="error-code">404</div>
    <h1>Page Not Found (404) on GTME Pulse Site</h1>
    <p>The page you're looking for doesn't exist or has been moved. Try one of these instead:</p>
    <div style="display:flex;flex-direction:column;gap:0.75rem;align-items:center;">
        <a href="/" class="btn btn--primary">Back to Homepage</a>
        <a href="/salary/" class="btn btn--ghost">Browse Salary Data</a>
        <a href="/newsletter/" class="btn btn--ghost">Get the Newsletter</a>
    </div>
</div>
'''
    page = get_page_wrapper(
        title=title, description=description, canonical_path="/404.html",
        body_content=body, body_class="page-inner",
    )
    write_page("404.html", page)
    print(f"  Built: 404.html")


# ---------------------------------------------------------------------------
# Salary page generators
# ---------------------------------------------------------------------------

def build_salary_index():
    title = "GTM Engineer Salary Data: Full Breakdown Guide"
    description = (
        "GTM Engineer salary data: breakdowns by seniority, location, and company"
        " stage. 10 role comparisons. From the State of GTME Report 2026 (n=228 respondents)."
    )
    crumbs = [("Home", "/"), ("Salary Data", None)]
    bc_html = breadcrumb_html(crumbs)

    seniority_cards = ""
    for key, data in SALARY_BY_SENIORITY.items():
        seniority_cards += f'''<a href="/salary/{data["slug"]}/" class="salary-index-card">
    <h3>{data["label"]}</h3>
    <div class="card-range">{fmt_salary(data["min"])}&#8209;{fmt_salary(data["max"])}</div>
    <p>Median: {fmt_salary(data["median"])} | {data["sample"]} respondents</p>
</a>\n'''

    location_cards = ""
    for key in ["san-francisco", "new-york", "seattle", "austin", "remote"]:
        data = SALARY_BY_LOCATION[key]
        location_cards += f'''<a href="/salary/{key}/" class="salary-index-card">
    <h3>{data["label"]}</h3>
    <div class="card-range">{fmt_salary(data["min"])}&#8209;{fmt_salary(data["max"])}</div>
    <p>Median: {fmt_salary(data["median"])} | {data["sample"]} US respondents</p>
</a>\n'''

    stage_cards = ""
    for key, data in SALARY_BY_STAGE.items():
        stage_cards += f'''<a href="/salary/{data["slug"]}/" class="salary-index-card">
    <h3>{data["label"]}</h3>
    <div class="card-range">{fmt_salary(data["min"])}&#8209;{fmt_salary(data["max"])}</div>
    <p>Median: {fmt_salary(data["median"])} | Equity: {data["equity"]}</p>
</a>\n'''

    vs_links = ""
    for key, data in SALARY_VS.items():
        vs_links += f'<a href="/salary/{data["slug"]}/" class="comparison-link"><span class="vs-badge">VS</span> {data["label"]}</a>\n'

    total_sample = sum(d["sample"] for d in SALARY_BY_SENIORITY.values())

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary Data</div>
        <h1>GTM Engineer Salary Data: Full Breakdown Guide</h1>
        <p>Compensation data from the State of GTM Engineering Report 2026 (228 survey respondents across 32 countries + 3,342 job postings analyzed). Breakdowns by seniority, location, company stage, and head-to-head role comparisons.</p>
    </div>
</section>

{salary_stats_html({"min": 60000, "max": 250000, "median": 135000, "sample": 228})}

<div class="salary-content">
    <h2>By Seniority</h2>
    <div class="salary-index-grid">{seniority_cards}</div>

    <h2>By Location</h2>
    <div class="salary-index-grid">{location_cards}</div>
    <p style="margin-top:var(--gtme-space-4)"><a href="/salary/san-francisco/">See all 15 locations &rarr;</a></p>

    <h2>By Company Stage</h2>
    <div class="salary-index-grid">{stage_cards}</div>

    <h2>Role Comparisons</h2>
    <p>How GTM Engineer compensation stacks up against 10 adjacent roles.</p>
    <div class="comparison-grid" style="margin-top:var(--gtme-space-4)">{vs_links}</div>

    <h2>Salary Calculator</h2>
    <p>Get a personalized salary estimate based on your seniority, location, and company stage.</p>
    <a href="/salary/calculator/" class="btn btn--primary" style="margin-top:var(--gtme-space-3)">Calculate My Market Rate</a>

    <h2>How We Collect This Data</h2>
    <p>Salary figures are sourced from the State of GTM Engineering Report 2026, which surveyed 228 GTM Engineers across 32 countries and analyzed 3,342 job postings. We cross-reference survey data with public job listings for validation. <a href="/salary/methodology/">Read our full methodology</a>.</p>
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly salary data updates.")

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("salary/index.html", page)
    print(f"  Built: salary/index.html")


def build_salary_seniority_pages():
    for key, data in SALARY_BY_SENIORITY.items():
        slug = data["slug"]
        label = data["label"]

        title = f"{label} GTM Engineer Salary Data (2026)"
        full_title = f"{title} - GTME Pulse"
        if len(full_title) > 60:
            title = f"{label} GTM Engineer Salary (2026)"

        description = (
            f"{label} GTM Engineer salary data: {fmt_salary(data['min'])} to {fmt_salary(data['max'])} range"
            f" with a {fmt_salary(data['median'])} median. Data from the State of GTME Report 2026 (n=228)."
        )
        description = pad_description(description)

        crumbs = [("Home", "/"), ("Salary Data", "/salary/"), (label, None)]
        bc_html = breadcrumb_html(crumbs)

        context_html = "".join(f"    <p>{p}</p>\n" for p in data["context"])
        drivers_html = "".join(f"        <li>{d}</li>\n" for d in data["drivers"])

        faq_pairs = [
            (f"What is the average {label.lower()} GTM Engineer salary?",
             f"The median {label.lower()} GTM Engineer salary is {fmt_salary(data['median'])}, based on the State of GTME Report 2026 (n=228). The full range spans {fmt_salary(data['min'])} to {fmt_salary(data['max'])}."),
            (f"What skills increase {label.lower()} GTM Engineer pay?",
             f"Python, SQL, and Clay expertise command the highest premiums at the {label.lower()} level. Engineers who can write code and build API integrations earn 10-20% more than those using only no-code tools."),
            (f"How fast can a {label.lower()} GTM Engineer get promoted?",
             f"Typical advancement from {label.lower()} to the next seniority level takes 18-24 months. Engineers who build measurable pipeline impact and develop technical depth advance fastest."),
        ]

        body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary by Seniority</div>
        <h1>{label} GTM Engineer Salary Data (2026)</h1>
        <p>Compensation data for {label.lower()} GTM Engineers from the State of GTM Engineering Report 2026 ({data["sample"]} survey respondents).</p>
    </div>
</section>
{salary_stats_html(data)}
{salary_range_bar_html(data)}
<div class="salary-content">
    <h2>Market Context</h2>
{context_html}
    <h2>What Drives Compensation</h2>
    <ul>
{drivers_html}    </ul>
    <h2>Beyond Base: Total Compensation</h2>
    <p>{data["total_comp"]}</p>
{faq_html(faq_pairs)}
{salary_related_links(slug, "seniority")}
</div>
'''
        body += source_citation_html()
        body += newsletter_cta_html(f"Get weekly {label.lower()} salary updates.")
        extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

        page = get_page_wrapper(
            title=title, description=description, canonical_path=f"/salary/{slug}/",
            body_content=body, active_path="/salary/",
            extra_head=extra_head, body_class="page-inner",
        )
        write_page(f"salary/{slug}/index.html", page)
        print(f"  Built: salary/{slug}/index.html")


def build_salary_location_pages():
    for key, data in SALARY_BY_LOCATION.items():
        label = data["label"]

        title = f"GTM Engineer Salary in {label} (2026)"
        full_title = f"{title} - GTME Pulse"
        if len(full_title) > 60:
            title = f"GTM Engineer Pay in {label} (2026)"
            full_title = f"{title} - GTME Pulse"
        if len(full_title) > 60:
            title = f"GTM Engineer Pay in {label}"
        # Ensure minimum 50 chars for full title
        full_title = f"{title} - GTME Pulse"
        if len(full_title) < 50:
            title = f"GTM Engineer Salary Data: {label} (2026)"

        description = (
            f"GTM Engineer salary data for {label}: {fmt_salary(data['min'])} to {fmt_salary(data['max'])} range"
            f" with a {fmt_salary(data['median'])} median. Data from the State of GTME Report 2026 (n=228)."
        )
        description = pad_description(description)

        crumbs = [("Home", "/"), ("Salary Data", "/salary/"), (label, None)]
        bc_html = breadcrumb_html(crumbs)

        faq_pairs = [
            (f"What is the average GTM Engineer salary in {label}?",
             f"The median GTM Engineer salary in {label} is {fmt_salary(data['median'])}. The range spans {fmt_salary(data['min'])} to {fmt_salary(data['max'])} based on the State of GTME Report 2026."),
            (f"Is {label} a good market for GTM Engineers?",
             f"{data['note']}"),
            (f"How does {label} GTM Engineer pay compare to other cities?",
             f"The {label} median of {fmt_salary(data['median'])} compares to the SF median of $195K and the national remote median of $155K. Cost of living differences should factor into your comparison."),
        ]

        body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary by Location</div>
        <h1>GTM Engineer Salary in {label} (2026)</h1>
        <p>Compensation data for GTM Engineers in {label}, from the State of GTM Engineering Report 2026 ({data["sample"]} US respondents).</p>
    </div>
</section>
{salary_stats_html(data)}
{salary_range_bar_html(data)}
<div class="salary-content">
    <h2>Market Context</h2>
    <p>{data["note"]}</p>
    <p>These figures represent base salary ranges from public job postings. Total compensation including equity, bonuses, and benefits varies by company stage and role seniority. For a personalized estimate, try the <a href="/salary/calculator/">salary calculator</a>.</p>

    <h2>What Drives Pay in {label}</h2>
    <ul>
        <li><strong>Company stage:</strong> Growth and enterprise companies in {label} pay at the top of the range</li>
        <li><strong>Technical depth:</strong> Python, API integration, and custom tooling skills command 10-20% premiums</li>
        <li><strong>Industry vertical:</strong> Fintech and cybersecurity companies consistently pay above median</li>
        <li><strong>Remote flexibility:</strong> {label} companies offering remote options may adjust comp based on employee location</li>
    </ul>

    <h2>Beyond Base: Total Comp in {label}</h2>
    <p>Base salary tells part of the story. GTM Engineers in {label} can expect 10-30% additional compensation from equity, bonuses, and benefits. Growth-stage companies offer the strongest total packages, with equity grants that can meaningfully increase total comp over a 4-year vesting period.</p>

{faq_html(faq_pairs)}
{salary_related_links(key, "location")}
</div>
'''
        body += source_citation_html()
        body += newsletter_cta_html(f"Get weekly {label} salary updates.")
        extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

        page = get_page_wrapper(
            title=title, description=description, canonical_path=f"/salary/{key}/",
            body_content=body, active_path="/salary/",
            extra_head=extra_head, body_class="page-inner",
        )
        write_page(f"salary/{key}/index.html", page)
        print(f"  Built: salary/{key}/index.html")


def build_salary_stage_pages():
    for key, data in SALARY_BY_STAGE.items():
        slug = data["slug"]
        label = data["label"]

        title = f"GTM Engineer Salary at {label} Companies"
        full_title = f"{title} - GTME Pulse"
        if len(full_title) > 60:
            title = f"GTM Engineer Pay: {label} Startups"
            full_title = f"{title} - GTME Pulse"
        if len(full_title) > 60:
            title = f"{label} GTM Engineer Salary"

        description = (
            f"GTM Engineer salary data at {label.lower()} companies: {fmt_salary(data['min'])} to {fmt_salary(data['max'])}"
            f" with {fmt_salary(data['median'])} median. Equity: {data['equity']}. State of GTME Report 2026 (n=228)."
        )
        description = pad_description(description)

        crumbs = [("Home", "/"), ("Salary Data", "/salary/"), (label, None)]
        bc_html = breadcrumb_html(crumbs)

        faq_pairs = [
            (f"What do GTM Engineers earn at {label.lower()} companies?",
             f"GTM Engineers at {label.lower()} companies earn {fmt_salary(data['min'])} to {fmt_salary(data['max'])} base salary with a {fmt_salary(data['median'])} median. Equity grants of {data['equity']} are typical at this stage."),
            (f"Is the equity at {label.lower()} companies worth it?",
             f"Equity at {label.lower()} companies carries {'higher risk but higher potential upside' if key in ['seed', 'series-a'] else 'moderate risk with meaningful expected value' if key == 'series-b' else 'lower risk with predictable value'}. The {data['equity']} range is standard for GTM Engineering hires at this stage."),
            (f"Should I join a {label.lower()} company as a GTM Engineer?",
             f"{label} companies offer {'more ownership and learning but less structure' if key in ['seed', 'series-a'] else 'a balance of structure and growth opportunity' if key == 'series-b' else 'more structure, higher base pay, and less equity upside'}. Your preference for autonomy vs. stability should guide the decision."),
        ]

        body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary by Company Stage</div>
        <h1>GTM Engineer Salary at {label} Companies</h1>
        <p>Compensation data for GTM Engineers at {label.lower()} B2B SaaS companies, from the State of GTM Engineering Report 2026 (228 respondents).</p>
    </div>
</section>
{salary_stats_html(data)}
{salary_range_bar_html(data)}
<div class="salary-content">
    <h2>Market Context</h2>
    <p>{data["note"]}</p>

    <h2>Equity at {label} Companies</h2>
    <p>Typical equity range for GTM Engineers at {label.lower()} companies: <strong>{data["equity"]}</strong>. This is in addition to base salary and any cash bonuses.</p>
    <p>When evaluating equity, consider the company's last valuation, the strike price, vesting schedule (typically 4 years with 1-year cliff), and your estimate of future outcomes. Equity at earlier stages carries more risk but offers larger percentage grants.</p>

    <h2>What Drives Compensation at {label} Companies</h2>
    <ul>
        <li><strong>Revenue impact:</strong> At {label.lower()} companies, your work directly moves the pipeline needle. Demonstrable impact accelerates both comp and promotion.</li>
        <li><strong>Technical scope:</strong> Engineers who build systems from scratch (vs. maintaining existing ones) earn more at this stage.</li>
        <li><strong>Funding round:</strong> Companies that just closed a round have budget to pay at the top of range.</li>
        <li><strong>Location:</strong> SF and NYC {label.lower()} companies pay 15-25% above remote equivalents.</li>
    </ul>

{faq_html(faq_pairs)}
{salary_related_links(slug, "stage")}
</div>
'''
        body += source_citation_html()
        body += newsletter_cta_html(f"Get weekly salary data for {label.lower()} companies.")
        extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

        page = get_page_wrapper(
            title=title, description=description, canonical_path=f"/salary/{slug}/",
            body_content=body, active_path="/salary/",
            extra_head=extra_head, body_class="page-inner",
        )
        write_page(f"salary/{slug}/index.html", page)
        print(f"  Built: salary/{slug}/index.html")


def build_salary_vs_pages():
    for key, data in SALARY_VS.items():
        slug = data["slug"]
        label = data["label"]

        title = f"GTM Engineer vs {label} Salary Comparison"
        full_title = f"{title} - GTME Pulse"
        if len(full_title) > 60:
            title = f"GTM Engineer vs {label} Salary (2026)"
            full_title = f"{title} - GTME Pulse"
        if len(full_title) > 60:
            title = f"GTM Engineer vs {label}: Pay Gap"

        description = (
            f"GTM Engineer vs {label} salary comparison for 2026. GTME range: {data['gtme_range']}"
            f" (median {data['gtme_median']}). {label} range: {data['other_range']} (median {data['other_median']})."
        )
        description = pad_description(description)

        crumbs = [("Home", "/"), ("Salary Data", "/salary/"), (f"vs {label}", None)]
        bc_html = breadcrumb_html(crumbs)

        context_html = "".join(f"    <p>{p}</p>\n" for p in data["context"])

        body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary Comparison</div>
        <h1>GTM Engineer vs {label} Salary Comparison</h1>
        <p>{data["verdict"]}</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">{data["gtme_median"]}</span>
        <span class="stat-label">GTM Engineer Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">{data["other_median"]}</span>
        <span class="stat-label">{label} Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">{data["gtme_range"]}</span>
        <span class="stat-label">GTM Engineer Range</span>
    </div>
</div>

<div class="salary-content">
    <h2>How the Roles Compare</h2>
{context_html}
    <h2>Salary Ranges Side-by-Side</h2>
    <table class="data-table">
        <thead>
            <tr><th>Metric</th><th>GTM Engineer</th><th>{label}</th></tr>
        </thead>
        <tbody>
            <tr><td>Salary Range</td><td>{data["gtme_range"]}</td><td>{data["other_range"]}</td></tr>
            <tr><td>Median Salary</td><td>{data["gtme_median"]}</td><td>{data["other_median"]}</td></tr>
            <tr><td>Job Growth (YoY)</td><td>205%</td><td>Varies</td></tr>
        </tbody>
    </table>

{faq_html(data["faq"])}
{salary_related_links(slug, "vs")}
</div>
'''
        body += source_citation_html()
        body += newsletter_cta_html("Get weekly GTM Engineer salary comparisons.")
        extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(data["faq"])

        page = get_page_wrapper(
            title=title, description=description, canonical_path=f"/salary/{slug}/",
            body_content=body, active_path="/salary/",
            extra_head=extra_head, body_class="page-inner",
        )
        write_page(f"salary/{slug}/index.html", page)
        print(f"  Built: salary/{slug}/index.html")


def build_salary_calculator():
    title = "GTM Engineer Salary Calculator (2026 Data)"
    description = (
        "Calculate your GTM Engineer market rate. Select seniority, location, and company"
        " stage for a personalized estimate based on State of GTME Report 2026 (n=228)."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Salary Calculator", None)]
    bc_html = breadcrumb_html(crumbs)

    seniority_opts = '<option value="">Select seniority</option>\n'
    for k, d in SALARY_BY_SENIORITY.items():
        seniority_opts += f'<option value="{k}">{d["label"]}</option>\n'

    location_opts = '<option value="">Select location</option>\n'
    for k, d in SALARY_BY_LOCATION.items():
        location_opts += f'<option value="{k}">{d["label"]}</option>\n'

    stage_opts = '<option value="">Select company stage</option>\n'
    for k, d in SALARY_BY_STAGE.items():
        stage_opts += f'<option value="{k}">{d["label"]}</option>\n'

    js_s = json.dumps({k: {"min": v["min"], "max": v["max"], "median": v["median"]} for k, v in SALARY_BY_SENIORITY.items()})
    js_l = json.dumps({k: {"min": v["min"], "max": v["max"], "median": v["median"]} for k, v in SALARY_BY_LOCATION.items()})
    js_c = json.dumps({k: {"min": v["min"], "max": v["max"], "median": v["median"]} for k, v in SALARY_BY_STAGE.items()})

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary Calculator</div>
        <h1>GTM Engineer Salary Calculator (2026 Data)</h1>
        <p>Get a personalized salary estimate. Select your seniority, location, and company stage.</p>
    </div>
</section>

<div class="salary-content">
    <div class="calculator-form">
        <div class="form-group">
            <label for="calc-seniority">Seniority Level</label>
            <select id="calc-seniority">{seniority_opts}</select>
        </div>
        <div class="form-group">
            <label for="calc-location">Location</label>
            <select id="calc-location">{location_opts}</select>
        </div>
        <div class="form-group">
            <label for="calc-stage">Company Stage</label>
            <select id="calc-stage">{stage_opts}</select>
        </div>
        <button class="btn btn--primary" style="width:100%" onclick="calculateSalary()">Calculate My Market Rate</button>
    </div>

    <div id="calc-result" class="calculator-result" style="display:none">
        <p style="color:var(--gtme-text-secondary);margin-bottom:var(--gtme-space-2)">Estimated salary range:</p>
        <div class="result-range" id="calc-range"></div>
        <p style="color:var(--gtme-text-secondary);margin-top:var(--gtme-space-2)" id="calc-median"></p>
    </div>

    <div class="email-gate">
        <h3>Get the Full Breakdown</h3>
        <p>Enter your email for percentile rankings, total comp estimates, and negotiation benchmarks.</p>
        <form class="email-gate-form" onsubmit="return false;">
            <input type="email" placeholder="Your email" aria-label="Email address" required>
            <button type="submit" class="btn btn--primary">Get Full Report</button>
        </form>
    </div>

    <h2>How This Calculator Works</h2>
    <p>We combine salary data from three dimensions (seniority, location, and company stage) to estimate your market rate. Each dimension contributes to the final range based on relative weighting from the State of GTM Engineering Report 2026 (228 respondents + 3,342 job postings).</p>
    <p>For detailed methodology, see our <a href="/salary/methodology/">data methodology page</a>.</p>

{salary_related_links("calculator", "calculator")}
</div>

<script>
var SD={js_s};
var LD={js_l};
var CD={js_c};
function fmt(n){{return"$"+(n/1000|0)+"K"}}
function calculateSalary(){{
    var s=document.getElementById("calc-seniority").value;
    var l=document.getElementById("calc-location").value;
    var c=document.getElementById("calc-stage").value;
    if(!s||!l||!c){{alert("Select all three fields.");return}}
    var sm=SD[s],lm=LD[l],cm=CD[c];
    var mn=Math.round((sm.min*0.4+lm.min*0.35+cm.min*0.25)/1000)*1000;
    var mx=Math.round((sm.max*0.4+lm.max*0.35+cm.max*0.25)/1000)*1000;
    var md=Math.round((sm.median*0.4+lm.median*0.35+cm.median*0.25)/1000)*1000;
    document.getElementById("calc-range").textContent=fmt(mn)+String.fromCharCode(8209)+fmt(mx);
    document.getElementById("calc-median").textContent="Estimated median: "+fmt(md);
    document.getElementById("calc-result").style.display="block";
}}
</script>
'''
    body += source_citation_html()
    body += newsletter_cta_html()

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/calculator/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("salary/calculator/index.html", page)
    print(f"  Built: salary/calculator/index.html")


def build_salary_methodology():
    title = "GTM Engineer Salary Data Methodology (2026)"
    description = (
        "How GTME Pulse sources GTM Engineer salary data. State of GTME Report 2026"
        " (n=228) survey plus 3,342 job postings. Methods, normalization, limitations."
    )
    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Methodology", None)]
    bc_html = breadcrumb_html(crumbs)

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Data Methodology</div>
        <h1>GTM Engineer Salary Data Methodology (2026)</h1>
        <p>How we collect, clean, and analyze GTM Engineer compensation data.</p>
    </div>
</section>

<div class="salary-content">
    <h2>Data Sources</h2>
    <p>Our salary data comes from two primary sources:</p>
    <ul>
        <li><strong>State of GTM Engineering Report 2026:</strong> A comprehensive survey of 228 GTM Engineers across 32 countries. This is our primary data source for compensation benchmarks, equity data, and career demographics.</li>
        <li><strong>Job posting analysis:</strong> We scrape and analyze 3,342+ job listings from major boards (LinkedIn, Indeed, Greenhouse, Lever, Ashby) twice per week. Postings with disclosed salary ranges validate and supplement the survey data.</li>
        <li><strong>Compensation databases:</strong> Cross-referenced with aggregated data from Glassdoor, Levels.fyi, and Pave where available for validation.</li>
    </ul>

    <h2>Collection Method</h2>
    <p>Our automated pipeline runs twice weekly (Tuesday and Friday at 8 PM PST). For each scrape cycle:</p>
    <ul>
        <li>We search 21 job title variants (GTM Engineer, Go-to-Market Engineer, Revenue Engineer, Growth Engineer, and seniority/leadership variants)</li>
        <li>Duplicate postings are detected via company + title + location matching and removed</li>
        <li>Salary ranges are extracted from structured data fields when available, or parsed from description text</li>
        <li>Postings without any salary information are excluded from compensation analysis but included in job market counts</li>
    </ul>

    <h2>Normalization</h2>
    <p>Raw salary data requires normalization before analysis:</p>
    <ul>
        <li><strong>Annualization:</strong> Hourly or monthly rates converted to annual equivalents</li>
        <li><strong>Base isolation:</strong> Where postings include OTE or total comp, we estimate base salary using role-specific base/variable ratios (typically 85/15 for GTM Engineers)</li>
        <li><strong>Currency:</strong> All figures are in USD. Non-US postings are converted at a 30-day rolling average exchange rate</li>
        <li><strong>Outlier removal:</strong> Postings with salaries below $50K or above $500K are flagged for manual review and typically excluded</li>
    </ul>

    <h2>Classification</h2>
    <p>Each posting is classified across three dimensions:</p>
    <ul>
        <li><strong>Seniority:</strong> Junior/Associate, Mid-Level, Senior, Lead/Staff. Classified by title keywords and requirements section analysis.</li>
        <li><strong>Location:</strong> Mapped to metro areas or "Remote" based on posting location data. Hybrid roles are classified by office location.</li>
        <li><strong>Company stage:</strong> Seed, Series A, Series B, Growth (C/D), Enterprise (public/late-stage). Determined by Crunchbase funding data where available.</li>
    </ul>

    <h2>Sample Sizes</h2>
    <p>Primary dataset: <strong>228 survey respondents</strong> from the State of GTM Engineering Report 2026, spanning 32 countries. Supplemented by <strong>3,342+ job postings</strong> collected since January 2025.</p>
    <p>The US represents 58% of survey respondents (132 respondents). Location-specific salary data uses this US cohort as the primary sample, validated against job postings with disclosed compensation.</p>

    <h2>Limitations</h2>
    <p>This data has known limitations:</p>
    <ul>
        <li><strong>Selection bias:</strong> Companies that disclose salary ranges tend to be larger and based in states with pay transparency laws. Our data may underrepresent small companies and non-disclosure states.</li>
        <li><strong>Role definition:</strong> "GTM Engineer" is a new and evolving title. Some relevant roles use different titles and may not appear in our searches. Conversely, some postings using "GTM" are traditional marketing or sales ops roles.</li>
        <li><strong>Timing:</strong> Salary data reflects posting date, not hire date. Market conditions between posting and hiring can shift compensation.</li>
        <li><strong>Total compensation:</strong> Base salary is more consistently reported than equity, bonuses, and benefits. Our total comp estimates use industry benchmarks for non-base components.</li>
    </ul>

    <h2>Update Frequency</h2>
    <p>Data is refreshed twice weekly. Published salary ranges are recalculated weekly (every Monday). Historical trends track month-over-month changes.</p>

    <h2>Questions or Corrections</h2>
    <p>If you spot an error or have data that could improve our analysis, reach out through the <a href="/about/">About page</a>. We take data accuracy seriously.</p>
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly data updates.")

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/methodology/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("salary/methodology/index.html", page)
    print(f"  Built: salary/methodology/index.html")


# ---------------------------------------------------------------------------
# New salary analysis pages (State of GTME Report 2026)
# ---------------------------------------------------------------------------

def build_salary_coding_premium():
    """Coding premium page: $45K gap between low-code operators and technical GTMEs."""
    title = "GTM Engineer Coding Premium: $45K Gap"
    description = (
        "GTM Engineers who code earn $45K more than low-code operators."
        " Bimodal skill distribution and salary data from the State of GTME Report 2026 (n=228)."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Coding Premium", None)]
    bc_html = breadcrumb_html(crumbs)

    stats_data = {"min": 90000, "max": 195000, "median": 135000, "sample": 228}

    faq_pairs = [
        ("How much more do GTM Engineers who code earn?",
         "GTM Engineers with Python, SQL, and API skills earn roughly $45K more than low-code operators. The median for technical GTMEs is around $135K, while low-code operators cluster near $90K."),
        ("Which programming languages should a GTM Engineer learn?",
         "Python is the highest-ROI language for GTM Engineers. SQL is a close second. Both are used daily for data enrichment, API integration, and pipeline automation. JavaScript helps with webhook handlers and Clay custom actions."),
        ("How long does it take to learn coding as a GTM Engineer?",
         "Most GTM Engineers report reaching productive proficiency in Python within 3-6 months of focused study. You don't need computer science depth. You need enough to write API calls, parse JSON, manipulate dataframes, and build simple automations."),
        ("Is Clay experience enough without coding skills?",
         "Clay-only operators earn well, but they hit a ceiling around $90K-$110K. Adding Python to Clay unlocks custom HTTP actions, complex data transformations, and multi-system orchestration that Clay alone can't handle. That's where the premium starts."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary Analysis</div>
        <h1>The $45K Coding Premium for GTM Engineers</h1>
        <p>Technical skills create a sharp salary divide in GTM Engineering. Here's what the data shows.</p>
    </div>
</section>
{salary_stats_html(stats_data)}
{salary_range_bar_html(stats_data)}
<div class="salary-content">
    <h2>The Coding Premium Explained</h2>
    <p>There's a $45K gap between GTM Engineers who code and those who don't. Low-code operators, the ones building Clay tables and Zapier workflows without touching a terminal, cluster around $90K median compensation. Technical GTMEs, those writing Python, running SQL queries, and building custom API integrations, earn significantly more.</p>
    <p>This isn't speculation. The State of GTM Engineering Report 2026 surveyed 228 GTM Engineers and found a clear bifurcation: compensation tracks technical depth more than years of experience or job title.</p>
    <p>The gap widens at senior levels. A senior low-code operator might earn $120K. A senior technical GTME regularly clears $195K. Same title, same function, $75K apart.</p>

    <h2>The Bimodal Skill Distribution</h2>
    <p>When asked to rate their coding skills on a 1-10 scale, respondents didn't spread evenly across the spectrum. They clustered at two extremes: 1-3 (no-code and low-code users) and 7-10 (developers and technical builders). Very few people rated themselves in the 4-6 range.</p>
    <p>This bimodal pattern mirrors the salary distribution perfectly. There's no middle ground in either skills or pay. You're either operating tools as-is, or you're extending them with code. The market prices these two groups differently.</p>
    <p>Why the gap in the middle? GTM Engineering tends to attract two distinct profiles. Former SDRs and marketers who picked up Clay and automation tools, and former developers or technical ops people who moved into go-to-market work. The two groups approach problems differently, and companies pay accordingly.</p>

    <h2>Which Technical Skills Pay Most</h2>
    <p>Not all technical skills carry equal weight. The report data points to three high-value areas:</p>
    <ul>
        <li><strong>Python:</strong> The single highest-value skill for GTM Engineers. Used for data enrichment scripts, API integration, custom Clay actions, and pipeline automation. Python-fluent GTMEs command the largest premiums.</li>
        <li><strong>SQL:</strong> Critical for anyone working with CRM data, warehouse queries, or building reporting pipelines. SQL skills separate "I can use HubSpot" from "I can query our data warehouse and build attribution models."</li>
        <li><strong>API integration:</strong> Building custom integrations between tools, handling webhooks, managing authentication flows. This is the connective tissue of modern GTM stacks, and it requires code.</li>
    </ul>
    <p>Clay power users who also code earn more than Clay-only operators. The combination of knowing the tool ecosystem and being able to extend it with custom code is where the premium lives.</p>

    <h2>Should You Learn to Code?</h2>
    <p>If you're a GTM Engineer earning around $90K with no coding skills, the math is straightforward. Adding Python proficiency could mean a $30K-$45K salary increase within 12-18 months. That's a better ROI than almost any certification or degree program.</p>
    <p>The learning curve is steep but bounded. You don't need to become a software engineer. You need to write API calls, parse JSON responses, manipulate data with pandas, and build simple automation scripts. That's a focused skill set you can develop in 3-6 months of deliberate practice.</p>
    <p>Start with Python. Build a project that solves a real problem in your current workflow. Automate something you do manually today. The first script you write that saves your team 5 hours a week is your proof of concept, and your strongest card in the next salary negotiation.</p>
    <p>For operators happy at $90K with no interest in coding, that's a valid path. Low-code GTM Engineers do meaningful work. But the ceiling is lower, and the competition for those roles is increasing as more people learn the tool ecosystem.</p>

    <h2>The Hiring Signal</h2>
    <p>Job postings tell the story in real time. GTM Engineer listings that mention Python or SQL in the requirements consistently post salary ranges 25-40% above those that don't. Companies that want technical GTMEs know they have to pay for them.</p>
    <p>The most telling signal: companies are starting to split the role. "GTM Ops Specialist" for the low-code operators at $80K-$110K. "GTM Engineer" for the technical builders at $130K-$195K. Same team, different pay bands, separated by coding ability.</p>
    <p>If you're interviewing, the technical assessment is your negotiating tool. Companies that give you a coding challenge are the ones willing to pay the premium. Companies that don't test technical skills are hiring for the lower band, and will comp accordingly.</p>

    <h2>The Path from Operator to Engineer</h2>
    <p>The most common upskilling path looks like this: start with Python basics (variables, loops, functions), then learn to make HTTP requests with the requests library, then parse JSON responses and work with pandas DataFrames. Within 3 months of consistent practice, you can build useful scripts.</p>
    <p>Months 3-6, apply Python to your actual GTM workflows. Write a script that enriches a CSV through an API. Build a webhook handler. Create a data quality checker. Each project reinforces the skills and builds your portfolio.</p>
    <p>By month 6, you should be comfortable enough to discuss your technical projects in interviews. That's when the $45K premium becomes accessible. You don't need to be an expert. You need to demonstrate that you can solve problems with code when the no-code tools fall short.</p>

{faq_html(faq_pairs)}
{salary_related_links("coding-premium", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer salary data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/coding-premium/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/coding-premium/index.html", page)
    print(f"  Built: salary/coding-premium/index.html")


def build_salary_company_size():
    """Salary by company size: 201-1,000 employees pay the most."""
    title = "GTM Engineer Salary by Company Size (2026)"
    description = (
        "GTM Engineer salary data by company size. Mid-size companies (201-1,000 employees)"
        " pay the highest base. Data from the State of GTME Report 2026 (n=228)."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Company Size", None)]
    bc_html = breadcrumb_html(crumbs)

    stats_data = {"min": 80000, "max": 250000, "median": 135000, "sample": 228}

    faq_pairs = [
        ("Which company size pays GTM Engineers the most?",
         "Mid-size companies with 201-1,000 employees pay the highest base salaries for GTM Engineers, according to the State of GTME Report 2026. These companies have dedicated GTM Engineering budgets but still value individual contributor impact."),
        ("Should I join a startup or enterprise as a GTM Engineer?",
         "Startups (1-50 employees) offer lower base salary but more equity and broader scope. You'll build everything from scratch. Enterprise (1,000+) pays competitive base with RSUs, but the role is more specialized. Mid-size is the sweet spot for base pay."),
        ("How does company size affect GTM Engineer career growth?",
         "Smaller companies give you breadth and ownership fast. You'll touch every part of the GTM stack. Larger companies offer depth, mentorship, and established career ladders. Mid-size companies fall in between, often with the most autonomy and the best compensation."),
        ("Do startups compensate GTM Engineers with equity?",
         "Early-stage startups (Pre-Seed to Seed) give meaningful equity to 29% of GTM Engineers, per the report. By Series A, that drops to 9%. If equity is important to you, the earliest stages are where you'll get it, but at a lower base salary."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary Analysis</div>
        <h1>GTM Engineer Salary by Company Size (2026)</h1>
        <p>How company headcount affects GTM Engineer compensation. 228 survey respondents, all company sizes.</p>
    </div>
</section>
{salary_stats_html(stats_data)}
{salary_range_bar_html(stats_data)}
<div class="salary-content">
    <h2>The Company Size Sweet Spot</h2>
    <p>Mid-size companies, those with 201 to 1,000 employees, pay the highest base salaries for GTM Engineers. They have real budget allocated to go-to-market automation, dedicated headcount for the function, and they still prize individual impact over process compliance.</p>
    <p>This tracks with how GTM Engineering teams grow inside organizations. At 200+ employees, companies have enough pipeline complexity to justify a dedicated GTM Engineer (or a small team). They're past the "one RevOps person does everything" stage. But they haven't yet reached the enterprise level where GTM Engineering gets absorbed into a larger ops organization with rigid role boundaries.</p>
    <p>The data from the State of GTME Report 2026 confirms this pattern across industries and geographies. If maximizing base salary is your priority, the 201-1,000 employee band is where the money is.</p>

    <h2>Small Companies (1-50 Employees)</h2>
    <p>At small companies, the GTM Engineer is often the first hire touching automation and data infrastructure. You're building everything: the Clay enrichment pipeline, the outbound sequences, the CRM architecture, the reporting. It's a generalist role with a building-from-zero mandate.</p>
    <p>Base salary is lower, typically $80K-$120K. Equity is the draw. The State of GTME Report 2026 shows that 29% of GTM Engineers at Pre-Seed companies hold meaningful equity. That percentage drops sharply after the seed stage.</p>
    <p>The trade-off is clear. Lower cash, higher ownership, more autonomy, steeper learning curve. If you want to build a GTM function from scratch and bet on the company's outcome, small is where to be.</p>

    <h2>Mid-Size (51-1,000 Employees)</h2>
    <p>This is where GTM Engineering becomes a strategic function, with a budget line, a team (or at least a team plan), and executive visibility. Companies in this range are scaling their go-to-market motion and need technical builders who can keep the engine running while it grows.</p>
    <p>Base salaries peak here. Mid-level GTM Engineers at 201-1,000 employee companies regularly earn $140K-$175K. Seniors push past $195K. The companies can afford top-of-market rates, and they're competing with both startups (equity) and enterprise (stability) for the same talent.</p>
    <p>The work is often the most interesting in this band too. You're building systems at meaningful scale, with enough complexity to stretch your skills, but without the bureaucratic overhead that slows things down at larger organizations.</p>

    <h2>Enterprise (1,000+ Employees)</h2>
    <p>Enterprise companies pay competitive base salaries with RSUs, annual bonuses, and full benefits packages. Total compensation can match or surpass mid-size companies, especially at public tech companies where RSU grants are substantial.</p>
    <p>The role is different here. You're more likely to own a specific piece of the GTM stack rather than the whole thing. Maybe you're the enrichment pipeline specialist, or the outbound automation owner, or the CRM integration engineer. Scope is narrower but depth is greater.</p>
    <p>Career ladders are more established. There's a path from individual contributor to team lead to director that's visible and documented. The trade-off is less autonomy and more process. If you prefer structure, enterprise is a good fit. If you want to build everything yourself, you'll feel constrained.</p>

    <h2>Choosing Your Company Size</h2>
    <p>The right company size depends on what you optimize for. If you want maximum learning velocity, go small. You'll touch every system, break things, fix them, and develop breadth that takes years to accumulate at larger companies. The pay gap closes later when you carry that experience to a mid-size role.</p>
    <p>If you want maximum base salary now, the 201-1,000 band is the target. These companies combine competitive pay with meaningful scope. You'll own significant projects without the startup chaos or enterprise bureaucracy.</p>
    <p>For total compensation including equity, the calculation gets more complex. A $95K base at a Pre-Seed startup with 0.5% equity could be worth more than $175K at a Series B company, if the startup exits well. Most don't. The expected value math favors the guaranteed higher base in most scenarios.</p>
    <p>One pattern worth noting: GTM Engineers who start at small companies and move to mid-size after 2-3 years often land the highest compensation. They bring the generalist skills and building-from-scratch experience that mid-size companies value, and they can negotiate from a position of demonstrated impact.</p>

    <h2>How Company Growth Changes the Role</h2>
    <p>Companies don't stay the same size. A 50-person startup that hired you as their first GTM Engineer might be 300 people when you've been there two years. Your compensation should track that growth, but it often doesn't automatically.</p>
    <p>When the company crosses the 200-employee threshold, review your comp against market rates for mid-size companies. The data shows that's where base salaries peak. If you're still earning your startup-era salary, you're leaving money on the table. Internal raises rarely keep pace with the jump in market value that comes with company growth.</p>
    <p>The smartest play: negotiate for automatic comp reviews tied to headcount milestones. "When we hit 200 employees, let's revisit my base" is a reasonable ask, especially at fast-growing companies where that milestone might be 12-18 months away.</p>

{faq_html(faq_pairs)}
{salary_related_links("company-size", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer compensation data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/company-size/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/company-size/index.html", page)
    print(f"  Built: salary/company-size/index.html")


def build_salary_funding_stage():
    """Salary by funding stage: Series B & D+ lead at $145K median."""
    title = "GTM Engineer Pay by Funding Stage (2026)"
    description = (
        "GTM Engineer salary by funding stage. Series B and D+ lead at $145K median."
        " Equity trade-offs by round. Data from the State of GTME Report 2026 (n=228)."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Funding Stage", None)]
    bc_html = breadcrumb_html(crumbs)

    stats_data = {"min": 85000, "max": 250000, "median": 145000, "sample": 228}

    faq_pairs = [
        ("Which funding stage pays GTM Engineers the most?",
         "Series B and Series D+ companies pay the highest base salaries, with a $145K median per the State of GTME Report 2026. These companies have proven product-market fit and dedicated GTM Engineering budgets."),
        ("Do early-stage startups give GTM Engineers equity?",
         "Yes, but it varies sharply by stage. At Pre-Seed, 29% of GTM Engineers receive meaningful equity. By Series A, that drops to just 9%. Exited or public companies see equity participation rise again to 33.3%, mostly as RSU grants."),
        ("What is the salary range for a GTM Engineer at a Series A company?",
         "Series A GTM Engineers earn $105K-$145K in base salary, per the report. The range is wide because these companies are still defining the role. Equity and early-employee upside can significantly boost total compensation."),
        ("How does total compensation change as a company raises more funding?",
         "Base salary generally increases with funding rounds, peaking at Series B and D+. Equity shifts from option grants (early stage) to RSUs (late stage and public). Bonuses become more common at growth stage and beyond, with 51% of all GTM Engineers receiving some form of bonus."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary Analysis</div>
        <h1>GTM Engineer Salary by Funding Stage (2026)</h1>
        <p>How funding round affects GTM Engineer pay, equity, and total compensation. All stages compared side by side.</p>
    </div>
</section>
{salary_stats_html(stats_data)}
{salary_range_bar_html(stats_data)}
<div class="salary-content">
    <h2>Funding Stage Salary Overview</h2>
    <p>Compensation for GTM Engineers varies significantly by company funding stage. The State of GTME Report 2026 shows a clear pattern: base salary rises with funding rounds, while equity compensation follows a U-shaped curve, high at the earliest stages, lowest at Series A, and rising again at exit or public stages.</p>
    <p>The highest base salaries cluster at Series B and Series D+, where the median hits $145K. These companies have the revenue, the headcount, and the organizational maturity to pay market rate for technical go-to-market talent. They've also proven that GTM Engineering works for them, which means dedicated budget and defined roles.</p>
    <p>Early-stage companies offer lower base, but the equity math can make up for it, if the company succeeds. The key question is whether you're optimizing for guaranteed cash or potential upside.</p>

    <h2>Pre-Seed to Series A</h2>
    <p>GTM Engineers at Pre-Seed and Seed companies earn $85K-$130K in base salary. The role is broad. You're the entire GTM operations function, building the outbound engine, managing enrichment pipelines, setting up the CRM, and probably doing some prospecting yourself.</p>
    <p>Equity is the draw. The report shows 29% of GTM Engineers at Pre-Seed companies hold meaningful equity stakes. That drops to 9% by Series A, one of the sharpest declines across any function. If equity matters to you, the seed stage is when to negotiate for it.</p>
    <p>Series A companies pay $105K-$145K base. The range is wide because these companies are still defining what "GTM Engineer" means internally. Some treat it as a senior ops role. Others see it as a technical builder position. The title is the same, but the scope and compensation differ.</p>
    <p>The risk-reward calculation at this stage is personal. Lower base, higher variance on total outcome. If the company hits, your equity could be worth multiples of the salary difference. If it doesn't, you earned below market for the duration.</p>

    <h2>Series B and Beyond</h2>
    <p>Series B is where GTM Engineering compensation matures. The median hits $145K, and the role becomes more defined. Companies at this stage have a working go-to-market motion and need technical talent to scale it, automate it, and make it more efficient.</p>
    <p>Series C and D+ companies maintain similar or higher base compensation. The role may be more specialized, you're owning a specific part of the pipeline rather than the whole thing, but the pay reflects the technical depth required.</p>
    <p>Growth-stage companies also offer the most consistent bonus structures. At 51% bonus participation across all stages, growth and late-stage companies are above that average. Bonuses are typically 10-25% of base, tied to pipeline metrics.</p>

    <h2>The Equity Trade-Off</h2>
    <p>Equity compensation follows a surprising pattern in GTM Engineering:</p>
    <ul>
        <li><strong>Pre-Seed:</strong> 29% receive meaningful equity. Options with low strike prices and significant ownership percentages.</li>
        <li><strong>Series A:</strong> Drops to 9%. The role is less likely to be early enough to command equity, but the company is still pre-liquidity.</li>
        <li><strong>Series B-D:</strong> Equity participation rises slightly, often as refresher grants or RSUs. Base salary increases offset the lower equity percentage.</li>
        <li><strong>Exited/Public:</strong> 33.3% receive meaningful equity, mostly as RSU grants with defined vesting schedules and immediate liquidity.</li>
    </ul>
    <p>The U-shaped curve matters for career planning. If you want equity, either join very early (Pre-Seed/Seed) or go public/late-stage where RSUs have defined value. The Series A dead zone, low equity and lower-than-peak base, is the least favorable stage for total compensation, though the learning opportunities are significant.</p>

    <h2>Stage-Specific Negotiation</h2>
    <p>How you negotiate varies by funding stage. At Pre-Seed and Seed, push hard on equity percentage, vesting schedule, and exercise window. Base salary has less room to move because the company is cash-constrained, but equity terms are often flexible because they haven't established comp frameworks yet.</p>
    <p>At Series A, negotiate base aggressively. This is the stage where equity is hardest to get but base salary is still flexible. Companies at this stage are hiring their first dedicated GTM Engineers and often don't have established salary bands. Use market data to anchor high.</p>
    <p>At Series B and beyond, the comp structure is more formalized. Focus on bonus targets (make sure they're tied to metrics you control), RSU grant sizes, and refresher schedules. Base salary bands are often fixed, but the variable comp components have room to move.</p>
    <p>Across all stages, one principle applies: know the company's funding situation before you negotiate. A company that just closed a $50M Series B has different budget constraints than one that's 18 months post-raise and watching its runway. Timing your negotiation to align with fresh capital gives you the most room.</p>

{faq_html(faq_pairs)}
{salary_related_links("funding-stage", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer compensation insights.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/funding-stage/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/funding-stage/index.html", page)
    print(f"  Built: salary/funding-stage/index.html")


def build_salary_experience():
    """Salary by experience level: $105K for <1yr, scaling with years."""
    title = "GTM Engineer Salary by Experience Level"
    description = (
        "GTM Engineer salary by years of experience. $105K for newcomers, scaling"
        " with technical depth. Data from the State of GTME Report 2026 (n=228)."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Experience Level", None)]
    bc_html = breadcrumb_html(crumbs)

    stats_data = {"min": 105000, "max": 250000, "median": 135000, "sample": 228}

    faq_pairs = [
        ("What is the starting salary for a GTM Engineer?",
         "GTM Engineers with less than one year of experience earn a median of $105K, according to the State of GTME Report 2026. Most enter from SDR, RevOps, or marketing ops roles with transferable automation skills."),
        ("How fast does GTM Engineer salary grow with experience?",
         "The biggest jumps happen in years 2-4, where engineers who develop technical depth see 30-40% increases. After year 5, compensation growth slows, partly because the role is so new that few people have 5+ years of dedicated GTM Engineering experience."),
        ("Can I become a GTM Engineer without prior experience?",
         "Yes. Many GTM Engineers entered the field with zero prior experience in the specific role. Backgrounds in SDR/BDR, sales ops, marketing ops, or even software engineering all transfer well. Clay proficiency and automation skills are the price of entry."),
        ("Does experience matter more than skills for GTM Engineer pay?",
         "In a role this new, demonstrated skills often outweigh years of experience. A two-year GTME with Python, Clay, and API integration skills can out-earn a four-year GTME who relies solely on no-code tools. Build a portfolio of measurable pipeline impact."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary Analysis</div>
        <h1>GTM Engineer Salary by Experience Level</h1>
        <p>How years in role affect compensation. From $105K for newcomers to $195K+ for veterans.</p>
    </div>
</section>
{salary_stats_html(stats_data)}
{salary_range_bar_html(stats_data)}
<div class="salary-content">
    <h2>Experience vs Compensation</h2>
    <p>GTM Engineer salary scales with experience, but the relationship is less linear than you'd expect for a traditional engineering role. The State of GTME Report 2026 shows $105K median for engineers with less than one year of experience, rising sharply through years 2-4, then plateauing as the role's newness limits how many people have deep tenure.</p>
    <p>The correlation between years and pay is strong, but it's mediated by technical skill development. An engineer who spends three years in low-code tools earns less than one who picks up Python in year two. Experience matters. What you do with that experience matters more.</p>

    <h2>Year 1: Breaking In</h2>
    <p>New GTM Engineers earn a median of $105K. Most arrive from adjacent roles: SDR, BDR, sales ops, marketing ops, or RevOps. They bring domain knowledge about the sales process and buyer journey, but they're learning the technical GTM stack from scratch.</p>
    <p>The first year is a fire hose. Clay tables, enrichment waterfalls, sequencing tools, CRM automation, webhook configurations. The tool ecosystem is broad, and most new hires spend their first 6 months just getting competent across the core stack.</p>
    <p>Compensation at this level is stable. There's less variance than at any other experience band because the market has a clear sense of what a year-one GTME is worth. The floor is around $85K (small companies, non-tech hubs), the ceiling is $130K (SF/NYC, well-funded startups).</p>

    <h2>Years 2-4: The Steep Climb</h2>
    <p>This is where the biggest salary jumps happen. Mid-level GTM Engineers who develop technical depth, Python, SQL, API integration, see 30-40% increases over their year-one compensation. The jump from "I can use these tools" to "I can build systems with these tools" is where the market rewards you most.</p>
    <p>By year three, strong engineers own significant parts of the pipeline. They're designing enrichment workflows, building multi-step automations, and making architectural decisions about the GTM stack. Companies pay for this ownership and the institutional knowledge that comes with it.</p>
    <p>The variance in this band is extreme. A three-year GTME who stayed in low-code ops might earn $120K. One who learned Python and built custom integrations could earn $175K. Same years of experience, $55K gap. The differentiator is skill trajectory.</p>

    <h2>Years 5+: Senior and Beyond</h2>
    <p>Few people have five or more years of dedicated GTM Engineering experience. The role didn't exist in its current form before 2022-2023. Those who do are commanding $195K+ and often carry titles like Head of GTM Engineering, Director of Revenue Operations, or Senior GTM Architect.</p>
    <p>Compensation at this level starts to plateau against base salary, with the delta shifting to equity, bonuses, and total compensation packages. A senior GTME at a growth-stage company might earn $195K base with a $30K-$50K bonus and meaningful equity.</p>
    <p>The scarcity premium is real. Companies that want a senior GTM Engineer with proven pipeline impact and technical depth are fishing in a very small pond. That supply-demand imbalance keeps senior compensation elevated.</p>

    <h2>Experience vs Skills: What Matters More</h2>
    <p>In a role this new, demonstrated skills carry more weight than a resume timeline. The market can't rely on "10 years of GTM Engineering experience" as a signal because nobody has that. Instead, hiring managers look for:</p>
    <ul>
        <li><strong>Portfolio of work:</strong> Clay tables you've built, automations you've designed, pipelines you've architected. Show the work.</li>
        <li><strong>Technical breadth:</strong> Python, SQL, APIs. Each technical skill you add increases your market value by 10-20%.</li>
        <li><strong>Pipeline impact:</strong> Quantified results. "Built an enrichment pipeline that generated 500 qualified leads per month" beats "5 years of experience."</li>
        <li><strong>Tool depth:</strong> Deep expertise in 2-3 core tools (Clay + HubSpot + Python, for example) signals more than surface-level familiarity with 15 tools.</li>
    </ul>
    <p>This dynamic won't last forever. As the role matures and more people accumulate 5-10 years of experience, tenure will become a stronger signal. Right now, skills and impact are the primary currency.</p>

    <h2>Maximizing Your Experience Value</h2>
    <p>Every year of GTM Engineering experience is worth more when you can quantify what you built. "3 years of GTM Engineering" on a resume tells a hiring manager very little. "Built an enrichment pipeline processing 50K contacts monthly with a 92% accuracy rate" tells them everything they need to know.</p>
    <p>Keep a running log of projects, metrics, and outcomes. Pipeline generated, time saved through automation, data quality improvements, tools evaluated and implemented. This log becomes your negotiation toolkit at review time and your resume ammunition when exploring new roles.</p>
    <p>The other accelerant: teach what you know. GTM Engineers who write about their work, share Clay templates, or contribute to the community build reputations that translate directly into compensation. When a hiring manager has already seen your work online, the interview is a formality and the salary negotiation starts from a higher baseline.</p>

{faq_html(faq_pairs)}
{salary_related_links("by-experience", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer salary data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/by-experience/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/by-experience/index.html", page)
    print(f"  Built: salary/by-experience/index.html")


def build_salary_age():
    """Salary by age bracket: 36+ earns $140K, median age 25."""
    title = "GTM Engineer Salary by Age Bracket (2026)"
    description = (
        "GTM Engineer salary by age. Median age is 25, a Gen Z function. 36+ earns $140K."
        " Age distribution data from the State of GTME Report 2026 (n=228)."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Age Bracket", None)]
    bc_html = breadcrumb_html(crumbs)

    stats_data = {"min": 80000, "max": 250000, "median": 135000, "sample": 228}

    faq_pairs = [
        ("What is the average age of a GTM Engineer?",
         "The median age of GTM Engineers is 25, making it one of the youngest functions in B2B SaaS. The State of GTME Report 2026 shows the majority are under 30, reflecting the role's emergence alongside Gen Z entering the workforce."),
        ("Is it too late to become a GTM Engineer at 30+?",
         "No. GTM Engineers over 30 often earn more than their younger peers because they bring domain expertise from RevOps, sales, or marketing. The 36+ bracket earns a $140K median. Career switchers who combine GTM Engineering skills with business experience are highly valued."),
        ("Does age affect GTM Engineer salary?",
         "Age correlates with salary primarily through experience and seniority. The 36+ bracket earns $140K median, above the overall $135K. But younger engineers with strong technical skills can out-earn older peers who rely on tool-only approaches."),
        ("Why is GTM Engineering so young?",
         "The role emerged in 2022-2023, coinciding with Gen Z entering the workforce. This generation grew up with automation-first thinking, making them natural fits for a role that combines sales process knowledge with technical tool-building skills."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary Analysis</div>
        <h1>GTM Engineer Salary by Age Bracket (2026)</h1>
        <p>Age distribution and compensation data. Median age: 25. A Gen Z function with room for experienced professionals.</p>
    </div>
</section>
{salary_stats_html(stats_data)}
{salary_range_bar_html(stats_data)}
<div class="salary-content">
    <h2>A Gen Z Function</h2>
    <p>The median age of GTM Engineers is 25. That makes this one of the youngest professional functions in B2B SaaS, younger than sales engineering, younger than RevOps, younger than product management. It's a Gen Z role built by the first generation that thinks in automations, not spreadsheets.</p>
    <p>This isn't an accident. GTM Engineering emerged in 2022-2023, right as Gen Z professionals were hitting their stride in the workforce. They grew up building Zapier workflows before they had job titles. Clay, Make, and API integrations feel native to them in a way that doesn't translate to older professionals who learned these tools later.</p>
    <p>The youth of the field shapes everything: compensation curves, career ladder expectations, management structures. When most of your colleagues are under 30, the norms are still being written.</p>

    <h2>Under 30: The Majority</h2>
    <p>Most GTM Engineers are in their 20s. They entered the field from SDR/BDR roles, marketing coordinator positions, or directly from school with Clay and automation skills already in hand. A growing number have no prior professional experience at all, they built their portfolios through Clay Bootcamp, online courses, and side projects.</p>
    <p>Salary for this cohort reflects their experience level. The median sits below the overall $135K, with most earning $90K-$130K depending on technical depth and market. The ceiling rises quickly for those who develop coding skills early.</p>
    <p>The advantage of entering young: you're accumulating experience in a role with explosive demand. A 24-year-old with 2 years of GTM Engineering experience today will have 5+ years by the time they're 27. That kind of tenure will be rare and valuable as the function matures.</p>

    <h2>30-35: The Experience Premium</h2>
    <p>GTM Engineers in the 30-35 bracket tend to be career switchers. They spent their 20s in RevOps, sales ops, marketing ops, or sometimes software engineering, then transitioned into GTM Engineering when the role formalized. They bring something younger engineers don't have: deep domain knowledge about how sales and marketing organizations work.</p>
    <p>This combination of GTM Engineering technical skills and business context commands a premium. A 32-year-old who spent five years in RevOps before becoming a GTM Engineer understands pipeline dynamics, attribution models, and sales team workflows at a level that takes years to develop.</p>
    <p>Compensation in this bracket runs $130K-$175K, above the overall median. The premium reflects the domain expertise layered on top of the technical skill set.</p>

    <h2>36+: The Senior Tier</h2>
    <p>The 36+ bracket is the smallest group of GTM Engineers, but they earn the highest median: $140K. These are heads of GTM Engineering, directors, or senior individual contributors who brought decades of sales, marketing, or operations experience into the role.</p>
    <p>Many in this group don't carry the "GTM Engineer" title. They're VP of Revenue Operations who built out a GTM Engineering function, or Directors of Marketing Technology who evolved into the role as their companies adopted the GTM Engineering framework.</p>
    <p>The path for experienced professionals entering GTM Engineering is clear: your domain expertise is your differentiator. You won't out-code a 23-year-old developer. But you'll out-strategize them on pipeline architecture, sales process optimization, and cross-functional collaboration. The market values both, and pays accordingly.</p>

    <h2>What This Means for Career Planning</h2>
    <p>The youth of the field creates an unusual dynamic: there's no established career ladder. No one has "20 years of GTM Engineering experience" because the role didn't exist 20 years ago. The ceiling is being set right now by the current generation.</p>
    <p>For young professionals, this is an opportunity. You can define what a senior GTM Engineering career looks like. Head of GTM Engineering roles are emerging at growth-stage companies, and the first people to fill them will set the template for everyone who follows.</p>
    <p>For experienced professionals considering the switch, the window is open. Your business knowledge fills a gap that pure-technical GTM Engineers can't cover. The role rewards generalists who can bridge technology and strategy, and that's exactly what career switchers with domain expertise bring to the table.</p>

    <h2>Age and Hiring</h2>
    <p>Do companies discriminate by age when hiring GTM Engineers? The data doesn't directly answer this, but the hiring patterns suggest a preference for outcome over demographic. Companies posting GTM Engineer roles care about Clay proficiency, technical skills, and pipeline impact. Resume age signals (graduation year, career length) matter less in a function where a 23-year-old can out-produce a 35-year-old and vice versa.</p>
    <p>If you're over 30 and entering the field, position your experience as a feature. A RevOps manager who becomes a GTM Engineer brings pipeline strategy, cross-functional relationships, and operational maturity. These are things that take years to develop and can't be taught through a bootcamp.</p>
    <p>The companies most receptive to experienced GTM Engineers are those building their first GTM Engineering function. They need someone who can set direction, not just execute. A 28-year-old who's built Clay tables for two years is great at execution. A 35-year-old who understands the full revenue cycle and can also build Clay tables is a force multiplier.</p>

{faq_html(faq_pairs)}
{salary_related_links("by-age", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Weekly GTM Engineer career and salary data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/by-age/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/by-age/index.html", page)
    print(f"  Built: salary/by-age/index.html")


def build_salary_bonus():
    """Bonus structure page: 51% receive bonus, 56% get 10-25% of base."""
    title = "GTM Engineer Bonus Data: Who Gets Paid"
    description = (
        "51% of GTM Engineers receive bonuses. 56% get 10-25% of base salary."
        " Performance vs guaranteed breakdown. State of GTME Report 2026 (n=228)."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Bonus Data", None)]
    bc_html = breadcrumb_html(crumbs)

    # Custom stats block for bonus data (percentages, not salary ranges)
    bonus_stats = '''<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">51%</span>
        <span class="stat-label">Receive a Bonus</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">10&#8209;25%</span>
        <span class="stat-label">Most Common Range</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">61%</span>
        <span class="stat-label">Performance-Based</span>
    </div>
</div>'''

    faq_pairs = [
        ("What percentage of GTM Engineers get bonuses?",
         "51% of GTM Engineers receive some form of bonus, according to the State of GTME Report 2026. The remaining 49% are compensated with base salary only, common among freelancers, agency GTMEs, and early-stage startup employees."),
        ("How big is a typical GTM Engineer bonus?",
         "56% of GTM Engineers who receive bonuses get 10-25% of their base salary. On a $135K base, that's $13,500 to $33,750 in additional annual compensation. Some receive less than 10%, and a small percentage earn 25%+."),
        ("Are GTM Engineer bonuses performance-based or guaranteed?",
         "61% of bonuses are performance-based, tied to pipeline metrics, meetings booked, or revenue influenced. The remaining 39% are guaranteed (annual, quarterly, or signing bonuses). Performance-based bonuses are more common at growth-stage and enterprise companies."),
        ("How should I negotiate a bonus as a GTM Engineer?",
         "Tie your bonus to metrics you can control and measure. Pipeline generated, qualified meetings booked, and enrichment coverage rates are strong targets. Avoid bonuses tied to team revenue goals you can't directly influence. Get the targets in writing before accepting the offer."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Compensation Analysis</div>
        <h1>GTM Engineer Bonus Structure Data (2026)</h1>
        <p>Who gets bonuses, how much, and what type. Bonus participation and structure data from 228 GTM Engineers.</p>
    </div>
</section>
{bonus_stats}
<div class="salary-content">
    <h2>The Bonus Picture</h2>
    <p>Just over half of GTM Engineers, 51%, receive some form of bonus compensation. That's lower than enterprise sales roles (where variable comp is standard) but higher than most operations and engineering functions. GTM Engineering sits in a compensation gray zone: technical enough for base-heavy packages, revenue-adjacent enough for performance bonuses.</p>
    <p>The 49% without bonuses aren't being shortchanged by default. Freelance and agency GTMEs set their own rates and don't typically structure bonus agreements. Early-stage startup engineers may trade bonus potential for equity. And some companies simply haven't figured out how to comp a role this new.</p>

    <h2>Bonus Size Distribution</h2>
    <p>Among GTM Engineers who receive bonuses, the distribution breaks down clearly:</p>
    <ul>
        <li><strong>Under 10% of base:</strong> Common at companies that are experimenting with variable comp for the role. Often a quarterly or annual discretionary bonus rather than a structured plan.</li>
        <li><strong>10-25% of base (56% of bonused GTMEs):</strong> The most common range. On a $135K base, that's $13,500-$33,750 in annual bonus potential. This is where most structured bonus plans land.</li>
        <li><strong>25%+ of base:</strong> Rare, usually at companies that treat GTM Engineering as a revenue-generating function (not a support function). These are often tied to aggressive pipeline or revenue targets.</li>
    </ul>
    <p>The 10-25% range is the market standard. If you're negotiating a bonus and the company offers less than 10%, push for more or negotiate a higher base instead. Below 10%, the bonus often isn't worth the complexity of tracking and paying out.</p>

    <h2>Performance vs Guaranteed</h2>
    <p>61% of GTM Engineer bonuses are performance-based. They're tied to measurable outcomes: pipeline generated, qualified meetings booked, revenue influenced, enrichment coverage rates. The specific metrics vary by company, but the common thread is quantifiable impact on the go-to-market motion.</p>
    <p>The remaining 39% are guaranteed: annual bonuses, quarterly payouts, or signing bonuses that pay regardless of performance. Guaranteed bonuses are more common at enterprise companies with established comp structures and at companies that haven't yet defined GTM Engineering KPIs.</p>
    <p>Performance-based bonuses carry more risk but typically have higher ceilings. If you're confident in your ability to hit pipeline targets, performance comp is the better deal. If you're joining a company where GTM Engineering metrics aren't well-defined yet, push for guaranteed comp until the measurement framework matures.</p>

    <h2>Who Gets Bonuses</h2>
    <p>Bonus participation varies significantly by company type and employment arrangement:</p>
    <ul>
        <li><strong>In-house at growth-stage companies:</strong> Highest bonus participation. These companies have the budget, the pipeline complexity, and the performance data to structure meaningful variable comp.</li>
        <li><strong>In-house at enterprise:</strong> High participation with structured plans. Bonuses are often part of company-wide comp frameworks rather than GTM Engineering-specific plans.</li>
        <li><strong>In-house at early-stage:</strong> Lower participation. Many early-stage companies compensate with equity instead of bonuses, or haven't formalized comp structures yet.</li>
        <li><strong>Agency/freelance:</strong> Rare. Freelance GTMEs set their own rates and build performance incentives into their contract structures (retainer + performance fees).</li>
    </ul>

    <h2>Negotiating Your Bonus</h2>
    <p>Three principles for negotiating GTM Engineer variable comp:</p>
    <p><strong>Tie it to metrics you control.</strong> Pipeline generated from your enrichment workflows, meetings booked from your outbound sequences, data quality improvements you can measure. Avoid bonuses tied to team-level revenue goals where your individual contribution is hard to isolate.</p>
    <p><strong>Get the targets in writing.</strong> "Performance bonus" means nothing without defined targets, measurement methods, and payout timing. Before accepting, know exactly what "on target" looks like and what the payout schedule is.</p>
    <p><strong>Do the math on guaranteed vs performance.</strong> A guaranteed $20K bonus is worth more than a $30K target you have a 60% chance of hitting. If the company can't clearly explain how you'd hit your bonus targets, negotiate for guaranteed comp or a higher base instead.</p>

    <h2>Bonus Trends to Watch</h2>
    <p>As GTM Engineering matures as a function, bonus structures are evolving. Three trends are emerging from the report data and job posting analysis:</p>
    <p>First, more companies are adding performance bonuses for GTM Engineers. The 51% participation rate is up from what industry observers estimate was around 30-35% two years ago. As companies get better at measuring GTM Engineering impact, they're more willing to compensate for it.</p>
    <p>Second, bonus metrics are getting more specific. Early GTM Engineering bonuses were often tied to vague "team performance" or "company revenue" goals. Now, companies are tying them to pipeline generated through automated workflows, enrichment coverage rates, and outbound meeting conversion. These are metrics the GTM Engineer directly controls.</p>
    <p>Third, the total comp package is becoming more standardized. At growth-stage companies, the emerging standard is base salary plus 15-20% performance bonus plus equity. This mirrors the compensation structure of senior RevOps roles and reflects GTM Engineering's growing recognition as a strategic function.</p>

    <h2>Bonus vs Higher Base: Which to Prioritize</h2>
    <p>Given the choice between a $140K base with no bonus and a $125K base with a $20K target bonus, which should you take? The guaranteed base is worth more in most scenarios. Bonuses depend on target attainment, company performance, and sometimes manager discretion. Base salary is a commitment.</p>
    <p>The exception: if the bonus targets are well-defined, measurable, and within your control. A $125K base with a $25K bonus tied to "generate 500 qualified leads per quarter through automated enrichment pipelines" is a strong deal if you're confident in your pipeline. You'll likely beat target and earn more than the $140K flat offer.</p>
    <p>When evaluating bonus offers, ask three questions. What were the actual payout rates for this bonus plan last year? What percentage of GTM Engineers on the team hit their targets? And who decides whether the targets were met? The answers will tell you whether the bonus is real compensation or a number on paper.</p>

{faq_html(faq_pairs)}
{salary_related_links("bonus", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Weekly GTM Engineer compensation data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/bonus/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/bonus/index.html", page)
    print(f"  Built: salary/bonus/index.html")


def build_salary_equity():
    """Equity compensation page: 68% have no meaningful equity."""
    title = "GTM Engineer Equity: 68% Have No Stake"
    description = (
        "68% of GTM Engineers hold no meaningful equity. Pre-Seed (29%) and Exited/Public"
        " (33%) are the only stages where equity matters. State of GTME Report 2026."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Equity Data", None)]
    bc_html = breadcrumb_html(crumbs)

    # Custom stats block for equity data (percentages, not salary ranges)
    equity_stats = '''<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">68%</span>
        <span class="stat-label">No Meaningful Equity</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">29%</span>
        <span class="stat-label">Pre-Seed w/ Equity</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">33%</span>
        <span class="stat-label">Exited/Public w/ Equity</span>
    </div>
</div>'''

    faq_pairs = [
        ("What equity do most GTM Engineers get?",
         "68% of GTM Engineers report holding 0-0.10% equity, which is functionally zero after dilution. Only at Pre-Seed (29% get meaningful grants) and Exited/Public companies (33.3% via RSU programs) does equity become a real part of compensation."),
        ("Should I prioritize equity or base salary as a GTM Engineer?",
         "For most GTM Engineers, base salary should be the priority. Equity is only meaningful at Pre-Seed (high risk, 29% chance of a real grant) or public companies (RSUs with predictable value). At Series A through Series B, equity grants are typically too small to matter after dilution."),
        ("How do I evaluate a GTM Engineer equity offer?",
         "Ask three questions: what percentage of fully diluted shares, what is the current 409A valuation, and what is the most recent preferred share price. Multiply your shares by the 409A price for a floor value. Then discount heavily for illiquidity, dilution from future rounds, and the probability the company reaches an exit."),
        ("When is equity worth taking a lower base salary?",
         "Only at Pre-Seed or very early Seed, where you might get 0.1-0.5% of the company. The expected value of that equity has to cover the salary gap over your expected tenure. For a $20K/year salary cut over 3 years, your equity needs to be worth at least $60K at exit to break even. Most startups don't exit."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Compensation Analysis</div>
        <h1>GTM Engineer Equity: 68% Have Nothing</h1>
        <p>Equity ownership data across funding stages. Most GTM Engineers hold zero meaningful equity.</p>
    </div>
</section>
{equity_stats}
<div class="salary-content">
    <h2>The Equity Reality</h2>
    <p>68% of GTM Engineers report holding 0-0.10% equity in their company. That's functionally zero. After dilution from future funding rounds, a 0.05% stake in a Series A company is worth pennies unless the company reaches a multi-billion-dollar exit.</p>
    <p>This matches the operational nature of the role at most companies. GTM Engineers are hired to build outbound infrastructure, not to be founding team members. Companies treat the position as a skilled technical hire, compensated primarily through base salary and bonuses, not ownership.</p>
    <p>The State of GTME Report 2026 surveyed 228 GTM Engineers across all funding stages. The equity picture is clear: for most practitioners, equity is a line item on an offer letter, not a wealth-building mechanism. Understanding when equity does matter, and when it doesn't, is critical for making smart compensation decisions.</p>

    <h2>By Funding Stage</h2>
    <p>Equity distribution follows a U-shaped curve across funding stages. The earliest and latest stages offer meaningful equity. Everything in between is a dead zone.</p>
    <p><strong>Pre-Seed: 29% get meaningful equity.</strong> At this stage, you're employee 1-5 and building the GTM function from nothing. Companies haven't raised much capital, so they compensate with ownership. A 0.1-0.5% grant is common. The risk is enormous, the base salary is lower ($90K-$120K typical), and the company might not exist in 18 months. But the equity could be worth something real if the company works.</p>
    <p><strong>Series A: 9% get meaningful equity.</strong> The drop from 29% to 9% is sharp. By Series A, the company has raised $5M-$15M, the founding team has allocated most of the option pool, and GTM Engineers are viewed as operational hires. You'll get a grant, but it will be small, often 0.01-0.05%. At this stage, negotiate for base salary.</p>
    <p><strong>Exited/Public: 33.3% get meaningful equity.</strong> The rebound at public and post-exit companies comes from RSU programs. These aren't startup lottery tickets. They're liquid stock grants with predictable value. A $50K-$100K annual RSU grant at a public company is real compensation you can model and plan around.</p>

    <h2>Seed and Series B: The Dead Zone</h2>
    <p>Over 70% of GTM Engineers at Seed and Series B companies carry negligible or zero equity. These stages represent the worst of both worlds for equity compensation.</p>
    <p>At Seed, the company has raised enough to pay competitive base salaries ($120K-$150K), which means they don't need to compensate with large equity grants. But they haven't yet built RSU programs or formalized equity refreshers. You get a token option grant and a verbal promise that "we'll revisit equity at the next round."</p>
    <p>Series B is similar. The company has $20M-$50M in the bank. The option pool has been carved up across multiple rounds of hiring. Your 0.02-0.05% grant will be diluted by at least one more funding round before any exit. The math rarely works in your favor.</p>
    <p>If you're at a Seed or Series B company and equity matters to you, the honest advice is to optimize for base salary and bonus instead. Your equity grant at these stages is more of a retention tool (vesting schedule keeps you around) than a wealth-building instrument.</p>

    <h2>When Equity Matters</h2>
    <p>Equity is worth pursuing in two scenarios, and they look very different.</p>
    <p><strong>Scenario 1: Pre-Seed bet.</strong> You join a 3-person company, take a $100K salary when you could earn $135K elsewhere, and get 0.25% of the company. If the company reaches a $500M exit in 5-7 years, your stake is worth $1.25M before dilution (probably $500K-$800K after). That's a life-changing outcome. But 90%+ of startups at this stage fail or exit below the preference stack. You're betting $35K/year in foregone salary (over 3 years, that's $105K) on a lottery ticket with better-than-average but still long odds.</p>
    <p><strong>Scenario 2: Public company RSUs.</strong> You join a public SaaS company, get a $70K annual RSU grant that vests over 4 years, and the stock trades at a known price. This is straightforward. RSUs at a profitable public company are cash-equivalent compensation. Factor them into your total comp calculation at face value, discounted slightly for vesting risk (you might leave before full vesting).</p>
    <p>The middle ground, Series A through late-stage private companies, is where equity gets murky. The grants are too small to be life-changing, the companies are too far from exit for the value to be predictable, and the base salary foregone to join "for the equity" is rarely recovered.</p>

    <h2>Negotiating Equity</h2>
    <p>If you're in a position to negotiate equity as a GTM Engineer, here's what matters.</p>
    <p><strong>Know the stage.</strong> Your negotiating power on equity is highest at Pre-Seed and lowest at Series B+. If the company won't move on equity, push on base salary instead. At Post-Series A companies, a $10K base increase is almost always worth more than an extra 0.01%.</p>
    <p><strong>Ask for the cap table.</strong> Specifically, ask: what is my percentage of fully diluted shares, what is the current 409A valuation, and how many shares are in the option pool. Without this information, your equity offer is meaningless numbers on paper.</p>
    <p><strong>Understand dilution.</strong> Your 0.1% today will be 0.06-0.07% after the next funding round. Model two rounds of dilution into any equity calculation. If the number still looks compelling after 30-40% dilution, the grant is worth considering.</p>
    <p><strong>Check the exercise window.</strong> Standard ISOs have a 90-day exercise window after you leave. Early exercise provisions or extended exercise windows (7-10 years) are valuable. If you have to come up with $50K in cash to exercise options within 90 days of leaving, that changes the math on whether the equity is worth anything to you.</p>

{faq_html(faq_pairs)}
{salary_related_links("equity", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Weekly GTM Engineer compensation data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/equity/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/equity/index.html", page)
    print(f"  Built: salary/equity/index.html")


def build_salary_us_vs_global():
    """US vs global salary comparison: $135K vs $75K median."""
    title = "GTM Engineer Salary: US vs Global Pay Gap"
    description = (
        "US GTM Engineers earn $135K median vs $75K outside the US. Geographic distribution"
        " across 32 countries. Data from the State of GTME Report 2026 (n=228)."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("US vs Global", None)]
    bc_html = breadcrumb_html(crumbs)

    # Side-by-side comparison stats
    geo_stats = '''<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">$135K</span>
        <span class="stat-label">US Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$75K</span>
        <span class="stat-label">Non-US Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">32</span>
        <span class="stat-label">Countries Represented</span>
    </div>
</div>'''

    faq_pairs = [
        ("How much more do US GTM Engineers earn than global peers?",
         "US GTM Engineers earn a $135K median vs $75K for non-US peers, an 80% premium. This reflects the concentration of GTM Engineering roles in US tech companies, higher cost of living, and stronger demand in the US market."),
        ("Which countries outside the US pay GTM Engineers the most?",
         "UK, Germany, and Australia pay the highest non-US salaries for GTM Engineers. European salaries are growing as US companies hire remote workers in the region. UK-based GTM Engineers working for US companies often earn close to US rates."),
        ("Do US companies pay global remote GTM Engineers US rates?",
         "Some do, most don't. US companies hiring globally typically pay 60-80% of US rates for equivalent roles. Companies using geo-adjusted pay reduce offers by 20-40% based on local cost of living. A few companies (GitLab model) pay the same regardless of location."),
        ("What's the best market for GTM Engineers outside the US?",
         "Europe, specifically the UK and Germany. 17% of GTM Engineers in the report are in Europe, and the market is growing. Many European GTMEs work for US companies remotely, earning above local market rates. APAC is growing but skews heavily toward agency work."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Geographic Analysis</div>
        <h1>GTM Engineer Salary: US vs Global Pay</h1>
        <p>The $60K gap between US and non-US GTM Engineer compensation, with geographic distribution data.</p>
    </div>
</section>
{geo_stats}
<div class="salary-content">
    <h2>The $60K Gap</h2>
    <p>US GTM Engineers earn $135K median. Everyone else earns $75K. That's an 80% premium for working in the United States, and it's the largest geographic pay gap in the State of GTME Report 2026.</p>
    <p>The gap reflects three factors. First, the concentration of GTM Engineering demand: 58% of all survey respondents work in the US, and an even larger share of job postings originate from US companies. Second, US cost of living, particularly in tech hubs like San Francisco ($195K median), New York ($185K), and Seattle ($190K). Third, the maturity of the US GTM Engineering market, where the role is better understood, better compensated, and more established in hiring frameworks.</p>
    <p>For non-US GTM Engineers, the gap creates both a challenge and an opportunity. The challenge: your local market may not value the role as highly as the US does. The opportunity: US companies hiring remotely will pay you significantly above local market rates, even if they apply a geographic discount.</p>

    <h2>Geographic Distribution</h2>
    <p>The State of GTME Report 2026 drew respondents from 32 countries. Here's how they're distributed:</p>
    <ul>
        <li><strong>United States: 58% (132 respondents).</strong> The center of gravity for GTM Engineering. More than half of all practitioners work here, and the overwhelming majority of job postings target US-based candidates.</li>
        <li><strong>Europe: 17% (38 respondents).</strong> The second-largest market. UK, Germany, and France lead. European GTM Engineering is growing as SaaS adoption increases and US companies build remote teams in the region.</li>
        <li><strong>APAC: 9% (21 respondents).</strong> India, Australia, and Singapore are the main markets. APAC skews toward agency and freelance work rather than in-house roles. Companies in India and Southeast Asia provide GTM Engineering services to US and European clients.</li>
        <li><strong>MEA (Middle East & Africa): 5% (12 respondents).</strong> An emerging market. Israel has the strongest GTM Engineering presence in the region, driven by its dense startup ecosystem. South Africa and the UAE are growing.</li>
        <li><strong>Canada: 5% (11 respondents).</strong> Canadian GTM Engineers benefit from proximity to the US market. Many work for US companies, earning above Canadian market rates. Toronto and Vancouver are the primary hubs.</li>
        <li><strong>LATAM: 2% (5 respondents).</strong> The smallest market by far. Brazil and Mexico have emerging GTM Engineering communities, often serving US clients at competitive rates. The region is early in adoption.</li>
    </ul>

    <h2>Europe: The Growing Market</h2>
    <p>Europe represents 17% of GTM Engineering practitioners, making it the largest market outside the US. Three trends are shaping European GTM Engineering compensation.</p>
    <p>First, US companies are hiring European GTM Engineers as remote workers. A UK-based GTME working for a US SaaS company might earn GBP 70K-90K ($88K-$113K), which is below US rates but well above UK market rates for similar operational roles. This arbitrage is drawing talent into the field.</p>
    <p>Second, European SaaS companies are building their own GTM Engineering teams. Companies like Personio, Dealfront, and Paddle are hiring for the role at European salaries. The pay is lower than US equivalents ($60K-$90K for mid-level roles in most European markets), but the function is growing.</p>
    <p>Third, the UK leads European adoption. London's fintech and SaaS concentration makes it the strongest European hub for GTM Engineering. Berlin and Amsterdam follow, benefiting from thriving startup ecosystems and large English-speaking professional communities.</p>

    <h2>APAC and MEA: Agency-Heavy Markets</h2>
    <p>APAC and MEA account for 14% of GTM Engineers combined, but the employment model is different from the US and Europe. In these regions, GTM Engineering skews heavily toward agency and freelance work rather than in-house positions.</p>
    <p>In India, companies offer GTM Engineering as a service to US clients at rates of $2K-$5K per month. The individual GTME might earn $25K-$40K annually, which is competitive locally. The business model works because the labor cost arbitrage is substantial: a US company paying $4K/month for an Indian GTM Engineering agency is spending a fraction of what a US-based hire would cost.</p>
    <p>Australia is an outlier in APAC. Salaries are closer to European levels ($70K-$100K), and the market is primarily in-house roles at Australian SaaS companies. The small market size (Australia's tech sector is much smaller than the US or Europe) limits the number of pure GTM Engineering positions.</p>
    <p>MEA is the most nascent market. Israel has a sophisticated GTM Engineering community, driven by the country's dense concentration of B2B SaaS startups. Outside Israel, the role is still rare in the Middle East and Africa, with most practitioners working as freelancers for international clients.</p>

    <h2>Remote Work and Global Arbitrage</h2>
    <p>The remote work revolution has created a global arbitrage opportunity for GTM Engineers. The pattern is simple: earn closer to US rates while living in a lower-cost market.</p>
    <p>US companies hiring globally typically apply one of three models:</p>
    <ul>
        <li><strong>Location-agnostic pay:</strong> Same salary regardless of location. Rare, but companies like GitLab and some early-stage startups use this approach. A European GTME at these companies earns US rates.</li>
        <li><strong>Geo-adjusted pay:</strong> US rates discounted by 20-40% based on local cost of living. This is the most common model. A GTM Engineer in Lisbon might earn $85K-$95K working for a US company, vs $50K-$65K at a Portuguese company.</li>
        <li><strong>Local market rates:</strong> Pay based entirely on the local market. Usually at companies using Employer of Record (EOR) services to hire internationally. Salaries match local benchmarks, which means $40K-$70K in most markets outside the US and UK.</li>
    </ul>
    <p>For non-US GTM Engineers, the strategy is clear: develop skills that US companies need, build a portfolio of automation work, and target remote roles at US-headquartered companies. Even with a 30% geographic discount, you'll earn substantially more than local market rates in most countries.</p>
    <p>The risk in this arbitrage: US companies may eventually push more aggressively on local market pricing as the global talent pool expands. For now, demand for GTM Engineers outpaces supply everywhere, which keeps the arbitrage window open.</p>

{faq_html(faq_pairs)}
{salary_related_links("us-vs-global", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Weekly GTM Engineer salary data from 32 countries.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/us-vs-global/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/us-vs-global/index.html", page)
    print(f"  Built: salary/us-vs-global/index.html")


def build_salary_posted_vs_actual():
    """Posted vs actual salary comparison: $150K posted vs $135K reported."""
    title = "Posted vs Actual GTM Engineer Salary Data"
    description = (
        "Job postings list $150K median for GTM Engineers but actual pay is $135K."
        " How to interpret salary ranges in job listings. GTME Report 2026 data."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Posted vs Actual", None)]
    bc_html = breadcrumb_html(crumbs)

    # Comparison stats
    posted_stats = '''<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">$150K</span>
        <span class="stat-label">Job Listing Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$135K</span>
        <span class="stat-label">Survey Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">224</span>
        <span class="stat-label">Listings Analyzed</span>
    </div>
</div>'''

    faq_pairs = [
        ("Why are posted GTM Engineer salaries higher than actual salaries?",
         "Posted salaries include aspirational ranges, are skewed toward larger companies that are required to disclose pay, and often reflect the high end of the band. Smaller companies that don't disclose pay (and often pay less) are invisible in posting data, pulling the posted median above the survey median."),
        ("How much should I discount a job posting salary range?",
         "Expect to receive an offer 10-15% below the posted midpoint. If a posting says $130K-$175K, the actual offer will likely land between $130K and $150K. The top of the posted range is rarely offered to external candidates without competing offers."),
        ("Is Glassdoor salary data accurate for GTM Engineers?",
         "Glassdoor data is limited for GTM Engineers because the role is too new for large sample sizes. Most Glassdoor estimates for 'GTM Engineer' are modeled from adjacent roles, not reported by actual GTM Engineers. The State of GTME Report 2026 (n=228) provides the most reliable salary data available."),
        ("How should I use posted salary data when negotiating?",
         "Use the posted range as a ceiling, not a starting point. If the posting says $130K-$175K, anchor your ask at $150K-$160K and be prepared to explain why you're worth the upper half. Bring data from the GTME Report or this page to support your number."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Salary Analysis</div>
        <h1>Posted vs Actual GTM Engineer Salaries</h1>
        <p>Job postings show higher numbers than people report earning. Here's why, and how to use both data sets.</p>
    </div>
</section>
{posted_stats}
<div class="salary-content">
    <h2>The Posting Premium</h2>
    <p>Job postings list higher salaries than GTM Engineers report earning. The posted median is $150K (from 224 GTM Engineer listings with disclosed compensation). The self-reported median is $135K (from 228 survey respondents). That's a $15K gap, about 11%.</p>
    <p>This isn't unique to GTM Engineering. Posted salaries run above reported salaries across most tech roles. But the gap matters for GTM Engineers specifically because the role is new enough that candidates don't have strong salary benchmarks. Without context, a job seeker might expect $150K based on postings and be disappointed by a $135K offer, not realizing the offer is at market rate.</p>
    <p>Understanding the gap is a negotiation advantage. Walk into an interview knowing that $135K is the true median, that postings inflate by 10-15%, and that the posted range ceiling is rarely the actual offer ceiling. You'll negotiate from a position of data, not hope.</p>

    <h2>Why Postings Run Higher</h2>
    <p>Three factors push posted salaries above actual compensation.</p>
    <p><strong>Selection bias in who posts.</strong> Pay transparency laws in California, Colorado, New York, and Washington require salary range disclosure. Companies in these states tend to be larger, better-funded, and based in high-cost markets. They pay more. Smaller companies outside these states, which often pay less, aren't required to disclose and frequently don't. The posted data over-represents well-paying companies.</p>
    <p><strong>Range inflation.</strong> Job postings show ranges, not single numbers. A $130K-$175K range has a midpoint of $152.5K, but the actual offer distribution within that range skews toward the lower end. Companies post wide ranges to attract candidates, then offer near the bottom unless the candidate has competing offers or exceptional experience.</p>
    <p><strong>Aspirational upper bounds.</strong> The top of a posted range often represents what the company would pay an internal promotion or a candidate with 2-3 more years of experience than the posting targets. External hires rarely land at the top of the range. It's the price tag, not the purchase price.</p>

    <h2>US Posted Salary Bands</h2>
    <p>For US-based GTM Engineer postings with disclosed compensation, here's the detailed breakdown:</p>
    <ul>
        <li><strong>Median posted salary:</strong> $130K</li>
        <li><strong>25th percentile (P25):</strong> $107K</li>
        <li><strong>75th percentile (P75):</strong> $150K</li>
        <li><strong>90th percentile (P90):</strong> $180K</li>
        <li><strong>Average minimum of posted ranges:</strong> $128K</li>
        <li><strong>Average of posted ranges:</strong> $152K</li>
        <li><strong>Average maximum of posted ranges:</strong> $175K</li>
    </ul>
    <p>The P25-P75 spread ($107K-$150K) represents where 50% of posted salaries fall. If a posting is within this range, it's market rate. Below $107K signals a junior role, an agency position, or a company underpricing the function. Above $150K typically means senior level, high-cost-of-living market, or a company that treats GTM Engineering as a strategic priority.</p>

    <h2>What This Means for Negotiation</h2>
    <p>Armed with both posted and actual salary data, here's how to negotiate effectively.</p>
    <p><strong>Calibrate your expectations.</strong> If a posting says $130K-$175K, expect an offer in the $130K-$150K range. The midpoint of the posted range is your realistic target, not the top. Only candidates with competing offers, rare skills, or perfect role fit land above the midpoint.</p>
    <p><strong>Use the survey data as your anchor.</strong> When the recruiter asks "what are you looking for?", cite the GTME Report median ($135K) as a starting point and explain why your specific skills, experience, and location justify above-median comp. Data-backed anchors are stronger than "I was thinking around $145K."</p>
    <p><strong>Push on the gap.</strong> If a company offers $125K for a role posted at $130K-$175K, point out that even the median posted salary is above their offer. Companies that post salary ranges are making a public commitment. Hold them to it.</p>
    <p><strong>Watch for total comp tricks.</strong> Some postings inflate the salary range by including estimated bonus, equity, or benefits value. If the posted range is $150K-$200K but includes "$30K estimated equity," the actual cash compensation is lower. Always clarify whether the posted range is base salary or total comp.</p>

    <h2>Global vs US Gap</h2>
    <p>The posted-vs-actual gap is sharper outside the US. Non-US postings may overstate salaries by 20-30% because US-headquartered companies post US salary ranges for roles that will be filled globally.</p>
    <p>A posting from a San Francisco company listing "$130K-$175K" for a "remote" GTM Engineer role might result in a $90K offer for a candidate in Portugal or a $70K offer for someone in India. The company posted US ranges for compliance or attraction purposes, but the actual offer reflects geographic adjustment.</p>
    <p>If you're outside the US applying to US-posted roles, ask about location-based pay adjustments early in the process. Don't wait until the offer stage to discover that the posted range doesn't apply to your geography. Specifically ask: "Is this salary range location-adjusted, and if so, what range applies to my location?"</p>
    <p>For US-based candidates, the posted salary data is more reliable. The 10-15% posted-to-actual gap still applies, but at least the geography matches. Use posted ranges as a ceiling and the survey median as your baseline.</p>

{faq_html(faq_pairs)}
{salary_related_links("posted-vs-actual", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly salary data and job market updates.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/posted-vs-actual/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/posted-vs-actual/index.html", page)
    print(f"  Built: salary/posted-vs-actual/index.html")


# ---------------------------------------------------------------------------
# Meta file generators
# ---------------------------------------------------------------------------

def build_sitemap():
    urls = ""
    for page_path in ALL_PAGES:
        clean = page_path.replace("index.html", "")
        if not clean.startswith("/"):
            clean = "/" + clean
        if not clean.endswith("/"):
            clean += "/"
        if clean == "//":
            clean = "/"
        urls += f"  <url>\n    <loc>{SITE_URL}{clean}</loc>\n    <lastmod>{BUILD_DATE}</lastmod>\n  </url>\n"

    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"  Built: sitemap.xml ({len(ALL_PAGES)} URLs)")


def build_robots():
    content = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Built: robots.txt")


# ---------------------------------------------------------------------------
# Content standards validator
# ---------------------------------------------------------------------------

def validate_pages():
    warnings = []
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            filepath = os.path.join(root, fname)
            rel = os.path.relpath(filepath, OUTPUT_DIR)
            with open(filepath, "r", encoding="utf-8") as f:
                html = f.read()

            title_match = re.search(r"<title>(.*?)</title>", html)
            if title_match:
                title_text = title_match.group(1)
                tlen = len(title_text)
                if tlen < 50 or tlen > 60:
                    warnings.append(f"{rel}: title length {tlen} (want 50-60): \"{title_text}\"")
            else:
                warnings.append(f"{rel}: missing <title> tag")

            desc_match = re.search(r'<meta name="description" content="(.*?)"', html)
            if desc_match:
                desc_text = desc_match.group(1)
                dlen = len(desc_text)
                if dlen < 150 or dlen > 158:
                    warnings.append(f"{rel}: description length {dlen} (want 150-158): \"{desc_text}\"")
            else:
                warnings.append(f"{rel}: missing meta description")

            h1_count = len(re.findall(r"<h1[^>]*>", html))
            if h1_count != 1:
                warnings.append(f"{rel}: found {h1_count} H1 tags (want exactly 1)")

            if "\u2014" in html:
                warnings.append(f"{rel}: contains em-dash character (U+2014)")

            html_lower = html.lower()
            for word in BANNED_WORDS:
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

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    print("  Cleaned output/")

    shutil.copytree(ASSETS_DIR, os.path.join(OUTPUT_DIR, "assets"))
    print("  Copied assets/")

    print("\n  Building core pages...")
    build_homepage()
    build_about_page()
    build_newsletter_page()
    build_privacy_page()
    build_terms_page()
    build_404_page()

    print("\n  Building salary pages...")
    build_salary_index()
    build_salary_seniority_pages()
    build_salary_location_pages()
    build_salary_stage_pages()
    build_salary_vs_pages()
    build_salary_calculator()
    build_salary_methodology()
    build_salary_coding_premium()
    build_salary_company_size()
    build_salary_funding_stage()
    build_salary_experience()
    build_salary_age()
    build_salary_bonus()
    build_salary_equity()
    build_salary_us_vs_global()
    build_salary_posted_vs_actual()

    print("\n  Building meta files...")
    build_sitemap()
    build_robots()

    with open(os.path.join(OUTPUT_DIR, "CNAME"), "w", encoding="utf-8") as f:
        f.write("gtmepulse.com\n")
    print("  Built: CNAME")

    validate_pages()

    print(f"\n=== Build complete: {len(ALL_PAGES)} pages ===")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Preview: cd output && python3 -m http.server 8090")


if __name__ == "__main__":
    main()
