# content/tools_analytics.py
# Review prose for 2 analytics tools (Segment, PostHog).

TOOL_REVIEWS = {

"segment": {
    "overview": """
<p>Segment is a customer data platform (CDP) that collects event data from websites, apps, and servers, then routes it to 400+ downstream tools. You instrument Segment once, and it fans your data out to your analytics platform, your CRM, your email tool, your ad platforms, and your data warehouse simultaneously. For companies with complex multi-tool stacks, Segment eliminates the need to build individual integrations for every tool.</p>
<p>The product sits in the data infrastructure layer, not the analytics layer. Segment doesn't generate dashboards or reports. It collects, cleans, routes, and resolves identity across touchpoints. When a prospect visits your website, opens an email, and signs up for a trial, Segment stitches those events into a single user profile. That unified profile then flows to every downstream tool with consistent data.</p>
<p>Twilio acquired Segment in 2020 for $3.2B, which created both opportunities (deeper Twilio product integrations) and uncertainty (product roadmap shifts, organizational restructuring). The core product remains strong, but the CDP market has evolved. Newer alternatives like RudderStack (open-source Segment) and composable CDPs (Hightouch, Census) challenge Segment's position by offering warehouse-native approaches that skip the middleman.</p>
""",
    "gtm_use_cases": """
<ul>
    <li><strong>Unified event tracking across marketing and product.</strong> Instrument Segment's analytics.js on your website and app. Every pageview, button click, form submission, and product action gets captured once and sent to all your tools. No more maintaining separate tracking code for Google Analytics, Mixpanel, and HubSpot.</li>
    <li><strong>Identity resolution for prospect-to-customer journeys.</strong> Segment's Profiles feature merges anonymous visitor data with known user data after they identify themselves. Track the full journey from first ad click through demo request to closed deal with a single identity graph.</li>
    <li><strong>Real-time event routing to outbound tools.</strong> When a prospect hits your pricing page for the third time, Segment can push that event to Slack, HubSpot, or your sales engagement tool in real-time. GTM Engineers build intent-based triggers off Segment events.</li>
    <li><strong>Data quality enforcement with Protocols.</strong> Segment Protocols lets you define a tracking plan (which events, which properties, which types) and validates incoming data against it. Malformed events get blocked or flagged. This prevents the "garbage in, garbage out" problem that plagues analytics stacks.</li>
    <li><strong>Warehouse integration for custom analysis.</strong> Segment's Warehouses destination pushes raw event data to Snowflake, BigQuery, or Redshift. GTM Engineers who write SQL can build custom attribution models, cohort analyses, and pipeline analytics on the raw event stream.</li>
</ul>
""",
    "pricing": """
<table class="data-table">
    <thead><tr><th>Plan</th><th>Price</th><th>MTUs</th><th>Key Features</th></tr></thead>
    <tbody>
        <tr><td>Free</td><td>$0</td><td>1,000</td><td>2 sources, 300+ integrations, basic analytics</td></tr>
        <tr><td>Team</td><td>$120/mo</td><td>10,000</td><td>Unlimited sources, Protocols, custom functions</td></tr>
        <tr><td>Business</td><td>Custom</td><td>Custom</td><td>Identity resolution, data governance, SLA, SSO</td></tr>
    </tbody>
</table>
<p>Segment's pricing is based on Monthly Tracked Users (MTUs), which counts unique users sending events through Segment. The free tier's 1,000 MTUs work for early-stage products. The jump to $120/month for 10,000 MTUs is steep for what remains a data routing tool, not an analytics product.</p>
<p>The real cost escalation happens at scale. Companies with 50,000-500,000 MTUs pay thousands per month. Segment's Business tier pricing is custom-quoted and starts at $12,000+/year. For companies spending that much on data routing, the ROI calculation needs to account for the engineering time Segment saves versus maintaining direct integrations. At smaller scale, the question is whether you need a CDP at all.</p>
""",
    "criticism": """
<p>Most GTM Engineers don't need a CDP. Segment solves a problem that emerges at scale: managing event data across many downstream tools. If your stack is Clay + Apollo + HubSpot + Instantly, you don't have a data routing problem. Direct integrations between these tools work fine. Segment adds value when you have 10+ downstream destinations consuming the same event stream. Below that threshold, it's engineering overhead without proportional benefit.</p>
<p>Pricing escalates quickly with MTUs. A SaaS company with 50,000 monthly active users can face $500-$1,500/month in Segment costs just for data routing. This is money that buys no dashboards, no reports, no insights. It buys the infrastructure to send data to tools that generate those insights. For budget-conscious teams, maintaining direct integrations (more engineering time, lower tool cost) is often the better trade.</p>
<p>The Twilio acquisition created roadmap uncertainty. Segment's original vision was "API for customer data." Under Twilio, the product has shifted toward Twilio Engage (campaign orchestration) and tighter Twilio product integrations. Some long-time users report that innovation on the core CDP features has slowed while the company pursues Twilio-centric use cases. Whether this matters depends on whether you use Twilio's other products.</p>
""",
    "verdict": """
<p>Segment is excellent infrastructure for companies with complex, multi-tool data stacks. If you're routing event data to 10+ downstream tools and need identity resolution across web, mobile, and server-side touchpoints, Segment saves significant engineering time and ensures data consistency.</p>
<p>Most GTM Engineers won't need Segment directly. It's a platform engineering decision, not a practitioner purchase. If your company already uses Segment, learn to work with it: understand the tracking plan, use the Protocols to enforce data quality, and build workflows off Segment events. If your company doesn't use Segment, don't buy it just for GTM purposes. HubSpot, Apollo, and Clay handle the data routing GTM Engineers need without a CDP layer.</p>
""",
    "faq": [
        ("Do GTM Engineers need Segment?", "Most don't. Segment solves data routing at scale (10+ downstream tools). GTM Engineers typically work with 4-6 tools that have direct integrations. Segment becomes relevant when you're building complex event-driven workflows or when your company already has Segment deployed and you can build on top of it."),
        ("How does Segment compare to PostHog?", "Different products for different problems. Segment routes data to other tools. PostHog analyzes data directly. Segment has no dashboards. PostHog is primarily dashboards. Some companies use both: Segment for data collection/routing, PostHog as one of the analytics destinations. For GTM Engineers who want analytics, PostHog is the more useful tool."),
        ("Is RudderStack a better alternative to Segment?", "RudderStack is open-source Segment with warehouse-first architecture. If your team is comfortable self-hosting and wants to avoid MTU-based pricing, RudderStack is a strong alternative. Data quality and integration coverage are comparable for most use cases. The tradeoff: you manage the infrastructure. For cloud-hosted, RudderStack's pricing is competitive with Segment."),
        ("What's the difference between Segment and a data warehouse?", "Segment collects and routes data in real-time. A data warehouse (Snowflake, BigQuery) stores data for batch analysis. Segment can send data to your warehouse, making them complementary. Think of Segment as the pipeline and the warehouse as the destination. You can skip Segment and send data directly to your warehouse, but you lose real-time routing to other tools."),
    ],
},

"posthog": {
    "overview": """
<p>PostHog is an open-source product analytics platform that combines event tracking, session replay, feature flags, A/B testing, and user surveys in a single tool. The generous free tier (1M events/month, 5K session replays) makes it accessible to startups and solo practitioners. For GTM Engineers who code, PostHog's developer-friendly approach and self-hosting option make it the analytics tool that fits their workflow best.</p>
<p>Unlike Segment (which routes data), PostHog analyzes it. You instrument PostHog's SDK, track events, and build funnels, retention charts, user paths, and dashboards directly in PostHog. Session replay lets you watch real user interactions. Feature flags let you roll out changes to segments of your user base. The all-in-one approach eliminates the need for separate tools for each capability.</p>
<p>PostHog launched as a Mixpanel/Amplitude alternative for developers. The product has matured significantly: SOC 2 compliance, EU data hosting, HIPAA-compliant options, and a growing set of enterprise features. The self-hosted version runs on your own infrastructure for full data control. The cloud version handles hosting for you with a usage-based pricing model.</p>
""",
    "gtm_use_cases": """
<ul>
    <li><strong>Product-led growth analytics.</strong> Track trial-to-paid conversion funnels, feature adoption rates, and activation metrics. PostHog's funnel analysis shows where prospects drop off and which features correlate with conversion. GTM Engineers use this data to trigger outbound at drop-off points.</li>
    <li><strong>Session replay for prospect research.</strong> Watch recordings of how prospects interact with your product during trials. See which features they explore, where they get confused, and what they try before churning. This informs personalized outbound messaging tied to observed behavior.</li>
    <li><strong>Feature flag-driven A/B testing.</strong> Test different onboarding flows, pricing page layouts, and feature experiences with PostHog's built-in experimentation. GTM Engineers running product-led growth experiments can iterate without engineering bottlenecks.</li>
    <li><strong>Event-triggered outbound workflows.</strong> PostHog's webhook destinations push events to n8n, Make, or custom endpoints. When a trial user hits a usage threshold, completes onboarding, or goes inactive for 3 days, trigger an automated outbound sequence.</li>
    <li><strong>Custom dashboards for pipeline visibility.</strong> Build dashboards combining product usage data with pipeline metrics. Track which product actions correlate with closed deals. Share dashboards with sales teams to surface product-qualified leads.</li>
</ul>
""",
    "pricing": """
<table class="data-table">
    <thead><tr><th>Product</th><th>Free Tier</th><th>Paid (per unit)</th><th>Notes</th></tr></thead>
    <tbody>
        <tr><td>Product Analytics</td><td>1M events/mo</td><td>$0.00031/event</td><td>Funnels, trends, paths, retention</td></tr>
        <tr><td>Session Replay</td><td>5,000 recordings/mo</td><td>$0.005/recording</td><td>Full DOM capture, network tab</td></tr>
        <tr><td>Feature Flags</td><td>1M requests/mo</td><td>$0.0001/request</td><td>Multivariate, percentage rollouts</td></tr>
        <tr><td>Surveys</td><td>250 responses/mo</td><td>$0.20/response</td><td>Targeted in-app surveys</td></tr>
    </tbody>
</table>
<p>PostHog's free tier is the most generous in the analytics category. 1M events per month covers most early-stage SaaS products and internal tools. The usage-based pricing means you pay only for what you use, with no seat-based fees. A startup tracking 5M events per month pays roughly $120/month for analytics, which undercuts Mixpanel and Amplitude significantly.</p>
<p>Self-hosting is free with no event limits. You pay only for infrastructure. This is the option for companies that need data sovereignty, HIPAA compliance, or want to eliminate recurring analytics costs entirely. The tradeoff: you manage the deployment, scaling, and upgrades.</p>
""",
    "criticism": """
<p>PostHog is product analytics, not marketing analytics. If you need multi-touch attribution, campaign performance tracking, or ad spend optimization, PostHog won't replace Google Analytics, HubSpot analytics, or a dedicated marketing analytics tool. The product tracks what users do inside your product. It doesn't track how they found you, which ads drove them, or which content influenced their purchase. GTM Engineers focused on top-of-funnel metrics need a separate tool.</p>
<p>Self-hosting requires infrastructure expertise. Running PostHog's ClickHouse-based analytics stack on your own servers demands familiarity with Kubernetes, database management, and monitoring. The minimum recommended spec (8 CPU, 32GB RAM for ClickHouse) means hosting costs $100-300/month for serious workloads. For most teams, cloud PostHog is simpler unless data sovereignty is a hard requirement.</p>
<p>Some enterprise features are still catching up to incumbents. PostHog has added group analytics, data warehouse queries, and SQL-based insights, but the depth of analysis in Mixpanel's advanced reports or Amplitude's behavioral cohorting is deeper in edge cases. For common analytics tasks (funnels, retention, user paths), PostHog matches competitors. For advanced statistical analysis on large datasets, the incumbents have a head start.</p>
""",
    "verdict": """
<p>PostHog is the best analytics tool for GTM Engineers who work on product-led growth. The combination of analytics, session replay, feature flags, and A/B testing in one platform with a generous free tier makes it the default choice for technical teams. The developer-friendly approach (API-first, open-source, self-hostable) matches how GTM Engineers prefer to work.</p>
<p>Use PostHog if you need product analytics (not marketing analytics), you want to avoid per-seat pricing, and you value the ability to self-host or access your data via API. Skip PostHog if you need marketing attribution, campaign analytics, or if your analytics needs are simple enough for Google Analytics. For GTM Engineers at companies already using Mixpanel or Amplitude, PostHog is worth evaluating for the cost savings and session replay features alone.</p>
""",
    "faq": [
        ("Is PostHog free?", "The cloud version includes 1M free events/month, 5K free session replays, and 1M free feature flag requests. Most early-stage products and internal tools stay within the free tier. The self-hosted version is free with no usage limits. You pay only for server hosting."),
        ("How does PostHog compare to Mixpanel?", "PostHog offers analytics + session replay + feature flags + A/B testing in one tool. Mixpanel is pure analytics with deeper statistical features. PostHog's free tier (1M events) is more generous than Mixpanel's (20M events but limited features). PostHog is open-source and self-hostable. Mixpanel is cloud-only. For GTM Engineers who want one tool for analytics and experimentation, PostHog wins on breadth. For advanced behavioral analytics, Mixpanel has more depth."),
        ("Can I use PostHog for GTM workflows?", "Yes, through event-triggered webhooks. When users hit specific events (trial signup, feature activation, usage threshold), PostHog can push those events to n8n, Make, or custom API endpoints. This enables product-qualified lead workflows where product behavior triggers outbound sales actions."),
        ("Is PostHog suitable for enterprise?", "PostHog has SOC 2 Type II compliance, EU hosting, HIPAA options, SSO, and role-based access. Enterprise adoption is growing, with companies like Airbus and Phantom using PostHog. The main gap vs incumbents is in advanced governance features and dedicated support tiers, which PostHog is actively building."),
    ],
},

}
