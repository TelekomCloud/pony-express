from flask import Flask, jsonify, current_app, request

from ponyexpress.api.exceptions import *


def create_app(environment='ponyexpress.config.configuration.DefaultConfig'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(environment)
    app.config.from_pyfile('/etc/pony-express/ponyexpress.cfg', True)

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

    if app.debug is not True and app.testing is not True:
        import logging

        from logging.handlers import RotatingFileHandler

        file_handler = RotatingFileHandler(app.config.get('REQUEST_LOG', 'ponyexpress.log'), maxBytes=1024 * 1024 * 100,
                                           backupCount=20)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        app.logger.addHandler(file_handler)

        app.before_request(log_entry)

    return app


def log_entry():
    context = {
        'url': request.path,
        'method': request.method,
        'ip': request.environ.get("REMOTE_ADDR")
    }

    current_app.logger.info("%(ip)s %(method)s %(url)s", context)


# Register error handlers
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response
