# Project Brief

## User Story

As an operator of Cursor agents, I want a short always-on ISO 24495 decompression key so that agent-to-operator prose follows the ISO plain-language standard without copying paid standard text.

## Use-Case(s)

### Use-Case 1

An agent writes to the operator. The rule names ISO 24495 and its four principles. The agent applies the standard in the spirit of those principles.

### Use-Case 2

A consumer installs the rule a la carte from `rules/`. The file points at a public, freely available summary. The consumer does not need a paid ISO PDF.

## Requirements

1. Fill in the stub `rules/iso-24495.mdc`.
2. Match the shape of `rules/asd-ste100.mdc`: short, `alwaysApply: true`, name the standard, point at a canonical public URL, keep the precision exception.
3. Treat the file as a decompression key: name the framework so pretrained knowledge can fire. Do not rewrite the standard.
4. Ground the key in the ISO 24495 series, not only Part 3.
5. Include the four Part 1 principles: relevant, findable, understandable, usable.
6. Note that later parts apply those principles to legal communication (Part 2) and science writing (Part 3).
7. Link to https://www.iplfederation.org/iso-standard/ as the public canonical summary. Do not link to a sample PDF.

## Constraints

1. Do not copy paid ISO standard text.
2. Do not add a ruleset unless later requested. `asd-ste100.mdc` ships a la carte from `rules/`.
3. If the style would drop a required technical term or a precise meaning, keep the term. Clarity wins.
4. Canonical source is `rules/iso-24495.mdc`. Do not edit generated `.cursor/` copies.

## Acceptance Criteria

1. `rules/iso-24495.mdc` is a short always-on decompression key in the same spirit as `rules/asd-ste100.mdc`.
2. The rule names ISO 24495, the four Part 1 principles, and Parts 2 and 3 by role.
3. The only standard URL is the IPL Federation page.
4. The precision exception is present.
5. `make test` still passes.
