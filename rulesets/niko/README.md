# Niko Ruleset

_Based on the blog post at https://medium.com/@aashari/getting-better-results-from-cursor-ai-with-simple-rules-cbc87346ad88_

`niko` introduces a set of rules that transform your AI code assistant into a seasonsed senior dev (Niko) that can "oneshot" complex coding tasks.

This specific configuration of `niko` is designed to be used in Cursor, installed as _local_ rules with the [ai-rizz](https://github.com/texarkanine/ai-rizz) tool. **You will need to make manual changes** if you want to use `niko` in other environments.

## Niko

Niko's core operating principles are defined in the [niko-core](../../rules/niko-core.mdc) rule.

There are two supplementary prompt wrappers that support Niko's core operating principles:

* [niko-request](../../rules/niko-request.mdc) - for starting a coding task
* [niko-refresh](../../rules/niko-refresh.mdc) - when an AI agent gets stuck on a coding task

## Supplementary Rules

The Niko ruleset includes other supplementary rules to give Niko the capabilities it needs:

* [always-tdd](../../rules/always-tdd.mdc) - forces test-driven development (TDD) for all code changes
* [test-running-practices](../../rules/test-running-practices.mdc) - best-practices for using tests to guide development
* [task-list-management](../../rules/task-list-management.mdc) - for managing task lists during long-running projects

## Setup

### Step 1: Niko Core

Install the `niko` ruleset to `.cursor/rules/local/niko-*.mdc`. The [ai-rizz](https://github.com/texarkanine/ai-rizz) tool can help you do this.

    ai-rizz init https://github.com/texarkanine/.cursor-rules.git --local
    ai-rizz add ruleset niko

### Step 2: Niko Custom Cursor Modes

`niko-request` and `niko-refresh` should be set up as [Custom Modes](https://docs.cursor.com/chat/custom-modes) in Cursor:

**niko-request**

1. Create a new Custom Mode in Cursor named `Niko`
2. Set the "Custom Instructions" to the contents of the `niko-request` rule (exclude the `yaml` header).
3. Turn every switch on
4. Pin to a good agentic model

**niko-refresh**

1. Create a new Custom Mode in Cursor named `Niko Refresh`
2. Set the "Custom Instructions" to the contents of the `niko-refresh` rule (exclude the `yaml` header).
3. Turn every switch on
4. Pin to a good agentic model

## Usage

1. Activate the `Niko` custom mode (with the `niko-request` instructions) and write your initial prompt.
2. If the agent gets stuck, activate the `Niko Refresh` custom mode (with the `niko-refresh` instructions) and ask it to troubleshoot the issue:
    > Please troubleshoot the issue with `[issue description]`
3. Switch back to the `Niko` custom mode and continue working.

### Context Refreshing

Niko *should* find and use [task-list-management](../../rules/task-list-management.mdc) to manage task lists during long-running projects.
If you find that your AI agent is going off-task or forgetting things, you may have filled its context window.
Start a new chat and refer back to the Task list to get back on track without having forgotten the *important* things.
If you do this, you may wish to ask the original chat to update the Task List before you abandon it.

## Other Environments

There are `mdc:` links in the `niko-core` and `niko-refresh` rules that point to other rules in this repository. You will need to make manual changes to these links if you want to use `niko` in other environments.
