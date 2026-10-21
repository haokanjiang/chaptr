# Chaptr

**Turn video transcripts into animated chapter timelines.**

## Requirements

- Python 3.10+, yt-dlp, FFmpeg/ffprobe
- Node.js 20+, Chromium (for Remotion)
- A coding agent (Codex/Claude Code) capable of reading/writing local files

## Quick start

```bash
git clone https://github.com/haokanjiang/chaptr.git
cd chaptr
python3 skills/chaptr/scripts/chaptr.py fetch "VIDEO_URL" --job jobs/demo
# Optional: --source-lang en --browser-cookies chrome
```

Or bring your own files:

```bash
python3 skills/chaptr/scripts/chaptr.py prepare --video /path/to/video.mp4 --srt /path/to/video.srt --job jobs/demo
```

Ask Codex to follow [skills/chaptr/SKILL.md](skills/chaptr/SKILL.md) (or install that directory as a Codex Skill). It will process short subtitle batches and generate `chapters.json`.

Then:

```bash
python3 skills/chaptr/scripts/chaptr.py finalize --job jobs/demo
cd renderer && npm install && node render.mjs --job ../jobs/demo && cd ..
python3 skills/chaptr/scripts/chaptr.py compose --job jobs/demo
python3 skills/chaptr/scripts/chaptr.py verify --job jobs/demo
```

Result: `jobs/demo/chaptr.mp4`. Customize styles with `jobs/demo/timeline-design.json` (see [design contract](skills/chaptr/references/design.md)). Includes built-in tech/travel/game/minimal palettes; the agent may propose its own colors.

Run Python unit tests:

```bash
python3 -m unittest discover -s tests -v
```

## Principles

Original SRT is not altered; timestamps are resolved from cue IDs instead of hallucinated by the model. Deterministic media tools handle transcoding and validation. The current agent handles creative chapter choices and optional visual art direction. The earliest version intentionally avoids a Web backend, subscriptions, databases and an external translation API.

Use only videos you are authorized to download. Chaptr does not circumvent DRM or access restrictions.

MIT license.
