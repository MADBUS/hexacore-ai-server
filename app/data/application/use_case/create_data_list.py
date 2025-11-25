from typing import List

from app.data.application.port.data_repository_port import DataRepositoryPort
from app.data.domain.data import Data
from app.data_keyword.application.port.data_keyword_repository_port import (
    DataKeywordRepositoryPort,
)
from app.keywords.application.port.keyword_repository_port import (
    KeywordRepositoryPort,
)


class CreateDataList:
    def __init__(
        self,
        data_repository: DataRepositoryPort,
        keyword_repository: KeywordRepositoryPort,
        data_keyword_repository: DataKeywordRepositoryPort,
    ):
        self.data_repository = data_repository
        self.keyword_repository = keyword_repository
        self.data_keyword_repository = data_keyword_repository

    def execute(
        self,
        items: List[dict],
    ) -> List[Data]:
        """
        여러 데이터를 한 번에 생성
        items: [{"title": str, "content": str, "published_at": datetime, "keywords": List[str]}, ...]
        """
        created_data_list: List[Data] = []

        for item in items:
            # 1. 데이터 저장
            data = Data(
                title=item["title"],
                content=item["content"],
                published_at=item["published_at"],
            )
            saved_data = self.data_repository.save(data)

            # 2. 키워드 처리 및 연결
            keyword_ids: List[int] = []
            for keyword_name in item.get("keywords", []):
                if keyword_name.strip():  # 빈 문자열 제외
                    keyword = self.keyword_repository.get_or_create(
                        keyword_name.strip()
                    )
                    keyword_ids.append(keyword.id)

            # 3. 데이터-키워드 연결
            if keyword_ids:
                self.data_keyword_repository.attach_keywords(
                    saved_data.id, keyword_ids
                )

            created_data_list.append(saved_data)

        return created_data_list

