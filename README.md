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

Version 6 includes the Python command center plus a local static website foundation for Concrete Motivation and Concrete Conversations. The command center still runs offline by default, supports optional OpenAI generation when configured, saves Markdown assets to the output vault, and includes a Weekly Content Calendar Engine.

Offline mode uses no paid services, internet connection, account, API key, or user tracking. OpenAI mode is opt-in through environment variables and falls back to offline mode if generation is unavailable. Saved outputs stay local in `outputs/`.

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

The app will display the bot menu. Enter `1` through `8` to generate with a bot, enter `9` to view recent saved outputs, enter `10` to build a weekly content calendar, or enter `0` to exit. For example:

```text
Provider: offline
Enter your choice (0-10): 2
What do you want this bot to create today?
> Create a 7-minute speech about discipline after failure.
Any specific audience, tone, or personal detail to include? Press Enter to skip.
> for high school football players
Save this output to the content vault? [Y/n]
```

Press Enter at the optional personalization question to skip it. When you provide detail, the runner folds it into the `Concrete Motivation Angle` section so the output can target a specific audience, tone, or life context. Press Enter at the save prompt to save by default, or type `n` to skip.

For the calendar workflow, choose option `10`, enter the main theme for the week, then optionally add an audience, platform, event, or business goal. The engine creates Monday through Sunday content with hooks, scripts or captions, calls to action, platforms, and repurpose ideas.

## Content Vault

Saved outputs are Markdown files with metadata at the top:

```text
---
bot: Bot Name
goal: User goal
provider: offline
fallback_used: false
created_at: 2026-06-23T12:00:00-04:00
---
```

The vault organizes files by bot type:

- `outputs/speeches`
- `outputs/podcast_episodes`
- `outputs/social_posts`
- `outputs/outreach_messages`
- `outputs/business_growth`
- `outputs/operations`
- `outputs/faith_mindset`
- `outputs/brand`
- `outputs/content_calendars`

Filenames include date/time, bot slug, and a short goal slug, such as `2026-06-23-120000-motivational-speech-starting-from-bottom.md`. The folders are committed, but generated Markdown files are ignored by Git so local drafts do not accidentally enter pull requests.

## Provider Modes

Offline mode is the default:

```bash
CONCRETE_AI_PROVIDER=offline python main.py
```

To enable OpenAI mode, copy the example file and add your key:

```bash
cp .env.example .env
```

Then set:

```text
OPENAI_API_KEY=your_real_api_key
CONCRETE_AI_PROVIDER=openai
```

Load those values in your shell before running the app:

```bash
export OPENAI_API_KEY=your_real_api_key
export CONCRETE_AI_PROVIDER=openai
python main.py
```

Return to offline mode by setting `CONCRETE_AI_PROVIDER=offline` or removing the provider variable. Never commit a real `.env` file.

## Run Tests

```bash
python -m pytest
```

## Preview the Website

Open `website/index.html` in a browser. The website is static and needs no backend, build step, API key, payment setup, form service, or deployment.

The first website foundation includes:

- Concrete Motivation hero with booking and podcast calls to action
- Jaytee Miller founder story
- Speaking topics
- Concrete Conversations podcast section with placeholders
- Programs and offers
- Early testimonial placeholders
- Static booking/contact placeholder form

## How Version 6 Works

- `concrete_motivation/bot_registry.py` is the single source of truth for bot metadata and response sections.
- `prompts/` holds each specialist's durable voice and safety guidance.
- `brand/concrete_motivation_profile.md` holds the Concrete Motivation brand identity, Jaytee Miller founder context, audience, themes, preferences, and guardrails.
- `concrete_motivation/brand_profile.py` loads the brand profile for offline personalization.
- `concrete_motivation/providers/` holds the offline provider, OpenAI provider, shared provider interface, and provider factory.
- `concrete_motivation/bot_runner.py` coordinates the configured provider and falls back to offline output when OpenAI is unavailable.
- `concrete_motivation/output_vault.py` saves full Markdown responses with metadata and lists recent saved outputs.
- `concrete_motivation/slugify.py` creates safe file slugs for vault filenames.
- `concrete_motivation/content_calendar.py` creates the offline 7-day Weekly Content Calendar Engine output.
- `website/` holds the static public website foundation.
- Offline mode sends no input or output over the internet and saves nothing to disk.
- OpenAI mode sends the selected bot, goal, optional personalization detail, and brand profile to OpenAI for generation.

## Troubleshooting

- If the app prints `Provider: offline`, offline mode is active or OpenAI mode was not fully configured.
- If OpenAI generation fails, the app prints `OpenAI generation was unavailable, so offline mode was used for this response.` and still returns a response.
- If tests cannot import `openai`, activate your virtual environment and run `python -m pip install -r requirements.txt`.

See [Bot Team](docs/BOT_TEAM.md) for specialist guidance, [Runbook](docs/RUNBOOK.md) for setup and troubleshooting, [Website](docs/WEBSITE.md) for the static site, and [Roadmap](docs/ROADMAP.md) for the path beyond Version 1.

## Codex Build Prompt

Use this prompt inside Codex:

```text
You are building the Concrete Motivation AI bot system. Review the README, CODEX.md, bot registry, and prompt files. Build a clean Python CLI that allows Jaytee to select a bot, enter a goal, and receive structured output. Add tests, keep the code simple, document everything, and do not remove the brand direction.
```
