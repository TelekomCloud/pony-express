from flask import Blueprint, request, Response, json
from ponyexpress.api.exceptions import *

from ponyexpress.api.lib.repositories import Repositories

updater = Blueprint('updater', __name__)


@updater.route('/v1/updater')
def default():
    raise InvalidAPIUsage('Invalid request method', status_code=400)


@updater.route('/v1/updater', methods=['POST'])
def repository_update():
    """Update metadata of a set of repositories."""

    # Safeguard
    if request.method == 'POST':
        request_json = request.get_json()

        repo = None
        label = None

        if request_json is not None:
            repo = request_json.get('repolist')
            label = request_json.get('repolabel')

        # Repository api lib
        handler = Repositories()

        if repo is not None and label is None:
            repo_list = handler.get_repositories(repo)
        elif label is not None and repo is None:
            repo_list = handler.get_repositories_by_label(label)
        else:
            repo_list = handler.get_all_repositories()

        # Return list of updated repositories
        resp = []

        if repo_list is not None:
            for repo in repo_list:
                handler.select_provider(repo)
                ret = handler.update_repository(repo)

                if ret is not None and ret > 0:
                    resp.append(repo.name)

            return Response(json.dumps({'repositories': resp}), status=200, mimetype='application/json')
        else:
            raise InvalidAPIUsage('No repositories configured', status_code=400)

    else:
        raise InvalidAPIUsage('Invalid request method', status_code=400)

