# Project Brief

## User Story

As a Cursor rules consumer, I want a minimal alwaysApply rule that steers agent prose toward STE-inspired plain technical English, so that agent communication is clearer and the rule names ASD-STE100 as a decompression key for the full standard.

## Use-Case(s)

### Use-Case 1

An agent with the rule installed writes chat and status prose using short sentences, one idea per sentence, active voice, consistent wording, and no idioms — without claiming full ASD-STE100 dictionary compliance.

### Use-Case 2

A human reading the rule sees the names **ASD-STE100** and **Simplified Technical English** so they can look up the official standard at https://www.asd-ste100.org/.

## Requirements

1. Add `rules/asd-ste100.mdc` as an alwaysApply (`alwaysApply: true`) GlobalPrompt rule.
2. Keep the rule minimal in scope and length (STE-inspired constraints, not the full dictionary).
3. Explicitly name **ASD-STE100** and the full name **Simplified Technical English** so the rule functions as a decompression key.
4. Do work on a feature branch.
5. Open a pull request when the work is ready.

## Constraints

1. Canonical source is `rules/` (do not edit generated `.cursor/` / `.claude/` trees).
2. Do not claim full ASD-STE100 compliance or reproduce the copyrighted dictionary.
3. Follow repo markdown/prompt-authoring conventions (headings, reserve absolutes, no heading parentheticals).
4. Licensing via existing `REUSE.toml` path annotations for `rules/**/*.mdc` (PPL-S); no REUSE.toml change needed if only that path is added.

## Acceptance Criteria

1. `rules/asd-ste100.mdc` exists with `alwaysApply: true` and STE-inspired prose constraints.
2. The rule body names ASD-STE100 and Simplified Technical English (decompression key).
3. Work landed on a feature branch with a PR opened.
4. `make test` passes.
