# NeurIPS 2025 Notes

**Conference:** Neural Information Processing Systems 2025

**Location:** San Diego, CA, USA

**Dates:** December 9-15, 2025

**Website:** [neurips.cc](https://neurips.cc)

## Overview

NeurIPS (Neural Information Processing Systems) is one of the premier conferences in machine learning and artificial intelligence. These notes capture insights from invited talks, tutorials, panels, and oral presentations I attended during the conference.

## Talks Attended

### Invited Talks

| Talk Title | Speaker | Notes |
|------------|---------|-------|
| [On the Science of "Alien Intelligences": Evaluating Cognitive Capabilities](invited-talk-cognitive-capability-evaluation.md) | Melanie Mitchell | Six principles for rigorous AI evaluation; exposing flaws in current benchmarking |
| [The Art of (Artificial) Reasoning](invited-talk-ai-reasoning.md) | Yejin Choi | Era of Large Reasoning Models; smarter scaling through RL and synthetic data |
| [From Benchmarks to Problems: Problem Finding in AI](Invited-talk-problem-finding-in-ai.md) | Kyunghyun Cho | Learning algorithms from data; therapeutic antibody design applications |
| [Are We Having the Wrong Nightmares About AI?](invited-talk-wrong-nightmares-ai.md) | Zeynep Tufekci | Five proofs being destroyed; real dangers of engagement-driven AI business models |

### Tutorials

| Tutorial Title | Topic Area | Notes |
|----------------|------------|-------|
| [Explainable AI (xAI)](xAI.md) | Interpretability | Feature, data, and component attribution methods; inherent interpretability through training constraints |

### Panels & Workshops

| Session Title | Topic | Notes |
|---------------|-------|-------|
| [Responsible AI Research & Unlearning](rai-pannel.md) | Ethics & Governance | Non-consensual data in research; machine unlearning limitations; research integrity challenges |
| [Agentic Development at the Frontier](agentic-development-frontier.md) | AI Agents | PyTorch RL infrastructure; OpenEnv for RL environments; coding agents as primary success case |
| [Deep Learning for Coding (DL4C)](workshop-dl4c.md) | Coding Agents | Building usable coding agents; agentic training; benchmarking; Qwen3-Coder; panel discussion |

### Oral Presentations

| Paper Title | Research Area | Notes |
|-------------|---------------|-------|
| [Multimodal Oral Session](multimodal-oral.md) | Vision-Language | Dynam3D (3D navigation), Perception Encoder, text-3D retrieval, CoralVQA, OpenHOI |

## Key Highlights

### Most Impactful Insights

**1. AI Evaluation is Fundamentally Broken (Melanie Mitchell)**
- Current benchmarks suffer from data contamination, spurious associations, and lack of robustness testing
- High accuracy doesn't guarantee intended abstraction recognition
- Need to distinguish between performance and competence
- Six principles: cognitive bias awareness, skeptical hypothesis testing, failure analysis, novel variations, performance vs competence distinction, replication

**2. The Era of Large Reasoning Models (AI Reasoning Talk)**
- Transition from brute-force scaling to "smarter scaling"
- Data saturation forcing new approaches: learn faster, synthesize data, or reason beyond training data
- RL effectiveness mixed - entropy management crucial (Goldilocks zone)
- Synthetic data innovation: aggressive filtering (70-90%), weaker teacher models can outperform 20x larger ones
- Democratizing AI: "of humans, by humans, for humans"

**3. Learning Algorithms from Data (Problem Finding Talk)**
- Shift from manually designing algorithms to learning them through meta-learning
- Applications: targeted causal discovery (20K+ genes), black-box causal inference, mutual information estimation, sequential optimization
- Moving from "learning tools" to "learning the process of scientific inquiry itself"
- Trade-off: lose a priori guarantees but gain scalability through extensive empirical verification

**4. Five Proofs Being Destroyed by Generative AI**
- Proof of effort (essays, cover letters now mass-produced)
- Proof of authenticity (voice, video no longer trustworthy)
- Proof of accuracy (well-written ≠ expertise)
- Proof of sincerity (non-sincere entities acting sincere)
- Proof of humanity (art value from shared human vulnerability)
- **Real danger**: engagement-driven advertising model creating propaganda/control mechanisms
- **Actual doom scenario**: demand for mass surveillance to restore authenticity proofs

**5. Explainability Through Three Eras**
- Before 2014: Linear models and trees
- 2014-2020: Data attribution for DNNs
- After 2022: Component attribution for LLMs
- Unified framework: perturbations, gradients, linear approximations across feature/data/component attribution
- **Key insight**: Build interpretability into training (concept constraints, adversarial training) rather than post-hoc methods

**6. Responsible AI Challenges**
- 8M+ non-consensual nude images used in 150 CS papers without consent
- Machine unlearning doesn't work as expected - models learn latent information beyond training data
- Gap between technical capabilities and regulatory expectations
- AI-generated survey papers creating DDoS attack on research community
- Need for refutations/critiques track and scientific consensus building

**7. Agentic AI Infrastructure Revolution**
- Environments now as important as models
- PyTorch Monarch framework for distributed RL with heterogeneous compute
- OpenEnv: 1,800+ environments for RL training (used in DeepSeek-V3.2)
- Coding agents as first success case: deterministic, verifiable, easy feedback
- Task horizons doubling every 7 months

**8. Multimodal Models Still Struggle**
- Vision-language navigation plagued by spatial amnesia and geometry blindness
- Dynam3D solution: hierarchical semantic pyramid (patch → instance → zone)
- Perception Encoder: best features not at output layer - need self-distillation
- Domain-specific challenges: CoralVQA shows 13% performance drop cross-region
- Current VLMs struggle with complex reasoning in specialized domains

## Major Themes

- **Evaluation Crisis**: Moving beyond accuracy to robustness, consistency, and true understanding
- **Smarter Not Bigger**: Data efficiency and reasoning over raw compute scaling
- **Societal Impact**: Real dangers aren't superintelligence but engagement optimization and proof destruction
- **Research Integrity**: Ethics in data collection and AI-generated content pollution
- **Infrastructure for Agents**: Distributed RL systems and diverse training environments
- **Interpretability by Design**: Building understanding into models during training
- **Multimodal Challenges**: Vision-language models need better 3D understanding and domain adaptation

## Personal Reflections

The conference revealed a field at an inflection point. The conversations weren't about whether models would get bigger, but how to make them smarter, more aligned with human values, and more rigorously evaluated. The most sobering realization: our benchmarks are broken, our research practices have ethical gaps, and the real AI risks aren't about AGI takeover but about the mundane deployment of engagement-maximizing systems that destroy trust, authenticity, and truth.

## Resources

- [NeurIPS 2025 Proceedings](https://neurips.cc/Conferences/2025)
- Tutorial materials and code repositories linked in individual talk notes

## Follow-Up

- Implement six principles for evaluating my own AI experiments
- Revisit Yejin Choi's talk for RL review
- Explore PyTorch Monarch for distributed RL projects
- Try OpenEnv environments for agent training
- Try explanable AI method from tutorial in my interpretability work
