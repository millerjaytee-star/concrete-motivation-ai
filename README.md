# Concrete Motivation AI

Concrete Motivation AI is the operating system for the Concrete Motivation brand and the Concrete Conversations podcast.

This repo is designed for Codex, ChatGPT, GitHub, and your local VS Code setup to work together to build a full bot team for content creation, podcast preparation, motivational speaking, business growth, outreach, and operations.

## Mission

Build AI agents that help Concrete Motivation become a world-class motivational platform by turning life lessons, leadership, discipline, faith, struggle, family, sports, and business wisdom into consistent content, conversations, speeches, and opportunities.

## Bot Team

The system is organized as a team of specialist bots:

1. **Brand Architect Bot**  
   Builds the Concrete Motivation voice, mission, values, taglines, audience, offers, and brand consistency.

2. **Motivational Speech Bot**  
   Creates high-energy speeches in the style of powerful motivational speaking: pain, purpose, discipline, comeback, belief, execution, and legacy.

3. **Concrete Conversations Podcast Bot**  
   Builds podcast episode ideas, outlines, guest questions, intros, outros, clips, titles, and summaries.

4. **Social Media Content Bot**  
   Creates reels, captions, hooks, carousels, short-form scripts, and daily content calendars.

5. **Athlete Outreach Bot**  
   Helps write messages and campaigns to reach athletes, coaches, schools, trainers, youth programs, and sports organizations.

6. **Business Growth Bot**  
   Builds offers, pricing, speaking packages, sponsorship ideas, partnership decks, and monetization plans.

7. **Operations Bot**  
   Creates weekly execution plans, task lists, launch checklists, SOPs, dashboards, and workflows.

8. **Faith & Mindset Bot**  
   Builds spiritually grounded motivation, self-discipline messages, leadership reflections, and renewal-of-the-mind content.

## Current Status

Version 2 is a working, offline-first Python command center with a Concrete Motivation personalization layer. Choose any of the eight specialists, enter a goal, optionally add audience, tone, or personal context, and receive a useful response organized around that bot's required deliverables plus a `Concrete Motivation Angle`. It uses no paid services, internet connection, account, API key, or user tracking.

## Recommended Tech Stack

Initial version:

- Python 3.11+
- Command-line interface
- Markdown prompt library
- JSON bot registry
- Pytest tests

Future version:

- FastAPI backend
- Streamlit or Next.js dashboard
- OpenAI API integration
- Airtable/Notion/Google Drive content library
- Social media scheduler integration

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. If your system exposes Python as `python3`, use that command in place of `python`.

The app will display the bot menu. Enter `1` through `8`, then describe what you want created. Enter `0` to exit. For example:

```text
Enter your choice (0-8): 2
What do you want this bot to create today?
> Create a 7-minute speech about discipline after failure.
Any specific audience, tone, or personal detail to include? Press Enter to skip.
> for high school football players
```

Press Enter at the optional personalization question to skip it. When you provide detail, the offline runner folds it into the `Concrete Motivation Angle` section so the output can target a specific audience, tone, or life context.

## Run Tests

```bash
python -m pytest
```

## How Version 2 Works

- `concrete_motivation/bot_registry.py` is the single source of truth for bot metadata and response sections.
- `prompts/` holds each specialist's durable voice and safety guidance.
- `brand/concrete_motivation_profile.md` holds the Concrete Motivation brand identity, Jaytee Miller founder context, audience, themes, preferences, and guardrails.
- `concrete_motivation/brand_profile.py` loads the brand profile for offline personalization.
- `concrete_motivation/bot_runner.py` creates distinct structured output locally, appends the `Concrete Motivation Angle`, and remains the integration seam for a future opt-in AI provider.
- No input or output is sent over the internet or saved to disk.

See [Bot Team](docs/BOT_TEAM.md) for specialist guidance, [Runbook](docs/RUNBOOK.md) for setup and troubleshooting, and [Roadmap](docs/ROADMAP.md) for the path beyond Version 1.

## Codex Build Prompt

Use this prompt inside Codex:

```text
You are building the Concrete Motivation AI bot system. Review the README, CODEX.md, bot registry, and prompt files. Build a clean Python CLI that allows Jaytee to select a bot, enter a goal, and receive structured output. Add tests, keep the code simple, document everything, and do not remove the brand direction.
```
