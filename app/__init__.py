from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
# from flask_marshmallow import Marshmallow
# from flaskext.markdown import Markdown


db = SQLAlchemy()


def create_app(test_config=False):
    app = Flask(__name__)
    if test_config:
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['develop'])

    db.init_app(app)
    from app.create_db import init_app
    init_app(app)

    from app.api import bp_api
    app.register_blueprint(bp_api)
    return app


from app import models
