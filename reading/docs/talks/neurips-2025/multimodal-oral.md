# Multimodal Oral

## **Dynam3D**

**Dynam3D**

[GitHub Repository](https://github.com/MrZihan/Dynam3D)

Slides: 

Vision and Language Navigation (VLN) - agents follow natural language instructions to navigate 3D environments

**Existing approaches**

**The Video Tape Approach**

- Treats world as stream of frames processed by video VLM
- Issues:
    - Spatial amnesia - forgets objects once they leave frame
    - Geometry blindness - 2D video lacks explicit 3D structure, leads to poor planning and collisions

**The Frozen Map Approach**

- Builds explicit 3D map and reasons with 3D VLM
- Issues:
    - Assumes static world - fails when objects move
    - Granularity efficiency trade-off - dense maps too slow, sparse maps lose semantic details

**Five Core Requirements for Good VLN Model:**

1. Explicit 3D structure (not just 2D appearances)
2. Multiple semantic scales (fine details to objects and rooms)
3. Compact enough to fit VLM context window
4. Update online as world changes
5. Bind language directly to 3D objects and regions

**Semantic Pyramid Tokenization**

Compresses millions of dense 3D feature points into manageable token set with three-level hierarchy:

**Patch Level:**

- Lifts CLIP patch features into 3D using DAPF
- Preserves fine-grained texture, edges, precise geometry
- ~557 tokens per image

**Instance Level:**

- Groups patch features using FastSAM mask
- Aggregates into persistent 3D object instances
- Reduces to ~300 tokens
- Tracks objects instead of fixed points

**Zone Level:**

- Divides 3D space into uniform cubic zones
- Aggregates instances within zones into room-level tokens
- Final count: just few thousand tokens

**Online 3D Instance Construction**

**Process:**

1. Generate 2D instances using FastSAM and instance encoder
2. Project into 3D and compare against existing instance memory
3. Get top K 3D instance matches based on feature distances
4. Pass candidates through learned merging discriminator
    - Selects best 2D to 3D matches using feature similarity and geometric distance
    - If object exists: update instance in 3D memory
    - If new: create new 3D instance

**Result:** Persistent, compact, language-grounded object memory that updates continuously

**Adapt to the Dynamic World**

**Dynamic Frustum Coordinating:**

- Adds new features when surfaces become newly visible
- Removes outdated features based on camera frustums and depth when objects move
- Prevents long-term accumulation of outdated information
- Keeps 3D memory physically consistent over time
- Essential for handling moving objects in real environments

**Dataset for Training**

**Scale:**

- 1,800+ object categories
- 5,000+ 3D scenes
- 2 million language descriptions
- Meticulously curated over multiple large 3D datasets
- Diversity key for generalization

**Contrastive Learning for Semantic Alignment**

**Three Complementary Losses:**

1. **Segmentation Loss:** Ensures accurate 2D to 3D instance grouping
2. **Distillation Loss:** Transfers CLIP knowledge into 3D instance and zone tokens
3. **Alignment Loss:** Directly grounds 3D tokens to natural language descriptions

**Multi-view Consistency:**

- Contrastively aligns features of same 3D instances across different viewpoints
- Pulls same instance features together, pushes different instances apart
- Produces view-invariant 3D embeddings crucial for stable reasoning as camera moves

**Multimodal Reasoning and Action Prediction**

**Architecture:**

- Patch, instance, zone tokens + natural language instruction + action history fed into lightweight 3.8B parameter VLM
- VLM fine-tuned to output continuous navigation actions (turning, moving forward, stopping)
- VLM reasons over structured dynamic 3D token memory instead of raw pixels

**Local Minima Mitigation:**

- Since no global map maintained, planner susceptible to local minima
- Maintains historical record of robot actions to mitigate this issue

**Evaluation Results:**

- Tested on three challenging VLN benchmarks
- Consistently outperforms video-based and map-based baselines in:
    - Navigation success
    - Path efficiency
    - Robustness to freeform instructions
- Successfully deployed on real robot in indoor environment
- Continues operating correctly even when objects move during execution

**Conclusion**

Dynam3D provides hierarchical, compact and dynamic 3D memory that is:

- Explicitly geometrical
- Continuously updated
- Directly grounded in language
- Key towards scalable embodied reasoning in real world
Vision and language navigation (VLN)

## **Perception Encoder: The best visual embeddings are not at the output of the network**

[Perception Encoder Paper](https://arxiv.org/abs/2504.13181)

**PE Core**

- State-of-the-art image and video joint CLIP model
- Built by making CLIP recipe robust through eliminating shortcuts
    - Varied resolution during training to prevent overfitting
    - Increased batch size for more hard negatives
    - Improvements plateaued on ImageNet validation but significantly boosted robustness metrics
- Extended to video using synthetic data engine
    - Used image-only model as frame-based encoder
    - Built custom Perception LLM for video captioning
    - Video fine-tuning surprisingly improved image performance too
- Outperforms SigLIP-2 at all model scales on classification, fine-grained classification, and retrieval
- Demonstrates superior compositionality and robustness compared to CLIP-L
    - Better understanding of complex queries like “orange berries” and “blue street sign with white text”
    - More robust to image variations (night vision example with raccoons vs opossums)

**PE Lang (alignment method)**

- Addresses problem: PE Core has strong language features in intermediate layers but poor last-layer performance
- Solution: Fine-tune Perception LM on top of PE model for 60M samples
- Results in state-of-the-art multimodal LLM performance
    - Stronger than InternVL-1.5 and Qwen2-VL at time of publication
    - Successfully aligns language features to final layer
- Enables strong performance on OCR QA and visual QA tasks

**PE Spatial**

- Challenge: Spatial features degraded at last layer due to global tokens appearing after layer 32
- Solution: Self-distillation approach
    - Distill model to itself at earlier layer (~layer 40)
    - Use SAM mask logic features for enhanced locality
    - Combines semantic understanding with clean spatial features
- Achieves state-of-the-art COCO detection performance
- Qualitative results show clean, semantic part-level similarities
- Addresses dense prediction tasks like detection, tracking, depth estimation

## **Interactive Cross-modal Learning for Text-3D Scene Retrieval**

**Overview**

- IDeal: Interactive Text-3D Scene Retrieval method enhancing alignment between text queries and 3D scenes through continuous interaction
- Four main contributions:
    1. Interactive text-3D retrieval method with active alignment enhancement
    2. Interactive Retrieval Refinement (IRR) framework supporting structural interaction
    3. Interaction Adaptation Tuning (IAT) strategy
    4. Comprehensive experimental validation demonstrating superiority
- [Paper](https://arxiv.org/pdf/2502.19128) available.

**Open World Obstacles**

- Incomplete one-shot descriptions fail to capture user intent
    - Single shot queries provide limited scene summaries
    - Lead to mismatches between queries and retrieval results
- Domain shifts across users with different languages, regional experiences, semantic skills
    - Models trained on one text type struggle to generalize to other niches
- Ambiguous/unspecific descriptions in complex scenes
    - Users omit crucial details or use vague terms
    - Significantly impairs accuracy and reliability
- Limited generalization of static models
    - Unable to adapt to new contexts and scenarios
    - Constrained by internal knowledge within pre-trained models

**Motivation**

- Leverage interactive retrieval with external agents (e.g. LLM) for general solution
- Two main challenges identified:
    1. Applying existing interactive methods to text-3D scene retrieval
        - Current methods lack holistic interaction perspective for complex scenes
        - Focus limited to initially described regions rather than entire spatial layouts
    2. Making existing static retrieval methods interactive
        - Static models struggle to adapt to interactive text inputs
        - Domain gap between original training and interactive scenarios
- Performance gap evidence: enriched text from interactions only achieved 30.67 recall@1 with 7-point gain

**Method**

- Interactive Retrieval Refinement (IRR) Framework:
    - Coordinates questioner, answerer, and retriever for continuous interactions
    - Questioner posts questions based on dense capacity entropy between response and scene features
    - Answerer describes scenes based on user responses
    - Retriever performs comprehensive retrieval from three perspectives:
        1. Initial query processing for baseline prediction
        2. Multi-round response integration using weighted linear fusion
        3. Semantic-level feature extraction and summarization
- Interaction Adaptation Tuning (IAT) Strategy:
    - Addresses domain adaptation challenge for static-to-interactive transition
    - Two-step process:
        1. Construct simulated memory for text augmentation using training data descriptions
        2. Adapt model using discriminability and diversity risk minimization
    - Loss terms ensure matched pairs cluster together while negative pairs remain separated
- Experimental Results:
    - Effective under coarse-grained memory without additional information
    - Novel performance improvement over existing 2D and interactive methods under fine-grained memory
    - Seamless integration with conventional cross-modal retrieval methods
    - Substantial performance gains demonstrated across three datasets

## **CoralVQA: A Large-Scale Visual Question Answering Dataset for Coral Reef Image Understanding**

[Paper](https://arxiv.org/abs/2507.10449)

Abstract:
Coral reefs are vital yet vulnerable ecosystems that require continuous monitoring to support conservation. While coral reef images provide essential information in coral monitoring, interpreting such images remains challenging due to the need for domain expertise. Visual Question Answering (VQA), powered by Large Vision-Language Models (LVLMs), has great potential in user-friendly interaction with coral reef images. However, applying VQA to coral imagery demands a dedicated dataset that addresses two key challenges: domain-specific annotations and multidimensional questions. In this work, we introduce CoralVQA, the first large-scale VQA dataset for coral reef analysis. It contains 12,805 real-world coral images from 67 coral genera collected from 3 oceans, along with 277,653 question-answer pairs that comprehensively assess ecological and health-related conditions. To construct this dataset, we develop a semi-automatic data construction pipeline in collaboration with marine biologists to ensure both scalability and professional-grade data quality. CoralVQA presents novel challenges and provides a comprehensive benchmark for studying vision-language reasoning in the context of coral reef images. By evaluating several state-of-the-art LVLMs, we reveal key limitations and opportunities. These insights form a foundation for future LVLM development, with a particular emphasis on supporting coral conservation efforts

**Background**

- Coral reefs are vital yet vulnerable ecosystems requiring continuous monitoring for conservation
- Current global mass coral bleaching event affecting 44% of world’s coral across 53+ countries over 40 years
    - Worst coral bleaching event ever recorded
- Coral reef image interpretation requires extensive domain expertise
- Visual Question Answering (VQA) powered by Large Vision-Language Models (LVLMs) offers potential for user-friendly coral image interaction
- Current coral datasets focus mainly on classification and segmentation tasks

**Find interesting ways for meaningful things**

- VQA can help bridge the gap between complex ecological assessment and clear insights
- Translates domain-specific coral analysis into accessible format for broader understanding
- Enables answering questions about coral health, diversity, bleaching coverage through natural language interaction

**Problem**

- Absence of comprehensive, high-quality VQA datasets for coral conservation
- Coral reef VQA presents unique challenges:
    - Domain-specific labels requiring expert knowledge
    - Multidimensional/multi-task questions covering various aspects of coral health
- Building VQA datasets for coral reefs more challenging than general image datasets
    - Requires marine biology expertise for question-answer generation
    - Multiple scale questions needed concurrently

**Work**

- CoralVQA: First large-scale VQA dataset for coral reef analysis
- Dataset specifications:
    - 12,805 real-world coral images from 67 coral genera
    - Images collected from 3 oceans across different geographic regions
    - 277,653 question-answer pairs for comprehensive ecological assessment
- Semi-automatic data construction pipeline developed with marine biologists
- Provides comprehensive benchmark for vision-language reasoning in coral reef context

**Data pipeline**

- Six-stage process:
    1. Data collection → 2. Label cleaning → 3. Textual attribute extraction → 4. Prompt engineering → 5. Question-answer generation → 6. Human verification
- Data sources:
    1. RC dataset
    2. XL co clean survey project
    3. Cores of the world namespace
- Attribute organization into key groups:
    1. Basic real-world fields
    2. Health-related attributes
- Quality assurance through three-stage process:
    1. Human manual tagging
    2. Cross tagging
    3. Expert validation
- Images span different marine regions across multiple countries and oceans
- Average coral coverage: 21.6%
- Average bleached area coverage: 14.4%

**Evaluation**

- Three evaluation subsets created:
    1. **Test dataset** - Standard performance evaluation
    2. **Cross-region dataset** - Tests model generalization across different geographic locations
    3. **Bleaching-coverage dataset** - Specialized for coral bleaching assessment tasks
- Performance results:
    1. Zero-shot performance drops significantly on coral-specific tasks
    2. Internal models show stronger average performance across both groups
    3. Cross-region evaluation shows 13% performance decrease, indicating generalization challenges
- Coral bleaching evaluation metrics:
    1. Current best model MASC scores: 1.2326 (channel) and 0.8967 (income)
    2. Models tend to overestimate bleaching region size and extent
    3. Significant challenges remain in complex reasoning tasks for coral analysis
- Key finding: Current vision-language models struggle with understanding and complex reasoning in coral reef contexts

## **OpenHOI: Open-World Hand-Object Interaction Synthesis with Multimodal Large Language Model**

[Paper](https://arxiv.org/abs/2505.18947)

**OpenHOI Framework Overview**

- First open-world hand-object interaction synthesis framework
- Generates realistic motion sequences for unseen objects using open vocabulary language instructions
- Addresses two key challenges:
    - Handling unseen objects in open-world scenarios
    - Processing open vocabulary free-form instructions

**Technical Architecture**

- Two main components:
    1. Affordance and subtask decomposition
    2. Diffusion-driven HOI generation
- 3D Multimodal LLM (MLLM):
    1. Processes open vocabulary instructions via language encoder
    2. Handles 3D point clouds through 3D vision encoder
    3. Outputs sequence of subtasks and 3D affordance maps
- Affordance decoder:
    1. Takes object features and event program
    2. Generates 3D affordance maps over point clouds
    3. Specifies where hand should interact with objects

**Training and Generation Process**

- Two-stage training approach:
    - Stage 1: Object-centric affordance learning
    - Stage 2: Full instruction alignment with 3D affordance masks
- Diffusion model conditioning:
    - Object geometry
    - Subtask decomposition
    - 3D affordance maps from MLLM
- Training objectives:
    - Standard diffusion loss
    - Auxiliary losses (hand-object contact, orientation)
    - Classifier guidance for better object/affordance alignment
    - Compositional noise scheduling for motion refinement

**Applications and Results**

- Example interaction: “I want to write a paper using my laptop”
    - System decomposes into three subtasks
    - Generates realistic motion sequence for each subtask
- State-of-the-art performance across evaluation metrics
- Handles complex multi-step interactions:
    - Brushing teeth, taking photos, making phone calls
    - Opening/closing objects with both hands
    - Playing with toys, eating fruit, making toast
- Achieves strong generalization through 3D MLLM processing of open vocabulary targets