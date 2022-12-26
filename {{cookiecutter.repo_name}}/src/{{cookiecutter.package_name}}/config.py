__all__ = ['config']

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    TESTING = False

    PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME') or 'http'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    WTF_CSRF_ENABLED = True

    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, '..', '..', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ApiConfig(Config):
    pass


class DevelopConfig(Config):
    TESTING = True
    APISPEC_SPEC_VERSION = 'Develop'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopConfig,
    'api': ApiConfig,
    'testing': TestConfig,

    'default': Config
}
