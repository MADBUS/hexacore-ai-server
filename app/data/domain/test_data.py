from app.data.domain.data import Data


class TestData:
    def test_data_init_with_required_fields(self):
        """Data 객체가 필수 필드(title, content, published_at)로 생성됨"""
        data = Data(
            title="테스트 제목",
            content="테스트 내용",
            published_at="2024-01-01"
        )

        assert data.title == "테스트 제목"
        assert data.content == "테스트 내용"
        assert data.published_at == "2024-01-01"

    def test_data_init_with_keywords(self):
        """Data 객체가 keywords와 함께 생성됨"""
        data = Data(
            title="테스트 제목",
            content="테스트 내용",
            published_at="2024-01-01",
            keywords=["삼성전자", "반도체"]
        )

        assert data.keywords == ["삼성전자", "반도체"]

    def test_data_init_without_keywords_defaults_to_empty_list(self):
        """keywords 없이 생성 시 빈 리스트"""
        data = Data(
            title="테스트 제목",
            content="테스트 내용",
            published_at="2024-01-01"
        )

        assert data.keywords == []

    def test_data_add_keyword(self):
        """add_keyword 메서드가 키워드를 추가함"""
        data = Data(
            title="테스트 제목",
            content="테스트 내용",
            published_at="2024-01-01"
        )

        data.add_keyword("삼성전자")

        assert "삼성전자" in data.keywords

    def test_data_id_defaults_to_none(self):
        """id 기본값이 None"""
        data = Data(
            title="테스트 제목",
            content="테스트 내용",
            published_at="2024-01-01"
        )

        assert data.id is None