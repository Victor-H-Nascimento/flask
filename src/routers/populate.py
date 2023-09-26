
from contextlib import closing
from flask_restx import Resource
from http import HTTPStatus
from loguru import logger
from sqlalchemy.orm import Session

from src import populate_namespace as app
from src.models import Clinica, Pet, Services, User, Timeline, Vet
from src.routers.helpers import get_response, configure_session


@app.route('')
class RoutePopulate(Resource):
    def post(self):
        with closing(configure_session()) as session:
            try:
                create_user(session)
                create_pets(session)
                create_clinic(session)
                create_vets(session)
                create_services(session)
                connect_services_clinics(session)
                connect_services_pets(session)
                create_timeline(session)
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
            'document': '123456789',
            'phone_number': '123456789',
            'pwd': 'admin',
            'address': 'Rua João Manuel da Silva',
            'number': '1234',
            'zip_code': '13046-240',
            'neighborhood': 'Parque dos Cisnes',
            'username': 'admin',
        }

        session.add(User(user['email'], user['name'], user['document'],
                        user['phone_number'], user['pwd'], user['address'], user['number'],
                        user['zip_code'], user['neighborhood'], user['username']))
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
                'description': 'Uma cachorra docil e amiga de todos',
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
                'description': None,
                'user_id': user_id,
            },
        ]
        
        for pet in pets:
            session.add(Pet(pet['name'], pet['size'], pet['breed'], pet['age'],
                            pet['castrated'], pet['weight'], pet['specie'],
                            pet['gender'], pet['user_id'], pet['description']))
        session.commit()


def create_clinic(session: Session):
    
    clinica: Clinica = session.query(Clinica).filter(Clinica.activated).filter(Clinica.cnpj == '52.181.712/0001-58').first()

    if not clinica:

        clinica = {
            'name': 'Animale Pet Care',
            'cnpj': '52.181.712/0001-58',
            'address': 'Rua Cônego Manoel Garcia',
            'number': '167',
            'zip_code': '13070-036',
            'neighborhood': 'Jardim Novo Chapadão',
            'username': 'admin clinica',
            'pwd': 'admin',
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
            {
                'name': 'Dra. Admin Silva',
                'username': 'admin.silva',
                'pwd': 'admin',
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


def connect_services_clinics(session: Session):
    
    clinica: Clinica = session.query(Clinica).filter(Clinica.activated).filter(Clinica.id == 1).first()
    services: Services = session.query(Services).filter(Services.activated).all()

    for service in services:
        clinica.services.append(service)
    session.commit()


def connect_services_pets(session: Session):
    
    clinica: Clinica = session.query(Clinica).filter(Clinica.activated).filter(Clinica.id == 1).first()
    pets: Pet = session.query(Pet).filter(Pet.activated).all()

    for pet in pets:
        clinica.pets.append(pet)
    session.commit()


def create_timeline(session: Session):
    
        timelines = [
            {
                'type': 'Consulta',
                'title': 'Diagnóstico de Giárdia',
                'description': '''Lily foi atendida e aparentava não estar muito mal, tutora relatou que havia aprensentado diarréia
                                no dia anterior. Foi feito teste rápido na presença da tutora para Parvivirose, que teve resultado
                                negativo. Foi indicada a internação da paciente por 24 horas para acompanhamento do quadro e medicação.''',
                'vet': 'Luís Cardoso',
                'clinic': 'Pet&Amor',
                'pet_id': 1,
                'created_by_id': 1,
                'created_by_role': 'user'
            },
            {
                'type': 'Procedimento',
                'title': 'Internação 24h',
                'description': '''Lily ficou internada e fez diversos exames''',
                'vet': 'Luís Cardoso',
                'clinic': 'Pet&Amor',
                'pet_id': 1,
                'created_by_id': 1,
                'created_by_role': 'vet'
            },
            {
                'type': 'Consulta',
                'title': 'Diagnóstico de Giárdia',
                'description': '''Nick foi atendido e aparentava não estar muito mal, tutora relatou que havia aprensentado diarréia
                                no dia anterior. Foi feito teste rápido na presença da tutora para Parvivirose, que teve resultado
                                negativo. Foi indicada a internação da paciente por 24 horas para acompanhamento do quadro e medicação.''',
                'vet': 'Luís Cardoso',
                'clinic': 'Pet&Amor',
                'pet_id': 2,
                'created_by_id': 1,
                'created_by_role': 'clinica'
            },
            {
                'type': 'Procedimento',
                'title': 'Alta',
                'description': '''Lily recebeu alta no dia seguinte''',
                'vet': 'Luís Cardoso',
                'clinic': 'Pet&Amor',
                'pet_id': 1,
                'created_by_id': 2,
                'created_by_role': 'user'
            },
        ]
        
        for timeline in timelines:
            session.add(Timeline(timeline['type'], timeline['title'], timeline['description'],
                                  timeline['vet'], timeline['clinic'], timeline['pet_id'],
                                  timeline['created_by_id'], timeline['created_by_role'],
                                ))
        session.commit()
