# Production Ownership

- **Source of truth:** this GitHub repository.
- **Public website:** `apps/web`, deployed by the root `netlify.toml` from protected `main`.
- **Member application:** must be migrated into this repository before the full platform can be certified; see `OWNER-ACTIONS.md`.
- **Database and authentication:** Supabase production ownership remains with Jaytee Miller. Schema, migrations, policies, and server integration must be version controlled here before release approval.
- **Payments:** Stripe production ownership remains with Jaytee Miller. Dashboard configuration and secrets stay outside Git; handlers, event contracts, and tests belong here.
- **Brand:** the approved brand constitution and Concrete Bible govern all implementation. The Six Pillars remain Foundation, Discipline, Resilience, Purpose, Leadership, and Legacy.
- **Deployment:** production infrastructure changes require a documented reason, reviewed repository change, passing release gate, and owner approval.
