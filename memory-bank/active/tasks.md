# Task: asd-ste100-rule

* Task ID: asd-ste100-rule
* Complexity: Level 2
* Type: simple enhancement

Add a minimal alwaysApply GlobalPrompt at `rules/asd-ste100.mdc` that steers agent prose toward STE-inspired plain technical English, naming **ASD-STE100** and **Simplified Technical English** as a decompression key. Ship on feature branch `feat/asd-ste100-rule` and open a PR.

## Test Plan (TDD)

### Behaviors to Verify

- [B1 frontmatter]: File `rules/asd-ste100.mdc` has YAML frontmatter with `alwaysApply: true` → Cursor treats it as a GlobalPrompt
- [B2 decompression key]: Rule body contains the strings `ASD-STE100` and `Simplified Technical English` → reader can look up the official standard
- [B3 STE-inspired constraints]: Rule states concrete prose constraints (short sentences / one idea per sentence; active voice; same meaning → same word; no idioms/figurative language; no full-compliance claim) → agent has actionable instructions, not slogans
- [B4 minimal]: Rule stays short (target roughly ≤ half a screen / similar scale to `rules/git-safety.mdc`, much smaller than ADHD-skill scope) → alwaysApply token cost stays bounded
- [B5 no dictionary]: Rule does not reproduce ASD-STE100 dictionary entries or claim compliance → legal/honest scope
- [Edge: ruleset layout]: Adding only `rules/asd-ste100.mdc` (no ruleset symlink) → `make test` still passes (same packaging pattern as `conserve-context`)

### Test Infrastructure

- Framework: Make targets `test-symlinks` / `test-readme-links` (`Makefile`); no prose-content unit tests for `.mdc` GlobalPrompts
- Test location: `scripts/check-ruleset-symlinks.sh`, `scripts/check-ruleset-readme-links.sh`
- Conventions: layout/link regression only; content correctness is QA semantic review against `projectbrief.md`
- New test files: none (no content-test harness for alwaysApply prose rules; do not invent one)

## Implementation Plan

1. Author `rules/asd-ste100.mdc` (TDD: assert B1–B5 by inspection against brief, then write file)
   - Files: `rules/asd-ste100.mdc` (new)
   - Changes: frontmatter `alwaysApply: true`; short body naming ASD-STE100 / Simplified Technical English; link or point to https://www.asd-ste100.org/; STE-inspired constraints; explicit non-compliance boundary; follow `markdown-style` + `prompt-authoring` prose style
2. Run regression gate
   - Files: none
   - Changes: run `make test`; fix only if this change broke layout/links (unexpected)
3. Commit implementation
   - Files: `rules/asd-ste100.mdc`, memory-bank updates
   - Changes: conventional commit `feat(rules): add always-on ASD-STE100 prose rule` (or similar)
4. Push feature branch and open PR
   - Files: none (git/gh)
   - Changes: `git push -u origin HEAD`; `gh pr create` with summary + test plan

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing alwaysApply pattern: `rules/conserve-context.mdc`, `rules/git-safety.mdc`
- Prompt/style guidance: `rules/prompt-authoring/SKILL.md`, `rules/markdown-style.mdc`
- Distribution: `ai-rizz.skbd` already maps `rules/` → consumer `.cursor/rules`; no skbd change for a lone top-level rule (matches #90)

## Challenges & Mitigations

- [Challenge 1] Overlap with existing "be concise" guidance dilutes the rule into a no-op: Mitigation — each constraint must forbid a specific LLM habit (synonym hopping, idioms, nested multi-idea sentences), not restate "be clear"
- [Challenge 2] Accidental compliance claim or dictionary dump: Mitigation — one explicit boundary sentence; keep vocabulary guidance qualitative ("prefer common short words"), never list STE dictionary
- [Challenge 3] alwaysApply bloat: Mitigation — hard length budget; cut examples if the rule grows past minimal

## Pre-Mortem

- [Rule reads as "write simply" and changes no behavior]: Plan response — during authoring, apply behavioral test: would removing each bullet change default posture? Drop any that fail
- [PR/review asks for ruleset wiring or README pitch]: already covered by Challenge packaging choice (match #90 single-file); defer ruleset marketing unless operator expands scope
- [Trademark/copyright concern on naming]: Plan response — name the standard as a pointer + link to official site; state inspiration not compliance (Challenge 2)

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
