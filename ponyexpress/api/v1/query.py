from flask import Blueprint, request, Response, json
from ponyexpress.api.lib.repositories import Repositories

from ponyexpress.models import Repository, Package, PackageHistory, Node

from ponyexpress.api.exceptions import *

from ponyexpress.api.lib.helpers import Pagination

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

    limit = int(request.args.get('limit', 100))
    page = int(request.args.get('page', 1))

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

    paginator = None

    limit = int(request.args.get('limit', 100))
    page = int(request.args.get('page', 1))

    filter = str(request.args.get('filter', ''))

    outdated = str(request.args.get('outdated', ''))
    repo = str(request.args.get('repo', ''))
    label = str(request.args.get('repolabel', ''))

    if outdated == '':
        if (10 <= limit <= 100) and page >= 1:

            if filter is not None:
                filter_string = ('%%%s%%' % filter)
                paginator = Package.query.filter(Node.name.like(filter_string)).order_by(Package.name).order_by(
                    Package.version).paginate(page=page, per_page=limit,
                                              error_out=False)
            else:
                paginator = Package.query.order_by(Package.name).order_by(Package.version).paginate(page=page,
                                                                                                    per_page=limit,
                                                                                                    error_out=False)
    elif outdated != '' and (repo != '' or label != ''):
        # Repository api lib
        handler = Repositories()

        # Get selected repositories
        if repo != '' and label == '':
            repo_list = handler.get_repositories(repo)
        elif label != '' and repo == '':
            repo_list = handler.get_repositories_by_label(label)
        else:
            raise InvalidAPIUsage('Invalid request', 410)

        nodes_filter = ''
        if filter != '':
            nodes_filter = ('%%%s%%' % filter)

        if repo_list:
            outdated_packages = handler.get_outdated_packages(nodes_filter, repo_list)

            length = len(outdated_packages)
            paginator = Pagination(page=page, per_page=limit, total_count=length)
            paginator.items = outdated_packages
        else:
            paginator = None
    else:
        raise InvalidAPIUsage('Invalid request', 410)

    if paginator:
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
                    'upstream': p.upstream_version
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


@query.route('/v1/repositories', methods=['GET', 'POST'])
def repositories():
    if request.method == 'GET':
        return repository_get()
    elif request.method == 'POST':
        return repository_post()


def repository_get():
    result = []

    limit = int(request.args.get('limit', 100))
    page = int(request.args.get('page', 1))

    if (10 <= limit <= 100) and page >= 1:
        #queried_nodes = Node.query.limit(limit).offset(offset)
        paginator = Repository.query.paginate(page=page, per_page=limit, error_out=False)
    else:
        raise InvalidAPIUsage('Invalid request', 410)

    if paginator:
        for n in paginator.items:
            c = {
                'id': n.id,
                'name': n.name,
                'uri': n.uri,
                'label': n.label,
                'provider': n.provider
            }
            result.append(c)

        headers = hypermedia_headers(request.base_url, page, paginator)

        return Response(json.dumps(result), mimetype='application/json', headers=headers)
    else:
        raise InvalidAPIUsage('Invalid request', 410)


def repository_post():
    handler = Repositories()

    # validation
    j = request.get_json()
    if j['uri'] is None:
        raise InvalidAPIUsage('You must provide a URI when creating a new repository.', 404)

    # fill data with all the fields necessary for creating a repository entry
    data = {}
    data['name'] = str(j['name'])
    data['label'] = str(j['label'])
    data['uri'] = str(j['uri'])
    data['provider'] = str(j['provider'])

    # create new new repository
    try:
        id = handler.create_repository(data)

        # add the newly created id to the data to be returned
        data['id'] = id

        # return the object
        return Response(json.dumps(data), status=201, mimetype='application/json')
    except:
        raise InvalidAPIUsage('Failed to create new repository', 404)


@query.route('/v1/repositories/<id>', methods=['PATCH', 'DELETE'])
def repository_by_id(id):
    if request.method == 'PATCH':
        return repository_update(id)
    elif request.method == 'DELETE':
        return repository_delete(id)


def repository_update(id):
    if id != '':
        repo = Repository.query.filter_by(id=id).first()
    else:
        raise InvalidAPIUsage('Invalid API usage', 410)

    if repo:
        # update all known fields
        repodata = request.get_json()
        handler = Repositories()
        handler.update_repository_info(repo, repodata)

        # extract the result for the response
        result = {'id': repo.id, 'name': repo.name, 'uri': repo.uri, 'label': repo.label,
                  'provider': repo.provider
        }

        return Response(json.dumps(result), mimetype='application/json')
    else:
        raise InvalidAPIUsage('Repository not found', 404)


def repository_delete(id):
    if id != '':
        repo = Repository.query.filter_by(id=id).first()
    else:
        raise InvalidAPIUsage('Invalid API usage', 410)

    if repo:
        id = repo.id
        # remove the repo
        handler = Repositories()
        handler.delete_repository(repo)

        # return
        return Response('', status=204, mimetype='application/json')
    else:
        raise InvalidAPIUsage('Repository not found', 404)
