# Polishing — visual review (layout, typography, spacing)

Full mechanics of `/slide-creator polish <name>`. This is an **optional** review process, orthogonal to content review (`review`). It handles how each slide renders: distribution, hierarchy, sizes, margins, font-size, placement. It **does not** touch color or palette (that's `style`).

---

## When to run `polish`

- **After** `review` (content is stable) and **before** or **after** `approve`.
- It's optional: a deck can be approved without polish. If polish happens later, commits land as `polish: <slide>` with no need to re-tag.
- If content changes post-polish, affected slides need re-polishing (the skill detects this by comparing the mtime of `slides.md` against screenshots in `polish/`).

---

## Modes

### Sequential (first use, default mode)
Processes slides one by one, **live with the user**. Each slide is a small conversation: Claude observes, proposes, the user confirms, edits are applied, slide is re-screenshotted. **Criteria are built during this mode** and live in [`polish-criteria.md`](polish-criteria.md).

### Parallel (available once criteria exist)
Processes all pending slides in parallel, applying established criteria. Claude doesn't ask — it applies the heuristics, records what was applied in `POLISH.md`, and leaves before/after screenshots. The user reviews at the end.

> **Rule:** while `polish-criteria.md` has fewer than ~5 solid criteria, **force sequential mode** even if the user asks for parallel. Without criteria, there's no agent that knows what to do.

---

## Screenshot tooling

### Default: `slidev export --format png`

```bash
cd <SLIDES_DIR>/<name> && npm run export -- --format png --output polish/
```

Generates one PNG per slide (`01.png`, `02.png`, …) in the `polish/` folder. Advantages:
- Native to the stack (no external dependencies)
- Reproducible — the dev server doesn't need to be running
- Predictable filenames
- Uses the same renderer as the production build → "what you see is what gets published"

The command reuses the Playwright browser that's already in the deck's `dependencies`. If it fails due to a missing chromium:
```bash
npx playwright install chromium
```

### Alternative: browser tooling

If `slidev export` fails on the user's machine or you need to capture **intermediate states** (overlays, builds paused at step N), you can use:

- **Browser automation MCP** — navigate manually to `localhost:3030/N` and screenshot. Requires the dev server to be running.
- **Playwright directly** — write a `polish/capture.ts` script that iterates slides and captures. More flexible but more code.

These alternatives are **optional**, depending on the user's setup. **The skill always starts with `slidev export`**; if it fails, it proposes one of the alternatives.

---

## Sequential flow — step by step

### Setup (first time in the deck)

1. Verify that `<SLIDES_DIR>/<name>/` exists.
2. Verify that the deck has stable content (ideally `review-2` or higher; if it's `draft`, warn and ask for confirmation).
3. Create `polish/` if it doesn't exist.
4. Capture all slides:
   ```bash
   cd <SLIDES_DIR>/<name> && npm run export -- --format png --output polish/
   ```
5. Rename outputs to `NN-before.png` (raw output is `NN.png`).
6. Create `POLISH.md` with initial state (`in-progress`, `0/N polished`).

### Per-slide loop

For each pending slide:

1. **Show context:**
   - Screenshot `polish/NN-before.png`
   - Corresponding fragment of `slides.md` (between the `---` markers of the slide)
   - Layout declared in the slide's frontmatter (if any)

2. **Apply current criteria** (from `polish-criteria.md`).
   - If the file is empty → Claude observes open-endedly with obvious principles (readability, hierarchy, balance, density).
   - If it has criteria → explicit checklist.

3. **Propose:** list of observations + concrete edits (don't apply yet).

4. **User feedback:**
   - Accept / reject / modify edits
   - If an observation reveals a **general principle** (not specific to this slide), propose adding it to `polish-criteria.md`

5. **Apply edits:**
   - To `slides.md`: layouts, UnoCSS classes, reorganized content, slide frontmatter
   - To `style.css`: custom typo/spacing if necessary (careful: `style.css` is user-owned — append at the bottom, don't break the Goto workaround)
   - **Never to `uno.config.ts`** — that's managed by `style`

6. **Re-screenshot the specific slide:**
   ```bash
   cd <SLIDES_DIR>/<name> && npm run export -- --format png --output polish/ --range NN
   ```
   Rename to `NN-after.png`.

7. **Show visual diff:** before vs after side-by-side.

8. **Confirm and commit:**
   ```bash
   git add slides.md style.css polish/NN-*.png POLISH.md polish-criteria.md
   git commit -m "polish(slide-NN): <summary>"
   ```

9. **Update `POLISH.md`** with the slide's entry and advance the counter.

10. Move to the next slide. If the user says "pause", the skill remembers where it stopped (`POLISH.md` has the state).

### Completion

When all slides are polished:

1. Mark `POLISH.md` as `completed` with date.
2. Final commit: `polish: complete <name>`.
3. Push.
4. Suggest tag/release if there wasn't a `v1.0.0` yet, or a patch (`v1.0.1`) if it was already approved.

---

## Parallel flow (when criteria exist)

Available via `/slide-creator polish <name> --parallel`. Requires `polish-criteria.md` with ≥ 5 established criteria.

1. Setup is the same as sequential (capture before-screenshots).
2. **For each pending slide, launch an agent** (`Agent` tool, `subagent_type: general-purpose`) with:
   - Path to the before-screenshot
   - Fragment of `slides.md`
   - Full contents of `polish-criteria.md`
   - Instruction: apply the criteria to the slide, return proposed edits without applying them
3. Collect proposals from all agents.
4. **Show the user a consolidated summary** — slide-by-slide, proposed edits.
5. User approves in bulk or slide by slide.
6. Apply approved edits, re-screenshot, commit, update `POLISH.md`.

> The user still needs to review visually — confidence in the criteria grows over time, but we don't get to auto-apply without human gating.

---

## File structure inside the deck

### `polish/` (committed)

```
<SLIDES_DIR>/<name>/polish/
├── 01-before.png
├── 01-after.png
├── 02-before.png
├── 02-after.png
└── ...
```

The PNGs stay in git as visual reference for future iterations and so a PR/diff shows the visual change. If the deck has many slides or images are heavy, consider Git LFS — but for normal decks (15-30 slides @ ~200kb each), it's not necessary.

### `POLISH.md` schema

```markdown
# Polish — <name>

**State:** in-progress | completed
**Started:** YYYY-MM-DD
**Last update:** YYYY-MM-DD
**Total slides:** N
**Slides polished:** M / N
**Current criteria count:** K (see polish-criteria.md)

---

## Slide 01 — <title or first line>

**Before:** polish/01-before.png
**After:** polish/01-after.png

**Observations:**
- Title started below the fold at 1024px
- 5 bullets, the last was a sub-idea of the 4th

**Edits applied:**
- slides.md: added `class: pt-8` to the slide's frontmatter
- slides.md: merged bullets 4+5 into one with a sub-item

**New criterion derived:** "Slides never start content below the visible fold at 1024px" → polish-criteria.md > Composition

**Commit:** abc1234

---

## Slide 02 — ...
```

---

## Command: `polish`

**Trigger:** `/slide-creator polish <name> [--parallel | --status]`

| Form | Behavior |
|------|----------|
| `/slide-creator polish <name>` | Sequential mode. Takes the next pending slide and starts the conversation. If there's no `POLISH.md`, initializes the full setup. |
| `/slide-creator polish <name> --status` | Just shows progress (`M / N polished`, last slide, current criteria). |
| `/slide-creator polish <name> --parallel` | Parallel mode. Requires ≥ 5 criteria in `polish-criteria.md`. If not, errors with a suggestion to continue in sequential. |

---

## Integration with `status` and `approve`

- **`/slide-creator status`** should include a polish line: `Polish: M/N slides | active criteria: K`.
- **`/slide-creator approve`** **does not require** completed polish. But if `POLISH.md` is `in-progress`, it warns: "deck approved with incomplete polish — slides X, Y, Z not polished".
- If a slide's content changed post-polish (mtime of `slides.md` > mtime of `polish/NN-after.png` and slide N was affected), `/slide-creator polish status` marks it as `re-polish needed`.

---

## Notes

- **No criteria, no parallel.** Force sequential. The quality of parallel depends on the quality of the criteria.
- **Criteria belong to the skill, not the deck.** What we learn on one deck serves all the others. That's why `polish-criteria.md` lives in the skill folder, not in the deck repo.
- **The slide-by-slide log does belong to the deck.** `POLISH.md` lives in the deck repo and is part of its history.
- **Don't polish on `draft`**, ideally. Polishing unstable content is wasted work when a slide gets deleted or rewritten during `review`.
