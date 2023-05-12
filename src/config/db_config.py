from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import NullPool


load_dotenv()


@staticmethod
def get_db_con_uri() -> str:

    user: str = getenv('POSTGRES_USER')
    password: str = getenv('POSTGRES_PASSWORD')
    host: str = getenv('POSTGRES_HOST')
    port: str = getenv('POSTGRES_PORT')
    database: str = getenv('POSTGRES_DB')

    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'


@staticmethod
def create_default_db_engine(database_uri: str | None = None) -> Engine:

    return create_engine(database_uri, client_encoding='utf8', poolclass=NullPool)
