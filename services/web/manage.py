""" the management """
from flask.cli import FlaskGroup
from flask import current_app
from project import db, create_app

app = create_app()
cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    """ create db  """
    print("trying to set up")
    with current_app.app_context():
        print("set up proces")
        db.drop_all()
        db.create_all()
        db.session.commit()


if __name__ == "__main__":
    cli()
