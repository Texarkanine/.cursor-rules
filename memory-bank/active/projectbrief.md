# Project Brief

## User Story

As an operator running an agent against a finished, behavior-correct codebase, I want a slash-invocable skill `/speedup-giesen` that opens on Fabian Giesen's full 2× / 100× quote and then walks the tree looking for stupid work we can stop doing, so the product gets faster without changing what it does.

## Use-Case(s)

### Use-Case 1

An operator invokes `/speedup-giesen` on a repo that already works (the Sep 6 coachhouse-isp-status pass, and the sibling client-side-mdc-render pass). The agent decompresses into that hunt: find the stupid work, stop doing it, leave behavior alone.

### Use-Case 2

An agent that has the skill installed recognizes a "make it faster without changing what it does / we aren't doing something stupid" request and loads `/speedup-giesen` instead of inventing a micro-optimization pass.

## Requirements

1. Canonical skill at `rules/speedup-giesen/SKILL.md`, invocably named `speedup-giesen` (`/speedup-giesen`).
2. The opening decompression key is the entire Giesen line, attributed, with the operator-confirmed URL `https://x.com/rygorous/status/1271296834439282690`:
    look, I'm sorry, but the rule is simple: if you made something 2x faster, you might have done something smart if you made something 100x faster, you definitely just stopped doing something stupid
3. The body encodes the passover already run by hand: walk a finished, behavior-correct codebase looking for stupid work we can stop doing. Shape it from the coachhouse-isp-status session (`4ca55929-6140-4444-b3eb-d3183f57a455`) and the client-side-mdc-render session (`5dc46b7a-40af-48dd-8e69-fadf1e1caae9`).
4. Edit only canonical source under `rules/` (and a ruleset README/symlink only if Plan finds an existing home that fits). Do not edit generated `.cursor/` or `.claude/` trees.

## Constraints

1. This is prose/policy. Do not add change-detector tests that lock skill wording. `make test` (ruleset layout / README links) must still pass.
2. Do not change product behavior as part of the skill's charter: faster by coding less dumb, not by dropping features or rewriting tests "so they pass."
3. Do not paraphrase Giesen. Cite the entire tweet-body as the opening key.
4. The 50% / 10× wording is a circulating paraphrase; the skill uses Giesen's 2× / 100× original.

## Acceptance Criteria

1. `/speedup-giesen` exists as a skill an agent can invoke.
2. The skill opens on the full Giesen quote with attribution and the confirmed X.com link.
3. Following the skill produces a behavior-preserving hunt for "stop doing something stupid" speedups, not a clever-micro-opt pass.
4. `make test` passes.
