from flask import Blueprint, jsonify

query = Blueprint('query', __name__)

@query.route('/v1/nodes')
def nodes():
    nodes = {}

    return jsonify(nodes)

@query.route('/v1/node/<fqdn>')
def node(fqdn):
    node = {}

    return jsonify(node)

@query.route('/v1/packages')
def packages():
    return jsonify('')


@query.route('/v1/package/<id>')
def package(id):
    return jsonify('')
