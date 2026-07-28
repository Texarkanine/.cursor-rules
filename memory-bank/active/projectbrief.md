# Project Brief

## User Story

As a PR author, I want `pr-feedback-judgier` synced with `main` and conflicts resolved so that the open PR can be updated cleanly after main's skill reformatting.

## Use-Case(s)

### Use-Case 1

Merge current `main` into `pr-feedback-judgier`, resolve the conflict in `rules/pr-feedback-judge/SKILL.md` (keep this branch's judge-gating behavior while adopting main's reformatting), and push the result to `origin`.

## Requirements

1. Sync `pr-feedback-judgier` with current `main`.
2. Resolve conflicts, especially in `rules/pr-feedback-judge/SKILL.md`.
3. Preserve this branch's functional changes (feedback gating) while incorporating main's reformatting.
4. Push the updated branch to update PR #91.

## Constraints

1. Do not force-push unless required and explicitly requested.
2. Prefer a merge (or rebase if already the branch convention) that keeps history reviewable.
3. Commit with `--no-gpg-sign` and use `git --no-pager` for git commands.

## Acceptance Criteria

1. Branch includes latest `main` commits.
2. No unresolved conflict markers remain.
3. `rules/pr-feedback-judge/SKILL.md` retains gating semantics and matches main's formatting conventions where applicable.
4. Updated branch is pushed to `origin/pr-feedback-judgier`.
