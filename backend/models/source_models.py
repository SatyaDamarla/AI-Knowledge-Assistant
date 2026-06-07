from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class SourceRecord(BaseModel):
    user_id: str = Field(..., description="ID of the user who owns this source")
    source_id: str = Field(..., description="Unique source identifier")
    source_type: str = Field(..., description="Source type: pdf | youtube | text")
    title: str = Field(..., description="Human-readable source title")

    original_name: Optional[str] = Field(
        default=None,
        description="Original uploaded filename if applicable"
    )
    storage_path: Optional[str] = Field(
        default=None,
        description="Path to original stored file"
    )
    raw_text_path: Optional[str] = Field(
        default=None,
        description="Path to normalized extracted text"
    )
    url: Optional[str] = Field(
        default=None,
        description="Original URL for source types like youtube"
    )
    status: str = Field(
        default="pending",
        description="Source lifecycle status: pending | indexed | failed"
    )
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="ISO timestamp when source was created"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Flexible source-specific metadata"
    )


class LoadedSourceContent(BaseModel):
    user_id: str
    source_id: str
    source_type: str
    title: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChunkRecord(BaseModel):
    user_id: str
    chunk_id: str
    source_id: str
    source_type: str
    title: str
    chunk_index: int
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)