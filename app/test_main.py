import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """DB 연결 없이 테스트하기 위해 lifespan을 모킹"""
    with patch('app.main.engine') as mock_engine:
        with patch('app.main.Base') as mock_base:
            mock_engine.dispose = MagicMock()
            from app.main import app
            with TestClient(app) as c:
                yield c


class TestHealthEndpoint:
    def test_health_endpoint_returns_ok(self, client):
        """/health 엔드포인트 정상 응답"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestDataEndpoint:
    def test_get_data_endpoint(self, client):
        """GET /data 엔드포인트"""
        with patch('app.data.adapter.input.web.data_router.get_db') as mock_get_db:
            with patch('app.data.adapter.input.web.data_router.DataRepositoryImpl') as mock_repo:
                with patch('app.data.adapter.input.web.data_router.KeywordRepositoryImpl'):
                    mock_repo.return_value.get_recent.return_value = []
                    mock_get_db.return_value = MagicMock()

                    response = client.get("/data/")

                    assert response.status_code == 200
                    assert isinstance(response.json(), list)


class TestKeywordsEndpoint:
    def test_get_keywords_endpoint(self, client):
        """GET /keywords 엔드포인트"""
        with patch('app.keywords.adapter.input.web.keyword_router.get_db') as mock_get_db:
            with patch('app.keywords.adapter.input.web.keyword_router.KeywordRepositoryImpl') as mock_repo:
                mock_repo.return_value.get_all.return_value = []
                mock_get_db.return_value = MagicMock()

                response = client.get("/keywords/")

                assert response.status_code == 200
                assert isinstance(response.json(), list)