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

"hightouch": {
    "overview": """
<p>Hightouch is the reverse ETL platform that won GTM Engineer mindshare in 2024-2025. The product takes data from your warehouse (Snowflake, BigQuery, Redshift, Databricks) and syncs it to operational tools where sales and marketing teams work: HubSpot, Salesforce, Outreach, LinkedIn Ads, Segment, Iterable, and 180+ other destinations. The pitch lands cleanly with technical GTM teams who already have a warehouse and want to activate that data without writing brittle API integrations from scratch.</p>
<p>The platform's defining feature is the SQL-first model. You write a SELECT query against your warehouse. Hightouch maps the result columns to fields in your destination tool. You configure the sync frequency (real-time CDC, hourly, daily). Hightouch handles the rest: API authentication, batching, upsert logic, error handling, retry queues, and audit logs. For GTM Engineers who can write SQL but don't want to maintain custom API code, this changes the economics of activating warehouse data.</p>
<p>Hightouch has expanded beyond reverse ETL into adjacent categories: audience segmentation with Customer Studio, AI-powered personalization, identity resolution, and event-stream forwarding. The strategic pitch is that Hightouch becomes the activation layer on top of your warehouse, replacing the operational CDP entirely. For GTM Engineers, this means more product surface area to learn but also fewer disconnected tools to stitch together.</p>
""",
    "gtm_use_cases": """
<ul>
    <li><strong>Sync warehouse lead scores into CRM and outbound tools.</strong> Your data team builds a scoring model in dbt that combines product usage, firmographics, and intent data. Hightouch syncs the score to HubSpot or Salesforce hourly. The score becomes a routing input, a sequence-enrollment trigger, and a sales prioritization signal without any custom integration code.</li>
    <li><strong>Activate product-qualified leads in seconds, not days.</strong> A free user crosses a usage threshold in your product. The event lands in the warehouse via Segment. A Hightouch model running every five minutes detects the new PQL and pushes it to Outreach as a sequence enrollment. End-to-end latency drops from "next morning batch" to under 10 minutes.</li>
    <li><strong>Build audiences in SQL and push to ad platforms.</strong> Marketing wants to retarget customers who churned in the last 90 days but excluded enterprise accounts in active renewal cycles. Write the SQL, sync to LinkedIn Ads and Google Ads as a Custom Audience. The audience refreshes daily as the underlying data changes.</li>
    <li><strong>Reverse the flow for revenue ops dashboards.</strong> Pull computed metrics (account health scores, ICP grades, deal velocity by segment) out of the warehouse and into Salesforce or Attio as custom fields. Sales reps see one number on the account record that summarizes 40+ underlying signals.</li>
    <li><strong>Replace half-built API integrations.</strong> Most GTM Engineering stacks have 3-8 internal Python scripts pushing data between systems. Each script has its own auth handling, error logging, and maintenance debt. Hightouch consolidates these into a single platform with one auth flow, one observability stack, and one place to debug failed syncs.</li>
    <li><strong>Coordinate identity across tools.</strong> Use Hightouch Match to build identity graphs in your warehouse, then sync resolved profiles to every destination tool so you stop seeing the same person as five different leads in five different systems.</li>
</ul>
""",
    "pricing": """
<table class="data-table">
    <thead><tr><th>Plan</th><th>Price</th><th>Models/Syncs</th><th>Key Features</th></tr></thead>
    <tbody>
        <tr><td>Developer (Free)</td><td>$0</td><td>3 syncs, 1 source</td><td>200+ destinations, basic monitoring</td></tr>
        <tr><td>Starter</td><td>$450/mo</td><td>10 syncs, 2 sources</td><td>Reverse ETL, CDC, audience features</td></tr>
        <tr><td>Pro</td><td>$800/mo+</td><td>Unlimited models</td><td>Audience Studio, AI Decisioning, Match</td></tr>
        <tr><td>Business</td><td>Custom</td><td>Custom</td><td>SSO, audit logs, enterprise support</td></tr>
    </tbody>
</table>
<p>Hightouch pricing is volume-based with a destination count component. The free tier covers small GTM teams testing the product or running one or two syncs. The paid tiers add destinations, scheduled syncs, real-time CDC, and the audience features. Most GTM Engineering teams in mid-market companies end up on Pro or custom Business pricing in the $1K-$5K/month range depending on data volume and destination count.</p>
<p>The hidden cost most teams underestimate is warehouse compute. Hightouch runs queries against your warehouse on every sync. A model that runs every five minutes against a Snowflake source can rack up real compute spend if the underlying query is expensive. Monitor warehouse credits alongside Hightouch costs. Optimize expensive models with materialized views or pre-aggregated tables before scaling sync frequency.</p>
""",
    "criticism": """
<p>Pricing transparency stops at the Starter tier. Once you need Pro features (Audience Studio, AI Decisioning, Match), pricing moves to "talk to sales" territory. The list price you see on the website rarely reflects what mid-market customers pay in practice, and the discount math during procurement adds friction to evaluation. Census handles pricing more openly.</p>
<p>The sync configuration UI can hide complexity that bites later. Setting up a sync looks simple: pick a source, write SQL, map columns, choose a destination, hit save. Edge cases (custom field mapping in HubSpot, association rules in Salesforce, audience matching in LinkedIn Ads) require digging into destination-specific documentation that varies in quality. Plan for 2-3 days of fiddling on each new destination type before the sync is production-ready.</p>
<p>Real-time CDC has limits worth understanding. Hightouch supports change data capture for Snowflake and Postgres sources, which sounds like "instant updates." In practice, "real-time" lands closer to 30 seconds to 5 minutes of latency depending on warehouse and destination. For most GTM use cases this is fine. For workflows where 30-second latency hurts (live ad bidding, real-time fraud detection), Hightouch is not the right tool.</p>
<p>Audience Studio is useful but it's a second product to learn. Marketing teams using it well treat it as a self-service segmentation tool. Teams using it badly treat it as a CRM segmentation feature and get frustrated when business users can't write the SQL underneath. Without clear ownership between the data team and marketing, Audience Studio becomes a place where audiences proliferate, conflict, and stop being trustworthy.</p>
""",
    "verdict": """
<p>Hightouch is the right reverse ETL choice for GTM Engineers at companies with a working data warehouse and 5+ destination tools to integrate. The product saves enough engineering time on API integration work that the Pro plan typically pays for itself within the first quarter through replaced custom integrations and faster activation of warehouse-derived signals.</p>
<p>Choose Hightouch over Census if you value a slightly more polished UI, the additional Audience Studio and AI Decisioning features, and a roadmap that's pushing into operational CDP territory. Choose Census if pricing transparency and a more focused reverse ETL feature set matter more to your team. Most GTM Engineering teams could be successful on either; the gap is narrower than vendor marketing suggests.</p>
<p>Skip both if you don't have a warehouse yet. Reverse ETL needs something to reverse out of. Companies running their analytics in spreadsheets or directly against operational databases should fix the warehouse foundation first, then evaluate Hightouch a quarter later. Buying Hightouch without a warehouse produces a system that ingests data faster than your team can clean it.</p>
""",
    "faq": [
        ("How is Hightouch different from Segment or a CDP?", "Segment captures user events and pipes them to destination tools. Hightouch pulls modeled data out of your warehouse and pushes it to destinations. The two tools complement each other rather than competing directly. A common stack uses Segment for event capture, the warehouse for modeling, and Hightouch for activating the modeled data. Hightouch has added event-stream features that overlap with Segment, but most teams still use both."),
        ("Is Hightouch overkill for a 10-person startup?", "Usually yes. The free tier supports small use cases, but the value of Hightouch comes from having 5+ destination tools that need synchronized data. Startups with HubSpot as their primary operational tool can often get by with HubSpot's native warehouse sync or a simpler reverse ETL tool. Reach for Hightouch when you have a real warehouse, multiple operational tools, and a GTM Engineer with the time to build sync infrastructure."),
        ("How long does Hightouch implementation take?", "First sync: 1-3 days. First production-grade sync with proper monitoring, error handling, and field mapping: 1-2 weeks. Full integration across 5+ destinations with the audience features in active use: 6-12 weeks. The implementation timeline scales with the number of destinations and the complexity of your warehouse models, not with vendor onboarding speed."),
        ("Hightouch vs Census, which one wins for GTM Engineers?", "It depends on what you optimize for. Hightouch wins on UI polish, audience features, and breadth of operational CDP capabilities. Census wins on pricing transparency, a more focused product, and slightly faster sync execution for high-frequency use cases. For most GTM Engineers the practical difference is minor. Evaluate both with your actual data, your actual destinations, and a real production use case before committing to a multi-year contract."),
    ],
},

"census": {
    "overview": """
<p>Census is the reverse ETL platform that GTM Engineers reach for when they want a focused product with transparent pricing and clean integration patterns. The architecture mirrors Hightouch: warehouse as source, operational tools as destinations, SQL or dbt models defining what data moves where. Where Hightouch has expanded into operational CDP territory, Census has stayed closer to the core reverse ETL mission, which some technical teams prefer.</p>
<p>The product launched in 2018 and grew through the dbt community. Many of Census's early customers were data teams using dbt heavily for transformation work, and the dbt-native integration patterns remain a strong point. If your warehouse is already organized around dbt models with clear documentation, exposing those models to Census takes minutes. The mental model maps directly: a dbt model becomes a Census source, and you sync it to wherever it needs to go.</p>
<p>Census supports 200+ destinations including all the GTM-relevant tools: Salesforce, HubSpot, Marketo, Outreach, Salesloft, LinkedIn Ads, Google Ads, Iterable, Customer.io, Intercom, Zendesk, and Slack. The destination quality stays consistently high, with deep field mapping support and careful upsert behavior. Census has invested heavily in destination connector reliability, which shows up in lower sync error rates than competitor benchmarks suggest.</p>
""",
    "gtm_use_cases": """
<ul>
    <li><strong>Sync dbt-modeled lead scores into Salesforce or HubSpot.</strong> Your dbt models compute lead scores by combining product usage, firmographics, and engagement signals. Census wraps the dbt model as a source, syncs the result to your CRM, and the score becomes available as a sales workflow input within minutes of model refresh.</li>
    <li><strong>Activate customer health scores in operational tools.</strong> Build a health score in the warehouse from product usage, support ticket volume, NPS responses, and billing data. Sync to Salesforce as a custom field and to Slack as alerting for accounts trending toward churn. Customer success teams act on the same data engineering builds.</li>
    <li><strong>Build audiences for ad platforms with SQL precision.</strong> Marketing wants to suppress retargeting ads for customers who already converted but include trial users who churned in the last 30 days and matched ICP. The SQL takes 10 lines. Census syncs the audience to LinkedIn Ads and Google Ads. The audience refreshes daily.</li>
    <li><strong>Replace ad-hoc Python scripts with auditable syncs.</strong> Every GTM team has Python scripts pushing data between tools that someone wrote three years ago and nobody fully understands. Census replaces these with versioned, monitored syncs that the team can debug from a single dashboard.</li>
    <li><strong>Coordinate identity stitching across destinations.</strong> Use Census Match (the equivalent to Hightouch Match) to build identity graphs in the warehouse, then push resolved identities to every destination so contact records stay consistent across HubSpot, Salesforce, and the marketing automation platform.</li>
    <li><strong>Trigger workflows based on warehouse events.</strong> Census Live Syncs can fire syncs when warehouse data changes, enabling sub-minute activation of high-value signals like a target account hitting a specific usage threshold or a contract renewal moving into the danger zone.</li>
</ul>
""",
    "pricing": """
<table class="data-table">
    <thead><tr><th>Plan</th><th>Price</th><th>Destinations</th><th>Key Features</th></tr></thead>
    <tbody>
        <tr><td>Free</td><td>$0</td><td>10 destinations</td><td>100 rows/sync, limited sync frequency</td></tr>
        <tr><td>Starter</td><td>$300/mo</td><td>3 destinations</td><td>Unlimited rows, daily sync minimum</td></tr>
        <tr><td>Platform</td><td>$800/mo</td><td>10 destinations</td><td>Hourly syncs, audience hub, RBAC</td></tr>
        <tr><td>Enterprise</td><td>Custom</td><td>Custom</td><td>SSO, advanced security, dedicated support</td></tr>
    </tbody>
</table>
<p>Census pricing is more transparent than Hightouch's, with clear destination counts and sync frequency tiers published on the pricing page. Most mid-market GTM Engineering teams land on the Platform plan around $800-$2,000/month depending on destination count and data volume. The pricing model favors teams that need many destinations over teams running heavy volume to a few destinations, which fits the typical GTM use case well.</p>
<p>Warehouse compute is again the hidden cost. Census runs SQL queries against your source on every sync. A model that runs hourly against Snowflake can produce real compute bills if the query is poorly optimized. Monitor warehouse spend alongside Census costs. Cache expensive aggregations in dbt models before exposing them as Census sources.</p>
""",
    "criticism": """
<p>The UI feels less polished than Hightouch's. Census prioritizes function over form, which technical operators appreciate and business users find harder to use. If your audience for the product is data engineers and GTM Engineers, this is fine. If you expect marketing managers to self-serve audience creation, you'll get more friction from Census than from Hightouch's audience tools.</p>
<p>Documentation depth varies by destination. The popular destinations (Salesforce, HubSpot, Outreach) have extensive docs with field mapping examples and gotcha lists. Less popular destinations (some marketing automation tools, niche ad platforms) have thinner documentation that requires reading the destination's own API docs alongside Census's. Plan for extra ramp time on uncommon destinations.</p>
<p>The audience features lag Hightouch's Audience Studio in maturity. Census has audience capabilities and they work for SQL-fluent users, but the business-user-friendly audience builder is less developed than Hightouch's. Teams that need marketing self-service on audience creation will be happier on Hightouch. Teams where audience creation is a data engineering or GTM Engineering task are fine on either.</p>
<p>Real-time sync is supported but premium-tier. The most responsive sync patterns require the Platform or Enterprise plans. Free and Starter users get daily syncs at most, which limits the use cases for low-budget testing. Hightouch's free tier offers slightly faster sync frequencies, which can affect early evaluation.</p>
""",
    "verdict": """
<p>Census is the right reverse ETL choice for GTM Engineers at companies where data engineering and GTM Engineering work closely together, where dbt is already the transformation layer, and where pricing transparency matters. The product is excellent at the core reverse ETL job and slightly less ambitious about expanding into operational CDP territory than Hightouch.</p>
<p>Choose Census if your warehouse runs on dbt and your team values focused tooling. Choose Hightouch if you want broader operational CDP capabilities, more polished business-user features, and you accept the pricing opacity. The functional gap between the two products is narrow enough that team preferences and existing relationships often determine the choice as much as feature differences.</p>
<p>Both products are correct answers for "we have a warehouse and need to activate it." The wrong answer is buying neither and continuing to maintain custom Python scripts for every integration. The cost-benefit math on reverse ETL platforms hits a clear win once you have 3+ destinations and any meaningful warehouse model complexity.</p>
""",
    "faq": [
        ("Does Census require dbt?", "No, but it works best with dbt. Census can pull from any SQL source: raw warehouse tables, views, materialized views, or dbt models. Teams that use dbt get a tighter integration with model documentation, lineage, and test results showing in the Census UI. Teams that don't use dbt still get full Census functionality, just with less context about source data quality."),
        ("How does Census handle schema changes?", "Census detects schema changes in source queries and surfaces them in the sync configuration. Adding a column to a source model adds it as an available field to map. Removing a column breaks the sync until you remove the mapping. Renaming a column requires updating the mapping manually. The behavior is predictable but not automatic, which is the right trade-off for production syncs where silent column changes could push wrong data downstream."),
        ("Is Census faster than Hightouch for high-frequency syncs?", "For most use cases, the two tools have similar sync performance. Census has historically had a slight edge on the lowest-latency syncs because the architecture is more focused. Hightouch has closed the gap with their CDC features. For sub-minute sync requirements, both products work but neither matches the latency of a custom event-streaming pipeline built on Kafka or similar."),
        ("Can Census handle SOC 2 and enterprise security needs?", "Yes. Census has SOC 2 Type II, HIPAA-eligible deployments on Enterprise tier, and supports SSO, RBAC, and customer-managed encryption keys. For regulated industries (healthcare, financial services), the Enterprise plan includes the controls most procurement teams require. Implementation timelines for regulated deployments are longer because of the additional security review, typically 6-10 weeks from contract to first production sync."),
    ],
},

"common-room": {
    "overview": """
<p>Common Room is the community-intelligence and signal platform that GTM Engineers reach for when their product has a developer audience, an open-source component, or significant community-driven adoption. The product captures signals from places traditional sales tools don't look: GitHub stars and contributions, Discord and Slack community activity, Reddit and Hacker News mentions, Stack Overflow questions, and Twitter conversations. It maps those signals to companies and contacts so the people engaging with your product publicly become identifiable revenue opportunities.</p>
<p>The product won early traction with developer-tool companies (PostHog, Grafana, Hex, Cal.com) where community engagement reliably precedes commercial adoption. A developer who stars your GitHub repo, joins your Discord, and asks questions in your community Slack is showing buying intent in a form that LinkedIn Sales Navigator and 6sense don't capture. Common Room makes that engagement legible to your GTM team.</p>
<p>Beyond the community angle, Common Room has expanded into broader signal aggregation: website visitor identification (similar to RB2B), job change tracking, technographic shifts, and CRM activity. The platform sits as a signal layer that pushes context into existing operational tools (CRM, outbound sequencer, Slack) rather than trying to replace them. For GTM Engineers, it's the place where community signals become actionable revenue signals.</p>
""",
    "gtm_use_cases": """
<ul>
    <li><strong>Identify when developers at target accounts engage publicly with your product.</strong> A developer at a Fortune 500 company stars your GitHub repo, asks a question in your Discord, and contributes a small PR. Common Room maps that activity to the company, identifies the developer's role, and surfaces a sales-relevant signal that wouldn't appear in any other tool.</li>
    <li><strong>Trigger sales outreach on community-engagement thresholds.</strong> A target account has 5+ employees active in your Discord, 3 GitHub repository interactions, and 2 documentation page visits in the last 30 days. Push that account to your sales engagement tool with the engagement context attached. Outreach starts informed instead of cold.</li>
    <li><strong>Track competitive context in the wild.</strong> A developer in your community mentions evaluating a competitor in a public Reddit thread. Common Room flags the conversation and the company involved. Your team responds with positioning context before the comparison decision is made.</li>
    <li><strong>Identify product-qualified accounts from open-source usage.</strong> Open-source telemetry data combined with public GitHub activity reveals which companies are running your project in production at scale. Common Room maps this to account records so sales can prioritize companies showing real production adoption.</li>
    <li><strong>Coordinate community engagement with sales outreach.</strong> Developer Relations engages a community member in Discord while sales runs a contract evaluation with the same company. Common Room shows both teams the full context so DevRel doesn't accidentally undercut sales messaging and sales doesn't ignore DevRel relationships during contract negotiations.</li>
    <li><strong>Score accounts on community + traditional signals combined.</strong> Build composite scoring that weighs Discord engagement alongside CRM activity, intent data, and website visits. The composite score routes attention to accounts where the buying signals are converging across multiple channels.</li>
</ul>
""",
    "pricing": """
<table class="data-table">
    <thead><tr><th>Plan</th><th>Price</th><th>Members/Sources</th><th>Key Features</th></tr></thead>
    <tbody>
        <tr><td>Free</td><td>$0</td><td>2 sources, 1 user</td><td>Basic community tracking, manual exports</td></tr>
        <tr><td>Team</td><td>$625/mo+</td><td>Custom</td><td>Up to 25K members, integrations, segmentation</td></tr>
        <tr><td>Enterprise</td><td>Custom</td><td>Custom</td><td>SSO, dedicated CSM, custom integrations</td></tr>
    </tbody>
</table>
<p>Common Room pricing has been notoriously opaque, with Team-tier pricing typically landing $600-$2,500/month depending on member count and integrations. Enterprise deals for product-led companies with large communities run $30K-$80K/year. The free tier exists but is limited enough that real evaluation requires a sales conversation. This pricing model fits the high-touch enterprise sales motion but creates evaluation friction for GTM Engineers used to self-service pricing on tools like Koala or RB2B.</p>
<p>Value calculation should center on signal-to-pipeline conversion. If 10% of community-engaged accounts you previously couldn't see become sales opportunities, the platform pays for itself at modest deal sizes. If your community is small or your buyers aren't developers, the math gets worse and a cheaper signal stack covers the actionable surface area.</p>
""",
    "criticism": """
<p>The product works best for developer audiences. If your buyers are non-technical (marketing teams, finance leaders, operations managers) and your community engagement happens on platforms Common Room doesn't track deeply, you'll see less differentiated value than the marketing suggests. Evaluate with your actual community channels before committing.</p>
<p>Pricing opacity slows evaluation. Getting a real number requires a sales conversation, a discovery call, and frequently a custom quote. For solo GTM Engineers or startup teams accustomed to swiping a card and starting, this friction can push evaluation onto cheaper signal tools first. Common Room would convert more technical buyers earlier with self-service pricing tiers.</p>
<p>Member identification quality varies by source. GitHub identification is excellent because GitHub usernames and email addresses often link to real identity. Discord identification is harder because Discord users hide behind pseudonyms. Slack varies by community. Reddit is mostly anonymous. The mapped-to-company rates Common Room shows are accurate at the source level but worth understanding by channel before building activation workflows on top of them.</p>
<p>The activation features lag the data collection features. Common Room is excellent at capturing and organizing community signals. Pushing those signals into sales workflows happens through integrations that vary in depth. For most teams, the practical pattern is exporting signals into a CRM or outbound tool and running activation there, which works but creates friction compared to Common Room providing native activation throughout.</p>
""",
    "verdict": """
<p>Common Room is the right signal platform for GTM teams at developer-tool companies, open-source businesses, and PLG SaaS products with active communities. The product captures buying signals that traditional intent and CRM tools miss, and for the right audience the lift in pipeline visibility justifies the price.</p>
<p>For non-developer audiences or small communities, Common Room is over-engineered. A simpler signal stack (RB2B for website visitors, UserGems for job changes, intent data from G2 or 6sense) covers more of the actionable signal surface at lower cost. Buy Common Room when community engagement is structurally part of your buyer's journey, not because community feels like it should matter.</p>
<p>The category is converging. Common Room competes with broader signal platforms like Pocus (heavier on product-qualified leads), Default (heavier on outbound activation), and emerging players blending community plus product signals. Evaluate Common Room against the specific signal sources that matter for your buyer's journey rather than category labels. The right signal stack is whatever surfaces the buying moments your team can act on within 48 hours.</p>
""",
    "faq": [
        ("Common Room vs Pocus: which one for PLG companies?", "Pocus skews toward product usage signals and PQL identification. Common Room skews toward community engagement signals and broader signal aggregation. PLG companies with strong community motions often run both, with Pocus driving the product-qualified-lead funnel and Common Room driving community-qualified-lead context. Companies with strong product signals but weak communities should start with Pocus. Companies with strong communities but limited product telemetry should start with Common Room."),
        ("Does Common Room track private Slack and Discord communities?", "Yes, with proper authentication and admin permissions in your community workspaces. Common Room is deployed inside your Slack or Discord with admin-level access, which lets it read messages, identify members, and track engagement metrics. The integration respects member privacy in ways that vary by platform; for example, direct messages are typically not tracked. Configure carefully and communicate clearly with your community about what's being tracked."),
        ("How does Common Room compare to BuiltWith for technographic data?", "Different categories. BuiltWith specializes in technographic data sourced from website crawling. Common Room focuses on community and engagement signals plus some adjacent technographic features. Most GTM teams that need real technographic depth pair BuiltWith or Sumble with Common Room rather than using either as a substitute for the other."),
        ("Is Common Room overkill if we have a small community under 1,000 members?", "Probably yes at full Team-tier pricing. Small communities don't generate enough signal volume to justify the spend. Track manually with spreadsheets and lightweight tools until your community grows to 3,000-5,000 members. At that scale, the manual approach breaks down and a platform like Common Room produces enough new signal value to justify the cost. Below that size, the investment usually doesn't pay back."),
    ],
},

}
