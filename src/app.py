import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

from src.config import Db_config
from src.helpers import EnvVarsTranslater, ContextHelper

basedir = os.path.dirname(os.path.realpath(__file__))

load_dotenv()


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = Db_config.get_db_con_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET_KEY')
    app.config['SQLALCHEMY_ECHO'] = EnvVarsTranslater.get_bool(
        'SQLALCHEMY_SHOW_QUERY_LOGS')

    dispose_old_db_connection(app)

    return app


# WSGI keeps the same db connection to all cloned pods at first, which leads to error: "SSL error: decryption failed
# or bad record mac." Important refresh the connection after postfork
def dispose_old_db_connection(app: Flask) -> None:
    if not ContextHelper.is_running_inside_wsgi():
        logger.info(
            "Skipping disposing old db connection, since app is not running inside wsgi")
        return

    try:
        logger.info("Disposing old db connection")

        def _dispose_db_pool():
            with app.app_context():
                db.engine.dispose()

        # from uwsgidecorators import postfork
        # postfork(_dispose_db_pool)

        logger.info("Disposed old db connection successfully")
    except ImportError:
        logger.exception("Error disposing old db connection.")


# TODO: Refactor - replace this method with flask blueprint
def make_imports_into_app():
    import src.routers

    if EnvVarsTranslater.get_bool("SQLALCHEMY_AUTO_CREATE_TABLES"):
        db.create_all()
        db.session.commit()


app: Flask = create_app()

api = Api(app)

cors = CORS(app, resources=r'*', headers='Content-Type')

ma = Marshmallow(app)

db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app, db)
migrate.init_app(app, db)
