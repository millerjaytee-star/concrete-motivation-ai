# Payment Link Setup

Concrete Motivation uses payment-link-ready placeholders only.

## Supported placeholders
- `CONCRETE_MOTIVATION_MONTHLY_PAYMENT_LINK`
- `CONCRETE_MOTIVATION_ANNUAL_PAYMENT_LINK`
- `CONCRETE_MOTIVATION_BOOKING_PAYMENT_LINK`
- `CONCRETE_MOTIVATION_SPONSOR_PAYMENT_LINK`

## Files
- `config/payment_links.example.json`
- ignored local config: `config/payment_links.local.json`

## Run it
```bash
python3 scripts/create_payment_link_config.py
python3 scripts/show_payment_link_status.py
```

## Safety
- Never store card numbers in the repo.
- Never commit real payment secrets.
- Use an ignored local config or environment variables for approved links.

