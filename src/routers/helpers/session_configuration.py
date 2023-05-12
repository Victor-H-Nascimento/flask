from sqlalchemy.orm import sessionmaker, Session

from src.config import create_default_db_engine


def configure_session() -> Session:
    engine = create_default_db_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    session.begin()

    return session
