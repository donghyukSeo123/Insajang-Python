from pydantic import BaseModel
from typing import Optional

class ContentCreate(BaseModel):
    project_id: int
    title: str
    user_input: str

class ContentResponse(BaseModel):
    content_id: int
    generated_text: str