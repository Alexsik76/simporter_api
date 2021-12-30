import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = f"Expected environment variable {name} not set."
        raise Exception(message)


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'dev'
    BASE_DIR = basedir
    SOURCE_FILE_NAME = get_env_variable('SOURCE_FILE_NAME')
    SOURCE_PATH = os.path.join(BASE_DIR, 'source_data/', SOURCE_FILE_NAME)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


app_config = {
    'base_config': Config,
    'testing': TestingConfig,
    'develop': DevelopmentConfig
}
