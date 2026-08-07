# Decision: L1 Workflow Diagram — Verification as Terminal Subagent

**Status:** Historical exploration. **LOCKED decision:** C.2a Spawn / Verdict in `creative-verification-diagrams-review.md`. Do not build from options below.

**Approach:** Generic creative (process / visual grammar for Niko level workflows)

## Context

### What

How should `level1-workflow.md`'s mermaid express that QA runs in a **subagent that never advances the workflow**, while **advancing is a parent (or operator) act** after the verifier stops?

L1 is the degenerate case: one verification node (QA), no preflight. The chosen grammar must scale to preflight + QA on L2–L4 without a different dialect per level.

### Why it matters

Operator: level-N workflow charts are the **handcrafted source of truth**; phase mappings and skills derive from them. Prior plan treated subagent as an implementation detail and left mermaid alone — that is reversed. Wrong visual grammar either (a) still reads as “QA continues to Done” (today’s failure mode) or (b) invents notation that cannot extend to preflight or that overloads the existing solid/dashed legend.

### Constraints

- Stay in Mermaid that GitHub / Cursor preview render (`graph` / `sequenceDiagram`; no exotic plugins).
- Preserve existing Niko legend vocabulary where possible: 🐱 autonomous, 🧑‍💻 operator command, solid vs dashed edges — or **extend the legend explicitly** if meaning changes.
- Verification agent must not look like it owns the edge into Build/Done/Reflect.
- Manual recovery remains: skill alone is terminal; resume is elsewhere.
- Match Niko directness: prefer a small legend change over a baroque subgraph if both carry the meaning.
- Operator may hand-edit the winning chart; this doc’s job is options, not a premature lock.

### Semantic fork (decide with the picture)

Two different “terminal” meanings are in play. Pick one; the diagram should make it obvious.

| Sense | Meaning | L1 PASS edge |
| --- | --- | --- |
| **T1 — Subagent-terminal** | The agent that ran QA always stops; the **parent** still takes solid edges (L2 automation kept). | Solid `PASS → Done` owned by parent after fork returns |
| **T2 — Phase-terminal** | Like Reflect → Archive and L3 Preflight → `/niko-build`: verification **ends the turn**; next phase needs a new invoke (🧑‍💻 or parent re-entry). | Dashed `PASS → …` |

Today L1 is neither: QA looks like a normal diamond that advances. L3 preflight is already **T2**. Reflect is **T2**. The amended one-liner plan assumed **T1**. Your “like reflect / like L3 preflight” leans **T2**.

---

## Options Evaluated (L1 chart renditions)

Baseline today:

```mermaid
graph LR
    Start(("Complexity Analysis")) --> NikoBuild["🐱 Build"]
    NikoBuild --> NikoQA{"🐱 QA"}
    NikoQA -->|"PASS"| Done("Done")
    NikoQA -->|"FAIL"| NikoBuild
```

### A — Legend-only (chart shape unchanged)

Keep the same graph; extend the legend:

> Verification phases (🐱 QA, 🐱 preflight) run in a forked subagent and are terminal in that agent. Outbound edges are taken by the parent after the subagent stops (or by the operator on dashed edges).

| Pros | Cons |
| --- | --- |
| Zero chart churn; scales by legend | Easy to miss; agents pattern-match edges harder than legends |
| Fits T1 without redraw | Does not *show* the subagent cycle |

**Pattern fit:** Weakest visual; strongest minimalism.

### B — Parent gate node (result owned outside QA)

```mermaid
graph LR
    Start(("Complexity Analysis")) --> NikoBuild["🐱 Build"]
    NikoBuild --> ForkQA["🐱 fork QA"]
    ForkQA --> Gate{"QA result"}
    Gate -->|"PASS"| Done("Done")
    Gate -->|"FAIL"| NikoBuild
```

QA skill is not a diamond — only “fork” + parent gate. Subagent is implied.

| Pros | Cons |
| --- | --- |
| Clear: Done is not an edge out of QA | QA procedure invisible as a phase node |
| Natural T1 | “fork QA” is a new node type; must repeat for preflight |
| | Degenerate L1 gets busier |

### C — Subgraph: child stops; return edges to parent

```mermaid
graph LR
    Start(("Complexity Analysis")) --> NikoBuild["🐱 Build"]
    NikoBuild --> Fork["fork"]
    subgraph SA["QA subagent"]
        direction LR
        QA{"🐱 QA"} --> Halt(["stop"])
    end
    Fork --> QA
    Halt -.->|"PASS"| Done("Done")
    Halt -.->|"FAIL"| NikoBuild
```

| Pros | Cons |
| --- | --- |
| Shows subagent cycle + stop | Dashed overloaded if dashed still means “operator input” |
| Halt is visually terminal | Mermaid subgraph + cross edges can render messy in LR |
| | Agents may still follow Halt→Done as “QA continues” |

**Legend fix if chosen:** dashed from a `stop` node = “return to parent / operator,” not “QA executes Done.”

#### C.1 - Operator Tweaks

```mermaid
graph LR
    Start(("Complexity Analysis")) --> NikoBuild["🐱 Build"]
    NikoBuild --Spawn--> QA
    subgraph SA["QA subagent"]
        direction LR
        QA{"🐱 QA"} --> Verdict(["Verdict"])
    end
    Verdict -->|"PASS"| Done("Done")
    Verdict -->|"FAIL"| NikoBuild
```

Operator lean: subgraph makes the subagent obvious; `Spawn` edge into the diamond; `Verdict` (not `stop`) is what leaves the box. Open: edge labels (`returns` / `reports` / bare PASS) and stroke (solid vs `-.->`).

#### C.2 — Same grammar on Level 2 (continuation visible)

L2 is where PASS actually goes somewhere (preflight → build, QA → reflect). Three label/stroke variants; structure identical.

**C.2a — Bare PASS/FAIL, solid = auto, dashed = operator (keeps today’s legend)**

```mermaid
graph TD
    Start(("Complexity Analysis")) --> NikoPlan["🐱 plan"]
    NikoPlan --Spawn--> PF
    subgraph PFSA["Preflight subagent"]
        direction LR
        PF{"🐱 preflight"} --> PFV(["Verdict"])
    end
    PFV -->|"PASS"| NikoBuild["🐱 build"]
    PFV -.->|"FAIL"| ManualPlan[/"🧑‍💻 /niko-plan"/]

    NikoBuild --Spawn--> QA
    subgraph QASA["QA subagent"]
        direction LR
        QA{"🐱 qa"} --> QAV(["Verdict"])
    end
    QAV -->|"PASS"| NikoReflect["🐱 reflect"]
    NikoReflect -.-> ManualArchive[/"🧑‍💻 /archive"/]
    QAV -->|"FAIL (fixable)"| NikoBuild
    QAV -.->|"FAIL (rearchitect)"| ManualPlan

    ManualPlan -.-> NikoPlan
```

Automatic continuation reads clearly: solid out of `Verdict` into `build` / `reflect`. The subgraph still says those edges are *results leaving the subagent*, not the QA diamond walking into reflect. Dashed stays “needs operator” (FAIL rearchitect, archive, replan).

**C.2b — Label `returns` + dotted stroke on all Verdict outs**

```mermaid
graph TD
    Start(("Complexity Analysis")) --> NikoPlan["🐱 plan"]
    NikoPlan --Spawn--> PF
    subgraph PFSA["Preflight subagent"]
        direction LR
        PF{"🐱 preflight"} --> PFV(["Verdict"])
    end
    PFV -.->|"returns PASS"| NikoBuild["🐱 build"]
    PFV -.->|"returns FAIL"| ManualPlan[/"🧑‍💻 /niko-plan"/]

    NikoBuild --Spawn--> QA
    subgraph QASA["QA subagent"]
        direction LR
        QA{"🐱 qa"} --> QAV(["Verdict"])
    end
    QAV -.->|"returns PASS"| NikoReflect["🐱 reflect"]
    NikoReflect -.-> ManualArchive[/"🧑‍💻 /archive"/]
    QAV -->|"FAIL (fixable)"| NikoBuild
    QAV -.->|"returns FAIL (rearchitect)"| ManualPlan

    ManualPlan -.-> NikoPlan
```

`returns` stresses handoff. Cost: if every Verdict edge is dotted, you **lose** solid = autonomous vs dashed = operator — PASS and FAIL look the same stroke, and Reflect→Archive no longer unique. (C.2b above accidentally keeps FAIL fixable solid — that’s the tension.)

**C.2c — Label `reports` + keep solid/dashed legend**

```mermaid
graph TD
    Start(("Complexity Analysis")) --> NikoPlan["🐱 plan"]
    NikoPlan --Spawn--> PF
    subgraph PFSA["Preflight subagent"]
        direction LR
        PF{"🐱 preflight"} --> PFV(["Verdict"])
    end
    PFV -->|"reports PASS"| NikoBuild["🐱 build"]
    PFV -.->|"reports FAIL"| ManualPlan[/"🧑‍💻 /niko-plan"/]

    NikoBuild --Spawn--> QA
    subgraph QASA["QA subagent"]
        direction LR
        QA{"🐱 qa"} --> QAV(["Verdict"])
    end
    QAV -->|"reports PASS"| NikoReflect["🐱 reflect"]
    NikoReflect -.-> ManualArchive[/"🧑‍💻 /archive"/]
    QAV -->|"reports FAIL (fixable)"| NikoBuild
    QAV -.->|"reports FAIL (rearchitect)"| ManualPlan

    ManualPlan -.-> NikoPlan
```

### Edge vocabulary note

| Choice | Reading | Risk |
| --- | --- | --- |
| Bare `PASS` / `FAIL` | Outcome only; subgraph+Verdict carry “from subagent” | Least ink; relies on shape |
| `returns PASS` | Handoff / control back to parent | Sounds like a call stack; fine |
| `reports PASS` | Subagent’s output artifact | Slightly more “status file” flavored; also fine |
| Solid Verdict→next | Parent auto-continues (T1) | Same as today’s legend |
| Dotted all Verdict outs | “Not the subagent advancing” | Collides with dashed = operator input |

**Recommendation while you look at L2:** prefer **C.2a** (or C.2c if you want a verb). Keep **solid/dashed = auto vs operator**. Let the **subgraph + Verdict + Spawn** do the subagent storytelling — don’t spend the stroke channel on “returns,” or you have to rewrite the whole legend.

#### C.2 — “Terminal node” vs Spawn (operator concern)

Established Niko pattern: a **terminal node** is one whose *only* outbound edges are dashed (operator must continue) — Reflect → Archive, L3 Preflight → `/niko-build`.

| Chart | Looks good? | “Terminal node” honesty | Parent-driver risk |
| --- | --- | --- | --- |
| **C.2a** | Yes — solid PASS shows auto-continue | If we call QA/preflight terminal, we **lie**: solid lines leave Verdict | Low — solid means continue |
| **C.2b** | Weaker — PASS and operator edges same stroke | Can call Verdict terminal (only dotted outs) | **High** — parent pattern-matches dashed → STOP and wait |

Trying C.2b “to keep the word terminal” burns the stroke legend and may halt L2 after preflight/QA. Trying C.2a while still saying “QA is a terminal node” in parent-facing prose is the dealbreaker you suspect.

**Prose fix (keep C.2a, don’t overload terminal):**

- **Parent POV:** these are **Spawn** phases, not terminal nodes. Parent forks, receives Verdict, follows the edge (solid = go, dashed = stop for operator). Parent does *not* terminate when it Spawns.
- **Subagent POV:** the subgraph ends at **Verdict** — that agent stops; it never takes the outbound edge into build/reflect. Skill Step 4 can say stop / end of verification without the parent-workflow phrase “terminal node.”
- **Reserve “terminal node”** for nodes that still match the old definition (only dashed outs): Reflect, and any 🧑‍💻 handoff targets’ predecessors that already use that list.

Legend sketch:

> - `--Spawn-->` = parent forks a subagent to run that phase; do not run it in this conversation  
> - Subagent ends at `Verdict`; outbound edges from `Verdict` are taken by the **parent**  
> - Solid / dashed keep their meaning: auto vs operator  
> - **Terminal node** = only dashed outs (unchanged); Spawn/Verdict phases are not terminal nodes

That keeps pattern matching for “terminal,” keeps C.2a’s look, and puts the subagent stop where it belongs (child + Spawn wording), not in the parent’s STOP list.

### D — Dual subgraph (parent vs verifier) — clearest ownership

```mermaid
graph LR
    subgraph P["Parent"]
        Start(("Complexity Analysis")) --> NikoBuild["🐱 Build"]
        NikoBuild --> Fork["fork QA"]
        Gate{"result"} -->|"PASS"| Done("Done")
        Gate -->|"FAIL"| NikoBuild
    end
    subgraph V["QA subagent"]
        QA{"🐱 QA"} --> Halt(["stop"])
    end
    Fork -.-> QA
    Halt -.-> Gate
```

| Pros | Cons |
| --- | --- |
| Ownership unmistakable: only Parent reaches Done | Heaviest L1 diagram; L2/L3 get large |
| Scales: add Preflight subgraph the same way | More ceremony than Niko’s usual LR strip |
| Supports T1 (solid inside Parent) or T2 (dashed Parent edges) | |

### E — Sequence diagram (different type for verification handoff)

Keep a simple LR flowchart for phases, **or replace L1 chart** with:

```mermaid
sequenceDiagram
    participant P as Parent
    participant Q as QA subagent
    P->>P: Build
    P->>Q: fork niko-qa
    Q-->>P: PASS / FAIL
    Note over Q: stop — never advances workflow
    alt PASS
        P->>P: Done / wrap-up
    else FAIL
        P->>P: Build
    end
```

| Pros | Cons |
| --- | --- |
| Best at “Q never progresses” | Breaks flowchart-only consistency across levels |
| Matches how harnesses actually fork | FAIL→Build loop is clumsier in sequence form |
| | Operator would maintain two diagram dialects |

**Hybrid:** keep `graph LR` for the phase strip; add a tiny sequence under “Verification” — usually too much for L1.

### F — Phase-terminal like L3 preflight (T2, minimal new shapes)

Reuse existing dashed + 🧑‍💻 grammar; QA does not solid-edge to Done:

```mermaid
graph LR
    Start(("Complexity Analysis")) --> NikoBuild["🐱 Build"]
    NikoBuild --> NikoQA{"🐱 QA"}
    NikoQA -.->|"PASS"| ManualDone[/"🧑‍💻 wrap-up \/ Done"/]
    NikoQA -->|"FAIL"| NikoBuild
```

Or PASS also dashed back only via operator `/niko` / wrap-up command — exact 🧑‍💻 node label is yours to craft.

| Pros | Cons |
| --- | --- |
| Same dialect as L3 preflight + Reflect | Drops L1/L2 autonomous PASS continuity (behavior change) |
| No subgraph; Niko-familiar | Does not draw “subagent” — only “terminal phase” |
| Recovery path matches the chart | “Subagent” may still need one legend line |

**Pattern fit:** Strongest consistency with *existing* terminal phases; weakest at depicting fork.

### G — Shape cue + T2/T1 edge choice (light touch)

Use a distinct shape for verification diamonds (e.g. subroutine `[["🐱 QA"]]` or stadium) plus legend: “verification shape = forked subagent; node is terminal for that agent.”

```mermaid
graph LR
    Start(("Complexity Analysis")) --> NikoBuild["🐱 Build"]
    NikoBuild --> NikoQA[["🐱 QA"]]
    NikoQA -->|"PASS"| Done("Done")
    NikoQA -->|"FAIL"| NikoBuild
```

| Pros | Cons |
| --- | --- |
| Small diff; greppable shape | Shape semantics are easy to forget |
| Works with T1 or T2 edge style | Still looks like QA owns PASS→Done unless edges change too |

---

## Analysis

| Criterion | A Legend | B Gate | C Child subgraph | D Dual subgraph | E Sequence | F T2 dashed | G Shape |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Shows subagent can’t advance | Weak | Medium | Strong | Strongest | Strongest | Medium (phase-terminal) | Weak |
| Fits Niko chart dialect | Strong | Medium | Medium | Weak | Weak | Strongest | Strong |
| L1 simplicity | Best | OK | Busy | Busiest | OK as replace | Good | Best |
| Scales to preflight+QA | Legend only | Repeat gate | Repeat subgraph | Repeat V subgraph | Repeat seq | Same as L3 | Same shape |
| Aligns T2 “like Reflect” | Optional | Optional | Needs legend | Optional | Optional | Native | Optional |
| Agent misread risk | High | Low | Medium | Low | Low | Low | High |

Key insights:

- **Depicting “subagent” and “phase-terminal (T2)” are separable.** F gives you T2 with almost no new notation; D/E give you subagent ownership; you can combine F’s edge semantics with a one-line legend for fork.
- **Dashed already means operator input** in L2–L4 legends. Using dashed for “return from subagent” without a legend edit will be misread. Either keep dashed = operator (T2) or add a third edge kind (messy) or use subgraph returns with an explicit legend line.
- **L1 Wrap-Up is already a parent-side terminal ritual** after QA PASS (reconcile, commit, STOP). Today’s chart lies by drawing `QA → Done` as if QA performed Done. Even under T1, a Parent gate or Wrap-Up node would be more honest than an edge out of the QA diamond.
- **Do not overload Step 4 skill prose to carry chart semantics** — you asked for charts first; skills should later say “stop” in the same vocabulary as the legend (terminal / STOP and wait).

---

## Decision

**None selected — low confidence by design.** Operator will choose or hybridize.

### Soft recommendation (non-binding)

If the goal is **one grammar for all levels** and you meant **T2 (like L3 preflight / Reflect)**: start from **F**, add **one legend line** that verification runs in a forked subagent. No subgraph on L1.

If the goal is **show the subagent cycle** and keep **T1 parent automation**: start from **D** (or **B** if you refuse subgraphs), keep solid edges inside Parent.

If you want **maximum honesty on L1 with minimum novelty**: **B** with the PASS node labeled as today’s Wrap-Up, not a vague “Done.”

### Implementation notes (after you pick)

1. Edit `level1-workflow.md` mermaid + legend (+ “STOP and wait” list if T2).
2. Mirror the same grammar onto L2–L4 charts (preflight + QA).
3. Only then percolate: phase mappings one-liner, skill Step 4 / Handle Results, secondary call sites, README — vocabulary aligned to the legend (“terminal”, dashed, STOP).
4. Strike brief requirement “mermaid stay as-is” / out-of-scope “no redraw” (superseded).

### Validation

Renditions B–G were checked with `mmdc` (parse/render). Fix forward if a chosen hybrid fails render on GitHub.
