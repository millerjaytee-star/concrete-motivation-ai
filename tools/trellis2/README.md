# Microsoft TRELLIS.2 Integration

TRELLIS.2 is registered as the 3D-generation layer for the Concrete Motivation AI tool stack. The official source and model are **not vendored** into this repository; we pin their identities and the verified upstream Git commit so the integration remains reproducible without adding multi-gigabyte model files to GitHub.

## Verified sources

- Official GitHub: `https://github.com/microsoft/TRELLIS.2`
- Pinned upstream commit: `75fbf0183001ed9876c8dbb35de6b68552ee08bd`
- Hugging Face model: `microsoft/TRELLIS.2-4B`
- Official Hugging Face Space: `microsoft/TRELLIS.2`
- Task: image-to-3D
- License: MIT

The official implementation generates textured 3D assets with PBR material attributes and can export a `.glb` asset plus an `.mp4` turntable preview.

## Role in our stack

1. **ChatGPT** — choose or generate the source image, define asset requirements, and orchestrate the workflow.
2. **GitHub** — permanent source of truth for this integration, pinned upstream metadata, tests, and operating rules.
3. **Hugging Face** — model/Space discovery and remote compute route for `microsoft/TRELLIS.2-4B`.
4. **TRELLIS.2** — image-to-3D generation and PBR-ready asset extraction.
5. **to3D** — lightweight in-chat image-to-3D fallback/alternative when TRELLIS.2 GPU compute is unavailable.
6. **Runway / Higgsfield / Blender / web** — downstream animation, cinematic rendering, editing, or interactive 3D presentation.

## Execution routes

### A. Connected Hugging Face route — preferred

The ChatGPT Hugging Face connection can inspect the official model and Space and can submit Hugging Face Jobs when the account has compute entitlement. This keeps the heavy model off the local Mac.

At integration verification on **2026-09-08**, model and Space access were confirmed, while a Hugging Face Jobs execution probe returned HTTP `402 Payment Required`. The tool registration is valid; GPU execution through Jobs requires Hugging Face compute credits/billing or another supported GPU host.

### B. Official Hugging Face Space

The official Space is `microsoft/TRELLIS.2`. To inspect its callable Gradio endpoints from a development environment:

```bash
python -m pip install -r tools/trellis2/requirements.txt
python tools/trellis2/trellis2_tool.py probe-space
```

Set `HF_TOKEN` only when needed. Never commit it.

### C. Supported Linux/NVIDIA host

Microsoft documents the official local implementation as tested on Linux with an NVIDIA GPU with at least 24 GB VRAM; CUDA 12.4 is recommended. Use the pinned source instead of tracking `main` silently:

```bash
python tools/trellis2/trellis2_tool.py clone-command
```

Then follow Microsoft's `setup.sh` instructions inside the cloned TRELLIS.2 repository.

Do **not** try to make the Intel/AMD Mac the default TRELLIS.2 runtime. Use it as the control machine and run TRELLIS.2 on Hugging Face or another qualifying Linux/NVIDIA GPU host.

## Health checks

```bash
python tools/trellis2/trellis2_tool.py status
python tools/trellis2/trellis2_tool.py check-image path/to/input.png
python -m pytest tests/test_trellis2_tool.py
```

## Output contract

A successful TRELLIS.2 asset generation should preserve, when available:

- source image reference
- model id and pinned integration version
- seed and generation settings
- `.glb` PBR-ready 3D asset
- `.mp4` turntable/preview render
- downstream destination (website, Blender, Runway, Higgsfield, or asset library)

Do not commit generated model weights, Hugging Face caches, secrets, or large generated 3D/video outputs into the application repository by default.

## What “added to tools” means

This folder makes TRELLIS.2 an approved, documented, pinned external tool in our GitHub operating stack and ties it to the connected Hugging Face model/Space. A GitHub registry entry cannot by itself create a new native ChatGPT connector button. In ChatGPT, Hugging Face remains the execution/discovery bridge and `to3D` is the current native image-to-3D plugin; TRELLIS.2 is the higher-fidelity GPU backend we can invoke when compute is available.
