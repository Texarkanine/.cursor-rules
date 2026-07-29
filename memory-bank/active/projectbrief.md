# Project Brief

Authoritative specification: [issue #95](https://github.com/Texarkanine/.cursor-rules/issues/95). This brief does not restate the issue; it records the session's scope decisions on top of it.

## User Story

As an operator running Niko, I want TDD to apply only to executable behavior so that agents stop inventing worthless string and heading assertions on human-facing prose, and so that a plan proposing such tests is rejected before it reaches build.

## Use-Case(s)

### Editing a prose or policy artifact

An agent changes a PR template, CONTRIBUTING, docs content, or rule and skill wording. Today `always-tdd` pressures it to write pytest assertions on headings and checklist presence. After this change, the agent recognizes the artifact as non-executable and writes no tests, without appearing to violate TDD.

### Preflighting a plan that still proposes prose tests

A plan reaches `/niko-preflight` with steps that schedule string assertions on markdown content. Today preflight accepts it, and its blocking TDD check is part of what produced it. After this change, preflight fails the plan and instructs removal of those steps.

## Requirements

1. `always-tdd.mdc` states an executable-versus-prose scope carve-out: TDD governs executable behavior, and does not govern human-facing prose or policy artifacts.
2. The carve-out forbids inventing string, heading, or checklist assertions to satisfy TDD, and names the alternative enforcement paths: review, a purpose-built gate, or nothing.
3. `niko-preflight` fails a plan that proposes tests locking prose, policy, or markdown content, with a fix instruction to remove them.
4. `niko-preflight` does not fail a plan that correctly omits TDD ordering for non-executable units under its existing implementation-only check.

## Constraints

1. Edit only the tracked source of truth: `rules/always-tdd.mdc` and `rulesets/niko/skills/niko-preflight/SKILL.md`. The `.cursor/` and `.claude/` trees are generated copies and must not be edited.
2. `always-tdd.mdc` is distributed standalone by `ai-rizz`, so the carve-out must stand on its own without depending on Niko or preflight being installed.
3. The carve-out must not become a loophole for skipping tests on executable behavior. The prior failure was an agent reclassifying prose assertions as "structural markers," so the boundary has to resist relabeling.
4. Packaging-style tests that lock executable install contracts stay legitimate and must not be swept into the carve-out.
5. Repo prose conventions apply: `markdown-style.mdc` and `asd-ste100.mdc`.

## Out of Scope

Per the issue: rewriting the level2 plan and build documents, and banning packaging-style tests on executable install contracts.

## Acceptance Criteria

1. `always-tdd.mdc` states the executable-versus-prose carve-out.
2. `niko-preflight` fails plans that schedule prose or template string-assertion tests.
3. `niko-preflight` does not fail plans that correctly skip TDD for prose-only units.
4. `make test` passes.
