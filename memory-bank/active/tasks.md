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
| `QA` (subgraph node) | `NikoQA` |
| `QAV` | `QAVerdict` |
| `PFSA` | `PreflightSubagent` |
| `QASA` | `QASubagent` |

### Spawn charge template (Item 7) — nine sites

Shared stem (tripwire — identical at every site aside from skill name in the fence):

~~~markdown
Spawn a subagent (prefer smarter / different family if available); do not run the skill in this conversation. Charge the subagent with only this — do not add further instructions:

```
Run the `/niko-preflight` skill
```
~~~

(Use `/niko-qa` where the site is QA.) Build-gate sites keep their `STOP —` / re-check prefix around the same stem. Do **not** claim the entire prompt is exactly that one line.

### TDD self-heal (Item 2)

- `niko-preflight` writes `.preflight-status` = `FAIL (TDD)` for TDD plan-encoding failures (other fails stay `FAIL`)
- Handle Results: block build; cite units; **parent re-enters Plan immediately to restructure** (skill still stops at Step 4)
- L2/L3 (+ README mirrors): add solid `PreflightVerdict -->|"FAIL (TDD)"| NikoPlan` alongside existing dashed other-FAIL → ManualPlan
- L4 already solids all FAIL → NikoPlan; keep that; status value still `FAIL (TDD)` for clarity
- FAIL report Next Steps: mention TDD case → Plan auto (parent)

1. **Preflight Handle Results (Items 1–2)**
   - Files: `rulesets/niko/skills/niko-preflight/SKILL.md`
   - Changes: PASS with ADVISORY → document advisories; still a valid build/transition gate (drop “not a transition grant”). TDD FAIL → `FAIL (TDD)` status + parent re-enters Plan immediately. Optionally clarify status values near Generate Preflight Report.

2. **QA judge wording (Items 3–6)**
   - Files: `rulesets/niko/skills/niko-qa/SKILL.md`
   - Changes: Forbid = don’t modify the work under review. Closed allowlist bullets (status, tasks findings, progress notes, Phase field only). PASS/FAIL Findings templates per suggestions.

3. **Spawn charge at nine sites (Item 7)**
   - Files: `level1-workflow.md`, `level2-workflow.md`, `level2-build.md`, `level3-workflow.md`, `level3-build.md`, `level4-workflow.md`, `level4-plan.md`
   - Changes: apply template above

4. **Flowchart renames + TDD edge (Items 2, 8) + L4 delete (Item 9)**
   - Files: `level1-workflow.md`, `level2-workflow.md`, `level3-workflow.md`, `level4-workflow.md`, `rulesets/niko/README.md`
   - Changes: rename nodes; add `FAIL (TDD)` solid edges on L2/L3/README copies; delete L4 inherit sentence

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

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
