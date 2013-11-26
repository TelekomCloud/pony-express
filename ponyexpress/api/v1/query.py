from flask import Blueprint, request, Response, json
from ponyexpress.models.package import Package
from ponyexpress.models.node import Node
from ponyexpress.api.exceptions import *

query = Blueprint('query', __name__)


def hypermedia_headers(uri, page, paginator):
    #add pagination headers
    link = []

    if paginator.has_next:
        url = '<http://%s?page=%s&limit=%s>; rel="next"' % (uri, paginator.next_num, paginator.per_page)
        link.append(url)

    if paginator.has_prev:
        url = '<http://%s?page=%s&limit=%s>; rel="prev"' % (uri, paginator.prev_num, paginator.per_page)
        link.append(url)

    if page < paginator.pages:
        url = '<http://%s?page=%s&limit=%s>; rel="last"' % (uri, paginator.pages, paginator.per_page)
        link.append(url)

    if page > 1 and paginator.pages > 1:
        url = '<http://%s?page=%s&limit=%s>; rel="first"' % (uri, 1, paginator.per_page)
        link.append(url)

    headers = {
        'Link': ','.join(link)
    }

    return headers


@query.route('/v1/nodes', methods=['GET'])
def nodes():
    result = []

    limit = request.args.get('limit', 10)
    page = request.args.get('page', 1)

    if (10 <= limit <= 50) and page >= 1:
        #queried_nodes = Node.query.limit(limit).offset(offset)
        paginator = Node.query.paginate(page=page, per_page=limit, error_out=False)
    else:
        raise InvalidAPIUsage('Invalid request', 410)

    if paginator:
        for n in paginator.items:
            res = {
                'id': n.name,
                'packages': [],
            }
            result.append(res)

        headers = hypermedia_headers('localhost/v1/nodes', page, paginator)

        return Response(json.dumps(result), mimetype='application/json',headers=headers)


@query.route('/v1/node/<fqdn>', methods=['GET'])
def node(fqdn):
    full = request.args.get('full', True)

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
def packages():
    result = []

    limit = int(request.args.get('limit', 10))
    page = int(request.args.get('page', 1))

    if (10 <= limit <= 50) and page >= 1:
        paginator = Package.query.paginate(page=page, per_page=limit, error_out=False)
    else:
        raise InvalidAPIUsage('Invalid request', 410)

    if paginator.items:
        for p in paginator.items:
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

        #add pagination headers
        headers = hypermedia_headers('packages', page, paginator)

        return Response(json.dumps(result), mimetype='application/json', headers=headers)


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
