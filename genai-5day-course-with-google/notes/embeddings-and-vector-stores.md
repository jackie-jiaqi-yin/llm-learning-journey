# Day 2

Complete Unit 2: “Embeddings and Vector Stores/Databases”, which is:
- [Optional] Listen to the [summary podcast episode](https://www.youtube.com/watch?v=1CC39K76Nqs) for this unit (created by NotebookLM).
- Read the “[Embeddings and Vector Stores/Databases](../reference/Newwhitepaper_Embeddings%20%26%20vector%20stores.pdf)” whitepaper.
- Complete these code labs on Kaggle:
  1. Build a RAG question-answering system over custom documents 
  2. Explore text similarity with embeddings 
  3. Build a neural classification network with Keras using embeddings


## Leanings from the whitepaper

### Contents
- [Why embeddings are important?](#Why-embeddings-are-important)
- 

### Why embeddings are important?
-  Provide compact representations of data of different types, while simultaneously also 
allowing you to compare two different data objects and tell how similar or different they are 
on a numerical scale
   - Applications: 
     - Google Search is a retrieval  with 
the  search space of the whole internet. 
     - Today’s retrieval and recommendation systems’ 
success depends on: 1. Precomputing the embeddings for billions items of the search space; 2. Mapping query embeddings to the same embedding space; 3. Efficient computing and retrieving of the nearest neighbors of the query embeddings in 
the search space.
     - Multimodality. Project objects/content (e.g. text and videos) into a joint vector space with semantic meaning

#### Types of Embeddings

##### Text Embeddings
The process of turning text into embedding: Text, Tokenization, Indexing, Embedding.
