from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from typing_extensions import TypedDict

class Snippet(BaseModel):
    """Represents a single extracted snippet with a title and content."""
    title: str = Field(description="The title or heading for the snippet, often indicating the page number or main topic (e.g., 'Page 1', 'Snippet 1: Overall Performance Context and Scope').")
    content: str = Field(description="The main text content of the snippet, excluding the title line.")
    enriched_content: Optional[str] = Field(default=None, description="Enriched version of the content with entity labels.")

class ExtractedData(BaseModel):
    """A collection of extracted snippets."""
    snippets: List[Snippet] = Field(description="An array containing all the extracted snippets from the document.")

class Page(BaseModel):
    page_number: int
    image_path: str
    snippets: List[Snippet]
class GraphState(TypedDict):
    pages: List[Page]
    current_page: Optional[Page]
    processing_complete: bool
    aggregated_snippets: str

