import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, '../../', 'ponyexpress.db')


class ProductionConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, '../../', 'ponyexpress.db')


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


class TestingConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
