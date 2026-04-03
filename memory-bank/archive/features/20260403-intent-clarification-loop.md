---
task_id: intent-clarification-loop
complexity_level: 3
date: 2026-04-03
status: completed
---

# TASK ARCHIVE: Intent Clarification Loop

## SUMMARY

Added an intent-clarification step to Niko’s `/niko` entrypoint: after fresh user input (Step 4 “has input”) and before complexity analysis, the agent restates intent, refines with the user until approval, then proceeds. Resume, L4, and rework paths skip this step. Complexity analysis was updated to treat input as already validated (clarification clause removed). Canonical changes live under `rulesets/niko/`; `.cursor/` and `.claude/` copies follow the repo’s sync tooling.

## REQUIREMENTS

From the project brief:

- Lightweight when input is already well specified; never lossy-compress complete external specs—reference them by link when appropriate.
- Must run before complexity analysis; approved understanding feeds downstream phases.
- Works for bare prompts, links, and combinations; no new top-level command.
- Restatement loop must converge on user approval only.
- Proportional restatement (compress verbose input, expand terse as needed).
- External references that are complete specs pass through by reference, not summary.

Reference: [GitHub Issue #60](https://github.com/Texarkanine/.cursor-rules/issues/60).

## IMPLEMENTATION

**Approach:** Insert Step 5 “Clarify Intent” on the Step 4 “has input” edge only; renumber Resume 5→6 and Classify 6→7. Delegate behavior to a dedicated rule loaded from the `/niko` skill, mirroring the complexity-analysis pattern (routing in `SKILL.md`, procedure in `.mdc`).

**Canonical files touched (representative):**

- `rulesets/niko/niko/core/intent-clarification.mdc` — new: ingest, restate, approve/refine loop, convergence on approval.
- `rulesets/niko/skills/niko/SKILL.md` — flowchart and step definitions updated; Step 5 loads intent clarification; Steps 6–7 resume/classify.
- `rulesets/niko/niko/core/complexity-analysis.mdc` — Step 4 wording: input validated by intent clarification; removed redundant “prompt for clarification” clause.
- `rulesets/niko/niko/memory-bank/active/milestones.mdc` — step reference updated for renumbered Classify step.
- `memory-bank/systemPatterns.md` — Niko patterns updated for the new step.

**Note on `memory-bank/active/creative/creative-backcompat-guidance-placement.md`:** That document described a separate backwards-compatibility placement decision and was not part of this feature’s implementation; it was stray residue from an earlier task and was deleted with the rest of `memory-bank/active/creative/` during this archive.

### Creative phase decisions (inlined)

**Q1 — Which paths need intent clarification?**  
**Decision:** Fresh input only (Step 4 “has input”). L4 milestone paths, rework (after Step 3a/3b), and resume already carry validated intent. **Rationale:** Intent clarification bridges unvalidated input; other paths already passed validation. **Tradeoff:** Weak L4 milestone wording is not re-checked here (accepted: L4 planning validates milestones).

**Q2 — Artifact vs `projectbrief.md`?**  
**Decision:** No file from the loop—dialogue only. Complexity analysis still writes `projectbrief.md` from validated input. **Rationale:** Minimal change, no lossy file compression of external specs; planning still expands the brief. **Tradeoff:** Session loss mid-loop loses dialogue; acceptable because no ephemeral task files exist yet—`/niko` re-enters as Fresh.

**Q3 — Complexity analysis interaction?**  
**Decision:** Remove the “prompting for clarification” clause from complexity analysis; single owner for “do we understand intent?” upstream. **Rationale:** Avoid duplicate loops and undermining user approval.

**Q4 — Structural form?**  
**Decision:** New numbered step plus separate delegated file (rule `.mdc` with `Load:` from `/niko` skill), same pattern as complexity analysis—not inline wall of text in the state machine. **Implementation refinement:** Creative said “skill file”; plan correctly used `.mdc` to match existing `Load:` targets. **Tradeoff:** One-time renumbering of steps 5→6 and 6→7.

## TESTING

Specification-only deliverables (Markdown). Verification:

- Behavioral specs B1–B9 (fresh path fires clarification; L4/rework/resume bypass; proportional restatement; external refs preserved; convergence; no intent-loop file artifact; CA no longer prompts for clarification).
- Integration walks IT1–IT2 (fresh path through Step 5; L4 path skips Step 5).
- `/niko-qa`: PASS — plan steps, brief requirements, B1–B9, IT1–IT2, and cross-file step numbering checked.

## LESSONS LEARNED

- The `Load:` pattern in `/niko` (routing in `SKILL.md`, logic in `.mdc`) scales: one new node, one edge, one `Load:` for substantial new behavior.
- For spec-only work, upfront behavioral tests (B1–B9 style) give build and QA concrete pass/fail criteria instead of subjective review.
- Creative questions framed as named, narrow decisions map cleanly to implementation steps with little interpretation gap.
- Preflight justified itself by catching a missed `milestones.mdc` step reference; folded in as plan Step 4 before build.

## PROCESS IMPROVEMENTS

- Keep using behavioral test lists for Markdown-only L3 tasks.
- Keep creative questions specific enough that answers read as implementation instructions.

## TECHNICAL IMPROVEMENTS

- Optional future: sharpen L3-plan “Boundary Changes” language for public vs internal surfaces (not part of this task).
- Ensure stray `creative-*.md` files from other tasks do not linger in `memory-bank/active/creative/` after handoffs; archive or delete when closing a task.

## NEXT STEPS

None for this task. Memory bank active area was cleared for the next run; use `/niko` to start new work.
