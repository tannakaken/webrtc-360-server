from typing import Callable, Iterator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.config import get_settings

settings = get_settings()

engine = create_engine(settings.sqlalchemy_database_url,
                       pool_recycle=600,
                       connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db_with(
        session_local: Callable[[],
                                Session]) -> Callable[[], Iterator[Session]]:

    def _get_db() -> Iterator[Session]:
        db = session_local()
        try:
            yield db
        finally:
            db.close()

    _get_db.__name__ = "get_db"
    return _get_db


get_db = get_db_with(SessionLocal)
