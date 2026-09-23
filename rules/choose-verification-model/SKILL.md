---
name: choose-verification-model
description: "Use when Niko QA or Preflight needs a reviewer model. Run the picker beside this skill and spawn the slug it prints. Do not use it to choose a model for an ordinary coding turn."
---

# Choose a Verification Model

Pick the QA or Preflight reviewer by running `pick.py`. Do not choose a reviewer by deliberation.

## Pick a Reviewer

1. Set `--model` to your own model slug.
2. Set `--reviewer-models` to the enabled Task-tool model slugs, comma-separated. Leave out `inherit`.
3. Run `pick.py` beside this file with Python 3. Run the command from the directory that contains this file.
4. Spawn the subagent on the slug the command prints.
5. If the process exits non-zero, stop. Report the stderr text to the operator, including an unknown author slug. Do not guess a reviewer.

### Bash

```bash
python3 pick.py --model SLUG --reviewer-models a,b
```

### PowerShell

```powershell
py -3 pick.py --model SLUG --reviewer-models a,b
```

## Refresh Scores and Prices

`refresh.py` rewrites `catalog.json` from BenchLM category scores and Cursor output prices. It keeps tiers that are already set. Run it from the directory that contains this file.

### Bash

```bash
python3 refresh.py
```

### PowerShell

```powershell
py -3 refresh.py
```

## Tiers and Interim Scores

The nine spawnable slugs start in tier `general`. Fill any other tier by hand in `catalog.json`.

An interim score is a guess. Refresh replaces it once BenchLM has any of agentic, coding, or reasoning for that model.
