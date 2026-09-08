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

Do not commit credentials. Store the key in `MUAPI_API_KEY`.

During development, create a **Sandbox** key. Sandbox requests return mock data and do not consume production credits.

Production keys can consume credits. Never run production generation as part of CI or automated tests.

## Hosted MCP

Use:
`https://api.muapi.ai/mcp`

with:
`Authorization: Bearer $MUAPI_API_KEY`

The hosted MCP is the preferred low-friction agent route when the client supports authenticated Streamable HTTP.

## CLI / stdio MCP

Install:
`npm install -g muapi-cli@0.2.7`

Run:
`muapi mcp serve`

This route adds local-file upload capabilities and additional social publishing tools that depend on local filesystem access.

## REST pattern

Submit:
`POST https://api.muapi.ai/api/v1/{model}`

Poll:
`GET https://api.muapi.ai/api/v1/predictions/{request_id}/result`

## Security and spend guardrails

- never commit `MUAPI_API_KEY`
- use Sandbox keys for tests
- do not top up or consume credits without an explicit production-generation request
- keep model choice and estimated cost visible before expensive batch jobs
- use OAuth client credentials for autonomous agents when narrower scopes are appropriate
- do not embed API keys in URLs unless a client provides no header support

## Relation to our other tools

- TRELLIS.2 remains our dedicated open image-to-3D layer.
- LTX-2.5 Distilled remains our dedicated open synchronized audio-video layer.
- Runway and Higgsfield remain specialized creative providers.
- MuAPI becomes a **gateway/router** across many providers and media tasks.
- ChatGPT remains strategy, prompting, orchestration and review.
