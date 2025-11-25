from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class CreateDataItemRequest(BaseModel):
    """단일 데이터 생성 요청"""

    title: str = Field(..., description="제목")
    content: str = Field(..., description="내용")
    published_at: datetime = Field(..., description="발행 시간")
    keywords: List[str] = Field(default_factory=list, description="키워드 목록")


class CreateDataListRequest(BaseModel):
    """여러 데이터를 한 번에 생성하는 요청"""

    items: List[CreateDataItemRequest] = Field(..., description="데이터 목록")

