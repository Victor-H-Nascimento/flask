from http import HTTPStatus
from flask_restx import Resource, fields
from flask import request

from src import db, api, users_namespace
# from src.logs import logger
from src.models import User
from src.schemas import UserSchema
from src.routers.helpers import get_response


user_model = api.model('User', {
    'name': fields.String(required=True, description='The user name'),
    'email': fields.String(required=True, description='The user email'),
})


@users_namespace.route('')
class RouteUser(Resource):
    @users_namespace.doc('list_users')
    def get(self):
        '''List all users'''
        users = db.session.query(User).all()
        if not users:
            return get_response(HTTPStatus.NO_CONTENT, "No users created yet")
        # logger.info('get all users')
        return UserSchema(many=True).dump(users)

    @users_namespace.doc('create_user')
    @users_namespace.expect(user_model)
    def post(self):
        '''Create a new user'''
        user = User(name=request.json['name'],
                    email=request.json['email'])
        db.session.add(user)
        db.session.commit()
        return UserSchema().dump(user), HTTPStatus.CREATED
