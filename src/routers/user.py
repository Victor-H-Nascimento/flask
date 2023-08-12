from contextlib import closing
from flask import request
from flask_restx import Resource, fields
from http import HTTPStatus
from loguru import logger

from src import api, users_namespace as app
from src.models import User, UserSchema
from src.routers.helpers import get_response, configure_session


user_model_create = api.model('UserCreate', {
    'email': fields.String(required=True, description='Email do Usuário'),
    'name': fields.String(required=True, description='Nome do Usuário'),
    'lastname': fields.String(required=True, description='Sobrenome do Usuário'),
    'document': fields.String(required=True, description='CPF/RG do Usuário'),
    'phone_number': fields.String(required=True, description='Telefone do Usuário'),
    'pwd': fields.String(required=True, description='Senha do Usuário'),
    'activated': fields.Boolean(required=False, description='Informa se perfil do usuário esta ativo'),
})

user_model_update = api.model('UserUpdate', {
    'email': fields.String(required=False, description='Email do Usuário'),
    'name': fields.String(required=False, description='Nome do Usuário'),
    'lastname': fields.String(required=False, description='Sobrenome do Usuário'),
    'document': fields.String(required=False, description='CPF/RG do Usuário'),
    'phone_number': fields.String(required=False, description='Telefone do Usuário'),
})


@app.route('')
class RouteUser(Resource):
    @app.doc('list_users')
    def get(self):
        '''Lista todos os usuários'''
        with closing(configure_session()) as session:
            try:
                users: User = session.query(User).filter(
                    User.activated).order_by(User.id).all()
                if not users:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return UserSchema(many=True).dump(users)
            except Exception as e:
                session.rollback()
                logger.exception(
                    f'Unable to list all users. Rollback executed: {str(e)}')
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")


    @app.doc('create_user')
    @app.expect(user_model_create)
    def post(self):
        '''Cria um novo usuário'''
        with closing(configure_session()) as session:
            try:
                name: str = request.json.get('name')
                lastname: str = request.json.get('lastname')
                email: str = request.json.get('email')
                document: str = request.json.get('document')
                phone_number: str = request.json.get('phone_number')
                pwd: str = request.json.get('pwd')

                if None in (name, lastname, email, document, phone_number, pwd):
                    return get_response(HTTPStatus.BAD_REQUEST, "Unable to create user. Missing at least one mandatory field")

                user = User(email, name, lastname, document, phone_number, pwd)
                session.add(user)
                session.commit()
                return UserSchema().dump(user), HTTPStatus.CREATED
            except Exception as e:
                session.rollback()
                logger.exception(
                    f'Unable to create a new user. Rollback executed: {str(e)}')
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")


@app.route('/<int:id>')
class RouteUserWithId(Resource):
    @app.doc('list_single_user')
    def get(self, id: int):
        '''Mostra usuário pelo id'''
        with closing(configure_session()) as session:
            try:
                user: User = session.query(User).filter(
                    User.activated).filter(User.id == id).first()
                if not user:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                return UserSchema().dump(user)
            except Exception as e:
                session.rollback()
                logger.exception(
                    f'Unable to list user with id {id}. Rollback executed: {str(e)}')
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")


    @app.doc('update_single_user')
    @app.expect(user_model_update)
    def put(self, id: int):
        '''Atualiza os dados de um usuário'''
        with closing(configure_session()) as session:
            try:
                user: User = session.query(User).filter(
                    User.activated).filter(User.id == id).first()
                if not user:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                
                name: str = request.json.get('name')
                lastname: str = request.json.get('lastname')
                email: str = request.json.get('email')
                document: str = request.json.get('document')
                phone_number: str = request.json.get('phone_number')

                if name:
                    user.name = name
                if lastname:
                    user.lastname = lastname
                if email:
                    user.email = email
                if document:
                    user.document = document
                if phone_number:
                    user.phone_number = phone_number
                
                session.commit()

                return UserSchema().dump(user)

            except Exception as e:
                session.rollback()
                logger.exception(
                    f'Unable to list user with id {id}. Rollback executed: {str(e)}')
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")


    @app.doc('delete_single_user')
    def delete(self, id: int):
        '''Deleta um usuário'''
        with closing(configure_session()) as session:
            try:
                user: User = session.query(User).filter(
                    User.activated).filter(User.id == id).first()
                if not user:
                    return get_response(HTTPStatus.NO_CONTENT, None)
                user.activated = False
                session.commit()
                return get_response(HTTPStatus.OK, f"User {user.email} successfully deactivated")
            except Exception as e:
                session.rollback()
                logger.exception(
                    f'Unable to delete user with id {id}. Rollback executed: {str(e)}')
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")
