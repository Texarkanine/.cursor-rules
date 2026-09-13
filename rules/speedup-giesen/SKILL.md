---
name: speedup-giesen
description: Walk a finished, behavior-correct codebase looking for work you can stop doing so it gets faster without changing what it does. Use when the product already works and the ask is speed, a 10x or 100x win, or whether you are doing something stupid. Not for new features, a YAGNI simplification pass, or clever micro-opts that add machinery.
---

# Speedup Giesen

> look, I'm sorry, but the rule is simple:
> if you made something 2x faster, you might have done something smart
> if you made something 100x faster, you definitely just stopped doing something stupid
>
> — Fabian Giesen (@rygorous), 11 June 2020, https://x.com/rygorous/status/1271296834439282690

That quote is the stance. Do not unpack it into a performance textbook. Hunt wasted work, not cleverness. The pass below is only what the quote does not already say: a finished product, preserved behavior, and a stop when the only wins are the smart kind.

## The Pass

1. Confirm the product already behaves correctly. If the ask is a new feature or a behavior change, stop — this skill does not apply.
2. Name the surfaces that must get cheaper: whatever the operator named, or else the boot or request path the user actually waits on. Do not hunt the rest of the tree.
3. Walk those surfaces for wasted work. The class looks like: the same job every tick or render, parsing more than the answer requires, a new connection per request, rebuilding what is already in hand, destroying work before the replacement exists. Those are examples of the class, not a checklist to exhaust.
4. Classify each candidate. Stopping it is something stupid (the 100× class) or something smart (the 2× class: a new cache layer, a clever algorithm, an architecture rewrite). Keep the first. Leave the second unless the operator asked for clever.
5. Apply only the stupid-class cuts. Observable behavior stays. Do not add machinery to go faster. Do not edit tests unless a new hold would make a broken optimization invisible — then add the smallest behavior lock, not a wording assertion.
6. Verify behavior still holds. Report what you stopped doing and which class of speedup it is. When you can time the named surface, put the observed multiplier next to the class label. If you only find 2×-smart candidates, report them and stop.
