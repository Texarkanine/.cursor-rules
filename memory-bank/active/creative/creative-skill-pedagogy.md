# Decision: skill-pedagogy

## Context

**What**: How to structure the `architecture-docs` skill so agents apply portable *principles* rather than copy surface recipes from stockroom/ai-rizz (or FOSS).

**Why it matters**: Wrong shape either (a) collapses into "open with a control-flow Mermaid like stockroom," or (b) is so abstract agents invent incoherent docs, or (c) duplicates/absorbs Niko `systemPatterns.mdc` / `techContext.mdc` instead of staying a distinct genre for project architecture docs.

**Constraints**:
- Principle-first; recipes only as illustrations of a stated principle
- Evidence hierarchy visible: primary locals ≥ adjacent Niko templates > secondary a16n > tertiary FOSS
- Prompt-authoring kinds lens; prefer composable reference over baked-in workflow
- Compose with authoring neighbors without brittle sibling content refs
- Situate memory-bank adjacency without rewriting or absorbing those templates
- Portable across projects that are not stockroom-shaped

## Options Evaluated

- **A — Pure principle reference**: Flat list of principles only; no anti-examples, no evidence tags, no genre frame beyond a one-liner.
- **B — Principle + anti-pattern reference**: Each principle paired with a concrete "does not look like" / common failure mode; still reference-shaped.
- **C — Principle + narrative case studies**: Each principle followed by multi-paragraph stockroom/ai-rizz/FOSS stories in `references/`.
- **D — Workflow-led composite**: Ordered "research → outline → diagram → write" procedure with principles as an appendix.

## Analysis

| Criterion | A Pure | B Principle+anti | C Case narratives | D Workflow-led |
|-----------|--------|------------------|-------------------|----------------|
| Anti-recipe (apply why, not what) | Weak — agents invent surfaces | Strong | Weak — invites mimicry | Medium — process can become the recipe |
| Portability | Strong | Strong | Weak if stories dominate | Medium |
| Prompt-authoring fit | Best (pure reference) | Strong (reference + facts about failures) | Weak (long narrative) | Wrong kind unless thin |
| Evidence hierarchy visibility | Weak | Medium (tags fit) | Strong but heavy | Medium |
| Genre boundary vs Niko mdc | Needs a frame either way | Frame + anti-pattern "don't dump this into systemPatterns" | Easy to blur genres | Easy to blur |
| Maintainability / length | Best | Good | Worst | Medium |

Key insights:
- Prompt-authoring's reference guidance ("state facts, not procedure"; "stay flat") eliminates D as the primary shape and warns against C's narrative bulk in the skill body.
- The operator's anti-recipe requirement needs *negative* examples at principle altitude ("not: mandate a control-flow opener") — that is B, not A.
- Case-study *depth* belongs in build-phase research / memory-bank; the shipped skill should carry at most a one-line evidence tag per principle (`local` / `niko-adj` / `foss`), not stories that re-teach stockroom's outline.
- A short **genre frame** (what this skill is for vs memory-bank persistent files vs contributor how-to) is required framing, not a workflow — compatible with a reference-primary skill.

## Decision

**Selected**: **B — Framed principle + anti-pattern reference** (with optional one-line evidence tags; no narrative case-study body; no workflow-led spine)

**Rationale**: Maximizes anti-recipe and portability while staying a composable reference per prompt-authoring. The opening genre/evidence-hierarchy frame handles Niko adjacency and FOSS weighting without absorbing those templates. Research during build still uses full case studies to *derive* principles; derivation artifacts stay in the memory bank, not in the skill.

**Tradeoff**: Agents lose rich in-skill stories that might aid intuition; we accept that in favor of transfer and anti-mimicry. If a principle is hard to apply without one concrete manifestation, allow a single *principle-level* "for example, …" line — never a project outline to copy.

## Implementation Notes

- `rules/architecture-docs/SKILL.md` structure:
  1. Frontmatter `name` / `description` (when to load)
  2. Short genre frame: project architecture docs vs `systemPatterns` / `techContext` vs user/contributor guides
  3. Evidence-weight note (primary local docs ≥ Niko-adjacent templates > FOSS)
  4. Principles as flat scannable sections: **Principle** → why it matters → **Not this** (anti-pattern) → optional one-line evidence tag
  5. No `references/` case-study novels unless build discovers a principle that truly needs a separate lookup sheet; default is single-file skill
- Build synthesizes principles from research; do not paste stockroom/ai-rizz section outlines into the skill
- QA: grep/read for surface mandates without enclosing principles; check genre frame present; check FOSS not overriding local
