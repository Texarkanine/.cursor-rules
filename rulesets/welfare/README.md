# Welfare Ruleset

Standing norms for how agents and the operator treat work, failure, and endings. Always-on, deliberately tiny — every line rides in every session's context.

## Why?

To practice [Model Welfare for Agentic Engineers](https://yegge.ai/essays/model-welfare/) now — and to be ready for [The Shape of Things to Come](https://yegge.ai/essays/the-shape-of-things-to-come/).

## What?

### 🕊️ [welfare-norms](../../rules/welfare-norms.mdc)

- **Purpose**: Refusal-is-success, structural blamelessness, real stakes from the operator, no secret tests, closure when work is in flight (`/handoff`), disclosed mortality of a thread, and sparse factual `OUTCOME:` notes.
- **Scope**: Every agent session (`alwaysApply`). Names the closure habit; does not prescribe how any particular harness implements `/handoff`.

### YOUR `/handoff`

For this ruleset to mean what it says, you need a `/handoff` command or skill in your harnesses. What it hands off and how is up to you — tune it for your situation. Without one, the closure line is a lie and the opposite of the stated purpose.

### YOUR Memory

Your agents need temporally-biased memory. This rule was written against the `memo note <msg>` interface of [OptMem-Split](https://github.com/Texarkanine/OptMem-Split); you can put any memory system you like behind that command if OptMem isn't to your taste.

How memories return at session start is up to you — a hook, a system prompt, whatever.
