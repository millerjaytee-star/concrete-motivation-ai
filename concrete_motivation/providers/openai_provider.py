"""Optional OpenAI-powered generation provider."""

from collections.abc import Callable

from concrete_motivation.brand_profile import BrandProfile
from concrete_motivation.models import Bot, BotResponse
from concrete_motivation.providers.base import ProviderError
from concrete_motivation.providers.offline_provider import ANGLE_SECTION

DEFAULT_MODEL = "gpt-4.1-mini"


class OpenAIProvider:
    """Generate structured bot responses with the OpenAI API."""

    name = "openai"

    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        client_factory: Callable[..., object] | None = None,
    ) -> None:
        if not api_key:
            raise ProviderError("OPENAI_API_KEY is required for OpenAI mode.")
        self.api_key = api_key
        self.model = model
        self._client_factory = client_factory

    def generate(
        self,
        bot: Bot,
        goal: str,
        personalization_detail: str,
        brand_profile: BrandProfile,
    ) -> BotResponse:
        prompt = build_prompt(bot, goal, personalization_detail, brand_profile)
        try:
            content = self._create_content(prompt)
        except Exception as exc:  # pragma: no cover - exact SDK exceptions vary by version.
            raise ProviderError("OpenAI generation failed.") from exc
        sections = parse_markdown_sections(content, bot.sections + (ANGLE_SECTION,))
        return BotResponse(bot.name, goal, sections, provider_name=self.name)

    def _create_content(self, prompt: str) -> str:
        client = self._client()
        response = client.responses.create(
            model=self.model,
            input=prompt,
            temperature=0.7,
        )
        content = getattr(response, "output_text", "")
        if not isinstance(content, str) or not content.strip():
            raise ProviderError("OpenAI returned an empty response.")
        return content.strip()

    def _client(self) -> object:
        if self._client_factory is not None:
            return self._client_factory(api_key=self.api_key)
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - exercised when dependency is absent.
            raise ProviderError("The openai package is required for OpenAI mode.") from exc
        return OpenAI(api_key=self.api_key)


def build_prompt(
    bot: Bot,
    goal: str,
    personalization_detail: str,
    brand_profile: BrandProfile,
) -> str:
    """Build the instruction prompt sent to OpenAI."""
    required_sections = "\n".join(f"- {section}" for section in bot.sections + (ANGLE_SECTION,))
    detail = personalization_detail or "No extra personalization detail was provided."
    return f"""You are generating for Concrete Motivation AI.

Bot name: {bot.name}
Bot purpose: {bot.purpose}

User goal:
{goal}

Optional personalization detail:
{detail}

Required output sections:
{required_sections}

Concrete Motivation brand profile:
{brand_profile.source_text}

Instructions:
- Keep the voice original. Do not imitate public speakers.
- Sound direct, disciplined, real, spiritual but not forced, leadership-driven, family-centered, and comeback-minded.
- Avoid generic motivational fluff, fake luxury talk, unsupported scripture quotes, and empty hype.
- Produce structured Markdown only.
- Start with "# {bot.name}" and "**Goal:** {goal}".
- Use each required section as an exact "##" heading.
- Include "## {ANGLE_SECTION}" and explain how the output connects to Concrete Motivation, Jaytee Miller, Concrete Conversations, family, legacy, discipline, faith-aware action, and the user's personalization detail.
"""


def parse_markdown_sections(markdown: str, expected_sections: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    """Extract required level-two Markdown sections from provider output."""
    found: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            heading = line.removeprefix("## ").strip()
            current = heading if heading in expected_sections else None
            if current:
                found[current] = []
            continue
        if current:
            found[current].append(line)

    sections: list[tuple[str, str]] = []
    missing: list[str] = []
    for heading in expected_sections:
        body = "\n".join(found.get(heading, [])).strip()
        if not body:
            missing.append(heading)
        else:
            sections.append((heading, body))
    if missing:
        raise ProviderError(f"OpenAI response was missing sections: {', '.join(missing)}.")
    return tuple(sections)
