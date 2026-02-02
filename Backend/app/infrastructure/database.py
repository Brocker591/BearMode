from collections.abc import AsyncGenerator # Import AsyncGenerator für Typ-Hinting von asynchronen Generatoren

# Importe aus SQLAlchemy für asynchrone Datenbankverbindungen
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base # Import für ORM-Basis-Klasse zur Definition von Datenbankmodellen
from app.config import settings # Import der Konfiguration aus der Config-Datei (enthält Datenbank-URL)

# Erstellt die Basis-Klasse, von der alle ORM-Modelle erben werden
Base = declarative_base()

# Erstellt die asynchrone Datenbank-Engine mit folgenden Konfigurationen:
engine = create_async_engine(
    settings.database_url,  # Datenbank-URL aus den Einstellungen
    echo=False,  # SQL-Statements werden nicht in der Konsole ausgegeben
    pool_pre_ping=True,  # Testet Verbindung vor Nutzung (verhindert Connection Timeout)
)

# Erstellt eine Factory für asynchrone Datenbank-Sessions mit Konfigurationen:
async_session_factory = async_sessionmaker(
    engine,  # Verwendet die oben erstellte Engine
    class_=AsyncSession,  # Nutzt SQLAlchemy's asynchrone Session-Klasse
    expire_on_commit=False,  # Objekte werden nach Commit nicht automatisch neu abgefragt
    autocommit=False,  # Transaktionen müssen manuell committed werden
    autoflush=False,  # Änderungen werden nicht automatisch vor Queries geflusht
)


# Asynchrone Generatoren-Funktion, die eine Datenbank-Session bereitstellt
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    # Erstellt einen neuen Session-Kontext mit der Factory
    async with async_session_factory() as session:
        try:
            # Gibt die Session an den Aufrufer zurück (für Dependency Injection nutzbar)
            yield session
            # Nach erfolgreicher Nutzung: Committed alle Änderungen
            await session.commit()
        except Exception:
            # Bei Fehler: Rollback aller Änderungen
            await session.rollback()
            # Wirft den Fehler weiter nach oben
            raise
        finally:
            # Schliesst die Session in jedem Fall (auch bei Fehlern)
            await session.close()
