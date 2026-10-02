# Task: Dependabot Janitor Skill

* Task ID: dependabot-janitor
* Complexity: Level 2
* Type: New feature / Skill authoring

Draft and refine `/dependabot-janitor` at `rules/dependabot-janitor/SKILL.md` to automate triaging, combining, and excluding Dependabot pull requests across repositories based on protective test gates and receipted decisions.

## Test Plan (TDD)

Per the repository's `always-tdd` rule, rule and skill wording is carved out from automated unit test assertion suites, as asserting on markdown prose would create brittle change-detector tests. Correctness is verified via:
1. `make test` running ruleset symlink checks, README link audits, and test suites.
2. Structural verification against `create-skill` guidelines (valid YAML frontmatter, third-person description, under 500 lines, no broken links).
3. Negative pattern assertions verifying the absence of prohibited external blog URLs and company references.

### Behaviors to Verify

- Ingestion handles queue URLs, individual PR URLs, and pasted lists.
- Evaluation classifies PRs into discrete dispositions (Merge Ready, Combine, Exclude & Close, Caution / Manual Review, Hold / Blocked, Manual / Operational).
- Execution procedures use stock `git worktree` and `gh` only: lockstep updates, Dependabot ignores, and receipted explanations. No local aliases or operator-specific commit trailers.
- Zero references to external blog posts or company names.
- `make test` passes cleanly.

## Implementation Plan

1. [x] Create feature branch `feat/dependabot-janitor` off fresh `origin/main`
2. [x] Create directory `rules/dependabot-janitor/`
3. [x] Author `rules/dependabot-janitor/SKILL.md`
   - Define YAML frontmatter with discovery description and triggers
   - Document supported inputs (URLs, pasted lists, CLI discovery)
   - Detail core principles and deterministic guards
   - Specify evaluation and disposition rubric
   - Provide triage output format template
   - Document execution procedures for combines and excludes
4. [x] Verify constraints
   - Ensure zero links/references to external blog posts or company names
   - Check line count (229 lines, well within 500-line budget)
5. [x] Run `make test` baseline
   - `scripts/check-ruleset-symlinks.sh` passed
   - `scripts/check-ruleset-readme-links.sh` passed
   - `tests/choose-verification-model` passed
6. [x] Fill out `memory-bank/active/` state for handover
   - `projectbrief.md`
   - `tasks.md`
   - `activeContext.md`
   - `progress.md`
7. [x] Revision: stock `git` and `gh` only
   - Replace local worktree aliases with `git worktree add -b` / `git worktree remove`
   - Take the base branch, package manager, commit style, and merge method from the target repository
   - Drop the operator-specific commit trailer
   - Do not create a Dependabot config when the repository has none; group recurring peer splits when a config file already exists
8. [x] Move execution into `references/execute.md`
   - `SKILL.md` keeps triage and loads the reference only when explicitly asked to execute
   - The reference is the only copy of the checkout, combine, and exclude procedure
9. [ ] Commit and open PR on `.cursor-rules`

## Status

- [x] Initial implementation complete
- [x] Verification checks passed (initial draft)
- [x] Memory bank active state populated
- [x] Portability revision applied
- [x] Execution split into `references/execute.md`
- [ ] Review & PR creation
