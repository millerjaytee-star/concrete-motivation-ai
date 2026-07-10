# Concrete Motivation Content + Reels Automation Brief

This brief tells Codex exactly what to build next so Concrete Motivation can generate content, short reels scripts, YouTube packages, and daily execution assets from one command center.

## Goal

Turn one Concrete Motivation idea into a complete publish-ready content package:

1. Long-form YouTube concept
2. 60-second Reel script
3. 30-second Short script
4. 15-second hook clip
5. Instagram caption
6. Facebook caption
7. LinkedIn post
8. YouTube title, description, tags, thumbnail notes
9. Podcast segment idea
10. CRM/outreach follow-up angle

No automatic YouTube upload yet. Upload stays blocked until the local Composio YouTube connection is confirmed. The content factory must still work fully offline.

## Required Files To Build

### Python modules

- concrete_motivation/content_reels_factory.py
- concrete_motivation/content_package_models.py
- concrete_motivation/reels_script_writer.py
- concrete_motivation/content_batch_runner.py

### Scripts

- scripts/create_content_package.py
- scripts/create_30_day_content_batch.py
- scripts/create_reels_batch.py

### Docs

- docs/CONTENT_REELS_FACTORY.md

### Tests

- tests/test_content_reels_factory.py
- tests/test_content_batch_runner.py

## Content Package Output Folder

All generated assets should save under:

outputs/content_packages/

Each package must include:

- Markdown file for humans
- JSON file for automation
- CSV row-ready CRM/content tracker export

## Package Fields

Each package should include:

- topic
- audience
- core_message
- platform
- long_form_youtube_title
- long_form_youtube_outline
- youtube_description
- youtube_tags
- thumbnail_text
- reel_60_second_script
- short_30_second_script
- hook_15_second_script
- instagram_caption
- facebook_caption
- linkedin_post
- podcast_segment
- call_to_action
- repurpose_plan

## Voice Rules

Concrete Motivation should sound like:

- direct
- real
- disciplined
- faith-aware
- family-aware
- leadership-driven
- built from pressure
- practical, not fake hype

Signature phrases to rotate, not overuse:

- Pressure has a purpose.
- One brick at a time.
- Build through it.
- Discipline after motivation fades.
- The comeback is quiet first.
- Turn pressure into purpose.

## Command Examples

Create one package:

```bash
python3 scripts/create_content_package.py "discipline after pressure" --audience "high school athletes"
```

Create 30 days:

```bash
python3 scripts/create_30_day_content_batch.py --theme "Pressure Has a Purpose" --audience "students and fathers"
```

Create 10 reels:

```bash
python3 scripts/create_reels_batch.py --theme "one brick at a time" --count 10
```

## Safety Rules

- Do not upload automatically.
- Do not send emails automatically.
- Do not post to social automatically.
- Generate packages first, review second, publish manually or by confirmed tool later.

## Test Requirements

Tests must confirm:

1. One package can be generated.
2. Markdown and JSON save correctly.
3. 30-day batch creates 30 assets.
4. Reels batch creates requested count.
5. Output does not require network access.
6. Scripts can import project modules from scripts/.

## Final Verification

Codex must run:

```bash
python3 scripts/create_content_package.py "discipline after pressure" --audience "high school athletes"
python3 scripts/create_reels_batch.py --theme "one brick at a time" --count 3
python3 scripts/create_30_day_content_batch.py --theme "Pressure Has a Purpose" --audience "students and fathers"
python3 scripts/system_check.py
python3 -m pytest tests
```
