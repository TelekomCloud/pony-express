from flask import Blueprint, abort
from ponyexpress.api.exceptions import *

collector = Blueprint('collector', __name__)

@collector.route('/v1/collector')
def dataimport():
    #

    #recieve put/post data and parse the json data structure
    #create or update the node and package information in the database
    #

    #return json

    raise InvalidAPIUsage('This view is gone', status_code=410)

    #try:
    #    return ''
    #except Exception, e:
    #    raise InvalidUsage('This view is gone', status_code=410)
