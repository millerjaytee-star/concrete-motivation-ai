-- Additive, non-destructive receipt ledger used by the Next.js Stripe webhook.
create table if not exists public.stripe_webhook_events (
  id bigint generated always as identity primary key,
  stripe_event_id text not null unique,
  event_type text not null,
  livemode boolean not null default false,
  payload jsonb not null,
  received_at timestamptz not null default timezone('utc', now())
);

alter table public.stripe_webhook_events enable row level security;

comment on table public.stripe_webhook_events is
  'Durable Stripe event receipt ledger. Unique event IDs provide webhook idempotency.';
