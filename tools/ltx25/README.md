# LTX-2.5 Distilled Integration

LTX-2.5 Distilled is registered as an external audio-video generation tool for the Concrete Motivation AI stack. GitHub remains the source of truth for our integration code; Lightricks' official GitHub repository and Hugging Face model remain the source of truth for LTX itself.

## Verified upstream

- Official code: `https://github.com/Lightricks/LTX-2`
- Pinned commit: `a95ab856bf29407b6b066ede0abe1846050db56c`
- Upstream release at that commit: `1.3.0`
- Hugging Face model: `Lightricks/LTX-2.5`
- Official Space: `Lightricks/LTX-2.5`
- Distilled transformer: `diffusion_models/ltx-2.5-22b-distilled-transformer-bf16.safetensors`
- License: LTX-2.x Community License / model terms; review current terms before commercial deployment
- Model access: gated on Hugging Face

There is no separate official `Lightricks/LTX-2.5-Distilled` repository. The distilled transformer is a component inside `Lightricks/LTX-2.5`.

## What it does for our stack

Use LTX-2.5 Distilled for fast text-to-video and image-conditioned audio-video generation, synchronized sound/dialogue, cinematic B-roll, motivational shorts, faceless YouTube production, product spots, and operations/training simulations.

Recommended orchestration:

1. ChatGPT — script, shot plan, prompt, QA.
2. Image generation / approved brand photography — source frames or characters.
3. TRELLIS.2 — optional 3D assets.
4. LTX-2.5 Distilled — fast audio-video generation.
5. LTX DFR — higher-quality production render when warranted.
6. Runway / Higgsfield — specialty shots, finishing, edits.
7. Canva — graphics/thumbnails.
8. Metricool — distribution/analytics.

## Execution policy

The current Intel Mac should not be the heavy LTX runtime. The official quick start downloads roughly 66 GiB of model components and the practical production path assumes substantial accelerator memory. Use the official Hugging Face Space or a supported Linux/NVIDIA cloud GPU first.

Do not commit model weights, Hugging Face tokens, generated caches, or private source media.

## Gated model requirement

Before downloading checkpoints:

1. Open the official `Lightricks/LTX-2.5` model page.
2. Accept the model terms.
3. Authenticate with a Hugging Face Read token that can access gated repos.
4. Set `LTX25_TERMS_ACCEPTED=true` only after that acceptance.

## Tool helper

```bash
python tools/ltx25/ltx25_tool.py
```

It reports the pinned source, official model/Space, selected distilled checkpoint, and local runtime recommendation.

The helper can also be imported by repo automation to build reproducible clone, checkout, model-download and distilled-generation commands.

## Official distilled components

The integration expects:

- `diffusion_models/ltx-2.5-22b-distilled-transformer-bf16.safetensors`
- `text_encoders/gemma4-12b-with-proj-ltx-2.5-bf16.safetensors`
- `vae/ltx-2.5-video-vae-bf16.safetensors`
- `vae/ltx-2.5-audio-vae-bf16.safetensors`
- `latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors`

The official repository describes DistilledPipeline as the fast starting point and DFR as the slower production-quality path.

## Security and cost guardrails

- Never commit `HF_TOKEN`.
- Never commit model files or caches.
- Never launch paid cloud GPU jobs automatically.
- Use a feature branch for integration changes.
- Keep final publication/deployment behind existing review gates.
- Verify rights to source images, likenesses, music, voices, logos, and other media used in generation.
