# MuAPI Unified Generative Media Integration

MuAPI is registered as the multi-provider generative-media gateway for the Concrete Motivation AI stack.

## Verified official surfaces

- Platform: https://muapi.ai
- REST API: https://api.muapi.ai/api/v1
- Hosted MCP: https://api.muapi.ai/mcp
- Official CLI repository: https://github.com/SamurAIGPT/muapi-cli
- CLI pin: `0.2.7`
- Source commit pin: `59c9b9f7c0432f89f048ba3db8e04d4d94b12cd8`
- Official PyPI package: `muapi-cli==0.2.7`

MuAPI exposes one API pattern for multiple image, video, audio and editing models. It also exposes an MCP server designed for coding agents and an official CLI.

## Why it matters for our stack

Use MuAPI as a routing/orchestration layer when we want one credential and one request pattern instead of maintaining separate provider SDKs.

Primary uses:
- Concrete Motivation image and video generation
- faceless YouTube production
- image-to-video and text-to-video
- lipsync and audio generation
- background removal, enhancement and editing
- rapid model comparison before choosing a dedicated provider
- agent-driven media generation through MCP
- optional social publishing through the CLI transport

## Authentication

Do not commit credentials.

Add the Sandbox key once with the official CLI:

```bash
bash tools/muapi/run_cli.sh auth configure
```

The interactive CLI prefers the OS Keychain/keyring. MuAPI's own credential resolver then checks, in order:

1. `MUAPI_API_KEY`
2. OS Keychain/keyring
3. `~/.muapi/config.json`

During development, use a **Sandbox** key. Production keys can consume credits. Never run production generation as part of CI or automated tests.

## Codex integration

This repository includes a project-scoped Codex MCP entry at:

```text
.codex/config.toml
```

It launches the MuAPI MCP server through:

```bash
bash tools/muapi/run_mcp.sh
```

Bootstrap the local CLI, Codex MCP registration and native MuAPI credential fallback with:

```bash
bash tools/muapi/bootstrap_codex.sh
```

Then verify with:

```bash
bash tools/muapi/verify_codex.sh
```

The Codex project config contains no MuAPI credential.

## Native config fallback for sandboxed MCP processes

On this Intel macOS setup, interactive MuAPI CLI commands can read the Keychain successfully while the Codex-launched MCP process cannot. The previous direct-Keychain and `launchctl` bridges therefore remain unreliable inside the Codex sandbox.

MuAPI itself officially supports `~/.muapi/config.json` as the final credential fallback. `bootstrap_codex.sh` now uses the already-configured MuAPI credential resolver from the pinned PyPI package and writes only the API key into that native config path while preserving any existing settings.

Security controls:

- directory: `~/.muapi` with mode `700`
- file: `~/.muapi/config.json` with mode `600`
- no secret is written to Git, `.codex/config.toml`, `.env`, project files, shell history, or logs
- the older `launchctl` credential bridge is cleared during bootstrap
- `verify_codex.sh` checks the file exists, has restricted permissions, and that `muapi mcp serve` reaches its ready state without printing the key

This is a local plaintext fallback protected by Unix file permissions, so it is less isolated than the macOS Keychain. It is used only because the sandboxed MCP child cannot access the Keychain. Treat the Mac user account itself as the trust boundary.

When rotating the MuAPI key, run:

```bash
bash tools/muapi/run_cli.sh auth configure
bash tools/muapi/bootstrap_codex.sh
```

For future production hardening, MuAPI also supports OAuth 2.0 `client_credentials` for agents with scoped, short-lived tokens. That is preferable to a long-lived production API key when we move beyond Sandbox testing.

## Intel macOS compatibility

The npm installer currently attempts to fetch a native Intel macOS release asset that is not present upstream. This repository therefore uses the official PyPI distribution instead.

The bootstrap script creates a private virtual environment at:

```text
~/.local/share/muapi-cli-0.2.7
```

and installs:

```bash
muapi-cli==0.2.7
```

from PyPI. The package is published as a universal Python wheel and requires Python 3.9+.

`tools/muapi/run_cli.sh` first uses a normal `muapi` command if one is already installed, then falls back to the private virtual environment. This avoids PATH issues in Codex and on Intel Macs.

## Hosted MCP

Hosted endpoint:

```text
https://api.muapi.ai/mcp
```

For clients that support authenticated Streamable HTTP directly, use a bearer token from a secure environment variable or secret store. Do not hard-code bearer tokens in committed configuration.

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
