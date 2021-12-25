import os
# from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'dev'
    STATIC_FOLDER = 'app/static'
    TEMPLATES_FOLDER = 'app/templates'
    BASE_DIR = basedir
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    BASE_DIR = basedir
    # WTF_CSRF_ENABLED = False


app_config = {
    'base_config': Config,
    'testing': TestingConfig,
    'develop': DevelopmentConfig
}
