# Reviewing — review and approval process

**Every new presentation is born as `draft`. It is not "publishable" until ≥ 2 review rounds are complete.** State lives in `REVISIONS.md` inside the deck's repo.

---

## States

| State | Meaning |
|-------|---------|
| `draft` | Just created. Content is a skeleton / best first attempt. **Not publishable.** |
| `review-1` | Round 1 complete (changes applied + feedback recorded). **Not publishable.** |
| `review-2` | Round 2 complete. **Approvable** via `/slide-creator approve`. |
| `review-N` (N≥3) | Additional iterations before approval. **Approvable.** |
| `approved` | Approved by the owner. Publishable version. `v1.0.0` git tag. |

---

## `REVISIONS.md` — structure

```markdown
# Revisions — <name>

**State:** draft | review-N | approved
**Rounds completed:** N
**Minimum to approve:** 2
**Last updated:** YYYY-MM-DD

---

## Round N — YYYY-MM-DD

**Round focus:** (what was reviewed)

**Proposed changes:**
- ...

**Owner feedback:**
- ...

**Resolution:**
- Applied: ...
- Deferred: ...
- Rejected: ...

**Commit:** <hash>
```

---

## Command: `status`

**Trigger:** `/slide-creator status <name>`

1. Read `<SLIDES_DIR>/<name>/REVISIONS.md`.
2. Show:
   ```
   <name>
   State: <state>
   Rounds completed: N / 2 (minimum)
   Last round: YYYY-MM-DD
   Approvable: yes | no (X rounds missing)
   ```

---

## Command: `review`

**Trigger:** `/slide-creator review <name>`

1. Read `REVISIONS.md` to know the current state and prior rounds.
2. Read the full `slides.md`.
3. **Start the next round:**
   - Define the **focus** of the round (e.g.: "Round 1 → real content vs placeholders. Round 2 → polish flow + concrete examples.").
   - List **concrete proposals** for changes (slide-by-slide where it applies), with brief rationale.
   - **Apply nothing yet.** Wait for the owner's feedback.
4. After feedback:
   - Apply approved changes to `slides.md`.
   - Append a new entry in `REVISIONS.md` with the completed round.
   - Commit + push.
   - Advance state: `draft → review-1`, `review-1 → review-2`, etc.

---

## Command: `approve`

**Trigger:** `/slide-creator approve <name>`

1. Read `REVISIONS.md`.
2. **Block if `rounds < 2`**:
   ```
   ✗ Cannot approve — only X rounds completed. Minimum: 2.
     Run /slide-creator review <name> to continue.
   ```
3. If rounds ≥ 2 **and** the owner has confirmed in chat (don't assume):
   - Update `REVISIONS.md`: state → `approved`.
   - Commit in the deck's repo: `release: approve v1.0.0`.
   - Tag: `git tag v1.0.0 && git push --tags`.
   - Create a GitHub release: `gh release create v1.0.0 --notes-from-tag`.
   - Output: confirm release URL + Pages live URL.

---

## Inviolable rules

- **No approval without 2+ review rounds.** The `approve` command is gated by `REVISIONS.md`. No bypass.
- **Every `/slide-creator create` leaves the deck in `draft` state with `REVISIONS.md` ready** (see [`creating.md`](creating.md)).

---

## Relationship with polish

`approve` **does not require** completed polish — visual polish is optional (see [`polishing.md`](polishing.md)). But if `POLISH.md` exists and is `in-progress` at approval time, warn the owner which slides remain unpolished before tagging `v1.0.0`.
