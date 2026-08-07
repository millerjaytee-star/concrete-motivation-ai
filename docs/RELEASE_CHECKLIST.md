# Production Release Checklist

Release is fail-closed. Record evidence beside every checked item.

## Canonical source

- [ ] Lovable project ID is `09f0d02d-8d41-40c7-9c36-bbdbf8d11adf`.
- [ ] Production URL is `https://concrete-motivation-app.lovable.app` or an owner-approved custom-domain successor.
- [ ] Git candidate contains the current Lovable commit/source; `python scripts/verify_canonical_product.py` passes.
- [ ] Candidate is not based on `apps/web/` or `website/` without a completed reconciliation.
- [ ] Rollback deployment ID and Git commit are recorded.

## Quality and journeys

- [ ] Clean install, format/lint, typecheck, tests, production build, Python tests, and system check pass.
- [ ] All public routes, navigation, 404, metadata, sitemap, robots, canonical links, images, and social links pass desktop/mobile/tablet checks.
- [ ] Account create/verify/login/reset/delete and privacy controls pass.
- [ ] Member gate, saved Daily Brick/challenge progress, profile, orders, and membership state pass.
- [ ] Owner command center is protected by server/database authorization, not UI checks.
- [ ] Concrete Guide truth, privacy, loading, error, keyboard, rate-limit, and human escalation tests pass.
- [ ] Contact/support categories validate, persist, route, and only claim delivery after provider acceptance.
- [ ] Keyboard focus, contrast, labels, alt text, reduced motion, and screen-reader smoke tests pass.

## Integrations and policy

- [ ] Stripe test checkout: success, decline, cancel, webhook signature, duplicate event, renewal, cancellation, access, and merchandise order pass.
- [ ] Live Stripe remains disabled until owner approval and exact product/price mapping review.
- [ ] Official YouTube channel/API and caching are verified without exposing credentials.
- [ ] GA4 property, consent, DebugView, non-PII events, referral exclusions, and privacy settings are verified.
- [ ] Transactional email/provider and support escalation are verified; no false-send states.
- [ ] Privacy, terms, refunds, AI disclosure, account deletion, support, and consent surfaces are reviewed.
- [ ] Secret scan passes; no credentials, `.env`, signing keys, or private customer data are committed.

## Web/PWA/mobile

- [ ] HTTPS, chosen www redirect, custom canonical URL, OAuth callbacks, Stripe webhook, email links, sitemap, and robots are verified.
- [ ] Manifest, icons, service worker, installability, offline/update behavior, and Add to Home Screen pass.
- [ ] iOS and Android derive from the same canonical product and backend.
- [ ] Deep links, auth callbacks, safe areas, keyboard, external links, versioning, icons, and splash screens pass.
- [ ] Apple/Google signing remains in secure owner-controlled systems.
- [ ] Store privacy/data safety, descriptions, screenshots, reviewer access, support/privacy/terms URLs, rating, and purchase policy are complete.

## Approval and release

- [ ] Jaytee approves production deployment, live payments, DNS, and each store submission as applicable.
- [ ] CI is green on the draft PR; no unresolved critical failures.
- [ ] Deploy canonical candidate; run post-deploy smoke tests; monitor errors and conversion events.
- [ ] If a critical check fails, restore the recorded Lovable deployment and disable new checkout entry points.
