---
task_id: dependabot-janitor
complexity_level: 2
date: 2026-10-07
status: completed
---

# TASK ARCHIVE: Dependabot Janitor

## SUMMARY

Shipped `rules/dependabot-janitor/` so an agent can triage Dependabot pull requests and, when asked, combine peers or add an ignore, using stock `git` and `gh`. Triage, the disposition rubric, and the index stay in `SKILL.md`. Checkout, combine, and exclude stay in `references/execute.md` and load only when execution is requested. Pull request commands take the pull request URL. `gh pr create` passes `--repo` with the repository URL (the pull request URL with `/pull/<number>` removed). Draft PR: [#132](https://github.com/Texarkanine/.cursor-rules/pull/132) at `84a1bb2`.

## REQUIREMENTS

- A skill anyone with a repository, Dependabot, stock `git`, and stock `gh` can run.
- Triage into Merge Ready, Combine, Exclude & Close, Caution / Manual Review, Hold / Blocked, and Manual / Operational. Do not merge major bumps. Close with why and when.
- Isolated checkout with `git worktree`. Base branch, package manager, commit style, and merge method come from the target repository. No local git alias and no operator commit trailer.
- Do not name the external write-up this skill was distilled from, or its publisher.
- Canonical `rules/` only. No ruleset link in this pull request. No change-detector tests on skill wording. `make test` still passes.

Pasted `owner/repo#123`, `owner/repo 123`, and default `gh pr list` / `gh search prs` output were dropped during review. Those forms have no pull request URL, and Step 1 passes the URL through.

## IMPLEMENTATION

`rules/dependabot-janitor/SKILL.md` holds triage. `rules/dependabot-janitor/references/execute.md` holds checkout, lockstep combines, and ignore rules. Combines stop before the commit when a gating check cannot run or exits non-zero, and the split pull requests stay open. `groups` and `ignore` are appended under an existing key. The pull request body file is created outside the worktree. `gh pr create` uses `--base`, `--title`, `--body-file`, and `--repo <repository-url>`.

The command lines changed because of `gh`, not because the rubric was wrong. Rebuilding `owner/repo` from a URL drops the host, so a GitHub Enterprise pull request is read and closed on github.com. `gh repo clone` of a fork sets the parent as the default remote, so `gh pr create` with no `--repo` opens on the parent while `gh pr close <url>` still closes the fork.

## TESTING

No new automated tests. Skill wording is outside `always-tdd`. `make test` passed after the command-line fixes: ruleset symlink check, README link check, and 100 unit tests. `/niko-qa` was not run. There was no `memory-bank/active/.qa-validation-status`. The operator directed `/niko-reflect` anyway, after `/niko-archive` had stopped on the missing reflection.

## LESSONS LEARNED

- The `gh` argument is the URL already in the prompt. Splitting it into owner, repository, and number is what points a GitHub Enterprise URL at github.com.
- `gh pr create` on a fork clone needs `--repo` set to the repository URL. Close still uses the pull request URL.
- Adding `<host>` to `--repo <owner>/<repo>` keeps a parser. The smaller fix is to stop parsing.
- `make test` cannot see an a-la-carte skill under `rules/`. That is not a reason to lock wording with a test.

## PROCESS IMPROVEMENTS

Archive stops when `memory-bank/active/reflection/reflection-<task-id>.md` is missing. A handoff in that gap records a task the next session still has to reflect. Reflect first.

## TECHNICAL IMPROVEMENTS

If "the URL you were given is the `gh` argument" had been the starting rule, Supported Inputs would have been URLs only, and both create commands would have passed `--repo <repository-url>` from the first draft. The disposition rubric would be the same.

## NEXT STEPS

- Merge [PR 132](https://github.com/Texarkanine/.cursor-rules/pull/132) when the operator wants it merged.
- Link the skill from a ruleset in a follow-up. This pull request does not.
