# manage.py
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from ponyexpress import *
from ponyexpress.database import db

app = create_app()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def createdb():
    with app.app_context():
        db.create_all(app=app)

if __name__ == "__main__":
    manager.run()
