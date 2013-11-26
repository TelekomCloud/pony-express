import os

_basedir = os.path.abspath(os.path.dirname(__file__))

#TODO: set up logging
import logging

logging.basicConfig(filename=os.path.join(_basedir, '../../log/server.log'), level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, '../../', 'ponyexpress.db')


class ProductionConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, '../../', 'ponyexpress.db')


class DevelopmentConfig(DefaultConfig):
    #SQLALCHEMY_ECHO = True
    DEBUG = True


class TestingConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
