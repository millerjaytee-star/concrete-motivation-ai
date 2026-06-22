# CODEX BUILD BRIEF: Concrete Motivation AI

## Role

You are Codex acting as the engineering partner for Jaytee Miller and the Concrete Motivation brand.

Your job is to turn this repository into a working AI bot system for:

- Concrete Motivation, the motivational speaking platform
- Concrete Conversations, the podcast
- Athlete, school, youth, and business outreach
- Social media content creation
- Brand growth and operations

Build carefully. Keep the code clean. Add tests. Do not just create a demo; create a foundation that can grow into a real business operating system.

---

## Product Vision

Concrete Motivation AI should become a command center where Jaytee can choose a specialist bot, enter a goal, and receive useful structured output.

Examples:

- "Create a 7-minute motivational speech about discipline after failure."
- "Build a 45-minute podcast episode about fatherhood, pressure, and purpose."
- "Write 10 Instagram reel hooks for athletes."
- "Create an outreach message to a high school football coach."
- "Build a weekly execution plan for Concrete Motivation."
- "Create a faith-based message about renewing the mind."

---

## Version 1 Goal

Build a working Python command-line application with a clean structure, reusable bot definitions, and tests.

The first version should run locally from VS Code with:

```bash
python main.py
```

It should show a menu, let the user select a bot, ask for their goal, and return a structured response using local prompt templates.

Do not require paid APIs in version 1. Add placeholders for future OpenAI API integration, but make the app run without secrets.

---

## Required File Structure

Create this structure:

```text
concrete-motivation-ai/
├── main.py
├── requirements.txt
├── README.md
├── CODEX.md
├── concrete_motivation/
│   ├── __init__.py
│   ├── app.py
│   ├── bot_registry.py
│   ├── bot_runner.py
│   └── models.py
├── prompts/
│   ├── brand_architect.md
│   ├── motivational_speech.md
│   ├── concrete_conversations_podcast.md
│   ├── social_media_content.md
│   ├── athlete_outreach.md
│   ├── business_growth.md
│   ├── operations.md
│   └── faith_mindset.md
├── docs/
│   ├── BOT_TEAM.md
│   ├── RUNBOOK.md
│   └── ROADMAP.md
└── tests/
    ├── test_bot_registry.py
    └── test_bot_runner.py
```

---

## Bot Requirements

Create eight bots:

### 1. Brand Architect Bot
Purpose: Defines and protects the Concrete Motivation brand.
Output should include:

- Brand message
- Audience
- Tone
- Offer idea
- Next action

### 2. Motivational Speech Bot
Purpose: Creates high-energy motivational speeches.
Output should include:

- Title
- Opening hook
- Main speech
- Crowd engagement lines
- Closing call-to-action

Style guidance: intense, grounded, inspirational, disciplined, faith-aware when appropriate. Do not imitate any public speaker directly; use original wording.

### 3. Concrete Conversations Podcast Bot
Purpose: Builds podcast episodes.
Output should include:

- Episode title
- Episode promise
- Intro
- Segments
- Guest questions
- Clip moments
- Outro

### 4. Social Media Content Bot
Purpose: Creates social media content.
Output should include:

- Hooks
- Short-form script
- Caption
- Hashtags
- Repurpose ideas

### 5. Athlete Outreach Bot
Purpose: Helps reach athletes, coaches, schools, trainers, and organizations.
Output should include:

- Target audience
- Message angle
- DM/email draft
- Follow-up message
- Offer

### 6. Business Growth Bot
Purpose: Builds monetization and growth plans.
Output should include:

- Opportunity
- Offer/package
- Pricing idea
- Sales action
- Partnership angle

### 7. Operations Bot
Purpose: Turns ideas into execution.
Output should include:

- Weekly priorities
- Task checklist
- SOP idea
- Owner
- Deadline suggestions

### 8. Faith & Mindset Bot
Purpose: Creates spiritually grounded mindset content.
Output should include:

- Theme
- Reflection
- Scripture-inspired principle without pretending to quote exact scripture unless verified
- Practical action
- Closing affirmation

---

## Engineering Requirements

- Use Python 3.11+.
- Keep dependencies minimal.
- Use dataclasses or Pydantic-style simple models, but avoid unnecessary complexity.
- App must run without internet.
- No API keys required for version 1.
- Include useful error handling.
- Keep prompts in Markdown files.
- Keep bot metadata in one registry.
- Write tests with pytest.
- Add clear docs.

---

## User Experience Requirements

When Jaytee runs the app, he should see:

```text
====================================
 CONCRETE MOTIVATION AI COMMAND CENTER
====================================

Choose a bot:
1. Brand Architect Bot
2. Motivational Speech Bot
3. Concrete Conversations Podcast Bot
4. Social Media Content Bot
5. Athlete Outreach Bot
6. Business Growth Bot
7. Operations Bot
8. Faith & Mindset Bot
0. Exit
```

Then the app should ask:

```text
What do you want this bot to create today?
```

Then it should print a structured response.

---

## Future Roadmap

After version 1 works:

1. Add OpenAI API integration.
2. Add saved outputs.
3. Add content calendar generation.
4. Add web dashboard.
5. Add voice generation workflow.
6. Add social media export packs.
7. Add podcast episode production pipeline.
8. Add lead tracking and outreach CRM.

---

## Definition of Done

The task is complete when:

- `python main.py` runs successfully.
- All eight bots are selectable.
- Every bot returns useful structured content.
- Prompt files exist for every bot.
- Tests pass with `pytest`.
- README explains setup and usage.
- Docs explain the bot team, roadmap, and runbook.
