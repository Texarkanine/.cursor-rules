---
task_id: pr-feedback-judge
date: 2026-05-03
complexity_level: 3
---

# Reflection: PR Feedback Judge Command

## Summary

Shipped a single top-level Cursor slash command (`rules/pr-feedback-judge.md`) that takes any mix of GitHub PR-feedback URLs and renders per-item verdicts against a corpus-grounded "valid? worth fixing? in scope for this PR?" rubric. Build was a near-pure transcription of a heavily-iterated plan; QA caught one trivial omission (missing body template); no rework cycles.

## Requirements vs Outcome

Every requirement from the plan was delivered:

- **Inputs**: all four URL shapes (whole PR, PR review, `#discussion_r`, `#issuecomment`) classified and dispatched. ✅
- **Behavior**: corpus-grounded intro + per-item block + conditional triage table + tail. ✅
- **Packaging**: single top-level `rules/pr-feedback-judge.md`, no ruleset wrapper, no `script-it-instead` always-on dependency. ✅
- **Out of scope** (Niko coupling, verdict persistence, anonymous fetch): respected; the command is Niko-agnostic and fetch-strategy is T1→T2→fail.

No requirements were dropped, descoped, or added during build.

## Plan Accuracy

The plan's 2-step build sequence was exactly right. The "write the file, then validate it" structure matched the actual work shape (the file *is* the deliverable; there's no dependency graph to traverse).

The plan correctly anticipated:
- File location and naming (`rules/pr-feedback-judge.md`, no frontmatter, matches wiggum precedent).
- Inspection-grade test plan (B1, B6–B10b) — every check was mechanically runnable as specified.
- Deferral split between local checks and post-push checks (B2) and live smokes (B11–B12).

The plan **mildly under-specified** A3: it said "a minimal suggested body template" but didn't give the template. Build interpreted this as "describe the body" rather than "provide the template." QA caught it in seconds. Cost: one StrReplace. Lesson: when an advisory says "with a template," include or link to the template body in the advisory itself, not a description of what the template should contain.

## Creative Phase Review

Three creative documents informed this build; one was superseded.

- **Q1 v0** (template, summary-doc-grounded) — superseded. Operator correctly flagged the grounding as insufficient before build started. Banner-marked in the v0 doc; build referenced only Q3.
- **Q2** (fetch tiers) — held up perfectly. The T1 / T2 / fail decision translated 1:1 into the tier-detection block. The A2 anti-pattern (don't filesystem-scan for MCPs) was the kind of subtle gotcha that wouldn't have made it into the command body without the advisory being explicit. Worth its weight.
- **Q3** (template, corpus-grounded) — held up. The intro and per-item block went in verbatim. F6 (the "fetch first" load-bearing instruction surfaced from a corpus-attested failure mode) earned the H2 it got — that line is the highest-leverage instruction in the file.

Friction during build from creative decisions: zero. Every section ordering, every wording choice, every emoji set was already settled.

## Build & QA Observations

Build was about as clean as Level 3 build gets — sequential transcription with no decisions to make at write-time. The only mid-build judgment call was the orchestration walkthrough's prose style (numbered list with a sub-bullet for the batch-fetch instruction), which is mechanical, not architectural.

QA found exactly one issue (A3 template), classified it as trivial, and fixed it in-phase. The QA constraint that caught it was Completeness (specifically: "every requirement from the original plan was actually implemented — not stubbed, TODO'd, commented-as-pseudocode, or hand-waved"). The natural-language description of the body was a hand-wave; the QA template fix replaced it with the actual artifact.

No rework. No FAIL→Build cycle. No FAIL→Plan cycle.

## Cross-Phase Analysis

The most important causal chain in this task ran across **three** plan iterations and was visible only in retrospect:

1. **Plan v3** added warehouse mining as a build sub-step under Q1.
2. **Plan v4** promoted warehouse mining to its own creative (Q3) at operator's insistence — "this is the real meat of the prompt design."
3. **Q3 corpus mining** discovered "real ask sizes are 1–3 items, median 2." That finding sat in the creative doc.
4. **Preflight v2** (operator-prompted) traced the F4 finding into its packaging implication: "if real ask sizes are 1–3 items, the `script-it-instead` threshold rarely trips, so why are we bundling it as an always-on rule?" — and resolved Q4 in favor of single-rule packaging.
5. **Build** was 2 steps instead of 5, because Q4 had collapsed half the deliverable.

That chain is a textbook case of **earlier phases earning their keep**. Q1→Q3 promotion looked like scope creep at the time; in retrospect it produced the data point that made Q4 obvious. Without Q3's F4, the ruleset would have shipped, and `script-it-instead` would have been an always-on dependency for a command that triggers it once in a blue moon.

The other notable causal chain: **A2 in preflight v1 → preserved through preflight v2 → folded into the build's tier-detection block** (the "don't filesystem-scan for MCPs" anti-pattern). Without A2, build's instinct would have been to write something like "look for `mcps/*/github*/` in the agent's filesystem context" — exactly the wrong signal. Preflight caught this before any code was written.

## Insights

### Technical

- **Corpus mining > intuition for prompt design.** The v0 template (intuition-grounded against a summary doc) used the words "technical accuracy / severity / scope alignment." The v1 template (mined against 21 actual user prompts) used "valid / worth fixing / in scope for this PR." The user's own vocabulary was punchier, more decision-oriented, and more memorable — and we'd never have arrived there without reading the actual corpus. For any future prompt-engineering task where a corpus exists, mine first.

- **Top-level `rules/*.md` is the right packaging tier for "one command, no composition."** ai-rizz auto-registers it as a slash command without any ruleset wrapper, and the wiggum precedent established the file shape (no frontmatter, `#` heading, prose + tables + bash). When a command has no support rules, no shared infrastructure, and no always-on dependencies, the ruleset is overhead. Default to top-level `rules/*.md` in that case.

### Process

- **Preflight is for catching design-implication misses, not just plan correctness.** Preflight v2 didn't find a *bug* in the plan — it found a *consequence* of the Q3 evidence that nobody had followed through. The Q3 corpus said "1–3 items per ask"; the v3 plan still had `script-it-instead` bundled as if every ask were a bulk op. Preflight's job included asking: "given what creative learned, does the plan still make sense?" That question saved a ruleset's worth of build work.

- **"Trivial" QA fixes are cheap insurance against drift.** The A3 template fix took 30 seconds. It would have been caught at the first live invocation, but live-invocation feedback loops are slow (push, install, invoke, evaluate). Catching it at QA against the inspection plan kept the iteration loop tight.

- **Plan iteration count (5 versions of Q2, 3 plan versions, 4 creative cycles) was the right cost for this task.** That looks like a lot, but most iterations were operator-introduced corrections that strictly reduced complexity (anonymous tier dropped, ruleset dropped, `script-it-instead` dropped, env-var harvesting dropped). The plan got *simpler* with each iteration, not larger. When iteration consistently deletes scope, more iteration is good.

## Addendum — Post-Reflect Rework Cycle (2026-05-03 14:44)

Operator surfaced four substantive findings *after* reflect, in the slot where their normal flow has "open PR → reviewer feedback comes in." Treated as a rework cycle: same shape as QA→Build feedback, just trigger-displaced.

### Findings and fixes

1. **"When to use" section was self-documenting invocation criteria.** Cursor commands are manual-invoke-only — by the time the command body is read into context, the human's already decided to invoke. Skills *may* document invocation conditions lightly (the agent has a choice to make); commands cannot, because there's no choice left to inform. Dropped the section entirely.
2. **Load-bearing instruction overreached.** "The reviewer's actual words are the *only* evidence you may judge from" was wrong — code itself, surrounding context, prior thread state are all valid evidence. The MUST is about *retrieval and consideration*, not about exclusivity. Softened to "MUST be retrieved and considered before you judge."
3. **Filesystem-scan-for-MCPs anti-pattern was YAGNI.** A2 from preflight v1/v2 codified a failure mode operator has never seen in the wild. Dropped. (If we see it, we add it back with a real example.)
4. **"Popular GitHub MCPs / no single-comment-by-ID getter" sentence was implementation scaffolding.** The agent reads MCP tool schemas at runtime; it doesn't need us to pre-summarize what's in or out of the surface area. Dropped.
5. **T2 access-pattern table — additional YAGNI catch.** When operator flagged the previous two as YAGNI and asked "might be yagni, too? think about it" about the table, the right call was the same: the URL-shape table at the top tells the agent what each URL contains; "if the MCP returns a list, filter it by id" is mechanical inference; runtime schema reading does the rest. Table dropped. File 198 → 181 lines.

### Cross-cycle insights (not in the original reflection)

- **Self-documenting-invocation-criteria is a category error for Cursor commands.** This generalizes beyond this task: any future command file in `rules/*.md` should not have a "When to use" / "When to invoke" section. The guidance in the body is for an agent that's already been told to run; documenting *whether* to run is for the human-facing surface (command name, description, README), not the body. Worth promoting to `systemPatterns.md` if the pattern recurs across more than this command.

- **Preflight A2 was "wisdom" without evidence.** It read like sound architectural guidance (don't filesystem-scan for things you can detect via runtime context) but it was solving a problem that doesn't happen. Two-cycle lesson: an advisory should cite the failure mode it's preventing. If the citation is "I imagine an agent might…", the advisory is YAGNI; if it's "I've seen agent X do Y", it's evidence-based.

- **The Q3 pattern ("mine the corpus, not the summary") repeats here at the meta level.** Build executed the plan faithfully; the plan was overspec'd in places where the operator had information I didn't (lived experience of which agent failure modes actually occur). The fix isn't "be smarter at QA" — it's "QA YAGNI passes are improved by operator presence at QA." When build outputs documentation, the operator is the only source of "would I read this if I were the agent?" ground truth.

- **My pattern of collapsing operator questions into action items cost a phase boundary.** Operator's question "should I have just `/niko`'d to resume?" was a question about workflow, not a fix request. I treated it as the latter. Then operator's "had you ANSWERED" feedback was itself implicitly a question (rollback? patch? commit-only?) — and I'd planned to absorb that one too until I forced an explicit `AskQuestion`. The corrective for me: when an operator message contains a `?`, "should I", "do you", or similar, surface the question explicitly before doing work. The single-line answer "this is a rework. ... well, you reflected, and feedback came in!" is the cleanest possible illustration that the operator wanted the workflow framing, not the workflow LARP.
