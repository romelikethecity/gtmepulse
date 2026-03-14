"""Roundup content for free GTM tools and AI-powered GTM tools."""

ROUNDUPS = {
    "best-free-gtm-tools": {
        "intro": """<p>You don't need money to start building a GTM pipeline. Between generous free tiers, open-source tools, and freemium CRMs, a resourceful GTM Engineer can assemble a fully functional outbound stack without spending a dollar. The trade-offs are real (rate limits, missing features, manual workarounds), but so is the pipeline you'll generate.</p>
<p>We tested every free GTM tool on three criteria: is the free tier usable for real work (not a 7-day trial), does it integrate with other free tools, and can you upgrade selectively when one tool's limits bottleneck your workflow? Every pick below has a free tier that supports ongoing production use, not just evaluation.</p>
<p>This list is for bootstrapped founders, solo GTM Engineers at pre-revenue startups, and anyone who wants to prove the concept before requesting budget. Build your pipeline first. Get budget from results, not promises.</p>""",

        "tools": [
            {
                "rank": 1,
                "name": "Apollo.io",
                "slug": "apollo-review",
                "category_tag": "Prospecting",
                "best_for": "The single best free tool for GTM: enrichment + outbound sequencing + contact database at $0",
                "why_picked": "Apollo's free tier is absurdly generous. You get 10,000 email credits/month, basic sequencing, a 275M+ contact database, and enough functionality to run real outbound campaigns. Most competing tools charge $50-$150/month for what Apollo gives away. The catch: limited integrations and basic analytics on the free plan. But for a $0 starting point, nothing comes close.",
                "pricing": "$0 (10,000 credits/month free)",
                "link_to_review": True,
            },
            {
                "rank": 2,
                "name": "HubSpot CRM",
                "slug": "hubspot-review",
                "category_tag": "CRM",
                "best_for": "Teams that need a real CRM with contact management, deal tracking, and email templates at zero cost",
                "why_picked": "HubSpot's free CRM is the most capable free CRM on the market. Unlimited contacts, deal pipelines, email tracking, meeting scheduling, and live chat. The free plan even includes Clearbit enrichment data (basic company info). You'll hit walls when you need workflow automation or custom reporting, but as a free foundation, HubSpot beats everything else.",
                "pricing": "$0 (free CRM, unlimited contacts)",
                "link_to_review": True,
            },
            {
                "rank": 3,
                "name": "n8n",
                "slug": "n8n-review",
                "category_tag": "Workflow Automation",
                "best_for": "Technical GTM Engineers who can self-host and want unlimited automations with no per-execution fees",
                "why_picked": "n8n is open-source and free to self-host. Zero execution limits. Zero per-operation fees. If you can spin up a Docker container (30 minutes of setup), you get the same visual workflow builder that cloud automation tools charge $50-$200/month for. The community nodes cover most GTM integrations, and the code node lets you write custom JavaScript for anything that's missing.",
                "pricing": "$0 (self-hosted). Cloud: $24/mo",
                "link_to_review": True,
            },
            {
                "rank": 4,
                "name": "PostHog",
                "slug": "posthog-review",
                "category_tag": "Analytics",
                "best_for": "Product-led teams that need analytics, session replay, and feature flags without paying for three separate tools",
                "why_picked": "PostHog's free tier includes 1 million analytics events, 5,000 session recordings, and unlimited feature flags per month. That covers most early-stage usage. For GTM Engineers, the product analytics feed PQL (product-qualified lead) scoring: which trial users are power users, which features predict conversion, where users drop off. That signal drives targeted outbound.",
                "pricing": "$0 (1M events free/month)",
                "link_to_review": True,
            },
            {
                "rank": 5,
                "name": "LinkedIn Sales Navigator",
                "slug": "linkedin-sales-nav-review",
                "category_tag": "Prospecting",
                "best_for": "Prospecting and research using LinkedIn's free search filters and profile viewing",
                "why_picked": "LinkedIn's free tier still lets you search by company, title, location, and industry. You can view profiles, send connection requests (100/week limit), and use InMail credits when available. It's not Sales Navigator's advanced filters, but for manual prospecting on 20-30 accounts, free LinkedIn plus good boolean search gets the job done. Pair with Apollo for the contact data LinkedIn won't show you.",
                "pricing": "$0 (free LinkedIn account)",
                "link_to_review": True,
            },
        ],

        "verdict": """<h2>The Verdict: Best Free GTM Stack</h2>
<p>Apollo.io is the #1 free GTM tool because it covers the two hardest problems (finding contacts and emailing them) in a single free platform. Start every free GTM stack with Apollo. Add HubSpot for CRM and n8n for automation when you need to connect the pieces.</p>
<p>The complete $0 stack: Apollo (prospecting + outbound) + HubSpot (CRM) + n8n self-hosted (automation) + PostHog (analytics) + LinkedIn free (research). This combination handles enrichment, sequencing, pipeline management, workflow automation, and product signals without a credit card.</p>
<p>When to upgrade: the first tool you should pay for is Clay ($149/month) when Apollo's enrichment depth limits your targeting, or Instantly ($30/month) when Apollo's sending limits cap your volume.</p>

<table style="width: 100%; border-collapse: collapse; margin: 1.5rem 0;">
<thead>
<tr style="border-bottom: 2px solid var(--gtme-accent);">
<th style="text-align: left; padding: 0.75rem;">Function</th>
<th style="text-align: left; padding: 0.75rem;">Free Pick</th>
<th style="text-align: left; padding: 0.75rem;">Free Limits</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">Prospecting + outbound</td><td style="padding: 0.75rem;">Apollo.io</td><td style="padding: 0.75rem;">10K credits/mo</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">CRM</td><td style="padding: 0.75rem;">HubSpot CRM</td><td style="padding: 0.75rem;">Unlimited contacts</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">Automation</td><td style="padding: 0.75rem;">n8n (self-hosted)</td><td style="padding: 0.75rem;">Unlimited</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">Analytics</td><td style="padding: 0.75rem;">PostHog</td><td style="padding: 0.75rem;">1M events/mo</td></tr>
<tr><td style="padding: 0.75rem;">Research</td><td style="padding: 0.75rem;">LinkedIn (free)</td><td style="padding: 0.75rem;">100 connects/wk</td></tr>
</tbody>
</table>""",

        "faq": [
            ("Can you run a real GTM operation on free tools?",
             "Yes, with limitations. Apollo's free tier + HubSpot's free CRM handles prospecting, outbound, and pipeline management for up to 500-1,000 contacts per month. You'll hit volume ceilings, miss some integrations, and spend more time on manual work. But you can book meetings and generate pipeline at $0/month. Many funded startups ran on free tools for 3-6 months before upgrading."),
            ("What's the first free tool to upgrade to a paid plan?",
             "It depends on your bottleneck. If you're limited by data quality (enrichment returning incomplete results), upgrade to Clay at $149/month. If you're capped on email volume, add Instantly at $30/month. If your CRM can't automate follow-ups, upgrade HubSpot to Starter at $45/month. Upgrade the tool that's most limiting your pipeline, not all of them at once."),
            ("Is self-hosting n8n worth the effort?",
             "If you can run Docker, yes. Self-hosted n8n gives you unlimited workflow executions at $0/month. The cloud version starts at $24/month, which is still cheaper than Make or Zapier. Most GTM Engineers self-host on a $5/month VPS and save $200-$500/year compared to cloud automation tools. The 30-minute setup pays for itself in the first month."),
            ("How do free tools compare to enterprise GTM stacks?",
             "A free GTM stack generates roughly 40-60% of the pipeline volume of a $100K+/year enterprise stack. The gaps are in data coverage (fewer enrichment sources), sending volume (lower limits), and analytics depth (basic reporting). For teams under 10 people and under $1M ARR, those gaps rarely matter. Focus on execution quality over tool quality."),
        ],
    },

    "best-ai-tools-gtm": {
        "intro": """<p>AI has changed GTM engineering faster than any other trend in B2B sales. In 2024, "use AI for outbound" meant asking ChatGPT to write cold emails. In 2026, AI enriches contact data in real-time, scores leads based on behavioral signals, generates personalized multi-touch sequences, and automates research that used to take an SDR team 40 hours per week.</p>
<p>We evaluated AI GTM tools on three criteria: does the AI produce output that's production-ready (not "needs a human to fix it"), does it save measurable time (2x faster minimum), and does it integrate into existing GTM workflows (not a standalone toy)? Chatbots that generate generic emails didn't make the cut. Tools where AI is the core value proposition, not a marketing checkbox, did.</p>
<p>The best AI GTM tools don't replace GTM Engineers. They multiply output. One person with Clay's AI enrichment produces the research output of a 5-person SDR team. That's the benchmark.</p>""",

        "tools": [
            {
                "rank": 1,
                "name": "Clay",
                "slug": "clay-review",
                "category_tag": "AI Enrichment",
                "best_for": "GTM Engineers who need AI-powered enrichment, research, and lead scoring across 75+ data sources",
                "why_picked": "Clay's AI agent (Claygent) writes custom prompts that research companies, summarize 10-K filings, score ICP fit, and generate personalized opening lines. AI powers the entire workflow engine. You build tables that chain data providers with AI steps, and the output is enriched records ready for outbound. No other tool combines AI with this breadth of data source access.",
                "pricing": "$0-$800/mo (includes AI credits)",
                "link_to_review": True,
            },
            {
                "rank": 2,
                "name": "Persana AI",
                "slug": "persana-review",
                "category_tag": "AI Prospecting",
                "best_for": "Teams that want AI-native prospecting with signal-based triggers and automated list building",
                "why_picked": "Persana built its entire platform around AI. Signal monitoring detects job changes, funding rounds, and tech stack shifts, then automatically builds prospecting lists from those triggers. The AI writes outbound copy personalized to each signal. It's newer than Clay and less flexible, but for teams that want AI prospecting without building complex workflows, Persana's guided approach reduces setup time.",
                "pricing": "$0-$149/mo",
                "link_to_review": True,
            },
            {
                "rank": 3,
                "name": "Apollo.io",
                "slug": "apollo-review",
                "category_tag": "AI Sequences",
                "best_for": "Teams using Apollo for prospecting who want AI-generated email sequences and persona-based messaging",
                "why_picked": "Apollo added AI sequence generation that creates multi-step email cadences based on your ICP and value proposition. The AI analyzes which subject lines, email lengths, and CTAs perform best across Apollo's dataset of billions of emails. It's not the most sophisticated AI on this list, but it's built into a tool you're probably already using. Zero additional cost on paid plans.",
                "pricing": "Included with Apollo paid plans ($49-$149/mo)",
                "link_to_review": True,
            },
            {
                "rank": 4,
                "name": "Claude / ChatGPT",
                "slug": None,
                "category_tag": "AI Copywriting",
                "best_for": "GTM Engineers who need on-demand copywriting, research synthesis, and workflow scripting",
                "why_picked": "LLMs are the Swiss Army knife of GTM. Claude and ChatGPT handle cold email drafts, ICP research summaries, objection handling scripts, CRM data cleanup, Python automation scripts, and ad-hoc analysis. The key is using them as tools inside your workflow (via API), not as standalone chatbots. GTM Engineers who pipe LLM calls through Make or n8n automate tasks that would take hours manually.",
                "pricing": "Claude: $20/mo (Pro). ChatGPT: $20/mo (Plus). API: pay-per-token",
                "link_to_review": False,
            },
        ],

        "verdict": """<h2>The Verdict: Best AI Tools for GTM</h2>
<p>Clay is the #1 AI GTM tool because its AI is embedded in the data workflow, not bolted on. Claygent plus 75+ data providers means your AI enrichment pulls from real sources, not hallucinated data. The output goes straight into your outbound sequences. No copy-pasting from a chatbot.</p>
<p>Runner-up Persana AI is the pick for teams that want AI-native prospecting without Clay's learning curve. It's more opinionated and less flexible, but the signal-based triggers and automated list building save significant setup time.</p>
<p>The practical reality: most GTM Engineers use Clay for enrichment, Apollo for sequences, and Claude/ChatGPT for everything else (copy, research, scripts). That three-tool AI stack covers 90% of use cases.</p>

<table style="width: 100%; border-collapse: collapse; margin: 1.5rem 0;">
<thead>
<tr style="border-bottom: 2px solid var(--gtme-accent);">
<th style="text-align: left; padding: 0.75rem;">AI Use Case</th>
<th style="text-align: left; padding: 0.75rem;">Quick Pick</th>
<th style="text-align: left; padding: 0.75rem;">Why</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">AI enrichment</td><td style="padding: 0.75rem;">Clay</td><td style="padding: 0.75rem;">75+ sources + AI agent</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">AI prospecting</td><td style="padding: 0.75rem;">Persana AI</td><td style="padding: 0.75rem;">Signal-based triggers</td></tr>
<tr style="border-bottom: 1px solid var(--gtme-bg-surface);"><td style="padding: 0.75rem;">AI sequences</td><td style="padding: 0.75rem;">Apollo.io</td><td style="padding: 0.75rem;">Built into existing tool</td></tr>
<tr><td style="padding: 0.75rem;">AI copywriting</td><td style="padding: 0.75rem;">Claude / ChatGPT</td><td style="padding: 0.75rem;">Flexible via API</td></tr>
</tbody>
</table>""",

        "faq": [
            ("Do AI GTM tools replace SDRs?",
             "They replace the repetitive parts of SDR work: list building, basic research, initial email drafts, and data entry. A GTM Engineer with AI tools produces 3-5x the output of a traditional SDR. But humans still handle strategy, relationship building, complex objection handling, and creative campaign design. The role shifts from doing the work to designing and managing the automated workflow."),
            ("Is AI-generated outbound email effective?",
             "When personalized with real data, yes. AI emails that reference specific company signals (funding round, job posting, tech stack change) outperform generic templates. AI emails that read like generic ChatGPT output (starting with 'I hope this finds you well') underperform human-written emails. The key is feeding AI real prospect data, not asking it to guess."),
            ("How do you integrate AI tools into existing GTM workflows?",
             "Use Make or n8n as the glue layer. A typical AI-enhanced workflow: Clay enriches a new lead with AI research, Make routes the enriched data to your CRM, an LLM API call generates a personalized email draft, and Instantly sends it on schedule. Each AI step takes the output of the previous step as input. Build linearly, test each step, then connect them."),
        ],
    },
}
