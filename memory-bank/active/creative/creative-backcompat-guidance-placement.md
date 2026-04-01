# Architecture Decision: Backwards Compatibility Guidance Placement

## Requirements & Constraints

**Functional requirement**: Guidance must reliably suppress the agent's default conservative bias around backwards compatibility — specifically five beliefs: (1) compatibility is not a default obligation, (2) public interface identification is a prerequisite to compatibility analysis, (3) internal implementation is always free to change, (4) pre-release software has no compatibility obligation, (5) compatibility should not be used to avoid improvements.

**Quality attributes (ranked)**:
1. **Activation reliability** — must fire at the moment of decision, without requiring the agent to self-detect its bias
2. **Token economy** — cost proportional to frequency
3. **Stylistic fit** — match host location density and tone
4. **Maintainability** — minimal new infrastructure

**Technical constraints**: Always-on rules consume context every interaction. Skills require explicit invocation. Canonical rule sources live in `rules/` (synced by ai-rizz).

## Options Evaluated

- **Option A — Inline in `niko-core.mdc`**: Principle statement in Core Persona & Approach + operationalizing bullet in Research & Planning. ~8-10 lines total.
- **Option B — Standalone always-on rule**: New `rules/no-backcompat-bias.mdc` with `alwaysApply: true`. ~15-20 lines, comparable to `script-it-instead.mdc`.
- **Option C — Standalone skill**: On-demand skill, agent invokes when considering backwards compatibility.
- **Option D — Activator + skill**: Lightweight always-on activator + heavier skill for progressive disclosure.

## Analysis — Options A–D (Mechanism Type)

| Criterion | A: Inline | B: Standalone always-on | C: Skill | D: Activator + skill |
|---|---|---|---|---|
| Activation reliability | Excellent | Excellent | Poor — requires self-detection of bias | Mixed — activator fires but skill follow-through uncertain |
| Token economy | Best — marginal cost in already-loaded file | Good — new always-on overhead | Best when unused | Moderate |
| Stylistic fit | Excellent — "Be disagreeable" precedent | Good — `script-it-instead` precedent | Poor | Moderate — untested pattern |
| Maintenance | Best — no new files | Moderate — one file | Moderate — one file | Poor — two files |
| Proportionality | Excellent | Moderate | Poor | Poor |

Key insights:

- **Options C and D are eliminated** on activation reliability: C requires the agent to recognize its own bias (the exact thing it can't do), and D's progressive-disclosure model adds complexity without improving on A or B's activation guarantee. The pattern D is based on (`script-it-instead`) is also self-described as "relatively untested."
- **A vs. B**: Both provide guaranteed activation. A wins on precedent fit ("Be disagreeable" is the same kind of guidance), token economy (~8% marginal increase vs. a whole new file), and coherence (textual proximity with "Dependency & Impact Analysis" where the bias manifests). B's precedent (`script-it-instead`) is for detection-pattern + procedural-fix problems, which is a different shape.

## Analysis — Niko Workflow Phase Locations

The bias manifests when the agent is *scoping or implementing changes* — deciding what constraints apply, what interfaces to preserve, and how freely to restructure. The Niko workflow has procedural phases where these decisions happen. Each was evaluated as a potential home for compatibility surface awareness guidance.

### L3-plan, Step 3: Component Analysis

**Existing content**: L3-plan already contains a "Boundary Changes" bullet: *"Will this feature change any component's public interface, API contract, or data schema? Flag these — they have higher blast radius and may need creative phase exploration."*

**Fit assessment**: This is the closest natural hook. It already asks about public interfaces. However, it frames boundary changes purely as a risk flag without the corrective ("only these carry compatibility weight; internal changes are unconstrained"). As written, it could reinforce the bias by training the agent to treat boundary-adjacent changes as inherently dangerous.

**Problems**: (1) Only runs on L3+ tasks — L1 and L2 tasks never see this. (2) The guidance would need duplication into L2-plan, which lacks a boundary analysis step. (3) L1 has no planning phase at all.

**Verdict**: Natural amplification point for a future complementary enhancement, but cannot serve as the primary home.

### L2-plan, Step 4: Review Codebase Structure

**Existing content**: Identifies files, functions, and modules to be touched. Cross-references against systemPatterns.md for convention alignment. No explicit interface or boundary analysis.

**Fit assessment**: The bias could manifest here when the agent implicitly adds "maintain backwards compatibility" as a constraint while reviewing the codebase. But there's no structural hook for compatibility surface analysis, and adding one would be disproportionate for L2's "Simple Enhancement" design intent.

**Verdict**: Poor fit — no existing hook, and adding one is scope creep for L2.

### Preflight, Steps 2.3–2.4: Dependency Impact / Conflict Detection

**Existing content**: "Flag any proposed changes that would break existing contracts or interfaces."

**Fit assessment**: This is a validation phase — it checks the plan after it's been written. By the time preflight runs, the bias has already shaped the plan's scope and constraints. Preflight could catch a false positive ("this plan says it breaks an interface, but that interface is internal"), but it's treating the symptom (a plan that's too conservative) rather than the cause (the agent's reasoning during planning). Also only runs on L2+.

**Verdict**: Too late in the pipeline. Validation catches symptoms, not causes.

### QA, YAGNI / Regression Checks

**Existing content**: YAGNI says "prune speculative code, 'just-in-case' variables." Regression says "confirm no existing architectural patterns were broken."

**Fit assessment**: QA could theoretically catch unnecessary compatibility shims under YAGNI. But QA runs *after implementation* — the wasted effort has already been spent. And the QA reviewer would need to independently recognize that a compatibility shim is speculative, which is the same recognition problem that eliminates Option C.

**Verdict**: Worst fit — latest possible intervention point, relies on the same self-detection that fails for skills.

### L1

**Existing content**: Goes directly from Niko to Build. No planning, preflight, or QA phases.

**Verdict**: No procedural phase exists. The bias manifests just as readily on L1 tasks, and there is nowhere to put guidance.

### Phase Location Summary

The Niko workflow phases are either **too narrow** (L3-only), **too late** (preflight validates after the bias shapes the plan; QA catches after implementation), **missing a hook** (L2-plan), or **nonexistent** (L1). The bias manifests during scoping and implementation across all complexity levels, and also outside of Niko workflows entirely (ad-hoc conversations, non-Niko work). The core (`niko-core.mdc`) is the only document that covers all of these scenarios.

**Future consideration**: L3-plan's "Boundary Changes" bullet could be sharpened as a complementary enhancement someday (adding "only public interface changes carry compatibility weight" to the existing risk-flagging language). This is a low-priority, separate concern — not part of this task.

## Decision

**Selected**: Option A — Inline in `niko-core.mdc`

**Rationale**: The backwards compatibility bias manifests across all complexity levels (L1–L4), outside of Niko workflows, and during both scoping and implementation. The Niko workflow phases were evaluated as procedural integration points (plan, preflight, QA), but each is either too narrow in scope (L3-only), too late in the pipeline (post-plan or post-implementation), or nonexistent for lower complexity levels (L1 has no planning phase). The core is the only always-on, always-present document that reaches the agent at the moment of decision regardless of context. Inline placement matches the "Be disagreeable" precedent, provides the best activation reliability and token economy, and sits in natural textual proximity with the guidance it modifies.

**Tradeoff**: `niko-core.mdc` grows by ~8-10 lines (104 → ~114). Acceptable for high-value guidance in the system's most important always-on rule.

## Implementation Notes

### Placement 1: Core Persona & Approach

After the "Be disagreeable" paragraph. Establishes the principle as a companion bias correction:

```markdown
**Backwards compatibility is not a default obligation.** Do not preserve existing interfaces, code shapes, or behaviors out of mere existence. Compatibility is a constraint only when explicitly required by the operator, project documentation, or identified external consumers of a public interface. Pre-release software (unreleased, semver 0.x.x, initial buildout) has no prior contract to honor. Internal implementation details — private APIs, internal module structure, non-exported code — are never subject to compatibility concerns regardless of release status.
```

### Placement 2: Research & Planning

New bullet after "Dependency & Impact Analysis". Operationalizes the principle:

```markdown
- **Public Interface Identification**: Before assessing whether a change "breaks" something, first determine what the *public interface* actually is. Only contractual surfaces (exported APIs, published schemas, documented CLI interfaces, `action.yml` definitions) carry compatibility weight. Internal implementation can always be restructured freely if the public interface is unchanged. Do not let compatibility concerns inhibit improvements to non-public code.
```

### Canonical edit target

`rules/niko-core.mdc` (synced to `.cursor/rules/shared/niko-core.mdc` by ai-rizz).
