from flask import Blueprint, Response, json
from ponyexpress.models.package import Package
from ponyexpress.models.node import Node
from ponyexpress.api.exceptions import *

query = Blueprint('query', __name__)


@query.route('/v1/nodes', methods=['GET'])
@query.route('/v1/nodes/<int:limit>/<int:offset>', methods=['GET'])
def nodes(limit=10, offset=0):
    result = []

    if (0 < limit <= 50) and offset >= 0:
        queried_nodes = Node.query.limit(limit).offset(offset)
    else:
        raise InvalidAPIUsage('Not allowed to fetch more than 50 objects', 410)

    for n in queried_nodes:
        res = {
            'id': n.name,
            'packages': [],
        }
        result.append(res)

    return Response(json.dumps(result), mimetype='application/json')


@query.route('/v1/node/<fqdn>', methods=['GET'])
@query.route('/v1/node/<fqdn>/<full>', methods=['GET'])
def node(fqdn, full=None):
    if fqdn != '':
        q_node = Node.query.filter_by(name=fqdn).first()

        if q_node:
            r_node = {
                'id': q_node.name,
                'packages': []
            }

            if full is not None:
                for i in q_node.packages:
                    r_p = {
                        'id': i.sha,
                        'name': i.name,
                        'version': i.version,
                        'summary': '',
                        'uri': i.uri,
                        'provider': '',
                        'architecture': '',
                    }
                    r_node['packages'].append(r_p)

            return Response(json.dumps(r_node), mimetype='application/json')
        else:
            raise InvalidAPIUsage('Invalid API usage', 410)


@query.route('/v1/packages', methods=['GET'])
@query.route('/v1/packages/<int:limit>/<int:offset>', methods=['GET'])
def packages(limit=10, offset=0):
    result = []

    if (0 < limit <= 50) and offset >= 0:
        packages = Package.query.limit(limit).offset(offset)
    else:
        raise InvalidAPIUsage('Not allowed to fetch more than 50 objects', 410)

    for p in packages:
        r_p = {
            'id': p.sha,
            'name': p.name,
            'version': p.version,
            'summary': p.summary,
            'uri': p.uri,
            'provider': p.provider,
            'architecture': p.architecture,
        }
        result.append(r_p)

    return Response(json.dumps(result), mimetype='application/json')


@query.route('/v1/package/<id>', methods=['GET'])
def package(id):

    if id != '':
        package = Package.query.filter_by(sha=id).first()
    else:
        raise InvalidAPIUsage('Invalid API usage', 410)

    if package:
        result = {
            'id': package.sha,
            'name': package.name,
            'version': package.version,
            'summary': package.summary,
            'uri': package.uri,
            'provider': package.provider,
            'architecture': package.architecture,
        }

        return Response(json.dumps(result), mimetype='application/json')
    else:
        raise InvalidAPIUsage('Package not found', 404)
