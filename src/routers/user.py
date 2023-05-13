from flask import request
from flask_restx import Resource, fields
from http import HTTPStatus
from loguru import logger

from src import db, api, users_namespace as app
from src.models import User, UserSchema
from src.routers.helpers import get_response


user_model = api.model('User', {
    'email': fields.String(required=True, description='The user email'),
    'name': fields.String(required=True, description='The user name'),
    'lastname': fields.String(required=True, description='The user lastname'),
    'document': fields.String(required=True, description='The user document'),
    'phone_number': fields.String(required=True, description='The user phone_number'),
    'pwd': fields.String(required=True, description='The user pwd'),
    'activated': fields.Boolean(required=False, description='shows if user is activated'),
})


@app.route('')
class RouteUser(Resource):
    @app.doc('list_users')
    def get(self):
        '''List all users'''
        try:
            users: User = db.session.query(User).filter(
                User.activated == True).order_by(User.id).all()
            if not users:
                return get_response(HTTPStatus.NO_CONTENT, "No users created yet")
            return UserSchema(many=True).dump(users)
        except Exception as e:
            db.session.rollback()
            logger.exception(
                f'Unable to list all users. Rollback executed: {str(e)}')
            return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")

    @app.doc('create_user')
    @app.expect(user_model)
    def post(self):
        '''Create a new user'''
        try:
            user = User(email=request.json['email'], name=request.json['name'], lastname=request.json['lastname'],
                        document=request.json['document'], phone_number=request.json['phone_number'], pwd=request.json['pwd'])
            db.session.add(user)
            db.session.commit()
            return UserSchema().dump(user), HTTPStatus.CREATED
        except Exception as e:
            db.session.rollback()
            logger.exception(
                f'Unable to create a new user. Rollback executed: {str(e)}')
            return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")


@app.route('/<int:id>')
class RouteUserWithId(Resource):
    @app.doc('list_single_user')
    def get(self, id: int):
        '''List single user'''
        try:
            user: User = db.session.query(User).filter(
                User.activated == True).filter(User.id == id).first()
            if not user:
                return get_response(HTTPStatus.NO_CONTENT, f"No user existing with id {id}")
            return UserSchema().dump(user)
        except Exception as e:
            db.session.rollback()
            logger.exception(
                f'Unable to list user with id {id}. Rollback executed: {str(e)}')
            return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")

    @app.doc('update_single_user')
    def put(self, id: int):
        '''Update single user'''
        try:
            user: User = db.session.query(User).filter(
                User.activated == True).filter(User.id == id).first()
            if not user:
                return get_response(HTTPStatus.NO_CONTENT, f"No user existing with id {id}")

        except Exception as e:
            db.session.rollback()
            logger.exception(
                f'Unable to list user with id {id}. Rollback executed: {str(e)}')
            return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")

    @app.doc('delete_single_user')
    def delete(self, id: int):
        '''Delete single user'''
        try:
            user: User = db.session.query(User).filter(
                User.activated == True).filter(User.id == id).first()
            if not user:
                return get_response(HTTPStatus.NO_CONTENT, f"No user existing with id {id}")
            user.activated = False
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(
                f'Unable to delete user with id {id}. Rollback executed: {str(e)}')
            return get_response(HTTPStatus.INTERNAL_SERVER_ERROR, "An internal server error occurred")
