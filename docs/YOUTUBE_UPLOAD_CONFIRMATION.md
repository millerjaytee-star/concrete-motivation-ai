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

