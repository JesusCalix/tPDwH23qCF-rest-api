from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# this should be set in an env var, but for this use case I have decided to keep it here
DATABASE_URL = "sqlite:///./WeatherData.db"

engine = create_engine(DATABASE_URL)


# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """
    Yields a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
