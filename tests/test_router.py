import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from router.classifier import classify_prompt
from router.router import route

CASES = [
    ("Classify the PKM defense mode for this VC founder",          "PKM_CLASSIFICATION",      "gemini-flash-lite"),
    ("Write WhatsApp for funded founder MOTIVE_INFERENCE bypass",  "OUTREACH_GENERATION",     "claude-sonnet-4-6"),
    ("Classify reply: sounds good when can we talk",               "REPLY_CLASSIFICATION",    "gemini-flash-lite"),
    ("Research General Catalyst thesis Indian investments 2026",   "ARIA_CAPITAL_RESEARCH",   "kimi-k2-thinking"),
    ("Score Bessemer for Aonxi pre-seed 250K autonomous GTM",      "ARIA_INVESTOR_SCORING",   "grok-4-fast"),
    ("Search X for founders posting about needing office today",   "X_SIGNAL_DETECTION",      "grok-4-fast"),
    ("Score signal 5Cr seed round 23 employees SaaS Bengaluru",    "SIGNAL_SCORING",          "grok-4-fast"),
    ("Prospect says 999 per month too expensive reframe",          "OBJECTION_HANDLING",      "claude-sonnet-4-6"),
    ("Write 1200 word guide autonomous GTM for SMBs Perplexity",   "LLM_CONTENT_GENERATION",  "claude-sonnet-4-6"),
    ("Summarize Inc42 article Bengaluru startup Series B signals", "SUMMARIZATION",           "grok-4-fast"),
]

def run():
    print("=== AONXI ROUTER v2 — TEST SUITE ===\n")
    passed = failed = 0
    for prompt, exp_c, exp_m in CASES:
        r = route(prompt, dry_run=True)
        ok = r.task_cluster == exp_c and r.model == exp_m
        print(f"{'✓' if ok else '✗'} {prompt[:55]:55s}")
        if not ok:
            if r.task_cluster != exp_c:
                print(f"    cluster: expected {exp_c}, got {r.task_cluster}")
            if r.model != exp_m:
                print(f"    model:   expected {exp_m}, got {r.model}")
        passed += ok
        failed += not ok
    baseline = len(CASES) * 0.0015
    routed = sum(route(p, dry_run=True).estimated_cost_usd for p, _, _ in CASES)
    saving = (1 - routed / baseline) * 100
    print(f"\n{passed}/{len(CASES)} routing tests passed")
    print(f"Cost vs all-Sonnet: ${routed:.5f} vs ${baseline:.5f} = {saving:.0f}% savings")
    return failed == 0

if __name__ == "__main__":
    ok = run()
    exit(0 if ok else 1)
