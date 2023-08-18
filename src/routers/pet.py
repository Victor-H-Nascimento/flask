from contextlib import closing
from flask import request
from flask_restx import Resource, fields
from http import HTTPStatus
from loguru import logger

from src import api, pets_namespace as app
from src.models import Pet, PetSchema, User
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
    'activated': fields.Boolean(required=False, description='Informa se perfil do pet esta ativo'),
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
})

@app.route('')
class RoutePet(Resource):
    @app.doc('list_pets')
    def get(self):
        '''Mostra todos os pets'''
        with closing(configure_session()) as session:
            try:
                pets: Pet = session.query(Pet).filter(
                    Pet.activated).order_by(Pet.id).all()
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

                if None in (name, size, breed, age, castrated, weight, specie, gender, user_id):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to create pet. Missing at least one mandatory field")

                pet = Pet(name, size, breed, age, castrated, weight, specie, gender, user_id)
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
    @app.doc('list all pets from an user')
    def get(self, id: int):
        '''Mostra todos os pets de um usuario'''
        with closing(configure_session()) as session:
            try:
                user: User = session.query(User).filter(
                    User.activated).filter(User.id == id).first()
                if not user:
                    return get_response(HTTPStatus.NO_CONTENT, None)

                pets: Pet = session.query(Pet).filter(
                    Pet.activated).filter(Pet.user_id == id).order_by(Pet.name).all()
                if not pets:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return PetSchema(many=True).dump(pets)
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