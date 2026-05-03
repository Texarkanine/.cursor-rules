# Pull request feedback references
_Exported on 5/3/2026 at 12:06:25 CDT from Cursor (3.2.10)_

---

**User**

/cw-query find all conversations with "valid or invalid" or github links with `/pull/` in them - I'm looking for where I provide pull request feedback and ask for assessment. Sometimes the feedback is inline, but I'm interested in the ones with links, which'll either be

1. links to the pr
2. links to a pr review
3. links to a specific pr review comment

I want to extract the references to these, for later use in reviewing the way I ask for feedback - so you just need to do the FINDING, and make a table that someone else can use later to do analysis and synthesis. Thank you!

---

**Cursor**

Locating the warehouse query script and running SQL to find sessions containing "valid or invalid" or GitHub `/pull/` URLs, then building an extractable reference table.



Gathering total counts and building a normalized extract: one row per GitHub `/pull/` URL plus phrase-only hits, with URL classification.



Fixing DuckDB `regexp_extract_all` options syntax and re-running.



Refining URL classification (`#pullrequestreview`, `#issuecomment`), fetching phrase-only rows, and computing row counts.



Exporting full-resolution CSV files (CLI truncates columns at 60 chars) for downstream analysis.



Fixing the session rollup (query bug) and verifying CSV row counts — multiline fields may skew line counts.



Here is a concise **inventory** you (or someone else) can use for later analysis. No synthesis—just what was found and how.

### Scope and method

- **Data source:** local Cursor warehouse (`messages`, `sessions`), same DB as `/cw-query`.
- **Filters:** `is_subagent = false` (parent chats only).
- **Match rules (message `text_content`):**
  - **Phrase:** case-insensitive regex `\bvalid\s+or\s+invalid\b` (word boundaries via `\s+` between words).
  - **GitHub PR links:** `http(s)://github.com/.../pull/<digits>...` with URLs extracted using `regexp_extract_all` (multiple URLs per message kept as separate rows).
- **Note:** Only **github.com** links are captured (not `gist.github.com`, not non-GitHub hosts). Trailing markdown junk can appear on rare rows (e.g. `**`); cleaning is left for the analysis pass.

### Counts

| Metric | Value |
|--------|------:|
| Distinct sessions with **phrase OR** PR URL | **41** |
| Distinct sessions with at least one PR URL in some message | **40** |
| Distinct sessions with the **phrase** anywhere | **1** |
| Messages matching phrase **without** a PR URL in the **same** message | **1** |
| Total **extracted PR URL rows** (after unnesting duplicates per message) | **76** |
| Messages matching either rule (earlier probe) | **67** |

So in this warehouse snapshot, **“valid or invalid” basically does not appear**; almost all signal is **GitHub `/pull/` links**.

### URL shape (`url_kind`)

Classification is by URL string only (heuristic):

| `url_kind` | Count |
|------------|------:|
| `pr_root_or_other_fragment` | 51 |
| `review_comment_anchor` (`#discussion_r…`) | 15 |
| `pull_request_review_anchor` (`#pullrequestreview…`) | 8 |
| `issue_comment_anchor` (`#issuecomment…`) | 2 |

### Files for downstream work (full URLs, no 60-char CLI truncation)

Written on this machine:

1. **`/tmp/cursor-warehouse-pr-feedback-github-pull-urls.csv`** — one row per extracted URL with `session_id`, `session_created_at`, `project_name`, `project_path`, `session_store_path`, `message_uuid`, `role`, `msg_ts`, `hit_valid_or_invalid`, `github_pull_url`, `url_kind`.

2. **`/tmp/cursor-warehouse-pr-feedback-phrase-only-no-pull-url-in-message.csv`** — messages that contain the phrase but **no** PR URL in that same message (here: **1** row): `user_intent_text` is the stripped `<user_query>` body when present, else fallback.

### Re-run SQL (for tweaks)

Broadening “valid or invalid” (e.g. separated by punctuation) or including `github.io` / other hosts would be a one-line regex change on top of the same pattern.

---

**Takeaway for your goal (“PR feedback + ask for assessment”):** the warehouse strongly supports a **link-based corpus** (40 sessions, 76 URL rows with mix of PR root, review, and inline comment anchors). The exact phrase **“valid or invalid”** shows up in **one** session only here; if you expected more, next step is a wider phrase search (separate analysis pass), not more digging in this narrow literal phrase.

---

**User**

You may want to use the vetor embeddings to find things incase my exact phrases don't show up; I assume dyou would. Can you also use the vector embeddings to search for things *close to* my key phrases and see if that adds any legitimate convos?

---

**Cursor**

Exploring how the warehouse exposes vector search so we can find sessions semantically similar to your PR-feedback phrases.



Checking embedding coverage, then running multi-query semantic search and comparing results to the URL-based session set.



Running a unified semantic scan: encoding multiple PR-feedback probe phrases, computing max cosine similarity per `message_user_query` and `session` embedding, then comparing to sessions already flagged by GitHub `/pull/` URLs.



Running a narrower probe set anchored to your phrasing (“valid/invalid”, “each piece of feedback”) to reduce collisions from generic “code review” probes.



Here is what using **vectors** added, with the same stack as `vsearch.py` (`all-MiniLM-L6-v2`, cosine similarity on **`message_user_query`** embeddings — **1,644** rows in your DB; **`session`** embeddings were included in an earlier pass for ranking, but the interesting extra hits are almost all from **user_query**).

### Does semantic search find convos the URL regex missed?

**Yes, but sparse and noisy.**

- **GitHub `/pull/` URL sessions** (non-subagent): **40** (same as before).
- **Broad probes** (10 paraphrases like “assess my PR review”, “was I wrong…”) pull in **~19** sessions at **≥ 0.35** similarity that are **not** in that URL set; many are **collisions** (e.g. `…/alf-test-design-reviewer` in a repo path matching “code review feedback”, W3C validator “validation”, generic “review this codebase”).
- **Narrow probes** (7 phrases centered on **valid/invalid** + **each piece of feedback**) are much closer to your actual wording and surface a smaller set of **non-URL** sessions worth eyeballing.

### High-signal sessions **without any** `github.com/.../pull/N` in the thread

These are the clearest **“URL regex alone would drop this”** examples:

| Session ID | Project | Why it counts |
|------------|---------|----------------|
| `f5b7521e-579f-4b19-bce0-f3efa702b099` | rules | Explicit **reviewer PR feedback** / **YAGNI** judgment (“are they overengineering…”). Confirmed: **37** messages, **`any_pull_url = 0`** for the whole session. |
| `43bee403-387c-401f-a3e1-a445ba0bc684` | cursor-warehouse | **Peer PR review** rework after reflect (`…during peer pr review`). **`any_pull_url = 0`**. |

Several other **non-URL** sessions land at **~0.34–0.39** narrow similarity and mention **feedback / assess / placement / pushback** (mostly **rules**, **a16n**, **slobac**, **devblog**). Some are **PR-adjacent workflow critique**, not GitHub PR threads; some are **paper/editorial review** (devblog) — still useful if your research question is “how I ask for judgment on feedback,” not strictly “GitHub PR links.”

### Artifacts for whoever does synthesis later

1. **`/tmp/cursor-warehouse-pr-feedback-semantic-vs-url.csv`** ( **82** sessions )  
   Union of: GitHub `/pull/` URL sessions **or** narrow cosine **≥ 0.28** **or** broad cosine **≥ 0.35**, with columns:
   - `in_github_pull_url_session_set`, `narrow_max_cosine`, `narrow_best_probe`, `broad_max_cosine`, `broad_best_probe`, `message_user_query_preview`, etc.

2. **`/tmp/cursor-warehouse-pr-feedback-semantic-sessions.csv`**  
   Full **per-session** ranking from the first wide probe run (every session gets a max similarity vs **session ∪ user_query** embeddings — useful if someone wants **global** ranking, not a trimmed union).

### Practical takeaway

- **Exact phrase** search under-counts; **vectors** recover at least **two** unmistakable PR-feedback-assessment threads **with zero PR URLs** in the transcript (`f5b7521e…`, `43bee403…`).
- **Generic “code review” probes** over-recall; **narrow valid/invalid-style probes** match your intent better but still pick up **`/check`**, **paper review**, and **“assess”** in non-PR contexts — the CSV + manual skim is still needed.

If you want a **stricter** automated slice later, a good next filter is: **narrow ≥ 0.34** AND **not** URL-set AND (**preview** matches `(?i)pull request|pr feedback|reviewer|coderabbit|peer pr|inline review`**) — that drops most collisions without hand-maintaining a phrase list.

