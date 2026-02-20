# ⚠️ Under Construction

This is a rewrite in-progress. Don't try to use it yet!

# Niko Ruleset

Structured workflows & expert prompts that transform your AI code assistant into a seasoned senior dev (Niko) that can "oneshot" complex coding tasks & survive beyond a single session's context window.

## Installation Notes - IMPORTANT!

This specific configuration of `niko` is designed to be used in Cursor, installed as *committed* rules with the [ai-rizz](https://github.com/texarkanine/ai-rizz) tool:

	ai-rizz init https://github.com/texarkanine/.cursor-rules.git --commit
	ai-rizz add ruleset niko

**You will need to make manual changes** if you want to use `niko` in other environments.

If you use Claude Code, you can install Niko that way, then use [a16n](https://npmjs.com/package/a16n) to convert Niko to a compatible format:

	a16n convert --from cursor --to claude --delete-source --rewrite-path-refs

## Niko, the Dev

Niko's core problem-solving toolkit is defined in [niko-core](../../rules/niko-core.mdc).

The Niko ruleset includes other supplementary rules to give Niko the capabilities it needs:

* [always-tdd](../../rules/always-tdd.mdc) - forces test-driven development (TDD) for all code changes
* [visual-planning](../../rules/visual-planning.mdc) - Encourages use of `mermaid` diagrams when planning complex tasks.
* [test-running-practices](../../rules/test-running-practices.mdc) - best-practices for using tests to guide development

## Niko's Memory Bank

Niko will create **many** files in your repo, mostly in the `memory-bank/` directory. This is cool and good: Niko is storing memory on disk instead of in an LLM's context window.

Some of those files are long-lived, "persistent" files that serve as [AGENTS.md](https://agents.md/) but [better](https://blog.cani.ne.jp/2026/02/12/stop-doing-agents-md.html) - purpose-separated high-level indicies to crucial information that your agents need to know about.

Other files are ephemeral, created to track a task and its progress. They're cleaned up after you finish a task.

A key feature of the memory bank is `memory-bank/archive/` - a directory of summary documents of past work. These collect key decisions, insights, and tasks from past work. You can use them to help understand a specific piece of past work, *and* you can periodically comb over them to identify patterns and opportunities for improvement.

## Niko's Workflows

Niko will evaluate the complexity of the tasks and choose one of three workflows depending on the complexity. These may look daunting, but don't worry:

1. Niko will do most phase transitions for you.
2. Niko will tell you which command to run when a phase transition requires your input.
3. These charts *include* the actions you'd take on GitHub, too

<details>
<summary>Level 1: Quick Fix</summary>

```mermaid
graph LR
	Start(("🧑‍💻 /niko<br>Complexity Analysis")) --> NikoBuild["🐱 Build"]
	NikoBuild --> NikoQA{"🐱 QA"}
	NikoQA -->|"FAIL"| NikoBuild

	ManBuild[/"🧑‍💻 /build"/]

	PR{"🧑‍💻 Open Pull Request"}
	PR -."Rework PR".-> ManBuild

	NikoQA -->|"PASS"| PR
	
	ManBuild --> NikoBuild
	PR -."Ready".-> MergePR("Merge PR")
	
```
</details>

<details>
<summary>Level 2: Enhancement</summary>

Key differences from Level 1:

1. "Preflight" phase to validate plan
2. "Reflect" phase to capture insights before opening PR, may run multiple times depending on PR feedback/rework cycle
3. "Archive" phase to condense & record all Reflection insights 

```mermaid
flowchart TD
	Start(("🧑‍💻 /niko<br>Complexity Analysis")) --> NikoPlan["🐱 plan"]
	NikoPlan --> NikoPreflight{"🐱 preflight"}
	NikoPreflight -->|"PASS"| NikoBuild["🐱 build"]
	NikoPreflight -.->|"FAIL"| ManualPlan[/"🧑‍💻 /niko-plan"/]

	NikoBuild --> NikoQA{"🐱 qa"}
	NikoQA -->|"PASS"| NikoReflect["🐱 reflect"]
	NikoReflect -.-> ManualArchive[/"🧑‍💻 /archive"/]
	NikoQA -->|"FAIL (fixable)"| NikoBuild
	NikoQA -->|"FAIL (rearchitect)"| ManualPlan

	ManualPlan -.-> NikoPlan

	PR{"🧑‍💻 Open Pull Request"}

	NikoReflect -.-> PR

	PR -."Rework PR".-> ManualPlan
	PR -."Ready".-> ManualArchive
	ManualArchive -.-> MergePR("Merge PR")
```

</details>

<details>
<summary>Level 3: Feature</summary>

Key differences from Level 2:

1. "Creative" phase to resolve open-ended questions
2. Human must manually review plan after Preflight

```mermaid
graph TD
	Start(("Complexity Analysis")) --> NikoPlan["🐱 plan"]
	NikoPlan --> NikoPreflight{"🐱 preflight"}
	NikoPreflight -.->|"PASS"| ManualBuild[/"🧑‍💻 /niko-build"/]
	NikoPreflight -.->|"FAIL"| ManualPlan[/"🧑‍💻 /niko-plan"/]

	NikoPlan -->|"Open Questions"| NikoCreative{"🐱 creative"}
	NikoCreative -->|"High Confidence"| NikoPlan
	NikoCreative -.->|"Low Confidence"| ManualPlan[/"🧑‍💻 /niko-plan"/]

	ManualBuild --> NikoQA{"🐱 qa"}
	NikoQA -->|"PASS"| NikoReflect["🐱 reflect"]
	NikoReflect -.-> ManualArchive[/"🧑‍💻 /niko-archive"/]
	NikoQA -->|"FAIL (fixable)"| ManualBuild
	NikoQA -->|"FAIL (rearchitect)"| ManualPlan

	ManualPlan -.-> NikoPlan

	PR{"🧑‍💻 Open Pull Request"}

	NikoReflect -.-> PR

	PR -."Rework PR".-> ManualPlan
	PR -."Ready".-> ManualArchive
	ManualArchive -.-> MergePR("Merge PR")
```

</details>

## Usage

Use the `/niko` command to get started:

	/niko let's build this idea I had, it's like this...

Niko will start working on your request and will prompt you to use other commands **if necessary** to get the work done.

The full range of Niko's phases are:

```mermaid
flowchart LR

	%% Nodes
	Niko(("🧑‍💻 /niko"))
	Plan["Plan"]
	Creative["Creative"]
	Preflight{"Preflight"}
	QA{"QA"}
	Archive["Archive"]

	%% Paths
	subgraph Planning
        Niko -- "Level 2 & 3" --> Plan

        Plan -- "Level 3 (Feature)" --> Creative

        
	end

    Creative --> Preflight
    Niko -- "Level 1 (Fix)" --> Build
    Plan -- "Level 2 (Enhance)" --> Preflight

	Preflight -->|"Pass"| Build
    Preflight -.->|"Fail"| Plan

	subgraph Execution
        Build["Build"]
	end

    Build --> QA
    
    QA -.->|"Fail"| Plan
	QA -->|"Level1<br>Pass"| Done("Done")
    QA -->|"Level2+<br>Pass"| Reflect
	
	subgraph Learning
        Reflect["Reflect"]
        Reflect -.->|"Rework"| Plan

        Reflect --> Archive
	end
```


<br>
Key insights: 

1. `/niko-reflect` whenever a milestone is reached. `/niko-archive` at the very end before merge. You want your PR reviewers to see your reflections to answer things like "why didn't you..." or "why did you..." etc.
2. When iterating, return to `/niko` and it may route your refinements to a different level - e.g. if you finished a Level 3 feature but want a minor change, that iteration might be routed to the Level 1 flow.

### Context Refreshing

Niko stores progress on disk in the `memory-bank` directory. When your context window is getting full, let Niko finish the current task, then... start a new conversation! If Niko was building, you can just start a new chat with `/niko-build` and nothing else and Niko will resume the work!

### Advanced Troubleshooting

If you (or Niko!) get stuck on a problem, use the `/refresh` command to have Niko rigorously investigate the problem and give you a solution *or* places to investigate next.

**Note:** `/niko-creative` is for exploring solution spaces and creating new things. `/refresh` is for troubleshooting an existing defect.
