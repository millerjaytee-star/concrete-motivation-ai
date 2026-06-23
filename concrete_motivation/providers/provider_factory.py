"""Provider selection for Concrete Motivation AI."""

import os
from collections.abc import Mapping

from concrete_motivation.providers.base import BotProvider
from concrete_motivation.providers.offline_provider import OfflineProvider
from concrete_motivation.providers.openai_provider import OpenAIProvider

SUPPORTED_PROVIDERS = {"offline", "openai"}


def provider_name_from_env(env: Mapping[str, str] | None = None) -> str:
    """Return the configured provider name, defaulting safely to offline."""
    values = env or os.environ
    configured = values.get("CONCRETE_AI_PROVIDER", "offline").strip().lower()
    return configured if configured in SUPPORTED_PROVIDERS else "offline"


def create_provider(env: Mapping[str, str] | None = None) -> BotProvider:
    """Create the configured provider, falling back to offline when OpenAI is not ready."""
    values = env or os.environ
    provider_name = provider_name_from_env(values)
    if provider_name != "openai":
        return OfflineProvider()

    api_key = values.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return OfflineProvider()
    return OpenAIProvider(api_key=api_key)
