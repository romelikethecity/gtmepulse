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
        " Data from the State of GTME Report 2026 (n=228). Updated weekly. Vendor-neutral."
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
        "Complete GTM Engineer salary data: breakdowns by seniority, location, and company"
        " stage. Plus 10 role comparisons. Data from the State of GTME Report 2026 (n=228)."
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
        "How GTME Pulse sources GTM Engineer salary data from the State of GTME Report 2026"
        " (n=228 survey respondents, 3,342 job postings). Sources, methods, and limitations."
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
    <p>Our salary data comes from three primary sources:</p>
    <ul>
        <li><strong>Public job postings:</strong> We scrape job listings from major boards (LinkedIn, Indeed, Greenhouse, Lever, Ashby) twice per week. Postings with disclosed salary ranges are our primary data source.</li>
        <li><strong>Company career pages:</strong> Direct scraping of career pages from 200+ B2B SaaS companies that employ GTM Engineers.</li>
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
    <p>Current dataset: <strong>3,000+ unique job postings</strong> collected since January 2025. Salary data is available for approximately 60% of postings (those with disclosed compensation ranges).</p>
    <p>Sample sizes vary by category. We require a minimum of 50 postings per category to publish salary ranges. Categories below this threshold are noted.</p>

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
    body += newsletter_cta_html("Get weekly data updates.")

    page = get_page_wrapper(
        title=title, description=description, canonical_path="/salary/methodology/",
        body_content=body, active_path="/salary/",
        extra_head=get_breadcrumb_schema(crumbs), body_class="page-inner",
    )
    write_page("salary/methodology/index.html", page)
    print(f"  Built: salary/methodology/index.html")


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
