# Pelican images

Used by the 🐦 slide in `index.qmd` (`#pelican-grid`). Each SVG is the unedited response to the
prompt "Generate an SVG of a pelican riding a bicycle", from Simon Willison's runs of one model at one
`thinking_effort`, extracted from the transcripts below on 2026-11-06. One run per cell, so a
difference between two neighbouring cells can be chance.

No licence is stated on the gists or on simonwillison.net. The images are credited and linked on
the slide; ask the author before reusing them elsewhere.

| File | Model | Effort | Input tokens | Output tokens | Input $/M | Output $/M | Cost (¢) |
|---|---|---|--:|--:|--:|--:|--:|
| `haiku-low.svg` | claude-haiku-5-5 | low | 27 | 1,867 | 0.10 | 0.50 | 0.09 |
| `haiku-medium.svg` | claude-haiku-5-5 | medium | 27 | 2,796 | 0.10 | 0.50 | 0.14 |
| `haiku-high.svg` | claude-haiku-5-5 | high | 27 | 5,034 | 0.10 | 0.50 | 0.25 |
| `sonnet-low.svg` | claude-sonnet-5-5 | low | 27 | 1,623 | 2 | 10 | 1.63 |
| `sonnet-medium.svg` | claude-sonnet-5-5 | medium | 27 | 1,796 | 2 | 10 | 1.80 |
| `sonnet-high.svg` | claude-sonnet-5-5 | high | 27 | 2,334 | 2 | 10 | 2.34 |
| `opus-low.svg` | claude-opus-5-5 | low | 27 | 1,891 | 4 | 20 | 3.79 |
| `opus-medium.svg` | claude-opus-5-5 | medium | 27 | 2,941 | 4 | 20 | 5.89 |
| `opus-high.svg` | claude-opus-5-5 | high | 27 | 3,366 | 4 | 20 | 6.74 |
| `fable-low.svg` | claude-fable-5-1 | low | 27 | 1,998 | 10 | 50 | 10.02 |
| `fable-medium.svg` | claude-fable-5-1 | medium | 27 | 1,977 | 10 | 50 | 9.91 |
| `fable-high.svg` | claude-fable-5-1 | high | 27 | 2,612 | 10 | 50 | 13.09 |

Cost = (input tokens × input price + output tokens × output price) / 1,000,000, in cents. The formula
reproduces the costs the author published for the Opus and Fable cells and for Haiku on low.
List prices from <https://platform.claude.com/docs/en/about-claude/pricing>, checked 2026-11-06.

Sources:

- Haiku 5.5: <https://gist.github.com/simonw/485dfa24b4efa1267ee2d0911594fb81>
- Sonnet 5.5: <https://gist.github.com/simonw/1d85a9be7f3ecce26e7f1569161a0d01>
- Opus 5.5: <https://gist.github.com/simonw/61fd7c3683fffce9a3ab7c43d1180024>
- Fable 5.1: <https://gist.github.com/simonw/17318f748f8c2b476051ddc2ebeb94a7>
- Series: <https://simonwillison.net/tags/pelican-riding-a-bicycle/>
- Timeline: <https://nilethebot.github.io/pelican-timeline/?ref=runtimewire>
