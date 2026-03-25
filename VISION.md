# From AI to AGI — The Aonxi Router Vision

## What we are building

The Aonxi stack has three permanent intelligence cores:

**AROS** finds new revenue for 400 million businesses that cannot afford enterprise GTM.
**ARIA** finds capital for those same businesses when they need to grow.
**Outreach Agent** orchestrates every channel — email, WhatsApp, LinkedIn, SMS, ads — with approvals.

All three get smarter every day. All three share one brain — Airtable.
All three route through this repo.

## Why a router is the difference between AI and AGI

An AI system is smart. It does tasks well.
An AGI system is adaptive. It knows which cognitive resource to activate for which problem.

Right now, all three agents call one model for everything. That is AI — capable but uniform.

The router gives the stack a triage brain. Before any task executes, the system asks:
*What kind of problem is this, and which intelligence is best equipped to solve it?*

That question — and the ability to answer it from real data, not assumptions — is what separates AI from AGI.

## The compound loop

Every routing decision is recorded in Airtable.
When 500 records accumulate, the v2 classifier trains on real production behavior.
The v2 classifier discovers task boundaries humans did not name.
The system gets more accurate at routing.
More accurate routing means better outreach.
Better outreach means more revenue and capital.
More usage means more data.
More data means a better router.

The loop does not stop. The system never stops improving.
Every customer AROS wins makes the next outreach better.
Every investor ARIA contacts trains the next pitch.
Every routing decision improves the next one.

This is not a feature. This is a compounding organism.

## The ROI math

At 200 leads/day for AROS:
- PKM classification: 200 x $0.000155 vs 200 x $0.00025 = $0.031 vs $0.05 per day
- At 85% vs 70% accuracy: 30 more leads correctly profiled daily
- At even 5% conversion on correct profiling: 1.5 more closes per day
- At $999/month: $1,498/day in additional ARR potential

The router pays for itself in the first day of production.
The accuracy improvement compounds every month as the PKM cache grows.

## The v2 trigger

When Router_Log in Airtable hits 500 records:
```bash
python3 tools/build_v2_classifier.py
```

This runs the full FineRouter Stage 1 pipeline:
1. Embed all prompts via `text-embedding-3-small`
2. Build cosine similarity graph
3. Run Louvain community detection
4. Auto-discover task clusters from real behavior
5. Train BERT classifier
6. Deploy — replaces keyword matching with learned intelligence

The system will discover clusters we did not define.
Patterns in how AROS, ARIA, and Outreach Agent actually use AI.
Those patterns, once learned, make every future routing decision smarter.

That is the transition from AI to AGI.
