"""
Unified clients for all 4 providers.
All return: {"text": str, "model": str, "provider": str, "tokens_used": int}
Graceful fallback if any key is missing.
"""

import os
import logging
import requests

logger = logging.getLogger("aonxi.router.clients")


def call_model(model_id: str, prompt: str, system: str = "",
               max_tokens: int = 500, context: dict = None) -> dict:
    if model_id.startswith("gemini"):
        return _gemini(model_id, prompt, system, max_tokens)
    elif model_id.startswith("grok"):
        return _grok(model_id, prompt, system, max_tokens)
    elif model_id.startswith("kimi"):
        return _kimi(model_id, prompt, system, max_tokens)
    elif model_id.startswith("gpt"):
        return _openai(model_id, prompt, system, max_tokens)
    else:
        return _claude(model_id, prompt, system, max_tokens)


def _claude(model_id, prompt, system, max_tokens):
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return {"text": "[NO ANTHROPIC_API_KEY]", "model": model_id, "provider": "anthropic", "tokens_used": 0}
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model=model_id, max_tokens=max_tokens,
            system=system or "You are a helpful assistant.",
            messages=[{"role": "user", "content": prompt}],
        )
        return {"text": resp.content[0].text, "model": model_id,
                "provider": "anthropic", "tokens_used": resp.usage.input_tokens + resp.usage.output_tokens}
    except Exception as e:
        logger.error("Claude error: %s", e)
        return {"text": f"[Claude error: {e}]", "model": model_id, "provider": "anthropic", "tokens_used": 0}


def _gemini(model_id, prompt, system, max_tokens):
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        logger.warning("No GEMINI_API_KEY — falling back to claude-haiku")
        return _claude("claude-haiku-4-5-20251001", prompt, system, max_tokens)
    try:
        gm = "gemini-2.0-flash-lite"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{gm}:generateContent"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_tokens},
        }
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        r = requests.post(url, params={"key": key}, json=payload,
                          headers={"Content-Type": "application/json"}, timeout=30)
        r.raise_for_status()
        d = r.json()
        text = d["candidates"][0]["content"]["parts"][0]["text"]
        tokens = d.get("usageMetadata", {}).get("totalTokenCount", 0)
        return {"text": text, "model": gm, "provider": "google", "tokens_used": tokens}
    except Exception as e:
        logger.error("Gemini error: %s — falling back to claude-haiku", e)
        return _claude("claude-haiku-4-5-20251001", prompt, system, max_tokens)


def _grok(model_id, prompt, system, max_tokens):
    key = os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")
    if not key:
        logger.warning("No GROK_API_KEY — falling back to claude-haiku")
        return _claude("claude-haiku-4-5-20251001", prompt, system, max_tokens)
    try:
        gm = "grok-3-fast"
        r = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": gm, "max_tokens": max_tokens, "temperature": 0.1,
                  "messages": [{"role": "system", "content": system or "You are a helpful assistant."},
                                {"role": "user", "content": prompt}]},
            timeout=30)
        r.raise_for_status()
        d = r.json()
        return {"text": d["choices"][0]["message"]["content"], "model": gm,
                "provider": "xai", "tokens_used": d.get("usage", {}).get("total_tokens", 0)}
    except Exception as e:
        logger.error("Grok error: %s — falling back to claude-haiku", e)
        return _claude("claude-haiku-4-5-20251001", prompt, system, max_tokens)


def _kimi(model_id, prompt, system, max_tokens):
    key = os.getenv("KIMI_API_KEY") or os.getenv("MOONSHOT_API_KEY")
    if not key:
        logger.warning("No KIMI_API_KEY — falling back to claude-sonnet")
        return _claude("claude-sonnet-4-6", prompt, system, max_tokens)
    try:
        km = "kimi-k2-0711-preview"
        r = requests.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": km, "max_tokens": max_tokens, "temperature": 0.1,
                  "messages": [{"role": "system", "content": system or "You are a research assistant."},
                                {"role": "user", "content": prompt}]},
            timeout=90)
        r.raise_for_status()
        d = r.json()
        return {"text": d["choices"][0]["message"]["content"], "model": km,
                "provider": "moonshot", "tokens_used": d.get("usage", {}).get("total_tokens", 0)}
    except Exception as e:
        logger.error("Kimi error: %s — falling back to claude-sonnet", e)
        return _claude("claude-sonnet-4-6", prompt, system, max_tokens)


def _openai(model_id, prompt, system, max_tokens):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        logger.warning("No OPENAI_API_KEY — falling back to claude-sonnet")
        return _claude("claude-sonnet-4-6", prompt, system, max_tokens)
    try:
        om = "gpt-4o"
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": om, "max_tokens": max_tokens,
                  "messages": [{"role": "system", "content": system or "You are a helpful assistant."},
                                {"role": "user", "content": prompt}]},
            timeout=30)
        r.raise_for_status()
        d = r.json()
        return {"text": d["choices"][0]["message"]["content"], "model": om,
                "provider": "openai", "tokens_used": d.get("usage", {}).get("total_tokens", 0)}
    except Exception as e:
        logger.error("OpenAI error: %s — falling back to claude-sonnet", e)
        return _claude("claude-sonnet-4-6", prompt, system, max_tokens)
