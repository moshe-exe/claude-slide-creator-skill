---
theme: seriph
title: {{TITLE}}
info: |
  ## {{TITLE}}
  Presentation created on {{DATE}}.
class: text-center
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
---

<!--
  Palette: define the deck's colors with `/slide-creator style {{NAME}}`.
  Source of truth: palette.json · Generated: uno.config.ts (do not edit by hand).
  Available UnoCSS tokens: bg, fg, primary, primary-dk, accent
    (e.g. text-primary, bg-accent, border-primary-dk)
  Available CSS vars: --c-bg, --c-fg, --c-primary, --c-primary-dk, --c-accent
  Custom CSS (typography, custom classes, workarounds) → style.css
-->

# {{TITLE}}

{{DATE}}

<div class="abs-br m-6 text-xl">
  <a href="{{REPO_URL}}" target="_blank" class="slidev-icon-btn">
    <carbon:logo-github />
  </a>
</div>

---
transition: fade-out
---

# Agenda

1. Context
2. Proposal
3. How it works
4. Next steps

---

# Context

Why we're here.

- Point 1
- Point 2
- Point 3

---
layout: two-cols
---

# Proposal

Main idea in one line.

::right::

```ts
// Code example
function hello(name: string) {
  return `Hello ${name}`
}
```

---
layout: center
class: text-center
---

# Thanks

Questions → [@{{NAME}}]({{REPO_URL}})
