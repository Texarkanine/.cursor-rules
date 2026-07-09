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

## 2026-07-09 - PLAN - COMPLETE

* Work completed
    - Finalized L3 implementation plan: L2+L3 Pre-Mortem steps, L3 invariants clarify, `rg` verification behaviors
    - Dogfooded Pre-Mortem on this plan itself
* Decisions made
    - No L4/L1/preflight/creative file changes
    - Verification pattern: structural `rg` + QA (no executable tests)
* Insights
    - Insertion order Implementation → Pre-Mortem → Challenges is load-bearing for the two lenses to stay distinct

## 2026-07-09 - PREFLIGHT - COMPLETE

* Work completed
    - Validated plan against conventions, dependencies, conflicts, completeness
    - Amended plan for prose TDD ordering and Status checklist coverage
* Decisions made
    - PASS WITH ADVISORY: declined extracting shared Pre-Mortem reference (match Challenges duplication / YAGNI)
* Insights
    - Prior Niko prose work already established `rg` + QA as the TDD substitute; encode red→green explicitly in the plan

## 2026-07-09 - PLAN REVISION (operator design) - COMPLETE

* Work completed
    - Operator pushback: Challenges are valuable; Klein pre-mortem is visualize-failure; order must be explicit (prompt-authoring); corpus study of ~70 Challenges + archives
    - Revised creative Q1 to Option B2: Pre-Mortem **after** Challenges; Challenges unchanged
    - Rewrote tasks.md plan, behaviors, dogfood Pre-Mortem
* Decisions made
    - B2 over B1 and over Challenges-as-key-only (A)
    - Preflight remains concrete validation (not pre-mortem host)
* Insights
    - Historical Challenges ≈ ShadowBox identify+mitigate; expensive failures were premise/layer mistakes Challenges did not frame

## 2026-07-09 - PREFLIGHT (revised plan) - COMPLETE

* Work completed
    - Re-validated revised plan: TDD red→green still encoded; Challenges preservation invariant; L2+L3 only; hard-no declined
* Decisions made
    - PASS — ready for `/niko-build`
* Insights
    - None beyond prior advisory (shared extract still declined)

## 2026-07-09 - CREATIVE (creative-premortem-complement) + PLAN AMEND - COMPLETE

* Work completed
    - Q4: investigated what belongs in creative to complement plan-end Pre-Mortem
    - Specified architecture-only choice pre-mortem after Decide + template note; ship in this task
    - Updated projectbrief, tasks.md (B9–B11, steps 4–5)
* Decisions made
    - Choice PM ≠ plan PM (different objects); Risk criterion kept; not all creative types mandatory
    - Reject expand-Risk-only (D) and plan-only-without-spec (A as final)
* Insights
    - SLOBAC-class failures need decision-time stress-test; plan-end is necessary but late for load-bearing creatives

## 2026-07-09 - PREFLIGHT (with creative complement) - COMPLETE

* Work completed
    - Validated expanded plan against brief/requirements; creative files now in scope
* Decisions made
    - PASS — `/niko-build` when ready
