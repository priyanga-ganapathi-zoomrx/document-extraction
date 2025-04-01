from pydantic import BaseModel
from typing import List, Optional
from typing_extensions import TypedDict


class Slide(BaseModel):
    slide_number: int
    base64_image: str


class DocumentMetadata(BaseModel):
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
    extracted_data: List[str]  # Markdown-formatted extraction results
    processing_complete: bool
    pdf_path: str
