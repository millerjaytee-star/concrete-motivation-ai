# YouTube Upload Workflow for Concrete Motivation

## Current Status
Composio shows YouTube is ACTIVE. The safest production path is to generate video assets locally, review them, then upload through the connected YouTube account or Composio action once the exact upload tool is confirmed.

## First 3 Videos
1. Built Under Pressure
2. Discipline After Motivation Leaves
3. The Leadership Standard

## Local Video Generation
Run:

```bash
pip install moviepy pillow
python3 scripts/make_first_3_reels.py
```

Generated files:

```text
generated_videos/01_built_under_pressure.mp4
generated_videos/02_discipline_after_motivation_leaves.mp4
generated_videos/03_the_leadership_standard.mp4
```

## YouTube Upload Metadata

### Video 1
Title: Built Under Pressure | Concrete Motivation
Description: You are not weak. You are under construction. Concrete Motivation helps people turn pressure into purpose through discipline, leadership, and action.
Tags: Concrete Motivation, motivation, discipline, leadership, purpose, built under pressure
Visibility: public or unlisted for first review

### Video 2
Title: Discipline After Motivation Leaves | Concrete Motivation
Description: Motivation starts the fire. Discipline keeps the lights on. Save this for the day you do not feel like showing up.
Tags: Concrete Motivation, discipline, motivation, mindset, comeback, leadership
Visibility: public or unlisted for first review

### Video 3
Title: The Leadership Standard | Concrete Motivation
Description: Leadership starts with the promises nobody sees you keep. Be present. Be accountable. Be disciplined.
Tags: Concrete Motivation, leadership, accountability, family, purpose, discipline
Visibility: public or unlisted for first review

## VP Quality Standard
Do not publish weak assets just because the automation can publish them. If the AI-generated placeholders do not look strong enough, record real vertical clips on phone and use these scripts as the spoken words.
