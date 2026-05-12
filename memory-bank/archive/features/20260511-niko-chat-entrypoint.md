---
task_id: niko-chat-entrypoint
complexity_level: 2
date: 2026-05-11
status: completed
---

# TASK ARCHIVE: Memory-Bank Read-Only Chat (`/nk-chat`)

## SUMMARY

Implemented [issue #63](https://github.com/Texarkanine/.cursor-rules/issues/63): a read-only, memory-bank-aware conversational entrypoint so operators can ask questions about the codebase and in-flight Niko state without starting a full `/niko` workflow or producing creative artifacts. Initial delivery used **`/niko-chat`** with README text framing `niko-*` vs `nk-*` as “entrypoints/phases” vs “circuit breakers.” A **2026-05-11** follow-up tightened the documented rule: **`niko-` applies only to commands that appear as phases in the L1–L4 mode transition diagrams in `systemPatterns.md`**. Chat is not a phase, so the public command was renamed to **`/nk-chat`**. Canonical skill directory: **`rulesets/niko/skills/nk-chat/`**. **`niko-creative`** remains `niko-` because CREATIVE is an explicit workflow phase (may still be invoked out-of-band as a convenience).

## REQUIREMENTS

- Load persistent memory bank files (`productContext.md`, `systemPatterns.md`, `techContext.md`) and read ephemeral `memory-bank/active/` state when present, without mutating it.
- Strict read-only contract: no memory-bank writes, no commits, no workflow kickoff, no source edits for the duration of the chat.
- Hand off to `/niko` (or `/niko-creative` when design artifacts are wanted) when the conversation implies real work.
- Graceful behavior when memory bank or files are missing; when no ephemeral files exist, proceed with persistent context only.
- README: document the entrypoint (use cases, non-goals) and an explicit, discoverable `niko-*` vs `nk-*` naming convention for contributors.

## IMPLEMENTATION

- **`rulesets/niko/skills/nk-chat/SKILL.md`**: AgentSkills.io-style frontmatter (`name: nk-chat`), ordered load steps (persistent → ephemeral → optional archive skim), structured “Context Loaded” greeting with conditional branches for “question provided at invoke” vs not, conversational loop, explicit non-goals and handoff triggers. Skill evolved from an initial `niko-chat` path during the naming refinement.
- **`rulesets/niko/README.md`**: “Naming Convention” subsection updated to the **phase-based** falsifiable test; “Ad-Hoc Entrypoints” documents **`/nk-chat`** (read-only Q&A, three use cases, no artifacts). `niko-creative` remains documented as phase-backed `niko-` ad-hoc creative exploration.

## TESTING

No automated test harness for markdown skills in this repository. Verification followed the established Niko pattern: `/niko-preflight` PASS, `/niko-qa` PASS (including semantic check against planned behaviors and edge cases), `/niko-reflect` with reflection file written. One QA fix during original build: conditional closing prompt in the “Context Loaded” template so a supplied question is not followed by “What would you like to discuss?”

## LESSONS LEARNED

**Inlined reflection (`reflection-niko-chat-entrypoint.md`, 2026-05-06):**

- Skill `description:` frontmatter doubles as the agent’s invocation router; nuanced commands may need longer descriptions than simple phase labels.
- Conditional output templates need explicit branch documentation; otherwise agents may print literal template text when prose says to skip part of it.
- Implicit conventions from a small command set should be documented **before** the next extension, not under pressure.
- Workspace “tests first” rules are a poor fit for doc-only skill work; preflight + QA semantic review functioned as the real quality gate (flagged as a possible future workflow improvement, out of scope).

**Post-reflect naming refinement (2026-05-11):**

- Framing `nk-*` only as “circuit breakers” was imprecise (e.g. `/nk-save` is cadence/persistence, not only an emergency stop). The **phase diagram** test is stricter and easier to justify to new contributors.
- README sections are part of the operator-facing contract for categorization; small wording changes have high leverage for future agent routing.

## PROCESS IMPROVEMENTS

- Consider pattern-matching task type (code vs doc-only) so TDD expectations do not create recurring friction for skill-only changes without a test runner.

## TECHNICAL IMPROVEMENTS

- None required for closure. Optional: align any remaining docs or tooling that still say `/niko-chat` if found outside this archive.

## NEXT STEPS

None.
