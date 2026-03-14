"""Comparison content for Workflow Automation matchups."""

COMPARISONS = {
    "make-vs-n8n": {
        "intro": """<p>Make and n8n are the two workflow automation tools GTM Engineers debate most. Both let you connect APIs, transform data, and build multi-step automations without (much) code. But they differ fundamentally: Make is a cloud-hosted visual platform with per-operation pricing. n8n is source-available and self-hostable with no per-execution limits. That architectural difference shapes everything from cost to control.</p>
<p>In our 2026 survey, n8n hit 54% adoption among GTM Engineers, up from under 30% a year ago. Make holds steady at around 35%. Zapier, once the default, has fallen to third among technical users. The trend is clear: GTM Engineers prefer tools that give them more control and lower marginal costs at scale.</p>
<p>This comparison breaks down the real trade-offs between Make's polished cloud experience and n8n's self-hosted power. We'll cover the scenarios where each tool wins and why most GTM Engineers are moving toward n8n.</p>""",

        "feature_table": """<div class="table-responsive"><table class="data-table">
<thead>
<tr><th>Feature</th><th>Make (Integromat)</th><th>n8n</th></tr>
</thead>
<tbody>
<tr><td>Hosting</td><td>Cloud-only</td><td>Self-hosted or cloud</td></tr>
<tr><td>Pricing Model</td><td>Per-operation ($9-$299/mo)</td><td>Free (self-hosted) or $20+/mo (cloud)</td></tr>
<tr><td>Execution Limits</td><td>10K-800K ops/month (by plan)</td><td>Unlimited (self-hosted)</td></tr>
<tr><td>Visual Builder</td><td>Excellent (drag-and-drop modules)</td><td>Good (node-based editor)</td></tr>
<tr><td>Code Nodes</td><td>JavaScript only</td><td>JavaScript + Python</td></tr>
<tr><td>Error Handling</td><td>Built-in retry, error routes</td><td>Built-in retry, error workflows</td></tr>
<tr><td>Integrations</td><td>1,800+ built-in</td><td>400+ built-in + community nodes</td></tr>
<tr><td>API/Webhook</td><td>HTTP module + webhooks</td><td>HTTP node + webhooks</td></tr>
<tr><td>Data Privacy</td><td>Data transits Make's servers</td><td>Data stays on your infrastructure</td></tr>
<tr><td>Version Control</td><td>Scenario history (limited)</td><td>Git-based workflow versioning</td></tr>
<tr><td>Community</td><td>Active forums + templates</td><td>Active community + npm-style node library</td></tr>
<tr><td>Best For</td><td>Non-technical users + quick automations</td><td>Technical users + high-volume pipelines</td></tr>
</tbody>
</table></div>""",

        "tool_a_strengths": """<h2>Where Make Wins</h2>
<p>Make's visual builder is the best in the automation market. Modules snap together with drag-and-drop, data mapping is visual (you can see the JSON structure and click to map fields), and the execution log shows exactly what happened at each step. For building and debugging automations, Make's UX is faster than n8n's, especially for complex multi-branch workflows.</p>
<p>Integration count matters when you're connecting niche tools. Make has 1,800+ pre-built modules compared to n8n's 400+. If you're integrating with a lesser-known CRM, project management tool, or analytics platform, Make is more likely to have a native connector. n8n's community nodes help close the gap, but Make's library is broader.</p>
<p>Error handling in Make is more intuitive. You can create error routes that catch failures at specific modules and route them to alternate paths, retry logic, or error notification workflows. n8n has error handling, but Make's visual approach makes it easier to build resilient automations without deep technical knowledge.</p>
<p>For teams with mixed technical levels (GTM Engineer + non-technical marketing ops), Make's interface is accessible to everyone. Building and maintaining automations doesn't require the GTM Engineer to be the single point of failure. n8n's interface is good but skews more technical.</p>""",

        "tool_b_strengths": """<h2>Where n8n Wins</h2>
<p>Cost at scale is n8n's decisive advantage. Self-hosted n8n costs $0 in software fees. Run it on a $10/month VPS and execute millions of operations per month with zero marginal cost. Make's Pro plan ($16/month) gives you 10,000 operations. A single enrichment waterfall run on 5,000 leads could blow through that in one execution. The math is simple: if you run more than 10,000 operations per month, n8n saves money. Most GTM Engineers run far more than that.</p>
<p>Data sovereignty is non-negotiable for some teams. With self-hosted n8n, your data never leaves your infrastructure. Contact data, enrichment results, CRM syncs, and email content all flow through your own servers. Make routes everything through their cloud. If you're handling sensitive prospect data or your security team has data residency requirements, n8n is the answer.</p>
<p>Python support in code nodes is a differentiator for GTM Engineers. Make only supports JavaScript in code modules. n8n supports both JavaScript and Python. Since Python is the dominant language for data processing, enrichment scripts, and API integrations in the GTM stack, n8n's Python support means you can reuse existing scripts directly in your workflows.</p>
<p>Git-based version control lets you treat workflows as code. Export workflows as JSON, commit them to a repo, create branches for testing, and roll back to previous versions. This is how software engineers manage configuration, and it's how GTM Engineers should manage automation logic. Make's version history is limited to scenario-level snapshots with no branching.</p>
<p>The self-hosted architecture means you control uptime, scaling, and infrastructure. No dependency on Make's SaaS availability. During Make's outages (which happen quarterly), self-hosted n8n users are unaffected.</p>""",

        "pricing_comparison": """<h2>Pricing Breakdown</h2>
<p>Make pricing: Free (1,000 ops/month), Core ($9/mo for 10,000 ops), Pro ($16/mo for 10,000 ops + advanced features), Teams ($29/mo per user for 10,000 ops), Enterprise (custom). Extra operations cost $9 per 10,000. A GTM team running 100,000 operations per month on Pro: $16 + $81 (90K extra ops) = $97/month. At 500,000 ops: $457/month.</p>
<p>n8n cloud pricing: Starter ($20/mo for 2,500 executions), Pro ($50/mo for 10,000 executions), Enterprise (custom). n8n cloud counts executions (workflow runs), not individual operations. One workflow with 10 steps counts as 1 execution, not 10. This makes n8n cloud significantly cheaper than Make at equivalent workflow complexity.</p>
<p>n8n self-hosted: Free. Run it on a $5-$20/month VPS (Hetzner, DigitalOcean, or your existing infrastructure). No execution limits. The total cost is your server bill. A $10/month VPS handles most GTM automation workloads. That's $120/year vs Make's $1,164/year (Pro at 100K ops/month) or more. The self-hosted option is why n8n adoption is accelerating among GTM Engineers who can manage a basic Linux server.</p>""",

        "verdict": """<h2>The Verdict</h2>
<p>Use Make if you value the best visual builder in the market, need broad integration coverage (1,800+ modules), and prefer cloud-hosted simplicity. Make is the right choice for teams with mixed technical levels where non-engineers need to build and maintain automations. If your operation volume stays under 50,000 ops/month, Make's pricing is reasonable.</p>
<p>Use n8n if you run high-volume automations (100K+ operations/month), care about data sovereignty, want Python support, or prefer infrastructure you control. n8n is the technical operator's choice, and at 54% adoption among GTM Engineers, it's becoming the default for a reason. Self-hosting eliminates per-operation costs and gives you full control.</p>
<p>The market is moving toward n8n. The 54% adoption figure tells the story. GTM Engineers are technical users who optimize for cost, control, and flexibility. n8n delivers all three. Make remains excellent for its target audience (visual-first automation users), but that audience increasingly overlaps less with the GTM Engineer profile.</p>""",

        "faq": [
            ("Is n8n hard to self-host?", "No. n8n provides Docker images and one-click deploys for major cloud providers. A GTM Engineer with basic Linux skills can set up n8n on a VPS in under an hour. The community has extensive guides. If you can configure a Clay workflow, you can self-host n8n."),
            ("Can Make handle enterprise-scale automations?", "Yes, but the cost scales linearly with volume. Enterprise plans provide higher operation limits and priority support. For high-volume use cases (millions of ops/month), Make works but costs significantly more than self-hosted n8n."),
            ("Which integrates better with Clay?", "Both work well with Clay via HTTP/webhook nodes. Make's HTTP module is slightly more visual for configuring API calls. n8n's HTTP node is more flexible with code-based request customization. The difference is marginal. Pick based on other factors."),
            ("Can I migrate workflows from Make to n8n?", "There's no direct migration tool. You'd need to rebuild workflows manually. The concepts translate (modules map to nodes, data mapping is similar), but the actual configuration doesn't port. Plan for 1-2 hours per workflow for migration."),
            ("Does n8n cloud have the same benefits as self-hosted?", "n8n cloud gives you the same features without server management, but you lose the cost advantage (cloud pricing is per-execution) and data sovereignty (data transits n8n's infrastructure). For most GTM Engineers, self-hosted is the way to go. Use cloud if you don't want to manage a server."),
        ],
    },

    "make-vs-zapier": {
        "intro": """<p>Make and Zapier are both cloud-hosted automation platforms, but they serve different user profiles. Zapier is the automation tool for non-technical users: simple triggers, actions, and if/then logic. Make is the automation tool for power users: complex workflows with data transformation, branching, iteration, and error handling. For GTM Engineers, Make replaced Zapier in most stacks because Zapier's simplicity becomes a limitation at scale.</p>
<p>Zapier pioneered the automation category and remains the most widely known tool. Over 7,000 integrations make it the broadest connector in the market. But integration count isn't everything. When your workflow needs to loop through an array, transform JSON, handle errors gracefully, or execute conditional logic with more than two branches, Zapier starts breaking down.</p>
<p>This comparison helps GTM Engineers decide whether Zapier's simplicity is enough or whether Make's power justifies the learning curve.</p>""",

        "feature_table": """<div class="table-responsive"><table class="data-table">
<thead>
<tr><th>Feature</th><th>Make (Integromat)</th><th>Zapier</th></tr>
</thead>
<tbody>
<tr><td>Visual Builder</td><td>Flowchart-style (advanced)</td><td>Linear step-by-step</td></tr>
<tr><td>Pricing Model</td><td>Per-operation ($9-$299/mo)</td><td>Per-task ($0-$599/mo)</td></tr>
<tr><td>Free Tier</td><td>1,000 ops/month</td><td>100 tasks/month (5 Zaps)</td></tr>
<tr><td>Integrations</td><td>1,800+</td><td>7,000+</td></tr>
<tr><td>Branching Logic</td><td>Unlimited branches + routers</td><td>Paths (limited, paid feature)</td></tr>
<tr><td>Loops/Iteration</td><td>Full array iteration</td><td>Limited (Looping add-on)</td></tr>
<tr><td>Error Handling</td><td>Error routes + retry logic</td><td>Basic retry (no custom error routing)</td></tr>
<tr><td>Data Transformation</td><td>Built-in functions + JSON manipulation</td><td>Formatter tool (basic)</td></tr>
<tr><td>Code Steps</td><td>JavaScript</td><td>JavaScript + Python (Code by Zapier)</td></tr>
<tr><td>Execution Speed</td><td>Real-time or scheduled</td><td>1-15 min polling (or instant for webhooks)</td></tr>
<tr><td>Webhook Support</td><td>Native (instant triggers)</td><td>Webhooks by Zapier (addon)</td></tr>
<tr><td>Best For</td><td>Complex multi-step automations</td><td>Simple point-to-point integrations</td></tr>
</tbody>
</table></div>""",

        "tool_a_strengths": """<h2>Where Make Wins</h2>
<p>Workflow complexity is where Make pulls away. Make's flowchart builder supports routers (split one path into many), iterators (loop through arrays), aggregators (combine multiple results into one), and error handlers (catch failures and reroute). Zapier's linear step-by-step builder can't express this level of complexity. If your workflow has a single trigger and a single action, Zapier works fine. If it has conditional branches, loops, and error recovery, you need Make.</p>
<p>Data transformation is built into Make's DNA. Every module includes a data mapping panel where you can apply functions (substring, math, date formatting, JSON parsing) inline. Zapier's Formatter tool handles basic transformations, but anything beyond simple text manipulation requires Code by Zapier steps, which are clunky and have execution limits.</p>
<p>Real-time execution gives Make an edge for time-sensitive workflows. Make webhooks trigger instantly. Zapier's polling triggers check for new data every 1-15 minutes depending on your plan. When a lead fills out a form and you want to enrich and route them to a sales rep immediately, that 15-minute delay on Zapier's free tier is a dealbreaker.</p>
<p>Cost per operation is lower. Make counts operations (each step in a workflow = 1 operation). Zapier counts tasks (each action = 1 task, but multi-step Zaps count each step). At equivalent complexity, Make's per-operation cost is typically 30-50% lower than Zapier's per-task cost. The gap widens with workflow complexity.</p>""",

        "tool_b_strengths": """<h2>Where Zapier Wins</h2>
<p>Integration breadth is Zapier's moat. 7,000+ apps vs Make's 1,800+. If you need to connect a niche tool (a specific helpdesk, a regional CRM, a vertical SaaS product), Zapier is more likely to have a pre-built connector. For GTM Engineers, most critical tools (Clay, Apollo, HubSpot, Salesforce, Instantly, Slack) are available on both. But edge cases favor Zapier.</p>
<p>Simplicity is a feature for teams where the GTM Engineer isn't the only person building automations. Zapier's "when this happens, do that" mental model is intuitive enough for sales reps, marketing managers, and founders to build their own Zaps. Make's flowchart builder requires more training. If you want your team to self-serve on simple automations, Zapier has a lower barrier to entry.</p>
<p>Zapier's AI features (natural language workflow creation) are ahead of Make's. You can describe what you want in plain English, and Zapier generates a draft workflow. It's not perfect, but for simple Zaps, it reduces setup time. This matters for quick, throwaway automations that don't justify 30 minutes of manual configuration.</p>
<p>Brand recognition and community size mean more templates, more tutorials, and more third-party guides. When you Google "how to connect [tool] to [tool]," Zapier results dominate. This unofficial documentation layer makes troubleshooting faster.</p>""",

        "pricing_comparison": """<h2>Pricing Breakdown</h2>
<p>Zapier pricing: Free (100 tasks/mo, 5 Zaps), Starter ($29.99/mo for 750 tasks), Professional ($73.50/mo for 2,000 tasks), Team ($103.50/mo for 2,000 tasks + team features), Enterprise (custom). Multi-step Zaps (more than 2 steps) require Starter or above. Paths (branching) require Professional. Extra tasks cost roughly $0.01-$0.05 each depending on plan.</p>
<p>Make pricing: Free (1,000 ops/mo), Core ($9/mo for 10,000 ops), Pro ($16/mo for 10,000 ops + advanced features), Teams ($29/mo/user), Enterprise (custom). Make's free tier gives 10x the operations of Zapier's free tier. Make's Core plan ($9/mo) includes more operations than Zapier's Starter ($29.99/mo).</p>
<p>The pricing gap is significant at every tier. For 10,000 operations/month, Make costs $9-$16. Zapier costs $73.50+ (Professional, needed for multi-step + paths). At 100,000 operations/month, Make costs $97. Zapier costs $500+. GTM Engineers running enrichment pipelines, CRM syncs, and notification workflows easily hit 50,000-100,000 operations per month. At those volumes, Zapier is 3-5x more expensive than Make for similar capabilities.</p>""",

        "verdict": """<h2>The Verdict</h2>
<p>Use Make if you're a GTM Engineer building any automation more complex than a two-step workflow. Make's visual builder, data transformation capabilities, error handling, and pricing make it the clear choice for technical users. The learning curve over Zapier is a few hours at most, and the payoff is enormous in workflow power and cost savings.</p>
<p>Use Zapier only if: (1) you need an integration that Make doesn't have, (2) non-technical team members need to build their own simple automations, or (3) you're building a one-off, two-step integration that doesn't justify learning a new tool. These scenarios exist, but they're increasingly rare as Make's integration library grows.</p>
<p>For most GTM Engineers, the real comparison is Make vs n8n, not Make vs Zapier. Zapier has fallen behind for technical users. If you're still on Zapier, switching to Make saves money immediately and opens up workflow capabilities you didn't have before. If you're evaluating both, skip Zapier and compare Make vs n8n instead.</p>""",

        "faq": [
            ("Can I migrate my Zaps to Make?", "There's no direct migration tool. You'll need to rebuild each Zap as a Make scenario. For simple Zaps (2-3 steps), this takes 10-15 minutes each. For complex multi-step Zaps, plan 30-60 minutes. Make has templates for common workflows that accelerate migration."),
            ("Is Zapier ever the better choice for GTM Engineers?", "Rarely. The main scenario: you need a niche integration that only Zapier supports and building a custom HTTP connection in Make isn't worth the effort. For everything else, Make is better for technical users."),
            ("Which is better for connecting to Clay?", "Both work. Clay has native integrations with both Make and Zapier. Make's integration is more flexible because Make handles complex data structures (nested JSON, arrays) better than Zapier. If your Clay workflow outputs complex data, Make processes it more cleanly."),
            ("Does Zapier's AI workflow builder replace the need for Make?", "No. Zapier's AI generates simple, linear workflows. It can't build the branching, looping, and error-handling logic that Make (or n8n) provides. The AI builder is a convenience for simple automations, not a replacement for visual workflow design."),
            ("Why are GTM Engineers moving away from Zapier?", "Three reasons: cost (Zapier is 3-5x more expensive at scale), capability (Zapier can't handle complex workflows), and control (no self-hosting, limited error handling). The trend toward n8n and Make reflects GTM Engineers' preference for tools that scale with their technical ambitions."),
        ],
    },
}
