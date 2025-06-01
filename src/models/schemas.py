from typing import List, Optional
from pydantic import BaseModel

class Document(BaseModel):
    filename: str
    content: str
    size: int

class CategorySuggestion(BaseModel):
    name: str
    invoice_ids: List[int]
