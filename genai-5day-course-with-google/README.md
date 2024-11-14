# 5-Day Gen AI Intensive Course with Google

This repository contains my learning materials and implementations from Google's 5-Day Gen AI Intensive Course. While the original course utilizes the Gemini API and Google Cloud Platform, I've adapted the content to work with **Azure OpenAI** and **LlamaIndex** for several strategic reasons:

## Why Azure OpenAI?

- **Resource Availability**: As a Microsoft employee, I have access to Azure credits ($150/month) for exploring AI services
- **Enterprise-Grade Platform**: Azure OpenAI provides robust, production-ready AI capabilities with strong security and compliance features
- **Seamless Integration**: Direct compatibility with other Azure services and enterprise systems

## Why LlamaIndex over Other Frameworks?

LlamaIndex stands out among LLM toolkits for several compelling reasons:

- **Comprehensive Documentation**: Extensive API documentation with clear examples and best practices
- **Open Source Foundation**: Transparent development and community-driven improvements
- **Active Community**: Strong ecosystem of developers and regular community contributions
- **Versatile Implementation**: Supports various AI applications including:
  - Retrieval-Augmented Generation (RAG)
  - AI Agents
  - Fine-tuning
  - And more
- **Wide LLM Support**: Seamless integration with multiple LLM providers including:
  - Azure OpenAI
  - Anthropic
  - OpenAI
  - Other leading AI models

This implementation approach allows me to gain practical experience with enterprise-grade AI tools while following the course curriculum.

## Course Overview
The no-cost online course was developed by several Google ML researchers and engineers to help better understand some of the fundamentals behind Generative AI. Here's a brief overview of the course content:

- Day 1: Foundational Models & Prompt Engineering - Explore the evolution of LLMs, from transformers to techniques like fine-tuning and inference acceleration. Get trained with the art of prompt engineering for optimal LLM interaction. [My codes](codes/day-1-prompting.ipynb)
- Day 2: Embeddings and Vector Stores/Databases - Learn about the conceptual underpinning of embeddings and vector databases, including embedding methods, vector search algorithms, and real-world applications with LLMs, as well as their tradeoffs.
- Day 3: Generative AI Agents - Learn to build sophisticated AI agents by understanding their core components and the iterative development process.
- Day 4: Domain-Specific LLMs - Delve into the creation and application of specialized LLMs like SecLM and Med-PaLM, with insights from the researchers who built them.
- Day 5: MLOps for Generative AI - Discover how to adapt MLOps practices for Generative AI and leverage Vertex AI's tools for foundation models and generative AI applications.