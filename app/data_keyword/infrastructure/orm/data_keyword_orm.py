from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from config.database.session import Base


class DataKeywordORM(Base):
    __tablename__ = "data_keywords"
    __table_args__ = (
        UniqueConstraint("data_id", "keyword_id", name="uq_data_keyword_pair"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_id = Column(Integer, ForeignKey("datas.id", ondelete="CASCADE"), nullable=False)
    keyword_id = Column(Integer, ForeignKey("keywords.id", ondelete="CASCADE"), nullable=False)

    data = relationship("DataORM", back_populates="keyword_links")
    keyword = relationship("KeywordORM", back_populates="data_links")

