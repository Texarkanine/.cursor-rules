# Progress

Make Niko Plan emit per-unit always-tdd (stub → red → green) ordering for executable work so preflight stops rewriting plans, while keeping the prose carve-out and the hard preflight gate.

**Complexity:** Level 3

## 2026-08-18 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Restated intent; operator approved and added: leverage decompression keys / always-tdd content; decide whether Plan must load the rule document; mine stockroom for preflight TDD patches and infer the planning failure.
    - [Stockroom TDD plan fails](20ca6343-37e4-4857-bdb3-1c49efe0bfc7): ~31 explicit incidents; typical Plan shape was TDD in the preamble/label plus implementation-centric `Changes`; preflight usually amended in-phase (band-aid) rather than failing out.
    - [Decompression vs load always-tdd](319f1441-aed3-4a43-94c5-3df1c1e3b88b): `always-tdd` cannot be a daz.is key (local, no pretraining mass); "TDD red-green-refactor" is the pretrained name Plan already used; recommended making numbered substeps the work and holding an explicit load in reserve.
    - Classified Level 3.
* Decisions made
    - Level 3: one open question (how Plan activates always-tdd) needs Creative before a locked implementation plan.
    - Do not restore TDD self-heal.
* Insights
    - Bundling always-tdd did not fail because the file was missing from context. It failed because Plan compressed it into a disclaimer and the template's sibling fields (`Tests first` next to `Changes`) told the agent order did not matter.
    - `level2-build.md` already numbers stub → red → green; Plan still bullets a TDD cycle gloss. The two phases disagree.
    - Daz: named keys unpack pretrained knowledge; they are "not a replacement for explicit instructions when you need something specific or novel." always-tdd's stubbing ritual is that novel part.

## 2026-08-18 - PLAN - IN-PROGRESS

* Work completed
    - Component analysis written to `tasks.md`. One open question: how Plan activates always-tdd.
* Decisions made
    - Treat L2 and L3 plan docs as the change surface; do not widen into Preflight, always-tdd, or Build unless Creative forces it.
* Insights
    - Build already numbers the four-step process; Plan still bullets a TDD gloss. The phases disagree.

## 2026-08-18 - CREATIVE - COMPLETE

* Work completed
    - Explored plan-tdd-activation (generic creative). High confidence: D template-as-schedule; B load in reserve.
* Decisions made
    - Plan's output contract is numbered always-tdd stages per executable unit, not a TDD label or `Tests first:` field.
    - Do not paste always-tdd's body. Do not add a Read step in this change.
* Insights
    - `always-tdd` is not a daz.is decompression key (local policy). The pretrained key Plan already used ("TDD red-green-refactor") is the wrong ritual and Daz flags it. Structure has to carry order.

## 2026-08-18 - PLAN - COMPLETE

* Work completed
    - Test plan: no new tests (prose/policy); `make test` still required.
    - Implementation plan: L2 then L3 plan docs get typed units + numbered always-tdd substeps; non-goals dry-read for router/preflight/always-tdd/build/L4.
    - Challenges and pre-mortem recorded.
* Decisions made
    - This task's own `tasks.md` uses the target schedule shape (prose/policy units) so preflight judges the new contract.
    - Load step is not in the implementation plan.
* Insights
    - The first live test of executable encoding is the next Niko task that changes code, not this diff.

## 2026-08-18 - PREFLIGHT - COMPLETE (PASS WITH ADVISORY)

* Work completed
    - Ran all six checks against the plan. TDD Plan Encoding passes: three prose/policy units, no change-detectors scheduled.
    - Applied three plan amendments: installed-path form for `always-tdd` pointers; a prose/policy exemption slot in the `Behaviors to Verify` template; Unit 3's conditional Build clause rewritten as a confirmed one-line fix.
    - Verified no downstream consumer (`niko-qa`, `nk-save`, `niko-archive`, `niko-plan`, `level4-plan`) depends on the `Files` / `Tests first` / `Changes` field names.
* Decisions made
    - All three findings are amendments, not rearchitect: none changes the locked creative decision or the brief's scope.
    - Advisory "point Plan at Preflight's FAIL clauses" is recorded but not applied — it would contaminate the single-variable test the creative set up (D alone, B in reserve).
* Insights
    - The dry-read in Unit 3 would probably have missed the clash it was written to catch: `level3-build.md` carries the same red-green-refactor gloss this task deletes from `level3-plan.md`, while `level2-build.md` already names the full sequence. Only L3 disagrees with itself.
    - The plan fixed the artifact for implementation steps but left the Test Plan section instruction-only — the exact instruction-loses-to-template failure this task exists to fix, reappearing one section up.

## 2026-08-18 - BUILD - COMPLETE

* Work completed
    - L2 and L3 Plan docs: typed units; executable numbered always-tdd stages; prose/policy `No tests:` line; Behaviors to Verify exemption slot.
    - L3 Build Step 4.1 now names the same stub → red → green sequence as L2 Build.
    - Dry-read with no edits: niko-plan router, preflight TDD gate, always-tdd, L4 plan.
    - `make test` passed (symlink + README-link checks).
* Decisions made
    - Built D (template-as-schedule) only. No Read-always-tdd step. Preflight advisory (point Plan at FAIL clauses) left unapplied.
* Insights
    - Instruction and template had to change together; leaving `Tests first` / `Changes` in either file would have kept the FAIL shape.
