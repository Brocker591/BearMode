# Import der Pydantic-Settings Klasse für Konfigurationsverwaltung
from pydantic_settings import BaseSettings, SettingsConfigDict


# Definiert die Settings-Klasse für die Verwaltung von Anwendungskonfigurationen
class Settings(BaseSettings):
    # Konfiguriert die Einstellungen für diese Settings-Klasse
    model_config = SettingsConfigDict(
        env_file=".env",  # Liest Umgebungsvariablen aus .env Datei
        env_file_encoding="utf-8",  # Zeichenkodierung für die .env Datei
        extra="ignore",  # Ignoriert zusätzliche Umgebungsvariablen, die nicht definiert sind
    )

    # Datenbank-URL für die PostgreSQL-Verbindung mit asyncpg (async-Driver)
    # Format: postgresql+asyncpg://user:password@host:port/database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/bearmode"


# Erstellt eine globale Settings-Instanz, die in der ganzen Anwendung verwendet wird
settings = Settings()
