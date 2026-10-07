---
task_id: dependabot-janitor
date: 2026-10-07
complexity_level: 2
---

# Reflection: Dependabot Janitor

## Summary

Shipped `rules/dependabot-janitor/` so an agent can triage Dependabot pull requests and, when asked, combine peers or add an ignore, using stock `git` and `gh`. The skill is on [PR 132](https://github.com/Texarkanine/.cursor-rules/pull/132) at `84a1bb2`. `/niko-qa` was not run.

## Requirements vs Outcome

The brief's triage rubric, receipted closes, stock `git worktree` and `gh`, and the ban on an external write-up are in the skill. Execution lives only in `references/execute.md` and loads when execution is requested. Two requirements moved during review. Pasted `owner/repo#123`, `owner/repo 123`, and default `gh pr list` / `gh search prs` output were dropped, because Step 1 passes the pull request URL through and those forms have no URL. A ruleset link was never part of this pull request.

## Plan Accuracy

The plan was one `SKILL.md`. The build split checkout, combine, and exclude into `references/execute.md` so triage does not carry the procedure. The surprises were `gh`, not the rubric: rebuilding `owner/repo` drops the host, and `gh pr create` with no `--repo` opens on the parent of a fork.

## Build & QA Observations

Review comments on the command lines were the real defects, and each fix stayed on those lines. `make test` passed (ruleset symlink check, README link check, 100 unit tests) and does not read skill wording. There is no `memory-bank/active/.qa-validation-status`. The operator directed this reflection anyway.

## Insights

### Technical

- The `gh` argument is the URL already in the prompt. Splitting it into owner, repository, and number is what points a GitHub Enterprise URL at github.com.
- `gh repo clone` of a fork sets the parent as the default remote. `gh pr create` needs `--repo` set to the repository URL, the pull request URL with `/pull/<number>` removed. Close still uses the pull request URL.

### Process

- Adding `<host>` to `--repo <owner>/<repo>` keeps the parser. The smaller fix is to stop parsing.
- Archive stops when the reflection file is missing. Handing off in that gap records a task that the next session still has to reflect.

### Million-Dollar Question

If "the URL you were given is the `gh` argument" had been the starting rule, Supported Inputs would have been URLs only, and both create commands would have passed `--repo <repository-url>` from the first draft. The disposition rubric would be the same.
