# Third-party notices

Chaptr integrates and adapts source from **JZSub**, https://github.com/pengchujin/jzsub, at upstream commit `222a90265d2a8797ca258eb1a980cee0863a8311`.

- `skills/chaptr/scripts/media_fetch.py` originated as JZSub `skills/jzsub/scripts/fetch_video.py`.
- `skills/chaptr/scripts/subtitle_source.py` originated as JZSub `skills/jzsub/scripts/subtitle_pipeline.py`.
- Chaptr's `chaptr.py` consumes the upstream download manifest and the source-locked SRT Cue Ledger, but implements semantic chapter analysis and final video composition itself.

The source was originally licensed under MIT. The original license is reproduced below:

```text
MIT License

Copyright (c) 2026 pengchujin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
