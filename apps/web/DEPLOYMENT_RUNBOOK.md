# Production Deployment Preparation

This is preparation only. Do not deploy until the owner approves the exact commit, provider, project, domain, and environment.

## Release gates

1. Run `npm ci --no-audit --no-fund`.
2. Run `npm run typecheck`, `npm test`, `npm run build`, and `npm audit --omit=dev --audit-level=high`.
3. Verify `GET /api/health` returns `status: ok` and `externalActions: locked`.
4. Configure secrets in the hosting secret store, never in Git.
5. Keep `STRIPE_ENABLE_TEST_SESSION_CREATION=false` until exact test prices are approved.
6. Do not configure live Stripe keys in the release candidate. The adapter rejects them.
7. Do not configure GA until the property, measurement ID, privacy text, and consent behavior are approved.
8. Test with synthetic CRM records and internal email drafts only.
9. Verify security headers, mobile layouts, keyboard navigation, 404s, sitemap, robots, legal pages, success/cancel paths, and rollback in staging.
10. Obtain separate production deploy and DNS approvals.

## Required environment

- `NEXT_PUBLIC_SITE_URL`
- Approved public social and booking URLs from `.env.example`
- `NEXT_PUBLIC_GA_MEASUREMENT_ID` only after analytics approval
- `STRIPE_SECRET_KEY` using a test key only
- `STRIPE_WEBHOOK_SECRET` using the staging endpoint secret
- `STRIPE_ALLOWED_TEST_PRICE_IDS` as a comma-separated allowlist
- `STRIPE_ENABLE_TEST_SESSION_CREATION=true` only for an approved staging test

## Container contract

Build from `apps/web/Dockerfile`. The final image runs as an unprivileged user on port 3000 and exposes `/api/health` for readiness checks. The build does not publish an image or deploy a service.

## Rollback

Retain the previously accepted image/build, environment snapshot, and provider release identifier. Roll back application traffic before attempting data repair. Stripe, Gmail, YouTube, DNS, and analytics changes have separate rollback and owner gates.
