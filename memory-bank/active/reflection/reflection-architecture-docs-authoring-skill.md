---
task_id: architecture-docs-authoring-skill
date: 2026-07-14
complexity_level: 3
---

# Reflection: architecture-docs-authoring-skill

## Summary

Delivered a principle-first `architecture-docs` skill in the authoring ruleset, derived from stockroom/ai-rizz Architecture goldens, Niko memory-bank templates, secondary a16n conversion mental-model docs, and tertiary rust-analyzer / Flutter engine FOSS pages — with research trail in the memory bank and packaging matching `prompt-authoring`.

## Requirements vs Outcome

All projectbrief requirements met: skill exists under `rules/`; principles are portable with evidence tags and Not-this anti-patterns; FOSS limited to rust-analyzer + Flutter engine and weighted tertiary; genres kept distinct from memory-bank templates; sibling architecture trees untouched. No requirements dropped. Additive clarification only: Domain-Mapping Sibling section for a16n’s taxonomy genre (explicitly not a substitute systems atlas).

## Plan Accuracy

Implementation plan sequence held: research → synthesize → checklist-as-test → SKILL.md → packaging. Preflight’s symlink (not hardlink) and TDD checklist amendments were correct and prevented packaging/process mistakes. Surprises were research-side, not plan-side: stockroom Architecture authoring *why* lived densest in the feature archive + warehouse sessions once embeddings were current; early semantic queries before re-embed were misleadingly thin/self-referential.

## Creative Phase Review

Framed principle + anti-pattern reference held cleanly through build and QA. No friction translating pedagogy to SKILL.md shape. The right mega-unknown (pedagogy) was flagged; FOSS selection was correctly operator-gated before creative closed. Domain-Mapping Sibling is a thin reference extension, not a relapse into case-study novels or a workflow spine.

## Build & QA Observations

Build depth was research-bound (stockroom semantic after embed fix, git/archives, FOSS raw docs). Authoring the skill itself was straightforward once the inventory existed. QA was clean except one trivial portability fix (stockroom “Heal” how-to phrasing). Packaging smoke checks passed first try after preflight corrected the symlink pattern.

## Cross-Phase Analysis

Preflight’s packaging correction avoided a hardlink/symlink mismatch that would have been embarrassing at QA. Creative’s anti-recipe mandate directly shaped the orientation-diagram principle and kept stockroom’s control-flow opener from becoming a surface mandate — the highest-risk failure mode from the pre-mortem. Interrupted build + stale embeddings would have produced thin principles without operator intervention; that external dependency is the main process risk this run surfaced.

## Insights

### Technical

- A successful orientation diagram is justified by the system’s load-bearing story (e.g. shared entrypoint contract → control-flow), not by a universal “architecture docs open with Mermaid flowchart” rule — the skill must encode the justification, not the manifestation.
- Domain-mapping docs (a16n) and systems atlases (stockroom) are sibling genres; treating the former as Architecture goldens of the latter kind would teach the wrong structure.

### Process

- For prose skills with no unit runner, checklist-as-test before authoring is an effective TDD stand-in — same pattern stockroom used for Architecture page claims.
- When research depends on stockroom semantic recall of *just-authored* docs, confirm embeddings are current before treating empty/weak hits as absence of intent.

## Post-Reflect Polish Addendum

After Reflect COMPLETE, operator feedback drove two shipped-skill edits (research artifacts unchanged in intent):

1. **Niko-agnostic surface** — Skill must work for consumers without Niko. Removed memory-bank / `systemPatterns` / `techContext` / `niko-adj` vocabulary; kept portable genre distinctions (how-tos, maintainer orientation notes, agent compact models).
2. **Decompression keys** ([daz.is/blog/decompression-keys](https://daz.is/blog/decompression-keys/)) — Diátaxis explanation + Chesterton's fence compress genre/outbound/fence prose. Rejected C4 (recipe risk), arc42 (template mimicry), and overloaded keys (YAGNI/SSOT/SoC). Novel principles (change surfaces, atlas grain, diagram-*kind*) stay explicit. Net ~130→82 lines.
