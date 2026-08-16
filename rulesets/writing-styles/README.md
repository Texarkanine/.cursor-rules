# Writing Styles Ruleset

Four short decompression keys for prose. This ruleset ships only the ManualPrompt call-ins (`/<slug>-style`). The always-on `always-respond-*` and `always-write-*` rules live a la carte under `rules/` and are **not** in this ruleset — install one of those if you want the style on every reply or every prose write.

## Which Style

Pick one. They are siblings, not a stack.

- **ASD-STE100** — Simplified Technical English. Official standard: https://www.asd-ste100.org/
- **ISO 24495** — Plain language: relevant, findable, understandable, usable. Public summary: https://www.iplfederation.org/iso-standard/
- **TTT** — Classical style as Pinker describes it, per Thomas and Turner's *Clear and Simple as the Truth*. Book: https://press.princeton.edu/books/hardcover/9780691654744/clear-and-simple-as-the-truth
- **Orwell 6** — Orwell's six rules for writing.

## Skills

### ✈️ [asd-ste100-style](../../rules/asd-ste100-style/SKILL.md)

- **Purpose**: Apply ASD-STE100 for the invoked task.
- **Scope**: Whatever the operator points at (`/asd-ste100-style rewrite some-doc.md`).

### 📄 [iso-24495-style](../../rules/iso-24495-style/SKILL.md)

- **Purpose**: Apply ISO 24495 plain language for the invoked task.
- **Scope**: Whatever the operator points at (`/iso-24495-style rewrite some-doc.md`).

### ✒️ [thomas-turner-truth-style](../../rules/thomas-turner-truth-style/SKILL.md)

- **Purpose**: Apply Thomas and Turner's classical style for the invoked task.
- **Scope**: Whatever the operator points at (`/thomas-turner-truth-style rewrite some-doc.md`).

### 📰 [orwell-6-style](../../rules/orwell-6-style/SKILL.md)

- **Purpose**: Apply Orwell's six rules for the invoked task.
- **Scope**: Whatever the operator points at (`/orwell-6-style rewrite some-doc.md`).

## Sample

Shared prompt: `explain what nodejs is`

Fill each cell from a stripped Opus 5 `claude -p` run (no other rules, skills, or plugins loaded). Leave the placeholder until that run exists. Do not invent a sample.

| Style | Sample |
| --- | --- |
| ASD-STE100 | _placeholder — paste stripped Opus 5 `claude -p` output_ |
| ISO 24495 | _placeholder — paste stripped Opus 5 `claude -p` output_ |
| TTT | _placeholder — paste stripped Opus 5 `claude -p` output_ |
| Orwell 6 | _placeholder — paste stripped Opus 5 `claude -p` output_ |
