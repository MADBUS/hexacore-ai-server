from typing import Optional


class DataKeyword:
    """
    데이터와 키워드를 연결하는 도메인 객체
    """

    def __init__(self, data_id: int, keyword_id: int):
        self.id: Optional[int] = None
        self.data_id = data_id
        self.keyword_id = keyword_id