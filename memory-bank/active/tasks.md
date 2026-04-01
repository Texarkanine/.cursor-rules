# Task: Add Backwards Compatibility Guidance

* Task ID: no-backcompat-bias
* Complexity: Level 2
* Type: Enhancement (guidance content)

Add guidance correcting the AI agent bias of treating backwards compatibility as an implicit requirement. Two additions to `niko-core.mdc` (Core Persona paragraph + Research & Planning bullet), plus one sharpened bullet in preflight to remove accidental reinforcement of conservatism.


## Test Plan (TDD)

### Behaviors to Verify

- **B1 (Core Persona principle)**: `niko-core.mdc` Core Persona & Approach section contains a "Default to clean-break changes" paragraph placed before "Be disagreeable" (which retains its position as the section's closing coda)
- **B2 (R&P operationalization)**: `niko-core.mdc` Research & Planning section contains a "Public Interface Identification" bullet after "Dependency & Impact Analysis"
- **B3 (Preflight sharpening)**: Preflight "Conflict Detection" step scopes "contracts or interfaces" to public/published surfaces

### Test Infrastructure

- Framework: **None** — operator verification of final text against requirements and tone.


## Implementation Plan

### Step 1: `rules/niko-core.mdc` — Core Persona addition [DONE]

- File: `rules/niko-core.mdc`
- Location: Before the "Be disagreeable when necessary" paragraph (line 12), after the main persona paragraph (line 10). "Be disagreeable" retains its position as the section's closing coda.
- Add new paragraph:

```
**Default to clean-break changes.** Do not treat backwards compatibility as an implicit requirement. Compatibility is a factor to weigh; require it only when explicitly identified by the operator, project documentation, or documented consumers of a public interface.
```

- Behavior: B1

### Step 2: `rules/niko-core.mdc` — Research & Planning addition [DONE]

- File: `rules/niko-core.mdc`
- Location: After the "Dependency & Impact Analysis" bullet (line 25), before "Reusability Mindset" (line 26)
- Add new bullet:

```
- **Public Interface Identification**: Before evaluating whether a change "breaks" something, identify what the *public interface* actually is. Internal implementation, private APIs, and non-contractual code shapes are never subject to compatibility constraints. Pre-release software (`0.x.x`), unreleased code, and initial buildouts have no prior contract to honor — backwards compatibility is *inapplicable*, not merely unnecessary.
```

- Behavior: B2

### Step 3: `rulesets/niko/skills/niko-preflight/SKILL.md` — Sharpen "Conflict Detection" bullet [DONE]

- File: `rulesets/niko/skills/niko-preflight/SKILL.md`
- Location: Step 2 Preflight Workflow, item 4 "Conflict Detection", third sub-bullet (line 39)
- Current text:

```
   - Flag any proposed changes that would break existing contracts or interfaces
```

- Replace with:

```
   - Flag any proposed changes that would break public contracts or published interfaces — internal restructuring that preserves the public API surface is not a conflict
```

- Behavior: B3


## Dropped Steps

- **L3-plan "Boundary changes" sharpening**: Dropped. The existing bullet already scopes to "public interface, API contract, or data schema" — the word "public" is present. With the core principle in place, this will echo correctly without modification.


## Technology Validation

No new technology — validation not required.


## Dependencies

- Steps 1 and 2 both edit `rules/niko-core.mdc` — should be done together
- Step 3 is independent


## Challenges & Mitigations

- **Tone matching**: The Core Persona paragraph must match the density and imperative style of "Be disagreeable." Mitigated by modeling the structure directly on that precedent.
- **Syncing**: Canonical edits to `rules/` and `rulesets/` won't automatically sync to `.cursor/` — that's handled by the `ai-rizz` tool and is not this task's responsibility.


## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight
- [x] Build
- [x] QA
- [x] Reflect
