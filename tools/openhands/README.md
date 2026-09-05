# OpenHands Agent Canvas Integration

OpenHands is registered here as an external development tool for the Concrete Motivation AI engineering stack. Its source code is **not vendored into this repository**. GitHub remains the source of truth for project code; OpenHands acts as an execution/control layer around repo-scoped development work.

## Verified upstream

- Official repository: https://github.com/OpenHands/OpenHands
- Project: OpenHands Agent Canvas
- License: MIT
- Pinned stable release: `v1.16.0`
- Registry entry: `tools/registry.json`

OpenHands Agent Canvas can run the OpenHands software agent and can also connect to Codex and other ACP-compatible agents. This makes it useful as a common developer control center while preserving GitHub as the permanent record of code, branches, pull requests, and reviews.

## Role in our stack

Use the stack this way:

1. **ChatGPT** — strategy, requirements, research, architecture, review, and orchestration.
2. **GitHub** — source of truth for code, branches, issues, pull requests, and change history.
3. **Codex / OpenHands** — implementation and repo-scoped engineering execution.
4. **OpenHands Agent Canvas** — control center for switching between agents/backends and running repeatable engineering workflows.
5. **Production platforms** — deployment/runtime only after tests and review pass.

OpenHands does **not** replace GitHub, Codex, or ChatGPT. It gives us another execution layer and can coordinate multiple compatible coding agents from one interface.

## Guardrails

Default rules for all OpenHands work in this account:

- Work on a feature/chore/fix branch, never directly on `main` for substantive changes.
- Do not auto-merge production changes.
- Require human review for production-impacting pull requests.
- Do not place live Stripe keys, Supabase service-role keys, production database passwords, OAuth client secrets, or other production secrets in agent prompts or committed files.
- Mount only the project directories OpenHands needs.
- Do not give the agent unrestricted access to the whole Mac filesystem.
- Keep unrelated tools and projects in separate workspaces.
- Run the repository's existing tests and system checks before a pull request is considered ready.
- Preserve existing confirmation gates around uploads, email sends, payments, deployments, destructive database work, and other consequential actions.

## Recommended setup: Docker sandbox

Prerequisites:

- Docker Desktop
- A local directory containing only the GitHub projects you want OpenHands to access

Copy the environment template:

```bash
cd tools/openhands
cp .env.example .env
```

Edit `.env` and set an **absolute** project path, for example:

```text
PROJECTS_PATH=/Users/yourname/Projects
```

Then start the pinned OpenHands Agent Canvas release:

```bash
docker compose up -d
```

Open:

```text
http://localhost:8000/canvas
```

Stop it with:

```bash
docker compose down
```

The compose file pins `ghcr.io/openhands/agent-canvas:1.16.0` so an upstream release cannot silently change the local runtime.

## Alternative: local launcher

The upstream project also supports a direct launcher if Node.js 22.12+ and `uv` are installed:

```bash
npm install -g @openhands/agent-canvas
agent-canvas
```

This mode gives the agent broader local-machine access than the Docker workspace approach. For our default workflow, prefer the Docker sandbox.

## GitHub workflow

For any project OpenHands touches:

1. Pull the latest default branch.
2. Create a dedicated branch such as `feat/<work>` or `fix/<work>`.
3. Give OpenHands a narrowly scoped task with acceptance criteria.
4. Let the agent inspect, edit, and test only that project workspace.
5. Review the diff.
6. Run the project's canonical lint/typecheck/test/build commands.
7. Push the branch.
8. Open a pull request.
9. Merge only after required checks and review are complete.

## Initial projects to use with OpenHands

OpenHands can be useful for our GitHub engineering work across repositories, but each project should remain isolated. Do not combine their source trees just to make OpenHands available.

Good first uses:

- repo audits and dependency cleanup
- test generation and regression fixes
- issue-to-branch implementation
- build and deployment troubleshooting
- repetitive refactors
- documentation synchronization
- pull-request review preparation

## Verification checklist

Before calling this integration operational on a computer, verify:

```bash
docker --version
docker compose version
docker pull ghcr.io/openhands/agent-canvas:1.16.0
cd tools/openhands
docker compose config
```

Then launch it and confirm:

- Agent Canvas loads at `http://localhost:8000/canvas`.
- Only the intended projects are visible under `/projects`.
- A disposable test branch can be read and modified.
- No production secrets are visible in the mounted workspace.
- A simple test task can edit a file and run the repository's tests without touching `main`.

## What this GitHub integration does not do

Adding this folder does not magically make OpenHands a native ChatGPT connector in this chat. It establishes the approved GitHub-side integration, pinned runtime, security rules, and repeatable setup. To make OpenHands directly invokable from another assistant surface, that surface would still need an OpenHands/ACP/MCP-compatible connection or API endpoint.

## Upgrade procedure

Do not track `latest` in production workflows. When upgrading:

1. Check the newest official OpenHands release.
2. Read release notes for breaking changes and security changes.
3. Update the version in `tools/registry.json` and `docker-compose.yml` together.
4. Run `docker compose config`.
5. Pull the new image.
6. Test against a non-production repository/branch.
7. Commit the upgrade through a pull request.

This keeps the tool reproducible and reviewable instead of silently changing underneath active projects.
