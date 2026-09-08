# MuAPI Unified Generative Media Integration

MuAPI is registered as the multi-provider generative-media gateway for the Concrete Motivation AI stack.

## Verified official surfaces

- Platform: https://muapi.ai
- REST API: https://api.muapi.ai/api/v1
- Hosted MCP: https://api.muapi.ai/mcp
- Official CLI repository: https://github.com/SamurAIGPT/muapi-cli
- CLI pin: `0.2.7`
- Source commit pin: `59c9b9f7c0432f89f048ba3db8e04d4d94b12cd8`
- CLI install: `npm install -g muapi-cli@0.2.7`

MuAPI exposes one API pattern for multiple image, video, audio, editing and 3D models. It also exposes an MCP server designed for coding agents and an official CLI.

## Why it matters for our stack

Use MuAPI as a routing/orchestration layer when we want one credential and one request pattern instead of maintaining separate provider SDKs.

Primary uses:
- Concrete Motivation image and video generation
- faceless YouTube production
- image-to-video and text-to-video
- lipsync and audio generation
- background removal, enhancement and editing
- 3D generation routes
- rapid model comparison before choosing a dedicated provider
- agent-driven media generation through MCP
- optional social publishing through the CLI transport

## Authentication

Do not commit credentials.

For the Codex integration in this repo, authentication is intentionally handled by the official MuAPI CLI rather than storing the key in `.codex/config.toml`.

Add the key once with:

```bash
muapi auth configure
```

During development, use a **Sandbox** key. Production keys can consume credits. Never run production generation as part of CI or automated tests.

## Codex integration

This repository includes a project-scoped Codex MCP entry at:

```text
.codex/config.toml
```

It launches the official local MCP server with:

```bash
muapi mcp serve
```

Bootstrap everything except the secret key with:

```bash
bash tools/muapi/bootstrap_codex.sh
```

After adding the key with `muapi auth configure`, verify the connection with:

```bash
bash tools/muapi/verify_codex.sh
```

The Codex project config contains no MuAPI credential. It only points Codex to the local `muapi mcp serve` process.

## Hosted MCP

Hosted endpoint:

```text
https://api.muapi.ai/mcp
```

For clients that support authenticated Streamable HTTP directly, use the bearer token from a secure environment variable or secret store. Do not hard-code the bearer token in committed configuration.

## CLI / stdio MCP

Install:

```bash
npm install -g muapi-cli@0.2.7
```

Run:

```bash
muapi mcp serve
```

This is the default Codex route for this repository because it keeps the secret out of project config and gives the agent local-file upload support.

## REST pattern

Submit:

```text
POST https://api.muapi.ai/api/v1/{model}
```

Poll:

```text
GET https://api.muapi.ai/api/v1/predictions/{request_id}/result
```

## Security and spend guardrails

- never commit MuAPI API keys
- use Sandbox keys for integration tests
- do not top up or consume credits without an explicit production-generation request
- keep model choice and estimated cost visible before expensive batch jobs
- do not put live API keys into shell scripts, GitHub files, prompts, or committed `.env` files
- verification scripts perform read-only account/model checks and submit no generation jobs

## Relation to our other tools

- TRELLIS.2 remains our dedicated open image-to-3D layer.
- LTX-2.5 Distilled remains our dedicated open synchronized audio-video layer.
- Runway and Higgsfield remain specialized creative providers.
- MuAPI becomes a **gateway/router** across many providers and media tasks.
- ChatGPT remains strategy, prompting, orchestration and review.
