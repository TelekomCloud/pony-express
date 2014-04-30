import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////var/lib/pony-express/ponyexpress.db'
    REQUEST_LOG = '/var/log/ponyexpress.log'


class ProductionConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////var/lib/pony-express/ponyexpress.db'


class DevelopmentConfig(DefaultConfig):
    #SQLALCHEMY_ECHO = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, '../../', 'ponyexpress.db')
    REQUEST_LOG = os.path.join(_basedir, '../../ponyexpress.log')


class TestingConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    REQUEST_LOG = os.path.join(_basedir, 'ponyexpress.log')
