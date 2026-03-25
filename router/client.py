"""
Drop-in replacement for Anthropic() in AROS, ARIA, and Outreach Agent.

BEFORE (in any agent):
    from anthropic import Anthropic
    client = Anthropic()
    resp = client.messages.create(model="claude-sonnet-4-6", ...)
    text = resp.content[0].text

AFTER (2 line change, zero other changes):
    from router.client import RoutedClient
    client = RoutedClient(agent="AROS")
    resp = client.messages_create(prompt=..., system=..., task_context={...})
    text = resp["text"]

That's it. Model is auto-selected. Cost is logged. Everything else works the same.
"""
import logging
from typing import Optional
from .router import route
from .model_clients import call_model
from .task_clusters import TASK_CLUSTERS

logger = logging.getLogger("aonxi.router.client")


class RoutedClient:
    def __init__(self, agent: str = "AROS", dry_run: bool = False):
        self.agent = agent
        self.dry_run = dry_run

    def messages_create(self, prompt: str, system: str = "",
                        task_context: Optional[dict] = None,
                        force_cluster: Optional[str] = None,
                        max_tokens: Optional[int] = None) -> dict:
        r = route(prompt, self.agent, task_context or {}, force_cluster, self.dry_run)
        logger.info("→ %s | %s | $%.6f", r.task_cluster, r.model, r.estimated_cost_usd)
        if self.dry_run:
            return {"text": f"[DRY RUN] {r.model} / {r.task_cluster}", "routing": r.__dict__}
        tok = max_tokens or TASK_CLUSTERS.get(r.task_cluster, {}).get("max_tokens", 500)
        resp = call_model(r.model, prompt, system, tok, task_context)
        resp["routing"] = r.__dict__
        return resp
