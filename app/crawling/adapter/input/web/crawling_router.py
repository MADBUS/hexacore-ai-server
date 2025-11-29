from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from app.crawling.Engine.CrawlingEngine import CrawlingEngine, Article
from app.data.application.use_case.create_data_list import CreateDataList
from app.data.infrastructure.repository.data_repository_impl import DataRepositoryImpl
from app.keywords.infrastructure.repository.keyword_repository_impl import KeywordRepositoryImpl
from config.database.session import get_db


crawling_router = APIRouter(tags=["Crawling"])


class CrawlingResponse(BaseModel):
    articles: List[dict]
    total_count: int


@crawling_router.get("/paxnet", response_model=CrawlingResponse)
async def crawl_paxnet(
    page_count: int = Query(default=1, ge=1, le=5, description="크롤링할 페이지 수 (1-5)"),
    db: Session = Depends(get_db)
):
    """
    팩스넷 자유게시판 크롤링 및 DB 저장

    - page_count: 크롤링할 페이지 수 (기본 1, 최대 5)
    - 각 게시글의 제목, 본문, URL, 분석 결과를 반환하고 DB에 저장합니다.
    """
    engine = CrawlingEngine()
    articles = await engine.article_analysis(page_count=page_count)

    # DB 저장
    keyword_repository = KeywordRepositoryImpl(db)
    data_repository = DataRepositoryImpl(db, keyword_repository)
    use_case = CreateDataList(data_repository)

    items_to_save = [
        {
            "title": a.title,
            "content": a.content,
            "keywords": a.keywords,
            "published_at": a.published_at,
        }
        for a in articles
    ]

    if items_to_save:
        use_case.execute(items_to_save)
        db.commit()

    return CrawlingResponse(
        articles=[
            {"title": a.title, "content": a.content[:500], "url": a.url, "analysis": a.analysis}
            for a in articles
        ],
        total_count=len(articles)
    )


@crawling_router.get("/paxnet/test-parse")
async def test_parse_article():
    """
    파싱 로직 테스트 (실제 크롤링 없이 샘플 HTML로 테스트)
    """
    engine = CrawlingEngine()

    sample_html = """
    <html>
    <body>
        <h1>테스트 제목입니다</h1>
        <div class="board-view-cont">
            <p>이것은 테스트 본문입니다.</p>
        </div>
    </body>
    </html>
    """

    title, content = engine.parse_article(sample_html)

    return {
        "title": title,
        "content": content,
        "status": "파싱 로직이 정상 동작합니다"
    }
