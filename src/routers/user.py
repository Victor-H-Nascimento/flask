from http import HTTPStatus
from flask_restx import Resource

from src import db, api
# from src.logs import logger
from src.models import User
from src.schemas import UserSchema
from src.routers.helpers import get_response


@api.route('/user')
class RouteUser(Resource):
    def get(self):
        result = db.session.query(User).all()
        if not result:
            return get_response(HTTPStatus.NO_CONTENT, "No users created yet")
        # logger.info('get all users')
        return UserSchema(many=True).dump(result)


# from flask import request
# from flask_restx import Namespace, Resource, fields, Api
# from src.schemas.user import UserSchema
# from src.models.user import User
# from config import db
# from contextlib import closing
# from flask import Blueprint, jsonify

# from sqlalchemy.orm import sessionmaker, Session
# from sqlalchemy.pool import NullPool
# from sqlalchemy import create_engine


# user_bp = Blueprint('user', __name__)
# api = Api(user_bp, version='1.0', title='My API', description='A description')
# user_schema = UserSchema()
# users_schema = UserSchema(many=True)

# user_input_model = api.model('UserInput', {
#     'name': fields.String(required=True, description='The user name'),
#     'email': fields.String(required=True, description='The user email'),
# })


# @api.route('/')
# class RouteUser(Resource):
#     @api.doc('list_users')
#     def get(self):
#         '''List all users'''
#         users = User.query.all()
#         return users_schema.dump(users)

#     @api.doc('create_user')
#     @api.expect(user_input_model)
#     def post(self):
#         '''Create a new user'''
#         user = User(name=request.json['name'],
#                     email=request.json['email'])
#         db.session.add(user)
#         db.session.commit()
#         return user_schema.dump(user), 201
