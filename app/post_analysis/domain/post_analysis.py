from dataclasses import dataclass
from typing import List


@dataclass
class PostAnalysisResult:
    """주식 게시글 분석 결과 도메인 엔티티"""
    title: str
    content: str
    keywords: List[str]