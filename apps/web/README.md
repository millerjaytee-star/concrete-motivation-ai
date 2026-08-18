# Concrete Motivation Web

Independent production website for Concrete Motivation, Concrete Conversations, and Concrete Nation.

## Local development

```bash
cd apps/web
npm ci
cp .env.example .env.local
npm run dev
```

Open `http://localhost:3000`.

## Quality checks

```bash
npm run typecheck
npm run lint
npm test
npm run build
```

## Configuration

Public website, app, YouTube, booking, and social URLs are centralized in `lib/site-config.ts` and supplied through environment variables documented in `.env.example`.

## Deployment

Netlify builds this app from the repository-root `netlify.toml`, using `apps/web` as the base and the official Next.js runtime. Production deployment must originate from protected `main`; pull requests should receive preview deployments.

This is a server-capable Next.js deployment, not a static export. Do not add `output: "export"`: authentication, checkout, and signed webhook handlers require a runtime when those app capabilities are migrated into this repository.

## Stripe webhook architecture

Stripe should deliver signed events to `/api/stripe/webhook`. The Node.js route reads the raw request body, verifies the `Stripe-Signature` header with `STRIPE_WEBHOOK_SECRET`, rejects malformed or replay-expired signatures, ignores unsupported event types after verification, and records supported event IDs in Supabase's `stripe_webhook_events` receipt ledger using the server-only service-role credential. The unique event ID and PostgREST `resolution=ignore-duplicates` make replayed deliveries safe. The additive table migration is in `supabase/migrations/20260816000000_create_stripe_webhook_events.sql`.

This repository does not contain the existing authenticated member application's Supabase membership tables or state-sync handler. The receipt route deliberately does not guess those columns or activate access without that approved data contract. Complete the remaining owner actions in the repository root's `OWNER-ACTIONS.md` before enabling live membership fulfillment.

## Release and recovery

Run `npm ci`, `npm run typecheck`, `npm run lint`, `npm test`, and `npm run build` from `apps/web`. Deploy only from protected `main` through Netlify. If a release fails, disable the Netlify deploy or roll back to the last passing Git commit; Stripe retries any event that receives a 4xx/5xx response, and the receipt ledger prevents duplicate processing once the corrected deployment is live.

## Guardrails

- Public marketing pages must never require authentication.
- Stripe stays in test mode until staging acceptance is complete.
- Never publish fake testimonials, metrics, clients, partners, or social proof.
- Consequential bot, email, payment, and publishing actions require owner approval.
