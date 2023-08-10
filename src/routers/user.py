from contextlib import closing
from flask import request
from flask_restx import Resource, fields
from http import HTTPStatus
from loguru import logger

from src import api, users_namespace as app
from src.models import User, UserSchema
from src.routers.helpers import get_response, configure_session


user_model_create = api.model('User Create', {
    'email': fields.String(required=True, description='The user email'),
    'name': fields.String(required=True, description='The user name'),
    'lastname': fields.String(required=True, description='The user lastname'),
    'document': fields.String(required=True, description='The user document'),
    'phone_number': fields.String(required=True, description='The user phone_number'),
    'pwd': fields.String(required=True, description='The user pwd'),
    'activated': fields.Boolean(required=False, description='shows if user is activated'),
})

user_model_update = api.model('User Update', {
    'email': fields.String(required=False, description='The user email'),
    'name': fields.String(required=False, description='The user name'),
    'lastname': fields.String(required=False, description='The user lastname'),
    'document': fields.String(required=False, description='The user document'),
    'phone_number': fields.String(required=False, description='The user phone_number'),
})


@app.route('')
class RouteUser(Resource):
    @app.doc('list_users')
    def get(self):
        '''List all users'''
        with closing(configure_session()) as session:
            try:
                users: User = session.query(User).filter(
                    User.activated).order_by(User.id).all()
                if not users:
                    return get_response(HTTPStatus.NO_CONTENT, "No users created yet")
                return UserSchema(many=True).dump(users)
            except Exception as e:
                session.rollback()
                logger.exception(
                    f'Unable to list all users. Rollback executed: {str(e)}')
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")


    @app.doc('create_user')
    @app.expect(user_model_create)
    def post(self):
        '''Create a new user'''
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
        '''List single user'''
        with closing(configure_session()) as session:
            try:
                user: User = session.query(User).filter(
                    User.activated).filter(User.id == id).first()
                if not user:
                    return get_response(HTTPStatus.NO_CONTENT, f"No user existing with id {id}")
                return UserSchema().dump(user)
            except Exception as e:
                session.rollback()
                logger.exception(
                    f'Unable to list user with id {id}. Rollback executed: {str(e)}')
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")


    @app.doc('update_single_user')
    @app.expect(user_model_update)
    def put(self, id: int):
        '''Update single user'''
        with closing(configure_session()) as session:
            try:
                user: User = session.query(User).filter(
                    User.activated).filter(User.id == id).first()
                if not user:
                    return get_response(HTTPStatus.NO_CONTENT, f"No user existing with id {id}")
                
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
        '''Delete single user'''
        with closing(configure_session()) as session:
            try:
                user: User = session.query(User).filter(
                    User.activated).filter(User.id == id).first()
                if not user:
                    return get_response(HTTPStatus.NO_CONTENT, f"No user existing with id {id}")
                user.activated = False
                session.commit()
                return get_response(HTTPStatus.OK, f"User {user.email} successfully deactivated")
            except Exception as e:
                session.rollback()
                logger.exception(
                    f'Unable to delete user with id {id}. Rollback executed: {str(e)}')
                return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")
