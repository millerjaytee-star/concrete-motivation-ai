# NETLIFY OWNERSHIP — REQUIRED BEFORE PRODUCTION

These checks establish whether Jaytee—not merely the repository—controls the live deployment chain. Do not deploy until each ownership check is confirmed.

## 1. Confirm GitHub repository administration

### WHAT TO CHECK

Confirm the repository is `millerjaytee-star/concrete-motivation-ai`, the production branch is `main`, and Jaytee's GitHub identity has repository **Admin** permission.

### WHERE TO CHECK IT

GitHub → `millerjaytee-star/concrete-motivation-ai` → Settings → Collaborators and teams → access level; also Settings → Branches/Rulesets.

### WHAT HE SHOULD SEE

Jaytee's `millerjaytee-star` account is the owner/admin, `main` is the default production branch, and branch protection can be viewed and changed by him.

### WHAT CORRECT OWNERSHIP LOOKS LIKE

Jaytee can change repository settings, manage collaborators, protect `main`, create branches/tags, view Actions, and revoke every unneeded collaborator or deploy key.

### WHAT TO DO IF IT IS NOT UNDER HIS ACCOUNT

Do not transfer or delete anything blindly. Contact the current GitHub organization/owner, obtain an ownership transfer or admin grant, then rotate/revoke unknown deploy keys and collaborators after access is confirmed.

## 2. Confirm the Netlify site and team owner

### WHAT TO CHECK

Confirm the linked Netlify site ID is `fe8a7ba3-c206-4ed6-abbf-83ce493dec68`, the site is linked to `millerjaytee-star/concrete-motivation-ai`, and the Netlify user/team is Jaytee-controlled.

### WHERE TO CHECK IT

Netlify → Team switcher → Sites → the linked project → Project configuration → General, Build & deploy, and Team members. The local linked-site record is `.netlify/state.json` (ignored local metadata, not repository ownership proof).

### WHAT HE SHOULD SEE

The Netlify account is Jaytee Miller (`millerjaytee@gmail.com`), the site belongs to his controlled team, Git provider is GitHub, repository is `millerjaytee-star/concrete-motivation-ai`, and production branch is `main`.

### WHAT CORRECT OWNERSHIP LOOKS LIKE

Jaytee can trigger deploys, cancel builds, inspect logs, roll back/publish a prior deploy, edit environment variables and build settings, manage domains, manage deploy previews, and disconnect/reconnect GitHub without another person's approval.

### WHAT TO DO IF IT IS NOT UNDER HIS ACCOUNT

Stop. Ask the current Netlify team owner to transfer the site to Jaytee's controlled team or grant full team/site administration. Do not create a second production site until the existing domain and deployment history are accounted for.

## 3. Align Netlify build settings with the repository source of truth

### WHAT TO CHECK

Confirm the site uses the committed root `netlify.toml`, not stale UI settings. Required values are base `apps/web`, command `npm run build`, publish `.next`, and Node `22`.

### WHERE TO CHECK IT

Netlify → Project configuration → Build & deploy → Continuous deployment → Build settings, and Deploys → a deploy's build log. Confirm the repository root is the configuration-file location.

### WHAT HE SHOULD SEE

The build log runs from `apps/web`, executes `npm run build`, uses Node 22, detects Next.js, and produces a server-capable Next deployment. The repository's current Netlify API record still reports the old `website` directory and blank command, so this check is not yet passed.

### WHAT CORRECT OWNERSHIP LOOKS LIKE

Jaytee can edit these settings and can see a successful GitHub-triggered deploy using the committed configuration without Lovable or a manual upload.

### WHAT TO DO IF IT IS NOT UNDER HIS ACCOUNT

If Jaytee cannot edit the settings, resolve Netlify team ownership first. If he can edit them, set the repository configuration path to the root `netlify.toml` (or enter the same values in the UI), save, and verify with a preview deploy after this local change is approved.

## 4. Attach and verify the production domain

### WHAT TO CHECK

Confirm `concretemotivation.com` and any intended `www` alias are attached to this exact Netlify site, with HTTPS enabled and the canonical domain selected.

### WHERE TO CHECK IT

Netlify → Project configuration → Domain management; separately check the authoritative DNS provider for the domain.

### WHAT HE SHOULD SEE

Netlify lists `concretemotivation.com` on site ID `fe8a7ba3-c206-4ed6-abbf-83ce493dec68`, provisions a valid certificate, and shows DNS records targeting this site. The current Netlify API record reports `custom_domain: null`, and the domain did not resolve during this audit, so this check is not yet passed.

### WHAT CORRECT OWNERSHIP LOOKS LIKE

Jaytee controls both the Netlify domain mapping and the DNS account/zone. No registrar, DNS, or former platform owner is required to change records or renew the site configuration.

### WHAT TO DO IF IT IS NOT UNDER HIS ACCOUNT

Do not change DNS blindly. Identify the registrar and authoritative DNS provider, obtain ownership or delegated DNS administration, then add the exact Netlify records shown in Netlify Domain management and verify HTTPS before switching production traffic.

## 5. Verify deploy, rollback, preview, and recovery controls

### WHAT TO CHECK

Verify Jaytee can perform the complete operational loop: GitHub push/PR preview, production deploy from `main`, log inspection, cancel, rollback to a prior successful deployment, environment-variable update, and domain configuration change.

### WHERE TO CHECK IT

GitHub Actions and Netlify → Deploys, Deploy previews, Deploy logs, Environment variables, and Domain management.

### WHAT HE SHOULD SEE

A pull request produces a preview, `main` produces a production deploy, the deploy log identifies the GitHub commit, and the prior deploy can be republished without a new code push.

### WHAT CORRECT OWNERSHIP LOOKS LIKE

Every recovery action is available to Jaytee directly and audit logs identify his account; no Lovable project, credit balance, or third-party operator is part of the path.

### WHAT TO DO IF IT IS NOT UNDER HIS ACCOUNT

Pause production changes and resolve the missing GitHub/Netlify/domain permission before any deployment. Preserve the current site and deployment history while access is transferred.

## Deferred application work

The Supabase and Stripe items below are intentionally deferred. Do not execute them as part of this Netlify ownership task.

These are the only remaining actions that require Jaytee's account access, approval, credentials, or existing application knowledge. Repository-side implementation and tests are complete for the webhook receipt boundary.

## 1. Apply the additive webhook receipt migration

### WHAT TO DO

Apply `supabase/migrations/20260816000000_create_stripe_webhook_events.sql` to the intended staging Supabase project, validate it, then apply the same additive migration to production.

### WHERE

Supabase Dashboard SQL Editor or the approved Supabase CLI migration workflow.

### VALUE NEEDED

Supabase project owner access; no source code or secret should be pasted into the SQL editor.

### WHY

The Next.js webhook needs a durable, unique event ledger so duplicate Stripe deliveries are acknowledged safely without duplicate receipt processing. The migration only creates this table and enables RLS; it does not delete or alter existing business data.

### HOW TO VERIFY

Confirm `public.stripe_webhook_events` exists with a unique `stripe_event_id` constraint and RLS enabled. Run the staging webhook test twice with the same event ID and confirm one ledger row.

## 2. Configure encrypted production environment variables

### WHAT TO DO

Set the server-only variables in Netlify for the production context, using separate test and live values:

- `STRIPE_WEBHOOK_SECRET` — the signing secret for the exact endpoint below.
- `SUPABASE_URL` — the target Supabase project URL.
- `SUPABASE_SERVICE_ROLE_KEY` — a server-only least-privilege service credential permitted to insert the receipt ledger.
- `STRIPE_WEBHOOK_EVENTS_TABLE=stripe_webhook_events` — the migration's table name.
- `STRIPE_SECRET_KEY` — only if the migrated member application adds server-side Stripe API calls; use a restricted key.

### WHERE

Netlify site settings → Environment variables → Production.

### VALUE NEEDED

The values above from Stripe Workbench/API keys and Supabase Project Settings. Never use `NEXT_PUBLIC_` for any of them.

### WHY

The route cannot verify signatures or durably record supported events without these server-side values. They must never enter the browser bundle or repository.

### HOW TO VERIFY

Inspect the production build and client response headers for absence of secret values. A signed staging delivery reaches the route and creates a ledger row; an unsigned delivery returns HTTP 400.

## 3. Point Stripe to the real Netlify server endpoint

### WHAT TO DO

Create or update the Stripe webhook destination to:

`https://concretemotivation.com/api/stripe/webhook`

Subscribe only to the supported membership/payment events listed in `apps/web/lib/stripe-webhook.ts`.

### WHERE

Stripe Dashboard → Workbench → Webhooks.

### VALUE NEEDED

The production HTTPS URL above and the generated `whsec_...` signing secret from this endpoint.

### WHY

The prior 404 occurred because the deployed application had no `/api/stripe/webhook` route. This repository now provides a real Node.js Next route; Stripe must target it after the Netlify deployment is live.

### HOW TO VERIFY

Stripe's “Send test event” reports HTTP 200 for a configured supported event, HTTP 200 with `ignored: true` for an unsupported legitimate event, and the Supabase ledger contains the event ID exactly once after replay.

## 4. Provide the existing membership state contract

### WHAT TO DO

Provide the approved existing Concrete Nation application source or a written Supabase data contract identifying the tables/columns that represent users, profiles, memberships, subscriptions, purchases, payments, program access, and roles. Approve the mapping from Stripe customer/subscription/checkout IDs to those records.

### WHERE

The current member application repository/export and Supabase Dashboard → Table Editor/Database schema. Do not create a replacement app or spend Lovable credits.

### VALUE NEEDED

Read access to the existing approved app source/schema, plus owner approval of the exact membership-state mapping. No production data export is required.

### WHY

This repository previously contained no Supabase client, migrations, authenticated member routes, Stripe server handler, or membership update code. The new route safely records signed events, but it cannot invent or safely mutate an unknown membership schema.

### HOW TO VERIFY

The approved mapping is documented in code/tests, a staging checkout changes the intended membership/subscription state once, and a replay does not create a second state transition.

## 5. Approve legal and production account settings

### WHAT TO DO

Approve the policy language and confirm the production domain, Netlify site, GitHub branch protection, and Supabase/Stripe live-mode accounts are the intended accounts.

### WHERE

Counsel review; DNS provider; Netlify domain settings; GitHub repository rulesets; Supabase and Stripe dashboards.

### VALUE NEEDED

Owner/legal approval and account access. No source-code edit is required for this checklist item.

### WHY

The repository cannot approve legal terms, DNS ownership, account identity, or branch protection on Jaytee's behalf.

### HOW TO VERIFY

`https://concretemotivation.com` serves the Netlify build, `main` requires passing Web CI, approved policy versions are published, and staging/live mode separation is confirmed.
