# LLM-as-Judges

## Overview

The LLMs-as-judges paradigm is defined as a flexible and powerful evaluation framework where LLMs are utilized as evaluative tools. They are responsible for assessing the quality, relevance, and effectiveness of generated outputs based on defined evaluation criteria, leveraging their extensive knowledge and deep contextual understanding to adapt flexibly to diverse tasks in NLP and machine learning.

The LLMs-as-Judges concept is rooted in the LLMs' capability to serve as evaluators based on natural language responses, which has attracted considerable attention from both academia and industry

### Motivation
The rise of LLMs-as-Judges is motivated by the limitations of traditional evaluation methods when faced with modern generative AI outputs.
- **Addressing Limitations of Traditional Metrics**: Traditional metrics (like BLEU and ROUGE) are often insufficient for comprehensively evaluating the highly generative and open-ended nature of modern LLM outputs, failing to capture key aspects like text **fluency, logical coherence, and creativity**. The definition of LLMs as flexible judges capable of assessing quality, relevance, and effectiveness directly addresses this failure by allowing the criteria to be adjusted based on the specific task context, moving beyond fixed statistical metrics.
- **Need for Scalable and Interpretive Evaluation**: Human annotations are seen as the "ground truth" but are time-consuming and resource-intensive for large-scale evaluation. The definition highlights that LLMs-as-Judges offer a scalable and reproducible alternative to human evaluation. Furthermore, their capability to leverage deep contextual understanding allows them to generate interpretive evaluations, offering comprehensive feedback and deeper insights into performance, which traditional metrics lack.


## Key Concepts
The following equation provides the structural overview of how the LLM judge operates:
$$(Y, E, F) = f(T, C, X, R)$$

**Evaluation Input**:
- $f$ represents the evaluation function (the LLM judge itself). This function is categorized into three primary configurations: 
  - **Single-LLM Evaluation System**: A single model to perform the evaluation task. Limitation: struggle with complex tasks; may introduce bias.
  - **Multi-LLM Evaluation System**: Multiple LLMs are employed to evaluate.
  - **Human-AI Collaboration Systems (Hybrid)**: Combines human expertise with LLM capabilities for enhanced evaluation.
- $T$ defines the evaluation model. It mainly three approaches:  
    - **Pointwise**: Evaluates each output independently based on specific criteria.
    - **Pairwise**: Compares two candidates to determine which one performs better according to the specified criteria. 
    - **Listwise**: Evaluates the entire list of candidate items, evaluating and ranking them based on the specific criteria, e.g. ranking tasks,
- $C$ denotes the evaluation criteria, defining the specific standards that determine which aspects of the output should be assessed. Typically, teh criteria encompass the following aspects:
    - **Linguistic Quality**: Language related of the output, e.g. fluency, grammatical accuracy, coherence, and conciseness.
    - **Content Relevance**: Focuses on correctness and relevance of the content. 
    - **Task-Specifc Criteria**: Customized criteria tailored to the specific task, e.g. creativity for story generation.
- $X$ is the evaluation items.
- $R$ is evaluation reference, which is optional:
    - **Reference-based Evaluation**: leverage the reference data to determine the quality and relevance of the generated outputs.
    - **Reference-free Evaluation**: not rely on a specific reference $R$, instead, it evaluates $X$ based on intrinsic quality standards.

**Evaluation Output**:
- $Y$ primary output, which can take the form of a numerical score, a ranking, a categorical label, or a qualitative assessment.
- $E$ provides detailed reasoning and justifications for the evalution results.
- $F$ consists of actionable suggestions or recommendations for improving the evaluated outputs.


## Functionality
Three main functionalities of LLMs-as-Judges:
- **Performance Evaluation**: The most fundamental function. Two components:    
    - **Responses Evaluation**: focuses on aspects such as the quality, relevance, coherence, and fluency of the responses for a given task. 
    - **Model Evaluation**: assesses the overall capabilities of LLMs, such as coding, instruction-following, reasoning, and other specialized skills.
- **Model Enhancement**:  plays a key role in improving model performance from the training phase through inference, offering a novel optimization pathway for artificial intelligence by fostering the refinement and personalization of intelligent systems across real-world applications
    - **Reward Modeling During Training**, e.g. RLHF
    - **Acting as Verifier During Inference**, primarily responsible for selecting the optimal response from multiple candidates
    - **Feedback for Refinement** LLM judges provide actionable feedback to iteratively improve output quality
- **Data Construction**
    - **Data Annotation**: using LLM judges to efficiently label large, unlabeled datasets
    - **Data Synthesis**: using LLMs-as-Judges to create entirely new data from scratch or based on seed data

## Referecnces & Further Reading

- [LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods](http://arxiv.org/abs/2412.05579). A comprehensive survey on the emerging paradigm of Large Language Models (LLMs) used as judges for evaluation. The survey systematically reviews this concept across five main dimensions: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.

