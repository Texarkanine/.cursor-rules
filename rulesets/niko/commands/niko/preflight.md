# PREFLIGHT Command - Pre-Build Plan Validation

This command validates the implementation plan against codebase reality before any code is written. It catches design oversights, convention conflicts, and integration issues that would otherwise surface during or after the build.

**CRITICAL**: This command is **required for Level 3+ tasks** and **hard-blocks `/build`** until validation passes. It runs after `/plan` (and `/creative` if applicable) and before `/build`.

## Memory Bank Integration

Reads from:
- `memory-bank/tasks.md` - Implementation plan and requirements
- `memory-bank/creative/creative-*.md` - Design decisions (if creative phase ran)
- `memory-bank/activeContext.md` - Current project context
- `memory-bank/systemPatterns.md` - Established architectural patterns
- `memory-bank/techContext.md` - Technical stack and conventions
- `memory-bank/style-guide.md` - Code style conventions

Creates:
- `memory-bank/.preflight_status` - Validation status file (PASS/FAIL/ADVISORY)

Updates:
- `memory-bank/tasks.md` - Records preflight findings and any plan amendments

## Progressive Rule Loading

### Step 1: Load Core Rules
```
Load: rulesets/niko/niko/main.mdc
Load: rulesets/niko/niko/Core/memory-bank-paths.mdc
Load: rulesets/niko/niko/Core/command-execution.mdc
```

### Step 2: Load Complexity-Specific Rules
Based on complexity level from `memory-bank/tasks.md`:

**Level 3:**
```
Load: rulesets/niko/niko/Level3/planning-comprehensive.mdc
```

**Level 4:**
```
Load: rulesets/niko/niko/Level4/architectural-planning.mdc
```

## Workflow

1. **Verify Prerequisites**
   - Check `memory-bank/tasks.md` for planning completion
   - For Level 3-4: Verify creative phase documents exist (if creative phases were flagged)
   - Read implementation plan and design decisions

2. **Convention Compliance**
   - Verify the plan's proposed file locations, naming conventions, and patterns align with established codebase conventions documented in `memory-bank/systemPatterns.md` and `memory-bank/style-guide.md`
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
   - Write validation status to `memory-bank/.preflight_status`
   - Update `memory-bank/tasks.md` with any plan amendments or findings

8. **Handle Results**
   - **On PASS**: Allow transition to `/build`
   - **On PASS with ADVISORY**: Allow transition to `/build`, but document advisory findings for the operator's consideration
   - **On FAIL (rearchitect needed)**: Route back to `/plan` with specific findings that require plan revision
   - **On FAIL (conflict/convention)**: Provide specific fix instructions, block `/build`

## Usage

Type `/preflight` to validate the implementation plan before building. Required for Level 3+ tasks.

**Typical Workflow:**
```
/plan → /creative → /preflight → /build
```

## Next Steps

- **On PASS**: Proceed to `/build` command for implementation
- **On ADVISORY**: Review advisory findings, then proceed to `/build`
- **On FAIL (rearchitect)**: Return to `/plan` to revise the approach
- **On FAIL (fixable)**: Address findings and re-run `/preflight`

**Note**: BUILD mode is blocked for Level 3+ tasks until preflight validation passes. The system checks `memory-bank/.preflight_status` before allowing BUILD mode access for these tasks.
