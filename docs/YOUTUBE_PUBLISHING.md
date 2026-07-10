# YouTube Publishing

This repo now has a local YouTube publishing workflow built around Composio and the cached YouTube toolkit definitions.

## What Exists

- `scripts/check_composio_youtube.py` checks local Composio readiness and prints the cached YouTube action slugs.
- `concrete_motivation/youtube_publish_package.py` builds a publish package and the exact Composio execute command.
- `scripts/create_youtube_package.py` creates a package without uploading.
- `scripts/youtube_upload_dry_run.py` prints the exact upload command without running it.
- `scripts/youtube_upload_confirmed.py` only runs after the user types `UPLOAD TO YOUTUBE`.

## Exact YouTube Action

The cached upload action is:

```text
YOUTUBE_MULTIPART_UPLOAD_VIDEO
```

The execute shape is:

```bash
composio execute YOUTUBE_MULTIPART_UPLOAD_VIDEO --file <video-path> -d '<payload-json>'
```

The payload includes:

- `title`
- `description`
- `categoryId`
- `privacyStatus`
- `tags`

The upload default is private unless you override it.

## If YouTube Is Not Connected

Run:

```bash
composio link youtube
```

That opens the browser OAuth flow for the YouTube toolkit.

## Dry Run

Preview the upload package and command without uploading:

```bash
python3 scripts/youtube_upload_dry_run.py "your topic" --video-path path/to/video.mp4
```

## Confirmed Upload

Run the confirmed uploader only when you want to upload:

```bash
python3 scripts/youtube_upload_confirmed.py "your topic" --video-path path/to/video.mp4
```

When prompted, type:

```text
UPLOAD TO YOUTUBE
```

If the upload fails because the account is not connected, connect with `composio link youtube` and rerun the script.

## Recommended Flow

1. Build a video with the local reels pipeline or your own editor.
2. Create the package with `scripts/create_youtube_package.py`.
3. Review the dry run output.
4. Confirm the upload with the exact confirmation phrase.
5. Keep visibility `private` until you explicitly choose otherwise.
