"""Offline structured response generation for every registered bot."""

from collections.abc import Callable

from concrete_motivation.brand_profile import BrandProfile
from concrete_motivation.models import Bot, BotResponse
from concrete_motivation.providers.base import ProviderError

SectionBuilder = Callable[[str], tuple[str, ...]]
ANGLE_SECTION = "Concrete Motivation Angle"


def _brand(goal: str) -> tuple[str, ...]:
    return (
        f"Concrete Motivation helps people turn pressure into purpose through disciplined action. This direction centers that promise on: {goal}.",
        "Primary: athletes, young men, families, leaders, and people rebuilding. Secondary: coaches, schools, teams, and values-led businesses.",
        "Direct, grounded, hopeful, leadership-driven, and faith-aware--never polished beyond real life.",
        f"Create a focused message-and-action workshop around \"{goal},\" with a takeaway plan participants can use the same day.",
        "Interview three people in the target audience, capture their exact challenges, and turn the strongest insight into a one-sentence campaign promise.",
    )


def _speech(goal: str) -> tuple[str, ...]:
    return (
        "Pressure Has a Purpose",
        f"You did not come this far just to let one hard chapter write the ending. Today we confront this: {goal}.",
        f"Pressure reveals what comfort can hide. When the result disappoints you, return to the work--not to punish yourself, but to rebuild trust with yourself. Let \"{goal}\" become a decision: name the lesson, choose the next disciplined move, and repeat it when nobody is watching. Faith does not remove the work; it gives the work direction. Your past can explain the weight you carry, but it does not get to command your next step. Stand up, tell the truth about where you are, and lay one honest brick today. A comeback is not one loud moment. It is a wall built from quiet promises kept.",
        "Call: \"What do we do with pressure?\" Response: \"We build with it!\"\nCall: \"When do we start?\" Response: \"Right now!\"",
        "Before today ends, write down one promise you will keep for the next seven days. Make it measurable. Tell one person. Then put the first brick in place.",
    )


def _podcast(goal: str) -> tuple[str, ...]:
    return (
        f"Concrete Conversations: The Truth About {goal.title()}",
        "Listeners will leave with a more honest definition of the challenge and a three-step way to move through it with purpose.",
        f"Welcome to Concrete Conversations--where real pressure becomes practical wisdom. Today we are getting honest about {goal}.",
        "1. The real-life tension and why it matters (8 min)\n2. The story behind the lesson (12 min)\n3. What discipline looks like in practice (12 min)\n4. The faith, family, or leadership dimension (8 min)\n5. Three actions for this week (5 min)",
        f"1. When did {goal} become personal for you?\n2. What did you misunderstand at first?\n3. Which habit made the biggest difference?\n4. How did pressure affect the people around you?\n5. What should someone do in the next 24 hours?",
        "\"Pressure is information, not identity.\"\n\"The comeback began when I stopped waiting to feel ready.\"\nA 30-second summary of the three-action framework.",
        "Choose one lesson from this conversation and live it before you share it. Subscribe, send this episode to someone rebuilding, and keep laying the next brick.",
    )


def _social(goal: str) -> tuple[str, ...]:
    return (
        f"1. Nobody tells you this about {goal}.\n2. Your next level may require a quieter kind of discipline.\n3. Stop calling it failure before you collect the lesson.\n4. Pressure is not permission to quit.\n5. One brick today beats a perfect plan tomorrow.",
        f"[Hook] If {goal} feels heavy, listen.\n[Truth] You do not need to solve the whole future today.\n[Action] Name one move you control, complete it before the day ends, and keep the promise.\n[Close] Concrete is poured one section at a time. Build yours.",
        f"The goal is not to pretend {goal} is easy. The goal is to meet it with truth, faith, and disciplined action. Pick one promise. Keep it today. Then build again tomorrow. Save this for the day motivation gets quiet.",
        "#ConcreteMotivation #Discipline #Purpose #Leadership #Mindset #KeepBuilding",
        "Turn each hook into a Reel; use the three action lines as a carousel; post the closing line as a quote card; ask the audience to comment with their one promise.",
    )


def _outreach(goal: str) -> tuple[str, ...]:
    return (
        "High school and college coaches, athletic directors, trainers, youth-program leaders, and team captains who value character development.",
        f"Lead with service: connect {goal} to discipline, identity, leadership, and performance beyond the scoreboard.",
        f"Subject: A practical mindset session for your athletes\n\nCoach [Name], I'm Jaytee Miller with Concrete Motivation. I help athletes turn pressure, setbacks, and responsibility into disciplined action. I'm reaching out because I'd like to support your team with a practical conversation around {goal}. The session is direct, interactive, and built to leave athletes with a plan they can use immediately. Would you be open to a 15-minute call next week to see if it fits your program?",
        "Coach [Name], following up in case this got buried. I'd be glad to send a one-page session outline or tailor a short pilot conversation to a challenge your team is facing. Is there a better person or time to connect?",
        "A 30-45 minute team talk plus a seven-day discipline challenge and coach discussion guide. Begin with one pilot program and request feedback and a testimonial.",
    )


def _business(goal: str) -> tuple[str, ...]:
    return (
        f"Package Concrete Motivation's lived experience and action framework into a clear outcome centered on {goal}.",
        "Concrete Builder Session: keynote/workshop, participant action guide, seven-day follow-up challenge, and an optional leadership debrief.",
        "Pilot: $750-$1,500; standard local engagement: $2,500-$5,000; custom organization package: scoped after discovery. Validate demand before locking final pricing.",
        "Build a one-page offer, identify 20 aligned schools or organizations, request five discovery calls, and sell two paid pilots before expanding the package.",
        "Partner with athletic programs, youth organizations, churches, workforce-development groups, and values-led local businesses that already serve the audience.",
    )


def _operations(goal: str) -> tuple[str, ...]:
    return (
        f"1. Define the measurable result for {goal}.\n2. Create the first usable deliverable.\n3. Put outreach and feedback on the calendar.",
        "[ ] Write a one-sentence outcome\n[ ] Break work into three milestones\n[ ] Assign one owner per milestone\n[ ] Block two focused work sessions\n[ ] Share the draft with one real user\n[ ] Record feedback and the next decision",
        "Weekly Build Review: capture the goal, scoreboard, completed work, blockers, lessons, and next three commitments in one repeatable page every Friday.",
        "Jaytee owns the outcome and final decisions. Assign support by deliverable--not by vague responsibility--and name one accountable person for every task.",
        "Monday: outcome and plan. Tuesday-Wednesday: build. Thursday: test with a real person. Friday: review the scoreboard and commit next week's priorities.",
    )


def _faith(goal: str) -> tuple[str, ...]:
    return (
        "Renew the mind, then reinforce the renewal with disciplined action.",
        f"When {goal} tests your confidence, do not confuse a hard season with an abandoned purpose. Pause long enough to separate fear from truth. You may not control the whole road, but you can steward the next faithful step.",
        "Scripture teaches a pattern of renewed thinking, patient endurance, wise stewardship, and faith expressed through action. Treat this as a principle to explore, and verify exact wording in your preferred Bible translation before quoting it publicly.",
        "Write the fear you keep rehearsing. Replace it with one truthful, faith-aligned statement. Pray, then complete one concrete action that agrees with that statement today.",
        "I will not let pressure name me. My mind can be renewed, my actions can be disciplined, and I will faithfully build what is in front of me.",
    )


BUILDERS: dict[str, SectionBuilder] = {
    "brand_architect": _brand,
    "motivational_speech": _speech,
    "concrete_conversations_podcast": _podcast,
    "social_media_content": _social,
    "athlete_outreach": _outreach,
    "business_growth": _business,
    "operations": _operations,
    "faith_mindset": _faith,
}


class OfflineProvider:
    """Generate reliable structured output without network access or secrets."""

    name = "offline"

    def generate(
        self,
        bot: Bot,
        goal: str,
        personalization_detail: str,
        brand_profile: BrandProfile,
    ) -> BotResponse:
        if not bot.prompt_file.is_file():
            raise FileNotFoundError(f"Prompt file not found: {bot.prompt_file}")

        prompt = bot.prompt_file.read_text(encoding="utf-8").strip()
        if not prompt:
            raise ValueError(f"Prompt file is empty: {bot.prompt_file}")
        if not brand_profile.source_text:
            raise ValueError("Brand profile cannot be empty.")

        try:
            content = BUILDERS[bot.slug](goal)
        except KeyError as exc:
            raise ProviderError(f"No offline runner configured for {bot.name}.") from exc
        if len(content) != len(bot.sections):
            raise ProviderError(f"Invalid response configuration for {bot.name}.")

        sections = tuple(zip(bot.sections, content, strict=True))
        return BotResponse(
            bot.name,
            goal,
            sections + ((ANGLE_SECTION, self._personalized_angle(bot, goal, personalization_detail, brand_profile)),),
            provider_name=self.name,
        )

    def _personalized_angle(
        self,
        bot: Bot,
        goal: str,
        personalization_detail: str,
        profile: BrandProfile,
    ) -> str:
        audience = ", ".join(profile.primary_audience[:5])
        themes = ", ".join(profile.core_themes[:6])
        detail_line = (
            f"Personal detail to honor: {personalization_detail}."
            if personalization_detail
            else "No extra detail was added, so this stays broad enough for the core Concrete Motivation audience."
        )
        return (
            f"{profile.brand_name} should sound like {profile.founder} building through real pressure: "
            f"{profile.voice}. Keep it aligned with {profile.podcast_name} by turning honest conversation "
            f"into practical movement. For this {bot.name.lower()} on {goal}, connect the message to {themes} "
            f"for {audience}, then land it in family, legacy, and disciplined execution. {detail_line} "
            f"Make the next move clear: choose one action, keep the promise today, and build from there. "
            f"Signature message: {profile.signature_message}."
        )
