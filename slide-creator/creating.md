# Creating — scaffold a new presentation

Full mechanics of `/slide-creator create <name> [--public|--private]`. The repo is created with `<DEFAULT_VISIBILITY>` unless overridden by the flag.

---

## Steps

1. **Validate the name**: only `[a-z0-9-]`, no spaces.

2. **Check it doesn't exist**:
   - Local folder `<SLIDES_DIR>/<name>/` → if it exists, abort.
   - Remote repo `gh repo view <GITHUB_USER>/<name>` → if it exists, ask before continuing.

3. **Create the folder**: `mkdir -p <SLIDES_DIR>/<name>`.

4. **Copy templates** from `<this skill folder>/templates/` into the new folder:
   - `slides.md`
   - `package.json`
   - `.gitignore`
   - `README.md`
   - `REVISIONS.md` (initial state: `draft`)
   - `style.css` (includes a workaround for the Goto-dialog bug in Slidev 0.49.x)
   - `.github/workflows/deploy.yml`
   - `netlify.toml` (optional)

   Replace placeholders in each file:
   - `{{NAME}}` → deck name (kebab-case)
   - `{{TITLE}}` → readable title (convert kebab-case to Title Case)
   - `{{DATE}}` → current date `YYYY-MM-DD`
   - `{{REPO_URL}}` → `https://<GITHUB_USER>.github.io/<name>/`

5. **Install dependencies** (generates `package-lock.json`, **required for CI**):
   ```bash
   cd <SLIDES_DIR>/<name> && npm install
   ```
   Can take 1-2 minutes. **Wait for it to finish** before continuing — the lockfile must be in the first commit.

6. **Git init + first commit** (after `npm install` completes):
   ```bash
   cd <SLIDES_DIR>/<name>
   git init -b main
   git add -A
   git commit -m "init: slidev deck <name>"
   ```
   Verify `package-lock.json` is in the commit (the Pages workflow uses `npm ci` and fails without it).

7. **Create the GitHub repo** (defaults to `<DEFAULT_VISIBILITY>`):
   ```bash
   gh repo create <GITHUB_USER>/<name> --<visibility> --source=. --remote=origin --push
   ```
   Where `<visibility>` is `private` or `public` per `<DEFAULT_VISIBILITY>` or the flag.

8. **Enable GitHub Pages** (source: GitHub Actions):
   ```bash
   gh api repos/<GITHUB_USER>/<name>/pages -X POST -f build_type=workflow 2>/dev/null || true
   ```
   If it fails (already exists), continue silently. The workflow handles deploy from there.

9. **Output**:
   ```
   Presentation created: <name>

   - Path: <SLIDES_DIR>/<name>
   - GitHub: https://github.com/<GITHUB_USER>/<name>
   - Live (once the workflow finishes): https://<GITHUB_USER>.github.io/<name>/

   Commands:
     /slide-creator style <name>   # define the color palette
     /slide-creator dev <name>     # edit live
     /slide-creator build <name>   # static build
     /slide-creator export <name>  # export to PDF
   ```

---

## Notes

- The deck is born in `draft` state. See [`reviewing.md`](reviewing.md) for the approval flow.
- The deck is born **without a palette**. To define it: `/slide-creator style <name>` (see [`styling.md`](styling.md)).
- The `style.css` copied from templates carries the Goto-dialog workaround. The `style` command never touches it — it's user-owned.
