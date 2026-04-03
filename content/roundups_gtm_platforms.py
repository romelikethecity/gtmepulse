"""Roundup content for best GTM automation platforms."""

ROUNDUPS = {
    "best-gtm-automation-platforms": {
        "intro": """<p>GTM automation is the infrastructure that connects your data, enrichment, sequencing, and CRM into a single pipeline. The tools range from no-code platforms to developer-first frameworks. The right choice depends on your technical depth and workflow complexity.</p>
<p>We've run production pipelines on all seven of these tools. Some are drag-and-drop. Others require you to write code. The pricing models vary wildly, from free self-hosted options to enterprise contracts that don't list a number on the website. What they share: each one can wire together the APIs, webhooks, and data flows that make outbound work at scale.</p>
<p>Here's how they stack up for GTM engineers who need to move fast, handle complexity, and keep costs predictable.</p>""",

        "tools": [
            {
                "rank": 1,
                "name": "Clay",
                "slug": "clay-review",
                "category_tag": "Best for Enrichment Workflows",
                "best_for": "GTM engineers who build multi-step enrichment and outbound pipelines with 75+ data providers",
                "why_picked": "Clay is a spreadsheet that runs workflows. You chain enrichment providers, AI columns, and outbound actions in a single table. Need to waterfall Apollo, Clearbit, and FullEnrich to find an email? That's three columns. Want to score the result with an LLM and push it to HubSpot? Two more. The credit-based pricing means you're paying per operation, not per seat, which keeps costs sane for solo operators and small teams. The downside: Clay is purpose-built for GTM. You won't use it to sync your project management tools or trigger Slack alerts from Stripe.",
                "pricing": "$149-$800/mo",
                "link_to_review": True,
            },
            {
                "rank": 2,
                "name": "n8n",
                "slug": "n8n-review",
                "category_tag": "Best for Custom Automation",
                "best_for": "Engineers who want full control over their automation stack, including self-hosting and custom code nodes",
                "why_picked": "n8n gives you what Zapier won't: the ability to self-host, write custom JavaScript in any node, and build AI agent workflows without hitting arbitrary platform limits. The node editor handles branching, loops, error handling, and sub-workflows. You can run it on a $5/mo VPS and process millions of operations for free. The AI agent nodes are ahead of every competitor. The trade-off is setup time. You'll spend a few hours configuring Docker and learning the interface before you build your first flow. Worth it if you plan to run dozens of automations long-term.",
                "pricing": "$20+/mo or self-hosted (free)",
                "link_to_review": True,
            },
            {
                "rank": 3,
                "name": "Make",
                "slug": "make-review",
                "category_tag": "Best Visual Builder",
                "best_for": "Non-engineers and ops people who want more power than Zapier without writing code",
                "why_picked": "Make's visual canvas is the best in the category. You see your entire workflow as a connected graph, not a linear list of steps. Branching, filtering, and error handling are intuitive. The pricing charges per operation (not per task like Zapier), so complex multi-step flows cost a fraction of what they'd run elsewhere. 1,700+ integrations cover most SaaS tools. The weak spot: no self-hosting option, and AI/LLM capabilities lag behind n8n. For GTM teams that want visual clarity without code, Make is the sweet spot.",
                "pricing": "$9+/mo",
                "link_to_review": True,
            },
            {
                "rank": 4,
                "name": "Zapier",
                "slug": "zapier-review",
                "category_tag": "Best for Simple Integrations",
                "best_for": "Teams that need a specific niche integration and want the fastest setup possible",
                "why_picked": "6,000+ integrations. That's Zapier's moat. If you need to connect two SaaS tools and one of them only has a Zapier connector, your decision is made. Setup takes minutes, not hours. The problem starts when your workflows get complex. Multi-step Zaps with filters and paths work, but they're clunky to debug compared to Make's visual builder. And the pricing punishes volume. A workflow that costs $9/mo on Make runs $69+ on Zapier at the same operation count. Use Zapier for simple triggers. Move to Make or n8n when you outgrow it.",
                "pricing": "$19.99+/mo",
                "link_to_review": True,
            },
            {
                "rank": 5,
                "name": "Apollo.io",
                "slug": "apollo-review",
                "category_tag": "Best All-in-One",
                "best_for": "Teams that want data, enrichment, sequencing, and basic automation in a single platform",
                "why_picked": "Apollo is less an automation platform and more an all-in-one GTM stack. You get a 275M+ contact database, email sequences, a dialer, and workflow rules that trigger actions based on prospect behavior. The automation layer is simpler than Make or n8n. You can't build custom multi-step workflows with branching logic. But for teams that don't want to stitch together five different tools, Apollo covers prospecting through outreach in one login. The free tier with 10,000 email credits monthly makes it the cheapest way to get started.",
                "pricing": "Free-$99/user/mo",
                "link_to_review": True,
            },
            {
                "rank": 6,
                "name": "Tray.io",
                "slug": None,
                "category_tag": "Best Enterprise iPaaS",
                "best_for": "Enterprise GTM teams that need SOC 2 compliance, SSO, and IT-approved integration infrastructure",
                "why_picked": "Tray.io is what happens when an automation platform grows up and gets an enterprise sales team. You get visual workflow building (similar to Make), a massive connector library, and the compliance checkboxes that IT departments require. The platform handles complex data transformations, API orchestration, and multi-system syncs better than most competitors. The catch: pricing is opaque and expensive. You won't find a number on their website. Expect five-figure annual contracts. If your company already evaluates iPaaS vendors through procurement, Tray belongs on the shortlist. If you're a startup founder building automations at midnight, look elsewhere.",
                "pricing": "Custom pricing",
                "link_to_review": False,
            },
            {
                "rank": 7,
                "name": "Pipedream",
                "slug": None,
                "category_tag": "Best for Developers",
                "best_for": "Developers who want to build event-driven workflows with real code, not visual drag-and-drop",
                "why_picked": "Pipedream is the automation platform that doesn't pretend code is scary. You write Node.js or Python directly in the workflow editor. Every trigger, action, and transformation is code-first with a visual wrapper on top. The free tier is generous: 10,000 invocations per day. Pre-built connectors handle auth and API boilerplate so you're writing business logic, not OAuth flows. For developers who find Make and Zapier limiting, Pipedream removes the ceiling. The community is smaller, documentation is thinner, and you won't find a Pipedream consultant on Upwork. You're trading polish for power.",
                "pricing": "Free-$19+/mo",
                "link_to_review": False,
            },
        ],

        "verdict": """<h2>The Verdict</h2>
<p>Clay for enrichment-heavy workflows. n8n for engineers who want full control. Make for visual thinkers. Apollo if you want data + automation in one.</p>
<p>The honest answer is that most GTM teams end up using two or three of these together. Clay handles enrichment. Make or n8n handles the orchestration between systems. Apollo provides the data and sequencing layer. That's how the stack works when you're serious about automation.</p>
<p>If you're just starting out: pick Make. It's the easiest to learn, cheapest to scale, and powerful enough for 80% of GTM workflows. When you hit a wall, n8n is waiting. When you need enrichment depth, Clay is the answer.</p>

<table style="width: 100%; border-collapse: collapse; margin: 1.5rem 0;">
<thead>
<tr style="border-bottom: 2px solid var(--gtme-accent);">
<th style="text-align: left; padding: 0.75rem;">Tool</th>
<th style="text-align: left; padding: 0.75rem;">Best For</th>
<th style="text-align: left; padding: 0.75rem;">Starting Price</th>
<th style="text-align: left; padding: 0.75rem;">Self-Host?</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom: 1px solid rgba(255,79,31,0.15);">
<td style="padding: 0.75rem;">Clay</td>
<td style="padding: 0.75rem;">Enrichment workflows</td>
<td style="padding: 0.75rem;">$149/mo</td>
<td style="padding: 0.75rem;">No</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,79,31,0.15);">
<td style="padding: 0.75rem;">n8n</td>
<td style="padding: 0.75rem;">Custom automation</td>
<td style="padding: 0.75rem;">Free (self-hosted)</td>
<td style="padding: 0.75rem;">Yes</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,79,31,0.15);">
<td style="padding: 0.75rem;">Make</td>
<td style="padding: 0.75rem;">Visual workflows</td>
<td style="padding: 0.75rem;">$9/mo</td>
<td style="padding: 0.75rem;">No</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,79,31,0.15);">
<td style="padding: 0.75rem;">Zapier</td>
<td style="padding: 0.75rem;">Simple integrations</td>
<td style="padding: 0.75rem;">$19.99/mo</td>
<td style="padding: 0.75rem;">No</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,79,31,0.15);">
<td style="padding: 0.75rem;">Apollo.io</td>
<td style="padding: 0.75rem;">All-in-one GTM</td>
<td style="padding: 0.75rem;">Free</td>
<td style="padding: 0.75rem;">No</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,79,31,0.15);">
<td style="padding: 0.75rem;">Tray.io</td>
<td style="padding: 0.75rem;">Enterprise iPaaS</td>
<td style="padding: 0.75rem;">Custom</td>
<td style="padding: 0.75rem;">No</td>
</tr>
<tr>
<td style="padding: 0.75rem;">Pipedream</td>
<td style="padding: 0.75rem;">Developer workflows</td>
<td style="padding: 0.75rem;">Free</td>
<td style="padding: 0.75rem;">No</td>
</tr>
</tbody>
</table>""",

        "faq": [
            ("What's the difference between Clay and a workflow automation tool like Make?", "Clay is purpose-built for GTM data enrichment. You build waterfalls across 75+ data providers in a spreadsheet interface. Make is a general automation platform that connects any SaaS tool to any other SaaS tool via visual workflows. Most GTM teams use both: Clay enriches the data, Make moves it between systems. They solve different problems."),
            ("Can I replace Zapier with n8n completely?", "For most GTM workflows, yes. n8n has 400+ integrations covering the major SaaS tools. Where Zapier wins is niche connectors. If you're connecting two obscure tools and only one has a Zapier integration, you're stuck. Check n8n's integration list before migrating. For anything involving AI, custom code, or high-volume operations, n8n is strictly better."),
            ("Is Tray.io worth the enterprise pricing?", "Only if your company requires SOC 2 compliance, SSO, and IT-approved vendors for integration infrastructure. Tray.io does the same things Make does but with enterprise governance layers on top. If nobody at your company is asking about compliance certifications, you don't need Tray. Make or n8n will cost 90% less and do the same work."),
            ("Which automation tool is best for a one-person GTM team?", "Make. It's visual enough to build fast, cheap enough to not worry about costs, and powerful enough to handle multi-step enrichment and outbound workflows. If you're technical and comfortable with Docker, n8n self-hosted gives you unlimited operations for free. Apollo's free tier is also a strong starting point if you want data + sequencing without separate tools."),
        ],
    },
}
