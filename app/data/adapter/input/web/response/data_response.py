from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class DataKeywordResponse(BaseModel):
    id: int
    name: str


class DataResponse(BaseModel):
    """정보 응답 모델"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    published_at: datetime
    keywords: List[DataKeywordResponse]