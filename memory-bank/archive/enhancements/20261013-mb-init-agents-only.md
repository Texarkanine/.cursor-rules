---
task_id: mb-init-agents-only
complexity_level: 2
date: 2026-10-13
status: completed
---

# TASK ARCHIVE: Memory-bank init writes AGENTS.md only

## SUMMARY

Niko's first-init root bootstrap now writes only a thin `AGENTS.md`, and only when root `AGENTS.md` is absent. `CLAUDE.md` is never created and no longer affects the gate. Claude Code reads repo-root `AGENTS.md` directly, so the `@AGENTS.md` shim from issue #101 is retired. Preflight was `PASS WITH ADVISORY`; QA was `PASS`; `make test` was green. Non-draft PR #135 is open on `niko-no-CLAUDE.md`.

## REQUIREMENTS

1. Remove the `CLAUDE.md` template and all pair wording from `memory-bank-init.md`. Init installs only `AGENTS.md`.
2. Gate on root `AGENTS.md` alone: create when absent, skip when present. `CLAUDE.md` plays no part (operator decision, 2026-10-12). This replaced the recommended "skip if either exists".
3. Keep presence semantics (regular file or symlink), the no-edit-through-symlink rule, the no-append/rewrite rule, and the skip advisory.
4. Update the matching sentence in `rulesets/niko/README.md`.
5. `make test` passes. A non-draft PR is open and a `/handoff` note was left (done before this archive: PR #135).

## IMPLEMENTATION

Prose-only edit of two canonical files. The four-row `AGENTS.md` × `CLAUDE.md` decision table and the `CLAUDE.md` template were deleted. The `AGENTS.md` template text and the line-28 read-only anti-duplication scan (which still lists `CLAUDE.md` among docs a consumer repo may already have) were left as they were. One sentence states that init never creates `CLAUDE.md`.

- `rulesets/niko/skills/niko/references/core/memory-bank-init.md` — section retitled `### Root bootstrap file`; gate, advisory, and genericity wording singularized.
- `rulesets/niko/README.md` — line 36 describes the `AGENTS.md`-only behavior.

Generated `.cursor/` and `.claude/` trees were left for the operator's `chore(dev): ai-rizz sync`. No creative phase. Persistent memory-bank files were unchanged: the system shape did not move.

## TESTING

No new automated tests. Both edits are skill wording and repository-bootstrap text, which `always-tdd` places out of scope. A content assertion would be a change-detector.

- `grep -rn CLAUDE rulesets/` shows the line-28 scan and the planned "never creates `CLAUDE.md`" sentence only. `grep -R` and `git grep` also show `always-tdd.mdc:14` through a symlink; that hit is expected.
- `make test` green (symlink checks, README-link checks, 100 unittest).
- Preflight `PASS WITH ADVISORY` (Opus; Fable 5.1 was out of credits). Advisories: AC 6 had no tasks.md step (the orchestrating session did it); verify-grep tools that follow symlinks will show extra expected hits; a paste-in pointer when an existing `AGENTS.md` never mentions `memory-bank/` was raised and not applied.
- QA `PASS` against `main...HEAD` on the canonical `rulesets/` files. One kept redundancy: "do not follow symlinks to edit through them" overlaps "do not symlink-replace it" now that init never edits an existing file. Requirement 3 keeps both sentences.

## LESSONS LEARNED

- Issue #101's both-absent gate rested on a harness fact the rule never stated: Claude Code ignoring `AGENTS.md`. When a rule exists only for compatibility, it can name the harness behavior it covers, so the rule can be retired when that behavior changes.
- Base verify expectations (grep hits, counts) on the planned end state. The plan's grep listed only the pre-existing line 28 and forgot the sentence the plan itself added. The build corrected the expectation, not the content.

## PROCESS IMPROVEMENTS

None beyond the lesson above. The file list, sequence, and scope were right; the build was a straight run.

## TECHNICAL IMPROVEMENTS

Preflight advisory 3, left for the operator: most consumer repos already have an `AGENTS.md`, so the skip path is the common one and today only prints a general advisory. A read-only check could say so when that file never mentions `memory-bank/`, and print a pointer the operator can paste (the template's first paragraph plus the three persistent-file bullets), still without editing the file. Separate product decision; not part of this task.

## NEXT STEPS

Merge PR #135, then run `chore(dev): ai-rizz sync` so the generated `.cursor/` and `.claude/` trees match `rulesets/`.
