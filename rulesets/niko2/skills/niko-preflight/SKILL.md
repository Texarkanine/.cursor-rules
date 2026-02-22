---
name: niko-preflight
description: Niko Memory Bank System - Preflight Phase - Pre-Build Plan Validation
---

# Preflight Phase - Pre-Build Plan Validation

This command validates the implementation plan against codebase reality before any code is written. It catches design oversights, convention conflicts, and integration issues that would otherwise surface during or after the build.

## Step 1: Load Memory Bank Files

Read:
- `memory-bank/tasks.md`
- `memory-bank/projectbrief.md`
- `memory-bank/systemPatterns.md`
- `memory-bank/techContext.md`
- `memory-bank/creative/**/*.md` (if any exist)

## Step 2: Preflight Workflow

1. **Verify Prerequisites**
   - Check `memory-bank/tasks.md` for planning completion
   - For Level 3-4: Verify creative phase documents exist (if creative phases were flagged)
   - Read implementation plan and design decisions

2. **Convention Compliance**
   - Verify the plan's proposed file locations, naming conventions, and patterns align with established codebase conventions documented in `memory-bank/systemPatterns.md`
   - Cross-reference proposed module structure against existing project organization
   - Flag any deviation from established patterns with specific recommendations

3. **Dependency Impact**
   - Trace the plan's touchpoints through the dependency graph
   - Identify modules, consumers, or tests that will be affected but aren't accounted for in the plan
   - Verify that all downstream impacts are documented and addressed

4. **Conflict Detection**
   - Search for existing implementations, utilities, or patterns that overlap with or contradict the plan's approach
   - Identify duplication-in-waiting — cases where the plan proposes building something the codebase already provides
   - Flag any proposed changes that would break existing contracts or interfaces

5. **Completeness Precheck**
   - Verify the plan addresses all stated requirements with concrete implementation steps mapped to each one — not aspirationally, but with specific files, functions, and approaches identified
   - Flag any requirements that are acknowledged but lack a clear implementation path
   - Verify test coverage is planned for all new behavior

6. **Integration Elegance** *(advisory — not blocking)*
   - For each proposed change in the plan, examine the existing system and ask: what would the most elegant solution look like if this requirement had been a foundational assumption from the start? If the plan describes something that bolts on rather than weaves in, flag the gap between the planned approach and that cleaner design.
   - Describe the alternative integration concretely — not as a vague suggestion, but as a specific structural sketch the operator can evaluate against the cost of redesign.
   - **This check is advisory, not blocking** — the operator decides whether the investment is warranted before build tokens are spent.

7. **Generate Preflight Report**
   - Create comprehensive findings report
   - Write validation status to `memory-bank/.preflight-status`
   - Update `memory-bank/tasks.md` with any plan amendments or findings

8. **Handle Results**
   - **On PASS**: Good job!
   - **On PASS with ADVISORY**: Allow transition to `/niko-build`, but document advisory findings for the operator's consideration
   - **On FAIL (rearchitect needed)**: Operator decision required.
   - **On FAIL (conflict/convention)**: Provide specific fix instructions, block `/niko-build`; Operator decision required.

## Step 3: Log Progress

> 🚨 **Printing this notice is NOT the end of this phase.** After printing, continue immediately to the next step - do not stop.

Update `memory-bank/progress.md` to record completion of the preflight phase.

Print the appropriate block:

### PASS

~~~markdown
# Preflight Result

✅ PASS

## Findings

1. **Findings** — bulleted list of each finding with severity
2. **Advisory items** (if any) — concrete recommendations the operator can evaluate

~~~

### FAIL

~~~markdown
# Preflight Result

❌ FAIL

## Findings

1. **Findings** — bulleted list of each finding with severity
2. **Advisory items** (if any) — concrete recommendations the operator can evaluate

## Next Steps

- **On FAIL (rearchitect)**: Run `/niko-plan` when ready to revise the approach.
- **On FAIL (fixable)**: Address the findings and re-run `/niko-preflight`.
~~~

## Step 4: Phase Transition

- If operator input is required: stop and wait for them.
- If operator input is not required: load the appropriate complexity level-specific Niko workflow file, then use its Phase Mappings to execute the next phase.
