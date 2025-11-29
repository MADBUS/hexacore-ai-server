from typing import List, Optional, Dict, Any


class Data:
    def __init__(
        self,
        title: str,
        content: str,
        published_at: str,
        keywords: Optional[List[str]] = None,
        url: str = "",
        analysis: Optional[Dict[str, Any]] = None,
    ):
        self.id: Optional[int] = None
        self.title = title
        self.content = content
        self.keywords: List[str] = keywords or []
        self.published_at = published_at
        self.url = url
        self.analysis = analysis

    def add_keyword(self, keyword: str) -> None:
        self.keywords.append(keyword)