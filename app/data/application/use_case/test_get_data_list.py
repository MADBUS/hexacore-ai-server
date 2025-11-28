import pytest
from unittest.mock import Mock

from app.data.application.use_case.get_data_list import GetDataList
from app.data.application.port.data_repository_port import DataRepositoryPort
from app.data.domain.data import Data


class TestGetDataList:
    @pytest.fixture
    def mock_repository(self):
        return Mock(spec=DataRepositoryPort)

    @pytest.fixture
    def use_case(self, mock_repository):
        return GetDataList(data_repository=mock_repository)

    def test_get_data_list_returns_recent_data(self, use_case, mock_repository):
        """최근 데이터 반환"""
        expected_data = [
            Data(title="제목1", content="내용1", published_at="2024-01-01"),
            Data(title="제목2", content="내용2", published_at="2024-01-02")
        ]
        mock_repository.get_recent.return_value = expected_data

        result = use_case.execute(limit=10)

        assert result == expected_data
        mock_repository.get_recent.assert_called_once()

    def test_get_data_list_respects_limit(self, use_case, mock_repository):
        """limit 파라미터 적용"""
        mock_repository.get_recent.return_value = []

        use_case.execute(limit=5)

        mock_repository.get_recent.assert_called_once_with(5)