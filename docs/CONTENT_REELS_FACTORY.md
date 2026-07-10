# Content + Reels Factory

This repo now includes an offline-first content factory for Concrete Motivation.

## What It Produces

Each package generates:

- YouTube concept
- 60-second Reel script
- 30-second Short script
- 15-second hook
- Instagram caption
- Facebook caption
- LinkedIn post
- YouTube title, description, tags, and thumbnail notes
- Podcast segment
- Repurpose plan

Packages are saved under `outputs/content_packages/` as:

- `package.md`
- `package.json`
- `package.csv`

## Commands

Create one package:

```bash
python3 scripts/create_content_package.py "discipline after pressure" --audience "high school athletes"
```

Create a reels batch:

```bash
python3 scripts/create_reels_batch.py --theme "one brick at a time" --count 3
```

Create a 30-day content batch:

```bash
python3 scripts/create_30_day_content_batch.py --theme "Pressure Has a Purpose" --audience "students and fathers"
```

## Voice Rules

The generator keeps the copy:

- direct
- disciplined
- faith-aware
- family-aware
- practical
- built around pressure, consistency, and refusal to quit

It also carries the founder story through the package copy:

- losing multiple siblings
- overcoming adversity
- serving as a district leader
- raising six children
- building Concrete Motivation through pressure

## Publishing Rules

This factory does not post, upload, or send anything automatically.
Review the package first, then publish manually or through a confirmed workflow later.

