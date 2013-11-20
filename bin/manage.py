# manage.py
from flask.ext.script import Manager

from ponyexpress import app

manager = Manager(app)

# sample command
@manager.command
def hello():
    print "hello"

if __name__ == "__main__":
    manager.run()
