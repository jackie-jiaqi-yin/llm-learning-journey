# Topic Template Guide

This template provides a standardized structure for documenting new topics in your LLM learning journey.

## How to Use This Template

1. **Copy the entire `_TEMPLATE` directory**
   ```bash
   cp -r reading/docs/topics/_TEMPLATE reading/docs/topics/YourNewTopic
   ```

2. **Fill in the three main files:**
   - `index.md` - Landing page with brief overview and contents
   - `notes.md` - Comprehensive notes, concepts, and best practices
   - `paper-review.md` - Detailed reviews of relevant research papers

3. **Add figures/images:**
   - Place all images in the `figs/` directory
   - Reference them using relative paths: `figs/your-image.png`

4. **Update the main topics index:**
   - Add your new topic to `reading/docs/topics/index.md`

## File Structure

```
YourNewTopic/
├── index.md          # Landing page
├── notes.md          # Comprehensive notes
├── paper-review.md   # Paper reviews
├── figs/             # Images and diagrams
└── README.md         # (optional) Additional documentation
```

## Template Sections

### index.md
- Topic title and brief description
- Contents listing with links to notes and paper reviews
- Tagline or learning objective

### notes.md
- Overview and key concepts
- Core components and workflow
- Best practices and challenges
- Common approaches and methods
- Technical implementation details
- Use cases and tools
- Further reading and key takeaways

### paper-review.md
- Table of contents (links to each paper)
- Detailed review for each paper including:
  - Summary and publication info
  - Problem statement and motivation
  - Methodology and architecture
  - Key findings and results
  - Limitations and takeaways
  - Resources (paper link, code, demo)

## Tips for Filling Out the Template

### For notes.md:
- Start with a clear overview that sets context
- Break down complex concepts into digestible sections
- Include diagrams and visual aids where helpful
- Provide practical examples and use cases
- List relevant tools and frameworks in a table
- End with key takeaways that summarize main points

### For paper-review.md:
- Add papers in chronological order or by importance
- Include publish dates to track research timeline
- Use diagrams from papers to illustrate concepts
- Focus on practical insights and innovations
- Link to original papers and any available code
- For less critical papers, use the brief overview format

### For images:
- Use descriptive filenames (e.g., `workflow-diagram.png`, `architecture.png`)
- Always include figure captions
- Optimize images for web viewing
- Support both light and dark mode if possible

## What to Delete

When creating a new topic:
- Remove this README.md (or customize it for your topic)
- Delete placeholder sections you won't use
- Remove empty or irrelevant sections
- Clean up the `figs/` directory

## Customization

Feel free to:
- Add custom sections relevant to your topic
- Adjust the structure to fit the content
- Combine or split sections as needed
- Add additional files (e.g., `examples.md`, `tutorial.md`)

The template is a guide, not a strict requirement. Adapt it to best serve your learning and documentation needs.
