# Decision: Archive & Reflection Document Metadata Format

## Context

Archive and reflection documents currently use an unordered bullet list inside a `## METADATA`
section (immediately after the `h1`) to record task metadata: task ID, complexity level, date,
and status. The question is whether YAML frontmatter before the `h1` would be a better fit.

This matters because archive docs are long-lived canonical records read by agents, humans, and
potentially future tooling. Reflection docs feed into archives. The metadata format affects
document structure consistency across the project, agent readability, and future queryability.

**Constraints**:
- Must be readable by Claude agents without special tooling
- Reflection directory is currently empty — zero migration cost
- 5 existing archive docs use the current bullet-list format — low migration cost
- The project itself flagged YAML frontmatter as a future improvement in `niko2-level4-impl`

## Options Evaluated

- **Option A — Bullet list under `## METADATA`**: Current format. Metadata lives in the document
  body under a second-level heading.
- **Option B — YAML frontmatter before `h1`**: Standard markdown metadata convention. Metadata
  is separated from document content.
- **Option C — YAML frontmatter + inline summary echo**: Frontmatter for tooling, plus a
  one-liner blockquote in the body for human skimming.

## Analysis

| Criterion | Option A (bullet list) | Option B (frontmatter) | Option C (hybrid) |
|-----------|----------------------|----------------------|------------------|
| Project pattern consistency | Unique to `.md` docs | Aligns with `.mdc` convention | Aligns with `.mdc` convention |
| Agent readability | Clearly labeled in-body section | Well-known convention; Claude handles it | Well-known + inline summary |
| Human skimmability | In-document flow | Out-of-body; requires convention knowledge | Frontmatter + one-liner |
| Document structure simplicity | Extra heading level for non-content | Flatter — removes `## METADATA` | Flatter but adds a blockquote |
| Generation complexity | Low — forgiving format | Low — simple key-value types | Higher — two representations |
| Future tooling | Difficult to parse | Trivially parseable | Trivially parseable |
| Migration cost (5 archives) | None | Low | Low |

Key insights:

- **Project already uses YAML frontmatter.** `.mdc` rule files all use `---` frontmatter with
  `description`, `globs`, `alwaysApply`. Using a different format for archive/reflection `.md`
  files creates an unexplained inconsistency within the same ecosystem.
- **`## METADATA` is structure for structure's sake.** The heading exists solely to announce
  "metadata follows" — not to organize actual content. YAML frontmatter achieves the same signal
  more cleanly and is the established convention for this purpose in markdown.
- **YAGNI is weakened by the project's own foresight.** `niko2-level4-impl` explicitly notes:
  *"YAML front matter would be cleaner"* as a future consideration. Implementing it now, at
  only 5 archives and 0 reflections, is the minimum-cost moment.
- **YAML value types here are simple.** Fields are plain strings and dates — no quoting edge
  cases, no nesting. LLM mis-generation risk is negligible for this schema.
- **Option C eliminated.** GitHub renders frontmatter as a table; Claude reads it natively. A
  redundant blockquote echo adds noise without solving a real readability problem.

## Decision

**Selected**: Option B — YAML frontmatter

**Rationale**: The project already uses YAML frontmatter as its metadata convention in `.mdc`
files. Archive and reflection docs belong to the same ecosystem and should follow the same
convention. The `## METADATA` heading adds a structural layer with no content value; frontmatter
removes it. Migration cost is at its minimum right now (5 archives, 0 reflections). The project
itself has already flagged this as a pending improvement.

**Tradeoff**: Metadata is no longer in the document body flow. Readers unfamiliar with the
frontmatter convention may initially miss it. Accepted because Claude agents (primary consumers)
handle frontmatter natively, and GitHub renders it as a formatted table.

## Implementation Notes

- Update `level2-reflect.mdc` and `level3-reflect.mdc` to template YAML frontmatter instead of
  `## METADATA`
- Update `level2-archive.mdc` and `level3-archive.mdc` similarly
- Migrate the 5 existing archive docs (mechanical edit — swap `## METADATA` bullet block for
  `---` frontmatter block before the `h1`)
- Standard fields: `task_id`, `complexity`, `date`, `status` — lowercase-snake, consistent with
  `.mdc` frontmatter style
- No `## METADATA` section in new documents; `## SUMMARY` becomes the first section after `h1`

**Example target format**:

```markdown
---
task_id: niko2-level4-impl
complexity: level-3
date: 2026-02-22
status: completed
---

# TASK ARCHIVE: niko2-level4-impl

## SUMMARY
...
```
