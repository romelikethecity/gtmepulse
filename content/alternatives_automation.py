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
}
