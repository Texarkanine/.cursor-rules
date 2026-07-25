# System Patterns: Cursor Rules Repository

## How This System Works

This repo is the *canonical source* for a set of Cursor customizations. External tools compile and distribute them: `ai-rizz` installs them into consumer `.cursor/` trees, and `a16n` converts them to other harnesses. The `.cursor/` and `.claude/` trees committed here are *generated copies* — never edit them; edit only `rules/` and `rulesets/`.

The repo is also self-hosting: it both *defines* the Niko memory-bank system (under `rulesets/niko/`) and *uses* Niko to manage its own work (the `memory-bank/` at the repo root). A change to Niko's rules therefore changes how this very repo is developed. Because the Niko rules are in effect while working here, these persistent files must not restate what those rules already say — point at the canonical rule instead of copying it, or it will drift.

## File Organization
Source content in `rulesets/` and `rules/` is the source of truth. Two active tiers, distinguished by semantics:

1. **Rules** (`.mdc`) — Cursor auto-injects based on `alwaysApply` (GlobalPrompt) or `globs` (FileRule) frontmatter.
2. **Skills** (`<name>/SKILL.md` directory) — agent-selected SimpleAgentSkill and slash-invoked ManualPrompt (`disable-model-invocation: true`). Rich skills with `references/` subdirectories live under `rules/` and are symlinked into the appropriate ruleset's `skills/` directory.

Standalone frontmatter-less Commands (`.md`) are no longer an authoring tier in this repo; former commands are ManualPrompt skills. `.cursor/` and `.claude/` contain active copies produced by `ai-rizz` / `a16n`. Never edit those trees — only `rulesets/` and `rules/`.

## Workflow Invocation is Explicit Consent

Invoking a Niko workflow or skill (e.g. `/niko-build`, `/nk-save`) is itself the operator's present-tense authorization for every action that workflow prescribes — commits, edits, shell execution — satisfying harness safeguards that gate on "explicit user request". The consent header is deliberately *duplicated* inline across every commit-prescribing workflow and skill file rather than centralized; the duplication is load-bearing and grep-verifiable, so don't DRY it away. Actions beyond what the workflow prescribes still require a separate ask.

Verbatim duplication as a grep-verifiable tripwire is a recurring technique here, not a one-off: the persistent-file update contract uses it too ("factually wrong or materially incomplete", shared between the memory-bank guidance rules and `reconcile-persistent.md`). Before consolidating repeated phrasing in rule content, check whether the repetition is the mechanism.

## Archive Pattern

Archives live at `memory-bank/archive/<kind>/YYYYMMDD-<task-id>.md` and must be self-contained: ephemeral content is inlined rather than linked, so nothing breaks once the active state is cleared.
