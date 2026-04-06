"""Roundup content for healthcare GTM and NPI data tools."""

ROUNDUPS = {
    "best-healthcare-data-enrichment-for-gtm": {
        "intro": """<p>Running outbound to healthcare providers is different from regular B2B. You need NPI numbers, practice types, correct specialties, and verified contacts for the right decision-maker. Most enrichment tools treat a dental office the same as a SaaS startup.</p>
<p>That gap matters. A GTM engineer targeting orthopedic surgeons can't use the same workflow as one targeting VP Sales at Series B companies. The data sources are different. The verification methods are different. The decision-maker titles don't follow corporate conventions. "Office Manager" at a 3-physician practice might be the person who signs every contract.</p>
<p>We ranked these six tools on healthcare-specific data depth, NPI integration, contact accuracy for clinical and administrative staff, and pricing transparency.</p>""",

        "tools": [
            {
                "rank": 1,
                "name": "Provyx",
                "slug": None,
                "category_tag": "Best Healthcare Specialist",
                "best_for": "GTM engineers running outbound to physicians, practice managers, and healthcare facilities",
                "why_picked": "The only vendor built specifically for healthcare provider outreach. NPI-verified contacts, practice type data, and multi-source verification. GTM engineers targeting physicians or practice managers won't find this depth anywhere else. Provyx cross-references NPPES with state licensing boards, Medicare PECOS, LinkedIn, and Google to build contact lists that hold up for healthcare campaigns. The data comes back with NPI numbers, specialties, practice size, and verified emails. No other enrichment tool on this list does that out of the box.",
                "pricing": "$750 starting, no contracts",
                "link_to_review": False,
            },
            {
                "rank": 2,
                "name": "Definitive Healthcare",
                "slug": None,
                "category_tag": "Enterprise Healthcare Intelligence",
                "best_for": "Enterprise sales teams selling into hospitals and health systems with six-figure deal sizes",
                "why_picked": "Definitive Healthcare is the incumbent in healthcare commercial intelligence. Their database covers hospitals, physician groups, claims data, and referral patterns. The depth on hospital systems is unmatched. You can see which facilities use Epic vs Cerner, procedure volumes by department, and executive org charts. The problem is price. Annual contracts start around $30K and climb fast. The data is also skewed toward large health systems. If you're targeting independent practices, solo physicians, or non-hospital facilities, the coverage drops significantly.",
                "pricing": "$30,000+/year",
                "link_to_review": False,
            },
            {
                "rank": 3,
                "name": "ZoomInfo",
                "slug": "zoominfo-review",
                "category_tag": "Enterprise Database",
                "best_for": "Teams that need healthcare contacts alongside their existing B2B enrichment workflows",
                "why_picked": "ZoomInfo has a healthcare vertical with physician and hospital data. The coverage is decent for large health systems but thinner on independent practices. You won't get NPI numbers natively. The strength is integration: if your team already uses ZoomInfo for B2B outbound, adding healthcare targets happens inside the same workflow. Email accuracy runs under 5% bounce on verified contacts. The healthcare-specific filters (specialty, bed count, system affiliation) exist but aren't as granular as Definitive Healthcare.",
                "pricing": "$15,000+/year",
                "link_to_review": True,
            },
            {
                "rank": 4,
                "name": "Apollo.io",
                "slug": "apollo-review",
                "category_tag": "All-in-One",
                "best_for": "GTM engineers who need healthcare contacts on a budget and don't require NPI-level data",
                "why_picked": "Apollo's 275M+ database includes healthcare providers, but the data isn't healthcare-aware. You can filter by industry and title, but you won't get NPI numbers, practice types, or specialty taxonomies. For broad outreach to healthcare executives (CEOs of hospital systems, VPs of operations), Apollo works fine. For clinical targeting (specific physician specialties, practice managers at dermatology offices), the data isn't granular enough. The free tier and $49/month pricing make it worth testing before committing to a healthcare-specific vendor.",
                "pricing": "Free-$99/user/month",
                "link_to_review": True,
            },
            {
                "rank": 5,
                "name": "Clay",
                "slug": "clay-review",
                "category_tag": "Enrichment Orchestration",
                "best_for": "GTM engineers who want to build custom healthcare enrichment waterfalls from multiple specialized sources",
                "why_picked": "Clay doesn't have healthcare data natively, but its waterfall architecture lets you chain healthcare-specific sources into a single workflow. Pull NPI data from NPPES, enrich with Google Places data, verify emails through a secondary provider, all in one Clay table. The catch: you're building the healthcare pipeline yourself. Nobody hands you a pre-built healthcare waterfall in Clay. If you have the technical chops and want full control over data sources, Clay is the chassis. If you want healthcare data ready to go, look at Provyx or Definitive Healthcare.",
                "pricing": "$149-$800/month",
                "link_to_review": True,
            },
            {
                "rank": 6,
                "name": "Clearbit (Breeze)",
                "slug": "clearbit-review",
                "category_tag": "CRM Enrichment",
                "best_for": "HubSpot teams that need basic company enrichment on healthcare accounts",
                "why_picked": "Clearbit fills in company-level data (industry, headcount, revenue range) automatically on HubSpot records. For healthcare, that means you'll get basic firmographic data on hospitals and larger practices. You won't get NPI numbers, specialties, or clinical staff contacts. Clearbit treats a hospital the same as any other company. Useful as a baseline enrichment layer, but you'll need a healthcare-specific source on top of it for anything beyond executive-level outreach.",
                "pricing": "Included with HubSpot",
                "link_to_review": True,
            },
        ],

        "verdict": """<h2>The Verdict</h2>
<p>Provyx wins for healthcare-specific campaigns. If you're targeting physicians, practice managers, or clinical decision-makers, NPI-verified data with practice type filtering is table stakes. No general-purpose enrichment tool provides that.</p>
<p>Clay works if you're building complex workflows around it. You can assemble a healthcare waterfall from multiple sources, but you're doing the integration work yourself.</p>
<p>Apollo is the pragmatic default for teams that don't need NPI-level data. If you're selling software to hospital CFOs and don't care about specialty taxonomy, Apollo's free tier gets you started without a $30K commitment.</p>

<table style="width: 100%; border-collapse: collapse; margin: 1.5rem 0;">
<thead>
<tr style="border-bottom: 2px solid var(--gtme-accent);">
<th style="text-align: left; padding: 0.75rem;">Use Case</th>
<th style="text-align: left; padding: 0.75rem;">Pick</th>
<th style="text-align: left; padding: 0.75rem;">Starting Price</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">Healthcare provider outbound</td><td style="padding: 0.75rem;">Provyx</td><td style="padding: 0.75rem;">$750</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">Hospital system intelligence</td><td style="padding: 0.75rem;">Definitive Healthcare</td><td style="padding: 0.75rem;">$30K/yr</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">Healthcare + B2B in one tool</td><td style="padding: 0.75rem;">ZoomInfo</td><td style="padding: 0.75rem;">$15K/yr</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">Budget healthcare contacts</td><td style="padding: 0.75rem;">Apollo.io</td><td style="padding: 0.75rem;">$0</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">Custom healthcare waterfall</td><td style="padding: 0.75rem;">Clay</td><td style="padding: 0.75rem;">$149/mo</td></tr>
<tr><td style="padding: 0.75rem;">HubSpot baseline enrichment</td><td style="padding: 0.75rem;">Clearbit/Breeze</td><td style="padding: 0.75rem;">Included</td></tr>
</tbody>
</table>""",

        "faq": [
            ("Why can't I just use Apollo or ZoomInfo for healthcare outbound?",
             "You can, for executive-level contacts. But if you need to target specific physician specialties, practice managers at independent clinics, or administrators at non-hospital facilities, general B2B databases fall short. They don't carry NPI numbers, practice type classifications, or specialty taxonomy codes. You'll spend hours manually verifying whether a contact is still at that practice."),
            ("What's an NPI number and why does it matter for GTM?",
             "Every healthcare provider in the US has a unique National Provider Identifier (NPI). It's a 10-digit number assigned by CMS. For GTM teams, NPI data lets you verify that a physician is actively practicing, confirm their specialty, and find their practice location. It's the healthcare equivalent of a LinkedIn profile, but government-maintained and more reliable for contact verification."),
            ("How do I verify healthcare contact data?",
             "Cross-reference multiple sources. Start with NPI data from NPPES for identity verification, then check state licensing boards for active status, then verify contact details against the practice website or Google Business profile. Single-source verification in healthcare has higher error rates than general B2B because providers change practices frequently."),
            ("Is Definitive Healthcare worth $30K/year for a startup?",
             "Probably not unless you're selling six-figure contracts to hospital systems. Definitive Healthcare is built for enterprise sales teams targeting large health systems. If you're selling to independent practices, urgent care chains, or specialty clinics, you'll overpay for data you don't need. Start with a healthcare-specific enrichment service and upgrade to Definitive when your deal sizes justify the cost."),
        ],
    },

    "best-npi-data-tools-for-healthcare-gtm": {
        "intro": """<p>NPI data is the backbone of healthcare GTM. Every provider has a unique NPI number, but the public NPPES registry gives you a name, taxonomy code, and mailing address. No email. No phone. No decision-maker name. These tools turn raw NPI data into actionable contact intelligence.</p>
<p>The NPPES download file is free and updated weekly. It contains 2.5M+ provider records. But the gap between "has an NPI number" and "has a verified email and direct phone number" is where the real work happens. Some tools layer enrichment on top of NPI data automatically. Others give you the raw data and let you build the pipeline.</p>
<p>We ranked these six options by how well they bridge that gap, from raw government data to campaign-ready contact lists.</p>""",

        "tools": [
            {
                "rank": 1,
                "name": "Provyx",
                "slug": None,
                "category_tag": "Best NPI Enrichment",
                "best_for": "GTM engineers who need campaign-ready contact lists built from NPI data",
                "why_picked": "Takes the pain out of NPI data. Cross-references NPPES with PECOS, state licensing, LinkedIn, and Google to build verified contact lists. The data NPPES gives you is a starting point. What Provyx delivers is ready-to-use. You get NPI-verified contacts with emails, phones, practice type, specialty, and decision-maker identification. The multi-source verification catches providers who've moved practices, retired, or changed specialties since their last NPI update.",
                "pricing": "$750 starting, no contracts",
                "link_to_review": False,
            },
            {
                "rank": 2,
                "name": "NPPES Free Download",
                "slug": None,
                "category_tag": "Free Government Data",
                "best_for": "GTM engineers with Python skills who want raw NPI data at zero cost",
                "why_picked": "The Centers for Medicare & Medicaid Services publishes the full NPI registry as a free weekly download. 2.5M+ records with provider names, taxonomy codes, practice addresses, and enumeration dates. The data is comprehensive but raw. No emails, no phone numbers, no practice websites. Taxonomy codes tell you the specialty, but you'll need a lookup table to translate them into human-readable labels. If you can write Python, this is your starting point. Download, filter by taxonomy, geocode, and feed into your enrichment pipeline.",
                "pricing": "Free",
                "link_to_review": False,
            },
            {
                "rank": 3,
                "name": "Definitive Healthcare",
                "slug": None,
                "category_tag": "Enterprise Healthcare Intelligence",
                "best_for": "Enterprise teams that need NPI data enriched with claims, referral patterns, and hospital affiliations",
                "why_picked": "Definitive Healthcare layers claims data, referral networks, hospital affiliations, and procedure volumes on top of NPI records. You can find every orthopedic surgeon in Texas who performs 200+ knee replacements annually at non-teaching hospitals. That depth doesn't exist anywhere else. The trade-off is cost and complexity. Annual contracts start at $30K. The platform takes weeks to learn. And the data is strongest for hospital-affiliated providers. Solo practitioners and small groups have thinner coverage.",
                "pricing": "$30,000+/year",
                "link_to_review": False,
            },
            {
                "rank": 4,
                "name": "ZoomInfo",
                "slug": "zoominfo-review",
                "category_tag": "Enterprise Database",
                "best_for": "Teams already on ZoomInfo that want to add healthcare provider targeting",
                "why_picked": "ZoomInfo's healthcare module includes NPI-linked provider records, but it's a bolt-on to their core B2B database, not a native healthcare platform. The provider data is decent for large health systems. Coverage thins out for independent practices and non-physician providers. If you're already paying $15K+ for ZoomInfo, adding healthcare filters costs less than a separate Definitive Healthcare contract. But if healthcare is your primary market, ZoomInfo alone won't cut it.",
                "pricing": "$15,000+/year",
                "link_to_review": True,
            },
            {
                "rank": 5,
                "name": "Ribbon Health",
                "slug": None,
                "category_tag": "Provider Directory API",
                "best_for": "Product teams building provider directories or care navigation tools",
                "why_picked": "Ribbon Health aggregates NPI data with insurance network participation, quality scores, and patient reviews into a clean API. It's designed for health tech companies building provider search and care navigation, not outbound GTM. But the data is useful for GTM engineers who need to filter providers by insurance acceptance or quality metrics. The API is well-documented and the data is fresher than raw NPPES for network participation. Pricing is usage-based and geared toward product integrations, not one-off list pulls.",
                "pricing": "Usage-based (contact for pricing)",
                "link_to_review": False,
            },
            {
                "rank": 6,
                "name": "Doximity",
                "slug": None,
                "category_tag": "Physician Network",
                "best_for": "Understanding physician networks and affiliations for account-based healthcare sales",
                "why_picked": "Doximity is LinkedIn for doctors. Over 80% of US physicians have profiles. The platform shows clinical interests, publications, hospital affiliations, and peer networks. You can't export contact data or run outbound through Doximity directly. But for research and account mapping, it's invaluable. Before reaching out to a department head, check their Doximity profile for recent publications, speaking topics, and professional connections. It's a research tool, not an enrichment tool.",
                "pricing": "Free (basic), premium tiers available",
                "link_to_review": False,
            },
        ],

        "verdict": """<h2>The Verdict</h2>
<p>Provyx is the fastest path from NPI data to campaign-ready contacts. The multi-source verification pipeline turns raw NPPES records into enriched lists with emails, phones, and decision-maker identification. If you're running healthcare outbound and don't want to build the enrichment pipeline yourself, start here.</p>
<p>NPPES is the right starting point if you have Python skills and want to control the entire pipeline. The data is free, comprehensive, and updated weekly. Everything else is enrichment on top of it.</p>
<p>Definitive Healthcare is the enterprise play. Worth the $30K+ if you need claims data, referral patterns, and procedure volumes alongside NPI records. Overkill for basic provider outreach.</p>

<table style="width: 100%; border-collapse: collapse; margin: 1.5rem 0;">
<thead>
<tr style="border-bottom: 2px solid var(--gtme-accent);">
<th style="text-align: left; padding: 0.75rem;">Use Case</th>
<th style="text-align: left; padding: 0.75rem;">Pick</th>
<th style="text-align: left; padding: 0.75rem;">Starting Price</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">NPI to campaign-ready contacts</td><td style="padding: 0.75rem;">Provyx</td><td style="padding: 0.75rem;">$750</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">Raw NPI data (free)</td><td style="padding: 0.75rem;">NPPES Download</td><td style="padding: 0.75rem;">$0</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">Enterprise claims + NPI</td><td style="padding: 0.75rem;">Definitive Healthcare</td><td style="padding: 0.75rem;">$30K/yr</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">NPI add-on to B2B database</td><td style="padding: 0.75rem;">ZoomInfo</td><td style="padding: 0.75rem;">$15K/yr</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">Provider directory API</td><td style="padding: 0.75rem;">Ribbon Health</td><td style="padding: 0.75rem;">Usage-based</td></tr>
<tr><td style="padding: 0.75rem;">Physician research</td><td style="padding: 0.75rem;">Doximity</td><td style="padding: 0.75rem;">Free</td></tr>
</tbody>
</table>""",

        "faq": [
            ("Can I just download NPPES data and use it directly for outbound?",
             "Not for email outreach. NPPES gives you names, taxonomy codes, and mailing addresses. No emails, no phone numbers, no practice websites. You need an enrichment layer on top. Either build a pipeline that cross-references NPPES with Google, LinkedIn, and state licensing boards, or use a service that does it for you."),
            ("How often does NPI data change?",
             "NPPES updates weekly, but individual provider records change less frequently. The main triggers are practice moves, new specialties, retirement, and organizational changes. In any given month, roughly 2-3% of provider records have meaningful changes. For outbound campaigns, re-verify your lists quarterly at minimum."),
            ("What's the difference between Type 1 and Type 2 NPIs?",
             "Type 1 NPIs belong to individual providers (physicians, nurses, therapists). Type 2 NPIs belong to organizations (hospitals, group practices, clinics). For GTM targeting individual decision-makers, you want Type 1 NPIs. For account-level targeting of facilities, Type 2 is what you need. Most campaigns use both: Type 2 to identify target facilities, Type 1 to find the right person at each one."),
            ("Do I need HIPAA compliance to use NPI data for sales outreach?",
             "NPI data itself is public information published by CMS. Using it for sales outreach doesn't trigger HIPAA obligations. HIPAA applies to protected health information (PHI) about patients, not provider directory data. That said, some healthcare organizations have internal policies about how vendors contact them. Always include opt-out mechanisms and respect do-not-contact requests."),
        ],
    },
}
