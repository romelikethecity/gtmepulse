# content/tools_intent.py
# Review prose for 2 intent data tools (6sense, Bombora).

TOOL_REVIEWS = {

"6sense": {
    "overview": """
<p>6sense is an enterprise intent data and ABM orchestration platform that identifies anonymous website visitors, tracks buying signals across the web, and predicts which accounts are in-market for your product. The platform combines first-party intent (your website traffic), third-party intent (content consumption across publisher networks), and predictive analytics to score accounts and prioritize outbound efforts.</p>
<p>For enterprise GTM teams, 6sense replaces the guesswork in account prioritization. Instead of working a static target account list, reps focus on accounts showing active buying signals. The platform's Revenue AI model assigns buying stage predictions (Awareness, Consideration, Decision, Purchase) based on behavioral patterns. Segments, alerts, and CRM integrations push these insights directly into sales workflows.</p>
<p>The product sits squarely in the enterprise tier. Implementation takes 2-4 months, pricing starts at $25K+/year, and getting value requires integration with your CRM, MAP, and sales engagement tools. For solo GTM Engineers or startups, 6sense is priced out of reach. For enterprise revenue teams with $100K+ tool budgets, it can be transformative when implemented well.</p>
""",
    "gtm_use_cases": """
<ul>
    <li><strong>Account identification from anonymous website traffic.</strong> 6sense de-anonymizes company-level website visits, showing which accounts are researching your product pages, pricing pages, and competitors. You won't see individual names, but knowing that Acme Corp visited your pricing page 4 times this week is actionable.</li>
    <li><strong>Predictive buying stage scoring.</strong> 6sense's AI model assigns accounts to buying stages (Awareness through Purchase) based on content consumption patterns, website behavior, and firmographic signals. Reps focus outbound on accounts in Decision/Purchase stages where conversion probability is highest.</li>
    <li><strong>ABM campaign orchestration.</strong> Build target account segments based on intent signals, push them to advertising platforms (LinkedIn, display), and coordinate outbound sequences through Outreach or Salesloft. The platform synchronizes air cover (ads) with ground game (outbound emails).</li>
    <li><strong>Competitive displacement campaigns.</strong> Track which accounts are researching competitor products. 6sense shows topic-level intent including competitor brand keywords. Use this to trigger competitive displacement playbooks when an account is evaluating alternatives.</li>
    <li><strong>CRM enrichment with intent signals.</strong> Push 6sense intent scores, buying stages, and engagement data directly into Salesforce or HubSpot records. Sales reps see intent context without leaving their CRM.</li>
</ul>
""",
    "pricing": """
<table class="data-table">
    <thead><tr><th>Plan</th><th>Price</th><th>Accounts</th><th>Key Features</th></tr></thead>
    <tbody>
        <tr><td>Essentials</td><td>~$25K/yr</td><td>Limited</td><td>Account identification, basic intent, CRM integration</td></tr>
        <tr><td>Advanced</td><td>~$50K-$75K/yr</td><td>Expanded</td><td>Predictive scoring, segments, advertising orchestration</td></tr>
        <tr><td>Premium</td><td>~$100K+/yr</td><td>Unlimited</td><td>Full AI, custom models, dedicated CSM, advanced reporting</td></tr>
    </tbody>
</table>
<p>6sense doesn't publish pricing. The figures above are based on market intelligence and customer reports. Every deal is custom-quoted based on company size, number of users, and desired features. Expect a multi-week sales cycle with demos, POC discussions, and contract negotiation.</p>
<p>The cost structure makes 6sense viable only for companies with $100K+ annual tool budgets and $1M+ in pipeline to justify the investment. A $25K/year Essentials contract needs to generate at least $250K in influenced pipeline to break even at a generous 10x ROI threshold. Most companies evaluate 6sense at the Advanced tier ($50K-$75K), which requires demonstrating even more pipeline impact.</p>
""",
    "criticism": """
<p>The pricing is opaque and prohibitive for most GTM Engineers. Starting at $25K/year, 6sense is an enterprise budget decision, not a practitioner purchase. Solo GTM Engineers, startup teams, and agencies running lean stacks can't justify the cost. 6sense knows this and targets VP-level buyers with ROI models, but the individual contributor who would use the data daily has no path to procurement.</p>
<p>Implementation takes months, not days. Integrating 6sense with your CRM, MAP, and sales tools requires dedicated resources. Pixel installation, data mapping, segment configuration, and sales enablement training add up to a 2-4 month implementation timeline. During that period, you're paying for a product you can't fully use. Compare this to Apollo's intent data (available on Organization plans) that starts working the day you activate it.</p>
<p>Intent data accuracy is a persistent debate. 6sense aggregates signals from publisher networks, but "Company X is researching CRM software" can mean an intern read a blog post, not that the CFO is signing a purchase order. The predictive models smooth out noise, but users report that 30-50% of "in-market" accounts never become real opportunities. The signal-to-noise ratio improves with more data and better configuration, but it's never as precise as direct engagement signals (website visits, demo requests).</p>
""",
    "verdict": """
<p>6sense is the most capable intent data platform on the market, and one that most GTM Engineers will never use. The pricing, implementation complexity, and enterprise-only focus put it out of reach for the majority of practitioners in our survey. If you're at a company that can afford it and has the resources to implement it properly, 6sense delivers insights that no cheaper tool matches.</p>
<p>For the other 90% of GTM Engineers: look at Apollo's intent data features (included on Organization plans at $149/user/month), Bombora's topic-level signals through your existing tools, or LinkedIn Sales Navigator's buyer intent indicators. These won't match 6sense's depth, but they're accessible at GTM Engineer budget levels.</p>
""",
    "faq": [
        ("Is 6sense worth it for startups?", "Almost never. At $25K+/year with a 2-4 month implementation timeline, 6sense requires both budget and patience that startups lack. Use Apollo's intent data, manual LinkedIn research, or Bombora through a partner integration until your company has $5M+ in annual revenue and a dedicated RevOps team to manage the platform."),
        ("How accurate is 6sense's intent data?", "It depends on the signal type. First-party intent (website visits) is highly accurate for company identification. Third-party intent (content consumption) is noisier. Users report that 30-50% of accounts flagged as 'in-market' by third-party signals never convert. The value comes from combining multiple signal types and filtering aggressively, not from trusting any single signal."),
        ("How does 6sense compare to Bombora?", "6sense is a full platform (intent + account identification + ABM orchestration + predictive AI). Bombora is primarily an intent data provider that integrates with your existing tools. 6sense costs 3-5x more but does more. Bombora's data can feed into tools you already own. Most GTM Engineers encounter Bombora's data through CRM or MAP integrations rather than buying it directly."),
        ("Can GTM Engineers use 6sense directly?", "In enterprise companies with 6sense deployed, GTM Engineers use the platform for account research, segment building, and triggering automated workflows. But they rarely control the 6sense budget or configuration. It's typically managed by RevOps or Marketing Ops, with GTM Engineers as power users who build workflows on top of the data."),
    ],
},

"bombora": {
    "overview": """
<p>Bombora is a B2B intent data provider that tracks topic-level content consumption across a cooperative network of 5,000+ publisher websites. When a company shows statistically significant interest in a topic (reading more articles about "CRM migration" than their baseline), Bombora flags it as a "Company Surge" signal. This data integrates with CRMs, marketing automation platforms, and sales engagement tools to help GTM teams prioritize accounts showing buying intent.</p>
<p>Unlike 6sense (which is a full platform), Bombora is primarily a data layer. You access Bombora's intent signals through integrations with your existing tools. HubSpot, Salesforce, Outreach, 6sense, and dozens of other platforms have Bombora integrations. Some tools (like ZoomInfo and TrustRadius) bundle Bombora data into their own intent features. This means many GTM Engineers use Bombora-sourced intent data without realizing where it comes from.</p>
<p>The product's value proposition is account prioritization. Instead of cold-calling a static list, your team focuses on companies actively researching topics related to your product. The data doesn't tell you who at the company is researching, only that the company as a whole is showing elevated interest in specific topics.</p>
""",
    "gtm_use_cases": """
<ul>
    <li><strong>Account prioritization based on topic surge signals.</strong> Filter your target account list by Bombora surge scores. Accounts surging on topics relevant to your product (e.g., "sales automation," "data enrichment," "CRM implementation") get outbound attention first.</li>
    <li><strong>Trigger-based outbound sequences.</strong> Configure your sales engagement tool to auto-enroll accounts into outbound sequences when their Bombora surge score crosses a threshold. This turns static lists into dynamic, signal-driven outreach.</li>
    <li><strong>Content personalization based on research topics.</strong> If Bombora shows a company is surging on "email deliverability," your outbound messaging to that account focuses on deliverability pain points. Topic-level data enables message-to-intent matching.</li>
    <li><strong>Competitive intelligence at the account level.</strong> Bombora's topic taxonomy includes competitor brand names. Track which accounts are researching your competitors to trigger displacement campaigns or competitive battle card distribution to reps.</li>
    <li><strong>Marketing campaign targeting.</strong> Build LinkedIn and display ad audiences from accounts showing intent. Coordinate ads (air cover) with outbound (ground game) for accounts in active research phases.</li>
</ul>
""",
    "pricing": """
<table class="data-table">
    <thead><tr><th>Access Method</th><th>Price</th><th>Data</th><th>Notes</th></tr></thead>
    <tbody>
        <tr><td>Through partner tools</td><td>Varies</td><td>Filtered surge data</td><td>ZoomInfo, HubSpot, Outreach include Bombora data on certain plans</td></tr>
        <tr><td>Direct (Bombora Surge)</td><td>~$15K-$30K/yr</td><td>Full topic taxonomy</td><td>Custom segments, API access, direct data feed</td></tr>
        <tr><td>Data Co-op membership</td><td>Free (exchange)</td><td>Reciprocal</td><td>Contribute your content engagement data to receive intent data back</td></tr>
    </tbody>
</table>
<p>Bombora's pricing is as opaque as 6sense's. Direct contracts start around $15K-$30K/year depending on the number of topics tracked, account volume, and integration requirements. Most GTM Engineers access Bombora data indirectly through tools that bundle it (ZoomInfo, HubSpot, TrustRadius), which means the cost is embedded in those tool subscriptions.</p>
<p>The co-op model is worth understanding. Bombora's data comes from publishers who share their audience's content consumption patterns in exchange for receiving intent data back. This creates the network effect that makes Bombora's data valuable, but it also means the data quality depends on which publishers participate and how they tag content.</p>
""",
    "criticism": """
<p>Topic-level intent is inherently noisy. A company "surging" on "CRM" could mean their IT team is reading about CRM security, their intern is writing a college paper, or their VP of Sales is evaluating a switch. Bombora can't distinguish between a blog reader and a buying committee member. The signal tells you a company is consuming more content on a topic than usual. It doesn't tell you why, who, or whether a purchase is imminent.</p>
<p>The topic taxonomy requires significant filtering to be actionable. Bombora tracks thousands of topics, and selecting the right ones for your use case requires experimentation. Too broad (e.g., "software") and every company surges. Too narrow (e.g., "Clay enrichment alternatives") and the signal volume drops to zero. Finding the right topic combination takes weeks of testing, and the optimal set changes as your market evolves.</p>
<p>Attribution is difficult. Bombora will tell you that 40 accounts were surging before they entered your pipeline, but proving that the surge data caused your team to prioritize those accounts (rather than discovering them through other channels) is nearly impossible. The ROI calculation relies on correlation, not causation, which makes budget justification harder than tools with direct attribution like form fills or demo requests.</p>
""",
    "verdict": """
<p>Bombora provides useful signals for account prioritization, but it's a supporting data layer, not a standalone solution. The intent data works best when layered on top of direct engagement signals (website visits, content downloads, demo requests) to add context about what accounts are researching beyond your owned properties.</p>
<p>Access Bombora through tools you already pay for (ZoomInfo, HubSpot, Outreach) before buying a direct contract. If your existing tools already include Bombora data, configure topic-based alerts and test whether the surge signals improve your outbound conversion rates. Only buy direct if you need the full topic taxonomy, custom segments, or API access for programmatic workflows.</p>
""",
    "faq": [
        ("What's the difference between Bombora and 6sense?", "Bombora is a data provider. You get topic-level intent signals and integrate them into your own tools. 6sense is a full platform that includes intent data, account identification, predictive scoring, and ABM orchestration. Bombora costs $15K-$30K/year for data. 6sense costs $25K-$100K+/year for the full platform. Many 6sense customers also use Bombora data within 6sense."),
        ("Is Bombora data accurate?", "At the company level, the surge signals are directionally useful. Bombora's data comes from 5,000+ publishers, which creates broad coverage. The accuracy question is about interpretation: 'surging on CRM' is a weak signal on its own. Combined with other signals (website visits, tech install data, hiring patterns), intent data becomes more actionable. Expect 20-30% of surging accounts to have genuine purchase intent."),
        ("Do I need to buy Bombora directly?", "Most GTM Engineers don't. If you use ZoomInfo, HubSpot (Enterprise), or Outreach, you likely have access to Bombora-powered intent data already. Check your existing tools before starting a direct Bombora sales conversation. Buy direct only if you need API access, the full topic taxonomy, or custom topic definitions."),
        ("How do GTM Engineers use Bombora day-to-day?", "The most common pattern: set up alerts for target accounts surging on 5-10 relevant topics, review surging accounts weekly, and prioritize outbound to the accounts showing the strongest signals. Some GTM Engineers build automated workflows in n8n or Make that pull Bombora data and auto-enroll surging accounts into outbound sequences."),
    ],
},

}
