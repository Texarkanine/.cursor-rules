# Decision: Pre-Mortem Level Coverage

## Context

**What:** Which complexity levels get the dedicated Pre-Mortem plan step (Q1 decision)?

**Why it matters:** Under-applying leaves the issue's value on the table for the most common plan levels; over-applying adds ceremony to L1 and to L4's already-thin milestone plan.

**Constraints:**
- Q1: Pre-mortem lives inside plan, after Implementation Plan
- L1 has no plan phase (straight to build) — cannot host a plan step
- L2 and L3 both produce an implementation plan + Challenges
- L4 plan produces milestones + cross-milestone invariants, not an implementation plan; detailed planning happens in L1–L3 sub-runs
- Proportional ceremony; L4 sub-runs inherit whatever their classified level gets

## Options Evaluated

- **A — L3 only**: Add pre-mortem only to `level3-plan.md`
- **B — L2 + L3**: Add to both plan docs that produce implementation plans
- **C — L2 + L3 + L4 top-level**: Also add a milestone-plan pre-mortem to `level4-plan.md`
- **D — All levels including L1**: Force some form of pre-mortem even without a plan phase

## Analysis

| Criterion | A L3 only | B L2+L3 | C +L4 top | D +L1 |
|-----------|-----------|---------|-----------|-------|
| Consistency | Weak — L2 has Challenges but no pre-mortem twin | Strong — both implementation-plan levels | Over-extends | Breaks L1 lean path |
| Simplicity | Smallest diff | Two parallel edits (same pattern) | Three surfaces, L4 shape differs | Forces new L1 ceremony |
| Fitness | Misses L2 (common enhancement plans) | Covers every plan that has an implementation plan to stress-test | L4 top-level has no implementation plan — wrong object | L1 has nothing to pre-mortem |
| Reversibility | Easy | Easy | Medium — L4 wording would be a different ritual | Hard — pollutes quick fixes |

Key insights:
- Pre-mortem needs an **implementation plan** as its object. L4's object is a milestone list; "if this milestone decomposition failed" is a different question and is already partially served by cross-milestone invariants + later sub-run plans.
- L2 is the sweet spot the issue almost certainly wants: enough structure to have a plan, not enough creative loop to catch design holes another way.
- L1 must stay untouched (no plan phase).

## Decision

**Selected**: Option B — L2 + L3

**Rationale:** Pre-mortem attaches to "we have an implementation plan." That is exactly L2 and L3. L4 top-level is the wrong object; L4 sub-runs inherit via their own L2/L3 plans. L1 stays lean.

**Tradeoff:** L4 milestone decomposition does not get an explicit pre-mortem. Accepted: sub-run plans cover failure imagination where implementation exists; inventing a second L4 ritual is YAGNI unless experience shows milestone lists fail for predictable reasons.

## Implementation Notes

- Edit `rulesets/niko/skills/niko/references/level2/level2-plan.md` and `level3/level3-plan.md` in parallel (same step pattern + `tasks.md` template section).
- Do not edit `level4-plan.md` for pre-mortem in this task.
- Do not touch L1 workflow/build docs.
- Optional one-line note in L4 plan is out of scope unless needed for clarity during build — prefer silence over cross-references.
