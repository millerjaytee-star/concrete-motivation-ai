# Connection Matrix

Updated: 2026-08-07 (America/New_York). Evidence is read-only unless explicitly stated.

| Service | Status | Evidence | Next action |
|---|---|---|---|
| Lovable | OWNER ACTION REQUIRED | Production URL responds HTTP 200; editable canonical commit absent from GitHub; no Lovable Composio toolkit | Owner syncs/export source from official Lovable project |
| GitHub | CONNECTED + VERIFIED | Composio GitHub connection active; PR #33 and branch are accessible | Wait for canonical Lovable branch |
| Database | BLOCKED | Canonical backend/source unavailable | Verify after Lovable source sync |
| Auth | BLOCKED | Canonical auth implementation unavailable | Verify after source sync |
| Owner Role | BLOCKED | Server-side role assignment cannot be inspected | Verify after auth/backend access |
| Stripe Test | CONNECTED + NOT VERIFIED | Composio Stripe connection active; payment-link audit returned no links | Verify after canonical backend sync |
| Stripe Live | OWNER ACTION REQUIRED | Live charges intentionally disabled | Owner approval only after test-mode pass |
| Payment Webhook | BLOCKED | Canonical endpoint and secret unavailable | Verify after source sync |
| Concrete Guide | CONNECTED + NOT VERIFIED | Live Lovable UI advertises Guide and escalation copy | Test canonical source after sync |
| Email | CONNECTED + NOT VERIFIED | Gmail active connection exists; app delivery provider unverified | Verify after source sync |
| YouTube | CONNECTED + VERIFIED | Official channel and handle previously verified through active connection | Recheck canonical feed after source sync |
| GA4 | BLOCKED | No canonical property/DebugView evidence | Verify after source sync and owner property access |
| Custom Domain | OWNER ACTION REQUIRED | Lovable URL is canonical; custom domain not approved | Owner chooses/approves domain later |
| PWA | CONNECTED + NOT VERIFIED | Production advertises manifest and mobile metadata | Verify install/service worker after source sync |
| Apple Developer | OWNER ACTION REQUIRED | Native signing/submission requires owner account | Request after canonical app build exists |
| App Store Connect | OWNER ACTION REQUIRED | No app record/submission performed | Request after iOS project exists |
| Google Play | OWNER ACTION REQUIRED | No app record/release performed | Request after Android project exists |
