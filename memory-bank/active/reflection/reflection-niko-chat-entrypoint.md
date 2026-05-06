---
task_id: niko-chat-entrypoint
date: 2026-05-06
complexity_level: 2
---

# Reflection: Add `/niko-chat` Ad-Hoc Entrypoint

## Summary

Added `/niko-chat`, a read-only memory-bank-aware Q&A skill, plus a README paragraph documenting the previously-implicit `niko-*` (entrypoints/phases) vs `nk-*` (circuit breakers) namespace convention. Closes issue #63. Built clean to plan.

## Requirements vs Outcome

All 8 plan behaviors and 4 edge cases delivered. Two non-plan additions made it into the skill body — a "When to Use This vs. Other Entrypoints" section and a "Step 5: Ending the Chat" — both reinforce the read-only contract or routing logic and were sanity-checked against YAGNI in QA. No requirements dropped or descoped.

## Plan Accuracy

Plan was accurate. Sequence held, file list held, scope held. The challenges identified (read-only contract enforcement, `/niko-creative` differentiation, naming-paragraph placement, no-test-infra) all surfaced as real constraints during build. The preflight-identified "structured Context Loaded summary" improvement was within scope and folded in cleanly.

## Build & QA Observations

Build was smooth. The only QA finding was a trivial template inconsistency: the "Context Loaded" greeting's closing prompt (`What would you like to discuss?`) was unconditional, but the same Step 2 also instructed the agent to "proceed directly to answering" when a question was provided alongside the invocation. That would have produced "What would you like to discuss?" immediately before answering a question the operator already asked. Fix was a one-edit clarification splitting the two cases.

## Insights

### Technical

- Skill `description:` frontmatter does double duty as a human label *and* the agent's invocation router. For commands with nuanced trigger conditions (like chat: "ask, don't do; loads memory bank; safe to use parallel to in-flight work"), a longer description is a feature — it raises invocation precision. Short descriptions like `niko-creative`'s ("Creative Phase - Design Exploration") work for unambiguous-trigger skills but would underspecify chat.

- Conditional output templates need explicit branch documentation, not just inline guidance prose. An agent told "use this exact shape: [template]" *and* "but proceed directly to answering if X" will tend to print the literal template. Splitting the template into "always print this" + "branch on input" eliminates the ambiguity.

### Process

- The `always-tdd.mdc` rule's "if no test infra exists, STOP AND ASK" clause is well-meaning but misfit for documentation/skill-only repos. There is no test infra and no plausible way to create one for markdown skill files; the established pattern (preflight + QA semantic review) is the actual validation mechanism. Worth considering: a niko system enhancement that pattern-matches on task type (code-producing vs doc-only) and routes the TDD check accordingly. **Out of scope here, flagged for future.**

- Preflight on documentation/skill tasks is mostly a convention/coherence check; the "TDD blocking" check forces transparent justification rather than blocking work, which is fine but could be more graceful. Same future-improvement flag as above.

### Million-Dollar Question

> What's the most elegant solution if `/niko-chat` had been a foundational assumption from the start?

Probably nothing dramatically different in the skill itself — the structure (load context → greet → loop → handoff) is roughly forced by the read-only-with-memory-bank constraint. But the *namespace convention* would have been documented up-front as part of the original ruleset README, not retrofitted later as a "wait, what's the rule?" moment. The lesson generalizes: implicit conventions that emerge from a small sample (here: 8 commands) should be made explicit *before* the next contributor needs to extend the pattern, not when they get there.
