from types import SimpleNamespace

import pytest

from concrete_motivation.brand_profile import load_brand_profile
from concrete_motivation.bot_registry import get_bot
from concrete_motivation.providers.base import ProviderError
from concrete_motivation.providers.openai_provider import OpenAIProvider, build_prompt, parse_markdown_sections


def test_openai_prompt_includes_brand_goal_sections_and_personalization():
    bot = get_bot("motivational_speech")
    profile = load_brand_profile()

    prompt = build_prompt(
        bot,
        "starting from the bottom",
        "for fathers building a legacy",
        profile,
    )

    assert bot.name in prompt
    assert bot.purpose in prompt
    assert "starting from the bottom" in prompt
    assert "for fathers building a legacy" in prompt
    assert "Concrete Motivation Brand Profile" in prompt
    assert "Jaytee Miller" in prompt
    assert "Opening hook" in prompt
    assert "Concrete Motivation Angle" in prompt
    assert "Do not imitate public speakers" in prompt


def test_openai_provider_uses_mock_client_and_parses_sections():
    bot = get_bot("brand_architect")
    profile = load_brand_profile()
    markdown = """# Brand Architect Bot
**Goal:** build trust

## Brand message
Message body.

## Audience
Audience body.

## Tone
Tone body.

## Offer idea
Offer body.

## Next action
Action body.

## Concrete Motivation Angle
Brand angle body.
"""

    class FakeResponses:
        def create(self, **_kwargs):
            return SimpleNamespace(output_text=markdown)

    class FakeClient:
        responses = FakeResponses()

    provider = OpenAIProvider("test-key", client_factory=lambda **_kwargs: FakeClient())
    response = provider.generate(bot, "build trust", "", profile)

    assert response.provider_name == "openai"
    assert response.sections[-1] == ("Concrete Motivation Angle", "Brand angle body.")
    assert tuple(heading for heading, _ in response.sections) == bot.sections + ("Concrete Motivation Angle",)


def test_openai_parse_requires_expected_sections():
    with pytest.raises(ProviderError, match="missing sections"):
        parse_markdown_sections("## Only One\nBody", ("Only One", "Missing"))
