# QR — QR codes of links as deck assets

Full mechanics of `/slide-creator qr <name> <url> [slug] [options]`. Generates a QR code from a link and drops it **inside the deck's repo** (`<deck>/assets/qr/<slug>.<ext>`) as an asset ready to insert in the presentation. Returns the markdown snippet to paste into `slides.md`.

Engine: [`segno`](https://segno.readthedocs.io) (Python, no heavy deps). Default **SVG** (vector, sharp at any scale). PNG optional.

**Script:** the `generate_qr.py` in this skill's folder.
**QRs are saved to:** `<deck>/assets/qr/<slug>.<ext>`

> **Dependency:** requires `segno` (`pip install segno`, or `uv add segno`). The `--round --png` combo also needs `Pillow` (`pip install Pillow`).

Orthogonal to the other steps, like `illustrate`: it leans on the palette (`style`) to tint with the deck's identity, and is best run on an already-stable layout.

---

## Options

| Flag | Effect |
|------|--------|
| `--brand` | Tints the modules with the palette's `fg` (dark) color |
| `--mono` | Forces black even if `--brand` is requested |
| `--round` | Rounded corners (card look) |
| `--png` | Generates a PNG in addition to the SVG |

---

## Command flow

1. **Validate the deck.** Verify `<SLIDES_DIR>/<name>/` exists. If not, abort and suggest `/slide-creator list`.
2. **Resolve the slug.** If not passed, derive it from the URL: domain or last path segment, in kebab-case (e.g. `https://example.com/launch` → `example-launch`). No extension.
3. **Resolve the color.**
   - Default: **black** (`#000000`) on white — maximum scannability.
   - With `--brand`: read `<deck>/palette.json`, take the hex of the `fg` role (usually the deck's dark color) and pass it as `--dark`. **Never** use a light color for the modules — a low-contrast QR won't scan. If `fg` isn't clearly dark, stay black and warn.
   - With `--mono`: force black even if `--brand` is requested.
4. **Resolve the shape.** With `--round`, add `--round` to the command (rounded corners). The radius stays inside the quiet zone so it doesn't clip the finder patterns. **Rounding clips the margin to transparent → it shines over colored backgrounds or inside a card with `ring`/`shadow`** (see below); over flat white it's barely noticeable.
5. **Generate.** Run the script:
   ```bash
   python3 <this skill folder>/generate_qr.py \
     --url "<url>" \
     --out <SLIDES_DIR>/<name>/assets/qr/<slug>.svg \
     --dark "<hex>" [--round]
   ```
   With `--png`: repeat the command with `--out ...<slug>.png` (segno regenerates).
6. **Return the snippet.** Show the file path and the block ready for `slides.md` (see layouts below). With `--round`, wrap it in a card with `ring`/`shadow`.
7. **Don't commit automatically.** Leave the asset in the deck's working tree; it gets versioned with the deck's next commit.

---

## Why a relative path (and not `public/`)

Decks are built with `slidev build --base /<deck>/` for GitHub Pages. There are two ways to serve images:

| Form | In `slides.md` | Survives `--base`? |
|------|----------------|--------------------|
| **Relative** (recommended) | `![](./assets/qr/x.svg)` | ✅ Vite processes, hashes, and applies the base |
| Absolute / `public/` | `![](/qr/x.svg)` | ⚠️ Fragile — tends to break on the Pages deploy |

That's why the QR is saved in `assets/qr/` (next to `slides.md`) and referenced with `./`. **Don't use `public/`.**

---

## Slide layouts

### 1. Centered QR with a call-to-action

```md
---
layout: center
---

# Try it now

<div class="flex flex-col items-center gap-4">
  <img src="./assets/qr/demo.svg" class="w-60" />
  <p class="text-lg opacity-80">example.com/demo</p>
</div>
```

### 2. QR beside the content

```md
# Join the beta

<div class="grid grid-cols-[1fr_auto] gap-8 items-center">
  <div>

  - Early access
  - Direct feedback to the team
  - Free during the pilot

  </div>
  <img src="./assets/qr/beta.svg" class="w-48" />
</div>
```

### 3. Several QRs in columns (closing / contact)

```md
<div class="grid grid-cols-3 gap-8 max-w-5xl mx-auto">
  <div class="flex flex-col items-center gap-3">
    <div class="text-lg font-semibold text-primary">LinkedIn</div>
    <img src="./assets/qr/linkedin.svg" class="w-36 rounded-2xl ring-1 ring-[var(--c-primary)]/40 shadow-md" />
    <a href="https://linkedin.com/in/your-handle" class="text-xs opacity-70 break-words leading-tight">linkedin.com/in/your-handle</a>
  </div>
  <!-- ...more columns... -->
</div>
```

A pattern that works well on a closing slide: caption + QR + clickable link, one column per destination.

> Always pair the QR with the **link in text** or a label of what it opens. If the QR fails (bad angle, focus), the text is the fallback.

---

## Rounded corners (`--round`)

`--round` generates the QR with rounded corners. The radius stays **inside the quiet zone** (the margin) so it doesn't clip the *finder patterns* — clipping them would break scanning. The script raises the `border` to 4 modules if needed.

Rounding clips the margin to **transparent**:

- **Over a colored background** → it looks like a card with rounded corners. That's where it shines.
- **Over flat white** it's barely noticeable. To make it stand out, wrap it in a card with `ring`/`shadow`:

```md
<div class="flex flex-col items-center gap-2">
  <img src="./assets/qr/linkedin.svg"
       class="w-32 rounded-2xl ring-1 ring-[var(--c-primary)]/40 shadow-md" />
  <div class="text-sm opacity-70">Let's connect · linkedin.com/in/your-handle</div>
</div>
```

The `ring` with a palette color (`--c-primary`) traces the rounded border and gives it identity; `rounded-2xl` on the `<img>` matches the SVG's own rounding.

> Tune the radius with `--radius <modules>` (capped to the quiet zone). For sharper corners, also raise `--border`.

---

## Size, contrast, and scannability

- **Contrast:** dark modules on a light background. With `--brand`, it uses the palette's `fg` (dark color) — identity without losing scannability. Avoid light tints.
- **Quiet zone:** the script leaves `border=2` (white margin). Don't butt the QR against another element's edge or overlay it on a textured background.
- **Projected size:** aim for the QR to take ≥ 1/6 of the slide width. Too small = nobody scans it from the back of the room.
- **Error correction:** default `m` (15%). If a logo goes on top or the QR might get damaged, regenerate with `--error h` (30%).

---

## Verification

Before wrapping up: **scan the SVG/PNG with your phone** and confirm it opens the right link. A QR that doesn't open is useless in a presentation. Preview:

```bash
open <SLIDES_DIR>/<name>/assets/qr/<slug>.svg
```
