# Launch Status

Verified 2026-08-07 (America/New_York). `READY` means evidence exists; it does not authorize an external action. Current gate: Step 1 Lovable/GitHub source synchronization.

| System | Status | Evidence | Next action | Codex / owner |
|---|---|---|---|---|
| Website | READY | Lovable production HTTP 200; deployment ID recorded | Import source, then full interactive QA | Both |
| GitHub sync | BLOCKED | canonical commit absent from all fetched refs | Lovable Git sync or source ZIP | Owner |
| CI | READY | PR #33 checks green on commit `3a4eebf`; web/Python workflows plus canonical guard | Keep green while canonical source is imported | Codex |
| Custom domain | OWNER ACTION REQUIRED | no approved DNS/domain change | approve domain and Lovable-provided records | Owner |
| Stripe test | BLOCKED | active connection; no payment links; source unavailable | import source/configure test secrets and E2E | Both |
| Stripe live | OWNER ACTION REQUIRED | live money intentionally disabled | approve after complete test evidence | Owner |
| Auth | BLOCKED | backend/source unavailable | inspect and test canonical provider | Both |
| Database | BLOCKED | schema/RLS unavailable | provide Lovable backend access/export | Owner |
| Owner role | BLOCKED | server-side role unverified | audited assignment after auth access | Both |
| Concrete Guide | READY | live UI and escalation copy observed | source, safety, rate-limit tests remain | Codex after import |
| Email | BLOCKED | Gmail connection exists; app delivery unverified | configure/test transactional provider | Both |
| YouTube | READY | official channel ID/handle verified | inspect canonical feed implementation | Codex after import |
| GA4 | BLOCKED | no current DebugView evidence | property/stream consent test | Owner + Codex |
| PWA | READY | manifest/mobile metadata advertised | service-worker/install device tests | Codex after import |
| iOS project | BLOCKED | canonical source missing | import source, then generate shell | Codex |
| TestFlight | OWNER ACTION REQUIRED | Apple account/signing required | account, Bundle ID, signing, submission approval | Owner |
| Apple submission | OWNER ACTION REQUIRED | not submitted | approve after TestFlight acceptance | Owner |
| Android project | BLOCKED | canonical source missing | import source, then generate shell | Codex |
| Google testing | OWNER ACTION REQUIRED | Play account/signing required | app record, signing, internal track | Owner |
| Google production | OWNER ACTION REQUIRED | not submitted | approve after testing requirements | Owner |
| Privacy | BLOCKED | live page/source scope not fully verified | behavior-based legal review | Owner/counsel |
| Terms | BLOCKED | live page/source scope not fully verified | legal review against actual offers | Owner/counsel |
| Refunds | BLOCKED | policy and checkout not reconciled | approve policy and match checkout | Owner |
| Support | BLOCKED | UI observed; persistence/delivery unverified | category-by-category E2E | Both |
| Security | BLOCKED | local scan clean; backend unavailable | source/backend audit and restore test | Both |
