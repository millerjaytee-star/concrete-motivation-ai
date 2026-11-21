# Command Center integrations

The existing Next.js application uses Composio Platform REST v3.1 for Google connections. Composio hosts OAuth, stores the provider tokens, and proxies the app’s allowlisted read-only requests. The Next.js API uses a server-side project key and the authenticated command center owner. The browser gets simplified status and preview rows.

## Configure an environment

Use separate Composio projects and OAuth connections for staging and production. Keep project keys in local ignored environment files or the deployment secret store. The project key should have the permissions to read auth configs, read private connected accounts, create Connect Links, and use **Proxy execute (Legacy)**. Composio uses that permission label for its v3.1 proxy endpoint.

| Server environment value | Purpose |
| --- | --- |
| `COMPOSIO_API_KEY` | Scoped project key that the server sends to Composio |
| `COMPOSIO_USER_ID` | Optional existing Composio connection owner ID for this single-owner deployment. Otherwise the app uses the verified Supabase owner ID |
| `COMPOSIO_GOOGLE_ACCOUNT_EMAIL` | Google mailbox, primary calendar and Drive identity to verify |
| `COMPOSIO_YOUTUBE_CHANNEL_ID` | Existing YouTube channel ID to verify via `mine=true` |
| `COMPOSIO_GMAIL_AUTH_CONFIG_ID` | Dedicated Gmail OAuth config ID |
| `COMPOSIO_GOOGLECALENDAR_AUTH_CONFIG_ID` | Dedicated Calendar OAuth config ID |
| `COMPOSIO_GOOGLEDRIVE_AUTH_CONFIG_ID` | Dedicated Drive OAuth config ID |
| `COMPOSIO_YOUTUBE_AUTH_CONFIG_ID` | Dedicated YouTube OAuth config ID |
| `COMPOSIO_<TOOLKIT>_CONNECTED_ACCOUNT_ID` | Optional server-only account pin, for example `COMPOSIO_GMAIL_CONNECTED_ACCOUNT_ID`, when multiple valid accounts match |

Create or review the four dedicated configs under **Platform → Auth Configs** in the existing project. Use the listed scopes. OAuth identity scopes such as `openid` and `userinfo.email` are allowed. The command center rejects configs containing other scopes. Reconnect existing provider grants after changing scopes. Google OAuth verification, Workspace app authorization, or a custom OAuth client may be required by the selected Google account and scopes.

| Integration | OAuth scope suffix | Verification and enabled read |
| --- | --- | --- |
| Gmail | `gmail.readonly` | Mailbox profile email must match. Preview up to six inbox messages with subject, sender and snippet |
| Google Calendar | `calendar.readonly` | Primary calendar ID must match. Preview up to six upcoming events |
| Google Drive | `drive.metadata.readonly` | Drive user email must match. Preview up to six recently modified file metadata records |
| YouTube | `youtube.readonly` | Channel ID must match an owned channel. Preview up to six uploads from its uploads playlist |

All listed Google OAuth scope suffixes use the `https://www.googleapis.com/auth/` prefix.

1. Open **Integrations & Permissions** as the command center owner. Select **Authorize** for the relevant connection.
2. Complete the provider consent presented by the project’s Composio-hosted Connect Link. Choose the intended business account or channel.
3. Return to the command center and select **Verify**. The result is **Verified** only after the connected account is active and a live read-only request matches the configured provider identity. Refreshing the registry repeats these checks for active connections. Use the displayed timestamp as evidence of the last successful probe.
4. Verify each workspace read. For an unintended Google grant, revoke it in the relevant Composio project and Google account, then authorize the intended account. If multiple active accounts match, configure the intended account pin before retrying.

The CLI human login grants CLI access to the selected Composio organization. It is a separate step from OAuth consent by Gmail, Calendar, Drive, or YouTube. A provider Connect Link is generated only by the configured Composio project. For a fresh interactive CLI login, run `composio login --no-wait --no-skill-install`. After completing the returned link, poll with `composio login --poll --timeout 40 --no-skill-install --yes`. The documented CLI login expires in ten minutes. Never put CLI credential files, project keys, or provider tokens into source control or chat.

## Scope and live evidence

The four core adapters were exercised with controlled HTTP responses in the automated suite. Live authorization and owner-account reads require the existing Composio project key, scoped auth configurations, and owner consent. The registry’s remaining entries describe documented capabilities or prerequisites and have no command center authorization controls. Google Docs, Sheets, GitHub, Supabase management, Notion, Stripe, Instagram, Facebook, TikTok and LinkedIn have documented Composio toolkits. Netlify has an official API. External CRM, scheduling and marketing vendors require a provider decision. Existing billing and mobile release data are separate from the new integration registry.

Gmail writes, Calendar invitations, Drive file contents, YouTube Studio analytics and publishing, and external CRM/social writes are outside the current adapter. The hosted Connect Link is the only external navigation URL returned by the authorization operation. Provider preview links are built from fixed Google or YouTube origins. The adapter excludes upstream error detail, provider headers, connected-account payloads, and tokens from results.

Composio supports trigger subscriptions and signed outbound callbacks. Live event delivery requires a configured public HTTPS endpoint, provider subscriptions, and the project’s webhook signing secret. Verify `webhook-id`, `webhook-timestamp`, and `webhook-signature` against the unmodified request body and use the event ID to deduplicate processing. The Composio trigger configuration was not applied or tested against a connected account.

## Rate limits and cost

Public Platform pricing checked November 21, 2026 lists Hobby at **$0/month**, including **1,000 Proxy Execute calls/month**. Pro lists **$29/month** with included credits and metered overages. The published Pro proxy add-on is **$0.0002 per proxy call**, in addition to the applicable tool-call rate, after allowances. Existing account terms may differ. No billing changes were made.

A full refresh of the four previews uses up to **14 Proxy Execute calls**. One identity probe is required per preview, and Gmail can make one additional metadata request per message. A registry refresh uses up to four further probes. One registry-plus-preview refresh daily for 31 days would use up to **558 proxy calls**, before explicit verification or other workflows. This fits the published Hobby proxy allowance as a standalone usage estimate. Hosting, database, model usage, and existing service charges are separate.

Composio documents **2,000 requests/minute** for Hobby and **10,000 requests/minute** for Pro, shared organization-wide, plus provider-specific limits. The adapter bounds preview volume and request time and reports rate limiting without retrying authorization writes.

- [Composio Platform pricing](https://composio.dev/pricing/platform)
- [Composio Platform authentication](https://docs.composio.dev/docs/authentication)
- [Composio managed authentication for application-owned tools](https://docs.composio.dev/docs/authentication/managed-auth-for-custom-tools)
- [Composio scope configuration](https://docs.composio.dev/docs/authentication/controlling-scopes)
- [Composio REST rate limits](https://docs.composio.dev/reference/rate-limits)
- [Composio trigger delivery and signature verification](https://docs.composio.dev/docs/setting-up-triggers/subscribing-to-events)
