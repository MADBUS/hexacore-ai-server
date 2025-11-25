from fastapi import APIRouter, HTTPException, Depends

from app.post_analysis.adapter.input.web.request.analyze_post_request import AnalyzePostRequest
from app.post_analysis.adapter.input.web.response.document_analysis_response import StockPostAnalysisResponse
from app.post_analysis.application.usecase.analyze_document import AnalyzeStockPostUseCase
from app.post_analysis.infrastructure.service.openai_service_impl import OpenAIServiceImpl
from config.settings import Settings, get_settings


post_analysis_router = APIRouter(tags=["post_analysis"])


@post_analysis_router.post("/analyze", response_model=StockPostAnalysisResponse)
async def analyze_post(
    request: AnalyzePostRequest,
    settings: Settings = Depends(get_settings)
):
    """
    POST /post-analysis/analyze - 주식 게시글 분석

    크롤링된 주식 게시글 텍스트를 분석하여 title, content, keywords를 추출합니다.

    Args:
        request: raw_text가 포함된 요청 모델 (크롤링된 원본 텍스트)
        settings: 애플리케이션 설정

    Returns:
        StockPostAnalysisResponse: 분석 결과 (title, content, keywords)
    """
    try:
        # 서비스 초기화
        openai_service = OpenAIServiceImpl(api_key=settings.OPENAI_API_KEY)

        # 유스케이스 실행
        use_case = AnalyzeStockPostUseCase(openai_service)
        result = await use_case.execute(request.raw_text)

        return StockPostAnalysisResponse(
            title=result.title,
            content=result.content,
            keywords=result.keywords
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")