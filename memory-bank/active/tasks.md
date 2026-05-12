# Tasks: Positive-Principle Reframe for Memory Bank VCS Tracking

## What broke

Some AI models read the word "ephemeral" in `rulesets/niko/niko/core/memory-bank-paths.mdc` as "should not be committed to VCS." Observed failure modes: skipping `memory-bank/active/` files when staging commits; adding `memory-bank/active/` to `.gitignore`.

## Why

The rule named one category by a property ("ephemeral") that is semantically loaded toward *throwaway / not durable* in dev contexts. A previous corrective sentence at the bottom of the Ephemeral section told models to commit the files anyway, but it fights the noun rather than removing the ambiguity.

## What changed

`rulesets/niko/niko/core/memory-bank-paths.mdc`:

- Added a **Guiding principle** paragraph immediately after the `**CRITICAL:**` opener: *"The memory bank is the project's tracked working tree of context. Every file under `memory-bank/` is a versioned artifact — created, modified, and committed to source control as work progresses, and pruned only by an explicit archive step. The categories below distinguish files by lifetime (does this survive across tasks?), not by durability in source control."*
- Rewrote the trailing sentence in the Ephemeral section to keep only the lifetime semantics (execution trace, cleaned up by archive phase) and drop the now-redundant VCS-tracking reassurance.

## Files affected

- `rulesets/niko/niko/core/memory-bank-paths.mdc`
