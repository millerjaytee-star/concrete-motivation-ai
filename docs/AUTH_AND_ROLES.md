# Authentication and Roles

Current status: **blocked pending canonical source/backend access**. No claim is made that production authentication, persistence, or row-level security is verified.

Required roles are `member`, `support`, and `owner`; default new users are members. Authorization must be enforced in backend functions and database policies. Owner status must come from a protected server-managed role/claim table; never from client metadata, URL parameters, or local storage. Users may read/update only their own profile, progress, reflections, membership/order references, support requests, and deletion requests. Payment/webhook service roles receive only the narrow writes required.

Required evidence: email verification/reset, session expiry, CSRF/session-cookie posture, account deletion, data export, cross-user access denial, regular-member owner-route denial, revoked-owner denial, and audited owner assignment.

Owner assignment action: after backend access is available, Jaytee signs into the official production account, identifies the account by provider user ID (not a password), and an authorized database administrator assigns `owner` through a protected migration/admin procedure. Record the actor, target ID, timestamp, and reason.
