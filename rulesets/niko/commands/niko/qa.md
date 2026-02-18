# QA Command - Post-Implementation Semantic Review

This command performs a structured semantic review of the code just implemented against the original plan. It catches over-engineering, incomplete implementations, pattern violations, and implementation debris that mechanical checks (lint/build/test) cannot detect.

**CRITICAL**: This command is **required for Level 2+ tasks** and runs **after `/build`** and **before `/reflect`**. It blocks `/reflect` until the review passes.

## Memory Bank Integration

Reads from:
- `memory-bank/tasks.md` - Original plan and implementation requirements
- `memory-bank/creative/creative-*.md` - Design decisions (Level 3-4)
- `memory-bank/activeContext.md` - Current project context
- `memory-bank/progress.md` - Build outcomes and observations
- `memory-bank/systemPatterns.md` - Established architectural patterns
- `memory-bank/style-guide.md` - Code style conventions

Creates:
- `memory-bank/.qa_validation_status` - Validation status file (PASS/FAIL)

Updates:
- `memory-bank/tasks.md` - Records QA findings
- `memory-bank/progress.md` - QA outcomes

## Progressive Rule Loading

### Step 1: Load Core Rules
```
Load: .cursor/rules/shared/niko/main.mdc
Load: .cursor/rules/shared/niko/Core/memory-bank-paths.mdc
```

### Step 2: Load Complexity-Specific Rules
Based on complexity level from `memory-bank/tasks.md`:

**Level 2:**
```
Load: .cursor/rules/shared/niko/Level2/workflow-level2.mdc
```

**Level 3-4:**
```
Load: .cursor/rules/shared/niko/Level3/workflow-level3.mdc
```

## Workflow

1. **Verify Prerequisites**
   - Check `memory-bank/tasks.md` for build phase completion
   - Read the original implementation plan to establish the review baseline
   - For Level 3-4: Read creative phase documents for design intent

2. **Review the code just implemented against the original plan and apply these constraints:**

   - **KISS**: Simplify over-engineered logic; flatten unnecessary abstractions or indirection layers introduced during the build. If a simpler construct achieves the same outcome, prefer it. Do not preserve complexity merely because it was part of the initial implementation approach.

   - **DRY**: Consolidate any duplicate code, boilerplate, or redundant patterns introduced during iterative development into clean, reusable constructs. Cross-reference new code against existing utilities and helpers to avoid reinventing what the codebase already provides.

   - **YAGNI**: Prune speculative code, "just-in-case" variables, unused parameters, and features not explicitly required by the plan. If it wasn't asked for, it doesn't ship.

   - **Completeness**: Verify every requirement from the original plan was **actually implemented** — not stubbed, TODO'd, commented-as-pseudocode, or hand-waved. Treat any `// TODO` or placeholder value introduced during this session as a blocking deficiency, not a future suggestion.

   - **Regression**: Confirm no existing architectural patterns were broken — naming conventions, casing, error handling strategies, import styles, file structure, and established abstractions must remain consistent **across all affected projects**. New code must be indistinguishable in style from surrounding code **and integrate as a natural extension of existing architecture, not an accretion layer.**

   - **Integrity**: Replace any hardcoded shortcuts, magic numbers, placeholder strings, or debug artifacts (`console.log`, `print("HERE")`) introduced as temporary scaffolding. If it was a means to an end during development, it does not survive into the final commit.

   - **Integration Insight** *(advisory — does not block)*: Now that the change is implemented, examine whether it reveals a broader architectural simplification that wasn't visible from the plan alone. Ask: if this requirement had been a foundational assumption from the start, would the surrounding system look different? If yes — flag it prominently. Describe what that redesigned system would look like and why it would be cleaner. **Do not action this; surface it for the operator** as a concrete recommendation for future work.

3. **Apply Fixes**
   - For each finding, implement the correction directly
   - Re-run mechanical verification (lint/build/test) after each fix to ensure no regressions
   - Document significant changes in `memory-bank/progress.md`

4. **Generate QA Report**
   - Summarize findings and corrections applied
   - Write validation status to `memory-bank/.qa_validation_status`
   - Update `memory-bank/tasks.md` with QA results

5. **Handle Results**
   - **On PASS (clean or all issues fixed)**: Allow transition to `/reflect`
   - **On FAIL (issues requiring build changes)**: Return to `/build` to address findings, then re-run `/qa`
   - **On FAIL (fundamental plan issue discovered)**: Route back to `/plan` for replanning

## Usage

Type `/qa` after implementation to review the build against the original plan.

**Typical Workflow:**
```
/build → /qa → /reflect
```

## Output to Operator

When QA review is complete, print:
1. **QA result** — PASS or FAIL (with reason category: iterate or replan)
2. **Findings** — bulleted list of each semantic finding and the fix applied (or why it blocks)
3. **Integration Insight** (if any) — advisory recommendations surfaced during review
4. **Next command** — `/reflect`, re-run `/qa`, or return to `/build` or `/plan`

## Next Steps

- **On PASS**: Proceed to `/reflect` command for task review
- **On FAIL (iterate)**: Return to `/build` to fix issues, then re-run `/qa`
- **On FAIL (replan)**: Return to `/plan` if fundamental issues discovered

Workflow routing is governed by the loaded level-specific workflow rules.
