import os
import jwt

from contextlib import closing
from datetime import datetime, timedelta
from dotenv import load_dotenv
from http import HTTPStatus
from flask import request, make_response, jsonify
from flask_restx import Resource, fields
from loguru import logger
from src import api, login_namespace as app
from src.models import User, UserSchema
from src.routers.helpers import get_response, configure_session

load_dotenv()

login_model = api.model('Login', {
    'email': fields.String(required=True, description='The user email'),
    'pwd': fields.String(required=True, description='The user pwd'),
})


@app.route('')
@app.expect(login_model)
class RouteLogin(Resource):
    @staticmethod
    def post():

        email: str = request.json.get('email')
        pwd: str = request.json.get('pwd')

        if not (email and pwd):
            return get_response(HTTPStatus.BAD_REQUEST, "Both email and pwd fields must be sent")

        with closing(configure_session()) as session:

            user: User = session.query(User) \
                .filter(User.email == email) \
                .filter(User.activated) \
                .first()

            if not user or not User.verify_password(user, pwd):
                return get_response(HTTPStatus.FORBIDDEN, "Email or password is incorrect")

            token = jwt.encode({
                'id': user.id,
                'name': user.name,
                'lastname': user.lastname,
                'exp': datetime.utcnow() + timedelta(minutes=int(os.getenv('JWT_TOKEN_TIMEOUT_MINS')))
            }, os.getenv('JWT_CRYPT_KEY'),  algorithm="HS256")

            logger.info(
                f"{user.name} {user.lastname} logged in successfully")

            return make_response(jsonify({
                'token': token,
                "user": UserSchema().dump(user)
            }), HTTPStatus.ACCEPTED)