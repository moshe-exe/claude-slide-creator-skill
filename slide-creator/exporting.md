# Exporting — PDF, PPTX, and PNG

Full mechanics of `/slide-creator export <name> [format] [options]`. Slidev exports natively via Playwright (`playwright-chromium`, already in `dependencies`). No extra tooling required.

**Default format:** `pdf`.

---

## Command resolution

`/slide-creator export <name> [pdf|pptx|png] [--range ...] [--dark] [--clicks]`

1. **Validate the deck.** Verify `<SLIDES_DIR>/<name>/` exists. If not, abort and suggest `/slide-creator list`.
2. **Verify deps.** If `node_modules/` doesn't exist, run `npm install` before exporting.
3. **Pick the format.** Default `pdf` if none passed. Accept `pdf`, `pptx`, `png`.
4. **Run the export** (see table below) **from the deck root**.
5. **Report the path** to the generated file and its size.

Always run `cd <SLIDES_DIR>/<name> &&` before the command — the entry (`slides.md`) and output are relative to the deck root.

---

## Commands per format

| Format | Command | Output |
|--------|---------|--------|
| **PDF** (default) | `npm run export` | `slides-export.pdf` |
| **PowerPoint** | `npm run export:pptx` | `slides-export.pptx` |
| **PNG** (1 img/slide) | `npx slidev export --format png` | `slides-export/` folder with one `.png` per slide |

The `export` and `export:pptx` scripts live in each deck's `package.json` (they come from the template). For any other combination, use `npx slidev export` directly:

```bash
cd <SLIDES_DIR>/<name>

# PDF (default)
npm run export
# = npx slidev export

# PowerPoint
npm run export:pptx
# = npx slidev export --format pptx

# PNG (one image per slide)
npx slidev export --format png
```

---

## Useful `slidev export` options

Apply to any format (go after `npx slidev export`):

| Flag | Effect |
|------|--------|
| `--output <path>` | Output file name/path |
| `--format <pdf\|pptx\|png\|md>` | Output format |
| `--range "1,4-5,8"` | Export only those slides |
| `--dark` | Export in dark theme |
| `-c, --with-clicks` | One page per click/animation (`v-click`) |
| `--with-toc` | Include outline/bookmarks (PDF only) |
| `--per-slide` | Render slide by slide (better with global components; breaks cross-slide links and TOC) |
| `--scale <n>` | Scale factor for PNG (sharpness) |
| `--timeout <ms>` | Per-page render timeout (raise it for heavy slides) |

Examples:

```bash
# Only the first 5 slides to PDF
npx slidev export --range "1-5"

# PPTX with animations expanded
npx slidev export --format pptx --with-clicks

# High-resolution PNG
npx slidev export --format png --scale 2

# Output with a custom name
npx slidev export --format pptx --output client-delivery.pptx
```

---

## Note on PPTX

Slidev renders **each slide as a full-page image** inside the `.pptx` (not editable text/shapes). It's ideal for **sharing or presenting** in PowerPoint/Keynote, but **not for editing** the content slide by slide.

> For native editing: export **PDF** and keep the Slidev deck (`slides.md`) as the source of truth. Re-export after each change.

---

## Troubleshooting

- **Playwright browser missing** (`Executable doesn't exist`): `npx playwright install chromium`.
- **`EISDIR` when using `--output`:** the output path is an existing folder. Pass a file name, not a directory.
- **Heavy slides / timeout:** raise `--timeout 30000` or use `--wait 500`.
- **Animations don't show up:** add `-c` / `--with-clicks` to expand each step.
- **Output goes to the wrong place:** confirm you're running from the deck root (`cd <SLIDES_DIR>/<name>`).

---

## Rules

- **Don't commit** exported files (`slides-export.*`, the `slides-export/` folder). They're artifacts; keep them out of git or in `.gitignore`.
- The **source of truth** is always `slides.md`, not the export.
