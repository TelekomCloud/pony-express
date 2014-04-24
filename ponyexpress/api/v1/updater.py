from flask import Blueprint, request, Response
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
        repo = ''
        label = ''

        request_json = request.get_json()

        if request_json is not None:
            repo = request_json.get('repolist')
            label = request_json.get('repolabel')
        else:
            raise InvalidAPIUsage('No JSON data', 410)

        # Repository api lib
        handler = Repositories()

        if repo is not None and label is None:
            repo_list = handler.get_repositories(repo)
        elif label is not None and repo is None:
            repo_list = handler.get_repositories_by_label(label)
        else:
            raise InvalidAPIUsage('Invalid request', 410)

        if repo_list is not None:
            for repo in repo_list:
                handler.select_provider(repo)
                handler.update_repository(repo)
        else:
            print('NO REPOS')

        #TODO: return node object?
        return Response(status=200)
    else:
        raise InvalidAPIUsage('Invalid request method', status_code=400)

