from app.keywords.application.port.keyword_repository_port import KeywordRepositoryPort


class TestKeywordRepositoryPort:
    def test_keyword_repository_port_has_get_top_mentions_method(self):
        """get_top_mentions 메서드 존재"""
        assert hasattr(KeywordRepositoryPort, 'get_top_mentions')
        assert callable(getattr(KeywordRepositoryPort, 'get_top_mentions'))