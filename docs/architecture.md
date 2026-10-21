# Architecture

Chaptr is a Codex-first pipeline for extracting subtitles, generating semantic chapters, and rendering an animated timeline below the original video.

Agent: SRT cue batches -> semantic topic boundaries -> chapter JSON. No separate paid LLM API required.
Deterministic core: immutable SRT hash -> cue ID references -> timestamp resolution -> validated chapter ranges.
Presentation: themeable Remotion-only timeline video -> FFmpeg vstack under original picture -> MP4.

Unlike an overlay, v0.1 pads the picture at the bottom, so original picture content is not obscured. Output width is 1920 and picture height is scaled; resulting canvas is not necessarily 16:9. Source audio is copied where compatible.

Known limitations: no ASR, no dynamic chapter-editing UI, no HDR guarantee, 1920-wide render, source subtitle language selection is simplistic, Remotion browser required. Always validate on real media before promising platform coverage.

