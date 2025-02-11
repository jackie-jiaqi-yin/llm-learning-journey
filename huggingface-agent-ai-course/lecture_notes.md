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
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
Cutting Knowledge Date: December 2023
Today Date: 10 Feb 2025
<|eot_id|>
<|start_header_id|>user<|end_header_id|>
I need help with my order
<|eot_id|>
// ... rest of conversation with similar formatting ...
```

**Understanding Model Types**
There are two main variants of LLMs you'll encounter:

- **Base Models**: Trained on raw text to predict what comes next
- **Instruct Models**: Specially fine-tuned to follow instructions and have conversations

To use a Base Model effectively, you'll need to format your prompts in a way it understands consistently.

```python
system_message = {
    "role": "system",
    "content": "You are a professional customer service agent. Always be polite, clear, and helpful."
}
```

When using Agents, the System Message also gives information about the available tools, provides instructions to the model on how to format the actions to take, and includes guidelines on how the thought process should be segmented.

**User and Assistant Messages**. A conversation consists of alternating messages between a Human (user) and an LLM (assistant). The followings are examples of multi-turn conversations:

```python
conversation = [
    {"role": "user", "content": "I need help with my order"},
    {"role": "assistant", "content": "I'd be happy to help. Could you provide your order number?"},
    {"role": "user", "content": "It's ORDER-123"},
]
```

Those conversations are transformed into a prompt (adding some special tokens) that is given to the LLM. For example when using `Llama-3.2`:

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

- A Base Model is trained on raw text data to predict the next token.
- An Instruct Model is fine-tuned specifically to follow instructions and engage in conversations.

To make a Base Model behave like an Instruct Model, we need to format our prompts in a consistent way that the model can understand.

```python
system_message = {
    "role": "system",
    "content": "You are a professional customer service agent. Always be polite, clear, and helpful."
}
```

### Tools