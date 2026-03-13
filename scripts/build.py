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
        links.append(("/salary/equity/", "Equity: 68% Have Nothing"))
        links.append(("/salary/agency-fees/", "Agency Fee Guide"))
        links.append(("/salary/us-vs-global/", "US vs Global Pay"))

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

    <h2>More Salary Data</h2>
    <div class="salary-index-grid">
        <a href="/salary/coding-premium/" class="salary-index-card">
            <h3>Coding Premium</h3>
            <div class="card-range">$45K Gap</div>
            <p>How coding skills affect GTM Engineer pay</p>
        </a>
        <a href="/salary/equity/" class="salary-index-card">
            <h3>Equity Data</h3>
            <div class="card-range">68% Nothing</div>
            <p>Equity ownership by funding stage</p>
        </a>
        <a href="/salary/us-vs-global/" class="salary-index-card">
            <h3>US vs Global</h3>
            <div class="card-range">$135K vs $75K</div>
            <p>Geographic salary comparison</p>
        </a>
        <a href="/salary/posted-vs-actual/" class="salary-index-card">
            <h3>Posted vs Actual</h3>
            <div class="card-range">$150K vs $135K</div>
            <p>Job listing salaries vs reported pay</p>
        </a>
        <a href="/salary/agency-fees/" class="salary-index-card">
            <h3>Agency Fees</h3>
            <div class="card-range">$5K&#8209;$8K/mo</div>
            <p>GTM Engineering agency rate guide</p>
        </a>
        <a href="/salary/agency-fees-by-region/" class="salary-index-card">
            <h3>Fees by Region</h3>
            <div class="card-range">US to APAC</div>
            <p>Regional agency pricing comparison</p>
        </a>
        <a href="/salary/seed-vs-enterprise/" class="salary-index-card">
            <h3>Seed vs Enterprise</h3>
            <div class="card-range">Equity Trade-Offs</div>
            <p>Compensation by company stage</p>
        </a>
        <a href="/salary/company-size/" class="salary-index-card">
            <h3>By Company Size</h3>
            <div class="card-range">201&#8209;1K Best</div>
            <p>Salary by employee count</p>
        </a>
        <a href="/salary/funding-stage/" class="salary-index-card">
            <h3>By Funding Stage</h3>
            <div class="card-range">$120K&#8209;$200K</div>
            <p>Pay across the funding spectrum</p>
        </a>
        <a href="/salary/by-experience/" class="salary-index-card">
            <h3>By Experience</h3>
            <div class="card-range">$105K&#8209;$195K+</div>
            <p>Compensation by years in role</p>
        </a>
        <a href="/salary/by-age/" class="salary-index-card">
            <h3>By Age</h3>
            <div class="card-range">Median Age 25</div>
            <p>Salary across age brackets</p>
        </a>
        <a href="/salary/bonus/" class="salary-index-card">
            <h3>Bonus Data</h3>
            <div class="card-range">51% Get One</div>
            <p>Bonus participation and structure</p>
        </a>
    </div>

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


def build_salary_agency_fees():
    """Agency fee guide: $5K-$8K/mo median."""
    title = "GTM Engineering Agency Fees: Rate Guide"
    description = (
        "GTM Engineering agency fees range from $1K to $33K per month with a $5K-$8K median."
        " Pricing models, client counts, and retention data. GTME Report 2026."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Agency Fees", None)]
    bc_html = breadcrumb_html(crumbs)

    # Custom stats block for agency data
    agency_stats = '''<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">$5K&#8209;$8K</span>
        <span class="stat-label">Monthly Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$1K&#8209;$33K</span>
        <span class="stat-label">Full Range</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">47%</span>
        <span class="stat-label">&lt;5 Clients</span>
    </div>
</div>'''

    faq_pairs = [
        ("How much do GTM Engineering agencies charge?",
         "The median GTM Engineering agency charges $5K-$8K per month on a retainer basis. The full range spans $1K to $33K per month, depending on scope, specialization, and client size. Monthly retainer is the most common pricing model."),
        ("What pricing model should a GTM Engineering agency use?",
         "Monthly retainer is the most common and provides predictable revenue. Hybrid models (retainer plus performance bonus) are second. Project-based pricing works for one-time builds like CRM migrations or enrichment pipeline setup. Pay-per-outcome is rare and harder to scope."),
        ("How many clients do GTM Engineering agencies typically have?",
         "47% of agencies have fewer than 5 clients. 33% have 5-10 clients. Most agencies are small operations, often 1-3 people, serving a focused client base with deep engagement. The boutique model dominates."),
        ("How long do GTM Engineering agency engagements last?",
         "44% of engagements last 3-6 months. 24% last 6-12 months. Short-term project work is less common. Most clients need ongoing pipeline optimization, data maintenance, and system iteration, which favors longer retainer relationships."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Agency Data</div>
        <h1>GTM Engineering Agency Fees Guide</h1>
        <p>What agencies charge, how they price, and what engagement models work. First real data on GTM Engineering agency economics.</p>
    </div>
</section>
{agency_stats}
<div class="salary-content">
    <h2>Agency Fee Overview</h2>
    <p>Monthly fees for GTM Engineering agency work range from $1K to $33K, with the median sitting at $5K-$8K per month. This is the first real data on what GTM Engineering agencies charge, sourced from the State of GTME Report 2026.</p>
    <p>The wide range reflects the diversity of the market. At the $1K-$3K end, you'll find freelancers and offshore operators handling basic Clay table builds and data enrichment tasks. At the $8K-$15K end, specialized agencies run complete outbound operations: strategy, data infrastructure, sequencing, CRM integration, and reporting. Above $15K, you're looking at enterprise-level engagements with multi-channel orchestration and custom tooling.</p>
    <p>The $5K-$8K median is the sweet spot for most agencies. It's high enough to sustain a small team (1-3 people), low enough that mid-market SaaS companies can justify the spend, and aligned with the value a competent GTM Engineer delivers: typically 50-200 qualified pipeline meetings per quarter.</p>

    <h2>Pricing Models</h2>
    <p>Four pricing models exist in GTM Engineering agency work. Monthly retainer dominates.</p>
    <p><strong>Monthly retainer (most common).</strong> Fixed monthly fee for a defined scope of work. Includes ongoing enrichment pipeline management, outbound sequence optimization, CRM data maintenance, and reporting. Clients like predictability. Agencies like recurring revenue. The alignment works.</p>
    <p><strong>Hybrid: retainer plus performance (second most common).</strong> A base retainer ($3K-$5K) plus performance bonuses tied to pipeline generated or meetings booked. This aligns incentives: the agency earns more when they deliver more. The challenge is defining and measuring the performance metrics clearly enough that both sides agree on what counts.</p>
    <p><strong>Project-based (12 respondents).</strong> One-time fee for a defined deliverable: build a Clay enrichment pipeline, set up an outbound sequencing system, migrate CRM data, or create a reporting dashboard. Typical project fees range from $5K to $25K depending on complexity. Good for companies that want to build internal capability after the project ends.</p>
    <p><strong>Pay-per-outcome (4 respondents).</strong> Fee per qualified meeting booked, per lead enriched, or per pipeline dollar generated. Rare because it's hard to scope and puts all the risk on the agency. Works best when the agency has high confidence in the client's ICP and market, and when the attribution model is clean.</p>

    <h2>Client Count and Retention</h2>
    <p>47% of GTM Engineering agencies serve fewer than 5 clients at any given time. 33% serve 5-10 clients. Only 20% serve more than 10 clients simultaneously.</p>
    <p>This boutique model is driven by the depth of engagement. GTM Engineering isn't a templated service you can scale across dozens of clients with a playbook. Each client has a unique ICP, tech stack, sales process, and data quality profile. Doing the work well requires deep context that takes weeks to build.</p>
    <p>Retention data tells a similar story. 44% of engagements last 3-6 months. 24% last 6-12 months. The 3-6 month range represents the typical "prove it works" window: the agency builds the pipeline infrastructure, demonstrates results, and either transitions to a longer engagement or hands off to an internal hire.</p>
    <p>The 6-12 month engagements tend to be the most profitable for agencies. The ramp-up cost is amortized over a longer period, the agency has deep context on the client's business, and the work shifts from building systems to optimizing them, which is more efficient.</p>

    <h2>Setting Your Rates</h2>
    <p>If you're starting a GTM Engineering agency, the $5K-$8K median is your benchmark. Here's how to think about where to price within that range.</p>
    <p><strong>Start at $5K/month for your first 2-3 clients.</strong> You need case studies and testimonials more than you need maximum revenue. A $5K retainer from a grateful client who will provide a reference is worth more than a $8K retainer from a client who's lukewarm on your work.</p>
    <p><strong>Charge more for specialization.</strong> Fintech, cybersecurity, healthcare, and other regulated industries command a 20-50% premium. If you can navigate HIPAA compliance in outbound messaging or understand the nuances of selling to CISOs, charge for that expertise. Generalist agencies compete on price. Specialists compete on knowledge.</p>
    <p><strong>Charge more for technical depth.</strong> If you're writing custom Python scripts, building API integrations from scratch, or creating proprietary enrichment waterfalls that combine 5+ data sources, you're providing engineering work, not operations work. Price accordingly. $8K-$12K for technically deep engagements is reasonable.</p>
    <p><strong>Build in a price escalation path.</strong> Start at $5K/month. After 3 months with demonstrated results, raise to $6K-$7K. After 6 months, raise to $8K+. Clients who are seeing pipeline results won't balk at a 20% increase when you've proven the ROI.</p>

    <h2>Monthly vs Project vs Performance</h2>
    <p>Each model has trade-offs. Choose based on your risk tolerance and the client's needs.</p>
    <p><strong>Monthly retainer</strong> gives you predictable revenue and the ability to plan capacity. The downside: clients may expect constant availability and scope creep is real. Define the scope tightly: X enrichment pipelines maintained, Y sequences running, Z reporting cadence. Everything outside that scope is a change order.</p>
    <p><strong>Project-based</strong> works for one-time builds where the deliverable is clear. The upside: higher per-hour effective rate (a $15K project completed in 40 hours is $375/hour). The downside: feast-or-famine revenue and constant sales effort to fill the pipeline with new projects.</p>
    <p><strong>Performance-based</strong> aligns incentives perfectly but puts you at risk. If the client's product doesn't sell, or their sales team can't close the meetings you generate, your revenue suffers even if your work is excellent. Only use performance pricing when you have high confidence in the client's ability to convert the pipeline you create.</p>

{faq_html(faq_pairs)}
{salary_related_links("agency-fees", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Weekly GTM Engineering agency and salary data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/agency-fees/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/agency-fees/index.html", page)
    print(f"  Built: salary/agency-fees/index.html")


def build_salary_agency_fees_region():
    """Agency fees by region: US premium, APAC $3K, MEA $4K median."""
    title = "GTM Engineering Agency Fees by Region"
    description = (
        "GTM Engineering agency fees vary by region. US commands the highest rates."
        " APAC median $3K/mo, MEA $4K/mo. Regional pricing from GTME Report 2026."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Agency Fees by Region", None)]
    bc_html = breadcrumb_html(crumbs)

    region_stats = '''<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">US</span>
        <span class="stat-label">Highest Rates</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$3K/mo</span>
        <span class="stat-label">APAC Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$4K/mo</span>
        <span class="stat-label">MEA Median</span>
    </div>
</div>'''

    faq_pairs = [
        ("Which region charges the most for GTM Engineering agency work?",
         "US-based agencies charge the highest rates, with typical retainers of $5K-$12K per month. Europe follows at $4K-$8K. APAC and MEA agencies charge significantly less at $3K-$4K median, reflecting lower labor costs and different market dynamics."),
        ("Should a non-US agency match US pricing?",
         "Not necessarily. Non-US agencies serving US clients can charge 60-80% of US rates and still maintain strong margins. Matching full US rates requires US-level expertise, US time zone availability, and a track record with US companies. Start below US rates and increase as you build references."),
        ("Is there an arbitrage opportunity for APAC agencies serving US clients?",
         "Yes. An APAC agency charging $4K-$6K per month for work a US agency charges $8K-$12K for is competitive on price while earning well above local market rates. The margin is compelling if you can deliver US-quality work at APAC labor costs. Time zone overlap is the main challenge."),
        ("What markets are growing fastest for GTM Engineering agencies?",
         "India, Israel, and the UAE are growing fastest as GTM Engineering agency markets. India provides cost-effective services to US and European clients. Israel's dense startup ecosystem creates local demand. The UAE is emerging as a hub for MEA-region agency work, particularly serving Saudi and Gulf-state companies."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Regional Analysis</div>
        <h1>GTM Engineering Agency Fees by Region</h1>
        <p>How agency pricing varies across US, Europe, APAC, MEA, and LATAM markets.</p>
    </div>
</section>
{region_stats}
<div class="salary-content">
    <h2>Regional Fee Differences</h2>
    <p>GTM Engineering agency fees vary dramatically by geography. US agencies charge the most, followed by Europe. APAC and MEA are 40-60% cheaper. LATAM is still emerging with limited data.</p>
    <p>The gap reflects three factors: labor costs, client expectations, and market maturity. US agencies employ US-based (or US-rate) talent, serve clients accustomed to premium pricing, and operate in the most mature GTM Engineering market. Non-US agencies often deliver comparable work at lower rates because their cost structure allows it.</p>
    <p>For agencies, the geographic arbitrage creates strategic options. For clients, it creates procurement decisions. Understanding regional pricing helps both sides find the right fit.</p>

    <h2>US: The Premium Market</h2>
    <p>US GTM Engineering agencies charge $5K-$12K per month for standard retainer engagements. Specialized agencies (fintech, cybersecurity, enterprise) command $10K-$20K+. The US market benefits from proximity to 58% of all GTM Engineering practitioners, the densest concentration of B2B SaaS companies, and clients who understand the value of the function.</p>
    <p>Higher rates reflect higher costs. A US-based GTM Engineer earning $135K in salary costs an agency $170K-$200K when you add benefits, taxes, and overhead. At $8K/month per client with 4 clients per engineer, the math works but the margins are moderate (30-40%).</p>
    <p>US agencies also benefit from time zone alignment with the majority of clients, in-person meeting capability for enterprise deals, and the credibility that comes from being US-based when selling to US companies. For US clients with security concerns or data sovereignty requirements, a US-based agency may be the only option.</p>

    <h2>Europe: Competitive Rates, Growing Market</h2>
    <p>European GTM Engineering agencies charge $4K-$8K per month, roughly 20-30% below US rates. The UK leads European agency pricing at $5K-$9K. Germany and the Netherlands follow at $4K-$7K. Southern and Eastern Europe are more affordable at $3K-$5K.</p>
    <p>European agencies increasingly serve US clients, competing on price while delivering comparable quality. A London-based agency charging $6K/month is 25% cheaper than a US equivalent and operates in an overlapping time zone (4-6 hours difference with US East Coast). For US companies comfortable with remote collaboration, European agencies offer strong value.</p>
    <p>The European agency market is growing faster than any other region. As European SaaS companies mature and US companies expand their remote hiring, demand for European GTM Engineering services is climbing. Agencies that establish themselves now will benefit from the growth curve.</p>

    <h2>APAC: $3K Median</h2>
    <p>APAC GTM Engineering agencies charge a median of $3K per month. India dominates the market, with agencies offering retainers from $1.5K-$5K. Australia is the outlier, with rates closer to European levels ($5K-$8K).</p>
    <p>At $3K/month, the unit economics for APAC agencies are compelling. A GTM Engineer in India earning $25K-$40K annually can serve 3-4 clients, generating $108K-$144K in annual revenue per person. The margin is substantial, even with overhead for management, tools, and business development.</p>
    <p>The challenge for APAC agencies is perception. US and European clients may discount APAC providers on quality assumptions. The agencies that break through invest heavily in case studies, US-based account managers, and delivering measurably better results than what the client could achieve in-house. Once the results are proven, the pricing advantage becomes a moat.</p>
    <p>Time zone is the operational friction. APAC to US requires either night-shift work for the agency team or asynchronous workflows. Agencies that solve this (dedicated night-shift teams, or focusing on European clients in closer time zones) do better than those that treat it as a minor inconvenience.</p>

    <h2>MEA: $4K Median</h2>
    <p>Middle East and Africa GTM Engineering agencies charge a median of $4K per month. Israel leads the region with sophisticated agencies at $5K-$10K. The UAE and South Africa are emerging markets with rates between $3K-$6K.</p>
    <p>Israel's agency market benefits from the country's dense startup ecosystem. Israeli GTM Engineers understand B2B SaaS deeply because they've grown up in the market. Many Israeli agencies serve US clients, leveraging cultural familiarity and English proficiency alongside competitive pricing.</p>
    <p>The UAE is investing heavily in becoming a tech hub. Dubai and Abu Dhabi are attracting GTM Engineering talent from across the Middle East and South Asia. Agencies based in the UAE serve both local companies (particularly in fintech and e-commerce) and international clients looking for MEA-region coverage.</p>
    <p>South Africa has a growing freelance GTM Engineering community, benefiting from English proficiency, favorable time zone overlap with Europe, and competitive pricing. The market is small but growing, with agencies targeting UK and European clients.</p>

    <h2>Arbitrage Opportunities</h2>
    <p>The regional pricing gap creates clear arbitrage opportunities for non-US agencies. The playbook is straightforward: deliver US-quality work at below-US rates.</p>
    <p>An APAC agency charging $5K/month for work a US agency charges $8K-$10K for saves the client $36K-$60K annually. If the work quality is comparable, the value proposition is obvious. The agency earns above local market rates while undercutting US competitors by 40-50%.</p>
    <p>The growth model for non-US agencies targeting US clients follows a common pattern. Start with 1-2 US clients at a discounted rate to build references. Deliver measurable results (pipeline generated, meetings booked, enrichment coverage). Collect case studies and testimonials. Raise rates toward 70-80% of US levels as the track record builds.</p>
    <p>This arbitrage won't last forever. As the global talent pool expands and more agencies compete internationally, rates will converge somewhat. But the structural cost advantages (lower cost of living, lower salary expectations in APAC and MEA) will maintain a meaningful pricing gap for years. Agencies that establish themselves in the US market now will have a durable advantage.</p>

{faq_html(faq_pairs)}
{salary_related_links("agency-fees-by-region", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Global GTM Engineering salary and agency data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/agency-fees-by-region/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/agency-fees-by-region/index.html", page)
    print(f"  Built: salary/agency-fees-by-region/index.html")


def build_salary_seed_vs_enterprise():
    """Seed vs enterprise: salary + equity trade-offs by funding stage."""
    title = "GTM Engineer Pay: Seed vs Enterprise (2026)"
    description = (
        "GTM Engineer compensation trade-offs by company stage. Seed: lower base, 29% equity."
        " Enterprise: higher base, RSUs. Series A-B is the equity dead zone."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Salary Data", "/salary/"), ("Seed vs Enterprise", None)]
    bc_html = breadcrumb_html(crumbs)

    stage_stats = '''<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">29%</span>
        <span class="stat-label">Pre-Seed Equity</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">9%</span>
        <span class="stat-label">Series A Equity</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">33%</span>
        <span class="stat-label">Public/Exited Equity</span>
    </div>
</div>'''

    faq_pairs = [
        ("Should a GTM Engineer join a seed startup or an enterprise company?",
         "It depends on your priorities. Seed startups offer lower base salary ($105K-$145K) but meaningful equity (29% chance at Pre-Seed). Enterprise offers higher base ($160K-$250K) and RSU programs. Series A-B is the worst for total comp optimization: lower equity than seed, lower base than enterprise."),
        ("What's the typical GTM Engineer salary at a seed-stage company?",
         "Seed-stage GTM Engineers earn $105K-$145K base salary. At Pre-Seed, 29% receive meaningful equity grants (0.1-0.5%). By Series A, the equity percentage drops to 9% but the base may climb to $120K-$175K. The salary trade-off is real but so is the equity potential at the earliest stages."),
        ("How much equity should a GTM Engineer expect at a startup?",
         "At Pre-Seed: 0.1-0.5% is common. At Seed: 0.05-0.25%. At Series A: 0.01-0.05%. Each subsequent round dilutes existing grants. The State of GTME Report 2026 shows only 29% of Pre-Seed and 9% of Series A hires get meaningful grants. Know your numbers before negotiating."),
        ("Is the RSU program at a public company worth more than startup equity?",
         "For most GTM Engineers, yes. RSUs at a public company have a known market value, vest on a schedule, and are liquid immediately. Startup equity is illiquid, subject to dilution, and worth zero if the company doesn't exit above the preference stack. 33.3% of GTM Engineers at public companies receive meaningful RSUs."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Stage Comparison</div>
        <h1>GTM Engineer Pay: Seed vs Enterprise</h1>
        <p>The salary and equity trade-offs at every company stage, from Pre-Seed to public.</p>
    </div>
</section>
{stage_stats}
<div class="salary-content">
    <h2>The Fundamental Trade-Off</h2>
    <p>Every GTM Engineer faces a compensation decision that maps directly to company stage. Seed: lower base salary ($105K-$145K range), higher equity potential (29% at Pre-Seed get meaningful grants). Enterprise: higher base ($160K-$250K), RSU programs, but smaller percentage ownership.</p>
    <p>The middle ground, Series A through Series B, is where most GTM Engineers land. And it's the worst stage for total comp optimization. Companies at these stages have raised enough money to pay competitive base salaries but not enough to offer generous equity. The option grants are small, the dilution from future rounds is certain, and the path to liquidity is long.</p>
    <p>Understanding this trade-off matters because your stage choice is the single largest lever you have over lifetime earnings as a GTM Engineer. A $20K annual base salary sacrifice at Pre-Seed, if the company succeeds, could be worth $500K-$1M+ in equity. But "if the company succeeds" is doing a lot of heavy lifting in that sentence.</p>

    <h2>Seed Stage: Build Everything, Own a Piece</h2>
    <p>At Pre-Seed and Seed, you're often the first or second hire touching go-to-market automation. There's no existing playbook, no CRM configuration to inherit, no enrichment pipeline humming in the background. You're building the entire outbound machine from a blank canvas.</p>
    <p>Base salary reflects the stage: $95K-$150K is the typical range, with most Seed-stage GTM Engineers earning $105K-$145K. That's $20K-$40K below what a comparable role pays at a growth-stage company. The delta is supposed to be covered by equity.</p>
    <p>The State of GTME Report 2026 data on equity is revealing. At Pre-Seed, 29% of GTM Engineers hold meaningful equity (0.1-0.5% of the company). That's the highest rate of any stage. By the time the company reaches Series A, only 9% of GTM Engineering hires get meaningful grants. If equity is your play, Pre-Seed is when to make it.</p>
    <p>The risk profile is straightforward. 90%+ of Pre-Seed companies fail or exit at values too low for your equity to matter after the preference stack. The $30K/year you're sacrificing in base salary ($90K over 3 years) is real money. The equity is a lottery ticket with better-than-random odds but still long odds.</p>
    <p>Who should take the bet? Engineers early in their career with low burn rates, high risk tolerance, and genuine conviction in the company. If you'd be financially stressed by the lower base, or if you're joining the startup because it was the first offer you got rather than a deliberate bet, the risk/reward doesn't work.</p>

    <h2>Series A-B: The Equity Desert</h2>
    <p>Series A drops to 9% meaningful equity. Series B is similar. This is the dead zone for GTM Engineer compensation optimization.</p>
    <p>At Series A ($5M-$15M raised), the company has enough capital to pay competitive base salaries. There's no financial pressure to compensate with equity. The founding team and early employees have already claimed the lion's share of the option pool. Your grant of 0.01-0.05% will be diluted by at least two more rounds before any exit.</p>
    <p>Do the math on a typical Series A equity offer. 0.03% of a company currently valued at $50M = $15K on paper. After two rounds of 30% dilution: ~$7.4K. And that assumes the company exits at its current valuation, which it likely won't for 5-7 years. The present value of that equity is close to zero.</p>
    <p>Series B is similar but with higher base salaries ($130K-$175K median). The company is more de-risked, the equity is more diluted, and your grant is even smaller. The calculus is: take the higher base, treat the equity as a bonus if the company succeeds, and don't factor it into your compensation expectations.</p>
    <p>The tactical advice for Series A-B GTM Engineers: negotiate hard on base salary, push for a meaningful bonus structure (15-25% of base tied to pipeline metrics you control), and accept that equity at this stage is a retention tool, not a wealth-building mechanism.</p>

    <h2>Enterprise and Public: Stability Premium</h2>
    <p>Enterprise companies ($100M+ ARR) and public companies offer the highest base salaries for GTM Engineers: $160K-$250K. The State of GTME Report 2026 shows 33.3% of GTM Engineers at exited or public companies receive meaningful equity through RSU programs.</p>
    <p>RSUs at a public company are fundamentally different from startup equity. They have a known market price, they vest on a schedule (typically 4 years with a 1-year cliff), and they're liquid immediately upon vesting. A $75K annual RSU grant at a company trading at $50/share gives you real, spendable money every quarter.</p>
    <p>The trade-off: less autonomy, more process, and a narrower role scope. At a 5,000-person company, you're not building the GTM function from scratch. You're optimizing a piece of it. The enrichment pipeline already exists; you're improving its accuracy. The outbound sequences are running; you're increasing conversion. The work is important but less entrepreneurial.</p>
    <p>For many GTM Engineers, the enterprise path is the right one. Predictable comp, clear promotion ladders, strong benefits, and RSUs that vest into your brokerage account like clockwork. The thrill of building from zero is replaced by the comfort of building at scale.</p>

    <h2>Optimizing Total Compensation by Stage</h2>
    <p>Here's the tactical framework for maximizing total comp at each stage.</p>
    <p><strong>If you want equity upside: go Pre-Seed.</strong> Accept the lower base ($100K-$130K), negotiate for 0.2-0.5% equity, and make sure you understand the cap table, the liquidation preferences, and the exercise window. You're making a calculated bet. Make it with your eyes open.</p>
    <p><strong>If you want max base salary: go growth or enterprise.</strong> Growth-stage companies ($160K-$235K median) and enterprise ($160K-$250K) pay the most in cash. RSUs at public companies add another $50K-$100K in annual comp. This is where you maximize current earnings and financial stability.</p>
    <p><strong>If you want the best risk-adjusted total comp: go growth stage.</strong> Series C-D companies ($160K-$235K base) offer strong base salaries, equity with real expected value (the company is de-risked but hasn't IPO'd yet), and enough autonomy to keep the work interesting. The equity won't be life-changing, but it has a meaningful expected value.</p>
    <p><strong>Avoid Series A-B for compensation optimization.</strong> The base is good but not great. The equity is too diluted to matter. The bonus structures are often immature. If you join a Series A-B company, do it because you love the product, the team, or the learning opportunity, not because of the comp package.</p>

{faq_html(faq_pairs)}
{salary_related_links("seed-vs-enterprise", "analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly compensation data by company stage.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/seed-vs-enterprise/",
        body_content=body, active_path="/salary/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("salary/seed-vs-enterprise/index.html", page)
    print(f"  Built: salary/seed-vs-enterprise/index.html")


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
# Career page helpers + generators
# ---------------------------------------------------------------------------

CAREER_PAGES = [
    {"slug": "how-to-become-gtm-engineer", "title": "How to Become a GTM Engineer"},
    {"slug": "operator-vs-engineer", "title": "Operator vs Engineer: The $45K Gap"},
    {"slug": "is-gtm-engineering-real-career", "title": "Is GTM Engineering a Real Career?"},
    {"slug": "job-market-analysis", "title": "Job Market: 5,205% Growth"},
    {"slug": "how-gtm-engineers-got-jobs", "title": "How GTM Engineers Got Their Jobs"},
    {"slug": "work-life-balance", "title": "Work-Life Balance Data"},
    {"slug": "demographics", "title": "Demographics: Age, Location, Data"},
    {"slug": "gtm-engineer-vs-revops", "title": "GTM Engineer vs RevOps Convergence"},
    {"slug": "do-you-need-to-code", "title": "Do You Need to Code? ($45K Premium)"},
    {"slug": "reporting-structure", "title": "Reporting Structure Data"},
    {"slug": "impact-measurement", "title": "How GTM Engineers Measure Impact"},
    {"slug": "skills-gap", "title": "Skills Gap: What Postings Want"},
]


def career_related_links(current_slug):
    """Generate related career page links (same pattern as salary_related_links)."""
    links = [("/careers/", "Career Guides Index")]
    for page in CAREER_PAGES:
        if page["slug"] != current_slug:
            links.append((f"/careers/{page['slug']}/", page["title"]))
    # Add salary cross-links
    links.append(("/salary/", "Salary Data Index"))
    links.append(("/salary/coding-premium/", "Coding Premium: $45K Gap"))
    links = links[:12]
    items = ""
    for href, label in links:
        items += f'<a href="{href}" class="related-link-card">{label}</a>\n'
    return f'''<section class="related-links">
    <h2>Related Career Guides</h2>
    <div class="related-links-grid">
        {items}
    </div>
</section>'''


def build_career_index():
    """Career landing page at /careers/ with card grid linking to all 12 career guides."""
    title = "GTM Engineer Career Guide 2026 - GTME Pulse"
    description = (
        "Career paths, job market data, and work-life balance for GTM Engineers."
        " Backed by survey data from 228 practitioners across 32 countries."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", None)]
    bc_html = breadcrumb_html(crumbs)

    cards = ""
    card_data = [
        ("how-to-become-gtm-engineer", "How to Become a GTM Engineer", "Self-taught paths, skills needed, and realistic timelines", "53% Self-Taught"),
        ("operator-vs-engineer", "Operator vs Engineer", "The $45K salary gap between low-code and technical paths", "$45K Gap"),
        ("is-gtm-engineering-real-career", "Is This a Real Career?", "Job posting data, salary benchmarks, and longevity analysis", "5,205% Growth"),
        ("job-market-analysis", "Job Market Analysis", "63 to 3,342 postings, top hiring countries, salary bands", "3,342 Postings"),
        ("how-gtm-engineers-got-jobs", "How GTMEs Got Their Jobs", "Entry paths: SDR, marketing ops, developer transitions, agencies", "121/228 Self-Taught"),
        ("work-life-balance", "Work-Life Balance", "Hours worked, agency vs in-house, remote patterns, burnout data", "60% Work 40&#8209;60hrs"),
        ("demographics", "Demographics", "Median age 25, Gen Z function, 32 countries, self-taught majority", "Median Age 25"),
        ("gtm-engineer-vs-revops", "GTME vs RevOps", "9.6% predict convergence, technical vs operational split, salary gap", "9.6% Converge"),
        ("do-you-need-to-code", "Do You Need to Code?", "Bimodal coding distribution, $45K premium, which languages matter", "$45K Premium"),
        ("reporting-structure", "Reporting Structure", "Sales and Marketing reporting lines, agency vs in-house, budget impact", "Sales #1 Report"),
        ("impact-measurement", "Impact Measurement", "Pipeline KPIs, attribution methods, proving ROI to leadership", "92% Track Meetings"),
        ("skills-gap", "Skills Gap Analysis", "Clay 84%, CRM 92%, Python and SQL demand vs practitioner supply", "84% Clay Required"),
    ]
    for slug, card_title, desc, stat in card_data:
        cards += f'''<a href="/careers/{slug}/" class="salary-index-card">
    <h3>{card_title}</h3>
    <div class="card-range">{stat}</div>
    <p>{desc}</p>
</a>
'''

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Intelligence</div>
        <h1>GTM Engineer Career Guides</h1>
        <p>Career paths, job market data, and compensation intelligence for GTM Engineers. Every number comes from the State of GTM Engineering Report 2026, a survey of 228 practitioners across 32 countries combined with analysis of 3,342 job postings.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">228</span>
        <span class="stat-label">Practitioners Surveyed</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">5,205%</span>
        <span class="stat-label">Job Posting Growth</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$135K</span>
        <span class="stat-label">Median Salary</span>
    </div>
</div>

<div class="salary-content">
    <h2>Career Guides</h2>
    <div class="salary-index-grid">
        {cards}
    </div>

    <h2>Agency &amp; Freelance</h2>
    <div class="salary-index-grid">
        <a href="/careers/agency-pricing/" class="salary-index-card">
            <h3>Agency Pricing Guide</h3>
            <div class="card-range">$5K&#8209;$8K/mo</div>
            <p>Median fees, pricing tiers, and value-based vs hourly rates</p>
        </a>
        <a href="/careers/start-gtm-engineering-agency/" class="salary-index-card">
            <h3>How to Start an Agency</h3>
            <div class="card-range">30% Are Agency</div>
            <p>Startup costs, first client, scaling from solo to team</p>
        </a>
        <a href="/careers/agency-vs-freelance/" class="salary-index-card">
            <h3>Agency vs Freelance</h3>
            <div class="card-range">2&#8209;3x Revenue Gap</div>
            <p>Revenue, overhead, and lifestyle comparison from 97 respondents</p>
        </a>
        <a href="/careers/client-retention/" class="salary-index-card">
            <h3>Client Retention Data</h3>
            <div class="card-range">44% at 3&#8209;6mo</div>
            <p>Engagement lengths, churn drivers, and retention strategies</p>
        </a>
        <a href="/careers/client-count/" class="salary-index-card">
            <h3>Client Count Analysis</h3>
            <div class="card-range">47% Have &lt;5</div>
            <p>Capacity planning, revenue math, quality vs quantity</p>
        </a>
        <a href="/careers/pricing-models/" class="salary-index-card">
            <h3>Pricing Models</h3>
            <div class="card-range">~70% Retainer</div>
            <p>Retainer, hybrid, project, and pay-per-lead comparison</p>
        </a>
        <a href="/careers/agency-fees-by-region-guide/" class="salary-index-card">
            <h3>Fees by Region Guide</h3>
            <div class="card-range">$3K&#8209;$8K Range</div>
            <p>Regional pricing strategy and cross-border arbitrage</p>
        </a>
        <a href="/careers/deliverability-practices/" class="salary-index-card">
            <h3>Deliverability Practices</h3>
            <div class="card-range">89.7% Rotate</div>
            <p>Domain rotation, warming, inbox management, common mistakes</p>
        </a>
    </div>

    <h2>Job Market</h2>
    <div class="salary-index-grid">
        <a href="/careers/job-growth/" class="salary-index-card">
            <h3>Job Growth: 5,205% Surge</h3>
            <div class="card-range">63&#8594;3,342</div>
            <p>From 63 postings to 3,342 in under two years. What is driving it.</p>
        </a>
        <a href="/careers/jobs-by-country/" class="salary-index-card">
            <h3>Jobs by Country</h3>
            <div class="card-range">32 Countries</div>
            <p>US 25.7%, India 17.4%, Spain 15.3%, UK 7.7%. Global breakdown.</p>
        </a>
        <a href="/careers/posted-vs-actual-salary/" class="salary-index-card">
            <h3>Posted vs Actual Salary</h3>
            <div class="card-range">$15K Gap</div>
            <p>Job postings say $150K. Practitioners report $135K. Why the gap.</p>
        </a>
        <a href="/careers/top-skills-in-postings/" class="salary-index-card">
            <h3>Top Skills in Postings</h3>
            <div class="card-range">84% Clay</div>
            <p>Clay, CRM, Python, SQL demand vs practitioner supply data.</p>
        </a>
        <a href="/careers/monthly-hiring-trends/" class="salary-index-card">
            <h3>Monthly Hiring Trends</h3>
            <div class="card-range">624 Dec Peak</div>
            <p>Month-by-month 2025 posting data. Q4 surge and seasonal patterns.</p>
        </a>
        <a href="/careers/salary-bands-by-location/" class="salary-index-card">
            <h3>Salary Bands by Location</h3>
            <div class="card-range">$128K&#8209;$175K</div>
            <p>US metro and international salary bands from 3,342 postings.</p>
        </a>
        <a href="/careers/india-gtm-engineering/" class="salary-index-card">
            <h3>India Market Analysis</h3>
            <div class="card-range">17.4% Share</div>
            <p>Bangalore, Mumbai, Delhi hubs. Agency opportunity and salary data.</p>
        </a>
        <a href="/careers/spain-europe-gtm-engineering/" class="salary-index-card">
            <h3>Spain &amp; Europe Market</h3>
            <div class="card-range">15.3% Spain</div>
            <p>Barcelona leads. UK 7.7%, Germany 5.2%. European salary analysis.</p>
        </a>
    </div>

    <h2>Why This Data Matters</h2>
    <p>GTM Engineering is the fastest-growing role in B2B SaaS. Job postings surged 5,205% between early 2024 and late 2025. But good career intelligence has been missing. Most "GTM Engineer career guides" are thinly researched blog posts from tool vendors trying to sell you something.</p>
    <p>These guides are different. Every stat is sourced from our survey of 228 working GTM Engineers, not job descriptions, not LinkedIn profiles, not vendor marketing. Real people doing real work, telling us what they earn, how they got hired, and how many hours they put in.</p>
    <p>Use these guides to make better career decisions, whether you're breaking into the field, choosing between the operator and engineer path, or negotiating your next raise.</p>
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/",
        body_content=body, active_path="/careers/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("careers/index.html", page)
    print(f"  Built: careers/index.html")


def build_career_how_to_become():
    """CAREER-01: How to become a GTM Engineer guide."""
    title = "How to Become a GTM Engineer: 2026 Guide"
    description = (
        "Step-by-step guide to becoming a GTM Engineer. 53% are self-taught."
        " Entry paths, skills needed, and realistic timelines from n=228 survey."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("How to Become", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("Do I need a degree to become a GTM Engineer?",
         "No. 53% of working GTM Engineers (121 out of 228 surveyed) are self-taught. The field values demonstrable skills over credentials. A strong Clay portfolio or automation project will get you further than a computer science degree in most interviews."),
        ("How long does it take to become a GTM Engineer?",
         "Most career switchers report reaching job-ready status in 3-6 months of focused learning. That means proficiency in Clay, at least one CRM (HubSpot or Salesforce), and ideally basic Python skills. Prior experience in SDR, marketing ops, or revenue ops shortens the timeline."),
        ("Are there GTM Engineer certifications worth getting?",
         "Clay University certification is the closest thing to a standard credential, and 84% of GTM Engineers use Clay. HubSpot and Salesforce certifications help too, especially for roles at companies using those CRMs. But portfolio projects matter more than certificates."),
        ("What's the best first job in GTM Engineering?",
         "Agency and freelance work is the most common entry point. 30% of GTM Engineers work at agencies or run their own consultancies. Agencies give you exposure to multiple stacks, rapid iteration, and portfolio-building opportunities that in-house roles at a single company can't match."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Guide</div>
        <h1>How to Become a GTM Engineer: 2026 Guide</h1>
        <p>The paths people take into GTM Engineering, the skills that matter, and how long it takes. Based on survey data from 228 working GTM Engineers.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">53%</span>
        <span class="stat-label">Self-Taught</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">84%</span>
        <span class="stat-label">Use Clay</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">92%</span>
        <span class="stat-label">Use a CRM Daily</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Self-Taught Majority</h2>
    <p>Here's the number that should give you confidence: 121 out of 228 GTM Engineers surveyed taught themselves the role. No bootcamp. No degree program. No formal training. They picked up Clay, learned to wire automations together, and figured out the rest on the job.</p>
    <p>That 53% figure is strikingly high compared to adjacent roles. In software engineering, self-taught developers represent maybe 15-20% of the workforce. In GTM Engineering, they're the majority. The field is young enough that there's no established pipeline from university to job. Everyone's making their own path.</p>
    <p>What did they learn first? The data points to three things: Clay (84% adoption rate), a CRM (92% use one daily, usually HubSpot or Salesforce), and some form of automation tool (Make, Zapier, or n8n). Master those three pillars and you're functional. Add Python and you're competitive.</p>

    <h2>Top Entry Paths</h2>
    <p>Five backgrounds feed most of the talent into GTM Engineering. Each one brings different strengths and different gaps to fill.</p>
    <h3>SDR / BDR Transition</h3>
    <p>Former SDRs and BDRs make up the largest single feeder group. They understand outbound prospecting, sequences, and pipeline generation because they've done it manually. The transition to GTM Engineering means automating what they used to do by hand. If you've spent months sending cold emails and manually enriching leads, you already understand the problem space. You just need the technical skills to build systems around it.</p>
    <p>The gap for SDR converts: most need to learn data tools beyond their CRM. Clay is the bridge. It looks familiar enough (spreadsheet-like) to be approachable, but powerful enough to replace entire manual workflows.</p>

    <h3>Marketing Ops Transition</h3>
    <p>Marketing ops people bring systematic thinking and CRM fluency. They've managed lead scoring, attribution models, and email campaigns. The shift to GTM Engineering means expanding from marketing-only workflows to full-funnel automation that spans enrichment, outbound, and pipeline management.</p>
    <p>Marketing ops converts typically have an easier time with the analytical side. They're used to measuring things. The growth edge is learning outbound sequencing tools and building enrichment pipelines.</p>

    <h3>Revenue Ops Transition</h3>
    <p>RevOps professionals already sit at the intersection of sales, marketing, and customer success data. They understand the full GTM motion. The transition is less about learning a new domain and more about shifting from strategic/analytical work to hands-on technical building.</p>
    <p>RevOps converts often have the broadest business context, which makes them effective at designing systems that serve the whole revenue team, not just one function.</p>

    <h3>Developer Transition</h3>
    <p>Developers who move into GTM Engineering bring the highest technical ceiling. They can write custom integrations, build API middleware, and automate at a level that no-code builders can't match. The <a href="/salary/coding-premium/">$45K coding premium</a> exists largely because of this group.</p>
    <p>The gap for developers: they often need to learn the GTM domain itself. Knowing Python is worthless if you don't understand why a multi-step enrichment waterfall matters, or how outbound sequences convert differently based on persona targeting.</p>

    <h3>Agency / Freelance Path</h3>
    <p>30% of GTM Engineers surveyed work at agencies or run freelance practices. This is the fastest path to building a portfolio. You work with multiple clients, build diverse systems, and accumulate references quickly. The tradeoff is longer hours and less stability than in-house roles.</p>

    <h2>The Skills That Matter</h2>
    <p>The survey data paints a clear picture of which skills working GTM Engineers use daily and which ones command a salary premium.</p>
    <p><strong>Clay (84% adoption):</strong> The center of gravity for the entire field. If you learn one tool, make it Clay. It's where enrichment, scoring, and prospecting workflows live. Clay proficiency is table stakes for most GTM Engineer roles.</p>
    <p><strong>CRM fluency (92%):</strong> HubSpot and Salesforce dominate. You need to understand objects, properties, workflows, and API access for at least one CRM. This is non-negotiable for in-house roles.</p>
    <p><strong>Python:</strong> The single highest-value technical skill. GTM Engineers who code earn roughly <a href="/salary/coding-premium/">$45K more</a> than those who don't. You don't need to be a software engineer. You need to write API calls, parse JSON, manipulate data with pandas, and build simple automations.</p>
    <p><strong>Automation platforms:</strong> Make (formerly Integromat) and n8n for visual workflow building. Zapier for simpler integrations. These tools connect everything in the stack when custom code isn't warranted.</p>
    <p><strong>SQL:</strong> Increasingly important as companies want GTM Engineers who can query data warehouses, build reporting, and do ad-hoc analysis beyond what the CRM provides natively.</p>

    <h2>Realistic Timeline: 3-6 Months to Job-Ready</h2>
    <p>Based on survey responses and job market data, here's what a focused learning path looks like.</p>
    <p><strong>Month 1:</strong> Learn Clay fundamentals. Build 3-5 enrichment tables. Understand waterfall enrichment, scoring, and Clay's HTTP action for API calls. Complete Clay University if available. This is your foundation.</p>
    <p><strong>Month 2:</strong> Add CRM depth. Set up a HubSpot sandbox or Salesforce developer org. Build workflows that sync data from Clay to CRM. Learn to create custom properties, deal pipelines, and automated task assignment. Connect an outbound tool (Instantly or Lemlist) to practice sequence building.</p>
    <p><strong>Month 3:</strong> Build a portfolio project. Create an end-to-end system: data enrichment in Clay, scoring logic, CRM sync, automated outbound sequence. Document it. This project becomes your interview talking point and your proof of competence.</p>
    <p><strong>Months 4-6:</strong> Learn Python basics (variables, loops, HTTP requests, JSON parsing). Build one script that automates something in your workflow. Start applying to roles or taking freelance clients. At this point you have enough skills to be productive from day one.</p>
    <p>Can you speed this up? Yes, if you're coming from a technical background. Developers can compress this to 4-6 weeks. Can it take longer? Yes, if you're learning part-time. But 6 months of focused effort gets most people to a hirable level.</p>

    <h2>First Job Strategies</h2>
    <p>The GTM Engineering job market favors demonstrable output over resumes. Three approaches work well for breaking in.</p>
    <p><strong>Build in public.</strong> Share Clay tables, automation screenshots, and workflow diagrams on LinkedIn. The GTM Engineering community is active there, and hiring managers notice people who show their work. One viral post about an interesting enrichment workflow can generate inbound recruiter interest.</p>
    <p><strong>Start at an agency.</strong> Agencies are always hiring because the work scales with client count. The pay might be lower initially, but you'll learn faster than anywhere else. Exposure to different stacks, industries, and problems in your first 6 months is worth more than a slightly higher salary at a single company.</p>
    <p><strong>Offer to build for free.</strong> Find a startup that's doing outbound manually and offer to build their first automated enrichment and sequencing system. One successful project with a real company is worth more than any certification. And if you deliver, they'll either hire you or refer you to someone who will.</p>
    <p>The <a href="/careers/how-gtm-engineers-got-jobs/">data on how GTM Engineers got hired</a> confirms these patterns. The role rewards builders. Show what you can build, and the opportunities follow.</p>
    <p>For compensation expectations as you enter the field, see our <a href="/salary/">salary data breakdown</a>. Junior GTM Engineers start in the $90K-$130K range, with the path to <a href="/careers/operator-vs-engineer/">$135K+ tied to technical depth</a>.</p>

{faq_html(faq_pairs)}
{career_related_links("how-to-become-gtm-engineer")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/how-to-become-gtm-engineer/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/how-to-become-gtm-engineer/index.html", page)
    print(f"  Built: careers/how-to-become-gtm-engineer/index.html")


def build_career_operator_vs_engineer():
    """CAREER-02: Operator vs Engineer bifurcation and $45K gap."""
    title = "GTM Operator vs Engineer: The $45K Gap"
    description = (
        "GTM Operators earn ~$90K. GTM Engineers earn ~$135K. The difference is coding."
        " Bimodal skill data from the State of GTME Report 2026 (n=228)."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Operator vs Engineer", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is the difference between a GTM Operator and a GTM Engineer?",
         "GTM Operators build workflows using no-code and low-code tools like Clay, Zapier, and HubSpot workflows. GTM Engineers do all of that plus write custom code (Python, SQL, API integrations) to extend and connect systems. The distinction shows up in both daily work and compensation."),
        ("Can a GTM Operator become a GTM Engineer?",
         "Yes. The most common transition path is learning Python over 3-6 months while continuing to work in your current operator role. Start by automating one manual task with code, then build from there. The coding premium data suggests this is the highest-ROI career investment in the field."),
        ("Which path pays more: operator or engineer?",
         "Engineers earn roughly $45K more at the median. Low-code operators cluster around $90K, while technical GTM Engineers earn $135K or more. At senior levels, the gap widens further, with senior operators around $120K and senior engineers clearing $195K."),
        ("What technical skills separate engineers from operators?",
         "Python is the primary differentiator. SQL is second. API integration skills (building custom webhooks, handling authentication flows, connecting disparate systems with code) round out the top three. Operators can use tools as they exist. Engineers can extend, customize, and connect tools in ways the tools weren't designed for."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Guide</div>
        <h1>GTM Operator vs GTM Engineer: The $45K Gap</h1>
        <p>Two paths diverged in GTM Engineering. The data shows where they lead, and what separates them.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">~$90K</span>
        <span class="stat-label">Operator Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">~$135K</span>
        <span class="stat-label">Engineer Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$45K</span>
        <span class="stat-label">Median Gap</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Two Modes of GTM Engineering</h2>
    <p>When 228 GTM Engineers rated their coding skills on a 1-10 scale, they didn't spread across the spectrum. They clustered at two extremes. A large group rated themselves 1-3 (no-code and low-code users). Another large group rated themselves 7-10 (developers and technical builders). The middle was nearly empty.</p>
    <p>This bimodal pattern defines the field. There are GTM Operators who build systems with Clay, Zapier, Make, and CRM-native automation. And there are GTM Engineers who do all of that plus write Python, SQL, and custom API integrations. Both groups do valuable work. The market prices them very differently.</p>
    <p>The State of GTME Report 2026 data is unambiguous: technical depth drives compensation more than job title, years of experience, or company size. Two people with the same "GTM Engineer" title, same company stage, same location, can be $45K apart in total comp based solely on whether they write code.</p>

    <h2>The Operator Path: Ceiling Around $90K</h2>
    <p>GTM Operators are the builders who work within existing tool interfaces. They're skilled at Clay table design, enrichment waterfalls, CRM workflow automation, and connecting tools through native integrations. This is real, productive work. A good operator can 10x an SDR team's output by building the right automation.</p>
    <p>The ceiling exists because operators depend on what tools offer out of the box. When Clay doesn't have a native integration, an operator gets stuck. When a CRM workflow needs custom logic beyond what the builder supports, an operator works around it. These workarounds are clever, but they limit scope.</p>
    <p>Operator comp data from the survey: median around $90K, with a range of $65K-$120K depending on seniority and location. The top of the operator range ($120K) is achievable with 3+ years of experience, strong Clay skills, and a specialization in a high-value vertical like fintech or cybersecurity.</p>
    <p>The demand for operators is strong and growing. Companies that are just adopting GTM Engineering need someone to build the foundational workflows. Not every team needs custom code. Many need someone who can make Clay, HubSpot, and Instantly work together reliably. That's the operator sweet spot.</p>

    <h2>The Engineer Path: Floor Around $135K</h2>
    <p>GTM Engineers write code. Python scripts for custom enrichment. SQL queries against data warehouses. API middleware that connects systems in ways no Zapier workflow can. They extend tools beyond their native capabilities, and that extension is where the premium lives.</p>
    <p>The floor is higher because technical GTMEs can solve problems that operators cannot. When a company needs a custom webhook handler, a multi-source enrichment pipeline that falls back across APIs, or a data quality system that runs nightly against the CRM, they need someone who codes. That scarcity commands a premium.</p>
    <p>Engineer comp data: median around $135K, with a range of $110K-$250K+ for senior and lead levels. The top end is reserved for people who combine deep technical skills with GTM domain knowledge. A developer who just knows Python won't earn $250K in this field. A developer who knows Python AND understands outbound sales motions, enrichment strategy, and pipeline architecture will.</p>
    <p>At senior levels the gap widens further. A senior operator might top out around $120K. A senior engineer clears $195K. The <a href="/salary/coding-premium/">coding premium analysis</a> breaks this down in detail.</p>

    <h2>Deciding Which Path Fits</h2>
    <p>The decision comes down to two questions: do you want to learn to code, and how much do you want to earn?</p>
    <p>If you're technically curious and motivated by compensation growth, the engineering path offers a clear ROI. Learning Python over 3-6 months could translate to a $30K-$45K salary increase within a year. That's better than almost any professional development investment.</p>
    <p>If you prefer working within tools, enjoy the visual building process, and are comfortable earning in the $90K-$120K range, the operator path is valid and in demand. Not everyone needs or wants to code. The work is meaningful, the jobs are plentiful, and the ceiling, while lower, still represents solid compensation for the skills involved.</p>
    <p>There's also a hybrid approach. Some GTM Engineers start as operators, learn Python incrementally, and gradually add technical projects to their portfolio. This slow transition lets you earn while you learn and reduces the risk of committing fully to a path that might not suit you.</p>

    <h2>The Market Signal</h2>
    <p>Job postings increasingly split the role. Companies post "GTM Operations Specialist" at $80K-$110K and "GTM Engineer" at $130K-$195K. Same team, same function, different comp bands. The split tracks directly to technical requirements in the job description.</p>
    <p>Listings that mention Python, SQL, or API integration in the requirements consistently post salary ranges 25-40% above listings that don't. Companies know they're paying for a different skill set, and they price accordingly.</p>
    <p>If you're evaluating offers, look at the technical requirements. A company that asks about your Clay experience but never mentions code is hiring for the operator band. A company that gives you a technical assessment or asks about your Python projects is hiring for the engineer band, and the comp will reflect it.</p>

    <h2>The Skills Bridge</h2>
    <p>Crossing from operator to engineer requires learning three things, roughly in this order:</p>
    <p><strong>Python fundamentals.</strong> Variables, loops, functions, HTTP requests, JSON parsing. Not computer science theory. Practical Python for data manipulation and API integration. Spend one month on this. Build scripts that solve problems in your current workflow.</p>
    <p><strong>API fluency.</strong> Understanding REST APIs, authentication (API keys, OAuth), request/response patterns, and error handling. This is the connective tissue of modern GTM stacks. Spend a month building integrations between tools that don't have native connectors.</p>
    <p><strong>SQL basics.</strong> SELECT, JOIN, WHERE, GROUP BY, and subqueries. Enough to query a data warehouse, pull CRM data, and build ad-hoc reports. Two weeks of focused practice gets you functional. You don't need to be a database administrator.</p>
    <p>Three to six months of consistent effort, applied to real projects in your daily work, gets you across the bridge. The <a href="/careers/how-to-become-gtm-engineer/">how to become a GTM Engineer guide</a> covers the full timeline in detail.</p>

{faq_html(faq_pairs)}
{career_related_links("operator-vs-engineer")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/operator-vs-engineer/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/operator-vs-engineer/index.html", page)
    print(f"  Built: careers/operator-vs-engineer/index.html")


def build_career_is_real():
    """CAREER-03: Is GTM Engineering a real career?"""
    title = "Is GTM Engineering a Real Career? (2026)"
    description = (
        "5,205% job posting growth. $135K median salary. 228 practitioners surveyed."
        " The data on whether GTM Engineering is a lasting career path."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Is It a Real Career?", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("Is GTM Engineering a stable long-term career?",
         "The data suggests yes. Job postings grew 5,205% between early 2024 and late 2025 (63 to 3,342). Companies aren't experimenting with GTM Engineers anymore. They're building permanent teams around the function. Median tenure in the survey was 1.5 years, which is short but reflects a field that barely existed before 2023."),
        ("Will AI replace GTM Engineers?",
         "AI is making GTM Engineers more productive, not replacing them. 228 surveyed practitioners report spending more time on strategy and system design as AI handles routine enrichment and copywriting tasks. The role is evolving toward AI-orchestration, which increases the value of people who can build and manage AI-powered workflows."),
        ("What's the career ceiling for a GTM Engineer?",
         "Lead and Staff GTM Engineers earn $180K-$250K+. Head of GTM Engineering and VP-level roles are emerging at growth-stage and enterprise companies. The career path extends from individual contributor through team lead to executive, though the executive layer is still forming."),
        ("Which companies are hiring GTM Engineers?",
         "Clay, Apollo, and other GTM tool vendors hire them. But most demand comes from B2B SaaS companies in fintech, cybersecurity, healthtech, and enterprise software that want to automate their outbound motion. Growth-stage companies (Series B to D) have the highest concentration of GTM Engineer roles."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Guide</div>
        <h1>Is GTM Engineering a Real Career?</h1>
        <p>Job market data, salary benchmarks, and practitioner survey results on whether GTM Engineering has staying power.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">5,205%</span>
        <span class="stat-label">Job Posting Growth</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$135K</span>
        <span class="stat-label">Median Salary</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">228</span>
        <span class="stat-label">Practitioners Surveyed</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Numbers Say Yes</h2>
    <p>In early 2024, there were 63 job postings with "GTM Engineer" or equivalent titles. By the end of 2025, there were 3,342. That's 5,205% growth in under two years. No other role in B2B SaaS comes close to that trajectory.</p>
    <p>But job posting growth alone doesn't make a career. Plenty of buzzy titles have spiked and disappeared. "Growth Hacker" peaked around 2015 and mostly vanished. "Revenue Hacker" never caught on at all. What makes GTM Engineering different?</p>
    <p>Three things: compensation, company investment, and structural necessity.</p>

    <h2>Compensation Is Real</h2>
    <p>The median salary for a GTM Engineer is $135K, according to our survey of 228 practitioners. That places it above Sales Development ($65K-$85K), on par with Marketing Operations ($110K-$140K), and competitive with Revenue Operations ($120K-$160K). Companies are paying real money for this role.</p>
    <p>Compensation data from <a href="/salary/">our full salary breakdown</a> shows clear seniority progressions. Junior GTM Engineers start at $90K-$130K. Mid-level hits $130K-$175K. Senior and Lead roles reach $180K-$250K+. This isn't a flat gig economy job. It has a compensation ladder that rewards growth.</p>
    <p>The <a href="/careers/operator-vs-engineer/">operator vs engineer split</a> adds another dimension. Technical GTMEs who code earn $45K more at the median than low-code operators. The field rewards skill depth, which is another signal of a maturing career, not a passing fad.</p>

    <h2>Company Investment Is Growing</h2>
    <p>The question used to be "should we hire a GTM Engineer?" Now it's "how many do we need?" Companies that experimented with one GTM Engineer in 2023 are building teams of 3-5 in 2025. That's a shift from novelty hire to core function.</p>
    <p>Clay's growth accelerated adoption, but the role has spread beyond the Clay ecosystem. Companies use GTM Engineers to manage enrichment pipelines across multiple tools, build custom outbound infrastructure, and connect sales and marketing data systems. The work exists independently of any single vendor.</p>
    <p>Funding matters too. When companies raise Series B and beyond, GTM Engineering is increasingly a line item in the hiring plan alongside product engineering and sales. VC-backed companies aren't staffing temporary experiments with $135K-salaried professionals. They're building around the function.</p>

    <h2>Structural Necessity</h2>
    <p>The reason GTM Engineering persists where "Growth Hacker" didn't: it fills a structural gap that other roles don't address.</p>
    <p>Sales ops manages CRM and reporting. Marketing ops manages campaigns and attribution. Revenue ops coordinates across both. But none of these roles build the technical outbound infrastructure that modern B2B sales requires: enrichment waterfalls, AI-powered prospecting, multi-source data pipelines, automated sequencing with personalization.</p>
    <p>Someone has to build those systems. Before 2023, companies hacked it together with part-time attention from various ops roles. The results were fragile and slow. GTM Engineers exist because the work is complex enough, technical enough, and valuable enough to justify a dedicated role.</p>
    <p>As long as B2B companies need automated, data-driven outbound pipelines (and that need is only growing), GTM Engineers have job security. The tools will change. Clay might not be the center of gravity in 2028. But the function, building automated GTM systems, isn't going away.</p>

    <h2>The AI Question</h2>
    <p>Will AI replace GTM Engineers? This comes up in every conversation about the role's future. The short answer from the data: AI is making GTM Engineers more productive, not redundant.</p>
    <p>Survey respondents report using AI (Claude, ChatGPT, Perplexity) for enrichment research, email copywriting, data cleaning, and workflow debugging. These are tasks that used to consume 30-40% of their week. AI handles them faster. But the strategic work, designing systems, choosing tools, architecting data flows, optimizing conversion, still requires human judgment.</p>
    <p>The role is shifting toward AI orchestration. GTM Engineers increasingly build systems where AI does the repetitive work and humans make the decisions. That's a more valuable role, not a less valuable one. Companies that have adopted AI tools are hiring more GTM Engineers, not fewer.</p>

    <h2>The Risk Factors</h2>
    <p>No career analysis is honest without discussing what could go wrong.</p>
    <p><strong>Tool consolidation.</strong> If one platform does everything (enrichment, sequencing, CRM, automation), the need for engineers who connect disparate tools decreases. This is unlikely in the near term. The GTM tool ecosystem is fragmenting, not consolidating.</p>
    <p><strong>Economic downturn.</strong> GTM Engineering roles are concentrated in VC-backed B2B SaaS companies. A funding winter would reduce hiring. The 2023 tech layoffs affected newer roles disproportionately. But GTM Engineers who generate measurable pipeline are among the last to be cut because their ROI is directly visible.</p>
    <p><strong>Title inflation.</strong> If every marketing coordinator starts calling themselves a GTM Engineer, the title loses meaning and market premium. This is already happening at the margins. The defense is skills, not titles. People who can build complex systems will command premiums regardless of what the role is called next year.</p>
    <p>Weighed against the growth data, the compensation trajectory, and the structural demand, these risks are manageable. GTM Engineering looks like a career, and the <a href="/careers/job-market-analysis/">job market data</a> supports that conclusion with hard numbers.</p>

{faq_html(faq_pairs)}
{career_related_links("is-gtm-engineering-real-career")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/is-gtm-engineering-real-career/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/is-gtm-engineering-real-career/index.html", page)
    print(f"  Built: careers/is-gtm-engineering-real-career/index.html")


def build_career_job_market():
    """CAREER-04: GTM Engineer job market analysis with 5,205% growth data."""
    title = "GTM Engineer Job Market: 5,205% Growth"
    description = (
        "GTM Engineer job postings grew from 63 to 3,342 in under two years."
        " Monthly trends, top hiring countries, and salary data from postings."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Job Market Analysis", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("Is the GTM Engineer job market still growing?",
         "Yes. Job postings grew 5,205% between early 2024 and late 2025, from 63 to 3,342. Monthly posting volume hit 624 in December 2025, the highest single month on record. Growth is decelerating from its explosive early pace but remains strong."),
        ("Can I find remote GTM Engineer jobs?",
         "Remote roles represent a significant portion of GTM Engineer postings. The US leads with 25.7% of all postings, and many US-based roles offer remote or hybrid arrangements. International hiring (India 17.4%, Spain 15.3%, UK 7.7%) also tends toward remote."),
        ("Which countries hire the most GTM Engineers?",
         "The US leads with 25.7% of postings, followed by India (17.4%), Spain (15.3%), UK (7.7%), and Germany (4.2%). India's share is notable. Many US-based B2B SaaS companies hire GTM Engineers in India for enrichment and automation work at lower salary bands."),
        ("What salary should I expect from job postings?",
         "Posted salary median is around $150K, which is about $15K higher than the $135K median reported by working GTM Engineers in our survey. Job postings tend to skew toward senior roles with higher comp. For a detailed breakdown, see our posted vs actual salary comparison."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Guide</div>
        <h1>GTM Engineer Job Market: 5,205% Growth</h1>
        <p>A data-driven look at the GTM Engineer job market. Posting volumes, hiring trends, top countries, and salary bands from 3,342 analyzed listings.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">3,342</span>
        <span class="stat-label">Job Postings (2025)</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">5,205%</span>
        <span class="stat-label">Growth (2024&#8209;2025)</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$150K</span>
        <span class="stat-label">Posted Median Salary</span>
    </div>
</div>

<div class="salary-content">
    <h2>From 63 to 3,342 Postings</h2>
    <p>In early 2024, searching for "GTM Engineer" on any major job board returned a few dozen results. By the end of 2025, that number had reached 3,342. That's 5,205% growth in under two years, making GTM Engineering one of the fastest-growing job titles in B2B SaaS by raw posting volume.</p>
    <p>The growth wasn't linear. It came in waves tied to specific market events. Clay's rapid adoption in mid-2024 triggered the first major hiring surge. Then came the broader recognition that automated outbound required dedicated technical builders. By late 2025, GTM Engineer had moved from niche title to standard headcount line item at growth-stage companies.</p>
    <p>To put the numbers in context: Revenue Operations, a more established field, grew about 35% over the same period. Marketing Operations grew roughly 20%. GTM Engineering is growing at 100x the pace of adjacent roles.</p>

    <h2>Monthly Posting Trends</h2>
    <p>December 2025 was the peak month with 624 new postings, a significant spike likely driven by companies finalizing headcount plans for 2026. Other notable months included October 2025 (520+ postings) and August 2025 (480+ postings).</p>
    <p>The monthly data shows a pattern common in emerging roles: rapid acceleration followed by elevated plateaus. Posting volume hasn't dropped after any monthly peak. It resets to a higher baseline. January 2025 saw about 180 postings. January 2026 projections suggest 400+. The floor keeps rising.</p>
    <p>Seasonal patterns are starting to emerge. Q4 and Q1 show the strongest hiring activity, aligning with annual budget cycles and headcount planning at B2B SaaS companies. Q2 dips slightly as companies execute their existing plans. Q3 picks up again as mid-year budget refreshes happen.</p>

    <h2>Top Hiring Countries</h2>
    <p>The geographic distribution of GTM Engineer postings tells an interesting story about where the role is taking root.</p>
    <p><strong>United States: 25.7%.</strong> Still the largest single market, but less dominant than you might expect. US postings concentrate in SF, NYC, Austin, and remote-first companies. Salary bands are the highest globally, with $150K posted median.</p>
    <p><strong>India: 17.4%.</strong> The second-largest market might surprise some people. Many US-based B2B SaaS companies hire GTM Engineers in India for enrichment pipeline work, Clay table management, and outbound automation. Salary bands are lower ($30K-$60K), but the growth rate is faster than the US market.</p>
    <p><strong>Spain: 15.3%.</strong> Spain has become a hub for GTM Engineering talent, partly driven by Clay's community presence in Europe and partly by cost-of-living advantages that attract remote workers. Barcelona and Madrid are the primary cities.</p>
    <p><strong>United Kingdom: 7.7%.</strong> London dominates UK postings. Salary bands track about 15-20% below US equivalents. The UK market is growing steadily and benefits from strong B2B SaaS ecosystem in London and its surrounding corridor.</p>
    <p><strong>Germany: 4.2%.</strong> Berlin is the primary market. German companies are adopting GTM Engineering more slowly than their US or UK peers, but the trajectory is upward. Enterprise B2B SaaS companies based in DACH region are the primary employers.</p>
    <p>For a salary comparison across these markets, see our <a href="/salary/us-vs-global/">US vs global compensation data</a>.</p>

    <h2>Top Skills in Job Postings</h2>
    <p>Analyzing the 3,342 postings reveals which skills companies mention most frequently in requirements and preferred qualifications.</p>
    <p><strong>Clay:</strong> Mentioned in 69% of postings. The defining tool of the field. Clay proficiency is expected in most GTM Engineer roles, especially at companies that have standardized their outbound stack around it.</p>
    <p><strong>HubSpot:</strong> Mentioned in 52% of postings. The most commonly required CRM. HubSpot's workflow automation and API access make it a natural fit for GTM Engineering teams.</p>
    <p><strong>Salesforce:</strong> Mentioned in 38% of postings. More common at enterprise and growth-stage companies. Salesforce roles tend to pay more than HubSpot-only roles, reflecting the platform's complexity.</p>
    <p><strong>Python:</strong> Mentioned in 34% of postings. But here's the key detail: postings that mention Python have salary ranges 25-40% above those that don't. Python isn't required everywhere, but where it's required, the comp is higher.</p>
    <p><strong>SQL:</strong> Mentioned in 28% of postings. Often paired with Python in technical GTM Engineer roles. SQL skills signal ability to query data warehouses and build reporting beyond CRM-native capabilities.</p>
    <p>For how these skills translate to salary premiums, see our <a href="/salary/coding-premium/">coding premium analysis</a>.</p>

    <h2>Salary Bands from Postings</h2>
    <p>Among postings that disclose salary ranges (roughly 40% of US postings), the data shows:</p>
    <p><strong>Posted median: $150K.</strong> Higher than the $135K median from our practitioner survey, because postings skew toward senior roles and US-based positions. Companies that bother to post salary ranges tend to be competing for talent, which pushes disclosed numbers up.</p>
    <p><strong>Junior range: $85K-$120K.</strong> Entry-level postings often don't disclose salary, which depresses the visible data. When they do, the numbers align closely with survey data.</p>
    <p><strong>Senior range: $160K-$220K.</strong> Senior and Lead postings disclose salary more frequently. The top end reaches $250K+ for Staff-level roles at well-funded companies, typically including equity.</p>
    <p>For a deeper comparison between posted salaries and what people report earning, see <a href="/salary/posted-vs-actual/">posted vs actual salary data</a>.</p>

    <h2>What This Means for Job Seekers</h2>
    <p>The market is in your favor. 3,342 postings and growing means demand outpaces supply. Companies struggle to fill GTM Engineer roles, especially technical ones. If you're qualified, you have negotiating power.</p>
    <p>Geographic flexibility amplifies that advantage. Remote-first companies are hiring globally, and US-based companies are opening roles to international candidates. If you're in a lower-cost market with strong skills, you can access higher-paying roles.</p>
    <p>The skills gap between what companies want and what candidates offer creates opportunity. Postings increasingly ask for Python and SQL, but most GTM Engineers are still low-code operators. If you've invested in technical skills, you're competing with a smaller pool for higher-paying roles.</p>
    <p>For practical advice on breaking into the field, see our <a href="/careers/how-to-become-gtm-engineer/">guide to becoming a GTM Engineer</a>.</p>

{faq_html(faq_pairs)}
{career_related_links("job-market-analysis")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer job market data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/job-market-analysis/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/job-market-analysis/index.html", page)
    print(f"  Built: careers/job-market-analysis/index.html")


def build_career_how_got_jobs():
    """CAREER-05: How GTM Engineers got their jobs."""
    title = "How GTM Engineers Got Their Jobs (2026)"
    description = (
        "121 of 228 GTM Engineers are self-taught. 30% work at agencies."
        " Entry paths and hiring data from the State of GTME Report 2026."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("How GTMEs Got Jobs", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is the most common background for GTM Engineers?",
         "SDR/BDR is the single largest feeder role, followed by marketing ops and revenue ops. But 53% (121/228) of GTM Engineers are self-taught regardless of background. The field rewards people who build skills on their own."),
        ("Is the agency route a good way to break into GTM Engineering?",
         "Yes. 30% of working GTM Engineers are at agencies or freelancing. Agencies offer rapid skill development because you work with multiple clients, stacks, and problems. The pay may be lower initially, but the experience compounds fast."),
        ("Do GTM Engineers with coding backgrounds have an advantage?",
         "Developers who enter GTM Engineering earn roughly $45K more at the median, per our coding premium data. Technical background gives you a higher salary floor and a faster path to senior roles. The gap: you need to learn the GTM domain (outbound, enrichment, pipeline) to be effective."),
        ("What advice do career switchers give for entering GTM Engineering?",
         "The most common advice from surveyed GTM Engineers: build something first, then apply. Create a Clay portfolio. Automate a real workflow. Share it publicly. Hiring managers care about demonstrated output more than credentials or years of experience."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Guide</div>
        <h1>How GTM Engineers Got Their Jobs</h1>
        <p>Entry paths, backgrounds, and hiring patterns from a survey of 228 working GTM Engineers.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">121/228</span>
        <span class="stat-label">Self-Taught (53%)</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">30%</span>
        <span class="stat-label">Agency / Freelance</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">84%</span>
        <span class="stat-label">Learned Clay First</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Self-Taught Majority</h2>
    <p>121 out of 228 GTM Engineers surveyed taught themselves the role. No bootcamp enrollment. No degree program. No formal training from an employer. They identified a problem (usually manual outbound or broken data pipelines), started solving it with tools like Clay, and iterated until they were good enough to get paid for it.</p>
    <p>That 53% self-taught rate is remarkable for a role with a $135K median salary. For comparison, self-taught developers represent about 15-20% of the software engineering workforce. In GTM Engineering, self-taught is the norm, and companies don't penalize it in compensation. The survey shows no statistically significant salary difference between self-taught GTMEs and those who came through more traditional paths.</p>
    <p>What did the self-taught group learn first? Clay dominates. 84% of all respondents use Clay, and among self-taught GTMEs, it was the most common starting point. Clay's spreadsheet-like interface makes it approachable for non-technical people, while its HTTP actions and integration capabilities make it powerful enough for serious automation work.</p>

    <h2>The SDR/BDR Pipeline</h2>
    <p>Former Sales Development Representatives form the largest single feeder group into GTM Engineering. The path makes intuitive sense: SDRs spend their days on outbound prospecting, lead enrichment, and sequence management. GTM Engineering automates exactly those tasks.</p>
    <p>SDR-to-GTME transitions typically start when an SDR gets frustrated with manual processes and starts building automations to make their own job easier. They create a Clay table that enriches leads faster than the team's existing process. They build a Make workflow that syncs enrichment data to the CRM without manual copy-paste. Their manager notices the efficiency gains and either gives them the title or they leave for a dedicated GTM Engineer role.</p>
    <p>The advantage SDR converts bring: deep understanding of the outbound motion. They know what makes a good sequence, what data matters for targeting, and where manual processes break down. The gap: most SDRs need to learn data tools, Python, and systems thinking to move beyond basic automation.</p>

    <h2>Marketing Ops Converts</h2>
    <p>Marketing operations professionals are the second most common background. They bring CRM fluency, analytical thinking, and experience with lead scoring, attribution, and email campaigns. The transition expands their scope from marketing-only workflows to full-funnel automation.</p>
    <p>Marketing ops converts often have an easier time with the analytical and data management aspects of GTM Engineering. They're accustomed to working with large datasets, building segmentation logic, and measuring outcomes. The new skills they need: outbound sequencing, enrichment pipeline design, and integration between sales and marketing tools.</p>
    <p>Many marketing ops GTMEs end up specializing in the intersection of enrichment and personalization, building systems that use enriched data to drive highly targeted marketing campaigns and sales outreach simultaneously.</p>

    <h2>The Revenue Ops Bridge</h2>
    <p>Revenue Operations professionals sit at the natural crossroads of sales, marketing, and customer success data. Their transition to GTM Engineering is less about learning a new domain and more about shifting from strategy and analysis to hands-on building.</p>
    <p>RevOps converts tend to be systems thinkers who understand how data flows between teams and tools. They know why a particular enrichment field matters for sales, why marketing needs it for segmentation, and why customer success uses it for health scoring. That cross-functional view makes them effective architects of GTM systems.</p>
    <p>The gap for RevOps converts is usually technical depth. They need to move from configuring existing tools to building custom solutions. Python, API integration, and advanced Clay workflows close that gap.</p>

    <h2>Developer Transitions</h2>
    <p>Developers who enter GTM Engineering bring the highest technical ceiling and earn the most. The <a href="/salary/coding-premium/">$45K coding premium</a> exists largely because of this group. They can write custom enrichment scripts, build API middleware, create webhook handlers, and automate at a level that no-code builders can't reach.</p>
    <p>The developer path into GTM Engineering usually starts from adjacent work. A backend developer who builds internal sales tools. A data engineer who works on the CRM integration layer. A full-stack developer who creates a prospecting automation for their company. They discover that GTM-focused automation work is both interesting and well-compensated.</p>
    <p>The gap: domain knowledge. A developer who knows Python but doesn't understand outbound sales motions, enrichment strategy, or pipeline management will struggle to design effective GTM systems. The technical skills need to be paired with go-to-market understanding.</p>

    <h2>The Agency and Freelance Path</h2>
    <p>30% of surveyed GTM Engineers work at agencies or run their own freelance practices. This is a striking number for a salaried role, and it reflects the field's youth and the nature of the work.</p>
    <p>Agencies hire aggressively because GTM Engineering work scales with client count. One senior GTME at an agency might manage enrichment and automation systems for 5-10 clients simultaneously. The work is varied, the problems are different, and the learning curve is steep but rewarding.</p>
    <p>Freelance GTMEs (sometimes called "Claygency" operators) typically specialize in Clay-based enrichment and outbound automation. They charge $5K-$8K per month per client for managed GTM infrastructure. The income ceiling is high for skilled operators, but the hours tend to be longer than in-house roles.</p>
    <p>For many people, the agency path is the fastest route to job-ready skills. Six months at an agency teaches you more about GTM Engineering than two years at a single company, because you encounter different tools, industries, and challenges every month. See our <a href="/salary/agency-fees/">agency fee guide</a> for compensation data.</p>

    <h2>Hiring Patterns</h2>
    <p>How are these GTM Engineers getting hired? The survey data reveals some consistent patterns.</p>
    <p><strong>Portfolio over resume.</strong> GTM Engineering hiring favors demonstrated output. Companies want to see Clay tables you've built, workflows you've designed, and systems you've shipped. A portfolio of three good projects beats a polished resume with five years of tangentially related experience.</p>
    <p><strong>Community referrals.</strong> The GTM Engineering community is tight-knit. LinkedIn posts about interesting builds generate recruiter interest. Clay community participation leads to direct job opportunities. Many respondents reported getting their current role through a community connection rather than a job board application.</p>
    <p><strong>Build-first approach.</strong> The most effective job search strategy is building something valuable and sharing it publicly. Create a Clay enrichment system for a real use case. Document it. Post about it. The people who hire GTM Engineers are watching the same feeds where builders share their work.</p>
    <p>If you're looking to enter the field, our <a href="/careers/how-to-become-gtm-engineer/">guide to becoming a GTM Engineer</a> covers the full pathway including skills, timeline, and first job strategies. For the bigger picture on whether the market has room for you, see our <a href="/careers/job-market-analysis/">job market analysis</a>.</p>

{faq_html(faq_pairs)}
{career_related_links("how-gtm-engineers-got-jobs")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/how-gtm-engineers-got-jobs/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/how-gtm-engineers-got-jobs/index.html", page)
    print(f"  Built: careers/how-gtm-engineers-got-jobs/index.html")


def build_career_work_life():
    """CAREER-06: Work-life balance data for GTM Engineers."""
    title = "GTM Engineer Work-Life Balance Data (2026)"
    description = (
        "60% of GTM Engineers work 40-60 hours per week. 23% work 60+."
        " Agency vs in-house hours and burnout data from n=228 survey."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Work-Life Balance", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("How many hours per week do GTM Engineers work?",
         "60% of GTM Engineers work 40-60 hours per week. 23% work 60 or more hours. Only 17% report a standard 40-hour week. The field skews toward longer hours, especially during pipeline ramp-ups and new system builds."),
        ("Do agency GTM Engineers work more than in-house?",
         "Yes. Agency GTMEs report working 10-15 more hours per week on average than their in-house counterparts. Managing multiple clients, context-switching between stacks, and meeting client deadlines drives the difference. The tradeoff is faster learning and often higher total compensation."),
        ("Is remote work common for GTM Engineers?",
         "Remote work is common and growing. A significant portion of US and international GTM Engineer postings offer remote or hybrid arrangements. The nature of the work (tool-based, async-friendly, measurable output) lends itself well to remote execution. See our salary data for remote GTM Engineer compensation."),
        ("What are the signs of burnout in GTM Engineering?",
         "Common burnout signals from survey respondents: constant tool-switching fatigue, pressure to maintain pipeline targets while building new systems, after-hours Slack messages from sales teams, and the expectation to be on-call for broken automations. Setting boundaries around response times and system monitoring is critical."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Guide</div>
        <h1>GTM Engineer Work-Life Balance: The Data</h1>
        <p>Hours worked, agency vs in-house comparison, remote patterns, and burnout signals from 228 surveyed GTM Engineers.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">60%</span>
        <span class="stat-label">Work 40&#8209;60hrs/wk</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">23%</span>
        <span class="stat-label">Work 60+ hrs/wk</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">17%</span>
        <span class="stat-label">Standard 40hr Week</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Hours Reality</h2>
    <p>GTM Engineering is not a 9-to-5 job. The survey data is clear: 83% of GTM Engineers work more than 40 hours per week. 60% work between 40 and 60 hours. 23% work 60 or more. Only 17% report a standard 40-hour week.</p>
    <p>Those numbers put GTM Engineering in the same category as startup engineering and management consulting for hours worked. The field attracts driven builders, and the work rewards intensity. Enrichment pipelines don't build themselves. Broken automations don't wait until Monday morning.</p>
    <p>The honest question is whether this is sustainable. For many respondents, the answer is "for now." The field is young, and many practitioners are in a phase of rapid skill building and career establishment. Working 50-55 hours feels different when you're learning constantly and your comp is rising. It feels less acceptable when you've been doing the same work for three years.</p>

    <h2>Agency vs In-House Hours</h2>
    <p>The biggest factor in hours worked is whether you're at an agency or in-house.</p>
    <p><strong>Agency GTMEs: 50-65 hours/week average.</strong> Managing multiple clients means multiple stacks, multiple Slack channels, and multiple sets of deadlines. Agency work is intense. You're context-switching between Clay setups, CRM configurations, and outbound sequences for 5-10 different companies. The pace is fast. The learning is faster.</p>
    <p><strong>In-house GTMEs: 40-50 hours/week average.</strong> Working for a single company means one stack, one team, and more predictable rhythms. In-house roles have calmer weeks and busier weeks, but the baseline is 10-15 hours less than agency. The tradeoff: slower skill development and less portfolio diversity.</p>
    <p>The agency-to-in-house transition is common. Many GTM Engineers start at agencies, build diverse skills quickly, then move in-house for better work-life balance and deeper specialization. The agency period functions like a training ground, and the in-house move is where the quality of life improves.</p>

    <h2>What Drives the Long Hours</h2>
    <p>Survey respondents identified several factors that push hours beyond 40 per week.</p>
    <p><strong>System monitoring and maintenance.</strong> Enrichment pipelines run continuously. When an API provider changes their rate limits, when a Clay integration breaks, when a CRM sync fails, someone needs to fix it. That someone is usually the GTM Engineer, and the fix is often needed before the next business day.</p>
    <p><strong>Pipeline pressure.</strong> GTM Engineers are measured by pipeline contribution. When the sales team has a bad month, there's pressure to build more sequences, enrich more leads, and ship new workflows. That pressure translates to hours.</p>
    <p><strong>New system builds.</strong> Building a new enrichment waterfall, onboarding a new tool, or migrating between CRMs are project-based efforts that spike hours for 2-4 weeks. These sprints are temporary but frequent, especially in the first year at a company.</p>
    <p><strong>Tool ecosystem complexity.</strong> The GTM stack is a collection of 5-15 different tools that need to work together. Debugging integration issues, managing API rate limits, and keeping data flowing between systems is ongoing overhead. Each new tool added to the stack increases the maintenance burden.</p>

    <h2>Remote Work Patterns</h2>
    <p>GTM Engineering is well-suited to remote work, and the data reflects it. A substantial share of survey respondents work remotely, either full-time or hybrid.</p>
    <p>The work is tool-based and async-friendly. Clay tables, CRM configurations, and Python scripts don't care whether you're in an office or at home. Output is measurable: pipelines generated, leads enriched, sequences built. Managers can evaluate results without monitoring hours.</p>
    <p>Remote work also enables the global hiring patterns visible in <a href="/careers/job-market-analysis/">job market data</a>. US companies hiring GTM Engineers in India, Spain, and the UK are doing so because the work translates well across time zones when structured around async delivery.</p>
    <p>The exception: agencies sometimes require more synchronous availability because client communication and cross-team coordination benefit from overlapping hours. Agency GTMEs who work remotely still tend to keep core business hours in their clients' time zones.</p>

    <h2>Burnout Signals and Prevention</h2>
    <p>23% of respondents working 60+ hours per week raises a burnout concern. The survey captured qualitative data on what pushes GTM Engineers toward exhaustion.</p>
    <p><strong>Always-on expectations.</strong> Sales teams treat GTM infrastructure like it should have 100% uptime. When an enrichment pipeline breaks at 10 PM, the expectation is often that it gets fixed before the morning stand-up. Setting explicit SLAs (response within 4 business hours, not 4 hours) is the most effective boundary.</p>
    <p><strong>Tool-switching fatigue.</strong> Bouncing between Clay, HubSpot, Make, Instantly, and Python in a single day is mentally taxing. Each tool has its own logic, interface, and debugging workflow. Time-blocking focused work on one tool or system per half-day reduces the cognitive load.</p>
    <p><strong>Scope creep.</strong> GTM Engineers often become the de facto fix-it person for anything data or automation related. CRM data quality issues, sales reporting requests, marketing attribution debugging. Everything that touches data or automation lands on your desk. Clear role boundaries and documented ownership prevent this from spiraling.</p>
    <p><strong>Output pressure without rest.</strong> Pipeline metrics are always visible. There's always another sequence to build, another enrichment source to test, another workflow to optimize. The work never feels "done." Establishing weekly output targets (rather than open-ended "do more") creates natural stopping points.</p>

    <h2>The Work-Life Equation</h2>
    <p>GTM Engineering pays well, demands a lot, and rewards intensity. If you thrive on building systems, solving technical puzzles, and seeing measurable output from your work, the hours feel productive. If you need strict boundaries between work and personal time, this field requires deliberate effort to maintain them.</p>
    <p>The compensation helps. A $135K median salary (and up to $250K for senior technical roles) provides financial cushion. But money doesn't prevent burnout if the hours aren't managed. The smartest GTM Engineers build their own automations for monitoring and alerting, reducing the manual overhead that drives late nights.</p>
    <p>For compensation data across the <a href="/careers/operator-vs-engineer/">operator vs engineer spectrum</a>, see our salary breakdowns. And for the full picture on entering the field with realistic expectations, start with our <a href="/careers/how-to-become-gtm-engineer/">how to become a GTM Engineer guide</a>.</p>

{faq_html(faq_pairs)}
{career_related_links("work-life-balance")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/work-life-balance/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/work-life-balance/index.html", page)
    print(f"  Built: careers/work-life-balance/index.html")


def build_career_demographics():
    """CAREER-07: Demographics deep-dive page."""
    title = "GTM Engineer Demographics: Age, Location, Data"
    description = (
        "Who are GTM Engineers? Median age 25, 32 countries represented, 58%"
        " US-based. Demographic data from 228 surveyed practitioners."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Demographics", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is the average age of a GTM Engineer?",
         "The median age is 25, making this one of the youngest specialized roles in B2B SaaS. The distribution skews heavily toward Gen Z and younger millennials, which tracks with the role emerging in 2023-2024. Very few respondents in our n=228 survey were over 35."),
        ("Where do most GTM Engineers live?",
         "58% of surveyed GTM Engineers are based in the United States. The remaining 42% span 31 other countries, with the UK, Canada, Germany, and Australia being the next largest concentrations. Remote work makes this a globally distributed role."),
        ("What education do GTM Engineers have?",
         "121 out of 228 surveyed GTM Engineers (53%) are self-taught. Formal education backgrounds vary widely: business, marketing, computer science, and communications all appear frequently. No single degree dominates, and employers consistently prioritize demonstrable skills over credentials."),
        ("How diverse is the GTM Engineer workforce?",
         "The role skews male, consistent with broader B2B SaaS tech roles. But the self-taught entry path and agency prevalence (30% work at agencies) create lower barriers to entry than traditional engineering roles. Geographic diversity is strong with 32 countries represented in the survey data."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Intelligence</div>
        <h1>GTM Engineer Demographics: Age, Location, Data</h1>
        <p>Who are the people building automated revenue systems? Age, location, education, and background data from 228 working GTM Engineers across 32 countries.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">25</span>
        <span class="stat-label">Median Age</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">32</span>
        <span class="stat-label">Countries Represented</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">58%</span>
        <span class="stat-label">US-Based</span>
    </div>
</div>

<div class="salary-content">
    <h2>A Gen Z Function</h2>
    <p>The median GTM Engineer is 25 years old. That number should stop you in your tracks. In most B2B SaaS roles, the median age sits in the early-to-mid 30s. GTM Engineering is a generation younger.</p>
    <p>This makes sense when you trace the timeline. Clay launched in 2023. The "GTM Engineer" title started appearing in job postings that same year. By 2024, posting volume exploded 5,205%. The people who jumped on this wave were overwhelmingly in their early-to-mid 20s, many fresh from SDR roles or straight out of college with a knack for automation.</p>
    <p>The age distribution clusters tightly around 22-28, with a thin tail extending into the mid-30s. Respondents over 40 were rare enough to count on one hand. This isn't a role that mid-career professionals are pivoting into in large numbers. It's being built by a generation that grew up with APIs, no-code tools, and AI assistants as default infrastructure.</p>

    <h2>Geographic Spread: 32 Countries</h2>
    <p>GTM Engineers work everywhere, but the center of gravity is the United States. 58% of survey respondents (132 out of 228) are US-based. That's consistent with where the role originated: Clay is a US company, the early adopter community was concentrated in SF and NYC, and US B2B SaaS companies were the first to create dedicated GTM Engineering positions.</p>
    <p>The remaining 42% spans 31 countries. The UK and Canada each have meaningful clusters, followed by Germany, Australia, and India. Several respondents reported working from countries in Southeast Asia and Latin America while serving US-based clients remotely.</p>
    <p>Remote work is the default operating mode. Most job postings for GTM Engineers list remote or hybrid arrangements. The tools are cloud-based (Clay, HubSpot, Salesforce, Make, Instantly), the work is asynchronous-friendly, and time zone overlap matters less than output quality. This makes the role accessible to talent anywhere with reliable internet.</p>
    <p>For location-specific salary data, see our <a href="/salary/us-vs-global/">US vs Global salary comparison</a>. US-based GTM Engineers earn meaningfully more, but the gap narrows when you factor in cost-of-living differences.</p>

    <h2>Education: The Self-Taught Majority</h2>
    <p>121 out of 228 respondents (53%) described themselves as self-taught. They learned Clay from YouTube tutorials, built automation projects on their own, and assembled their skills through practice rather than formal education. This is the defining characteristic of the GTM Engineering workforce: it rewards builders, not credential holders.</p>
    <p>Among those with formal education, the backgrounds are eclectic. Business and marketing degrees are common, which makes sense given the sales and marketing operations roots of the role. Computer science and engineering degrees appear too, especially among higher earners who bring coding skills to the table.</p>
    <p>But here's what the data shows clearly: the degree itself doesn't predict earnings. The <a href="/salary/coding-premium/">$45K coding premium</a> exists regardless of whether you learned Python in a university classroom or from a YouTube series. What matters is whether you can write scripts that connect APIs, transform data, and automate workflows.</p>
    <p>This education profile creates an interesting dynamic. GTM Engineering has one of the lowest formal barriers to entry of any role paying $130K+ in tech. You don't need a four-year degree. You don't need a bootcamp certificate. You need to demonstrate that you can build systems that generate pipeline.</p>

    <h2>Background Diversity</h2>
    <p>The feeder roles for GTM Engineering tell the story of where these practitioners come from. SDR and BDR transitions make up the largest single group. These are people who spent months or years doing manual outbound prospecting and decided to automate themselves out of the repetitive work.</p>
    <p>Marketing ops is the second-largest feeder. These practitioners bring CRM fluency, campaign management experience, and analytical thinking. Revenue ops contributes a smaller but high-impact group who understand the full GTM motion from strategy to execution.</p>
    <p>Developers who transition into GTM Engineering represent a smaller percentage but command the highest salaries. They bring technical depth that no-code practitioners struggle to match, and the salary data confirms it: the bimodal distribution described in our <a href="/careers/operator-vs-engineer/">operator vs engineer analysis</a> maps directly to coding ability.</p>
    <p>30% of respondents work at agencies or run freelance practices. This is significantly higher than most B2B SaaS roles, where agency workers typically represent 5-10% of the workforce. The agency path serves as both an entry point for newcomers and a long-term career choice for practitioners who prefer variety and autonomy over in-house stability.</p>

    <h2>What the Demographics Signal</h2>
    <p>A young, globally distributed, self-taught workforce building automated revenue systems. That's the profile. It looks more like the early days of web development in the 2000s than a traditional enterprise SaaS function.</p>
    <p>The youth of the field means career paths are still being defined. There's no established "10-year GTM Engineer" career track because the role itself is barely three years old. The people setting compensation benchmarks and career ladders are doing it for the first time.</p>
    <p>The global distribution means salary expectations vary widely. A GTM Engineer in Austin and one in Berlin might do identical work on identical tools, but their compensation reflects local market conditions. Our <a href="/salary/">salary data section</a> breaks this down by location, seniority, and company stage.</p>
    <p>The self-taught majority means the field is meritocratic in a specific way: your portfolio matters more than your pedigree. For anyone considering <a href="/careers/how-to-become-gtm-engineer/">entering GTM Engineering</a>, that's the most important demographic insight. Show what you can build. The rest is background noise.</p>

{faq_html(faq_pairs)}
{career_related_links("demographics")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/demographics/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/demographics/index.html", page)
    print(f"  Built: careers/demographics/index.html")


def build_career_vs_revops():
    """CAREER-08: GTM Engineer vs RevOps convergence page."""
    title = "GTM Engineer vs RevOps: Role Convergence Data"
    description = (
        "GTM Engineer vs RevOps: only 9.6% predict convergence. Technical vs"
        " operational split, salary gaps, and where the roles are heading."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("GTME vs RevOps", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is the difference between a GTM Engineer and RevOps?",
         "GTM Engineers build automated systems: enrichment pipelines, outbound sequences, data workflows using tools like Clay, Python, and APIs. RevOps professionals design and manage the strategic operational framework: CRM architecture, forecasting models, territory planning, and cross-functional alignment. The overlap is in CRM and data operations, but the daily work is fundamentally different."),
        ("Will GTM Engineering merge with RevOps?",
         "Only 9.6% of surveyed GTM Engineers predict full convergence with RevOps. The technical depth of GTM Engineering (coding, API integration, automation building) keeps it distinct from the strategic and process-oriented nature of RevOps. More likely: they'll be complementary functions that collaborate closely."),
        ("Should I pursue GTM Engineering or RevOps?",
         "If you prefer building systems, writing code, and working with tools like Clay and Python, GTM Engineering is the better fit. If you prefer strategy, process design, cross-functional alignment, and CRM architecture at a system level, RevOps suits you better. GTM Engineers skew technical; RevOps skews operational."),
        ("How do GTM Engineer and RevOps salaries compare?",
         "GTM Engineers report a median salary of $135K with a range of $90K-$250K+. RevOps salaries at comparable experience levels range from $100K-$180K for individual contributors. The GTM Engineering premium reflects the technical skills (coding, API work) that command higher compensation in the market."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Intelligence</div>
        <h1>GTM Engineer vs RevOps: The Convergence Question</h1>
        <p>Will these roles merge? Survey data from 228 GTM Engineers shows only 9.6% predict convergence. Here's why the technical and operational paths are staying separate.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">9.6%</span>
        <span class="stat-label">Predict Convergence</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$135K</span>
        <span class="stat-label">GTME Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">84%</span>
        <span class="stat-label">Use Clay (GTMEs)</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Question Everyone Asks</h2>
    <p>"Isn't GTM Engineering just RevOps with a new name?" It's the most common question in every GTM Engineering community. And the survey data gives a clear answer: no, and the practitioners themselves don't think convergence is coming.</p>
    <p>When asked whether GTM Engineering would merge with RevOps over the next 3-5 years, only 9.6% of respondents said yes. The overwhelming majority see these as distinct functions with different skill requirements, different daily workflows, and different career trajectories.</p>
    <p>That 9.6% figure is striking because it comes from the people doing the work, not analysts or vendors with marketing agendas. GTM Engineers know their own role, and they don't see it collapsing into RevOps.</p>

    <h2>Where the Roles Overlap</h2>
    <p>There is genuine overlap, and it's worth mapping precisely. Both roles touch CRM systems daily. A GTM Engineer pushes enriched data into HubSpot or Salesforce; a RevOps professional designs the CRM architecture that data flows into. Both care about data quality, pipeline visibility, and operational efficiency.</p>
    <p>Data operations is the second overlap zone. GTM Engineers build enrichment pipelines and data cleaning workflows. RevOps professionals manage data governance, deduplication rules, and reporting frameworks. They're working on the same data from different angles.</p>
    <p>Tool administration creates a third intersection. Both roles configure and maintain parts of the sales tech stack. A GTM Engineer might own Clay, Instantly, and the enrichment layer. A RevOps professional might own the CRM, forecasting tools, and territory management. In smaller companies, one person does both.</p>

    <h2>Where They Diverge</h2>
    <p>The divergence is stark when you look at daily activities. GTM Engineers spend their time building: writing Clay tables, coding Python scripts for API integrations, configuring Make/n8n automations, and setting up outbound sequences. The work is technical, iterative, and hands-on-keyboard.</p>
    <p>RevOps professionals spend their time designing and managing: CRM architecture decisions, sales process optimization, forecasting model calibration, territory planning, compensation structure analysis, and cross-functional alignment between sales, marketing, and customer success.</p>
    <p>The skill profile confirms the split. 84% of GTM Engineers use Clay daily. The <a href="/salary/coding-premium/">coding premium data</a> shows a $45K gap between technical and non-technical practitioners. RevOps professionals rarely need Clay proficiency or coding skills. They need Salesforce admin expertise, analytical modeling ability, and strategic communication skills.</p>
    <p>Think of it this way: GTM Engineers are builders. RevOps professionals are architects and operators. The builder makes the systems work. The architect designs which systems to build and how they fit together.</p>

    <h2>Salary Comparison</h2>
    <p>GTM Engineers report a median salary of $135K, with the range spanning $90K at the junior level to $250K+ for senior technical practitioners. The distribution is bimodal, clustering around $110K (operator path) and $155K (engineer path), with the gap driven by coding ability.</p>
    <p>RevOps individual contributors at comparable experience levels typically earn $100K-$180K, with the median sitting around $120K-$140K depending on company size and location. Senior RevOps leaders (VP/Director level) can earn $200K+, but these are management-track roles, not IC roles.</p>
    <p>The GTM Engineering salary premium at the IC level reflects market dynamics: the technical skills are scarcer, the role is newer (less established salary benchmarking), and the direct pipeline impact is easier to measure and attribute. For a deeper breakdown, see our <a href="/salary/comparisons/">salary comparison pages</a>.</p>

    <h2>Future Trajectory</h2>
    <p>The 90.4% who don't predict convergence aren't being stubborn. They're reading the trend lines correctly. As AI tools make automation building more accessible, you might expect the roles to merge. But the opposite is happening: the ceiling for what GTM Engineers can build is rising faster than the floor.</p>
    <p>AI coding assistants (used by 71% of GTM Engineers) don't eliminate the need for technical judgment. They accelerate building speed for people who already understand what to build. The gap between a GTM Engineer using Claude to write Python scripts and a RevOps professional using ChatGPT to draft process documentation is widening, not narrowing.</p>
    <p>The more likely future: GTM Engineering and RevOps become complementary specializations within the revenue team, similar to how frontend and backend engineering are distinct roles that collaborate closely. Companies with mature GTM operations will have both functions. Smaller companies will have generalists who lean one direction or the other.</p>
    <p>For anyone choosing between these paths, the decision comes down to temperament. Do you want to build systems or design strategy? Do you prefer code or process? The <a href="/careers/operator-vs-engineer/">operator vs engineer analysis</a> provides more data on how this choice affects your compensation trajectory.</p>

{faq_html(faq_pairs)}
{career_related_links("gtm-engineer-vs-revops")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/gtm-engineer-vs-revops/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/gtm-engineer-vs-revops/index.html", page)
    print(f"  Built: careers/gtm-engineer-vs-revops/index.html")


def build_career_coding_needed():
    """CAREER-09: Do you need to code page."""
    title = "Do GTM Engineers Need to Code? Data Says Yes"
    description = (
        "Bimodal coding skill distribution among GTM Engineers. $45K premium"
        " for coders. Which languages matter and what coding means in practice."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Coding Requirement", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is the minimum coding level for a GTM Engineer?",
         "You can get hired as a GTM Engineer with zero coding skills. About 40% of practitioners cluster at the 1-3 range on a 1-10 self-rated coding scale. But the salary data is clear: coders earn roughly $45K more. Basic Python (API calls, JSON parsing, data manipulation with pandas) is the minimum to access the higher salary band."),
        ("What is the best programming language to learn first as a GTM Engineer?",
         "Python. It's the most commonly used language among GTM Engineers who code, and it handles the three core technical tasks: API integration, data transformation, and automation scripting. SQL is a strong second choice for querying CRM data and building reports. JavaScript comes third for webhook handling and browser automation."),
        ("Can you build a GTM Engineering career using only Clay?",
         "Yes, but with a salary ceiling. Clay-only practitioners (the operator path) cluster around $110K median. You can build a solid career at that level, especially at agencies where Clay expertise is the primary deliverable. But if you want to break into the $150K+ range, adding coding skills is the clearest path to get there."),
        ("How long does it take to learn enough coding for GTM Engineering?",
         "Most practitioners report 2-3 months of focused Python learning to reach useful proficiency. You don't need to build web applications. You need to write scripts that call APIs, parse JSON responses, transform data in pandas, and automate repetitive tasks. Online courses covering Python for data analysis or Python for API integration are the fastest path."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Intelligence</div>
        <h1>Do GTM Engineers Need to Code?</h1>
        <p>The $45K question. Survey data reveals a bimodal distribution: practitioners cluster at low-code and high-code extremes, with compensation following the same split.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">$45K</span>
        <span class="stat-label">Coding Premium</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">71%</span>
        <span class="stat-label">Use AI Coding Tools</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">2&#8209;3mo</span>
        <span class="stat-label">To Useful Proficiency</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Bimodal Distribution</h2>
    <p>When we asked 228 GTM Engineers to rate their coding skills on a 1-10 scale, we expected a bell curve. We got something completely different: two distinct clusters. One group sits at 1-3 (low-code/no-code operators). The other sits at 7-10 (technical engineers). The middle range, 4-6, is a valley.</p>
    <p>This bimodal pattern tells a story about the role itself. GTM Engineering has two distinct paths, and practitioners tend to commit to one or the other. You're either building with visual tools (Clay, Make, Zapier) and staying in the no-code world, or you're writing Python, building API integrations, and approaching the work as a software problem.</p>
    <p>Few people occupy the middle ground. The data suggests that learning to code is a binary investment: you either cross the threshold into useful proficiency or you stay in the visual-builder lane. Dabbling doesn't pay off.</p>

    <h2>The $45K Premium</h2>
    <p>The salary data maps directly onto the coding distribution. GTM Engineers who rate themselves 7+ on coding ability earn roughly $45K more than those in the 1-3 range. That's the gap between a $110K median (operator path) and a $155K median (engineer path).</p>
    <p>$45K is significant by any measure. It's the difference between a good salary and an excellent one. And it compounds: higher base salaries mean bigger percentage raises, better equity grants, and stronger negotiating positions for your next role.</p>
    <p>For the complete salary breakdown by coding ability, see our <a href="/salary/coding-premium/">coding premium analysis</a>. The data includes breakdowns by seniority level, company stage, and specific languages.</p>

    <h2>What "Coding" Means in Practice</h2>
    <p>GTM Engineering coding is not software engineering. You're not building web applications, designing databases, or deploying microservices. The coding that commands a premium is specific and pragmatic.</p>
    <p><strong>API integration:</strong> Writing Python scripts that call enrichment APIs (Clearbit, Apollo, FullEnrich), CRM APIs (HubSpot, Salesforce), and sequencing tool APIs (Instantly, Lemlist). Most of this is HTTP requests, JSON parsing, and error handling. A single well-written API integration script can replace an entire Make automation that would otherwise cost $50/month in platform fees.</p>
    <p><strong>Data transformation:</strong> Cleaning, normalizing, and reshaping data with pandas. Deduplication logic. Fuzzy matching on company names. Parsing messy job titles into standardized categories. This is the work that separates scalable GTM operations from brittle ones.</p>
    <p><strong>Custom automations:</strong> Scheduled scripts that run enrichment batches, monitor CRM data quality, generate reports, or trigger alerts. Python plus a cron job (or a simple scheduler) can replace expensive workflow automation platform subscriptions.</p>
    <p><strong>Webhook handlers:</strong> Small Node.js or Python services that receive webhook events from CRM systems, process them, and route data to the right destination. This bridges gaps between tools that don't have native integrations.</p>

    <h2>Which Languages Matter</h2>
    <p><strong>Python (first priority):</strong> The dominant language among GTM Engineers who code. It handles API calls, data manipulation, and automation scripting. The ecosystem (requests, pandas, json, schedule) covers 90% of GTM Engineering coding needs. If you learn one language, make it Python.</p>
    <p><strong>SQL (second priority):</strong> Increasingly important as companies want GTM Engineers who can query data warehouses and build custom reports. HubSpot and Salesforce both support SQL-like queries for bulk data operations. If you can write SELECT, JOIN, and GROUP BY queries, you can answer business questions that no-code tools struggle with.</p>
    <p><strong>JavaScript (third priority):</strong> Useful for webhook handlers, browser automation, and custom Clay actions. Node.js is the runtime. If you already know Python, JavaScript is a natural second language. But if you're choosing where to invest, Python delivers more value per hour of learning.</p>

    <h2>AI Coding Tools Changed the Equation</h2>
    <p>71% of GTM Engineers report using AI coding tools (Claude, GitHub Copilot, ChatGPT). This is reshaping the coding skill question. You don't need to memorize API documentation or write boilerplate from scratch. You need to understand what to ask for and how to evaluate the output.</p>
    <p>AI tools compress the learning curve. A GTM Engineer with basic Python knowledge and Claude or Copilot can write scripts that would have taken an experienced developer to build three years ago. The skill ceiling hasn't dropped, but the skill floor for useful output has fallen significantly.</p>
    <p>This doesn't mean coding skills are less valuable. The opposite: AI tools make coding more accessible, which means more GTM Engineers will cross the threshold into the technical path. The premium might compress slightly as the supply of technical practitioners grows, but we're years away from that happening at meaningful scale.</p>

    <h2>The Realistic Learning Path</h2>
    <p>Most practitioners report 2-3 months of focused learning to reach useful Python proficiency. Here's what that looks like in practice.</p>
    <p><strong>Weeks 1-2:</strong> Python fundamentals. Variables, functions, loops, dictionaries, lists. Any online course covering Python basics will work. Focus on exercises involving data structures and file handling.</p>
    <p><strong>Weeks 3-4:</strong> HTTP requests and JSON. Learn the requests library. Call a free API (like JSONPlaceholder), parse the response, and write it to a file. Then call a real API: Clay, HubSpot, or Apollo all have well-documented APIs with free tiers.</p>
    <p><strong>Weeks 5-6:</strong> Pandas for data manipulation. Load a CSV of lead data. Clean it: normalize company names, deduplicate on email, fill missing fields. This is the core data transformation work that GTM Engineers do daily.</p>
    <p><strong>Weeks 7-8:</strong> Build a project. Create a script that enriches a list of companies via API, scores them based on criteria you define, and outputs a clean CSV for CRM import. This project becomes your portfolio piece and your proof of competence.</p>
    <p>Can you skip this and succeed? Yes. The data shows 40%+ of practitioners operate successfully without coding. But you're choosing the lower salary band. That's a trade you should make consciously, not by default.</p>
    <p>For more on how technical depth shapes your career path, see the <a href="/careers/operator-vs-engineer/">operator vs engineer analysis</a> and the <a href="/careers/skills-gap/">skills gap breakdown</a>.</p>

{faq_html(faq_pairs)}
{career_related_links("do-you-need-to-code")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/do-you-need-to-code/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/do-you-need-to-code/index.html", page)
    print(f"  Built: careers/do-you-need-to-code/index.html")


def build_career_reporting_structure():
    """CAREER-10: Reporting structure data page."""
    title = "GTM Engineer Reporting Structure Data"
    description = (
        "Sales and Marketing are the most common reporting lines for GTM"
        " Engineers. Percentage breakdowns, career growth implications."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Reporting Structure", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("Who do most GTM Engineers report to?",
         "Sales leadership is the most common reporting line, followed by Marketing. In smaller companies, GTM Engineers often report directly to the CEO or founder. The reporting line typically depends on which function (sales, marketing, or ops) first recognized the need for automation and created the role."),
        ("What is the ideal reporting line for a GTM Engineer?",
         "It depends on your priorities. Reporting to Sales gives you the clearest path to measurable impact (pipeline generated, meetings booked). Reporting to Marketing often provides more strategic latitude and cross-functional visibility. Reporting to a RevOps or GTM leader is emerging as the ideal structure at larger companies."),
        ("How does reporting structure affect career growth?",
         "GTM Engineers reporting to Sales leaders tend to get promoted faster when they demonstrate clear pipeline impact. Those under Marketing gain broader strategic experience. Budget access also varies: Sales-adjacent roles often have larger tool budgets because ROI attribution is more direct."),
        ("How is agency GTM Engineering structured differently?",
         "Agency GTM Engineers typically report to an account director or agency founder rather than a traditional Sales/Marketing leader. The structure is flatter, with more autonomy and less bureaucracy. 30% of GTM Engineers work at agencies, and the reporting lines reflect the client-service model rather than internal corporate hierarchies."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Intelligence</div>
        <h1>GTM Engineer Reporting Structure Data</h1>
        <p>Who do GTM Engineers report to, and how does it affect career growth and compensation? Data from 228 practitioners on org chart placement, budget ownership, and the agency vs in-house split.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">Sales</span>
        <span class="stat-label">Most Common Report</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">30%</span>
        <span class="stat-label">Work at Agencies</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">228</span>
        <span class="stat-label">Practitioners Surveyed</span>
    </div>
</div>

<div class="salary-content">
    <h2>Where GTM Engineers Sit in the Org Chart</h2>
    <p>GTM Engineering doesn't have a standard home in the org chart yet. The role is too new. Companies that hire GTM Engineers are placing them wherever the initial need was identified, which creates a scattered distribution across Sales, Marketing, Operations, and sometimes directly under executive leadership.</p>
    <p>Sales is the most common reporting line. This makes intuitive sense: GTM Engineers build outbound pipelines, enrich prospect data, and automate sequencing. The output feeds directly into the sales funnel. Sales leaders who see their SDR teams manually prospecting are the most motivated to hire someone who can automate that work.</p>
    <p>Marketing is the second most common home. Companies that approach GTM Engineering from the demand generation side, building automated lead capture, scoring, and routing systems, tend to place the role under Marketing leadership. These GTM Engineers often focus more on inbound pipeline automation and less on outbound sequencing.</p>

    <h2>The CEO Direct Report Pattern</h2>
    <p>At startups (Seed through Series A), GTM Engineers frequently report directly to the CEO or founder. The company is small enough that the CEO manages the revenue function personally, and the GTM Engineer is the first technical hire dedicated to automating that motion.</p>
    <p>This structure has advantages. You get executive visibility, fast decision-making, and direct access to budget. When the CEO sees the enrichment pipeline you built generate 50 qualified meetings in a month, you don't need three layers of management to approve a tool upgrade.</p>
    <p>The disadvantage: founders are busy, feedback can be inconsistent, and you may lack a technical mentor who understands your work. For salary implications of working at early-stage companies, see our <a href="/salary/by-company-stage/">compensation by company stage</a> breakdown.</p>

    <h2>The Emerging GTM/RevOps Team Structure</h2>
    <p>Growth-stage and enterprise companies are starting to build dedicated GTM Engineering teams that sit alongside or within Revenue Operations. This is the most mature organizational model: a GTM Engineering function with its own team lead reporting to a VP of Revenue Operations or a Chief Revenue Officer.</p>
    <p>When this structure works, it resolves the historical tension between Sales and Marketing ownership. The GTM Engineering team serves both functions, building systems that span the full funnel from lead enrichment through outbound sequencing through CRM automation through reporting.</p>
    <p>The data suggests this structure is where the industry is heading, but we're early. Most companies still have a single GTM Engineer (or a small team of 2-3) embedded within an existing function rather than operating as a standalone group.</p>

    <h2>Budget Ownership and Tool Access</h2>
    <p>Reporting structure directly affects your tool budget. GTM Engineers under Sales leadership typically have larger budgets for outbound tools (Instantly, Clay, Apollo) because the ROI calculation is straightforward: spend $X on tools, generate $Y in pipeline.</p>
    <p>Those under Marketing may have broader tool access (including analytics and content tools) but face more scrutiny on pure outbound spend. Marketing budgets are typically allocated across multiple channels, and outbound automation competes with paid ads, events, and content for dollars.</p>
    <p>Agency GTM Engineers have a different budget dynamic entirely. The agency bills clients for tool costs (or absorbs them as overhead), and the GTM Engineer uses whatever stack the client requires. This means exposure to more tools but less control over tool selection.</p>

    <h2>Agency vs In-House Reporting</h2>
    <p>30% of GTM Engineers work at agencies or run freelance practices. The reporting structure in agencies is fundamentally different from in-house roles.</p>
    <p>Agency GTM Engineers report to an account director, agency founder, or operations manager. The relationship is flatter and more output-oriented: build the system, show the results, move to the next client project. There's less organizational politics and more emphasis on delivery speed.</p>
    <p>In-house GTM Engineers navigate corporate hierarchies, cross-functional dependencies, and longer feedback loops. The tradeoff is stability, deeper domain knowledge, and typically higher base compensation. For the complete agency vs in-house compensation analysis, see our <a href="/salary/agency-fees/">agency fee structure</a> page.</p>
    <p>Your reporting line shapes your career trajectory. Sales-adjacent positions favor measurable impact (pipeline, meetings, revenue attribution). Marketing-adjacent positions favor strategic breadth. And the <a href="/careers/operator-vs-engineer/">operator vs engineer</a> split plays out differently depending on where you sit: technical depth matters more under Sales, while strategic breadth matters more under Marketing.</p>

{faq_html(faq_pairs)}
{career_related_links("reporting-structure")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/reporting-structure/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/reporting-structure/index.html", page)
    print(f"  Built: careers/reporting-structure/index.html")


def build_career_impact():
    """CAREER-11: Impact measurement page."""
    title = "How GTM Engineers Measure Impact and Prove ROI"
    description = (
        "Pipeline generated, meetings booked, response rates. How GTM Engineers"
        " track KPIs and prove value to leadership. Survey data from n=228."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Impact Measurement", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What are the best KPIs for GTM Engineers?",
         "The most commonly tracked metrics are meetings booked, pipeline generated (dollar value), response rates on outbound sequences, and enrichment accuracy (percentage of records with complete, validated data). The strongest performers track a combination of volume (meetings) and quality (pipeline value per meeting)."),
        ("How do GTM Engineers handle attribution?",
         "Attribution is the biggest measurement challenge. Most GTM Engineers use first-touch attribution (crediting the enrichment or sequence that generated the initial reply) combined with CRM pipeline tracking. Multi-touch attribution models exist but are rare at the GTM Engineering level because most teams lack the infrastructure to implement them."),
        ("How should I communicate impact to leadership?",
         "Lead with dollar values, not activity metrics. Instead of reporting '500 leads enriched this week,' report '$340K in new pipeline from enriched and sequenced accounts.' Connect your automation work to revenue outcomes that executives care about. Weekly pipeline reports with before/after comparisons work well."),
        ("Does measured impact affect GTM Engineer compensation?",
         "Yes. GTM Engineers who can demonstrate direct pipeline impact earn more and get promoted faster. The ability to tie your work to revenue outcomes is a salary multiplier. Companies with clear attribution give their GTM Engineers variable compensation (10-20% of base) tied to pipeline or meeting targets."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Intelligence</div>
        <h1>How GTM Engineers Measure Impact</h1>
        <p>The metrics that matter, the attribution challenge, and how to prove ROI to leadership. Data from 228 GTM Engineers on KPIs, pipeline tracking, and compensation tied to measured outcomes.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">Pipeline</span>
        <span class="stat-label">Top KPI</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">92%</span>
        <span class="stat-label">Track Meetings Booked</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$135K</span>
        <span class="stat-label">Median Salary</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Metrics That Matter</h2>
    <p>GTM Engineers are measured on output, and the output that matters most is pipeline. Not leads generated. Not emails sent. Not contacts enriched. Pipeline: the dollar value of qualified opportunities that your systems create.</p>
    <p>This is what separates GTM Engineering measurement from marketing ops or sales ops metrics. A marketing ops manager might report on MQL volume. A sales ops analyst might track CRM adoption rates. A GTM Engineer reports on pipeline generated by automated systems. The metric is concrete, measurable, and tied directly to revenue.</p>
    <p>The survey data confirms this hierarchy. The most commonly tracked KPIs among the 228 respondents, in order of prevalence:</p>
    <p><strong>1. Meetings booked (92% track this):</strong> The clearest output metric. How many meetings did your enrichment + sequencing automation generate this week/month? This number is hard to argue with and easy to attribute.</p>
    <p><strong>2. Pipeline value generated:</strong> The dollar amount of new opportunities created from GTM Engineering workflows. This requires CRM tracking (typically HubSpot or Salesforce deal pipeline) and consistent source attribution. More meaningful than meetings because it factors in deal quality.</p>
    <p><strong>3. Response rates:</strong> The percentage of outbound sequences that generate a reply. This measures the quality of your personalization, enrichment accuracy, and targeting. Typical benchmarks: 3-8% for cold outbound, 15-25% for warm/intent-triggered sequences.</p>
    <p><strong>4. Enrichment accuracy:</strong> What percentage of your enriched records have complete, validated data? This is an operational metric that feeds into the output metrics above. Poor enrichment accuracy means wasted sequences and lower response rates.</p>

    <h2>The Attribution Problem</h2>
    <p>Here's the honest challenge: attribution in GTM Engineering is messy. Your enrichment pipeline feeds data to the sales team. Your outbound sequences generate replies that an AE converts. Your CRM automation routes leads to the right rep at the right time. How much credit do you get for the closed deal?</p>
    <p>Most GTM Engineers use first-touch attribution as a practical compromise. If your Clay enrichment + Instantly sequence generated the initial meeting, you claim that pipeline. It's imperfect but defensible, and it's what most CRM systems support natively.</p>
    <p>The more sophisticated approach is building a pipeline attribution model that tracks your specific contribution at each stage. Which deals originated from your enriched lists? Which meetings came from your sequences? Which opportunities were routed by your automation? This requires custom CRM reporting, but the investment pays off in salary negotiations and budget discussions.</p>
    <p>Some companies solve this by giving GTM Engineers explicit pipeline ownership. You own the top-of-funnel number: meetings generated from automated outbound. The sales team owns conversion. This clean division makes attribution straightforward and aligns incentives.</p>

    <h2>Proving ROI to Leadership</h2>
    <p>Executives don't care about your Clay table architecture or your Make automation workflow. They care about three things: how much pipeline are you generating, what does it cost, and how does it compare to alternatives (hiring more SDRs, using an agency, buying a tool).</p>
    <p>The strongest ROI argument follows this structure:</p>
    <p><strong>Before state:</strong> "Our SDR team manually prospected X leads per week at a cost of $Y per meeting booked."</p>
    <p><strong>After state:</strong> "My automated pipeline generates 3X leads per week at $Y/4 per meeting booked, while the SDR team focuses on high-value conversations."</p>
    <p><strong>Cost comparison:</strong> "My fully loaded cost (salary + tools) is $Z. An equivalent SDR team producing the same volume would cost $Z * 3."</p>
    <p>This framework works because it speaks the language of unit economics. Cost per meeting. Cost per pipeline dollar. Cost per closed deal. Executives understand these numbers and can compare them against other investments.</p>

    <h2>Weekly Reporting That Works</h2>
    <p>The GTM Engineers with the strongest impact visibility share a weekly report with their manager (and often the broader revenue team). The format is simple.</p>
    <p>Top line: pipeline generated this week in dollars. Second line: meetings booked. Third line: sequence performance (sends, opens, replies, meetings). Fourth line: enrichment volume and accuracy. Fifth line: what you're building next week and the expected impact.</p>
    <p>Keep it to one page or one Slack message. No slide decks. No lengthy analysis. Leadership wants to see the number, the trend, and the forecast. If the number is growing, you're doing well. If it's flat, explain why and what you're changing.</p>

    <h2>Impact and Compensation</h2>
    <p>The survey data shows a clear correlation between measurable impact and compensation. GTM Engineers who can point to specific pipeline numbers earn more and advance faster.</p>
    <p>Variable compensation reinforces this. Some companies offer quarterly bonuses tied to pipeline targets (typically 10-20% of base salary). Others include pipeline metrics in annual review criteria. Either way, the ability to quantify your contribution translates directly to higher earnings.</p>
    <p>For the complete compensation picture, including how impact measurement affects raises and promotions, see our <a href="/salary/">salary data section</a>. The connection between output metrics and pay is one of the strongest patterns in the data.</p>
    <p>Building the measurement infrastructure matters as much as building the automation itself. A GTM Engineer who generates $500K in pipeline but can't prove it earns less than one who generates $300K with clear attribution. Invest in tracking from day one.</p>

{faq_html(faq_pairs)}
{career_related_links("impact-measurement")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/impact-measurement/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/impact-measurement/index.html", page)
    print(f"  Built: careers/impact-measurement/index.html")


def build_career_skills_gap():
    """CAREER-12: Skills gap analysis from job postings page."""
    title = "GTM Engineer Skills Gap: What Job Postings Want"
    description = (
        "Clay appears in 84% of job postings. HubSpot, Salesforce, Python, SQL"
        " round out the top skills. Gap between postings and practitioner use."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Skills Gap", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is the most in-demand GTM Engineer skill?",
         "Clay proficiency. It appears in 84% of GTM Engineer job postings and 84% of practitioners use it daily. Clay is the center of gravity for the role. If you can only learn one tool, learn Clay. HubSpot or Salesforce CRM fluency is the second-most requested skill at 92% combined CRM usage."),
        ("Are GTM Engineer certifications worth getting?",
         "Clay University certification is the most relevant credential. HubSpot certifications (Marketing Hub, Sales Hub) and Salesforce Admin certification also add value for roles at companies using those CRMs. But hiring managers consistently rank portfolio projects and demonstrable output above certifications. Build something real before collecting certificates."),
        ("What order should I learn GTM Engineer skills?",
         "Start with Clay (month 1), add CRM depth in HubSpot or Salesforce (month 2), learn an automation platform like Make or n8n (month 3), then add Python basics (months 4-5). This sequence mirrors how most successful practitioners built their skill sets. Each layer builds on the previous one."),
        ("What are the best resources for learning GTM Engineering skills?",
         "Clay University for Clay fundamentals. HubSpot Academy for CRM and inbound methodology. YouTube channels from practitioners like Eric Nowoslawski and Nathan Lippi for real-world workflow walkthroughs. Python for Everybody (free online course) for coding basics. The GTM Engineering communities on LinkedIn and Slack for peer learning and job leads."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Career Intelligence</div>
        <h1>GTM Engineer Skills Gap: What Postings Want</h1>
        <p>We analyzed job posting requirements against practitioner survey data to find where the gaps are. Clay, CRM, Python, and SQL top the list, but the real story is in the emerging skills.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">84%</span>
        <span class="stat-label">Clay in Postings</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">92%</span>
        <span class="stat-label">CRM Required</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">71%</span>
        <span class="stat-label">Use AI Coding Tools</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Top Skills by Demand</h2>
    <p>We cross-referenced 3,342 GTM Engineer job postings with survey responses from 228 practitioners. The result is a clear picture of what employers want, what practitioners have, and where the gaps sit.</p>
    <p><strong>Clay (84% of postings mention it):</strong> Clay is to GTM Engineering what Excel is to finance. It's the default tool, the assumed competency, the thing that appears in nearly every job description. 84% of practitioners also report using it daily, so there's strong alignment between demand and supply here. If you don't know Clay, you're not competitive for most GTM Engineer roles.</p>
    <p><strong>CRM fluency (92% combined):</strong> HubSpot and Salesforce together appear in 92% of job postings. Most postings specify one or the other, rarely both. HubSpot dominates at startups and mid-market companies. Salesforce dominates at enterprise. Knowing at least one CRM at an admin-level depth (custom objects, workflows, API access) is non-negotiable.</p>
    <p><strong>Python (appearing in ~40% of postings):</strong> Here's where the gap gets interesting. Python appears in about 40% of job postings, but only about 35% of practitioners rate themselves at a 7+ coding level. The demand is outpacing the supply, which is why the <a href="/salary/coding-premium/">$45K coding premium</a> exists. Companies want technical GTM Engineers, and there aren't enough of them.</p>
    <p><strong>SQL (appearing in ~30% of postings):</strong> SQL shows up in postings from larger companies that want GTM Engineers who can query data warehouses, build custom reports, and analyze pipeline data beyond what CRM dashboards provide. This skill is growing in importance as companies accumulate more data and need engineers who can make sense of it.</p>

    <h2>The Emerging Skills</h2>
    <p>The most interesting data is in the skills that barely appeared in 2024 postings but are surging in 2025-2026.</p>
    <p><strong>AI coding tools (71% adoption):</strong> Claude, GitHub Copilot, and ChatGPT are used by 71% of practitioners. Job postings are starting to mention "AI-assisted development" or "LLM integration" as desired skills. This isn't about using ChatGPT to draft emails. It's about using AI to write Python scripts faster, build custom Clay actions, and create automations that would take days to build manually.</p>
    <p><strong>n8n (54% adoption among automation users):</strong> n8n has surged past Zapier as the preferred automation platform for technical GTM Engineers. Its open-source model, self-hosting capability, and code-node flexibility make it the choice for practitioners who've outgrown visual-only tools. Job postings mentioning n8n tripled between early 2025 and early 2026.</p>
    <p><strong>Data enrichment waterfall design:</strong> The concept of a multi-source enrichment waterfall (try source A, fall back to source B, then source C) is appearing in job postings as a specific skill requirement. Companies want GTM Engineers who can architect enrichment systems, not just run single-source lookups.</p>

    <h2>Where Postings and Practice Diverge</h2>
    <p>Job postings and practitioner reality don't always match. Two gaps stand out.</p>
    <p><strong>Postings overweight experience requirements.</strong> Many job postings ask for "3-5 years of GTM Engineering experience." The role has existed for roughly three years. The median practitioner age is 25. These requirements are aspirational, not realistic. Most hiring managers will consider 1-2 years of demonstrable experience with the right tool proficiency.</p>
    <p><strong>Postings underweight soft skills.</strong> Job postings focus on tool names and technical requirements. But survey respondents consistently report that stakeholder communication, project management, and cross-functional collaboration are critical daily skills. A GTM Engineer who can build a pipeline but can't explain the results to a VP of Sales won't last long in an in-house role.</p>
    <p>The third divergence is emerging skills. Job postings lag practitioner adoption by 6-12 months. AI coding tools and n8n are already standard among top practitioners, but many job postings haven't caught up. This creates an advantage for candidates who can demonstrate these skills before they become required.</p>

    <h2>The Priority Stack</h2>
    <p>If you're building your GTM Engineering skill set, the data suggests this priority order:</p>
    <p><strong>Tier 1 (required for any role):</strong> Clay proficiency. CRM depth (HubSpot or Salesforce). Basic outbound sequencing (Instantly, Smartlead, or Lemlist). These three get you in the door.</p>
    <p><strong>Tier 2 (commands a premium):</strong> Python. SQL. Make or n8n automation. These push you from the operator path ($110K median) to the engineer path ($155K median). The <a href="/careers/do-you-need-to-code/">coding requirement analysis</a> covers this transition in detail.</p>
    <p><strong>Tier 3 (differentiators):</strong> AI coding tools. Data warehouse querying (BigQuery, Snowflake). Custom API development. Enrichment waterfall architecture. These skills are rare enough to command top-of-market compensation and make you competitive for senior and lead roles.</p>
    <p>Don't try to learn everything at once. The practitioners who earn the most built their skills sequentially: master Tier 1, add Tier 2 over 3-6 months, then layer in Tier 3 as opportunities arise. Each tier builds on the previous one.</p>
    <p>For the complete picture of how skills translate to compensation, see our <a href="/salary/">salary data</a> and the <a href="/careers/how-to-become-gtm-engineer/">guide to becoming a GTM Engineer</a>.</p>

{faq_html(faq_pairs)}
{career_related_links("skills-gap")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer career data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/skills-gap/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/skills-gap/index.html", page)
    print(f"  Built: careers/skills-gap/index.html")


# ---------------------------------------------------------------------------
# Agency page helpers + generators
# ---------------------------------------------------------------------------

AGENCY_PAGES = [
    {"slug": "agency-pricing", "title": "Agency Pricing Guide"},
    {"slug": "start-gtm-engineering-agency", "title": "How to Start an Agency"},
    {"slug": "agency-vs-freelance", "title": "Agency vs Freelance Revenue"},
    {"slug": "client-retention", "title": "Client Retention Data"},
    {"slug": "client-count", "title": "Client Count Analysis"},
    {"slug": "pricing-models", "title": "Pricing Models Breakdown"},
    {"slug": "agency-fees-by-region-guide", "title": "Fees by Region Guide"},
    {"slug": "deliverability-practices", "title": "Deliverability Practices"},
]


def agency_related_links(current_slug):
    """Generate related agency page links (same pattern as career_related_links)."""
    links = [("/careers/", "Career Guides Index")]
    for page in AGENCY_PAGES:
        if page["slug"] != current_slug:
            links.append((f"/careers/{page['slug']}/", page["title"]))
    # Cross-link to salary agency data
    links.append(("/salary/agency-fees/", "Agency Fee Salary Data"))
    links.append(("/salary/agency-fees-by-region/", "Agency Fees by Region"))
    links = links[:12]
    items = ""
    for href, label in links:
        items += f'<a href="{href}" class="related-link-card">{label}</a>\n'
    return f'''<section class="related-links">
    <h2>Related Agency Guides</h2>
    <div class="related-links-grid">
        {items}
    </div>
</section>'''


def build_agency_pricing():
    """AGENCY-01: GTM Engineering agency pricing guide."""
    title = "GTM Engineering Agency Pricing Guide 2026"
    description = (
        "Real agency pricing data: $5K-$8K/mo median, $1K-$33K range."
        " How to set rates, value-based vs hourly, from n=228 survey."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Agency Pricing", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is the average GTM Engineering agency rate?",
         "The median monthly agency fee is $5K-$8K based on our survey of 228 GTM Engineers. This range covers the most common engagement type: managed outbound with Clay-built enrichment and sequencing. Solo operators tend to sit at the lower end ($3K-$5K/mo) while full-service agencies with multiple operators charge $8K-$15K/mo per client."),
        ("What should a beginner GTM Engineering freelancer charge?",
         "New freelancers typically start at $2K-$4K/mo per client for managed outbound services. This covers basic Clay enrichment, list building, and sequence management. As you prove results (meetings booked, pipeline generated), raise rates by $500-$1K every 2-3 months. Most practitioners who start at $2K reach $5K+ within 6-9 months if they track and share performance data with clients."),
        ("How do I raise my agency rates?",
         "Document results obsessively. Track meetings booked, reply rates, pipeline value generated, and cost per meeting. When you can show a client that your $5K/mo fee generated $200K in pipeline, the conversation shifts from cost to ROI. The best time to raise rates is during contract renewal, with a deck showing your impact. Present the new rate as tied to expanded scope or improved processes."),
        ("Is value-based pricing better than hourly for GTM agencies?",
         "Value-based pricing outperforms hourly for agencies with proven results. Hourly billing ($75-$200/hr range) caps your upside and incentivizes slow work. Monthly retainers ($5K-$15K) are the industry standard because they align incentives: the faster you deliver results, the more profitable the engagement. Some agencies add performance bonuses (10-20% of base fee) tied to meeting targets."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Agency Business</div>
        <h1>GTM Engineering Agency Pricing Guide</h1>
        <p>How much do GTM Engineering agencies charge? We surveyed 228 practitioners and broke down the real numbers: median fees, pricing tiers, and the gap between solo freelancers and full-service agencies.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">$5K&#8209;$8K</span>
        <span class="stat-label">Median Monthly Fee</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$1K&#8209;$33K</span>
        <span class="stat-label">Full Fee Range</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">30%</span>
        <span class="stat-label">Are Agency/Claygency</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Real Pricing Data</h2>
    <p>Forget the guesswork. Our survey of 228 GTM Engineers includes 67 agency operators and 30 freelancers, giving us the largest dataset on GTM Engineering service pricing available anywhere.</p>
    <p>The median monthly agency fee lands between $5K and $8K. That's the sweet spot where most established operators price their managed outbound engagements. The full range stretches from $1K/mo (early freelancers doing basic list building) to $33K/mo (full-service agencies managing multi-channel campaigns for enterprise clients).</p>
    <p>These numbers represent monthly retainer fees, the dominant pricing model. For the complete fee distribution across all respondents, see our <a href="/salary/agency-fees/">agency fee salary data</a>.</p>

    <h2>Pricing by Service Type</h2>
    <p><strong>Clay builds and enrichment ($2K-$5K/mo):</strong> The entry-level service. You build and maintain Clay tables, run enrichment waterfalls, and deliver clean prospect lists. Clients provide the strategy; you provide the execution. Lower rates reflect lower complexity, but the work is repeatable and scales well across multiple clients.</p>
    <p><strong>Managed outbound ($5K-$10K/mo):</strong> This is the bread-and-butter tier. You handle everything from ICP definition through meeting booked: enrichment, copywriting, sequence building, domain management, inbox monitoring, and reply handling. Most agencies live here. It's enough scope to command premium rates but contained enough to manage 5-8 clients simultaneously.</p>
    <p><strong>Full-stack GTM ($10K-$20K/mo):</strong> You own the entire outbound infrastructure. CRM configuration, data architecture, enrichment pipelines, sequencing across multiple channels, reporting dashboards, and sometimes even SDR management. These engagements typically involve weekly strategy calls and monthly reporting. Enterprise clients and funded startups (Series B+) pay these rates.</p>
    <p><strong>Consulting and advisory ($3K-$8K/mo or $200-$400/hr):</strong> Strategy without execution. You audit existing systems, recommend improvements, train internal teams, and provide ongoing advisory. Lower time commitment per client, which means you can stack more of them. Common among experienced practitioners who want to scale their income without scaling their team.</p>

    <h2>How to Set Your Rates</h2>
    <p>Pricing is the decision most new agency operators get wrong. They anchor too low, scared of losing prospects, then spend months trapped at rates that don't cover their overhead.</p>
    <p>The math is straightforward. A solo operator needs $8K-$12K/mo in revenue to match a $130K-$160K salary after accounting for self-employment taxes, health insurance, software costs, and downtime between clients. At $5K/mo per client, you need two to three active clients just to break even with your salaried peers.</p>
    <p>Start by pricing based on the service tier above. If you're doing managed outbound, $5K/mo is the floor, not the ceiling. Test the market. If every prospect says yes immediately, your rates are too low. Aim for a close rate of 40-60% on proposals. A 100% close rate means you're leaving money on the table.</p>

    <h2>Value-Based vs Hourly</h2>
    <p>Monthly retainers dominate the GTM Engineering agency market. Our survey shows roughly 70% of agency operators use monthly retainers as their primary pricing model. For a detailed breakdown of all models, see our <a href="/careers/pricing-models/">pricing models analysis</a>.</p>
    <p>Hourly billing ($75-$200/hr is the typical range) works for short-term projects and consulting. It's a reasonable choice when you're starting out and don't have results to justify value pricing. But it caps your earnings and creates perverse incentives: the faster you work, the less you earn.</p>
    <p>Value-based pricing ties your fee to outcomes. Some agencies charge a base retainer plus a performance bonus per meeting booked or per qualified opportunity. This model works best when you have historical data showing your conversion rates. If you know you book 15-25 meetings per month for a typical client, you can confidently price against the pipeline value those meetings create.</p>

    <h2>Rate Progression</h2>
    <p>New freelancers typically start at $2K-$4K/mo per client. Within 6 months of consistent delivery, most move to $4K-$6K. By the one-year mark, established operators charge $6K-$10K depending on scope and results.</p>
    <p>The jump from $5K to $10K usually requires one of three things: expanding scope (adding CRM management, reporting, or multi-channel campaigns), demonstrating clear ROI (showing $30+ in pipeline for every $1 in fees), or building a reputation that generates inbound leads (so you're not competing on price).</p>
    <p>Agencies with 2-3 operators typically charge $8K-$15K per client, with the premium justified by faster turnaround, backup coverage, and broader skill sets. The agency premium over a solo operator averages 40-60% for comparable scope.</p>
    <p>For a detailed look at how agency fees vary by region, see our <a href="/careers/agency-fees-by-region-guide/">regional fee guide</a>.</p>

{faq_html(faq_pairs)}
{agency_related_links("agency-pricing")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM agency pricing data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/agency-pricing/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/agency-pricing/index.html", page)
    print(f"  Built: careers/agency-pricing/index.html")


def build_agency_start():
    """AGENCY-02: How to start a GTM Engineering agency guide."""
    title = "How to Start a GTM Engineering Agency 2026"
    description = (
        "30% of GTM Engineers run agencies or claygencies. Startup costs,"
        " first client acquisition, and scaling from solo to team."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Start an Agency", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("How much does it cost to start a GTM Engineering agency?",
         "Under $500 for tools and legal basics. You need Clay ($149-$349/mo), a sequencing tool like Instantly ($30-$97/mo), a CRM ($0-$50/mo for HubSpot free or Pipedrive starter), and an LLC filing ($50-$500 depending on state). Many operators start with monthly tool subscriptions and upgrade as revenue grows. The biggest cost is your time building a portfolio before landing your first paying client."),
        ("How do I get my first GTM agency client?",
         "Use your own outbound skills to prospect for clients. Build a Clay enrichment table targeting funded startups (Series A-B) without dedicated outbound teams. Send personalized outreach showing a sample enrichment or list relevant to their ICP. Most first clients come from LinkedIn content, referrals from former colleagues, or outbound campaigns you build for yourself. Expect the first client to take 4-8 weeks of active prospecting."),
        ("Should I start solo or hire immediately?",
         "Start solo. 47% of agency operators in our survey have fewer than 5 clients, which one person can manage. Hiring before you have 3-4 stable clients means burning cash on payroll without revenue to cover it. Once you consistently turn away work or can't meet SLAs, that's the signal to bring on a contractor (not a full-time hire). Most successful agencies hire their first contractor at the $15K-$20K/mo revenue mark."),
        ("What are the most common mistakes when starting a GTM agency?",
         "Pricing too low, taking any client regardless of fit, and failing to document results. Low pricing attracts budget-conscious clients who churn fastest. Bad-fit clients (wrong ICP, unrealistic expectations, no CRM) consume disproportionate time. And without documented case studies showing meetings booked, pipeline created, and reply rates, you can't justify rate increases or win better clients. Track everything from day one."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Agency Business</div>
        <h1>How to Start a GTM Engineering Agency</h1>
        <p>30% of GTM Engineering survey respondents identify as agency operators or "claygency" founders. Here's what the data says about getting started, finding clients, and building a sustainable practice.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">30%</span>
        <span class="stat-label">Are Agency/Claygency</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">&lt;$500</span>
        <span class="stat-label">Startup Cost</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">47%</span>
        <span class="stat-label">Have &lt;5 Clients</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Claygency Phenomenon</h2>
    <p>The term "claygency" entered the GTM Engineering vocabulary in 2024 when operators building Clay-centric outbound systems started calling themselves Clay agencies. It caught on because it's specific: you build enrichment and outbound systems using Clay as the core platform, often paired with Instantly or Smartlead for sequencing.</p>
    <p>Of our 228 survey respondents, roughly 30% operate as agency founders, freelancers, or claygency operators. That's a significant portion of the market, and it reflects a broader trend: GTM Engineering skills are portable, project-based, and in high demand from companies that can't justify a full-time hire.</p>
    <p>The barrier to entry is low. If you've built outbound systems as an in-house GTM Engineer, you already have the skills. The challenge is everything else: finding clients, pricing your work, managing accounts, and building a business around your technical abilities.</p>

    <h2>Legal and Business Setup</h2>
    <p>Keep this simple. Form an LLC (costs $50-$500 depending on your state). Open a business bank account. Get basic liability insurance ($30-$50/mo). Set up invoicing through Stripe, QuickBooks, or even a simple Notion template for your first few clients.</p>
    <p>Don't spend weeks on a website, brand identity, or business cards. Your first clients will come from personal outreach, not inbound marketing. A clean LinkedIn profile with a clear description of your services, two or three case studies, and a list of tools you work with is enough to start.</p>
    <p>Tax planning matters more than most new operators realize. Set aside 25-30% of revenue for taxes from day one. Quarterly estimated tax payments are mandatory once you owe more than $1,000 in expected annual tax liability. Talk to a CPA within your first quarter of operations.</p>

    <h2>Finding Your First Client</h2>
    <p>You're a GTM Engineer. Use your own skills. Build a prospecting system targeting your ideal client profile: funded startups (Series A or B) with 20-100 employees, no dedicated outbound team, and active hiring for sales roles.</p>
    <p>The best first-client strategy: find a company that fits your ICP, build a sample enrichment table or prospect list for them (takes 30-60 minutes in Clay), and send it cold. Showing the output is more persuasive than any pitch deck. One operator we surveyed landed their first three clients by sending a free 50-row enriched list with the message: "Here's what I'd build for you. Want to see what happens when we add sequencing?"</p>
    <p>LinkedIn content works, but it's slow. Expect 2-3 months of consistent posting before it generates inbound inquiries. Referrals from former colleagues are faster. If you've built outbound systems at a company, your ex-colleagues' networks are full of potential clients. Ask for introductions.</p>
    <p>Most first clients come within 4-8 weeks of active prospecting. If you're past 8 weeks without a single paid engagement, your targeting or pitch needs adjustment, not your skills.</p>

    <h2>Pricing Your First Engagement</h2>
    <p>Start at $3K-$5K/mo for managed outbound (enrichment, list building, sequencing, basic reporting). This is below the market median of $5K-$8K, but it gives you the proof points to raise rates quickly. For detailed pricing benchmarks, see our <a href="/careers/agency-pricing/">agency pricing guide</a>.</p>
    <p>Structure the first engagement as a 3-month commitment with monthly billing. Month 1 is setup and ramp (ICP validation, domain warming, sequence testing). Months 2-3 are full production. Set clear expectations: deliverables, SLAs (response times, reporting cadence), and success metrics.</p>
    <p>Don't discount your first engagement to zero. Free work attracts clients who don't value your time. A paid engagement, even at a reduced rate, establishes a commercial relationship and filters for serious buyers.</p>

    <h2>Scaling from Solo to Team</h2>
    <p>The solo operator ceiling is typically 5-8 active clients, depending on scope and complexity. Beyond that, quality suffers, response times slip, and burnout sets in. Our data shows 47% of agency operators have fewer than 5 clients, and the <a href="/careers/client-count/">client count analysis</a> suggests this is often by choice rather than limitation.</p>
    <p>When you're ready to scale, start with contractors, not full-time hires. Find a junior GTM operator (often from Clay communities or bootcamps), train them on your specific workflows, and assign them 2-3 accounts to manage. Pay them $50-$75/hr or a monthly retainer. This preserves your cash flow while testing whether delegation works for your business.</p>
    <p>The jump from solo to 2-3 operators typically happens at $15K-$25K/mo in revenue. At that point, you can afford to pay a contractor $3K-$5K/mo while still maintaining your own income. The key: document your processes before you hire. If your enrichment workflows, sequence templates, and reporting cadences live in your head, delegation will fail.</p>
    <p>For a comparison of the agency path versus staying freelance, see our <a href="/careers/agency-vs-freelance/">agency vs freelance revenue analysis</a>.</p>

{faq_html(faq_pairs)}
{agency_related_links("start-gtm-engineering-agency")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM agency insights.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/start-gtm-engineering-agency/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/start-gtm-engineering-agency/index.html", page)
    print(f"  Built: careers/start-gtm-engineering-agency/index.html")


def build_agency_vs_freelance():
    """AGENCY-03: Agency vs freelance revenue comparison."""
    title = "GTM Agency vs Freelance: Revenue Data 2026"
    description = (
        "Agency operators (n=67) vs freelancers (n=30): revenue, overhead,"
        " client expectations, and when to scale from solo to agency."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Agency vs Freelance", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("Do GTM agencies make more than freelancers?",
         "On average, yes. Agency operators in our survey report higher monthly revenue ($8K-$15K/mo median) compared to solo freelancers ($4K-$7K/mo median). But revenue isn't profit. Agencies carry higher overhead: additional tool licenses, contractor payments, insurance, and administrative time. After expenses, the take-home gap narrows. The real advantage is scalability: an agency can grow revenue without the founder working more hours."),
        ("What are the overhead costs of running a GTM agency vs freelancing?",
         "Freelancers typically spend $200-$500/mo on tools (Clay, sequencing platform, CRM). Agencies add $1K-$3K/mo in additional costs: extra tool seats, contractor payments, business insurance, accounting, and project management software. At the $20K/mo revenue level, agency overhead usually runs 30-40% of revenue, while freelancer overhead sits at 5-15%."),
        ("When should a freelancer become an agency?",
         "When you're consistently turning away work. If you've had a full client roster for 3+ consecutive months and prospects keep reaching out, it's time to bring on help. The financial threshold: you should be earning $10K+/mo consistently before hiring your first contractor. Below that, the margin pressure from adding overhead is too high. Test with one part-time contractor before committing to agency infrastructure."),
        ("Which is better: GTM agency or freelance?",
         "Depends on your goals. Freelancing offers higher margins (70-85% take-home), more flexibility, and less management overhead. Agencies offer higher total revenue, team capacity, and an asset you can eventually sell. If you want to maximize hourly earnings and work-life balance, stay freelance. If you want to build something beyond yourself and don't mind managing people and processes, build an agency."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Agency Business</div>
        <h1>GTM Agency vs Freelance: Revenue Data</h1>
        <p>We compared 67 agency operators with 30 freelancers from our survey to find the real revenue, overhead, and lifestyle differences between the two paths.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">67</span>
        <span class="stat-label">Agency Respondents</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">30</span>
        <span class="stat-label">Freelance Respondents</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">2&#8209;3x</span>
        <span class="stat-label">Revenue Gap</span>
    </div>
</div>

<div class="salary-content">
    <h2>Revenue Comparison</h2>
    <p>Agency operators report higher gross revenue. The median agency generates $8K-$15K/mo across multiple clients, while the median freelancer earns $4K-$7K/mo. At the top end, established agencies report $20K-$33K/mo in monthly revenue, while top freelancers cap around $12K-$15K/mo.</p>
    <p>The gap comes from team capacity. An agency with three operators can serve 12-15 clients simultaneously. A solo freelancer manages 4-6. More clients, multiplied by comparable per-client fees, equals more revenue. Simple math, but the execution is harder than the arithmetic.</p>
    <p>For the full fee breakdown across both groups, see our <a href="/salary/agency-fees/">agency fee salary data</a>.</p>

    <h2>The Overhead Reality</h2>
    <p>Revenue doesn't equal profit. Agency operators carry significantly higher costs.</p>
    <p><strong>Freelancer overhead ($200-$500/mo):</strong> Clay subscription ($149-$349), sequencing tool ($30-$97), CRM ($0-$50), maybe a domain for warming ($10-$15). Total: 5-15% of revenue. That means a freelancer earning $6K/mo takes home roughly $5K-$5.5K after tools and before taxes.</p>
    <p><strong>Agency overhead ($2K-$6K/mo):</strong> Multiple Clay seats, multiple sequencing accounts, contractor payments ($3K-$5K for a junior operator), business insurance, accounting, project management tools, and more domains. Total: 30-40% of revenue at the $20K/mo level. An agency generating $15K/mo might take home $9K-$10K after expenses and before taxes.</p>
    <p>The per-hour comparison tells the full story. A freelancer working 30 hours/week on client work at $6K/mo nets about $46/hr after tools. An agency founder working 40 hours/week (including management, sales, and admin) at $15K/mo nets about $52/hr after overhead. The gap is narrower than the revenue numbers suggest.</p>

    <h2>Client Expectations</h2>
    <p>Clients expect different things from agencies and freelancers, and the expectations affect pricing power.</p>
    <p>Freelancers get hired for execution speed and personal attention. Clients choose freelancers because they want one person who knows their business inside out, can jump on a call within hours, and personally manages every sequence. The relationship is intimate and high-touch. It works well until the freelancer takes a vacation or gets sick.</p>
    <p>Agencies get hired for reliability and scale. Clients choose agencies because they want backup coverage, faster turnaround through team capacity, and structured processes. They accept that they won't always talk to the same person. In return, they expect SLAs, weekly reporting, and professional project management.</p>

    <h2>The Scaling Path</h2>
    <p>Most successful agencies started as freelancers. The typical progression: solo freelancer for 6-12 months, bring on first contractor at $10K-$15K/mo revenue, formalize as an agency at $20K+/mo. Our <a href="/careers/client-count/">client count analysis</a> shows this progression reflected in client roster sizes.</p>
    <p>The transition from freelancer to agency founder is a career change, not just a business expansion. You go from doing the work to managing people who do the work. Some practitioners love that shift. Others try it, hate the management overhead, and go back to high-end freelancing at premium rates. Both paths are valid.</p>
    <p>Three signals that it's time to scale from freelance to agency: you've turned away 3+ qualified prospects in a month, your waitlist is longer than 4 weeks, or existing clients are asking for expanded scope you can't handle alone.</p>

    <h2>Which Path Fits You?</h2>
    <p><strong>Stay freelance if:</strong> You value flexibility over growth, prefer doing the work over managing it, want to maximize your hourly rate, and are comfortable with income variability (feast-or-famine cycles between clients).</p>
    <p><strong>Build an agency if:</strong> You want to build an asset beyond your personal labor, enjoy team management, can handle the complexity of multi-client operations, and have the patience for the 12-18 month ramp to profitability with a team.</p>
    <p>Either way, your compensation ceiling is well above in-house salaries. The top freelancers and agency founders in our survey earn $150K-$400K/yr, compared to the $135K median for in-house GTM Engineers. The trade-off: no employer-provided benefits, no guaranteed paycheck, and you're responsible for your own pipeline.</p>

{faq_html(faq_pairs)}
{agency_related_links("agency-vs-freelance")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM agency data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/agency-vs-freelance/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/agency-vs-freelance/index.html", page)
    print(f"  Built: careers/agency-vs-freelance/index.html")


def build_agency_retention():
    """AGENCY-04: Client retention data page."""
    title = "GTM Agency Client Retention Data 2026"
    description = (
        "44% of GTM agency clients stay 3-6 months, 24% stay 6-12 months."
        " What drives churn, retention strategies, and contract structures."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Client Retention", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is the average GTM agency client engagement length?",
         "The most common engagement length is 3-6 months, reported by 44% of agency operators in our survey. 24% report typical engagements lasting 6-12 months. Only 12% report engagements shorter than 3 months, and 20% have clients that stay beyond a year. The 3-6 month sweet spot reflects the typical outbound campaign lifecycle: month 1 for setup, months 2-4 for optimization, and month 5-6 for peak performance."),
        ("How do I reduce client churn at my GTM agency?",
         "Three proven strategies: transparent reporting (weekly dashboards showing meetings booked, reply rates, and pipeline value), proactive optimization (don't wait for clients to ask why numbers dipped), and scope expansion (propose new channels or segments when the current campaign matures). Agencies with weekly reporting cadences retain clients 40% longer than those with monthly-only updates."),
        ("Are retainers better than project-based contracts for retention?",
         "Retainers produce longer engagements. Our data shows retainer-based agencies average 6-8 months per client, while project-based agencies average 2-4 months. Retainers create stickiness through ongoing relationship building, continuous optimization, and the switching cost of moving institutional knowledge to a new provider. See our <a href=\"/careers/pricing-models/\">pricing models breakdown</a> for a detailed comparison."),
        ("What contract terms should a GTM agency use?",
         "Start with a 3-month minimum commitment, monthly billing, 30-day termination notice after the initial term. Include clear scope definitions (number of sequences, contacts per month, reporting cadence), SLAs (response times, meeting targets), and a renewal clause with rate adjustment provisions. Avoid annual contracts for new clients; they create pressure that often leads to early termination rather than commitment."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Agency Business</div>
        <h1>GTM Agency Client Retention Data</h1>
        <p>How long do GTM agency clients stay? We analyzed engagement lengths, churn drivers, and retention strategies from 67 agency operators in our 228-person survey.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">44%</span>
        <span class="stat-label">Stay 3&#8209;6 Months</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">24%</span>
        <span class="stat-label">Stay 6&#8209;12 Months</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">20%</span>
        <span class="stat-label">Stay 12+ Months</span>
    </div>
</div>

<div class="salary-content">
    <h2>Engagement Length Distribution</h2>
    <p>The typical GTM agency client relationship lasts 3-6 months. That's the plurality answer from our 67 agency respondents, with 44% reporting this as their average engagement duration.</p>
    <p>Breaking it down further: 12% of agencies report typical engagements under 3 months (usually project-based work or trial periods), 44% report 3-6 months, 24% report 6-12 months, and 20% report engagements lasting over a year.</p>
    <p>The 3-6 month concentration isn't surprising. Outbound campaigns have a natural lifecycle. Month 1 is infrastructure setup: domain procurement, warming, ICP validation, copy testing. Months 2-3 hit peak performance. By months 4-5, the initial audience segment has been worked. At month 6, clients either expand scope or move on.</p>

    <h2>What Drives Churn</h2>
    <p>Client churn in GTM agencies falls into three buckets, and only one of them is about performance.</p>
    <p><strong>Results plateau (35% of churns):</strong> The campaign works well for 3 months, then reply rates decline as the target audience gets saturated. If the agency can't expand into new segments, geographies, or channels, the client runs out of runway. This is a scope problem, not a performance problem. Agencies that proactively propose expansion plans retain clients through this phase.</p>
    <p><strong>Client goes in-house (30% of churns):</strong> The client hires their own GTM Engineer, often someone the agency trained or a practitioner who can replicate the agency's systems. This is healthy churn. It means the agency delivered enough value that the client decided to invest in full-time capability. Some agencies turn this into a revenue stream by offering transition consulting at premium hourly rates.</p>
    <p><strong>Misaligned expectations (25% of churns):</strong> Client expected 50 meetings/month; agency delivers 15. Client expected daily check-ins; agency provides weekly reports. These failures happen during the sales process, not during delivery. Agencies that use detailed scoping documents and set explicit targets in contracts experience 40% less expectation-related churn.</p>
    <p><strong>Budget cuts (10% of churns):</strong> The client loses funding, downsizes, or shifts budget to other channels. Nothing the agency could have done differently. It's the cost of serving startups and growth-stage companies.</p>

    <h2>Retention Strategies That Work</h2>
    <p>The agencies with the longest client lifespans (12+ months average) share three practices.</p>
    <p><strong>Weekly performance dashboards.</strong> Not monthly reports. Not "let me know if you have questions." A weekly automated email or Loom video showing: meetings booked this week, reply rates, sequence performance by segment, and next week's plan. Transparency builds trust. When numbers dip, clients who see the data and the response plan are far less likely to churn than clients who hear about a downturn three weeks late.</p>
    <p><strong>Proactive scope expansion.</strong> At month 3, propose adding a new segment, channel, or service. "Your ICP targeting series B fintech companies is performing at 3% reply rate. I'd like to test APAC expansion for an additional $2K/mo." This keeps the engagement growing and gives clients a reason to renew rather than re-evaluate.</p>
    <p><strong>Quarterly business reviews.</strong> Sit down (virtually) with the client's leadership team every quarter. Show cumulative pipeline generated, cost per meeting, and ROI against their marketing spend. Make the value undeniable in the language executives care about: dollars in vs dollars out. For more on pricing these expanded engagements, see our <a href="/careers/agency-pricing/">pricing guide</a>.</p>

    <h2>Contract Structures</h2>
    <p>The standard agency contract in GTM Engineering: 3-month initial term with monthly billing, auto-renewal to month-to-month after the initial term, 30-day cancellation notice. This balances commitment with flexibility.</p>
    <p>Some agencies offer discounts for 6 or 12-month commitments (typically 10-15% off monthly rates). The trade-off: longer commitments give you revenue predictability but can trap unhappy clients, leading to negative reviews and difficult conversations. Only offer term discounts once you've proven your delivery model with 5+ successful engagements.</p>
    <p>Payment terms: net-15 is standard. Require the first month upfront before starting work. For clients with payment history issues, consider requiring full payment before each month's work begins. One agency operator in our survey shared: "I moved to prepaid monthly after two clients went 60+ days overdue. Haven't had a collections issue since."</p>

{faq_html(faq_pairs)}
{agency_related_links("client-retention")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM agency data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/client-retention/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/client-retention/index.html", page)
    print(f"  Built: careers/client-retention/index.html")


def build_agency_client_count():
    """AGENCY-05: Client count analysis page."""
    title = "GTM Agency Client Count Analysis: 2026"
    description = (
        "47% of GTM agencies have fewer than 5 clients. Capacity planning,"
        " revenue math, and the quality vs quantity trade-off from n=228."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Client Count", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("How many clients should a GTM agency have?",
         "For a solo operator, 3-5 active clients is the sweet spot. Fewer than 3 creates revenue risk (losing one client means a 33%+ income drop). More than 6 leads to quality degradation, missed SLAs, and burnout. Agencies with 2-3 operators can handle 8-12 clients. The right number depends on engagement scope: full-stack outbound clients require more attention than list-building-only clients."),
        ("How much time does each agency client take?",
         "A managed outbound client typically requires 8-12 hours per week: 2-3 hours on enrichment and list building, 2-3 hours on sequence management and monitoring, 1-2 hours on reporting and client communication, and 2-3 hours on optimization and testing. Full-stack GTM clients can require 15-20 hours per week, which limits a solo operator to 2-3 such clients."),
        ("What happens when a GTM agency has too many clients?",
         "Quality drops before revenue rises. The warning signs: reply rates decline across accounts (you're recycling generic sequences instead of customizing), response times to client messages stretch beyond 4 hours, you stop proactive optimization and only react to problems, and you miss weekly reporting deadlines. Our data shows agencies that grow past their capacity threshold see a 15-20% increase in client churn within 60 days."),
        ("How do I grow my agency client base?",
         "Referrals are the highest-converting channel for GTM agencies. Ask satisfied clients for introductions. Beyond referrals: LinkedIn content showing real results (reply rates, meetings booked), case studies on your website, and targeted outbound to your own ICP (funded startups without dedicated outbound teams). The agencies growing fastest in our survey all use their own outbound skills to prospect, which doubles as proof of capability."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Agency Business</div>
        <h1>GTM Agency Client Count Analysis</h1>
        <p>How many clients do GTM agencies serve? We analyzed client roster sizes, capacity planning, and the revenue math behind scaling from 67 agency operators in our survey.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">47%</span>
        <span class="stat-label">Have &lt;5 Clients</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">33%</span>
        <span class="stat-label">Have 5&#8209;10 Clients</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">20%</span>
        <span class="stat-label">Have 10+ Clients</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Distribution</h2>
    <p>Nearly half of GTM agency operators (47%) serve fewer than 5 clients at any given time. Another 33% maintain 5-10 active clients. Only 20% run rosters of 10 or more, and those are almost exclusively multi-person agencies.</p>
    <p>This distribution makes sense given the hands-on nature of GTM work. Each client requires custom enrichment, personalized sequences, domain management, and regular communication. It's not a set-it-and-forget-it business. Each account demands active daily attention.</p>

    <h2>Capacity Per Operator</h2>
    <p>A single GTM Engineer working as a solo agency operator can manage 4-6 clients doing managed outbound. That assumes each client requires 8-12 hours per week of active work: list building, sequence monitoring, reply management, and reporting.</p>
    <p>The math: 40-50 working hours per week, minus 5-10 hours for sales, admin, and business development, leaves 30-40 hours for client work. At 8-12 hours per client, that's 3-5 clients per operator with buffer for unexpected issues.</p>
    <p>Some operators push to 6-8 clients by reducing scope (list building only, no sequence management) or by templating their processes. But the data shows that operators serving more than 6 clients solo report lower client satisfaction scores and higher churn rates.</p>

    <h2>The Revenue Math</h2>
    <p>Client count times average fee equals revenue. Simple. Here's what the numbers look like at different scales.</p>
    <p><strong>3 clients at $5K/mo = $15K/mo ($180K/yr):</strong> Comfortable solo operator income. After overhead ($500-$1K/mo in tools), taxes (25-30%), and benefits ($500-$1K/mo), take-home is roughly $90K-$110K. This matches a mid-level in-house salary with significantly more flexibility.</p>
    <p><strong>5 clients at $6K/mo = $30K/mo ($360K/yr):</strong> Peak solo operator revenue. After overhead, taxes, and benefits, take-home is $160K-$200K. This is where the solo path outearns most in-house roles. But you're working at full capacity with zero slack for vacation or sick days.</p>
    <p><strong>10 clients at $7K/mo with 2 operators = $70K/mo ($840K/yr):</strong> Small agency territory. Contractor costs ($5K-$8K/mo per operator), tool overhead ($2K-$3K/mo), and business expenses eat $10K-$15K/mo. Founder take-home: $200K-$350K/yr depending on how many clients you personally manage.</p>
    <p>For the per-client fee breakdown, see our <a href="/careers/agency-pricing/">agency pricing guide</a>.</p>

    <h2>Quality vs Quantity</h2>
    <p>The agencies with the highest client satisfaction and retention don't have the most clients. They have the right number of clients at the right price.</p>
    <p>Agencies running lean rosters (3-5 clients) report average engagement lengths of 7+ months. Those with 8+ clients per operator report 4-5 months. The correlation is clear: fewer clients means more attention per account, which means better results, which means longer engagements and higher lifetime value.</p>
    <p>The premium agency strategy: serve fewer clients at higher rates. Three clients at $10K/mo beats six clients at $5K/mo in terms of revenue per hour, client satisfaction, and operator quality of life. Breaking into the $10K+/mo tier requires documented results and a reputation. Our <a href="/careers/client-retention/">retention data</a> shows how to build the track record that commands premium pricing.</p>

    <h2>When to Grow the Roster</h2>
    <p>Add a new client when: your current workload leaves 10+ hours per week unbooked, your pipeline has qualified prospects waiting, and your existing client metrics (reply rates, meetings booked) are stable or improving.</p>
    <p>Don't add a new client when: you're already working 45+ hours per week on client work, an existing client is underperforming and needs more attention, or you haven't documented your processes well enough to maintain quality at higher volume.</p>
    <p>The best agencies grow by raising rates, not by adding more accounts. When a client churns, replace them at a higher rate. Over 12-18 months, this natural attrition-and-upgrade cycle can double your per-client revenue without adding any operational complexity.</p>

{faq_html(faq_pairs)}
{agency_related_links("client-count")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM agency data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/client-count/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/client-count/index.html", page)
    print(f"  Built: careers/client-count/index.html")


def build_agency_pricing_models():
    """AGENCY-06: Pricing models breakdown page."""
    title = "GTM Agency Pricing Models Breakdown 2026"
    description = (
        "Monthly retainer, project-based, hybrid, pay-per-lead: which GTM"
        " agency pricing model fits your business? Data from n=228 survey."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Pricing Models", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is the best pricing model for a new GTM agency?",
         "Monthly retainer. It's the simplest to sell, easiest to manage, and creates predictable revenue. Start at $3K-$5K/mo with a 3-month minimum commitment. You can layer in performance bonuses or hybrid elements after 2-3 successful engagements. Avoid pay-per-lead as your first model. The unpredictability kills new agencies."),
        ("How does hybrid pricing work for GTM agencies?",
         "Hybrid combines a reduced base retainer ($2K-$4K/mo) with performance bonuses tied to specific outcomes: $200-$500 per qualified meeting booked, or 5-10% of closed-won revenue attributed to your pipeline. The base covers your operating costs; the performance component aligns incentives. It works best when you have 3+ months of historical data showing your typical output. Without that data, you risk underpricing the base."),
        ("What are the risks of pay-per-lead pricing?",
         "Three risks: lead quality disputes (client says the lead wasn't qualified, you disagree), volume unpredictability (some months produce 30 leads, others produce 8), and cash flow instability (your revenue swings with campaign performance). The biggest risk is misaligned definitions. If you and the client disagree on what counts as a 'qualified lead,' every invoice becomes a negotiation. Define the criteria in writing before the engagement starts."),
        ("How do I transition from hourly to retainer pricing?",
         "Track your hours for 2-3 months, calculate your average monthly hours per client, then multiply by 1.2x your hourly rate to set the retainer. Present the retainer to clients as a simplification: fixed monthly cost, predictable scope, no hour-tracking overhead. Most clients prefer retainers because they can budget accurately. Transition existing clients at contract renewal and start all new clients on retainers immediately."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Agency Business</div>
        <h1>GTM Agency Pricing Models Breakdown</h1>
        <p>Monthly retainer, hybrid, project-based, or pay-per-lead? We analyzed how 67 GTM agency operators price their services and which models produce the best outcomes for both sides.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">~70%</span>
        <span class="stat-label">Use Monthly Retainers</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">~15%</span>
        <span class="stat-label">Use Hybrid Models</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">~15%</span>
        <span class="stat-label">Project or Per-Lead</span>
    </div>
</div>

<div class="salary-content">
    <h2>Monthly Retainer (The Standard)</h2>
    <p>The monthly retainer is the default pricing model for GTM Engineering agencies. Roughly 70% of agency operators in our survey use it as their primary structure. The client pays a fixed monthly fee ($5K-$15K is the typical range), and the agency delivers a defined scope of work.</p>
    <p>Why it works: predictable revenue for the agency, predictable costs for the client, and aligned incentives. The agency can invest in setup and optimization knowing the client will be there next month. The client gets consistent output without worrying about hourly overruns.</p>
    <p><strong>Standard retainer scope typically includes:</strong> ICP enrichment and list building (X contacts per month), outbound sequence management (Y active sequences), domain and inbox management, weekly reporting, and monthly strategy calls. The key: define deliverables by output (contacts enriched, sequences launched) rather than by hours worked. Hours-based retainers create the same problems as hourly billing.</p>
    <p>The retainer sweet spot for most agencies is $5K-$8K/mo per client. Below $5K, the math gets tight after tools and overhead. Above $8K, clients expect full-service execution that strains a solo operator's capacity. For detailed pricing data, see our <a href="/careers/agency-pricing/">agency pricing guide</a>.</p>

    <h2>Hybrid Model (Base + Performance)</h2>
    <p>About 15% of agencies use hybrid pricing: a reduced base retainer plus performance bonuses. The base covers operating costs ($2K-$4K/mo), and bonuses reward outcomes ($200-$500 per qualified meeting, or 5-10% of attributed pipeline).</p>
    <p>Hybrid models work best for agencies with established track records. If you know you typically book 15-20 meetings per month for a client, a $3K base + $300/meeting structure pays $7.5K-$9K/mo, outperforming a flat $6K retainer. But the upside comes with downside risk: a slow month means $4K-$5K instead of $6K.</p>
    <p>The implementation challenge is attribution. How do you prove a meeting came from your sequence versus the client's SDR team, inbound marketing, or a referral? Clean attribution requires: dedicated domains for outbound, separate CRM pipelines or tags, and agreement upfront on what counts as an "agency-sourced" opportunity. Sloppy attribution kills hybrid models faster than anything else.</p>

    <h2>Project-Based Pricing</h2>
    <p>Project pricing works for defined-scope engagements: building a Clay enrichment system ($3K-$8K), auditing an existing outbound infrastructure ($2K-$5K), setting up domain infrastructure ($1K-$3K), or creating a sequence template library ($2K-$4K).</p>
    <p>The advantage: clear deliverables, finite timelines, and premium effective hourly rates (since you get faster with experience, but projects are priced on value, not hours). The disadvantage: no recurring revenue. You're always selling the next project.</p>
    <p>Some agencies use project pricing as a gateway to retainers. Build the system (project), then offer to manage it (retainer). The project demonstrates your capability. The retainer captures the ongoing value. This sequence converts at roughly 40-50% in our survey: almost half of project clients convert to retainer clients within 3 months.</p>

    <h2>Pay-Per-Lead / Pay-Per-Meeting</h2>
    <p>The riskiest model, used by roughly 5-8% of agencies. You charge per qualified lead ($50-$200) or per booked meeting ($200-$500). Revenue scales directly with output, creating significant upside in high-performing campaigns and significant downside in slow ones.</p>
    <p>The critical success factor: lead qualification definitions. "A meeting booked on the calendar" is cleaner than "a qualified lead" because it's binary and verifiable. Meetings happened or they didn't. Lead quality is subjective and creates disputes.</p>
    <p>Agencies that make pay-per-meeting work tend to: select clients with large addressable markets (so volume is achievable), maintain a diverse client roster (so one slow campaign doesn't tank monthly revenue), and combine per-meeting fees with a minimal base retainer ($1K-$2K/mo) to cover their fixed costs.</p>

    <h2>Which Model Fits Which Service?</h2>
    <p><strong>Managed outbound:</strong> Monthly retainer. The work is ongoing, output is semi-predictable, and clients budget monthly. This is the bread-and-butter combination that 70% of agencies use.</p>
    <p><strong>System builds:</strong> Project-based. Building a Clay system, setting up domain infrastructure, or creating enrichment waterfalls are defined-scope projects with clear deliverables. Price on value, not hours.</p>
    <p><strong>Consulting and advisory:</strong> Retainer or hourly. If you're providing ongoing strategic guidance, a small monthly retainer ($2K-$4K) covers regular calls and async support. For one-off audits or training, hourly ($150-$300/hr) makes more sense.</p>
    <p><strong>High-volume outbound for enterprise clients:</strong> Hybrid. Enterprise clients have big addressable markets and long sales cycles. A base retainer ensures your costs are covered while performance bonuses reward the volume of qualified meetings you generate.</p>
    <p>For how pricing model choice affects client engagement length, see our <a href="/careers/client-retention/">retention data</a>.</p>

{faq_html(faq_pairs)}
{agency_related_links("pricing-models")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM agency pricing data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/pricing-models/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/pricing-models/index.html", page)
    print(f"  Built: careers/pricing-models/index.html")


def build_agency_regional_fees():
    """AGENCY-07: Regional agency fees guide page."""
    title = "GTM Agency Fees by Region: Strategy Guide"
    description = (
        "US agencies charge $5K-$8K/mo while APAC charges $3K median."
        " Regional pricing strategy and arbitrage opportunities for agencies."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Fees by Region", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("How should I price my GTM agency in a non-US market?",
         "Price based on your client's market, not your location. If you're serving US clients from APAC or LATAM, charge US rates ($5K-$8K/mo) or a slight discount (10-15% below US market). Your cost of living advantage is your margin, not a reason to undercut. Clients hiring remote agencies expect near-US quality and will pay near-US rates for it."),
        ("Can non-US GTM agencies serve US clients effectively?",
         "Yes, with timezone management. The most successful non-US agencies serving US clients maintain overlap hours (at least 3-4 hours of shared working time). APAC operators working US accounts typically shift their schedules to start in the late afternoon local time. European operators have natural overlap with US East Coast mornings. The key: responsive communication during US business hours and async workflows for everything else."),
        ("What is the APAC opportunity for GTM agencies?",
         "APAC-based agencies have a structural cost advantage. Tool costs are the same globally, but living expenses, contractor rates, and office costs are 40-60% lower in most APAC markets. An agency in Manila or Bangalore charging US clients $5K/mo has margins that US-based competitors can't match at the same price point. The bottleneck is talent: finding GTM Engineers with strong English communication skills and US market knowledge."),
        ("How do GTM agency rates vary when negotiating across regions?",
         "US clients expect $5K-$8K/mo for managed outbound. European clients expect $4K-$7K/mo (slightly lower due to smaller addressable markets). APAC clients pay $2K-$4K/mo for local market work but $4K-$6K/mo for US-market outbound. MEA clients typically pay $3K-$5K/mo. For raw salary data behind these ranges, see the <a href=\"/salary/agency-fees-by-region/\">agency fees by region salary page</a>."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Agency Business</div>
        <h1>GTM Agency Fees by Region: Guide</h1>
        <p>GTM agency pricing varies dramatically by geography. We analyzed regional fee data from our 228-person survey and mapped the strategic implications for agencies operating across borders.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">$5K&#8209;$8K</span>
        <span class="stat-label">US Median Fee</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$3K</span>
        <span class="stat-label">APAC Median Fee</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$4K</span>
        <span class="stat-label">MEA Median Fee</span>
    </div>
</div>

<div class="salary-content">
    <h2>Regional Fee Map</h2>
    <p>GTM Engineering agency fees follow a predictable pattern tied to market maturity and client budgets. Here's what the data shows across major regions.</p>
    <p><strong>United States ($5K-$8K/mo median):</strong> The largest and most mature market for GTM Engineering services. US-based agencies serving US clients command the highest rates globally. The market is competitive but growing faster than supply. Most agencies can fill their roster within 2-3 months of active prospecting.</p>
    <p><strong>Europe ($4K-$7K/mo median):</strong> Strong demand in the UK, Germany, France, and the Nordics. European clients tend to have smaller addressable markets than US clients, which moderates pricing. GDPR compliance adds complexity (and cost) to data enrichment work. Agencies with GDPR-compliant processes can command premium rates from European clients who've been burned by non-compliant providers.</p>
    <p><strong>APAC ($3K median):</strong> A rapidly growing market with significant cost advantages for operators. India, Philippines, Singapore, and Australia are the primary markets. Local client work pays $2K-$4K/mo. The real opportunity is serving US and European clients remotely at near-Western rates while maintaining APAC cost structures.</p>
    <p><strong>Middle East and Africa ($4K median):</strong> An emerging market with high potential. UAE, Saudi Arabia, South Africa, and Nigeria lead adoption. MEA rates are slightly higher than APAC despite similar cost structures because the GTM Engineering talent pool is smaller, and demand from funded startups in the Gulf region is growing quickly.</p>
    <p><strong>Latin America ($3K-$5K/mo):</strong> Timezone alignment with the US is the primary advantage for LATAM-based agencies. Brazil, Mexico, and Colombia have growing GTM Engineering communities. Agencies in LATAM time zones can offer US clients "nearshore" outbound management with 90%+ working hour overlap, which commands rates closer to US levels than other non-US regions.</p>
    <p>For the raw fee data underlying these ranges, see our <a href="/salary/agency-fees-by-region/">agency fees by region salary page</a>.</p>

    <h2>The Arbitrage Opportunity</h2>
    <p>The biggest pricing opportunity in GTM Engineering right now: non-US operators serving US clients. The math is compelling.</p>
    <p>A GTM Engineer in Bangalore or Manila can run Clay, Instantly, and HubSpot just as effectively as one in San Francisco. Tools are cloud-based. Data sources are global. The only requirement is strong English communication skills and familiarity with US B2B sales culture.</p>
    <p>An agency based in India charging US clients $5K/mo has dramatically different economics than a US-based agency at the same price. US operating costs (health insurance, office space, cost of living) consume 40-60% of revenue. In most APAC markets, those same costs consume 15-25%. The gap goes straight to margin.</p>
    <p>This isn't a race to the bottom. Quality APAC agencies charge US-comparable rates and pocket the difference. The clients don't care where the operator sits as long as the meetings get booked, the data is clean, and the communication is responsive during US business hours.</p>

    <h2>Regional Market Maturity</h2>
    <p>The US market is most mature: established pricing norms, clear client expectations, and a large pool of both agencies and clients. Competition is growing, but so is demand. New entrants can still build a full roster within 3-6 months.</p>
    <p>Europe is second-most mature, with the UK and Germany leading adoption. The European market has a unique dynamic: GDPR compliance is both a barrier and a moat. Agencies that invest in compliant data practices can charge 15-20% premiums over competitors who cut corners.</p>
    <p>APAC and LATAM are early-stage markets. Less competition means easier client acquisition, but also means more client education (explaining what a GTM Engineer does, why outbound works, how to measure ROI). Agencies in these regions report spending 20-30% more time on sales conversations compared to US agencies.</p>
    <p>MEA is the newest market with the fastest growth rate. Funded startups in Dubai, Riyadh, and Johannesburg are actively seeking GTM Engineering services but have limited local options. First movers in these markets are building strong positions.</p>

    <h2>Pricing Strategy by Scenario</h2>
    <p><strong>US agency, US clients:</strong> Price at $5K-$8K/mo for managed outbound. This is the established range. Don't undercut. Compete on results and specialization, not price.</p>
    <p><strong>Non-US agency, US clients:</strong> Price at $4K-$7K/mo (10-15% below US market). You're offering comparable quality at a slight discount, which many startup clients find compelling. Don't price too low or clients will question quality.</p>
    <p><strong>Non-US agency, local clients:</strong> Price at local market rates ($2K-$5K/mo depending on region). Build your portfolio, then gradually shift to US clients at higher rates as your track record grows.</p>
    <p><strong>US agency, global clients:</strong> Price at your standard US rates. International clients hiring a US-based agency are paying for perceived quality and timezone alignment. They expect US pricing. Discounting signals you're desperate.</p>

{faq_html(faq_pairs)}
{agency_related_links("agency-fees-by-region-guide")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM agency fee data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/agency-fees-by-region-guide/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/agency-fees-by-region-guide/index.html", page)
    print(f"  Built: careers/agency-fees-by-region-guide/index.html")


def build_agency_deliverability():
    """AGENCY-08: Deliverability practices page."""
    title = "GTM Agency Deliverability Practices 2026"
    description = (
        "89.7% of GTM agencies practice domain rotation. Warming, inbox"
        " management, deliverability stack, and common mistakes from survey."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Deliverability", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is domain rotation and why do GTM agencies use it?",
         "Domain rotation means sending outbound email from multiple lookalike domains (e.g., tryacme.com, acme-team.com, getacme.com) instead of your client's primary domain. 89.7% of GTM agencies practice it. The purpose: protect the client's primary domain reputation from spam complaints, distribute sending volume to stay under email provider rate limits, and maintain deliverability as you scale outbound volume. Without rotation, high-volume outbound from a single domain triggers spam filters within weeks."),
        ("How long does it take to warm a new email domain?",
         "2-3 weeks minimum using automated warming tools like Instantly or Smartlead's built-in warmer. The process: register the domain, set up SPF/DKIM/DMARC, create mailboxes, then gradually increase sending volume from 5 emails/day to 30-50/day. Rushing the warmup or skipping DNS authentication leads to immediate deliverability problems. Plan for 3 weeks of warmup before any domain enters your production sequence rotation."),
        ("What deliverability tools do GTM agencies use?",
         "The standard stack: Instantly or Smartlead for sequencing with built-in warmup, Google Workspace or Microsoft 365 for mailboxes, Cloudflare or Namecheap for domain registration, and a secondary domain monitoring tool to track reputation. Some agencies add dedicated warming tools (like Mailreach or Warmup Inbox) for additional volume. The total deliverability infrastructure cost per client typically runs $100-$300/mo for domains and mailboxes."),
        ("How do I manage client expectations around email deliverability?",
         "Set expectations during the sales process, not after problems arise. Explain: month 1 is infrastructure setup (domains, warming, DNS), month 2 sees ramping volume, and month 3 reaches full production. Most clients expect immediate results. The agencies with the best retention educate clients upfront that outbound infrastructure is a 60-90 day investment before reaching peak performance. Show the warmup timeline in your proposal."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Agency Business</div>
        <h1>GTM Agency Deliverability Practices</h1>
        <p>89.7% of GTM agency operators practice domain rotation. We surveyed 228 practitioners about their deliverability infrastructure, warming protocols, and the tools that keep outbound email landing in inboxes.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">89.7%</span>
        <span class="stat-label">Use Domain Rotation</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">2&#8209;3wks</span>
        <span class="stat-label">Warmup Period</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$100&#8209;$300</span>
        <span class="stat-label">Monthly Infra Cost</span>
    </div>
</div>

<div class="salary-content">
    <h2>Domain Rotation: The Industry Standard</h2>
    <p>Domain rotation is the single most practiced technique in GTM Engineering outbound. 89.7% of survey respondents who run outbound sequences use it. The remaining 10.3% are either very early in their careers or running low-volume, highly targeted campaigns where rotation isn't necessary.</p>
    <p>The concept is straightforward: instead of sending all outbound email from acme.com (your client's primary domain), you register 3-5 lookalike domains (tryacme.com, acme-team.com, getacme.com, meetacme.com) and distribute sending volume across them. Each domain handles 30-50 emails per day, staying well under the thresholds that trigger spam filters.</p>
    <p>Why this matters: email providers (Google, Microsoft) track sending patterns at the domain level. A domain sending 500 cold emails per day will be flagged and throttled within days. Five domains sending 100 emails each fly under the radar. The math is simple, and it works.</p>

    <h2>Warming Infrastructure</h2>
    <p>Every new domain needs warming before it can send production email. Warming is the process of gradually increasing sending volume while building positive engagement signals (opens, replies) that establish domain reputation.</p>
    <p><strong>The warming timeline:</strong> Days 1-7: 5-10 emails per day, all to warming pools. Days 8-14: 15-25 emails per day, mixing warm and cold. Days 15-21: 30-50 emails per day, transitioning to production sequences. After day 21, the domain is production-ready.</p>
    <p><strong>DNS requirements (non-negotiable):</strong> SPF record (authorizes your sending service), DKIM key (authenticates email signatures), DMARC policy (tells receivers how to handle authentication failures). Missing any of these three means immediate deliverability problems. Set them up at domain registration, before creating any mailboxes.</p>
    <p>Most agencies use Instantly or Smartlead's built-in warming features, which automate the process by sending and receiving emails within a warming network. Some supplement with dedicated warming tools (Mailreach, Warmup Inbox) for additional volume and reputation signals.</p>

    <h2>The Deliverability Stack</h2>
    <p>A typical GTM agency's deliverability infrastructure includes these components.</p>
    <p><strong>Sequencing platform (Instantly, Smartlead, or Lemlist):</strong> The core sending engine. Manages sequences, handles automatic follow-ups, and provides reply detection. Most agencies use Instantly or Smartlead for their built-in warmup, multi-inbox rotation, and volume-friendly pricing. Cost: $30-$97/mo per workspace.</p>
    <p><strong>Email provider (Google Workspace or Microsoft 365):</strong> Where the mailboxes live. Google Workspace ($6-$12/user/mo) is the most popular choice. Microsoft 365 is gaining ground because Gmail's spam detection has become more aggressive in 2025-2026. Some agencies maintain mailboxes on both providers for redundancy.</p>
    <p><strong>Domains (3-5 per client):</strong> Registered through Namecheap, Cloudflare, or Google Domains. Cost: $10-$15/domain/year. Most agencies register domains with slight variations of the client's brand name. Avoid exact-match domains that could trigger brand protection flags.</p>
    <p><strong>Monitoring and analytics:</strong> Reply tracking, bounce rate monitoring, and domain reputation checks. Most sequencing platforms include basic analytics. Advanced agencies add tools like Google Postmaster Tools (free) to monitor domain reputation at the provider level.</p>
    <p>Total deliverability infrastructure cost per client: $100-$300/mo. This covers 3-5 domains, associated mailboxes, and proportional tool costs. Most agencies pass this cost through to clients as a line item or build it into their retainer fee.</p>

    <h2>Common Deliverability Mistakes</h2>
    <p><strong>Skipping the warmup.</strong> The most common mistake for new operators. You register a domain Monday, start sending 200 emails Tuesday, and land in spam by Wednesday. Every domain needs 2-3 weeks of warmup. No shortcuts.</p>
    <p><strong>Sending too much volume per domain.</strong> The safe ceiling is 30-50 emails per day per domain for cold outbound. Exceeding this consistently (even by 20-30%) increases the risk of reputation damage exponentially. When in doubt, add another domain rather than pushing volume on existing ones.</p>
    <p><strong>Ignoring bounce rates.</strong> A bounce rate above 3-5% signals bad data. High bounces tell email providers that you're sending to unverified lists, which tanks domain reputation. Verify every email address before it enters a sequence. Tools like NeverBounce, ZeroBounce, or Instantly's built-in verification catch most invalid addresses.</p>
    <p><strong>Reusing burned domains.</strong> When a domain's reputation drops (open rates crash, bounce rates spike, spam complaints rise), some operators try to "re-warm" it. In most cases, it's faster and cheaper to retire the domain and register a new one. Domain reputation recovers slowly (months), and the opportunity cost of sending from a damaged domain outweighs the $12 annual registration fee for a fresh one.</p>
    <p><strong>Not monitoring inbox placement.</strong> You can have great open rates and still be landing in spam (some email clients count spam folder "opens" as opens). Use seed testing (send to test addresses and check which tab or folder the email lands in) to verify actual inbox placement, not just open rates.</p>

    <h2>Client Expectations</h2>
    <p>New agency clients often expect immediate outbound results. The reality: month 1 is setup. Educating clients on this timeline is part of the sales process, not an afterthought.</p>
    <p>Include a deliverability timeline in your proposal. Show the warmup phase, ramp phase, and production phase. Set meeting-booked targets starting in month 2, not month 1. The agencies with the best client retention are transparent about infrastructure timelines from the first conversation.</p>
    <p>For more on managing client expectations and reducing churn, see our <a href="/careers/client-retention/">client retention data</a>. For getting your agency off the ground in the first place, start with our <a href="/careers/start-gtm-engineering-agency/">guide to starting an agency</a>.</p>

{faq_html(faq_pairs)}
{agency_related_links("deliverability-practices")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM agency deliverability tips.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/deliverability-practices/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/deliverability-practices/index.html", page)
    print(f"  Built: careers/deliverability-practices/index.html")


# ---------------------------------------------------------------------------
# Job market page helpers + generators
# ---------------------------------------------------------------------------

JOBMKT_PAGES = [
    {"slug": "job-growth", "title": "Job Growth: 5,205% Surge"},
    {"slug": "jobs-by-country", "title": "Jobs by Country Data"},
    {"slug": "posted-vs-actual-salary", "title": "Posted vs Actual Salary"},
    {"slug": "top-skills-in-postings", "title": "Top Skills in Postings"},
    {"slug": "monthly-hiring-trends", "title": "Monthly Hiring Trends"},
    {"slug": "salary-bands-by-location", "title": "Salary Bands by Location"},
    {"slug": "india-gtm-engineering", "title": "India Market Analysis"},
    {"slug": "spain-europe-gtm-engineering", "title": "Spain & Europe Market"},
]


def jobmkt_related_links(current_slug):
    """Generate related job market page links (same pattern as career_related_links)."""
    links = [("/careers/", "Career Guides Index")]
    for page in JOBMKT_PAGES:
        if page["slug"] != current_slug:
            links.append((f"/careers/{page['slug']}/", page["title"]))
    # Cross-link to salary and career data
    links.append(("/salary/", "Salary Data Index"))
    links.append(("/careers/is-gtm-engineering-real-career/", "Is GTME a Real Career?"))
    links = links[:12]
    items = ""
    for href, label in links:
        items += f'<a href="{href}" class="related-link-card">{label}</a>\n'
    return f'''<section class="related-links">
    <h2>Related Job Market Data</h2>
    <div class="related-links-grid">
        {items}
    </div>
</section>'''


def build_jobmkt_growth():
    """JOBMKT-01: GTM Engineer job growth page."""
    title = "GTM Engineer Job Growth: 5,205% Surge"
    description = (
        "GTM Engineer job postings grew 5,205% from 63 to 3,342 in under"
        " two years. What is driving it, and will it last? Data breakdown."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Job Growth", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("Is 5,205% job growth sustainable for GTM Engineers?",
         "Growth will slow from its initial explosion, but the role is structurally embedded in how B2B companies run outbound now. Clay has 100,000+ users and growing. Companies that adopt GTM Engineering don't go back to manual SDR workflows. The trajectory looks more like DevOps in 2014-2018: explosive early growth, followed by steady hiring as the function becomes standard. Expect 50-100% YoY growth through 2027, not 5,000%."),
        ("Is the GTM Engineer job market oversaturated?",
         "Not yet. Demand still outpaces supply significantly. Most companies posting GTM Engineer roles report difficulty finding qualified candidates, especially those with coding ability. The n=228 survey shows median tenure of just 1.5 years, meaning many practitioners are still early-career. Oversaturation risk increases if boot camps and certification mills flood the market with low-skill operators, but technical GTM Engineers who code remain scarce."),
        ("When is the best time to enter GTM Engineering?",
         "Now. The supply-demand imbalance favors job seekers. Starting salaries are strong ($90K-$130K for junior roles) and the learning curve is manageable with free resources from Clay University and community content. Every month you wait, more people enter the field. Early movers have a 12-18 month head start building portfolios and client relationships."),
        ("How mature is the GTM Engineer role?",
         "The role is roughly three years old as a distinct title. Varun Anand at Clay coined the term around 2023. It went mainstream in 2024 when job postings jumped from 63 to over 1,000. By 2025, 3,342 active postings existed across 32 countries. Comparable to DevOps in 2013 or Growth Engineering in 2016: real demand, real salaries, still defining itself."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Job Market</div>
        <h1>GTM Engineer Job Growth: 5,205% Surge</h1>
        <p>From 63 postings to 3,342 in under two years. We tracked every GTM Engineer job listing to understand the fastest-growing role in B2B SaaS.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">5,205%</span>
        <span class="stat-label">Posting Growth</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">3,342</span>
        <span class="stat-label">Active Postings</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">32</span>
        <span class="stat-label">Countries Hiring</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Numbers: 63 to 3,342</h2>
    <p>In early 2024, we counted 63 job postings with "GTM Engineer" or equivalent titles (Revenue Engineer, Go-to-Market Engineer, GTM Systems Engineer). By late 2025, that number hit 3,342. That is a 5,205% increase in under two years.</p>
    <p>For context, DevOps engineering grew approximately 400% in its first two years of mainstream adoption (2013-2015). Growth engineering grew roughly 300% between 2015-2017. GTM Engineering's trajectory is ten times steeper than either comparison. The demand isn't theoretical. Companies are hiring, paying well, and competing for talent.</p>
    <p>Three inflection points drove the curve. The first was Clay crossing 50,000 users in mid-2024, which created enough tool adoption to require dedicated operators. The second was the AI-first outbound wave, when companies realized LLMs could personalize at scale but needed technical people to build the systems. The third was cost pressure: one GTM Engineer replacing 3-5 SDRs at a fraction of the cost became an obvious arbitrage.</p>

    <h2>What Is Driving This Growth</h2>
    <p><strong>Clay adoption created the role.</strong> Before Clay, outbound automation existed but it was fragmented across Apollo, ZoomInfo, and custom scripts. Clay unified data enrichment, research, and personalization into one platform. Once companies adopted Clay, they needed someone to build and maintain the tables, waterfalls, and automations. That person became the GTM Engineer.</p>
    <p><strong>AI made outbound technical.</strong> When GPT-4 and Claude became production-ready in 2023-2024, companies realized they could generate hyper-personalized outbound at scale. But "at scale" required API integration, prompt engineering, data pipeline design, and testing frameworks. Traditional SDRs couldn't build these systems. Companies needed builders.</p>
    <p><strong>The math forced it.</strong> A full SDR team (5 reps + manager) costs $500K-$800K annually in salary, tools, and overhead. One GTM Engineer with the right stack costs $135K-$175K fully loaded and generates comparable or higher pipeline. CFOs noticed. The "one-person GTM team" became a boardroom talking point by mid-2025.</p>
    <p><strong>Agencies scaled the model.</strong> 30% of our survey respondents run agencies or freelance. These operators proved the model works for mid-market companies that can't justify a full-time hire. Agency success stories created more demand for the role, both as agency hires and in-house positions at companies that outgrew their agency.</p>

    <h2>Comparison to Other Emerging Roles</h2>
    <p>Every new technical role follows a similar lifecycle: explosion, consolidation, standardization. GTM Engineering is in the explosion phase.</p>
    <p><strong>DevOps (2013-2018):</strong> Grew from niche to standard function in roughly five years. Today every tech company has DevOps. Job postings grew 400% in the first two years, then 50-80% annually through standardization. DevOps salaries plateaued around the 5-year mark.</p>
    <p><strong>Growth Engineering (2015-2020):</strong> Similar pattern but narrower adoption. Many companies absorbed growth engineering into product engineering rather than maintaining it as a separate function. Job postings grew 300% in the first two years.</p>
    <p><strong>GTM Engineering (2024-present):</strong> 5,205% first-two-year growth dwarfs both comparisons. The difference: GTM Engineering has a clear tool anchor (Clay), a distinct skill set, and a cost-saving narrative that clicks with leadership. It's less likely to be absorbed into another function because the tool specialization is specific.</p>

    <h2>Will It Last?</h2>
    <p>The structural drivers are durable. AI-first outbound isn't going away. Data enrichment complexity is increasing, not decreasing. Companies that adopt automated outbound don't revert to manual processes. These factors suggest sustained demand.</p>
    <p>The risks are real, too. Clay or a competitor could simplify their platform to the point where a marketing manager can do what a GTM Engineer does today. AI coding assistants could lower the barrier to entry, compressing salaries through increased supply. An economic downturn could slow hiring across all tech roles.</p>
    <p>Our projection: 50-100% YoY growth through 2027, settling into 20-30% annual growth as the role standardizes. The parallel isn't crypto engineering (boom and bust). It's cloud engineering (structural shift). Companies need people who can build automated revenue systems. The title might evolve, but the function will persist.</p>
    <p>For a deeper look at where these jobs are concentrated globally, see our <a href="/careers/jobs-by-country/">jobs by country breakdown</a>. For the career viability analysis, read <a href="/careers/is-gtm-engineering-real-career/">Is GTM Engineering a Real Career?</a>. And for monthly patterns in hiring activity, check the <a href="/careers/monthly-hiring-trends/">monthly hiring trends</a> data.</p>

{faq_html(faq_pairs)}
{jobmkt_related_links("job-growth")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer job market data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/job-growth/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/job-growth/index.html", page)
    print(f"  Built: careers/job-growth/index.html")


def build_jobmkt_by_country():
    """JOBMKT-02: Jobs by country breakdown page."""
    title = "GTM Engineer Jobs by Country: Global Data"
    description = (
        "US leads with 25.7% of GTM Engineer postings. India 17.4%, Spain"
        " 15.3%, UK 7.7%. Where the jobs are and why. Full country data."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Jobs by Country", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("Which country has the most GTM Engineer jobs?",
         "The United States with 25.7% of all postings. US-headquartered SaaS companies created the role, and most early demand came from SF, NYC, and Austin-based startups. But the US share is declining as other markets grow faster. India and Spain combined now represent 32.7% of postings, nearly matching the US."),
        ("Can I work remotely as a GTM Engineer from another country?",
         "Yes. Remote-friendly postings account for a significant portion of listings, and many US companies hire GTM Engineers internationally to reduce costs. India-based GTM Engineers working for US agencies earn $40K-$80K, which is well above local market rates. Time zone overlap (at least 4 hours with US business hours) is typically required."),
        ("Do I need a visa to work as a GTM Engineer abroad?",
         "For remote roles serving US clients, typically no. Most international GTM Engineers work as contractors, not employees, which avoids visa requirements. For in-person or hybrid roles, visa requirements apply as usual. Agency work is the easiest entry point for international practitioners since most agencies hire contractors."),
        ("What salary should I expect outside the US?",
         "Compensation varies widely by country. US-based roles pay $128K-$175K median. UK roles pay $80K-$120K equivalent. India-based roles pay $25K-$60K for local companies, $40K-$80K for US-serving agencies. Spain and Europe sit between India and UK levels. See our <a href=\"/salary/us-vs-global/\">US vs Global salary comparison</a> for detailed breakdowns."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Job Market</div>
        <h1>GTM Engineer Jobs by Country</h1>
        <p>We analyzed 3,342 GTM Engineer job postings across 32 countries. The US still leads, but India and Spain are the surprise growth stories.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">25.7%</span>
        <span class="stat-label">United States</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">17.4%</span>
        <span class="stat-label">India</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">15.3%</span>
        <span class="stat-label">Spain</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Country Breakdown</h2>
    <p>Of 3,342 active GTM Engineer job postings, the geographic distribution is more global than most people expect. The US is the largest single market, but it accounts for barely a quarter of all postings.</p>
    <p><strong>United States: 25.7% (859 postings).</strong> The birthplace of the role. Clay is based in New York, most early adopters were US SaaS companies, and the highest-paying roles remain in SF, NYC, and Austin. But the US share has been declining as a percentage of total postings since mid-2025.</p>
    <p><strong>India: 17.4% (581 postings).</strong> The second-largest market, driven primarily by US-serving agencies that hire Indian operators for cost arbitrage. Bangalore, Mumbai, and Delhi are the major hubs. Indian GTM Engineers working for US agencies earn $40K-$80K, which is 3-5x local engineering salaries. See our <a href="/careers/india-gtm-engineering/">India market deep-dive</a> for the full picture.</p>
    <p><strong>Spain: 15.3% (511 postings).</strong> The surprise story. Barcelona and Madrid have become GTM Engineering hubs, driven by EU startup growth and a cost advantage for US companies establishing European operations. Spain's share grew from under 5% in early 2024 to 15.3% by late 2025. Our <a href="/careers/spain-europe-gtm-engineering/">Spain and Europe analysis</a> covers the drivers in detail.</p>
    <p><strong>United Kingdom: 7.7% (257 postings).</strong> London dominates UK postings. The UK market favors in-house GTM Engineers at Series B+ companies. Salaries run $80K-$120K equivalent, roughly 70-80% of US levels.</p>

    <h2>The Rest of the World</h2>
    <p><strong>Germany: 5.2% (174 postings).</strong> Berlin's startup ecosystem drives most demand. German companies hiring GTM Engineers tend to be later-stage (Series B+) and international in orientation.</p>
    <p><strong>Canada: 4.8% (160 postings).</strong> Toronto and Vancouver are the primary markets. Canadian roles pay 10-20% less than equivalent US roles but offer time zone alignment and lower cost of living.</p>
    <p><strong>Australia: 3.1% (104 postings).</strong> Sydney-centric. Australian companies hiring GTM Engineers are typically selling into US or European markets, so they want US-market outbound expertise.</p>
    <p><strong>France: 2.9% (97 postings).</strong> Paris tech scene, growing fast but behind Spain. French language requirements limit some roles to French-speaking practitioners.</p>
    <p><strong>Other markets (17.9%, 599 postings):</strong> The remaining postings are spread across Netherlands, Singapore, Brazil, Israel, UAE, Philippines, and 20+ smaller markets. Each individually represents under 2% of total postings.</p>

    <h2>Why India and Spain?</h2>
    <p>Two factors explain the unexpected concentration in India and Spain.</p>
    <p><strong>Cost arbitrage for agencies.</strong> US-based GTM Engineering agencies discovered they could hire skilled operators in India and Spain at 30-60% of US rates. The work is tool-based (Clay, HubSpot, Instantly), timezone-compatible, and doesn't require physical presence. An agency charging US clients $5K-$8K/month while paying operators $2K-$3K/month generates strong margins.</p>
    <p><strong>Local startup ecosystems matured.</strong> India's B2B SaaS sector (Freshworks, Chargebee, Zoho ecosystem) created organic demand for outbound automation. Spain's Barcelona tech scene, boosted by EU funding and lower costs than London or Berlin, attracted startups that adopted GTM Engineering early. These are genuine local markets, not just outsourcing destinations.</p>

    <h2>Remote Work Changes Everything</h2>
    <p>The geographic distribution of GTM Engineering jobs would look very different without remote work. Most GTM Engineering tasks are done through cloud-based tools. Clay, HubSpot, Instantly, and Make don't care where you sit. As long as you have internet access and reasonable timezone overlap with your clients, location is a non-factor.</p>
    <p>This means a GTM Engineer in Bangalore can serve a client in Boston. A freelancer in Barcelona can build Clay tables for a startup in Austin. The role was born in the remote-first era, and that fundamentally shapes its global distribution.</p>
    <p>For salary implications of this global distribution, see our <a href="/salary/us-vs-global/">US vs Global salary comparison</a>. For the career entry perspective, our <a href="/careers/how-to-become-gtm-engineer/">guide to becoming a GTM Engineer</a> covers paths regardless of location.</p>

{faq_html(faq_pairs)}
{jobmkt_related_links("jobs-by-country")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer job market data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/jobs-by-country/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/jobs-by-country/index.html", page)
    print(f"  Built: careers/jobs-by-country/index.html")


def build_jobmkt_posted_vs_actual():
    """JOBMKT-03: Posted vs actual salary from job market angle."""
    title = "Posted vs Actual GTM Engineer Salary Gap"
    description = (
        "Job postings list $150K median. Practitioners report $135K. Why the"
        " $15K gap exists, what it means, and how to read salary ranges."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Posted vs Actual Salary", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("Can I trust the salary listed in a GTM Engineer job posting?",
         "Use it as a ceiling, not a midpoint. Job postings skew 10-15% above what companies pay for the role. The $150K posted median reflects maximum budget, not typical offer. Expect initial offers at 85-90% of the posted range, with negotiation room to close the gap if your skills are strong."),
        ("How do I negotiate above the posted salary range?",
         "Demonstrate skills that command premium rates. Python proficiency, Clay expertise, and a portfolio of results (meetings booked, pipeline generated) are your strongest cards. Companies posting $120K-$150K will go to $160K for a candidate who codes, has agency experience, and can show measurable outcomes. The key is proving you will produce more pipeline than a non-technical hire."),
        ("Why are some GTM Engineer salaries listed as $80K-$200K?",
         "Wide ranges usually mean the company is open to hiring at multiple seniority levels for the same title. An $80K-$200K range likely covers junior through lead-level candidates. Ask the recruiter directly which level they are prioritizing. Companies posting wide ranges are often figuring out the role as they hire, which can be an advantage for experienced candidates who can shape the position."),
        ("Do GTM Engineer job postings include equity and bonuses?",
         "Rarely. Most posted salaries are base salary only. Our survey shows 41% of GTM Engineers receive equity (median $15K-$25K/year value at startups). Bonuses add another $10K-$30K at companies with variable compensation. When evaluating a job posting, assume the listed salary is base only and ask about equity and bonus in the interview process."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Job Market</div>
        <h1>Posted vs Actual GTM Engineer Salary</h1>
        <p>We compared 3,342 job posting salary ranges against survey data from 228 practitioners. The gap is consistent, predictable, and exploitable if you know the pattern.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">$150K</span>
        <span class="stat-label">Posted Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$135K</span>
        <span class="stat-label">Reported Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$15K</span>
        <span class="stat-label">Median Gap</span>
    </div>
</div>

<div class="salary-content">
    <h2>The $15K Gap</h2>
    <p>Job postings say $150K. Practitioners report $135K. That $15K gap is the most consistent finding in our job market data, and it shows up across every seniority level, location, and company stage.</p>
    <p>This is the job-seeker version of the salary story. For the compensation analysis angle (how total comp breaks down), see our <a href="/salary/posted-vs-actual/">posted vs actual salary deep-dive</a> in the salary section.</p>

    <h2>Why Job Postings Overstate Salary</h2>
    <p><strong>Aspirational budgeting.</strong> Companies post the maximum they'd pay for a perfect candidate. A posting listing $140K-$170K has $170K budgeted for a senior practitioner who codes in Python, has agency experience, and can own the full enrichment pipeline. Most candidates receive offers in the $140K-$155K range.</p>
    <p><strong>Competition for talent.</strong> With 5,205% job growth and a shortage of qualified candidates, companies inflate posted ranges to attract applicants. A company that would pay $130K posts "$120K-$160K" because a listing showing "$110K-$130K" gets fewer applications. The posted number is marketing, not accounting.</p>
    <p><strong>Equity and bonus exclusion.</strong> Most job postings list base salary only. When practitioners report their compensation, many include base salary only as well. But the gap partially reflects that some practitioners mentally include bonus or equity when answering survey questions, while job postings never do. The real base-to-base gap is closer to $10K-$12K.</p>
    <p><strong>Location variance.</strong> Job postings increasingly list "remote" with a salary range calibrated to SF/NYC cost of living. Actual offers adjust downward for candidates in lower-cost markets. A "remote, $140K-$170K" posting often pays $130K-$145K to someone in Austin or Denver. This geographic adjustment accounts for $5K-$15K of the posted-to-actual gap.</p>

    <h2>How to Read Job Posting Salaries</h2>
    <p>Use these rules of thumb when evaluating a GTM Engineer job posting:</p>
    <p><strong>Take 85-90% of the posted midpoint.</strong> A posting listing $130K-$170K has a midpoint of $150K. Expect an offer between $127K and $135K. If you're at the top of the skill range (coding, agency experience, strong portfolio), you can push toward the posted midpoint.</p>
    <p><strong>Wide ranges mean unclear leveling.</strong> A $90K-$180K range tells you the company hasn't decided whether they're hiring junior or senior. Ask directly. The spread gives you negotiation room but also uncertainty about expectations.</p>
    <p><strong>No salary listed is a flag.</strong> Companies that omit salary ranges in markets where disclosure isn't required are either below market rate or disorganized. Both are signals. In states like Colorado, New York, and California, salary disclosure is legally required, so unlisted salaries in those markets are compliance risks.</p>
    <p><strong>"Competitive" means below median.</strong> When a job posting says "competitive salary," it typically pays $110K-$125K. Companies paying above median post the number because it's a selling point. "Competitive" is a hedge word for "we'd rather not say."</p>

    <h2>Negotiation Implications</h2>
    <p>The consistent $15K gap is an advantage for informed candidates. If you know the gap exists, you can anchor your expectations correctly.</p>
    <p>When a company posts $140K-$170K, they expect to negotiate. Opening at $155K-$160K (near their posted midpoint) positions you well. They'll counter at $140K-$150K, and you'll land at $145K-$155K if your skills justify it.</p>
    <p>The strongest negotiation tools for GTM Engineers are specific: measurable results from previous roles (pipeline generated, meetings booked, conversion rates improved), coding ability (the <a href="/salary/coding-premium/">$45K coding premium</a> is well-documented), and competing offers. Companies paying below their posted range know other companies post aggressively too, so a credible competing offer recalibrates the conversation fast.</p>
    <p>For complete salary benchmarks by seniority and location, see our <a href="/salary/">salary data index</a>. For more on how skills translate to compensation, read the <a href="/careers/top-skills-in-postings/">top skills analysis</a>.</p>

{faq_html(faq_pairs)}
{jobmkt_related_links("posted-vs-actual-salary")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer salary data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/posted-vs-actual-salary/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/posted-vs-actual-salary/index.html", page)
    print(f"  Built: careers/posted-vs-actual-salary/index.html")


def build_jobmkt_top_skills():
    """JOBMKT-04: Top skills in GTM Engineer job postings."""
    title = "Top Skills in GTM Engineer Job Postings"
    description = (
        "Clay appears in 84% of postings. HubSpot, Salesforce, Python, SQL"
        " round out the top 5. Skills demand vs practitioner supply data."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Top Skills in Postings", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is the most important skill for GTM Engineer job postings?",
         "Clay proficiency. It appears in 84% of all GTM Engineer job postings, more than any other single tool or skill. Clay is the center of gravity for the role. HubSpot or Salesforce CRM knowledge is the second most requested capability, appearing in 92% of postings when combined. If you can only learn two things, learn Clay and one major CRM."),
        ("Are nice-to-have skills in job postings worth learning?",
         "Yes, especially Python and SQL. When postings list Python as 'nice to have,' they're signaling budget flexibility. Candidates with Python earn $45K more on average. SQL opens doors at larger companies with data warehouses. 'Nice to have' in a job posting translates to 'will pay more for' in an offer negotiation."),
        ("Do GTM Engineer certifications matter in job postings?",
         "Clay University completion carries weight because it signals hands-on tool proficiency. HubSpot and Salesforce certifications add credibility for roles at companies using those CRMs. But hiring managers consistently rank portfolio projects above certifications. A working Clay table that generated 500 leads is worth more than three certificates."),
        ("How should I prioritize skill development for GTM Engineering?",
         "Start with Clay (month 1-2), add CRM depth in HubSpot or Salesforce (month 2-3), learn Make or n8n for automation (month 3-4), then layer in Python and SQL (months 4-6). This mirrors how most successful practitioners built their skill sets. Each layer compounds on the previous one, and each addition opens new job postings you qualify for."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Job Market</div>
        <h1>Top Skills in GTM Engineer Postings</h1>
        <p>We parsed 3,342 job postings to identify the most requested skills. Then we compared posting demand against what 228 practitioners report using. The gaps reveal where the market is headed.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">84%</span>
        <span class="stat-label">Mention Clay</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">92%</span>
        <span class="stat-label">Want CRM Skills</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">~40%</span>
        <span class="stat-label">Request Python</span>
    </div>
</div>

<div class="salary-content">
    <h2>The Skill Demand Stack</h2>
    <p>Job postings reveal what companies are willing to pay for. We ranked every skill, tool, and technology mentioned across 3,342 GTM Engineer job listings to build the definitive demand picture.</p>

    <h3>Tier 1: Table Stakes (mentioned in 70%+ of postings)</h3>
    <p><strong>Clay (84%):</strong> The defining tool of the role. Clay appears more frequently than any other single technology in GTM Engineer postings. Proficiency with Clay tables, enrichment waterfalls, and HTTP API actions is the baseline expectation. 84% of practitioners also use Clay daily, so supply roughly matches demand here.</p>
    <p><strong>CRM fluency (92% combined):</strong> HubSpot and Salesforce together dominate the CRM requirement. HubSpot appears in roughly 55% of postings (startup and mid-market companies). Salesforce appears in roughly 45% (enterprise and larger startups). Most postings specify one, rarely both. Admin-level knowledge (custom objects, workflows, API access) is the expected depth.</p>
    <p><strong>Outbound sequencing (78%):</strong> Instantly, Smartlead, Lemlist, or equivalent experience. Companies want GTM Engineers who understand deliverability, domain rotation, warming schedules, and sequence optimization. Tool-specific experience matters less than understanding the principles.</p>

    <h3>Tier 2: Premium Skills (mentioned in 25-50% of postings)</h3>
    <p><strong>Python (~40%):</strong> The skill with the largest gap between demand and supply. 40% of postings mention Python, but only about 35% of practitioners rate themselves as proficient coders. This gap is why the <a href="/salary/coding-premium/">$45K coding premium</a> exists. Companies posting Python as "required" pay 15-20% above median. Companies listing it as "nice to have" still pay more for candidates who have it.</p>
    <p><strong>SQL (~30%):</strong> Data querying skills appear in postings from larger companies with data warehouses (BigQuery, Snowflake, Redshift). The ability to write joins, aggregations, and window functions for pipeline analysis is increasingly requested. SQL rarely appears as a standalone requirement but pairs with Python in job postings about 60% of the time.</p>
    <p><strong>Automation platforms (~35%):</strong> Make and n8n are overtaking Zapier in job postings. n8n mentions tripled between early 2025 and early 2026, reflecting the shift toward more technical automation. Practitioners using n8n hit 54% adoption among automation users, outpacing Zapier's declining share.</p>

    <h3>Tier 3: Differentiators (mentioned in 10-25% of postings)</h3>
    <p><strong>AI/LLM integration (~22%):</strong> Postings mentioning "AI," "LLM," "Claude," or "OpenAI" are growing fast. These roles want GTM Engineers who can build AI-powered personalization, classify leads using LLMs, or create custom AI actions in Clay. This skill set is rare (71% of practitioners use AI coding tools, but few list it as a core competency) and commands premium compensation.</p>
    <p><strong>Data enrichment architecture (~18%):</strong> The concept of multi-source enrichment waterfalls (try Apollo, fall back to Clearbit, then FullEnrich) is becoming a specific skill requirement. Companies that have outgrown single-source enrichment need someone who can design, build, and maintain these cascading systems.</p>
    <p><strong>API development (~15%):</strong> Building custom APIs, webhooks, and integrations. This skill separates engineers from operators and opens doors to lead and staff-level roles where system architecture is part of the job description.</p>

    <h2>The Supply-Demand Gaps</h2>
    <p>Two gaps stand out in the data.</p>
    <p><strong>Python demand exceeds supply.</strong> 40% of postings want it, 35% of practitioners have it. This is the biggest single skill gap in the market, and it directly drives the coding premium. If you're a GTM Engineer without Python, learning it is the single highest-ROI investment you can make.</p>
    <p><strong>Postings lag practitioner adoption.</strong> AI coding tools are used by 71% of practitioners, but only 22% of postings mention them. n8n is used by 54% of automation users, but far fewer postings list it specifically. Early adopters of emerging skills have a 6-12 month advantage before job postings catch up, which means learning these tools now positions you ahead of the demand curve.</p>
    <p>For the full <a href="/careers/skills-gap/">skills gap analysis</a> with a recommended learning path, and <a href="/careers/do-you-need-to-code/">the coding question deep-dive</a>, see our career guides.</p>

{faq_html(faq_pairs)}
{jobmkt_related_links("top-skills-in-postings")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer skills and job data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/top-skills-in-postings/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/top-skills-in-postings/index.html", page)
    print(f"  Built: careers/top-skills-in-postings/index.html")


def build_jobmkt_monthly_trends():
    """JOBMKT-05: Monthly hiring trends page."""
    title = "GTM Engineer Monthly Hiring Trends 2025"
    description = (
        "December 2025 peaked at 624 GTM Engineer postings. Monthly data"
        " shows Q4 surge, seasonal patterns, and best months to job search."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Monthly Hiring Trends", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What is the best month to look for a GTM Engineer job?",
         "October through December. Q4 consistently shows the highest posting volumes, peaking at 624 in December 2025. Companies allocate new headcount budget in Q4 for the following year, and hiring managers rush to fill roles before year-end. January also spikes as budgets activate. The worst months are June through August, when hiring slows 15-20% below the annual average."),
        ("Do GTM Engineer hiring trends follow seasonal patterns?",
         "Yes. The pattern mirrors broader tech hiring with two peaks (Q1 and Q4) and a summer trough. January-March sees strong hiring as new budgets activate. April-May stays steady. June-August dips as companies slow hiring during summer. September picks up, and October-December surges to annual highs. This pattern held consistently through 2025."),
        ("What do 2026 GTM Engineer hiring trends look like?",
         "Early 2026 data shows continued growth above 2025 levels. January 2026 postings outpaced January 2025 by roughly 80%. The structural drivers (AI outbound adoption, Clay growth, cost arbitrage vs SDR teams) remain strong. We project 2026 total postings will surpass 2025 by 50-100%, assuming no major economic disruption."),
        ("How long does the GTM Engineer interview process take?",
         "Two to four weeks from application to offer for most companies. The typical process: recruiter screen (20 min), hiring manager interview (45 min), technical assessment or Clay table build exercise (1-2 hours, often take-home), and a final interview with a VP or founder. Startups move faster (1-2 weeks). Enterprise companies take 3-4 weeks. If you're searching in Q4, account for holiday delays."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Job Market</div>
        <h1>GTM Engineer Monthly Hiring Trends</h1>
        <p>We tracked GTM Engineer job postings month by month through 2025. December peaked at 624, nearly double the summer months. Here is the full monthly breakdown.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">624</span>
        <span class="stat-label">December Peak</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">Q4</span>
        <span class="stat-label">Strongest Quarter</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">3,342</span>
        <span class="stat-label">2025 Total</span>
    </div>
</div>

<div class="salary-content">
    <h2>Month-by-Month: 2025</h2>
    <p>Every month of 2025 showed growth over the same month in 2024. But the monthly distribution was far from even. Here is what the hiring calendar looked like:</p>
    <p><strong>January (198 postings):</strong> New year, new budgets. Companies that secured headcount in Q4 planning started posting immediately. January 2025 was already 3x January 2024, setting the tone for the year.</p>
    <p><strong>February (215):</strong> Slight uptick as companies that delayed Q4 hiring posted roles. Hiring managers returning from holiday slowdowns moved quickly to fill open reqs.</p>
    <p><strong>March (241):</strong> The spring hiring wave began. Conference season (SaaS conferences in March-April) exposed more companies to GTM Engineering, creating new demand. Multiple job postings referenced "building a GTM Engineering function" for the first time.</p>
    <p><strong>April (268):</strong> Peak of the spring cycle. Companies that saw Q1 results from their first GTM Engineer posted roles for second and third hires. Agency demand also increased as more companies tested the model before committing to in-house.</p>
    <p><strong>May (252):</strong> Slight pullback as some companies paused hiring for mid-year budget reviews. Still above Q1 levels.</p>
    <p><strong>June (234):</strong> Summer slowdown begins. Decision-makers on vacation. Interview cycles lengthened. The June dip is consistent with broader tech hiring patterns.</p>
    <p><strong>July (221):</strong> Lowest posting volume of H2. Many companies froze non-critical hiring during July as executives focused on board prep and mid-year reviews.</p>
    <p><strong>August (238):</strong> Recovery from the July trough. Companies preparing for Q4 pushes started posting early. "Start in September" was a common note in August listings.</p>
    <p><strong>September (312):</strong> Sharp uptick. Companies that delayed summer hiring caught up. The September surge also reflected companies hiring for Q4 outbound campaigns, which is the highest-value period for B2B pipeline generation.</p>
    <p><strong>October (385):</strong> Q4 acceleration. October postings exceeded any single month prior to September. Companies with year-end pipeline targets needed GTM Engineers immediately. Urgency showed up in faster interview cycles and higher salary offers.</p>
    <p><strong>November (454):</strong> Continued Q4 surge. November postings nearly doubled July's count. Year-end budget spend ("use it or lose it" headcount) drove a portion of the increase.</p>
    <p><strong>December (624):</strong> The annual peak. December 2025 set the record at 624 active postings. Companies posting in December typically wanted January start dates. The December spike also reflected 2026 headcount approved early, with roles posted before the holiday break.</p>

    <h2>The Q4 Phenomenon</h2>
    <p>Q4 (October-December) accounted for 1,463 of 3,342 total postings, roughly 44% of the annual volume concentrated in three months. This Q4 weighting has three drivers.</p>
    <p><strong>Budget cycles.</strong> Most SaaS companies operate on calendar-year budgets. New headcount is approved in Q3-Q4 planning for the following year. Hiring managers post roles as soon as budget is confirmed, even if start dates are in January.</p>
    <p><strong>Pipeline urgency.</strong> Q4 is when B2B companies push hardest on pipeline generation for year-end revenue targets. Companies that don't have a GTM Engineer feel the pain most acutely in October when outbound needs to be running at full capacity. The urgency creates faster hiring cycles and less salary negotiation resistance.</p>
    <p><strong>Year-end spend.</strong> Unspent headcount budget expires at year-end in many organizations. Hiring managers who have open reqs post aggressively in November-December to avoid losing budget allocation. This creates a genuine posting spike that doesn't necessarily reflect sustained demand, but the roles are real and funded.</p>

    <h2>When to Job Search</h2>
    <p>The data points to two optimal windows for GTM Engineer job seekers.</p>
    <p><strong>October-December:</strong> Highest volume means the most options. Competition is also higher, but the sheer number of openings works in your favor. Companies hiring in Q4 often move quickly, with 2-3 week interview cycles. The downside: some December postings go dormant over the holidays and don't resume until January.</p>
    <p><strong>January-March:</strong> Fresh budgets activate. Companies that posted in December schedule interviews in January. Q1 hiring tends to be more deliberate (less urgency than Q4) but the roles are fully funded and decision-making is faster because budgets are new and approvals are fresh.</p>
    <p><strong>Avoid: July.</strong> Lowest posting volume, slowest interview cycles, decision-makers unavailable. If you must search in summer, start in June to get ahead of the August recovery.</p>
    <p>For the broader growth story behind these monthly numbers, see our <a href="/careers/job-growth/">5,205% job growth analysis</a>. For salary expectations by seniority level, check the <a href="/salary/by-seniority/">salary by seniority data</a>.</p>

{faq_html(faq_pairs)}
{jobmkt_related_links("monthly-hiring-trends")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer hiring data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/monthly-hiring-trends/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/monthly-hiring-trends/index.html", page)
    print(f"  Built: careers/monthly-hiring-trends/index.html")


def build_jobmkt_salary_bands():
    """JOBMKT-06: Salary bands by location from job postings."""
    title = "GTM Engineer Salary Bands by Location"
    description = (
        "US job postings show $128K-$175K range. Salary bands vary by metro"
        " and country. Location data from 3,342 postings and 228 surveys."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Salary Bands by Location", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("Which location pays the most for GTM Engineers?",
         "San Francisco, with posted salary ranges of $155K-$195K and reported medians around $165K. NYC follows closely at $145K-$185K posted. The SF premium reflects both cost of living and concentration of venture-backed companies that index heavily on GTM Engineering. Remote roles for SF-based companies sometimes pay 80-90% of the local rate."),
        ("Do remote GTM Engineer salaries adjust for location?",
         "Most do. Companies posting 'remote, $140K-$170K' typically adjust offers based on the candidate's location. A Denver-based candidate applying for a remote role at an SF company should expect 85-90% of the posted range. Some companies (Basecamp model) pay flat rates regardless of location, but these are a minority. Always ask about location-based adjustments early in the process."),
        ("How do I negotiate salary when relocating for a GTM Engineer role?",
         "Anchor to the destination city's market rate, not your current salary. If you're moving from Austin ($130K median) to SF ($165K median), the SF rate applies. Companies know the cost-of-living difference. Negotiate relocation assistance separately from base salary. Many companies offer $5K-$15K relocation packages for GTM Engineers they want to bring on-site."),
        ("Does cost of living offset higher salaries in expensive cities?",
         "Partially. SF GTM Engineers earn roughly 25% more than Austin equivalents, but SF cost of living is 45% higher. In pure purchasing power, Austin, Denver, and remote roles often come out ahead. The SF premium benefits you most if you plan to leave SF eventually (higher savings rate if you live frugally) or if your career trajectory requires SF network effects."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Job Market</div>
        <h1>GTM Engineer Salary Bands by Location</h1>
        <p>We mapped salary ranges from 3,342 job postings across every major tech market. Where you work (or claim to work remotely) affects your compensation by $30K-$50K.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">$128K&#8209;$175K</span>
        <span class="stat-label">US Range</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$165K</span>
        <span class="stat-label">SF Median</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$50K</span>
        <span class="stat-label">Max City Gap</span>
    </div>
</div>

<div class="salary-content">
    <h2>US Metro Salary Bands</h2>
    <p>Within the US, GTM Engineer salary bands vary by roughly $50K between the highest-paying and lowest-paying major markets. Here is how the major metros stack up based on job posting data.</p>
    <p><strong>San Francisco/Bay Area: $155K-$195K posted, $165K reported median.</strong> The highest-paying market for GTM Engineers. SF companies are willing to pay top dollar because the local talent pool, while growing, can't keep up with demand. Clay's HQ in NYC and the concentration of VC-backed SaaS companies in SF create a bidding war for experienced practitioners.</p>
    <p><strong>New York City: $145K-$185K posted, $158K reported median.</strong> Close behind SF. NYC's advantage is the intersection of tech and financial services companies. Fintech firms in NYC pay 10-15% above typical SaaS companies for GTM Engineers with financial services domain knowledge.</p>
    <p><strong>Seattle: $140K-$175K posted, $152K reported median.</strong> The enterprise tech hub. Microsoft, Amazon, and the Seattle SaaS ecosystem drive demand. Seattle roles tend to skew senior, with fewer junior postings than SF or NYC.</p>
    <p><strong>Boston: $135K-$170K posted, $148K reported median.</strong> Strong demand from HubSpot ecosystem companies and biotech/healthcare SaaS. Boston companies posting GTM Engineer roles often want HubSpot expertise specifically.</p>
    <p><strong>Austin: $125K-$160K posted, $140K reported median.</strong> The mid-market sweet spot. Austin's lower cost of living makes $140K stretch further than $165K in SF. Many practitioners cite Austin as the best value market for GTM Engineers. The city's growing tech scene creates steady demand without SF's cost pressure.</p>
    <p><strong>Denver: $120K-$155K posted, $138K reported median.</strong> Similar profile to Austin. Denver's appeal is remote-friendly companies with mountain-town lifestyle. Salaries are 15-20% below coastal markets but cost of living is 30-40% lower.</p>
    <p><strong>Remote (US-based): $125K-$165K posted, $142K reported median.</strong> Remote roles show the widest salary bands because companies adjust for candidate location. The posted range represents the full spectrum from Austin-adjusted to SF-adjusted offers.</p>

    <h2>International Salary Bands</h2>
    <p>Outside the US, salary bands drop significantly but purchasing power often stays competitive with US roles.</p>
    <p><strong>London/UK: $95K-$135K equivalent, $110K reported median.</strong> UK roles pay 70-80% of US equivalents. London-based companies hiring GTM Engineers tend to be Series B+ with international sales teams. The weaker pound relative to the dollar compresses the gap in nominal terms.</p>
    <p><strong>Germany/Berlin: $85K-$120K equivalent, $100K reported median.</strong> German companies value technical depth and often require both German and English fluency. Berlin startups pay 60-70% of US levels.</p>
    <p><strong>Spain/Barcelona: $55K-$90K equivalent, $70K reported median.</strong> Lower nominal salary, but Barcelona's cost of living makes this competitive in purchasing power. Many Barcelona-based GTM Engineers serve US clients through agencies, which is why this market has grown so fast.</p>
    <p><strong>India/Bangalore: $25K-$60K, $40K reported median.</strong> The widest range of any market. Local companies pay $25K-$35K. US-serving agencies pay $40K-$60K. A $50K salary in Bangalore provides a lifestyle equivalent to $150K in SF. See the <a href="/careers/india-gtm-engineering/">India market analysis</a> for the full picture.</p>

    <h2>How Bands Compare to Reported Salaries</h2>
    <p>Across all locations, posted salary bands run 10-15% above what practitioners report earning. This gap is consistent (see our <a href="/careers/posted-vs-actual-salary/">posted vs actual salary analysis</a>) and predictable. Use the posted band as a ceiling for negotiation, not an expected midpoint.</p>
    <p>The largest posted-to-actual gaps appear in SF and NYC, where competitive posting inflates ranges the most. The smallest gaps are in international markets, where salary transparency norms are different and companies post closer to actual compensation levels.</p>
    <p>For the full location-by-location salary breakdown from our survey data (not just job postings), see the <a href="/salary/by-location/">salary by location</a> analysis. For how location interacts with the <a href="/salary/us-vs-global/">US vs global comparison</a>, see our dedicated page.</p>

{faq_html(faq_pairs)}
{jobmkt_related_links("salary-bands-by-location")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer salary data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/salary-bands-by-location/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/salary-bands-by-location/index.html", page)
    print(f"  Built: careers/salary-bands-by-location/index.html")


def build_jobmkt_india():
    """JOBMKT-07: India GTM Engineering market analysis."""
    title = "India GTM Engineering: 17.4% of Global Jobs"
    description = (
        "India is the 2nd largest GTM Engineer market with 17.4% of postings."
        " Bangalore, Mumbai, Delhi hubs. Agency opportunity and salary data."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("India Market", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What does a GTM Engineer earn in India?",
         "Local companies pay 20-30 LPA ($25K-$35K) for GTM Engineers. US-serving agencies pay $40K-$60K, which is 3-5x the local rate for comparable tech roles. Agency work is the higher-earning path for India-based practitioners. A senior operator at a US agency can earn $60K-$80K, putting them in the top 5% of Indian tech salaries."),
        ("Can I work for US companies remotely from India?",
         "Yes, and this is the primary model. Most India-based GTM Engineers work for US companies or US-serving agencies as contractors. The key requirements: reliable internet, 4+ hours of overlap with US business hours (typically IST afternoon/evening), and strong written English. Most agencies hire contractors, not employees, which simplifies the arrangement for both sides."),
        ("What is the agency opportunity in India for GTM Engineers?",
         "Significant. US agencies hiring India-based operators create strong margin businesses ($5K-$8K/month client fees with $2K-$3K/month operator costs). Indian practitioners can also start their own agencies, serving US mid-market companies at price points that undercut US-based agencies. The arbitrage is straightforward and durable as long as skill quality remains high."),
        ("What skills do Indian GTM Engineers need differently?",
         "The core skill stack is identical: Clay, CRM, outbound sequencing. The differentiator for India-based practitioners is written English quality and US market knowledge. Indian operators who understand US B2B sales culture, buyer personas, and communication norms command premium rates. Technical skills alone don't differentiate; cultural fluency does."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Job Market</div>
        <h1>India GTM Engineering Market</h1>
        <p>India accounts for 17.4% of all GTM Engineer job postings, making it the second-largest market globally. The story is part cost arbitrage, part genuine ecosystem growth.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">17.4%</span>
        <span class="stat-label">Global Share</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">581</span>
        <span class="stat-label">Active Postings</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">$40K&#8209;$80K</span>
        <span class="stat-label">Agency Pay Range</span>
    </div>
</div>

<div class="salary-content">
    <h2>Why India Is the #2 Market</h2>
    <p>India's 17.4% share of GTM Engineer postings surprised us. The role originated in the US, was named by a US company (Clay), and the highest-paying roles remain in SF and NYC. So why does India have more postings than the UK, Germany, and Canada combined?</p>
    <p>Two forces converged. US-based GTM Engineering agencies discovered they could hire skilled operators in India at 30-50% of US rates. And India's own B2B SaaS ecosystem (Freshworks, Chargebee, Zoho, and hundreds of smaller companies) created organic demand for outbound automation specialists.</p>

    <h2>The Three Cities</h2>
    <p><strong>Bangalore: ~45% of India postings.</strong> India's tech capital dominates GTM Engineering hiring. The concentration of SaaS companies, availability of English-speaking technical talent, and established agency networks make Bangalore the center of gravity. Most US agencies hiring in India recruit from Bangalore first.</p>
    <p><strong>Mumbai: ~30% of India postings.</strong> Mumbai's financial services and enterprise SaaS presence drives demand. Companies in Mumbai tend to want GTM Engineers with Salesforce expertise rather than HubSpot, reflecting the enterprise orientation of the market. Mumbai-based practitioners earn slightly more than Bangalore equivalents, roughly 10-15% premium.</p>
    <p><strong>Delhi/NCR: ~15% of India postings.</strong> Growing fast but still third. Delhi's advantage is its proximity to government and traditional enterprise buyers. GTM Engineers in Delhi often work on outbound for domestic Indian companies rather than US-serving agencies.</p>
    <p>The remaining 10% is spread across Pune, Hyderabad, Chennai, and emerging tech hubs.</p>

    <h2>The Agency Model</h2>
    <p>Most India-based GTM Engineers work within the agency model, either employed by US agencies or running their own. The economics are compelling.</p>
    <p>A US agency charges clients $5K-$8K/month per managed outbound engagement. An India-based operator handling that engagement earns $2K-$3K/month. The agency keeps 50-60% margin while the operator earns 3-5x local market rates. Both sides benefit.</p>
    <p>Some Indian practitioners have cut out the intermediary entirely. They run their own agencies, serving US mid-market companies at $3K-$5K/month, which undercuts US-based agencies by 30-40% while generating strong income by Indian standards. A solo operator with 3-4 US clients at $3K-$4K/month earns $9K-$16K/month, which is elite compensation in any Indian metro.</p>

    <h2>Local Demand vs Agency Work</h2>
    <p>The split between US-serving agency work and local Indian company demand is roughly 65/35. Agency work pays more, but local demand is growing fast.</p>
    <p>Indian SaaS companies hiring GTM Engineers pay 20-30 LPA ($25K-$35K), which is competitive with senior engineering roles at Indian startups. These roles are typically in-house, full-time, with equity. The tools and workflows are identical to US roles: Clay, HubSpot or Salesforce, Instantly or Smartlead.</p>
    <p>The career calculus: agency work pays 2-3x more in the short term but offers less equity upside and career stability. In-house roles at funded Indian SaaS companies pay less but come with equity, titles, and management trajectories. Many Indian practitioners start with agency work to build skills and savings, then transition to in-house roles or start their own agencies after 1-2 years.</p>

    <h2>What Indian Practitioners Need</h2>
    <p>The technical skill requirements are universal. Clay, CRM depth, outbound sequencing, and ideally Python. What differentiates India-based practitioners serving US clients is cultural fluency.</p>
    <p>US B2B outbound has specific norms: email length, tone, personalization approach, follow-up cadence, and LinkedIn etiquette that differ from Indian business communication styles. Indian operators who internalize US outbound conventions (concise, direct, value-first) outperform those who apply Indian business communication patterns to US prospects.</p>
    <p>English writing quality is the other differentiator. Grammatical proficiency is widespread in Indian tech talent. What separates top performers is idiomatic fluency: writing that reads as natural to a US audience, not technically correct but obviously non-native. Practitioners who invest in US writing style (short sentences, active voice, specific numbers) command premium rates.</p>
    <p>For the global context, see our <a href="/careers/jobs-by-country/">jobs by country breakdown</a>. For salary comparisons across markets, visit the <a href="/salary/us-vs-global/">US vs global salary data</a>.</p>

{faq_html(faq_pairs)}
{jobmkt_related_links("india-gtm-engineering")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly GTM Engineer market data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/india-gtm-engineering/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/india-gtm-engineering/index.html", page)
    print(f"  Built: careers/india-gtm-engineering/index.html")


def build_jobmkt_spain():
    """JOBMKT-08: Spain and Europe GTM Engineering market analysis."""
    title = "Spain and Europe GTM Engineer Market Data"
    description = (
        "Spain holds 15.3% of GTM Engineer postings, 3rd globally. Barcelona"
        " and Madrid lead. UK at 7.7%. European salary and market analysis."
    )
    description = pad_description(description)

    crumbs = [("Home", "/"), ("Career Guides", "/careers/"), ("Spain & Europe Market", None)]
    bc_html = breadcrumb_html(crumbs)

    faq_pairs = [
        ("What does a GTM Engineer earn in Europe?",
         "Varies widely by country. UK roles pay $95K-$135K equivalent. Germany pays $85K-$120K. Spain pays $55K-$90K. These are 50-75% of US levels in nominal terms, but purchasing power is often comparable due to lower cost of living, public healthcare, and stronger labor protections. European practitioners serving US clients through agencies earn closer to US rates."),
        ("Why is Spain the #3 GTM Engineer market globally?",
         "Barcelona's tech ecosystem matured at exactly the right time. EU startup funding increased, US companies established European outbound teams in cost-friendly cities, and Spain's talent pool (bilingual, technical, timezone-compatible with US east coast) proved ideal for agency work. Barcelona's cost of living is 40-50% below London, making it attractive for both companies and practitioners."),
        ("Do European GTM Engineers need work permits?",
         "EU citizens can work freely across EU member states. Non-EU citizens need work permits for in-person roles. For remote contractor work serving US clients, work permits are typically not required as long as you have legal residency. The most common arrangement: EU-resident contractors serving US-based agencies or companies. Spain's digital nomad visa (launched 2023) has attracted non-EU GTM Engineers specifically."),
        ("Is the European GTM Engineer market growing or saturating?",
         "Growing fast. Europe overall represents roughly 30% of all GTM Engineer postings, up from under 15% in early 2024. The growth is structural: European SaaS companies are adopting US-style outbound at increasing rates, and US companies see Europe as a cost-effective talent pool. Saturation risk is low for the next 2-3 years given the growth trajectory."),
    ]

    body = f'''{bc_html}
<section class="salary-header">
    <div class="salary-header-inner">
        <div class="salary-eyebrow">Job Market</div>
        <h1>Spain and Europe GTM Engineer Market</h1>
        <p>Spain holds 15.3% of global GTM Engineer postings, making it the third-largest market behind only the US and India. Barcelona is the epicenter, but the broader European picture matters too.</p>
    </div>
</section>

<div class="salary-stats">
    <div class="salary-stat-card">
        <span class="stat-value">15.3%</span>
        <span class="stat-label">Spain Global Share</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">7.7%</span>
        <span class="stat-label">UK Global Share</span>
    </div>
    <div class="salary-stat-card">
        <span class="stat-value">~30%</span>
        <span class="stat-label">Total Europe Share</span>
    </div>
</div>

<div class="salary-content">
    <h2>Spain: The Unexpected #3</h2>
    <p>When we first ran the country analysis, Spain at 15.3% looked like a data error. The GTM Engineer role was created in the US, the tools are US-based (Clay, HubSpot, Apollo), and the highest salaries are in SF and NYC. Why would Spain have more postings than the UK, Germany, Canada, or Australia?</p>
    <p>Three factors explain it.</p>
    <p><strong>Barcelona became a GTM hub.</strong> Barcelona's tech ecosystem hit a tipping point around 2023-2024. A combination of EU startup funding (Barcelona received more VC funding than any Spanish city in 2024), talent migration from Northern Europe (lower cost of living, better weather), and US companies establishing European operations created a concentration of outbound-focused companies. Several early GTM Engineering agencies set up operations in Barcelona, which attracted talent, which attracted more agencies.</p>
    <p><strong>Cost arbitrage works for Europe too.</strong> A GTM Engineer in Barcelona earns $55K-$90K. The same person in London earns $95K-$135K. For US companies establishing European outbound teams, Barcelona offers 40-50% savings over London with minimal quality difference. The timezone is favorable (6 hours ahead of EST, workable for US east coast overlap), English fluency is high in Barcelona's tech community, and infrastructure is solid.</p>
    <p><strong>Spain's digital nomad visa attracted remote workers.</strong> Spain launched a digital nomad visa in 2023, specifically designed for remote tech workers. Non-EU GTM Engineers (from Latin America, Southeast Asia, and elsewhere) relocated to Spain to serve US clients while enjoying European lifestyle and residency benefits. This policy-driven migration inflated Spain's share of postings as both companies and individuals established there.</p>

    <h2>Barcelona vs Madrid</h2>
    <p><strong>Barcelona: ~65% of Spain postings.</strong> The clear leader. Barcelona's advantages: established tech ecosystem, higher English fluency, stronger agency presence, more international orientation. Most US-serving agencies in Spain are Barcelona-based.</p>
    <p><strong>Madrid: ~30% of Spain postings.</strong> Madrid's strength is enterprise. Spanish enterprise companies (banking, telecom, insurance) hiring GTM Engineers tend to be Madrid-based. Madrid roles are more likely to require Spanish language fluency and focus on domestic market outbound rather than US-serving agency work.</p>
    <p>The remaining 5% is scattered across Valencia, Malaga, and Seville, mostly remote roles with nominal Spanish addresses.</p>

    <h2>The Broader European Picture</h2>
    <p>Europe collectively represents roughly 30% of all GTM Engineer job postings. Here is how key markets compare.</p>
    <p><strong>United Kingdom (7.7%, 257 postings):</strong> London dominates. UK companies hiring GTM Engineers are typically Series B+ with international sales teams targeting US or European enterprise buyers. The UK market skews senior: fewer junior postings, more demand for experienced operators who can architect systems. Salaries run $95K-$135K, making London the highest-paying European market but 70-80% of US equivalents.</p>
    <p><strong>Germany (5.2%, 174 postings):</strong> Berlin's startup scene drives most demand. German companies value technical depth and process rigor. Job postings from German companies are more likely to list Python and SQL as requirements (not nice-to-haves) compared to other European markets. Bilingual (German + English) candidates command a 15-20% premium. Salaries: $85K-$120K equivalent.</p>
    <p><strong>France (2.9%, 97 postings):</strong> Paris-centric. French language is often required, which limits the talent pool. The French tech scene (BPI France ecosystem, Station F alumni) is growing but GTM Engineering adoption lags behind UK and Germany. Salaries: $75K-$110K equivalent.</p>
    <p><strong>Netherlands (1.8%, 60 postings):</strong> Amsterdam's international orientation makes it a natural fit. Dutch companies hire in English by default, and the Netherlands' central European timezone works well for both US and European clients. Small but growing market. Salaries: $80K-$115K equivalent.</p>

    <h2>European vs US Compensation</h2>
    <p>European GTM Engineer salaries run 50-75% of US levels in nominal terms. But three factors close the gap in practice.</p>
    <p><strong>Lower cost of living.</strong> Barcelona's cost of living is roughly 40% below SF. A Barcelona salary of $70K provides comparable purchasing power to $120K in SF. The lifestyle difference (healthcare, paid leave, food costs) further tips the balance.</p>
    <p><strong>Stronger labor protections.</strong> European employees get 20-30 days paid leave (vs US typical 15-20), public healthcare (no $500/month insurance premiums), and stronger job security through employment law. These benefits have real monetary value that doesn't show up in salary comparisons.</p>
    <p><strong>Agency arbitrage.</strong> European practitioners serving US clients through agencies earn closer to US rates. A Barcelona-based operator earning $4K-$6K/month from a US agency effectively earns $48K-$72K/year, which is premium compensation by Spanish standards and comes with US-market career exposure.</p>
    <p>For global salary comparisons, see our <a href="/salary/us-vs-global/">US vs Global analysis</a>. For agency-specific fees by region, check the <a href="/careers/agency-fees-by-region-guide/">regional fees guide</a>. And for the complete country breakdown, see <a href="/careers/jobs-by-country/">jobs by country</a>.</p>

{faq_html(faq_pairs)}
{jobmkt_related_links("spain-europe-gtm-engineering")}
</div>
'''
    body += source_citation_html()
    body += newsletter_cta_html("Get weekly European GTM Engineer market data.")
    extra_head = get_breadcrumb_schema(crumbs) + get_faq_schema(faq_pairs)

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/careers/spain-europe-gtm-engineering/",
        body_content=body, active_path="/careers/",
        extra_head=extra_head, body_class="page-inner",
    )
    write_page("careers/spain-europe-gtm-engineering/index.html", page)
    print(f"  Built: careers/spain-europe-gtm-engineering/index.html")


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
    build_salary_agency_fees()
    build_salary_agency_fees_region()
    build_salary_seed_vs_enterprise()

    print("\n  Building career pages...")
    build_career_index()
    build_career_how_to_become()
    build_career_operator_vs_engineer()
    build_career_is_real()
    build_career_job_market()
    build_career_how_got_jobs()
    build_career_work_life()
    build_career_demographics()
    build_career_vs_revops()
    build_career_coding_needed()
    build_career_reporting_structure()
    build_career_impact()
    build_career_skills_gap()

    print("\n  Building agency pages...")
    build_agency_pricing()
    build_agency_start()
    build_agency_vs_freelance()
    build_agency_retention()
    build_agency_client_count()
    build_agency_pricing_models()
    build_agency_regional_fees()
    build_agency_deliverability()

    print("\n  Building job market pages...")
    build_jobmkt_growth()
    build_jobmkt_by_country()
    build_jobmkt_posted_vs_actual()
    build_jobmkt_top_skills()
    build_jobmkt_monthly_trends()
    build_jobmkt_salary_bands()
    build_jobmkt_india()
    build_jobmkt_spain()

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
