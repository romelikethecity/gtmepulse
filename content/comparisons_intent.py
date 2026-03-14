"""Comparison content for Intent Data matchups."""

COMPARISONS = {
    "6sense-vs-bombora": {
        "intro": """<p>6sense and Bombora both sell intent data, but they package it differently. 6sense is a full ABM platform that includes intent signals, account identification, predictive analytics, and advertising orchestration. Bombora is a pure intent data provider that sells raw signals you pipe into your existing stack. The choice shapes your entire account-based strategy.</p>
<p>For GTM Engineers, intent data is the difference between spraying outbound at cold lists and targeting accounts that are actively researching your category. Both platforms promise to surface those accounts. The question is whether you need a full ABM platform (6sense) or a data feed you control (Bombora).</p>
<p>This comparison breaks down signal quality, integration flexibility, pricing realities, and which approach fits different GTM architectures. One costs 6 figures. The other starts at five figures. The ROI depends on how you use the data.</p>""",

        "feature_table": """<div class="table-responsive"><table class="data-table">
<thead>
<tr><th>Feature</th><th>6sense</th><th>Bombora</th></tr>
</thead>
<tbody>
<tr><td>Product Type</td><td>Full ABM platform</td><td>Intent data provider</td></tr>
<tr><td>Intent Signal Sources</td><td>Proprietary network + web tracking</td><td>Data Co-op (5,000+ B2B sites)</td></tr>
<tr><td>Account Identification</td><td>De-anonymize website visitors</td><td>Account-level research signals</td></tr>
<tr><td>Signal Granularity</td><td>Account + buying stage prediction</td><td>Topic-level surge scoring</td></tr>
<tr><td>CRM Integration</td><td>Native Salesforce + HubSpot</td><td>Via integrations (Salesforce, HubSpot, others)</td></tr>
<tr><td>Advertising</td><td>Built-in display + LinkedIn ad orchestration</td><td>None (data feed only)</td></tr>
<tr><td>Predictive Analytics</td><td>AI-driven buying stage model</td><td>Surge score (baseline vs current)</td></tr>
<tr><td>Data Freshness</td><td>Near real-time</td><td>Weekly updates</td></tr>
<tr><td>API Access</td><td>REST API (Enterprise plans)</td><td>REST API + data feeds</td></tr>
<tr><td>Pricing</td><td>$60,000-$150,000+/year</td><td>$20,000-$50,000+/year</td></tr>
<tr><td>Contract Terms</td><td>Annual (multi-year common)</td><td>Annual</td></tr>
<tr><td>GTM Engineer Fit</td><td>Platform users (less customizable)</td><td>Data engineers (full control)</td></tr>
</tbody>
</table></div>""",

        "tool_a_strengths": """<h2>Where 6sense Wins</h2>
<p>6sense's buying stage predictions are the most sophisticated in the market. Instead of just telling you "this account is researching CRM software," 6sense classifies accounts into stages: Awareness, Consideration, Decision, and Purchase. That classification drives prioritization. Your sales team can focus on accounts in the Decision stage rather than chasing early-stage researchers who won't buy for months.</p>
<p>Website de-anonymization reveals which companies visit your site before they fill out a form. 6sense matches anonymous traffic to company-level accounts using IP intelligence, cookie data, and device graphs. For inbound-heavy GTM motions, this data turns unknown website traffic into actionable account lists.</p>
<p>The built-in advertising platform lets you orchestrate display and LinkedIn ads to accounts showing intent. You create audiences based on intent signals, buying stage, and ICP fit, then run targeted campaigns without exporting data to a separate ad platform. The closed-loop reporting shows which ads influenced pipeline. Bombora's data can power ads, but you need to build the workflow yourself through your ad platforms.</p>
<p>For marketing-led GTM teams that want a single platform for intent detection, account prioritization, ad orchestration, and pipeline attribution, 6sense is the integrated solution. Everything lives in one system with shared reporting.</p>""",

        "tool_b_strengths": """<h2>Where Bombora Wins</h2>
<p>Bombora's Company Surge data is the industry standard for intent signals. The Data Co-op spans 5,000+ B2B media sites, tracking content consumption patterns across millions of accounts. When an account researches 3x more content about "sales automation" than their historical baseline, Bombora flags a surge. This methodology is well-understood, transparent, and has been validated across thousands of customers since 2014.</p>
<p>Flexibility is Bombora's core advantage for GTM Engineers. Bombora sells raw intent data. You decide how to use it. Pipe it into Clay for enrichment workflows. Push it to your CRM for lead scoring. Feed it to your SDR team's prospecting lists. Build custom models that combine Bombora signals with your own data. 6sense locks you into their platform's workflow. Bombora gives you the data and gets out of the way.</p>
<p>Pricing makes Bombora accessible to mid-market companies. Starting around $20,000-$25,000/year, Bombora costs 60-70% less than a comparable 6sense deployment. For companies that want intent data without a $100K+ platform commitment, Bombora is the pragmatic choice.</p>
<p>Bombora's data is available through dozens of partner integrations. Tools like Clay, ZoomInfo, Outreach, Salesforce, and HubSpot all offer native Bombora integrations. You don't need to rip out your existing stack to use Bombora's signals. 6sense typically requires a more significant implementation that touches multiple systems.</p>""",

        "pricing_comparison": """<h2>Pricing Breakdown</h2>
<p>6sense pricing starts around $60,000/year for the base platform with limited seats and features. Most deployments land between $80,000-$150,000/year when you add advertising credits, additional users, and API access. Enterprise contracts regularly pass $200,000/year. Multi-year commitments are common and come with modest discounts. Implementation costs add another $15,000-$50,000 depending on CRM complexity and team training needs.</p>
<p>Bombora pricing starts around $20,000-$25,000/year for Company Surge data. Pricing scales with the number of topics you track and accounts you monitor. A typical mid-market deal runs $25,000-$40,000/year. Enterprise packages with deeper analytics and custom topic taxonomies can reach $50,000-$75,000/year. Implementation is faster because you're integrating a data feed, not deploying a platform.</p>
<p>The ROI question: 6sense costs 3-5x more than Bombora. To justify that premium, you need to use the full platform: advertising orchestration, buying stage predictions, website de-anonymization, and pipeline attribution. If you only want intent signals to prioritize outbound prospecting, you're paying for capabilities you won't use. Bombora gives you the signal data for a fraction of the price and lets you decide how to act on it.</p>""",

        "verdict": """<h2>The Verdict</h2>
<p>Use 6sense if your company runs a marketing-led ABM motion with $100K+ in platform budget. The buying stage predictions, ad orchestration, and website visitor identification create a closed-loop system that's hard to replicate with point solutions. You need a dedicated admin, a 3-6 month implementation timeline, and executive buy-in for the investment. In return, you get the most complete intent-to-pipeline platform available.</p>
<p>Use Bombora if you want high-quality intent signals without the platform commitment. Bombora's Company Surge data integrates into whatever tools you already use. GTM Engineers who build their own enrichment and scoring workflows in Clay or n8n get more value from Bombora's raw data than from 6sense's prescribed workflows. You keep full control at 60-70% lower cost.</p>
<p>For most GTM Engineering teams, Bombora is the better investment. Intent data is most valuable when combined with your own scoring logic, enrichment waterfalls, and outbound workflows. Bombora gives you the input signal. You build the intelligence layer. 6sense makes sense at enterprise scale where the platform ROI justifies six-figure annual spend.</p>""",

        "faq": [
            ("How accurate is intent data from either platform?", "Both platforms detect account-level interest, not individual buying intent. Accuracy varies by topic and industry. Expect 60-70% of flagged accounts to confirm interest when contacted. False positives are higher for broad topics ('cloud computing') than narrow ones ('cold email deliverability'). Neither platform guarantees that a surging account will buy from you."),
            ("Can I use Bombora data inside 6sense?", "6sense has its own proprietary intent network. They don't integrate Bombora's data natively. However, you can run both platforms and compare signal overlap. Some teams use 6sense as the primary platform and Bombora data in their CRM for a second signal source."),
            ("Is intent data worth the investment for small teams?", "Bombora at $20K-$25K/year can be worth it if your ACV is $25K+ and you convert even 2-3 additional deals from intent-prioritized outreach. 6sense at $60K+ is harder to justify for small teams. Start with free intent signals from G2 Buyer Intent or LinkedIn's account interest data before committing budget."),
            ("How do intent signals fit into a GTM Engineer's workflow?", "The highest-value pattern: Bombora surge data feeds into your Clay enrichment workflow. Surging accounts get enriched with contact data, scored against your ICP, and pushed to outbound sequences automatically. The intent signal triggers the workflow. Everything downstream is automated."),
            ("Which integrates better with Clay?", "Bombora's data is available as an enrichment source in Clay, making it straightforward to include intent signals in your enrichment waterfalls. 6sense has an API, but most GTM Engineers use Bombora with Clay because it's a data feed rather than a platform."),
        ],
    },
}
