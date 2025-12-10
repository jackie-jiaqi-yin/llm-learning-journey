# Invited talk: From Benchmarks to Problems - A Perspective on Problem Finding in AI

[Video Recording](https://neurips.cc/virtual/2025/loc/san-diego/invited-talk/109605)

**Research Philosophy & Problem-Solving Framework**

- Computer science as discipline of problem solving, not discovery
    - Find challenging, impactful problems → identify common substructures → abstract details → develop systematic, generalizable solutions
    - Example: NLP problems (translation, speech, dialogue) → scalable conditional density estimation over sequences → autoregressive neural models
- Criteria for next problems: interesting + impactful
    - Healthcare chosen for maximum societal impact despite being “miserable” to work on
    - Drug discovery as specific focus area with tangible positive outcomes

**Machine Translation to Sequence Modeling Evolution**

- 2013: Machine translation as conditional density estimation via nonlinear function approximation
- Encoder-decoder/sequence-to-sequence approach development (2014-2019)
    - Attention mechanism invention
    - Multilingual systems, unsupervised translation, non-monotonic generation
- 2017 realization: not about translation specifically, but general sequence modeling solution
    - Ilya’s 2014 prediction proved correct: solves any sequence-to-sequence problem

**Learning-to-X Paradigm Emergence**

- Core insight: learn algorithms directly instead of manually designing them
    - Turn algorithm design into supervised learning problem
    - Build reasonable simulators → generate input-output pairs → train deep neural networks
- Historical context: learning-to-learn, amortized inference, simulation-based inference
- Scale-up breakthrough: from 5 examples per class (2017) to thousands of examples per dataset
    - Attention mechanisms enable variable input sizes and dimensions

**Therapeutic Antibody Design Application**

- Lab-in-the-loop molecular design paradigm
    1. Target protein + initial candidates → generative model mutations → scoring → multi-objective optimization → lab synthesis/testing → feedback loop
- Four key challenges requiring algorithmic solutions:
    1. Target discovery - what should antibody bind to?
    2. Evolution - optimal mutation strategies
    3. Uncertainty quantification for candidate selection
    4. Candidate selection from millions of possibilities with lab constraints
- Underlying problems: scalable causal discovery, causal inference, black-box optimization
    1. All require “learning an algorithm” approach since humans can’t solve these systematically

**Four Case Studies of Learned Algorithms**

**Targeted Causal Discovery**

- Problem: identify actionable causes of target variable from thousands of variables
- Solution: train neural network on millions of synthetic causal graphs
    - Input: observational dataset → Output: binary cause indicators
- Results: learned algorithm different from naive graph reconstruction + traversal
    - Flat error rate vs. distance (pairwise independence testing-like) vs. increasing error for graph-based methods
    - Scales to 20,000+ genes in human cells

**Black-Box Causal Inference**

- Problem: estimate causal effects without manually deriving estimators
- Solution: meta-distribution over structural causal models → train set transformer
- Results: outperforms existing estimators on sample efficiency and complex nonlinear cases
    - Validated on LaLonde job training dataset - matched randomized control trial results
- Future: single universal causal inference network for all identifiable problems

**Neural Mutual Information Estimation**

- Problem: mutual information estimation requires full density estimation (too hard)
- Solution: train neural network on 500K+ synthetic joint distributions
    - Varying dimensions (2-32), sample sizes, distribution families
- Results: dramatically outperforms KSG, MINE baselines
    - Works well for high mutual information values (others underestimate)
    - Single forward pass, built-in uncertainty quantification via simultaneous quantile regression

**Sequential Black-Box Optimization**

- Problem: use trajectory information for better candidate selection in multi-round optimization
- Solution: extract procedural knowledge from optimization trajectories
    1. Generate trajectories via MDP + deep Q-network
    2. Train prior-fitted network with positional embedding using MAML
- Results: faster convergence, better final solutions on molecular binder discovery
    1. MAML crucial to prevent overfitting to spurious trajectory correlations

**Open Research Questions**

- Uncertainty quantification: meta-distribution uncertainty + meta-training uncertainty + usual uncertainties
- Meta-generalization: learned algorithms failing on out-of-distribution tasks
    - Need principled training objectives beyond current meta-learning approaches
- Trust and verification: learned algorithms are black boxes vs. classical algorithms with guarantees
    - Paradigm shift from a priori guarantees to extensive empirical verification
    - Embrace approximations rather than seeking optimal solutions

**Vision for Scientific Discovery**

- Path toward learned scientific discovery
    - Current: learning specific tools to automate known processes
    - Future: learn the process of scientific inquiry itself
- Capture discovery strategies from traces of past discoveries
- AI-driven loop for continuous scientific advancement
    - Move beyond coding “aha moments” to learning discovery patterns