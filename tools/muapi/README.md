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

For the Codex integration in this repo, authentication is handled by the official MuAPI CLI rather than storing the key in `.codex/config.toml`.

Add the key once with:

```bash
bash tools/muapi/run_cli.sh auth configure
```

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

Bootstrap the local CLI, Codex MCP registration and macOS GUI credential bridge with:

```bash
bash tools/muapi/bootstrap_codex.sh
```

After adding or rotating the key, rerun the bootstrap and verify with:

```bash
bash tools/muapi/bootstrap_codex.sh
bash tools/muapi/verify_codex.sh
```

Then fully quit and reopen Codex/VS Code so the GUI process uses the current login-session environment.

The Codex project config contains no MuAPI credential.

## macOS credential bridge for MCP

The official MuAPI CLI stores an API key in the macOS Keychain under service `muapi-cli` and account `api-key` when Keychain access is available.

Interactive CLI commands can read that Keychain entry, but a Codex-launched MCP child process may not be able to resolve the same Keychain backend. The integration therefore uses a two-stage runtime bridge:

1. `bootstrap_codex.sh` runs from an interactive Terminal and reads the already-configured MuAPI credential from Keychain (or the official MuAPI credential resolver);
2. it seeds `MUAPI_API_KEY` into the current macOS user `launchd` session with `launchctl setenv`;
3. after Codex is restarted, `run_mcp.sh` first tries the normal environment and Keychain path, then falls back to `launchctl getenv MUAPI_API_KEY`;
4. the value is exported only into the MuAPI MCP child process before `muapi mcp serve` starts.

This bridge does **not** write the secret to Git, `.codex/config.toml`, `.env`, project files, command arguments, or logs.

`launchctl setenv` keeps the value in the current macOS login session, so other processes running as the same user may be able to query that environment value. When rotating or removing the MuAPI credential, rerun the bootstrap with the new key or clear the session value with:

```bash
/bin/launchctl unsetenv MUAPI_API_KEY
```

Then quit and reopen Codex/VS Code.

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

For clients that support authenticated Streamable HTTP directly, use the bearer token from a secure environment variable or secret store. Do not hard-code the bearer token in committed configuration.

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
