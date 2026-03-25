import os, logging, requests
from datetime import datetime, timezone

logger = logging.getLogger("aonxi.router.airtable")
KEY = os.getenv("AIRTABLE_API_KEY", "")
BASE = os.getenv("AIRTABLE_BASE_ID", "")
TABLE = "Router_Log"


def log_routing_decision(prompt_preview, cluster, model, confidence,
                         cost_estimate, agent, latency_ms):
    if not KEY or not BASE:
        return
    try:
        requests.post(
            f"https://api.airtable.com/v0/{BASE}/{TABLE}",
            headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
            json={"fields": {"prompt_preview": prompt_preview, "cluster": cluster,
                             "model": model, "confidence": round(confidence, 3),
                             "cost_estimate_usd": round(cost_estimate, 7),
                             "agent": agent, "latency_ms": latency_ms,
                             "logged_at": datetime.now(timezone.utc).isoformat()}},
            timeout=5)
    except Exception as e:
        logger.debug("Airtable log failed (non-fatal): %s", e)


def get_stats() -> dict:
    if not KEY or not BASE:
        return {}
    try:
        r = requests.get(
            f"https://api.airtable.com/v0/{BASE}/{TABLE}",
            headers={"Authorization": f"Bearer {KEY}"},
            params={"maxRecords": 1000, "fields[]": ["cluster", "model",
                    "cost_estimate_usd", "agent", "confidence"]},
            timeout=10)
        records = r.json().get("records", [])
        total = sum(x["fields"].get("cost_estimate_usd", 0) for x in records)
        baseline = len(records) * 0.0015
        cd, md = {}, {}
        for x in records:
            c = x["fields"].get("cluster", "?")
            m = x["fields"].get("model", "?")
            cd[c] = cd.get(c, 0) + 1
            md[m] = md.get(m, 0) + 1
        return {
            "total_calls": len(records),
            "total_cost_usd": round(total, 4),
            "sonnet_baseline_usd": round(baseline, 4),
            "savings_usd": round(baseline - total, 4),
            "savings_pct": round((baseline - total) / baseline * 100 if baseline else 0, 1),
            "cluster_distribution": cd,
            "model_distribution": md,
            "v2_status": f"{len(records)}/500 — {'RUN tools/build_v2_classifier.py NOW' if len(records)>=500 else 'collecting...'}",
        }
    except Exception as e:
        return {"error": str(e)}
