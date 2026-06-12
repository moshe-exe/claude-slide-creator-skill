# Illustrating — minimalist icons with shaped backgrounds

Full mechanics of `/slide-creator illustrate <name>`. Adds light illustration to slides: icons from a library, chosen based on content, over shaped backgrounds (circle, squircle) tinted with the deck's palette. **Minimalist by design** — few icons, high intention.

Orthogonal to the other steps:
- `style` defines the palette → the icons and backgrounds inherit it
- `polish` organizes the layout → illustration is added **afterward**, on a stable layout
- `illustrate` (this one) adds the graphic elements

---

## Prerequisites

1. **Defined palette** (`palette.json` + `uno.config.ts`). The badges use `var(--c-*)`. Without a palette, abort and suggest `/slide-creator style`.
2. **Stable layout** (ideally post-`polish`). Illustrating before polishing is wasted work if the slides get reorganized.
3. **`IconBadge` component** in the deck (`components/IconBadge.vue`). If it doesn't exist, the first `/slide-creator illustrate` creates it (see below).

---

## Icon library

**Phosphor** (`ph:`) via UnoCSS `preset-icons` (= Iconify) — already integrated in Slidev, no installation.

- Static class syntax: `i-ph:scissors` (the one UnoCSS detects — see the warning in the component)
- Default weight: **regular** solid (clean, contrasts over the shaped background). Others: `i-ph-bold:...`, `i-ph-light:...`, `i-ph-duotone:...`
- `@iconify-json/ph` already ships with Slidev — no extra install
- Browsable: https://phosphoricons.com

> **One library per deck.** Don't mix `ph:` with `mdi:`/`carbon:`/etc. Stroke consistency is what makes it look intentional. (Tolerated exception: `carbon:logo-github` and other brand logos that Phosphor doesn't have.)

If the deck needs another library, change it globally — not slide by slide.

---

## The `IconBadge` component

Single source of truth for badge styling. Lives in the deck's `components/IconBadge.vue`. The first `/slide-creator illustrate` creates it if it doesn't exist:

```vue
<!-- components/IconBadge.vue -->
<script setup>
defineProps({
  shape: { type: String, default: 'circle' }, // circle | squircle
  size:  { type: String, default: 'md' },     // sm | md | lg
})
</script>

<template>
  <div class="icon-badge" :class="[`shape-${shape}`, `size-${size}`]">
    <slot />
  </div>
</template>

<style scoped>
.icon-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
  background: color-mix(in srgb, var(--c-accent) 12%, transparent);
  color: var(--c-accent);
}
.icon-badge :deep(> *) { width: 58%; height: 58%; }
.shape-circle   { border-radius: 9999px; }
.shape-squircle { border-radius: 28%; }
.size-sm { width: 2.25rem; height: 2.25rem; }
.size-md { width: 3.25rem; height: 3.25rem; }
.size-lg { width: 4.75rem; height: 4.75rem; }
</style>
```

Use in `slides.md` — **the glyph goes as a slot with a static class**:
```md
<IconBadge shape="squircle" size="lg"><div class="i-ph:scissors" /></IconBadge>
```

> **⚠️ Critical: the icon goes as a slot, NOT as a prop built at runtime.**
> UnoCSS does **static** class extraction — it only generates the CSS for an icon if it literally sees the class `i-ph:...` in the source code. If the component builds the class at runtime (`:class="`i-${icon}`"`), UnoCSS doesn't detect it and **the badge comes out empty** (just the background, no glyph). That's why the icon is written as `<div class="i-ph:scissors" />` in the slot, where UnoCSS sees it in `slides.md`.

**Why a component and not loose markup:** you change the badge style (default shape, tint, sizes) in a single place and the whole deck updates. The component provides the background/shape/size; the slide just declares which glyph goes inside.

---

## Icon selection — semantic, not decorative

The icon must **reinforce the slide's concept**, not fill space. Per-slide process:

1. Read the content + screenshot of the slide.
2. Identify the central concept (1 word/idea).
3. Map it to a Phosphor icon that represents it literally or metaphorically.
4. If there's no clear, honest mapping → **don't add an icon**. Forcing a generic icon is worse than none.

Examples:
| Slide | Concept | Icon |
|-------|---------|------|
| Cut until it hurts | cut scope | `ph:scissors` |
| The 48 hours in blocks | time / phases | `ph:clock` or `ph:timer` |
| Minimal stack | layers / architecture | `ph:stack` |
| Top mistakes | warning | `ph:warning` |
| When to change course | pivot / direction | `ph:compass` or `ph:arrows-split` |

---

## Where the icons go

Two uses, both minimalist:

### 1. Accent badge on key content slides
A badge next to the title. Subordinate to the h1 — never competing.
```md
<div class="flex items-center gap-4">
  <IconBadge shape="squircle" size="md"><div class="i-ph:scissors" /></IconBadge>
  <h1 class="!m-0">Rule #1: cut until it hurts</h1>
</div>
```

### 2. Section icon on transition slides
"Part 1/2/3" or section-opener slides: large centered badge.
```md
<div class="flex justify-center mb-6">
  <IconBadge shape="squircle" size="lg"><div class="i-ph:wrench" /></IconBadge>
</div>

# Part 1 · The method
```

**Don't** put inline icons on every bullet — it breaks the minimalism and loads the slide visually. See `icon-criteria.md`.

---

## Flow (screenshot-driven, like polish)

### Setup (first time)
1. Verify palette (`palette.json`). If missing → abort, suggest `/slide-creator style`.
2. Create `components/IconBadge.vue` if it doesn't exist.
3. Capture current screenshots (reuse `polish/` if it exists, or `npm run export --format png`).

### Per-slide loop
1. Show content + screenshot.
2. Decide: **does this slide gain from an icon?** Most dense slides (tables, long lists) → **no**. Concept/title slides → candidates.
3. If yes: propose `icon` + `shape` + placement, with a semantic rationale.
4. Apply `<IconBadge>`, re-screenshot, verify it doesn't compete or unbalance.
5. What generalizes → `icon-criteria.md`.

### Parallel mode
Available once `icon-criteria.md` has established conventions (≥ 5). One agent per slide proposes an icon; the user reviews the consolidated set before applying. Same gating as `polish`.

---

## Artifacts

**In the skill (shared across decks):**
- `illustrating.md` (this one) — mechanics
- `icon-criteria.md` — selection and style conventions, grows with use

**In the deck:**
- `components/IconBadge.vue` — the component
- `slides.md` — the inserted `<IconBadge>`s
- `ICONS.md` (optional) — log of which icon each slide carries and why

---

## Notes

- **Selectivity > coverage.** An 18-slide deck with 5 well-chosen icons looks more intentional than with 18. Minimalism is the feature.
- **The icon never competes with the h1.** Size and position always subordinate.
- **One stroke weight across the whole deck.** Don't mix `ph:scissors` (regular) with `ph-bold:scissors`. Define the weight in the component and respect it.
- **Color from the palette, not hardcoded.** The badge uses `var(--c-accent)`. If the palette changes via `style`, the badges update on their own.
- **Brand logos** (GitHub, etc.) are the only exception to "one library" — use the correct logo even if it's not Phosphor.
