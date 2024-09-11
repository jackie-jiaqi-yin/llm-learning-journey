# Content
- [Compressing Large Language Models](#compressing-large-language-models)
- [3 Key Approaches](#3-key-approaches)
  - [Quantization](#quantization)
    - [PTQ](#ptq)
    - [QAT](#qat)
  - [Pruning](#pruning)
    - [Unstructured Pruning](#unstructured-pruning)
    - [Structured Pruning](#structured-pruning)
- [Knowledge Distillation](#knowledge-distillation)
- [Reference](#reference)
  - [Papers](#papers)
  - [Online Articles](#online-articles)


# Compressing Large Language Models
Model compression aims to reduce the size of machine learning models without sacrificing performance. The key benenfits is lower inference costs, e.g. running LLMs locally on mobile devices. 

## 3 Key Approaches
1. **Quantization**: Reducing the number of bits used to represent the model's weights.
2. **Pruning**: Removing unimportant weights from the model. 
3. **Knowledge Distillation**: Training a smaller model to mimic the behavior of a larger model. 

## Quantization
Lowering the precision of model paramters. Two common classes of quantization techniques:
- Post-training quantization (PTQ)
- Quantization-aware training (QAT)

### PTQ
Replacting parameters with a lower-precision data type (e.g. FP16 to INT8). Fastes and simplest way. However, often leads to performance degration.

### QAT
Trainig model (from scratch) with lower-precision data types. For example, the BitNet architecture used ternary data type (e.g. 1.58 bit) to match the performance of  Llama. 

## Pruning
Remove model components that have little impact on the performance, icnluding unstructured pruning and structured pruning.

### Unstructured Pruning
Removes unimportant weights from a neural network, i.e removing weights with smallest absolute value. But it requires specialzied hardware due to sparse matrics operations. See Ref 1. 

### Structured Pruning
Remove entire structures from the neural network, e.g. attention heads, neurons, and layers. It avoids the spars matrix problem. Seen ref 2.

## Knowledge Distillation
Knowledge distillation transfters knowledge from a larger teacher model to a smaller student model, e.g. use predictions from teacher and train on student model.

Examples. Alpaca model finetuned the LLaMA7B model using synthetic data from OpenAI's text-davinci-003, seen ref 3. 

# Reference
## Papers
1.  [To prune, or not to prune: exploring the efficacy of pruning for model compression](https://arxiv.org/abs/1710.01878)
2.  [A Survey on Model Compression for Large Language Models](https://arxiv.org/abs/2308.07633)
3. [Alpaca: A Strong, Replicable Instruction-Following Model](https://crfm.stanford.edu/2023/03/13/alpaca.html)

## Online Articles
- [Compressing Large Language Models (LLMs)](https://medium.com/towards-data-science/compressing-large-language-models-llms-9f406eea5b5e)
