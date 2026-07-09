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
        f"1. Nobody tells you this about {goal}.\n2. Your next level may require a quieter kind of discipline.\n3. Stop calling it failure before you collect the lesson.\n4. Pressure is not permission to quit.\n5. One brick today beats a perfect plan tomorrow.\n6. The standard has to outlive the emotion.",
        f"[0-3 sec hook] If {goal} feels heavy, listen.\n[Truth] You do not need to solve the whole future today.\n[Story beat] Name the moment where pressure exposed what needed structure.\n[Action] Choose one move you control, complete it before the day ends, and keep the promise.\n[Close] Concrete is poured one section at a time. Build yours.",
        f"The goal is not to pretend {goal} is easy. The goal is to meet it with truth, faith, and disciplined action. Pick one promise. Keep it today. Then build again tomorrow. Save this for the day motivation gets quiet.\n\nCTA: Comment \"one brick\" if you are choosing one disciplined action today.",
        "#ConcreteMotivation #Discipline #Purpose #Leadership #Mindset #KeepBuilding",
        "Turn each hook into a Reel; use the three action lines as a carousel; post the closing line as a quote card; ask the audience to comment with their one promise; save the best comment as the next podcast question.",
    )


def _outreach(goal: str) -> tuple[str, ...]:
    return (
        "High school and college coaches, athletic directors, trainers, youth-program leaders, school counselors, church youth leaders, community center directors, and team captains who value character development.",
        f"Lead with service: connect {goal} to discipline, identity, leadership, and performance beyond the scoreboard.",
        f"Subject: A practical mindset session for your athletes\n\nCoach [Name], I'm Jaytee Miller with Concrete Motivation. I help athletes turn pressure, setbacks, and responsibility into disciplined action. I'm reaching out because I'd like to support your team with a practical conversation around {goal}. The session is direct, interactive, and built to leave athletes with a plan they can use immediately.\n\nWould you be open to a 15-minute call next week to see if this fits your program?",
        "Follow-up 1: Coach [Name], following up in case this got buried. I can send a one-page outline for a short athlete mindset session around discipline, accountability, and pressure.\n\nFollow-up 2: If now is not the right time, should I reconnect before your next season, camp, or leadership meeting?",
        "A 30-45 minute team talk plus a seven-day discipline challenge, coach discussion guide, and optional follow-up huddle. Begin with one pilot program, request feedback, then ask for a testimonial and referral.",
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


def _ceo(goal: str) -> tuple[str, ...]:
    return (
        f"Make {goal} the operating priority, then judge every task by whether it builds audience, proof, trust, revenue, or execution capacity.",
        "1. Clarify the offer and audience.\n2. Publish proof-building content.\n3. Move warm relationships into conversations.\n4. Protect the weekly execution rhythm.\n5. Review the scoreboard before adding new ideas.\n6. Decide what will not be worked on this week.",
        "Revenue conversations, content published, leads added, follow-ups sent, meetings booked, offers made, assets shipped, testimonials requested, and lessons captured.",
        "Risk: scattered execution. Control: one weekly theme and one owner per outcome.\nRisk: content without sales motion. Control: every campaign creates a next conversation.\nRisk: vague progress. Control: numbers reviewed every Friday.",
        "Choose the one decision that unlocks the week, write it in plain language, assign the next action, and review progress within 48 hours.",
    )


def _content_director(goal: str) -> tuple[str, ...]:
    return (
        f"The campaign should make the audience believe this: {goal} can become a disciplined next step, not just an emotional idea.",
        "YouTube: one anchor video. Shorts/Reels: five cutdowns. Podcast: one conversation angle. Email/Gmail: one relationship-building message. Website: one proof or booking update.",
        "1. Built under pressure.\n2. Discipline after motivation fades.\n3. Family, faith, and legacy.\n4. Leadership in real life.\n5. Practical next actions.",
        "Anchor script, five hooks, three captions, one carousel outline, one podcast segment, one outreach email, and one CTA tied to booking or conversation.",
        "Plan on Monday, record Tuesday, edit Wednesday, publish Thursday through Sunday, and review comments, replies, saves, and leads every Friday.",
    )


def _podcast_producer(goal: str) -> tuple[str, ...]:
    return (
        f"Concrete Conversations episode: {goal.title()} -- a grounded conversation about pressure, purpose, discipline, and the next honest move.",
        "Cold open (45 sec), host intro (2 min), personal story (8 min), guest or teaching segment (18 min), Concrete Challenge (5 min), closing CTA (90 sec).",
        "Send the guest the episode promise, audience, three core questions, recording logistics, clip expectations, and one prompt asking for a real story behind the lesson.",
        "Create one hook clip, one story clip, one practical framework clip, one quote card, and one YouTube Short with the Concrete Challenge.",
        "Confirm topic, prepare questions, check audio, record backup, name files clearly, capture timestamps, write title/description, export clips, and log the episode in the content tracker.",
    )


def _sales_outreach(goal: str) -> tuple[str, ...]:
    return (
        "Schools, athletic programs, youth organizations, churches, community groups, local businesses, podcast sponsors, wellness brands, training facilities, and leadership teams with a values-led audience.",
        f"Position Concrete Motivation as a practical speaking, workshop, or media partner that helps people act on {goal}.",
        f"Subject: Concrete Motivation conversation\n\nHello [Name],\n\nI am Jaytee Miller, founder of Concrete Motivation and host of Concrete Conversations. I am reaching out because your work seems aligned with a message around {goal}, discipline, leadership, and turning pressure into purpose.\n\nI can support through a keynote, workshop, podcast conversation, or partnership built around practical action instead of empty hype. Would you be open to a brief call next week to see whether this could serve your audience?\n\nRespectfully,\nJaytee Miller",
        "Open with the mission, ask what their audience is facing right now, connect the answer to one Concrete Motivation offer, confirm whether there is a fit, ask who else should be involved, and close with a calendar-ready next step.",
        "Day 2: send a short value follow-up. Day 5: send a one-page outline, sample topic list, or episode idea. Day 10: ask whether to close the loop or reconnect later. Log every reply in the CRM with stage, next action, and due date.",
    )


def _youtube_growth(goal: str) -> tuple[str, ...]:
    return (
        f"Build a searchable anchor video around {goal}, then cut it into Shorts that drive viewers back to the full message and the Concrete Conversations brand.",
        "Title 1: The Truth About [Goal]\nTitle 2: Built Under Pressure: [Goal]\nTitle 3: How to Keep Building When [Obstacle]\nThumbnail text: PRESSURE BUILDS / KEEP BUILDING / DISCIPLINE WINS\nDescription angle: name the pressure, promise one practical action, link speaking and podcast paths.",
        "First 5 seconds: direct tension. First 30 seconds: promise a practical outcome. Middle: story, lesson, action. Every 60-90 seconds: reset attention with a question, example, or challenge. Final 60 seconds: recap and invite comment with one concrete commitment.",
        "Create five Shorts: hook, personal line, practical framework, faith-aware reflection, and closing challenge. Each Short should stand alone and point to the full video or podcast.",
        "Write title, description, tags, pinned comment, thumbnail text, chapters, three Shorts scripts, and one community post before recording the next upload.",
    )


def _crm(goal: str) -> tuple[str, ...]:
    return (
        f"Track {goal} by source, relationship strength, offer fit, last touch, next action, owner, and due date.",
        "Warm relationships, schools, coaches, churches, youth programs, businesses, sponsors, podcast guests, content collaborators, and past replies.",
        "Add every new contact, assign a stage, write one next action, set a follow-up date, and move any stale lead to nurture instead of letting it disappear.",
        "Daily: new replies and urgent follow-ups. Monday: new prospect list. Wednesday: second-touch messages. Friday: pipeline review and next-week priorities.",
        "Name, organization, role, email, phone, source, segment, stage, offer, last contact, next action, due date, notes, and outcome.",
    )


def _gmail_outreach(goal: str) -> tuple[str, ...]:
    return (
        f"Use Gmail to create a disciplined daily outreach block for {goal}: find the right thread or lead, send a useful message, track the next action, and follow up on time.",
        "Search Gmail for prior contacts, replies, schools, coaches, churches, sponsors, podcast guests, and local organizations. If a CSV lead list exists, work from the highest-fit names first. Suggested Gmail searches: older_than:30d Concrete Motivation, coach OR athletic director, youth program, church youth, sponsor, podcast guest.",
        "Email 1: short introduction and value angle.\nFollow-up 1: helpful outline or episode/session idea.\nFollow-up 2: close-loop message with a clear yes/no next step.\nReply handling: tag interested, waiting, not now, no fit, or referral needed.",
        "Every sent email gets a CRM entry with date, recipient, segment, offer, thread status, next action, and follow-up due date. Never rely on memory for follow-up. Use labels such as CM/Interested, CM/Waiting, CM/Follow-Up, and CM/Closed.",
        "Send 10 targeted messages, process replies, update CRM, schedule follow-ups, save strong language for reuse, and stop when quality drops.",
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
    "ceo": _ceo,
    "content_director": _content_director,
    "podcast_producer": _podcast_producer,
    "sales_outreach": _sales_outreach,
    "youtube_growth": _youtube_growth,
    "crm": _crm,
    "gmail_outreach": _gmail_outreach,
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
