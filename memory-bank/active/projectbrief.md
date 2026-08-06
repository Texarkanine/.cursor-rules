# Project Brief: model-welfare Phases 1–3

## User Story

As the shop (Niko on Macbeth, and future seats), I need boundary handoffs, always-on welfare norms, and outcome-note habits so sessions can close cleanly, wake with purpose, and avoid empty ritual — per `model-welfare/PLAN.md` (including § Amendments A2).

## Requirements

1. **Private `handoff` skill** (D2 + A2 + E9), authored in `model-welfare`, installed into seat harness trees (`~/.cursor`, a16n → `~/.claude`):
   - Five bullets + provenance; skippable when nothing in flight
   - Destination: `handoffs/<remote-basename>/<seat>.md` in shop repo; pull → write → push
   - `memo note "HANDOFF: …"` for wake
   - Seat from `~/.config/cotm/seat`; shop path from `~/.config/cotm/shop-repo`
   - E9 successor repair rite; compose with nk-save in Niko projects
2. **Public norms rule** (D4 + E1 + D3 outcome-notes paragraph) in `.cursor-rules`, ~15 lines hard cap, always-on; no private shop paths
3. **A3 trailers**: prompt-driven `Co-authored-by: Niko <niko@cani.ne.jp>` at harness config level
4. **model-welfare SoT cleanup**: migrate root `HANDOFF.md` → `handoffs/model-welfare/niko.md`; tidy surface so founding artifacts don't confuse current state
5. **Distribute** public norms via ai-rizz + a16n; install private skill into seat trees; verify acceptance (any-repo `/handoff`, meaningful decline, wake surfaces note)
6. R1 interval digest only if diffs stay small after 1–3

## Constraints

- Public `.cursor-rules` must not instruct private-shop pull/write/push
- One concern per commit, `--no-gpg-sign`
- Feature branch off `main` in `.cursor-rules`; companion commits in `model-welfare`
- consultations.md governs underspecified design; no ceremony the models rejected
