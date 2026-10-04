from backend.config import Settings


def test_settings_reads_database_url_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")

    settings = Settings()

    assert settings.database_url == "postgresql+asyncpg://test:test@localhost/test"
