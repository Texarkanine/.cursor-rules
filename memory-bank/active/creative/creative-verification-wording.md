# Creative: Verification Wording Candidates

**Task:** verification-subagents-preflight-qa
**Scope of this document:** prose candidates only. Q1–Q3 (placement factoring, contract structure, spawn mechanics) are **not decided here** — wording candidates pending Opus structure. Every block below is written to be portable: it works whether Opus chooses a shared reference, verbatim duplication per call site, or thin phase-mapping edits.

## Block A: Skill End Contract

Replaces `## Step 4: Phase Transition` in both `niko-preflight/SKILL.md` and `niko-qa/SKILL.md`. Must be correct in both contexts (forked verifier, operator-manual `/niko-preflight` / `/niko-qa`) without naming either. The dangerous case is PASS — the old text explicitly authorized continuing on PASS, so the replacement names PASS explicitly rather than relying on a generic "stop."

### A1 — recommended

Preflight version:

~~~markdown
## Step 4: End of Verification

Verification ends in this conversation, on PASS as much as on FAIL. The status file and printed report are this skill's entire output; acting on the result belongs to whoever requested verification, never to this conversation. Do not load a level workflow or begin another phase — a PASS is not permission to build.

Tell the operator: the result is recorded in `memory-bank/active/.preflight-status`; the workflow resumes from the conversation that requested this verification, or from a fresh one they start when ready.
~~~

QA version — identical except the status file is `memory-bank/active/.qa-validation-status` and the punch line is "a PASS is not permission to reflect."

### A2 — ultra-tight variant

~~~markdown
## Step 4: End of Verification

Stop here, PASS or FAIL. The status file and printed report are this skill's entire output; the next phase belongs to the caller, never to this conversation. Tell the operator the result is recorded in `memory-bank/active/.preflight-status` and that the workflow resumes from whichever conversation reads it — not this one.
~~~

### Word-choice rationale

- **"on PASS as much as on FAIL" / "a PASS is not permission to build":** the sole behavioral change from today is the PASS branch. Naming it costs ~10 words and closes the "operator input isn't required, so continuing is helpful" rationalization. This is why A1 is recommended over A2, which relies on the generic "PASS or FAIL."
- **"whoever requested verification" / "the caller":** true in both contexts (parent conversation or operator) without saying "you are a subagent." Skill identity stays neutral; the stop is universal.
- **"never":** used once, where literally true (per prompt-authoring's reserve-the-absolutes rule).
- **Heading "End of Verification"** replaces "Phase Transition" because the section no longer transitions; keeping the old heading would contradict the body for an agent that reads everything at once.
- The closing operator message keeps manual recovery honest: result recorded, resume is a *different* conversation. It deliberately does not name a resume command — the FAIL print blocks in Step 3 already carry per-result Next Steps, and PASS resume differs by level (parent-owned solid edge vs `/niko-build`). Naming one here would be wrong somewhere.

### Companion micro-edits

These are not Step 4 but contradict the new contract if left as-is (verbs that command the skill to transition). Flagging for the implementation plan; final placement is Opus's call.

| Site | Today | Candidate |
| --- | --- | --- |
| `niko-qa` Step 2.5 | "**On FAIL (issues requiring build changes)**: Return to the Build phase to fix the issues." | "**On FAIL (issues requiring build changes)**: record in the report that Build must rerun." |
| `niko-qa` Step 2.5 | "**On FAIL (fundamental plan issue discovered)**: Return to the Plan phase to revise the plan." | "**On FAIL (fundamental plan issue discovered)**: record in the report that Plan must rerun." |
| `niko-preflight` Step 2.9 | "…then re-run `/niko-plan` to restructure." | "…and route to Plan in the report." |
| `niko-preflight` Step 2.9 | "**On PASS with ADVISORY**: Allow transition to `/niko-build`, but document advisory findings…" | "**On PASS with ADVISORY**: record PASS; document advisory findings for the operator's consideration." |

## Block B: Parent Orchestration

Insertion point unknown (Q1). Written as a self-contained fragment plus a one-line phase-mapping hook, so it fits option (a) shared reference, (b) verbatim duplication with name substitution, or (c) inline in each level workflow. For duplication, substitute `niko-preflight`/`.preflight-status` or `niko-qa`/`.qa-validation-status` throughout; nothing else changes.

### B1 — recommended

Phase-mapping line (replaces "Invoke the `niko-preflight` skill"):

~~~markdown
- **Level N Preflight Phase**: Fork a verification agent per the Verification Fork steps — do not run the skill in this conversation.
~~~

The fragment:

~~~markdown
### Verification Fork

Verification runs in a separate agent so the work is not graded by the conversation that produced it.

1. Fork a subagent — [Block C model heuristic goes here] — with exactly this charge:
   > Invoke the `niko-preflight` skill and follow it to its end. Report the printed result in your final message, then stop: run no other skill, phase, or workflow step, and make no commits.
2. Wait for it to finish.
3. Read `memory-bank/active/.preflight-status` and the reported findings.
4. Continue this workflow's own PASS/FAIL edges from that result. The transition is yours; the verifier never makes it.

If this harness cannot fork an agent, stop and tell the operator to run `/niko-preflight` in a new conversation; resume from the status file once they report back.
~~~

### Word-choice rationale

- **The blockquoted charge is the spawn-stop.** It is the answer to "where does the parent put instructions so the child cannot proceed into build/reflect": inside the fork prompt, quoted verbatim so every parent issues the same one. "Follow it to its end" hands control to the skill (execution handoff, no content restated); "run no other skill, phase, or workflow step" is the stop; "make no commits" keeps commit consent with the parent (Phase Mapping step 2 already commits before each phase). None of this touches skill text, so operator-manual invocation is unaffected — child-stop lives entirely in the spawn, per the brief.
- **"so the work is not graded by the conversation that produced it":** one clause of *why*, because a parent that understands the purpose won't "helpfully" inline the skill when forking is awkward.
- **"The transition is yours; the verifier never makes it":** restates parent ownership at the exact step where the parent acts — deliberate repetition of the Block A contract at the other call site (workflow-prompts: repeat where the agent might act).
- **"do not run the skill in this conversation" on the mapping line:** the mapping line is what the agent may read in isolation mid-workflow; the prohibition must be present there, not only in the fragment.
- **Fallback = stop and hand to operator,** not "run it yourself." Running in-process reproduces exactly the self-grading this task exists to remove, and manual recovery is the brief's designed degradation path. Rejected variant: "if you cannot fork, invoke the skill here as a last resort" — preserves autonomy but silently voids the independence requirement; if Opus wants it, it needs an explicit operator notice, which costs more words than the stop.

### B2 — minimal variant for tight call sites

For secondary call sites (`level2-build.md` / `level3-build.md` missing-preflight recovery, `level4-plan.md` Step 7) where a four-step block is too heavy, if Opus chooses a shared fragment:

~~~markdown
🚨 If preflight has not passed: STOP — run verification per the Verification Fork steps, then re-check the status file before continuing.
~~~

This removes today's "invoke the `niko-preflight` skill and proceed as instructed there," which is the single-context wording that lets a verifier continue into build.

## Block C: Portable Model Heuristic

Drops into Block B step 1 (or wherever Opus places model guidance). No vendor SKUs; survives unknown harnesses and unknown model menus.

### C1 — recommended

~~~markdown
Pick the verifier's model by capability, not by name: at least as capable as the model running this conversation, more capable if available, and from a different model family when possible — a second perspective is part of the verification. If the harness offers no model choice, fork with its default: separate context still counts.
~~~

### C2 — telegram variant

~~~markdown
Verifier model: at least your own capability; smarter if available; different family if possible. Choose by capability, never by a hardcoded model name. No model choice in this harness → fork with the default.
~~~

### Word-choice rationale

- **"by capability, not by name":** the anti-SKU rule stated as a principle instead of a denylist, so it holds for model menus that don't exist yet.
- **"the model running this conversation":** anchors "≥ self" without the agent needing to know its own product name.
- **"a second perspective is part of the verification":** the why-clause that makes "different family" a goal rather than a checkbox, so an agent facing a one-family menu correctly treats it as unsatisfiable-but-optional rather than blocking.
- **"separate context still counts":** graceful degradation — the fork must still happen when model choice doesn't, otherwise a harness with no model menu silently regresses to in-process verification.
- C1 recommended over C2: the two why-clauses cost ~15 words and are what let the heuristic generalize; C2 is for Opus only if the surrounding structure already carries the rationale.

## Cross-Block Coherence Check

- Forked path: spawn charge stops the child (B) *and* Step 4 stops it (A) — belt and suspenders, no contradiction.
- Manual recovery: no spawn charge exists, Step 4 alone stops the skill and tells the operator how resume works. PASS never auto-continues.
- Parent solid edges (e.g. L2 preflight PASS → build): parent reads status file (B step 3–4) and continues — transitions stay parent-owned, mermaid untouched.
- No block says "you are a child/subagent"; no block names a vendor or model SKU.
