# Email and Support Setup

Current status: Gmail is connected for authorized review workflows, but the canonical application delivery provider and production form persistence are not verified. Forms must never display “sent” merely because local validation passed.

Support categories: General Contact, Speaking Inquiry, Partnership, Sponsorship, Membership Help, Billing Help, Order Help, Technical Support, Account Help. Validate required fields, apply honeypot/rate limits, store consent/source safely, exclude secrets/payment-card data, create an immutable request ID, and route only after persistence succeeds. Email provider acceptance and CRM persistence are separate statuses.

Owner action: choose the transactional sender/domain, verify it with the provider, configure SPF/DKIM/DMARC through approved DNS changes, and add provider credentials only to Lovable secrets. Then test a single message per category to the approved business inbox and verify provider event, inbox receipt, CRM record, and failure UI.
