from abc import ABC, abstractmethod
from typing import List


class DataKeywordRepositoryPort(ABC):
    @abstractmethod
    def attach_keywords(self, data_id: int, keyword_ids: List[int]) -> None:
        """
        데이터와 키워드를 다대다로 연결
        """
        raise NotImplementedError

    @abstractmethod
    def get_keyword_ids(self, data_id: int) -> List[int]:
        """
        데이터에 연결된 키워드 ID 조회
        """
        raise NotImplementedError