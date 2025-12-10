# Invited talk: On the Science of “Alien Intelligences”: Evaluating Cognitive Capabilities in Babies, Animals, and AI
[Video Recording](https://neurips.cc/virtual/2025/invited-talk/109607)

**Introduction and Context**

- Melanie Mitchell keynote at NeurIPS 2025 on evaluating “alien intelligences”
- Focus on rigorous methods for assessing cognitive capabilities across babies, animals, and AI
- Conference has grown significantly since 1990s (few hundred to current scale)

**Benchmark and Evaluation Method Problems**

- Current AI benchmarking approach fundamentally flawed
    - Nature headline: benchmarks saturated, systems scoring better than humans
    - NYT: “AI has a measurement problem”
    - Technology Review: “terrible” progress measurement methods
- Core issues with benchmark performance:
    - Data contamination (test data in training sets)
    - Approximate retrieval (similar questions enable pattern matching)
    - Exploitable spurious associations or shortcuts
    - No testing for consistency, robustness, or generalization
    - Lack of construct validity (passing bar exam ≠ practicing law)
    - Anthropomorphism assumptions (human test design doesn’t translate to AI)

**Six Principles for More Rigorous Evaluation of Cognitive Capacities**

1. **Cognitive Bias Awareness**
    - Recognize anthropomorphism tendencies
    - Example: monkey “smile” = fear grimace, not happiness
    - Eliza effect: fluent language triggers human quality attribution
2. **Skeptical Hypothesis Testing**
    - Always consider alternative explanations
    - Clever Hans example: horse appeared to do math but actually read facial cues
    - Required control experiments: questioner knowledge, visual access
    - Recent infant morality study: babies chose “helper” vs “hinderer” characters
        - Confound discovered: bounce animation at top (helper) vs bottom (hinderer)
        - When bounce controlled: babies followed bounce location, not moral preference
3. **Analyze Failure Types**
    - Failures more insightful than successes for understanding systems
    - Psychology uses human errors to understand cognition
    - Field bias against negative results (“killjoy explanations”)
    - Journal of Negative Results exists but low impact
4. **Design Novel Variations for Robustness Testing**
    - Mitchell’s analogical reasoning research example
    - UCLA study: GPT-3 outperformed undergrads on letter string analogies
    - Robustness test: counterfactual alphabets (M and E swapped, symbol sequences)
    - Results: humans maintained performance, AI models failed dramatically
    - Importance: test generalization beyond original benchmark conditions
5. **Performance vs. Competence Distinction**
    - System may understand rules but lack execution ability
    - Abstraction and Reasoning Corpus (ARC) example:
        - Chollet’s 1000 tasks based on core knowledge priors
        - O3 model achieved 88% (high reasoning) vs 64% human performance
        - But analysis of reasoning strategies revealed differences
    - Mitchell’s simplified ARC study (480 tasks, 16 concepts):
        - Asked for both output grids AND stated transformation rules
        - O3 often correct output but “alien” reasoning (using color numbers vs visual concepts)
        - Visual input: models performed poorly but often had correct rules
        - Competence present despite poor performance
6. **Replicate and Build on Others’ Results**
    - Converging evidence across multiple experimental tasks essential
    - Academic bias against “incremental” replication work
    - Replication and incremental extension = hallmark of good science

**Conclusion**

- Don’t just need harder benchmarks (like “humanity’s last exam”)
- Need more rigorous evaluation methods with substantial creativity
- High accuracy doesn’t guarantee intended abstraction recognition
- Low accuracy may mask competence issues rather than fundamental incapability
- AI systems need human-like world understanding for safe interaction
- Accuracy alone can mask exploitation of superficial features and non-human reasoning patterns