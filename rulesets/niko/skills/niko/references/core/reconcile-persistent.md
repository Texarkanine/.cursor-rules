# Reconcile Persistent Files

> **TL;DR:** Quick scan of persistent memory bank files against the work just completed. Update what this task invalidated, or what the standing-contract probe marks as materially incomplete. If you update nothing, print a one-line skip receipt per file — do not skip silently.

## Persistent Files to Check

| File | Guidance Rule |
|------|---------------|
| `memory-bank/productContext.md` | `.cursor/rules/shared/niko/memory-bank/productContext.mdc` |
| `memory-bank/systemPatterns.md` | `.cursor/rules/shared/niko/memory-bank/systemPatterns.mdc` |
| `memory-bank/techContext.md` | `.cursor/rules/shared/niko/memory-bank/techContext.mdc` |

## Procedure

For each persistent file listed above:

1. **Load** its guidance rule - this defines what belongs in the file and how to write it.
2. **Read** the file's current contents.
3. **Compare** against the work just completed: with the guidance rule's definition in mind, does the file contain anything that is now **factually wrong** or **materially incomplete** because of the changes made in this task?
4. **Standing-contract probe** (answer yes/no for the task just completed, scoped to *this* file):
    - Did we introduce or change a shared contract used across multiple scripts or tests (typed errors, placeholders, path layers, fixture isolation rules, oracle rules)?
    - Would a future contributor adding a similar test or validation, with only the current persistent files + code, invent a conflicting approach (e.g. message-regex oracles, plain `Error`, colliding `err.code` values)?
    If yes to either **and** this file's guidance rule is where that contract belongs: this file is materially incomplete — update it surgically. A contract that belongs in `systemPatterns` or `techContext` must not force an update to the other files. Listing every new helper module is still out of scope; documenting the *contract* is in scope. Guidance-rule Avoid lists govern the altitude and shape of what you write; they must not short-circuit a yes on this probe.
5. **If no** (compare is clean and probe does not require an update to this file): do not touch the file. Print one line: `[productContext|systemPatterns|techContext]: skip — <reason>` where the reason cites the standing-contract probe outcome, not only "not invalidated."
6. **If yes** (compare found invalidation, or the probe requires an update to this file): make a **surgical update** following the guidance rule's conventions - fix only the specific content invalidated by this task, or add the brief standing-contract briefing the probe required.

If any file was updated, briefly note what changed and why in your output to the operator.

## Guardrails

- **Deliberately incomplete.** These files are a high-level overview of a subset of important facts. They will always omit some truths. That is by design. They must never contain content that does not belong.
- **Selective, not routine.** Most tasks won't change persistent files. This step should be a quick mental scan, not a ritual rewrite.
- **Surgical, not comprehensive.** Update what this task invalidated or what the probe required. Do not audit for unrelated staleness. Do not rewrite sections that aren't directly affected. Do not chase completeness.
- **System-level scope.** These files describe the system's shape, not individual tasks.
- **Skip only when absence is harmless.** Under-updating is preferable to noise for narrative and history. It is *not* harmless for a new standing contract that future authors must follow (error identity, test oracles, path layers, build invariants). When unsure which case you are in, print the skip receipt with your reason — do not skip silently. Prefer leaving a file alone over inventing content that may not belong.
