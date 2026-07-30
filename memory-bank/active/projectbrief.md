# Project Brief

## User Story

As the operator triaging review feedback on my own pull requests, I want `/pr-feedback-judge` to retrieve the reviewer's words *and* the current state of the code those words describe, so that its verdicts rest on what is actually true of the branch now rather than on a stale anchor.

## Use-Case(s)

### Use-Case 1: Mid-flight triage on my own PR

I am on the PR's feature branch, reviewers have commented, and I have already pushed fixes for some of it. The skill must tell apart feedback that still applies from feedback the current head already satisfies, and never quote me the code at a line number that has since moved.

### Use-Case 2: Triage from somewhere other than the PR head

I am in the repository but on another branch or commit, or I am not in the repository at all. The skill must still judge correctly, obtaining code by the cheapest sufficient means and saying so when it could not obtain any.

### Use-Case 3: A pull request on a repository I do not own

I point the skill at a PR URL from a temporary directory. Fetching works; the skill must not silently degrade into hunk-only judgment without saying so, and must not attempt a multi-gigabyte clone to answer a question a single file fetch would settle.

## Requirements

1. Classify every inline comment's anchor state from `subject_type`, `line`, and `commit_id` before judging it.
2. Never address current code by `original_line` or `original_commit_id`; retain both for reporting what the reviewer saw.
3. Resolve outdated anchors by locating `diff_hunk` content in the current file, not by line number.
4. Gate code access on need: `diff_hunk` plus the reviewer's text is the default, and escalation happens only when the claim reaches outside the hunk or an outdated anchor must be resolved.
5. Implement the four-tier code-access ladder — at PR head, in-repo at another commit, not in the repository, clone as last resort — with the clone gated behind a repository-size check.
6. Add `already addressed` as a fifth disposition, requiring code evidence rather than mere anchor movement.
7. Project comment and review fetches to the fields the rubric uses, retaining every field anchor classification depends on.
8. Declare which access tier was used, and state plainly when a verdict rests on `diff_hunk` alone.

## Constraints

1. Correctness before economy. A cheaper retrieval that risks judging the wrong text is not cheaper.
2. Never disturb the operator's working state; obtain any needed checkout additively.
3. Cloning is a last resort, gated on `repos/{o}/{r}.size`, because the operator maintains repositories in the tens of gigabytes.
4. Field projection must not strip the fields staleness detection needs.
5. One coordinated change to `rules/pr-feedback-judge/SKILL.md`. The generated `.cursor/` and `.claude/` trees are not touched — they re-sync separately per `systemPatterns.md`.
6. Out of TDD scope per the `always-tdd` carve-out: this is skill wording. A test asserting on `SKILL.md` contents would be a change-detector. Verification is review plus the existing gates.
7. Out of scope: a standalone transport rule, and any PR-review skill.

## Acceptance Criteria

1. The skill body states the anchor-state model and forbids indexing current code by `original_line`.
2. The skill body states the four-tier ladder, its need gate, and the size check before cloning.
3. The disposition vocabulary is five values, with `already addressed` defined and evidence-gated; the triage table and tail counts include it.
4. Fetch recipes carry `--jq` projections that retain `subject_type`, `line`, `original_line`, `commit_id`, `original_commit_id`, `side`, `in_reply_to_id`, `body`, and `diff_hunk`.
5. `Orchestration walkthrough` has a gate-and-escalate step between fetching and filtering; `Failure modes` covers an unreachable code source.
6. `scripts/verify-skillify.py` still passes, and the repository's link CI still passes.
