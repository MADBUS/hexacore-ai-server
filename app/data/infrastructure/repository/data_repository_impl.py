from typing import List

from sqlalchemy.orm import Session, joinedload

from app.data.application.port.data_repository_port import DataRepositoryPort
from app.data.domain.data import Data, DataKeywordSummary
from app.data.infrastructure.orm.data_orm import DataORM
from app.data_keyword.infrastructure.orm.data_keyword_orm import DataKeywordORM


class DataRepositoryImpl(DataRepositoryPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_recent(self, limit: int) -> List[Data]:
        query = (
            self.db.query(DataORM)
            .options(
                joinedload(DataORM.keyword_links).joinedload(DataKeywordORM.keyword)
            )
            .order_by(DataORM.published_at.desc())
            .limit(limit)
        )
        data_rows = query.all()

        results: List[Data] = []
        for row in data_rows:
            keywords = []
            for link in row.keyword_links:
                if link.keyword:
                    keywords.append(
                        DataKeywordSummary(
                            keyword_id=link.keyword.id,
                            name=link.keyword.name,
                        )
                    )

            data = Data(
                title=row.title,
                content=row.content,
                published_at=row.published_at,
                keywords=keywords,
            )
            data.id = row.id
            results.append(data)

        return results

    def save(self, data: Data) -> Data:
        orm_data = DataORM(
            title=data.title,
            content=data.content,
            published_at=data.published_at,
        )
        self.db.add(orm_data)
        self.db.flush()  # ID를 얻기 위해 flush

        data.id = orm_data.id
        return data

