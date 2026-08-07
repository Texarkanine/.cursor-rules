# Task: verification-subagents-preflight-qa (PR #108 rework)

* Task ID: verification-subagents-preflight-qa
* Complexity: Level 2
* Type: bug fix / remediation (PR review)

Apply nine agreed operator-review fixes on draft PR #108 without changing Spawn/Verdict grammar or the skill stop-at-Verdict contract.

## Test Plan (TDD)

Prose/policy under `rulesets/niko/` — always-tdd carve-out applies. No new executable unit tests; no change-detector tests on skill wording.

### Behaviors to Verify

- [Dry-read Item 1]: PASS with ADVISORY Handle Results no longer says “not a transition grant”; remains compatible with L2/L3 build accepting `PASS WITH ADVISORY`
- [Dry-read Item 2]: TDD FAIL writes `FAIL (TDD)`; Handle Results directs parent to re-enter Plan immediately; L2/L3 charts gain solid `FAIL (TDD)` → Plan; skill Step 4 still stops
- [Dry-read Items 3–6]: QA forbid/allowlist/Findings templates match rework brief
- [Dry-read Item 7]: All nine Spawn sites use shared parent stem + fenced `Run the `/niko-…` skill` charge; no “entire prompt exactly”
- [Dry-read Item 8]: No `PF`/`PFV`/`QAV`/`PFSA`/`QASA` node IDs remain under `rulesets/niko/`; full indicative names used
- [Dry-read Item 9]: L4 “Milestone bodies inherit…” sentence removed
- [make test]: symlinks + README internal links still pass
- [mmdc]: all Mermaid blocks in touched workflow/README files still compile
- [Dry-read F1]: `preflight-status.mdc` documents all four status values, including `FAIL (TDD)` and `PASS WITH ADVISORY`
- [Dry-read F2]: no L2/L3 STOP list or narrative sentence contradicts the new solid `FAIL (TDD)` → plan edge
- [Dry-read F3]: the Spawn stem sentence appears once per site at all nine sites and renders correctly inside its list context

### Test Infrastructure

- Framework: `make test` (`scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh`); Mermaid via `mmdc` on PATH
- New test files: none

## Implementation Plan

### Naming convention (Item 8)

Replace abbreviations everywhere under `rulesets/niko/`:

| Old | New |
| --- | --- |
| `PF` | `NikoPreflight` |
| `PFV` | `PreflightVerdict` |
| `QA` (phase node) | `NikoQA` |
| `QAV` | `QAVerdict` |
| `PFSA` | `PreflightSubagent` |
| `QASA` | `QASubagent` |

### Spawn charge template (Item 7) — nine sites

**Amended by preflight (see Finding F3/F6).** Shared **single-line** stem (tripwire — byte-identical at every site aside from the skill name):

~~~markdown
Spawn a subagent (prefer smarter / different family if available); the only instruction you add is `` Run the `/niko-preflight` skill ``. Do not run the skill in this conversation.
~~~

(Use `/niko-qa` where the site is QA.) Build-gate sites keep their `STOP —` / re-check text around the same stem sentence.

Constraints on the stem:

- One line, no fenced block. The nine sites sit in four different indentation contexts (flush-left prose, a `🚨` line, a `- 🚨` bullet, and a nested bullet under a numbered step); a fenced block cannot be byte-identical across them and a flush-left fence inside a list item breaks the list. A single line is indentation-immune for `rg` and matches how `systemPatterns.md` already describes the tripwire ("the nine-site Spawn phase-mapping **line**").
- The charge is delimited with a double-backtick span so the inner `/niko-…` backticks stay literal.
- Do **not** claim the entire prompt is exactly that one line — "the only instruction you add" scopes the constraint to what the parent authors, leaving harness/OptMem injection untouched.

### TDD self-heal (Item 2)

- `niko-preflight` writes `.preflight-status` = `FAIL (TDD)` for TDD plan-encoding failures (other fails stay `FAIL`)
- Handle Results: block build; cite units; **parent re-enters Plan immediately to restructure** (skill still stops at Step 4)
- L2/L3 (+ README mirrors): add solid `PreflightVerdict -->|"FAIL (TDD)"| NikoPlan` alongside existing dashed other-FAIL → ManualPlan
- L4 already solids all FAIL → NikoPlan; keep that; status value still `FAIL (TDD)` for clarity
- FAIL report Next Steps: mention TDD case → Plan auto (parent)

**Amended by preflight (Findings F1/F2).** The new edge and the new status value invalidate content at sites the plan did not list. All of these must change in the same pass, or the STOP lists will contradict the charts and the self-heal will never fire:

- `rulesets/niko/niko/memory-bank/active/preflight-status.mdc` — the canonical status-file vocabulary contract; currently documents only `PASS` / `FAIL`. Add `FAIL (TDD)` **and** `PASS WITH ADVISORY` (the latter is already relied on by both build gates but was never documented here).
- `level2-workflow.md` — the auto-continue sentence ("Parent auto-continues on solid Verdict→build / Verdict→reflect") must include the TDD FAIL → plan edge; STOP-list entry `Preflight FAIL -> Plan` must be narrowed so it does not cover the TDD case.
- `level3-workflow.md` — "both of preflight's Verdict outs are dashed: the parent stops after preflight, PASS included" becomes false with a third, solid out; STOP-list entry `Preflight FAIL -> Plan` needs the same narrowing.
- Status-value literal: write `PASS WITH ADVISORY` in that exact casing, because both `level2-build.md` and `level3-build.md` gate on that string (Handle Results prose may keep "PASS with ADVISORY").

1. **Preflight Handle Results (Items 1–2)**
   - Files: `rulesets/niko/skills/niko-preflight/SKILL.md`, `rulesets/niko/niko/memory-bank/active/preflight-status.mdc`
   - Changes: PASS with ADVISORY → document advisories; still a valid build/transition gate (drop “not a transition grant”). TDD FAIL → `FAIL (TDD)` status + parent re-enters Plan immediately. Enumerate the status values near Generate Preflight Report (`PASS` / `PASS WITH ADVISORY` / `FAIL` / `FAIL (TDD)`) and mirror them into `preflight-status.mdc`.

2. **QA judge wording (Items 3–6)**
   - Files: `rulesets/niko/skills/niko-qa/SKILL.md`
   - Changes: Forbid = don’t modify the work under review. Closed allowlist bullets (status, tasks findings, progress notes, Phase field only). PASS/FAIL Findings templates per suggestions.
   - **Amended by preflight (Finding F5):** Items 4–6 already landed in commit `74afebb` — the allowlist at `SKILL.md:39` is already closed, and the Findings templates at `:67` / `:78` already read “why it does or does not block” / “why it blocks”. Verify and leave them alone. The only remaining QA edit is the `/ruleset/` phrase at `SKILL.md:38` (Item 3).

3. **Spawn charge at nine sites (Item 7)**
   - Files: `level1-workflow.md`, `level2-workflow.md`, `level2-build.md`, `level3-workflow.md`, `level3-build.md`, `level4-workflow.md`, `level4-plan.md`
   - Changes: apply template above

4. **Flowchart renames + TDD edge (Items 2, 8) + L4 delete (Item 9)**
   - Files: `level1-workflow.md`, `level2-workflow.md`, `level3-workflow.md`, `level4-workflow.md`, `rulesets/niko/README.md`
   - Changes: rename nodes; add `FAIL (TDD)` solid edges on L2/L3/README copies; delete L4 inherit sentence
   - README rename sites (six charts): short version, long version, L1, L2, L3, L4-init. README carries no STOP lists, so only chart bodies and the shared legend change there.
   - **Amended by preflight (Finding F2):** in the same pass, fix the L2 auto-continue sentence, the L3 "both outs are dashed" sentence, and the L2/L3 STOP-list `Preflight FAIL -> Plan` entries.

5. **Verify**
   - `make test`; `mmdc` compile of mermaid in touched files; `rg` for leftover abbrevs / old spawn one-liner / “not a transition grant” / inherit sentence

## Technology Validation

No new technology - validation not required

## Dependencies

- None new. Relies on existing `make test` and `mmdc`.

## Challenges & Mitigations

- **TDD FAIL vs Step 4 stop**: Skill must not invoke Plan; parent/chart must. Mitigation: status `FAIL (TDD)` + solid chart edge + Handle Results names the parent.
- **Spawn tripwire drift**: Multi-line charge must stay identical across nine sites. Mitigation: shared stem string; verify with `rg -c` / diff of stems.
- **Creative review page still says PF/PFV**: Historical LOCKED creative for prior build — out of scope to rewrite unless reflect wants a note. Live SoT is `rulesets/niko/`.
- **systemPatterns tripwire description**: Reflect may one-line update if the greppable phrase changes; not a build blocker.

## Pre-Mortem

- **Parent ignores `FAIL (TDD)` and waits forever**: Chart solid edge + explicit Handle Results “parent re-enters Plan immediately” — if still weak, add one parent-resume bullet under Phase Mappings in L2/L3 during build.
- **“Exactly” language sneaks back and fights OptMem**: Brief forbids it; dry-read Item 7 checks wording.
- **Rename misses a README ideology chart**: Step 5 `rg` for `PFV|PFSA|QASA|\bPF\b` under `rulesets/niko/`.

## Preflight Findings (2026-08-07)

Verdict: **PASS WITH ADVISORY**. Plan amended in place for F1–F3 and F6; F4–F5 and F7–F8 are advisory only.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | Medium | `preflight-status.mdc` is the canonical status-file vocabulary and documents only `PASS` / `FAIL`; the plan adds `FAIL (TDD)` and leans on the already-undocumented `PASS WITH ADVISORY` | Plan amended: file added to step 1 |
| F2 | Medium | The new solid `FAIL (TDD)` edge invalidates the L2 auto-continue sentence, the L3 "both outs are dashed" sentence, and the L2/L3 STOP-list `Preflight FAIL -> Plan` entries; unfixed, the STOP list contradicts the chart and the self-heal never fires | Plan amended: sites added to step 4 |
| F3 | Medium | The multi-line fenced Spawn stem cannot be byte-identical across the four indentation contexts the nine sites live in, and a flush-left fence inside a list item breaks the list — defeating the grep tripwire the plan depends on | Plan amended: stem collapsed to one line (see F6) |
| F4 | Low | Both build gates match the literal `PASS WITH ADVISORY`; the skill's prose says "PASS with ADVISORY" | Plan amended: exact casing specified for the status file |
| F5 | Low | Items 4–6 already landed in commit `74afebb`, and Item 7's "no exactly/entire-prompt" half is already satisfied (no such wording exists under `rulesets/niko/`) | Advisory: verify and skip; do not churn |
| F6 | Advisory (applied) | Radical Innovation: make the duplicated unit one line instead of a multi-line block — indentation-immune, greppable with a plain `rg -c`, and already how `systemPatterns.md` describes the tripwire | Applied to the plan; operator may revert to the fenced form |
| F7 | Advisory | Nothing bounds a plan → preflight → `FAIL (TDD)` → plan loop | Accepted: restores prior behavior, not a new regression |
| F8 | Advisory | The LOCKED creative chart page (brief Requirement 1's declared chart source of truth) now diverges from `rulesets/niko/` in both node names and the TDD edge | Suggest reflect adds a one-line "superseded by rework" banner rather than leaving a silent divergence |

TDD Plan Encoding: **PASS** — every unit delivers rule/skill wording and documentation prose, which the always-tdd carve-out exempts; no change-detector tests are scheduled (`make test` and `mmdc` are pre-existing integrity gates, and the dry-read items are acceptance checks, not committed tests).

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight (PASS WITH ADVISORY)
- [ ] Build
- [ ] QA
