from flask import Flask, jsonify

from ponyexpress.api.v1.collector import collector
from ponyexpress.api.v1.query import query

from ponyexpress.api.exceptions import *
from ponyexpress.config.configuration import *

from ponyexpress.database import db
from ponyexpress.models.node import Node
from ponyexpress.models.package import Package

app = Flask(__name__)

# Load configuration
#TODO: load configuration depending on environment
app.config.from_object('ponyexpress.config.configuration.DevelopmentConfig')

# Database
db.init_app(app)

# Register blueprints
app.register_blueprint(collector)
app.register_blueprint(query)

# Register error handlers
@app.errorhandler(InvalidAPIUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response
