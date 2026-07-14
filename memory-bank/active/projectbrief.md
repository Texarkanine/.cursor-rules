# Project Brief

## User Story

As an agent authoring (or reviewing) project architecture documentation, I want a Cursor skill that encodes principles for writing good architecture docs — derived from studied golden examples — so that new architecture docs explain the system the way those goldens do, for the same underlying reasons, rather than by copying surface recipes.

## Use-Case(s)

### Use-Case 1

An agent is asked to write or improve a project's architecture documentation. It loads this skill and applies the principles (audience, diagram choice, section structure, what to omit, how to relate code to concepts) instead of inventing ad-hoc structure or mimicking a single template.

### Use-Case 2

During planning/creative work on a new subsystem, an agent consults the skill to decide *what kind* of architecture explanation is warranted and how to open it — guided by principles backed by local golden case studies (stockroom, ai-rizz; a16n weaker) plus operator-selected FOSS supplements (rust-analyzer, Flutter engine).

## Requirements

1. Deliver a Cursor **skill** (canonical home in `.cursor-rules`) on writing good architecture documentation.
2. Content must be **principle-first**: for each observed good practice in the case studies, back out the principle that made it right — not surface prescriptions (e.g. not "open with a control-flow diagram," but "open with a diagram that \<principle\>," which in the studied goldens often manifested as control flow done a specific way).
3. **Evidence hierarchy (weighted):**
   - **Primary:** local goldens `stockroom/docs/architecture` and `ai-rizz/docs/developer-guide` — full weight because stockroom + git history let us recover *why* they evolved.
   - **Adjacent local authoring guidance:** Niko memory-bank templates `rulesets/niko/niko/memory-bank/systemPatterns.mdc` and `techContext.mdc` — not `docs/architecture` pages, but they already teach briefing-altitude architecture/tech orientation (what to include, what to omit, update discipline). Full research weight for principle derivation because their evolution is also recoverable via stockroom; skill must not rewrite those templates or collapse genres.
   - **Secondary local:** a16n `understanding-conversions` (weaker in-set).
   - **Tertiary FOSS supplements:** rust-analyzer contributing architecture doc; Flutter engine architecture doc — enlarge sample size only; weighted below the two primary locals because we cannot peer into author thought-process the way stockroom enables for local work.
4. Research primary locals and adjacent Niko templates via `sr-search` / `sr-query` and git history of the branches/commits that introduced or shaped them.
5. For FOSS supplements, inspect git history / PRs that introduced the docs (surface + history only — no stockroom depth).
6. Encode the derived principles in the skill (with case-study grounding as needed for agent followability). When local and FOSS evidence conflict, prefer local. Clarify (briefly) how project architecture docs relate to — without duplicating — memory-bank `systemPatterns` / `techContext` when both exist.

## Constraints

1. Do not rewrite stockroom / ai-rizz / a16n architecture docs, nor the Niko `systemPatterns.mdc` / `techContext.mdc` templates, as part of this task — the deliverable is the authoring skill only.
2. Prefer principles over checklists of surface moves; recipes are only acceptable when they clearly instantiate a stated principle.
3. FOSS is tertiary: never let rust-analyzer or Flutter redefine "good" relative to stockroom/ai-rizz; use them to corroborate or widen, not override.
4. Keep genres distinct: memory-bank persistent files vs project `docs/architecture` — draw principles from both; do not merge them into one template.
5. Subagents may help with survey/history collection, but do not fracture primary context — synthesize into one coherent principle set.
6. Follow repo conventions for skill placement (canonical sources under `rulesets/` / skills trees as applicable; do not edit installed `.cursor/` copies of shared assets).

## Acceptance Criteria

1. A skill exists in `.cursor-rules` that an agent can load when writing architecture documentation.
2. The skill states principles derived from the primary local case studies (and FOSS supplements where they corroborate), each principle traceable to observed practices and — for locals — recoverable *why*.
3. The skill does not reduce to "copy stockroom's outline" or similar surface mimicry.
4. FOSS supplements are rust-analyzer and Flutter engine only; other survey candidates are not treated as goldens. Evidence weighting (local > FOSS) is explicit in the skill or its research trail.
5. Memory-bank ephemeral files track research findings and principle derivation through plan → (creative if needed) → build → QA → reflect.
