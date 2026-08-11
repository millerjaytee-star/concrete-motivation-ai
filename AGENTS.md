# Concrete Motivation repository instructions

## Canonical product

- Official Lovable project: **Concrete Motivation AI / concrete-motivation-app**
- Lovable project ID: `09f0d02d-8d41-40c7-9c36-bbdbf8d11adf`
- Production URL: <https://concrete-motivation-app.lovable.app>
- GitHub mirror: `millerjaytee-star/concrete-motivation-ai`
- Last owner-supplied canonical Lovable commit: `f52ad32139ebffea6b413a475b4dd46dd5585b2c` (`Rebuilt Concrete Nation public`)

Lovable is the product source of truth. GitHub is the collaborative, review, automation, and release mirror. Before changing production product code, Codex must obtain the newest Lovable source/export, verify its commit, and reconcile from Lovable into GitHub. When implementations conflict, Lovable wins unless Jaytee Miller explicitly approves the deviation.

`apps/web/`, `website/`, and generated/static previews are historical or supporting implementations until a reconciliation report explicitly verifies that they match the canonical Lovable source. They must not be deployed over the Lovable production project.

## Repository areas

- Production product mirror: future verified Lovable import; status tracked in `docs/LOVABLE_GITHUB_RECONCILIATION.md`
- Legacy/reference web implementation: `apps/web/` and `website/`
- AI and bot automation: `concrete_motivation/`, `concrete-motivation-bots/`, `Core/`, `prompts/`
- Automation and release scripts: `scripts/`
- Documentation: `docs/` and evidence reports at the repository root
- Tests: `tests/` and colocated web tests
- Release configuration: `.github/workflows/`, `config/`, deployment manifests

## Release safeguards

1. Never deploy a stale branch or the legacy application over Lovable production.
2. Never commit `.env` files, credentials, tokens, signing keys, private keys, Stripe secrets, or Google/Apple secrets.
3. Preserve working bot and media automation when reconciling product source.
4. Run canonical validation, web lint/typecheck/tests/build, Python tests, system check, secret scan, and route/integration verification before release.
5. Do not claim an integration is live without recorded verification evidence.
6. Production deployment, live Stripe activation, DNS changes, store submission, publishing, and consequential external writes require owner approval.
7. Keep a tested rollback target and identify the exact Lovable deployment/Git commit before any approved release.
