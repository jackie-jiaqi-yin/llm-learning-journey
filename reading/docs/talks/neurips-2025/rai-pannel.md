## Responsible AI Research & Unlearning: From Consent to Compliance to Critique

**Research Findings on Non-Consensual Imagery**

- **Princessa Cinquecchia (Boston University)** - systematic review of nude image use in AI research
    - Analyzed 150 computer science papers using real nude images without consent
    - Over 8 million non-consensual nude images identified across papers
    - 8 papers published 2023+ in flagship venues (ACCP, CBPR, AAA)
    - Growing trend - majority published in last 5 years
- Content sources include:
    - Banned Reddit communities with abusive content
    - Hidden camera footage and upskirt images
    - Child sexual abuse material (explicitly mentioned in some papers)
    - Pornography industry content used without creator consent
- Published papers show identifiable faces without censoring
- Recommendation: Partner with industry platforms before conducting research, question necessity of using nude imagery

**Machine Unlearning for AI Regulation Compliance**

- **Bill Marino (Cambridge)** - bridging machine unlearning and AI regulation
    - EU AI Act as proof of concept (world’s first comprehensive AI regulation, already in effect)
    - Identified 6 potential use cases for machine unlearning in regulatory compliance
    - Significant gaps exist between current unlearning capabilities and regulatory needs
- Economic motivation: billion-dollar training runs make retraining prohibitive
    - Machine unlearning offers alternative to full model retraining
    - Trade-offs exist: removing mislabeled data may introduce bias or security vulnerabilities
- Specific compliance challenge: accuracy requirements
    - Identifying “forget sets” (bad/mislabeled data) difficult at scale
    - Paring down datasets may violate other AI Act provisions

**Technical Limitations of Machine Unlearning**

- **A. Feder Cooper (Yale)** - “Machine Unlearning Doesn’t Do What You Think”
    - Gold standard assumption flawed: retraining from scratch with unwanted data removed
    - Models learn latent information beyond just repeating training data
    - Example: Creative Commons-trained diffusion model still generates Mickey Mouse when prompted
- Scope expansion beyond data removal:
    - Originally focused on removing specific training data influence
    - Now includes suppressing unwanted generative outputs
    - Encompasses alignment methods and content filters
- Gap between technical capabilities and policy expectations
    - Need conceptual clarity between different “unlearning” techniques
    - Removal vs suppression serve different goals
    - Policymaker education needed on technique limitations and appropriate applications

## Strengthening the AI Research Ecosystem: Integrity, Critique, and Consensus

**AI Research Integrity Challenges**

- **DDoS Attack on Research Community** (Jiang Hao Lin)
    - AI-generated survey papers overwhelming review capacity and research attention
    - Arxiv implemented stricter policy (Oct 2024) - only peer-reviewed surveys allowed
    - Wrong reward signals: AI-generated surveys on hot topics getting 100+ citations with minimal effort
    - MCP protocol example: 5+ survey papers in one month, content already outdated
    - Hallucinations in AI surveys become “truth” especially for junior researchers
- **Current Incentive Problems**
    - Bad behavior rewarded: 30-minute ChatGPT surveys getting high citations
    - Quality research vs. gaming the system misalignment
    - Citation count not reliable quality indicator anymore

**Proposed Solutions**

- **Refutations and Critiques Track** (Rylan Shaffer)
    - New venue for correcting scientific record
    - Address misleading, incorrect, flawed, or fraudulent research
    - Current problem: negative results seen as ad hominem, hard to publish
    - Need consequences for malfeasance when discovered
    - Arxiv comments feature exists but underutilized
- **Scientific Consensus Building** (Rishi Wamansi)
    - NeurIPS should facilitate consensus on policy-relevant topics
    - Not universal agreement, but articulated consensus where it exists
    - Policymakers need peer-reviewed research basis for reports
    - No better alternative institution than NeurIPS for this role
    - Requires innovation in conference structure
- **Individual Actions**
    - Speak out about problematic prior research despite difficulty
    - Use AI as copilot, not autopilot for survey writing
    - Don’t rely solely on citation count for survey quality
    - Consult senior researchers when entering new fields

**Next Steps**

- **Community Engagement Needed**
    - Articulate demand and volunteer capacity for new tracks
    - Show substantive interest beyond just proposing changes
    - Consider celebrating negative results and “spectacular failures”
    - Shift incentives to reward vulnerability and honest reporting
- **Alternative Approaches Discussed**
    - Specialized reviewers for failure/learning tracks
    - Collaboration with policy think tanks and social scientists
    - Better utilization of existing Arxiv comment system
    - Focus on synthetic reviews vs. annotated bibliographies