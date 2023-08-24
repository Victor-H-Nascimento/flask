from contextlib import closing
from flask import request
from flask_restx import Resource, fields
from http import HTTPStatus
from loguru import logger

from src import api, vets_namespace as app
from src.models import Vet, VetSchema, Clinica
from src.routers.helpers import get_response, configure_session

vet_model_create = api.model('VetCreate', {
    'name': fields.String(required=True, description='Nome do Veterinário'),
    'username': fields.String(required=True, description='Usuário do Veterinário'),
    'pwd': fields.String(required=True, description='Senha do Veterinário'),
    'clinica_id': fields.Integer(required=True, description='Id da Clinica que o Veterinário trabalho'),
})

vet_model_update = api.model('VetUpdate', {
    'name': fields.String(required=False, description='Nome do Veterinário'),
    'clinica_id': fields.Integer(required=False, description='Id da Clinica em que o Veterinário trabalha'),
})

@app.route('')
class RouteVet(Resource):
    @app.doc('list_vets')
    def get(self):
        '''Mostra todos os veterinários'''
        with closing(configure_session()) as session:
            try:
                vets: Vet = session.query(Vet).filter(
                    Vet.activated).order_by(Vet.name).all()
                if not vets:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return VetSchema(many=True).dump(vets)
            except Exception as e:
                session.rollback()
                msg = f'Unable to list all vets. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
            
    @app.doc('create_vet')
    @app.expect(vet_model_create)
    def post(self):
        '''Cria um novo vet'''
        with closing(configure_session()) as session:
            try:
                name: str = request.json.get('name')
                username: str = request.json.get('username')
                pwd: str = request.json.get('pwd')
                clinica_id: int = request.json.get('clinica_id')

                if None in (name, username, pwd, clinica_id):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to create vet. Missing at least one mandatory field")

                vet = Vet(name, username, pwd, clinica_id)
                session.add(vet)
                session.commit()
                return VetSchema().dump(vet), HTTPStatus.CREATED
            except Exception as e:
                session.rollback()
                msg = f'Unable to create a new vet. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


@app.route('/<int:id>')
class RouteVetWithId(Resource):
    @app.doc('list all vets from a clinic')
    def get(self, id: int):
        '''Mostra todos os vets de uma clinica.USAR O ID DA CLINICA'''
        with closing(configure_session()) as session:
            try:
                clinica: Clinica = session.query(Clinica).filter(
                    Clinica.activated).filter(Clinica.id == id).first()
                if not clinica:
                    return get_response(HTTPStatus.NO_CONTENT, None)

                vets: Vet = session.query(Vet).filter(
                    Vet.activated).filter(Vet.clinica_id == id).order_by(Vet.name).all()
                if not vets:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return VetSchema(many=True).dump(vets)
            except Exception as e:
                session.rollback()
                msg = f'Unable to list all vets. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
    

    @app.doc('update_single_vet_from_a_clinica')
    @app.expect(vet_model_update)
    def put(self, id: int):
        '''Atualiza os dados de um vet de um usuário'''
        with closing(configure_session()) as session:
            try:
                vet: Vet = session.query(Vet).filter(
                    Vet.activated).filter(Vet.id == id).first()
                if not vet:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                
                name: str = request.json.get('name')
                clinica_id: int = request.json.get('clinica_id')
                
                if name:
                    vet.name = name
                if clinica_id:
                    vet.clinica_id = clinica_id
                
                session.commit()

                return VetSchema().dump(vet)

            except Exception as e:
                session.rollback()
                msg = f'Unable to list vet with id {id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


    @app.doc('delete_single_vet')
    def delete(self, id: int):
        '''Deleta um vet'''
        with closing(configure_session()) as session:
            try:
                vet: Vet = session.query(Vet).filter(
                    Vet.activated).filter(Vet.id == id).first()
                if not vet:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                vet.activated = False
                session.commit()
                return get_response(HTTPStatus.OK, f"Vet {vet.name} successfully deactivated")
            except Exception as e:
                session.rollback()
                msg = f'Unable to delete vet with id {id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
