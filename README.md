# claude-slide-creator-skill

A [Claude Code](https://docs.claude.com/en/docs/claude-code) skill for managing [Slidev](https://sli.dev/) presentations end-to-end: scaffold a deck as its own GitHub repo, define its color palette, iterate through review rounds, and polish the visual layout — with automatic deployment to GitHub Pages.

Each presentation is an independent Git repo. The skill handles creation, styling, review, polish, build, and export through `/slide-creator` slash commands.

## What this skill does

| Command | What it does |
|---------|--------------|
| `/slide-creator` or `/slide-creator list` | List local decks |
| `/slide-creator create <name> [--public\|--private]` | Scaffold a new deck, init git, push to GitHub, enable Pages |
| `/slide-creator style <name> [palette]` | Define / regenerate the color palette (from coolors.co or hex codes) |
| `/slide-creator status <name>` | Show review state (`draft` / `review-N` / `approved`) |
| `/slide-creator review <name>` | Start or continue the next review round |
| `/slide-creator approve <name>` | Tag `v1.0.0` and release (requires ≥ 2 review rounds) |
| `/slide-creator polish <name>` | Optional visual review (layout, typography, spacing) |
| `/slide-creator dev <name>` | Run the dev server |
| `/slide-creator build <name>` | Build to `dist/` |
| `/slide-creator export <name>` | Export to PDF |
| `/slide-creator open <name>` | Open the folder in your editor |

## Install

1. Clone this repo:
   ```bash
   git clone https://github.com/<your-user>/claude-slide-creator-skill.git
   ```

2. Copy (or symlink) the `slide-creator/` folder into your Claude skills directory:
   ```bash
   # Personal (available everywhere)
   cp -r slide-creator ~/.claude/skills/

   # Or per-project (committed with the project)
   cp -r slide-creator <your-project>/.claude/skills/
   ```

3. Open `slide-creator/SKILL.md` and edit the **Configuration** section at the top to match your setup:
   - `GITHUB_USER` — your GitHub username (or org)
   - `SLIDES_DIR` — local directory where deck repos will live
   - `DEFAULT_VISIBILITY` — `private` or `public` for newly created repos

4. (One-time) Make sure you have the required CLIs available:
   - [`gh`](https://cli.github.com/) (logged in)
   - `node` ≥ 20 and `npm`
   - Optionally, [Playwright Chromium](https://playwright.dev/) for PDF/PNG export (`npx playwright install chromium`)

Restart Claude Code (or reload skills) and you should see `/slide-creator` in the slash command list.

## How it works

Every deck created by this skill:

- Lives at `<SLIDES_DIR>/<name>/` locally and at `github.com/<GITHUB_USER>/<name>` remotely.
- Ships with a GitHub Actions workflow (`.github/workflows/deploy.yml`) that publishes to GitHub Pages on every push to `main`.
- Starts in `draft` state with a `REVISIONS.md` file. The skill enforces ≥ 2 review rounds before `approve` will tag `v1.0.0`.
- Gets its palette from `palette.json` (source of truth) → generated `uno.config.ts` (UnoCSS tokens + CSS variables). User-owned `style.css` is never touched by the skill.
- Optionally goes through a visual polish loop. Polish criteria accumulate across decks in `polish-criteria.md` — what you learn on one deck applies to the next.

## Customizing

The skill is opinionated by design — Slidev + GitHub Pages + UnoCSS palette + review/polish workflow. To adapt it:

- **Different hosting?** Edit `slide-creator/templates/.github/workflows/deploy.yml` (Netlify config also included).
- **Different theme?** Edit `slide-creator/templates/slides.md` and `package.json`.
- **Different commands?** Edit `slide-creator/SKILL.md` and the referenced `*.md` files.

## License

Apache 2.0 — see [LICENSE](LICENSE).

## Acknowledgements

Built on top of [Slidev](https://sli.dev/) by Anthony Fu. Inspired by the [Anthropic skills](https://github.com/anthropics/skills) reference structure.
