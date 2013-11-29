from flask import Blueprint, request, Response, json
from ponyexpress.models.package import Package
from ponyexpress.models.node import Node
from ponyexpress.api.exceptions import *

query = Blueprint('query', __name__)


def hypermedia_headers(uri, page, paginator):
    #add pagination headers
    link = []

    if paginator.has_next:
        url = '<%s?page=%s&limit=%s>; rel="next"' % (uri, paginator.next_num, paginator.per_page)
        link.append(url)

    if paginator.has_prev:
        url = '<%s?page=%s&limit=%s>; rel="prev"' % (uri, paginator.prev_num, paginator.per_page)
        link.append(url)

    if page < paginator.pages:
        url = '<%s?page=%s&limit=%s>; rel="last"' % (uri, paginator.pages, paginator.per_page)
        link.append(url)

    if page > 1 and paginator.pages > 1:
        url = '<%s?page=%s&limit=%s>; rel="first"' % (uri, 1, paginator.per_page)
        link.append(url)

    headers = {
        'Link': ','.join(link)
    }

    return headers


@query.route('/v1/nodes', methods=['GET'])
def nodes():
    result = []

    limit = request.args.get('limit', 100)
    page = request.args.get('page', 1)

    if (10 <= limit <= 100) and page >= 1:
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

        headers = hypermedia_headers(request.base_url, page, paginator)

        return Response(json.dumps(result), mimetype='application/json', headers=headers)
    else:
        raise InvalidAPIUsage('Invalid request', 410)


@query.route('/v1/node/<fqdn>', methods=['GET'])
def node(fqdn):
    if fqdn != '':
        q_node = Node.query.filter_by(name=fqdn).first()

        if q_node:
            r_node = {
                'id': q_node.name,
                'packages': []
            }

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

    limit = int(request.args.get('limit', 100))
    page = int(request.args.get('page', 1))

    if (10 <= limit <= 100) and page >= 1:
        paginator = Package.query.order_by(Package.name).order_by(Package.version).paginate(page=page, per_page=limit,
                                                                                            error_out=False)
    else:
        raise InvalidAPIUsage('Invalid request', 410)

    if paginator.items:
        for p in paginator.items:
            l = len(result)
            index = ((l - 1), 0)[0 > (l - 1)]

            if l > 0 and result[index]['name'] == p.name:
                r = result[index]
                ver = {'version': p.version, 'id': p.sha}
                r['versions'].append(ver)
            else:
                r_p = {
                    'name': p.name,
                    'versions': [],
                    'summary': p.summary,
                    'uri': p.uri,
                    'provider': p.provider,
                    'architecture': p.architecture,
                }
                ver = {'version': p.version, 'id': p.sha}
                r_p['versions'].append(ver)

                result.append(r_p)

        #add pagination headers
        headers = hypermedia_headers(request.base_url, page, paginator)

        return Response(json.dumps(result), mimetype='application/json', headers=headers)
    else:
        raise InvalidAPIUsage('Invalid API usage', 410)


@query.route('/v1/package/<id>', methods=['GET'])
def package(id):
    if id != '':
        package = Package.query.filter_by(sha=id).first()
    else:
        raise InvalidAPIUsage('Invalid API usage', 410)

    if package:
        result = {'id': package.sha, 'name': package.name, 'version': package.version, 'summary': package.summary,
                  'uri': package.uri, 'provider': package.provider, 'architecture': package.architecture,
                  'nodes': []}

        for n in package.nodes:
            result['nodes'].append({'id': n.name})

        return Response(json.dumps(result), mimetype='application/json')
    else:
        raise InvalidAPIUsage('Package not found', 404)
