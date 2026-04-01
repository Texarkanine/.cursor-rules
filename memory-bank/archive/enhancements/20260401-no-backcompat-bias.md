---
task_id: no-backcompat-bias
complexity_level: 2
date: 2026-04-01
status: completed
---

# TASK ARCHIVE: Add Backwards Compatibility Guidance to Niko System

## SUMMARY

Added explicit backwards compatibility guidance to the Niko system to correct the AI agent bias of treating backwards compatibility as an implicit requirement. The change anchors a clean-break default in `niko-core.mdc`, operationalizes it in Research & Planning, and sharpens preflight's conflict detection to focus on public contracts and published interfaces.

## REQUIREMENTS

- Establish a core principle in the Core Persona & Approach section that backwards compatibility is not a default obligation.
- Add Research & Planning guidance requiring explicit identification of the public interface before evaluating whether a change "breaks" something.
- (Dropped) Sharpen the L3-plan "Boundary Changes" bullet to clarify that internal implementation changes are not boundary changes.
- Sharpen preflight "Conflict Detection" language to scope conflicts to public contracts and published interfaces.

## IMPLEMENTATION

### Core Persona & Approach (`rulesets/niko/niko-core.mdc`)

- Integrated backwards compatibility guidance directly into the main Core Persona paragraph:
  - Final wording: `Default to clean-break changes. Backwards compatibility is a factor to weigh in light of the public interface and its consumers - not an implicit requirement.`
  - Placement: after the bold autonomy sentence (`Prioritize proactive execution...`) and before the temperance/scope-limiter pair (`Not every interaction requires code changes...` / `When code changes are needed...`).
- Kept `Be disagreeable when necessary` as a standalone bolded coda paragraph to preserve its role as the section's closing posture directive.

### Research & Planning (`rulesets/niko/niko-core.mdc`)

- Added a new bullet after `Dependency & Impact Analysis`:
  - `Public Interface Identification`: requires explicitly identifying what the public interface actually is before deciding whether a change is a "break."
  - Clarifies that internal implementation, private APIs, and non-contractual shapes are never subject to compatibility constraints.
  - Notes that pre-release (`0.x.x`), unreleased code, and initial buildouts have no prior contract to honor — backwards compatibility is inapplicable, not just unnecessary.

### Preflight (`rulesets/niko/skills/niko-preflight/SKILL.md`)

- Sharpened the Step 2 "Conflict Detection" bullet:
  - From: `Flag any proposed changes that would break existing contracts or interfaces`
  - To: `Flag any proposed changes that would break public contracts or published interfaces — internal restructuring that preserves the public API surface is not a conflict`
- Ensures preflight focuses on real compatibility contracts rather than internal refactors.

### Dropped Scope

- L3-plan "Boundary Changes" sharpening was intentionally dropped after creative and planning phases:
  - Existing L3-plan text already scopes to "public interface, API contract, or data schema" and includes the word "public."
  - With the new core principle and R&P bullet in place, further sharpening would be redundant; treated as a potential future enhancement rather than part of this task.

## TESTING

- **Planned behaviors (from `memory-bank/active/tasks.md`):**
  - B1: Core Persona section contains backwards compatibility guidance in the intended location and tone.
  - B2: Research & Planning section contains a "Public Interface Identification" bullet after "Dependency & Impact Analysis."
  - B3: Preflight "Conflict Detection" scopes conflicts to public/published surfaces.
- **Verification approach:**
  - Manual inspection of the edited files (`niko-core.mdc`, `niko-preflight` SKILL) to ensure:
    - Content matches the finalized wording and placement decisions.
    - Tone and density remain consistent with surrounding text.
  - Operator-led QA conversation:
    - Iterated on Core Persona wording and placement until it matched the intended posture and scope.
    - Confirmed that R&P and preflight changes correctly operationalize the new principle without unnecessary duplication.
- **Outcome:**
  - All three planned behaviors (B1–B3) are satisfied in the final state.
  - QA validation marked `PASS` in `memory-bank/active/.qa-validation-status` after operator review.

## LESSONS LEARNED

- **Content classification before placement:** The Core Persona paragraph has an implicit two-part structure:
  - Sentences 1–6: posture (how to operate when acting).
  - Sentences 7–8: scope limiters (when to not act or act via conversation only).
  - New statements must be classified as posture vs. scope-limiter before choosing a placement; otherwise, they can be given the wrong apparent scope.
- **Backcompat as posture, not footnote:** Backwards compatibility guidance is a posture statement that governs planning, scoping, and architecture, not just code changes. It belongs with other posture statements, not tacked onto "when code changes are needed" where it would read as a narrow coding guideline.

## PROCESS IMPROVEMENTS

- **Semantic over purely rhetorical reasoning:** When multiple placements are rhetorically defensible (e.g., end of paragraph vs. mid-paragraph), prioritize semantic reasoning:
  - Ask: what kind of statement is this? What scope does each candidate context imply?
  - Commit to the semantically correct option and defend it, rather than oscillating between options that merely "sound good."
- **Plan specificity for textual changes:** For text-heavy tasks, plans should specify not just "before X" or "after Y" at the section level, but also the intended role of the new text (inline calibration vs. standalone directive) and its relationship to neighboring sentences.

## TECHNICAL IMPROVEMENTS

- The Niko core guidance is now more explicit about when backwards compatibility matters and when it does not, which should reduce conservative bias in future agents.
- The combination of:
  - Core Persona posture,
  - R&P "Public Interface Identification,"
  - and preflight "Conflict Detection" sharpening
  creates a coherent pipeline: decide *how* to think (core), *what* is in scope (R&P), and *where* conflicts really live (preflight).

## NEXT STEPS

- Optionally update the project brief or create a follow-on task if you want to revisit L3-plan "Boundary Changes" sharpening as a separate enhancement.
- Otherwise, no further work is required for this task; the memory bank has been archived and the guidance is in place.

