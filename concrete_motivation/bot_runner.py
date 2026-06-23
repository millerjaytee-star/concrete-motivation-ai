"""Safe bot response coordination across configured providers."""

from concrete_motivation.brand_profile import BrandProfile, load_brand_profile
from concrete_motivation.models import Bot, BotResponse
from concrete_motivation.providers.base import BotProvider, ProviderError
from concrete_motivation.providers.offline_provider import OfflineProvider
from concrete_motivation.providers.provider_factory import create_provider


class BotRunner:
    """Run registered bots with optional OpenAI generation and offline fallback."""

    def __init__(
        self,
        brand_profile: BrandProfile | None = None,
        provider: BotProvider | None = None,
        fallback_provider: BotProvider | None = None,
    ) -> None:
        self.brand_profile = brand_profile or load_brand_profile()
        self.provider = provider or create_provider()
        self.fallback_provider = fallback_provider or OfflineProvider()

    @property
    def provider_name(self) -> str:
        """Return the active primary provider name."""
        return self.provider.name

    def run(self, bot: Bot, goal: str, personalization_detail: str = "") -> BotResponse:
        clean_goal = " ".join(goal.split())
        if not clean_goal:
            raise ValueError("Goal cannot be empty.")
        clean_detail = " ".join(personalization_detail.split())

        try:
            return self.provider.generate(bot, clean_goal, clean_detail, self.brand_profile)
        except (ProviderError, OSError, ValueError):
            if self.provider.name == self.fallback_provider.name:
                raise
            response = self.fallback_provider.generate(bot, clean_goal, clean_detail, self.brand_profile)
            return BotResponse(
                response.bot_name,
                response.goal,
                response.sections,
                provider_name=response.provider_name,
                fallback_used=True,
            )
