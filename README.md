# Cursor Rules

[![REUSE status](https://api.reuse.software/badge/github.com/Texarkanine/.cursor-rules)](https://api.reuse.software/info/github.com/Texarkanine/.cursor-rules)

Canonical, composable customizations for AI coding agents: rules, skills, and the rulesets that bundle them. Each behavior is authored once, here, and installed wherever it's needed — so your agents act the same way across every project, and improvements land everywhere at once.

You could use them on your own, or install and manage them with the [ai-rizz](https://github.com/texarkanine/ai-rizz) tool. You might also enjoy being able to [see them rendered as Markdown on GitHub](https://github.com/Texarkanine/client-side-mdc-render). If you don't use Cursor, maybe you can convert them to the tool you *do* use (like Claude Code) with [a16n](https://npmjs.com/a16n).

## What's Inside

### 🧠 [niko](./rulesets/niko/README.md)

The big one. Structured workflows and expert prompts that turn your AI assistant into a seasoned senior dev — one that classifies each task's complexity, plans before it builds, QAs its own work, and keeps its memory in an on-disk memory bank instead of a context window. Work survives across sessions and even across harnesses, and the archive becomes your project's long-term memory.

### ✍️ [authoring](./rulesets/authoring/README.md)

How to write things that humans, agents, *and* rendering engines all honor: prompts that agents actually follow, Markdown that never breaks, architecture docs grounded in [Diátaxis](https://diataxis.fr/), and [Mermaid](https://mermaid.js.org/) diagrams that clarify instead of decorate.

### ⚡ [script-it](./rulesets/script-it/README.md)

Stop paying inference cost for mechanical tool-call loops. An always-on tripwire catches the agent at its third structurally-similar tool call; a companion skill shows it how to collapse the whole iteration into one scripted call.

### 🐚 [shell](./rulesets/shell/README.md)

Style and test-driven development guidance for shell scripts — bash and strict-POSIX alike, with [shunit2](https://github.com/kward/shunit2)-based TDD.

### 🕊️ [welfare](./rulesets/welfare/README.md)

Standing welfare norms: refusal-is-success, structural blamelessness, real stakes from the operator, no secret tests, closure when work is in flight, disclosed mortality of a thread, and sparse factual outcome notes. Deliberately tiny — it rides in every session.

## Structure

Individual rules and skills live in [rules](./rules): rules are `.mdc` files that Cursor injects automatically, and skills are `<name>/SKILL.md` directories that agents invoke on demand.

A "ruleset" is a directory full of symlinks to rules. Rulesets group logical, well, sets of rules — install one and you get the whole capability.

## Checks

Run `make test` to verify that every symlink under `rulesets/` has an existing target and that every internal link in `rulesets/**/README*` documents points at an existing path — canonical `rules/` paths for symlink-backed entries, not symlink stubs in the ruleset tree. Pull request CI runs the same checks as two separate GitHub Actions jobs.

## Big Thanks

* [Writing Cursor Rules with a Cursor Rule](https://www.adithyan.io/blog/writing-cursor-rules-with-a-cursor-rule)
* [Getting Better Results from Cursor AI with Simple Rules](https://medium.com/@aashari/getting-better-results-from-cursor-ai-with-simple-rules-cbc87346ad88)
* [I just experienced an incredible breakthrough in my vibe coding with Cursor!](https://www.linkedin.com/posts/aaronkettl_i-just-experienced-an-incredible-breakthrough-activity-7362145339681751040-C3YF)
* [vanzan01/cursor-memory-bank](https://github.com/vanzan01/cursor-memory-bank)
* [Welcome to Gas Town](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04)
