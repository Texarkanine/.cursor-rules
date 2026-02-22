---
name: niko-qa
description: Niko Memory Bank System - QA Phase - Post-Implementation Semantic Review
---

# QA Phase - Post-Implementation Semantic Review

This command performs a structured semantic review of the code just implemented against the original plan. It catches over-engineering, incomplete implementations, pattern violations, and implementation debris that mechanical checks (lint/build/test) cannot detect.

## Step 1: Load Memory Bank Files

Read:
- `memory-bank/tasks.md`
- `memory-bank/projectbrief.md`
- `memory-bank/systemPatterns.md`
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`
- `memory-bank/creative/`

## Step 2: QA Workflow

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

3. **Apply Fixes or Fail**
     - **Trivial fixes** (debug artifacts, naming inconsistencies, dead code, magic numbers): fix directly, re-run lint/build/test after each.
     - **Substantive issues** (missing requirements, wrong approach, broken contracts, incomplete implementations): do NOT fix. Record as a FAIL finding with enough detail for the next Build or Plan cycle to act on it.
     - The line: if the fix requires understanding design intent or making a decision between approaches, it's not QA's job. Fail and route back.

4. **Generate QA Report**
    - Summarize findings and corrections applied
    - Write validation status to `memory-bank/.qa-validation-status`
    - Update `memory-bank/tasks.md` with QA results

5. **Handle Results**
    - **On PASS (clean or all issues fixed)**: Good job!
    - **On FAIL (issues requiring build changes)**: Return to the Build phase to fix the issues.
    - **On FAIL (fundamental plan issue discovered)**: Return to the Plan phase to revise the plan.

## Step 3: Log Progress

> 🚨 **Printing this notice is NOT the end of this phase.** After printing, continue immediately to the next step - do not stop.

Update `memory-bank/progress.md` to record completion of the QA phase.

When QA review is complete, print:

### PASS

~~~markdown
# QA Result

✅ PASS

1. **Findings** — bulleted list of each semantic finding and the fix applied (or why it blocks)
2. **Integration Insight** (if any) — advisory recommendations surfaced during review

~~~

### FAIL

~~~markdown
# QA Result

❌ FAIL

1. **Findings** — bulleted list of each semantic finding and the fix applied (or why it blocks)
2. **Integration Insight** (if any) — advisory recommendations surfaced during review

## Next Steps

(the next command, if any, based on the current complexity-level's workflow & QA result)
~~~

## Step 4: Phase Transition

- If operator input is required: stop and wait for them.
- If operator input is not required: load the appropriate complexity level-specific Niko workflow file, then use its Phase Mappings to execute the next phase.