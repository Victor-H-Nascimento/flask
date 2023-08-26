from contextlib import closing
from flask import request
from flask_restx import Resource, fields
from http import HTTPStatus
from loguru import logger

from src import api, services_namespace as app
from src.models import Services, ServicesSchema
from src.routers.helpers import get_response, configure_session


service_model_create = api.model('ServiceCreate', {
    'name': fields.String(required=True, description='Nome do Serviço'),
})

service_model_update = api.model('ServiceUpdate', {
    'name': fields.String(required=False, description='Nome do Serviço'),
})


@app.route('')
class RouteService(Resource):
    @app.doc('list_services')
    def get(self):
        '''Lista todos os serviços'''
        with closing(configure_session()) as session:
            try:
                services: Services = session.query(Services).filter(
                    Services.activated).order_by(Services.name).all()
                if not services:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return ServicesSchema(many=True).dump(services)
            except Exception as e:
                session.rollback()
                msg = f'Unable to list all services. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


    @app.doc('create_service')
    @app.expect(service_model_create)
    def post(self):
        '''Cria um novo serviço'''
        with closing(configure_session()) as session:
            try:
                name: str = request.json.get('name')

                if not name:
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to create service. Missing at least one mandatory field")

                service = Services(name)
                session.add(service)
                session.commit()
                return ServicesSchema().dump(service), HTTPStatus.CREATED
            except Exception as e:
                session.rollback()
                msg = f'Unable to create a new service. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


@app.route('/<int:id>')
class RouteServicerWithId(Resource):
    @app.doc('list_single_service')
    def get(self, id: int):
        '''Mostra serviço pelo id'''
        with closing(configure_session()) as session:
            try:
                service: Services = session.query(Services).filter(
                    Services.activated).filter(Services.id == id).first()
                if not service:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return ServicesSchema().dump(service)
            except Exception as e:
                session.rollback()
                msg = f'Unable to list service with id {id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


    @app.doc('update_single_service')
    @app.expect(service_model_update)
    def put(self, id: int):
        '''Atualiza os dados de um serviço'''
        with closing(configure_session()) as session:
            try:
                service: Services = session.query(Services).filter(
                    Services.activated).filter(Services.id == id).first()
                if not service:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                
                name: str = request.json.get('name')

                if name:
                    service.name = name
                
                session.commit()

                return ServicesSchema().dump(service)

            except Exception as e:
                session.rollback()
                msg = f'Unable to list service with id {id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)


    @app.doc('delete_single_service')
    def delete(self, id: int):
        '''Deleta um serviço'''
        with closing(configure_session()) as session:
            try:
                service: Services = session.query(Services).filter(
                    Services.activated).filter(Services.id == id).first()
                if not service:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                service.activated = False
                session.commit()
                return get_response(HTTPStatus.OK, f"Services {service.name} successfully deactivated")
            except Exception as e:
                session.rollback()
                msg = f'Unable to delete service with id {id}. Rollback executed: {str(e)}'
                logger.exception(msg)
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, msg)
