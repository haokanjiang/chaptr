# Architecture

Chaptr borrows the reliable division of labor pioneered by [JZSub](https://github.com/pengchujin/jzsub): yt-dlp for extraction, Python for deterministic checks, the active coding agent for language understanding, and FFmpeg for final media delivery. The media acquisition and subtitle parsing modules are derived from JZSub, kept directly inside Chaptr and credited under MIT.

Agent: SRT cue batches -> semantic topic boundaries -> chapter JSON. No separate paid LLM API required.
Deterministic core: immutable SRT hash -> cue ID references -> timestamp resolution -> validated chapter ranges.
Presentation: themeable Remotion-only timeline video -> FFmpeg vstack under original picture -> MP4.

Unlike an overlay, v0.1 pads the picture at the bottom, so original picture content is not obscured. Output width is 1920 and picture height is scaled; resulting canvas is not necessarily 16:9. Source audio is copied where compatible.

Known limitations: no ASR, no dynamic chapter-editing UI, no HDR guarantee, 1920-wide render, source subtitle language selection is simplistic, Remotion browser required. Always validate on real media before promising platform coverage.

References:
- https://github.com/pengchujin/jzsub
- https://github.com/pengchujin/livecanvas
- https://github.com/serenawangCU/chapter-progress-bar
