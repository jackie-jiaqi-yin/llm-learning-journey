This is my notes for the online learning courses from Hugging Face; [link](https://huggingface.co/learn/nlp-course/chapter1/1).
## Content
- [Fine-tuning Large Language Models](#fine-tuning-large-language-models)
  - [Introduction](#introduction)
  - [Chat Templates](#chat-templates)
  - [Fine-Tuning with SFTTrainer](#fine-tuning-with-sfttrainer)
  - [Low-Rank Adaptation (LoRA)](#low-rank-adaptation-lora)
  - [Evaluation](#evaluation)

# Fine-tuning Large Language Models
Original course content can be found [here](https://huggingface.co/learn/nlp-course/chapter11/1).

## Introduction
In this chapter, we will cover:
- **Chat Templates**: Components like system prompts and role-based messages.
- **Supervised Fine-tuning (SFT)**: Training the model on task-specific datasets with labeled examples.
- **Low-Rank Adaptation (LoRA)**: Adding low-rank matrices to the model's layers, enabling efficient fine-tuning while preserving the model's pre-trained knowledge.
- **Evaluation**: Assessing the model's performance.

## Chat Templates
A base model is trained on raw text data to predict the next token, while an instruct model is fine-tuned specifically to follow instructions and engage in conversations. To make a base model behave like an instruct model, we need to format prompts consistently in a way the model can understand. This is where chat templates come into play, providing clear role indicators such as "system," "user," and "assistant."

An example of a conversation structure:
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi! How can I help you today?"},
    {"role": "user", "content": "What's the weather?"},
]
```
Different LLMs (e.g., Llama 2, Mistral, Qwen, ChatGPT, etc.) may use varying syntaxes to represent such conversation structures.

Chat templates can handle more complex scenarios beyond simple conversational interactions, including:
- **Tool Use**: When models need to interact with external tools or APIs.
- **Multimodal Inputs**: For processing images, audio, or other media types.
- **Function Calling**: For executing structured functions.
- **Multi-turn Context**: For maintaining conversation history across multiple exchanges.

## Fine-Tuning with SFTTrainer
This page provides a step-by-step guide to fine-tuning the [deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) model using the [SFTTrainer](https://huggingface.co/docs/trl/en/sft_trainer).

SFT involves significant computational resources and engineering effort. When to use SFT?
- need additional performance beyond the base model + prompt.
- cost of llm outweights the cost of FT a small model.
- require specialized formats or domain-sepcific knowledge.

The datesets for fine-tuning should contain input prompt, expected model repsonse, and any additional metadata. 

The Hugging Face tutorial provides sample codes by using the `SFTTrainer` class to fine-tune the model on a dataset. 

## Low-Rank Adaptation (LoRA)
LoRA (Low-Rank Adaptation) is a parameter-efficient fine-tuning technique that freezes the pre-trained model weights and injects trainable rank decomposition matrices into the model’s layers. Instead of training all model parameters during fine-tuning, LoRA decomposes the weight updates into smaller matrices through low-rank decomposition, significantly reducing the number of trainable parameters while maintaining model performance.

## Evaluation
There are general benchmarks for evaluating fine-tuned models, it works for specific domanis like math, coding, and chat. In this section, I will mainly focus on custom benchmark suits. To develop a custom evalution, here is a general workflow:
1. Start with relevant standard benchmarks to establish a baseline and enable comparison with other models.
2. Identify the specific requirements and challenges of your use case. What tasks will your model actually perform? What kinds of errors would be most problematic?
3. Develop custom evaluation datasets that reflect your actual use case. This might include:
    - Real user queries from your domain
    - Common edge cases you’ve encountered
    - Examples of particularly challenging scenarios
4. Consider implementing a multi-layered evaluation strategy:
    - Automated metrics for quick feedback
    - Human evaluation for nuanced understanding
    - Domain expert review for specialized applications
    - A/B testing in controlled environments

# Build Reasoning Models
Original course content can be found [here](https://huggingface.co/learn/nlp-course/chapter12/1).