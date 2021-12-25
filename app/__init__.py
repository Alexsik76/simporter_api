from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
# from flask_marshmallow import Marshmallow
# from flaskext.markdown import Markdown


db = SQLAlchemy()
# ma = Marshmallow()


# def get_choices_v1(flask_app):
#     """ Creates choices lists for Swaggers documentation.
#     Lists of groups and courses must be created before the first api call for them to appear in the Swagger.
#     But when running init-db, if the database does not exist, it causes an error.
#     """
#     from app.models import StudentModel
#     engine = db.get_engine(flask_app)
#     tables = engine.table_names()
#     if tables:
#         with flask_app.app_context():
#             StudentModel.get_all_groups_and_courses()
#
#
# def get_choices_v2(flask_app):
#     """ Same as get_choices_v1()."""
#     with flask_app.app_context():
#         from app.models import StudentModel
#         try:
#             StudentModel.get_all_groups_and_courses()
#         except OperationalError as _:
#             print('Expected error.')


def create_app(test_config=False):
    app = Flask(__name__)
    if test_config:
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['develop'])

    db.init_app(app)
    from app.create_db import init_app
    init_app(app)

    # from app.api import bp_api
    # app.register_blueprint(bp_api, url_prefix='/api/v1/')
    return app


from app import models
