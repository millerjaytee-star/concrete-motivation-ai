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

This repository has been initialized as the working home for the Concrete Motivation AI bot system.

Next steps for Codex:

1. Review every file in this repository.
2. Build the first working Python CLI app.
3. Create structured prompt files for each bot.
4. Add tests so the system can be validated.
5. Expand the app into a web dashboard or API after the CLI works.

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
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Codex Build Prompt

Use this prompt inside Codex:

```text
You are building the Concrete Motivation AI bot system. Review the README, CODEX.md, bot registry, and prompt files. Build a clean Python CLI that allows Jaytee to select a bot, enter a goal, and receive structured output. Add tests, keep the code simple, document everything, and do not remove the brand direction.
```
