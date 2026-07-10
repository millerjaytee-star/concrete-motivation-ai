# YouTube Upload Confirmation

Concrete Motivation uses a manual confirmation gate before any YouTube upload.

## Rules

- Default visibility is `private`.
- Do not upload automatically.
- Typed confirmation must match exactly: `UPLOAD TO YOUTUBE`
- The confirmed Composio action is `YOUTUBE_MULTIPART_UPLOAD_VIDEO`

## Dry Run

Use this command to preview the exact upload command without uploading:

```bash
python3 scripts/youtube_upload_dry_run.py "topic" --video-path /path/to/video.mp4
```

## Confirmed Upload

Use this command only after typing the confirmation text:

```bash
python3 scripts/youtube_upload_confirmed.py "topic" --video-path /path/to/video.mp4
```

## Recovery

If the Composio connection fails, run:

```bash
composio link youtube
```

## Verification Upload

To run the private verification upload against the generated reel, use:

```bash
python3 scripts/test_youtube_upload.py
```

That script uploads only `generated_videos/01_built_under_pressure.mp4` with the title `Built Under Pressure` and the description `Test upload from Concrete Motivation AI Operating System.` It reports upload status, video ID, video URL, and channel name after the upload attempt.
