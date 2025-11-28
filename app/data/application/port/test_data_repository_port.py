import inspect
from app.data.application.port.data_repository_port import DataRepositoryPort


class TestDataRepositoryPort:
    def test_data_repository_port_has_save_method(self):
        """save 메서드 존재"""
        assert hasattr(DataRepositoryPort, 'save')
        assert callable(getattr(DataRepositoryPort, 'save'))

    def test_data_repository_port_has_get_recent_method(self):
        """get_recent 메서드 존재"""
        assert hasattr(DataRepositoryPort, 'get_recent')
        assert callable(getattr(DataRepositoryPort, 'get_recent'))