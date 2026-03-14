"""Comparison content for LinkedIn & Social matchups."""

COMPARISONS = {
    "heyreach-vs-expandi": {
        "intro": """<p>HeyReach and Expandi are both LinkedIn automation platforms, but they target different operators and solve different scaling problems. HeyReach is built for agencies and teams that need to run LinkedIn outreach across multiple accounts with centralized management. Expandi is built for individual users and small teams that want cloud-based LinkedIn automation with smart safety limits.</p>
<p>LinkedIn automation sits in a gray area. Both tools violate LinkedIn's Terms of Service by automating actions (connection requests, messages, profile visits). The risk of account restrictions is real. The tools differ in how they manage that risk and how they scale outreach without getting flagged.</p>
<p>This comparison evaluates both platforms on automation depth, multi-account management, safety features, pricing, and integration with the broader GTM stack. We'll be direct about the compliance risks.</p>""",

        "feature_table": """<div class="table-responsive"><table class="data-table">
<thead>
<tr><th>Feature</th><th>HeyReach</th><th>Expandi</th></tr>
</thead>
<tbody>
<tr><td>Multi-account Support</td><td>Unlimited LinkedIn accounts per workspace</td><td>1 account per subscription</td></tr>
<tr><td>Automation Actions</td><td>Connect, message, InMail, profile visit, follow</td><td>Connect, message, InMail, profile visit, follow, endorse</td></tr>
<tr><td>Campaign Types</td><td>Connection + message sequences</td><td>Smart sequences with conditions</td></tr>
<tr><td>Smart Limits</td><td>Account-level daily limits</td><td>AI-driven activity simulation</td></tr>
<tr><td>Dedicated IP</td><td>Yes (per account)</td><td>Yes (dedicated country-based IP)</td></tr>
<tr><td>CRM Integration</td><td>HubSpot, Salesforce (native)</td><td>HubSpot, Salesforce, Pipedrive (via webhooks)</td></tr>
<tr><td>Webhook Support</td><td>Yes</td><td>Yes</td></tr>
<tr><td>Agency Features</td><td>Multi-client dashboards, unified inbox</td><td>Limited (1 account per sub)</td></tr>
<tr><td>A/B Testing</td><td>Connection request + message A/B</td><td>Campaign-level A/B testing</td></tr>
<tr><td>Analytics</td><td>Per-account + aggregate dashboards</td><td>Campaign analytics + funnel metrics</td></tr>
<tr><td>Pricing</td><td>$79/mo per sender (volume discounts)</td><td>$99/mo per account</td></tr>
<tr><td>Best For</td><td>Agencies + multi-account teams</td><td>Solo users + small teams</td></tr>
</tbody>
</table></div>""",

        "tool_a_strengths": """<h2>Where HeyReach Wins</h2>
<p>Multi-account management is HeyReach's defining feature. You can connect unlimited LinkedIn accounts to a single workspace, run campaigns across all of them, and manage replies from a unified inbox. For agencies running outbound on behalf of 10-50 clients, this centralization is essential. Expandi requires separate subscriptions for each LinkedIn account, making multi-client management expensive and fragmented.</p>
<p>The unified inbox aggregates replies from all connected LinkedIn accounts into one view. Instead of logging into 15 LinkedIn accounts to check messages, your team sees all conversations in one place. You can assign replies to team members, tag conversations by status, and track response rates across accounts. This operational efficiency is significant when managing high-volume LinkedIn outreach.</p>
<p>Pricing scales better for teams. HeyReach charges $79/month per sender with volume discounts. At 10+ accounts, the per-account cost drops further. Expandi charges $99/month per account with no volume discounts. A 10-account operation costs $790/month on HeyReach vs $990/month on Expandi, and the gap widens with scale.</p>
<p>HeyReach's campaign distribution feature splits a single prospect list across multiple LinkedIn accounts. Instead of one account sending 100 connection requests per day (risky), five accounts each send 20. This approach reduces per-account activity, lowering the risk of LinkedIn restrictions while maintaining outreach volume.</p>""",

        "tool_b_strengths": """<h2>Where Expandi Wins</h2>
<p>Expandi's smart sequences are more sophisticated than HeyReach's campaign builder. You can create conditional workflows: if a connection request is accepted, send message A. If the prospect views your profile but doesn't accept, send an InMail. If they don't respond to the first message, follow up with a different angle after 3 days. This conditional logic creates personalized outreach flows that respond to prospect behavior.</p>
<p>Safety features are more granular. Expandi uses AI to simulate human-like browsing patterns between automation actions. The platform randomizes delays, varies action types, and mimics organic LinkedIn usage patterns. Dedicated country-based IPs match your LinkedIn account's location. These precautions reduce the risk of LinkedIn detecting automated activity.</p>
<p>Expandi's personalization capabilities include dynamic images and GIFs embedded in LinkedIn messages. Custom images with the prospect's name, company logo, or profile photo increase reply rates by making automated messages feel manual. HeyReach supports text personalization through variables, but Expandi's visual personalization goes further.</p>
<p>For individual users and small teams (1-3 accounts), Expandi's single-account focus means the product is optimized for one user's workflow. The interface is simpler, the analytics focus on your campaigns, and the setup doesn't require understanding multi-account architecture. If you're a solo GTM Engineer running LinkedIn outreach from your own account, Expandi's focused experience is less overwhelming.</p>""",

        "pricing_comparison": """<h2>Pricing Breakdown</h2>
<p>HeyReach: $79/month per sender account. Volume discounts apply at 5+ accounts. Agency and enterprise plans offer further discounts with annual commitments. A solo operator pays $79/month. A 10-account team pays approximately $700-$790/month. The per-sender model means you pay for each LinkedIn account you automate, regardless of how many team members manage it.</p>
<p>Expandi: $99/month per LinkedIn account. No volume discounts on the standard plan. Business plans for agencies are custom-priced. A solo operator pays $99/month. A 10-account agency pays $990/month or more. Expandi also offers a 7-day free trial to test before committing.</p>
<p>For a single account, the difference is $20/month ($79 vs $99). For agencies and teams with 10+ accounts, HeyReach saves 20-30% monthly. The pricing advantage compounds with scale: at 25 accounts, HeyReach saves $500+/month over Expandi. Factor in HeyReach's unified inbox and multi-account dashboards (which Expandi lacks), and the total cost of ownership favors HeyReach for any operation running more than 3 LinkedIn accounts.</p>""",

        "verdict": """<h2>The Verdict</h2>
<p>Use HeyReach if you manage LinkedIn outreach across multiple accounts. Agencies, teams with dedicated prospecting accounts, and any operation running 3+ LinkedIn profiles should use HeyReach for the multi-account management, unified inbox, and volume pricing. HeyReach was purpose-built for the multi-sender workflow that most GTM teams need.</p>
<p>Use Expandi if you're a solo operator running outreach from a single LinkedIn account and you want the most sophisticated automation sequences. Expandi's conditional workflows, visual personalization, and safety features are best-in-class for individual users. The single-account focus means the product is refined for that use case.</p>
<p>A compliance note: both tools automate LinkedIn actions that violate LinkedIn's Terms of Service. Account restrictions happen. Use dedicated LinkedIn accounts (not your primary profile) for automation. Keep daily activity within conservative limits (20-30 connection requests/day). Accept that occasional account warnings are part of the trade-off. The risk is real, and neither tool can eliminate it.</p>""",

        "faq": [
            ("Will LinkedIn ban my account for using automation?", "LinkedIn actively detects and restricts accounts using automation tools. Both HeyReach and Expandi include safety features to reduce risk, but no tool can guarantee your account won't be flagged. Use dedicated prospecting accounts (not your personal profile), keep daily limits conservative, and warm up new accounts gradually. Temporary restrictions (1-2 week lockouts) are common."),
            ("Can I use HeyReach or Expandi with Clay?", "Both integrate with GTM tools via webhooks. You can trigger LinkedIn outreach from Clay workflows when a lead meets certain criteria. The typical pattern: Clay enriches a lead, pushes it to HeyReach/Expandi via webhook, and the LinkedIn campaign starts automatically. HeyReach's API is more developed for this type of programmatic integration."),
            ("Do I need LinkedIn Sales Navigator with these tools?", "Sales Navigator is recommended but not required. Both tools work with free LinkedIn accounts, but Sales Navigator provides better search filters, InMail credits, and higher connection request limits. Most serious LinkedIn outreach operations pair Sales Navigator with an automation tool."),
            ("Which is better for B2B outbound LinkedIn prospecting?", "For teams: HeyReach. The multi-account management and unified inbox are necessary at scale. For solo GTM Engineers: Expandi's conditional sequences and safety features provide a better individual experience. Both connect to the same LinkedIn infrastructure and achieve similar outreach outcomes."),
            ("Can LinkedIn automation replace cold email?", "No. LinkedIn automation supplements cold email. Typical reply rates on LinkedIn (15-25% for warm connection requests) are higher than cold email (2-5%), but LinkedIn limits daily volume. Most GTM teams run email for volume and LinkedIn for high-value targets. Tools like Lemlist combine both channels in one sequence."),
        ],
    },

    "linkedin-sales-nav-vs-apollo": {
        "intro": """<p>LinkedIn Sales Navigator and Apollo represent two fundamentally different approaches to B2B prospecting. Sales Navigator gives you access to LinkedIn's 900M+ member database with advanced search, lead tracking, and InMail capabilities. Apollo gives you a standalone 275M+ B2B contact database with email finding, enrichment, and built-in outbound sequencing. One lives inside LinkedIn's ecosystem. The other is an independent prospecting platform.</p>
<p>For GTM Engineers, this comparison is about data source and workflow architecture. Sales Navigator's data is LinkedIn's first-party profile data, always current because users maintain their own profiles. Apollo's data is aggregated from multiple sources, verified through their own processes, and can go stale. But Apollo gives you emails, phone numbers, and sequencing that Sales Navigator doesn't.</p>
<p>This comparison covers data quality, prospecting workflows, pricing at different scales, and how each tool fits into a GTM Engineer's pipeline infrastructure.</p>""",

        "feature_table": """<div class="table-responsive"><table class="data-table">
<thead>
<tr><th>Feature</th><th>LinkedIn Sales Navigator</th><th>Apollo.io</th></tr>
</thead>
<tbody>
<tr><td>Database Size</td><td>900M+ LinkedIn members</td><td>275M+ B2B contacts</td></tr>
<tr><td>Data Source</td><td>First-party (user-maintained profiles)</td><td>Aggregated + verified</td></tr>
<tr><td>Email Addresses</td><td>No (InMail only)</td><td>Yes (built-in email finder)</td></tr>
<tr><td>Phone Numbers</td><td>No</td><td>Yes (direct + mobile)</td></tr>
<tr><td>Search Filters</td><td>Advanced (title, company, industry, geography, seniority, tenure, growth signals)</td><td>Advanced (title, company, industry, geography, tech stack, revenue, headcount)</td></tr>
<tr><td>Lead Tracking</td><td>Save leads + get activity alerts</td><td>Save leads + intent signals</td></tr>
<tr><td>InMail</td><td>50-150/month (plan-dependent)</td><td>No</td></tr>
<tr><td>Outbound Sequencing</td><td>No</td><td>Built-in (email + call sequences)</td></tr>
<tr><td>CRM Integration</td><td>Salesforce + HubSpot (sync leads)</td><td>Salesforce + HubSpot (bi-directional sync)</td></tr>
<tr><td>Chrome Extension</td><td>LinkedIn-embedded features</td><td>Chrome extension for LinkedIn prospecting</td></tr>
<tr><td>Pricing</td><td>$99-$179/user/month</td><td>$0-$149/user/month</td></tr>
<tr><td>Free Tier</td><td>No (free trial only)</td><td>Yes (10,000 email credits/month)</td></tr>
<tr><td>Best For</td><td>LinkedIn-native research + InMail</td><td>Full-cycle prospecting + outbound</td></tr>
</tbody>
</table></div>""",

        "tool_a_strengths": """<h2>Where LinkedIn Sales Navigator Wins</h2>
<p>Data freshness is Sales Navigator's unbeatable advantage. LinkedIn profiles are maintained by users themselves: job changes, promotions, company switches, and new skills are updated in real-time. When someone changes roles, their LinkedIn profile reflects it within days. Apollo's database can take weeks or months to catch up. For targeting people in specific roles at specific companies, Sales Navigator's data is the most current available.</p>
<p>The search filter depth is unmatched for finding specific personas. Filter by years in current role, recent job changes, company headcount growth, shared connections, group memberships, and posted content. These signals let you identify not just who matches your ICP, but who is most likely to respond: people who just started a new role (open to new tools), at growing companies (have budget), or who post about relevant topics (engaged).</p>
<p>InMail reaches prospects you can't email. InMail messages go directly to a LinkedIn member's inbox even if you're not connected. Response rates on InMail (10-25%) are typically higher than cold email (2-5%) because InMail carries the implicit trust of the LinkedIn platform. For enterprise prospects who don't respond to cold email, InMail is often the only channel that works.</p>
<p>Lead and account alerts track changes in your saved prospects: job changes, company news, content posts, and profile views. These signals create timely outreach triggers. "Congratulations on the new VP Sales role" is a warm opener that converts better than generic cold outreach. No other prospecting tool provides these behavioral signals from LinkedIn's first-party data.</p>""",

        "tool_b_strengths": """<h2>Where Apollo Wins</h2>
<p>Apollo gives you contact data that Sales Navigator withholds. Email addresses, phone numbers, and direct dials are the output GTM Engineers need to run outbound campaigns. Sales Navigator shows you who to target but doesn't give you a way to reach them outside of LinkedIn. Apollo gives you the email, the phone number, and the sequencing platform to run campaigns. This makes Apollo a complete prospecting solution while Sales Navigator is a research tool.</p>
<p>The free tier is transformative. 10,000 email credits per month, access to the full database, basic sequencing, and a Chrome extension that overlays contact data on LinkedIn profiles. A GTM Engineer can use Apollo's free tier alongside LinkedIn (free or Sales Navigator) to get contact details for any profile they find. No other tool matches this free value.</p>
<p>Built-in sequencing means you can go from search to outbound in one platform. Find 200 accounts matching your ICP, export their contacts with verified emails, build a 5-step email sequence, and launch the campaign. On Sales Navigator, you'd need to export leads (limited), find their emails separately (Clay, FullEnrich, or another tool), import to a sequencing platform (Instantly, Lemlist), and then send. Apollo collapses 4 tools into 1.</p>
<p>Apollo's Chrome extension turns LinkedIn browsing into a prospecting workflow. View any LinkedIn profile and Apollo overlays their email, phone number, company data, and a one-click "add to sequence" button. This effectively gives you Sales Navigator's search + Apollo's contact data in one browser tab. Many GTM Engineers use LinkedIn for searching and Apollo's extension for capturing contact details.</p>""",

        "pricing_comparison": """<h2>Pricing Breakdown</h2>
<p>LinkedIn Sales Navigator: Core ($99.99/user/month annual), Advanced ($179.99/user/month annual). Core includes advanced search, lead alerts, and 50 InMail credits. Advanced adds TeamLink (shared connections across your org), CRM integration, and smart links tracking. There's no free tier. The annual commitment is required for these prices; monthly billing is approximately 20% higher.</p>
<p>Apollo: Free (10,000 email credits/month, basic features), Basic ($59/user/month for 5,000 credits + sequencing), Professional ($99/user/month for unlimited credits + advanced filters), Organization ($149/user/month for API access + advanced reporting). Monthly or annual billing, with annual discounts of roughly 20%.</p>
<p>The practical comparison: many GTM Engineers use Sales Navigator Core ($100/month) alongside Apollo Free ($0/month). Total: $100/month for LinkedIn's search + research capabilities plus Apollo's contact data and basic sequencing. This combination costs less than Apollo Professional alone ($99/month) while giving you the best of both platforms. If budget is tight, start with Apollo Free and upgrade Sales Navigator only when you need advanced LinkedIn search or InMail.</p>""",

        "verdict": """<h2>The Verdict</h2>
<p>These tools complement more than they compete. Sales Navigator is a research and signal tool. Apollo is a prospecting and outbound tool. The strongest setup is using both: Sales Navigator for finding the right people with LinkedIn's first-party data, Apollo's Chrome extension for capturing their contact details, and Apollo's sequencing for running campaigns.</p>
<p>If you can only pick one, choose Apollo. Apollo gives you a complete prospecting workflow (search, enrichment, sequencing) in one platform with a generous free tier. Sales Navigator gives you LinkedIn search and InMail but no emails, no phone numbers, and no sequencing. For a GTM Engineer who needs to generate pipeline, Apollo covers more of the workflow.</p>
<p>Add Sales Navigator when your outbound operation matures and you need: (1) better search filters for precise targeting, (2) InMail as a channel for enterprise prospects, or (3) lead alerts for trigger-based outreach. The $100/month investment pays for itself if LinkedIn search quality improves your ICP targeting enough to lift reply rates.</p>""",

        "faq": [
            ("Can I export leads from LinkedIn Sales Navigator?", "Sales Navigator allows limited list exports to CRM (Salesforce/HubSpot) via its built-in sync. You cannot bulk export contact details (emails, phone numbers) because LinkedIn doesn't provide them. Most GTM Engineers use Apollo's Chrome extension on Sales Navigator search results to capture contact data for each profile."),
            ("Is Apollo's data from LinkedIn?", "Apollo aggregates data from multiple sources, and LinkedIn profiles are one input. But Apollo's email addresses and phone numbers come from their own verification process, not from LinkedIn. The data quality and freshness are independent of LinkedIn's database."),
            ("Do I need Sales Navigator if I have Apollo's Chrome extension?", "Apollo's extension works on free LinkedIn, but Sales Navigator's advanced search filters (company growth, years in role, shared connections) produce better prospect lists. Think of it as: free LinkedIn + Apollo extension is the budget option, Sales Navigator + Apollo extension is the premium option. The search quality difference is noticeable."),
            ("Which is better for enterprise prospecting?", "Sales Navigator. Enterprise prospects are harder to reach by email and more responsive to InMail. Sales Navigator's lead alerts, shared connection intelligence (TeamLink), and company news signals create warmer outreach opportunities. Apollo works for volume-based enterprise prospecting, but Sales Navigator adds the context layer that enterprise selling requires."),
            ("Can I run LinkedIn automation from Sales Navigator?", "Not natively. Sales Navigator has no automation features. You'd pair it with a LinkedIn automation tool like HeyReach or Expandi. The workflow: use Sales Navigator for search, export profiles to your automation tool, and run automated connection requests and messages. Sales Navigator provides the targeting, the automation tool handles execution."),
        ],
    },
}
