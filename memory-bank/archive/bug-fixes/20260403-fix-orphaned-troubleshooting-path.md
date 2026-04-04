---
task_id: fix-orphaned-troubleshooting-path
complexity_level: 2
date: 2026-04-03
status: completed
---

# TASK ARCHIVE: Fix Orphaned Troubleshooting Path

## SUMMARY

Corrected `/nk-refresh` so diagnostic scratch logs live under `memory-bank/active/troubleshooting/` (with explicit `troubleshooting-<YYYYMMDD-HHmmss>.md` filenames), registered them in the ephemeral file glossary, documented that they are deleted without inlining during archive, and added `troubleshooting/` to `/niko` selective cleanup (L4 Step 2a and standalone rework Step 3b). Follow-up PR edits simplified wording (“distilled learning belongs in the reflection”) and replaced per-item “(if present)” with a single qualifier on delete lists.

## REQUIREMENTS

- Stop writing ephemeral troubleshooting logs outside `active/` so archive and cleanup contracts apply.
- Register path and lifecycle in `memory-bank-paths.mdc`; archive exception in `archives.mdc`.
- Extend `/niko` milestone-advance and rework delete lists for `troubleshooting/`.
- Edit only canonical `rulesets/` (`.cursor/` / `.claude/` synced out-of-band).
- Avoid same-day filename collisions (datetime in filename, not date-only).

## IMPLEMENTATION

**Canonical files (rulesets):**

- `rulesets/niko/skills/nk-refresh/SKILL.md` — path + filename pattern.
- `rulesets/niko/niko/core/memory-bank-paths.mdc` — Troubleshooting Docs ephemeral entry.
- `rulesets/niko/niko/memory-bank/archives.mdc` — exception: no inlining; learning captured in reflection.
- `rulesets/niko/skills/niko/SKILL.md` — Step 2a and Step 3b delete lists (with affirmative “delete existing items” style phrasing after iteration).

**Process:** Full Niko Level 2 flow (plan → preflight → build → QA → reflect) before archive.

## TESTING

No automated test suite for rule markdown. Validation: `rg` over `rulesets/` for stale `memory-bank/troubleshooting` without `active/`; semantic QA on edited files; PR review iterations for timestamp format and wording.

## LESSONS LEARNED

From reflection (inlined):

- Niko uses two deletion patterns: **archive phases** wipe ephemeral under `active/` broadly; **`/niko` entrypoint** uses **selective** delete lists in Steps 2a and 3b. New ephemeral subdirectories must be added to the selective lists when they need clearing between milestones or on rework—even if archive would catch them on full task completion.
- Vague `<timestamp>` led agents toward date-only naming (like archives); explicit `<YYYYMMDD-HHmmss>` prevents same-day collisions without UUIDs or directory scans.
- “Distilled learning belongs in the reflection” is the right anchor; archive gets that content via reflection inlining, not by duplicating troubleshooting scratch.

## PROCESS IMPROVEMENTS

- When adding a new ephemeral directory under `active/`, checklist: (1) `memory-bank-paths.mdc`, (2) archive inlining rules if needed, (3) `/niko` Step 2a + 3b if applicable.

## TECHNICAL IMPROVEMENTS

None beyond the contract fixes above.

## NEXT STEPS

None for this task. Re-sync installed copies (`ai-rizz` / `a16n`) in consumer repos so `.cursor/` and `.claude/` reflect `rulesets/`.
