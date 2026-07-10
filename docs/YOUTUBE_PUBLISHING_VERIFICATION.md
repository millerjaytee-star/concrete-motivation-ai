# YouTube Publishing Verification

The YouTube verification harness is private-only and single-video only.

## Target Video

`generated_videos/01_built_under_pressure.mp4`

## Metadata

- Title: Built Under Pressure
- Description: Test upload from Concrete Motivation AI Operating System.
- Visibility: PRIVATE

## Dry Run

```bash
python scripts/test_youtube_upload.py
```

The dry run prints upload metadata and does not contact YouTube.

## Private Upload Gate

The script refuses execution unless both conditions are true:

1. The operator passes `--execute`.
2. The shell has `CONCRETE_ALLOW_YOUTUBE_UPLOAD_PRIVATE=yes`.

The script only accepts the one configured video path and keeps visibility locked to private.
