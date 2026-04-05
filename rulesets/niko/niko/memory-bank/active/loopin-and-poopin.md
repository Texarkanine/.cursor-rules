# Unrolled Prompts Beat Loops: Evidence from Instruction Compounding, Attention Bias, and Transformer Architecture Research

**No study directly compares "for each item, do X" against fully-unrolled per-item instruction blocks in a controlled experiment.** This is a clear gap in the literature. However, converging evidence from at least a dozen adjacent research programs — spanning instruction-following benchmarks, batch processing studies, attention mechanism analysis, and official AI lab guidance — points decisively toward the same conclusion: **explicit, per-item instruction blocks improve instruction adherence over abstract loop constructs, with the advantage growing as set size and step complexity increase.** The effect is driven by multiplicative failure compounding, positional attention bias, and the fundamental properties of causal masking in transformers. The practical crossover point appears to be around 4–6 items for simple tasks, shrinking to 2–3 items for complex multi-step procedures.

## The "curse of instructions" makes loops exponentially fragile

The strongest quantitative evidence comes from the **ManyIFEval benchmark** (Harada et al., ICLR 2025)[^1], which discovered a devastating mathematical relationship: the probability of an LLM following all instructions simultaneously equals the individual instruction success rate raised to the power of the total instruction count. At a 95% per-instruction success rate, 10 simultaneous instructions yield just 60% all-correct compliance. Empirically, GPT-4o achieved only 15% success with 10 simultaneous instructions; Claude 3.5 Sonnet managed 44%. Self-refinement loops improved these to 31% and 58% respectively, but the exponential penalty remained.[^1]

This finding has direct implications for loop-style prompts. When a prompt says "for each of 10 items, follow these 5 steps," the model must satisfy 50 effective constraints in a single generation. The multiplicative decay means that even individually easy steps compound into near-certain failure at scale. Unrolling into separate per-item calls keeps each call at 5 constraints, preserving the per-instruction success rate without cross-item compounding.

The **IFScale benchmark** (Jaroslawicz et al., July 2025)[^2] extended this finding to 500 simultaneous keyword-inclusion instructions across 20 state-of-the-art models. Even the best frontier models achieved only 68% accuracy at 500 instructions. Crucially, the study identified three distinct degradation patterns across model families: **threshold decay** for reasoning models like o3 and Gemini-2.5-Pro (near-perfect until ~150 instructions, then collapse), **linear decay** for GPT-4.1 and Claude-Sonnet-4, and **exponential decay** for GPT-4o and Llama-4-Scout.[^2] This means the choice between loop and unrolled prompts is partly model-dependent — reasoning models tolerate higher instruction density before degradation kicks in.

## Instance count matters more than context length

A March 2026 study on multi-instance processing (Chen et al.)[^3] provides the most directly relevant evidence. It found that the number of instances processed in a single prompt has a stronger effect on performance than total context length alone. All tested LLMs followed the same pattern: slight degradation for small instance counts (approximately 20–100), followed by performance collapse on larger counts. Tasks that models handled perfectly in isolation degraded significantly when batched together — even when the total token count remained well within context window limits.

The batch prompting literature reinforces this. The seminal EMNLP 2023 paper on batch prompting (Cheng et al.)[^4] found that batch size 4 was the sweet spot, balancing cost savings (up to 5× fewer API calls) against quality. The ICLR 2024 follow-up, BatchPrompt[^5], confirmed that naïve batching degrades accuracy and showed that LLM performance varies significantly depending on where data appears within a batch — a direct consequence of autoregressive generation. Their Batch Permutation and Ensembling technique (running the same batch in multiple orderings and voting) could recover single-item accuracy, but at the cost of multiple API calls per batch.

A counterpoint comes from the **Multi-Task Inference** benchmark (February 2024)[^6], which found that for 2–3 closely related subtasks sharing context, batching them together actually improved performance by up to 12.4% on GPT-4. This suggests a small-batch regime where cross-item context sharing outweighs the compounding penalty — but only for very small sets of related items.

## Why it happens: attention sinks, causal masking, and the lost middle

The mechanistic explanation for why unrolled prompts work better draws on three well-established phenomena in transformer architecture research.

**Lost in the middle.** The landmark study by Liu et al. (TACL 2024)[^7] demonstrated a U-shaped performance curve: LLMs access information at the beginning and end of their context with 30%+ higher accuracy than information in the middle. A follow-up paper, "Found in the Middle" (Hsieh et al., ACL Findings 2024)[^8], traced this to an intrinsic attention bias — LLMs exhibit U-shaped attention allocation regardless of content relevance. In a loop-style prompt processing 50 items, items 10–40 land squarely in the degraded middle zone. Unrolling gives every item its own beginning and end.

**Attention sinks.** Research from MIT (Xiao et al., ICLR 2024)[^9] revealed that LLMs dump disproportionate attention onto initial tokens due to softmax normalization — a phenomenon called "attention sinks." A 2025 follow-up[^10] confirmed this is an intrinsic architectural property, not input-dependent, and that it emerges more strongly with longer contexts. In a loop-style prompt, the initial instruction block becomes the attention sink while middle items are starved. Unrolling creates fresh attention sinks at each item's instruction header.

**Causal masking and prompt repetition.** Google Research's December 2025 "Prompt Repetition" paper (Leviathan, Kalman, Matias)[^11] provides perhaps the most elegant evidence. Simply duplicating the entire prompt improved accuracy by up to 76% — on one task, Gemini 2.0 Flash Lite jumped from 21.33% to 97.33%.[^12] The mechanism: in causal (left-to-right) attention, instruction tokens are processed before data tokens, meaning the instruction encoding lacks awareness of the data it must operate on. When instructions are repeated after the data (or, by extension, repeated per-item), each instruction instance can attend to all preceding context, creating a richer instruction signal. Padding the prompt to equivalent length without repetition produced no improvement, confirming the gain comes from information repetition, not length.[^11]

## What the AI labs actually recommend

No major lab frames guidance as "loop vs. unrolled," but their recommendations map directly onto this distinction.

**Anthropic's prompt chaining documentation**[^13] states that breaking complex tasks into subtasks gives each subtask Claude's full attention, reducing errors, and offers an optimization tip: for tasks with independent subtasks (like analyzing multiple docs), create separate prompts and run them in parallel. Anthropic's recommended multi-document structure uses explicit per-item XML tagging (`<document index="1">...</document>`)[^14], which is essentially structural unrolling within a single prompt.

**OpenAI's GPT-4.1 prompting guide**[^15] contains the most direct acknowledgment, noting that in some isolated cases the model resists producing very long, repetitive outputs (e.g., analyzing hundreds of items one by one) and recommending that developers instruct the model strongly or consider breaking down the problem. For structural markers within prompts, they found XML performed well for multi-document inputs while JSON performed particularly poorly.[^15]

**Google's prompt repetition research**[^11] suggests a middle path: if you must use a loop-style prompt, repeating the core instruction block after each item (partial unrolling) can recapture much of the benefit.

## Set size, step complexity, and model family all matter

The evidence allows specific answers to the sub-questions:

**Does set size matter?** Yes, dramatically. The relationship is exponential, not linear. Batch prompting research finds quality holds at batch sizes of 2–4 items[^4], begins degrading at 5–10, and collapses beyond 20–100 items depending on the model[^3]. Reasoning models like o3 and Gemini-2.5-Pro maintain performance up to roughly 150 simple instructions before threshold collapse, while non-reasoning models like GPT-4o and Llama-4-Scout show exponential decay from the start.[^2]

**Does step complexity matter?** Yes. The LogiSafetyBench study (2025)[^16] compared workflow-oriented instructions (explicit step-by-step scaffolding) against goal-oriented instructions (abstract, high-level intent) and found GPT-5 dropped from 75% to 28% compliance when explicit scaffolding was removed. The Chain-of-Instructions study[^17] showed progressive degradation across chained subtask positions: ROUGE-L scores dropped from 81.49 for subtask 1 to 32.73 for subtask 3 in a three-step chain.

**Do different model families handle this differently?** Markedly. A comparative study in MDPI Electronics (2024)[^18] found no definitive rule favoring single-task prompts over multitask prompts; rather, their relative performance is highly contingent on the specific model's data and architecture. Among five open-weight models tested, some performed better with multitask prompts and others degraded. The IFScale benchmark's three degradation patterns — threshold, linear, and exponential — map roughly to reasoning models, large frontier models, and smaller/older models respectively.[^2] Reasoning models benefit least from unrolling because their internal chain-of-thought already provides a form of "re-reading" that mimics the prompt repetition effect.

**Do structural markers help?** Yes. Both Anthropic[^14] and OpenAI[^15] recommend XML tags for multi-item prompts, with Anthropic specifically advocating indexed document tags. OpenAI's long-context testing confirmed XML outperforms JSON for document-based inputs. The Instruction Boosting paper (Guardieiro et al., June 2025)[^19] formalizes this as a competition between instruction rules and context-derived rules, with attention acting as the mediator. Clear structural markers increase the attention signal allocated to instruction tokens, reducing the chance of context overriding instructions.

## Practical decision framework for prompt architects

The evidence converges on a clear decision matrix, which depends primarily on three variables: item count, per-item complexity, and whether items need cross-referencing.

- **1–3 simple items needing comparison**: Use a loop-style prompt with XML-tagged items. The batch regime is small enough that compounding penalties are minimal, and cross-item context sharing may actually help.[^6]
- **4–6 simple items, independent**: Use a single prompt with per-item XML structure and instructions repeated at both the beginning and end. This is the "partially unrolled" sweet spot identified by batch prompting research.[^4][^5]
- **7+ items or complex multi-step procedures**: Fully unroll into separate API calls. Use Batch APIs from Anthropic or OpenAI for cost savings. Each call gets the model's full attention with no positional degradation.[^3]
- **Any number of items on weaker/smaller models**: Default to unrolling. Smaller models (7B–13B range) show the steepest degradation curves.[^2]
- **Reasoning models (o3, Gemini-2.5-Pro)**: More tolerant of loop-style prompts, but still degrade past ~150 instruction density. Unrolling still helps for complex tasks.[^2]

If you must keep items in a single prompt, three mitigation strategies improve compliance: **repeat the core instruction block** after each item or at the end of the prompt[^11], use **indexed XML tags** for each item[^14], and add a **self-verification step** asking the model to check whether it completed all items (per the self-refinement results in the Curse of Instructions paper, which improved 10-instruction compliance from 15% to 31%)[^1].

## Conclusion

The case for unrolled prompts over loop-style abstractions rests on strong indirect evidence across multiple research programs, even though no one has published the direct A/B comparison. The exponential compounding of instruction failures[^1], the U-shaped attention bias that penalizes middle items[^7][^8], and the causal masking mechanism that weakens instruction signals far from their data[^11] all point the same direction. The practical threshold sits at roughly 4–6 items for simple tasks and 2–3 items for complex multi-step procedures — beyond these, unrolling delivers measurably better instruction adherence. The most important insight may be the prompt repetition finding: it is not merely that fewer items helps, but that each item seeing its own copy of the instructions is mechanistically superior in a causal attention architecture. The instruction tokens, when repeated near each data block, encode richer contextual representations that improve downstream compliance. This represents a genuine architectural insight, not just a prompting trick — and it suggests that the most effective prompt structure is one that mirrors the transformer's own attention economics.

---

[^1]: Harada et al., "Curse of Instructions: Large Language Models Cannot Follow Multiple Instructions at Once," ICLR 2025. <https://openreview.net/forum?id=R6q67CDBCH>
[^2]: Jaroslawicz et al., "How Many Instructions Can LLMs Follow at Once?" July 2025. <https://arxiv.org/html/2507.11538v1>
[^3]: Chen et al., "Understanding LLM Performance Degradation in Multi-Instance Processing: The Roles of Instance Count and Context Length," March 2026. <https://arxiv.org/abs/2603.22608>
[^4]: Cheng et al., "Batch Prompting: Efficient Inference with Large Language Model APIs," EMNLP 2023. <https://ar5iv.labs.arxiv.org/html/2301.08721>
[^5]: "BatchPrompt: Accomplish more with less," ICLR 2024. <https://arxiv.org/html/2309.00384v3>
[^6]: "Multi-Task Inference: Can Large Language Models Follow Multiple Instructions at Once?" February 2024. <https://arxiv.org/abs/2402.11597>
[^7]: Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," TACL 2024. <https://arxiv.org/abs/2307.03172>
[^8]: Hsieh et al., "Found in the Middle: Calibrating Positional Attention Bias Improves Long Context Utilization," ACL Findings 2024. <https://arxiv.org/abs/2406.16008>
[^9]: Xiao et al., "Efficient Streaming Language Models with Attention Sinks," ICLR 2024. <https://arxiv.org/html/2309.17453v3>
[^10]: "Why do LLMs attend to the first token?" April 2025. <https://arxiv.org/html/2504.02732v1>
[^11]: Leviathan, Kalman, Matias, "Prompt Repetition Improves Non-Reasoning LLMs," Google Research, December 2025. <https://arxiv.org/pdf/2512.14982>
[^12]: Coverage and discussion of the prompt repetition findings: Analytics Vidhya, <https://www.analyticsvidhya.com/blog/2026/02/prompt-repetition/>; VentureBeat, <https://venturebeat.com/orchestration/this-new-dead-simple-prompt-technique-boosts-accuracy-on-llms-by-up-to-76-on>; PromptLayer, <https://blog.promptlayer.com/prompt-repetition-improves-llm-accuracy/>
[^13]: Anthropic, "Chain complex prompts for stronger performance," Claude API Docs. <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-prompts>
[^14]: Anthropic, "Use XML tags to structure your prompts," Claude API Docs. <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags>
[^15]: OpenAI, "GPT-4.1 Prompting Guide," OpenAI Cookbook. <https://cookbook.openai.com/examples/gpt4-1_prompting_guide>
[^16]: "Evaluating Implicit Regulatory Compliance in LLM Tool Invocation via Logic-Guided Synthesis," 2025. <https://arxiv.org/html/2601.08196>
[^17]: "Chain-of-Instructions: Compositional Instruction Tuning on Large Language Models." Reviewed at <https://liner.com/review/chainofinstructions-compositional-instruction-tuning-on-large-language-models>
[^18]: "Comparative Analysis of Prompt Strategies for Large Language Models: Single-Task vs. Multitask Prompts," MDPI Electronics, 2024. <https://www.mdpi.com/2079-9292/13/23/4712>
[^19]: Guardieiro et al., "Instruction Following by Principled Boosting Attention of Large Language Models," June 2025. <https://arxiv.org/abs/2506.13734>