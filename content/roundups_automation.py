"""Roundup content for GTM automation tool comparison."""

ROUNDUPS = {
    "zapier-vs-make-vs-n8n": {
        "intro": """<p>Every GTM engineer needs an automation backbone. Zapier is the default. Make is the visual alternative. n8n is the power tool. The right choice depends on how complex your workflows are and whether you want to self-host.</p>
<p>We've built production GTM workflows on all three. Zapier gets you started fastest. Make handles mid-complexity flows better than anything else. And n8n is where you go when you've outgrown the other two and want full control over your automation layer.</p>
<p>Here's what matters for GTM engineers specifically: AI agent nodes, webhook flexibility, error handling, and cost at scale. A simple Zap that fires on a form submission is fine. A 15-step enrichment waterfall with conditional branching and LLM calls is where the tools diverge hard.</p>""",

        "tools": [
            {
                "rank": 1,
                "name": "n8n",
                "slug": "n8n-review",
                "category_tag": "Self-Hosted / Cloud",
                "best_for": "GTM engineers who want maximum control and AI workflow capabilities",
                "why_picked": "The GTM engineer's choice. Self-hostable, code-optional, and the AI agent nodes are ahead of everyone else. You can run local LLMs, chain API calls with custom JavaScript, and deploy workflows that would cost $500/month on Zapier for under $20. The learning curve is real, but once you're in, the flexibility is unmatched.",
                "pricing": "Free (self-hosted) / $20+/mo (cloud)",
                "link_to_review": True,
            },
            {
                "rank": 2,
                "name": "Make",
                "slug": "make-review",
                "category_tag": "Visual Builder",
                "best_for": "Visual thinkers who want Zapier's ease with more power",
                "why_picked": "Cleaner than Zapier, cheaper than Zapier, more flexible than Zapier. The visual flow builder is noticeably better for complex multi-step GTM workflows. You can see your entire automation as a connected graph instead of a linear sequence. Error handling is more intuitive. And the pricing model charges per operation, not per task, which means complex workflows cost a fraction of what they'd run on Zapier.",
                "pricing": "$9+/mo (1,000 ops included)",
                "link_to_review": True,
            },
            {
                "rank": 3,
                "name": "Zapier",
                "slug": "zapier-review",
                "category_tag": "Simplicity",
                "best_for": "Teams that need a specific integration the others don't have",
                "why_picked": "The default. 6,000+ integrations. If you need to connect two SaaS tools and one of them only has a Zapier integration, your decision is made. But it's expensive at scale, limited on logic, and the execution model gets clunky for anything beyond simple triggers. Multi-step Zaps with filters and paths work, but they're harder to debug than Make's visual builder or n8n's node editor.",
                "pricing": "$19.99+/mo (750 tasks)",
                "link_to_review": True,
            },
        ],

        "verdict": """<h2>The Verdict</h2>
<p>n8n for GTM engineers who want maximum control and AI capabilities. Make for visual thinkers who want Zapier's ease with more power. Zapier only if you need a specific integration that the others don't have.</p>
<p>The cost difference is significant at scale. A GTM workflow that runs 10,000 operations per month costs roughly $9 on Make, $20 on n8n Cloud, and $69+ on Zapier. Over a year, that gap adds up to hundreds of dollars per workflow.</p>
<p>If you're just getting started with GTM automation, Make is the safest pick. It's visual, affordable, and powerful enough for 90% of use cases. When you hit the ceiling, n8n is waiting.</p>

<table style="width: 100%; border-collapse: collapse; margin: 1.5rem 0;">
<thead>
<tr style="border-bottom: 2px solid var(--gtme-accent);">
<th style="text-align: left; padding: 0.75rem;">Factor</th>
<th style="text-align: left; padding: 0.75rem;">n8n</th>
<th style="text-align: left; padding: 0.75rem;">Make</th>
<th style="text-align: left; padding: 0.75rem;">Zapier</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom: 1px solid rgba(255,79,31,0.15);">
<td style="padding: 0.75rem;">Pricing (10K ops/mo)</td>
<td style="padding: 0.75rem;">$20/mo</td>
<td style="padding: 0.75rem;">$9/mo</td>
<td style="padding: 0.75rem;">$69+/mo</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,79,31,0.15);">
<td style="padding: 0.75rem;">Self-hosting</td>
<td style="padding: 0.75rem;">Yes (Docker)</td>
<td style="padding: 0.75rem;">No</td>
<td style="padding: 0.75rem;">No</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,79,31,0.15);">
<td style="padding: 0.75rem;">AI/LLM nodes</td>
<td style="padding: 0.75rem;">Best in class</td>
<td style="padding: 0.75rem;">Good</td>
<td style="padding: 0.75rem;">Basic</td>
</tr>
<tr style="border-bottom: 1px solid rgba(255,79,31,0.15);">
<td style="padding: 0.75rem;">Integrations</td>
<td style="padding: 0.75rem;">400+</td>
<td style="padding: 0.75rem;">1,700+</td>
<td style="padding: 0.75rem;">6,000+</td>
</tr>
<tr>
<td style="padding: 0.75rem;">Learning curve</td>
<td style="padding: 0.75rem;">Steep</td>
<td style="padding: 0.75rem;">Moderate</td>
<td style="padding: 0.75rem;">Easy</td>
</tr>
</tbody>
</table>""",

        "faq": [
            ("Is n8n hard to learn?", "Harder than Zapier, comparable to Make. The node-based editor takes a few hours to get comfortable with. If you've used any visual automation tool before, you'll pick it up in a day. The self-hosting setup takes an additional hour with Docker. The AI agent nodes require understanding prompt engineering, but that's true regardless of platform."),
            ("Can Make replace Zapier completely?", "For 90% of GTM workflows, yes. Make has 1,700+ integrations and covers most popular SaaS tools. The 10% where Zapier wins is niche integrations. If you're connecting two obscure tools and only one has a Zapier connector, you're stuck. Check Make's integration directory before switching."),
            ("Which is cheapest for high-volume GTM automation?", "n8n self-hosted is free regardless of volume. For cloud options, Make is cheapest at $9/month for 10,000 operations. Zapier's equivalent plan starts at $69/month. At 50,000+ operations per month, the gap widens further. Make stays under $30/month while Zapier crosses $150."),
            ("Do any of these tools handle AI agent workflows?", "n8n is furthest ahead with dedicated AI agent nodes, vector store integrations, and support for local LLMs. Make has AI modules for OpenAI and Anthropic that work well for single-call tasks. Zapier's AI features are the most basic, focused on simple prompt-response patterns rather than multi-step agent workflows."),
        ],
    },
}
