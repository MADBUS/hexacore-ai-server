from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from config.database.session import Base


class DataORM(Base):
    __tablename__ = "datas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    published_at = Column(DateTime, nullable=False)

    keyword_links = relationship(
        "DataKeywordORM",
        back_populates="data",
        cascade="all, delete-orphan",
    )

