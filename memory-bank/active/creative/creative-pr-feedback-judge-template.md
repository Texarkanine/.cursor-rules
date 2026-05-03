# Decision: PR Feedback Judge — Intro & Verdict Template (v0 — SUPERSEDED)

> **⚠️ This v0 is superseded by `creative-pr-feedback-judge-template-grounded.md`.**
>
> The grounded version mines the actual user-prompt corpus from the local Cursor warehouse and revises the criteria vocabulary, structure, and ask-size assumptions in light of real evidence. The v0 below is preserved for design-history reasons (so the trade between this and the grounded version is auditable), but the grounded doc is the authoritative template.

---

# Decision: PR Feedback Judge — Intro & Verdict Template

## Context

**What needs to be decided.** The exact wording of the questioning intro the `pr-feedback-judge` command injects, and the structural shape of each per-item verdict.

**Why it matters.** Every invocation of the command emits output in this shape. Get it wrong in either direction:
- Too terse → verdicts can't drive rework decisions.
- Too verbose → a 30-comment PR review becomes a wall of text that's harder to triage than the original GitHub thread.

The decision also defines the "questioning idiom" that's currently only in the user's head — the warehouse extract (`memory-bank/cursor_pull_request_feedback_references.md`) shows the literal phrase "valid or invalid" appears in only 1 of ~40 PR-feedback sessions, meaning the user re-improvises the framing every time. Pinning it down is a real ergonomic win.

**Constraints.**
1. Must capture the "valid or invalid" framing the user already uses.
2. Must scale gracefully from 1-item runs to 30+-item runs (whole-PR invocations).
3. Must keep the command body short enough to live in a single rule file (`rules/pr-feedback-judge.md`).
4. Must make verdicts actionable for rework iteration — a "valid" verdict needs enough info to drive a fix; an "invalid" verdict needs enough to confidently dismiss.
5. Must not couple to Niko (works in either context, since the command is content-agnostic about its surrounding workflow).

## Options Evaluated

The decision has two semi-orthogonal axes (intro framing × per-item verdict shape). I'll evaluate the realistic combos rather than the full cross-product.

**Intro framing**

- **I-Terse**: "For each item below, decide: valid or invalid. Justify briefly."
- **I-Scaffolded**: Names the implicit evaluation criteria the user is actually applying when they say "valid or invalid" — technical accuracy, scope/applicability, severity — and instructs the agent to weigh each.

**Per-item verdict shape**

- **V-Prose**: One paragraph per item.
- **V-Structured**: A fixed-section block per item (Summary / Verdict / Reasoning / Suggested Action).
- **V-Hybrid**: A scannable summary table at the top (one row per item with URL, author, verdict, one-line reason) followed by detailed structured blocks for items the agent recommends acting on.

## Analysis

| Criterion | I-Terse + V-Prose | I-Scaffolded + V-Structured | I-Scaffolded + V-Hybrid |
|---|---|---|---|
| Capture of "valid or invalid" idiom | Verbatim, but only as a label | Idiom preserved in the verdict line; criteria explain the *judgment* | Same as middle column |
| Scannability for whole-PR runs (30+ items) | Poor — wall of paragraphs | OK — fixed sections aid scanning, but every item gets full treatment whether it deserves it or not | **Best** — table triages, detail focuses on actionables |
| Rework actionability | Variable; depends on what prose the agent writes | Strong — every item has an explicit "Suggested Action" line | Strong for actionable items; quiet for dismissed ones (which is correct) |
| Reproducibility across runs | Low — agent improvises each time | High — fixed structure | High |
| Boilerplate cost per invocation | Low | High (same block repeated N times) | Moderate (table is cheap; detail blocks only for valid items) |
| Fit in a single rule file | Trivial | Trivial | Trivial — the templates are short |
| 1-item runs (single comment) | Natural | Natural | Collapses cleanly: 1-row table + 1 detail block |

**Key insights:**
- The "valid or invalid" idiom is actually a compression of three implicit criteria. Naming them in the intro doesn't bloat — it makes the verdicts reproducible across invocations and across reviewers (which is most of the point of having a command in the first place).
- For a 30-comment PR, the user's downstream action is *triage first, then deep-dive* on the items worth acting on. A flat list of structured blocks forces deep-dive reading on items the agent has already dismissed. The hybrid avoids this without losing detail where it matters.
- Per `script-it-instead`, the fetch step is already bounded to one batch — so the "scaling" concern is purely about output rendering, not tool-call economics.

## Decision

**Selected**: **I-Scaffolded + V-Hybrid**.

**Rationale**: It satisfies all five constraints simultaneously. It captures the user's idiom verbatim (the verdict label remains "valid" / "invalid"), scales to large runs via the triage table, keeps actionability strong via the per-item Suggested Action, and stays reproducible across invocations because the criteria are stated rather than improvised.

**Tradeoff**: A small amount of boilerplate per invocation (the criteria intro + the table header) that's noise on a 1-item run. Acceptable: the noise is fixed-cost and the same every time, which the agent emits without thought.

## Templates

These are the literal blocks the command body will instruct the agent to emit. They go into `rules/pr-feedback-judge.md` verbatim.

### Intro (emitted once per invocation, before the table)

> Evaluating the PR feedback you provided. For each item I'll decide **valid** or **invalid** by weighing three criteria:
>
> - **Technical accuracy** — is the reviewer's claim factually right about the code?
> - **Scope alignment** — does the feedback apply to *this* PR's stated intent, or is it about adjacent/future work?
> - **Severity** — is the issue worth blocking, fixing in a follow-up, or dismissing?
>
> "Valid" means the feedback is accurate, in scope, and severe enough to act on. "Invalid" means it fails one or more of those tests; the reasoning will say which.

### Triage table (emitted once, listing every fetched item)

```markdown
| # | Item | Author | Verdict | One-line reason |
|---|---|---|---|---|
| 1 | [discussion_r12345](url) | @reviewer | ✅ valid | Caught a real off-by-one in the pagination loop |
| 2 | [issuecomment-67890](url) | @reviewer | ❌ invalid | Style preference, not in any project style rule |
| 3 | … | … | … | … |
```

### Detail block (emitted ONLY for items marked ✅ valid)

```markdown
### #N — [link to comment](url) by @author

**File / location**: `path/to/file.ts:L42` (or "(conversation comment)" for issue-level)

**Reviewer's point** *(quoted or paraphrased)*:
> …

**Evaluation**:
- Technical accuracy: …
- Scope alignment: …
- Severity: …

**Verdict**: ✅ valid

**Suggested action**: …
```

### Tail (emitted once, after all detail blocks)

> N items evaluated · M valid · K invalid · 0 inconclusive
>
> Items marked invalid are intentionally not detailed above — the one-line reason in the table is sufficient to dismiss them. If you want a deeper look at any invalid item, name it and I'll expand.

## Implementation Notes

- All four blocks above go into `rules/pr-feedback-judge.md` as fenced examples inside a "Output Format" section.
- The command body must explicitly tell the agent: emit blocks in order (intro → table → detail-blocks-for-valid-only → tail), and never emit a detail block for an invalid item unless the user asks.
- "Inconclusive" is a deliberate third bucket for items the agent genuinely can't judge without more context (e.g., comment references a file not in the PR diff). The tail counts it; no detail block is emitted but the table row uses `⚠️ inconclusive` and the one-line reason explains what's missing.
- The template uses emoji prefixes (✅/❌/⚠️) for verdict scannability in the table; this matches the user's other Niko output conventions and is cheap.
