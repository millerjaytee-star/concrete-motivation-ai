# Analytics

Current status: not verified against GA4 DebugView for the canonical Lovable build. Analytics must remain consent-aware and must not receive names, email addresses, payment details, support text, reflection text, or other sensitive content.

Approved event vocabulary: `page_view`, `membership_view`, `membership_checkout_start`, `membership_checkout_complete`, `merch_view`, `merch_checkout_start`, `merch_purchase`, `speaking_inquiry`, `partnership_inquiry`, `support_request`, `guide_open`, `guide_question`, `account_signup`, `account_login`, `challenge_start`, `challenge_complete`, `daily_brick_complete`, and `video_click`.

Events use stable content/offer IDs, coarse source, and success/failure state—not PII. Consent denial prevents nonessential storage/transmission. Before launch verify the official property/streams, internal traffic, referral exclusions (including Stripe), cross-domain behavior, data retention, DebugView events, duplicate suppression, and deletion/privacy handling.
