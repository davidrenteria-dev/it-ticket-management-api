import pytest
import database

@pytest.fixture
def test_database(tmp_path, monkeypatch):
    test_db = tmp_path / "test_tickets.db"
    monkeypatch.setattr(database, "TICKETS_DATABASE", str(test_db))
    database.initialize_database()