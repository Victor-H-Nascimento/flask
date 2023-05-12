from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from os import getenv

from src.config import get_db_con_uri
from src.helpers import EnvVarsTranslater


load_dotenv()


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_con_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SECRET_KEY'] = getenv('SESSION_SECRET_KEY')
    app.config['SQLALCHEMY_ECHO'] = EnvVarsTranslater.get_bool(
        'SQLALCHEMY_SHOW_QUERY_LOGS')

    return app


def make_imports_into_app():
    import src.routers

    if EnvVarsTranslater.get_bool("SQLALCHEMY_AUTO_CREATE_TABLES"):
        db.create_all()
        db.session.commit()


app: Flask = create_app()

api = Api(app,
          version='1.0',
          title='Dogpass API',
          description='O que falar dessa api que mal conheço e já considero pacas?'
          )

users_namespace = api.namespace('user', description='Users operations')

cors = CORS(app, resources=r'*', headers='Content-Type')

ma = Marshmallow(app)

db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app, db)
migrate.init_app(app, db)
