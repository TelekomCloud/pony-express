from flask import Flask, jsonify

from ponyexpress.api.exceptions import *


def create_app(environment='ponyexpress.config.configuration.DevelopmentConfig'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(environment)
    app.config.from_pyfile('/etc/pony-express/ponyexpress.cfg', True)
    app.config.from_envvar('PONYEXPRES_CFG', True)

    # Database
    from ponyexpress.database import db
    db.init_app(app)

    # Register blueprints
    from ponyexpress.api.v1.collector import collector
    from ponyexpress.api.v1.query import query
    from ponyexpress.api.v1.updater import updater

    app.register_blueprint(collector)
    app.register_blueprint(query)
    app.register_blueprint(updater)

    # Error handler
    app.register_error_handler(InvalidAPIUsage, handle_invalid_usage)

    return app


# Register error handlers
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response
