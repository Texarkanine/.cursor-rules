# Project Brief

## User Story

As an operator who installs Cursor rules a la carte or as a ruleset, I want four writing-style decompression keys (ASD-STE100, ISO 24495, Thomas and Turner classic prose, Orwell's six rules), each in always-respond, always-write, and ManualPrompt flavors, so I can turn a style on for chat, for prose, or for a one-shot `/<slug>-style` rewrite without bundling always-on rules into the installable set.

## Use-Case(s)

### Use-Case 1

Install one `always-respond-<slug>.mdc` (or one `always-write-<slug>.mdc`) from `rules/` so every reply (or every prose write) uses that style, with the precision qualifier intact.

### Use-Case 2

Install the `writing-styles` ruleset and invoke `/style-asd-ste100 rewrite some-doc.md` (or the sibling slugs) so the agent applies that style for the invoked task only.

### Use-Case 3

Read `rulesets/writing-styles/README.md` to compare the four styles against one shared prompt, then fill the placeholder sample cells after a stripped `claude -p` Opus 5 run.

## Requirements

1. Four slugs: `asd-ste100`, `iso-24495`, `thomas-turner-truth`, `orwell-6`.
2. Three files per slug (12 total; 10 new): `rules/always-respond-<slug>.mdc`, `rules/always-write-<slug>.mdc`, `rules/<slug>-style/SKILL.md`.
3. Rename the existing always-on keys: `rules/asd-ste100.mdc` → `rules/always-respond-asd-ste100.mdc`, `rules/iso-24495.mdc` → `rules/always-respond-iso-24495.mdc`.
4. Always-on pair: `alwaysApply: true`. Not members of the ruleset.
5. Skills: ManualPrompt with `disable-model-invocation: true`. Body is the key plus qualifier only — no respond/write domain.
6. Headings on each file state the flavor (respond / write / style).
7. Shared qualifier on every file: "If doing so would remove a required technical term or a precise meaning, keep the term. Clarity and accuracy trump style."
8. Keys stay decompression keys: name the framework; do not rewrite ASD-STE100, ISO 24495, Thomas and Turner, or Orwell's six rules.
9. `thomas-turner-truth` (TTT on the available-styles list) credits [Thomas and Turner's *Clear and Simple as the Truth*](https://press.princeton.edu/books/hardcover/9780691654744/clear-and-simple-as-the-truth) and Pinker's classical style; `orwell-6` is "Use Orwell's 6 rules for writing."
10. New ruleset `rulesets/writing-styles/` ships only the four `*-style` skills (directory symlinks to `rules/<slug>-style`) plus a README.
11. README describes the four styles and includes one shared sample prompt (e.g. "explain what nodejs is") with a placeholder table for operator-filled `claude -p` samples. Do not generate those samples by moving `~/.claude` trees.
12. Add a `writing-styles` door on the root `README.md`, sibling to the other rulesets.
13. Canonical sources only — do not edit generated `.cursor/` or `.claude/` copies.

## Constraints

1. Existing `make test` layout checks must still pass (ruleset symlink targets; README links to canonical `rules/` paths).
2. No wording/change-detector tests on rule or skill bodies.
3. Do not move or back up `~/.claude/{rules,skills,plugins}` to harvest samples.
4. Do not register the new ruleset in this clone's `ai-rizz.skbd` unless later asked.
5. `REUSE.toml` already covers `rules/**/*.mdc`, `rules/**/*.md`, and `rulesets/**/README.md` — no license-table edit unless a new path falls outside those globs.

## Acceptance Criteria

1. Twelve style files exist at the paths above; the two old `rules/asd-ste100.mdc` and `rules/iso-24495.mdc` names are gone.
2. Each always-on file is `alwaysApply: true`; each skill has `disable-model-invocation: true` and a heading that marks it as a style call-in.
3. `rulesets/writing-styles/` contains only the four skill symlinks plus README; no always-on `.mdc` files.
4. README links resolve to canonical `rules/` skill paths; sample table cells are explicit placeholders.
5. Root README lists `writing-styles` as a ruleset door.
6. `make test` passes.
