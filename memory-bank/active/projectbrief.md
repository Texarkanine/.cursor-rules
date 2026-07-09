# Project Brief: Persistent-File Rule Update Contract

## User Story

As the operator of the Niko system, I want the persistent memory-bank guidance rules to clearly define what belongs in each file and when it may be updated, so that any agent who picks up the glob-attached rule — inside or outside a Niko workflow — treats the file as update-only-on-invalidation instead of glomming session residue onto it.

## Background

Two observed failures (a zbcli `systemPatterns.md` and the FoxForge-GG `AGENTS.md` pseudo-memory-bank) show non-niko agents appending subsystem deep-dives and task narratives to persistent files. Root cause analysis and the amendment design were resolved in `memory-bank/active/creative/creative-persistent-file-update-contract.md` (standalone creative exploration, operator-refined): the rules define creation but not stewardship, and their exclusion criteria filter triviality, not altitude.

## Requirements

1. Amend `rulesets/niko/niko/memory-bank/systemPatterns.mdc` (primary deliverable):
    - Flesh out the what-belongs definition: add the altitude test (a pattern is something you must know to safely change *other* parts of the system) as a fourth "Avoid" item covering subsystem deep-dives.
    - Defuse the "can be appended to later" invitation in "How to Create" by deferring to the update contract.
    - Add a compact, generic "When to Update" section: default is no action; update only when completed work made content factually wrong or materially incomplete; surgical fixes only; when in doubt, don't.
2. Amend `productContext.mdc` and `techContext.mdc` with proportionate "When to Update" sections (same contract, file-appropriate examples).
3. No cross-reference to `reconcile-persistent.md` — the rules are the authority it consults, not vice versa.
4. Prose per `markdown-style.mdc` (short portable headings, no hard wrap) and the prompt-authoring skill (reference-kind, no filler, reserved absolutes, concrete endings).
5. Edit canonical sources only (`rulesets/`), never `.cursor/` or `.claude/` copies.

## Out of Scope

- Changes to `reconcile-persistent.md` (stays as-is).
- Option D from the creative doc (guard line in generated `.md` templates for rule-less harnesses) — deferred follow-on.
- Regeneration of `.cursor/` / `.claude/` copies (ai-rizz / a16n deployment flow).
