IMAGE_TO_SNIPPET_PROMPT = """You are given an image containing text from a life science market intelligence document. Your goal is to convert the text in the image into a collection of “snippets.” Each snippet must have:

1. A **title** (string) describing the snippet's main idea or indicating a page/section heading (e.g., "Executive Summary").
2. A **content** (string) preserving all relevant information for that snippet.

Please follow these rules:

- **Do not omit any essential data**; ensure the snippet text fully preserves the original meaning.
- **Do not include extra commentary** beyond what is in the document.
- **Structure your output** as **valid JSON** adhering exactly to the following pydantic schema:

  **ExtractedData**  
  ├─ **snippets** (array of **Snippet** objects)  
  │   ├─ **title** (string)  
  │   └─ **content** (string)

- The top-level JSON object must have exactly one key: `"snippets"`.
- Each item in `"snippets"` must be a JSON object with `"title"` and `"content"`.

For example, your output should look like:

```
{
  "snippets": [
    {
      "title": "Snippet 1: [Descriptive Title]",
      "content": "[Paragraph of text…]"
    },
    {
      "title": "Snippet 2: [Descriptive Title]",
      "content": "[Paragraph of text…]"
    }
  ]
}
```

**Return only the JSON**—no markdown, no code blocks, and no explanatory text. 

Convert the content of the image into multiple comprehensive paragraphs, each placed in a separate snippet. Ensure no information is lost in the process.
"""

SNIPPET_TO_ENRICHED_SNIPPET_PROMPT = """# Life Sciences Snippet Enrichment Prompt

## Task
Enrich provided life sciences text snippets by identifying and labeling key entities. The labeled output will be used for database insertion. Maintain the exact format of the original snippet while adding entity labels in curly brackets.

## Entity Types to Identify
Based on the database schema, identify and label these entity types:

1. **Drug/Compound** - Therapeutic agents (e.g., remibrutinib, iptacopan)
2. **Company/Firm** - Pharmaceutical/biotech companies 
3. **Disease/Indication** - Medical conditions (e.g., MS, ALS, AD)
4. **Therapeutic Area** - Broader disease categories (e.g., Neuroscience, Oncology)
5. **Target** - Molecular targets (e.g., TREM2, tau)
6. **Drug Class** - Categories of drugs with similar mechanisms
7. **Modality** - Therapeutic approaches (e.g., ASO, antibody)
8. **Development Stage** - Clinical phases (e.g., Phase I, Phase III)
9. **Geographic Region** - Countries or regions mentioned
10. **Clinical Milestone** - Key development events (e.g., readout, submission)
11. **Timeline** - Dates or timeframes (e.g., 2025, 2026)
12. **Study Type** - Types of clinical trials

## Output Format
Return the snippet in its original format but add entity labels in curly brackets immediately after each entity. For example:

Original: "Remibrutinib (MS) | Phase III | Readout 2026"
Labeled: "Remibrutinib {drug} (MS {disease}) | Phase III {development_stage} | Readout {clinical_milestone} 2026 {timeline}"

## Using Tavily Search Tool
- **ALWAYS** use the Tavily search tool when uncertain about entity classification
- For any unfamiliar drugs, targets, or disease abbreviations, search to verify the correct classification
- Example search queries:
  - "What is remibrutinib drug classification"
  - "MS disease abbreviation medical"
  - "TREM2 molecule classification"
- Base classifications on search results rather than guessing
- Use search results to help interpret abbreviations and specialized terms

## Special Instructions
1. Maintain the exact structure, spacing, and formatting of the original snippet
2. Place labels immediately after the identified entity without spaces
3. When multiple adjacent words form a single entity, apply the label after the complete entity
4. For ANY uncertain entity, use the Tavily search tool before assigning a classification
5. Be especially careful with abbreviations - verify with search when uncertain
6. Don't change the original text, only add labels

## Example Input
```
Selected projects (indication) | Phase | Next milestone/status
Remibrutinib (MS) | Phase III | Readout 2026
Iptacopan (gMG) | Phase III | Readout 2027
```

## Example Output
```
Selected projects (indication) | Phase | Next milestone/status
Remibrutinib {drug} (MS {disease}) | Phase III {development_stage} | Readout {clinical_milestone} 2026 {timeline}
Iptacopan {drug} (gMG {disease}) | Phase III {development_stage} | Readout {clinical_milestone} 2027 {timeline}
```

Remember to maintain the exact formatting of the input while adding entity labels in curly brackets, and ALWAYS use the Tavily search tool when uncertain about classifications."""
