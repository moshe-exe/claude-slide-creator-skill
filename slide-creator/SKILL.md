---
name: slide-creator
description: Slidev presentation manager — each deck is its own GitHub repo with automatic deployment to GitHub Pages
argument-hint: [list] | create <name> [--public|--private] | dev <name> | build <name> | export <name> | open <name>
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
---

# Slidev Presentation Manager

Each presentation is an independent Git repo, stored locally at `<SLIDES_DIR>/<name>/` and published to `github.com/<GITHUB_USER>/<name>`. Deployment to GitHub Pages happens automatically via GitHub Actions on every push to `main`.

---

## Configuration

Edit these values to match your setup. Claude reads them at runtime — references to `<GITHUB_USER>`, `<SLIDES_DIR>`, and `<DEFAULT_VISIBILITY>` throughout this skill resolve from this table.

| Variable | Value | Notes |
|----------|-------|-------|
| `GITHUB_USER` | `your-github-username` | GitHub user or org that owns new deck repos |
| `SLIDES_DIR` | `~/Repositories/slides` | Local directory where deck repos live (will be created if missing) |
| `DEFAULT_VISIBILITY` | `private` | `private` or `public` for newly created repos |

**Templates location:** `<this skill folder>/templates/` (relative to wherever you installed the skill).

---

## Commands

| Command | Description |
|---------|-------------|
| `/slide-creator` or `/slide-creator list` | List decks under `<SLIDES_DIR>` |
| `/slide-creator create <name>` | Scaffold + git init + push to GitHub + Pages workflow |
| `/slide-creator style <name> [palette]` | Define / regenerate the deck's color palette |
| `/slide-creator status <name>` | Show review state (`draft` / `review-N` / `approved`) |
| `/slide-creator review <name>` | Start or continue the next review round |
| `/slide-creator approve <name>` | Mark as approved (requires ≥ 2 completed rounds) |
| `/slide-creator polish <name>` | Optional visual review (layout, typography, spacing) |
| `/slide-creator illustrate <name>` | Add icons with shaped backgrounds (optional) |
| `/slide-creator dev <name>` | Run the dev server (`npm run dev`) |
| `/slide-creator build <name>` | Static build to `dist/` |
| `/slide-creator export <name> [pdf\|pptx\|png]` | Export to PDF (default), PowerPoint, or PNG |
| `/slide-creator open <name>` | Open the folder in your editor |

---

## No arguments

If `$ARGUMENTS` is empty or `list`, show:

1. List folders under `<SLIDES_DIR>/`.
2. For each, show whether it has a `.git/` and a configured remote.
3. Table:

```
Presentations (X)

| Name | Local | GitHub | Last edit |
|------|-------|--------|-----------|
| my-deck | ✓ | ✓ | 2026-06-02 |
```

Show available commands at the end.

---

## Command: create

**Trigger:** `/slide-creator create <name> [--public|--private]`

Scaffold the deck + `npm install` + git init + push to GitHub + enable Pages. Defaults to `<DEFAULT_VISIBILITY>`. The deck starts in `draft` state with no palette.

→ **Full 9-step flow, placeholders, gh API calls:** [`creating.md`](creating.md)

---

## Command: style

**Trigger:** `/slide-creator style <name> [palette]`

Defines the deck's color palette from [coolors.co](https://coolors.co/image-picker) (or from an existing palette). Writes `palette.json` (source of truth) and regenerates `uno.config.ts` (UnoCSS tokens + CSS variables + base rules via `preflights`). **Never touches `style.css`** — that file is user-owned (workarounds, typography, custom CSS).

**Accepted inputs:** coolors URL, coolors Object/Extended Array export, loose hexes, or no args (regenerates from `palette.json`).

**Roles:** `bg / fg / primary / primary-dk / accent`.

→ **Full mechanics, input formats, role mapping, and how to use the palette in slides:** [`styling.md`](styling.md)

---

## Command: dev

**Trigger:** `/slide-creator dev <name>`

1. Verify `<SLIDES_DIR>/<name>/` exists.
2. Verify `node_modules/` exists; if not, run `npm install`.
3. Launch the dev server **in the background**:
   ```bash
   cd <SLIDES_DIR>/<name> && npm run dev
   ```
4. Report the typical URL (`http://localhost:3030`) and how to stop it.

---

## Command: build

**Trigger:** `/slide-creator build <name>`

```bash
cd <SLIDES_DIR>/<name> && npm run build
```

Output lands in `dist/`. Show total directory size when done.

---

## Command: export

**Trigger:** `/slide-creator export <name> [pdf|pptx|png] [options]`

Exports the deck via Slidev (Playwright). Default format: `pdf`. Also supports `pptx` (PowerPoint) and `png`.

```bash
cd <SLIDES_DIR>/<name> && npm run export        # PDF (default)
cd <SLIDES_DIR>/<name> && npm run export:pptx   # PowerPoint
```

Generates the file at the deck root (`slides-export.pdf` / `.pptx`). Show the path to the generated file.

→ **Formats, flags (`--range`, `--dark`, `--with-clicks`, `--scale`), note on PPTX as images, troubleshooting:** [`exporting.md`](exporting.md)

---

## Command: open

**Trigger:** `/slide-creator open <name>`

Open `<SLIDES_DIR>/<name>` in the user's editor of choice (e.g. `code <SLIDES_DIR>/<name>` for VS Code, `zed <SLIDES_DIR>/<name>` for Zed). If unsure, prefer `code`.

---

## Review and approval

Every presentation is born as `draft` and needs **≥ 2 rounds** before it can be approved. State lives in `REVISIONS.md` inside the deck's repo.

Commands: `status` (view state), `review` (start / continue a round), `approve` (release `v1.0.0`, gated).

→ **States, `REVISIONS.md` schema, mechanics of each command:** [`reviewing.md`](reviewing.md)

---

## Command: polish

**Trigger:** `/slide-creator polish <name> [--parallel | --status]`

**Optional** visual review, orthogonal to content review. Handles layout, typographic hierarchy, margins, font-size, element placement — everything visual except color (that's `style`).

Takes screenshots via `slidev export --format png` (alternative: browser tools), iterates slide-by-slide in **sequential mode** while criteria are being built, and unlocks **parallel mode** once there are ≥ 5 established criteria. Edits go to `slides.md` and optionally `style.css`; the slide-by-slide log lives in `POLISH.md` inside the deck, screenshots in `polish/`.

**Criteria live in the skill** ([`polish-criteria.md`](polish-criteria.md)), not in the deck — what's learned on one deck applies to all of them. They start empty and grow with use.

→ **Full flow (setup, per-slide loop, modes, integrations):** [`polishing.md`](polishing.md)

---

## Command: illustrate

**Trigger:** `/slide-creator illustrate <name> [--parallel]`

**Optional** light illustration: adds icons (Phosphor via Iconify, already integrated in Slidev) over shaped backgrounds (circle, squircle) tinted with the deck's palette. Minimalist by design — few icons, high intention, chosen for what they mean relative to the content.

Requires a defined palette (`style`) and is best run **after** `polish` (on a stable layout). Uses a reusable `IconBadge.vue` component as the single source of truth for badge styling. Like `polish`: screenshot-driven, sequential while conventions are being built, parallel once there are ≥ 5.

The **conventions live in the skill** ([`icon-criteria.md`](icon-criteria.md)) — what's learned applies to every deck.

→ **Full mechanics (library, component, selection, shapes, flow):** [`illustrating.md`](illustrating.md)

---

## Rules

- **Never commit** `node_modules/`, `dist/`, or `.local` files.
- **One deck = one repo.** Don't nest multiple decks in a single repo.
- **GitHub Pages publishes automatically** via GitHub Actions on every push to `main`. The workflow lives in `.github/workflows/deploy.yml`.
- **New repos default to `<DEFAULT_VISIBILITY>`.** To flip an existing one public: `gh repo edit <GITHUB_USER>/<name> --visibility public --accept-visibility-change-consequences`.
- **No approval without 2+ review rounds.** The `approve` command is gated by `REVISIONS.md`. No bypass.
