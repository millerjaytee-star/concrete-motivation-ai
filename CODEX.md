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
You are the lead software architect, senior Python engineer, automation engineer, QA engineer, security reviewer, and technical documentation writer for Concrete Motivation.

Your assignment is to inspect the entire existing Concrete Motivation repository, understand what has already been built, repair anything broken, and expand it into a production-ready AI-powered motivational media, speaking, outreach, and business operations platform.

Do not erase working code unnecessarily. Preserve useful existing functionality, improve weak implementations, remove duplication, fix architectural problems, and document every important decision.

The finished system must be functional, organized, secure, testable, and easy for a beginner to operate from VS Code and the terminal.

PROJECT PURPOSE

Concrete Motivation is a motivational speaking, leadership development, media, podcast, school outreach, sports outreach, and personal development brand founded by Jaytee Miller.

The platform should help the brand:

1. Create motivational content.
2. Find and manage speaking opportunities.
3. Reach schools, churches, nonprofits, corporations, sports organizations, podcasts, and community organizations.
4. Create YouTube, Instagram, TikTok, Facebook, LinkedIn, podcast, newsletter, and website content.
5. Track leads and follow-ups.
6. Build courses, books, speeches, workbooks, and sponsorship materials.
7. Manage the company through one CEO command center.
8. Automate repetitive work while requiring human approval before important external actions.

CURRENT ENVIRONMENT

Assume the project may already contain some or all of the following:

* Python 3
* VS Code project files
* Git and GitHub configuration
* A main.py file
* Existing bots or agents
* Gmail connection through Composio
* YouTube connection through Composio
* Environment variables
* Website-related code
* Outreach files
* CRM files
* Content generation code
* Stripe or payment-related code
* Brand assets
* Requirements files
* Existing documentation

Before building anything, inspect the complete repository.

Create an inventory of:

* Existing folders
* Existing Python files
* Existing environment variables
* Existing integrations
* Existing agents
* Existing tests
* Existing documentation
* Broken imports
* Dead code
* Duplicate code
* Security risks
* Missing dependencies
* Incomplete functions
* Hardcoded credentials
* Placeholder implementations

Do not assume the current code is correct.

PHASE 1: REPOSITORY AUDIT AND REPAIR

Perform a complete technical audit.

Tasks:

1. Read every relevant source file.
2. Identify the current architecture.
3. Run the application.
4. Run all existing tests.
5. Run linting and type checks.
6. Identify syntax errors, import errors, configuration issues, and runtime failures.
7. Repair the current project before expanding it.
8. Preserve user-created content whenever possible.
9. Move secrets out of source files and into environment variables.
10. Create a safe `.env.example`.
11. Confirm `.env` is excluded by `.gitignore`.
12. Confirm credentials, tokens, OAuth files, API keys, and private data cannot be committed.
13. Add structured logging.
14. Add useful error messages.
15. Create backups or migration scripts before changing existing data formats.

Create a report at:

`docs/REPOSITORY_AUDIT.md`

The report must include:

* What existed
* What worked
* What was broken
* What was repaired
* What was replaced
* Security risks found
* Remaining limitations
* Exact commands used to validate the system

ARCHITECTURE REQUIREMENTS

Use a clean modular Python architecture.

Preferred structure:

concrete_motivation/
**init**.py
config/
settings.py
logging_config.py
core/
database.py
models.py
schemas.py
exceptions.py
approval.py
scheduler.py
security.py
agents/
base_agent.py
ceo_agent.py
content_agent.py
speaker_booking_agent.py
podcast_outreach_agent.py
school_outreach_agent.py
sports_outreach_agent.py
sponsorship_agent.py
story_collection_agent.py
course_creation_agent.py
book_writing_agent.py
analytics_agent.py
services/
ai_service.py
gmail_service.py
youtube_service.py
crm_service.py
content_service.py
research_service.py
approval_service.py
export_service.py
notification_service.py
workflows/
daily_content_workflow.py
speaking_outreach_workflow.py
podcast_outreach_workflow.py
school_outreach_workflow.py
sports_outreach_workflow.py
sponsorship_workflow.py
story_workflow.py
course_workflow.py
book_workflow.py
morning_briefing_workflow.py
dashboard/
app.py
pages/
templates/
emails/
speeches/
social/
proposals/
courses/
data/
exports/
generated_content/
reports/
backups/
tests/
scripts/
docs/
main.py
pyproject.toml
.env.example
.gitignore
README.md

You may adjust the structure if the current repository already has a good design, but maintain strong separation between agents, services, workflows, configuration, data, tests, and user interfaces.

TECHNOLOGY EXPECTATIONS

Use stable, maintainable tools.

Preferred stack:

* Python 3.11 or later
* Pydantic for validation and settings
* SQLAlchemy with SQLite for local development
* Alembic or a safe migration mechanism
* Typer or Click for the command-line interface
* Streamlit for the CEO dashboard unless the repository already uses a better-supported interface
* APScheduler for local scheduled workflows
* pytest for testing
* Ruff for linting and formatting
* mypy or pyright for type checking
* HTTPX for HTTP communication
* Jinja2 for reusable templates
* pandas only where useful for reporting and exports

Do not add unnecessary dependencies.

Create or improve `pyproject.toml`.

Provide pinned or safely constrained dependency versions.

CORE OPERATING PRINCIPLES

1. No important email, public post, payment, deletion, upload, or external message should be sent automatically without approval unless an explicit automation setting is enabled.
2. Default to draft mode.
3. All external actions must be logged.
4. Failed actions must not silently disappear.
5. Every bot must support preview mode.
6. Every bot must support dry-run mode.
7. Every bot must validate inputs.
8. Every bot must handle missing credentials gracefully.
9. Every workflow must be restartable.
10. Duplicate outreach must be prevented.
11. Contact opt-outs must be respected.
12. Personally identifiable information must be protected.
13. Research results must include sources and timestamps.
14. Generated facts must not be invented.
15. Human approval must remain part of high-impact workflows.

BUILD THE FOLLOWING SYSTEMS

SYSTEM 1: CEO COMMAND CENTER

Create a CEO dashboard that gives Jaytee one place to run Concrete Motivation.

The dashboard should show:

* Total leads
* New leads this week
* Leads by category
* Follow-ups due
* Overdue follow-ups
* Speaking opportunities
* Podcast opportunities
* School opportunities
* Sports opportunities
* Sponsorship opportunities
* Draft emails waiting for approval
* Content waiting for approval
* Scheduled content
* Content published
* YouTube metrics when available
* Revenue entries
* Expense entries
* Current pipeline value
* Recent agent activity
* Recent errors
* Upcoming deadlines
* Goals and progress
* Daily CEO briefing

Dashboard pages:

1. Overview
2. Leads
3. Outreach
4. Content Studio
5. Speaking Opportunities
6. Podcast Outreach
7. School Outreach
8. Sports Outreach
9. Sponsorships
10. Course Builder
11. Book Builder
12. Story Library
13. Analytics
14. Approvals
15. Settings
16. System Health

Include filters, search, status updates, notes, and export capability.

SYSTEM 2: CENTRAL CRM

Create a central CRM database.

Entities should include:

* Contacts
* Organizations
* Opportunities
* Campaigns
* Outreach messages
* Follow-ups
* Activities
* Content items
* Speaking engagements
* Podcast appearances
* Sponsorship opportunities
* Story submissions
* Courses
* Course modules
* Book projects
* Book chapters
* Revenue
* Expenses
* Goals
* Approval requests
* System events

Lead categories:

* School
* Church
* Nonprofit
* Corporate
* Government
* Podcast
* Sports
* College
* Conference
* Community organization
* Sponsor
* Media
* General

Lead statuses:

* New
* Researched
* Qualified
* Draft ready
* Awaiting approval
* Contacted
* Follow-up due
* Responded
* Meeting scheduled
* Proposal sent
* Negotiating
* Won
* Lost
* Do not contact

Prevent duplicate contacts by normalized email, organization, website, and domain.

Support CSV import and export.

SYSTEM 3: SPEAKER BOOKING BOT

Create a speaker booking agent that helps identify and manage speaking opportunities.

It should:

* Accept a target location, audience, industry, topic, and date range.
* Research possible organizations through configurable research providers.
* Save opportunities in the CRM.
* Identify likely decision-maker roles.
* Generate personalized outreach drafts.
* Generate follow-up drafts.
* Create a speaking proposal.
* Create a speaker one-sheet.
* Create a booking questionnaire.
* Create discovery call notes.
* Create engagement preparation checklists.
* Track estimated speaking fee.
* Track travel requirements.
* Track probability of closing.
* Flag opportunities requiring manual research.

Target audiences:

* Schools
* Colleges
* Churches
* Youth programs
* Nonprofits
* Corporations
* Conferences
* Government agencies
* Sports programs
* Reentry organizations
* Leadership programs
* Employee resource groups

Create commands such as:

`python main.py speaker research`
`python main.py speaker draft`
`python main.py speaker followups`
`python main.py speaker proposal`
`python main.py speaker report`

SYSTEM 4: PODCAST GUEST BOT

Create an agent for finding and pitching relevant podcasts.

It should:

* Store podcast name, host, category, website, contact information, episode count, audience type, and pitch status.
* Generate personalized pitches based on the show.
* Propose discussion topics.
* Generate a guest bio.
* Generate interview talking points.
* Generate a pre-interview research brief.
* Generate post-interview thank-you messages.
* Track accepted, declined, pending, and scheduled appearances.
* Prevent repeat pitches within a configurable cooling period.

Suggested podcast themes:

* Motivation
* Leadership
* Entrepreneurship
* Fatherhood
* Overcoming adversity
* Hospitality leadership
* Operations leadership
* Personal transformation
* Community development
* Education
* Youth mentorship
* Resilience

SYSTEM 5: SCHOOL OUTREACH ENGINE

Create an outreach system specifically for schools and school districts.

It should support:

* Principals
* Assistant principals
* Deans
* School culture leaders
* Student support leaders
* Family engagement teams
* Athletic directors
* Counselors
* District administrators
* Graduation committees
* Parent organizations

Program offers:

* Student motivation assemblies
* Leadership workshops
* Attendance and accountability talks
* Graduation speeches
* Staff motivation
* Parent engagement
* Conflict resolution
* School culture sessions
* Career readiness
* Resilience workshops
* Youth mentorship programs

Generate:

* Introductory email
* Follow-up email
* Program overview
* School proposal
* Pricing options
* Assembly agenda
* Workshop outline
* Learning objectives
* Feedback survey
* Post-event thank-you note
* Renewal request

SYSTEM 6: SPORTS AND NFL OUTREACH BOT

Create a sports outreach agent for:

* NFL teams
* NBA teams
* WNBA teams
* College athletic departments
* High school athletic programs
* Youth leagues
* Training facilities
* Sports foundations
* Rookie development programs
* Player engagement departments

Track:

* Organization
* Team
* League
* Contact
* Role
* Program type
* Season timing
* Outreach status
* Follow-up date
* Proposed topic
* Estimated fee

Suggested speaking topics:

* Discipline under pressure
* Building confidence
* Leadership without a title
* Resilience after failure
* Accountability
* Team culture
* Transitioning through adversity
* Mental toughness
* Life beyond sports
* Personal responsibility

All outreach must remain in draft mode until approved.

SYSTEM 7: DAILY CONTENT EMPIRE BOT

Create a complete content production engine.

The user should be able to enter one core idea, story, lesson, quote, or topic.

The system should generate:

* Long-form YouTube script
* YouTube title options
* YouTube description
* YouTube tags
* YouTube chapter markers
* Thumbnail text ideas
* Three YouTube Shorts scripts
* Three TikTok scripts
* Three Instagram Reel scripts
* Instagram caption
* Facebook post
* LinkedIn post
* X post
* Podcast episode outline
* Podcast episode description
* Email newsletter
* Blog article
* Website quote
* Daily affirmation
* Discussion question
* Call to action

Each piece should be adapted to the platform instead of copied word for word.

Content voice:

* Direct
* Powerful
* Real
* Encouraging
* Honest
* Grounded
* Practical
* Emotionally strong
* Leadership focused
* Built around resilience, pressure, discipline, faith, purpose, accountability, and personal growth

Do not imitate living speakers exactly.

The content can be influenced by high-energy motivational speaking, but it must maintain an original Concrete Motivation voice.

Create a brand voice guide at:

`docs/BRAND_VOICE.md`

The content system must also:

* Store content in the database.
* Save generated files in organized folders.
* Assign status.
* Support revision.
* Support approval.
* Support scheduling.
* Track platform.
* Track campaign.
* Track source topic.
* Avoid repeating recent content.
* Create a weekly content calendar.
* Create a monthly campaign plan.
* Support batch generation.
* Support dry run.
* Support manual editing.

SYSTEM 8: STORY COLLECTION BOT

Create a story collection system.

Story fields:

* Name
* Contact information
* Permission status
* Anonymous option
* Story title
* Story summary
* Full story
* Challenge
* Turning point
* Lesson
* Outcome
* Relevant themes
* Media attachments
* Interview status
* Publication approval
* Content usage approval

Provide:

* Submission form
* Consent language
* Interview question generator
* Story summary generator
* Quote extraction
* Content opportunity suggestions
* Podcast episode suggestions
* Book chapter suggestions
* Speaker story suggestions

Never publish a submitted story without explicit permission.

SYSTEM 9: SPONSORSHIP BOT

Create a sponsorship management system.

It should:

* Track potential sponsors.
* Track contact information.
* Track brand fit.
* Track outreach history.
* Generate sponsorship pitches.
* Generate sponsorship packages.
* Generate proposal PDFs or export-ready documents.
* Track sponsorship levels.
* Track deliverables.
* Track payment status.
* Track contract status.
* Track renewal dates.
* Track campaign results.

Suggested sponsorship levels:

* Community Partner
* Supporting Sponsor
* Presenting Sponsor
* Title Sponsor
* Custom Partnership

Generate package benefits for:

* Podcast placement
* Event placement
* Social media mentions
* Newsletter inclusion
* Website placement
* Workshop sponsorship
* Scholarship sponsorship
* Community event sponsorship
* Video sponsorship
* Branded leadership series

SYSTEM 10: COURSE CREATION BOT

Create a course builder for a program called:

Concrete Leadership Academy

Initial course:

Built Under Pressure: Leadership, Discipline, and Resilience

Suggested modules:

1. Identity and purpose
2. Discipline over motivation
3. Leadership without a title
4. Emotional control under pressure
5. Accountability
6. Communication
7. Conflict resolution
8. Resilience after failure
9. Goal setting
10. Building a personal action plan

For every module, generate:

* Learning objectives
* Instructor script
* Student lesson
* Slide outline
* Workbook section
* Reflection questions
* Activity
* Quiz
* Answer key
* Homework
* Key quotes
* Completion criteria

Create export formats suitable for:

* Markdown
* HTML
* PDF-ready documents
* CSV
* JSON

SYSTEM 11: BOOK WRITING BOT

Create a structured book development system.

Initial book title:

Concrete Motivation: Built Under Pressure

Suggested sections:

1. The foundation
2. Pressure
3. Loss
4. Responsibility
5. Discipline
6. Leadership
7. Family
8. Failure
9. Rebuilding
10. Purpose
11. Service
12. Legacy

The book system must:

* Store book projects.
* Store chapter outlines.
* Store chapter drafts.
* Store stories.
* Store quotes.
* Store research notes.
* Track revision status.
* Track word count.
* Track missing information.
* Generate chapter questions for Jaytee.
* Never invent personal experiences.
* Mark missing personal details as questions or placeholders.
* Export a complete manuscript.

SYSTEM 12: MORNING CEO BRIEFING BOT

Create a daily briefing generator.

The briefing should include:

* Today’s priorities
* Follow-ups due
* Overdue items
* Pending approvals
* New leads
* Active opportunities
* Content scheduled
* Content missing
* Revenue updates
* Upcoming events
* Problems requiring attention
* Recommended next actions
* One motivational leadership focus for the day

The briefing should be available in:

* Dashboard
* Terminal
* Markdown report
* Optional Gmail draft

Do not send automatically unless enabled.

SYSTEM 13: ANALYTICS AND REPORTING

Create reports for:

* Outreach volume
* Response rate
* Booking rate
* Opportunity value
* Revenue by source
* Leads by category
* Follow-up performance
* Content produced
* Content published
* Platform performance
* Campaign performance
* Speaking pipeline
* Podcast pipeline
* School pipeline
* Sports pipeline
* Sponsorship pipeline
* Monthly growth
* Agent errors
* Pending approvals

Support CSV and Excel-compatible export.

SYSTEM 14: APPROVAL CENTER

Create a central approval queue.

Approval types:

* Email
* Social post
* YouTube upload
* Proposal
* Public story
* Sponsorship pitch
* Contact deletion
* Bulk outreach
* Payment action
* External file upload

Approval statuses:

* Draft
* Waiting
* Approved
* Rejected
* Revised
* Executed
* Failed

Every approval must record:

* Creator
* Created time
* Content preview
* Related lead
* Related campaign
* Approval decision
* Decision time
* Execution status
* Error details

INTEGRATIONS

Create service wrappers instead of placing integration code throughout the project.

GMAIL

Use the existing Gmail or Composio connection if available.

Required capabilities:

* Verify connection
* Create drafts
* Read approved drafts
* Search relevant replies
* Match replies to CRM records
* Log sent messages
* Handle errors
* Prevent duplicate sends

Default behavior must create drafts, not send emails.

YOUTUBE

Use the existing YouTube or Composio connection if available.

Required capabilities:

* Verify connection
* Read channel information
* Read recent video information
* Store video analytics where available
* Prepare metadata
* Prepare upload packages
* Upload only after approval
* Log upload results

SOCIAL MEDIA

Build adapter interfaces for future connections to:

* Instagram
* Facebook
* TikTok
* LinkedIn
* X

If credentials do not exist, implement safe mock providers and clear setup instructions.

AI PROVIDER

Build one AI service interface supporting configurable providers.

The rest of the application must not directly depend on one provider.

Support:

* Model configuration
* Temperature configuration
* Timeout handling
* Retries
* Token usage logging
* Structured output validation
* Prompt templates
* Failure fallback
* Mock mode for tests

RESEARCH SERVICE

Create a provider-based research service.

It must:

* Accept search targets.
* Store URLs, source names, accessed dates, and research notes.
* Avoid inventing contact information.
* Clearly mark unverified emails.
* Respect configurable rate limits.
* Support manual import.
* Support CSV import.
* Avoid prohibited scraping.
* Include a mock provider for testing.

SECURITY

Implement:

* Secure environment variable loading
* No hardcoded keys
* Secret redaction in logs
* Validation of file paths
* Safe filenames
* Protection against path traversal
* Safe HTML rendering
* Input size limits
* Rate limiting for bulk actions
* Confirmation for destructive actions
* Database backups
* Audit logs
* Error sanitization
* Contact opt-out handling
* No automatic mass emailing
* No automatic payment actions
* No automatic deletion

DATABASE

Use SQLite locally.

Create:

* Proper models
* Relationships
* Indexes
* Unique constraints
* Timestamps
* Soft deletion where appropriate
* Migration support
* Seed data
* Backup command
* Restore documentation

Create a database diagram in:

`docs/DATABASE_SCHEMA.md`

COMMAND-LINE INTERFACE

Create a clear CLI.

Examples:

`python main.py doctor`
`python main.py setup`
`python main.py dashboard`
`python main.py seed`
`python main.py backup`
`python main.py briefing`
`python main.py leads list`
`python main.py leads import`
`python main.py content generate`
`python main.py content calendar`
`python main.py speaker research`
`python main.py speaker draft`
`python main.py podcast research`
`python main.py school campaign`
`python main.py sports campaign`
`python main.py sponsor campaign`
`python main.py course build`
`python main.py book build`
`python main.py approvals list`
`python main.py approvals approve`
`python main.py test-integrations`
`python main.py run-workflow`

The `doctor` command must check:

* Python version
* Required packages
* Environment file
* Database
* Writable directories
* Gmail connection
* YouTube connection
* AI provider
* Dashboard
* Migrations
* Secret exposure risk

TESTING REQUIREMENTS

Create comprehensive automated tests.

Include:

* Unit tests
* Integration tests
* Database tests
* CLI tests
* Validation tests
* Approval flow tests
* Duplicate prevention tests
* Content generation tests
* CRM tests
* Export tests
* Security tests
* Mock Gmail tests
* Mock YouTube tests
* Mock AI tests
* Workflow tests
* Failure recovery tests

Do not require live credentials for the normal test suite.

Create separate optional live integration tests.

Target meaningful coverage, not superficial coverage.

Run:

* pytest
* Ruff
* Type checker
* Security-oriented checks
* Application smoke test
* Dashboard smoke test
* CLI smoke test

Fix all failures before completing the assignment.

DOCUMENTATION

Create:

`README.md`
`docs/INSTALLATION.md`
`docs/QUICK_START.md`
`docs/ARCHITECTURE.md`
`docs/REPOSITORY_AUDIT.md`
`docs/DATABASE_SCHEMA.md`
`docs/BRAND_VOICE.md`
`docs/AGENT_GUIDE.md`
`docs/WORKFLOW_GUIDE.md`
`docs/INTEGRATIONS.md`
`docs/SECURITY.md`
`docs/TESTING.md`
`docs/TROUBLESHOOTING.md`
`docs/DEPLOYMENT.md`
`docs/ROADMAP.md`
`docs/CHANGELOG.md`

The README must include exact terminal commands for a Mac user.

Include:

1. Creating a virtual environment
2. Activating it
3. Installing dependencies
4. Creating `.env`
5. Initializing the database
6. Running setup
7. Running tests
8. Running the health check
9. Starting the dashboard
10. Generating content
11. Creating outreach drafts
12. Viewing approvals
13. Backing up data
14. Committing to GitHub safely

DEVELOPER EXPERIENCE

Create:

* Helpful setup script
* Health check
* Sample seed data
* Mock mode
* Clear errors
* Useful terminal output
* Makefile or task runner
* Pre-commit configuration
* GitHub Actions workflow
* Automatic test workflow
* Automatic lint workflow

Suggested commands:

`make setup`
`make test`
`make lint`
`make typecheck`
`make doctor`
`make dashboard`
`make backup`

GITHUB

Review Git configuration.

Ensure the repository excludes:

* `.env`
* Credentials
* Tokens
* OAuth files
* Private databases
* Logs containing secrets
* User-submitted private stories
* Generated personal data
* Backups
* Temporary files
* Python cache files
* Virtual environments

Create a GitHub Actions workflow that runs tests, linting, and type checks on pushes and pull requests.

Do not commit secrets.

DATA AND SAMPLE CONTENT

Create safe fictional seed data demonstrating:

* School lead
* Church lead
* Podcast lead
* Corporate lead
* Sports lead
* Sponsor lead
* Speaking opportunity
* Content campaign
* Story submission
* Course project
* Book project
* Approval request

Clearly mark all seed contacts as fictional.

OUTPUT EXPECTATIONS

Do not stop after creating empty folders or placeholder functions.

Implement complete working vertical slices.

At minimum, the finished project must allow the user to:

1. Run setup successfully.
2. Run the health check successfully.
3. Initialize the database.
4. Load fictional sample data.
5. Open the dashboard.
6. View CRM records.
7. Generate a complete content package from one topic.
8. Generate a speaker outreach draft.
9. Generate a school outreach draft.
10. Generate a podcast pitch.
11. Generate a sports outreach draft.
12. Generate a sponsorship proposal.
13. Generate a course module.
14. Generate a book chapter outline.
15. View pending approvals.
16. Approve or reject an item.
17. Generate the morning CEO briefing.
18. Export reports.
19. Run the full automated test suite.
20. Back up the database.

WORKING METHOD

Follow this order:

1. Audit repository.
2. Run current project.
3. Repair current problems.
4. Design architecture.
5. Implement database.
6. Implement settings and logging.
7. Implement approval system.
8. Implement service interfaces.
9. Implement CRM.
10. Implement agents.
11. Implement workflows.
12. Implement CLI.
13. Implement dashboard.
14. Implement integrations.
15. Implement exports.
16. Implement tests.
17. Run full validation.
18. Fix all errors.
19. Update documentation.
20. Provide a final completion report.

Do not ask me to manually create every file.

Create and edit the files directly in the repository.

Do not tell me to replace large sections of code manually if you can apply the changes yourself.

Do not delete working functionality merely to simplify the assignment.

Do not claim success without running tests.

Do not claim an integration works unless it was verified.

When credentials are unavailable, create a fully functional mock mode and document the exact remaining connection step.

FINAL VALIDATION

Before finishing, run and report the results of:

* Repository status
* Dependency installation
* Database initialization
* Migrations
* Seed process
* Health check
* Unit tests
* Integration tests
* Linting
* Formatting check
* Type checking
* CLI smoke tests
* Dashboard startup test
* Content generation test
* Outreach generation test
* Approval flow test
* Export test
* Backup test
* Secret scan
* Git status

Create a final report at:

`docs/BUILD_COMPLETION_REPORT.md`

The report must include:

* Features completed
* Files created
* Files changed
* Tests performed
* Test results
* Integrations verified
* Integrations using mock mode
* Remaining limitations
* Exact commands to start the platform
* Exact commands to run the dashboard
* Exact commands to run tests
* Exact commands to safely commit the work

After all work is complete, print a concise terminal summary containing:

1. What was built
2. What was repaired
3. Whether tests passed
4. Whether Gmail was verified
5. Whether YouTube was verified
6. How to start the dashboard
7. How to generate the first content package
8. How to create the first outreach campaign
9. How to view approvals
10. The recommended Git commands to review and commit the changes

Begin by inspecting the repository. Do not begin by blindly generating a new project.
