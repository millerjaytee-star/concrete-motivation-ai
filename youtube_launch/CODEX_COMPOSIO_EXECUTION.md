# CODEX EXECUTION BRIEF — Concrete Motivation YouTube Full Revamp

## Mission

Use Codex + Composio to turn the existing `@concretemotivation444` YouTube channel into the production Concrete Motivation channel described in `YOUTUBE_REVAMP_MANIFEST_2026.json`.

The channel must match the live Concrete Nation brand system: black/charcoal concrete, white, construction gold, family, discipline, leadership, purpose, and real life.

## Non-negotiables

- Target only `@concretemotivation444`.
- Use the user's real photos only for people. Do not generate, redraw, reshape, beautify, or replace faces or body structure.
- Never invent subscriber counts, views, verification badges, testimonials, awards, or claims.
- Never delete a YouTube video in this revamp.
- Never make an existing private/unlisted video public without explicit owner approval.
- Never upload a new video without explicit owner approval.
- Audit before mutating.
- Preserve working content and improve organization rather than erasing history.

## Current Composio YouTube tools to use

Composio's 2026 YouTube toolkit exposes the actions needed for the code-side revamp:

- `YOUTUBE_GET_CHANNEL_ID_BY_HANDLE`
- `YOUTUBE_LIST_CHANNELS`
- `YOUTUBE_UPDATE_CHANNEL`
- `YOUTUBE_LIST_USER_PLAYLISTS`
- `YOUTUBE_CREATE_PLAYLIST`
- `YOUTUBE_UPDATE_PLAYLIST`
- `YOUTUBE_ADD_VIDEO_TO_PLAYLIST`
- `YOUTUBE_LIST_CHANNEL_SECTIONS`
- `YOUTUBE_CREATE_CHANNEL_SECTION`
- `YOUTUBE_UPDATE_CHANNEL_SECTION`
- `YOUTUBE_LIST_CHANNEL_VIDEOS`
- `YOUTUBE_GET_VIDEO_DETAILS_BATCH`
- `YOUTUBE_UPDATE_VIDEO`
- `YOUTUBE_UPDATE_THUMBNAIL` only when an approved thumbnail asset is actually available

Inspect every action schema before execution with:

```bash
composio tools info ACTION_NAME
```

If the installed CLI is an older version, the repo's compatibility runner can fall back to the legacy `composio execute ACTION -d '{}'` shape.

## Execution order

### 1. Verify identity

Resolve the authenticated channel and confirm it is Concrete Motivation / `@concretemotivation444`. Stop if identity does not match.

### 2. Audit

List:

- channel metadata
- owned playlists
- Home tab channel sections
- channel videos
- video titles/descriptions/privacy status

Write an audit artifact before changing anything.

### 3. Apply the safe channel revamp

Run:

```bash
python3 scripts/youtube_full_revamp.py
```

Review the audit.

Then apply only after owner approval:

```bash
python3 scripts/youtube_full_revamp.py --apply
```

Type:

```text
REVAMP CONCRETE MOTIVATION
```

This updates supported channel metadata, creates/refreshes the approved playlist architecture, and creates supported playlist-backed Home sections.

### 4. Organize existing videos

Classify existing uploads into the approved playlists using title, description, transcript/caption availability, and content context. Do not guess when ambiguous. One video may belong to multiple playlists when genuinely relevant.

Priority playlists:

1. START HERE — CONCRETE MOTIVATION
2. CONCRETE CONVERSATIONS
3. BUILD FROM PRESSURE
4. DISCIPLINE OVER FEELINGS
5. LEAD WITH PURPOSE
6. FAITH, FAMILY & LEGACY
7. REAL LIFE. REAL TALK.
8. MINDSET & PERSONAL GROWTH
9. CONCRETE NATION

### 5. Metadata modernization

For existing public videos, create a review batch containing proposed title, description, tags, playlist placement, and thumbnail text. Do not mass-update titles blindly. Preserve high-performing searchable titles unless the new title is clearly stronger and accurate.

Use the standard description and CTA system from the manifest while keeping each video's first paragraph specific to its actual content.

### 6. Visual rollout

Use the approved real-photo Canva assets for:

- channel banner
- profile image/logo
- custom thumbnails

Because the Composio toolkit's `YOUTUBE_UPDATE_THUMBNAIL` expects a supported media source, do not publish temporary public links for private family photos merely to automate upload. Prefer manual YouTube Studio upload for banner/profile images when a secure direct-file path is unavailable.

### 7. Trailer and returning-subscriber feature

Set these in YouTube Studio if not exposed by the current Composio schema:

- New visitor trailer: `WELCOME TO CONCRETE MOTIVATION | BUILD FROM PRESSURE`
- Returning subscriber feature: strongest current motivational long-form video until the final `PRESSURE BUILDS LEGENDS` asset is approved.

### 8. Final QA

Verify:

- channel description
- correct handle
- website/shop/contact links
- playlist titles/descriptions
- Home tab section order
- no fake metrics or claims
- no unintended privacy changes
- no deleted videos
- thumbnails use real photos only
- brand phrase is consistent

## Definition of done

The YouTube channel should visually and structurally tell one story:

**Discover Concrete Motivation → trust Concrete Conversations → join Concrete Nation → shop, attend, book, or partner.**

The finished channel should feel like the same organization as the Concrete Nation website/catalog, not a separate legacy YouTube page.
