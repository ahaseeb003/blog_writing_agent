from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class Section(BaseModel):
    id: int
    heading: str
    subheading: Optional[str] = None
    research_needed: bool = False
    content: Optional[str] = None
    image_suggestion: Optional[Dict[str, str]] = None

class Task(BaseModel):
    id: int
    section_id: int
    description: str
    status: str = "pending"

class BlogState(BaseModel):
    topic: str
    research_required: bool = False
    outline: List[Section] = Field(default_factory=list)
    tasks: List[Task] = Field(default_factory=list)
    research_data: List[Dict[str, Any]] = Field(default_factory=list)
    worker_outputs: Dict[int, str] = Field(default_factory=dict)
    citations: List[str] = Field(default_factory=list)
    images: List[Dict[str, Any]] = Field(default_factory=list)
    review_feedback: List[str] = Field(default_factory=list)
    final_blog: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
