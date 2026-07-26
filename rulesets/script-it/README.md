# Script-It Ruleset

Agents love to implement for-loops at inference cost: the same tool call, over and over, with slightly different arguments. This ruleset stops that. A tripwire rule catches the loop as it starts, and a skill shows how to collapse the whole iteration into a single scripted tool call.

## 🚨 [script-it-instead](./script-it-instead.mdc)

- **Purpose**: Always-on tripwire. Before the third structurally-similar tool call, stop — you're implementing a for-loop at inference cost — and script the iteration instead.
- **Scope**: Every agent session (`alwaysApply`). Triggers on mechanical "for each X, do Y" patterns, collect-then-reason loops, and reimplemented standard CLI operations.

## 📜 [how-to-script-it-instead](./skills/how-to-script-it-instead/SKILL.md)

- **Purpose**: The how-to that the tripwire hands off to: discover what runtimes and CLI tools the environment already provides, choose the right approach (shell pipeline, API CLI, or runtime stdlib), and structure a collect → compress → output script that replaces N tool calls with one.
- **Scope**: Invoked when the tripwire fires, or any time repetitive tool-call work should become a batch script. Zero-install by design — it never adds dependencies to your project.
