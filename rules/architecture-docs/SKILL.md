---
name: architecture-docs
description: How to write project architecture documentation as portable principles — genre framing, inclusion bars, orientation diagrams, invariants, and change-surface routing. Use when writing or improving architecture docs, systems atlases, or design-surface explanations (not memory-bank briefings or product how-tos).
---

# Architecture Documentation

Write architecture docs so a reader can load the system's design surface and change it without removing a fence they did not see. Prefer principles over outlines to copy. Recipes appear only as illustrations of a stated principle.

## Genre and Evidence

**This skill is for project architecture docs** — the human-facing systems atlas / design surface (often under `docs/architecture` or a developer-guide Architecture page).

It is **not** for:

- Memory-bank persistent briefings (`systemPatterns.md`, `techContext.md`) — those are implementation-orientation files with their own altitude and update rules
- Product how-to, contributor day-to-day loops, or escape-hatch CLI recipes — those belong in user/contributor/advanced guides
- Agent-only compact system models that ship with a plugin — link them; do not fork them into the atlas

When architecture docs and memory-bank files both exist, they may share themes. Keep genres distinct: audience pointers beat pasted Avoid-blocks or a forced single SSOT.

**Evidence weight when deriving or applying judgment:** primary local architecture docs ≥ Niko-adjacent memory-bank templates > secondary domain-mapping docs (e.g. conversion taxonomies) > tertiary FOSS architecture pages. When sources conflict, prefer local recoverable why. FOSS enlarges the sample; it does not redefine "good."

This skill is a **reference**: hold the principles while you write. It is not a step-by-step authoring workflow.

## Frame the Genre Before the Outline

**Principle:** Open by stating what this document is for and what neighboring doc genres own — before listing pieces or drawing diagrams.

**Why:** Without a genre frame, Architecture becomes a second user guide, a second `systemPatterns`, or an unbounded dump. Readers (and agents) need the ownership boundary first so inclusion decisions have somewhere to land.

**Not this:** Jumping straight into a piece inventory or copying another project's section list with no "what this is / is not."

Evidence: `local`, `niko-adj`, `a16n`

## Apply an Inclusion Bar

**Principle:** Include a topic only if it helps load the whole-system model, marks an unusual constraint that looks removable (a Chesterton's fence), or is unsafe to change without knowing it. Omit ordinary facts, procedure recipes, and subsystem deep-dives that only matter inside one corner.

**Why:** Completeness without a bar produces either a thin seed list or a second briefing dump. The bar keeps the atlas coherent and short enough to stay true.

**Not this:** Mirroring memory-bank pattern catalogs into Architecture, or treating a brainstorm seed list as the entire outline with no inclusion test.

Evidence: `local`, `niko-adj`

## Lead with What Is; Explain Why for Fences

**Principle:** State what the system *is* first. Add *why* only where the design is unusual enough that a newcomer might "simplify" it away — or where the consequence of ignorance is damage.

**Why:** Design-diary voice ages badly and hides the model under history. Fence explanations are load-bearing: they prevent Chesterton's-fence removals.

**Not this:** Chronological design narrative as the spine, or unexplained magic with no hint that a constraint is intentional.

Evidence: `local` (FOSS constraint writeups corroborate)

## Orient with a Diagram That Loads the Model

**Principle:** Near the start, give a diagram that places the major pieces (and, when relevant, actors and flows) so a reader can navigate the rest of the atlas. Choose the *kind* of diagram for the load-bearing story of *this* system — control flow, stack anatomy, desired-state vs generated-state, or another shape that actually orients.

**Why:** Architecture is spatial. A well-chosen orientation diagram is a map, not decoration. Mandating one diagram type teaches mimicry: a control-flow opener is right when shared entrypoints and callers are the story; a stack anatomy is right when layer/API ownership is the story.

**Not this:** "Always open with a control-flow Mermaid flowchart," or a diagram that only restates the piece list without relationships.

Evidence: `local` (FOSS bird's-eye / anatomy diagrams corroborate choice-of-kind, not a mandated type)

## Name Invariants and Load-Bearing Boundaries

**Principle:** Call out deliberate absences, API or ownership boundaries, and contracts that look optional but are not — as named invariants or doctrines, not buried asides.

**Why:** The dangerous parts of a system are often what is *not* there (no fallback path, no migrate-on-UI-open, no truncation at rest) or where rules change (desired state vs generated output). Naming them makes the fence visible.

**Not this:** Implying every module is equally special, or documenting only happy-path structure while leaving "never do X" unstated.

Evidence: `local`, `foss`

## Route Change Surfaces

**Principle:** Help a changer find which page or section owns a class of edits — a short routing table or "when you change X, read Y" guidance on the overview.

**Why:** An atlas that cannot answer "where do I look before I touch this?" fails its job the moment someone modifies the system.

**Not this:** An overview that only markets the topic pages as optional appendices, with no change-oriented entry path.

Evidence: `local`

## Keep Procedures Outbound

**Principle:** Architecture owns the model (what/why-of-fences). Install steps, heal recipes, Make loops, and CLI flag tables live in how-to guides, with outbound links from Architecture — not recopied as the body of the atlas.

**Why:** Procedure dumps drift and blur ownership. A single named model target lets every how-to point at the fence instead of re-explaining it.

**Not this:** Turning Architecture into Contributing 2.0 or pasting troubleshooting runbooks into doctrine pages.

Evidence: `local`

## Allow Audience-Split Overlap; Forbid Silent Forks

**Principle:** Related briefings (maintainer memory-bank files, agent compact system models) may intentionally overlap Architecture on the same themes. Point at them by audience; do not paste their Avoid/update blocks into Architecture, and do not force one merged SSOT that serves every audience badly.

**Why:** Humans, agents, and in-checkout maintainers need different altitudes of the same truths. Silent forks drift; forced merges either bloat the atlas or starve a briefing.

**Not this:** Instructing an agent to edit `systemPatterns.md` / `techContext.md` when the ask was for project architecture docs, or copying memory-bank templates wholesale into `docs/architecture`.

Evidence: `local`, `niko-adj`

## Cluster at Atlas Grain

**Principle:** Split pages or major sections by how the system is changed or understood (e.g. how code arrives and runs vs when work fires vs the data plane) — not one page per noun. Keep tightly coupled contracts on the same page as deep-linkable sections.

**Why:** Fine-grained atomization creates "is this Packaging or Shim?" link thrash. Coarse single-page dumps hide change surfaces. Atlas grain matches how maintainers navigate.

**Not this:** A dozen micro-pages for every buzzword, or one undifferentiated mega-file with no thematic contracts.

Evidence: `local`

## Prefer Durable, Brief Stewardship

**Principle:** Prefer pointers to sources of truth that can change (config files, lockfiles, linked guides) over copying values that will rot. After creation, treat length as a liability: update when factually wrong or materially incomplete — do not append every task's residue.

**Why:** Architecture that accumulates stale specifics stops being trusted. Brevity is a product of inclusion discipline and update discipline together.

**Not this:** Cataloging every dependency version in prose, or treating every completed feature as a new Architecture section.

Evidence: `niko-adj`

## Domain-Mapping Sibling

Some projects need a **domain mental model** (shared concept taxonomy, lossiness, honesty boundaries across tools) more than a systems atlas. That is a sibling genre: lead with the product goal, partition outcomes (clean / approximate / refuse), and write boundary essays when mechanical translation is the wrong problem. Do not force atlas machinery onto that job — and do not treat a taxonomy guide as a substitute for a systems atlas when the ask is "how do the pieces fit and which fences must stay."

Evidence: `a16n`
