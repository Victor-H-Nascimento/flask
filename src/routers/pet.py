from contextlib import closing
from flask import request
from flask_restx import Resource, fields
from http import HTTPStatus
from loguru import logger
from sqlalchemy import not_

from src import api, pets_namespace as app
from src.models import Clinica, ClinicaSchema, Pet, PetSchema, Timeline, TimelineSchema, User, Vet
from src.models import pets_clinicas
from src.routers.helpers import get_response, configure_session


pet_model_create = api.model('PetCreate', {
    'name': fields.String(required=True, description='Nome do Pet'),
    'size': fields.String(required=True, description='Tamanho do Pet'),
    'breed': fields.String(required=True, description='Raça do Pet'),
    'age': fields.String(required=True, description='Idade do Pet'),
    'castrated': fields.Boolean(required=True, description='Informa se Pet é castrado'),
    'weight': fields.Float(required=True, description='Peso do Pet'),
    'specie': fields.String(required=True, description='Espécie do Pet'),
    'gender': fields.String(required=True, description='Gênero do Pet'),
    'user_id': fields.Integer(required=True, description='Id do Tutor do Pet'),
    'description': fields.String(required=False, description='Breve Descriçao do Pet'),
})


pet_model_update = api.model('PetUpdate', {
    'name': fields.String(required=False, description='Nome do Pet'),
    'size': fields.String(required=False, description='Tamanho do Pet'),
    'breed': fields.String(required=False, description='Raça do Pet'),
    'age': fields.String(required=False, description='Idade do Pet'),
    'castrated': fields.Boolean(required=False, description='Informa se Pet é castrado'),
    'weight': fields.Float(required=False, description='Peso do Pet'),
    'specie': fields.String(required=False, description='Espécie do Pet'),
    'gender': fields.String(required=False, description='Gênero do Pet'),
    'description': fields.String(required=False, description='Breve Descriçao do Pet'),
})


pet_clinica_model = api.model('Pet-Clinica-Connect', {
    'clinica': fields.Integer(description='ID da clinica', required=True),
    'pet': fields.Integer(description='ID do pet', required=True)
})


timeline_item_create = api.model('TimelineCreate', {
    'type': fields.String(required=True, description='Tipo do Item'),
    'title': fields.String(required=True, description='Titulo do Item'),
    'description': fields.String(required=True, description='Descrição do Item'),
    'vet': fields.String(required=True, description='Veterinário do Item'),
    'clinic': fields.String(required=True, description='Clinica do Item'),
    'created_by_id': fields.Integer(required=True, description='Id de quem criou o Item'),
    'created_by_role': fields.String(required=True, description='Role de quem criou o Item'),
})

timeline_item_update = api.model('TimelineUpdate', {
    'type': fields.String(required=False, description='Tipo do Item'),
    'title': fields.String(required=False, description='Titulo do Item'),
    'description': fields.String(required=False, description='Descrição do Item'),
    'vet': fields.String(required=False, description='Veterinário do Item'),
    'clinic': fields.String(required=False, description='Clinica do Item'),
})


@app.route('')
class RoutePet(Resource):
    @app.doc('list_pets')
    def get(self):
        '''Mostra todos os pets'''
        with closing(configure_session()) as session:
            try:
                pets: Pet = session.query(Pet).filter(
                    Pet.activated).order_by(Pet.name).all()
                if not pets:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return PetSchema(many=True).dump(pets)
            except Exception as e:
                session.rollback()
                msg = f'Unable to list all pets. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
            
    @app.doc('create_pet')
    @app.expect(pet_model_create)
    def post(self):
        '''Cria um novo pet'''
        with closing(configure_session()) as session:
            try:
                name: str = request.json.get('name')
                size: str = request.json.get('size')
                breed: str = request.json.get('breed')
                age: str = request.json.get('age')
                castrated: bool = request.json.get('castrated')
                weight: float = request.json.get('weight')
                specie: str = request.json.get('specie')
                gender: str = request.json.get('gender')
                user_id: int = request.json.get('user_id')
                description: str = request.json.get('description')

                if None in (name, size, breed, age, castrated, weight, specie, gender, user_id):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to create pet. Missing at least one mandatory field")

                pet = Pet(name, size, breed, age, castrated, weight, specie, gender, user_id, description)
                session.add(pet)
                session.commit()
                return PetSchema().dump(pet), HTTPStatus.CREATED
            except Exception as e:
                session.rollback()
                msg = f'Unable to create a new pet. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


@app.route('/<int:id>')
class RoutePetWithId(Resource):
    @app.doc('list a single pet')
    def get(self, id: int):
        '''Lista um pet pelo id'''
        with closing(configure_session()) as session:
            try:
                pet: Pet = session.query(Pet).filter(
                    Pet.activated).filter(Pet.id == id).first()
                if not pet:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return PetSchema(many=False).dump(pet)
            except Exception as e:
                session.rollback()
                msg = f'Unable to list all pets. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
    

    @app.doc('update_single_pet_from_an_user')
    @app.expect(pet_model_update)
    def put(self, id: int):
        '''Atualiza os dados de um pet de um usuário'''
        with closing(configure_session()) as session:
            try:
                pet: Pet = session.query(Pet).filter(
                    Pet.activated).filter(Pet.id == id).first()
                if not pet:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                
                name: str = request.json.get('name')
                size: str = request.json.get('size')
                breed: int = request.json.get('breed')
                age: str = request.json.get('age')
                castrated: bool = request.json.get('castrated')
                weight: str = request.json.get('weight')
                specie: str = request.json.get('specie')
                gender: str = request.json.get('gender')
                description: str = request.json.get('description')

                if name:
                    pet.name = name
                if size:
                    pet.size = size
                if breed:
                    pet.breed = breed
                if age:
                    pet.age = age
                if castrated:
                    pet.castrated = castrated
                if weight:
                    pet.weight = weight
                if specie:
                    pet.specie = specie
                if gender:
                    pet.gender = gender
                if description:
                    pet.description = description
                
                session.commit()

                return PetSchema().dump(pet)

            except Exception as e:
                session.rollback()
                msg = f'Unable to list pet with id {id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


    @app.doc('delete_single_pet')
    def delete(self, id: int):
        '''Deleta um pet'''
        with closing(configure_session()) as session:
            try:
                pet: Pet = session.query(Pet).filter(
                    Pet.activated).filter(Pet.id == id).first()
                if not pet:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                pet.activated = False
                session.commit()
                return get_response(HTTPStatus.OK, f"Pet {pet.name} successfully deactivated")
            except Exception as e:
                session.rollback()
                msg = f'Unable to delete pet with id {id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


@app.route('/connect')
class RoutePetConnect(Resource):
    @api.expect(pet_clinica_model, validate=True)
    def post(self):
        '''Conecta um pet à uma clinica'''
        with closing(configure_session()) as session:
            try:

                clinica_id: int = request.json.get('clinica')
                pet_id: int = request.json.get('pet')

                if not (clinica_id and pet_id):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to connect clinica to pet. Missing at least one mandatory field")
                
                clinica: Clinica = session.query(Clinica).filter(Clinica.activated).filter(Clinica.id == clinica_id).first()
                pet: Pet = session.query(Pet).filter(Pet.activated).filter(Pet.id == pet_id).first()

                if not (clinica and pet):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to connect clinica to pet. Not found clinic or pet")

                clinica.pets.append(pet)
                session.commit()

                return get_response(HTTPStatus.OK, f"Pet {pet.name} successfully added to Clinic {clinica.name}")
            except Exception as e:
                session.rollback()
                msg = f'Unable to add connection between clinic and pet. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
    

    @api.expect(pet_clinica_model, validate=True)
    def delete(self):
        '''Deleta conexao entre pet e clinica'''
        with closing(configure_session()) as session:
            try:

                clinica_id: int = request.json.get('clinica')
                pet_id: int = request.json.get('pet')

                if not (clinica_id and pet_id):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to disconnect pet from clinic. Missing at least one mandatory field")
                
                clinica: Clinica = session.query(Clinica).filter(Clinica.activated).filter(Clinica.id == clinica_id).first()
                pet: Pet = session.query(Pet).filter(Pet.activated).filter(Pet.id == pet_id).first()

                if not (clinica and pet):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to disconnect pet from clinic. Not found clinic or pet")

                clinica.pets.remove(pet)
                session.commit()

                return get_response(HTTPStatus.OK, f"Pet {pet.name} successfully removed from Clinic {clinica.name}")
            except Exception as e:
                session.rollback()
                msg = f'Unable to remove connection between clinic and pet. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


@app.route('/<int:id>/clinicas/conectadas')
class RoutePetShowServices(Resource):
    def get(self, id: int):
        '''Mostra todos as clinicas que um pet esteja conectado'''
        with closing(configure_session()) as session:
            try:
                pet: Pet = session.query(Pet).filter(Pet.activated).filter(Pet.id == id).first()
                if not pet:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                
                clinicas: Clinica = session.query(Clinica) \
                .outerjoin(pets_clinicas, pets_clinicas.c.clinicas_id == Clinica.id) \
                .filter(pet.id == pets_clinicas.c.pets_id) \
                .order_by(Clinica.name).all()

                return ClinicaSchema(many=True).dump(clinicas)
            except Exception as e:
                msg = f'Unable to list all clinicas a pet is connected: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
            

@app.route('/<int:id>/clinicas/nao-conectadas')
class RoutePetShowServices(Resource):
    def get(self, id: int):
        '''Mostra todos as clinicas que um pet nao esteja conectado'''
        with closing(configure_session()) as session:
            try:
                pet: Pet = session.query(Pet).filter(Pet.activated).filter(Pet.id == id).first()
                if not pet:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                
                clinicas_tuple: Clinica = session.query(Clinica.id) \
                .outerjoin(pets_clinicas, pets_clinicas.c.clinicas_id == Clinica.id) \
                .filter(pet.id == pets_clinicas.c.pets_id) \
                .order_by(Clinica.name).all()
                
                clinicas_ids = [id[0] for id in clinicas_tuple]

                clinicas: Clinica = session.query(Clinica) \
                .filter(not_(Clinica.id.in_(clinicas_ids))) \
                .order_by(Clinica.name).all()

                return ClinicaSchema(many=True).dump(clinicas)
            except Exception as e:
                msg = f'Unable to list all clinicas a pet is connected: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


@app.route('/<int:id>/timeline')
class RoutePetShowTimeline(Resource):
    @app.doc('list_timeline')
    def get(self, id: int):
        '''Lista timeline'''
        with closing(configure_session()) as session:
            try:
                timeline: Timeline = session.query(Timeline).filter(
                    Timeline.activated).filter(Timeline.pet_id == id).order_by(Timeline.created_date).all()
                if not timeline:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return TimelineSchema(many=True).dump(timeline)
            except Exception as e:
                msg = f'Unable to list timeline: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
            

    @app.doc('create_timeline')
    @app.expect(timeline_item_create)
    def post(self, id: int):
        '''Cria um novo item na timeline'''
        with closing(configure_session()) as session:
            try:

                pet: Pet = session.query(Pet).filter(
                    Pet.activated).filter(Pet.id == id).first()
                if not pet:
                    return get_response(HTTPStatus.NO_CONTENT, None)

                type: str = request.json.get('type')
                title: str = request.json.get('title')
                description: str = request.json.get('description')
                vet: str = request.json.get('vet')
                clinic: str = request.json.get('clinic')
                created_by_id: int = request.json.get('created_by_id')
                created_by_role: str = request.json.get('created_by_role')
                
                if None in (type, title, description, vet, clinic, created_by_id, created_by_role):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to create timeline item. Missing at least one mandatory field")
                
                match created_by_role.lower():
                    case 'user':
                        user: User = session.query(User).filter(
                        User.activated).filter(User.id == created_by_id).first()
                        if not user:
                            return get_response(HTTPStatus.BAD_REQUEST, f"Unable to get user with id {created_by_id}")
                    case 'clinica':
                        clinica: Clinica = session.query(Clinica).filter(
                        Clinica.activated).filter(Clinica.id == created_by_id).first()
                        if not clinica:
                            return get_response(HTTPStatus.BAD_REQUEST, f"Unable to get clinica with id {created_by_id}")
                    case 'vet':
                        vet: Vet = session.query(Vet).filter(
                        Vet.activated).filter(Vet.id == created_by_id).first()
                        if not vet:
                            return get_response(HTTPStatus.BAD_REQUEST, f"Unable to get vet with id {created_by_id}")
                
                timeline = Timeline(type, title, description, vet, clinic, id, created_by_id, created_by_role.lower())
                session.add(timeline)
                session.commit()
                return TimelineSchema().dump(timeline), HTTPStatus.CREATED
            except Exception as e:
                session.rollback()
                msg = f'Unable to create a new timeline item. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
            

@app.route('/<int:timeline_id>/timeline')
class RoutePetEditAndDeleteTimeline(Resource):

    @app.doc('update_timeline_item')
    @app.expect(timeline_item_update)
    def put(self, timeline_id: int):
        '''Atualiza os dados de um item na timeline'''
        with closing(configure_session()) as session:
            try:
                timeline: Timeline = session.query(Timeline).filter(
                    Timeline.activated).filter(Timeline.id == timeline_id).first()
                if not timeline:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                
                type: str = request.json.get('type')
                title: str = request.json.get('title')
                description: str = request.json.get('description')
                vet: str = request.json.get('vet')
                clinic: str = request.json.get('clinic')
                
                if type:
                    timeline.type = type
                if title:
                    timeline.title = title
                if description:
                    timeline.description = description
                if vet:
                    timeline.vet = vet
                if clinic:
                    timeline.clinic = clinic
                
                session.commit()

                return TimelineSchema().dump(timeline)

            except Exception as e:
                session.rollback()
                msg = f'Unable to update timeline item with id {timeline_id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)

    @app.doc('delete_timeline_item')
    def delete(self, timeline_id: int):
        '''Deleta um item da Timeline'''
        with closing(configure_session()) as session:
            try:
                timeline: Timeline = session.query(Timeline).filter(
                    Timeline.activated).filter(Timeline.id == timeline_id).first()
                if not timeline:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                timeline.activated = False
                session.commit()
                return get_response(HTTPStatus.OK, f"Timeline item with id {timeline_id} successfully deactivated")
            except Exception as e:
                session.rollback()
                msg = f'Unable to delete timeline item with id {timeline_id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
            