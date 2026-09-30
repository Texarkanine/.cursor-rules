# Project Brief

## User Story

As a consumer of `choose-verification-model`, I want the skill's assets to live in an XDG home directory, and I want to run refresh myself as soon as a new model drops, so that I can set and adjust tiers locally while later skill updates still fill in models I never touched.

## Use-Case(s)

### Run refresh before the upstream skill updates

A new model has dropped and the installed skill does not list it yet. The consumer runs refresh. The new model is pulled into their XDG copy.

### Adjust tiers locally

The consumer puts their own tier list next to that catalog and changes tiers to taste, including placing a model they care about.

### Take shipped defaults for untouched models

The consumer has set one model locally. A later skill update ships five new models they did not set. Those five take the shipped defaults. The model they set keeps their local setting.

## Requirements

1. The skill's assets can be stored in an XDG home directory.
2. `scripts/refresh.py` writes to that same XDG directory.
3. A consumer can run refresh, not only the maintainer.
4. A refresh run before the upstream skill has updated pulls in a newly dropped model.
5. The consumer can assign a tier and can adjust the tier list in that home directory.
6. Local settings take precedence.
7. Models the consumer did not set take the defaults shipped by a later skill update.
8. The merge is mechanical and is done by the Python scripts.
9. The consumer can put their own tier list next to the catalog.

## Constraints

1. The merge is invisible to agents that invoke the scripts.
2. The agent-facing skill does not change.
3. Catalog score precedence is unlikely to matter: a model's score rarely changes after it first lands. Tiers are what consumers adjust.

## Acceptance Criteria

1. After installing the skill, a consumer can run refresh and have it write into their XDG directory.
2. A model that exists only because the consumer ran refresh, before the upstream skill shipped it, is present in that directory.
3. A local tier edit survives a later skill update, and models the consumer never set receive the shipped defaults.
4. Agents still invoke the skill the same way. They do not perform the merge.
