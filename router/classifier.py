"""
Stage 1 classifier: prompt → task cluster.
v1: keyword + context matching (~80% accuracy, zero latency)
v2: graph-based auto-discovery (trigger at 500 Router_Log records)
"""
import logging
logger = logging.getLogger("aonxi.router.classifier")

KEYWORD_MAP = {
    "PKM_CLASSIFICATION": [
        "defense mode", "pkm", "classify", "psychological", "resistance",
        "profile", "defense pattern", "motive inference", "overload avoidance",
        "persuasion knowledge", "tactic recognition", "identity threat",
    ],
    "OUTREACH_GENERATION": [
        "write", "generate", "draft", "outreach", "whatsapp message", "email",
        "linkedin message", "opening line", "cold email", "investor email",
        "bypass", "message for", "follow up",
    ],
    "REPLY_CLASSIFICATION": [
        "classify reply", "this reply", "they replied", "responded with",
        "is this hot", "hot warm", "not now", "unsubscribe", "outcome",
        "what category", "classify this response", "classify this message",
        "reply:", "when can we talk", "sounds good", "send me the deck",
    ],
    "ARIA_CAPITAL_RESEARCH": [
        "investor", "vc fund", "portfolio", "thesis", "bessemer", "general catalyst",
        "antler", "blume", "kae capital", "lp network", "check size", "fund stage",
        "investment history", "backed", "raised from", "capital research",
    ],
    "ARIA_INVESTOR_SCORING": [
        "score investor", "rank investors", "thesis fit", "stage preference",
        "india exposure", "does this vc", "which investors", "fit for aonxi",
        "score bessemer", "score for aonxi", "pre-seed", "autonomous gtm",
    ],
    "X_SIGNAL_DETECTION": [
        "twitter", "tweet", "x.com", "posted on x", "real-time signal",
        "wfh reversal", "office hunting", "founder post x", "monitor x",
        "search x for", "x signal", "social signal x",
    ],
    "SIGNAL_SCORING": [
        "score signal", "scoring", "intent score", "urgency", "rank signals",
        "prioritize", "how urgent", "rate this signal", "icp fit score",
        "sector ltv", "confidence score", "workspace likelihood",
    ],
    "OBJECTION_HANDLING": [
        "objection", "too expensive", "not ready", "price is too high",
        "already using", "happy with", "reframe", "negotiate",
        "handle this objection", "respond to objection", "they said the price",
    ],
    "LLM_CONTENT_GENERATION": [
        "blog post", "article", "guide", "long form", "1000 word", "1200 word",
        "perplexity", "reddit post", "seo content", "comparison article",
        "write a guide", "llm indexed", "content for",
    ],
    "SUMMARIZATION": [
        "summarize", "summary", "extract", "key facts", "brief",
        "tldr", "main points", "daily brief", "compress this", "what does this say",
    ],
}


def classify_prompt(prompt: str, context: dict = {}) -> tuple:
    prompt_lower = prompt.lower()
    scores = {}
    for cluster_id, keywords in KEYWORD_MAP.items():
        hits = sum(1 for kw in keywords if kw in prompt_lower)
        if hits > 0:
            scores[cluster_id] = hits / len(keywords)
    if scores:
        best = max(scores, key=scores.get)
        return best, min(1.0, scores[best] * 12)
    # Context hints
    if context.get("defense_mode"):
        return "OUTREACH_GENERATION", 0.75
    if context.get("reply_text"):
        return "REPLY_CLASSIFICATION", 0.75
    if context.get("investor") or context.get("fund"):
        return "ARIA_CAPITAL_RESEARCH", 0.70
    if context.get("x_search"):
        return "X_SIGNAL_DETECTION", 0.80
    if context.get("signal"):
        return "SIGNAL_SCORING", 0.70
    # Length heuristic
    wc = len(prompt.split())
    if wc < 20:
        return "PKM_CLASSIFICATION", 0.50
    elif wc > 150:
        return "LLM_CONTENT_GENERATION", 0.50
    return "OUTREACH_GENERATION", 0.45
