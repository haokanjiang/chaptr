# Timeline design contract

Timeline appearance is AI-directed but rendered through a stable component. Save `timeline-design.json`:

```json
{
  "theme": "tech",
  "background": "#101827",
  "foreground": "#f5f7ff",
  "muted": "#a5b5cc",
  "accent": "#42cfb0",
  "transition": "#4577d4",
  "motion": "smooth",
  "display": "proportional"
}
```

Themes: `tech`, `travel`, `game`, `minimal`. `motion`: `smooth` or `linear`. The renderer validates hex colors, theme and layout. If omitted, deterministic theme defaults apply. Agent chooses design based on topic, not video genre stereotypes; keep names legible and contrast sufficient. Chapter spans always reflect elapsed duration, not equal-width decorative blocks. Never use AI-designed text lengths as timing signals. The default bottom bar is 104px tall, rendered as a separate video before joining under the source (not overlaying original pixels).

## Layout and labels

- The segment track represents chapter timing only. Allocate segment widths by elapsed duration and fill them from playback progress.
- For videos around 10–30 minutes, target 6–8 chapters by merging adjacent subtopics that belong to one continuous explanation.
- Write chapter titles in the selected subtitle language. If the selected captions contain multiple languages, ask the user which language to use before creating chapter titles.
- Put the active short chapter title, chapter index, and playback time in a separate padded header. Keep the title faithful to the source chapter or transcript meaning; prefer no more than 8 Chinese characters or 28 Latin characters.
- Do not place every chapter title in a second row sized by segment duration. Short segments cannot fit readable labels, so that layout truncates most titles. The active title in the header identifies the current segment.
- Bound the active title to the full track width and truncate only as a last-resort safeguard. Never let chapter text overflow past the track or canvas edges.
- The segment track spans the full 1920px canvas and aligns with both edges of the source picture. Apply horizontal padding to header content, not the track.
- Match the timeline base to the source picture's lower edge color. If that color changes across scenes, use black or another neutral that blends with the video's usual lower edge; let the progress accent carry the visual identity.
- Keep progress colors restrained: use one theme accent for completed chapters and a gradient between the theme accent and one transition color for the active chapter. Keep upcoming segments neutral and dark; do not cycle a rainbow palette across chapters.
- After rendering, inspect at least one frame from the start and one later chapter. Confirm the active title is readable, progress is apparent, and the track remains edge-aligned.
