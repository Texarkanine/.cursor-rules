# Decision: How `/niko` Should Seed Persistent Memory-Bank Context

## Context

**What**: How should `/niko` Step 0 ensure the three persistent memory-bank files are in agent context before the state machine runs (issue [#97](https://github.com/Texarkanine/.cursor-rules/issues/97))?

**Why it matters**: Without product/system/tech context, intent clarification and complexity classification run blind. Downstream phases already read some of these files, but the entry path (`/niko` → clarify → classify) does not. A wrong fix (wrong paths, wrong layer) can silently fail or burn context without solving the bug.

**Constraints**:
- Persistent files live at `memory-bank/{productContext,systemPatterns,techContext}.md` — not under `memory-bank/active/` ([memory-bank-paths](memory-bank-paths.mdc)).
- Step 0 is the *existence guarantee point*. `/niko` may be invoked against a project with no memory bank, so the read cannot precede the init gate — there would be nothing to read. Once the init gate has run, all three persistent files exist unconditionally. The read therefore belongs in Step 0, between the init gate and the state machine, and nowhere else.
- `Load:` fences in Niko skills mean "load a ruleset instruction document" (paths under `.cursor/rules/` / `.cursor/skills/`). Project artifacts are "read" elsewhere.
- `nk-chat` already has a correct persistent-file load pattern; Niko should not invent a conflicting one.
- conserve-context: pay for reads that seed the task; do not inject persistent content into always-apply rules.
- Prompt-authoring: workflows state ordering explicitly; prefer closed-stack consistency over novel DRY abstractions unless the abstraction is an execution handoff.

**Branch under review**: `read-membank-first` (`4fcbaa1`) adds a `Load:` block after the init-only early exit, but points at `memory-bank/active/{productContext,systemPatterns,techContext}.md` — paths that do not exist for persistent files.

## Options Evaluated

- **A — Keep branch shape, fix paths only**: Same `Load:` fence in Step 0 after the init gate; correct paths to `memory-bank/*.md`.
- **B — Step 0 unconditional read**: Same placement as A, but phrased as a read of project artifacts rather than a `Load:` of instruction documents, and stated unconditionally — no "if present" hedge, because Step 0 has already guaranteed existence.
- **B′ — Step 0 read with `nk-chat` graceful degradation**: Same as B, but copying `nk-chat` Step 1.1 wholesale, including its "read if the memory bank exists" conditional and missing-file fallbacks.
- **C — Shared "seed persistent context" reference**: Extract a small reference both `/niko` and `nk-chat` load via execution handoff.
- **D — Rely on downstream phases**: Leave Step 0 as ensure-only; assume later skills will load what they need.
- **E — alwaysApply injection**: Surface persistent content via always-on rules so every session has it.

## Analysis

| Criterion | A Fix paths | B Unconditional read | B′ nk-chat degradation | C Shared ref | D Downstream | E alwaysApply |
|-----------|-------------|----------------------|------------------------|--------------|--------------|---------------|
| Correctness (paths / layer) | OK if paths fixed | Strong | Strong | Strong if authored carefully | Fails entry gap | Wrong layer |
| Consistency with Niko skills | Weak (`Load:` misuse) | Strong | Strong | Medium (new indirection) | N/A | Conflicts with memory-bank model |
| Honors the Step 0 guarantee | Yes | Yes | No — re-opens a settled question | Depends on caller | N/A | N/A |
| Simplicity | High | High | Medium | Medium | Highest (no change) | Low |
| Context cost | Appropriate | Appropriate | Appropriate | Appropriate | Misses early decisions | Tax every turn |
| Reversibility | Easy | Easy | Easy | Medium (call sites) | N/A | Hard (drift) |

Key insights:
- The branch's *placement* was correct and is the crux of the fix: Step 0 both creates the files when absent and sits ahead of the state machine, so it is the one point where "these files exist" and "nothing has been decided yet" are simultaneously true. Only the paths were wrong (`memory-bank/active/…` is the ephemeral tree; persistent files sit one level up), and the working tree has since corrected them.
- `/niko` and `nk-chat` differ in a way that forbids copying `nk-chat`'s posture. `nk-chat` is read-only and must degrade when the memory bank is absent; `/niko` initializes, so by the time control reaches the read, absence is impossible. Hedged phrasing ("if present", as the issue text puts it) would invite the agent to re-derive a conclusion Step 0 already guaranteed, and hedges are how a guaranteed step turns into a skipped one.
- In this ruleset, `Load:` is reserved for instruction documents under `.cursor/…` — "go follow what this says". Persistent files are project data, read for grounding, and the init doc already distinguishes the two ("Load: `…/systemPatterns.mdc` and create the file by following the instructions in the rule"). Pointing `Load:` at `memory-bank/*.md` blurs that line, and it is what made `active/` look plausible in the first place.
- One path re-reads: when init just ran *and* the user supplied task input, the agent authored the three files moments earlier and re-reads what it wrote. A conditional to avoid that would cost more agent attention than the duplicate read, so the unconditional phrasing wins anyway.
- Option D does not close [#97]: classify/intent run before those later loads.
- Option E fights conserve-context and the memory-bank design (files are project artifacts, not harness rules).
- Option C is premature for three path strings, and systemPatterns favors intentional duplication when it is load-bearing and grep-verifiable.

## Decision

**Selected**: Option B — Step 0 unconditional read, placed after the init gate

**Rationale**: Step 0 is the only position that satisfies both halves of the requirement — the files are guaranteed to exist there, and nothing downstream has run yet. Keeping the read unconditional preserves that guarantee instead of re-litigating it. Phrasing it as a read rather than a `Load:` keeps the ruleset's instruction-versus-data distinction intact and removes the ambiguity that produced the wrong paths.

**Tradeoff**: Diverges from `nk-chat`'s otherwise-parallel block, so the two seed lists are similar but not identical, and a redundant re-read in the init-plus-task path. Both accepted.

## Implementation Notes

- In `rulesets/niko/skills/niko/SKILL.md` Step 0, keep the block where it is — after the init gate and the init-only early exit, before "proceed to the state machine".
- Convert the `Load:` fence to a read of the three persistent files, stated unconditionally and without fallback prose, since Step 0 has guaranteed they exist.
- Do not load ephemeral files in Step 0; state detection still owns that.
- Paths were already corrected in the working tree; the remaining change is the `Load:`-to-read conversion and the unconditional phrasing.
- Out of scope for [#97]: changing when downstream phases re-read these files (conserve-context already covers "don't re-read if still visible"), and `memory-bank-init.md`'s coarse handling of *partially* present persistent files — its flowchart branches on all-or-nothing, so one missing file routes to full initialization. Worth a separate issue.
