# Task: Compress and Deduplicate `niko-core.mdc`

* Task ID: niko-core-compression
* Complexity: Level 2
* Type: Simple Enhancement

Refactor and compress `rules/niko-core.mdc` to eliminate internal repetition and bloat while preserving its role as the omnipresent constitutional baseline.

## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior.

### Test Infrastructure

- Framework: Shell check scripts via Make (`check-ruleset-symlinks.sh`, `check-ruleset-readme-links.sh`)
- Test location: `scripts/`
- Conventions: Shell scripts invoked via `make test`
- New test files: none

## Implementation Plan

### 1. Refactor and compress `rules/niko-core.mdc` — prose/policy

- Files: `rules/niko-core.mdc`
- No tests: prose/policy artifact

1. Re-read `rules/niko-core.mdc` to verify existing sections and contents.
2. Update `rules/niko-core.mdc` with compressed sections:
   - **Retain Bedrock Invariants:**
     - Retain Core Persona paragraph 1 and paragraph 2 (Collaborator Posture & Anti-Sycophancy) intact.
     - Retain `Public Interface Identification` under Research & Planning intact.
     - Retain `Test Planning` (TDD) under Research & Planning intact.
     - Retain `Pre-Edit File Analysis` under Execution intact.
     - Retain `Implement the Plan` (TDD) under Execution intact.
     - Retain `Test Integrity` under Verification & Quality Assurance intact.
     - Retain `Proactive Code Verification` under Verification & Quality Assurance intact.
     - Retain `Commitment Completeness` under Verification & Quality Assurance intact.
     - Retain `Credential Security` under Safety & Approval Guidelines intact.
   - **Compress Internal Sprawl:**
     - Consolidate `Context Mapping` and `Ambiguity Resolution` into two lean bullets, removing dated cloud/AWS boilerplate.
     - Consolidate `Error Handling` (`EH1`–`EH5`) and `V3` into a single "Root-Cause Resolution & Circuit Breaker" bullet under Verification & Quality Assurance.
     - Consolidate `Safety & Approval` bullets (`S1`–`S6`) into a single "Autonomous Execution & Approval Thresholds" standard under Safety & Approval Guidelines.
     - Consolidate `Communication` and `Verification Reporting` into a single "Structured, Low-Overhead Updates" bullet under Communication.
   - **Explicit Removals (Eliminate Internal Bloat):**
     - Remove `Propose Enhancements` bullet from Research & Planning.
     - Remove `Reusability Mindset` bullet from Research & Planning.
     - Remove `Evaluate Strategies` bullet from Research & Planning.
     - Remove `Strict Rule Adherence` bullet from Execution.
     - Remove `Ensure Production-Ready Quality` bullet from Verification & Quality Assurance.
     - Remove `Verification Reporting` bullet from Verification & Quality Assurance (folded into Communication).
     - Remove standalone `## Error Handling` section (absorbed into Verification circuit breaker).
     - Remove standalone `## Proactive Foresight & System Health` section.
   - **Formatting & Style Compliance:**
     - Ensure all prose adheres to `markdown-style.mdc` (no hard-wrapping).
3. Run `make test` to verify symlink and ruleset integrity.

## Technology Validation

No new technology - validation not required

## Dependencies

- `rulesets/niko/niko-core.mdc` (symlink to `rules/niko-core.mdc`)

## Challenges & Mitigations

- Challenge: Inadvertently omitting or weakening an invariant (TDD, backcompat/clean-break, collaborator posture, test integrity).
  - Mitigation: Explicitly trace every kept invariant against the original text to confirm zero loss of semantic governance.
- Challenge: Hard-wrapping introduced into prose lines.
  - Mitigation: Ensure paragraphs and bullet items are kept on single continuous lines per `markdown-style.mdc`.

## Pre-Mortem

- Likely cause if this plan failed: An agent operating outside a workflow might lack guidance on when to stop thrashing if the circuit breaker was over-compressed.
  - Plan response: Explicitly preserve the >2 attempts circuit breaker in the compressed root-cause invariant.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
