import logging

from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(test_config=False):
    app = Flask(__name__)
    if test_config:
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['develop'])

    db.init_app(app)
    engine = db.get_engine(app)
    if not engine.table_names():
        logging.warning('\nDatabase is not exist')
    from app.create_db import init_app
    init_app(app)

    from app.api import bp_api
    app.register_blueprint(bp_api)
    return app


from app import models
