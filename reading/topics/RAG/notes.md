# RAG

## Contents
- [Introduction](#Introduction)
- [Papers](#papers)
- [Online Articles](#Online-Articles)   
- [Implementation](#Implementation)

## Introduction
RAG stands for Retrieval-Augumented Generation. RAG system works two steps: 1. Retrieve: It retrieves relevant information from a large corpus of text. 2. Generate: It generates a response based on the retrieved information. Common Use-case: question answering, document summarization, content generation.
![RAG](../../figs/rag.webp "How rag works")
Why do we need RAG? 1. avoid hallucination 2. timeliness 3. LLMs cannot access private data, feed more internal/user private data to get customized results. 4. Answer constraint. 

A naive RAG mainly consists of the following steps:
1. **Indexing**: Cleaning and extracting the raw text into standardized plain text -> Chunking -> transformed into vector via embedding -> create (key, value) pairs, which is (index, vector) pairs.
2. **Retrieval**: users query processed by an encoding model -> query embedding -> similarity search on a vector database -> top-k results are retrieved.
3. **Generation**: user query and retrieved documents are fed into a prompt template -> generate the response.

## Best practices of RAG
In Paper [2]:
> A typical RAG workflow usually contains multiple intervening processing steps: query classification (determining whether retrieval is necessary for a given input query), retrieval (efficiently obtaining relevant documents for the query), reranking (refining the order of retrieved documents based on their relevance to the query), repacking (organizing the retrieved documents into a structured one for better generation), summarization (extracting key information for response generation from the repacked document and eliminating redundancies) modules. Implementing RAG also requires decisions on the ways to properly split documents into chunks, the types of embeddings to use for semantically representing these chunks, the choice of vector databases to efficiently store feature representations, and the methods for effectively fine-tuning LLMs

### RAG Workflow
1. Query Classification. For tasks entirely based on user-given information, we denote as “sufficient”, which need not retrieval; otherwise, we denote as “insufficient”, and retrieval may be necessary.
2. Chunking. Three types of chunking: token sentence, and semantic levels. 
   - Token-level chunking: split the text into tokens, usually with a fixed length.
   - Sentence-level chunking: split the text into sentences.
   - Semantic-level chunking: take the embeddings of every sentence in the document, comparing the similarity of all sentences with each other, and then grouping sentences with the most similar embeddings together.
3. Vector databases. Store embedding vectors with their metadata, enabling efficient retrival of documents relevant to queries through various indexing and approximate nearest neighbor search. 
4. Retrieval Method. The recommended steps:  
   1. query rewriting.
   2. query decomposition.
   3. pseudo-document generation. This approach generates a hypothetical document based on the user query and uses the embedding of hypothetical answers to retrieve similar documents. One notable implement is HyDE.
   4. Hybrid search. Combining sparse retrieval (BM25) and dense retrieval (original embedding). The weights between the two retrieval methods can be appropriately adjusted. 
   5. Reranking. Enhance the relevance of the retrieved documents.  
   6. Document repacking. The performance of subsequent processes, such as LLM response generation, may be affected by the order documents are provided.
   7. Summarization. Extractive or abstractive. 


![img.png](figs/rag-workflow.png)

## Papers
1.  Lewis, Patrick, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, et al. “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.” arXiv, April 12, 2021. http://arxiv.org/abs/2005.11401.
> The first paper talks about RAG - models which combine pre-trained parametric and non-parametric memory for language generation. RAG models, the parametric memory is a pre-trained seq2seq transformer and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever.
other resource: Youtube video
- https://www.youtube.com/watch?v=JGpmQvlYRdU (by the Author of the paper)
- https://www.youtube.com/watch?v=dzChvuZI6D4 (explanation of the paper)
2. Wang, Xiaohua, Zhenghua Wang, Xuan Gao, Feiran Zhang, Yixin Wu, Zhibo Xu, Tianyuan Shi, et al. “Searching for Best Practices in Retrieval-Augmented Generation.” arXiv, July 1, 2024. http://arxiv.org/abs/2407.01219.
> it gives an overview of current practice of RAG. A good [tech blog](https://pub.towardsai.net/the-best-practices-of-rag-300e313322e6) to explain the paper.

3. Shi, Yunxiao, Xing Zi, Zijing Shi, Haimin Zhang, Qiang Wu, and Min Xu. “Enhancing Retrieval and Managing Retrieval: A Four-Module Synergy for Improved Quality and Efficiency in RAG Systems.” arXiv, July 15, 2024. http://arxiv.org/abs/2407.10670.
> This paper introduces 4 modules to solving several key challenges with RAG.  

4. Luyu Gao, Xueguang Ma, Jimmy Lin, and Jamie Callan. Precise zero-shot dense retrieval without relevance labels. arXiv preprint arXiv:2212.10496, 2022.
> this is the paper talks about HYDE method.  
## Online Articles
### Introduction
- [Introduction to RAG — GenAI Systems for Knowledge](https://medium.com/curiosity-ai/introduction-to-rag-genai-systems-for-knowledge-918a34054228)
- [A Brief Introduction to Retrieval Augmented Generation(RAG)](https://medium.com/ai-in-plain-english/a-brief-introduction-to-retrieval-augmented-generation-rag-b7eb70982891)
- [The Best Practices of RAG](https://pub.towardsai.net/the-best-practices-of-rag-300e313322e6)

**Chucking**
- [Semantic Chunking for RAG](https://medium.com/the-ai-forum/semantic-chunking-for-rag-f4733025d5f5#:~:text=Semantic%20chunking%20involves%20taking%20the%20embeddings%20of%20every,Semantic%20Chunking%20significantly%20enhances%20the%20quality%20of%20retrieval.)

**Retrieval**
- [HYDE: Revolutionising Search with Hypothetical Document Embeddings](https://medium.com/prompt-engineering/hyde-revolutionising-search-with-hypothetical-document-embeddings-3474df795af8#:~:text=At%20its%20core%2C%20the%20HyDE%20methodology%20is%20designed,document%20based%20on%20a%20specific%20question%20or%20subject.)
## Implementation
- [How do domain-specific chatbots work? An Overview of Retrieval Augmented Generation (RAG)](https://scriv.ai/guides/retrieval-augmented-generation-overview/)
- [A beginner’s guide to building a Retrieval Augmented Generation (RAG) application from scratch](https://towardsdatascience.com/a-beginners-guide-to-building-a-retrieval-augmented-generation-rag-application-from-scratch-e52921953a5d)
- [Retrieval-Augmented Generation (RAG): From Theory to LangChain Implementation](https://towardsdatascience.com/retrieval-augmented-generation-rag-from-theory-to-langchain-implementation-4e9bd5f6a4f2)

**Chucking**
- [Semantic Chunking for RAG](https://medium.com/the-ai-forum/semantic-chunking-for-rag-f4733025d5f5#:~:text=Semantic%20chunking%20involves%20taking%20the%20embeddings%20of%20every,Semantic%20Chunking%20significantly%20enhances%20the%20quality%20of%20retrieval.)

**Retrieval**
- [Power of Hypothetical Document Embeddings: An In-Depth Exploration of HyDE](https://medium.com/ai-insights-cobet/power-of-hypothetical-document-embeddings-an-in-depth-exploration-of-hyde-92601a335e5f)
- [Exploring Query Rewriting](https://medium.com/@florian_algo/advanced-rag-06-exploring-query-rewriting-23997297f2d1). This blog uses `LlamaIndex` and `LangChain` to demostrate several techniques for query rewriting: Hypothetical Document Embeddings (HyDE), Rewrite-Retrieve-Read, Step-Back Prompting, and etc..

