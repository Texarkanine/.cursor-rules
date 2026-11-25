# Project Brief

Finish the held Gemini 4 gas placement on draft PR 141 (`google-gasses`).

## User Story

As the operator of choose-verification-model, I want the catalog refreshed from current BenchLM scores and the Gemini 4 gas models placed from experience, so the picker uses tiers I trust.

## Requirements

1. Refresh choose-verification-model from BenchLM.
2. Set tiers by hand:
   - `gemini-4-carbon` moves from A to S
   - `gemini-4-neon` is listed in A
   - `gemini-4-hydrogen` is listed in B
   - `gemini-4-argon` stays in A, because it is being sunset
3. Compare each model's intelligence or benchmark score with the other models in its tier. Flag any score that sits well apart from its tier-mates. Flags are for review only. Do not move a model because of a score mismatch.
4. Continue the in-flight work. It was held because Hydrogen and Neon lacked scores and experience. Those are now enough to place them.

## Out of Scope

- Changing the tier of a flagged non-gas model
- Deriving a tier from a score
