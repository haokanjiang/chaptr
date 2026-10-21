# Vendored JZSub components

Source: https://github.com/pengchujin/jzsub
Pinned commit: 222a90265d2a8797ca258eb1a980cee0863a8311
Files: `fetch_video.py`, `subtitle_pipeline.py`.
License: MIT; see `LICENSE`. Originals are vendored unmodified.

Chaptr delegates video probing, format selection, authentication retries, subtitles and SRT conversion to `fetch_video.execute(... --deliver video)`. Chaptr's SRT parsing and immutable cue provenance use the upstream `parse_srt_bytes` and `_build_cue_ledger` functions. Agent topic analysis and rendering are Chaptr-specific.

Update by reviewing the upstream diff, copying the two files and updating the pinned commit and license if necessary. Avoid editing vendor code directly.
