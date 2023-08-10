from sqlalchemy.orm import sessionmaker, Session

from src.config import Db_config

def configure_session() -> Session:
    engine = Db_config.create_default_db_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    session.begin()
    return session
