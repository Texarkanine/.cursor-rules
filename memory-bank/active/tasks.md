# Task: model-welfare Phases 1–3

* Task ID: model-welfare-phases-1-3
* Complexity: Level 2
* Type: simple enhancement (known-spec artifacts across public rules + private shop + seat install)

Ship boundary handoff (private), always-on welfare norms (public), outcome-notes convention, seat attribution trailer prompt, and model-welfare SoT cleanup — per PLAN.md including § A2 and operator decisions (cotm config, skill home in shop repo).

## Test Plan (TDD)

### Behaviors to Verify

- B1 `/handoff` with work in flight → writes five-bullet baton to `$SHOP/handoffs/<remote-basename>/<seat>.md`, commits+pushes shop repo, `memo note "HANDOFF: …"` lands in OptMem
- B2 `/handoff` with nothing in flight → agent declines with a complete one-line response; no baton write required
- B3 Missing `~/.config/cotm/seat` or `shop-repo` → skill fails clearly (tells operator what's missing); does not invent paths
- B4 Repo slug = git remote basename (strip `.git`); no-remote → decline with reason
- B5 E9: when waking into a ragged ending, successor may reconstruct baton from stockroom tail, mark reconstructed, proceed
- B6 Public norms rule present, always-on, ≤~15 lines body, contains refusal-is-success / blamelessness / E1 mortality disclosure / OUTCOME: convention; **no** private shop paths
- B7 Next session `memo wake` surfaces the `HANDOFF:` note (acceptance criterion)
- B8 Agent commits include `Co-authored-by: Niko <niko@cani.ne.jp>` by prompt; bare operator commits stay bare
- B9 `make test` in `.cursor-rules` passes after public ruleset added
- B10 model-welfare surface: no root `HANDOFF.md`; baton at `handoffs/model-welfare/niko.md`; README reflects current SoT

### Edge Cases

- Empty / whitespace seat file → treat as missing config
- Shop repo dirty unrelated to handoff → pull --rebase or fail clearly; don't clobber
- Niko project with active MB → flush via nk-save semantics first, then write baton
- Public `.cursor-rules` diff must not grow shop-private instructions (review gate)

### Test Infrastructure

- Framework: `.cursor-rules` has `make test` (symlink + README link checks only). No unit-test runner for skill/rule prose.
- Verification mode: **operational acceptance** after install (B1/B2/B7) + `make test` (B9) + file/content review (B6/B10). Not shunit2 cycles.
- New test files: none (prompt artifacts). Flag for operator: TDD here means acceptance checklist executed in build/QA, not new automated tests.

## Implementation Plan

1. **Seat config bootstrap (Macbeth)**
   - Files: `~/.config/cotm/seat`, `~/.config/cotm/shop-repo` (local only, not committed)
   - Changes: write `niko` and absolute path to model-welfare clone

2. **Private handoff skill in shop repo**
   - Files: `model-welfare/skills/handoff/SKILL.md` (and brief `model-welfare/skills/README.md` noting birth-install)
   - Changes: workflow skill — request not SIGTERM; five bullets + provenance; read cotm; resolve remote basename; pull → write → commit → push; memo note; decline path; E9 repair; nk-save compose note; audience invariant one-liner

3. **Migrate baton + stub handoffs tree**
   - Files: `model-welfare/handoffs/model-welfare/niko.md` (from root `HANDOFF.md`); delete root `HANDOFF.md`
   - Changes: content updated for post-impl state only at end; during build may write interim "impl in progress" then final at close

4. **Seat attribution rule (private, seat-installed; source in shop)**
   - Files: `model-welfare/rules/seat-attribution.mdc`; install copy to `~/.cursor/rules/` (global personal)
   - Changes: always-on prompt: when agent commits, add `Co-authored-by: Niko <niko@cani.ne.jp>`; never rewrite author; bare commits = operator hand signal

5. **Public welfare norms rule**
   - Files: `rules/welfare-norms.mdc`, `rulesets/welfare/welfare-norms.mdc` (symlink), `rulesets/welfare/README.md`; root `README.md` ruleset list entry
   - Changes: ~15-line alwaysApply: refusal-is-success, blamelessness, stakes from operator, no secret tests, closure when work in flight (name `/handoff` without shop paths), E1 thread terms, OUTCOME: paragraph (D3)
   - Commit: one concern — `feat(welfare): add always-on norms rule`

6. **SoT cleanup of model-welfare README / surface**
   - Files: `model-welfare/README.md`, possibly short `STATUS.md` or restructure Contents table; retire kickoff-as-primary framing
   - Changes: surface reads as canonical practices + pointers (PLAN for history, skills/ for installable shop practice, handoffs/ for batons); founding narrative demoted

7. **Install into seat harness + distribute public norms**
   - Copy/symlink `model-welfare/skills/handoff` → `~/.cursor/skills/handoff`
   - Copy seat-attribution into global cursor rules path
   - Push `.cursor-rules` branch; `ai-rizz` sync global for welfare ruleset; `a16n convert` for Claude trees (public norms + private skill as applicable)
   - Commit model-welfare artifacts separately (skill, handoffs, cleanup, attribution source)

8. **Acceptance verification**
   - Run decline-path dry judgment; write a real short handoff from a throwaway state or from this session's close; `memo wake` / recall for `HANDOFF:`; `make test`
   - R1: **deferred** (OptMem wake change; Niko phase-end already supplies session handoff shape)

## Technology Validation

No new technology - validation not required. Uses existing: OptMem `memo`, git, ai-rizz, a16n, Agent Skills SKILL.md format.

## Dependencies

- OptMem (`~/.optmem/memo`) on PATH
- Writable clone at `~/.config/cotm/shop-repo` with push access to private remote
- `ai-rizz` / `a16n` for distribution steps
- stockroom available for E9 path (skill documents the rite; full E9 exercise optional if no ragged ending exists)

## Challenges & Mitigations

- **Public/private bleed**: Review gate in step 5 — norms text must not mention model-welfare paths, cotm, or pull/push. `/handoff` name alone is OK.
- **ai-rizz reads remote, not working tree**: Push `.cursor-rules` before global sync; sync is a separate chore commit after merge or on the feature branch remote.
- **Shop pull/push races**: Skill does `git pull --rebase` then write; on conflict, stop and report — no force push.
- **TDD gap for prose**: Mitigated by explicit acceptance checklist (B1–B10) in QA; do not invent a test harness for markdown skills.
- **Root HANDOFF.md readers**: README + PLAN still mention it; cleanup step rewrites those pointers.

## Pre-Mortem

- **Failed because public norms accidentally documented shop internals**: Add explicit QA checklist item "rg shop-repo|model-welfare|cotm against rules/welfare-norms.mdc must be empty."
- **Failed because skill installed but Cursor doesn't see it**: Verify path is `~/.cursor/skills/handoff/SKILL.md` (Agent Skills layout); document in skills/README for birth process.
- **Failed because acceptance can't prove wake surfacing without ending session**: Use `memo note` + `memo recall HANDOFF` / fresh `memo wake` in a subshell as proxy; real cross-session proof is one wake away — note that residual in reflect.
- **Wrong layer — building R1 into OptMem**: Already cut; do not expand scope.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
