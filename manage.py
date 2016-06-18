from flask.ext.script import Manager

from app.beep import app

manager = Manager(app)

@manager.command
def createdb():
    from models import db
    db.create_all()

if __name__ == "__main__":
    createdb()