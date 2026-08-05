# Task: illustrate-complexity

* Task ID: illustrate-complexity
* Complexity: Level 2
* Type: Simple enhancement (rename + content rewrite)

Rename `rules/visual-planning/` to `rules/illustrate-complexity/` and rewrite its frontmatter and four body areas, so the skill triggers on any explanation that needs an illustration. Repoint every reference to the old name. Add agentskills.io pointers to the authoring ruleset: one link in its README, and a new `skill-frontmatter.md` reference under `prompt-authoring`.

## Test Plan (TDD)

`always-tdd.mdc` carves out "rule and skill wording" as prose. A test that asserts on this content could only go red when someone edits the artifact, which makes it a change-detector. So no new test files. The rename does touch real layout contracts, and the repo already has a purpose-built gate for them.

### Committed Gates

These already exist and run in CI. They go red when a link or symlink actually breaks for a consumer.

- Symlink integrity: `make test-symlinks` → both ruleset symlinks resolve to `rules/illustrate-complexity`.
- README link integrity: `make test-readme-links` → every internal link in the two ruleset READMEs resolves.

### One-Time Build Checks

Run once at step 12 to confirm the edit landed. **Do not commit any of these as tests.** Each asserts on document content, so as a persisted test it would only go red when someone edits the artifact — a change-detector.

- Rename completeness: `rg 'visual-planning' rules/ rulesets/` → no matches.
- Persistent file accuracy: `rg 'illustrate-complexity' memory-bank/techContext.md` → one match.
- Description limit: measure the `description:` value → under 1024 characters.
- Framing removed: `rg 'Planning Workflow' rules/illustrate-complexity/SKILL.md` → no matches.
- No regression in the diagram reference: diff the five diagram examples, the syntax rules, and the emoji block against the pre-rename file → byte-identical.

### Test Infrastructure

- Framework: `make test`, which runs `scripts/check-ruleset-symlinks.sh` and `scripts/check-ruleset-readme-links.sh`.
- Test location: `scripts/`.
- Conventions: shell scripts sharing `scripts/rulesets-check-common.sh`. CI runs the same Make targets via `.github/workflows/rulesets-links.yml`.
- New test files: none.

## Implementation Plan

1. Rename the skill directory.
   - Files: `rules/visual-planning/` → `rules/illustrate-complexity/`
   - Changes: `git mv`. Content unchanged at this step.
2. Repoint the two ruleset symlinks.
   - Files: `rulesets/authoring/skills/visual-planning`, `rulesets/niko/skills/visual-planning`
   - Changes: remove both links. Create `illustrate-complexity` links pointing at `../../../rules/illustrate-complexity`. Run `make test-symlinks`.
3. Replace the frontmatter.
   - Files: `rules/illustrate-complexity/SKILL.md`
   - Changes: `name: illustrate-complexity`. New description, target ~300 characters: imperative opener, the artifact list, "even when nobody asked for a diagram", and the numeric-charting exclusion.
4. Rewrite the body opening.
   - Files: `rules/illustrate-complexity/SKILL.md`
   - Changes: retitle the H1. Replace "When planning non-trivial work" with the general case. Move the "more than a paragraph of *and then*" test up so it sits directly under the opening.
5. Add the chart-type escape hatch.
   - Files: `rules/illustrate-complexity/SKILL.md`
   - Changes: one sentence below the diagram-type table naming a few omitted types, linking <https://mermaid.js.org/intro/syntax-reference.html>.
6. Replace `## Planning Workflow` with a three-use section.
   - Files: `rules/illustrate-complexity/SKILL.md`
   - Changes: one short block each for planning, documenting, and answering a question. State the size rule: keep chat diagrams small, because most chat UIs render them badly; a large diagram is correct on a web page, because Mermaid gives the reader a lightbox.
   - Constraint from preflight: no block may prescribe a diagram type or a fixed order of diagrams. `rules/architecture-docs/SKILL.md` line 46 explicitly rejects "Always open with a control-flow Mermaid flowchart" and warns that mandating one type teaches mimicry. Type selection stays with the table at step 5. These blocks carry only size and rendering context.
7. Update the authoring ruleset README.
   - Files: `rulesets/authoring/README.md`
   - Changes: rename the heading and path on line 20. Restate Purpose and Scope. Add the agentskills.io best-practices link.
8. Update the niko ruleset README.
   - Files: `rulesets/niko/README.md`
   - Changes: rename the entry on line 25 and rewrite its one-line pitch, which currently says "when planning complex tasks".
9. Update the persistent tech context.
   - Files: `memory-bank/techContext.md`
   - Changes: line 21 names the new skill.
10. Add the skill-frontmatter reference.
    - Files: `rules/prompt-authoring/references/skill-frontmatter.md` (new)
    - Changes: short file covering what this repo omits — `description` drives triggering, the 1024-character limit, and when to split into `references/`. It links the agentskills best-practices and optimizing-descriptions pages. It points at upstream rather than restating it.
    - Added by preflight: two sentences saying that when a skill is split, or when its siblings are retired, the survivor's description must be re-derived. This is the root cause of the present task, and nothing in the repo currently prompts that check.
11. Point `prompt-authoring` at the new reference.
    - Files: `rules/prompt-authoring/SKILL.md`
    - Changes: one line in the existing references list at lines 21-25, stating the condition for reading it.
12. Verify.
    - Files: none
    - Changes: run `make test`. Run each grep listed under Behaviors to Verify.

## Technology Validation

No new technology - validation not required. All four external URLs were verified to return 200 during complexity analysis.

## Dependencies

- `make test` must pass before the task is complete.
- The generated `.cursor/` and `.claude/` trees are re-synced in a later, separate `chore(dev): ai-rizz sync` commit. That sync cannot happen in this task, because `ai-rizz` reads the git remote.
- Verified in preflight, no action needed: `REUSE.toml` licenses by glob (`rules/**/*.md`), so the rename needs no REUSE edit and the new reference file is covered as PPL-S. `ai-rizz.skbd` lists directories only, with no per-skill entries, so the rename does not touch it.

## Challenges & Mitigations

- Symlink rename is not a content edit: `git mv` on a symlink keeps the old link name. Mitigation: delete and recreate both links, then run `make test-symlinks` at step 2 rather than waiting for the end.
- Renaming a skill breaks consumers who installed `visual-planning` through `ai-rizz`. Mitigation: none needed. The repo defaults to clean-break changes. Note it in reflect so the PR description carries the warning.
- Editing `memory-bank/techContext.md` during build overlaps the reflect phase's persistent-file reconciliation. Mitigation: make the surgical rename now, because leaving it wrong would fail QA, and record in reflect that this line is already reconciled.
- The description could grow past its budget while trying to cover every context. Mitigation: hold the ~300-character target and drop artifacts from the list before dropping the exclusion clause.
- `prompt-authoring` warns against referring to documents you do not own. The new reference file links an external site. Mitigation: the pointer must name what upstream uniquely owns and must not restate its content, so drift cannot occur.

## Pre-Mortem

- The rewrite balloons into a full rework of the skill. The operator asked for the smallest change that reaches the goal. Plan response: steps 3-6 name the only four areas that may change. The five diagram examples, the syntax rules, and the emoji block stay byte-identical, and the final verification diffs them.
- The new description over-triggers and the skill fires on every request. Plan response: keep both narrowing devices - the subject qualifier "structure, flow, or relationships" and the numeric-charting exclusion. Do not broaden to "any explanation".
- `skill-frontmatter.md` grows into a summary of the agentskills page and then drifts from it. Plan response: already covered by Challenge 5. Cap the file at a short orientation plus links.
- A reference to the old name survives somewhere unsearched. Plan response: step 12 greps `rules/` and `rulesets/` rather than trusting the edit list.
- The three-use section reintroduces the planning framing under a new heading. Plan response: planning must appear as one peer among three, never first-among-equals, and the section must not be titled as a workflow.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [ ] Build
- [ ] QA
