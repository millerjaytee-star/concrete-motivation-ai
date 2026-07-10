# Championship Launch System

This system aligns CEO Bot, YouTube, Gmail, Website, Stripe, ElevenLabs, FFmpeg, CRM, dashboard, and social handoff for the Concrete Motivation launch.

## Safety Rules

- Do not send emails from automation.
- Do not publish public YouTube videos from automation.
- Do not create live Stripe charges or payment links from automation.
- Do not commit secrets, OAuth tokens, generated credentials, or private lead data.
- Treat YouTube verification uploads as private until Jaytee gives explicit public approval.

## Verification

Run the local readiness report:

```bash
python scripts/verify_launch_system.py
```

Run the JSON version for dashboards or future automation:

```bash
python scripts/verify_launch_system.py --json
```

## Operating Flow

1. Use CEO Bot from the command center for launch sequencing.
2. Run the launch verification script.
3. Review `dashboard/launch_dashboard.html`.
4. Use `crm/lead_pipeline_template.csv` as the structure for local lead tracking.
5. Use `social_handoff/launch_handoff.md` for manual post review.
6. Use `scripts/test_youtube_upload.py` in dry-run mode before any private upload attempt.

The system is intentionally conservative. It prepares the launch so the next public move is deliberate, reviewed, and reversible.
