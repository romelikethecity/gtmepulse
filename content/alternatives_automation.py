"""Alternatives content for Workflow Automation tools (Zapier)."""

ALTERNATIVES = {
    "zapier": {
        "intro": """<p>Zapier is the automation tool that taught the world what workflow automation could do. 7,000+ integrations, a dead-simple interface, and a free tier that lets you connect two apps with zero code. But Zapier's simplicity becomes its limitation the moment your workflows get complex. Per-task pricing at $19.99-$599/month punishes high-volume automation. The linear step-by-step builder can't handle branching logic, loops, or error handling without ugly workarounds.</p>
<p>GTM Engineers outgrow Zapier fast. The first time you need to loop through an array of leads, transform JSON from a webhook, or build a multi-branch workflow that handles success and failure differently, Zapier forces you into hacks or paid add-ons. The per-task pricing model means a workflow that runs 10,000 times a month costs real money, while alternatives offer flat-rate or unlimited execution pricing.</p>
<p>The alternatives below range from visual automation tools that handle complexity better, to self-hosted platforms where you own the infrastructure and pay nothing per execution. Most GTM Engineers have already made this switch.</p>""",

        "alternatives": [
            {
                "name": "Make (Integromat)",
                "slug": "make-review",
                "tagline": "Visual automation with real branching and data transformation",
                "best_for": "Power users who need complex workflows with branching, loops, and data transformation at lower cost than Zapier",
                "pros": [
                    "Visual flowchart builder with unlimited branching and routers",
                    "Full array iteration and JSON manipulation",
                    "Per-operation pricing is cheaper than Zapier's per-task model",
                    "Error routes for graceful failure handling",
                ],
                "cons": [
                    "Steeper learning curve than Zapier's simple interface",
                    "1,800 integrations vs Zapier's 7,000+",
                    "Per-operation pricing still scales with volume (unlike n8n self-hosted)",
                ],
                "pricing": "Free (1,000 ops/mo). Paid $9-$299/mo",
                "verdict": "Make is the first Zapier alternative most GTM Engineers try. The visual builder is more powerful (routers, iterators, error handling), and the pricing is more forgiving. If your workflows need any complexity beyond linear trigger-action chains, Make handles it natively where Zapier requires workarounds. The integration library is smaller, but HTTP modules fill most gaps.",
            },
            {
                "name": "n8n",
                "slug": "n8n-review",
                "tagline": "Self-hosted automation with zero per-execution costs",
                "best_for": "GTM Engineers who want unlimited automation on their own infrastructure with Python support",
                "pros": [
                    "Self-hosted: zero per-execution costs on a $10/mo VPS",
                    "Python + JavaScript code nodes for custom logic",
                    "Git-based workflow versioning",
                    "54% adoption among GTM Engineers in our 2026 survey",
                ],
                "cons": [
                    "Requires basic Linux/Docker skills to self-host",
                    "400+ integrations (fewer than Zapier or Make)",
                    "Interface is functional but less polished than Make",
                ],
                "pricing": "Free (self-hosted). Cloud from $20/mo",
                "verdict": "n8n is the Zapier alternative for GTM Engineers who want to own their automation infrastructure. Self-hosting eliminates per-execution costs entirely. Python code nodes mean you can run enrichment scripts, data transforms, and API calls in the language you already know. At 54% adoption in our survey, n8n has already won this category among technical users. If you can manage a Linux server, there's no reason to pay Zapier.",
            },
            {
                "name": "Clay",
                "slug": "clay-review",
                "tagline": "GTM-specific automation with 75+ data integrations",
                "best_for": "GTM Engineers who use Zapier primarily for enrichment and prospecting workflows",
                "pros": [
                    "Purpose-built for GTM workflows (enrichment, scoring, routing)",
                    "75+ data provider integrations in one platform",
                    "AI research agent for custom data points",
                    "Visual workflow builder designed for data operations",
                ],
                "cons": [
                    "Only handles GTM workflows, not general automation",
                    "Credit-based pricing that scales with data volume",
                    "Can't replace Zapier for non-GTM integrations (Slack, Google Sheets, etc.)",
                ],
                "pricing": "$149-$800/mo",
                "verdict": "Clay replaces Zapier specifically for GTM data workflows. If your Zapier zaps are mostly 'when X happens, enrich a lead and push to CRM,' Clay does that better with waterfall enrichment, AI research, and GTM-native logic. It won't replace Zapier for Slack notifications or spreadsheet syncing. Use Clay for GTM pipelines and n8n/Make for everything else.",
            },
            {
                "name": "Tray.io",
                "slug": None,
                "tagline": "Enterprise automation platform with unlimited API connectors",
                "best_for": "Enterprise teams that need Zapier-like automation with SOC 2 compliance, SLAs, and unlimited API connections",
                "pros": [
                    "Enterprise-grade security and compliance (SOC 2, HIPAA)",
                    "Universal connector lets you integrate with any REST API",
                    "Complex data mapping and transformation",
                    "Team workspaces with role-based access",
                ],
                "cons": [
                    "Enterprise pricing (starts around $600/mo)",
                    "Overkill for small teams and simple automations",
                    "Learning curve is steep compared to Zapier",
                ],
                "pricing": "Custom, starts around $600/mo",
                "verdict": "Tray.io is the Zapier alternative for enterprise teams that need compliance certifications and SLAs. If your security team rejected Zapier because of data handling concerns, Tray.io checks the enterprise boxes. The pricing is enterprise-level, but so are the capabilities. Most GTM teams won't need this. Enterprise RevOps teams with complex, regulated data flows might.",
            },
            {
                "name": "Pipedream",
                "slug": None,
                "tagline": "Code-first automation with a generous free tier",
                "best_for": "Developers and GTM Engineers who prefer writing code over visual builders",
                "pros": [
                    "Write Node.js or Python directly (not constrained by visual UI)",
                    "Generous free tier (10,000 invocations/month)",
                    "Connect to any API with custom code",
                    "Built-in data store for workflow state",
                ],
                "cons": [
                    "Requires coding skills (not accessible for non-technical users)",
                    "Visual builder is basic compared to Make or n8n",
                    "Smaller community than established automation platforms",
                ],
                "pricing": "Free (10K invocations/mo). Paid from $19/mo",
                "verdict": "Pipedream is Zapier for developers. If you find visual builders limiting and want to write JavaScript or Python for your automations, Pipedream gives you a hosted runtime with a generous free tier. It's faster to build custom integrations in code than clicking through Zapier's UI. The trade-off: your team needs to maintain code, not drag-and-drop workflows.",
            },
        ],

        "faq": [
            ("Is Zapier still worth using?", "For non-technical users connecting two apps with simple trigger-action logic, Zapier is still the fastest option. The 7,000+ integrations mean it connects to everything. For GTM Engineers with technical skills and high-volume workflows, Zapier's per-task pricing and limited logic make alternatives like n8n or Make better choices."),
            ("What's the best free Zapier alternative?", "n8n self-hosted is free with unlimited executions. Pipedream's free tier gives you 10,000 invocations/month. Make's free tier offers 1,000 operations/month. For fully free automation, self-hosted n8n can't be beat. You'll need a $5-$10/month VPS, but the software itself costs nothing."),
            ("Can I migrate my Zaps to another tool?", "There's no automatic migration. You'll need to rebuild each workflow in the new tool. The logic translates (triggers, actions, filters map to similar concepts in Make/n8n), but the configuration doesn't port. Plan for 15-30 minutes per simple Zap and 1-2 hours for complex multi-step workflows."),
            ("Why do GTM Engineers leave Zapier?", "Three reasons dominate: (1) per-task pricing escalates as automation volume grows, (2) the linear builder can't handle complex branching, loops, and error handling, and (3) no Python support for inline data processing. Most switch to n8n (self-hosted, unlimited, Python support) or Make (visual power, lower per-operation cost)."),
        ],
    },

    "make": {
        "intro": """<p>Make (formerly Integromat) is the visual workflow automation platform that GTM Engineers reach for when Zapier feels limiting and n8n feels overengineered. At $9-$34/month with per-operation pricing, Make sits in the middle of the automation market on both price and complexity. The product is solid for visual multi-step workflows but has real limitations that push teams toward alternatives.</p>
<p>Teams explore Make alternatives for predictable reasons: operation-based pricing gets expensive at scale (a multi-step scenario processing 1,000 records burns 5,000+ operations per run), debugging complex scenarios is painful (no consolidated data view across 20-step flows), error handling configuration requires understanding Make's specific taxonomy, and community modules vary wildly in quality. Performance issues on browser-based scenario editing also frustrate teams running scenarios with 30+ modules.</p>
<p>The alternatives below cover three categories: self-hosted tools that eliminate per-execution costs (n8n), no-code tools that prioritize simplicity over flexibility (Zapier), and developer-first tools that trade visual building for code-based flexibility. The right choice depends on whether you optimize for cost, simplicity, or programming flexibility.</p>""",

        "alternatives": [
            {
                "name": "n8n",
                "slug": "n8n-review",
                "tagline": "Self-hosted automation with code-first flexibility",
                "best_for": "Technical GTM Engineers who want unlimited workflow executions at zero per-run cost",
                "pros": [
                    "Self-hosted version is free with unlimited executions",
                    "JavaScript and Python code nodes for custom logic",
                    "Git-based workflow versioning treats workflows as code",
                    "400+ native integrations plus community-built nodes",
                ],
                "cons": [
                    "Self-hosting requires DevOps skills and infrastructure management",
                    "Browser UI lags on workflows with 30+ nodes",
                    "Some community nodes lack documentation and stability",
                ],
                "pricing": "$0 (self-hosted) - $60/mo (cloud)",
                "verdict": "n8n is the right Make alternative for GTM Engineers willing to self-host. The cost savings at scale are dramatic: zero per-execution fees versus Make's per-operation pricing that scales linearly with usage. The trade-off is operational responsibility for server uptime, backups, and upgrades. For technical teams running 10K+ operations per month, n8n's self-hosted economics produce 80-95% cost savings versus equivalent Make scenarios.",
            },
            {
                "name": "Zapier",
                "slug": "zapier-review",
                "tagline": "Simpler automation with the broadest integration library",
                "best_for": "Teams that want the easiest possible setup with 6,000+ pre-built integrations",
                "pros": [
                    "6,000+ integrations (versus Make's 1,800+)",
                    "Simpler trigger-action mental model for non-technical users",
                    "Faster setup for basic point-to-point automations",
                    "AI features for natural-language workflow creation",
                ],
                "cons": [
                    "Per-task pricing gets expensive at scale (more so than Make)",
                    "Limited branching and iteration compared to Make's flowchart builder",
                    "Data transformation features are basic without Code by Zapier",
                ],
                "pricing": "$0-$103.50/mo",
                "verdict": "Zapier is the right Make alternative when simplicity matters more than flexibility. For teams running fewer than 1,000 tasks per month with mostly simple trigger-action patterns, Zapier delivers faster setup and broader integration coverage. The cost case turns negative above 1,000 tasks per month, where Make's per-operation pricing usually undercuts Zapier's per-task pricing.",
            },
            {
                "name": "Tray.io",
                "slug": None,
                "tagline": "Enterprise automation platform with serious data manipulation",
                "best_for": "Enterprise teams running complex multi-system integrations with deep data transformation needs",
                "pros": [
                    "Most-mature data transformation features in the visual automation space",
                    "Enterprise security, compliance, and audit logging",
                    "Strong support for complex API patterns (OAuth, pagination, rate limiting)",
                    "Native ETL and reverse ETL capabilities alongside workflow automation",
                ],
                "cons": [
                    "Enterprise pricing (starts $2K+/month, typical $30K-$100K/year)",
                    "Steeper learning curve than Make's drag-and-drop interface",
                    "Overkill for simple multi-step workflows",
                ],
                "pricing": "Custom, typically $30K-$100K+/yr",
                "verdict": "Tray.io is the Make alternative for enterprise teams with serious data transformation requirements and budget to match. The product handles complex data workflows that Make struggles with (large payload transformations, sophisticated branching logic, enterprise security controls). For mid-market or below, Tray is overkill. For Fortune 500 enterprise teams running integrations across 20+ systems, Tray is often the right answer.",
            },
            {
                "name": "Pipedream",
                "slug": None,
                "tagline": "Developer-first workflow platform with Node.js and Python",
                "best_for": "Engineering-fluent GTM teams that prefer code over visual builders",
                "pros": [
                    "First-class code-step support in Node.js and Python",
                    "Generous free tier with 100K invocations per month",
                    "Strong API for building, deploying, and managing workflows programmatically",
                    "Built-in event sources and HTTP triggers without separate setup",
                ],
                "cons": [
                    "Smaller visual-building audience than Make",
                    "Fewer pre-built integrations than Make or Zapier",
                    "Best suited to workflows that benefit from custom code",
                ],
                "pricing": "Free (100K invocations) - $19+/mo",
                "verdict": "Pipedream is the right Make alternative for GTM Engineers who prefer writing code to wiring visual modules. The generous free tier covers most early-stage outbound automations, and the code-first approach handles edge cases that Make's visual builder can't express cleanly. The trade-off is a smaller community and fewer pre-built patterns, which makes Pipedream best for teams comfortable building from primitives.",
            },
            {
                "name": "Workato",
                "slug": None,
                "tagline": "Enterprise iPaaS with strong governance and recipe sharing",
                "best_for": "Large companies that need centralized automation governance across many teams",
                "pros": [
                    "Strong recipe-sharing model (one team builds, others reuse)",
                    "Enterprise governance, security, and audit logging",
                    "Pre-built recipes for common business processes",
                    "Solid support for complex enterprise integration patterns",
                ],
                "cons": [
                    "Enterprise pricing (typical $20K-$80K/year)",
                    "Less GTM-specific recipe library than Make's community",
                    "Pricing model based on workflow count plus tasks gets complex",
                ],
                "pricing": "Custom, typically $20K-$80K/yr",
                "verdict": "Workato is the Make alternative for large companies with central IT or RevOps functions running automation governance across many business units. The recipe-sharing model and governance controls justify the enterprise pricing at sufficient scale. For single-team or smaller-org use cases, Workato is overpriced versus Make's per-operation model.",
            },
            {
                "name": "Latenode",
                "slug": None,
                "tagline": "Visual automation with AI-native node design",
                "best_for": "Teams building AI-heavy workflows that need LLM nodes integrated into the visual builder",
                "pros": [
                    "Native AI/LLM nodes for OpenAI, Anthropic, and others",
                    "Code nodes alongside visual builder for hybrid workflows",
                    "Generous free tier compared to most competitors",
                    "Faster onboarding than Make for AI workflow use cases",
                ],
                "cons": [
                    "Newer platform with smaller integration library",
                    "Less mature community and templates than Make",
                    "Some higher-level features still rolling out",
                ],
                "pricing": "Free - $97/mo",
                "verdict": "Latenode is the emerging Make alternative for teams building AI-heavy GTM workflows. The native LLM nodes eliminate the friction of orchestrating OpenAI or Anthropic APIs through Make's HTTP module. The platform is newer and less proven than Make, but for teams whose workflows are primarily AI orchestration rather than traditional API integration, the AI-native design is meaningfully better.",
            },
        ],

        "faq": [
            ("Is n8n really cheaper than Make at scale?",
             "Yes, dramatically. Self-hosted n8n costs $5-$20/month in server hosting with no per-execution fees. Make's Pro plan at $16/month gives you 10,000 operations. At 100,000 operations per month, Make costs ~$100/month (operation packs). At 1M operations, Make costs $700-$1,000/month. n8n stays at the server cost regardless of execution volume. For high-volume GTM workflows, the n8n cost advantage is 80-95% versus Make."),
            ("Can I migrate workflows from Make to n8n?",
             "Not automatically. There's no direct migration tool. You'll need to rebuild workflows manually. The concepts translate (Make modules map to n8n nodes, data mapping is similar), but the configuration doesn't port. Plan for 1-2 hours per workflow for migration depending on complexity. The migration cost is real but typically amortizes against the cost savings within 3-6 months at scale."),
            ("Which Make alternative has the best AI features?",
             "Latenode has the most AI-native design, with first-class LLM nodes built into the visual builder. n8n has solid AI nodes too, with the advantage of unlimited execution volume for AI workflows that would be expensive on operation-based pricing. Pipedream's code-first approach gives the most flexibility for custom AI workflows. Make's AI features lag the alternatives, though Make handles AI workflows fine through the HTTP module."),
            ("Should I pick Make or n8n for a new GTM stack in 2026?",
             "If you have engineering capacity to self-host: n8n. The cost advantage compounds significantly at scale. If you don't have engineering capacity to manage server infrastructure: Make. The cost premium is worth not having to be your own DevOps team. The middle path that some teams take: start on Make for the first 6-12 months while building out workflows, then migrate to n8n once volume justifies the engineering investment."),
            ("What about Power Automate or Azure Logic Apps?",
             "Microsoft's automation tools work fine inside Microsoft ecosystems but have weaker third-party integration libraries than Make, Zapier, or n8n. For GTM workflows that mostly touch HubSpot, Salesforce, Outreach, Apollo, and similar SaaS tools, the Microsoft options are usually slower to configure and less flexible than the dedicated automation platforms. For companies deep in the Microsoft ecosystem with mostly Microsoft-source data, Power Automate can work, but it's not a typical GTM Engineering choice."),
        ],
    },
}
