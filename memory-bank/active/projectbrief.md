# Project Brief

## User Story

As an agent authoring (or reviewing) project architecture documentation, I want a Cursor skill that encodes principles for writing good architecture docs — derived from studied golden examples — so that new architecture docs explain the system the way those goldens do, for the same underlying reasons, rather than by copying surface recipes.

## Use-Case(s)

### Use-Case 1

An agent is asked to write or improve a project's architecture documentation. It loads this skill and applies the principles (audience, diagram choice, section structure, what to omit, how to relate code to concepts) instead of inventing ad-hoc structure or mimicking a single template.

### Use-Case 2

During planning/creative work on a new subsystem, an agent consults the skill to decide *what kind* of architecture explanation is warranted and how to open it — guided by principles backed by local golden case studies (stockroom, ai-rizz, a16n) plus a few operator-selected FOSS supplements.

## Requirements

1. Deliver a Cursor **skill** (canonical home in `.cursor-rules`) on writing good architecture documentation.
2. Content must be **principle-first**: for each observed good practice in the case studies, back out the principle that made it right — not surface prescriptions (e.g. not "open with a control-flow diagram," but "open with a diagram that \<principle\>," which in the studied goldens often manifested as control flow done a specific way).
3. **Evidence hierarchy:** local goldens are primary — `stockroom/docs/architecture`, `ai-rizz/docs/developer-guide`, and (weaker but in-set) a16n `understanding-conversions`. FOSS examples are supplements to enlarge sample size; the operator picks which FOSS count.
4. Research local goldens via `sr-search` / `sr-query` and git history of the branches/commits that introduced those docs, to understand *why* they turned up as good examples.
5. Begin with a wide FOSS survey of architecture (or architecture-like) documentation; operator signals which are supplemental goldens. For those, inspect git history / PRs that introduced the docs.
6. Encode the derived principles in the skill (with case-study grounding as needed for agent followability).

## Constraints

1. Do not rewrite stockroom / ai-rizz / a16n architecture docs as part of this task — the deliverable is the authoring skill only.
2. Prefer principles over checklists of surface moves; recipes are only acceptable when they clearly instantiate a stated principle.
3. Keep FOSS analysis secondary; do not let FOSS redefine what "good" means relative to the local goldens.
4. Subagents may help with survey/history collection, but do not fracture primary context — synthesize into one coherent principle set.
5. Follow repo conventions for skill placement (canonical sources under `rulesets/` / skills trees as applicable; do not edit installed `.cursor/` copies of shared assets).

## Acceptance Criteria

1. A skill exists in `.cursor-rules` that an agent can load when writing architecture documentation.
2. The skill states principles derived from the primary local case studies (and any operator-approved FOSS supplements), each principle traceable to observed practices and the *why* behind them.
3. The skill does not reduce to "copy stockroom's outline" or similar surface mimicry.
4. Operator-selected FOSS supplements (if any) are reflected; unselected survey candidates are not treated as goldens.
5. Memory-bank ephemeral files track research findings and principle derivation through plan → (creative if needed) → build → QA → reflect.
