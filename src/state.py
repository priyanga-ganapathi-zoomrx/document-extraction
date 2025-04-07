from pydantic import BaseModel
from typing import List, Optional, Dict
from typing_extensions import TypedDict

class Page(BaseModel):
    page_number: int
    image_path: str
    base64_image: str
    markdown: str

class GraphState(TypedDict):
    pages: List[Page]
    current_page: Optional[Page]
    processing_complete: bool
