# Review Page: C.2a Spawn / Verdict Charts

**Status:** For operator review — not applied to `rulesets/` yet.  
**Grammar:** C.2a + Spawn vocabulary (see `creative-l1-verification-diagram.md`).  
**Renderer:** Cursor markdown preview.

## Shared legend

- 🐱 = Phase executed autonomously  
- 🧑‍💻 = Phase initiated by operator with explicit command  
- Solid edge = Transition does not require operator input (parent continues)  
- Dashed edge = Transition requires operator input (STOP and wait)  
- `--Spawn-->` = Parent forks a subagent to run that phase; do not run it in this conversation  
- Subagent ends at `Verdict`; outbound edges from `Verdict` are taken by the **parent**  
- **Terminal node** = only dashed outs (e.g. Reflect → Archive). Spawn/Verdict phases are **not** terminal nodes  

---

## Level 1

```mermaid
graph LR
    Start(("Complexity Analysis")) --> NikoBuild["🐱 Build"]
    NikoBuild --Spawn--> QA
    subgraph QASA["QA subagent"]
        direction LR
        QA{"🐱 QA"} --> QAV(("Verdict"))
    end
    QAV -->|"PASS"| Done("Done")
    QAV -->|"FAIL"| NikoBuild
```

---

## Level 2

```mermaid
graph TD
    Start(("Complexity Analysis")) --> NikoPlan["🐱 plan"]
    NikoPlan --Spawn--> PF
    subgraph PFSA["Preflight subagent"]
        direction LR
        PF{"🐱 preflight"} --> PFV(("Verdict"))
    end
    PFV -->|"PASS"| NikoBuild["🐱 build"]
    PFV -.->|"FAIL"| ManualPlan[/"🧑‍💻 /niko-plan"/]

    NikoBuild --Spawn--> QA
    subgraph QASA["QA subagent"]
        direction LR
        QA{"🐱 qa"} --> QAV(("Verdict"))
    end
    QAV -->|"PASS"| NikoReflect["🐱 reflect"]
    NikoReflect -.-> ManualArchive[/"🧑‍💻 /archive"/]
    QAV -->|"FAIL (fixable)"| NikoBuild
    QAV -.->|"FAIL (rearchitect)"| ManualPlan

    ManualPlan -.-> NikoPlan
```

Parent auto-continues on solid Verdict→build / Verdict→reflect. Reflect remains a **terminal node** (only dashed out).

---

## Level 3

Same Spawn/Verdict shape as L2; preflight PASS stays **dashed** to `/niko-build` (already operator-gated today).

```mermaid
graph TD
    Start(("Complexity Analysis")) --> NikoPlan["🐱 plan"]
    NikoPlan --Spawn--> PF
    subgraph PFSA["Preflight subagent"]
        direction LR
        PF{"🐱 preflight"} --> PFV(("Verdict"))
    end
    PFV -.->|"PASS"| ManualBuild[/"🧑‍💻 /niko-build"/]
    PFV -.->|"FAIL"| ManualPlan[/"🧑‍💻 /niko-plan"/]

    NikoPlan -->|"Open Questions"| NikoCreative{"🐱 creative"}
    NikoCreative -->|"High Confidence"| NikoPlan
    NikoCreative -.->|"Low Confidence"| ManualPlan

    ManualBuild --Spawn--> QA
    subgraph QASA["QA subagent"]
        direction LR
        QA{"🐱 qa"} --> QAV(("Verdict"))
    end
    QAV -->|"PASS"| NikoReflect["🐱 reflect"]
    NikoReflect -.-> ManualArchive[/"🧑‍💻 /niko-archive"/]
    QAV -->|"FAIL (fixable)"| ManualBuild
    QAV -.->|"FAIL (rearchitect)"| ManualPlan

    ManualPlan -.-> NikoPlan
```

Both Verdict outs from preflight are dashed → preflight’s *Verdict* is terminal-shaped in the old sense, but we still call the phase a **Spawn**, not a “terminal node,” so vocabulary stays consistent with L2. The STOP list still includes Preflight PASS → Build.

---

## Level 4

L4 has no L4-scoped QA/build/reflect — only **plan preflight** before milestone runs. Sub-run verification stays inside L1–L3 charts. Beastie change is just wrapping that one preflight in Spawn/Verdict.

```mermaid
graph TD
    Start(("Complexity Analysis")) --> NikoPlan["🐱 plan<br>(generate milestones)"]
    NikoPlan --Spawn--> PF
    subgraph PFSA["Preflight subagent"]
        direction LR
        PF{"🐱 preflight"} --> PFV(("Verdict"))
    end
    PFV -->|"FAIL"| NikoPlan
    PFV -.->|"PASS"| ManualReview["🧑‍💻 review plan"]
    ManualReview -.->|"🧑‍💻 /niko"| Niko
    subgraph SubWorkflow["L1-L3 Workflow"]
        Niko(("Milestone Execution"))
        Niko -.->|"Next Milestone Complete<br>🧑‍💻 /niko"| Niko
    end
    Niko -.->|"All Milestones Complete"| NikoArchive[/"🧑‍💻 /niko-archive"/]
```

Milestone bodies inherit Spawn/QA from whichever L1/L2/L3 chart applies — L4 chart does not redraw them.

---

## README abridged (proposed)

Not applied to `rulesets/niko/README.md` yet — preview only.

### Short version

```mermaid
graph LR
	Start(("🧑‍💻 /niko")) --> NikoPlan["🐱 plan"]
	NikoPlan --Spawn--> PF
	subgraph PFSA["Preflight subagent"]
		direction LR
		PF{"🐱 preflight"} --> PFV(("Verdict"))
	end
	PFV -->|"PASS"| NikoBuild["🐱 build"]
	PFV -->|"FAIL"| NikoPlan
	NikoBuild --Spawn--> QA
	subgraph QASA["QA subagent"]
		direction LR
		QA{"🐱 qa"} --> QAV(("Verdict"))
	end
	QAV -->|"PASS"| NikoReflect["🐱 reflect"]
	NikoReflect --> ManualArchive[/"🧑‍💻 /niko-archive"/]
	QAV -->|"FAIL"| NikoBuild
```

(Short chart stays idealized — collapses L2/L3 preflight PASS differences.)

### Long version (abridged)

Ideology subgraphs stay: **Planning / Execution / Learning**. Subagent boxes are a second kind of subgraph — nest them *inside* the ideology they belong to rather than floating beside a fake `SpawnPF` node. Spawn is an **edge label** only (`--Spawn-->`), same as the level charts.

**This pass:** Preflight lives under **Planning** (plan validation before build). QA still hangs off Build as before — whether it belongs inside Execution (or Learning) is the next question; left alone for now.

```mermaid
flowchart LR
	Niko(("🧑‍💻 /niko"))
	Archive["Archive"]

	subgraph Planning
		Plan["Plan"]
		Creative["Creative"]
		Niko -- "Level 2 & 3" --> Plan
		Plan -- "Level 3 (Feature)" --> Creative
		Plan --Spawn--> PF
		Creative --Spawn--> PF
		subgraph PFSA["Preflight subagent"]
			direction LR
			PF{"Preflight"} --> PFV(("Verdict"))
		end
		PFV -.->|"Fail"| Plan
	end

	Niko -- "Level 1 (Fix)" --> Build
	PFV -->|"Pass"| Build

	subgraph Execution
		Build["Build"]
	end

	Build --Spawn--> QA
	subgraph QASA["QA subagent"]
		direction LR
		QA{"QA"} --> QAV(("Verdict"))
	end

	QAV -->|"Level 1<br>Fail"| Build
	QAV -.->|"Level 2+<br>Fail"| Plan
	QAV -->|"Level1<br>Pass"| Done("Done")
	QAV -->|"Level2+<br>Pass"| Reflect

	subgraph Learning
		Reflect["Reflect"]
		Reflect -.->|"Rework"| Plan
		Reflect --> Archive
	end
```

**Pin — QA ideology:** Is QA part of Execution (with Build), or its own band, or Learning? Not decided this pass.

**Pin — Creative as subagent?** Intuition: **no** — creative should stay in the parent context so exploration colors the continuing plan work; parent is no longer the judge for verification, but creative is not a judgment gate in that sense. Revisit later; not in scope for this verification change.

### Per-level README details

Same Spawn/Verdict bodies as the level sections above; README can keep PR/Merge ornaments outside the verification subgraphs. No need to duplicate full PR machinery here — when applying, swap only the preflight/QA diamonds for the Spawn→subgraph→Verdict pattern from L1–L3 above.

### README Level 4 init slice

```mermaid
graph TD
	Start(("🧑‍💻 /niko")) --> NikoPlan["🐱 plan<br>(milestones)"]
	NikoPlan --Spawn--> PF
	subgraph PFSA["Preflight subagent"]
		direction LR
		PF{"🐱 preflight"} --> PFV(("Verdict"))
	end
	PFV -->|"FAIL"| NikoPlan
	PFV -.->|"PASS"| ManualReview["🧑‍💻 review plan"]
	ManualReview -.-> Sub["L1–L3 milestone runs<br>(their charts own QA)"]
```

---

## What to look for in review

1. Does Spawn + Verdict + subgraph read clearly in Cursor preview at L2 and L3 side by side?  
2. Is L3’s double-dashed preflight Verdict acceptable next to L2’s solid PASS?  
3. Is L4’s single Spawn preflight enough, with QA only inside sub-run charts?  
4. README long version: does nesting Preflight subagent inside Planning fix the two-kinds-of-subgraph clash? (QA nesting still open.)  
5. Confirm: never list Spawn phases under “terminal nodes” / STOP lists — only Reflect-style only-dashed nodes (plus L3 preflight PASS→build as operator wait, worded as today without calling the phase “terminal”).  
