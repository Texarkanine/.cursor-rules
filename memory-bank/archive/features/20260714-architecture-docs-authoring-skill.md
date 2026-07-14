---
task_id: architecture-docs-authoring-skill
complexity_level: 3
date: 2026-07-14
status: completed
---

# TASK ARCHIVE: Architecture Docs Authoring Skill

## SUMMARY

Delivered a principle-first Cursor skill (`rules/architecture-docs/SKILL.md`) wired into the `authoring` ruleset that teaches how to write project architecture documentation. Principles were reverse-engineered from primary local goldens (stockroom Architecture atlas, ai-rizz Architecture), adjacent Niko memory-bank templates (`systemPatterns.mdc`, `techContext.mdc`), secondary a16n conversion mental-model docs, and tertiary FOSS supplements (rust-analyzer, Flutter engine) — researched via stockroom history and git/PR archaeology, not surface recipe mimicry.

Post-reflect polish made the shipped skill Niko-agnostic (no memory-bank / `systemPatterns` / `techContext` vocabulary) and compressed genre/outbound prose with Diátaxis + Chesterton's fence decompression keys (~130→82 lines). Packaging matches `prompt-authoring` (directory symlink into `rulesets/authoring/skills/`). QA passed; sibling architecture trees and Niko mdc templates were not modified.

## REQUIREMENTS

From the project brief:

1. Deliver a Cursor **skill** (canonical under `rules/`) on writing good architecture documentation.
2. Content must be **principle-first**: reverse-engineer *why* practices worked in goldens; do not ship surface prescriptions (e.g. not “open with a control-flow diagram”).
3. **Evidence hierarchy:** primary local goldens (stockroom, ai-rizz) ≥ adjacent Niko templates > secondary a16n > tertiary FOSS (rust-analyzer, Flutter engine only). Local wins on conflict.
4. Research locals/adjacent via stockroom + git; FOSS via git/PR surface only.
5. Keep genres distinct: project architecture docs vs memory-bank persistent files vs how-tos; do not rewrite sibling repos or Niko templates.
6. Acceptance: skill exists and is discoverable; principles portable; anti-recipe; FOSS weighting explicit in research trail; ephemeral memory bank tracks derivation through the workflow.

All requirements were met. Additive clarification only: **Domain-Mapping Sibling** section for a16n’s taxonomy genre (explicitly not a substitute systems atlas). Post-reflect: installable skill must not require Niko vocabulary.

## IMPLEMENTATION

### Deliverables

| Path | Role |
|------|------|
| `rules/architecture-docs/SKILL.md` | Canonical skill (Diátaxis explanation + Chesterton's fence; flat principles with Not-this anti-patterns) |
| `rulesets/authoring/skills/architecture-docs` | Directory symlink → `../../../rules/architecture-docs` |
| `rulesets/authoring/README.md` | Ruleset entry documenting purpose + scope (Niko-agnostic) |

REUSE: existing `rules/**/*.md` PPL-S annotation covers the new skill; no `REUSE.toml` edit required.

### Research corpus (inlined from research notes)

| Weight | Corpus | Primary evidence |
| --- | --- | --- |
| Primary | stockroom `docs/architecture/*` | Shipped pages + archive + warehouse sessions (sr-query) |
| Primary | ai-rizz `docs/developer-guide/architecture.md` | Shipped page + archive + git |
| Adjacent | Niko `systemPatterns.mdc` / `techContext.mdc` | Templates + persistent-file-update-contract archive |
| Secondary | a16n `understanding-conversions/*` | Shipped pages + practice inventory |
| Tertiary | rust-analyzer contributing architecture | Raw content + GitHub commits |
| Tertiary | Flutter engine architecture | Raw content + GitHub commits |

Key recovered practice → principle moves: stockroom’s control-flow opener is justified by a shared entrypoint contract (encode diagram *kind* for load-bearing story, not Mermaid type); a16n taxonomy is a sibling genre to systems atlases; Niko Avoid/When-to-Update rules are portable stewardship principles without being the same deliverable genre.

### Candidate principles synthesized (ten + sibling note)

1. Frame the genre before the outline  
2. Apply an inclusion bar  
3. WHAT-first; WHY for Chesterton’s fences  
4. Orient with a diagram that loads the whole model  
5. Name invariants and load-bearing boundaries  
6. Route change surfaces  
7. Keep procedures outbound  
8. Allow audience-split overlap; forbid silent forks  
9. Cluster at atlas grain  
10. Prefer durable, brief stewardship  

Plus Domain-Mapping Sibling for taxonomy / honesty-boundary docs. Dropped surface-only observations (always five pages, always flowchart TB, etc.).

### Creative decision (inlined)

**Selected:** Framed principle + anti-pattern reference (option B).

**Options considered:** (A) pure principle list; (B) principle + anti-pattern; (C) principle + narrative case studies; (D) workflow-led composite.

**Rationale:** Maximizes anti-recipe and portability while staying a composable reference per prompt-authoring. Genre/evidence frame handles adjacency and FOSS weighting without absorbing Niko templates. Case-study depth stays in research artifacts, not the skill body. Optional one-line evidence tags; no workflow spine.

**Tradeoff accepted:** Agents lose rich in-skill stories; prefer transfer and anti-mimicry. Single principle-level “for example” lines allowed; never a project outline to copy.

### Post-reflect polish

1. **Niko-agnostic surface** — Genres expressed as how-tos, maintainer orientation notes, agent compact models; research notes may still name Niko as derivation source.
2. **Decompression keys** ([daz.is/blog/decompression-keys](https://daz.is/blog/decompression-keys/)) — Diátaxis (explanation) + Chesterton's fence compress genre/outbound/fence prose. Rejected C4 (recipe risk), arc42 (template mimicry), overloaded YAGNI/SSOT/SoC. Novel principles (change surfaces, atlas grain, diagram-*kind*) stay explicit.

### Preflight correction

Initial plan assumed file hardlinks; repo standard is **directory symlink** into `rulesets/authoring/skills/` (as `prompt-authoring`). Amended before build.

## TESTING

No automated test runner for skill prose in this repo. Verification:

### Preflight — PASS

Validated packaging pattern, REUSE coverage, and TDD encoding via checklist-as-test before authoring. Status file: `.preflight-status` = PASS.

### Build verification — PASS

Acceptance checklist (`architecture-docs-acceptance.md`) exercised against shipped `SKILL.md`:

- Structure: frontmatter, genre frame (Niko-free), prefer-local-why note, reference shape, principle → why → Not-this
- All ten principles present; Domain-Mapping Sibling retained
- Anti-recipe: no “always open with control-flow” except under Not-this
- Packaging: `readlink` symlink, README entry, REUSE coverage, sibling/Niko templates untouched

### QA — PASS

Semantic review against plan, creative pedagogy, projectbrief acceptance criteria, and packaging invariants. One trivial portability fix: stockroom-specific “Heal” how-to phrasing → generic named-model-target language under Procedures Outbound. Status file: `.qa-validation-status` = PASS. No substantive FAIL.

## LESSONS LEARNED

### Technical

- Encode diagram *justification* (load-bearing story → diagram kind), not diagram *type*. Stockroom’s control-flow opener is one successful manifestation of orientation, not a universal opener rule.
- Domain-mapping docs and systems atlases are sibling genres; treating taxonomy guides as Architecture goldens of the atlas kind teaches the wrong structure.
- Decompression keys replace *framework spelling*, not project-specific novel principles — change-surface / atlas-grain / diagram-kind remain worth stating explicitly.
- Principle-level fence examples stay portable; noun-level how-to names (“Heal”) are the portability trap.

### Process

- For prose skills with no unit runner, checklist-as-test before authoring is an effective TDD stand-in.
- When research depends on stockroom semantic recall of recently authored docs, confirm embeddings are current before treating weak hits as absence of intent.
- Preflight packaging correction (symlink vs hardlink) prevented an embarrassing QA miss.
- Creative’s anti-recipe mandate was the highest-value gate against the pre-mortem’s “ship a stockroom outline guide” failure mode.

## PROCESS IMPROVEMENTS

- Treat checklist-as-test as the default TDD encoding for rules/skills prose deliverables in this repo.
- For stockroom-dependent authoring-why research, bake an “embeddings current?” probe into the research step before concluding thin intent.
- Keep FOSS selection operator-gated before creative closes when evidence weight depends on which supplements are in-set.

## TECHNICAL IMPROVEMENTS

- Optional follow-up: register `architecture-docs` in any consumer install manifests / skill browsers that list authoring skills explicitly (out of scope for content authoring; same class of follow-up as prior authoring skill work).
- No persistent memory-bank briefing updates were required — adding an authoring skill did not invalidate `productContext` / `systemPatterns` / `techContext` altitude content.

## NEXT STEPS

None required for this task. Memory bank is cleared for the next `/niko` run. Consumers who install the `authoring` ruleset gain the skill after push/merge of this branch.
