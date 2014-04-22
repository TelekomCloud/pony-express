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
        repo = str(request.args.get('repo', ''))
        label = str(request.args.get('repolabel', ''))

        # Repository api lib
        handler = Repositories()

        if repo != '' and label == '':
            repo_list = handler.get_repositories(repo)
        elif label != '' and repo :
            repo_list = handler.get_repositories_by_label(label)
        else:
            raise InvalidAPIUsage('Invalid request', 410)

        if repo_list is not None:
            for repo in repo_list:
                handler.update_repository(repo)

        #TODO: return node object?
        return Response(status=200)
    else:
        raise InvalidAPIUsage('Invalid request method', status_code=400)

