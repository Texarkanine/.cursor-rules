# Product Context

## Target Audience

Primarily the repository author, who uses these rules daily in Cursor. Secondarily, anyone who installs a subset with `ai-rizz`, converts them to another harness (e.g. Claude Code) with `a16n`, or reads them rendered on GitHub.

## Use Cases

- Reusable Cursor rules and rulesets that shape AI behavior consistently across many projects.
- The Niko memory-bank system: complexity-based task routing, context preservation across sessions, and archival of completed work.
- Topic-specific guidance (shell, markdown authoring, prompt authoring, TDD, and so on) that an agent pulls in when it becomes relevant.

## Key Benefits

- One canonical source for each rule, consumed by multiple harnesses instead of copy-pasted per project.
- Rules compose into rulesets, so a consumer installs only the slice they need.

## Success Criteria

- A rule is self-contained enough to install on its own, yet composes cleanly into a ruleset.
- Guidance is durable: it states intent and points at canonical sources rather than duplicating values that drift.

## Key Constraints

- This repo is consumed by external tooling (`ai-rizz`, `a16n`), so the shape of `rules/` and `rulesets/` is a contract, not just an internal layout.
- The repo both *defines* the Niko system and *uses* it on itself, so its own `memory-bank/` must obey the same rules it ships.
