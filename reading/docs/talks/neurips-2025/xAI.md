# Explainable AI (xAI) Tutorials - NeurIPS 2025

## **Explainable AI - Deep Dive 1**

**Tutorial Overview**

- Tutorial page: [link](https://shichangzh.github.io/xaiTutorial/)
- AI explainability evolution across three eras:
    - Before 2014: Linear models and trees for explanation
    - 2014-2020: Interpretable models (feature) → data attribution interpretable (DNNs)
    - After 2022: Component attribution (LLM era)
- Technical Deep Dive covers three attribution types:
    - Feature attribution
    - Data attribution
    - Component attribution

**Attribution Problem**

- General framework: Training data → model → output
- Three perspectives for explaining AI system outputs
- Unified mathematical notation:
    - Feature attribution scores: φᵢ
    - Data attribution scores: ψⱼ
    - Component attribution scores: γₖ

**Feature Attribution**

- Core question: How do features impact the output?
- Applications:
    - Justify predictions and provide counterfactual explanations
    - Identify spurious correlations (e.g., husky classified as wolf based on snow background)
- Example: Loan application model explaining denial based on salary, credit score vs inappropriate reliance on gender

**Data Attribution**

- Core question: Why this output for those training data points?
- Studies how training data influences model output
- Applications:
    - Characterize training data properties
    - Determine data values and identify harmful training examples
- Example: Fish classification traced back to semantically similar training image with coral background

**Component Attribution**

- Core question: Why this output for these model components?
- Components can be: neurons, attention heads, layers, subnetworks
- Example: Language model answering “When Mary and John went to the store, John gave…” → “Mary”
    - Sparse attention head activation map shows only small subset needed for indirect object identification

**Perturbation-Based Feature Attribution**

- Direct perturbation:
    - Perturb features and observe output changes
    - Problem: Feature interactions require considering all possible subsets
- Game theoretic perturbation:
    - SHAP method using Shapley values
    - Considers all 2^d marginal contributions
    - Computational complexity: O(2^d) - not scalable for large feature sets
- Perturbation mask learning:
    - Continuous and learnable masks instead of binary
    - Generates saliency maps for computer vision
    - Learned masking model applicable across multiple inputs

**Gradient-Based Feature Attribution**

- Key distinction: Feature gradients for attribution vs parameter gradients for training
- Measures output sensitivity with respect to input features
- SmoothGrad method:
    - Adds noise to create multiple input versions
    - Aggregates gradients across noisy versions
    - More robust than vanilla gradients
- Produces increasingly intuitive saliency maps as methods evolved

**Linear Approximation for Feature Attribution**

- LIME (Local Interpretable Model-agnostic Explanations):
    - Uses linear model for local approximation around decision boundary
    - Trains on binary indicators (feature present/absent) rather than actual input values
    - Linear coefficients become attribution scores
- Successfully identified husky-wolf misclassification based on background snow

**Data Attribution Methods**

**Perturbation-Based Data Attribution**

- Leave-one-out (direct perturbation):
    - Remove one training data point, retrain model, observe changes
    - Computationally expensive: requires n retraining cycles
- Game-theoretic perturbation:
    - Data Shapley algorithm
    - Requires 2^n marginal contributions with retraining
    - Only approximate versions practical

**Gradient-based Data Attribution**

- No perturbation required - avoids retraining
- Gradient similarity method:
    - Compute gradients for test and training points
    - Dot product measures similarity between gradient representations
    - Problem: No causal interpretation, only similarity measure
- Influence functions:
    - Approximates leave-one-out computationally efficiently
    - Introduces Hessian matrix for second-order information
    - Mathematical derivation recovers leave-one-out with modified training objective

**Linear Approximation for Data Attribution**

- Datamodel approach:
    - Skip training step - directly predict model output from training data
    - Linear model G approximates relationship: training data → test output
- Counterfactual data collection:
    - Each data point: subset of training data + prediction from model trained on that subset
    - Binary indicator vector Z shows which training points included
    - Linear coefficients become attribution scores

**Perturbation-Based Component Attribution**

- Causal mediation analysis:
    - Replace components with dummy values, observe output changes
    - Neural Shapley applies game theory to capture component interactions
- Mask learning and subnetwork probing:
    - Learnable continuous masks for component selection
    - Optimize mask to recover original output while identifying important components
- Causal tracing (three-run patching):
    - Clean input → model → output
    - Perturbed input → model → baseline output
    - Perturbed input + restored component K → model → recovered output
    - Attribution score: difference between run 3 and run 2
- Target perturbation:
    - Control model behavior by optimizing component values
    - Example: Change “capital of France” answer from Paris to London by modifying identified component

**Gradient-Based Component Attribution**

- Approximates three-run patching paradigm using Taylor approximation
- Efficiency advantage: Batches multiple inputs in single forward/backward pass
- Avoids expensive instance-wise patching step
- Gradient of perturbed output with respect to component × component value difference

**Linear Approximation for Component Attribution**

- Direct prediction: model components → test output
- Linear function G locally approximates component influence
- Counterfactual data collection from different component subsets
- Coefficients become component attribution scores

**Unified Framework**

- Three attribution problems solved by three method categories:
    1. Perturbations (direct, game-theoretic, mask learning)
    2. Gradients (similarity, influence functions, Taylor approximation)
    3. Linear approximations (LIME, datamodel, component linear models)
- Additional methods exist beyond these three categories
- Mechanistic interpretability includes: sparse autoencoders, logit lens, linear probing

# **XAI - Deep Dive 2**

**Inherent Interpretability Framework**

- Goal: Design interpretable yet performant language models at scale
- Alternative to post-hoc explanation methods (gradients, probes, influence functions)
- Core approach: Add interpretability constraints during training pipeline
    - Data constraints: Reprocess datasets for human understanding
    - Architecture constraints: Modify transformer layers for traceability
    - Representation constraints: Force interpretable concept encoding
    - Training constraints: Add interpretability losses to standard task loss

**Concept-Constrained Interpretable Models**

- Architecture modification: Replace transformer layer with interpretable transformation
    - Maps representations to basis of known concepts (blue neurons) vs unknown (black neurons)
    - Example: Paper review system with clarity, novelty, significance concepts
- Loss function structure: L_total = L_task + λ L_interp
    - Task loss: Standard next token prediction
    - Interpretability loss: Forces specific neurons to represent target concepts
- Scaling results: Achieves comparable performance to GPT models at billions of parameters
    - Tested on 33K supervised concepts, 160K unsupervised concepts
    - Trained on billions of tokens with minimal performance degradation

**Post-Hoc Method Limitations**

- Feature attribution mismatch
    - Gradient-based methods often contradict occlusion analysis
    - Example: Amino acid sequence task where gradients highlight distractors, not task-relevant features
- Concept probing challenges
    - Can identify features in activations but not causal relevance to output
    - Spurious correlations between causal and irrelevant features mislead probes
- Training data attribution complexity
    - Influence functions require Hessian computation (billion × billion matrices)
    - Computational intractability and convexity assumptions limit practical application

**Training Solutions for Interpretability**

- Input masking during training
    - Randomly mask inputs to force robustness
    - Aligns gradient behavior with human-expected occlusion patterns
    - Makes models smooth and differentiable for better gradient interpretability
- Adversarial training
    - Train on adversarial examples for off-manifold robustness
    - Similar alignment benefits between gradients and perturbation analysis
- Architecture modifications
    - Backpack Language Models: Rewrite transformer as generalized additive model
    - Split token embeddings into sense vectors (fruit Apple vs company Apple)
    - Enables surgical intervention and concept toggling

**Scaling and Performance Results**

- Concept-constrained models scale to billions of parameters with <2% performance drop
- Training data attribution achievable in single forward pass (no Hessian computation)
- Prototype-based clustering losses enable direct tracing from outputs to training data
- Maintains competitive performance on standard LM benchmarks while providing interpretability