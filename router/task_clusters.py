"""
Task cluster definitions for the Aonxi AGI stack.

The three permanent cores:
  AROS    — Autonomous Revenue Operating System  ($199K collected, $0.50/day)
  ARIA    — Autonomous Relationship Intelligence  (investors, capital, relationships)
  OUTREACH — Aonxi Outreach Agent               (multi-vertical, multi-channel)

Everything else merges into these three forever.

Model selection based on real 2026 benchmark data:
  Classification tasks  → Gemini 3.1 Flash Lite  (85% acc, $0.155/M — beats Claude Haiku at 70%)
  X/Twitter signals     → Grok 4.1 Fast          (ONLY model with real-time X data, $0.20/M)
  Scoring/Summarization → Grok 4.1 Fast          (43x cheaper than Opus, sufficient accuracy)
  Deep research         → Kimi K2.5 Thinking     (78.4% BrowseComp, 300+ tool calls stable)
  Revenue generation    → Claude Sonnet 4.6      (leads GDPval-AA Elo — never downgrade)
  Complex negotiation   → Claude Sonnet 4.6      (GPT-4o fallback for >10 step chains)

FineRouter paper: P(model|prompt) = P(model|task_cluster) × P(task_cluster|prompt)
arxiv: 2603.19415
"""

TASK_CLUSTERS = {

    # ── SHARED ACROSS ALL 3 AGENTS ────────────────────────────────

    "PKM_CLASSIFICATION": {
        "description": "Classify prospect psychological defense mode from profile text.",
        "used_by": ["AROS", "ARIA", "OUTREACH"],
        "examples": [
            "Classify the defense mode for this VC who came out of Gong",
            "What PKM mode for home care owner getting 60 pitches a week",
            "Identify psychological resistance from this LinkedIn bio",
            "Defense mode for serial founder who pattern-matches templates instantly",
        ],
        "optimal_model": "gemini-flash-lite",
        "fallback_model": "claude-haiku-4-5-20251001",
        "max_tokens": 250,
        "quality_critical": False,
        "cost_per_1m_input": 0.155,
        "why": "Gemini Flash Lite 85% on OpenMark classification benchmark. Claude Haiku 70%. Better AND 2x cheaper. PKM is the most frequent task — this improvement compounds daily.",
        "impact_on_aros": "15% more leads classified correctly = 15% more correctly-targeted outreach = direct revenue",
        "impact_on_aria": "VC defense mode accuracy goes from 70% to 85% — fewer wasted emails to wrong persona",
    },

    "OUTREACH_GENERATION": {
        "description": "Write PKM-calibrated outreach: WhatsApp, email, LinkedIn, SMS.",
        "used_by": ["AROS", "ARIA", "OUTREACH"],
        "examples": [
            "Write WhatsApp for funded founder MOTIVE_INFERENCE defense PURE_DATA bypass",
            "Email to VC Series A investor running MOTIVE_INFERENCE — no pitch language",
            "LinkedIn message enterprise buyer SOCIAL_PROOF_SKEPTICISM mode",
            "SMS follow-up cleaning franchise owner OVERLOAD_AVOIDANCE 60 words max",
        ],
        "optimal_model": "claude-sonnet-4-6",
        "fallback_model": "claude-sonnet-4-6",
        "max_tokens": 600,
        "quality_critical": True,
        "cost_per_1m_input": 3.00,
        "why": "Claude Sonnet 4.6 leads GDPval-AA Elo at 1633 pts for office/professional work. This is the task that touches revenue directly. NEVER downgrade. Every dollar saved here costs ten in missed closes.",
        "impact_on_aros": "This IS the revenue. Quality of this message = quality of the close.",
        "impact_on_aria": "The investor email is ARIA's only weapon. Sonnet 4.6 is its best shot.",
    },

    "REPLY_CLASSIFICATION": {
        "description": "Classify inbound reply into outcome: HOT / OBJECTION / REFERRAL / NOT_NOW / UNSUBSCRIBE.",
        "used_by": ["AROS", "ARIA", "OUTREACH"],
        "examples": [
            "Classify: 'sounds good when can we talk' — HOT or WARM",
            "Is 'not right now maybe Q3' a NOT_NOW or TIMING_OBJECTION",
            "Classify investor reply: 'interesting send me the deck'",
            "Reply: 'we already use a different tool' — OBJECTION or UNSUBSCRIBE",
        ],
        "optimal_model": "gemini-flash-lite",
        "fallback_model": "claude-haiku-4-5-20251001",
        "max_tokens": 60,
        "quality_critical": False,
        "cost_per_1m_input": 0.155,
        "why": "Pure classification. Gemini Flash Lite 85% for $0.000155/run. Runs on EVERY inbound — this adds up fast at scale.",
        "impact_on_aros": "HOT reply triggers 5-min SDR alert. Misclassified HOT = missed close.",
        "impact_on_aria": "Investor reply classified correctly = ARIA knows to escalate vs move on.",
    },

    "SIGNAL_SCORING": {
        "description": "Score business signals: urgency, ICP fit, sector LTV, confidence.",
        "used_by": ["AROS", "OUTREACH"],
        "examples": [
            "Score: 5Cr seed round, 23 employees, SaaS, Bengaluru — workspace urgency",
            "Rank these 5 funding signals by home care expansion likelihood",
            "Intent score: MCA new subsidiary + Naukri hiring surge same company",
            "Prioritize: 14 signals across BLR and MUM this week",
        ],
        "optimal_model": "grok-4-fast",
        "fallback_model": "claude-haiku-4-5-20251001",
        "max_tokens": 200,
        "quality_critical": False,
        "cost_per_1m_input": 0.20,
        "why": "Grok 4.1 Fast $0.00007/query vs Claude Opus $0.003 = 43x cheaper. Structured scoring over numbers needs no frontier model.",
        "impact_on_aros": "Runs on every signal every day. 43x cost reduction compounds at scale.",
    },

    "X_SIGNAL_DETECTION": {
        "description": "Real-time X/Twitter signal detection. UNIQUE CAPABILITY — no other model has this.",
        "used_by": ["AROS", "OUTREACH"],
        "examples": [
            "Search X: founders posting about needing office space today",
            "Find tweets about WFH policy reversals Indian startups this week",
            "Monitor: Series A closed + office hunting signals X last 24h",
            "Detect: home care operators posting about expansion on X",
        ],
        "optimal_model": "grok-4-fast",
        "fallback_model": "grok-4-fast",
        "max_tokens": 800,
        "quality_critical": False,
        "cost_per_1m_input": 0.20,
        "why": "ONLY Grok has real-time X data. Claude/GPT/Gemini see X posts 24-48h later when they hit news. AROS can contact a founder 5 minutes after they post about needing office space. This capability does not exist without Grok.",
        "impact_on_aros": "Catches high-intent signals 24-48h before every competitor. First mover wins.",
        "impact_on_outreach": "New signal source across every vertical. Home care, cleaning, franchise — all post on X.",
    },

    "SUMMARIZATION": {
        "description": "Summarize news, profiles, signal batches, daily briefs.",
        "used_by": ["AROS", "ARIA", "OUTREACH"],
        "examples": [
            "Summarize Inc42 article Bengaluru startup Series B — key workspace signals",
            "Extract 3 thesis keywords from this VC fund page",
            "Daily brief: last 7 days of AROS signals across 5 cities",
            "Compress this 50-page investor deck into 200 words for ARIA context",
        ],
        "optimal_model": "grok-4-fast",
        "fallback_model": "claude-haiku-4-5-20251001",
        "max_tokens": 300,
        "quality_critical": False,
        "cost_per_1m_input": 0.20,
        "why": "Fast, cheap, accurate enough. Saves Claude Sonnet budget for revenue-generating tasks.",
    },

    "OBJECTION_HANDLING": {
        "description": "Autonomous negotiation responses to pricing, timing, or competitor objections.",
        "used_by": ["AROS", "ARIA", "OUTREACH"],
        "examples": [
            "Prospect says 999/month too expensive, reframe as cost per day",
            "Reply: we already use a competitor and are happy — IDENTITY_THREAT bypass",
            "Investor: your ARR is too low — reframe with trajectory not current number",
            "Handle: not ready yet — TIMING_SKEPTICISM bypass with specific trigger",
        ],
        "optimal_model": "claude-sonnet-4-6",
        "fallback_model": "claude-sonnet-4-6",
        "max_tokens": 500,
        "quality_critical": True,
        "cost_per_1m_input": 3.00,
        "why": "Deal closure. One well-handled objection = $999/month recurring. Claude Sonnet 4.6 for standard chains. GPT-4o upgrade for >10-step negotiation sequences.",
        "impact_on_aros": "90-day ROI guarantee depends on this. Objection handling is where deals are won or lost.",
        "impact_on_aria": "VC objection handling is ARIA's Gen 4 feature. Every reply moves the raise forward or kills it.",
    },

    # ── ARIA-SPECIFIC ─────────────────────────────────────────────

    "ARIA_CAPITAL_RESEARCH": {
        "description": "Deep multi-source investor research: thesis, portfolio, LP networks, fund patterns.",
        "used_by": ["ARIA"],
        "examples": [
            "Research General Catalyst thesis and all Indian B2B investments 2023-2026",
            "Map Bessemer portfolio companies autonomous GTM SaaS",
            "Find all angels who backed Indian revenue automation startups under $500K ARR",
            "Analyze Blume VC check size patterns from portfolio page and press releases",
            "Which LPs does Antler India share with Kae Capital",
        ],
        "optimal_model": "kimi-k2-thinking",
        "fallback_model": "claude-sonnet-4-6",
        "max_tokens": 3000,
        "quality_critical": True,
        "cost_per_1m_input": 0.60,
        "why": "Kimi K2.5 Thinking: 300+ sequential tool calls without coherence drift. FinGPT Agent built on Kimi. AlphaEngine uses it for financial analysis. ARIA's capital research is the same problem domain — multi-source deep synthesis. Claude Sonnet fails at 20 tool calls. Kimi runs to 300.",
        "impact_on_aria": "ARIA Gen 3 research goes from 'scrape 3 sources' to '100-agent parallel synthesis of entire VC landscape'. Transforms ARIA from a good email tool into a genuine intelligence system.",
    },

    "ARIA_INVESTOR_SCORING": {
        "description": "Score investor thesis fit, stage preference, India exposure, check size match.",
        "used_by": ["ARIA"],
        "examples": [
            "Score Bessemer for Aonxi: pre-seed $250K, autonomous GTM, India, 0 raised",
            "Rank these 20 investors by thesis fit for revenue automation SaaS",
            "Does General Catalyst invest pre-revenue pre-seed India",
            "Which of these 50 angels have backed autonomous sales tools",
        ],
        "optimal_model": "grok-4-fast",
        "fallback_model": "claude-haiku-4-5-20251001",
        "max_tokens": 300,
        "quality_critical": False,
        "cost_per_1m_input": 0.20,
        "why": "Structured scoring over structured data. Grok 4.1 Fast is accurate and 43x cheaper than Opus.",
        "impact_on_aria": "Runs on every investor in every CSV load. Cost compounds at scale.",
    },

    # ── OUTREACH AGENT SPECIFIC ───────────────────────────────────

    "LLM_CONTENT_GENERATION": {
        "description": "Long-form LLM-indexed content: guides, comparison posts, Reddit, Perplexity submissions.",
        "used_by": ["OUTREACH", "AROS"],
        "examples": [
            "1200-word guide: autonomous GTM for SMBs — how AI agents replace sales teams",
            "Reddit post r/Entrepreneur: we replaced our SDR team with an AI agent here is what happened",
            "FAQ content for Perplexity: best AI sales automation for home care businesses",
            "Comparison: AROS vs traditional outreach tools — real cost breakdown",
        ],
        "optimal_model": "claude-sonnet-4-6",
        "fallback_model": "claude-sonnet-4-6",
        "max_tokens": 2500,
        "quality_critical": True,
        "cost_per_1m_input": 3.00,
        "why": "Content quality determines whether AROS/ARIA show up in AI search. Claude Sonnet 4.6 leads professional writing benchmarks. This is presence at the inference layer.",
        "impact_on_outreach": "LLM-indexed content = warm leads before AROS contacts them. Compound effect.",
    },
}

# ── Cost impact summary ────────────────────────────────────────────
ROUTING_IMPACT = {
    "before": "All tasks → Claude Sonnet 4.6 → $3.00/M input",
    "after_blended_cost": "$0.76/M input (blended)",
    "cost_reduction_pct": 75,
    "accuracy_gains": {
        "PKM_CLASSIFICATION": "+15pp (Haiku 70% → Gemini 85%)",
        "REPLY_CLASSIFICATION": "+15pp same",
        "ARIA_CAPITAL_RESEARCH": "Qualitative leap — Claude fails at 20 tool calls, Kimi runs to 300",
    },
    "new_capabilities": [
        "X/Twitter real-time signals via Grok (impossible before this router)",
        "300-tool-call ARIA capital research via Kimi K2.5 (impossible on Claude)",
    ],
    "v2_trigger": "When Router_Log in Airtable hits 500 records, run tools/build_v2_classifier.py",
    "v2_method": "Embed all prompts → cosine similarity graph → Louvain clustering → BERT classifier",
}
