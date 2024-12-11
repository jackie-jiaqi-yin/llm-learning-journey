# Day 2

Complete Unit 2: “Embeddings and Vector Stores/Databases”, which is:
- [Optional] Listen to the [summary podcast episode](https://www.youtube.com/watch?v=1CC39K76Nqs) for this unit (created by NotebookLM).
- Read the “[Embeddings and Vector Stores/Databases](../reference/Newwhitepaper_Embeddings%20%26%20vector%20stores.pdf)” whitepaper.
- Complete these code labs on Kaggle:
  1. [Build](../codes/day-2-documentQA-with-rag.ipynb) a RAG question-answering system over custom documents 
  2. [Explore](../codes/day-2-embeddings-and-simmilarity-scores.ipynb) text similarity with embeddings 
  3. Build a neural classification network with Keras using embeddings


## Leanings from the whitepaper

### Contents
- [Why embeddings are important?](#Why-embeddings-are-important)
- [Types of Embeddings](#Types-of-Embeddings)
    - [Text Embeddings](#Text-Embeddings)
    - [Image and multimodal embeddings](#Image-and-multimodal-embeddings)
    - [Graph embeddings](#Graph-embeddings)
    - [Training embeddings](#Training-embeddings)
- [Vector Search](#Vector-Search)
  - [Important vector search algorithms](#Important-vector-search-algorithms)
  - [Vector databases](#Vector-databases)

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

### Types of Embeddings

#### Text Embeddings
The process of turning text into embedding: Text, Tokenization, Indexing, Embedding.

- **Word Embedding**
   - **Word2Vec**:
     - **CBOW**: Predict the target word based on the context words
     - **Skip-gram**: Predict the context words based on the target word
     - Training process:
         - Initialization:  Initializing each word in the corpus as a high-dimensional vector (typically 100-300 dimensions) with random values
         - Word2Vec uses a shallow, two-layer neural network to process text. The input layer takes in batches of raw textual data, which are then processed to produce a vector space of several hundred dimensions.
         - The training objective of the skip-gram model, for example, is to maximize the probability of predicting context words given the target word. 
         - To improve efficiency, Word2Vec often employs negative sampling. This technique involves selecting a few negative examples (words that don't appear in the context) to update during training, rather than using the entire vocabulary
     - It accounts well for local statistics of words within a certain sliding window, but it does not capture the global statistics of words in the whole corpus.
    - **GloVe**: Global Vectors for Word Representation
    - Word embedding downstream tasks: Named Entity Recognition

- **Document Embedding**
  - Two Stage: from Bag-of-Words (BoW) to deeper pretrained large language models
  - **BoW**: 
    - **TF-IDF**: Term Frequency-Inverse Document Frequency
    - **LSA**: Latent Semantic Analysis
    - **LDA**: Latent Dirichlet Allocation
    - Weakness: ignore the order of words in the document and the semantic meaning of the words.
  - **Deeper pretrained large lanaguage model**: 
    - **BERT**: Bidirectional Encoder Representations from Transformers
    - LLM based: GTR and Sentence-T5 (show better performance on retrieval and sentence similarity than BERT)
    - Multi-vector embedding: family include ColBERT and XTR

#### Image and multimodal embeddings
Unimodal image embeddings can be derived in many ways: one of which is by training a
CNN or Vision Transformer model on a large scale image classification task (for example,
Imagenet), and then using the penultimate layer as the image embedding. This layer has
learnt some important discriminative feature maps for the training task. It contains a set of
feature maps that are discriminative for the task at hand and can be extended to other tasks
as well.

To obtain multimodal embeddings19 you take the individual unimodal text and image
embeddings and their semantic relationships learnt via another training process. This
gives you a fixed size semantic representation in the same latent space. 
- **General structured**:
   Given a general structured data table, we can create embedding for each row. This can be
done by the ML models in the dimensionality reduction category, such as the PCA model.
- **User/item structured**: The input is no longer a general structured data table as above. Instead, the input includes
the user data, item/product data plus the data describing the interaction between user and
item/product, such as rating score.

#### Graph embeddings
Graph embeddings are another embedding technique that lets you represent not
only information about a specific object but also its neighbors (namely, their graph
representation). 

#### Training embeddings
Current embedding models usually use dual encoder (two tower) architecture. For example,
for the text embedding model used in question-answering, one tower is used to encode
the queries and the other tower is used to encode the documents. The loss used in embedding models training is usually a variation of contrastive loss, which
takes a tuple of <inputs, positive targets, (optional) negative targets> as the inputs. Training
with contrastive loss brings positive examples closer and negative examples far apart. 

To use embeddings for downstream tasks like classification or named entity recognition,
extra layers (for example, softmax classification layer) can be added on top of the embedding
models. The embedding model can either be frozen (especially when the training dataset is
small), trained from scratch, or fine-tuned together with the downstream tasks.


## Vector Search

Vector search lets you to go beyond searching for exact query literals and allows you to
search for the meaning across various data modalities.
After you have a function that can compute embeddings of various items, you
compute the embedding of the items of interest and store this embedding in a database.
You then embed the incoming query in the same vector space as the items. Next, you have
to find the best matches to the query. This process is analogous to finding the most ‘similar’
matches across the entire collection of searchable vectors: similarity between vectors can be
computed using a metric such as euclidean distance, cosine similarity, or dot product.
 
### Important vector search algorithms
Using approximate nearest neighbor (ANN) search algorithms. Some of the most popular approaches:
- **Locality Sensitive Hashing (LSH)**: 
  - creating one or more hash functions that map similar items to the same hash
bucket with high probability. 
  - looking at the candidate items in the same hash bucket (or adjacent
buckets) and do a linear search amongst those candidate pairs. 
- **Tree-based**: 
  - **KD-Tree**: 
    - creating the decision boundaries by computing the median of the values of the first dimension, then
that of the second dimension and so on
    - Naturally this can be ineffective if searchable vectors are high dimensional
  - **Ball Tree**: 
    - instead of going by dimension-wise medians it creates buckets based on the radial distance of the data points
from the center. 
- **FAISS** Facebook AI similarity search
  - leverages the concept of hierarchical navigable small world (HNSW) to perform vector similarity search in sub-
linear (O(Logn)) runtime with a good degree of accuracy 
  - 
### Vector databases
Vector embeddings embody semantic meanings of data, while vector search algorithms
provide a means for efficiently querying them. 
Each vector database differs in its implementation, but the general flow is shown in Figure:
1. An appropriate trained embedding model is used to embed the relevant data points as
vectors with fixed dimensions.
2. The vectors are then augmented with appropriate metadata and complementary
information (such as tags) and indexed using the specified algorithm for efficient search.
3. An incoming query gets embedded with the same model, and used to query and return
specific amounts of the most semantically similar items and their associated unembedded
content/metadata. Some databases might provide caching and pre-filtering (based on
tags) and post-filtering capabilities (reranking using another more accurate model) to
further enhance the query speed and performance.
