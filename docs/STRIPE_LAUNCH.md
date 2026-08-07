# Stripe Launch

Current status: **blocked for end-to-end verification**. The connected Stripe account is active through Composio, but the latest payment-link audit returned no payment links. No live product, price, charge, webhook, or entitlement was created.

## Canonical price source

Memberships: Foundation `$9/month` or `$90/year`; Builder `$19/month` or `$190/year`; Legacy `$49/month` or `$490/year`. Merchandise: Tee `$28`, Hoodie `$55`, Cap `$25`, Bottle `$24`, Wristband `$8`. Store external Stripe IDs in environment-backed deployment configuration; business amounts and slugs must be defined once in canonical application source and checked by pricing-consistency tests.

## Test-mode activation

1. In the Lovable backend secret manager, add Stripe **test** secret and webhook secrets; never use client code or Git.
2. Create/verify test products and recurring/one-time prices matching the canonical price source.
3. Map price IDs by stable offer slug in server configuration.
4. Use server-side Checkout Session creation with authenticated customer/offer validation and idempotency keys.
5. Verify signed webhooks before parsing; persist event IDs uniquely; make entitlement/order updates transactional.
6. Test successful card, decline, user cancel, duplicate delivery, retry, renewal, cancellation, portal, and membership/order state.

## Live activation (owner-only)

After all test evidence passes, Jaytee selects the official Stripe account, approves product names/prices/refund terms, creates or approves live products/prices, installs live secrets in Lovable, registers the final HTTPS webhook URL, and performs one explicitly approved low-value live transaction and refund. Do not copy test IDs into live configuration and do not charge a real card without separate approval.
