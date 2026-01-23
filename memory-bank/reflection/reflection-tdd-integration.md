# Reflection: TDD Integration into Niko

## Task Summary
Integrated Test-Driven Development (TDD) enforcement throughout the Niko memory bank system, ensuring flowcharts and workflows guide agents to write tests before implementation.

**Complexity:** Level 2 (Enhancement)
**Commits:** `5fe9de8`, `040a703`, `545074c`, `3e72244`

## What Went Well

1. **Clear separation of concerns emerged**
   - Main TDD rule (`always-tdd.mdc`): Defines HOW to do TDD (4-step methodology)
   - Memory bank rules/commands: Define WHEN to apply TDD (per subtask, per phase)
   - This allows users to mix/match different TDD methodologies while Niko enforces timing

2. **Flowcharts updated consistently**
   - All level workflows now show: Analyze → Test → Implement → Verify
   - Visual order reinforces the TDD principle without re-explaining methodology
   - Red styling (`#ff5555`) used for TDD gates matches existing visual language for mandatory checkpoints

3. **Minimal change for maximum impact**
   - Avoided over-engineering (no TDD checks in reflect/qa modes)
   - Focused changes on plan and build phases where TDD matters most
   - Verification checklists ask "Tests written BEFORE implementation?" without prescribing HOW

## Challenges Encountered

1. **Initial over-trimming of `build.md`**
   - First attempt removed too much, losing valuable level-specific workflow context
   - Had to revert and apply surgical trim instead
   - Lesson: Level-specific workflows are about WHEN/WHAT, not HOW - they belong even when delegating methodology

2. **Structural ambiguity in Level 3-4 workflow**
   - Integration testing placement after the phase gate was ambiguous
   - Fixed by restoring indentation to show gate is per-phase, integration is after all phases

3. **Balancing explicitness vs. duplication**
   - Too explicit = duplicates main TDD rule, risks staleness
   - Too minimal = agents may not know WHEN to apply TDD
   - Solution: Say "Follow the TDD process" at decision points, let main rule define process

## Lessons Learned

1. **Separation of HOW vs WHEN is key for cross-cutting concerns**
   - Methodology rules define HOW (reusable across projects)
   - Workflow rules define WHEN (project-specific integration points)
   - This pattern applies beyond TDD to any methodology integration

2. **Structure matters for clarity**
   - Indentation and list nesting communicate iteration vs. sequence
   - Explicit parentheticals like "(after all phases complete)" remove ambiguity

3. **User feedback loop is valuable**
   - User's reversion of `(TDD)` annotations taught restraint
   - "Minimum change for maximum nudge" is a good principle

## Files Modified

| File | Change |
|------|--------|
| `rules/niko-core.mdc` | TDD language in Research & Planning, Execution sections |
| `commands/niko/plan.md` | Added Test Planning step |
| `commands/niko/build.md` | Surgical trim of TDD methodology duplication |
| `niko/main.mdc` | Testing Requirements table row marked "(TDD)" |
| `visual-maps/plan-mode-map.mdc` | Added TEST PLANNING gates (red styling) |
| `visual-maps/build-mode-map.mdc` | Updated flowcharts to show TDD order |
| `Level1/workflow-level1.mdc` | TDD order in flowchart and checkpoints |
| `Level1/optimized-workflow-level1.mdc` | Added TEST step to process flow |
| `Level2/workflow-level2.mdc` | TDD order in implementation phase |
| `Level3/workflow-level3.mdc` | TDD for each module in implementation |
| `Level3/implementation-intermediate.mdc` | TDD emphasis in workflow |
| `Level4/workflow-level4.mdc` | TDD for each phase in implementation |

## Recommendations for Future

1. **Monitor agent behavior** - Verify agents actually follow TDD when using Niko
2. **Keep main TDD rule authoritative** - If methodology needs to change, change `always-tdd.mdc`, not scattered references
3. **Consider version compatibility** - Users may have different `always-tdd.mdc` versions; memory bank references should remain generic ("the TDD process")
