import os
from abc import ABC
from dotenv import load_dotenv
from flask import jsonify, make_response, Response
from http import HTTPStatus
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import NullPool
from sshtunnel import SSHTunnelForwarder

from src.helpers import EnvVarsTranslater

load_dotenv()


class Db_config(ABC):
    SSH_TUNNEL: SSHTunnelForwarder | None = None

    # TODO: Improve this connection in order to handle SSH Tunnel Timeout
    # TODO: For example: A simple thread that check and refreshea ssh tunnel connection
    @staticmethod
    def create_ssh_tunnel():
        try:
            if not os.getenv('SSH_TUNNEL_DB_ADDRESS'):
                return None

            ssh_tunnel: SSHTunnelForwarder | None = Db_config.SSH_TUNNEL
            if ssh_tunnel and ssh_tunnel.is_active:
                return ssh_tunnel

            ssh_tunnel = SSHTunnelForwarder(
                (os.getenv('SSH_TUNNEL_DB_ADDRESS'), 22),
                ssh_username=os.getenv('SSH_TUNNEL_DB_USER'),
                ssh_private_key=os.getenv('SSH_TUNNEL_DB_PRIVATE_KEY_PATH'),
                remote_bind_address=(os.getenv('POSTGRES_HOST'),
                                     EnvVarsTranslater.get_int('POSTGRES_PORT'))
            )

            ssh_tunnel.start()
            Db_config.SSH_TUNNEL = ssh_tunnel
            return ssh_tunnel
        except Exception as e:
            msg = f'Error creating SSH tunnel: {str(e)}'
            logger.exception(msg)
            return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)

    @staticmethod
    def get_db_con_uri():
        try:
            ssh_tunnel: SSHTunnelForwarder | None = Db_config.create_ssh_tunnel()

            user: str = os.getenv('POSTGRES_USER')
            password: str = os.getenv('POSTGRES_PASSWORD')
            host: str = os.getenv('POSTGRES_HOST')
            port: str = os.getenv('POSTGRES_PORT')
            database: str = os.getenv('POSTGRES_DB')

            if ssh_tunnel:
                host = 'localhost'
                port = ssh_tunnel.local_bind_port

            return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
        except Exception as e:
            msg = f'Error retrieving database connection URI: {str(e)}'
            logger.exception(msg)
            return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)

    @staticmethod
    def create_default_db_engine(database_uri: str | None = None):
        try:
            if not database_uri:
                database_uri = Db_config.get_db_con_uri()
            return create_engine(database_uri, client_encoding='utf8', poolclass=NullPool)
        except SQLAlchemyError as e:
            msg = f'Error creating database engine: {str(e)}'
            logger.exception(msg)
            return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)

# TODO: Refactor - replace this method because it already exists but throw a dependency cicle


def get_response(status_code: int, content: str | dict | list = None) -> Response:
    if isinstance(content, str):
        logger.info(content)
        content = {"message": content}
    return make_response(jsonify(content), status_code)
