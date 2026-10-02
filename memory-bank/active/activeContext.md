# Active Context

## Current Task: dependabot-janitor
**Phase:** BUILD - IN-PROGRESS (execution split out)

## What Was Done
- Branched `feat/dependabot-janitor` from clean `origin/main` in `.cursor-rules`.
- Drafted `rules/dependabot-janitor/SKILL.md` with triage dispositions, lockstep combines, Dependabot ignores, and receipted closures. No external blog or company references.
- Operator review: the skill must work for anyone who has a repository, Dependabot, stock `git`, and stock `gh`.
- Revised the skill:
  - Isolated checkouts use `git worktree add -b` and `git worktree remove`. No shell aliases or wrapper commands, and no force-reset of an existing branch.
  - The base branch is the Dependabot PR's `baseRefName`. The package manager, commit style, and merge method come from the target repository.
  - No operator-specific commit trailer.
  - Do not create a Dependabot config that the repository does not already have. When the config exists, group a recurring peer split so the next bump is one PR.
- `gh pr view` and `gh search prs` field lists were checked against `gh` help on this machine.

## Next Step
- Execution lives in `rules/dependabot-janitor/references/execute.md`. `SKILL.md` loads it only when explicitly asked to execute.
- Opening the draft pull request for `feat/dependabot-janitor`.
