# Timeline design contract

Timeline appearance is AI-directed but rendered through a stable component. Save `timeline-design.json`:

```json
{
  "theme": "tech",
  "background": "#101827",
  "foreground": "#f5f7ff",
  "muted": "#a5b5cc",
  "accent": "#42cfb0",
  "segmentColors": ["#4577d4","#986deb","#42cfb0","#f3b652"],
  "motion": "smooth",
  "display": "proportional"
}
```

Themes: `tech`, `travel`, `game`, `minimal`. `motion`: `smooth` or `linear`. The renderer validates hex colors, theme and layout. If omitted, deterministic theme defaults apply. Agent chooses design based on topic, not video genre stereotypes; keep names legible and contrast sufficient. Chapter spans always reflect elapsed duration, not equal-width decorative blocks. Never use AI-designed text lengths as timing signals. The default bottom bar is 104px tall, rendered as a separate video before joining under the source (not overlaying original pixels).
