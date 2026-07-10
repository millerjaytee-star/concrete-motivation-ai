# FFmpeg Export Workflow

Concrete Motivation uses local ffmpeg for MP4 export.

## Resolution order

1. `--ffmpeg-bin` passed to the script
2. `CONCRETE_MOTIVATION_FFMPEG_BIN`
3. `imageio-ffmpeg` bundled binary in the virtual environment
4. `/usr/bin/ffmpeg`
5. `ffmpeg` on `PATH`

## Diagnostics

Check the active encoder:

```bash
python3 scripts/check_ffmpeg.py
```

## Reel generation

Generate the first three vertical reels:

```bash
python3 scripts/make_first_3_reels.py
```

Use a specific build tree if you have compiled ffmpeg locally:

```bash
python3 scripts/make_first_3_reels.py --ffmpeg-bin /Users/jayteemiller/Downloads/ffmpeg-8.1.2
```

The script will accept a direct binary path or a directory containing `ffmpeg`, `bin/ffmpeg`, or `build-test/bin/ffmpeg`.
