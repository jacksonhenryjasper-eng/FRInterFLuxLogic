import os
from typing import Any, Dict

import httpx


class AIProviderError(RuntimeError):
    """Raised when a configured AI provider cannot answer a request."""


async def generate_response(prompt: str, user_email: str) -> Dict[str, Any]:
    provider = os.getenv("AI_PROVIDER", "demo").lower()

    if provider == "demo":
        return {
            "message": (
                f"AI Bridge received your request, {user_email}. "
                "Add AI_PROVIDER and AI_API_KEY to .env to enable a live provider."
            ),
            "provider": "demo",
        }

    api_key = os.getenv("AI_API_KEY")
    model = os.getenv("AI_MODEL")
    base_url = os.getenv("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    if not api_key or not model:
        raise AIProviderError(
            "AI_API_KEY and AI_MODEL are required when AI_PROVIDER is not demo."
        )

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{base_url}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()
            payload = response.json()
    except (httpx.HTTPError, ValueError) as error:
        raise AIProviderError("The configured AI provider could not answer.") from error

    try:
        message = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise AIProviderError("The AI provider returned an unexpected response.") from error

    return {"message": message, "provider": provider}
