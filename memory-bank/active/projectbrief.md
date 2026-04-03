# Project Brief: Intent Clarification Loop

## User Story

Add an intent-clarification loop to Niko's `/niko` entrypoint, after entry and before complexity analysis. When a user provides input, Niko ingests it fully — fetching any linked resources and doing whatever additional research it judges necessary to build understanding. From that, Niko produces a restatement of the user's intent, sized proportionally to the input. The user either approves or doesn't; if not, Niko asks questions, researches further, and restates again until the user confirms.

When an external source (issue tracker, spec doc, etc.) already contains a complete intent definition, the restatement must not lossy-compress it into a self-contained summary that downstream phases treat as canonical *instead of* the source. In such cases, the restatement should reference the external source as authoritative and can be as minimal as "as described in [link]" — the goal is to build a robust canonical intent statement via dialogue only when the user hasn't already provided one through other means.

Success criterion is user approval alone — no encoded definition of ready. The approved restatement becomes the source of truth consumed by downstream phases. Placement is known (after entry, before complexity analysis); structural form is not yet decided.

## Requirements

- Zero added friction when input is already well-specified — the phase should be lightweight, not invisible (always restates), but must not shed information from complete external specs
- Must precede complexity analysis — produces the refined intent that complexity analysis consumes
- Works for all input types: bare prompts, links to external specs, combinations
- No new top-level command — lives within `/niko`
- Restatement loop must converge — cannot become infinite "are you sure?" cycles
- Restatement is sized proportionally to the input (compress verbose input, expand terse input as needed)
- External references that are already complete specs should be passed through by reference, not summarized

## Reference

- GitHub Issue: https://github.com/Texarkanine/.cursor-rules/issues/60
