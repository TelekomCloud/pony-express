from flask import Blueprint

query = Blueprint('query', __name__)

@query.route('/v1/nodes')
def nodes():
    return ''

@query.route('/v1/packages')
def packages():
    return ''
