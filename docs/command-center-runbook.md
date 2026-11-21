# Operate the Concrete Command Center

The owner workspace is served at `/command-center` in the existing Next.js website. The separate Concrete Nation app remains the source for member access, payments and the authenticated release center. See the [verified infrastructure inventory](command-center-inventory.md) for system ownership and exact native build evidence. [Provider setup](command-center-integrations.md) covers Composio and OAuth.

## Set up staging

1. Confirm the intended existing Supabase staging project. The Command Center migration `20261121025851_create_command_center` creates its own schema, tables and service-role-only RPCs. This migration was applied to Concrete Motivation Staging and verified with a rolled-back synthetic fixture. All six private tables enable RLS. The advisory that they have no browser-role policies is expected for this service-role-only schema. Follow the existing staging migration process and check that the migration history matches the repository. The application expects the migration before enabling store credentials.
2. In the staging Auth project, select an authorized password-enabled owner with a verified email. Set the exact Auth user UUID and the staging URL, publishable key and server-only secret in Netlify environment settings. Use the variable names in [the environment example](../apps/web/.env.example). Provision only a staging browser session.
3. Enable provider settings after sizing cost and confirming account identity. Open Composio from the command center, complete each OAuth consent and verify the live read in the owner session.
4. Verify the owner can create a workspace record and record an approval decision. Verify a normal account receives HTTP 401 and cross-origin mutations receive HTTP 403. Confirm the staging database contains no production credentials or raw customer data.
5. Netlify scheduled functions run on the published deploy for a site. For staging previews, use an already approved HTTPS scheduler to POST to `/api/command-center/cron` every five minutes with the environment's bearer secret. For a published deploy, set `COMMAND_SCHEDULER_ORIGIN` and `COMMAND_CRON_SECRET` so the existing Netlify site schedules its own endpoint. Set separate random secrets of at least 32 characters for each environment. Schedules stay paused until the owner enables them.

From `apps/web`, run `npm ci`, `npm run dev`, then open [the local workspace](http://localhost:3000/command-center). Without Auth settings the route displays its setup state and the API fails closed. Passwords are entered only in the workspace sign-in form. An HTTP-only cookie is limited to the Command Center API and expires within one hour. A cached or invalid browser session cannot bypass the server's Supabase identity check.

## Agent team

All twelve roles can draft or analyze on the internal workspace. Select a role, enter a task, optionally select scoped records and review the generated output. The agent gets only the task, explicitly selected and truncated context, and its role instructions. The run claim deduplicates identical requests. The daily owner budget limits attempted runs and each provider request has an output cap. Provider execution gets no external tools. Save a draft to the Content Library, put it in the relevant pipeline or queue it for a decision.

| Agent | Typical output |
| --- | --- |
| Chief Executive Officer | Decision brief with strategic priorities and missing information |
| Chief Operating Officer | Plan with owners, dependencies, handoffs and next steps |
| Executive Assistant | Inbox or scheduling triage, meeting preparation and reply drafts |
| Chief Marketing Officer | Positioning, campaign brief and measurement plan |
| Content Director | Scripts, captions, outlines and production calendar drafts |
| YouTube Producer | Video or Shorts plan, metadata, thumbnails, upload checklist and experiments |
| Podcast Producer | Episodes, interview questions, production checklists and show notes |
| Partnership & Outreach Director | Lead qualification, invitation and proposal drafts |
| Curriculum Director | Age-appropriate lessons, assessments and educator guidance |
| Membership & Community Director | Onboarding, retention and challenge plans |
| Chief Financial Officer | Source-labeled finance analysis, projections and missing data |
| Engineering & Quality Director | Defect triage, release and test plans, verification evidence |

## Workflows and approvals

| Workflow | Trigger implemented | Result |
| --- | --- | --- |
| Daily executive briefing | Enabled interval | Draft from recorded calendar, email, production, CRM, and engineering work, plus pending approvals. |
| Content preparation | Approved theme record | Production brief in Content Library. |
| Podcast preparation | Guest confirmed record with evidence | Episode preparation record and checklist. |
| Outreach follow-up | Reply received record with evidence | CRM follow-up draft. |
| Membership follow-up | Joined, at-risk or cancelled record with evidence | Engagement draft. |
| Engineering review | Enabled interval | Review of recorded evidence-backed release and health issues. |

Local scheduled and event-record workflows are draft-only. Signed provider webhook ingestion, live monitoring alerts, and external execution after approval still need implementation and live acceptance. Workflow errors and retries are visible under System Health. Repeated event IDs deduplicate at the database. Retry uses five- and ten-minute backoff with three attempts. Stop the scheduler or pause the workflow if the failure is ongoing, inspect the current run and fix the source before enabling it. For an uncertain model run, review provider usage before reissuing the request.

The approval queue records a decision on a specific request and preserves its proposal details. Owner approval is a prerequisite for consequential external work. Use the original reviewed artifact and the intended provider when executing an action manually. Link the final evidence to its workspace record. Owner-uploaded evidence and provider-confirmed operations should be read as different sources.

## Verification and recovery

For web checks, use `npm run typecheck`, `npm run lint`, `npm test`, and `npm run build` in `apps/web`. Rehearse the SQL regression script against a disposable Supabase or PostgreSQL database as described in the comments in [command-store.test.sql](../scripts/tests/command-store.test.sql). Do not run the fixture on a production system.

If a deploy needs to be withdrawn, open a revert change and let existing Netlify CI redeploy the previous application behavior. For service failures, disable the scheduler and rotate the affected secret. Before any approved production migration, verify the existing database backup/restore options and rehearse recovery on staging. Keep the additive Command Center schema for recovery after a web rollback. Removing it later requires a separately reviewed backup and migration.

## Estimated incremental monthly cost

At 300 agent runs with 2,000 input and 1,600 output tokens each, the default GPT-4.1 mini model costs about **$1.01** in model usage at published token rates. Four connector previews refreshed twice daily would use up to 868 Composio proxy calls in a 31-day month before separate checks. Composio lists **$0 Hobby** and **$29 Pro** before extra usage. That makes the illustrated agent-plus-connector subtotal **about $1–$30/month**, excluding hosting, database plans, scheduler/function usage, taxes, existing contracts and overages. Actual Netlify and Supabase account billing was not inspected. Review those accounts before budget approval. [OpenAI model pricing](https://developers.openai.com/api/docs/models/gpt-4.1-mini) · [Composio pricing](https://composio.dev/pricing/platform)
