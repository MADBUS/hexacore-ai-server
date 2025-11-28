import pytest
from unittest.mock import Mock

from app.data.application.use_case.create_data_list import CreateDataList
from app.data.application.port.data_repository_port import DataRepositoryPort
from app.data.domain.data import Data


class TestCreateDataList:
    @pytest.fixture
    def mock_repository(self):
        mock = Mock(spec=DataRepositoryPort)
        mock.save.side_effect = lambda data: data
        return mock

    @pytest.fixture
    def use_case(self, mock_repository):
        return CreateDataList(data_repository=mock_repository)

    def test_create_data_list_with_single_item(self, use_case, mock_repository):
        """단일 항목 생성"""
        items = [
            {"title": "제목1", "content": "내용1", "published_at": "2024-01-01", "keywords": ["키워드1"]}
        ]

        result = use_case.execute(items)

        assert len(result) == 1
        assert result[0].title == "제목1"
        mock_repository.save.assert_called_once()

    def test_create_data_list_with_multiple_items(self, use_case, mock_repository):
        """복수 항목 생성"""
        items = [
            {"title": "제목1", "content": "내용1", "published_at": "2024-01-01", "keywords": []},
            {"title": "제목2", "content": "내용2", "published_at": "2024-01-02", "keywords": []}
        ]

        result = use_case.execute(items)

        assert len(result) == 2
        assert mock_repository.save.call_count == 2

    def test_create_data_list_strips_keyword_whitespace(self, use_case):
        """키워드 공백 제거"""
        items = [
            {"title": "제목", "content": "내용", "published_at": "2024-01-01", "keywords": ["  삼성전자  ", " SK하이닉스 "]}
        ]

        result = use_case.execute(items)

        assert result[0].keywords == ["삼성전자", "SK하이닉스"]

    def test_create_data_list_filters_empty_keywords(self, use_case):
        """빈 키워드 필터링"""
        items = [
            {"title": "제목", "content": "내용", "published_at": "2024-01-01", "keywords": ["삼성전자", "", "  ", None]}
        ]

        result = use_case.execute(items)

        assert result[0].keywords == ["삼성전자"]

    def test_create_data_list_handles_missing_published_at(self, use_case):
        """published_at 없을 때 빈 문자열 처리"""
        items = [
            {"title": "제목", "content": "내용", "keywords": []}
        ]

        result = use_case.execute(items)

        assert result[0].published_at == ""