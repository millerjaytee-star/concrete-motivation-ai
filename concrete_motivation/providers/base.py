"""Shared provider interfaces."""

from typing import Protocol

from concrete_motivation.brand_profile import BrandProfile
from concrete_motivation.models import Bot, BotResponse


class ProviderError(RuntimeError):
    """Raised when a configured provider cannot produce a valid response."""


class BotProvider(Protocol):
    """A generation provider for one Concrete Motivation bot response."""

    name: str

    def generate(
        self,
        bot: Bot,
        goal: str,
        personalization_detail: str,
        brand_profile: BrandProfile,
    ) -> BotResponse:
        """Generate a structured bot response."""
