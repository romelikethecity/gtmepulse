"""Roundup content for outbound infrastructure and LinkedIn scraping tools."""

ROUNDUPS = {
    "best-cold-email-infrastructure": {
        "intro": """<p>Sending cold email in 2026 is an infrastructure problem. You need dedicated domains, warmed inboxes, rotation logic, and deliverability monitoring before your first campaign goes out. The tools below handle the plumbing so your emails land in inboxes instead of spam folders.</p>
<p>We ranked these platforms on four things that matter for GTM Engineers: inbox management at scale (can you run 50+ inboxes without losing track?), warmup quality (do their warmup networks measurably improve reputation?), deliverability analytics (can you diagnose problems before reply rates tank?), and API access for automation workflows. Price matters too, but cheap infrastructure that lands in spam isn't a deal.</p>""",

        "tools": [
            {
                "rank": 1,
                "name": "Instantly",
                "slug": "instantly-review",
                "category_tag": "Email Infrastructure",
                "best_for": "GTM Engineers running 10+ inboxes who need reliable deliverability at scale",
                "why_picked": "Instantly owns the cold email infrastructure category for a reason. Unlimited email accounts, the largest warmup network in the space, and a campaign builder that handles rotation across dozens of inboxes without breaking. The analytics dashboard shows deliverability trends per inbox, so you catch problems before they tank your reply rate. At $30/month for the Growth plan, the unit economics are hard to beat. The API is solid enough for n8n/Make integrations, though it's not as deep as Smartlead's for custom workflows.",
                "pricing": "$30-$77.6/mo",
                "link_to_review": True,
            },
            {
                "rank": 2,
                "name": "Smartlead",
                "slug": "smartlead-review",
                "category_tag": "Email Infrastructure",
                "best_for": "Agencies and multi-client GTM operations that need white-label infrastructure",
                "why_picked": "Smartlead was built for agencies, and it shows. Client-level campaign management, white-label dashboards, and unlimited mailboxes make it the default for GTM Engineers running outbound for multiple companies. The API is deeper than Instantly's, which matters when you're building custom pipelines with n8n or Clay. Deliverability is comparable to Instantly. The tradeoff: the UI is less polished, and the learning curve for the multi-client architecture takes a few hours to navigate.",
                "pricing": "$39+/mo",
                "link_to_review": True,
            },
            {
                "rank": 3,
                "name": "Saleshandy",
                "slug": None,
                "category_tag": "Email Infrastructure",
                "best_for": "Budget-conscious teams that want sending + verification in one platform",
                "why_picked": "Saleshandy bundles email verification with sending, which saves you a separate tool subscription. The inbox rotation and warmup work out of the box, and the interface is clean enough that you won't waste time figuring out the UI. It won't win awards for innovation, but it ships emails reliably at a fair price. The $25/month starting point includes features that Instantly charges more for, like built-in verification. The downside: smaller user community means fewer templates, guides, and community support when you hit issues.",
                "pricing": "$25+/mo",
                "link_to_review": False,
            },
            {
                "rank": 4,
                "name": "Mailforge",
                "slug": None,
                "category_tag": "Domain Infrastructure",
                "best_for": "High-volume senders who need cheap sending domains and mailboxes",
                "why_picked": "Mailforge solves one specific problem: spinning up sending domains and mailboxes at scale for pennies. At $3/mailbox/month, you can run 50 inboxes for $150/month. That's the infrastructure layer underneath Instantly or Smartlead. It handles DNS configuration, SPF/DKIM/DMARC setup, and basic warmup. The catch: it's infrastructure only. No campaign builder, no analytics, no sequences. You still need a sending platform on top. Think of Mailforge as the factory that produces your sending infrastructure.",
                "pricing": "$3+/mailbox",
                "link_to_review": False,
            },
            {
                "rank": 5,
                "name": "Infraforge",
                "slug": None,
                "category_tag": "Domain Infrastructure",
                "best_for": "GTM Engineers who want automated domain buying and DNS setup",
                "why_picked": "Infraforge automates the tedious part of cold email infrastructure: buying domains, configuring DNS records, and setting up forwarding. For GTM Engineers spinning up new campaigns every month, the time savings add up. The tool is newer and less battle-tested than Mailforge, but the automation angle is compelling if you're managing infrastructure for multiple clients or campaigns. Documentation is thin, and the team is small, so expect to figure some things out on your own.",
                "pricing": "Pay-per-domain",
                "link_to_review": False,
            },
            {
                "rank": 6,
                "name": "EmailGuard",
                "slug": None,
                "category_tag": "Deliverability Monitoring",
                "best_for": "Teams that want proactive deliverability monitoring across all inboxes",
                "why_picked": "EmailGuard monitors your sending reputation across inbox providers and alerts you when deliverability drops. It's a monitoring layer, not a sending tool. The value shows up when you're running 20+ inboxes and can't manually check each one. Before EmailGuard, most GTM Engineers discovered deliverability problems when reply rates fell off a cliff. With it, you catch reputation damage early enough to pull an inbox from rotation before it drags down your whole campaign. Still a young product with limited integrations.",
                "pricing": "Varies",
                "link_to_review": False,
            },
        ],

        "verdict": """<h2>The Verdict</h2>
<p>Instantly is the default pick for most GTM Engineers. The combination of unlimited inboxes, strong warmup, and clean analytics covers 90% of cold email infrastructure needs at $30/month. Smartlead is the better choice if you're running campaigns for multiple clients or need deeper API access for custom automation.</p>
<p>The power move: use Mailforge for cheap mailbox provisioning, connect those inboxes to Instantly or Smartlead for sending, and layer EmailGuard on top for monitoring. That three-layer stack gives you enterprise-grade infrastructure for under $200/month.</p>""",

        "faq": [
            ("How many sending domains do I need for cold email?",
             "Plan for 2-3 mailboxes per domain and 30-50 sends per mailbox per day. If you're sending 500 emails daily, you need roughly 10-15 mailboxes across 4-6 domains. Never use your primary company domain for cold outbound. Buy dedicated sending domains that look related to your brand but won't damage your main domain's reputation if something goes wrong."),
            ("Is Mailforge or Infraforge better for domain setup?",
             "Mailforge if you want cheap mailboxes at scale with manual-ish DNS setup. Infraforge if you want the domain buying and DNS configuration automated. Mailforge is more established with a bigger user base. Infraforge saves more time but is newer. Many high-volume senders use both: Infraforge for the initial domain purchase and setup, then manage ongoing mailboxes through Mailforge."),
            ("What's the minimum warmup period before sending cold email?",
             "Two weeks minimum, three weeks preferred. Start by sending 2-3 warmup emails per day and gradually increase to 30-40 per day. Both Instantly and Smartlead automate this process. Sending cold email from a brand-new inbox without warmup is the fastest way to get flagged as spam. There are no shortcuts here."),
            ("Do I need EmailGuard if I already use Instantly's analytics?",
             "For under 10 inboxes, Instantly's built-in analytics are sufficient. Past 20 inboxes, a dedicated monitoring tool catches problems that per-inbox dashboards miss. EmailGuard shows cross-inbox trends and provider-specific reputation data that campaign-level analytics don't surface. It's insurance, not a requirement."),
        ],
    },

    "best-linkedin-scraping-tools-gtm": {
        "intro": """<p>LinkedIn is the richest source of B2B prospect data on the internet. The problem: LinkedIn doesn't want you scraping it. Every tool in this category operates in a gray area. Some are safer than others. All require careful configuration to avoid account restrictions.</p>
<p>We ranked LinkedIn scraping tools on five criteria: data extraction depth (can you pull emails, job history, and company data?), account safety (how likely is a LinkedIn ban?), automation capabilities (can you run multi-step workflows?), pricing structure, and API quality for integration with your GTM stack. Every tool here works, but each involves tradeoffs between speed, safety, and depth.</p>""",

        "tools": [
            {
                "rank": 1,
                "name": "PhantomBuster",
                "slug": "phantombuster-review",
                "category_tag": "LinkedIn Automation",
                "best_for": "GTM Engineers who need flexible LinkedIn automation with 100+ pre-built workflows",
                "why_picked": "PhantomBuster has the widest library of LinkedIn automation Phantoms: profile scraping, Sales Navigator extraction, auto-connect sequences, post engagement, group member extraction, and more. The proxy integration reduces account risk, and the scheduling system lets you control throughput to stay under LinkedIn's radar. At $49/month for the Starter plan, you get 5 Phantom slots and 10,000 AI credits. The learning curve is moderate. You'll spend a few hours understanding the Phantom ecosystem before you're productive.",
                "pricing": "$49+/mo",
                "link_to_review": True,
            },
            {
                "rank": 2,
                "name": "Waalaxy",
                "slug": None,
                "category_tag": "LinkedIn Outreach",
                "best_for": "Teams that want LinkedIn outreach + email sequences in one simple tool",
                "why_picked": "Waalaxy combines LinkedIn messaging with email sequences in a single workflow. Connect on LinkedIn, send a follow-up message, then switch to email if they don't respond. The interface is the cleanest in this category. Setup takes 15 minutes. The tradeoff: it's less flexible than PhantomBuster for custom scraping workflows and doesn't support Sales Navigator on lower plans. For straightforward LinkedIn outreach with email fallback, it's the fastest path to a working campaign.",
                "pricing": "$40+/mo",
                "link_to_review": False,
            },
            {
                "rank": 3,
                "name": "HeyReach",
                "slug": "heyreach-review",
                "category_tag": "LinkedIn Multi-Account",
                "best_for": "Teams running LinkedIn outreach from multiple accounts to distribute risk",
                "why_picked": "HeyReach is built for multi-account LinkedIn outreach. Connect 5-10 LinkedIn profiles and distribute connection requests across all of them. If one account gets restricted, the campaign continues from others. The campaign builder handles unified inbox management across accounts, which is a logistical headache without a dedicated tool. Pricing starts at $79/month for the Starter plan. The main risk: LinkedIn is actively cracking down on multi-account automation, so the long-term viability of this approach is uncertain.",
                "pricing": "$79+/mo",
                "link_to_review": True,
            },
            {
                "rank": 4,
                "name": "Evaboot",
                "slug": None,
                "category_tag": "Sales Navigator Export",
                "best_for": "Sales Navigator users who need clean data exports with verified emails",
                "why_picked": "Evaboot does one thing well: export Sales Navigator search results with clean data and verified emails. It strips the noise from LinkedIn exports (fake profiles, job seekers, duplicates) and enriches with email addresses. The Chrome extension approach is simpler than PhantomBuster's Phantom architecture. For GTM Engineers who already pay for Sales Navigator and just need a clean export, Evaboot removes the manual copy-paste workflow. Limited to Sales Navigator only, so it won't help with regular LinkedIn scraping.",
                "pricing": "$29+/mo",
                "link_to_review": False,
            },
            {
                "rank": 5,
                "name": "Dripify",
                "slug": None,
                "category_tag": "LinkedIn Automation",
                "best_for": "Individual reps who want simple LinkedIn automation without technical setup",
                "why_picked": "Dripify is the simplest LinkedIn automation tool in this list. Set up a sequence (view profile, send connection request, follow-up message), pick your targets, and let it run. The analytics dashboard tracks acceptance rates and response rates per campaign. It works well for individual reps who don't need multi-account management or complex scraping workflows. The limitation: it runs from a cloud instance, which means LinkedIn can detect non-human browsing patterns more easily than browser-based tools.",
                "pricing": "$39+/mo",
                "link_to_review": False,
            },
            {
                "rank": 6,
                "name": "Captain Data",
                "slug": None,
                "category_tag": "Data Orchestration",
                "best_for": "GTM teams building multi-step workflows that combine LinkedIn with other data sources",
                "why_picked": "Captain Data positions itself as a data orchestration platform rather than just a LinkedIn scraper. You can chain LinkedIn extraction with CRM enrichment, email finding, and custom API calls in visual workflows. The platform connects to 30+ data sources. For GTM Engineers building complex pipelines that start with LinkedIn data and flow through enrichment and into CRM, Captain Data reduces the number of tools in the stack. The $399/month starting price limits it to teams that can justify the investment.",
                "pricing": "$399+/mo",
                "link_to_review": False,
            },
        ],

        "verdict": """<h2>The Verdict</h2>
<p>PhantomBuster is the most versatile LinkedIn scraping tool for GTM Engineers. The breadth of pre-built Phantoms, proxy support, and scheduling flexibility make it the default choice. HeyReach is the pick for teams that need multi-account distribution. Evaboot is the simplest option for Sales Navigator exports.</p>
<p>A warning on all LinkedIn automation: these tools operate in violation of LinkedIn's Terms of Service. Account restrictions are a real risk, especially for profiles with limited connection history. Use dedicated LinkedIn accounts for automation, implement conservative rate limits, and assume any automated account could get restricted.</p>""",

        "faq": [
            ("Is LinkedIn scraping legal?",
             "It's a gray area. The 2022 hiQ Labs v. LinkedIn ruling established that scraping publicly available data isn't a violation of the Computer Fraud and Abuse Act. However, LinkedIn's Terms of Service prohibit automated scraping, and they actively enforce restrictions on accounts caught using automation. Using these tools won't land you in legal trouble, but LinkedIn can and does restrict accounts."),
            ("Which LinkedIn scraping tool is safest for my account?",
             "Browser-based tools (Evaboot, Waalaxy) are generally safer than cloud-based tools (Dripify) because they mimic human browsing patterns more naturally. PhantomBuster with proxy integration falls in the middle. No tool is completely safe. The best protection: use a dedicated LinkedIn account, keep daily actions under 50 connection requests, and use residential proxies instead of data center IPs."),
            ("Can I use PhantomBuster and HeyReach together?",
             "Yes, and some GTM Engineers do. PhantomBuster for data extraction (scraping search results, pulling profile data) and HeyReach for outreach (connection requests, messaging sequences). This keeps your scraping activity separate from your outreach activity, reducing risk on both fronts. The combined cost runs $130+/month."),
            ("How many LinkedIn connection requests can I send per day without getting restricted?",
             "LinkedIn's current limit is roughly 100 connection requests per week for established accounts, fewer for newer profiles. Most automation tools recommend 20-30 per day maximum. Exceeding 50/day consistently will trigger a restriction. Note-based connection requests (where you include a personalized message) have slightly higher acceptance rates but count toward the same limits."),
        ],
    },
}
