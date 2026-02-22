# Project Brief: Archive & Reflection Metadata Format

## User Story

As a developer using the Niko system, I want archive and reflection documents to use YAML
frontmatter for metadata instead of inline bullet lists, so that the format is consistent with
the project's existing `.mdc` convention and better suited for future programmatic tooling.

## Requirements

1. **Update archive format template** in `rulesets/niko2/niko/memory-bank/archives.mdc`:
   - Replace `## METADATA` section (bullet list) with YAML frontmatter before the `h1`
   - Standard fields: `task_id`, `complexity`, `date`, `status`

2. **Update reflection format template** in `rulesets/niko2/niko/memory-bank/reflections.mdc`:
   - Replace inline bold bullets after `h1` with YAML frontmatter before the `h1`
   - Standard fields: `task_id`, `date`, `complexity`

3. **Update level2-reflect.mdc** in `rulesets/niko2/niko/level2/level2-reflect.mdc`:
   - Update the Step 5 template to use YAML frontmatter

4. **Update level3-reflect.mdc** in `rulesets/niko2/niko/level3/level3-reflect.mdc`:
   - Update the Step 5 template to use YAML frontmatter

5. **Migrate 5 existing archive documents** in `memory-bank/archive/`:
   - Convert `## METADATA` bullet blocks to YAML frontmatter in all existing archive docs
   - Files:
     - `memory-bank/archive/bug-fixes/20260125-niko-command-paths.md`
     - `memory-bank/archive/enhancements/20260120-archive-inlining-fix.md`
     - `memory-bank/archive/enhancements/20260125-archive-completion-gate.md`
     - `memory-bank/archive/enhancements/20260222-niko2-level4-impl.md`
     - `memory-bank/archive/systems/20260221-niko2-l3-reflect-archive-creative.md`

## Design Decision

Already resolved via creative phase (see `memory-bank/creative/creative-archive-reflection-metadata-format.md`).
YAML frontmatter was selected over the current bullet-list format.

**Target format for archives:**
```markdown
---
task_id: [task-id]
complexity: level-[n]
date: [YYYY-MM-DD]
status: [completed|in-progress]
---

# TASK ARCHIVE: [Task Name]

## SUMMARY
...
```

**Target format for reflections:**
```markdown
---
task_id: [task-id]
date: [YYYY-MM-DD]
complexity: level-[n]
---

# Reflection: [Task Name]

## Summary
...
```

## Out of Scope

- Syncing changes to `.cursor/rules/shared/niko/` or `.claude/rules/shared/niko/` (ai-rizz handles this)
- Level 4 archive template (already minimal; no format template defined, references archives.mdc)
- level2-archive.mdc / level3-archive.mdc (they reference archives.mdc for format, no embedded template)
