from app.keywords.domain.keyword import Keyword, KeywordMention


class TestKeyword:
    def test_keyword_init(self):
        """Keyword 객체가 name으로 생성됨"""
        keyword = Keyword(name="삼성전자")

        assert keyword.name == "삼성전자"

    def test_keyword_id_defaults_to_none(self):
        """Keyword id 기본값이 None"""
        keyword = Keyword(name="삼성전자")

        assert keyword.id is None


class TestKeywordMention:
    def test_keyword_mention_init(self):
        """KeywordMention이 keyword_id, name, mention_count로 생성됨"""
        mention = KeywordMention(
            keyword_id=1,
            name="삼성전자",
            mention_count=100
        )

        assert mention.id == 1
        assert mention.name == "삼성전자"
        assert mention.mention_count == 100
