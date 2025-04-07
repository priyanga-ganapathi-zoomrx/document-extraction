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
