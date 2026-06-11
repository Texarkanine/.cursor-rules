# Task: Markdown Style Update & Prompt-Authoring Skill

* Task ID: md-style-and-prompt-authoring
* Complexity: Level 3
* Type: docs/authoring (rule enhancement + new skill)

Sharpen `rules/markdown-style.mdc` (tilde code-fence nesting, no-hard-wrap rule, heading
sub-rules, broadened globs) and author a new self-contained prompt-authoring skill under
a new `rulesets/authoring/` group.

## Component Analysis

### Affected Components
- `rules/markdown-style.mdc` (existing rule): styling conventions → broaden globs; replace
  code-fence-nesting section; add no-hard-wrap section; add two heading sub-rules.
- `rulesets/authoring/` (NEW ruleset group): does not exist → create group with a `README.md`
  describing it, mirroring the `rulesets/shell/README.md` and `rulesets/niko` conventions.
- `rulesets/authoring/skills/prompt-authoring/SKILL.md` (NEW): the skill entrypoint —
  classify lens, self-containment principle, cross-reference rules, prose-style guidance,
  self-check pass.
- `rulesets/authoring/skills/prompt-authoring/references/*.md` (NEW): per-type deep guidance
  (workflow / reference / personality), loaded by explicit path from the skill.

### Cross-Module Dependencies
- `SKILL.md` → its own `references/*.md`: loaded by explicit path. This is internal to the
  skill, so it does NOT violate the self-containment constraint (the references ship with it).
- New skill → `ai-rizz.skbd`: registering the new `rulesets/authoring` group for installation
  is a deployment concern, tracked as a challenge below; not part of content authoring.

### Boundary Changes
- New public artifact (a skill other repos may install). Its prose contract: self-contained,
  no references to sibling repo skills.

## Open Questions

- [x] Where does the new general-purpose skill's canonical source live? → Resolved:
  new `rulesets/authoring/` ruleset group (skills currently only exist under
  `rulesets/niko/skills/`, which is niko-coupled; a dedicated group keeps it general and
  independently installable). Reasoned default; surfaced to operator in plan report for veto.

## Test Plan (TDD)

### Applicability

Both deliverables are prose (a `.mdc` rule and a `SKILL.md` + `.md` references). There is no
executable code and no Markdown test runner in this repo. Traditional automated TDD does not
apply. Verification is a self-consistency + acceptance check performed in the QA phase. This
is flagged honestly rather than fabricating tests.

### Behaviors / Acceptance Checks to Verify

- markdown-style frontmatter `globs` matches both `.md` and `.mdc` files.
- Code-fence section teaches the `~~~` outer-fence technique for markdown-in-markdown;
  indented blocks demoted to last-resort fallback; backtick-counting ladder removed.
- A "no hard wrapping" section exists with the three-part rationale (machine-parsed ignores
  breaks; renderers soft-wrap; hard wraps add maintenance/diff burden) and no real exceptions
  (whitespace-in-code lives in code blocks, preserved regardless).
- Heading section gains: (a) no clarifying parentheticals; (b) short, nav/anchor-friendly bias.
- Skill exists at `rulesets/authoring/skills/prompt-authoring/SKILL.md` with `name:` /
  `description:` frontmatter.
- Classify lens includes the explicit "none of these / composite" escape (advisory framing).
- Skill prose contains zero references to other repo skills (grep self-check).
- Cross-reference section lists exactly the two acceptable cases (execution handoff; closed
  execution stack).
- Prose-style section adopts the mapped Rossmann rules (no dramatic headings, no filler
  phrases, no hollow statements, no overused intensifiers).
- Both artifacts obey `markdown-style.mdc` themselves (no hard wraps; tilde nesting where they
  embed markdown; heading rules).

### Test Infrastructure
- Framework: none (prose artifacts). Verification is manual QA against acceptance criteria,
  plus `rg` self-checks for the grep-able invariants (no sibling-skill references; globs).
- New test files: none.

## Implementation Plan

1. Edit `rules/markdown-style.mdc` frontmatter.
    - Files: `rules/markdown-style.mdc`
    - Changes: broaden `globs` to cover `.mdc` / cursor-rule files in addition to `**/*.md`.
2. Replace the "Markdown Code Fence Nesting" section.
    - Files: `rules/markdown-style.mdc`
    - Changes: lead with the `~~~` tilde technique (use a tilde outer fence so inner content
      uses normal triple backticks); keep a brief indented-block fallback; remove the
      "one more backtick" escalation ladder and the five-backtick example.
3. Add a "No Hard Wrapping" section.
    - Files: `rules/markdown-style.mdc`
    - Changes: state the rule, give the three-part rationale, clarify the code-block point.
4. Extend the "Section Headings" section with two sub-rules.
    - Files: `rules/markdown-style.mdc`
    - Changes: no clarifying parentheticals; bias for short, stand-alone, nav/anchor-friendly
      headings. Include WRONG/RIGHT examples.
   - BUILD NOTE (preflight): the existing WRONG/CORRECT example blocks in this file use
     tab-indentation to display markdown-in-markdown. Convert them to the `~~~` tilde
     technique so the document practices its own newly-primary rule (don't leave the doc
     demonstrating the demoted fallback as its main style).
5. Create the new ruleset group scaffold.
    - Files: `rulesets/authoring/README.md`
    - Changes: short README describing the authoring ruleset and listing the skill.
6. Author the skill entrypoint.
    - Files: `rulesets/authoring/skills/prompt-authoring/SKILL.md`
    - Changes: frontmatter (`name`, `description`); purpose; classify lens (workflow /
      reference / personality + none/composite escape, advisory) INCLUDING one short composite
      worked example (e.g., a doc that is mostly reference but sets a little personality) so
      the escape is concrete; self-containment principle; cross-reference rules (two cases);
      prose-style (Rossmann-derived); self-check pass; explicit-path pointers to references.
7. Author the per-type references.
    - Files: `rulesets/authoring/skills/prompt-authoring/references/workflow-prompts.md`,
      `.../reference-prompts.md`, `.../personality-prompts.md`
    - Changes: workflow = agent reads whole prompt before acting, so ordering is explicit not
      positional (numbered steps, explicit transitions, no "as above", intentional repetition,
      sparing load-bearing emoji); reference = facts/constraints, scannable, no procedure or
      personality; personality = disposition/posture/defaults/voice.
8. Self-consistency pass.
    - Files: all of the above
    - Changes: verify each artifact obeys `markdown-style.mdc`; run `rg` for sibling-skill
      references in the skill; confirm globs.

## Technology Validation

No new technology - validation not required. (New Markdown/MDC files only; no dependencies,
build tools, or runtimes introduced.)

## Challenges & Mitigations

- New `rulesets/authoring/` group may need registration in `ai-rizz.skbd` to be installable.
  Mitigation: authoring the canonical content is independent of install wiring; flag the
  registration as a follow-up for the operator (out of scope for this task's content goal).
- Self-containment is easy to violate by reflex (citing niko/shell skills as examples).
  Mitigation: use only generic/hypothetical examples in skill prose; grep-verify in QA.
- The skill is prose about prose; risk of it not obeying its own rules. Mitigation: the
  self-consistency pass (step 8) treats the artifacts as their own worked examples.

## Preflight Findings

- [LOW] Convention: `systemPatterns.md` documents skills only under `rulesets/niko/skills/`.
  New `rulesets/authoring/skills/` extends the underlying pattern (skills live in a ruleset
  group's `skills/` dir). Not a violation; generalize the pattern language at reflect.
- [LOW] Consistency: existing `markdown-style.mdc` examples use tab-indentation to show
  markdown-in-markdown; convert to tilde fences in build (see step 4 BUILD NOTE).
- [INFO] Dependency: `ai-rizz.skbd` may need a `rulesets/authoring` entry to be installable;
  deployment follow-up, out of scope for content authoring.
- [INFO] Glob broadening auto-injects markdown-style on `.mdc` files too — intended, low risk.
- [ADVISORY] Applied in-scope: classify section gains one composite worked example (step 6).
- [ADVISORY] Deferred (operator): generalize `systemPatterns.md` skill-location language.

## Status

- [x] Component analysis complete
- [x] Open questions resolved
- [x] Test planning complete (TDD) — N/A for prose, documented
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Preflight — PASS with advisory
- [x] Build — all 8 steps complete
- [ ] QA
