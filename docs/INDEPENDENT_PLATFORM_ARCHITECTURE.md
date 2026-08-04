# Concrete Motivation Independent Platform Architecture

## Decision

Lovable is no longer the development source of truth. GitHub is the permanent source of truth for code, content, configuration, infrastructure, tests, and deployment.

## Platform Structure

### 1. Public Website
- Framework: Next.js with TypeScript
- Styling: Tailwind CSS and shared design tokens
- Hosting: Vercel
- Content: version-controlled MDX/JSON initially, with an admin CMS layer added only when required
- SEO: metadata, sitemap, robots, schema, Open Graph, canonical URLs

### 2. Member App
- Web/PWA: same Next.js application and component system
- Native mobile: Expo React Native when App Store and Google Play packaging begins
- Shared packages: brand tokens, content models, API client, validation, analytics events

### 3. Backend
- Database/Auth/Storage: Supabase PostgreSQL, Auth, Row Level Security, Storage
- Server functions: Next.js route handlers and server actions
- Background jobs: GitHub Actions initially; dedicated job runner when volume requires it

### 4. Payments
- Stripe Checkout, Billing Portal, Products, Prices, subscriptions, merchandise orders, signed webhooks, and idempotent event processing
- Test and live environments remain strictly separated
- No secret keys in browser code or repository history

### 5. AI and Bots
- Python service for CEO, content, outreach, YouTube, community, and operations bots
- One Brand Constitution and machine-readable operating-system configuration
- Retrieval from approved brand, business, content, and customer-support sources
- Human approval gates for publishing, sending email, payments, account changes, and consequential actions

### 6. Media
- YouTube as discovery engine
- Concrete Conversations as trust engine
- Concrete Nation as action/community engine
- Asset manifests connect website, app, YouTube, Shorts, podcast, email, and social channels

### 7. Email and CRM
- Gmail for approved outbound communication
- CRM data model for prospects, organizations, contacts, opportunities, activities, proposals, and follow-ups
- No mass spam; researched outreach and owner-approved sending only

### 8. Deployment
- Preview deployment for every pull request
- Production deployment only from protected main branch
- GitHub Actions for lint, typecheck, unit tests, build, route checks, accessibility checks, and secret scanning
- Rollback through Vercel deployments and Git history

## Repository Target Layout

```text
apps/
  web/                 Next.js public website and PWA
  mobile/              Expo React Native app
  bots/                Python bot service
packages/
  brand/               design tokens, voice, copy rules
  config/              shared platform configuration
  content/             structured content and schemas
  database/            migrations, policies, generated types
  email/               templates and outreach sequences
  ui/                  reusable components
  validation/          shared schemas
infrastructure/
  github/              workflows and repository controls
  vercel/              deployment configuration
  supabase/            migrations, seed, local config
  stripe/              product manifest and webhook docs
docs/
  architecture/
  operations/
  release/
```

## Environments

- local: developer machine with test services
- preview: per-pull-request deployment using non-production data
- staging: stable release candidate using Stripe Test mode
- production: public domain, live Supabase, live Stripe, protected secrets

## Migration Rules

1. Preserve the existing public site, payment logic, business documents, bot logic, content packages, and assets before replacement.
2. Build the new platform alongside legacy directories.
3. Add automated parity tests for public routes and critical business flows.
4. Move one capability at a time: public website, forms, auth, payments, community, bots, mobile.
5. Retire Lovable only after the independent production deployment passes acceptance tests.

## Definition of Done

The independent platform is complete when:

- the public website is deployed from GitHub;
- all public pages are accessible and responsive;
- authentication, profiles, memberships, payments, customer portal, and webhooks work;
- Concrete Nation community v1 works;
- the AI coach and internal bots use the shared operating system;
- Gmail outreach drafts and CRM tracking work;
- YouTube, app, booking, and social links are centrally configured;
- CI passes lint, typecheck, tests, production build, accessibility, route checks, and secret scanning;
- no production capability depends on Lovable.
