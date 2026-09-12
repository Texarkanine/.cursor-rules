<!-- Title: conventional commit. Squash-merge uses the title as the commit message and,
     when the repo cuts releases from conventional commits (e.g. release-please), as the
     changelog entry — so write it for someone reading history or CHANGELOG.md. feat/fix
     typically cut a release in those setups; chore typically does not. -->

## Goal

<!-- What this needs to accomplish, in a line. If there's an issue, "closes #N" plus a clause
     is plenty — the issue is already the goal statement. -->

## What's here

<!-- Write this last, against the branch as it stands — not the plan you opened with.
     If it ended up somewhere other than the Goal (scope added or dropped, an approach
     abandoned, something deferred to a follow-up), that sentence is the most useful one in
     this PR. An undisclosed gap between these two is how surprises land in review. -->

## How I know it works

<!-- Proof that this change does the Goal. Then the suite, if any.

     1. Bug — catching test, red then green. Already-green didn't catch it.
     2. Behavior change — the product used, showing it (before → after is fine).
     3. Else — what convinced you, and why that is the proof.

     Form follows the change: a terminal trace, a screenshot, a document —
     as many blocks as it takes to make your case. A UI change is a picture,
     not a forced transcript.
     The final passing suite alone is not sufficient proof.
     -->

**Proof:**

**Suite:**

<details>
<summary>Transcript</summary>

```

```

</details>

## What changes for a user

<!-- Anything a user can notice or depend on: CLI flags and output shapes, API or config
     surface, docs, setup steps, env vars. "Nothing user-visible" is a common and useful
     answer. If something did change, say so where a user would look. -->
