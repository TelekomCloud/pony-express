from flask import Blueprint, abort
from ponyexpress.api.exceptions import *

from ponyexpress.database import db
from ponyexpress.models.package import Package
from ponyexpress.models.node import Node

collector = Blueprint('collector', __name__)

@collector.route('/v1/collector')
def dataimport():
    #

    #recieve put/post data and parse the json data structure
    #create or update the node and package information in the database

    node = Node('foo.bar.baz')

    db.session.add(node)
    db.session.commit()

    #return json

    raise InvalidAPIUsage('This view is gone', status_code=410)

    #try:
    #    return ''
    #except Exception, e:
    #    raise InvalidUsage('This view is gone', status_code=410)
