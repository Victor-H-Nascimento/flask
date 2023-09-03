from contextlib import closing
from flask import request
from flask_restx import Resource, fields
from http import HTTPStatus
from loguru import logger

from src import api, clinicas_namespace as app
from src.models import Clinica, ClinicaSchema, Services, ServicesSchema, Vet, VetSchema
from src.routers.helpers import get_response, configure_session


clinica_model_create = api.model('ClinicaCreate', {
    'name': fields.String(required=True, description='Nome da Clínica'),
    'cnpj': fields.String(required=True, description='CNPJ da Clínica'),
    'address': fields.String(required=True, description='Logradouro da Clínica'),
    'number': fields.String(required=True, description='Número do logradouro da Clínica'),
    'zip_code': fields.String(required=True, description='CEP da Clínica'),
    'neighborhood': fields.String(required=True, description='Bairro da Clínica'),
    'username': fields.String(required=True, description='Usuario da Clínica'),
    'pwd': fields.String(required=True, description='Senha da Clínica')
})

clinica_model_update = api.model('ClinicaUpdate', {
    'name': fields.String(required=False, description='Nome da Clínica'),
    'cnpj': fields.String(required=False, description='CNPJ da Clínica'),
    'address': fields.String(required=False, description='Logradouro da Clínica'),
    'number': fields.String(required=False, description='Número do logradouro da Clínica'),
    'zip_code': fields.String(required=False, description='CEP da Clínica'),
    'neighborhood': fields.String(required=False, description='Bairro da Clínica')
})


clinica_servico_model = api.model('Clinica-Service-Connect', {
    'clinica': fields.Integer(description='ID da clínica', required=True),
    'servico': fields.Integer(description='ID do serviço', required=True)
})

@app.route('')
class RouteClinica(Resource):
    @app.doc('list_clinicas')
    def get(self):
        '''Lista todas as clinicas'''
        with closing(configure_session()) as session:
            try:
                clinicas: Clinica = session.query(Clinica).filter(
                    Clinica.activated).order_by(Clinica.id).all()
                if not clinicas:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return ClinicaSchema(many=True).dump(clinicas)
            except Exception as e:
                session.rollback()
                msg = f'Unable to list all clinicas. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


    @app.doc('create_clinica')
    @app.expect(clinica_model_create)
    def post(self):
        '''Cria uma nova clinica'''
        with closing(configure_session()) as session:
            try:
                name: str = request.json.get('name')
                cnpj: str = request.json.get('cnpj')
                address: str = request.json.get('address')
                number: str = request.json.get('number')
                zip_code: str = request.json.get('zip_code')
                neighborhood: str = request.json.get('neighborhood')
                username: str = request.json.get('username')
                pwd: str = request.json.get('pwd')
                
                if None in (name, cnpj, address, number, zip_code, neighborhood, username, pwd):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to create clinica. Missing at least one mandatory field")

                clinica = Clinica(name, cnpj, address, number, zip_code, neighborhood, username, pwd)
                session.add(clinica)
                session.commit()
                return ClinicaSchema().dump(clinica), HTTPStatus.CREATED
            except Exception as e:
                session.rollback()
                msg = f'Unable to create a new clinica. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


@app.route('/<int:id>')
class RouteClinicaWithId(Resource):
    @app.doc('list_single_clinica')
    def get(self, id: int):
        '''Mostra clinica pelo id'''
        with closing(configure_session()) as session:
            try:
                clinica: Clinica = session.query(Clinica).filter(
                    Clinica.activated).filter(Clinica.id == id).first()
                if not clinica:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return ClinicaSchema().dump(clinica)
            except Exception as e:
                session.rollback()
                msg = f'Unable to list clinica with id {id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


    @app.doc('update_single_clinica')
    @app.expect(clinica_model_update)
    def put(self, id: int):
        '''Atualiza os dados de uma clinica'''
        with closing(configure_session()) as session:
            try:
                clinica: Clinica = session.query(Clinica).filter(
                    Clinica.activated).filter(Clinica.id == id).first()
                if not clinica:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                
                name: str = request.json.get('name')
                cnpj: str = request.json.get('cnpj')
                address: str = request.json.get('address')
                number: str = request.json.get('number')
                zip_code: str = request.json.get('zip_code')
                neighborhood: str = request.json.get('neighborhood')
                username: str = request.json.get('username')
                pwd: str = request.json.get('pwd')

                if name:
                    clinica.name = name
                if cnpj:
                    clinica.cnpj = cnpj
                if address:
                    clinica.address = address
                if number:
                    clinica.number = number
                if zip_code:
                    clinica.zip_code = zip_code
                if neighborhood:
                    clinica.neighborhood = neighborhood
                if username:
                    clinica.username = username
                if pwd:
                    clinica.pwd = pwd
                
                session.commit()

                return ClinicaSchema().dump(clinica)

            except Exception as e:
                session.rollback()
                msg = f'Unable to list clinica with id {id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


    @app.doc('delete_single_clinica')
    def delete(self, id: int):
        '''Deleta uma clinica'''
        with closing(configure_session()) as session:
            try:
                clinica: Clinica = session.query(Clinica).filter(
                    Clinica.activated).filter(Clinica.id == id).first()
                if not clinica:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                clinica.activated = False
                session.commit()
                return get_response(HTTPStatus.OK, f"Clinica {clinica.name} successfully deactivated")
            except Exception as e:
                session.rollback()
                msg = f'Unable to delete clinica with id {id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


@app.route('/conectar-serviço')
class RouteClinicaWithQueryParams(Resource):
    @api.expect(clinica_servico_model, validate=True)
    def post(self):
        '''Adiciona um serviço à uma clinica'''
        with closing(configure_session()) as session:
            try:

                clinica_id: int = request.json.get('clinica')
                servico_id: int = request.json.get('servico')

                if not (clinica_id and servico_id):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to connect clinica to service. Missing at least one mandatory field")
                
                clinica: Clinica = session.query(Clinica).filter(Clinica.activated).filter(Clinica.id == clinica_id).first()
                service: Services = session.query(Services).filter(Services.activated).filter(Services.id == servico_id).first()

                if not (clinica and service):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to connect clinica to service. Not found clinic or service")

                clinica.services.append(service)
                session.commit()

                return get_response(HTTPStatus.OK, f"Service {service.name} successfully added to Clinic {clinica.name}")
            except Exception as e:
                session.rollback()
                msg = f'Unable to add connection between clinic and service. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
            

    @api.expect(clinica_servico_model, validate=True)
    def delete(self):
        '''Deleta conexão entre clinica e serviço'''
        with closing(configure_session()) as session:
            try:

                clinica_id: int = request.json.get('clinica')
                servico_id: int = request.json.get('servico')

                if not (clinica_id and servico_id):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to disconnect clinica to service. Missing at least one mandatory field")
                
                clinica: Clinica = session.query(Clinica).filter(Clinica.activated).filter(Clinica.id == clinica_id).first()
                service: Services = session.query(Services).filter(Services.activated).filter(Services.id == servico_id).first()

                if not (clinica and service):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to disconnect clinica to service. Not found clinic or service")

                clinica.services.remove(service)
                session.commit()

                return get_response(HTTPStatus.OK, f"Service {service.name} successfully removed from Clinic {clinica.name}")
            except Exception as e:
                session.rollback()
                msg = f'Unable to remove connection between clinic and service. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)

@app.route('/<int:id>/services')
class RouteServicesFromClinic(Resource):
    def get(self, id: int):
        '''Retorna todos os serviços de uma clínica'''
        with closing(configure_session()) as session:
            try:

                clinica: Clinica = session.query(Clinica).filter(Clinica.activated).filter(Clinica.id == id).first()

                if not clinica:
                    return get_response(HTTPStatus.BAD_REQUEST, f"Unable to get services from clinic with id {id}")
                
                services = clinica.services

                return ServicesSchema(many=True).dump(services), HTTPStatus.OK
            except Exception as e:
                msg = f'Unable to get services from clinic {clinica.name}: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


@app.route('/<int:id>/pets')
class RoutePetsFromClinic(Resource):
    def get(self, id: int):
        '''Retorna todos os pets de uma clínica'''
        with closing(configure_session()) as session:
            try:

                clinica: Clinica = session.query(Clinica).filter(Clinica.activated).filter(Clinica.id == id).first()

                if not clinica:
                    return get_response(HTTPStatus.BAD_REQUEST, f"Unable to get pets from clinic with id {id}")
                
                pets = clinica.pets

                return ServicesSchema(many=True).dump(pets), HTTPStatus.OK
            except Exception as e:
                msg = f'Unable to get pets from clinic {clinica.name}: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


@app.route('/<int:id>/vets')
class RouteVetFromClinica(Resource):
    @app.doc('list all vets from a clinic')
    def get(self, id: int):
        '''Mostra todos os vets de uma clinica.'''
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
            