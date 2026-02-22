# Task: Archive & Reflection Metadata Format

* Task ID: archive-reflection-metadata-format
* Complexity: Level 2
* Type: Simple Enhancement

Switch archive and reflection document metadata from `## METADATA` bullet lists (and inline
bold bullets) to YAML frontmatter before the `h1`. Decision rationale documented in
`memory-bank/creative/creative-archive-reflection-metadata-format.md`.


## Test Plan (TDD)

### Behaviors to Verify

> ⚠️ No automated test infrastructure exists in this project (markdown/ruleset). Verification
> is manual inspection per the established pattern in this project.

- [archives.mdc format]: Template shows `---` frontmatter block before `# TASK ARCHIVE:` heading
- [archives.mdc format]: Template has NO `## METADATA` section
- [reflections.mdc format]: Template shows `---` frontmatter block before `# Reflection:` heading
- [reflections.mdc format]: Template has NO inline bold metadata bullets after `h1`
- [level2-reflect.mdc Step 5]: Template uses YAML frontmatter
- [level3-reflect.mdc Step 5]: Template uses YAML frontmatter
- [migrated archives x5]: Each archive doc has YAML frontmatter block at top
- [migrated archives x5]: Each archive doc has NO `## METADATA` section
- [frontmatter field names]: All use lowercase-snake: `task_id`, `complexity`, `date`, `status`

### Test Infrastructure

- Framework: None (markdown/ruleset project)
- Verification: Manual inspection of file contents after each edit

## Implementation Plan

**Template Files (rulesets source):**

1. Update `archives.mdc` format template
   - File: `rulesets/niko2/niko/memory-bank/archives.mdc`
   - Change: Replace `## METADATA` + bullet list with YAML frontmatter before `h1`
   - Fields: `task_id`, `complexity`, `date`, `status`

2. Update `reflections.mdc` format template
   - File: `rulesets/niko2/niko/memory-bank/reflections.mdc`
   - Change: Replace inline bold bullets after `h1` with YAML frontmatter before `h1`
   - Fields: `task_id`, `date`, `complexity`

3. Update `level2-reflect.mdc` Step 5 template
   - File: `rulesets/niko2/niko/level2/level2-reflect.mdc`
   - Change: Replace inline bold bullets in the Step 5 markdown template with YAML frontmatter

4. Update `level3-reflect.mdc` Step 5 template
   - File: `rulesets/niko2/niko/level3/level3-reflect.mdc`
   - Change: Replace inline bold bullets in the Step 5 markdown template with YAML frontmatter

**Existing Archive Migrations:**

5. Migrate `20260125-niko-command-paths.md`
   - File: `memory-bank/archive/bug-fixes/20260125-niko-command-paths.md`
   - Change: Move `## METADATA` bullet block to YAML frontmatter before `h1`

6. Migrate `20260120-archive-inlining-fix.md`
   - File: `memory-bank/archive/enhancements/20260120-archive-inlining-fix.md`
   - Change: Move `## METADATA` bullet block to YAML frontmatter before `h1`

7. Migrate `20260125-archive-completion-gate.md`
   - File: `memory-bank/archive/enhancements/20260125-archive-completion-gate.md`
   - Change: Move `## METADATA` bullet block to YAML frontmatter before `h1`

8. Migrate `20260222-niko2-level4-impl.md`
   - File: `memory-bank/archive/enhancements/20260222-niko2-level4-impl.md`
   - Change: Move `## METADATA` bullet block to YAML frontmatter before `h1`

9. Migrate `20260221-niko2-l3-reflect-archive-creative.md`
   - File: `memory-bank/archive/systems/20260221-niko2-l3-reflect-archive-creative.md`
   - Change: Move `## METADATA` bullet block to YAML frontmatter before `h1`

## Technology Validation

No new technology — validation not required.

## Dependencies

- None

## Challenges & Mitigations

- **Inconsistent `status` field in existing archives**: Some have "COMPLETE", some have
  "COMPLETED & ARCHIVED", one has no status. Normalize to `completed` for all migrated docs.
- **Date field name**: Existing archives use "Date Completed" (archives) vs "Date" (reflections).
  Normalize both to `date` in frontmatter for simplicity.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [ ] Preflight
- [ ] Build
- [ ] QA
