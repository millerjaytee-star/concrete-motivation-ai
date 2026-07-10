# Revenue Commander

Revenue Commander stages the Concrete Builders Membership launch stack without sending emails or processing payments automatically.

## What it builds
- Revenue decision note
- Offer stack
- Membership plan
- Payment link map
- Website sales page summary
- Social sales campaign summary
- Gmail sales sequence summary
- CRM revenue actions
- Weekly revenue scoreboard

## Run it
```bash
python3 scripts/run_revenue_commander.py --theme "Concrete Builders Membership" --monthly-price 40 --annual-price 400
```

## Full revenue sequence
```bash
python3 scripts/create_membership_program.py --monthly-price 40 --annual-price 400
python3 scripts/create_payment_link_config.py
python3 scripts/show_payment_link_status.py
python3 scripts/update_revenue_website_pages.py
python3 scripts/create_social_sales_campaign.py --offer "Concrete Builders Membership" --days 14
python3 scripts/stage_membership_gmail_sequence.py --offer "Concrete Builders Membership"
python3 scripts/create_speaker_booking_package.py --segment schools --theme "Pressure Has a Purpose"
python3 dashboard/ceo_dashboard.py
python3 main.py
```

## Safety
- Do not store card numbers in this repo.
- Do not send email or process payment automatically.
- Use payment-link placeholders until approved external links are ready.
