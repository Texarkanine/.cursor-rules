# Research Notes: architecture-docs-authoring-skill

Evidence → observed practices → candidate principles. Local wins on conflict. FOSS is tertiary.

## Corpora examined

| Weight | Corpus | Primary evidence |
| --- | --- | --- |
| Primary | stockroom `docs/architecture/*` | Shipped pages + archive `20260714-architecture-docs.md` + sessions `2de2cdd1…`, `c8592ca6…` (sr-query full text) |
| Primary | ai-rizz `docs/developer-guide/architecture.md` | Shipped page + archive `20260509-ai-rizz-properdocs…` + git `0199d9d` |
| Adjacent | Niko `systemPatterns.mdc` / `techContext.mdc` | Templates + archive `20260709-persistent-file-update-contract.md` |
| Secondary | a16n `understanding-conversions/*` | Shipped pages + observed-practices brief (session research) |
| Tertiary | rust-analyzer `docs/book/src/contributing/architecture.md` | Raw content + GitHub commit list |
| Tertiary | Flutter `docs/about/The-Engine-architecture.md` | Raw content + GitHub commit list |

Semantic search (post-embed fix) recovered authoring intent for stockroom Architecture and Niko persistent-file stewardship; a16n practice inventory; weaker direct hits for ai-rizz architecture *authoring* (git/archive carry that load).

---

## Observed practices (high confidence)

### Stockroom Architecture (primary)

1. **Genre frame on the index** — Opening states what Architecture is (systems atlas / design surface) and what it is *not* (User Guide, Contributing, Advanced).
2. **Inclusion bar** — Creative decision C: include if on the control-flow map, OR unusual Chesterton-fence constraint, OR unsafe to change without knowing. Explicitly rejected mirroring `systemPatterns` and seed-only thin pages.
3. **WHAT-first; WHY for fences** — Operator/intent: lead with what is; why only where design invites mistaken removal; constraints not design diary.
4. **Whole-system orientation diagram** — Index opens with Mermaid placing actors → shim → engine → warehouse/embeddings/dashboard. Post-reflect expanded subgraphs for clarity. Chosen because *callers share one entrypoint contract* is the load-bearing story — not because “architecture docs open with control-flow.”
5. **Change-surfaces table** — “If you change X → read page Y” on the index (preflight advisory → adopted).
6. **Related procedures footers** — Outbound links to UG/Contributing/Advanced; Architecture does not re-own recipes.
7. **Audience-split overlap** — Human Architecture, agent `system-model.md`, and `systemPatterns.md` may overlap on packaging/torch/truncation/identity; managed by audience pointers, not forced single SSOT or forking.
8. **Thematic clusters** — Packaging (how code arrives/runs), Lifecycle (when things fire), Warehouse/Embeddings (data plane). Shim/heal stay deep links on Packaging (not own pages / not index doctrines).
9. **Named doctrines / contracts** — e.g. no truncation at rest, RO by construction, baked-only shim, heal-is-not-ingest.

### ai-rizz Architecture (primary)

10. **Mental model in three bullets before diagrams** — manifests mutate; sync rebuilds; cache is implementation detail.
11. **Cross-cutting page + sibling deep pages** — Architecture owns flow; schema/cache/modes live elsewhere with inline links.
12. **Diagram type matches job** — system-shape graph, command sequenceDiagram, sync decision graph — different purposes.
13. **Development Boundaries** — names the load-bearing boundary (desired vs generated state) and the touch-list when extending.

### Niko templates (adjacent)

14. **Briefing altitude** — “How This System Works” / tech orientation; not subsystem design docs.
15. **Avoid lists** — obvious, ordinary, temporal, subsystem deep-dives (altitude test: would damage elsewhere?).
16. **Invalidation-only updates** — value ∝ 1/length; update only when factually wrong or materially incomplete; surgical fixes.
17. **Durable pointers over drift-prone values** — techContext prefers “configured in X” over copying versions.

### a16n Understanding Conversions (secondary)

18. **Domain mental model, not systems atlas** — taxonomy of customization kinds; clean / approximated / skipped; structural vs non-invertible.
19. **Honesty-boundary essays** — hooks.md refuses conversion and argues category error; not a missing feature list.
20. **Tables over Mermaid for cross-tool mapping**; Mermaid reserved for thin pipeline overviews in package docs.
21. **Published docs ≠ maintainer “don’t break this”** — that altitude lives in memory-bank for a16n.

### rust-analyzer (tertiary)

22. **Onboarding frame** — familiarize with codebase; bird’s-eye then entry points then code map.
23. **Architecture Invariant callouts** — deliberate absences and non-obvious constraints called out as named invariants.
24. **API Boundary labels** — rules differ at boundaries; link out to deeper essays without absorbing them.

### Flutter engine (tertiary)

25. **Anatomy + ownership** — stack layers with who owns each piece and which API boundary sits between them.
26. **Constraint pages with consequences** — threading rules tied to jank, watchdogs, assertion failures — why the fence exists.

---

## Conflicts & resolutions

| Conflict | Resolution |
| --- | --- |
| Stockroom atlas vs a16n taxonomy-as-architecture | Different genres; skill teaches systems-atlas principles as primary; notes domain-mapping as adjacent genre, not a substitute atlas |
| RA/Flutter deep crate/thread inventories vs local inclusion bar | FOSS depth corroborates “name fences”; does not license dumping every module into project Architecture |
| “Open with control-flow Mermaid” surface mimicry vs stockroom’s actual why | Principle is orientation diagram that loads the model; stockroom’s control-flow is one successful manifestation |
| Forced SSOT across Architecture / system-model / systemPatterns vs observed overlap | Prefer audience pointers + deliberate overlap over merge or fork |

---

## Candidate principle inventory (for skill)

Portable principles with recoverable why. Evidence tags: `local` | `niko-adj` | `a16n` | `foss`.

1. **Frame the genre before the outline** — Say what this doc is for and what neighboring genres own. (`local`, `niko-adj`, `a16n`)
2. **Apply an inclusion bar** — Keep what loads the system model or is unsafe to change blind; omit procedure dumps and ordinary facts. (`local`, `niko-adj`)
3. **WHAT-first; WHY for Chesterton’s fences** — Explain motive where removal would look “obviously wrong” to a newcomer. (`local`; `foss` corroborates)
4. **Orient with a diagram that loads the whole model** — Choose diagram *kind* for the load-bearing story; do not mandate a type. (`local`; `foss` bird’s-eye/anatomy corroborates)
5. **Name invariants and load-bearing boundaries** — Deliberate absences, API/desired-vs-generated boundaries, contracts. (`local`, `foss`, ai-rizz)
6. **Route change surfaces** — Help a changer find the owning page/section. (`local`, ai-rizz)
7. **Keep procedures outbound** — Model here; recipes elsewhere with links. (`local`)
8. **Allow audience-split overlap; forbid silent forks** — Related briefings may share themes with pointers; don’t paste Avoid-blocks or merge genres. (`local`, `niko-adj`)
9. **Cluster at atlas grain** — Sections/pages by how the system is changed, not one page per noun. (`local`)
10. **Prefer durable, brief stewardship** — Pointers over copy-paste values; don’t accumulate task residue. (`niko-adj`)

Dropped (surface-only / non-portable): “always five pages,” “always Mermaid flowchart TB,” “always warning-code tables,” wry tone from hooks.md.
