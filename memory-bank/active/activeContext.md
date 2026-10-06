# Active Context

## Current Task: dependabot-janitor
**Phase:** BUILD - IN-PROGRESS (PR 132 at 2bde729)

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
- Review on PR 132: `gh pr create` had no `--title`, `--body-file`, or `--base`, and no `git push`. The `groups` edit ran after the pull request was opened. The triage index had no Hold / Blocked section. The draft milestone named a local worktree alias. The brief quoted the external source it forbids.
- Rework: push, then `gh pr create --base --title --body-file`, on both create paths. `groups` is committed before the pull request. The index template includes Hold / Blocked. The alias and the external source name are gone from `memory-bank/`.
- A combine stops before the commit when a gating check cannot be run or exits non-zero. Pushed as `828e5cd`.
- `groups` and `ignore` are appended under an existing key. `<body-file>` is created outside the worktree. Pushed as `2bde729` on [PR 132](https://github.com/Texarkanine/.cursor-rules/pull/132).
- Review on PR 132: `gh pr view --repo <owner>/<repo>` and `gh repo clone <owner>/<repo>` drop the host from a GitHub Enterprise URL. Operator: that is the skill pretending to be a parser. The URL in the prompt is already the `gh` argument. Fix the command lines; do not rewrite the skill.

## Next Step
- The URL pass-through edit is committed locally. PR 132 stays at `2bde729` until that commit is pushed.
- The skill is not linked from a ruleset; that install path is a follow-up.
