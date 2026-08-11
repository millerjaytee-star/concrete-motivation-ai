# Lovable–GitHub Reconciliation Report

Verified: 2026-08-07 (America/New_York)

## Executive finding

Lovable is the authoritative product, but its editable source is not currently present in this Git repository. The owner-supplied commit `f52ad32139ebffea6b413a475b4dd46dd5585b2c` is absent from the local object database, `origin/main`, and every fetched remote ref. The Lovable editor could not be reached through an authenticated browser session. Therefore no source import, merge, deletion, or deployment was attempted.

The production URL returned HTTP 200 and deployment ID `4bdf282a60ca6495454e0dad86f6597f80b7c02946bc3f78a5ac1f53ab144d1c`. Its rendered application is materially newer than the local Next.js site.

## Lovable-only capabilities observed from production

- Authentic founder and family media under `/brand/`
- Vite-style application bundle and router
- PWA manifest and Apple mobile metadata
- Concrete Guide UI and support escalation
- Public Daily Brick and seven-day challenge journeys
- Concrete Nation membership presentation with the canonical three tiers
- Routes observed directly in the production route bundle: `/`, `/about`, `/challenge`, `/community-impact`, `/concrete-story`, `/contact`, `/conversations`, `/daily-brick`, `/join`, `/membership`, `/pillars/$slug`, `/start-here`, and `/support`
- Public language explicitly distinguishing free content from member value

This is evidence of deployed behavior, not an editable-source export. Minified production assets must not be treated as the canonical development source.

## GitHub-only systems to preserve

- Python bot/automation packages in `concrete_motivation/`, `concrete-motivation-bots/`, and `Core/`
- Prompt, content, CRM, media, YouTube, FFmpeg, catalog, QA, and packaging scripts
- Test suite and system check
- Launch evidence, reports, rollback and disaster-recovery documentation
- YouTube and Composio audit records
- The Next.js implementation under `apps/web/` as historical/reference work only
- Static pages under `website/` as historical/reference work only

## Conflicts and stale configuration

| Area | Lovable production | GitHub local | Resolution |
|---|---|---|---|
| Product stack | Bundled Lovable/Vite application | Next.js 16 app | Lovable wins; do not deploy Next.js over it |
| Primary routes | Start Here, Daily Brick, challenge, pillars, membership, Guide | Different slug/content map | Import Lovable source before modifying routes |
| Product URL | `concrete-motivation-app.lovable.app` | defaults to unverified `concretemotivation.com` | Canonical config records Lovable URL |
| App URL | same canonical Lovable product/PWA | placeholder `app.concretemotivation.com` | remove only after source reconciliation identifies consumers |
| Social URLs | only verified links should render | local defaults construct unverified URLs | legacy app remains non-deployable |
| Payments | prices visible; live processing not verified | test-only adapter/staged docs | keep disabled until end-to-end test evidence exists |
| Auth/database | production behavior requires source/backend inspection | no verified production backend | blocked pending Lovable export/backend access |

## Duplicate/obsolete implementation policy

No files are deleted in this reconciliation phase. `apps/web/` and `website/` are marked non-canonical in `AGENTS.md` and `README.md`. After a verified Lovable export is imported, compare feature-by-feature, move reusable automation out of any obsolete product tree, then remove duplicates in a separate reviewed commit.

## Missing source/tests/documentation

- Missing: editable Lovable source and exact canonical commit object
- Missing: Lovable backend schema/functions and environment-variable inventory
- Missing: authenticated verification of auth, member state, owner role, database RLS, Stripe checkout/webhooks, email delivery, and GA4 DebugView
- Missing: native iOS/Android projects derived from canonical source
- Added: canonical product configuration, CI guard, tests, release checklist, integration runbooks, and launch status

## Exact owner action to unblock source reconciliation

In the Lovable project editor, connect/sync the project to `millerjaytee-star/concrete-motivation-ai` on a new branch named `lovable/canonical-f52ad321`, or download the full project source ZIP and place it at `imports/lovable/concrete-motivation-app-f52ad321.zip`. Select project `09f0d02d-8d41-40c7-9c36-bbdbf8d11adf`. Do not paste tokens or credentials. The delivered source must identify commit `f52ad32139ebffea6b413a475b4dd46dd5585b2c` or explain the newer canonical commit.
