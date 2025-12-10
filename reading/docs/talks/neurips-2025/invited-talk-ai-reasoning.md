# Invited Talk: The Art of (Artificial) Reasoning

[Video Recording](https://neurips.cc/virtual/2025/loc/san-diego/invited-talk/109603)

**Era of Smarter Scaling**

- Brute-force scaling era ending, smarter scaling beginning
- Computing growing but data not growing fast enough
- Three approaches to data saturation:
    1. Learn better/faster with limited data (human-like efficiency)
    2. Synthesize more data artificially
    3. Reason beyond what’s in training data
- 2025: Year of Large Reasoning Models (LRMs) vs Large Language Models

**Reinforcement Learning Research Findings**

- Mixed evidence on RL effectiveness in reasoning
    - Papers show RL can improve performance but questions remain about true reasoning vs probability shifting
    - Pass@1 performance improves but Pass@K performance may worsen after RL
    - Models show homogeneity across different LLMs, especially after post-training
- ProRL (Prolonged RL) results:
    - 1.5B parameter model pushed to compete with 7B models
    - Key insight: Entropy management crucial - clipping boundaries matter significantly
    - Goldilocks zone: Low entropy but not too low prevents collapse
- RL as Pre-training (RLP):
    - Information gain reward for predicting next tokens with vs without thought
    - Performance gains survive post-training (SFT + RL)
    - Works even with controlled compute/fewer tokens

**Synthetic Data Innovation**

- Prismatic Synthesis approach challenges conventional wisdom
- Used weaker teacher model (32B vs largest available) intentionally
- Key innovations:
    - Gradient-based data representation for diversity measurement
    - G-Bandy score in gradient space correlates with out-of-distribution performance
    - Aggressive filtering (70-90% of generated data removed)
    - Fully synthetic problems and solutions
- Results: Outperformed models using 20x larger teacher models with zero human-labeled data

**Democratizing AI Philosophy**

- AI should be “of humans, by humans, for humans”
    - Ownership: Reflects values of all humanity, not just few countries/companies
    - Creation: Developed by people worldwide, not just those who can afford it
    - Beneficiary: Serves all humans, not just some or AI serving AI
- Unconventional collaboration example: OpenThought project
    - Multi-institutional team across universities and startups
    - Achieved remarkable results through effortful SFT competing with RL models
- Current AI relies heavily on human intelligence and massive human annotation efforts

**Open Research Questions**

- Need new theories of intelligence (plural) - LLMs may be one approach among many
- How to reach “dark matter of human knowledge” that current data doesn’t cover
- Human brain uses light bulb energy vs massive compute requirements
- Small working memory might be architectural advantage vs million-token windows
- Robotics lacks internet data - requires different approaches entirely