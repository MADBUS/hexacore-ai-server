from abc import ABC, abstractmethod
from typing import Dict


class OpenAIServicePort(ABC):
    """OpenAI 서비스 포트 (인터페이스)"""

    @abstractmethod
    async def analyze_stock_post(self, text: str) -> Dict[str, any]:
        """
        주식 게시글을 분석하여 title, content, keywords를 추출합니다

        Returns:
            {
                "title": str,
                "content": str,
                "keywords": List[str]
            }
        """
        pass