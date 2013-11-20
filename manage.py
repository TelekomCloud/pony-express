# manage.py
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from ponyexpress import app
from ponyexpress import db


manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    """Creates the necessary tables in the database
    specified in the `DB_PATH` config variable."""

    print "Initializing budget tables ..."
    db.metadata.create_all(db.engine)

# sample command
@manager.command
def hello():
    print "hello"

if __name__ == "__main__":
    manager.run()
