# Decision: PR Feedback Judge — Intro & Verdict Template (Grounded in Corpus)

This is the **final** Q1/Q3 resolution. It supersedes the v0 template in `creative-pr-feedback-judge-template.md`, which was grounded only in the warehouse summary doc. Operator flagged that as insufficient and required this exploration to mine the actual user-prompt corpus before writing the command body.

## Context

**What needs to be decided.** The exact wording of the questioning intro the `pr-feedback-judge` command injects, and the structural shape of each per-item verdict.

**Why it matters.** The command's whole reason for existing is to formalize a pattern the user re-improvises every time they ask the question. To formalize that pattern correctly, we need the actual data — what they actually ask for, in what shape — not a paraphrase.

**Constraints.** Same as the v0 doc, plus:
1. The template wording must match the user's actual vocabulary in their corpus, not synonyms an outside observer would pick.
2. The template granularity must match what the user actually asks for in their corpus, not what would be theoretically nice.

## Methodology

Three steps, all reproducible.

### Step A — Re-read the warehouse extract deliberately

Re-read `memory-bank/cursor_pull_request_feedback_references.md` end-to-end. Confirmed the analyst's framing: 40 sessions, 76 URL rows, dominant URL shape is `pr_root_or_other_fragment` (51) with `review_comment_anchor` second (15). Note: the literal phrase "valid or invalid" appears in only 1 session — that's the analyst's summary phrase, not the user's actual idiom. The CSVs from that session are still on disk at `/tmp/cursor-warehouse-pr-feedback-*.csv`.

### Step B — Extract the user-side prompt text

The CSV has rows for both user and assistant turns; we want only the user-side, URL-bearing rows. SQL run via `cw-query`:

```sql
COPY (
  SELECT s.session_id, s.project_name, s.created_at, m.uuid,
    LEFT(COALESCE(
      NULLIF(regexp_extract(m.text_content, '<user_query>\s*([\s\S]*?)\s*</user_query>', 1), ''),
      m.text_content
    ), 4000) AS user_text
  FROM messages m JOIN sessions s ON m.session_id = s.session_id
  WHERE (m.session_id, m.uuid) IN (<list extracted from CSV where role='user'>)
  ORDER BY s.created_at
) TO '/tmp/pr-feedback-user-prompts-extracted.csv' (HEADER, DELIMITER ',')
```

21 unique user messages extracted. Read all 21.

### Step C — Filter noise and synthesize patterns

Of the 21 messages:
- **9 are noise** for our purpose: 5 are `<external_links>` blobs where the URL is in pre-fetched search results (the user's actual question came in a different turn that wasn't URL-bearing); 2 are operational ("are we ready to merge?", "open a PR"); 2 are uploaded-document blobs.
- **12 are clean signal**: explicit "evaluate this PR feedback" prompts. Listed below with date and shape.

The clean 12 are the data the template should be grounded in.

## Findings

### F1 — The user's actual criteria, in the user's own words

Across the 12 clean prompts, three criteria recur, in this exact vocabulary:

1. **"valid"** — also rendered as "valid and true", "valid and real", "real correctness issue". Asks: is the reviewer technically right about the code? Appears in 9 of 12.
2. **"worth fixing"** — also "worth fixing here and now", "real correctness issue worth fixing". Asks: is the issue real and severe enough to act on at all? Appears in 7 of 12.
3. **"in scope for this PR"** — also "worth fixing IN THIS PR", "worth fixing within the scope of this pr", "in-scope to fix on this branch". Asks: should it be fixed on this branch, deferred to follow-up, or dismissed? Appears in 6 of 12.

**Delta vs v0:** the v0 template named these "technical accuracy / severity / scope alignment." The user's words are punchier and more decision-oriented. **Use the user's words.**

### F2 — The user wants the three questions answered separately, not collapsed

Of the 12 clean prompts, **8 explicitly enumerate the questions as a numbered list** the agent should answer separately:

> "1. valid? why or why not? 2. worth fixing? why or why not? 3. in scope to fix in this pr? why or why not?"
> *(rows 11, 17, 18, 19, 20, 21)*

> "real correctness issue worth fixing here and now on this pr, or not worth fixing now because not a real correctness issue, or due to some other mitigating/scope factor? or something else? why?"
> *(row 9 — same intent, prose form)*

**Delta vs v0:** v0 collapsed the three criteria into a single "verdict" with a "reasoning" paragraph that mentioned each criterion. The user wants three separate explicit answers, each with its own "why." **Restructure to one block per criterion.**

### F3 — The user wants a disposition, which is the composition of the three answers

Implicit in every clean prompt: the user is trying to decide what to *do* with each piece of feedback. The three answers compose into a small disposition space:

- valid + worth fixing + in scope → **fix in this PR**
- valid + worth fixing + not in scope → **defer to follow-up**
- valid + not worth fixing → **dismiss with acknowledgment**
- not valid → **dismiss**

**Delta vs v0:** v0 had no disposition line; the user inferred it from the verdict + reasoning. Add an explicit `Disposition:` line per item so the rework decision is one glance away.

### F4 — Real ask sizes are 1–3 items, not 30

Item counts in the 12 clean prompts:

| Items | Count of prompts |
|---|---|
| 1 | 4 |
| 2 | 4 |
| 3 | 2 |
| "all feedback on the PR" (whole-PR) | 1 |
| follow-up question on a single item | 1 |

**Delta vs v0:** v0's "triage table on top, detail blocks for valid-only" optimization was designed for the 30-item case. Real median is 2 items. Cut the triage-table-by-default. Keep it as an *optional* prefix when the agent ends up with > 5 items (e.g., the whole-PR case), but don't make it the standard shape.

### F5 — The opener is "PR feedback:" and the closer is "why?"

Opener tokens across the 12 prompts: `PR feedback:` / `Pr feedback:` (5×), `One piece of pr feedback:` / `PR reviewer had one piece of feedback:` (2×), `more pr feedback:` / `we've got some pr feedback:` (2×), `coderabbit had some feedback:` (1×), `some pr feedback, what do you think about each?` (1×). The opener is consistently terse.

Closer: every clean prompt asks "why?" or "why or why not?" at least once. The user always wants justification.

**Delta vs v0:** v0's intro was scaffolded but verbose. Mirror the user's terse opener; the criteria block does the scaffolding work.

### F6 — Failure modes the user has actually corrected for in the corpus

Row 5 ("Uhhh did you read the comment at the deep link?") is a follow-up where the user caught the agent answering before fetching the linked comment. The agent had improvised a response based on the URL alone.

**Delta vs v0:** v0 didn't address this. The intro should explicitly tell the agent to **fetch first, then evaluate** — never form an opinion before reading the actual comment text. This is a corpus-attested failure mode.

## Decision

**Final template.** Drops v0's collapsed verdict, adopts the user's vocabulary verbatim, makes the three questions explicit and separately answered, adds a disposition line, demotes the triage table to a >5-items option, and adds a fetch-first instruction.

### Intro (always emitted, before any items)

> Evaluating each piece of PR feedback. I'll fetch the actual comment text first — never judging from the URL alone — then for each item answer three questions and state the disposition.
>
> 1. **Valid?** Is the reviewer technically right about the code? Why or why not?
> 2. **Worth fixing?** Is the issue real and severe enough to act on at all? Why or why not?
> 3. **In scope for this PR?** Should it be fixed on this branch, deferred to a follow-up, or dismissed? Why or why not?
>
> The three answers compose into a disposition. Feedback can be valid but not worth fixing, or valid and worth fixing but out of scope for *this* PR — I'll spell each one out.

### Per-item block (emitted for every item, in order)

```markdown
### Item N — [link to comment](url) by @author

**Where**: `path/to/file.ts:L42` (or "(conversation comment)" for issue-level / "(review body)" for review-level)

**Reviewer's point** *(quoted or paraphrased)*:
> …

**1. Valid?** ✅ / ❌ — …

**2. Worth fixing?** ✅ / ❌ — …

**3. In scope for this PR?** ✅ / ❌ / 🕒 follow-up — …

**Disposition**: fix in this PR | defer to follow-up | dismiss with acknowledgment | dismiss
```

### Triage table (emitted ONLY when item count > 5, BEFORE the per-item blocks)

```markdown
| # | Item | Author | Disposition |
|---|---|---|---|
| 1 | [discussion_r123](url) | @reviewer | fix in this PR |
| 2 | [issuecomment-456](url) | @reviewer | dismiss |
```

### Tail (always emitted, after the per-item blocks)

> N items evaluated · X to fix in this PR · Y deferred · Z dismissed.

## Implementation Notes

- The intro's "fetch first, never judge from the URL alone" instruction is **load-bearing** — it's a corpus-attested failure mode (F6). Do not soften it.
- The disposition vocabulary is fixed (4 values). The agent must use one of those four; if a piece of feedback genuinely doesn't fit, it goes under "dismiss with acknowledgment" with the reason in the criteria answers.
- The 🕒 follow-up emoji on Q3 is reserved for when something is valid + worth fixing but doesn't belong on this branch — that maps to disposition "defer to follow-up." Keep the emoji set small (✅ ❌ 🕒) so the table stays scannable.
- The per-item block uses bold headers, not headings (`**1. Valid?**` not `#### 1. Valid?`), to keep the markdown nesting reasonable when many items are emitted.
- For the >5-item triage table, "disposition" is the only sensible column — putting "valid?" alone would mislead, since a valid+not-worth-fixing item still gets dismissed.
