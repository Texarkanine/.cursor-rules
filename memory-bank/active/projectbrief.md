# Project Brief: Positive-Principle Reframe for Memory Bank VCS Tracking

## User Story

As the operator of the Niko ruleset, I want the `memory-bank-paths.mdc` rule to state — as a positive guiding principle near the top of the file — that the memory bank is a tracked working tree of context and every file under `memory-bank/` is a versioned artifact. This eliminates the failure mode where some AI models, primed by the word "ephemeral," exclude `memory-bank/active/` files from commits or add them to `.gitignore`.

## Requirements

- Add a positive-principle statement near the top of the `CORE MEMORY BANK FILE LOCATIONS` section in `rulesets/niko/niko/core/memory-bank-paths.mdc` asserting that every file under `memory-bank/` is a tracked, versioned artifact.
- Reframe the persistent/ephemeral split as a *lifetime* distinction, not a *durability-in-VCS* distinction.
- Do NOT rename the "ephemeral" category — the operator considers a rename too high-churn for a long-tail failure mode.
- Do NOT add anti-pattern callouts ("don't gitignore", "don't skip commits"). The positive principle should make those fall out automatically.
- Fold the existing corrective sentence (current line 33) into the new framing so the rule isn't redundant.

## Out of Scope

- Renaming "ephemeral" to anything else.
- Editing other rule files, skills, or memory-bank prose that use the word "ephemeral".
- Adding an `AGENTS.md` or per-directory README in `memory-bank/active/`.
