---
task_id: niko-core-compression
date: 2026-09-02
complexity_level: 2
---

# Reflection: Compress and Deduplicate `niko-core.mdc`

## Summary

Successfully refactored and compressed `rules/niko-core.mdc` from 81 lines down to 49 lines, eliminating internal repetition and speculative bloat while preserving all bedrock invariants (collaborator posture, clean-break default, public interface identification, strict TDD, test integrity, circuit breaker, and credential security) intact as the omnipresent constitutional baseline.

## Requirements vs Outcome

- **Bedrock Invariants**: All core invariants were preserved verbatim, including both paragraphs of Core Persona, Public Interface Identification, Test Planning and Implement the Plan (TDD), Pre-Edit File Analysis, Proactive Code Verification, Test Integrity, Commitment Completeness, and Credential Security.
- **Internal Sprawl Compression**: Successfully consolidated repetitive safety/approval bullets into a single clear reversibility threshold, root-cause diagnosis into a single circuit-breaker bullet, context mapping and ambiguity resolution into lean non-AWS principles, and communication updates into a single low-overhead rule.
- **Bloat Removal**: Successfully excised redundant filler bullets (`Propose Enhancements`, `Reusability Mindset`, `Evaluate Strategies`, `Strict Rule Adherence`, `Ensure Production-Ready Quality`), folded `Verification Reporting`, and dropped the obsolete standalone `## Error Handling` and `## Proactive Foresight & System Health` sections.
- **Verification**: `make test` confirmed symlink and link integrity throughout.

## Plan Accuracy

The initial Level 2 plan had two minor blind spots caught by Preflight and QA gates:
1. Preflight caught that the plan scheduled keeping certain invariants without explicitly enumerating the removal of all five named filler bullets from the brief.
2. The initial Build run slightly tightened the `Implement the Plan` bullet by dropping its example parentheticals; QA caught this because the plan explicitly specified keeping it intact. Rework immediately restored the exact original wording. After QA passed, the operator asked whether that restored length was still necessary: it was not. The TDD clause is the only load-bearing part; the rest duplicated Autonomy, Ambiguity Resolution, Handle Minor Issues, and Communication. The bullet was then trimmed to the TDD invariant.

## Build & QA Observations

The automated verification subagents performed exceptionally well:
- Preflight (`claude-opus-5-thinking-medium` followed by `gpt-5.6-terra-medium`) caught omission ambiguities in the plan and validated the revised plan.
- QA (`claude-sonnet-5-thinking-high` followed by `claude-opus-5-thinking-medium`) caught subtle approximation in an invariant bullet and verified the exact-match restoration.

## Insights

### Technical

`niko-core.mdc` functions as an omnipresent rule (`alwaysApply: true`). Its density and signal-to-noise ratio directly govern agent attention across all tasks, whether in multi-phase workflows or ad-hoc chats. Eliminating repetitive restatements of "you are autonomous" and "diagnose errors" prevents token dilution, allowing the high-gravity invariants (TDD, test integrity triage, collaborator posture) to command full compliance.

### Process

When a plan specifies that an existing bullet is to be kept "intact", implementers should copy the line verbatim rather than paraphrasing or streamlining it. If streamlining is intended, it should be explicitly specified as a consolidation in the plan.

### Million-Dollar Question

If `niko-core.mdc` were designed from scratch today alongside the mature Niko workflows, it would consist strictly of frontmatter plus ~8 numbered, stable invariant rules (like an addressable constitution), with any procedural mechanics or explanations residing in dedicated references or workflow phases.

