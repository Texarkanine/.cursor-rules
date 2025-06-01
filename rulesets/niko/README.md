# Niko Ruleset

_Based on the blog post at https://medium.com/@aashari/getting-better-results-from-cursor-ai-with-simple-rules-cbc87346ad88_

`niko` introduces a set of "core operating principles" that transforms your AI code assistant into a seasonsed senior dev (Niko).

There are two supplementary prompt wrappers that underscore Niko's core operating principles:

* `niko-request` - for starting a coding task
* `niko-refresh` - when an AI agent gets stuck on a coding task

Depending on how AI agents will interact with the codebases you work on, the optimal Niko setup will vary.

## Setup

### Step 1: Niko Core

#### All Repos Use AI Agents

If **all** repositories that you work with will *also* be worked on by AI agents outside your Cursor, you probably want to commit `niko-core.mdc` to the repositories as Cursor rule.

If you have remote or headless AI agents, you may  also wish to add `niko-request` as a prompt wrapper around user requests they receive.

#### Some Repos use AI Agents

If **some** repositories that you work with will *also* be worked on by AI agents outside your Cursor, but some repositories will not, you probably want to:

1. store `niko-core.mdc` in `.cursor/rules` without committing it for repos that won't use other AI agents
2. commit `niko-core.mdc` to `.cursor/rules` for the repositories that will use other AI agents

The [ai-rizz](https://github.com/texarkanine/ai-rizz) tool can help you manage this (but is not required).

#### Only I use AI Agents

If **none** of the repositories that you work with be worked on by AI agents outside your Cursor, you may wish to make Niko's core operating principles part of your [Cursor User Rules](https://docs.cursor.com/context/rules#user-rules). This will make Niko's core operating principles always available with no per-repository setup required on your part.

Just paste the contents of `niko-core.mdc` into your User Rules.

### Step 2: Niko Custom Cursor Modes

In all cases, `request` and `refresh` should be set up as [Custom Modes](https://docs.cursor.com/chat/custom-modes) in Cursor:

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

#### Ad-Hoc Usage

If you don't create any Custom Modes, you can still use Niko's Request and Refresh by directly referencing the Rules in your prompts:

**Initial Prompt**

> Please follow the instructions in `@niko-refresh.mdc` to troubleshoot the issue.

but it's probably easiser to put it in a mode.

## Workflow

1. Activate the `Niko` custom mode (with the `niko-request` instructions) and write your initial prompt.
2. If the agent gets stuck, activate the `Niko Refresh` custom mode (with the `niko-refresh` instructions) and ask it to troubleshoot the issue:
    > Please follow the instructions in `@niko-refresh.mdc` to troubleshoot the issue with `[issue description]`
3. Switch back to the `Niko` custom mode and continue working.
