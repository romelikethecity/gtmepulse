"""Alternatives content for LinkedIn & Social tools (LinkedIn Sales Navigator)."""

ALTERNATIVES = {
    "linkedin-sales-navigator": {
        "intro": """<p>LinkedIn Sales Navigator costs $99.99-$179.99/month per seat. For that, you get advanced search filters, lead recommendations, and InMail credits on a platform you're already using for free. The value proposition is essentially: pay LinkedIn to remove the limits LinkedIn created. Many GTM Engineers question whether the premium filters and InMail credits justify a $1,200-$2,160 annual investment per rep.</p>
<p>Sales Navigator frustrations go beyond pricing: InMail response rates have plummeted (under 3% in most campaigns), the search filters haven't meaningfully improved in years, the export restrictions prevent you from using the data in other tools without scraping (which violates ToS), and the mobile experience is mediocre. LinkedIn also restricts connection requests regardless of your subscription tier.</p>
<p>These alternatives either replicate Sales Navigator's data through different means or replace the prospecting workflow entirely. Some extract LinkedIn data programmatically. Others provide contact databases that make LinkedIn search unnecessary. The common thread: spending less money for similar or better prospecting outcomes.</p>""",

        "alternatives": [
            {
                "name": "Apollo.io",
                "slug": "apollo-review",
                "tagline": "275M+ contacts with emails and phones you can export",
                "best_for": "GTM teams that want Sales Navigator's search capabilities with actual data export and outbound tools",
                "pros": [
                    "275M+ contacts searchable by title, company, industry, and more",
                    "Email and phone data you can export (not locked behind LinkedIn)",
                    "Built-in sequencing eliminates needing separate outbound tools",
                    "Free tier with 10,000 email credits/month",
                ],
                "cons": [
                    "LinkedIn-specific data (connections, activity, group membership) isn't available",
                    "Data accuracy on smaller companies is inconsistent",
                    "No LinkedIn InMail or connection automation",
                ],
                "pricing": "Free tier. Paid $49-$149/mo per user",
                "verdict": "Apollo is the Sales Navigator replacement for teams that use LinkedIn mainly to find contacts. Instead of searching LinkedIn and manually noting emails, Apollo gives you the contact data directly with export. You lose LinkedIn-specific signals (who viewed your profile, shared connections), but you gain emails, phones, and outbound sequencing. For most prospecting workflows, Apollo makes Sales Navigator redundant.",
            },
            {
                "name": "Clay",
                "slug": "clay-review",
                "tagline": "Multi-source prospecting that includes LinkedIn data",
                "best_for": "GTM Engineers building automated prospecting workflows that pull from LinkedIn and 75+ other sources",
                "pros": [
                    "LinkedIn profile data as one of 75+ enrichment sources",
                    "Waterfall logic that falls back to other providers when LinkedIn data is incomplete",
                    "Automated research workflows that replace manual LinkedIn browsing",
                    "AI agent that reads profiles and extracts custom data points",
                ],
                "cons": [
                    "Steep learning curve for new users",
                    "Credit costs escalate at high volume",
                    "No direct LinkedIn messaging or connection automation",
                ],
                "pricing": "$149-$800/mo",
                "verdict": "Clay makes Sales Navigator unnecessary for prospecting research. Instead of manually browsing LinkedIn profiles, Clay pulls profile data programmatically and enriches it with data from dozens of other sources. You build the prospecting list once as a workflow, then run it on thousands of accounts. If your Sales Navigator workflow is 'search > read profile > note details,' Clay automates all of it.",
            },
            {
                "name": "PhantomBuster",
                "slug": "phantombuster-review",
                "tagline": "LinkedIn automation and data extraction at scale",
                "best_for": "Teams that want to extract LinkedIn search results, profile data, and connections programmatically",
                "pros": [
                    "Extract data from LinkedIn searches, profiles, and Sales Navigator lists",
                    "Automated connection requests and message sequences",
                    "100+ pre-built automation templates ('Phantoms')",
                    "Works with LinkedIn, Twitter, Instagram, and other platforms",
                ],
                "cons": [
                    "Scraping LinkedIn violates LinkedIn's ToS (account ban risk)",
                    "Credit-based pricing limits high-volume extraction",
                    "Requires careful rate-limiting to avoid detection",
                ],
                "pricing": "$69-$439/mo",
                "verdict": "PhantomBuster extracts the data that Sales Navigator shows you but won't let you export. Profile scraping, search result extraction, and automated outreach. The risk is real: LinkedIn actively detects scraping and will restrict or ban accounts. Use dedicated LinkedIn accounts, respect rate limits, and accept the risk. For teams willing to operate in this gray area, PhantomBuster provides data that would cost thousands in Sales Navigator seats.",
            },
            {
                "name": "HeyReach",
                "slug": "heyreach-review",
                "tagline": "Multi-account LinkedIn outreach automation",
                "best_for": "Teams that want to automate LinkedIn connection requests and messages across multiple profiles",
                "pros": [
                    "Distribute outreach across multiple LinkedIn accounts",
                    "Automated connection requests, follow-ups, and InMail",
                    "Campaign analytics for LinkedIn engagement",
                    "Growing integration library with CRM and outbound tools",
                ],
                "cons": [
                    "LinkedIn outreach automation carries account restriction risk",
                    "Newer platform with less mature features",
                    "No data extraction or enrichment (outreach only)",
                ],
                "pricing": "$79-$499/mo",
                "verdict": "HeyReach replaces Sales Navigator's InMail with automated connection requests at scale. Instead of paying $179/month for 50 InMail credits, HeyReach sends hundreds of connection requests across multiple profiles. The engagement rates on connection requests typically exceed InMail. The trade-off is LinkedIn account risk. If InMail is your primary Sales Navigator use case, HeyReach is more effective.",
            },
            {
                "name": "Lusha",
                "slug": "lusha-review",
                "tagline": "Chrome extension for instant LinkedIn contact data",
                "best_for": "Reps who browse LinkedIn manually and want contact details without switching to another platform",
                "pros": [
                    "One-click email and phone from any LinkedIn profile",
                    "Chrome extension overlays directly on LinkedIn",
                    "Free tier for testing (5 credits/month)",
                    "GDPR-compliant data sourcing",
                ],
                "cons": [
                    "Credit-based pricing limits volume",
                    "No automation or campaign features",
                    "Only useful if you're already browsing LinkedIn",
                ],
                "pricing": "Free (5 credits/mo). Paid from $49/mo",
                "verdict": "Lusha turns every LinkedIn profile into an actionable contact. If you use Sales Navigator mainly to find people and then scramble to find their email, Lusha gives you the email and phone right on the LinkedIn page. It doesn't replace Sales Navigator's search filters, but it extracts more value from the free LinkedIn experience. Pair Lusha with free LinkedIn search, and you might not need Sales Navigator at all.",
            },
            {
                "name": "LeadIQ",
                "slug": "leadiq-review",
                "tagline": "LinkedIn prospecting with one-click CRM sync",
                "best_for": "Sales teams that prospect on LinkedIn and need instant contact capture with CRM push",
                "pros": [
                    "Captures contacts from LinkedIn with one click",
                    "Direct push to Salesforce, HubSpot, and Outreach",
                    "AI-powered email personalization from LinkedIn profile data",
                    "Free tier available",
                ],
                "cons": [
                    "Phone number accuracy is inconsistent",
                    "Designed for individual reps, not automated workflows",
                    "Data coverage outside North America is weaker",
                ],
                "pricing": "Free tier. Paid $39-$89/mo per user",
                "verdict": "LeadIQ is the Sales Navigator companion that LinkedIn should have built. Browse LinkedIn, click to capture a contact, and it pushes directly to your CRM with enriched data. If your workflow is LinkedIn search > find contacts > add to CRM > sequence, LeadIQ compresses that to two clicks. Some teams use LeadIQ instead of Sales Navigator, since free LinkedIn + LeadIQ costs less than Sales Navigator alone.",
            },
        ],

        "faq": [
            ("Is Sales Navigator worth $100+/month?", "For account executives working named account lists with deal sizes above $25K, Sales Navigator's advanced filters and relationship mapping provide value. For SDRs and GTM Engineers doing high-volume prospecting, the money is better spent on Apollo (for data) or Instantly (for outbound). Sales Navigator's value drops every year as third-party databases improve."),
            ("What's the best free alternative to Sales Navigator?", "Apollo's free tier gives you 275M+ contacts with search filters that rival Sales Navigator, plus actual email and phone data. Free LinkedIn search with Lusha's free tier (5 credits/month) provides basic contact capture. Neither matches Sales Navigator's LinkedIn-specific features (shared connections, profile view tracking), but for pure prospecting, they're close."),
            ("Can I use Sales Navigator data in other tools?", "Not directly. LinkedIn restricts data export. You can manually copy contact data, use browser extensions (Lusha, LeadIQ) to capture enriched data from profiles, or use tools like PhantomBuster to extract search results (which violates LinkedIn's ToS). The export restriction is Sales Navigator's biggest limitation and the primary reason GTM Engineers prefer tools like Apollo where data is exportable by design."),
            ("Will I get banned for using LinkedIn automation?", "LinkedIn detects automated actions (mass connection requests, profile viewing, message sending) and will restrict or ban accounts. The risk is real. Mitigation: use dedicated LinkedIn accounts, stay under daily action limits (50-80 connections/day), randomize timing, and warm up accounts gradually. Even with precautions, account restrictions happen. Factor this into your decision."),
        ],
    },
}
