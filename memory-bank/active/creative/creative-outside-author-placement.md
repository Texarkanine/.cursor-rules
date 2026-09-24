# Architecture Decision: Outside Author Placement

How should `pick.py` choose a reviewer for an author whose model is not a catalog row, so that every author gets a reviewer?

## Requirements & Constraints

Ranked quality attributes:

1. Correct reviewer: strong enough and a different family, judged by the operator's tiers.
2. Coverage: the authors who actually show up outside the catalog get a reviewer.
3. Predictability: the operator can say in one sentence why a reviewer was printed.
4. Size and upkeep: no machinery whose output is not used.

Operator facts (2026-09-24):

- **Tiers are trust calibration, not score.** A hand-set tier is the operator's judgment of how well a model does what they ask, the way they ask it. `kimi-k3` sits at A above `claude-opus-5-5` at S on purpose: it scores high, but it is not yet trusted with S-tier work. A tier cannot be derived from a score.
- **Outside authors are always brand-new models, in the hour they ship.** The operator is present and sets a tier as part of onboarding the model to try it.

Constraints from the brief: the catalog is the hand-tiered set; one score per model; no invented numbers; `SKILL.md` stays a thin caller.

## Components

- `assets/catalog.json`: hand-set tier, BenchLM mean, and price for each onboarded model. A row is a reviewer candidate only when its slug is also in `--reviewer-models`.
- `select`: works out the author's tier, then runs the rank window, then the one-tier-up cheapest step. An author whose model is not a row is printed back with exit 0.

## Evidence

- Every rule that reads a tier off score neighbours contradicts the tiers' meaning. With the adjacent-rows rule, `claude-mythos-5` (85.45) lands at A and `step-5-preview` (77.47) at S. That result is not a bug to fix with a better rule: no score rule can reproduce a trust judgment.
- `scores[model_key(slug)]` matches 2 of 12 live Task slugs, because BenchLM uses dashes where Cursor uses dots.
- A wide `scores.json` is written at refresh time. A model released after the last refresh is in neither file, and brand-new models are the only outside authors.
- On the current branch (`5f4b940`), `make test` passes 48 tests. Acceptance commands 1, 2, and 5 print `claude-opus-5-5-high-fast`, `claude-opus-5-5-high`, and `missing-author`, each with exit 0.

## Options Evaluated

- **A. Plan as written**: wide `scores.json`; tier from the two adjacent catalog rows, higher on a boundary.
- **B. Plan, fixed**: A plus an ordered slug lookup and a tier rule that never ranks a better author lower.
- **C. Hand-set default tier for any outside author**: one catalog field; no score lookup.
- **D. B, with C as the fallback.**
- **E. Onboard, don't place**: a new model gets a catalog row and a hand tier when the operator adopts it. `select` keeps printing the author back for the brief gap before that. No new asset or placement code.

## Analysis

| Criterion | A | B | C | D | E |
|---|---|---|---|---|---|
| Correct reviewer | Tier from score: wrong in principle | Tier from score: wrong in principle | Guessed tier | Guessed tier | Operator's tier |
| Coverage | Misses new models | Misses new models | Every author | Every author | Every onboarded author; echo in the gap |
| Predictability | Low | Medium | High | Medium | High |
| Size and upkeep | New asset + rules | More | ~10 lines | Most | Nothing new |

Key insights:

- A, B, and D infer a tier from a score, and tiers encode trust, not score. C guesses a tier for a model the operator is about to tier anyway.
- The case every option was built for (an author with no catalog row) exists only in the minutes between release and onboarding. The existing echo already covers those minutes, with exit 0.

## Decision

### Choice Pre-Mortem

- A new model is used as an author before it has a catalog row: **checked**. The operator onboards in the release hour, and the echo keeps the pick from failing meanwhile.
- Onboarding is too heavy, so it gets skipped: **checked** in part. It is a mapping row plus `refresh.py`, which warns about a missing tier, then one hand-set tier.

**Selected**: E. Onboard, don't place.
**Rationale**: The ranked top attribute is a correct reviewer by the operator's judgment, and only the operator's tier gives that. Coverage holds because onboarding happens in the release hour. It adds nothing to maintain.
**Tradeoff**: An author used before onboarding reviews itself (the echo), not a peer. Accepted, because that window is minutes and the operator is present.

## Implementation Notes

- Drop plan steps 1 and 2 (`benchlm_scores`, `scores.json`, outside-author placement) and Rework rules 3 and 4 in the brief.
- Keep the stem-keyed catalog and the effort collapse from `5f4b940`; the tests and acceptance commands already pass there.
- `refresh.md`: say that tiers are hand-set trust calibration and that a new model is onboarded with a mapping row, a refresh, and a tier. This is prose; no tests.
