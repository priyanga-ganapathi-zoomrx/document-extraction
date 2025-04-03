# state.py
from pydantic import BaseModel
from typing import List, Optional, Dict
from typing_extensions import TypedDict


class ModelExtraction(BaseModel):
    """Represents an extraction result from a single model."""

    model_name: str  # e.g., "gemini-1.5-pro", "gpt-4", "claude-3-opus"
    provider: str  # e.g., "google", "openai", "anthropic"
    extraction: str  # The markdown extraction result


class Slide(BaseModel):
    """Represents a slide from the presentation."""

    slide_number: int
    base64_image: str
    model_extractions: List[ModelExtraction] = []
    aggregated_extraction: Optional[str] = None


class DocumentMetadata(BaseModel):
    """Metadata about the document."""

    title: str
    company: str
    date: str
    event: str
    document_id: str


class GraphState(TypedDict, total=False):
    """Graph state with optional fields"""

    document_metadata: Optional[DocumentMetadata]
    slides: List[Slide]
    current_slide: Optional[Slide]
    extracted_data: List[str]
    processing_complete: bool
    pdf_path: str
