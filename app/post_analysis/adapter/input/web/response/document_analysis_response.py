from typing import List
from pydantic import BaseModel


class StockPostAnalysisResponse(BaseModel):
    """주식 게시글 분석 결과 응답 모델"""
    title: str
    content: str
    keywords: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "삼성전자 실적 발표",
                "content": "삼성전자가 2분기 실적을 발표했으며, 예상을 상회하는 영업이익을 기록했습니다. 메모리 반도체 부문의 회복세가 두드러졌습니다.",
                "keywords": ["삼성전자", "실적발표", "메모리반도체", "영업이익", "2분기"]
            }
        }