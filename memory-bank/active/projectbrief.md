# Project Brief: Markdown Style Update & Prompt-Authoring Skill

## User Story

As the author/maintainer of this rules repository, I want (1) my Markdown styling
rule sharpened to encode my real preferences, and (2) a new self-contained skill that
guides good prompt/rule/skill authorship, so that anything written in this repo (and by
agents installing these artifacts elsewhere) follows consistent, defensible conventions.

## Use-Case(s)

### Use-Case 1: Authoring Markdown in this repo

An author (human or agent) writes or edits a `.md` or `.mdc` file and needs unambiguous
guidance on code-fence nesting, line wrapping, and section-heading style.

### Use-Case 2: Authoring a prompt, rule, or skill

An author writes a prompt/rule/skill and needs guidance on classifying what they're
writing, ordering instructions for agent consumption, handling cross-references, and
prose style — without that guidance assuming any particular co-installed artifacts.

## Requirements

### Deliverable 1: Edit `rules/markdown-style.mdc`

1. Broaden `globs` to also match `.mdc` / cursor-rule files, not only `**/*.md`.
2. Replace the "count backticks, add one" code-fence-nesting section with the tilde
   technique: when embedding a Markdown example inside Markdown, use a `~~~` outer fence
   so inner content can use normal triple-backtick fences. Keep the indented-block trick
   only as a last-resort fallback.
3. Add a "no hard wrapping" section. Never hard-wrap Markdown prose — no exceptions.
   Include the rationale: machine-parsed Markdown ignores soft line breaks; human-read
   Markdown is soft-wrapped by the renderer; hard wraps only add maintenance/diff burden.
   Whitespace is meaningful to *code*, which lives in code blocks where it is preserved.
4. Add two heading sub-rules: (a) no clarifying parentheticals in headings;
   (b) bias toward short, stand-alone headings that survive extraction into nav bars,
   breadcrumbs, and anchor text.

### Deliverable 2: New self-contained prompt-authoring skill

5. Classify-what-you're-writing guidance: workflow / reference / personality, plus an
   explicit "none of these / composite" escape so authors are not pigeonholed. The lens
   is advisory; per-type guidance lives in reference files.
6. The skill's *prose* must be self-contained: it must not cite other skills in this repo
   as examples (users may install it alone). Use generic/hypothetical examples only.
7. Workflow-prompt guidance: an agent reads the whole prompt before acting, so ordering
   must be explicit, not positional — numbered steps, explicit transitions, no "as above",
   intentional repetition, sparing and load-bearing emoji.
8. Cross-reference guidance: avoid cross-references in prompt prose; only two cases are
   acceptable — (a) execution handoff ("now invoke X"); (b) a closed execution stack where
   the author controls both sides and every entry point into the flow.
9. Prose-style guidance: adopt the Rossmann anti-slop rules that map onto patterns already
   present in this repo's rules (no dramatic/teasing headings, no filler phrases, no hollow
   statements, no overused intensifiers).

## Constraints

1. Canonical sources only: edit `rules/markdown-style.mdc`; never edit copies under
   `.cursor/**` or `.claude/**`. New skill's canonical source goes under `rulesets/`.
2. The markdown-style rule and the new skill must each obey their own rules (worked example).
3. Self-containment of Deliverable 2 is a hard constraint (see requirement 6).

## Acceptance Criteria

1. `rules/markdown-style.mdc` reflects requirements 1-4 and still reads cleanly.
2. The new skill exists under `rulesets/` in the correct SKILL.md + references shape,
   satisfies requirements 5-9, and contains no references to other repo skills in its prose.
3. Both artifacts pass a self-consistency check (they follow the markdown rules they state).
