""" the management """
import csv
import subprocess
from flask.cli import FlaskGroup
from flask import current_app
from project import db, create_app, Film, Genre, User, Director

app = create_app()
cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    """ create db  """
    with current_app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()

def seed_from_file_decorator(function):
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        with open(result[0], "r") as f:
            data = list(csv.reader(f, delimiter=","))
        is_created = result[2].query.first()
        if not is_created:
            for item in data:
                if result[2] is Film:
                    genres = item[-1].split('_')
                    item = item[0:-1]
                    values = dict(zip(result[1], item))
                    object_in = result[2](**values)

                    for i in genres:
                        genre = Genre.query.where(Genre.name == i).first()
                        if genre is not None:
                            object_in.genres.append(genre)
                else:
                    values = dict(zip(result[1], item))
                    object_in = result[2](**values)
                if 'is_admin' in result[1]:
                    object_in.is_admin = bool(values['is_admin'])
                db.session.add(object_in)
                db.session.commit()
        return result
    return wrapper


@seed_from_file_decorator
def seed_from_file(file, table):
    if table == 'Users':
        return file, User.__table__.columns.keys(), User
    if table == 'Directors':
        return file, Director.__table__.columns.keys(), Director
    if table == 'Genres':
        return file, Genre.__table__.columns.keys(), Genre
    if table == 'Films':
        return file, Film.__table__.columns.keys(), Film


@cli.command("seed")
def seed():
    print("the seed command")
    with app.app_context():

        subprocess.run(["flask", "db", "init"])
        subprocess.run(["flask", "db", "upgrade"])
        subprocess.run(["flask", "db", "migrate"])
        subprocess.run(["flask", "db", "upgrade"])
        seed_from_file("./project/static/seed/directors_mock.csv", 'Directors')
        seed_from_file("./project/static/seed/users_mock.csv", 'Users')
        seed_from_file("./project/static/seed/genres_mock.csv", 'Genres')
        seed_from_file("./project/static/seed/films_mock.csv", 'Films')


if __name__ == "__main__":
    cli()
