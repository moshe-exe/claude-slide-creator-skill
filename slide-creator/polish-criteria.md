# Polish Criteria — visual review heuristics

Heuristics the `slide-creator` skill applies during `/slide-creator polish`. This file **grows with use**: every time an observation during a polish session reveals a general principle (not specific to a single slide), it gets appended here.

The heuristics guide Claude in sequential mode and are the basis for parallel mode (which unlocks at ≥ 5 established criteria — see [`polishing.md`](polishing.md)).

---

## How to add a criterion

During `/slide-creator polish <name>`, if an observation applies beyond the specific slide:

1. Identify the **category** it belongs to (see below).
2. Phrase the rule in 1–2 lines, **actionable and verifiable**.
3. Append with: rule + why + example slide where it appeared.

A well-phrased rule can be verified **without opening Slidev**: just by reading `slides.md` or looking at a screenshot. If it needs "depends on context", it's probably an observation, not a criterion.

---

## Composition and space

- **C1 · Single block, vertically centered.** On "sparse" slides (≤ 6 lines of total content including the title), treat title + body as **a single block** and center it vertically. Inside the block, increase the spacing between elements relative to the default (more breathing room between title and body, between subtitle and content).
  **Why:** Slidev top-aligns by default; when content is scarce, the lower half stays empty and the slide feels "unfinished" or "rushed". Vertically centering as a block makes it feel intentional.
  **Origin:** real-world deck, slides 2, 3, 5, 6, 9, 10, 14, 16 (8 occurrences).

- **C2 · Mandatory breathing room when multiple styling treatments coexist.** When a slide combines several types of emphasis (bold, italic, inline code, callout, multiple heading levels, arrows ↑↓→), require explicit vertical spacing between elements. Don't trust default margins.
  **Why:** Without breathing room, the treatments read as visual noise instead of hierarchy.
  **Origin:** real-world deck, slides 6, 8, 12.

- **C3 · Callouts and diagrams get their own vertical padding.** Cards, callouts, blockquotes, diagrams, illustrations — all carry explicit vertical padding top and bottom. Never visually fused with the adjacent text band.
  **Why:** These elements have visual treatment distinct from the body text; without their own margin, the eye merges them as a single fused block, losing the hierarchy.
  **Origin:** real-world deck, slides 6, 14.

- **N2 · Header/description pairs with differential gap.** When multiple "question + answer" or "label + value" blocks stack vertically, the gap between header and its description is small (≈ `mt-2`) and the gap between pairs is large (≈ `mb-8`/`mb-10`).
  **Why:** Without gap contrast, 4 lines read as 4 flat items instead of 2 grouped units.
  **Origin:** real-world deck, slide 8.

---

## Hierarchy and typography

- **C4 · The title doesn't dominate.** On cover slides, the `h1` takes ≤ 40% of the slide's height. On internal slides, the `h1` feels intentional, not "as big as possible". If the title has to shrink so it doesn't crush the rest, shrink it.
  **Why:** A title that fills half a slide doesn't look elegant — it looks rushed, as if it were the only thing that matters.
  **Origin:** real-world deck, slide 1.

- **C5 · Visible size jump between heading levels.** If an `h2`/`h3` introduces ≤ 1 line of content, it must clearly look smaller than the `h1` — otherwise the slide reads as "header soup" with several headlines competing.
  **Why:** Without a clear jump, the eye doesn't find the focal point.
  **Origin:** real-world deck, slide 6.

- **C6 · Deliberate gap between title and subtitle.** When there's a subtitle or tagline below the `h1`, the vertical gap must be ≥ 1.5× the title's line-height. The default usually glues them too tight.
  **Why:** A subtitle stuck to the title reads as a second line of the title.
  **Origin:** real-world deck, slide 1.

- **N1 · Sibling paragraphs in parallel, same visual weight.** When several short paragraphs coexist with parallel function (e.g. 3 points the speaker will develop, an intro + two cofounder lines, a question followed by two options), all carry the same treatment — same size, weight, and opacity. If the theme applies a "lead" style (lowered opacity, gray) to the first `<p>` under the `<h1>`, neutralize it by wrapping the body in a `<div>` or with explicit CSS.
  **Why:** A dimmed line between solid lines breaks the parallelism; the eye reads "one main + two secondary" instead of "three equivalents". This is C9 (parallel columns) applied to paragraphs.
  **Origin:** real-world deck, slides 1, 2, 3.

- **N6 · Mini-labels instead of h3 when introducing ≤ 1 line.** If an `h3` just introduces a short phrase (not a section with its own content), replace it with a small label (uppercase, wide tracking, reduced opacity) in a `label / value` grid. Concrete refinement of C5.
  **Why:** Without this, the slide fills up with "h1 + two magenta h3s competing" — header soup. The mini-label resolves the conceptual dichotomy without creating fake headlines.
  **Origin:** real-world deck, slide 6.

---

## Layout patterns

- **C7 · Two-cols for diagram + supporting text.** When a slide combines a diagram/illustration with explanatory text, prefer a two-cols layout (diagram-left / text-right) over a vertical stack if the stack cramps the diagram.
  **Why:** Vertical stack compresses the diagram between text bands; two-cols gives it the full horizontal space.
  **Origin:** real-world deck, slide 14.

- **C8 · Body left-indent > title left-indent.** On sparse slides, the body carries slightly more left-padding than the title — slightly, not exaggerated. Creates soft hierarchy without needing bullets or cards.
  **Why:** Title flush-left + body with a slight indent guides the reading without needing explicit markers.
  **Origin:** real-world deck, slide 2.

- **C9 · Parallel columns → parallel treatments.** When a slide has two columns with analogous content, both use the same header treatment (same size, weight, color), same bullet type, same internal hierarchy.
  **Why:** Typographic asymmetry in analogous columns reads as carelessness.
  **Origin:** real-world deck, slide 9.

- **N4 · `two-cols-header` when both columns are parallel with a shared title.** If two columns carry analogous content and an `h1` that conceptually covers both, the `h1` goes above both columns using `layout: two-cols-header`, not inside one. Any footer/payoff that comments on both also goes full-width (`col-span-2`), not anchored under a single column.
  **Why:** A title inside one column breaks the parallelism from the start — one col begins with an `h1` while the other begins with a bold line. Asymmetry from the first pixel.
  **Origin:** real-world deck, slide 9.

- **N9 · Diagnostic prompt + criterion bullets belong to the diagram, not to the reveal.** When an axis/spectrum diagram includes a diagnostic prompt ("ask yourself: ...") and criterion bullets to locate yourself on the axis, group them visually with the diagram (same column/block). The `v-click` reveal is reserved for the insight or counter-example, not for the bullets that are already part of the main reasoning.
  **Why:** The criterion bullets are part of "how to use the diagram" — if they get delayed with `v-click`, the diagram looks incomplete at the start. The reveal should be surprise or depth, not completion.
  **Origin:** real-world deck, slide 14.

- **N10 · Axis/spectrum diagrams with flex + border, not ASCII dashes.** To render a binary axis "A ━━━━ B", use a flex layout with a border instead of repeated dash characters. Base pattern:
  ```html
  <div class="flex items-center text-lg font-mono">
    <span class="font-bold">A</span>
    <div class="flex-1 mx-3 border-t-2 border-current opacity-60"></div>
    <span class="font-bold">B</span>
  </div>
  ```
  Annotations under each end via `<div class="flex justify-between">`.
  **Why:** ASCII dashes (`━`, `─`, etc.) wrap unpredictably when the font size grows or the container width shrinks — the "line" breaks and the diagram stops reading. The CSS border scales with the container.
  **Origin:** real-world deck, slide 14 (second iteration).

---

## Tables

- **C10 · Column widths tuned for consistent wrap.** In tables, column widths must be tuned so the wrap is consistent between rows of the same column. Target: each column keeps the same line count across rows. If a row wraps to 3 when the rest fit in 2, reassign width between columns.
  **Why:** Irregular wrap generates broken visual rhythm; the table looks "broken" even if the content is correct.
  **Origin:** real-world deck, slide 7.

- **N3 · `table-layout: fixed` + explicit widths as default for slide tables.** The auto-layout that markdown renders by default assigns widths by content and tends to produce sub-optimal ratios. Apply `table-layout: fixed`, explicit per-column widths (percentages), and `white-space: nowrap` on columns with short identifiers (IDs, numeric ranges, labels ≤ ~12 chars).
  **Why:** Auto-layout is the root cause of inconsistent wraps; `fixed` is a technical prerequisite so C10 is applicable with precision. `nowrap` on atomic columns (e.g. "3. Demo + pitch", "36 – 48h") avoids accidental wraps that break the rhythm.
  **Origin:** real-world deck, slide 7.

---

## Lists

- **C11 · Summary lists: "bold headline / non-bold description" on separate lines.** For lists that summarize key points (closings, recommendations, summary), each item is: line 1 with a short headline in bold (without numbering if it's a long list; with numbering if they're sequential steps), line 2 with a brief description in normal weight.
  **Why:** Uniform structure eliminates the problem of "one line here, two full there, an orphan word on the next". Predictable visual rhythm.
  **Origin:** real-world deck, slide 17.

- **N7 · Explanatory tail after a bold = noise, cut it.** When a phrase already delivers the point in bold and is followed by a tail like "— they just have to…", "— basically…", "— that is…", remove the tail. The bold already carried the weight.
  **Why:** On dense slides, the tail dilutes the impact of the bold and adds words without hierarchy. If the point needs clarification, move the clarification to a separate line (C11/N2 style), not hung from the end.
  **Origin:** real-world deck, slide 12.

---

## Decorative elements

- **C12 · Zero emojis on slides.** No exceptions — including "semantic" emojis like ❌/✅ that look like they add meaning. If the idea is an error/solution comparison, use theme typography or color, not glyphs.
  **Why:** Emojis break the deck's editorial tone (elegant serif). Even the "functional" ones reduce the sense of intentionality.
  **Origin:** real-world deck, slides 12, 16, 18.

- **N5 · Concrete replacement for semantic glyphs.** Operational refinement of C12. Glyphs like ❌/✅/⚠️ used as column headers or comparison items are replaced by: (a) a typographic label with theme color (e.g. `color: var(--c-primary)` for "Error", `color: var(--c-fg)` for "How to avoid it") + weight 600, optionally with (b) unicode prefixes `× / ✓ / !` injected via CSS `::before` with opacity ~0.85.
  **Why:** "Zero emojis" in ALL uses, but the error/solution opposition needs fast scanning. Color + typography + ASCII-safe unicode give the contrast without breaking the editorial tone.
  **Origin:** real-world deck, slide 16.

---

## Closing / credits slides

- **C13 · Separate link categories into distinct blocks.** On closing slides, don't mix heterogeneous categories on the same line (personal profile · projects · tools). Each category goes in its own line or visual block.
  **Why:** A line with `github.com/foo · ProjectA · ProjectB` mixes "who I am" with "what I do" and reads as soup.
  **Origin:** real-world deck, slide 18.

- **N8 · Closing slide: max 3 info blocks, descending hierarchy.** The typical closing has "optional resource / personal identity / affiliations" or equivalent — each block in its own div, with **descending** visual weight (size/opacity) from top to bottom. Cap: 3 blocks. If there are more categories, it's better to move some to a previous slide or cut.
  **Why:** Without descending hierarchy, all links compete equally and the viewer doesn't know which to note down. More than 3 blocks turns the closing into a dense footer.
  **Origin:** real-world deck, slide 18.

---

## Confirmed positive patterns

These are not rules to apply — they are combinations that **work** and are worth preserving/replicating when they appear.

- **P1 · `layout: center` + small title + large payoff in bold + short tail** works perfectly for "title-payoff" slides with sparse content. *(real-world deck, slides 4, 15.)*
- **P2 · Comparison tables with balanced widths and succinct cells** look good without adjustments. *(real-world deck, slides 11, 13.)*

---

## Anti-criteria

Things that are **not** polish criteria (they go elsewhere):

- **Color, palette, chromatic contrast** → `style` / [`styling.md`](styling.md)
- **Content, messaging, clarity of the argument** → `review` / [`reviewing.md`](reviewing.md)
- **Deck setup, deploy, repo** → `create` / [`creating.md`](creating.md)

If an observation during polish touches color or content, mark it and redirect it to the corresponding command — don't add it here.
