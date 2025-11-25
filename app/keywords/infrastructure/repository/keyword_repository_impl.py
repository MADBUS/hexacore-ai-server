from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.keywords.application.port.keyword_repository_port import KeywordRepositoryPort
from app.keywords.domain.keyword import Keyword, KeywordMention
from app.keywords.infrastructure.orm.keyword_orm import KeywordORM
from app.data_keyword.infrastructure.orm.data_keyword_orm import DataKeywordORM


class KeywordRepositoryImpl(KeywordRepositoryPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_top_mentions(self, limit: int) -> List[KeywordMention]:
        rows = (
            self.db.query(
                KeywordORM.id.label("keyword_id"),
                KeywordORM.name,
                func.count(DataKeywordORM.data_id).label("mention_count"),
            )
            .join(
                DataKeywordORM,
                KeywordORM.id == DataKeywordORM.keyword_id,
            )
            .group_by(KeywordORM.id)
            .order_by(func.count(DataKeywordORM.data_id).desc())
            .limit(limit)
            .all()
        )

        return [
            KeywordMention(
                keyword_id=row.keyword_id,
                name=row.name,
                mention_count=row.mention_count,
            )
            for row in rows
        ]

    def get_or_create(self, name: str) -> Keyword:
        orm_keyword = (
            self.db.query(KeywordORM).filter(KeywordORM.name == name).first()
        )
        if orm_keyword is None:
            orm_keyword = KeywordORM(name=name)
            self.db.add(orm_keyword)
            self.db.flush()  # ID를 얻기 위해 flush

        keyword = Keyword(name=orm_keyword.name)
        keyword.id = orm_keyword.id
        return keyword

    def find_by_id(self, keyword_id: int) -> Keyword:
        orm_keyword = (
            self.db.query(KeywordORM).filter(KeywordORM.id == keyword_id).first()
        )
        if orm_keyword is None:
            raise ValueError(f"Keyword with id {keyword_id} not found")

        keyword = Keyword(name=orm_keyword.name)
        keyword.id = orm_keyword.id
        return keyword

