# Project Brief: `/niko-chat` Ad-Hoc Entrypoint

Implement [issue #63](https://github.com/Texarkanine/.cursor-rules/issues/63): add a new `/niko-chat` ad-hoc entrypoint that loads the memory bank's persistent context (and is *aware of* but not locked into ephemeral context) so the operator can have free-form Q&A conversations about the codebase without any harness lift.

## Why

AI harnesses don't automatically load the memory bank. There is currently no first-class way to have a memory-bank-aware conversation about the codebase that doesn't either:

- spin up a full `/niko` workflow (creates ephemeral state, classifies complexity, commits to a task), or
- invoke `/niko-creative` (heavier, produces a creative doc, intended to seed future workflow work).

`/niko-chat` fills the gap: read-only, conversational, produces no artifacts.

## Use Cases

1. **Parallel consultation while a workflow is in flight (separate context window).** Ask about an in-progress task without disturbing it. "What's this task about?", "Why did we pick X in the plan?", "What milestones are left?" Loads persistent context and reads ephemeral state without mutating either.

2. **Codebase Q&A when nothing is in flight.** Lightweight questions about how the project works without the ceremony of `/niko-creative`. "How does the archive work?", "Where would I add a new ruleset?"

3. **Pre-task scoping / thinking out loud.** Mulling whether something is even a thing, before committing to `/niko`. May naturally lead to a `/niko` invocation later, but chat itself seeds nothing on disk.

## Non-Goals

- Chat must NOT modify ephemeral state, write to memory bank, or kick off workflows.
- If the conversation reveals real work needs doing, chat hands off explicitly ("sounds like you want `/niko` for this") rather than silently doing it.

## Naming Decision

`/niko-chat` (not `/nk-chat`, not `/niko-with`).

- `-chat` over `-with`: clearer intent, more natural verb.
- `niko-` over `nk-`: it is definitionally an ad-hoc entrypoint (peer to `niko-creative`), not a circuit breaker that mutates live workflow state. The `nk-*` namespace is reserved for in-workflow state-mutating interventions (`nk-refresh`, `nk-save`).

## Deliverables

1. New skill: `rulesets/niko/skills/niko-chat/SKILL.md`
2. README updates in `rulesets/niko/README.md`:
   - Document `/niko-chat` under "Ad-Hoc Entrypoints" with its three use-cases and non-goals.
   - Add a short, explicit naming-convention note distinguishing `niko-*` (entrypoints/phases) from `nk-*` (circuit breakers) so the convention isn't reverse-engineered by the next contributor.
