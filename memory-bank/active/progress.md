# Progress: Add Backwards Compatibility Guidance (no-backcompat-bias)

Add guidance to the Niko system correcting the AI agent bias of treating backwards compatibility as an implicit requirement. Core principle in niko-core.mdc + sharpened language in L3-plan and preflight.

**Complexity:** Level 2

## History

- **Creative Phase**: Complete. Option A selected (inline in niko-core.mdc). Workflow phases (plan, preflight, QA) evaluated as primary homes and rejected — too narrow (L3-only), too late (post-plan/post-impl), or nonexistent (L1). Sharpening existing language in L3-plan and preflight identified as low-cost complementary enhancement to remove accidental reinforcement of conservatism. External review independently corroborated Option A and noted TDD analogy is weak (TDD is procedural, backcompat is judgment correction — closer to "Be disagreeable").
- **Plan Phase**: Complete. Plan revised per operator feedback: Core Persona paragraph placed before "Be disagreeable"; Research & Planning bullet simplified (no concrete examples); L3-plan sharpening dropped; preflight "Conflict Detection" sharpening retained. Awaiting build.

## 2026-04-01 - PREFLIGHT - COMPLETE

* Work completed
    - Verified `memory-bank/active/tasks.md` reflects completed planning and creative phases for task `no-backcompat-bias`.
    - Confirmed creative decision record in `memory-bank/active/creative/creative-backcompat-guidance-placement.md` and project brief requirements in `memory-bank/active/projectbrief.md`.
    - Cross-checked implementation plan in `memory-bank/active/tasks.md` against system patterns and tech context to ensure edits target canonical sources in `rulesets/` and avoid `.cursor/` copies.
* Decisions made
    - Accepted plan scope that omits L3-plan "Boundary Changes" sharpening from this task, treating it as a future complementary enhancement rather than a current requirement.
* Insights
    - Backwards compatibility guidance is best anchored in `niko-core.mdc` so it applies across all complexity levels and even outside explicit Niko workflows; workflow-phase sharpenings (e.g., L3-plan) are optional amplifiers, not primary enforcement points.

# Preflight Result

✅ PASS

## Findings

1. **Prerequisites - PASS (low)**: Planning and creative artifacts are present and consistent for Level 2 task `no-backcompat-bias`; implementation plan clearly identifies canonical edit targets in `rulesets/niko/niko-core.mdc` and `rulesets/niko/skills/niko-preflight/SKILL.md`.
2. **Convention Compliance - PASS (low)**: Planned changes respect repository patterns (`rulesets/` as source of truth, no edits to `.cursor/` copies) and align with existing rule file structure and naming conventions.
3. **Dependency Impact - PASS (low)**: Planned edits are limited to guidance text in rules; no additional dependent modules or tests beyond those already identified are implicated.
4. **Completeness - PASS_WITH_ADVISORY (medium)**: Requirement (3) from the original project brief (L3-plan "Boundary Changes" sharpening) has been explicitly dropped in the implementation plan and creative notes, narrowing the task scope to core guidance plus preflight sharpening.

## Advisory items

1. **Scope alignment (medium)**: Consider updating the project brief to explicitly record that L3-plan sharpening is out of scope for `no-backcompat-bias`, or scheduling a follow-on task if you want that complementary enhancement tracked separately.