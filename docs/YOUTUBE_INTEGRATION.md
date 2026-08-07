# YouTube Integration

The official channel is verified as **Concrete Motivation**, handle `@concretemotivation444`, channel ID `UCUY3F-FRATp4djFYk64QElA`. The connected API previously returned live uploads, but the canonical Lovable source/API implementation is unavailable for inspection.

Use a server-side YouTube Data API integration or a non-secret channel feed, cache successful responses, retain last-known-good items, cap refresh frequency, and render an honest empty/error state. Never expose an API key with unrestricted scope. Curate newest uploads, Concrete Conversations, long-form motivation, Shorts, and featured content using actual playlist/video IDs. Re-verify channel identity before changing content.

Required environment configuration must live in Lovable secrets and may include a restricted server API key or managed OAuth connection plus channel/playlist IDs. Test quota handling, deleted/private videos, cache expiry, link destinations, thumbnails, captions, and mobile performance.
