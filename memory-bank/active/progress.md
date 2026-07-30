# Progress

Rework `rules/pr-feedback-judge/SKILL.md` so its verdicts rest on the current state of the code: classify each inline comment's anchor state before judging, obtain code through a need-gated four-tier access ladder, add an evidence-gated `already addressed` disposition, and project fetches to the fields the rubric actually uses.

**Complexity:** Level 2

## 2026-07-30 - CREATIVE - COMPLETE

* Work completed
    - Explored the operator's open questions about how the skill reaches the diff, standalone (no memory bank task in flight at the time).
    - Measured the corpus with `gh` across all 86 PRs on this repository: 293 inline comments, all `subject_type == "line"`.
    - Measured API transport costs: `pulls/{N}/files` versus raw diff at 1.07–1.25x, `pulls/{N}` bare at 24x, `.patch` versus `.diff` at 18,378 versus 891 bytes, review projection at 57%, inline projection at 28%, raw single-file fetch at 2,070 versus 3,782 bytes.
    - Verified the ladder's recipes: blobless `cli/cli` clone at 1.27s/12MB, `git fetch origin pull/N/head`, `git worktree add` at 1.5MB with no re-download, and `repos/{o}/{r}.size` separating a 769KB repository from a 62GB one.
    - Wrote `memory-bank/active/creative/creative-pr-feedback-judge-retrieval.md`.
* Decisions made
    - Anchor trust: adopt an explicit anchor-state model; never index current code by `original_line`.
    - Code access: adopt a need-gated four-tier ladder, with cloning last and size-gated.
    - Disposition vocabulary: add `already addressed` as an evidence-gated fifth value.
    - Rejected a standalone transport rule and a PR-review skill, both at operator direction.
* Insights
    - Only 49 of 293 anchors (17%) are safe to read at face value; the skill was judging the wrong text most of the time, silently.
    - The operator's premise that the API is JSON-bloated is only selectively true. It is false for diffs, where cloning to avoid JSON would be a net loss, and true for `pulls/{N}` and the comment endpoints' metadata.
    - The three requested fixes are one decision with three faces: staleness detection is what makes code access necessary, and projection is where a careless economy would delete the staleness signal. Shipping them separately would let them contradict each other.
    - A first draft of the measurements presented overlapping sets as additive and summed to 303 against a corpus of 293. Corrected to a real partition; the 41% headline and the conclusion were unaffected.

## 2026-07-30 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Confirmed the persistent memory-bank files exist; routed the state machine as Fresh with input.
    - Operator approved the intent restatement.
    - Created the ephemeral files and determined Level 2.
* Decisions made
    - Level 2: one self-contained component (`rules/pr-feedback-judge/SKILL.md`), design already resolved by the creative phase, contained risk, no architectural implications. Not Level 1, because it is a coordinated change across roughly seven sections that alters a user-visible contract. Not Level 3, because no second component and no architectural reach.
    - `always-tdd` does not govern this change: the carve-out names "rule and skill wording" as out of scope, and a test asserting on `SKILL.md` contents would be a change-detector. Verification is review plus the existing gates.
* Insights
    - `pr-feedback-judge` has no `rulesets/` symlink, so the change really is a single source file. `scripts/verify-skillify.py` constrains only its structure as a command-skill, not its content.
    - The `always-tdd` copy injected into context came from the lagging generated `.cursor/` tree and lacked the prose carve-out. Reading the canonical `rules/always-tdd.mdc` changed the TDD determination — a live instance of the "generated tree is expected to lag" pattern.
* Open questions
    - Tier B cleanup: the operator questioned orchestrating `git worktree remove` and suggested a `mktemp` worktree left to clean up naturally. To be resolved in the plan phase.
