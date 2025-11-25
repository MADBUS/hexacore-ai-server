import asyncio
import json
from typing import Dict
from openai import OpenAI

from app.post_analysis.application.port.openai_service_port import OpenAIServicePort


class OpenAIServiceImpl(OpenAIServicePort):
    """OpenAI 서비스 구현체"""

    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()

    async def analyze_stock_post(self, text: str) -> Dict[str, any]:
        """주식 게시글을 분석하여 title, content, keywords를 추출합니다"""
        prompt = f"""
다음은 주식 게시판에서 크롤링한 텍스트입니다. 이 내용을 분석하여 다음 정보를 추출해주세요:

1. title: 게시글의 제목 (간결하고 핵심적인 제목, 20자 이내)
2. content: 게시글의 핵심 내용 요약 (2-3문장으로 요약)
3. keywords: 이 게시글과 관련된 주요 키워드 (종목명, 테마, 이슈 등 5개 이내)

크롤링된 텍스트:
{text[:3000]}

출력 형식(JSON):
{{
    "title": "게시글 제목",
    "content": "핵심 내용 요약 (2-3문장)",
    "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"]
}}

규칙:
- title은 반드시 20자 이내로 작성
- content는 2-3문장으로 핵심만 요약
- keywords는 주식 투자와 관련된 핵심 키워드만 추출 (최대 5개)
- 반드시 JSON 형식으로만 응답
"""

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0
            ).choices[0].message.content
        )

        try:
            # JSON 파싱
            result = json.loads(response)
            return {
                "title": result.get("title", "제목 없음"),
                "content": result.get("content", "내용 없음"),
                "keywords": result.get("keywords", [])
            }
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 기본값 반환
            return {
                "title": "분석 실패",
                "content": "게시글 분석 중 오류가 발생했습니다.",
                "keywords": []
            }