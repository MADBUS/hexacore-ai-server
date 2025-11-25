from abc import ABC, abstractmethod
from typing import Optional

from app.data.domain.data import Data


class DataRepositoryPort(ABC):

    @abstractmethod
    def save(self, user: Data) -> Data:
        pass

    @abstractmethod
    def find_by_keywords(self, keywords: str) -> Data:
        pass

    @abstractmethod
    def find_by_title(self, title: str) -> Optional[Data]:
        pass

    @abstractmethod
    def find_by_time(self, title: str) -> Optional[Data]:
        pass