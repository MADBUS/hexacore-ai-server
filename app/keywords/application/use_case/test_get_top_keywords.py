import pytest
from unittest.mock import Mock

from app.keywords.application.use_case.get_top_keywords import GetTopKeywords
from app.keywords.application.port.keyword_repository_port import KeywordRepositoryPort
from app.keywords.domain.keyword import KeywordMention


class TestGetTopKeywords:
    @pytest.fixture
    def mock_repository(self):
        return Mock(spec=KeywordRepositoryPort)

    @pytest.fixture
    def use_case(self, mock_repository):
        return GetTopKeywords(keyword_repository=mock_repository)

    def test_get_top_keywords_returns_mentions(self, use_case, mock_repository):
        """상위 키워드 반환"""
        expected_mentions = [
            KeywordMention(keyword_id=1, name="삼성전자", mention_count=100),
            KeywordMention(keyword_id=2, name="SK하이닉스", mention_count=50)
        ]
        mock_repository.get_top_mentions.return_value = expected_mentions

        result = use_case.execute(limit=10)

        assert result == expected_mentions
        mock_repository.get_top_mentions.assert_called_once()

    def test_get_top_keywords_respects_limit(self, use_case, mock_repository):
        """limit 파라미터 적용"""
        mock_repository.get_top_mentions.return_value = []

        use_case.execute(limit=5)

        mock_repository.get_top_mentions.assert_called_once_with(5)