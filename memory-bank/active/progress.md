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
