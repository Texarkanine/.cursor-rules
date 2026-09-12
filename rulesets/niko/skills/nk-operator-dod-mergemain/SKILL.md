---
name: nk-operator-dod-mergemain
description: Definition of Done - Merge to Main via Serial Landing and Rebase
---

# Definition of Done: Merge to Main

This skill defines the autonomous landing Definition of Done (DoD) for `/nk-operator`. Each task is driven through implementation, PR creation, review stabilization, clean archiving, and serial landing into the target base branch with automated merge conflict reconciliation.

## Success Criteria

A wave is considered complete under `mergemain` when all of the following conditions are met:

1. **PR Ready Gate Satisfied:** Every task in the wave completes the full requirements of `/nk-operator-dod-prready`:
   - TDD implementation and passing test suite.
   - QA pass.
   - Non-draft pull request opened.
   - Continuous integration green (max 2 fix attempts).
   - Review bots and comments evaluated via `/pr-feedback-judge` with all critical findings resolved (max 3 loops).
   - Archive completed on the pull request branch, producing a single permanent archive document and deleting `memory-bank/active/`.
2. **Serial Landing Protocol:** Pull requests are merged one at a time into the base branch. Never attempt concurrent bulk merges of sibling branches.
   - Inspect the candidate pull request status: `gh pr view <pr-number> --json mergeable,mergeStateStatus,statusCheckRollup`.
   - When checks are green and the merge status is clean, squash-merge the pull request into the base branch: `gh pr merge <pr-number> --squash --delete-branch=false`.
   - Update the primary repository checkout: `git checkout <base-branch> && git pull origin <base-branch>`.
3. **Rebase and Conflict Reconciliation:**
   - Before landing the next pull request, rebase its branch in its worktree onto the updated base tip:
     ```bash
     git -C <worktree-path> fetch origin
     git -C <worktree-path> rebase origin/<base-branch>
     ```
   - If rebase conflicts occur on shared artifacts (such as lockfiles, documentation, or common utility modules):
     1. Dispatch or resume a worker in that worktree to resolve the conflict.
     2. The worker resolves conflicts, runs the full test suite locally, and verifies all tests pass.
     3. The worker completes the rebase and force-pushes with lease: `git -C <worktree-path> push --force-with-lease`.
   - Await green continuous integration status checks on the rebased pull request.
4. **All Pull Requests Landed:** Repeat steps 2 and 3 sequentially until every pull request in the wave is merged into the base branch.
5. **Clean Teardown:**
   - Remove all worker worktrees: `git worktree remove <worktree-path>`.
   - Retain all local and remote branches. Do not delete git branches.
6. **Operator Branch Disposition:** Once all task pull requests are landed, evaluate the operator's orchestration branch against `<base-branch>`. If it contains a systems capstone archive or durable persistent updates, squash-merge it into `<base-branch>`; otherwise, abandon or delete the operator branch cleanly without an unnecessary commit.
