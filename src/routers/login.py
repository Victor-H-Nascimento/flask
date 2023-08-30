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
from src.models import Clinica, ClinicaSchema, User, UserSchema, Vet, VetSchema
from src.routers.helpers import get_response, configure_session

load_dotenv()

login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username do usuário, veterinário ou clinica'),
    'pwd': fields.String(required=True, description='Senha do usuário'),
})


@app.route('')
@app.expect(login_model)
class RouteLogin(Resource):
    @staticmethod
    def post():

        username: str = request.json.get('username')
        pwd: str = request.json.get('pwd')

        if not (username and pwd):
            return get_response(HTTPStatus.BAD_REQUEST, "Both username and pwd fields must be sent")

        with closing(configure_session()) as session:

            user: User = session.query(User) \
                .filter(User.username == username) \
                .filter(User.activated) \
                .first()

            if user:
                if not User.verify_password(user, pwd):
                    return get_response(HTTPStatus.FORBIDDEN, "Username or password is incorrect")

                token = jwt.encode({
                    'id': user.id,
                    'name': user.name,
                    'lastname': user.lastname,
                    'role': user.role,
                    'exp': datetime.utcnow() + timedelta(minutes=int(os.getenv('JWT_TOKEN_TIMEOUT_MINS')))
                }, os.getenv('JWT_CRYPT_KEY'), algorithm="HS256")

                logger.info(
                    f"{user.role.capitalize()} {user.name} {user.lastname} logged in successfully")

                return make_response(jsonify({
                    'token': token,
                    "user": UserSchema().dump(user)
                }), HTTPStatus.ACCEPTED)
            
            clinica: Clinica = session.query(Clinica) \
                .filter(Clinica.username == username) \
                .filter(Clinica.activated) \
                .first()
            
            if clinica:
                if not Clinica.verify_password(clinica, pwd):
                    return get_response(HTTPStatus.FORBIDDEN, "Username or password is incorrect")

                token = jwt.encode({
                    'id': clinica.id,
                    'name': clinica.name,
                    'role': clinica.role,
                    'exp': datetime.utcnow() + timedelta(minutes=int(os.getenv('JWT_TOKEN_TIMEOUT_MINS')))
                }, os.getenv('JWT_CRYPT_KEY'), algorithm="HS256")

                logger.info(
                    f"{clinica.role.capitalize()} {clinica.name} logged in successfully")

                return make_response(jsonify({
                    'token': token,
                    "clinica": ClinicaSchema().dump(clinica)
                }), HTTPStatus.ACCEPTED)
            
            vet: Vet = session.query(Vet) \
                .filter(Vet.username == username) \
                .filter(Vet.activated) \
                .first()
            
            if vet:
                if not Vet.verify_password(vet, pwd):
                    return get_response(HTTPStatus.FORBIDDEN, "Username or password is incorrect")

                token = jwt.encode({
                    'id': vet.id,
                    'name': vet.name,
                    'role': vet.role,
                    'exp': datetime.utcnow() + timedelta(minutes=int(os.getenv('JWT_TOKEN_TIMEOUT_MINS')))
                }, os.getenv('JWT_CRYPT_KEY'), algorithm="HS256")

                logger.info(
                    f"{vet.role.capitalize()} {vet.name} logged in successfully")

                return make_response(jsonify({
                    'token': token,
                    "vet": VetSchema().dump(vet)
                }), HTTPStatus.ACCEPTED)
            
            return get_response(HTTPStatus.NOT_FOUND, f"Username {username} not found")