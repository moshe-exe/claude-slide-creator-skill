# Icon Criteria — illustration conventions

Conventions the `slide-creator` skill applies during `/slide-creator illustrate`. Like `polish-criteria.md`, this **grows with use**: every time an illustration decision reveals a general principle, it gets appended here.

They guide sequential mode and are the basis for parallel mode (which unlocks at ≥ 5 conventions — see [`illustrating.md`](illustrating.md)).

---

## Icon selection

- **I1 · Semantic, not decorative.** The icon reinforces the slide's central concept (literal or metaphorical). If there's no honest mapping, don't add an icon. A generic icon ("star", "circle") is worse than none.
  **Why:** Filler icons add noise without information; the eye processes and discards them, costing attention without paying anything back.

- **I2 · One concept, one icon.** Each illustrated slide carries **at most one** icon. Don't combine multiple glyphs on a slide.
  **Why:** Two icons compete to be the visual anchor; minimalism loses.

- **I3 · Don't illustrate dense slides.** Tables, long lists, text-heavy slides → no icon. They already have enough visual mass.
  **Why:** An icon on an already-loaded slide is decoration, not hierarchy.

---

## Style and consistency

- **I4 · One library, one weight, across the whole deck.** All icons from the same collection (`ph:`) and the same stroke weight. Defined in the `IconBadge` component, not slide by slide.
  **Why:** Inconsistent stroke reads as a collage, not a system. (Exception: brand logos — GitHub, etc.)

- **I5 · The icon never competes with the h1.** Size and position subordinate to the title. A `sm` badge next to the title, or `lg` centered on a section slide — never dominating a content slide.
  **Why:** The title is the anchor; the icon accompanies it.

- **I6 · Color from the palette.** Badge and glyph use `var(--c-*)`, never hardcoded hex. Background = accent at low opacity (~12%), glyph = solid accent.
  **Why:** If the palette changes via `style`, the illustration updates on its own. Hardcoding breaks that link.

---

## Background shapes

- **I7 · Consistent shape per role.** Icons of the same role use the same shape: e.g. all section icons in `squircle`, all content ones in `circle`. Don't vary shape arbitrarily.
  **Why:** The shape encodes hierarchy; varying it at random turns it into noise.

---

## Density

- **I8 · Selectivity over coverage.** Don't illustrate every slide. A chosen subset (concept slides, section transitions) looks more intentional than full coverage.
  **Why:** Minimalism IS the feature. One icon per slide across 18 slides saturates; 5 well-placed ones breathe.

---

## Anti-criteria

Things that are **not** illustration conventions (they go elsewhere):

- **Color, palette** → `style` / [`styling.md`](styling.md)
- **Layout, spacing, hierarchy** → `polish` / [`polishing.md`](polishing.md)
- **Content** → `review` / [`reviewing.md`](reviewing.md)

These conventions (I1–I8) are the initial seeds. They'll get refined and expanded with every deck that uses `/slide-creator illustrate`.
