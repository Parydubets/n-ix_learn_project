from sqlalchemy import create_engine, Column, Integer, Numeric, String, Date, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, mapped_column
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

film_genre = db.Table('film_genre',
    db.Column('film_id', db.Integer, db.ForeignKey('films.film_id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.genre_id'))
)

class Genre(db.Model):
    __tablename__ = "genres"

    genre_id    = db.Column(Integer, primary_key=True)
    name        = db.Column(String, nullable=False)


class Director(db.Model):
    __tablename__ = "directors"

    director_id     = Column(Integer, primary_key=True)
    first_name      = Column(String, nullable=False)
    last_name       = Column(String, nullable=False)
    date_of_birth   = Column(Date, nullable=False)
    films = db.relationship('Film', backref='director')


class User(db.Model):
    __tablename__ = "users"

    user_id     = Column(Integer, primary_key=True)
    first_name  = Column(String, nullable=False)
    last_name   = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    email       = Column(String, nullable=False)
    password    = Column(String, nullable=False)
    phone       = Column(String, nullable=False)
    is_admin    = Column(Boolean, nullable=False)
    films = db.relationship('Film', backref='user')


class Film(db.Model):
    __tablename__ = "films"

    film_id         = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)
    release_date    = Column(Date, nullable=False)
    description     = Column(String, nullable=True)
    rating          = Column(Numeric, nullable=False)
    poster          = Column(String, nullable=False)
    users_user_id   = mapped_column(ForeignKey("users.user_id"))
    directors_director_id   = mapped_column(ForeignKey("directors.director_id"))
    genres = db.relationship("Genre", secondary=film_genre)
