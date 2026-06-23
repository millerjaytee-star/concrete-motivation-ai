# Product Roadmap

## Version 1 — Offline command center

- Eight selectable specialists
- Local structured generation with no secrets
- Markdown prompt library and central registry
- Tested terminal experience and operating docs

## Version 2 — Offline personalization layer

- Concrete Motivation brand profile loaded from Markdown
- Jaytee Miller, Concrete Conversations, audience, theme, and voice context applied to every bot
- Optional audience, tone, or personal-detail follow-up after the main goal
- `Concrete Motivation Angle` included in each response
- No API key, account, internet connection, or saved history required

## Version 2.1 — Useful local history

- Optional Markdown/JSON export
- Saved project names and output history
- More goal parameters, such as audience, duration, and platform
- Accessibility and Windows terminal testing

## Version 3 — Provider-backed intelligence

- A provider interface with the offline runner as the default
- Opt-in OpenAI integration configured through environment variables
- Offline fallback when OpenAI is unavailable
- Provider-aware CLI status
- OpenAI prompt construction with reusable brand context

## Version 3.1 — Provider polish

- Prompt versioning, safety checks, and cost visibility
- Streaming output

## Version 4 — Output vault and content library

- Local Markdown output vault
- Save prompt after every generated response
- Metadata for bot, goal, provider, fallback status, and timestamp
- Recent saved outputs menu
- Safe filenames organized by content type

## Version 5 — Web command center

- FastAPI service and authenticated dashboard
- Content calendar and approval workflow
- Podcast production and social export packs
- Lead tracking, outreach CRM, and team roles

Each phase should preserve the local, no-secret Version 1 path. External integrations must be opt-in, tested, and documented before becoming defaults.
