# Progress

Add a pre-mortem lens to Niko's planning path so plans are stress-tested for likely failure modes before build. Investigate whether the issue's "what must never" / hard-no idea is redundant with existing constraints/invariants and either fold, reframe, or drop it. Design placement and wording deliberately — not a bare paste of the issue prompts.

**Complexity:** Level 3

## 2026-07-09 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Validated intent with operator (pre-mortem primary; hard-no secondary/suspect)
    - Classified as Level 3: multi-component planning-path change with open design questions
* Decisions made
    - Level 3 over Level 2 because placement/wording/relationship-to-invariants need creative design, not a single-file enhancement
    - Level 3 over Level 4 because this is one planning-path feature, not a multi-subsystem redesign
* Insights
    - Existing L3/L4 invariants and L2 Challenges & Mitigations are the closest cousins; preflight is codebase critique, not prospective failure brainstorming

## 2026-07-09 - CREATIVE (premortem-placement) - COMPLETE

* Work completed
    - Architecture creative for Q1: placement of pre-mortem vs Challenges / preflight / creative
* Decisions made
    - Dedicated Pre-Mortem step in plan phase after Implementation Plan, before Challenges & Mitigations
    - Challenges stay step-scoped; pre-mortem is plan-level; not creative or preflight
* Insights
    - The incantation matters: renaming Challenges would likely keep producing step laundry lists

## 2026-07-09 - CREATIVE (premortem-levels) - COMPLETE

* Work completed
    - Generic creative for Q2: which levels receive pre-mortem
* Decisions made
    - L2 + L3 only; L1 untouched; L4 top-level skipped (sub-runs inherit via their level)
* Insights
    - Pre-mortem's object is an implementation plan; L4 milestone lists are a different object

## 2026-07-09 - CREATIVE (hard-no-disposition) - COMPLETE

* Work completed
    - Generic creative for Q3: hard-no / what-must-never disposition
* Decisions made
    - Decline separate hard-no ritual; clarify L3 Invariants (positive framing) for any useful residue
    - Do not expand L2 with a new invariants section for this issue
* Insights
    - "Never allow ¬X" and "must preserve X" are the same constraint set; keep the positive form
