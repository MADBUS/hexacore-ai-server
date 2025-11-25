from pydantic import BaseModel


class AnalyzePostRequest(BaseModel):
    """주식 게시글 분석 요청 모델"""
    raw_text: str

    class Config:
        json_schema_extra = {
            "example": {
                "raw_text": "삼성전자가 2분기 실적을 발표했습니다. 영업이익은 전년 대비 50% 증가한 12조원을 기록했으며, 메모리 반도체 부문의 회복세가 두드러졌습니다. 특히 HBM(고대역폭메모리) 수요 증가로 인해 3분기에도 좋은 실적이 예상됩니다."
            }
        }