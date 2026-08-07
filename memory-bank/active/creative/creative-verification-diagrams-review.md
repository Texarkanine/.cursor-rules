# Review Page: C.2a Spawn / Verdict Charts

**Status:** ✅ LOCKED (operator-approved 2026-08-07) — apply to `rulesets/` at build. This page is the chart source of truth for the task.  
**Grammar:** C.2a + Spawn vocabulary. Exploration trail: `creative-l1-verification-diagram.md` (historical).  
**Renderer:** Cursor markdown preview.

## Shared legend

- 🐱 = Phase executed autonomously  
- 🧑‍💻 = Phase initiated by operator with explicit command  
- Solid edge = Transition does not require operator input (parent continues)  
- Dashed edge = Transition requires operator input (STOP and wait)  
- `--Spawn-->` = Parent forks a subagent to run that phase; do not run it in this conversation  
- Subagent ends at `Verdict`; outbound edges from `Verdict` are taken by the **parent**  
- **Terminal node** = only dashed outs (e.g. Reflect → Archive)  

---

## Level 1

```mermaid
graph LR
    Start(("Complexity Analysis")) --> NikoBuild["🐱 Build"]
    NikoBuild --Spawn--> QA
    subgraph QASA["QA subagent"]
        direction LR
        QA{"🐱 QA"} --> QAV("Verdict")
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
        PF{"🐱 preflight"} --> PFV("Verdict")
    end
    PFV -->|"PASS"| NikoBuild["🐱 build"]
    PFV -.->|"FAIL"| ManualPlan[/"🧑‍💻 /niko-plan"/]

    NikoBuild --Spawn--> QA
    subgraph QASA["QA subagent"]
        direction LR
        QA{"🐱 qa"} --> QAV("Verdict")
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
        PF{"🐱 preflight"} --> PFV("Verdict")
    end
    PFV -.->|"PASS"| ManualBuild[/"🧑‍💻 /niko-build"/]
    PFV -.->|"FAIL"| ManualPlan[/"🧑‍💻 /niko-plan"/]

    NikoPlan -->|"Open Questions"| NikoCreative{"🐱 creative"}
    NikoCreative -->|"High Confidence"| NikoPlan
    NikoCreative -.->|"Low Confidence"| ManualPlan

    ManualBuild --Spawn--> QA
    subgraph QASA["QA subagent"]
        direction LR
        QA{"🐱 qa"} --> QAV("Verdict")
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
        PF{"🐱 preflight"} --> PFV("Verdict")
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
		PF{"🐱 preflight"} --> PFV("Verdict")
	end
	PFV -->|"PASS"| NikoBuild["🐱 build"]
	PFV -->|"FAIL"| NikoPlan
	NikoBuild --Spawn--> QA
	subgraph QASA["QA subagent"]
		direction LR
		QA{"🐱 qa"} --> QAV("Verdict")
	end
	QAV -->|"PASS"| NikoReflect["🐱 reflect"]
	NikoReflect --> ManualArchive[/"🧑‍💻 /niko-archive"/]
	QAV -->|"FAIL"| NikoBuild
```

(Short chart stays idealized — collapses L2/L3 preflight PASS differences.)

### Long version (abridged)

Ideology subgraphs: **Planning / Execution / Learning**. Subagent boxes nest inside them. Spawn is an **edge label** only (`--Spawn-->`).

- Preflight → inside **Planning**
- QA → inside **Execution** (with Build)
- Ideology bands get a light wash (`classDef ideology`); **subagent subgraphs stay unstyled** (Mermaid default) so they read as the sharp inner boxes

Fill is a soft gray wash — custom Mermaid fills do **not** reliably flip for GitHub/Cursor dark mode; if dark preview looks wrong, tune the wash later rather than styling the subagent boxes.

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
			PF{"Preflight"} --> PFV("Verdict")
		end
		PFV -.->|"Fail"| Plan
	end

	Niko -- "Level 1 (Fix)" --> Build
	PFV -->|"Pass"| Build

	subgraph Execution
		Build["Build"]
		Build --Spawn--> QA
		subgraph QASA["QA subagent"]
			direction LR
			QA{"QA"} --> QAV("Verdict")
		end
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

	classDef ideology fill:#eceff4,stroke:#9aa0a6,color:#333
	class Planning,Execution,Learning ideology
```

**Pin — Creative as subagent?** Intuition: **no** — creative stays in parent context. Revisit later.

**Pin — Spawn emoji?** No obvious diminutive-cat emoji (🐱 is already “autonomous phase”). Could label edges `🐾` / `Spawn` later; not blocking.

### Per-level README details

Same Spawn/Verdict bodies as the level sections above; README can keep PR/Merge ornaments outside the verification subgraphs. No need to duplicate full PR machinery here — when applying, swap only the preflight/QA diamonds for the Spawn→subgraph→Verdict pattern from L1–L3 above.

### README Level 4 init slice

```mermaid
graph TD
	Start(("🧑‍💻 /niko")) --> NikoPlan["🐱 plan<br>(milestones)"]
	NikoPlan --Spawn--> PF
	subgraph PFSA["Preflight subagent"]
		direction LR
		PF{"🐱 preflight"} --> PFV("Verdict")
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
4. README long version: ideology wash + nested Preflight (Planning) / QA (Execution) — do the bands read distinct from default subagent boxes in preview (light and dark)?  
5. Confirm: never list Spawn phases under “terminal nodes” / STOP lists — only Reflect-style only-dashed nodes (plus L3 preflight PASS→build as operator wait, worded as today without calling the phase “terminal”).  
