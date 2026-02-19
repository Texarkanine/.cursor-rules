---
name: niko-reflect
description: Niko Memory Bank System - Reflect Phase - Post-Implementation Reflection
---

# Reflect Phase - Post-Implementation Reflection

This command produces a structured reflection on the task just completed - what worked, what didn't, and what to do differently next time. It reviews the full lifecycle (plan → creative → build → QA) against outcomes, and extracts actionable insights that survive into the archive.

## Step 1: Load Memory Bank Files

Read:
- `memory-bank/tasks.md`
- `memory-bank/projectbrief.md`
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`
- `memory-bank/creative/` (if any exist)

## Step 2: Determine Complexity Level

Read the complexity level from `memory-bank/activeContext.md`.

If no complexity level is set, or `memory-bank/activeContext.md` does not exist: 🛑 STOP! It doesn't make sense to reflect before a task has been completed.

Ask the operator for clarification, and wait for their instructions. You're done for now.

## Workflow

1. **Verify Prerequisites**
    - Check `memory-bank/.qa-validation-status` exists and contains `PASS`
    - If QA has not passed: 🛑 STOP - it does not make sense to reflect on work whose correctness has not been verified. Ask the operator for clarification, and wait for their instructions. You're done for now.

2. **Review the Full Task Lifecycle**

    Walk through the task from start to finish, comparing what was planned against what actually happened:

    - **Requirements vs Outcome**: Did the final implementation satisfy every requirement in the original plan? Were any requirements dropped, descoped, or reinterpreted during build? Were any added that weren't in the plan?

    - **Plan Accuracy**: Was the implementation plan's sequence, file list, and scope correct? Did steps need reordering, splitting, or adding? Were the identified challenges the ones that actually materialized - or did surprises come from elsewhere?

    - **Creative Phase Effectiveness** *(Level 3-4 only)*: For each creative phase that was executed - did the chosen approach hold up during implementation? Were there friction points where the design decision didn't translate cleanly to code? Were the right things flagged as mega-unknowns, or were there unknowns that should have been flagged but weren't?

    - **Build & QA Observations**: What went smoothly during build? Where did you struggle or iterate? Did QA catch substantive issues, or was the build clean? If QA failed and required rework - what caused the gap between plan and implementation?

    - **Process Observations**: Did the workflow structure itself help or hinder? Were any phases unnecessary overhead for this task? Were any missing?

3. **Extract Actionable Insights**

    Search hard for genuine insights - but do not reach. A forced insight pollutes the archive; an honest "nothing notable" is better than a manufactured lesson. The bar is: would this observation change how you approach a future task? If yes, write it down. If you're stretching to find something, leave the section empty.

    When insights do surface, they can be raw observations ("the auth module's session middleware has implicit coupling to route guards - this bit us") or concrete recommendations ("next time, check session middleware first"). Both are valuable. Patterns may only become actionable after several reflections reveal the same friction point.

    Categorize insights as:
    - **Technical**: patterns discovered, gotchas in the codebase, library behaviors, architectural observations
    - **Process**: workflow adjustments, estimation accuracy, phase-skipping opportunities, tooling improvements

4. **Write Reflection Document**

    Create `memory-bank/reflection/reflection-<task-id>.md` using this structure:

    ~~~markdown
    # Reflection: [Task Name]

    **Task ID:** [task-id]
    **Date:** [date]
    **Complexity:** Level [N]

    ## Summary

    [1-2 sentence summary of what was built and whether it succeeded]

    ## Requirements vs Outcome

    [Did we deliver what was asked? Any gaps or additions?]

    ## Plan Accuracy

    [Was the plan right? What surprised us?]

    ## Creative Phase Review

    [L3-4 only: For each creative decision - did it hold up? Friction points?]
    [L2: Omit this section]

    ## Build & QA Observations

    [What went well, what was hard, what QA caught]

    ## Actionable Insights

    ### Technical
    - [Concrete technical insight]

    ### Process
    - [Concrete process insight]
    ~~~

    Scale the depth to complexity level:
    - **Level 2**: Keep it focused - a few sentences per section. One page max. The goal is to capture the key lesson, not write a retrospective.
    - **Level 3**: Full treatment of each section. Creative phase review is mandatory. Cross-phase analysis (did planning gaps cause build problems? did creative decisions create QA findings?).
    - **Level 4**: Everything in L3, plus: strategic technical insights (what does this task reveal about the system's architecture?), process improvement recommendations for the workflow itself, and estimation accuracy analysis.

5. **Update Memory Bank**
    - Update `memory-bank/tasks.md`: mark Reflect phase complete
    - Update `memory-bank/activeContext.md` with reflection outcome

## Output to Operator

When reflection is complete, print:

~~~markdown
# Reflect Result

## Summary

[1-2 sentence summary]

## Key Insights

- [Most important technical insight]
- [Most important process insight]

## Next Steps

Run `/archive` to create the archive document and finalize the current project.
~~~

Then, wait for operator input.
