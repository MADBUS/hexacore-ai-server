from datetime import datetime
from typing import List, Optional


class DataKeywordSummary:
    """
    데이터에 연결된 키워드 정보 요약
    """

    def __init__(self, keyword_id: int, name: str):
        self.id = keyword_id
        self.name = name


class Data:
    def __init__(
        self,
        title: str,
        content: str,
        published_at: datetime,
        keywords: Optional[List[DataKeywordSummary]] = None,
    ):
        self.id: Optional[int] = None
        self.title = title
        self.content = content
        self.published_at = published_at
        self.keywords: List[DataKeywordSummary] = keywords or []

    def add_keyword(self, keyword: DataKeywordSummary) -> None:
        self.keywords.append(keyword)