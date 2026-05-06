# Task: Add `/niko-chat` Ad-Hoc Entrypoint

* Task ID: niko-chat-entrypoint
* Complexity: Level 2
* Type: Simple Enhancement (additive)

Add a new `/niko-chat` ad-hoc entrypoint skill that loads the memory bank's persistent context (and reads ephemeral context if present, without mutating it) so the operator can have free-form, read-only Q&A conversations about the codebase. Document it in the README's "Ad-Hoc Entrypoints" section. While there, add an explicit naming-convention paragraph that codifies the existing-but-undocumented `niko-*` (entrypoints/phases) vs `nk-*` (circuit breakers) split so future contributors don't have to reverse-engineer it.

## Test Plan (TDD)

### Behaviors to Verify

The "behaviors" of a skill file are semantic: when an agent loads `niko-chat/SKILL.md`, it should reliably produce certain conversational behavior. These are validated by preflight (does the plan/skill internally cohere?) and QA (does the implemented skill match the plan and convey the right behavior?). They are not unit-testable in this repo (no test infra exists for skills — established repo pattern).

- B1 (context loading): On invocation, the skill instructs the agent to read all persistent memory bank files (`productContext.md`, `systemPatterns.md`, `techContext.md`) AND any ephemeral files in `memory-bank/active/` if they exist.
- B2 (read-only contract): The skill explicitly forbids mutation — no writes to memory bank, no commits, no workflow kickoff, no edits to source files for the duration of the chat.
- B3 (handoff on real work): If the conversation reveals real work to be done, the skill instructs the agent to recommend `/niko` (or other appropriate entrypoint) rather than silently doing the work.
- B4 (graceful when no memory bank): If `memory-bank/` does not exist or persistent files are missing, the skill instructs the agent to inform the operator and offer to initialize via `/niko` rather than fabricating context.
- B5 (graceful when no ephemeral): If no ephemeral files exist, the skill simply notes "no task currently in flight" and proceeds with persistent-context-only Q&A.
- B6 (frontmatter conformance): SKILL.md has the required `name:` and `description:` frontmatter matching the AgentSkills.io shape used by all sibling skills.
- B7 (README documents the entrypoint): README's "Ad-Hoc Entrypoints" section gains a `/niko-chat` subsection covering the three use-cases (parallel consultation, standalone Q&A, pre-task scoping) and the read-only/no-artifacts non-goal.
- B8 (README documents the convention): README contains an explicit, discoverable paragraph stating the `niko-*` vs `nk-*` naming convention with rationale.

### Edge Cases

- E1: Operator invokes `/niko-chat` with no input → agent should greet, summarize loaded context, and ask what they want to discuss.
- E2: Operator invokes `/niko-chat` with a question → agent should load context first, then answer (don't answer from cold).
- E3: Operator asks chat to "go ahead and do it" mid-conversation → skill must explicitly require a handoff to `/niko`, not capitulate.
- E4: Persistent files exist but ephemeral is in a partial/inconsistent state (e.g., `progress.md` only) → skill should treat this as informational ("looks like a task may be paused") and continue read-only.

### Test Infrastructure

- Framework: None exists for skill files in this repo (verified: no `tests/`, `test/`, `Makefile`, or `*.test.*` files).
- Test location: N/A
- Conventions: Skill correctness is validated via the niko workflow's own Preflight (plan-vs-skill coherence) and QA (semantic review of the implemented skill against the plan). This is the established repo pattern — no sibling skill has unit tests.
- New test files: none

## Implementation Plan

1. **Create the skill file** `rulesets/niko/skills/niko-chat/SKILL.md`
   - Files: `rulesets/niko/skills/niko-chat/SKILL.md` (new)
   - Changes: Author the skill with the AgentSkills.io frontmatter shape used by all sibling skills:
     - `name: niko-chat`
     - `description:` short, mentioning that this is the read-only memory-bank-aware codebase chat entrypoint, including trigger phrasing so the agent picks it up appropriately
   - Body sections (covering B1–B5):
     - Brief purpose statement and the read-only contract (B2)
     - "Step 1: Load Context" — instructs reading persistent files always, ephemeral files if present, with graceful degradation paths (B1, B4, B5)
     - "Step 2: Greet & Orient" — summarize what was loaded and what's known about any in-flight task; prompt operator if no question was provided (E1, E2)
     - "Step 3: Conversational Q&A Loop" — answer questions using loaded context; cite memory bank files when grounding answers; ask clarifying questions when needed
     - "Step 4: Handoff Triggers" — if conversation reveals real work, recommend `/niko` (or `/niko-creative` for design exploration), do not perform the work (B3, E3)
     - Explicit "Non-Goals" section reinforcing: no edits, no writes to memory bank, no commits, no workflow kickoff
   - Mirror tone/style of `niko-creative/SKILL.md` for consistency

2. **Update `rulesets/niko/README.md` — add `/niko-chat` to Ad-Hoc Entrypoints**
   - Files: `rulesets/niko/README.md`
   - Changes: After the existing `#### Creative Exploration` subsection, add a new `#### Codebase Chat` subsection documenting `/niko-chat`. Cover:
     - Purpose: read-only, memory-bank-aware Q&A
     - Three use-cases (parallel consultation, standalone Q&A, pre-task scoping) — concise
     - Non-goal: no artifacts, no state changes, hands off to `/niko` when real work is needed (B7)

3. **Update `rulesets/niko/README.md` — document the `niko-*` vs `nk-*` convention**
   - Files: `rulesets/niko/README.md`
   - Changes: Add a short paragraph (likely as a lead-in to the Circuit Breakers / Ad-Hoc Entrypoints sections, or a new tiny subsection just above them) stating the convention explicitly:
     - `niko-*`: entrypoints and workflow phases. Things you might autocomplete to during normal use.
     - `nk-*`: circuit breakers — out-of-band interventions on in-flight work, deliberately rare and not in the normal autocomplete flow.
   - Brief rationale on why the split exists (UX-discoverability primary, state-mutation-semantics secondary tell). (B8)

## Technology Validation

No new technology - validation not required.

## Dependencies

- Existing skill conventions in `rulesets/niko/skills/*/SKILL.md` (used as the structural template)
- Existing README structure in `rulesets/niko/README.md` (Circuit Breakers + Ad-Hoc Entrypoints sections at lines ~304–338)
- `ai-rizz` will mirror the new skill into `.cursor/skills/shared/niko-chat/` automatically; no manual mirror needed in this task

## Challenges & Mitigations

- **C1: Skill must reliably enforce the read-only contract.** An agent loading a chat skill might be tempted to "be helpful" and start editing. Mitigation: lift exact phrasing patterns from existing skills (e.g., the explicit non-goal blocks in `niko-creative/SKILL.md`) and add an explicit, prominent "Non-Goals" section. QA phase will semantically verify this is unambiguous.
- **C2: Avoid duplicating `/niko-creative`'s niche.** Creative produces a doc; chat does not. Mitigation: README copy explicitly contrasts the two; skill file directs operator to `/niko-creative` if they want a design-exploration artifact.
- **C3: Naming-convention paragraph could feel out of place in the README.** Mitigation: place it as a lead-in to the existing Circuit Breakers / Ad-Hoc Entrypoints structure, not as its own top-level section. Keep it short (3–5 lines).
- **C4: No test infra means semantic regressions are only caught by QA.** Mitigation: Be explicit and prescriptive in the skill body (numbered steps, explicit non-goals) so that QA's semantic review has unambiguous criteria to check against.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [ ] Preflight
- [ ] Build
- [ ] QA
