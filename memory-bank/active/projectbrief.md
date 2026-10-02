# Project Brief

## User Story

As a developer and maintainer managing dependency updates across repositories, I want a `/dependabot-janitor` skill that triages, assesses, and remediates open Dependabot pull requests — combining interdependent peer bumps and configuring `.github/dependabot.yaml` exclusions for breaking or premature updates — so that I can short-circuit manual triage and clean up dependency backlogs with consistent, receipted decisions.

## Use Cases

### Use-Case 1: Queue URL or List Triage
I pass a URL (e.g. `https://github.com/pulls/assigned`) or paste a list of pull requests. The skill parses each PR, identifies the repo and package bump type, checks CI and test protection, and renders a structured disposition index (Merge Ready, Combine, Exclude & Close, Caution / Manual Review, Hold / Blocked, Manual / Operational).

### Use-Case 2: Execution of Combined Updates
When interdependent packages are bumped in isolation by Dependabot and fail with peer dependency errors (e.g. Vitest ecosystem), the skill creates an isolated worktree off fresh `main`, upgrades the packages in lockstep, verifies test suites and build gates locally, opens a unified PR, and closes the original split PRs with cross-references.

### Use-Case 3: Execution of Dependabot Exclusions
When a major bump is premature or incompatible with project architecture (e.g. TypeScript 7 or Node engine floor mismatches), the skill opens an isolated worktree off fresh `main`, adds an `ignore` rule to `.github/dependabot.yaml`, opens an exclusion PR, and closes the original PR with an explanation detailing why excluding is correct now and when adoption will become appropriate.

## Requirements

1. Flexible input ingestion: GitHub queue URLs, PR URLs, pasted markdown/text lists, or automatic discovery via `gh search prs --state open --assignee @me`.
2. Author filtering: identify human/operational PRs and exclude them from automated dependency triage.
3. Deterministic guards: never auto-merge major version bumps unattended.
4. Honest CI diagnosis: identify peer dependency resolution splits (`ERESOLVE`) vs genuine code regressions vs baseline mismatches.
5. Protective test gate requirement: demand that PR-gating CI actually exercises the touched surface.
6. Structured disposition index presented before taking write actions.
7. Isolated execution with stock `git worktree` and stock `gh` only. No shell aliases, wrapper commands, or other CLIs.
8. Receipted closures: provide explicit "why" and "when" rationales when closing rejected PRs.
9. Commits and merges follow the target repository: its base branch, package manager, commit style, and merge method. No operator-specific commit trailer.

## Constraints

1. **Strict constraint**: Do NOT link to or reference external blog posts or company names (`tech.zenbusiness.com` or ZenBusiness) anywhere in the final content. All triage and remediation patterns must be internalized as native principles.
2. Canonical `rules/dependabot-janitor/SKILL.md` file layout under 500 lines.
3. `make test` must pass (valid ruleset symlinks, no broken README links, verification tests green).
4. No change-detector tests for prose wording per `always-tdd` carve-out.

## Acceptance Criteria

1. `rules/dependabot-janitor/SKILL.md` exists with valid YAML frontmatter and clear trigger description.
2. Ingestion handles URLs, pasted lists, and CLI discovery.
3. Evaluation rubric covers all five core dispositions plus manual/operational filtering.
4. Execution procedures provide stock `git` and `gh` instructions for combines and excludes, including `git worktree`.
5. Zero references to external blog posts or company names.
6. `make test` runs and passes.
