from typing import List

from sqlalchemy.orm import Session

from app.data_keyword.application.port.data_keyword_repository_port import (
    DataKeywordRepositoryPort,
)
from app.data_keyword.infrastructure.orm.data_keyword_orm import DataKeywordORM


class DataKeywordRepositoryImpl(DataKeywordRepositoryPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def attach_keywords(self, data_id: int, keyword_ids: List[int]) -> None:
        for keyword_id in keyword_ids:
            # 중복 체크 (UniqueConstraint가 있지만 안전하게)
            existing = (
                self.db.query(DataKeywordORM)
                .filter(
                    DataKeywordORM.data_id == data_id,
                    DataKeywordORM.keyword_id == keyword_id,
                )
                .first()
            )
            if existing is None:
                link = DataKeywordORM(data_id=data_id, keyword_id=keyword_id)
                self.db.add(link)

    def get_keyword_ids(self, data_id: int) -> List[int]:
        links = (
            self.db.query(DataKeywordORM)
            .filter(DataKeywordORM.data_id == data_id)
            .all()
        )
        return [link.keyword_id for link in links]

