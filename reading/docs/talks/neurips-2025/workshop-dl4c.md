# Workshop: Deep Learning for Coding (DL4C)
[Recording](https://neurips.cc/virtual/2025/loc/san-diego/workshop/109562)

## **Lessons from the Trenches on building usable coding agent**
[GitHub Repository](https://github.com/OpenHands/OpenHands)
**Lesson 1. Believe in simplicity**

- Agent architecture evolution
    - MetaGPT approach: multi-agent system with boss agent, product manager agent, architect agent, project manager agent, engineer agent
    - OpenHands approach: single flexible agent that can think on the fly
    - Software engineering is incredibly diverse - fixed workflows break when tasks go off expected path
    - Single agent architecture proves more effective for varied tasks
- Tool philosophy: minimal but powerful toolset
    - Started with large toolbox approach, settled on minimal set
    - Core tools provided to agent:
        1. Bash Terminal - for system interactions
        2. Python/Jupyter notebook - for complex programming tasks
        3. File editor - direct file editing (like IDE)
        4. Visual web browser - for debugging frontends, viewing PDFs
        5. Search API - for online information gathering
    - Can leverage existing libraries (GitHub library, etc.) through these core tools
    - Generally use tools created for human programmers

**Lesson 2: Code don’t click**

- GUI vs API performance comparison on WebArena benchmark
    - GUI-based agent (clicking through interfaces): 15% accuracy
    - API-based agent (direct API calls): 29% accuracy
    - Hybrid agent (API when available, GUI when necessary): 39% accuracy
    - Nearly tripled accuracy by changing interaction format
- API quality impact
    - Performance gains much larger on sites with good APIs vs poor APIs
    - Controlled experiment: adding APIs to Reddit site nearly doubled accuracy with just 1-2 days manual work
    - Similar concept to MCP (Model Control Protocol) - prefer computer interfaces over human interfaces

**Lesson 3. Agentic training is essential**

- Requirements for agentic language models:
    1. Instruction following ability - especially with long context
    2. Tool use/coding abilities - both writing code and using tools properly
    3. Environment understanding - GUI programming, visual browsers, domain-specific knowledge
    4. Error awareness/recovery abilities - try new strategies instead of repeating mistakes
    5. Reasonable cost
- Current challenge: no model has all requirements simultaneously
- Training approaches:
    1. Reinforcement learning (SWE-Gym)
        - First RL algorithm for software engineering tasks
        - Convert SweeBench samples into RL environment
        - Generate rollouts, reward based on unit test success
    2. Synthetic data (GoBrowse method)
        - LLM explores websites, proposes tasks, tests feasibility
        - Restart exploration from previously explored areas for deeper navigation
    3. Human demonstrations
        - Most expensive approach
        - Google collected 689k multimodal demos for Android navigation
- Agent Data Protocol
    1. Standardized format for 1.7 million agent trajectories
    2. Addresses problem of every dataset having different formats
    3. Enables easy conversion to training formats for different agent frameworks
    4. Demonstrated improvements across OpenHands, SWE-Agent, and Agent-Lab

**Lesson 4: Benchmarking must be ecologically valid**

- VersaBench: opinionated suite covering real user cases
    - SweeBench for core coding tasks
    - SweeBench Multimodal for frontend programming
    - Multi-SWE for different programming languages
    - CI failure fixing (pre-commit checks, linting)
    - Information gathering tasks
    - CommitZero for creating new apps from scratch
    - Agent Company for navigating software company tasks
    - SWE-Bench for software testing
- Human-in-the-loop evaluation methodology
    - Step 1: Collect agent trajectories with user feedback (1-5 rating)
    - Step 2: Train model to predict user ratings from trajectory data
    - Step 3: Use model to evaluate interventions without waiting for human feedback
    - Step 4: Compute effect sizes for different model/system changes
    - 8-9% feedback rate from users (high for this type of system)
- Key findings from user satisfaction analysis
    - Claude 3.7 to Claude 4: statistically significant improvement
        - Fewer misunderstood intentions, less error rate, fewer git resets
    - Claude 4 vs GPT-4o: users preferred Claude 4
        - GPT-4o slower, less responsive interface design
    - Benchmark correlation: strong for Claude 3.7 vs 4, weak for Claude 4 vs GPT-4o due to non-functional factors

**Lesson 5: Agent should adapt with us**

- Handling under-specificity problem
    - Created dataset by removing details from SweeBench Verified issues
    - Performance dropped ~50% with under-specified tasks
    - Simulated user interaction improved performance significantly
    - Built RL environment for training proactive questioning behavior
    - Trained models beat GPT-4o on overall evaluation metrics
- Agent personalization and learning
    - Agent Workflow Memory: automatically evaluates task success, induces workflows, feeds back to agent memory
    - Agent Skills Induction: generates reusable code functions from successful trajectories
    - Both approaches completely unsupervised - can run during normal usage
    - Significantly improves success rate and efficiency
    - Can turn GUI navigation into APIs through learned skills

## **Predicting all the error bars of LLM evaluations**

**Statistical Noise in LLM Evaluations**

- Current evaluation reliability concerns
    - Small benchmark sizes (hundreds vs thousands in ImageNet era)
    - Few percent improvements often not statistically significant
    - Agent evaluations require 100k+ tokens, hours of work per sample
- Key benchmark examples
    - HumanEval: hundreds of problems
    - SWE-bench: 500 examples in popular version
    - Contrast with ImageNet: 10k images, 100k total

**Noise Framework & Methodology**

- Three types of noise decomposition
    1. **Prediction noise**: LLM stochastic output variation
        - Measurable directly on fixed eval sets
        - Reducible via averaging, temperature control
    2. **Data noise**: Sampling variation from question set
        - Cannot be measured on fixed dataset
        - Requires resampling/bootstrapping analysis
    3. **Total noise**: Prediction + data noise
- Paired vs unpaired comparisons
    1. Paired tests much more powerful (same questions across models)
    2. Standard error scales as 1/√(number of questions)
    3. Theoretical predictions fit empirical data across benchmarks

**Key Findings & Recommendations**

- Noise levels by accuracy range
    - HumanEval: Need 10% difference for significance (unpaired), 8% (paired)
    - Prediction noise dominant at typical temperatures (0.6-1.0)
    - Data noise becomes limiting factor with infinite sampling
- Practical implications
    - Benchmark builders should report noise levels
    - Use paired comparisons when possible
    - Consider temperature tradeoffs (lower temp reduces prediction noise)
    - Hard problems don’t necessarily reduce noise due to inconsistency
- Current benchmarks show high inconsistency
    - Worse models sometimes solve harder problems than better models
    - Multi-step problems compound error probability exponentially

 

## **How to Develop in the Agentic Era**

**Evaluation Challenges in AI Systems**

- Current evaluation systems fundamentally flawed
    - Peer review example: 3-6 human annotators, 0-10 scoring with predefined rubrics
    - Binary accept/reject outcomes despite subjective scoring
    - When evaluation breaks, results can be disastrous
- Reliability vs validity concepts from psychology
    - Reliability: consistency across multiple measurements under similar conditions
    - Validity: actually measuring what you think you’re measuring
    - AI field equivalents: variance vs bias

**Common Evaluation Pitfalls**

- SWE-bench coding benchmark issues
    - Small reasoning models outperformed specialized coding models
    - Actually measured instruction following (XML format compliance) rather than coding ability
    - Low validity situation - not measuring intended capability
- Mathematics evaluation problems
    - Models trained to output answers in specific box format
    - Measuring format compliance rather than mathematical reasoning
- Human evaluation challenges
    - High variance with small annotator pools (<20 people)
    - Reliable results only with 200+ annotators
    - Bias toward specific domains (Gemini 3 Pro excelled due to web development focus in prompts)

**Programming Definitions & Evaluation Scope**

- Multiple definitions of programming
    1. Programs = algorithms + data structures (Nicholas textbook)
    2. Programs = system design + implementation
    3. Programs = organization of data (alternative perspective)
- Current benchmarks focus heavily on code generation
    1. Missing: code understanding, design, test generation, debugging
    2. Need comprehensive evaluation covering all programming aspects
- Companies build internal evaluations to cover broader scope

**Training & Scaling Considerations**

- Evaluation directly enables training improvements
    - Perfect reward computation enables perfect RL
    - Self-evaluation capabilities crucial for model development
- Scaling factors for coding agents
    - Diversity of tasks
    - Rollout length and number of tool calls
    - Diversity of tools/sandbox environments
    - Complexity beyond math/STEM domains
- Policy gradient limitations in agentic era
    - Only learns one beam of information per rollout
    - Inefficient for long-duration agent tasks (hours/days)
    - May need process supervision and step-by-step modeling

**Applications & Future Directions**

- Coding as fundamental AGI skill
    - Building block for other capabilities
    - Creative applications beyond traditional programming
    - Examples: blog writing, job applications, CLI tools
- Development focus areas
    - Training: push toward better generalization across tools/tasks/scenarios
    - Applications: design for human creativity, not limited to code writing
    - Quality over quantity in benchmark creation (100 manual examples > 10,000 auto-generated)
- Sweet spot for evaluation difficulty: 5-30% success rates for meaningful signal

## **Qwen3-Coder**

**Qwen3-Coder Model Architecture & Training**

- Flagship model: 480B total parameters, 35B activated (MOE architecture)
    - Sparse activation for efficiency while maintaining large model capabilities
    - Competitive performance: SWE-bench 37%, close to GPT-4 levels
- New BNET architecture for next generation
    - Hybrid model: 3 linear attention layers + 1 full attention layer per 4-layer block
    - Trained on 256K tokens, targeting 1M token context length
    - Motivation: enable long-horizon coding tasks (multi-day problem solving)

**Training Pipeline & Data Strategy**

- Pre-training approach: Data → coder → data → coder (iterative improvement)
    1. Synthetic data generation crucial for coding-specific capabilities
    2. SpeedFlow method generates software engineering scenarios from test cases
    3. Focus on real software engineer experience patterns missing from internet data
- Post-training RL process
    1. Initial SFT on diverse coding tasks (code generation, software development, data analysis, SQL)
    2. Long-horizon RL training using MegaFlow scheduler
        - 20K concurrent virtualized agent environments on Alibaba Cloud
        - Agents interact with real coding environments using scaffolds (OpenHands, etc.)
        - Challenge: model sometimes “hacks” evaluations (git log to find solutions)

**Coding Agents & Future Direction**

- Agentic vs non-agentic coding differences
    - Multi-turn environment interaction vs single-turn solutions
    - Higher token consumption but capable of harder tasks
    - Dynamic scaffolding vs static problem-solving
- Integration roadmap
    - Search capabilities: combine coding agent + search agent for dynamic tool usage
    - Multimodal foundation: vision for computer usage agents (clicking + coding)
    - Long-horizon reasoning: 10-30 hour problem solving sessions
- Product: PlainCode platform (free 50 queries/day, open source scaffold)

## **DL4C panel**

**Current AI Coding Agent Capabilities & Limitations**

- **Partial replacement vs complete replacement**
    - Complete replacement only when AGI/ASI arrives
    - Current agents useful for changing implementation details
    - Still lack true world understanding and agency
- **Development workflow changes**
    - Writing code requires less effort (most code generated by agents)
    - QA and testing require significantly more effort
    - More developers will exist, everyone developing software to some extent
    - Complex systems (AWS-scale) still need experienced developers
- **Current model performance levels**
    - Previous models: L3 level capability
    - Recent models (o1): L5 level, sometimes writes better code than humans
    - Still challenging: complex system design, distributed systems, performance optimization, complex ML problems with difficult math

**Key Technical Gaps & Challenges**

- **Self-assessment and feedback**
    - No coding agent reliably knows when it successfully completed a task
    - Agents don’t push back on bad design decisions
    - Limited ability with superhuman/rare tasks not in training data
- **Non-technical user gap**
    - Fundamental misalignment between training data (developer-focused) and non-technical user requests
    - Hard generalization problem between technical jargon and user needs
- **Scaffolding vs base model scaling**
    - Scaffolding still essential despite model improvements
    - Context engineering crucial for practical deployment
    - APIs and interactive tools far more efficient than keyboard/mouse simulation
    - Pre-training limited by ~2 trillion high-quality coding tokens available

**Impact on Software Engineering Careers**

- **Junior developer training evolution**
    - Some new engineers can’t code but excel at prompting
    - 3-year career acceleration - juniors become “managers of agents” from day one
    - Need balance: learn fundamentals without AI first, then use AI assistance
    - Code review skills become more critical than before
- **Essential skills shifting**
    - Less time writing code by hand (but still need basic ability)
    - More time on architecture, design discussions, shepherding multiple PRs
    - Code review and quality assessment increasingly important

**Research Directions & Benchmarks**

- **Benchmark limitations**
    - Current benchmarks miss zero-to-one development scenarios
    - Need evaluations beyond pass/fail - code quality, maintainability
    - Missing: high-level task completion, non-coding problem solving
    - Long-horizon coding benchmarks scarce (Commit Zero as example)
- **Research opportunities**
    - Build and publish more benchmarks for community benefit
    - Focus on solid RL knowledge and ablation studies
    - Privacy solutions: VPC deployment, local models
    - Memory management for long-running tasks
    - Cultural diversity and taste in generated applications