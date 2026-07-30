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

## 2026-07-30 - PLAN - COMPLETE

* Work completed
    - Resolved the open Tier B question with the operator and updated the creative doc's Tier B and Tier D accordingly.
    - Verified the replacement recipes in this repository against `pull/99/head`: `git show FETCH_HEAD:{path}`, `git ls-tree FETCH_HEAD`, and `git grep {pattern} FETCH_HEAD` all read the PR head with no checkout, and the working tree stayed clean.
    - Surveyed verification infrastructure: `make test` runs symlink and README-link gates, CI is `.github/workflows/rulesets-links.yml`, `scripts/verify-skillify.py` checks structure only. Confirmed green at baseline.
    - Wrote the full plan to `memory-bank/active/tasks.md`: 13 behaviors, 11 ordered implementation steps, 6 challenges, 5 pre-mortem findings.
* Decisions made
    - Tier B obtains code by reading against the fetched ref rather than by checking out. A worktree is materialized only to run something, and is then removed explicitly. Leaving a deleted `mktemp` worktree unremoved was rejected: it strands an entry under `.git/worktrees/` and leaves the repository dirty while the filesystem looks clean.
    - Code-access rungs are named by condition, not lettered, because the skill already uses `Tier`/`T1`/`T2` for fetch access and `Failure modes` references those by name.
    - No tests written, and none stubbed. The `always-tdd` carve-out governs: skill wording is out of scope, and a content assertion here would be a change-detector.
    - The live acceptance run against PR #91's outdated comment is the gating check, promoted from a nice-to-have by the pre-mortem.
* Insights
    - `git grep` works against a bare ref, which was not anticipated in the creative phase. Tree-wide search therefore stops being a reason to clone whenever the objects are already local, narrowing Tier D to the genuinely remote case.
    - The pre-mortem surfaced a failure mode the challenge register missed: the plan can succeed at retrieval and still be a null result if no verdict actually changes. Instrumentation is not the deliverable; different dispositions are.

## 2026-07-30 - PREFLIGHT - COMPLETE

* Work completed
    - Validated the plan against the canonical `rulesets/niko/skills/niko-preflight/SKILL.md` after discovering the generated copy was stale and lacked the prose carve-out.
    - Ran all six blocking checks plus the advisory innovation step. All six pass.
    - Mapped every requirement and acceptance criterion to a concrete step; no gaps.
    - Validated an anchor-computing `--jq` projection against PR #91 and adopted it into steps 1 and 3.
    - Read `rules/prompt-authoring/SKILL.md` to fix the authoring conventions build must satisfy; recorded four non-blocking advisories.
    - Wrote `memory-bank/active/.preflight-status`.
* Decisions made
    - TDD Plan Encoding passes on both limbs of the canonical check: skill wording owes no tests, and the plan schedules no change-detector.
    - Adopted the preflight innovation rather than merely flagging it, since it sits inside Level 2 and inside the project brief.
    - Left the pre-existing over-long heading alone; fixing it opportunistically is out of scope.
* Insights
    - The generated-tree lag changed agent behavior twice in one task, on `always-tdd` and then on `niko-preflight`. In both cases the stale copy would have produced the wrong call — the first would have demanded tests the carve-out excuses, the second would have failed to reject change-detectors. This is a sharper consequence than "the tree is merely behind" and is worth carrying to reflection.
    - Computing anchor state in the projection converts the plan's biggest risk from an adherence problem into a mechanical one. Prefer moving a policy into a transform over restating it as an instruction whenever the transform already exists.

## 2026-07-30 - BUILD - COMPLETE

* Work completed
    - Implemented steps 1–10 in `rules/pr-feedback-judge/SKILL.md`: Anchor State, code-access ladder, `--jq` projections with computed `anchor`, URL-table Fetches notes, item-filter wording, five dispositions, intro/triage/tail updates, gate-and-escalate orchestration step, failure modes, header prose.
    - Step 11 verification: `make test` green; live acceptance on `#discussion_r3653815924` confirmed outdated classification, no `original_line` indexing, hunk content locate, clean off-head fetch.
* Decisions made
    - Treated pre-existing `verify-skillify.py` failures (4 unrelated missing skills) as out of scope; asserted `pr-feedback-judge` command-skill structure directly instead of requiring a green whole-script exit that the baseline never had.
* Insights
    - Current L47 of the edited skill is Anchor State table prose — exactly the wrong text a naive `original_line` read would quote. The live acceptance made the defect concrete rather than hypothetical.
