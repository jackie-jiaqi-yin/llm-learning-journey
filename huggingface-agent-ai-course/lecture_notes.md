# Huggingface Agent AI Course

*Start Date: 2025-02-10*; *[Github](https://github.com/huggingface/agents-course/tree/main)*

## Course Overview

| Chapter | Topic              | Description                                                                                                                                                                           |
| ------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0       | Onboarding         | Set you up with the tools and platforms that you will use.                                                                                                                            |
| 1       | Agent Fundamentals | Explain Tools, Thoughts, Actions, Observations, and their formats. Explain LLMs, messages, special tokens and chat templates. Show a simple use case using python functions as tools. |
| 2       | Frameworks         | Understand how the fundamentals are implemented in popular libraries :`smolagents`, `LangGraph`, `LlamaIndex`                                                                   |
| 3       | Use Cases          | Let's build some real life use cases (open to PRs 🤗 from experienced Agent builders)                                                                                                 |
| 4       | Final Assignment   | Build an agent for a selected benchmark and prove your understanding of Agents on the student leaderboard 🚀                                                                          |

## Content

- [Unit 1: Introduction to Agents](#unit-1-introduction-to-agents)
  - [AI Agent](#ai-agent)
  - [Large Language Models (LLMs)](#large-language-models-llms)
  - [Messages and Special Tokens](#messages-and-special-tokens)
  - [Tools](#tools)
  - [Thought-Action-Observation Cycle](#understanding-ai-agents-through-the-thought-action-observation-cycle)
  - [Dummy Agent Library](#dummy-agent-library)
   - [Create First Agent Using smolagents](#create-first-agent-using-smolagents)

## Unit 1: Introduction to Agents

### AI Agent

An AI Agent is an intelligent system that uses Large Language Models (LLMs) to interact with its environment and accomplish user goals. Think of it as your smart assistant that can:

- Understand what you want through natural conversations
- Think carefully and make plans to solve your problems
- Take actions using various tools and learn from the results

### Large Language Models (LLMs)

LLMs are powerful AI models that can understand and generate human language with remarkable ability. They are built using the **Transformer** architecture - an innovative deep learning approach centered around the "Attention" mechanism that helps models focus on important information.

Modern LLMs come in three main flavors:

- **Encoder Models** (like BERT)

  - Act like expert readers that deeply analyze text
  - Great for tasks like classification and finding meaning
  - Relatively compact at millions of parameters
  - Perfect for understanding input text thoroughly
- **Decoder Models** (like GPT-4, Llama)

  - Act like creative writers generating text one piece at a time
  - Excel at chat, writing, and coding
  - Much larger at billions of parameters
  - Most common type for general AI assistants
- **Encoder-Decoder Models** (like T5, BART)

  - Combine reading and writing abilities
  - Shine at translation and summarization
  - Balance size at millions of parameters
  - Best for transforming text from one form to another

When generating text, LLMs work step-by-step (called autoregressive generation), creating each new word based on what came before. They know when to stop by looking for special markers like `<eot>`.

The secret sauce that makes these models so effective is the Attention mechanism. It helps the model zoom in on the most important parts of the input, kind of like how humans focus on key details when reading or writing.

### Messages and Special Tokens

Let's explore how LLMs communicate through different types of messages and special tokens:

**1. System Messages**
These are like setting up the ground rules. They tell the model how to behave throughout the conversation.

```python
system_message = {
    "role": "system",
    "content": "You are a professional customer service agent. Always be polite, clear, and helpful."
}
```

For AI Agents specifically, system messages do three important things:
- Describe available tools the agent can use
- Explain how to format actions
- Provide guidelines for structuring thoughts

**2. User and Assistant Messages**
These form the back-and-forth conversation between human and AI. Here's a typical exchange:

```python
conversation = [
    {"role": "user", "content": "I need help with my order"},
    {"role": "assistant", "content": "I'd be happy to help. Could you provide your order number?"},
    {"role": "user", "content": "It's ORDER-123"},
]
```

**Behind the Scenes: Special Tokens**
When these messages are fed to an LLM (like Llama-3.2), they get wrapped with special tokens that help the model understand the structure:

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Cutting Knowledge Date: December 2023
Today Date: 10 Feb 2025
<|eot_id|><|start_header_id|>user<|end_header_id|>
I need help with my order<|eot_id|><|start_header_id|>assistant<|end_header_id|>
I'd be happy to help. Could you provide your order number?<|eot_id|><|start_header_id|>user<|end_header_id|>
It's ORDER-123<|eot_id|><|start_header_id|>assistant<|end_header_id|>
```

#### Base Model vs. Instruct Model
- **Base Models**: Trained on raw text data to predict the next token
- **Instruct Models**: Fine-tuned specifically to follow instructions and engage in conversations

To make a Base Model behave like an Instruct Model, we need to format our prompts in a consistent way that the model can understand.

### Tools: Extending LLM Capabilities

Tools are functions that enable LLMs to interact with the external world and perform specific tasks. Think of them as the "hands" that allow an AI to take actual actions.

**Core Types of Tools:**
1. **Information Gathering**
   - Web Search: Finding real-time information
   - Retrievers: Accessing specific documents or knowledge bases
   - API Calls: Fetching data from external services

2. **Content Generation**
   - Image Generation: Creating visuals from text descriptions
   - Code Execution: Running and testing code
   - Document Processing: Working with various file formats

**Anatomy of a Tool:**
Every tool requires four key components:
1. **Description**: Clear explanation of the tool's purpose
2. **Callable Function**: The actual code that performs the action
3. **Input Arguments**: Clearly typed parameters
4. **Output Specification**: Expected return value and type

Here's a practical example:

```python
@tool
def calculator(a: int, b: int) -> int:
    """Multiply two integers and return their product."""
    return a * b

# Tool specification that the LLM sees:
print(calculator.to_string())
# Output: Tool Name: calculator, Description: Multiply two integers., 
#        Arguments: a: int, b: int, Outputs: int
```
The return is text suitable to be used as a tool description for an LLM


### Understanding AI Agents through the Thought-Action-Observation Cycle
In this section, we'll explore the Thought-Action-Observation cycle - the fundamental workflow that powers AI Agents.

**Core Components of the Agent Loop**
AI Agents operate in a continuous cycle that mirrors human decision-making:

1. **Thought**: The LLM analyzes the current state and plans the next step
   - Evaluates available information and context
   - Reasons about the best approach to achieve the goal
   - Decides which tool (if any) would be most effective

2. **Action**: The agent executes its planned action
   - Calls specific tools with carefully chosen parameters
   - Formats requests according to tool specifications
   - Can include API calls, calculations, or information retrieval

3. **Observation**: The agent processes the results
   - Analyzes the outcome of its action
   - Updates its understanding of the situation
   - Determines if the goal has been achieved

This cycle continues in a while loop until the agent determines the objective has been met or requires human intervention.

**System Message Configuration**
The agent's behavior is carefully controlled through the system message, which must specify:
- Core personality and behavioral traits
- Complete list of available tools and their specifications
- Explicit instructions for following the Thought-Action-Observation format
- Success criteria and stopping conditions
- Error handling and edge case protocols

#### Thought: Internal Reasoning and the Re-Act Approach

Agent breaks down complex problems into smaller, more manageable steps, reflect on past experiences, and continuously adjust its plans based on new information.

**ReAct Framework**: A powerful prompting technique that combines:
- Reasoning: Explicit step-by-step thinking process
- Acting: Executing planned actions based on reasoning
This framework significantly improves the agent's problem-solving capabilities by enforcing structured thinking.


#### Actions: Enabling the Agent to Engage with Its Environment
Actions are the concrete steps an AI agent takes to interact with its environment.

**Types of Agents by Action Format:**

| Type of Agent | Description |
|--------------|-------------|
| JSON Agent | The Action to take is specified as in JSON format |
| Code Agent | The Agent writes a code block that is interpreted externally |
| Function-calling Agent | It is a subcategory of the JSON Agent which has been fine-tuned to generate a new message for each action |

#### Observe: Integrating Feedback to Reflect and Adapt
In observation phase, the agent:
- collects feedbacks: receives data or confirmation that its action was successful (or not)
- Appends results: integrates the new information into existing context, effectively updating its memory
- Adapts its strategy: uses this updated context to refine  subsequent thoughts and actions

### Dummy Agent Library

This section focuses on the concepts and it can be applied to any agent framework. Check my implementation by following the instructions [here](notebook/dummy_agent_library.ipynb)

### Create First Agent Using smolagents

`smolagents` is a library that focuses on codeAgent, a kind of agent that performs “Actions” through code blocks, and then “Observes” results by executing the code.

I have git clone the repo `First_agent_template` from the course repo, saved [here](code/First_agent_template).
You can also find it in the course [website](https://huggingface.co/spaces/agents-course/First_agent_template).

In this section, we only need to modify the `tools` in [app.py](code/First_agent_template/app.py). 

Read through the code and get familiar with the structure. You can also run the code to see how the agent behaves.



