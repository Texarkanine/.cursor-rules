---
name: niko-preflight
description: Niko Memory Bank System - Preflight Phase - Pre-Build Plan Validation
---

# Preflight Phase - Pre-Build Plan Validation

This command validates the implementation plan against codebase reality before any code is written. It catches design oversights, convention conflicts, TDD violations, and integration issues that would otherwise surface during or after the build.

## Step 1: Load Memory Bank Files

Read:
- `memory-bank/active/tasks.md`
- `memory-bank/active/projectbrief.md`
- `memory-bank/systemPatterns.md`
- `memory-bank/techContext.md`
- `memory-bank/active/creative/**/*.md` (if any exist)

## Step 2: Preflight Workflow

1. **Verify Prerequisites**
   - Check `memory-bank/active/tasks.md` for planning completion
   - For Level 3-4: Verify creative phase documents exist (if creative phases were flagged)
   - Read implementation plan and design decisions

2. **TDD Plan Encoding** *(blocking)*
   - The test-first process lives in `.cursor/rules/shared/always-tdd.mdc`
   - This check governs units that change executable behavior. A unit delivering user-facing prose or policy (docs content, PR/issue templates, CONTRIBUTING, instructional comments, rule/skill wording, etc.) owes no tests for those artifacts; omitting tests for those artifacts passes this check
   - For each implementable unit of executable work (function, slice, milestone — whatever granularity the plan uses), confirm the ordered substeps place test-writing before production code, explicitly enough that a reasonable implementer cannot follow the plan by coding first
   - When a numbered step is a scheduled change-detector (a test that can only go red when someone deliberately edits the artifact it asserts on — heading, phrase, link, or checklist assertions on a document), delete that step. Keep the other steps. Record the finding and continue.
   - When a unit already has both test steps and production steps and they are in the wrong order, put the test steps first. Same steps. Record the finding and continue.
   - Do not invent tests. Do not emit always-tdd stages.
   - FAIL when the numbered steps for an executable unit have no test steps (implementation-only under a "we follow TDD" disclaimer, or TDD only in the preamble). This still applies after a change-detector strike.
   - On FAIL: cite the executable units lacking test steps. Write `FAIL (blocking)`.

3. **Convention Compliance**
   - Verify the plan's proposed file locations, naming conventions, and patterns align with established codebase conventions documented in `memory-bank/systemPatterns.md`
   - Cross-reference proposed module structure against existing project organization
   - Flag any deviation from established patterns with specific recommendations

4. **Dependency Impact**
   - Trace the plan's touchpoints through the dependency graph
   - Identify modules, consumers, or tests that will be affected but aren't accounted for in the plan
   - Verify that all downstream impacts are documented and addressed

5. **Conflict Detection**
   - Search for existing implementations, utilities, or patterns that overlap with or contradict the plan's approach
   - Identify duplication-in-waiting - cases where the plan proposes building something the codebase already provides
   - Flag any proposed changes that would break public contracts or published interfaces — internal restructuring that preserves the public API surface is not a conflict

6. **Completeness Precheck**
   - Verify the plan addresses all stated requirements with concrete implementation steps mapped to each one - not aspirationally, but with specific files, functions, and approaches identified
   - Flag any requirements that are acknowledged but lack a clear implementation path
   - Verify test coverage is planned for all new executable behavior — not for prose or policy artifacts; the TDD Plan Encoding check governs that boundary

7. **Radical Innovation** *(advisory - not blocking)*
    - What's the single smartest and most radically innovative and accretive and useful and compelling change you could make to the plan at this point?
    - Describe the change concretely - not as a vague suggestion, but as a specific structural sketch the operator can evaluate against the cost of redesign.
    - Record that idea as an advisory finding. Do not make the change to the plan, even if the idea fits the brief.

8. **Judge, Do Not Fix**
   - Surface and judge. Never modify the plan under review, except the TDD step swap and change-detector strike above.
   - Allowed writes only: `memory-bank/active/.preflight-status`, the `**Phase:**` field in `activeContext.md` (under **End of Verification**), `progress.md`, and those two in-phase plan edits on `tasks.md`.
   - Do not rewrite Implementation Plan units, behavior lists, or other scheduled work except that swap and that strike.
   - Record every issue as a finding. FAIL when the plan must change before build (`FAIL (fixable)` or `FAIL (blocking)`); PASS only when the plan is acceptable as-is (advisories allowed).

9. **Write Status**
   - Overwrite `memory-bank/active/.preflight-status`. First line is exactly one allowed value from `.cursor/rules/shared/niko/memory-bank/active/preflight-status.mdc`. After a blank line, write this run's findings.

## Step 3: Log Progress

> 🚨 **Printing this notice is NOT the end of this phase.** After printing, continue immediately to the next step - do not stop.

Update `memory-bank/active/progress.md` to record that Preflight completed and what the first line of `.preflight-status` was.

Print the appropriate block:

### PASS

~~~markdown
# Preflight Result

✅ PASS

## Findings

1. **Findings** - bulleted list of each finding with severity
2. **Advisory items** (if any) - concrete recommendations the operator can evaluate

~~~

### FAIL

~~~markdown
# Preflight Result

❌ FAIL

## Findings

1. **Findings** - bulleted list of each finding with severity
2. **Advisory items** (if any) - concrete recommendations the operator can evaluate

~~~

## Step 4: End of Verification

Update `memory-bank/active/activeContext.md` so `**Phase:**` records Preflight complete with the first line of `.preflight-status` (e.g. `**Phase:** PREFLIGHT - COMPLETE (PASS)`). Do not load a level workflow or begin another phase. Stop.
