"""
Core routing engine.
P(model|prompt) = P(model|task_cluster) × P(task_cluster|prompt)
"""
import os, time, logging
from dataclasses import dataclass
from typing import Optional
from .task_clusters import TASK_CLUSTERS
from .classifier import classify_prompt

logger = logging.getLogger("aonxi.router")

PROVIDER_MAP = {
    "gemini-flash-lite":       "google",
    "grok-4-fast":             "xai",
    "kimi-k2-thinking":        "moonshot",
    "claude-sonnet-4-6":       "anthropic",
    "claude-haiku-4-5-20251001": "anthropic",
    "gpt-4o":                  "openai",
}


@dataclass
class RoutingResult:
    model: str
    task_cluster: str
    confidence: float
    estimated_cost_usd: float
    quality_critical: bool
    routing_reason: str
    fallback_model: str
    provider: str


def route(prompt: str, agent: str = "AROS", context: Optional[dict] = None,
          force_cluster: Optional[str] = None, dry_run: bool = False) -> RoutingResult:
    start = time.time()
    if force_cluster and force_cluster in TASK_CLUSTERS:
        cluster_id, confidence = force_cluster, 1.0
    else:
        cluster_id, confidence = classify_prompt(prompt, context or {})

    cluster = TASK_CLUSTERS.get(cluster_id, TASK_CLUSTERS["OUTREACH_GENERATION"])
    model = cluster["optimal_model"]
    fallback = cluster["fallback_model"]
    cpm = cluster["cost_per_1m_input"]
    est_tokens = len(prompt.split()) * 1.3
    est_cost = (est_tokens / 1_000_000) * cpm + (cluster["max_tokens"] / 1_000_000) * cpm * 3

    result = RoutingResult(
        model=model, task_cluster=cluster_id, confidence=confidence,
        estimated_cost_usd=round(est_cost, 7), quality_critical=cluster["quality_critical"],
        routing_reason=f"{cluster_id} agent:{agent} conf:{confidence:.2f}",
        fallback_model=fallback, provider=PROVIDER_MAP.get(model, "anthropic"),
    )

    if not dry_run:
        try:
            from .airtable_logger import log_routing_decision
            log_routing_decision(
                prompt_preview=prompt[:100], cluster=cluster_id, model=model,
                confidence=confidence, cost_estimate=est_cost, agent=agent,
                latency_ms=int((time.time() - start) * 1000),
            )
        except Exception:
            pass

    logger.debug("→ %s | %s | $%.6f", cluster_id, model, est_cost)
    return result


def route_and_call(prompt: str, system: str = "", agent: str = "AROS",
                   context: Optional[dict] = None, force_cluster: Optional[str] = None,
                   max_tokens: Optional[int] = None) -> dict:
    from .model_clients import call_model
    r = route(prompt, agent, context, force_cluster)
    tok = max_tokens or TASK_CLUSTERS[r.task_cluster]["max_tokens"]
    resp = call_model(r.model, prompt, system, tok, context)
    return {**resp, "cluster": r.task_cluster, "cost_usd": r.estimated_cost_usd,
            "confidence": r.confidence, "provider": r.provider}


def get_routing_stats() -> dict:
    try:
        from .airtable_logger import get_stats
        return get_stats()
    except Exception:
        return {}
