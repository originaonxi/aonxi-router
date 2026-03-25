# Aonxi Router — The Intelligence Layer

> From AI to AGI: every prompt routed to the best model on earth for that exact task.
> The shared brain that makes AROS, ARIA, and the Aonxi Outreach Agent 10x better — permanently.

Based on **FineRouter** — Scalable Prompt Routing via Fine-Grained Latent Task Discovery
arxiv: 2603.19415

---

## The problem

AROS collected $199K. ARIA booked investor meetings. Both were calling Claude Sonnet for every single task — PKM classification, reply sorting, signal scoring, competitor research, content writing.

That's like a hospital where every patient from a paper cut to open-heart surgery sees the same neurosurgeon.

Five of ten tasks don't need Sonnet. Two tasks (capital research, competitor crawling) need a model that runs 300 sequential tool calls without losing coherence — something Claude cannot do. One task (X/Twitter signals) requires real-time social data that no model except Grok has.

The router fixes all of this permanently.

---

## The three cores this serves

| Agent | What it does | Router impact |
|-------|-------------|---------------|
| **AROS** | Finds new revenue. $199K collected, $0.50/day, 0 sales reps. | PKM accuracy +15pp. X signals 24-48h faster. 43x cheaper scoring. |
| **ARIA** | Finds capital. $250K pre-seed raise in progress. | Capital research transforms from 3-source scrape to 300-tool-call deep synthesis via Kimi K2.5. |
| **Outreach Agent** | Multi-channel, multi-vertical outreach. | All classification tasks routed to Gemini Flash Lite. Content to Claude Sonnet. Full multi-model stack. |

---

## The model matrix (real 2026 benchmark data)

| Task | Model | Accuracy | Cost/1M input | Why |
|------|-------|----------|--------------|-----|
| PKM defense classification | Gemini 3.1 Flash Lite | **85%** | $0.155 | Claude Haiku scores 70%. Better AND 2x cheaper. |
| Reply classification | Gemini 3.1 Flash Lite | **85%** | $0.155 | Same. Pure classification. |
| X/Twitter signal detection | Grok 4.1 Fast | Unique | $0.20 | **ONLY model with real-time X data.** 24-48h ahead of every other signal source. |
| Signal scoring | Grok 4.1 Fast | Sufficient | $0.20 | 43x cheaper than Claude Opus for structured scoring. |
| Summarization | Grok 4.1 Fast | Sufficient | $0.20 | Fast, cheap, accurate enough. |
| ARIA capital research | Kimi K2.5 Thinking | 78.4% BrowseComp | $0.60 | 300+ stable tool calls. Claude fails at 20. FinGPT built on Kimi. |
| Competitor web research | Kimi K2.5 Thinking | 78.4% BrowseComp | $0.60 | Same — sustained multi-step web intelligence. |
| Outreach generation | Claude Sonnet 4.6 | Best in class | $3.00 | Leads GDPval-AA Elo at 1633 pts. Revenue-critical. Never downgrade. |
| Objection handling | Claude Sonnet 4.6 | Best in class | $3.00 | Deal closure. GPT-4o for >10-step chains. |
| LLM content generation | Claude Sonnet 4.6 | Best in class | $3.00 | Content quality = LLM search presence. Compound effect. |

**Blended cost after routing: $0.76/M input vs $3.00/M all-Sonnet = 75% reduction.**

---

## New capability that didn't exist before

Grok's real-time X data is not a cost optimization. It is a capability AROS literally cannot have any other way.

A founder posts on X at 9pm: *"just closed our Series A, now I need to find an office fast"*
Without Grok: AROS sees this Thursday when Inc42 publishes the news.
With Grok: AROS contacts them at 9:05pm Tuesday. First mover.

Kimi K2.5 running ARIA's capital research is not a cost optimization either. It is a qualitative leap. Claude Sonnet loses coherence at ~20 sequential tool calls. Kimi K2.5 runs to 300+ without drift. ARIA's investor research goes from scraping 3 sources to parallel synthesis across the entire VC landscape.

---

## Usage — 2 line change in any agent
```python
# Before (in AROS, ARIA, Outreach Agent):
from anthropic import Anthropic
client = Anthropic()
resp = client.messages.create(model="claude-sonnet-4-6", ...)
text = resp.content[0].text

# After:
from router.client import RoutedClient
client = RoutedClient(agent="AROS")
resp = client.messages_create(prompt=..., system=..., task_context={})
text = resp["text"]
# Model auto-selected. Cost logged to Airtable. Zero other changes.
```
```python
# Direct routing check:
from router import route
r = route("Classify PKM defense mode for this VC", agent="ARIA")
print(r.model)           # gemini-flash-lite
print(r.task_cluster)    # PKM_CLASSIFICATION
print(r.estimated_cost_usd)  # 0.0000024

# Route and execute in one call:
from router import route_and_call
result = route_and_call(
    "Search X for founders posting about needing office space today",
    agent="AROS",
    context={"x_search": True}
)
# → Grok 4.1 Fast, real-time X data, $0.000020
```

---

## The v2 roadmap — AI to AGI

v1 is keyword matching. It works. It gets you 75% cost reduction and the Grok/Kimi capabilities.

v2 is the paper itself — FineRouter Stage 1 auto-discovery:

1. **Collect** 500+ real prompts from AROS + ARIA + Outreach production (tracked automatically in Airtable Router_Log)
2. **Embed** all prompts via `text-embedding-3-small`
3. **Build** cosine similarity graph (edge threshold: 0.85)
4. **Run** Louvain community detection → auto-discover task clusters humans didn't name
5. **Train** lightweight BERT classifier on discovered clusters
6. **Replace** `classifier.py` with the trained model

Real usage always reveals task boundaries that intuition misses. The paper found this in every domain tested. When Router_Log hits 500 records, run:
```bash
python3 tools/build_v2_classifier.py
```

This is the transition from AI routing to AGI routing — the system discovers its own cognitive structure from real behavior, not human assumptions.

---

## The compound effect

Every routing decision logged to Airtable is training data for v2.
Every v2 improvement makes all three agents more accurate.
Every accuracy improvement means more correct outreach.
More correct outreach means more revenue and more capital.
More data means a better router.
The loop never stops.

This is what makes AROS and ARIA permanently better — not a feature, a compounding organism.

---

## Integration
```bash
# Add to AROS:
git submodule add https://github.com/originaonxi/aonxi-router router

# Add to ARIA:
git submodule add https://github.com/originaonxi/aonxi-router router

# Add to Outreach Agent:
git submodule add https://github.com/originaonxi/aonxi-router router
```

Then replace `from anthropic import Anthropic` with `from router.client import RoutedClient` in each agent's core files. That's the entire integration.

---

## API keys (get these in parallel — all free tiers available)

| Key | Where | Cost | Used for |
|-----|-------|------|---------|
| `ANTHROPIC_API_KEY` | console.anthropic.com | ~$50/mo | Outreach, content, objections |
| `GEMINI_API_KEY` | aistudio.google.com | **Free tier** | PKM + reply classification |
| `GROK_API_KEY` | console.x.ai | ~$5/mo | X signals, scoring, summaries |
| `KIMI_API_KEY` | platform.moonshot.cn | ~$20/mo | ARIA research, competitor crawling |
| `OPENAI_API_KEY` | platform.openai.com | Optional | Complex negotiation >10 steps |

---

## Part of the Aonxi AGI stack

- [AROS](https://github.com/originaonxi/aros-agent) — revenue intelligence core
- [ARIA](https://github.com/originaonxi/ARIA) — capital intelligence core
- [Aonxi Outreach Agent](https://github.com/originaonxi/aonxi-outreach-agent) — multi-vertical outreach
- [PKM Analyzer](https://github.com/originaonxi/pkm-analyzer) — public defense profiling tool
- **aonxi-router** — the intelligence layer that makes all of them better

Every agent. Every task. Best model. Every time.
