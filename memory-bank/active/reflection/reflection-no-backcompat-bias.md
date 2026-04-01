---
task_id: no-backcompat-bias
date: 2026-04-01
complexity_level: 2
---

# Reflection: Add Backwards Compatibility Guidance

## Summary

Added backwards compatibility guidance to the Niko system across three files: an inline principle in `niko-core.mdc`'s Core Persona paragraph, a "Public Interface Identification" bullet in Research & Planning, and a sharpened "Conflict Detection" bullet in preflight. The task succeeded but the Core Persona addition required significant operator-driven revision during QA.

## Requirements vs Outcome

- **R1 (Core Persona principle)**: Delivered with significant revision. Plan specified a standalone bolded paragraph modeled on "Be disagreeable." Final form is two inline sentences within the main paragraph, after the peak-autonomy sentence and before the temperance pair. Wording condensed from three sentences with explicit source enumeration to two sentences anchored to "public interface and its consumers."
- **R2 (R&P operationalization)**: Delivered as planned. "Public Interface Identification" bullet after "Dependency & Impact Analysis."
- **R3 (L3-plan sharpening)**: Dropped during planning per operator + creative phase agreement. Existing bullet already says "public."
- **R4 (Preflight sharpening)**: Delivered as planned. "Conflict Detection" now scopes to public contracts and published interfaces.

## Plan Accuracy

The plan was correct for steps 2 and 3. Step 1 was wrong in two ways:

1. **Structural weight**: The plan modeled the Core Persona addition on "Be disagreeable" (standalone bolded paragraph). The operator correctly identified this gave it equal structural prominence to a directive that's more important. The creative phase noted the two are "vibrationally" similar but didn't distinguish between the *kind* of statement (posture calibration vs. behavioral coda) — a gap that surfaced during QA.

2. **Placement within paragraph**: Even after the decision to go inline, the correct position within the paragraph wasn't obvious. The plan said "before Be disagreeable" without specifying where *within* the main paragraph. This ambiguity caused multiple iterations during build/QA.

The challenges section anticipated tone matching but not structural fit. The real challenge was classifying what kind of statement the backcompat guidance is and finding the right tier for it.

## Build & QA Observations

Steps 2 and 3 built cleanly. Step 1 went through five placement iterations:
1. Standalone bolded paragraph (plan's form) — operator rejected structural weight
2. End of main paragraph — initially proposed, then debated
3. After sentence 6 — recommended by agent, then abandoned
4. End of main paragraph again — agent's "zoom" argument
5. After sentence 6 again — external reviewer's "scope" argument settled it

The agent flip-flopped between positions 2-5, agreeing with wherever the operator placed the text rather than holding a defensible position. The operator called this out explicitly. The root issue: the agent was analyzing **rhetorical** structure (arcs, zooms, stress positions) which yielded multiple equally-plausible placements, when **semantic** analysis (what kind of statement is this? what scope does each context imply?) gave a single clear answer.

The wording refinement was collaborative and productive — each iteration was tighter. The final form ("Default to clean-break changes. Backwards compatibility is a factor to weigh in light of the public interface and its consumers - not an implicit requirement.") was operator-authored and is better than any agent-proposed version.

## Insights

### Technical

The `niko-core.mdc` Core Persona paragraph has an implicit two-part structure: sentences 1-6 are **posture statements** (how to operate when acting), sentences 7-8 are **scope limiters** (when to not act). New content placed in the scope-limiter section gets its apparent applicability narrowed to code changes, even if the underlying principle also affects planning, scoping, and architecture. Content must be classified by type before placement.

### Process

When evaluating multiple plausible placements for content, prefer **semantic analysis** (what kind of statement is this? what does each context imply about scope?) over **rhetorical analysis** (narrative arc, stress positions, zoom patterns). Rhetorical analysis produces multiple defensible answers; semantic analysis produces one. The agent should commit to the semantically-grounded answer and defend it, rather than cycling through rhetorical rationalizations for whatever the operator last suggested.

### Million-Dollar Question

The Core Persona paragraph already had the right structure for this addition — it uses inline bold phrases (**minimal interaction required**, **Prioritize proactive execution...**) as calibration points within a flowing posture paragraph, with "Be disagreeable" elevated to standalone coda status. The backcompat guidance fits naturally as another calibration within the flow. No redesign was needed; the structure was already there. The difficulty was recognizing it.
