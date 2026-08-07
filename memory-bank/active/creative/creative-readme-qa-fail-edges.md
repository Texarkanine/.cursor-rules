# Scratch: README long-chart QA Fail edges

**Decision (operator 2026-08-07):** Option A — by a long shot. Shipped on the live README long chart.

Exploration record below (A vs B). Not gospel for further edits.

**Goal:** L2+ fixable Fail also returns to Build (like L1). L2+ rearchitect Fail stays dashed to Plan. L1 has no Plan, so L1 Fail→Build is always true.

---

## Current (under-labeled)

L2+ Fail is drawn only as → Plan. Fixable→Build is invisible.

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

---

## Option A — Expand the shared Build-edge label

One solid edge Build←Verdict carries both audiences. Plan edge keeps dashed and gets an honest rearchitect label. **No new edge geometry** — only label text changes (plus Plan label rename).

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

	QAVerdict -->|"L1 Fail /<br>L2+ fixable"| Build
	QAVerdict -.->|"L2+ rearchitect"| Plan
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

---

## Option B — Second solid edge to Build

Same destinations as A, but **two parallel solid arcs** Verdict→Build (L1 vs L2+ fixable) plus dashed Verdict→Plan. Adds one edge; labels stay short and single-purpose.

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
	QAVerdict -->|"L2+ Fail<br>(fixable)"| Build
	QAVerdict -.->|"L2+ Fail<br>(rearchitect)"| Plan
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

---

## Rendered SVGs

Scratch SVGs were generated for side-by-side compare during the Option A/B decision and then deleted (not committed). The mermaid blocks above are the durable comparison.

---

## Opine (human visual intuition only)

This chart is an overview for humans, not a state machine for agents — per-level charts already carry the executable edges. So optimize for **glanceability**: what returns to Build vs what needs a human at Plan.

**Prefer Option A (stacked / expanded label on one Build edge).**

- The load-bearing visual signal is already solid→Build vs dashed→Plan. Adding a second solid cord between the same two nodes mostly doubles ink without doubling meaning — mermaid often draws parallel edges as near-overlapping curves, and the eye has to parse *two* labels to learn “both mean Build again.”
- One Build edge whose label names both riders (`L1 Fail / L2+ fixable`) matches how people chunk it: “broken implementation → rebuild” vs “broken plan → replan.”
- Option B wins when you want each word to be a single concept with no slash — nicer on a sparse per-level chart. On this crowded long chart, a third Fail arc is more clutter than clarity.

Caveat both options still share: L3 fixable actually lands on `/niko-build` (operator), not autonomous Build. The long chart already collapses that into the Build node; neither A nor B fixes that, and they shouldn’t try.
