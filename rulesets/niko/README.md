# Niko Ruleset

Structured workflows & expert prompts that transform your AI code assistant into a seasoned senior dev (Niko) that can "oneshot" complex coding tasks & survive beyond a single session's context window.

## Installation Notes - IMPORTANT!

This specific configuration of `niko` is designed to be used in Cursor, installed as *committed* rules with the [ai-rizz](https://github.com/texarkanine/ai-rizz) tool:

	ai-rizz init https://github.com/texarkanine/.cursor-rules.git --commit
	ai-rizz add ruleset niko

If you use Claude Code, you can install Niko that way, then use [a16n](https://npmjs.com/package/a16n) to convert Niko to a compatible format:

	a16n convert --from cursor --to claude --delete-source --rewrite-path-refs

**You will need to make manual changes** if you want to use `niko` in other environments.

## Niko, the Dev

Niko's core problem-solving toolkit is defined in [niko-core](../../rules/niko-core.mdc).

The Niko ruleset includes other supplementary rules to give Niko the capabilities it needs:

* [always-tdd](../../rules/always-tdd.mdc) - forces test-driven development (TDD) for all code changes
* [illustrate-complexity](../../rules/illustrate-complexity/SKILL.md) - Encourages use of `mermaid` diagrams whenever structure is easier to show than to describe.
* [test-running-practices](../../rules/test-running-practices.mdc) - best-practices for using tests to guide development

## Niko's Memory Bank

Niko will create **many** files in your repo, mostly in the `memory-bank/` directory. This is cool and good: Niko is storing memory on disk instead of in an LLM's context window. See [memory-bank-paths.mdc](./niko/core/memory-bank-paths.mdc) for more details.

### Persistent Files

Some memory-bank files are long-lived, "persistent" files that serve as [AGENTS.md](https://agents.md/) but [better](https://blog.cani.ne.jp/2026/02/12/stop-doing-agents-md.html) - purpose-separated high-level indices to crucial information that your agents need to know about.

On first (uninitialized) memory-bank init, when neither root `AGENTS.md` nor `CLAUDE.md` exists, Niko also writes a thin pair that points harnesses at `memory-bank/`. If either file already exists, init leaves both alone.

| File                | Kind       | Purpose                                                                                                          |
|---------------------|------------|------------------------------------------------------------------------------------------------------------------|
| `productContext.md` | Persistent | Business context: target users, use cases, success criteria, constraints.                                        |
| `systemPatterns.md` | Persistent | Architectural patterns: code organization, naming conventions, design patterns in use.                           |
| `techContext.md`    | Persistent | Technical stack: languages, frameworks, build tools, file conventions, dependencies, design system references.   |
| `archive/**/*.md`   | Persistent | A directory of summary documents of past work.                                                                   |

The archive is a *key* feature! Archives collect key decisions, insights, and tasks from past work. You can use them to help understand a specific piece of past work, *and* you can periodically comb over them to identify patterns and opportunities for improvement. The archive is the long-term memory of work on the project.

### Ephemeral Files

Other memory-bank files are ephemeral, created to track a task and its progress. They're stored in the `memory-bank/active/` folder and cleaned up after you finish a task. These are the short-term memory for work on the current task.

| File                     | Kind      | Purpose                                                                                                       |
|--------------------------|-----------|---------------------------------------------------------------------------------------------------------------|
| `projectbrief.md`        | Ephemeral | Current session deliverable: user story & requirements. This guides all development.                          |
| `activeContext.md`       | Ephemeral | Current session focus: what's being worked on now, recent decisions, immediate next steps.                    |
| `progress.md`            | Ephemeral | Implementation progress: history of completed work and phase transitions.                                     |
| `tasks.md`               | Ephemeral | Active task tracking: current task details, checklists, component lists. The work to do in the current phase. |
| `reflection/*.md`        | Ephemeral | Insights from work performed during the current task                                                          |
| `creative/*.md`          | Ephemeral | Records of exploring & deciding on thorny or ambiguous design decisions for the current task.                 |
| `.preflight-status`      | Ephemeral | Records the Plan's validation; gates Build                                                                    |
| `.qa-validation-status`  | Ephemeral | Records QA validation; gates completion / Reflect                                                             |

## Niko's Workflows

Niko's workflows will guide your agent and you through several well-defined phases, tuned to the complexity of the task.

The short version is:

```mermaid
graph LR
	Start(("🧑‍💻 /niko")) --> NikoPlan["🐱 plan"]
	NikoPlan --Spawn--> NikoPreflight
	subgraph PreflightSubagent["Preflight subagent"]
		direction LR
		NikoPreflight{"🐱 preflight"} --> PreflightVerdict("Verdict")
	end
	PreflightVerdict -->|"PASS"| NikoBuild["🐱 build"]
	PreflightVerdict -->|"FAIL"| NikoPlan
	NikoBuild --Spawn--> NikoQA
	subgraph QASubagent["QA subagent"]
		direction LR
		NikoQA{"🐱 qa"} --> QAVerdict("Verdict")
	end
	QAVerdict -->|"PASS"| NikoReflect["🐱 reflect"]
	NikoReflect --> ManualArchive[/"🧑‍💻 /niko-archive"/]
	QAVerdict -->|"FAIL"| NikoBuild
```

The long version shows all the paths Niko can take, depending on the complexity of the task, with more details about phase transitions:

<details>
<summary>Long Version...</summary>

```mermaid
flowchart LR
	Niko(("🧑‍💻 /niko"))
	Archive["Archive"]

	subgraph Planning
		Plan["Plan"]
		Creative["Creative"]
		Niko -- "Level 2 & 3" --> Plan
		Plan -- "Level 3 (Feature)" --> Creative
		Plan --Spawn--> NikoPreflight
		Creative --Spawn--> NikoPreflight
		subgraph PreflightSubagent["Preflight subagent"]
			direction LR
			NikoPreflight{"Preflight"} --> PreflightVerdict("Verdict")
		end
		PreflightVerdict -.->|"Fail"| Plan
	end

	Niko -- "Level 1 (Fix)" --> Build
	PreflightVerdict -->|"Pass"| Build

	subgraph Execution
		Build["Build"]
		Build --Spawn--> NikoQA
		subgraph QASubagent["QA subagent"]
			direction LR
			NikoQA{"QA"} --> QAVerdict("Verdict")
		end
	end

	QAVerdict -->|"Level 1<br>Fail"| Build
	QAVerdict -.->|"Level 2+<br>Fail"| Plan
	QAVerdict -->|"Level1<br>Pass"| Done("Done")
	QAVerdict -->|"Level2+<br>Pass"| Reflect

	subgraph Learning
		Reflect["Reflect"]
		Reflect -.->|"Rework"| Plan
		Reflect --> Archive
	end

	classDef ideology fill:#eceff4,stroke:#9aa0a6,color:#333
	class Planning,Execution,Learning ideology
```

</details>

<br>
In case you want the "Long Version" but for just a single complexity level:

**Legend:**
- 🐱 = Phase executed autonomously
- 🧑‍💻 = Phase initiated by operator with explicit command
- Solid edge = Transition does not require operator input (parent continues)
- Dashed edge = Transition requires operator input (STOP and wait)
- `--Spawn-->` = Parent forks a subagent to run that phase; do not run it in this conversation
- Subagent ends at `Verdict`; outbound edges from `Verdict` are taken by the **parent**
- **Terminal node** = only dashed outs (e.g. Reflect → Archive)

<details>
<summary>Level 1: Quick Fix</summary>

```mermaid
graph LR
	Start(("🧑‍💻 /niko<br>Complexity Analysis")) --> NikoBuild["🐱 Build"]
	NikoBuild --Spawn--> NikoQA
	subgraph QASubagent["QA subagent"]
		direction LR
		NikoQA{"🐱 QA"} --> QAVerdict("Verdict")
	end
	QAVerdict -->|"FAIL"| NikoBuild

	ManBuild[/"🧑‍💻 /niko-build"/]

	PR{"🧑‍💻 Open Pull Request"}
	PR -."Rework PR".-> ManBuild

	QAVerdict -.->|"PASS"| PR

	ManBuild --> NikoBuild
	PR -."Ready".-> MergePR("Merge PR")
```
</details>

<details>
<summary>Level 2: Enhancement</summary>

**Key differences from Level 1:**

1. "Preflight" phase to validate plan
2. "Reflect" phase to capture insights before opening PR, may run multiple times depending on PR feedback/rework cycle
3. "Archive" phase to condense & record all Reflection insights

```mermaid
flowchart TD
	Start(("🧑‍💻 /niko<br>Complexity Analysis")) --> NikoPlan["🐱 plan"]
	NikoPlan --Spawn--> NikoPreflight
	subgraph PreflightSubagent["Preflight subagent"]
		direction LR
		NikoPreflight{"🐱 preflight"} --> PreflightVerdict("Verdict")
	end
	PreflightVerdict -->|"PASS"| NikoBuild["🐱 build"]
	PreflightVerdict -.->|"FAIL"| ManualPlan[/"🧑‍💻 /niko-plan"/]

	NikoBuild --Spawn--> NikoQA
	subgraph QASubagent["QA subagent"]
		direction LR
		NikoQA{"🐱 qa"} --> QAVerdict("Verdict")
	end
	QAVerdict -->|"PASS"| NikoReflect["🐱 reflect"]
	NikoReflect -.-> ManualArchive[/"🧑‍💻 /niko-archive"/]
	QAVerdict -->|"FAIL (fixable)"| NikoBuild
	QAVerdict -.->|"FAIL (rearchitect)"| ManualPlan

	ManualPlan -.-> NikoPlan

	PR{"🧑‍💻 Open Pull Request"}

	NikoReflect -.-> PR

	PR -."Ready".-> ManualArchive
	PR -."Rework PR".-> ManualPlan

	ManualArchive -.-> MergePR("Merge PR")
```

</details>

<details>
<summary>Level 3: Feature</summary>

**Key differences from Level 2:**

1. "Creative" phase to resolve open-ended questions
2. Human must manually review plan after Preflight

```mermaid
graph TD
	Start(("🧑‍💻 /niko<br>Complexity Analysis")) --> NikoPlan["🐱 plan"]
	NikoPlan --Spawn--> NikoPreflight
	subgraph PreflightSubagent["Preflight subagent"]
		direction LR
		NikoPreflight{"🐱 preflight"} --> PreflightVerdict("Verdict")
	end
	PreflightVerdict -.->|"PASS"| ManualBuild[/"🧑‍💻 /niko-build"/]
	PreflightVerdict -.->|"FAIL"| ManualPlan[/"🧑‍💻 /niko-plan"/]

	NikoPlan -->|"Open Questions"| NikoCreative{"🐱 creative"}
	NikoCreative -->|"High Confidence"| NikoPlan
	NikoCreative -.->|"Low Confidence"| ManualPlan[/"🧑‍💻 /niko-plan"/]

	ManualBuild --Spawn--> NikoQA
	subgraph QASubagent["QA subagent"]
		direction LR
		NikoQA{"🐱 qa"} --> QAVerdict("Verdict")
	end
	QAVerdict -->|"PASS"| NikoReflect["🐱 reflect"]
	NikoReflect -.-> ManualArchive[/"🧑‍💻 /niko-archive"/]
	QAVerdict -->|"FAIL (fixable)"| ManualBuild
	QAVerdict -.->|"FAIL (rearchitect)"| ManualPlan

	ManualPlan -.-> NikoPlan

	PR{"🧑‍💻 Open Pull Request"}

	NikoReflect -.-> PR

	PR -."Ready".-> ManualArchive
	PR -."Rework PR".-> ManualPlan

	ManualArchive -.-> MergePR("Merge PR")
```

</details>

<details>
<summary>Level 4: System</summary>

**Key differences from Level 3:**

1. Level 4 decomposes a complex task into multiple milestones, each of L1, L2, or L3 complexity.
2. "Reflections" accumulate after milestones are completed, and are archived once at the end ("Capstone" archive)
3. Manual `/niko` command required to advance from one completed milestone to the next
	- this is your chance to review Niko's work!

```mermaid
graph TD

    Start(("🧑‍💻 /niko<br>Complexity Analysis"))
    CheckIfMilestones{"L4 In-Progress?"}

    subgraph Init["First L4 Run"]
        NikoPlan["😺 plan<br>(generate milestones)"]
        ManualReview["🧑‍💻 review plan"]
        NikoPlan --Spawn--> NikoPreflight
        subgraph PreflightSubagent["Preflight subagent"]
            direction LR
            NikoPreflight{"😺 preflight"} --> PreflightVerdict("Verdict")
        end
        PreflightVerdict -->|"FAIL"| NikoPlan
        PreflightVerdict -.->|"PASS"| ManualReview
    end

    subgraph ReEntry["L4 Milestone Management"]
        CheckMilestoneCompletion{"All milestones complete?"}
        Capstone[/"🧑‍💻 /niko-archive<br>(capstone)"/]
        Capstone -->Done("Done")
        PrevDone{"Current Milestone Complete?"}
    end

    subgraph SubWorkflow["L1-L3 Milestone Execution"]
        NextSub(("😺 Complexity Analysis<br>on next milestone"))
        SubRun("😺 Run L1/L2/L3 workflow")
    end

    Start --> CheckIfMilestones

    CheckIfMilestones -->|"No"| NikoPlan

    ManualReview --> Start

    CheckIfMilestones -->|"Yes"| CheckMilestoneCompletion
    CheckMilestoneCompletion -->|"Yes"| Capstone

    CheckMilestoneCompletion -->|"No"| PrevDone
    PrevDone --"Yes"--> NextSub

    PrevDone --"No"--> SubRun

    NextSub --> SubRun
    SubRun -->|"Sub-run reflect complete<br>🧑‍💻 /niko"| Start
```

</details>

## Usage

Use the `/niko` command to get started:

	/niko let's build this idea I had, it's like this...

Niko will start working on your request and will prompt you to use other commands **if necessary** to get the work done.

If Niko stops and prompts you to run another command to continue, you should run that command in a new context window, to keep your context window clean and clear for work.

Niko's commands are split across two namespaces:

- **`niko-*`** - Workflow entrypoints. Things you might *want* to autocomplete to during normal use in order to advance a workflow. The `/niko-` prefix is the front door of the system.
- **`nk-*`** - Out-of-band interventions on in-flight work or interactions that use the memory-bank but do not advance a workflow. Deliberately *not* in the `/niko-` autocomplete cluster because reaching for them should be a conscious choice, not an accidental tab-completion.

### Circuit Breakers

Things the operator (that's you!) may choose to do by hand in the middle of a workflow, breaking the normal autonomous flow.

#### Refresh

`/nk-refresh`

If you (or Niko!) get stuck on a problem, use the `/nk-refresh` command to have Niko rigorously investigate the problem and give you a solution *or* places to investigate next. Run this in the *existing* context window, so that all the attempts and failures can be properly taken into account.

#### Save

`/nk-save`

This will flush any in-context state to the memory bank files and commit everything atomically. It is now safe to close the current context window.

When you're ready to resume, just run `/niko` in a new session; Niko will detect the active state and pick up where it left off.

You might want to save when:
- You want to switch AI harnesses mid-phase (e.g., Cursor → Claude Code)
- The context window is getting full and you'd rather checkpoint than push through
- You need to step away and want to guarantee nothing is lost

### Ad-Hoc Entrypoints

Outside the normal `/niko` workflow, there are some other ways to interact with Niko:

#### Creative Exploration

`/niko-creative`

The "Creative Phase" is usually used to resolve open design questions autonomously, but it can also be invoked on its own, outside a workflow.

You might use this if you know you want to build something, but you aren't sure exactly what to build yet and aren't ready to turn Niko loose. Run `/niko-creative` with what you DO know, and the memory-bank will guide Niko in exploring your codebase and the problem space, and help you come up with ideas.

#### Codebase Chat

`/nk-chat`

A read-only, memory-bank-aware Q&A session. Loads the persistent context (and reads any in-flight ephemeral state without mutating it) so you can ask questions about the codebase, an active task, or a possible future task without committing to a workflow and without producing any artifacts.
