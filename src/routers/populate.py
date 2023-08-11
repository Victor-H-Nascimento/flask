from contextlib import closing
from flask_restx import Resource
from http import HTTPStatus
from loguru import logger
from sqlalchemy.orm import Session

from src import populate_namespace as app
from src.models import User
from src.routers.helpers import get_response, configure_session


@app.route('')
class RoutePopulate(Resource):
    def post(self):
        with closing(configure_session()) as session:
            try:
                create_user(session)
            except Exception as e:
                msg = f'Unable to populate database. Rollback executed: {str(e)}'
                session.rollback()
                logger.exception(msg)
                return get_response(HTTPStatus.BAD_REQUEST, msg)

            msg = 'Database auto populate successfully'
            logger.info(msg)
            return msg, HTTPStatus.CREATED


def create_user(session: Session):
    email = 'admin@admin.com'
    name = 'admin'
    lastname = 'admin'
    document = '123456789'
    phone_number = '123456789'
    pwd = 'admin'

    user: User = session.query(User).filter(User.activated).filter(User.email == email).first()

    if not user:
        session.add(User(email, name, lastname, document, phone_number, pwd))
        session.commit()
