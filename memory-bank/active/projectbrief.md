# Project Brief: Niko Commit Autonomy

## Problem

Cursor's base agent prompt (injected under the `Shell` tool description, in `<committing-changes-with-git>`) contains:

> "NEVER commit changes unless the user explicitly asks you to. It is VERY IMPORTANT to only commit when explicitly asked, otherwise the user will feel that you are being too proactive."

This instruction — reinforced with "NEVER", "VERY IMPORTANT", and the user-annoyance framing ("user will feel...") — is strong enough to override workspace rules that prescribe commits. Agents running Niko phase transitions hesitate or skip the commits explicitly prescribed by:

- `level{2,3,4}-workflow.mdc` ("🚨 CRITICAL: Commit all changes - memory bank *and* other resources")
- `nk-save/SKILL.md` (`chore: saved work on [task-id] at [phase]`)
- Any Niko phase document that prescribes a commit as part of its wrap-up

Full diagnostic transcript (including verbatim excerpt of Cursor's injected block): `memory-bank/active/cursor_request_for_system_prompt_detail.md`.

## Goal

Design (not yet implement) a **minimal but effective** change to the Niko ruleset that dissolves the conflict so agents running Niko workflows reliably perform the prescribed commits without the operator having to re-ask each time.

## Requirements

1. **Minimal surface area** — one surgical insertion point preferred; avoid editing dozens of Niko files.
2. **Dissolves the conflict, doesn't fight it** — frame Niko-prescribed commits as *satisfying* the base prompt's "user explicitly asked" condition rather than as an *override*. First-person, standing, pre-authorization. (Claude's counter-proposal in the transcript; preferred over Grok's adversarial "override" framing.)
3. **Bounded scope** — must not license commits outside Niko-prescribed moments. The authorization covers phase-transition commits, `/nk-save`, and any commit a Niko phase document prescribes verbatim; nothing more.
4. **Creative phase required** — user wants to collaboratively pick-and-choose phrasing before anything ships.
5. **Placement decision is part of the design** — open questions: workspace-level (inside `rulesets/`) vs. user-level (`~/.cursor/rules/`); new standalone file vs. addition to `niko-core.mdc`.
6. **Validation strategy is part of the design** — need a lightweight way to confirm the rule actually works across models (Claude, GPT-5.x, Grok); none of this is guaranteed to win the priority fight, so A/B-style validation matters.

## Out of Scope

- Implementation (writing the final content / moving files). That comes after the creative phase lands on a chosen design.
- Touching the contents of existing Niko workflow files beyond, at most, a one-line pointer (to be decided in creative phase).
- Rearchitecting Niko's commit semantics.

## Success Criteria

- A creative-phase document that explores at least the placement and framing axes, with tradeoffs enumerated and a chosen option.
- A plan document precise enough to execute in the build phase without further design decisions.
- Explicit validation plan (how we'll know it worked).
