# Project Brief: README Refresh — Sell the High-Value Contents

## User Story

After retiring old/meta content on the `cleanup-old` branch, the repo's public face must tout what remains. A reader landing on the root README should immediately grok what this repo offers, why they should care, and where the value lives — with the highest-value contents (Niko, authoring, script-it, shell) positioned front-and-center.

## Deliverables

1. **Rewrite root `README.md`** as a tight sales pitch:
    - Open with why this repo exists / what a reader gets (canonical agent customizations that compose).
    - Present the four rulesets front-and-center with short value props and links to their READMEs:
        - **Niko** — senior-dev workflows + on-disk memory bank; work survives beyond a single context window.
        - **authoring** — how to write prompts, markdown, architecture docs, and diagrams that agents and humans both honor.
        - **script-it** — stop paying inference cost for mechanical tool-call loops; tripwire rule + how-to skill.
        - **shell** — style and TDD guidance for bash/POSIX scripts.
    - Keep install guidance (ai-rizz / a16n / client-side-mdc-render), Structure, Checks, and Big Thanks sections — refreshed where wording is stale (e.g., "rules"-only terminology after the skills migration).
    - **NOT** a full index of every rule/skill — ruleset READMEs own the catalogs.
2. **Create `rulesets/script-it/README.md`** in the same style as the authoring/shell ruleset READMEs:
    - Short intro to the ruleset's purpose.
    - Purpose/scope entries for `script-it-instead` (always-apply tripwire rule) and `how-to-script-it-instead` (the batch-scripting skill).

## Constraints

- Edit canonical sources only (root `README.md`, `rulesets/script-it/README.md`); never generated `.cursor/` / `.claude/` trees.
- Root README stays pitch, not catalog.
- `make test` must stay green: every internal link in `rulesets/**/README*` must resolve on disk (the new script-it README enters CI's link-check scope the moment it exists).
- Prose follows `rules/markdown-style.mdc` (no hard wrapping, clean headings, proper fence nesting).

## Acceptance Criteria

1. Root README leads with value: a reader understands what and why within the first screen.
2. All four rulesets are linked with accurate one-to-two-sentence value props.
3. `rulesets/script-it/README.md` exists, matches sibling README conventions, and its links resolve.
4. `make test` passes.
