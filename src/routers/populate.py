from contextlib import closing
from flask_restx import Resource
from http import HTTPStatus
from loguru import logger
from sqlalchemy.orm import Session

from src import populate_namespace as app
from src.models import Pet, User
from src.routers.helpers import get_response, configure_session


@app.route('')
class RoutePopulate(Resource):
    def post(self):
        with closing(configure_session()) as session:
            try:
                create_user(session)
                create_pets(session)
            except Exception as e:
                msg = f'Unable to populate database. Rollback executed: {str(e)}'
                session.rollback()
                logger.exception(msg)
                return get_response(HTTPStatus.BAD_REQUEST, msg)

            msg = 'Database auto populate successfully'
            logger.info(msg)
            return msg, HTTPStatus.CREATED


def create_user(session: Session):
    
    user: User = session.query(User).filter(User.activated).filter(User.email == 'admin@admin.com').first()

    if not user:

        user = {
            'email': 'admin@admin.com',
            'name': 'admin',
            'lastname': 'admin',
            'document': '123456789',
            'phone_number': '123456789',
            'pwd': 'admin',
            'address': 'Rua João Manuel da Silva',
            'number': '1234',
            'zip_code': '13046-240',
            'neighborhood': 'Parque dos Cisnes',
        }

        session.add(User(user['email'], user['name'], user['lastname'], user['document'], user['phone_number'],
                          user['pwd'], user['address'], user['number'], user['zip_code'], user['neighborhood']))
        session.commit()


def create_pets(session: Session):
    
    user_id = session.query(User.id).filter(User.activated).filter(User.email == 'admin@admin.com').scalar()

    pet: Pet = session.query(Pet).filter(Pet.activated).all()

    if not pet:
        pets = [
            {
                'name': 'Lily',
                'size': 'medio',
                'breed': 'SRD',
                'age': '3 anos',
                'castrated': True,
                'weight': 30,
                'specie': 'cachorro',
                'gender': 'femea',
                'user_id': user_id,
            },
            {
                'name': 'Nick',
                'size': 'pequeno',
                'breed': 'SRD',
                'age': '5 anos',
                'castrated': False,
                'weight': 3.5,
                'specie': 'gato',
                'gender': 'macho',
                'user_id': user_id,
            },
        ]
        
        for pet in pets:
            session.add(Pet(pet['name'], pet['size'], pet['breed'], pet['age'], pet['castrated'], pet['weight'], pet['specie'], pet['gender'], pet['user_id']))
        session.commit()
