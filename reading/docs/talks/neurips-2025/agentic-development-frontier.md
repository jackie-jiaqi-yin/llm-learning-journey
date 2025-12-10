# Agentic Development at the Frontier

**Agenda**

- Environments are foundational for agentic AI development
- Showcase tools, systems, and simulators needed for RL training
- Demonstrate how environments integrate with RL training and LM post-training
- Workshop jointly organized with Reflection AI, Hugging Face, Unsloth, and PyTorch Foundation

**PyTorch RL**

- Building agents requires new infrastructure stack
    - Infrastructure: getting infra out of the way to focus on algorithms
    - Data: exposing models to as many environments and skills as possible
- Key challenges in distributed RL systems
    - Orchestration - heterogeneous compute scheduling across different resource types
    - Programming model - torch distributed built for data parallel, not RL workflows
    - Performance - dual producer-consumer problems with replay buffer and parameter server bottlenecks
- Monarch: PyTorch-native distributed programming framework
    - Actor-based system with imperative Python API
    - RDMA transfers as first-class citizens
    - Enables fault tolerance and heterogeneous scaling
- Torch Forge built on Monarch
    - Control plane: service abstraction for routing and load balancing
    - Data plane: in-memory storage with automatic resharding
    - Reduces RL code from thousands of lines to simple, readable pseudocode
    - Supports both synchronous and asynchronous RL training

**OpenEnv - Hugging Face**

- Problem: static datasets plateau in reward, models degrade when deployed to real world
- Solution: unified, partially observable MDP interface for RL environments
    - Gymnasium-style API with step and reset functions
    - Can host environments locally or scale via Hugging Face Spaces API
- DeepSeek-V3.2 trained on 1,800 distinct environments with 85,000+ complex prompts
- Available environments
    - Coding environments for software engineering agents
    - Browser team environments
    - Wordle puzzles, games, and more
- CLI tool works like uv package manager
    - open init creates project skeleton
    - open push deploys to Hugging Face Hub
- Type-safe by design using Python data classes
    - Action, observation, and state classes prevent tensor mismatch errors
    - No external dependencies required

**Unsloth PyTorch OpenEnv**

- Colab notebook demo: [https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/OpenEnv_gpt_oss_(20B)_Reinforcement_Learning_2048_Game.ipynb](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/OpenEnv_gpt_oss_(20B)_Reinforcement_Learning_2048_Game.ipynb)
- 2048 game reinforcement learning example
    - Goal: train language model to generate winning strategies
    - Reward good actions, penalize bad actions over many iterations
    - Only requires one prompt and one environment - no additional training data needed
- Key RL principle: “more good, less bad” repeated over thousands of steps
- Integration with Hugging Face TRL framework
- Memory optimization: 50% reduction in memory usage with faster processing
- Provides 2,000+ RL environments through Unsloth integration
- Anti-cheating mechanisms to prevent strategy exploitation
- GitHub: https://github.com/unslothai/unsloth

**Reflection**

- Evolution from static benchmarks to agentic benchmarks requiring dynamic problem-solving
- Task horizon trends
    - AI models completing hour-long tasks 50% of the time
    - Task length doubling every 7 months
    - Software engineering acceleration even faster
- Required LLM capabilities for autonomous agents
    - Multi-step reasoning and planning
    - Tool use (already working well)
    - Self-correction and recovery from failed trajectories
    - Long horizon task coherence
- Coding agents as primary success case
    - Deterministic, text-based, and verifiable
    - Easy verification through unit tests and tool-assisted feedback
    - Evolution from autocomplete to autonomous coding across multiple files
- Pre-training vs post-training focus
    - Pre-training: reasoning ability and long horizon task solving
    - Post-training: environments provide both data and evaluation
    - Need diverse, challenging tasks at edge of current model capabilities
- Reflection AI hiring for frontier open agentic models development