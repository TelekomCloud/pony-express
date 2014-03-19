from flask import Blueprint, request, Response
from ponyexpress.api.exceptions import *

from ponyexpress.api.lib.package_import import PackageImport

collector = Blueprint('collector', __name__)

@collector.route('/v1/collector')
def default():
    raise InvalidAPIUsage('Invalid request method', status_code=400)

@collector.route('/v1/collector', methods=['POST', 'PUT'])
def dataimport():
    """Import json formated package information from a node.
    Store this information into a database for later querying
    """

    # Safeguard
    if request.method == 'PUT' or request.method == 'POST':

        request_json = request.get_json()

        importer = PackageImport()
        importer.process_node_info(request_json)

        #TODO: return node object?
        return Response(status=200)
    else:
        raise InvalidAPIUsage('Invalid request method', status_code=400)
