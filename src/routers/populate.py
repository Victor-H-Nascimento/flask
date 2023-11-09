
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
                # create_timeline(session)
            except Exception as e:
                msg = f'Unable to populate database. Rollback executed: {str(e)}'
                session.rollback()
                logger.exception(msg)
                return get_response(HTTPStatus.BAD_REQUEST, msg)

            msg = 'Database auto populate successfully'
            logger.info(msg)
            return msg, HTTPStatus.CREATED


def create_user(session: Session):

    users = [
        {
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
        },
        {
            'email': 'nascimento.victor01@gmail.com',
            'name': 'Victor Nascimento',
            'document': '111111111',
            'phone_number': '222222222',
            'pwd': 'tcc2023',
            'address': 'Rua José Lourenço de Sá',
            'number': '1108',
            'zip_code': '13060-740',
            'neighborhood': 'Vila União',
            'username': 'victor.nascimento',
        },
        {
            'email': 'tainarenata@gmail.com',
            'name': 'Tainá Renata',
            'document': '333333333',
            'phone_number': '444444444',
            'pwd': 'tcc2023',
            'address': 'Rua dos Guaiases',
            'number': '281',
            'zip_code': '13041-307',
            'neighborhood': 'Vila João Jorge',
            'username': 'taina.renata',
        },
        {
            'email': 'marcellaamorim@gmail.com',
            'name': 'Marcella Amorim',
            'document': '555555555',
            'phone_number': '666666666',
            'pwd': 'tcc2023',
            'address': 'Rua Gelsumino Lizardi',
            'number': '10',
            'zip_code': '13052-570',
            'neighborhood': 'Jardim San Diego',
            'username': 'marcella.amorim',
        },
    ]

    for user in users:
        session.add(User(user['email'], user['name'], user['document'],
                    user['phone_number'], user['pwd'], user['address'], user['number'],
                    user['zip_code'], user['neighborhood'], user['username']))
    session.commit()


def create_pets(session: Session):
    
    victor_id = session.query(User.id).filter(User.activated).filter(User.email == 'nascimento.victor01@gmail.com').scalar()
    marcella_id = session.query(User.id).filter(User.activated).filter(User.email == 'marcellaamorim@gmail.com').scalar()
    taina_id = session.query(User.id).filter(User.activated).filter(User.email == 'tainarenata@gmail.com').scalar()

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
            'description': 'Uma cachorra que não gosta de amizades com pessoas, mas que gosta de cachorro',
            'user_id': victor_id,
        },
        {
            'name': 'Luke',
            'size': 'medio',
            'breed': 'SRD',
            'age': '12 anos',
            'castrated': True,
            'weight': 20,
            'specie': 'cachorro',
            'gender': 'macho',
            'description': 'Um cachorro docil com pessoas e bravo com cachorros',
            'user_id': victor_id,
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
            'description': 'Um laranjinha muito dócil',
            'user_id': taina_id,
        },
        {
            'name': 'Jobbi',
            'size': 'grande',
            'breed': 'SRD',
            'age': '13 anos',
            'castrated': True,
            'weight': 28,
            'specie': 'cachorro',
            'gender': 'macho',
            'description': 'Um senhorzinho que ama todos',
            'user_id': taina_id,
        },
        {
            'name': 'Diana',
            'size': 'medio',
            'breed': 'SRD',
            'age': '7 anos',
            'castrated': True,
            'weight': 8,
            'specie': 'cachorro',
            'gender': 'femea',
            'description': 'Uma cachorra muito sapeca que adora pular',
            'user_id': marcella_id,
        },
        {
            'name': 'Zoe',
            'size': 'pequeno',
            'breed': 'SRD',
            'age': '6 anos',
            'castrated': True,
            'weight': 5,
            'specie': 'cachorro',
            'gender': 'femea',
            'description': 'Uma cachorra adorável e que não late',
            'user_id': marcella_id,
        },
        {
            'name': 'Luna',
            'size': 'pequeno',
            'breed': 'SRD',
            'age': '2 anos',
            'castrated': True,
            'weight': 1,
            'specie': 'cachorro',
            'gender': 'femea',
            'description': 'Uma pequenina que se acha gigante',
            'user_id': marcella_id,
        },
    ]
    
    for pet in pets:
        session.add(Pet(pet['name'], pet['size'], pet['breed'], pet['age'],
                        pet['castrated'], pet['weight'], pet['specie'],
                        pet['gender'], pet['user_id'], pet['description']))
    session.commit()


def create_clinic(session: Session):

    clinicas = [
        {
            'name': 'Animale Pet Care',
            'cnpj': '11.111.111/0001-11',
            'address': 'Rua Cônego Manoel Garcia',
            'number': '167',
            'zip_code': '13070-036',
            'neighborhood': 'Jardim Novo Chapadão',
            'username': 'animale',
            'pwd': 'tcc2023',
        },
        {
            'name': 'Hospital Clínica Animal',
            'cnpj': '22.222.222/0001-22',
            'address': 'Rua Martinópolis',
            'number': '286',
            'zip_code': '13050-471',
            'neighborhood': 'Vila Pompéia',
            'username': 'clinica.animal',
            'pwd': 'tcc2023',
        },
        {
            'name': 'Hospital Veterinário Dr Eicke Bucholtz',
            'cnpj': '33.333.333/0001-33',
            'address': 'Rua Manoel Francisco Mendes',
            'number': '795',
            'zip_code': '13030-110',
            'neighborhood': 'São Bernardo',
            'username': 'eicke',
            'pwd': 'tcc2023',
        },
        {
            'name': 'Oh my DOG Saúde Animal',
            'cnpj': '44.444.444/0001-44',
            'address': 'Rua Francisco Otaviano',
            'number': '592',
            'zip_code': '13070-056',
            'neighborhood': 'Jardim Chapadão',
            'username': 'omg',
            'pwd': 'tcc2023',
        },
        {
            'name': 'Savet Clínica Veterinária e Estética Animal',
            'cnpj': '55.555.555/0001-55',
            'address': 'Av. Adão Focesi',
            'number': '250',
            'zip_code': '13050-000',
            'neighborhood': 'Jardim do Lago',
            'username': 'savet',
            'pwd': 'tcc2023',
        },
    ]

    
    for clinica in clinicas:
        session.add(Clinica(clinica['name'], clinica['cnpj'], clinica['address'], clinica['number'], clinica['zip_code'],
                          clinica['neighborhood'], clinica['username'], clinica['pwd']))
    session.commit()


def create_vets(session: Session):
    
    animale_id = session.query(Clinica.id).filter(Clinica.activated).filter(Clinica.name == 'Animale Pet Care').scalar()
    clinica_animal_id = session.query(Clinica.id).filter(Clinica.activated).filter(Clinica.name == 'Hospital Clínica Animal').scalar()
    eicke_id = session.query(Clinica.id).filter(Clinica.activated).filter(Clinica.name == 'Hospital Veterinário Dr Eicke Bucholtz').scalar()
    omg_id = session.query(Clinica.id).filter(Clinica.activated).filter(Clinica.name == 'Oh my DOG Saúde Animal').scalar()
    savet_id = session.query(Clinica.id).filter(Clinica.activated).filter(Clinica.name == 'Savet Clínica Veterinária e Estética Animal').scalar()

    vet: Vet = session.query(Vet).filter(Vet.activated).all()

    if not vet:
        vets = [
            {
                'name': 'Dra. Thais Cruz',
                'username': 'thais.cruz',
                'pwd': 'tcc2023',
                'clinica_id': animale_id,
                
            },
            {
                'name': 'Dr. João Flávio',
                'username': 'joao.flavio',
                'pwd': 'tcc2023',
                'clinica_id': animale_id,
            },
            {
                'name': 'Dra. Cristiane Torres',
                'username': 'cris.torres',
                'pwd': 'tcc2023',
                'clinica_id': clinica_animal_id,
            },
            {
                'name': 'Dra. Thalita Alves',
                'username': 'thalita.alves',
                'pwd': 'tcc2023',
                'clinica_id': eicke_id,
            },
            {
                'name': 'Dra. Mallize Oliveira',
                'username': 'mallize.oliveira',
                'pwd': 'tcc2023',
                'clinica_id': omg_id,
            },
            {
                'name': 'Dra. Sabrina Abreu',
                'username': 'sabrina.abreu',
                'pwd': 'tcc2023',
                'clinica_id': savet_id,
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
        {
            'name': 'Internação',
        },
    ]
    
    for service in services:
        name = service['name']
        serv: Services = session.query(Services).filter(Services.activated).filter(Services.name == name).first()
        if not serv:
            session.add(Services(name))
            session.commit()


def connect_services_clinics(session: Session):
    
    clinicas: Clinica = session.query(Clinica).filter(Clinica.activated).all()
    services: Services = session.query(Services).filter(Services.activated).all()

    for clinica in clinicas:
        for service in services:
            clinica.services.append(service)
        session.commit()


def connect_services_pets(session: Session):

    animale_id = session.query(Clinica).filter(Clinica.activated).filter(Clinica.name == 'Animale Pet Care').first()
    clinica_animal_id = session.query(Clinica).filter(Clinica.activated).filter(Clinica.name == 'Hospital Clínica Animal').first()
    eicke_id = session.query(Clinica).filter(Clinica.activated).filter(Clinica.name == 'Hospital Veterinário Dr Eicke Bucholtz').first()
    omg_id = session.query(Clinica).filter(Clinica.activated).filter(Clinica.name == 'Oh my DOG Saúde Animal').first()
    savet_id = session.query(Clinica).filter(Clinica.activated).filter(Clinica.name == 'Savet Clínica Veterinária e Estética Animal').first()

    victor_id = session.query(User.id).filter(User.activated).filter(User.email == 'nascimento.victor01@gmail.com').scalar()
    marcella_id = session.query(User.id).filter(User.activated).filter(User.email == 'marcellaamorim@gmail.com').scalar()
    taina_id = session.query(User.id).filter(User.activated).filter(User.email == 'tainarenata@gmail.com').scalar()
    
    victor_pets: Pet = session.query(Pet).filter(Pet.activated).filter(Pet.user_id == victor_id).all()
    taina_pets: Pet = session.query(Pet).filter(Pet.activated).filter(Pet.user_id == taina_id).all()
    marcella_pets: Pet = session.query(Pet).filter(Pet.activated).filter(Pet.user_id == marcella_id).all()

    for pet in victor_pets:
        animale_id.pets.append(pet)
    session.commit()
    
    for pet in taina_pets:
        pet: Pet
        if pet.name == 'Jobbi':
            savet_id.pets.append(pet)
        else:
            omg_id.pets.append(pet)
    session.commit()

    for pet in marcella_pets:
        pet: Pet
        if pet.name == 'Diana':
            clinica_animal_id.pets.append(pet)
        else:
            eicke_id.pets.append(pet)
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
