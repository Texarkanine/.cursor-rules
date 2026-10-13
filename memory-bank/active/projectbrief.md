# Project Brief

## User Story

As the operator of `choose-verification-model`, I want Gemini 4 Argon and Claude Haiku 5.5 in the verification catalog, at tiers A and C, so that Niko preflight and QA can select them the hour they ship.

## Use-Case(s)

### Use-Case 1

Gemini 4 Argon has a BenchLM page and a Cursor model page. Refresh the catalog and set its tier to A.

### Use-Case 2

Claude Haiku 5.5 is available to select. Refresh the catalog and set its tier to C.

## Requirements

1. Onboard Gemini 4 Argon through the catalog refresh, then set its tier to A.
2. Onboard Claude Haiku 5.5 through the catalog refresh, then set its tier to C.
3. Leave existing mapping rows unchanged.

## Constraints

1. Tiers are hand-set in `tiers.toml`. Refresh never derives a tier from a score and never writes that file.
2. Edits stay in `rules/choose-verification-model/`. The generated `.cursor/` tree is not part of this task.

## Acceptance Criteria

1. The catalog contains Gemini 4 Argon at tier A and Claude Haiku 5.5 at tier C.
2. `pick.py` accepts each model's Cursor spelling.
3. A second refresh keeps those tiers and does not rewrite existing mapping rows.
