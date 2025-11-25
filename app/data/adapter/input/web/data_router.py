from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data.adapter.input.web.request.create_data_request import (
    CreateDataListRequest,
)
from app.data.adapter.input.web.response.data_response import (
    DataKeywordResponse,
    DataResponse,
)
from app.data.application.use_case.create_data_list import CreateDataList
from app.data.application.use_case.get_data_list import GetDataList
from app.data.infrastructure.repository.data_repository_impl import (
    DataRepositoryImpl,
)
from app.data_keyword.infrastructure.repository.data_keyword_repository_impl import (
    DataKeywordRepositoryImpl,
)
from app.keywords.adapter.input.web.response.keyword_response import (
    KeywordMentionResponse,
)
from app.keywords.application.use_case.get_top_keywords import GetTopKeywords
from app.keywords.infrastructure.repository.keyword_repository_impl import (
    KeywordRepositoryImpl,
)
from config.database.session import get_db

data_router = APIRouter()


@data_router.get("/", response_model=List[DataResponse])
def get_data(limit: int = 20, db: Session = Depends(get_db)):
    repository = DataRepositoryImpl(db)
    use_case = GetDataList(repository)
    data_list = use_case.execute(limit=limit)

    return [
        DataResponse(
            id=data.id,
            title=data.title,
            content=data.content,
            published_at=data.published_at,
            keywords=[
                DataKeywordResponse(id=keyword.id, name=keyword.name)
                for keyword in data.keywords
            ],
        )
        for data in data_list
    ]


@data_router.get("/top-keywords", response_model=List[KeywordMentionResponse])
def get_top_keywords(limit: int = 5, db: Session = Depends(get_db)):
    repository = KeywordRepositoryImpl(db)
    use_case = GetTopKeywords(repository)
    mentions = use_case.execute(limit=limit)

    return [
        KeywordMentionResponse(
            id=mention.id,
            name=mention.name,
            mention_count=mention.mention_count,
        )
        for mention in mentions
    ]


@data_router.post("/", response_model=List[DataResponse], status_code=status.HTTP_201_CREATED)
def create_data_list(
    request: CreateDataListRequest, db: Session = Depends(get_db)
):
    """
    여러 데이터를 한 번에 생성
    JSON 형태: {"items": [{"title": str, "content": str, "published_at": datetime, "keywords": List[str]}, ...]}
    """
    try:
        data_repository = DataRepositoryImpl(db)
        keyword_repository = KeywordRepositoryImpl(db)
        data_keyword_repository = DataKeywordRepositoryImpl(db)

        use_case = CreateDataList(
            data_repository, keyword_repository, data_keyword_repository
        )

        # 요청 데이터를 딕셔너리 리스트로 변환
        items = [
            {
                "title": item.title,
                "content": item.content,
                "published_at": item.published_at,
                "keywords": item.keywords,
            }
            for item in request.items
        ]

        created_data_list = use_case.execute(items)

        # 트랜잭션 커밋
        db.commit()

        # 응답 생성 (키워드 정보 포함)
        response_list = []
        for data in created_data_list:
            # 키워드 ID 조회
            keyword_ids = data_keyword_repository.get_keyword_ids(data.id)
            # 키워드 정보 조회
            keywords = []
            for keyword_id in keyword_ids:
                keyword = keyword_repository.find_by_id(keyword_id)
                keywords.append(
                    DataKeywordResponse(id=keyword.id, name=keyword.name)
                )

            response_list.append(
                DataResponse(
                    id=data.id,
                    title=data.title,
                    content=data.content,
                    published_at=data.published_at,
                    keywords=keywords,
                )
            )

        return response_list

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터 생성 중 오류가 발생했습니다: {str(e)}",
        )

