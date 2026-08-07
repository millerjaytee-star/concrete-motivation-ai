# Security Review

The tracked-file pattern scan found no recognized Stripe/Google/private-key signature in the inspected Git files. This is not a substitute for a full history and provider-side scan.

Confirmed safeguard: the local Stripe adapter is test-key oriented and the canonical product is fail-closed from legacy deployment. Confirmed risk: production backend/auth/database code is unavailable, so RLS, owner authorization, webhook verification, uploads, rate limits, logging, redirects, XSS/HTML handling, and analytics PII cannot yet be certified.

Before release run dependency and secret scans across history and candidate artifacts; inspect every client environment variable; verify secure cookies/session expiry, server authorization, database policies, webhook signatures/idempotency, URL allowlists, output encoding, CSP, upload type/size/storage rules, rate limiting, audit logs, deletion/export, backup restore, and absence of test credentials. Never log tokens, passwords, full payment data, support text, or AI transcripts containing private data.
