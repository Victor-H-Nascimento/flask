from contextlib import closing
from flask_restx import Resource
from http import HTTPStatus
from loguru import logger
from sqlalchemy.orm import Session

from src import populate_namespace as app
from src.models import Clinica, Pet, Services, User, Vet
from src.routers.helpers import get_response, configure_session


@app.route('')
class RoutePopulate(Resource):
    def post(self):
        with closing(configure_session()) as session:
            try:
                create_user(session)
                create_pets(session)
                create_clinica(session)
                create_vets(session)
                create_services(session)
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


def create_clinica(session: Session):
    
    clinica: Clinica = session.query(Clinica).filter(Clinica.activated).filter(Clinica.cnpj == '52.181.712/0001-58').first()

    if not clinica:

        clinica = {
            'name': 'Animale Pet Care',
            'cnpj': '52.181.712/0001-58',
            'address': 'Rua Cônego Manoel Garcia',
            'number': '167',
            'zip_code': '13070-036',
            'neighborhood': 'Jardim Novo Chapadão',
            'username': 'Animale',
            'pwd': 'Animale1234',
        }

        session.add(Clinica(clinica['name'], clinica['cnpj'], clinica['address'], clinica['number'], clinica['zip_code'],
                          clinica['neighborhood'], clinica['username'], clinica['pwd']))
        session.commit()


def create_vets(session: Session):
    
    clinica_id = session.query(Clinica.id).filter(Clinica.activated).filter(Clinica.cnpj == '52.181.712/0001-58').scalar()

    vet: Vet = session.query(Vet).filter(Vet.activated).all()

    if not vet:
        vets = [
            {
                'name': 'Dra. Thais Cruz',
                'username': 'thais.cruz',
                'pwd': 'Animale123',
                'clinica_id': clinica_id,
                
            },
            {
                'name': 'Dr. João Flávio',
                'username': 'joao.flavio',
                'pwd': 'Animale123',
                'clinica_id': clinica_id,
            },
        ]
        
        for vet in vets:
            session.add(Vet(vet['name'], vet['username'], vet['pwd'], vet['clinica_id']))
        session.commit()


def create_services(session: Session):
    
        services = [
            {
                'name': 'Banho e Tosa',
            },
            {
                'name': 'Vacinas',
            },
            {
                'name': 'Consultas',
            },
            {
                'name': 'Raio-X',
            },
            {
                'name': 'Ultrassom',
            },
        ]
        
        for service in services:
            name = service['name']
            serv: Services = session.query(Services).filter(Services.activated).filter(Services.name == name).first()
            if not serv:
                session.add(Services(name))
                session.commit()