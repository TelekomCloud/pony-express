from flask import Flask, jsonify

from ponyexpress.api.v1.collector import collector
from ponyexpress.api.v1.query import query
from ponyexpress.api.exceptions import *

app = Flask(__name__)

# Register blueprints
app.register_blueprint(collector)
app.register_blueprint(query)

# Register error handlers
@app.errorhandler(InvalidAPIUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response
