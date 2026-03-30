from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class HistoryCreate(BaseModel):
    workout_id: int
    notes: Optional[str] = Field(default=None, max_length=500)


class HistoryResponse(BaseModel):
    id: int
    workout_id: int
    workout_name: str
    completed_at: datetime
    notes: Optional[str]

    model_config = {"from_attributes": True}
