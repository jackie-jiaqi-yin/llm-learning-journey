# LLM Post-Train

Recurring arXiv summaries for LLM post-training research, including instruction tuning, preference optimization, reinforcement learning, alignment, evaluation, and post-training data design.

## Automation Contract

- Weekly cadence: Wednesday 19:00 America/Los_Angeles.
- Window: last 7 days.
- Entry title: `## YYYY-MM-DD`, using the automation run date in America/Los_Angeles.
- HTML report path: `reports/llm-post-train/YYYY-MM-DD.html`.
- Only the Markdown entry and copied HTML report are retained after each successful run.

<!-- arxiv-topic: llm-post-train -->
<!-- arxiv-runs:start -->
<!-- Future automation: insert the newest run below as "## YYYY-MM-DD" and keep runs in reverse chronological order. -->

## 2026-05-24

- Report: [HTML report](reports/llm-post-train/2026-05-24.html)
- Window: last 7 days
- Papers summarized: 66
- Date range: 2026-05-18 to 2026-05-22
- Query scope: LLM post-training, instruction tuning, SFT, preference optimization, RLHF/RLAIF/GRPO/DPO, reward modeling, and post-training data design.

### Key Themes

- **Credit assignment is the center of gravity.** Several papers treat outcome-level RLVR as too sparse for reliable reasoning training. SCRL derives verifiable subproblems from reasoning chains, OPPO estimates token-level success probabilities, DASD routes self-distillation by token uncertainty, and AVSPO/AGPO/NSR diagnose GRPO failures such as advantage collapse, fixed clipping, and discarded near-boundary signals.
- **Post-training is shifting from loss choice to state control.** The most useful conceptual frame is that SFT, RL, and on-policy distillation differ by the state distributions that receive supervision. ACC compiles agent trajectories into long-context QA data, OPCT trains safety consistency on the model's own responses, and Memory-R2/ReBel show why long-horizon agents need memory-aware or belief-aware credit assignment.
- **Open-ended alignment needs richer reward structure.** ARES generates question-specific rubrics for open-ended RL, GPRL represents preference as multidimensional comparison rather than a scalar reward, and LambdaPO uses pairwise rollout comparisons instead of a single group mean baseline.
- **Safety auditing must be post-training-specific.** New work argues that geopolitical bias can originate in chat post-training, instruction tuning can sharpen commitment into confident hallucination, and targeted fine-tuning data can poison narrow task families while leaving general benchmarks clean.
- **Efficiency and infrastructure are becoming part of the research agenda.** COALA, FuRA, Pion, MXFP4 correction, Quant.npu, torchtune, and Frontier all make the same point from different layers: rollout-heavy post-training has to be designed with compute, precision, serving, and reproducibility in mind.

### Notable Papers to Read First

- [Post-Training is About States, Not Tokens](https://arxiv.org/abs/2605.22731v1) - the cleanest conceptual frame for comparing SFT, RL, and on-policy distillation.
- [ARES](https://arxiv.org/abs/2605.23454v1) - a practical recipe for scalable rubric-based RL on open-ended tasks.
- [From Reasoning Chains to Verifiable Subproblems](https://arxiv.org/abs/2605.22074v1) - a strong example of turning long reasoning traces into denser verifiable supervision.
- [Advantage Collapse in GRPO](https://arxiv.org/abs/2605.21125v1) - useful for understanding why GRPO batches can stop producing meaningful gradients.
- [On-Policy Consistency Training](https://arxiv.org/abs/2605.21834v1) - a safety alignment paper that avoids much of the capability degradation seen with offline SFT consistency training.
- [General Preference Reinforcement Learning](https://arxiv.org/abs/2605.18721v3) - a clear argument for multidimensional preference RL on open-ended generation.

### Practical Takeaways

- If you are learning post-training, start by tracking the **unit of supervision**: token, subproblem, trajectory, group, state, memory, or preference dimension.
- Treat default GRPO as a baseline, not a finished algorithm. This week's papers mainly improve its credit assignment, clipping, grouping, exploration, or reward geometry.
- For open-ended tasks, rubric quality and reward dimensionality are now core design choices. Scalar reward models are increasingly treated as too easy to game.
- For safety, always compare base vs chat behavior and test multilingual/adversarial prompt variants. Post-training can add risks that are invisible in pretraining-only analysis.
- For implementation, do not separate algorithm design from systems constraints. Low-bit arithmetic, serving architecture, rollout cost, and reproducibility all affect whether a method is usable.

<!-- arxiv-runs:end -->

## Topic Scope

I want this page to track papers that explain how pretrained models are adapted into useful, aligned, and domain-capable assistants.

Useful subtopics:

- Supervised fine-tuning and instruction tuning
- Preference data and reward modeling
- RLHF, RLAIF, DPO, GRPO, and related methods
- Reasoning-oriented post-training
- Evaluation after post-training
- Data quality, filtering, and synthetic data pipelines
