# Concrete Motivation Web

Independent production website for Concrete Motivation, Concrete Conversations, and Concrete Nation.

## Local development

```bash
cd apps/web
npm install
cp .env.example .env.local
npm run dev
```

Open `http://localhost:3000`.

## Quality checks

```bash
npm run typecheck
npm run build
```

## Configuration

Public website, app, YouTube, booking, and social URLs are centralized in `lib/site-config.ts` and supplied through environment variables documented in `.env.example`.

## Deployment

Import the repository into Vercel and set the Root Directory to `apps/web`. Production deployment must originate from protected `main`. Preview deployments should run for pull requests.

## Guardrails

- Public marketing pages must never require authentication.
- Stripe stays in test mode until staging acceptance is complete.
- Never publish fake testimonials, metrics, clients, partners, or social proof.
- Consequential bot, email, payment, and publishing actions require owner approval.
