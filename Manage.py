
import os
from threading import Thread

from Billboard import DataBase as db
from Billboard import app
from Billboard.Jobs.jobs import Schedule
from Test import make_instances

from flask_script import Manager, prompt_bool


manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    make_instances()
    print ('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()
        print ('Dropped the database')


@manager.command
def run():

    app.secret_key = os.urandom(12)
    t = Thread(target=Schedule.run_schedule)
    t.daemon = True
    t.start()
    app.run(debug = True, host='0.0.0.0')


if __name__ == '__main__':
    manager.run()
